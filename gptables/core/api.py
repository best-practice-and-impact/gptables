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
        gridlines = "hide_all",
        cover_gridlines = False
        ):
    """
    Produces a GPWorkbook, ready to be written to the specified `.xlsx` file
    using the ``.close()`` method.

    Parameters
    ----------
    filename : str
        path to write final workbook to (an `.xlsx` file)
    sheets : dict
        mapping worksheet labels to ``GPTable`` objects
    theme : gptables.Theme, optional
        formatting to be applied to GPTable elements. ``gptheme`` is used by
        default.
    cover : gptables.Cover, optional
        cover page text. Including this argument will generate a cover page.
    contentsheet_label : str
        table of contents sheet label, defaults to "Contents". If None, table
        of contents will not be generated.
    contentsheet_options : dict, optional
        dictionary of contentsheet customisation parameters. Valid keys are
        `additional_elements`, `column_names`, `table_name`, `title`,
        `subtitles` and `instructions`.
    notes_table : pd.DataFrame, optional
        table with notes reference, text and (optional) link columns. If None,
        notes sheet will not be generated.
    notesheet_label : str, optional
        notes sheet label, defaults to "Notes"
    notesheet_options : dict, optional
        dictionary of notesheet customisation parameters. Valid keys are
        `table_name`, `title` and `instructions`.
    auto_width : bool, optional
        indicate if column widths should be automatically determined. True
        by default.
    gridlines : string, optional
        option to hide or show gridlines on worksheets. "show_all" - don't 
        hide gridlines, "hide_printed" - hide printed gridlines only, or 
        "hide_all" - hide screen and printed gridlines.
    cover_gridlines : bool, optional
        indication if gridlines should apply to the cover worksheet. False 
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
        if cover_gridlines:
            ws = wb.add_worksheet(cover.cover_label, gridlines=gridlines)
        else:
            ws = wb.add_worksheet(cover.cover_label, gridlines="hide_all")
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

    sheets = {**contentsheet, **notesheet, **sheets}
    for label, gptable in sheets.items():
        ws = wb.add_worksheet(label, gridlines=gridlines)
        ws.write_gptable(gptable, auto_width, wb._annotations)
    
    return wb


def write_workbook(
        filename,
        sheets,
        theme = None,
        cover = None,
        contentsheet = None,
        contentsheet_label = "Contents",
        contentsheet_options = {},
        notes_table = None,
        notesheet_label = "Notes",
        notesheet_options = {},
        auto_width = True,
        gridlines = "hide_all",
        cover_gridlines = False
        ):

    """
    Writes a GPWorkbook to the specified `.xlsx` file.

    This is an alternative main function that will take in data and theme
    information. It calls upon the package to write a formatted `.xlsx`
    file to the specified path.

    .. note:: Deprecated in v1.1.0: `contentsheet` will be removed
        in v2, it is replaced by `contentsheet_label`

    Parameters
    ----------
    filename : str
        Path to write final workbook to (an `.xlsx` file)
    sheets : dict
        mapping worksheet labels to ``GPTable`` objects
    theme : gptables.Theme, optional
        formatting to be applied to GPTable elements. ``gptheme`` is used by
        default.
    cover : gptables.Cover, optional
        cover page text. Including this argument will generate a cover page.
    contentsheet_label : str
        table of contents sheet label, defaults to "Contents". If None, table
        of contents will not be generated.
    contentsheet_options : dict, optional
        dictionary of contentsheet customisation parameters. Valid keys are
        `additional_elements`, `column_names`, `table_name`, `title`,
        `subtitles` and `instructions`
    note_table : pd.DataFrame, optional
        table with notes reference, text and (optional) link columns. If None,
        notes sheet will not be generated.
    notesheet_label : str, optional
        notes sheet label, defaults to "Notes"
    notesheet_options : dict, optional
        dictionary of notesheet customisation parameters. Valid keys are
        `table_name`, `title` and `instructions`.
    auto_width : bool, optional
        indicate if column widths should be automatically determined. True by
        default.
    gridlines : string, optional
        option to hide or show gridlines on worksheets. "show_all" - don't 
        hide gridlines, "hide_printed" - hide printed gridlines only, or 
        "hide_all" - hide screen and printed gridlines.
    cover_gridlines : bool, optional
        indication if gridlines should apply to the cover worksheet. False 
        by default.
    contentsheet : str
        alias for contentsheet_label, deprecated in v1.1.0

    Returns
    -------
    None
    """
    if contentsheet is not None:
        contentsheet_label = contentsheet

    wb = produce_workbook(
        filename,
        sheets,
        theme,
        cover,
        contentsheet_label,
        contentsheet_options,
        notes_table,
        notesheet_label,
        notesheet_options,
        auto_width,
        gridlines,
        cover_gridlines
        )
    wb.close()
