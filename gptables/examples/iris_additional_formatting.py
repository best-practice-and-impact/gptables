"""
Iris - Additional Formatting Example
------------------------------------

This example demonstrates additional formatting that is not supported in
the ``gptable.Theme``.

Specific columns, rows and cells of the table elements (indexes, column headings and data)
can be formatted using the ``gptable.GPTable(..., additional_formatting = ...)`` parameter.
This parameter takes a list of dictionaries, allowing you to select as many rows, columns
or cells as you like.

As with all formatting, supported arguments are desribed in the
`XlsxWriter documentation <https://xlsxwriter.readthedocs.io/format.html#format-methods-and-format-properties>`_.

Any formatting not possibly through this means can be achieved using
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
import os


## Read data and arrange
funcs = [np.mean, np.median]
parent_dir = os.path.dirname(os.path.realpath(__file__))
iris_data = pd.read_csv(parent_dir + "/iris.csv")

iris_data.rename(
        columns={
            "class":"class",
            "sepal_length":"Sepal Length",
            "petal_length":"Petal Length",
            "petal_width":"Petal Width",
            "sepal_width":"Sepal Width"
            }, 
        inplace=True
        )

iris_data["class"] = iris_data.apply(
        lambda row: row["class"][5:].capitalize(),
        axis=1)

# Calculate summaries
subtables = []
for func in funcs:
    subtables.append(iris_data.groupby("class").agg(func))
    subtables.append(pd.DataFrame(iris_data.agg(func).rename("All")).T)

iris_summary = pd.concat(subtables)
iris_summary["func"] = ["Mean"] * 4 + ["Median"] * 4

# Reshape
iris_summary = iris_summary.reset_index()
iris_summary = iris_summary.melt(["index", "func"])
iris_summary = iris_summary.pivot_table(
        index=["variable", "func"],
        columns="index",
        values="value"
        ).reset_index()

## Define table elements
title = "Iris flower dimensions"
subtitles = [
        "1936 Fisher, R.A; The use of multiple measurements in taxonomic problems",
        "Just another subtitile"
        ]
units = "cm"
scope = "Iris"
index = {
        1: 0,
        2: 1
        }

## Define additional formatting
# Columns can be references by name or number
# Rows may only be referenced by number
# Column and row numbers refer to the table elements, including indexes and column headings
additional_formatting = [
        {"column":
            {"columns": ["Setosa", "Versicolor"],  # str, int or list of either
             "format": {"align": "center"},
             "include_names": False  # Whether to include column headings (optional)
            }
        },
        {"column":
            {"columns": [3],
             "format": {"left": 1},
             "include_names": True
            }
        },
        {"row":
            {"rows": -1,  # Numbers only, but can refer to last row using -1
             "format": {"bottom": 1},  # Underline row
             "include_names": True  # Whether to include row indexes
             }
        },
        {"cell":
            {"cells": (3, 3),  # tuple or list of tuples
             "format": {"font_color": "red"}
                }
        }
]

# or just use kwargs
kwargs = {
        "title": title,
        "subtitles": subtitles,
        "units": units,
        "scope": scope,
        "source": None,
        "index_columns": index,
        "additional_formatting": additional_formatting
        }

## Define our GPTable
iris_table = gpt.GPTable(
        table = iris_summary,
        **kwargs
        )        

## Use produce workbook to return GPWorkbook
output_path = parent_dir + "/python_iris_additional_formatting_gptable.xlsx"
wb = gpt.produce_workbook(
        filename = output_path,
        sheets = {"iris flower dimensions": iris_table}
        )

# Carry out additional modifications on the GPWorkbook or GPWorksheets
# This supports all `XlsxWriter` package functionality
ws = wb.worksheets()[0]
ws.set_row(0, 30)  # Set the height of the first row

# Finally use the close method to save the output
wb.close()
print("Output written at: ", output_path)

