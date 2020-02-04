from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet

from .theme import Theme
from .gptable import GPTable

class GPWorksheet(Worksheet):
    """
    Wrapper for and XlsxWriter Worksheet object. Provides a method for writing
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
        
        pos = self.
        

        
    
    def _write_element(self, element, format_dict, pos):
        """
        Write the title element of a GPTable to the GPWorksheet.
        
        Parameters
        ----------
        element: str or list
            the string or list of rich string elements to be written
        format_dict: dict
            format to be applied to string
        pos: tuple
            the position of the worksheet cell to write the element to

        Returns
        -------
        pos: tuple
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
        element_list: list
            list of strings or nested list of rich string elements to write,
            one per row
        format_dict: dict
            format to be applied to string
        pos: tuple
            the position of the worksheet cell to write the elements to

        Returns
        -------
        pos: tuple
            new position to write next element from
        """
        format_obj = self._workbook.add_format(format_dict)
        for element in element_list:
            self._smart_write(*pos, element, format_obj)
            
            pos[0] += 1
            
        return pos
    
    def _write_units(self, units, format_dict, pos):
        """
        Writes units above each column heading.
        
        Parameters
        ----------
        units: str or dict
            single unit (for all columns) or map of column to unit type
            {str: str}
        format_dict: dict
            format to be applied to units
        pos: tuple
            the position of the worksheet cell to write the units to

        Returns
        -------
        pos: tuple
            new position to write next element from
        """
        pass
    
    def _write_table_element(self, gptable, pos):
        """
        Writes the table element of a GPTable. Uses the Workbook Theme, plus
        any additional formatting associated with the GPTable.
        
        Parameters
        ----------
        gptable: gptables.GPTable
            object containing the table and additional formatting data
        pos: tuple
            the position of the worksheet cell to write the units to

        Returns
        -------
        pos: tuple
            new position to write next element from
        """
        # Get theme and additional format
        theme = self.theme
        table = gptable.table
        
        pass
        
    def _smart_write(self, row, col, data, format_dict):
        """
        Depending on the input data, this function will write rich strings or
        use the standard write() method. For rich strings, the base format is
        merged with each rich format supplied within data.
        
        Parameters
        ----------
        row: int
            0-indexed row of cell to write to
        col: int
            0-indexed column of cell to write to
        data: str or list
            Simple string to be written with `format_dict` formatting. Or a
            list of alternating string and dictionary objects. Dictionaries
            specify additional formatting to be applied to the following string
            in the list.
        format_dict: dict
            Dictionary containing base format for the string.
            
        Returns
        -------
        None
        """
        wb = self._workbook  # Reference to Workbook that contains sheet
        if isinstance(data, list):
            data_with_formats = []
            for item in data:
                # Convert dicts to Format objects
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
        """
        updated_dict = base_dict.copy()
        return updated_dict.update(update_dict)
    
    @staticmethod
    def _excel_string_width(str):
        """
        Calculate the rough length of a string in Excel character units.
        This is highly inaccurate and doesn't account for font size etc.
    
        """
        string_width = len(str)
    
        if string_width == 0:
            return 0
        else:
            return string_width * 1.1


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
        """
        worksheet = super(GPWorkbook, self).add_worksheet(name, GPWorksheet)
        worksheet.theme = self.theme
        worksheet._workbook = self  # Create reference to wb, for formatting
        return worksheet

    def set_theme(self, theme):
        """
        Sets the theme for all GPTable objects written to the Workbook.
        """
        if not isinstance(theme, Theme):
            raise ValueError("`theme` must be a gptables.Theme object")
        self.theme = theme
