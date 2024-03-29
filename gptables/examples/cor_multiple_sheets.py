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
from copy import deepcopy
import gptables as gpt
import pandas as pd
from pathlib import Path

## Read data and arrange
parent_dir = Path(__file__).parent
core_data = pd.read_csv(parent_dir / "coreB.csv")

# 3 tables: summary, children and young people, and adults
summ = core_data.loc[:, ["age", "total_cost"]]
summ = summ.groupby("age").sum().reset_index()
summ.columns = ["Age group", "Total cost"]

# This returns adults first as per the data
ages = core_data.age.unique()

dct = {ages[0]: pd.DataFrame(), ages[1]: pd.DataFrame()}
for key in dct:
    frame = core_data.loc[core_data.age == key, ["reoffence_group", "total_cost"]]
    frame = frame.groupby("reoffence_group").sum().reset_index()
    frame.columns = ["Reoffence group", "Total cost"]
    dct[key] = frame

dct["Summary"] = summ


## Define table elements for each table

example = {
    "title": "Cost of Reoffending",
    "subtitles": ["12-month follow-up period for the 2016 offender cohort"],
    "units": {1:"£"},
    "scope": "England and Wales",
    "source": "Office for National Statistics",
}

table_parameters_dict = {}
for table in ["summary", "adults", "children"]:
    table_parameters = deepcopy(example)
    table_parameters["table_name"] = f"{table}_table"
    table_parameters["title"] = f"Cost of reoffending - {table}"
    table_parameters_dict[table] = table_parameters

elements = {
    "Summary": table_parameters_dict["summary"], 
    "Adults": table_parameters_dict["adults"], 
    "Children and young people": table_parameters_dict["children"]
}

## Generate a dictionary of sheet names to GPTable objects
## using the elements defined above
sheets = {name: gpt.GPTable(dct[name], **elements[name]) for name in dct}

## Use write_workbook to win!
if __name__ == "__main__":
    output_path = parent_dir / "python_cor_multiple_gptables.xlsx"
    gpt.write_workbook(filename=output_path, sheets=sheets)
    print("Output written at: ", output_path)
