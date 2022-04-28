import os
import re
import warnings
import pandas as pd
import numpy as np
from copy import deepcopy

from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet

from .theme import Theme
from .gptable import GPTable
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

    def write_contentsheet(self, contentsheet, auto_width):
        """
        Alias for writing contents sheet to worksheet
        
        Parameters
        ----------
        contentsheet : gptables.Contentsheet
            object containing table of contents to be written to Worksheet
        """
        # TODO: hyperlink sheet name column entries
        return self.write_gptable(contentsheet, auto_width)


    def write_notesheet(self, notesheet, sheets, auto_width):
        """
        Alias for writing notes sheet to worksheet.

        Parameters
        ----------
        notesheet : gptables.Notesheet
            object containing notes sheet content to be written to Worksheet
        """
        order = []
        for gptable in sheets.values():
            order.extend(gptable.annotations)
        
        order_df = pd.DataFrame({"order": order})
        
        notes = notesheet.table.copy()
        notes = notes.rename(columns={notes.columns[0]: "order"})

        ordered_notes = order_df.merge(notes, on="order", how="left")
        
        unreferenced_notes = notes[~notes["order"].isin(ordered_notes["order"])]

        if not unreferenced_notes.empty:
            warnings.warn(f"The following notes are not referenced: {list(unreferenced_notes['order'])}")

            ordered_notes = ordered_notes.append(unreferenced_notes)
    

        notesheet.table = pd.DataFrame()

        notesheet.table["Note number"] = range(1, len(order)+1) # TODO: note number input variable?

        notesheet.table = notesheet.table.join(ordered_notes).drop(columns=["order"])

        # TODO: move formatting into _write_array
        if notesheet.link_text_column_name is not None:
            notesheet.additional_formatting.append({
                "column": {
                    "columns": [notesheet.link_text_column_name],
                    "format": {"underline": True, "font_color": "blue"}
                }
            })

        self.write_gptable(notesheet, auto_width, notesheet.link_text_column_name, notesheet.link_url_column_name)
        

    def write_gptable(self, gptable, auto_width, link_text_column_name=None, link_url_column_name=None):
        """
        Write data from a GPTable object to the worksheet using the workbook
        Theme object for formatting.
        
        Parameters
        ----------
        gptable : gptables.GPTable
            object containing elements of the gptable to be written to the
            Worksheet
        
        Returns
        -------
        None
        """
        if not isinstance(gptable, GPTable):
            raise TypeError("`gptable` must be a gptables.GPTable object")
        
        theme = self.theme

        # Write each GPTable element using appropriate Theme attr
        pos = [0, 0]

        self._reference_annotations(gptable)

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
                link_text_column_name,
                link_url_column_name
                )

        self._mark_data_as_worksheet_table(gptable, theme.column_heading_format, link_url_column_name)


    def _reference_annotations(self, gptable):
        """
        Replace note references with numbered references. Acts on `title`,
        `subtitles`, `table` and `notes` attributes of a GPTable. References 
        are numbered from top left of spreadsheet, working across each row.
        
        Parameters
        ----------
        gptable : gptables.GPTable
            object containing data with references to notes

        Returns
        -------
        None
        """
        elements = [
                "title",
                "subtitles",
                "scope",
                "units",
                "legend"
                ]
        # Store annotation references in order detected
        ordered_refs = []
        
        # Loop through elements, replacing references in strings
        for attr in elements:
            attr_current = getattr(gptable, attr)
            setattr(
                    gptable,
                    attr,
                    self._replace_reference_in_attr(
                            attr_current,
                            ordered_refs
                            )
                    )
        self._reference_table_annotations(gptable, ordered_refs)

        gptable.annotations = ordered_refs
        

    def _reference_table_annotations(self, gptable, ordered_refs):
         """
         Reference annotations in the table column headings and index columns.
         """
         table = getattr(gptable, "table")
         
         table.columns = self._replace_reference_in_attr(
                 [x for x in table.columns],
                 ordered_refs
                 )
         
         index_columns = gptable.index_columns.values()
         
         for col in index_columns:
             table.iloc[:, col] = table.iloc[:, col].apply(
                     lambda x: self._replace_reference_in_attr(x, ordered_refs)
                     )

         setattr(gptable, "table", table)


    def _replace_reference_in_attr(self, data, ordered_refs):
        """
        Replaces references in a string or list/dict of strings. Works
        recursively on list elements and dict values. Other types are returned
        without modification. Updates `ordered_refs` with newly detected
        references.
        
        Parameters
        ----------
        data : any type
            object containing strings to replace references in
        ordered_refs : list
            list of references used so far. New references will be added to
            this list in order of detection

        Returns
        -------
        string : str
            input string with references replaced with numerical reference (n),
            where n is the order of appearance in the resulting document
        """
        if isinstance(data, str):
            data = self._replace_reference(data, ordered_refs)
        if isinstance(data, list):
            for n in range(len(data)):
                data[n] = self._replace_reference_in_attr(
                        data[n],
                        ordered_refs
                        )
        if isinstance(data, dict):
            for key in data.keys():
                data[key] = self._replace_reference_in_attr(
                        data[key],
                        ordered_refs
                        )

        return data
    

    @staticmethod
    def _replace_reference(string, ordered_refs):
        """
        Given a single string, record occurrences of new references (denoted by
        flanking dollar signs [$$reference$$]) and replace with number
        reference reflecting order of detection.
        
        Parameters
        ----------
        string : str
            the string to replace references within
        ordered_refs : list
            list of references used so far. New references will be added to
            this list in order of detection

        Returns
        -------
        string : str
            input string with references replaced with numerical reference (n),
            where n is the order of appearence in the resulting document
        """
        text_refs = re.findall(r"[$]{2}.*?[$]{2}", string)
        dict_refs = [w.replace("$", "") for w in text_refs]
        for n in range(len(dict_refs)):
            if dict_refs[n] not in ordered_refs:
                ordered_refs.append(dict_refs[n])
            num_ref = "[note " + str(ordered_refs.index(dict_refs[n]) + 1) + "]"
            string = string.replace(text_refs[n], num_ref)

        return string


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


    def _write_hyperlinked_toc_entry(self, pos, sheet_name):
        """
        Write a table of contents entry. Includes a hyperlink to the sheet
        in the first column. Then data for that sheet in the second column.

        Parameters
        ----------
        pos : list
            the position of the worksheet cell to write the elements to
        sheet_name : str
            name of sheet to hyperlink to

        Returns
        -------
        pos: list
            new position to write next element from
        """
        theme = self.theme

        link = f"internal:'{sheet_name}'!A1"
        hyperlink_format = deepcopy(theme.cover_text_format)
        hyperlink_format.update({"underline": True, "font_color": "blue"})
        self._smart_write(
            *pos,
            link,
            hyperlink_format,
            sheet_name
            )        

        return [pos[0] , pos[1] + 1]

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


    def _write_table_elements(self, pos, gptable, auto_width, link_text_column_name=None, link_url_column_name=None):
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
        link_text_column_name: str, optional
            name of (optional) column containing link text to display
        link_url_column_name: str, optional
            name of (optional) column contain link urls
            column entries should start with either
            `http://`, `https://`, `ftp://` or `mailto::`

        Returns
        -------
        pos : list
            new position to write next element from
        """
        # Raise error if any table element is null or whitespace
        gptable.table.replace(regex=r'^\s*$', value=np.NaN, inplace=True)
        if gptable.table.isna().values.any():
            msg = ("""
            Empty or null cell found in table, replace with
            appropriate shorthand before inputting to gptables.
            Guidance on shorthand can be found at:
            https://gss.civilservice.gov.uk/policy-store/symbols-in-tables-definitions-and-help/
            """)
            raise ValueError(msg)

        # Raise error if any table element is only special characters
        gptable.table.replace(regex=r'^\W*$', value=np.NaN, inplace=True)
        if gptable.table.isna().values.any():
            msg = ("""
            Cell found containing only special characters, replace with
            alphanumeric characters before inputting to gptables.
            Guidance on symbols in tables can be found at:
            https://gss.civilservice.gov.uk/policy-store/symbols-in-tables-definitions-and-help/
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
        
        ## Add additional table-specific formatting from GPTable
        self._apply_additional_formatting(
                formats,
                gptable.additional_formatting,
                gptable.index_levels
                )
        
        ## Write table
        pos = self._write_array(pos, data, formats, link_text_column_name, link_url_column_name)

        ## Set columns widths
        if auto_width:
            widths = self._calculate_column_widths(data, formats)
            self._set_column_widths(widths)
        
        return pos

    
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


    def _write_array(self, pos, data, formats, link_text_column_name=None, link_url_column_name=None):
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
        link_text_column_name: str, optional
            name of (optional) column containing link text to display
        link_url_column_name: str, optional
            name of (optional) column contain link urls
            column entries should start with either
            `http://`, `https://`, `ftp://` or `mailto::`
            
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

                if data.columns[col] == link_text_column_name:
                    self.write_url(
                        row=pos[0] + row,
                        col=pos[1] + col,
                        url=data.loc[row, link_url_column_name],
                        string=cell_data,
                        cell_format=cell_format_dict,
                    )

                if data.columns[col] == link_url_column_name:
                    pass
                
                else:
                    self._smart_write(
                        pos[0] + row,
                        pos[1] + col,
                        cell_data,
                        cell_format_dict
                        )
        
        pos = [pos[0] + rows, 0]
        
        return pos
        
    def _mark_data_as_worksheet_table(self, gptable, column_header_format_dict, link_url_column_name=None):
        """
        Marks the data to be recognised as a Worksheet Table in Excel.
        """
        data_range = gptable.data_range

        column_header_format = self._workbook.add_format(column_header_format_dict)
        
        column_list = gptable.table.columns.tolist()
        
        if link_url_column_name is not None:
            column_list.remove(link_url_column_name)
            data_range[-1] = data_range[-1] - 1
        
        column_headers = [{'header': column, 'header_format': column_header_format} for column in column_list]

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
        data : str or list
            Simple string to be written with `format_dict` formatting. Or a
            list of alternating string and dictionary objects. Dictionaries
            specify additional formatting to be applied to the following string
            in the list.
        format_dict : dict
            Dictionary containing base format for the string.
            
        Returns
        -------
        None
        """
        wb = self._workbook  # Reference to Workbook that contains sheet
        if isinstance(data, list):
            # At this point, any list should be a rich-text element
            data_with_formats = []
            for item in data:
                # Convert dicts to Format (with merge onto base format)
                if isinstance(item, dict):
                    rich_format = format_dict.copy()
                    rich_format.update(item) 
                    data_with_formats.append(wb.add_format(rich_format))
                else:
                    data_with_formats.append(item)
            if len(data) > 3:
                data_with_formats.insert(-1, wb.add_format(format_dict))
            
            self.write_rich_string(row,
                                   col,
                                   *data_with_formats,
                                   wb.add_format(format_dict),
                                   *args
                                   )
        else:
            # Write handles all other write types dynamically
            self.write(
                    row,
                    col,
                    data,
                    wb.add_format(format_dict),
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

    @staticmethod
    def _longest_line_length(cell_val):
        """
        Calculate the length of the longest line within a string. If the string contains line breaks,
        this will return the length of the longest line. Expects new lines to be marked with '\r\n'

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
            return(max([len(line) for line in re.split(split_strings, cell_val)]))
        else:
            return(0)
        


class GPWorkbook(Workbook):
    """
    Wrapper for and XlsxWriter Workbook object. The Worksheets class has been
    replaced by an alternative with a method for writting GPTable objects.
    """

    def __init__(self, filename=None, options={}):
        super(GPWorkbook, self).__init__(filename=filename, options=options)
        self.theme = None
        # Set default theme
        self.set_theme(gptheme)
        

    def add_worksheet(self, name=None):
        """
        Overwrite add_worksheet() to create a GPWorksheet object.
        
        Parameters
        ----------
        name : str (optional)
            name of the the worksheet to be created
        
        Returns
        -------
        worksheet : gptables.GPWorksheet
            a worksheet object, which supports writing of GPTable objects
        """
        worksheet = super(GPWorkbook, self).add_worksheet(name, GPWorksheet)
        worksheet.theme = self.theme
        worksheet._workbook = self  # Create reference to wb, for formatting
        worksheet.hide_gridlines(2)
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
