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
from pathlib import Path
from copy import deepcopy

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
title = "Mean Iris$$note2$$ sepal dimensions"
subtitles = [
    "1936 Fisher, R.A; The use of multiple measurements in taxonomic problems$$note1$$",
    "Just another subtitle",
    ]
units = {"Mean Sepal Length": "cm", "Mean Sepal Width": "cm"}
scope = "Iris"
source = "Source: Office for Iris Statistics"
index = {2: 0}  # Column 0 is a level 2 index

# or use kwargs to pass these to the appropriate parameters
kwargs = {
    "title": title,
    "subtitles": subtitles,
    "units": units,
    "scope": scope,
    "source": source,
    "index_columns": index,
    }

## Define our GPTable
iris_table = gpt.GPTable(table=iris_summary, table_name="iris_statistics", **kwargs)

iris_table_copy = deepcopy(iris_table)
iris_table_copy.set_title("A copy of the first sheet$$note3$$")
iris_table_copy.set_table_name("iris_statistics_copy")

sheets = {
    "Iris Flower Dimensions": iris_table,
    "Copy of Iris Flower Dimensions": iris_table_copy
}

cover = gpt.Cover(
    cover_label="Cover",
    title="A Workbook containing good practice tables",
    intro=["This is some introductory information", "And some more"],
    about=["Even more info about my data", "And a little more"],
    contact=["John Doe", "Tel: 345345345", "Email: [john.doe@snailmail.com](mailto:john.doe@snailmail.com)"],
    )

## Notesheet
notes = {
    "Note reference": ["note1", "note2", "note3"],
    "Note text": ["I've got 99 problems and taxonomy is one.", "Goo Goo Dolls, 1998.", "This is an extra note"],
    }
notes_table = pd.DataFrame.from_dict(notes)

## Use write_workbook to win!
if __name__ == "__main__":
    output_path = parent_dir / "python_iris_cover_gptable.xlsx"
    gpt.write_workbook(
        filename=output_path,
        sheets=sheets,
        cover=cover,
        notes_table=notes_table
    )
    print("Output written at: ", output_path)
