import pandas as pd
import numpy as np
import xlsxwriter

from .gptable import GPTable

class Worksheet(xlsxwriter.worksheet.Worksheet):
    """
    Wrapper for and XlsxWriter Worksheet object. Provides a method for writing
    a good practice table (GPTable) to a Worksheet.
    """
    
    def __init__(self):
        super(Worksheet, self).__init__()

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
