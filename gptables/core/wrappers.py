from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet

#from xlsxwriter.chartsheet import Chartsheet
#from .worksheet_wrapper import Worksheet

from .theme import Theme
# from gptables import gptheme
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
            raise ValueError("`gptable` must be a gptable.GPTable object")
        # TODO. Implement method
        # Get Theme from Worbook
        
        # Work through elements that have been provided and write them to workbook
    
#    def write_cover_page(self, cover_config):
#        """
#        Write a cover page to the worksheet.
#        """
#        pass

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
        
        # self.set_theme(gptheme)  # Set default theme
        
    def add_worksheet(self, name=None):
        # Overwrite add_worksheet() to create a GPsheet object.
        worksheet = super(GPWorkbook, self).add_worksheet(name, GPWorksheet)

        return worksheet

    def set_theme(self, theme):
        """
        Sets the theme for all GPTable objects written to the Workbook.
        """

        if not isinstance(theme, Theme):
            raise ValueError("`theme` must be a gptables.Theme object")
        self.theme = theme


