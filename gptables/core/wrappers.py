from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet

from .theme import Theme
from .gptable import GPTable

class GPWorksheet(Worksheet):
    """
    Wrapper for and XlsxWriter Worksheet object. Provides a method for writing
    a good practice table (GPTable) to a Worksheet.
    """        
    def write_gptable(self, gptable):
        """
        Write data from a GPTable object to the worksheet using the specified
        Theme object for formatting.
        """
        if not isinstance(gptable, GPTable):
            raise ValueError("`gptable` must be a gptables.GPTable object")
        # TODO. Implement method
        # Get Theme
        theme = self.theme
        
        # Write each GPTable element using appropriate Theme attr
    
#    def write_cover_page(self, cover_config):
#        """
#        Write a cover page to the worksheet.
#        """
#        pass
        
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



class MyWorksheet(Worksheet):
    """
    Subclass of the XlsxWriter Worksheet class to override the default
    write() method.

    """


class MyWorkbook(Workbook):
    """
    Subclass of the XlsxWriter Workbook class to override the default
    Worksheet class with our custom class.

    """

    def add_worksheet(self, name=None):
        # Overwrite add_worksheet() to create a MyWorksheet object.
        worksheet = super(MyWorkbook, self).add_worksheet(name, MyWorksheet)

        return worksheet