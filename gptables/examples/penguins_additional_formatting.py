"""
Penguins - Additional Formatting Example
------------------------------------

This example demonstrates additional formatting that is not supported in
the ``gptable.Theme``.

Specific columns, rows and cells of the table elements (indexes, column headings and data)
can be formatted using the ``gptable.GPTable(..., additional_formatting = ...)`` parameter.
This parameter takes a list of dictionaries, allowing you to select as many rows, columns
or cells as you like.

As with all formatting, supported arguments are desribed in the
`XlsxWriter documentation <https://xlsxwriter.readthedocs.io/format.html#format-methods-and-format-properties>`_.

Any formatting not possible through this means can be achieved using
``XlsxWriter`` `Workbook <https://xlsxwriter.readthedocs.io/workbook.html>`_
and `Worksheet <https://xlsxwriter.readthedocs.io/worksheet.html>`_ functionality.
A ``gptable.GPWorkbook`` object is returned when using the
``gptables.produce_workbook`` API function.
The ``GPWorkbook.worksheets()`` function returns a list of ``GPWorksheet`` objects,
which can also be modified.
"""

import gptables as gpt
import pandas as pd
import numpy as np
from pathlib import Path

## Read data and arrange
parent_dir = Path(__file__).parents[1]

penguins_data = pd.read_csv(parent_dir / "test/data/penguins.csv")

#Any data processing could go here as long as you end with a Pandas dataframe that you want to write in a spreadsheet

## Define table elements
penguins_table_name = "penguins_statistics"
penguins_title = "Penguins"

#Individual words/phrases can have formatting applied without the use of the additional_formatting argument
penguins_subtitles = [
    "The first subtitle",
    [{"bold": True}, "Just", " another subtitle"]
    ]
penguins_units = {key: "mm" for key in range(2,5)}
penguins_scope = "Penguins"

## Define additional formatting
# Columns can be referenced by name or number
# Rows may only be referenced by number
# Column and row numbers refer to the table elements, including indexes and column headings
penguins_additional_formatting = [
    {
        "column": {
            "columns": ["Species", "Island"],  # str, int or list of either
            "format": {"align": "center","italic":True}, #The "Species" and "Island" columns are centre-aligned and made italic
        }
    },
    {"column": {"columns": [3], "format": {"left": 1}}}, #Gives the fourth column a left border
    {
        "row": {
            "rows": -1,  # Numbers only, but can refer to last row using -1
            "format": {"bottom": 1, "indent":2},  # Give the last row a border at the bottom of each cell and indents two levels
        }
    },
    ]

kwargs = {
    "table_name": penguins_table_name,
    "title": penguins_title,
    "subtitles": penguins_subtitles,
    "units": penguins_units,
    "scope": penguins_scope,
    "source": None,
    "additional_formatting": penguins_additional_formatting,
    }

## Define our GPTable
penguins_table = gpt.GPTable(table=penguins_data, **kwargs)

## Use produce workbook to return GPWorkbook
if __name__ == "__main__":
    output_path = parent_dir / "python_penguins_additional_formatting_gptable.xlsx"
    wb = gpt.produce_workbook(
        filename=output_path, sheets={"Penguins": penguins_table}
        )

    # Carry out additional modifications on the GPWorkbook or GPWorksheets
    # This supports all `XlsxWriter` package functionality
    ws = wb.worksheets()[0]
    ws.set_row(0, 30)  # Set the height of the first row

    #To format cells using the set_row or set_column functions we must use a workbook to create a format object
    italic_format=wb.add_format({"italic":True})
    ws.set_column(2,3,10,italic_format) #Sets the width of the third and fourth column and makes them italic
    
    #Note that the first two arguments of set_column are the first and last columns (inclusive) you want to format as opposed
    #to set_row which only affects a single row at a time (the first argument).

    # Finally use the close method to save the output
    
    wb.close()
    print("Output written at: ", output_path)
    