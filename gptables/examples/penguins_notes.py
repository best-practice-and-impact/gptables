"""
Penguins - Notes Example
----------------------

This example demonstrates how to include notes in a GPTable. Notes cannot 
be included in data cells but may appear either in column headers or in text such 
as titles, subtitles, etc.

Placeholders for notes are put in using the notation, $$note$$. The actual note text 
must be provided as a Pandas dataframe to the notes_table argument of the ``gptables.write_workbook`` function.
This dataframe should contain the text of the placeholder, the actual text you want in the note and (optionally)
any hyperlinks you want in the note.
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

#Notes are added by using $$note$$ in text
penguins_title = "The Penguins Dataset$$noteabouty$$"
penguins_subtitles = [
    "This is the first subtitle$$noteaboutx$$",
    "Just another subtitle"
    ]

#Notes can also be included in column headers, see below
penguins_table_notes = {"species": "$$noteaboutx$$", 2: "$$noteaboutz$$"} #Columns can be referenced either by index or by name
penguins_units = {2:"mm", "bill_depth_mm":"mm",4:"mm","body_mass_g":"g"} #As above for column referencing
penguins_scope = "Penguins"
penguins_source = "Palmer Station, Antarctica"

kwargs = {
    "table_name": penguins_table_name,
    "title": penguins_title,
    "subtitles": penguins_subtitles,
    "units": penguins_units,
    "table_notes": penguins_table_notes,
    "scope": penguins_scope,
    "source": penguins_source,
    }

## Define our GPTable
penguins_table = gpt.GPTable(table=penguins_data, **kwargs)

penguins_sheets = {"Penguins": penguins_table}

# Notesheet - Note that the ordering of each list only matters with respect to the other lists in the "notes" dictionary. 
# GPTables will use the "Note reference" list to ensure the "Note text" is assigned correctly
notes = {
    "Note reference": ["noteaboutz", "noteaboutx", "noteabouty"],
    "Note text": ["This is a note about z linking to google.", "This is a note about x linking to duckduckgo.", "This is a note about y linking to the ONS website."],
    "Useful link": ["[google](https://www.google.com)", "[duckduckgo](https://duckduckgo.com/)", "[ONS](https://www.ons.gov.uk)"],
    }
penguins_notes_table = pd.DataFrame.from_dict(notes)

## Use write_workbook to win!
if __name__ == "__main__":
    output_path = parent_dir / "python_penguins_gptable.xlsx"
    gpt.write_workbook(
        filename=output_path, 
        sheets=penguins_sheets,
        notes_table=penguins_notes_table,
        contentsheet_options={"additional_elements": ["subtitles", "scope"]}
        )
    print("Output written at: ", output_path)
