"""
Penguins - Cover Page
-----------------

This example demonstrates use of the ``gptables.Cover`` class to create a cover page. This example also 
demonstrates how to create a workbook with multiple sheets.

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

## Read data
parent_dir = Path(__file__).parent

penguins_data = pd.read_csv(parent_dir / "penguins.csv")

#Any data processing could go here as long as you end with a Pandas dataframe that you want to write in a spreadsheet

## Define table elements
penguins_table_name = "penguins_statistics"
penguins_title = "The Penguins Dataset"
penguins_subtitles = [
    "This is the first subtitle",
    "Just another subtitle"
    ]
penguins_scope = "Penguins"
penguins_source = "Source: Office for Penguin Statistics"

# or use kwargs to pass these to the appropriate parameters
kwargs = {
    "table_name": penguins_table_name,
    "title": penguins_title,
    "subtitles": penguins_subtitles,
    "scope": penguins_scope,
    "source": penguins_source,
    }

## Define our GPTable
penguins_table = gpt.GPTable(table=penguins_data, table_name="penguins_statistics", **kwargs)

penguins_table_copy = deepcopy(penguins_table)
penguins_table_copy.set_title("A copy of the first sheet")
penguins_table_copy.set_table_name("penguins_statistics_copy") #All tables in a single workbook must have a unique name

penguins_sheets = {
    "Penguins": penguins_table,
    "Copy of Penguins": penguins_table_copy
}

penguins_cover = gpt.Cover(
    cover_label="Cover",
    title="A Workbook containing two copies of the data",
    intro=["This is some introductory information", "And some more"],
    about=["Even more info about my data", "And a little more"],
    contact=["John Doe", "Tel: 345345345", "Email: [john.doe@snailmail.com](mailto:john.doe@snailmail.com)"],
    )

## Use write_workbook to win!
if __name__ == "__main__":
    output_path = parent_dir / "python_iris_cover_gptable.xlsx"
    gpt.write_workbook(
        filename=output_path,
        sheets=penguins_sheets,
        cover=penguins_cover,
    )
    print("Output written at: ", output_path)
