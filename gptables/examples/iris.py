"""
Iris - Minimal Example
----------------------

This example demonstrates use of the ``gptables.write_workbook`` function.
This API function is designed for production of consistently structured and formatted tables.

Summary statistics from the classic iris dataset are used to build a ``gptables.GPTable``
object. Elements of metadata are provided to the corresponding parameters of the class.
Where you wish to provide no metadata in required parameters, use ``None``.

Table formatting can be defined as a ``gptable.Theme``, which is passed to the API functions
 using the ``theme`` parameter. Or you can reply on our default - gptheme.
"""
import gptables as gpt
import pandas as pd
import numpy as np
import os


## Read data and arrange
funcs = [np.mean, np.median]
parent_dir = os.path.dirname(os.path.realpath(__file__))

iris_data = pd.read_csv(parent_dir + "/iris.csv")
iris_data = iris_data.loc[:, ["class", "sepal_length", "sepal_width"]]

iris_summary = iris_data.groupby("class").agg(np.mean)
iris_summary.index = [_[5:].capitalize() for _ in iris_summary.index]
iris_summary.rename(
        columns={
            "class":"class",
            "sepal_length":"Mean Sepal Length",
            "sepal_width":"Mean Sepal Width"
            }, 
        inplace=True
        )

# Drop index into table
iris_summary.reset_index(inplace=True)

# Insert NA to demonstrate missing value representation
iris_summary.iloc[1, 1] = np.nan

## Define table elements
title = ["Mean", {"italic": True}, " Iris", "$$note2$$ sepal dimensions"]
subtitles = [
        "1936 Fisher, R.A; The use of multiple measurements in taxonomic problems$$note1$$",
        "Just another subtitile"
        ]
units = "cm"
scope = "Iris"
source = "Source: Office for Iris Statistics"
index = {2: 0}  # Column 0 is a level 2 index
annotations = {
        "note1": "I've got 99 problems and taxonomy is one.",
        "note2": "Goo Goo Dolls, 1998."
        }
notes = [
        "This note hath no reference."
        ]

# or use kwargs to pass these to the appropriate parameters
kwargs = {"title": title,
        "subtitles": subtitles,
        "units": units,
        "scope": scope,
        "source": source,
        "index_columns": index,
        "annotations": annotations,
        "notes": notes
        }

## Define our GPTable
iris_table = gpt.GPTable(
        table = iris_summary,
        **kwargs
        )        

## Use write_workbook to win!
output_path = parent_dir + "/python_iris_gptable.xlsx"
gpt.write_workbook(
        filename = output_path,
        sheets = {"iris flower dimensions": iris_table}
        )
print("Output written at: ", output_path)
