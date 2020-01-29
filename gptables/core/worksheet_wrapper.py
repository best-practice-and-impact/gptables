import numpy as np
import xlsxwriter
import yaml

class Worksheet(xlsxwriter.Workbook):
    """
    Wrapper for and XlsxWriter Workbook object. The Worksheets class has been
    replaced by an alternative that cumulatively stores styles (Formats) and
    data on a cell by cell basis.
    """
    
    def __init__(self):
        super(Worksheet, self).__init__()
        
        default_styles = {
                "sheet_global":{
                        "font_size":9,
                        "font":"Arial"
                        },
                                
                "title":{
                        "bold":True
                        },
                }
    
    def add_gptable(self, table, title, source, notes=None, styles=self.default_styles):
        
        # Merge user supplied styles with default styles before generating format objects
        
        # Work through elements that have been provided and write them to workbook
        
        
        pass
    
    def add_cover_page(self, cover_config):
        """
        Could be moved to Workbook, if we decide to wrap this too.
        """
        pass
    
class gptable_styles:
    """
    See XlsxWriter [format properties](https://xlsxwriter.readthedocs.io/format.html)
    for valid options.
    """
    def __init__(self, yaml_style_config):
        
