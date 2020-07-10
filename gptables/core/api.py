import pandas as pd

from gptables import GPWorkbook, GPTable


def produce_workbook(
        filename,
        sheets,
        theme = None,
        auto_width = False,
        disable_footer_parentheses = False,
#      cover_sheet = None
        ):
    """
    Produces a GPWorkbook, ready to be written to the specified `.xlsx` file
    using the ``.close()`` method.

    Parameters
    ----------
    filename : str
        path to write final workbook to (an `.xlsx` file)
    sheets : dict
        mapping worksheet labels to gptables.GPTable objects
    theme : gptables.Theme, optional)
        formatting to be applied tot GPTable elements. gptheme is used by
        default
    auto_width : bool, optional
        indicate if column widths should be automatically determined. False
        by default.
    disable_footer_parentheses : bool, optional
        indicate if addition of parentheses to footer elements should be
        disabled. Note that disabling this decreases machine-readability.
        
    Returns
    -------
    workbook : gptables.GPWorkbook
    """
    wb = GPWorkbook(filename)

    if theme is not None:
        wb.set_theme(theme)
    
    for sheet, gptable in sheets.items():
        ws = wb.add_worksheet(sheet)
        ws.write_gptable(gptable, auto_width, disable_footer_parentheses)
    
    return wb


def write_workbook(
        filename,
        sheets,
        theme = None,
        auto_width = False,
        disable_footer_parentheses = False,
#        cover_sheet = None
        ):

    """
    Writes a GPWorkbook to the specified `.xlsx` file.

    This is an alternative main function that will take in data and theme
    information. It calls upon the package to write a formatted `.xlsx`
    file to the specified path.

    Parameters
    ----------
    filename : str
        Path to write final workbook to (an `.xlsx` file)
    sheets : dict
        mapping worksheet labels to ``GPTable`` objects
    theme : gptables.Theme, optional
        formatting to be applied tot GPTable elements. ``gptheme`` is used by
        default
    auto_width : bool, optional
        indicate if column widths should be automatically determined. False by default.
    disable_footer_parentheses : bool, optional
        indicate if addition of parentheses to footer elements should be
        disabled. Note that disabling this decreases machine-readability.

    Returns
    -------
    None
    """
    wb = produce_workbook(
        filename,
        sheets,
        theme,
        auto_width,
        disable_footer_parentheses
        )
    wb.close()


def quick_and_dirty_workbook(
    filename,
    tables,
    theme = None,
    auto_width = True
    ):
    """
    Writes a list of tables to the specified `.xlsx` file, with no metadata.

    This function may be useful for creating simple outputs,
    with no ``title``, ``notes`` or other associated metadata.
    Tables must be ``pandas.DataFrame`` objects with the row indexes
    in the first 1, 2 or 3 columns.

    Parameters
    ----------
    filename : str
        path to write final workbook to (an `.xlsx` file)
    tables : list[pandas.DataFrame]
        ordered tables to be written to file
    theme : gptables.Theme, optional
        formatting to be applied tot GPTable elements. ``gptheme`` is used by
        default
    auto_width : bool, optional
        indicate if column widths should be automatically determined. True by default.

    Returns
    -------
    None
    """
    sheets = dict()
    for table_n in range(len(tables)):
        current_table = tables[table_n]
        if not isinstance(current_table, pd.DataFrame):
            raise TypeError("All tables must be pandas.DataFrame objects")
        
        index_columns = dict()
        index_column_map = {
            0: {2: 0},
            1: {1: 0, 2: 1},
            2: {1: 0, 2: 1, 3: 2}
        }
        cols = current_table.shape[1]
        for n in range(min(cols, 3)):
            if any(current_table.iloc[:, n].apply(lambda x: isinstance(x, str))):
                index_columns.update(index_column_map[n])
            
        sheets["Table " + str(table_n + 1)] = GPTable(
            current_table,
            None,
            None,
            None,
            None,
            index_columns = index_columns
            )

    write_workbook(
        filename = filename,
        sheets = sheets,
        theme = theme,
        auto_width = auto_width,
        disable_footer_parentheses = True
        )
