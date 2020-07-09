"""
Cost of Reoffending - Multiple Sheets Example
---------------------------------------------

This example demonstrates how multiple sheets can be defined and written
to a single .xlsx file using ``gptables``.

The elements dictionary below is used to define the metadata for each table,
with the sheet name as it's key. This metadata is used to generate the sheets
dictionary. ``gptables.write_workbook`` uses this dictionary to write each table
to the corresponding sheet.

``gptables.GPTable`` objects can be constructed one by one, but this demonstrates
one way to make this definition concise.
"""
import gptables as gpt
import pandas as pd
import os


## Read data and arrange
parent_dir = os.path.dirname(os.path.realpath(__file__))
core_data = pd.read_csv(parent_dir + "\coreB.csv")

# 3 tables: summary, children and young people, and adults
summ = core_data.loc[:,['age','total_cost']]
summ = summ.groupby('age').sum().reset_index()

# This returns adults first as per the data
ages = core_data.age.unique()

dct = {ages[0]: pd.DataFrame(), ages[1]: pd.DataFrame()}
for key in dct:
    frame = core_data.loc[core_data.age == key, ["reoffence_group", "total_cost"]]
    frame = frame.groupby("reoffence_group").sum().reset_index()
    dct[key] = frame

dct['summary'] = summ


## Define table elements for each table

example = {
            "title": "Cost of Reoffending",
            "subtitles": ["12-month follow-up period for the 2016 offender cohort"],
            "units": "£",
            "scope": "England and Wales",
            "source": "Office for National Statistics"
        }

elements = {
    'summary': example,
    'Adults': example,
    'Children and young people': example
    }

## Generate a dictionary of sheet names to GPTable objects
## using the elements defined above
sheets = {name: gpt.GPTable(dct[name], **elements[name]) for name in dct}

## Use write_workbook to win!
output_path = parent_dir + "\python_cor_multiple_gptables.xlsx"
gpt.write_workbook(
        filename = output_path,
        sheets = sheets
        )
print("Output written at: ", output_path)
