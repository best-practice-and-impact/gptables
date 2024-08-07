import os
import re
import warnings
import pandas as pd
import numpy as np
from copy import deepcopy

from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet

from gptables.core.cover import Cover

from .theme import Theme
from .gptable import GPTable, FormatList
from gptables.utils.unpickle_themes import gptheme


class GPWorksheet(Worksheet):
    """
    Wrapper for an XlsxWriter Worksheet object. Provides a method for writing
    a good practice table (GPTable) to a Worksheet.
    """
    def write_cover(self, cover):
        """
        Write a cover page to the Worksheet. Uses text from a Cover object and
        details of the Workbook contents.

        Parameters
        ----------
        cover : gptables.Cover
            object containing cover sheet text
        """
        theme = self.theme
        pos = [0, 0]

        self._parse_urls(cover)

        pos = self._write_element(pos, cover.title, theme.cover_title_format)

        if cover.intro is not None:
            pos = self._write_element(pos, "Introductory information", theme.cover_subtitle_format)
            pos = self._write_element_list(pos, cover.intro, theme.cover_text_format)

        if cover.about is not None:
            pos = self._write_element(pos, "About these data", theme.cover_subtitle_format)
            pos = self._write_element_list(pos, cover.about, theme.cover_text_format)

        if cover.contact is not None:
            pos = self._write_element(pos, "Contact", theme.cover_subtitle_format)
            pos = self._write_element_list(pos, cover.contact, theme.cover_text_format)
                  
        self.set_column(0, 0, cover.width)

    def write_gptable(self, gptable, auto_width, reference_order=[]):
        """
        Write data from a GPTable object to the worksheet using the workbook
        Theme object for formatting.
        
        Parameters
        ----------
        gptable : gptables.GPTable
            object containing elements of the gptable to be written to the
            Worksheet
        reference_order : list, optional
            order of annotations in workbook
            must be provided if gptable uses annotations
        Returns
        -------
        None
        """
        if not isinstance(gptable, GPTable):
            raise TypeError("`gptable` must be a gptables.GPTable object")
        
        if len(gptable._annotations)>0 and len(reference_order)==0:
            msg = "reference_order must be provided if gptable contains annotations"
            raise ValueError(msg)
        
        theme = self.theme

        # Write each GPTable element using appropriate Theme attr
        pos = [0, 0]

        self._reference_annotations(gptable, reference_order)
        self._parse_urls(gptable)

        gptable = deepcopy(gptable)

        pos = self._write_element(
                pos,
                gptable.title,
                theme.title_format
                )

        pos = self._write_element_list(
                pos,
                gptable.subtitles,
                theme.subtitle_format
                )

        description = theme.description_order
        for element in description:
            pos = getattr(self, "_write_" + element)(
                    pos,
                    getattr(gptable, element),
                    getattr(theme, element + "_format")
                    )

        pos = self._write_table_elements(
                pos,
                gptable,
                auto_width,
                )


    def _reference_annotations(self, gptable, reference_order):
        """
        Replace note references with numbered references and move to end of element.
        Acts on `title`, `subtitles`, `table` and `notes` attributes of a GPTable.
        References are numbered from top left of spreadsheet, working across each row.
        
        Parameters
        ----------
        gptable : gptables.GPTable
            object containing data with references to notes
        reference_order : list
            order of annotations in workbook

        Returns
        -------
        None
        """
        description_order = self.theme.description_order

        elements = [
                "title",
                "subtitles",
                *description_order,
                ]

        # Loop through elements, replacing references in strings
        for attr in elements:
            attr_current = getattr(gptable, attr)
            setattr(
                    gptable,
                    attr,
                    self._replace_reference_in_attr(
                            attr_current,
                            reference_order
                            )
                    )
        self._reference_table_annotations(gptable, reference_order)


    def _reference_table_annotations(self, gptable, reference_order):
        """
        Reference annotations in the table column headings and index columns.
        """
        table = getattr(gptable, "table")
        
        table.columns = self._replace_reference_in_attr(
                [x for x in table.columns],
                reference_order
                )
        
        index_columns = gptable.index_columns.values()

        for col in index_columns:
            table.iloc[:, col] = table.iloc[:, col].apply(
                    lambda x: self._replace_reference_in_attr(x, reference_order)
                    )

        setattr(gptable, "table", table)


    def _replace_reference_in_attr(self, data, reference_order):
        """
        Replaces references in a string or list/dict of strings. Works
        recursively on list elements and dict values. Other types are returned
        without modification.
        
        Parameters
        ----------
        data : any type
            object containing strings to replace references in
        reference_order : list
            order of annotations in workbook

        Returns
        -------
        string : str
            input string with references replaced with numerical reference (n),
            where n is the order of appearance in the resulting document
        """
        if isinstance(data, str):
            data = self._replace_reference(data, reference_order)
        if isinstance(data, list):
            for n in range(len(data)):
                data[n] = self._replace_reference_in_attr(
                        data[n],
                        reference_order
                        )
        if isinstance(data, dict):
            for key in data.keys():
                data[key] = self._replace_reference_in_attr(
                        data[key],
                        reference_order
                        )
        if isinstance(data, FormatList):
            data_list = data.list
            for n in range(len(data_list)):
                data_list[n] = self._replace_reference_in_attr(
                        data_list[n],
                        reference_order
                        )
            data = FormatList(data_list)

        return data
    

    @staticmethod
    def _replace_reference(string, reference_order):
        """
        Given a single string, record occurrences of new references (denoted by
        flanking dollar signs [$$reference$$]) and replace with number
        reference reflecting order of detection.
        
        Parameters
        ----------
        string : str
            the string to replace references within
        reference_order : list
            order of annotations in workbook

        Returns
        -------
        string : str
            input string with references replaced with numerical reference (n),
            where n is the order of appearence in the resulting document
        """
        text_refs = re.findall(r"[$]{2}.*?[$]{2}", string)
        dict_refs = [w.replace("$", "") for w in text_refs]
        for n in range(len(dict_refs)):
            num_ref = "[note " + str(reference_order.index(dict_refs[n]) + 1) + "]"
            string = string.replace(text_refs[n], "") + num_ref

        return string


    def _parse_urls(self, sheet):
        """
        Convert markdown URL formatting into URL, string tuple
        
        Parameters
        ----------
        sheet : gptables.GPTable, gptables.Cover
            object containing data with urls        
        """
        if isinstance(sheet, GPTable):
            elements = [
                "title",
                "subtitles",
                "legend",
                "source",
                "scope",
                "units",
                ]
        elif isinstance(sheet, Cover):
            elements = [
                "title",
                "intro",
                "about",
                "contact",
            ]

        # Loop through elements, replacing urls in strings
        for attr in elements:
            attr_current = getattr(sheet, attr)
            setattr(
                    sheet,
                    attr,
                    self._replace_url_in_attr(
                            attr_current,
                            )
                    )
        if isinstance(sheet, GPTable):
            self._parse_table_urls(sheet)
    
    def _parse_table_urls(self, gptable):
        """
        Parse URLs in table.
        """
        table = getattr(gptable, "table")
        rows, columns = table.shape

        for c in range(columns):
            for r in range(rows):
                cell = self._replace_url_in_attr(table.iloc[r, c])
                if isinstance(cell, dict):
                    table.iloc[r, c] = [cell]
                else:
                    table.iloc[r, c] = cell

        setattr(gptable, "table", table)
    
    def _replace_url_in_attr(self, data):
        """
        Replaces urls in a string or list/dict of strings. Works
        recursively on list elements and dict values. Other types
        are returned without modification.
        
        Parameters
        ----------
        data : any type
            object containing strings to replace references in
        """
        if isinstance(data, str):
            data = self._replace_url(data)
        if isinstance(data, list):
            for n in range(len(data)):
                data[n] = self._replace_url_in_attr(
                        data[n],
                        )
        if isinstance(data, dict):
            for key in data.keys():
                data[key] = self._replace_url_in_attr(
                        data[key],
                        )

        return data


    @staticmethod
    def _replace_url(string):
        """
        Given a single string, record occurrences of markdown 
        style urls (formatted as `"[url](display_text)"`) and 
        replace with tuples of `(url, string)`
        
        Parameters
        ----------
        string : str
            the string to replace references within

        Returns
        -------
        string or dict
            if no markdown style urls found, returns sting
            if found, return dictionary with key `string` and value `url`,
            where markdown style url in `string` is replaced with `display_text`            
        """
        f_url_pattern = r"\[.+\]\(.+\)" # "[display_text](url)"
        f_urls = re.findall(f_url_pattern, string)
        
        if len(f_urls) == 0:
            return string
        
        if len(f_urls) > 1:
            msg = "More than one link found in cell. Excel only permits one link per cell"
            raise ValueError(msg)
        else:
            f_url = f_urls[0]

            url = re.split(r"\(", f_url)[1].replace(")", "")
            display_text = re.split(r"\]", f_url)[0].replace("[", "")

            string = re.sub(f_url_pattern, display_text, string)

            return {string: url}


    def _write_element(self, pos, element, format_dict):
        """
        Write a single text element of a GPTable to the GPWorksheet.
        
        Parameters
        ----------
        element : str or list
            the string or list of rich string elements to be written
        format_dict : dict
            format to be applied to string
        pos : list
            the position of the worksheet cell to write the element to

        Returns
        -------
        pos : list
            new position to write next element from
        """
        if element:
            self._smart_write(*pos, element, format_dict)
            pos[0] += 1
        
        return pos       


    def _write_element_list(self, pos, element_list, format_dict):
        """
        Writes a list of elements row-wise.
        
        Parameters
        ----------
        element_list : list
            list of strings or nested list of rich string elements to write,
            one per row
        format_dict : dict
            format to be applied to string
        pos : list
            the position of the worksheet cell to write the elements to

        Returns
        -------
        pos: list
            new position to write next element from
        """
        if element_list:
            for element in element_list:
                pos = self._write_element(pos, element, format_dict)
        
        return pos


    def _write_instructions(self, pos, element, format_dict):
        """
        Alias for writting description elements by name.
        """
        return self._write_element(pos, element, format_dict)


    def _write_source(self, pos, element, format_dict):
        """
        Alias for writting description elements by name.
        """
        return self._write_element(pos, element, format_dict)

    
    def _write_scope(self, pos, element, format_dict):
        """
        Alias for writting description elements by name.
        """
        return self._write_element(pos, element, format_dict)


    def _write_legend(self, pos, element_list, format_dict):
        """
        Alias for writting description elements by name.
        """
        return self._write_element_list(pos, element_list, format_dict)


    def _write_notes(self, pos, element_list, format_dict):
        """
        Alias for writting description elements by name.
        """
        return self._write_element_list(pos, element_list, format_dict)


    def _write_table_elements(self, pos, gptable, auto_width):
        """
        Writes the table and units elements of a GPTable. Uses the
        Workbook Theme, plus any additional formatting associated with the
        GPTable.
        
        Parameters
        ----------
        gptable : gptables.GPTable
            object containing the table and additional formatting data
        pos : list
            the position of the worksheet cell to write the units to
        auto_width : bool
            select if column widths should be determined automatically using
            length of text in index and columns

        Returns
        -------
        pos : list
            new position to write next element from
        """
        # Convert whitespace only cells to None
        gptable.table.replace({r'^\s*$': None}, inplace=True, regex=True)

        if gptable.table.isna().values.all():
            msg = (f"""
            {gptable.table_name} contains only null or whitespace cells.
            Please provide alternative table containing data.
            """)
            raise ValueError(msg)

        if gptable.table.isna().all(axis=1).any():
            msg = (f"""
            Empty or null row found in {gptable.table_name}.
            Please remove blank rows before passing data to GPTable.
            """)
            raise ValueError(msg)

        if gptable.table.isna().values.any():
            msg = (f"""
            Empty or null cell found in {gptable.table_name}. The reason for
            missingness should be included in the `GPTable.instructions` attribute.
            There should only be one reason otherwise a shorthand should be
            provided in the `instructions` or `legend` attribute.
            Guidance on shorthand can be found at:
            https://analysisfunction.civilservice.gov.uk/policy-store/symbols-in-tables-definitions-and-help/
            """)
            warnings.warn(msg)

        # Raise error if any table element is only special characters
        if gptable.table.astype("string").stack().str.contains('^[^a-zA-Z0-9]*$').any():
            msg = (f"""
            Cell found in {gptable.table_name} containing only special characters,
            replace with alphanumeric characters before inputting to GPTable.
            Guidance on symbols in tables can be found at:
            https://analysisfunction.civilservice.gov.uk/policy-store/symbols-in-tables-definitions-and-help/
            """)
            raise ValueError(msg)

        # Get theme
        theme = self.theme
                
        # Reset position to left col on next row
        pos[1] = 0
        
        ## Create data array
        index_levels = gptable.index_levels
        index_columns = [col for col in gptable.index_columns.values()]
        data = pd.DataFrame(gptable.table, copy=True)
            
        # Create row containing column headings
        data.loc[-1] = data.columns
        data.index = data.index + 1
        data.sort_index(inplace=True)
        
        ## Create formats array
        # pandas.DataFrame did NOT want to hold dictionaries, so be wary
        formats = pd.DataFrame().reindex_like(data)
        dict_row = [{} for n in range(formats.shape[1])]
        for row in range(formats.shape[0]):
            dict_row = [{} for n in range(formats.shape[1])]
            formats.iloc[row] = dict_row
        
        ## Add Theme formatting to formats dataframe
        format_headings_from = 0
        self._apply_format(
                formats.iloc[0, format_headings_from:],
                theme.column_heading_format
                )
        
        self._apply_format(
                formats.iloc[1:, index_levels:],
                theme.data_format
                )
        
        index_level_formats = [
                theme.index_1_format,
                theme.index_2_format,
                theme.index_3_format
                ]
        for level, col in gptable.index_columns.items():
            self._apply_format(
                formats.iloc[1:, col],
                index_level_formats[level - 1]  # Account for 0-indexing
                )

        self._apply_column_alignments(data, formats, index_columns)

        ## Add additional table-specific formatting from GPTable
        self._apply_additional_formatting(
                formats,
                gptable.additional_formatting,
                gptable.index_levels
                )
        
        ## Write table
        pos = self._write_array(pos, data, formats)

        ## Set columns widths
        if auto_width:
            widths = self._calculate_column_widths(data, formats)
            self._set_column_widths(widths)

        self._mark_data_as_worksheet_table(gptable, formats)
        
        return pos


    def _apply_column_alignments(self, data_table, formats_table, index_columns):
        """
        Add column alignment to format based on datatype

        Parameters
        ----------
        data_table : pandas.DataFrame
            table to be written to an Excel workbook
        formats_table : pandas.DataFrame
            table with same dimensions as `data_table`,
            containing formating dictionaries

        """
        # look for shorthand notation, usually a few letters in square brackets
        # will also find note markers eg [Note 1]
        # Using np.nan instead on None for backwards compatibility with pandas <=1.4
        data_table_copy = data_table.replace(
            regex=r"\[[\w\s]+\]",
            value = np.nan,
        )

        data_table_copy = data_table_copy.convert_dtypes()

        column_types = data_table_copy.dtypes

        for column in data_table.columns:
            if data_table.columns.get_loc(column) in index_columns:
                alignment_dict = {"align": "left"}

            elif pd.api.types.is_numeric_dtype(column_types[column]):
                alignment_dict = {"align" : "right"}

            else:
                alignment_dict = {"align": "left"}

            self._apply_format(formats_table[column], alignment_dict)


    def _apply_additional_formatting(
            self,
            formats_table,
            additional_formatting,
            index_levels
            ):
        """
        Apply row, column and cell formatting to dataframe of formats.
        """
        for item in additional_formatting:
            fmt_type = list(item.keys())[0]
            format_desc = item[fmt_type]
            
            if fmt_type == "cell":
                formatting = format_desc["format"]
                cell_ilocs = format_desc["cells"]
                if isinstance(cell_ilocs, tuple):
                    cell_ilocs = [cell_ilocs]
                for row, col in cell_ilocs:
                    formats_table_slice = formats_table.iloc[row, col]
                    
                    self._apply_format(
                        formats_table_slice,
                        formatting
                        )
                return None
            
            if fmt_type == "column":
                cols_iloc = [
                        formats_table.columns.get_loc(col)
                        if isinstance(col, str)
                        else col
                        for col in format_desc["columns"]
                        ]
                row_start = 0
                if "include_names" in format_desc.keys():
                    row_start = 0 if format_desc["include_names"] else 1
    
                formats_table_slice = formats_table.iloc[row_start:, cols_iloc]
                formatting = format_desc["format"]

            elif fmt_type == "row":
                rows_iloc = format_desc["rows"]
                col_start = 0
                if "include_names" in format_desc.keys():
                    col_start = 0 if format_desc["include_names"] else index_levels
    
                formats_table_slice = formats_table.iloc[rows_iloc, col_start:]
                formatting = format_desc["format"]
            
            self._apply_format(
                formats_table_slice,
                formatting
                )


    def _write_array(self, pos, data, formats):
        """
        Write a two-dimensional array to the current Worksheet, starting from
        the specified position.
        
        Parameters
        ----------
        data : pandas.DataFrame
            array of data to be written to Worksheet
        formats : pandas.DataFrame
            array of dictionaries that specify the formatting to be applied
            to each cell of data
        pos : list
            the position of the top left cell to start writing the array from
            
        Returns
        -------
        pos : list
            new position to write next element from
        """
        if data.shape != formats.shape:
            raise ValueError("data and formats arrays must be of equal shape")
        
        rows, cols = data.shape
        for row in range(rows):
            for col in range(cols):
                cell_data = data.iloc[row, col]
                cell_format_dict = formats.iloc[row, col]

                self._smart_write(
                    pos[0] + row,
                    pos[1] + col,
                    cell_data,
                    cell_format_dict
                    )
        
        pos = [pos[0] + rows, 0]
        
        return pos


    def _mark_data_as_worksheet_table(self, gptable, formats_dataframe):
        """
        Marks the data to be recognised as a Worksheet Table in Excel.

        Parameters
        ----------
        gptable : gptables.GPTable
            object containing the table
        formats_dataframe : DataFrame
            DataFrame with same dimensions as gptable.table, containing
            formatting dictionaries
        """
        data_range = gptable.data_range

        column_list = gptable.table.columns.tolist()
        formats_list = [
            self._workbook.add_format(format_dict)
            for format_dict in formats_dataframe.iloc[0, :].tolist()
        ]

        column_headers = [
            {'header': header, 'header_format': header_format}
            for header, header_format in zip(column_list, formats_list)
        ]

        self.add_table(*data_range,
                       {'header_row': True,
                        'autofilter': False,
                        'columns': column_headers,
                        'style': None,
                        'name': gptable.table_name
                        })


    def _smart_write(self, row, col, data, format_dict, *args):
        """
        Depending on the input data, this function will write rich strings or
        use the standard `write()` method. For rich strings, the base format is
        merged with each rich format supplied within data.
        
        Parameters
        ----------
        row : int
            0-indexed row of cell to write to
        col : int
            0-indexed column of cell to write to
        data : str or list or dict
            Simple string to be written with `format_dict` formatting. Or a
            list of alternating string and dictionary objects. Dictionaries
            specify additional formatting to be applied to the following string
            in the list.
            Dictionaries will be written with (first) key as display text and
            (first) value as URL.
        format_dict : dict
            Dictionary containing base format for the string.
            
        Returns
        -------
        None
        """
        wb = self._workbook  # Reference to Workbook that contains sheet

        if isinstance(data, list):
            if len(data) == 1:
                data = data[0]
                self._smart_write(row, col, data, format_dict, *args)

            elif any([isinstance(element, FormatList) for element in data]):
                self._write_with_newlines_and_custom_formats(wb, row, col, data, format_dict, *args)

            else:
                self._write_with_newlines(wb, row, col, data, format_dict, *args)

        elif isinstance(data, FormatList):
            if len(data.list) == 2:
                text_format = format_dict.copy()
                text_format.update(data.list[0])
                text_data = data.list[1]
                self._smart_write(row, col, text_data, text_format, *args)
            else:
                self._write_with_custom_formats(wb, row, col, data, format_dict, *args)

        elif isinstance(data, dict):
            self._write_dict_as_url(wb, row, col, data, format_dict, *args)
            
        elif pd.isna(data):
            self.write_blank(row, col, None, wb.add_format(format_dict))

        else:
            # Write handles all other write types dynamically
            self.write(row, col, data, wb.add_format(format_dict), *args)


    def _write_with_newlines_and_custom_formats(self, wb, row, col, data, format_dict, *args):
        """
        Take list of FormatList (and str), join with newline characters and smart write
        """
        data_with_newlines = []

        first_element = data.copy()[0]
        if isinstance(first_element, FormatList):
            first_element = first_element.list
        else:
            first_element = [first_element]
        data_with_newlines.extend(first_element)

        for element in data[1:]:
            if isinstance(element, FormatList):
                element = element.list
                element_stings = [item for item in element if isinstance(item, str)]
                first_string = element_stings[0]
                new_string = "\n" + first_string
                element_with_newline = [new_string if item == first_string else item for item in element]
            else:
                element_with_newline = ["\n" + str(element)]
            data_with_newlines.extend(element_with_newline)

        self._write_with_custom_formats(
            wb,
            row,
            col,
            FormatList(data_with_newlines),
            format_dict,
            *args
        )


    def _write_with_newlines(self, wb, row, col, data, format_dict, *args):
        """
        Take list of str, join with newline character and write
        """
        data_string = "\n".join(data)

        self.write(
            row,
            col,
            data_string,
            wb.add_format(format_dict),
            *args
        )


    def _write_with_custom_formats(self, wb, row, col, data, format_dict, *args):
        data_with_custom_formats = []
        for item in data.list:
            # Convert dicts to Format (with merge onto base format)
            if isinstance(item, dict):
                rich_format = format_dict.copy()
                rich_format.update(item)
                data_with_custom_formats.append(wb.add_format(rich_format))
            else:
                data_with_custom_formats.append(item)

        data_with_all_formats = []
        for n in range(len(data_with_custom_formats)-1):
            data_with_all_formats.append(data_with_custom_formats[n])
            if isinstance(data_with_custom_formats[n], str):
                if isinstance(data_with_custom_formats[n+1], str):
                    data_with_all_formats.append(wb.add_format(format_dict))
        data_with_all_formats.append(data_with_custom_formats[-1])

        self.write_rich_string(
            row,
            col,
            *data_with_all_formats,
            wb.add_format(format_dict),
            *args
        )


    def _write_dict_as_url(self, workbook, row, col, data, format_dict, *args):
        url = list(data.values())[0]
        display_text = list(data.keys())[0]

        url_format = format_dict.copy()
        url_format.update({"underline": True, "font_color": "blue"})

        self.write_url(
            row,
            col,
            url,
            workbook.add_format(url_format),
            display_text,
            *args
        )


    @staticmethod
    def _apply_format(format_table_slice, format_dict):
        """
        Update all cells of a given dataframe slice with the format
        dictionary. Handles dict, series or dataframes.
        """
        if isinstance(format_table_slice, pd.Series):
            (format_table_slice
             .apply(lambda d: d.update(format_dict))
             )
        elif isinstance(format_table_slice, pd.DataFrame):
            # Vectorised for 2D
            (format_table_slice
             .apply(np.vectorize(lambda d: d.update(format_dict)))
             )
        elif isinstance(format_table_slice, dict):
            format_table_slice.update(format_dict)


    def _set_column_widths(self, widths):
        """
        Set the column widths using a list of widths.
        """
        for col_number in range(len(widths)):
            self.set_column(
                col_number,
                col_number,
                widths[col_number]
            )


    def _calculate_column_widths(self, table, formats_table):
        """
        Calculate Excel column widths using maximum length of strings
        and the maximum font size in each column of the data table.

        Parameters
        ----------
        table : pd.DataFrame
            data table to calculate widths from
        formats_table: pd.DataFrame
            formats table to retrieve font size from

        Returns 
        -------
        col_widths : list
            width to apply to Excel columns
        """
        cols = table.shape[1]
        max_lengths = [
            table.iloc[:, col].apply(self._longest_line_length).max()
            for col in range(cols)
            ]

        max_font_sizes = [
            formats_table.iloc[:, col]
            .apply(lambda x: x.get("font_size") or 10).max()
            for col in range(cols)
            ]

        col_widths = [
            self._excel_string_width(l, f)
            for l, f in zip(max_lengths, max_font_sizes)
            ]
        return col_widths

        
    @staticmethod
    def _excel_string_width(string_len, font_size):
        """
        Calculate the rough length of a string in Excel character units.
        This crude estimate does not account for font name or other font format
        (e.g. wrapping).
        
        Parameters
        ----------
        string_len : int
            length of string to calculate width in Excel for
        font_size : int
            size of font
        
        Returns 
        -------
        excel_width : float
            width of equivalent string in Excel
        """    
        if string_len == 0:
            excel_width = 0
        else:
            excel_width = string_len * ((font_size * 0.12) - 0.09)
        
        return excel_width


    def _longest_line_length(self, cell_val):
        """
        Calculate the length of the longest line within a cell.
        If the cell contains a string, the longest length between line breaks is returned.
        If the cell contains a float or integer, the longest length is calculated from the cell_value cast to a string.
        If the cell contains a link formatted as {display_text: link}, the longest length is calculated from the display text.
        If the cell contains a list of strings, the length of the longest string in the list is returned.
        Expects new lines to be marked with "\n", "\r\n" or new lines in multiline strings.

        Parameters
        ----------
        cell_val: 
            cell value

        Returns
        -------
        max_length: int
            the length of the longest line within the string
        """
        split_strings = """
|\r\n|\n"""

        if isinstance(cell_val, str):
            max_length = max([len(line) for line in re.split(split_strings, cell_val)])
        elif isinstance(cell_val, (float, int)):
            max_length = self._longest_line_length(str(cell_val))
        elif isinstance(cell_val, dict):
            max_length = self._longest_line_length(list(cell_val)[0])
        elif isinstance(cell_val, FormatList):
            max_length = self._longest_line_length(cell_val.string)
        elif isinstance(cell_val, list):
            if isinstance(cell_val[0], (dict, FormatList)):
                max_length = self._longest_line_length(cell_val[0])
            else:
                max_length = max([len(line) for line in cell_val])
        else:
            max_length = 0

        return max_length


class GPWorkbook(Workbook):
    """
    Wrapper for and XlsxWriter Workbook object. The Worksheets class has been
    replaced by an alternative with a method for writting GPTable objects.
    """

    def __init__(self, filename=None, options={}):
        super(GPWorkbook, self).__init__(filename=filename, options=options)
        self.theme = None
        self._annotations = None
        # Set default theme
        self.set_theme(gptheme)

    def add_worksheet(self, name=None, gridlines="hide_all"):
        """
        Overwrite add_worksheet() to create a GPWorksheet object.
        
        Parameters
        ----------
        name : str (optional)
            name of the the worksheet to be created
        gridlines : string, optional
        option to hide or show gridlines on worksheets. "show_all" - don't 
        hide gridlines, "hide_printed" - hide printed gridlines only, or 
        "hide_all" - hide screen and printed gridlines.
        
        Returns
        -------
        worksheet : gptables.GPWorksheet
            a worksheet object, which supports writing of GPTable objects
        """
        worksheet = super(GPWorkbook, self).add_worksheet(name, GPWorksheet)
        worksheet.theme = self.theme
        worksheet._workbook = self  # Create reference to wb, for formatting
        
        worksheet.hide_gridlines({
            "show_all": 0,
            "hide_printed": 1,
            "hide_all": 2
            }[gridlines]
        )
        
        return worksheet


    def set_theme(self, theme):
        """
        Sets the theme for all GPTable objects written to the Workbook.
        
        Parameters
        ----------
        theme : gptables.Theme
            a Theme object containing the formatting to be applied to GPTable
            objects written to Worksheets within this Workbook
        
        Returns
        -------
        None
        """
        if not isinstance(theme, Theme):
            raise TypeError(f"`theme` must be a gptables.Theme object, not: {type(theme)}")
        self.theme = theme

    def _update_annotations(self, sheets):
        ordered_refs = []
        for gptable in sheets.values():
            gptable._set_annotations(self.theme.description_order)
            ordered_refs.extend(gptable._annotations)

        # remove duplicates from ordered_refs and assign to self._annotations
        self._annotations = list(dict.fromkeys(ordered_refs))

    def make_table_of_contents(
        self,
        sheets,
        additional_elements = None,
        column_names = None,
        table_name = None,
        title = None,
        subtitles = None,
        instructions = None,
        ):
        """
        Generate table of contents from sheet and optional customisation parameters.

        Parameters
        ----------
        sheets : dict
            mapping worksheet labels to gptables.GPTable objects
        additional_elements : List[str], optional
            additional GPTable elements to display in the contents table. Allowed
            elements are "subtitles", "scope", "source" and "instructions".
        column_names : List[str], optional
            table of contents column names, defaults to
            "Sheet name", "Table description"
        table_name: str, optional
            contents table name, defaults to "contents_table"
        title : str, optional
            table of contents title, defaults to "Table of contents"
        subtitles: List[str], optional
            list of subtitles as strings
        instructions: str, optional
            description of the page layout
            defaults to "This worksheet contains one table."

        Return
        ------
        gpt.GPTable
        """
        if column_names is None:
            column_names = ["Sheet name", "Table description"]
        if table_name is None:
            table_name = "contents_table"
        if title is None:
            title = "Table of contents"
        if instructions is None:
            instructions = "This worksheet contains one table."

        if additional_elements is not None:
            valid_elements = ["subtitles", "scope", "source", "instructions"]
            if not all(element in valid_elements for element in additional_elements):
                msg = ("Cover `additional_elements` list can only contain"
                    "'subtitles', 'scope', 'source' and 'instructions'")
                raise ValueError(msg)

        contents_dict = {}
        for label, gptable in sheets.items(): 
            contents_entry = []
            contents_entry.append(self._strip_annotation_references(gptable.title))

            if additional_elements is not None:
                for element in additional_elements:
                    content = getattr(gptable, element)
                    if element == "subtitles":
                        [contents_entry.append(self._strip_annotation_references(element)) for element in content]
                    else:
                        contents_entry.append(self._strip_annotation_references(content))

            link = {label: f"internal:'{label}'!A1"}

            contents_dict[label] = [link, contents_entry]

        contents_table = pd.DataFrame.from_dict(contents_dict, orient="index").reset_index(drop=True)

        contents_table.columns = column_names

        return GPTable(
            table=contents_table, 
            table_name=table_name, 
            title=title, 
            subtitles=subtitles, 
            instructions=instructions
        )

    @staticmethod
    def _strip_annotation_references(text):
        """
        Strip annotation references (as $$ $$) from a str or list text element.
        """
        pattern = r"\$\$.*?\$\$"
        if isinstance(text, str):
            no_annotations = re.sub(pattern, "", text)
        elif isinstance(text, FormatList):
            no_annotations = FormatList([
                re.sub(pattern, "", part)
                if isinstance(part, str) else part
                for part in text.list
                ])
        elif isinstance(text, list): # TODO: this shouldn't get used - check and delete
            no_annotations = [
                re.sub(pattern, "", part)
                if isinstance(part, str) else part
                for part in text
                ]
        
        return no_annotations


    def make_notesheet(
        self,
        notes_table,
        table_name = None,
        title = None,
        instructions = None,
        ):
        """
        Generate notes table sheets from notes table and optional customisation parameters.

        Parameters
        ----------
        notes_table : pd.DataFrame
            table with notes reference, text and (optional) link columns
        table_name: str, optional
            notes table name, defaults to "notes_table"
        title : str, optional
            notes page title, defaults to "Notes"
        instructions: str, optional
            description of the page layout
            defaults to "This worksheet contains one table."

        Return
        ------
        gpt.GPTable
        """
        # set defaults
        if table_name is None:
            table_name = "notes_table"

        if title is None:
            title = "Notes"

        if instructions is None:
            instructions = "This worksheet contains one table."

        # order notes table by worksheet reference order
        ordered_refs = self._annotations

        order_df = pd.DataFrame({"order": ordered_refs})
        
        notes = notes_table.copy()
        notes = notes.rename(columns={notes.columns[0]: "order"})

        ordered_notes = order_df.merge(notes, on="order", how="left")
        
        unreferenced_notes = notes[~notes["order"].isin(ordered_notes["order"])]

        if not unreferenced_notes.empty:
            warnings.warn(f"The following notes are not referenced: {list(unreferenced_notes['order'])}")

            ordered_notes = pd.concat([ordered_notes, unreferenced_notes])

        # replace note references with note number
        ordered_notes = (ordered_notes
            .reset_index()
            .rename(columns={"index": "Note number"})
            .drop(columns=["order"])
        )

        # convert from python 0-indexing
        ordered_notes["Note number"] = ordered_notes["Note number"] + 1

        return GPTable(
            table=ordered_notes, 
            table_name=table_name, 
            title=title, 
            instructions=instructions,
            index_columns={}
        )
