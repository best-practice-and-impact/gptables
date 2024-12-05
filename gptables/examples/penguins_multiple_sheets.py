"""
Penguins - Multiple Pages
-----------------

This example demonstrates how to create a workbook with multiple sheets. Note that it
will auto-generate a table of contents.
"""

import gptables as gpt
import pandas as pd
import numpy as np
from pathlib import Path
from copy import deepcopy

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
    "source": penguins_source
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

## Use write_workbook to win!
if __name__ == "__main__":
    output_path = parent_dir / "python_penguins_cover_gptable.xlsx"
    gpt.write_workbook(
        filename=output_path,
        sheets=penguins_sheets
    )
    print("Output written at: ", output_path)
