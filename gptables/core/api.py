from gptables import GPWorkbook, GPTable

def produce_workbook(
        filename,
        sheets,
        theme = None,
        auto_width = True,
#      cover_sheet = None
        ):
    """
    Produces a GPWorkbook, ready to be written to the specified ``.xlsx`` using the `.close()` method.

    Parameters
    ----------
    filename : str
        Path to write final workbook to (an ``.xlsx`` file)
    sheets : dict
        A dictionary mapping worksheet labels to gptables.GPTable objects
    theme : gptables.Theme, optional)
        The formatting to be applied tot GPTable elements. gptheme is used by
        default
    auto_width : bool, optional)
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
    Writes a GPWorkbook to the specified ``.xlsx`` file.

    This is an alternative main function that will take in data and theme
    information. It calls upon the package to write a formatted ``.xlsx``
    file to the specified path.

    Parameters
    ----------
    filename : str
        Path to write final workbook to (an ``.xlsx`` file)
    sheets : dict
        A dictionary mapping worksheet labels to gptables.GPTable objects
    theme : gptables.Theme, optional
        The formatting to be applied tot GPTable elements. gptheme is used by
        default
    auto_width : bool, optional
        Select if column widths should be automatically determined. True by default.

    Returns
    -------
    None
    """
    wb = produce_workbook(filename, sheets, theme, auto_width)
    wb.close()


def quick_and_dirty_workbook(filename, tables, theme = None, auto_width = True):
    """
    Writes a list of tables to the specified ``.xlsx`` file, with no metadata.

    This function may be useful for creating simple outputs,
    with no Title, Notes or other associated metadata.

    Parameters
    ----------
    filename : str
        Path to write final workbook to (an .xlsx file)
    tables : list[pd.DataFrame]
        ordered tables to be written to file
    theme : gptables.Theme, optional
        The formatting to be applied tot GPTable elements. gptheme is used by
        default
    auto_width : bool, optional
        Select if column widths should be automatically determined. True by default.

    Returns
    -------
    None
    """
    sheets = dict()
    for table_n in range(len(tables)):
        sheets["Table " + str(table_n + 1)] = GPTable(tables[table_n], None, None, None, None)

    write_workbook(filename, sheets, theme = theme, auto_width = auto_width)
