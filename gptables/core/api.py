from gptables import GPWorkbook

def produce_workbook(
        filename,
        sheets,
        theme = None,
        auto_width = True,
#      cover_sheet = None
        ):
    """
    Produces a GPWorkbook.

    This is the main function that will take in data and theme information,
    It calls upon the packages to return a formatted ``.xlsx`` file, ready to
    be written using `workbook.close()`.

    Parameters
    ----------
    filename : str
        Path to write final workbook to (an .xlsx file)
    sheets : dict
        A dictionary mapping worksheet labels to gptables.GPTable objects
    theme : gptables.Theme (optional)
        The formatting to be applied tot GPTable elements. gptheme is used by
        default
    auto_width : bool (optional)
        Select if column widths should be automatically determined. True by default.
        
    Returns
    -------
    workbook : gptables.GPWorkbook
    """
    wb = GPWorkbook(filename)

    if theme is not None:
        wb.set_theme(theme)
    
    for sheet, gptable in sheets.items():
        ws = wb.add_worksheet(sheet)
        ws.write_gptable(gptable, auto_width)
    
    return wb

def write_workbook(
        filename,
        sheets,
        theme = None,
        auto_width = True,
#        cover_sheet = None
        ):

    """
    Writes a GPWorkbook to the specified file.

    This is an alternative main function that will take in data and theme
    information. It calls upon the packages to write a formatted ``.xlsx``
    file to the specified path.

    Parameters
    ----------
    filename : str
        Path to write final workbook to (an .xlsx file)
    sheets : dict
        A dictionary mapping worksheet labels to gptables.GPTable objects
    theme : gptables.Theme (optional)
        The formatting to be applied tot GPTable elements. gptheme is used by
        default
    auto_width : bool (optional)
        Select if column widths should be automatically determined. True by default.

    Returns
    -------
    None
    """
    wb = produce_workbook(filename, sheets, theme, auto_width)
    wb.close()
