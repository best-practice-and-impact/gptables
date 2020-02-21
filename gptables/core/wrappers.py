import os
import re
import pandas as pd
import numpy as np

from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet

from .theme import Theme
from .gptable import GPTable

class GPWorksheet(Worksheet):
    """
    Wrapper for an XlsxWriter Worksheet object. Provides a method for writing
    a good practice table (GPTable) to a Worksheet.
    """

    # TODO: Implement cover page
#    def write_cover_page(self, cover_config):
#        """
#        Write a cover page to the worksheet.
#        """
#        pass

    def write_gptable(self, gptable):
        """
        Write data from a GPTable object to the worksheet using the workbook
        Theme object for formatting.
        
        Parameters
        ----------
        gptable : gptables.GPTable
            object contianing elements of the gptable to be written to the
            Worksheet
        
        Returns
        -------
        None
        """
        if not isinstance(gptable, GPTable):
            raise ValueError("`gptable` must be a gptables.GPTable object")

        theme = self.theme

        # Write each GPTable element using appropriate Theme attr
        pos = [0, 0]

        self._reference_annotations(gptable)

        pos = self._write_element(
                gptable.title,
                theme.title_format,
                pos
                )

        pos = self._write_element_list(
                gptable.subtitles,
                theme.subtitle_format,
                pos
                )
        pos[0] += 1

        pos = self._write_table_elements(
                gptable,
                pos
                )

        self._format_footer_elements(gptable)

        footer = theme.footer_order
        for element in footer:
            pos = getattr(self, "_write_" + element)(
                    getattr(gptable, element),
                    getattr(theme, element + "_format"),
                    pos
                    )

    def _format_footer_elements(self, gptable):
        """
        Flank notes with parentheses. Handles strings and lists (rich strings).
        """
        def flank(element):
            if isinstance(element, str):
                return  "(" + element + ")"
            elif isinstance(element, list):
                return ["("] + element + [")"]
        
        gptable.source = flank(gptable.source)
        
        for n in range(len(gptable.notes)):
            gptable.notes[n] = flank(gptable.notes[n])
            
        for n in range(len(gptable.legend)):
            gptable.legend[n] = flank(gptable.legend[n])
        
    def _reference_annotations(self, gptable):
        """
        Replace note references with numbered references. Acts on `title`,
        `subtitles`, `table` and `notes` attributes of a GPTable. References 
        are numbered from top left of spreadsheet, working row-wise.
        
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
        # Store references in order detected
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

        new_annotations = {}
        # Add to dict in order
        for n in range(len(ordered_refs)):
            new_annotations.update({n+1: gptable.annotations[ordered_refs[n]]})
        # Warn if all annotations not referenced
        annotations_diff = len(gptable.annotations) - len(new_annotations)
        if annotations_diff:
            output_file = os.path.basename(self._workbook.filename)
            msg =(f"Warning: {annotations_diff} annotations have not been"
                  f" referenced in {output_file}") 
            print(msg)
        # Replace old notes refs
        gptable.annotations = new_annotations
        
    def _reference_table_annotations(self, gptable, ordered_refs):
         """
         Reference annotaitons in the table column headings and index columns.
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
            where n is the order of appearence in the resulting document
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

    def _replace_reference(self, string, ordered_refs):
        """
        Given a single string, record occurences of new references (denoted by
        flanking $$) and replace with number reference reflecting order of
        detection.
        
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
            num_ref = "(" + str(ordered_refs.index(dict_refs[n]) + 1) + ")"
            string = string.replace(text_refs[n], num_ref)

        return string

    def _write_element(self, element, format_dict, pos):
        """
        Write the title element of a GPTable to the GPWorksheet.
        
        Parameters
        ----------
        element : str or list
            the string or list of rich string elements to be written
        format_dict : dict
            format to be applied to string
        pos : tuple
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
        
    def _write_element_list(self, element_list, format_dict, pos):
        """
        Writes a list of elements row-wise.
        
        Parameters
        ----------
        element_list : list
            list of strings or nested list of rich string elements to write,
            one per row
        format_dict : dict
            format to be applied to string
        pos : tuple
            the position of the worksheet cell to write the elements to

        Returns
        -------
        pos: list
            new position to write next element from
        """
        if element_list:
            for element in element_list:
                self._smart_write(*pos, element, format_dict)
                pos[0] += 1         
        
        return pos
    
    def _write_source(self, element, format_dict, pos):
        """
        Alias for writting footer elements by name.
        """
        return self._write_element(element, format_dict, pos)
    
    def _write_legend(self, element_list, format_dict, pos):
        """
        Alias for writting footer elements by name.
        """
        return self._write_element_list(element_list, format_dict, pos)
        
    def _write_notes(self, element_list, format_dict, pos):
        """
        Alias for writting footer elements by name.
        """
        return self._write_element_list(element_list, format_dict, pos)
        
    def _write_annotations(self, annotations_dict, format_dict, pos):
        """
        Writes a list of ordered annotations row-wise.
        
        Parameters
        ----------
        notes_dict : dict
            note associate with each references, as {reference: note}
        format_dict : dict
            format to be applied to string
        pos : tuple
            the position of the worksheet cell to write the elements to

        Returns
        -------
        pos: list
            new position to write next element from
        """
        for ref, annotation in annotations_dict.items():
            element = f"({ref}: {annotation})"
            self._smart_write(*pos, element, format_dict)
            pos[0] += 1
            
        return pos
    
    def _write_table_elements(self, gptable, pos):
        """
        Writes the table, scope and units elements of a GPTable. Uses the
        Workbook Theme, plus any additional formatting associated with the
        GPTable. Also replaces `np.nan` with a missing value marker.
        
        Parameters
        ----------
        gptable : gptables.GPTable
            object containing the table and additional formatting data
        pos : tuple
            the position of the worksheet cell to write the units to

        Returns
        -------
        pos : list
            new position to write next element from
        """
        # Get theme
        theme = self.theme
        
        # Write scope
        self._smart_write(
                *pos,
                gptable.scope,
                theme.scope_format
                )
        
        # Write units above each col heading
        # TODO: add support for dictionary {"Column_name":"unit"}
        pos[1] += gptable.index_levels
        n_cols = len(gptable._column_headings)
        units = gptable.units
        if isinstance(units, str):
            pos[1] += n_cols - 1
            self._smart_write(
                *pos,
                units,
                theme.units_format
                )
            pos[1] += 1

        elif isinstance(units, list):
            for n in range(n_cols):
                self._smart_write(
                    *pos,
                    units[n],
                    theme.units_format
                    )
                pos[1] += 1
        
        # Reset position to left col on next row
        pos[0] += 1
        pos[1] = 0
        
        ## Create data array
        index_levels = gptable.index_levels
        index_columns = [col for col in gptable.index_columns.values()]
        data = pd.DataFrame(gptable.table, copy=True)
            
        # Create row containing column headings
        data.loc[-1] = data.columns
        data.index = data.index + 1
        data.sort_index(inplace=True)
        data.iloc[0, index_columns] = ""  # Delete index col headings
        
        ## Create formats array
        # pandas.DataFrame did NOT want to hold dictionaries, so be wary
        formats = pd.DataFrame().reindex_like(data)
        dict_row = [{} for n in range(formats.shape[1])]
        for row in range(formats.shape[0]):
            dict_row = [{} for n in range(formats.shape[1])]
            formats.iloc[row] = dict_row
        
        
        ## Handle missing values
        missing_marker = theme.missing_value

        if data.isna().values.any():
            if missing_marker is not None:
                # Super inefficient format update loop
                # Only run if align not set for data
                if not "align" in theme.data_format.keys():
                    rows, cols = data.shape
                    for row in range(rows):
                        for col in range(cols):
                            if pd.isna(data.iloc[row, col]):
                                (formats.iloc[row, col]
                                .update({"align":"center"})
                                )

                data.fillna(missing_marker, inplace=True)
                gptable.legend.append(f"{missing_marker} not available")
            else:
                msg = ("`Theme.missing_marker` must be assigned if values are"
                       " missing within GPTable.")
                raise ValueError(msg)
        
        
        ## Add Theme formatting
        self._apply_format(
                formats.iloc[0, index_levels:],
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
                index_level_formats[level]
                )
        
        # Add additional formatting
        # TODO: Implement row, col and cell wise formatting
        additional_formatting = gptable.additional_formatting
        
        ## Write table
        pos = self._write_array(data, formats, pos)
        
        return pos
    
    @staticmethod
    def _apply_format(format_table_slice, format_dict):
        if isinstance(format_table_slice, pd.Series):
            (format_table_slice
             .apply(lambda d: d.update(format_dict))
             )
        elif isinstance(format_table_slice, pd.DataFrame):
            # Vectorised for 2D
            (format_table_slice
             .apply(np.vectorize(lambda d: d.update(format_dict)))
             )

    def _write_array(self, data, formats, pos):
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
        pos : tuple
            the position of the top left cell to start writing the array from
            
        Returns
        -------
        pos : list
            new position to write next element from
        """
        if data.shape != formats.shape:
            raise ValueError("Data and format arrays must be of equal shape")
        
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
        
    def _smart_write(self, row, col, data, format_dict):
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
            data_with_formats = []
            for item in data:
                # Convert dicts to Format (with merge onto base format)
                if isinstance(item, dict):
                    rich_format = self._merge_dict(format_dict, item)
                    data_with_formats.append(wb.add_format(rich_format))
                else:
                    data_with_formats.append(item)
            self.write_rich_string(row,
                                   col,
                                   data_with_formats,
                                   wb.add_format(format_dict)
                                   )
        else:
            self.write(row,
                       col,
                       data,
                       wb.add_format(format_dict)
                       )
    @staticmethod
    def _merge_dict(base_dict, update_dict):
        """
        Creates a new dictionary, by updating a base dictionary not in-place.
        
        Parameters
        ----------
        base_dict : dict
            the base dictionary to be updated not in-place
        update_dict : dict
            the dictionary to update `base_dict` with
        
        Returns
        -------
        updated_dict : dict
            copy of `base_dict` updated with `update_dict`
        
        """
        updated_dict = base_dict.copy()
        return updated_dict.update(update_dict)
    
    @staticmethod
    def _excel_string_width(string):
        """
        Calculate the rough length of a string in Excel character units.
        This is highly inaccurate and doesn't account for font size etc.
        
        Parameters
        ----------
        string : str
            string to calculate width in Excel for
        
        Returns 
        -------
        string_width : float
            width of equivalent string in Excel
        """
        string_len = len(string)
    
        if string_len == 0:
            excel_width = 0
        else:
            excel_width =  string_len * 1.1
        
        return excel_width


class GPWorkbook(Workbook):
    """
    Wrapper for and XlsxWriter Workbook object. The Worksheets class has been
    replaced by an alternative with a method for writting GPTable objects.
    """
    def __init__(self, filename=None, options={}):
        super(GPWorkbook, self).__init__(filename=filename, options=options)
        self.theme = None
        
        # self.set_theme(Theme(gptheme.yaml))  # Set default theme
        
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
            raise ValueError("`theme` must be a gptables.Theme object")
        self.theme = theme
