from pathlib import Path
import numpy as np
import xlsxwriter as xlw
import json

class Workbook:
    """
    An Excel workbook.
    """
    def __init__(self, filename, styles={}):

        self.filename = filename
        if not Path(self.filename).parent.exists():
            msg = f"Can't write {filename}, directory does not exist."
            raise OSError(msg)
        
        if not str(filename).endswith(".xlsx"):
            raise ValueError("`filename` must end with '.xlsx'")
        
        self.worksheets = []
        self.styles = styles
        
    def add_worksheet(self, name, shape):
        """
        Create a new worksheet with the specified name.
        """
        new_worksheet = worksheet(name, shape)
        self.worksheets.append(new_worksheet)
        return new_worksheet
    
    def write_output_to_excel(self):
        """
        Use XlsxWriter to write Workbook to an excel file.
        """
        wb = xlw.Workbook(self.filename)
        
        for sheet in self.worksheets:
            ws = wb.add_worksheet(sheet.name)
            
            rows, cols = sheet.shape()
            for row in range(rows):
                for col in range(cols):
                    cell_format = wb.add_format(sheet.cells[row, col].style)
                    ws.write(row, col, sheet.cells[row, col].data, cell_format)
        
        wb.close()
    
    def write_cell_attributes_to_excel(self):
        """
        Use XlsxWriter to write data and style dictionaries to Excel.
        """
        wb = xlw.Workbook(self.filename.replace(".xlsx", "_parameters.xlsx"))
        
        for sheet in self.worksheets:
            ws = wb.add_worksheet(sheet.name)
            
            rows, cols = sheet.shape()
            for row in range(rows):
                for col in range(cols):
                    output_str = "\n".join([sheet.cells[row, col].data,
                                           json.dumps(sheet.cells[row, col].style)])
                    ws.write(row, col, output_str)
                    
        wb.close()
    
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
    def __init__(self, name, shape):
        self.name = name
        self.cells = np.array([cell() for _ in range(shape[0]*shape[1])]).reshape(shape)
        
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
