import xlsxwriter

from xlsxwriter.chartsheet import Chartsheet
from .worksheet_wrapper import Worksheet

from .theme import Theme
# from gptables import gptheme


class Workbook(xlsxwriter.workbook.Workbook):
    """
    Wrapper for and XlsxWriter Workbook object. The Worksheets class has been
    replaced by an alternative that cumulatively stores styles (Formats) and
    data on a cell by cell basis.
    """
    def __init__(self, filename=None, options={}):
        super(Workbook, self).__init__(filename=filename, options=options)
#        xlsxwriter.worksheet.Worksheet = gptables.core.worksheet_wrapper.Worksheet  # Monkey patch our ws in
        
        self.theme = None
        
        # self.set_theme(gptheme)  # Set default theme
        
    
    def _add_sheet(self, name, is_chartsheet):
        """
        Override creation of XlsxWriter Worksheet, with gptables Worksheet.
        """
        # Utility for shared code in add_worksheet() and add_chartsheet().

        sheet_index = len(self.worksheets_objs)
        name = self._check_sheetname(name, is_chartsheet)

        # Initialization data to pass to the worksheet.
        init_data = {
            'name': name,
            'index': sheet_index,
            'str_table': self.str_table,
            'worksheet_meta': self.worksheet_meta,
            'optimization': self.optimization,
            'tmpdir': self.tmpdir,
            'date_1904': self.date_1904,
            'strings_to_numbers': self.strings_to_numbers,
            'strings_to_formulas': self.strings_to_formulas,
            'strings_to_urls': self.strings_to_urls,
            'nan_inf_to_errors': self.nan_inf_to_errors,
            'default_date_format': self.default_date_format,
            'default_url_format': self.default_url_format,
            'excel2003_style': self.excel2003_style,
            'remove_timezone': self.remove_timezone,
        }

        if is_chartsheet:
            worksheet = Chartsheet()
        else:
            worksheet = Worksheet()

        worksheet._initialize(init_data)

        self.worksheets_objs.append(worksheet)
        self.sheetnames[name] = worksheet

        return worksheet
    
    
    def set_theme(self, theme):
        """
        Sets the theme for all GPTable objects written to the Workbook.
        """
        if not isinstance(theme, Theme):
            raise ValueError("`theme` must be a gptables.Theme object")

        self.theme = theme
        
