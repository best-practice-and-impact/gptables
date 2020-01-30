import pandas as pd
import numpy as np
import xlsxwriter
import yaml

class Worksheet(xlsxwriter.Workbook):
    """
    Wrapper for and XlsxWriter Worksheet object. Enables a good practice table
    (gptable) to be added to the worksheet. All elements of the table must be
    supplied at once.
    """
    
    def __init__(self):
        super(Worksheet, self).__init__()

    def write_gptable(self, gptable, theme): # Could supply a default theme here, if prefered to XlsxWrite default
        """
        Write data from a gptable object to the worksheet using the specified
        theme object for formatting.
        """
        
        # Merge user supplied styles with default styles before generating format objects
        
        # Work through elements that have been provided and write them to workbook
        
        
        pass
    
    def add_cover_page(self, cover_config):
        """
        Could be moved to Workbook, if we decide to wrap this too.
        """
        pass
