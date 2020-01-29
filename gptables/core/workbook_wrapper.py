from pathlib import Path
import numpy as np
import xlsxwriter
import json


from .worksheet_wrapper import Worksheet

class Workbook(xlsxwriter.Workbook):
    """
    Wrapper for and XlsxWriter Workbook object. The Worksheets class has been
    replaced by an alternative that cumulatively stores styles (Formats) and
    data on a cell by cell basis.
    """
    
    
    