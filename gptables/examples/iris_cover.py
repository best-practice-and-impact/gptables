"""
Iris - Cover Page
-----------------

This example demonstrates use of the ``gptables.Cover`` class to create a cover page.

A gptables cover pages contain a range of custom text elements, along with a hyperlinked table of contents.
Text elements are defined as a ``gptables.Cover`` instance, which is passed to the ``cover`` parameter of ``gptables.write_worbook()`` or ``gptables.produce_worbook()``.
In this example, we have also set ``auto_width`` to ``True``.
This automatically determines the width of the first column on the cover sheet, as well as all columns of the tables of the workbook.
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

cover = gpt.Cover(
        cover_label = "Notes",
        title = "My book of tables",
        intro = ["This is some introductory information", "And some more"],
        about = ["Even more info about my data", "And a little more"],
        contact = ["John Doe", "Tel: 345345345"],
        additional_elements = ["subtitles", "scope", "source", "notes"]
        )

## Use write_workbook to win!
output_path = parent_dir + "/python_iris_cover_gptable.xlsx"
gpt.write_workbook(
        filename = output_path,
        sheets = {"iris flower dimensions": iris_table},
        cover = cover,
        auto_width=True,
        )
print("Output written at: ", output_path)