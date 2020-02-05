from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet

from .theme import Theme
from .gptable import GPTable

class GPWorksheet(Worksheet):
    """
    Wrapper for an XlsxWriter Worksheet object. Provides a method for writing
    a good practice table (GPTable) to a Worksheet.
    """        
#    def write_cover_page(self, cover_config):
#        """
#        Write a cover page to the worksheet.
#        """
#        pass
    
    def write_gptable(self, gptable):
        """
        Write data from a GPTable object to the worksheet using the specified
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
        # Get theme
        theme = self.theme
        
        # Write each GPTable element using appropriate Theme attr
        pos = (0, 0)
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
        
        pos = self._write_table_elements(
                gptable,
                pos
                )
        
        pos = self._write_element(
                gptable.source,
                theme.source_format,
                pos)
        
        pos = self._write_element_list(
                gptable.legend,
                theme.legend_format,
                pos
                )
        
        pos = self._write_element_list(
                gptable.notes,
                theme.notes_format,
                pos
                )

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
        pos : tuple
            new position to write next element from
        """
        format_obj = self._workbook.add_format(self.format_dict)
        self._smart_write(*pos, element, format_obj)
        
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
        pos: tuple
            new position to write next element from
        """
        format_obj = self._workbook.add_format(format_dict)
        for element in element_list:
            self._smart_write(*pos, element, format_obj)
            
            pos[0] += 2
            
        return pos
    
    def _write_table_elements(self, gptable, pos):
        """
        Writes the table, scope and units elements of a GPTable. Uses the
        Workbook Theme, plus any additional formatting associated with the
        GPTable.
        
        Parameters
        ----------
        gptable : gptables.GPTable
            object containing the table and additional formatting data
        pos : tuple
            the position of the worksheet cell to write the units to

        Returns
        -------
        pos : tuple
            new position to write next element from
        """
        # Get theme, table and additional formatting
        theme = self.theme
        table = gptable.table
        addn_formats = gptable._additional_formats
        
        # Write scope
        scope_format_obj = self._workbook.add_format(theme.scope_format)
        self._smart_write(
                *pos,
                gptable.scope,
                scope_format_obj
                )
        
        # Write units above each col heading
        pos[1] += gptable.index_levels
        n_cols = len(gptable._column_headings)
        if isinstance(gptable.units, str):
            units = [gptable.units for n in n_cols]
        elif isinstance(gptable.units, list):
            units = gptable.units
        # TODO: add support for dictionary {"Column_name":"unit"}
        
        units_format_obj = self._workbook.add_format(theme.units_format)
        for n in range(n_cols):
            self._smart_write(
                *pos,
                units[n],
                units_format_obj
                )
            pos[1] += 1
        
        # Write table
        pos[0] += 1
        pos[1] = 0
        
        # TODO: Implement table writing
        # May need to create an array of format dictionaries to merge
        # additional formatting with Theme formats
        # Can then iterate across array of data and formats to write table
        
        # Move to next row and reset column position
        pos[0] += 1
        pos[1] = 0
        return pos
    
    def _write_array(self, data, formats, pos):
        """
        Write a two-dimensional array to the current Worksheet, starting from
        the specified position.
        
        Parameters
        ----------
        data : numpy.array
            array of data to be written to Worksheet
        formats : numpy.array
            array of dictionaries that specify the formatting to be applied
            to each cell of data
        pos : tuple
            the position of the top left cell to start writing the array from
            
        Returns
        -------
        None
        """
        if data.shape != formats.shape:
            raise ValueError("Data and format arrays must be of equal shape")
        
        rows, cols = data.shape
        for row in range(rows):
            for col in range(cols):
                cell_data = data[row, col]
                cell_format_dict = formats[row, col]
                
                self._smart_write(
                        pos[0]+row,
                        pos[1]+col,
                        cell_data,
                        cell_format_dict
                        )
        
    def _smart_write(self, row, col, data, format_dict):
        """
        Depending on the input data, this function will write rich strings or
        use the standard write() method. For rich strings, the base format is
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
