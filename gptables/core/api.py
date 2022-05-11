import warnings
import pandas as pd
from pathlib import Path

from gptables import GPWorkbook, GPTable


def produce_workbook(
        filename,
        sheets,
        theme = None,
        cover = None,
        contentsheet_label = "Contents",
        contentsheet_options = {},
        notes_table = None,
        notesheet_label = "Notes",
        notesheet_options = {},
        auto_width = True,
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
    theme : gptables.Theme, optional
        formatting to be applied to GPTable elements. gptheme is used by
        default
    cover : gptables.Cover, optional
        cover page text. Including this argument will generate a cover page
    contentsheet_label : str, None
        table of contents sheet label, defaults to "Contents"
        if None, table of contents will not be generated
    contentsheet_options : dict, optional
        dictionary of contentsheet customisation parameters
        valid keys are `additional_elements`, `column_names`,
        `table_name`, `title`, `subtitles`, `instructions`
    notes_table : None
        table with notes reference, text and (optional) link columns
        if None, notes sheet will not be generated
    notesheet_label : str
        notes sheet label, defaults to "Notes"
    notesheet_options : dict, optional
        dictionary of notesheet customisation parameters
        valid keys are `table_name`, `title`, `instructions`
    auto_width : bool, optional
        indicate if column widths should be automatically determined. True
        by default.
        
    Returns
    -------
    workbook : gptables.GPWorkbook
    """
    if isinstance(filename, Path):
        filename = filename.as_posix()

    wb = GPWorkbook(filename)

    if theme is not None:
        wb.set_theme(theme)

    if cover is not None:
        ws = wb.add_worksheet(cover.cover_label)
        ws.write_cover(cover)

    contentsheet = {}
    if contentsheet_label is not None:
        if contentsheet_options:
            valid_keys = ["additional_elements", "column_names",
                "table_name", "title", "subtitles", "instructions"]
            if not all(key in valid_keys for key in contentsheet_options.keys()):
                msg = ("Valid `contentsheet_options` keys are 'additional_elements',"
                    "'column_names', 'table_name', 'title', 'subtitles', 'instructions'")
                raise ValueError(msg)
        contents_gptable = wb.make_table_of_contents(sheets, **contentsheet_options)
        contentsheet = {contentsheet_label: contents_gptable}

    wb._update_annotations(sheets)

    notesheet = {}
    if notes_table is None:
        warnings.warn("No note text provided, notes sheet has not been generated")
    else:
        note_gptable = wb.make_notesheet(notes_table, **notesheet_options)
        notesheet = {notesheet_label: note_gptable}

    sheets = {**contentsheet, **notesheet, **sheets}     #TODO: add custom order from theme?
    for label, gptable in sheets.items():
        ws = wb.add_worksheet(label)
        ws.write_gptable(gptable, auto_width, wb._annotations)
    
    return wb


def write_workbook(
        filename,
        sheets,
        theme = None,
        cover = None,
        contentsheet = "Contents",
        contentsheet_options = {},
        notes_table = None,
        notesheet_label = "Notes",
        notesheet_options = {},
        auto_width = True,
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
    cover : gptables.Cover, optional
        cover page text. Including this argument will generate a cover page
    contentsheet : str, False
        table of contents sheet label, defaults to "Contents"
        if False, table of contents will not be generated
    contentsheet_options : dict, optional
        dictionary of contentsheet customisation parameters
        valid keys are `additional_elements`, `column_names`,
        `table_name`, `title`, `subtitles`, `instructions`
    notesheet : gptables.Notesheet, optional
        notes page content. Including this argument will generate a notes page
    auto_width : bool, optional
        indicate if column widths should be automatically determined. True by default.

    Returns
    -------
    None
    """
    wb = produce_workbook(
        filename,
        sheets,
        theme,
        cover,
        contentsheet,
        contentsheet_options,
        notes_table,
        notesheet_label,
        notesheet_options,
        auto_width
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
            f"Table{table_n + 1}",
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
        auto_width = auto_width
        )
