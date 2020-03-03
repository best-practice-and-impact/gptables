from gptables import GPWorkbook

def produce_workbook(
        file,
        sheets,
        theme = None,
#        cover_sheet = None
        ):
    """
    Produces a GPWorkbook.

    This is the main function that will take in data and theme information,
    It calls upon the packages to return a formatted ``.xlsx`` file, ready to
    be written using `workbook.close()`.

    Parameters
    ----------
    file : str
        Path to write final workbook to (an .xlsx file)
    sheets : dict
        A dictionary mapping worksheet labels to gptables.GPTable objects
    theme : gptables.Theme
        The formatting to be applied tot GPTable elements
    cover_sheet : dict (optional)
        cover sheet data
        
    Returns
    -------
    workbook : gptables.GPWorkbook
    """
    wb = GPWorkbook(file)
    
    if theme is not None:
        wb.set_theme(theme)
    
    for sheet, gptable in sheets.items():
        ws = wb.add_worksheet(sheet)
        ws.write_gptable(gptable)
    
    return wb

def write_workbook(file, sheets, theme, cover_sheet=None):

    """
    Writes a GPWorkbook to the specified file.

    This is an alternative main function that will take in data and theme
    information. It calls upon the packages to write a formatted ``.xlsx``
    file to the specified path.

    Parameters
    ----------
    file : str
        Path to write final workbook to (an .xlsx file)
    sheets : dict
        A dictionary mapping worksheet labels to gptables.GPTable objects
    theme : gptables.Theme
        The formatting to be applied tot GPTable elements
    cover_sheet : dict (optional)
        cover sheet data

    Returns
    -------
    None
    """
    wb = produce_workbook(file, sheets, theme, cover_sheet)
    wb.close()
