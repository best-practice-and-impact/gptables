"""
Penguins - Minimal Example
----------------------

This example demonstrates  another way to use the ``gptables.write_workbook`` function.
This code is equivalent to that in the above example.
"""

import gptables as gpt
import pandas as pd
import numpy as np
from pathlib import Path

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
penguins_source = "Palmer Station, Antarctica"

#Use kwargs to pass these to the appropriate parameters
kwargs = {
    "table_name": penguins_table_name,
    "title": penguins_title,
    "subtitles": penguins_subtitles,
    "scope": penguins_scope,
    "source": penguins_source,
    }

penguins_table = gpt.GPTable(table=penguins_data, **kwargs)

#Every table must be associated to a sheet name for writing
penguins_sheets = {"Penguins": penguins_table}

## Use write_workbook to win!
if __name__ == "__main__":
    output_path = parent_dir / "python_penguins_gptable.xlsx"
    gpt.write_workbook(
        filename=output_path, 
        sheets=penguins_sheets,
        contentsheet_options={"additional_elements": ["subtitles", "scope"]}
        )
    print("Output written at: ", output_path)
