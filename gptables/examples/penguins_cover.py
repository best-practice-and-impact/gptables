"""
Penguins - Cover Page
-----------------

This example demonstrates use of the ``gptables.Cover`` class to create a cover page. This example also 
demonstrates the usage of the ``index_columns``.

A gptables cover page contains a range of custom text elements, along with a hyperlinked table of contents.
Text elements are defined as a ``gptables.Cover`` instance, which is passed to the ``cover`` parameter of ``gptables.write_workbook()`` or ``gptables.produce_workbook()``.
"""

import gptables as gpt
import pandas as pd
import numpy as np
from pathlib import Path

## Read data
parent_dir = Path(__file__).parents[1]

penguins_data = pd.read_csv(parent_dir / "test/data/penguins.csv")

#Any data processing could go here as long as you end with a Pandas dataframe that you want to write in a spreadsheet

## Define table elements
penguins_table_name = "penguins_statistics"
penguins_title = "The Penguins Dataset"
penguins_subtitles = [
    "This is the first subtitle",
    "Just another subtitle"
    ]
penguins_scope = "Penguins"
penguins_source = "Palmer Station, Antarctica"

kwargs = {
    "table_name": penguins_table_name,
    "title": penguins_title,
    "subtitles": penguins_subtitles,
    "scope": penguins_scope,
    "source": penguins_source,
    "index_columns": {2: 0}  # The level 2 index from our Pandas dataframe is put in the first (zeroth with Python indexing) column of the spreadsheet
    }

## Define our GPTable
penguins_table = gpt.GPTable(table=penguins_data, table_name="penguins_statistics", **kwargs)

penguins_sheets = {
    "Penguins": penguins_table
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
    output_path = parent_dir / "python_penguins_cover_gptable.xlsx"
    gpt.write_workbook(
        filename=output_path,
        sheets=penguins_sheets,
        cover=penguins_cover,
    )
    print("Output written at: ", output_path)
