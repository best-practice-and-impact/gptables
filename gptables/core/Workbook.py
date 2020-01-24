from pathlib import Path
import numpy as np
import xlsxwriter as xlw

class Workbook:
    """
    An Excel workbook.
    """
    def __init__(self, filename, styles={}):

        self.filename = Path(filename)
        if not self.filename.parent.exists():
            msg = f"Can't write {filename}, directory does not exist."
            raise OSError(msg)
        
        if not str(filename).endswith(".xlsx"):
            raise ValueError("`filename` must end with '.xlsx'")
        
        self.worksheets = []
        self.styles = styles
        
    def add_worksheet(self, name):
        """
        Create a new worksheet with the specified name.
        """
        new_worksheet = worksheet(name)
        self.worksheets.append(new_worksheet)
        return new_worksheet
    
    def write_output_to_excel(self):
        """
        Uses xlsxwriter to write workbook to an excel file.
        """
        wb = xlw.Workbook(self.filename)
        
        for sheet in self.worksheets:
            ws = wb.add_worksheet(sheet.name)
            
            rows, cols = sheet.shape()
            for row in rows:
                for col in cols:
                    cell_format = wb.add_format(sheet[row, col].data)
                    ws.write(row, col, sheet[row, col].data, cell_format)
    
    def write_cell_parameters_to_excel(self):
        """
        Write data and style dictionaries to Excel.
        """
        wb = xlw.Workbook(self.filename.replace(".xlsx", "_parameters.xlsx"))
        
        for sheet in self.worksheets:
            ws = wb.add_worksheet(sheet.name)
            
            rows, cols = sheet.shape()
            for row in rows:
                for col in cols:
                    output_str = "\n".join(sheet[row, col].data,
                                           sheet[row, col].style)
                    ws.write(row, col, output_str)
    
    def list_worksheets(self):
        """
        List existing worksheets in order.
        """
        print([ws.worksheet_name for ws in self.worksheets])
        
    def reorder_worksheets(order_list):
        """
        Reorder worksheets list according to specified list.
        """
        pass


class worksheet:
    """
    An Excel worksheet within a Workbook.
    """
    def __init__(self, worksheet_name, shape):
        self.worksheet_name = worksheet_name
        self.cells = np.empty(shape)
        
    def shape(self):
        return self.cells.shape


class cell:
    """
    A cell of an Excel worksheet.
    
    This could be represented by two array attributes of a worksheet, if no
    more complexity is required at this level.
    """
    def __init__(self):
        self.data = ""
        self.style = {}
        
    def set_data(self, new_data):
        """
        Sets data of cell. Will replace any existing data with `new_data`. 
        """
        self.data = new_data
        
    def update_style(self, new_style):
        """
        Update style dictionary with style from new style dictionary. Note that
        existing values will be replaced by new values when keys exist in both
        dictionaries.
        """
        self.style.update(new_style)
