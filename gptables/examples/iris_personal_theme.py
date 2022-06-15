"""
Iris - Minimal Example
----------------------

This example demonstrates use of the ``gptables.write_workbook`` function and how to add a personalised theme.
This API function is designed for production of consistently structured and formatted tables.

Summary statistics from the classic iris dataset are used to build a ``gptables.GPTable``
object. Elements of metadata are provided to the corresponding parameters of the class.
Where you wish to provide no metadata in required parameters, use ``None``.

Table formatting can be defined as a ``gptable.Theme``, which is passed to the API functions
 using the ``theme`` parameter. Or you can reply on our default - gptheme.
 
 The theme parameter must take either a directory or a yaml file in the ``gptables.write_workbook`` function. The yaml file used in this example can be found in the themes folder as ''iris_test_theme.yaml''.
 The personalised theme removes any bold or italics from the table. 
"""
import gptables as gpt
import pandas as pd
import numpy as np
from pathlib import Path

## Read data and arrange
parent_dir = Path(__file__).parent

iris_data = pd.read_csv(parent_dir / "iris.csv")
iris_data = iris_data.loc[:, ["class", "sepal_length", "sepal_width"]]

iris_summary = iris_data.groupby("class").agg(np.mean)
iris_summary.index = [_[5:].capitalize() for _ in iris_summary.index]
iris_summary.reset_index(inplace=True)
iris_summary.rename(
    columns={
        "index": "Class",
        "sepal_length": "Mean Sepal Length",
        "sepal_width": "Mean Sepal Width",
    },
    inplace=True,
    )

## Define table elements
table_name = "iris_statistics"
title = "Mean Iris$$note2$$ sepal dimensions"
subtitles = [
    "1936 Fisher, R.A; The use of multiple measurements in taxonomic problems$$note1$$",
    "Just another subtitle",
    ]
units = {1:"cm", 2:"cm"}
scope = "Iris"
source = "Source: Office for Iris Statistics"
index = {2: 0}  # Column 0 is a level 2 index

# or use kwargs to pass these to the appropriate parameters
kwargs = {
    "table_name": table_name,
    "title": title,
    "subtitles": subtitles,
    "units": units,
    "scope": scope,
    "source": source,
    "index_columns": index
    }

## Define our GPTable
iris_table = gpt.GPTable(table=iris_summary, **kwargs)

sheets = {"Iris Flower Dimensions": iris_table}

## Notesheet
notes = {
    "Note reference": ["note1", "note2"],
    "Note text": ["I've got 99 problems and taxonomy is one.",
                  "Goo Goo Dolls, 1998."],
    "Useful link": ["[google](https://www.google.com)", "[duckduckgo](https://duckduckgo.com/)"],
    }
notes_table = pd.DataFrame.from_dict(notes)

## Use write_workbook to win!
if __name__ == "__main__":
    output_path = parent_dir / "python_iris_theme_gptable.xlsx"
    theme_path = str(Path(__file__).parent.parent / "themes/iris_test_theme.yaml")
    gpt.write_workbook(
        filename=output_path,
        sheets={"Iris Flower Dimensions": iris_table},
        theme = gpt.Theme(theme_path),
        notes_table=notes_table,
        contentsheet_options={"additional_elements": ["subtitles", "scope"]}
        )
    print("Output written at: ", output_path)
