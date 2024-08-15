

import gptables as gpt
import pandas as pd
import numpy as np
from pathlib import Path

## Read data and arrange
parent_dir = Path(__file__).parent

iris_data = pd.read_csv(parent_dir / "iris.csv")

iris_data.rename(
    columns={
        "class": "class",
        "sepal_length": "Sepal Length",
        "petal_length": "Petal Length",
        "petal_width": "Petal Width",
        "sepal_width": "Sepal Width",
    },
    inplace=True,
    )

iris_data["class"] = iris_data.apply(lambda row: row["class"][5:].capitalize(), axis=1)

# Calculate summaries
subtables = []
funcs = [np.mean, np.median]
for func in funcs:
    subtables.append(iris_data.groupby("class").agg(func))
    subtables.append(pd.DataFrame(iris_data.iloc[:,0:4].agg(func).rename("All")).T)
iris_summary = pd.concat(subtables)
iris_summary["Average"] = ["Mean"] * 4 + ["Median"] * 4

# Reshape
iris_summary = iris_summary.reset_index()
iris_summary = iris_summary.melt(["index", "Average"], var_name="Iris feature")
iris_summary = iris_summary.pivot_table(
    index=["Iris feature", "Average"], columns="index", values="value"
    ).reset_index()

## Define table elements
table_name = "iris_statistics"
title = "Iris flower dimensions"
subtitles = [
    [{"font_name": "Chiller"}, "The", {"font_size": 30}, " first", {"font_color": "red"}, " subtitle"],
    [{"bold": True}, "The", {"italic": True}, " second", {"underline": True}, " subtitle"],
    [{"font_script": 1}, "Ignore", {"font_script": 2}, " this"],
    [{"font_strikeout": True}, "bye", " "] 
     ]   # checking font formatting 
units = {key: "cm" for key in range(2,6)}
scope = "Iris"
index = {1: 0, 2: 1}

# Additional formatting

additional_formatting = [
    {
        "column": {
            "columns": ["Setosa", "Versicolor"], 
            "format": {"align": "vcenter"}, #checking vertical alignment
            "include_names": False, 
        }
    },
    {"column": {"columns": [0], "format": {"indent": 2, "rotation": 90}, "include_names": True}}, #checking alignment formatting
    {
        "row": {
            "rows": -1, 
            "format": {"bottom": 1, "top": 2, "bottom_color": "blue", "top_color": "yellow",
                       "pattern": 6, "bg_color": "lime", "fg_color": "pink"}, # checking pattern formatting
        }
    },
    {
        "row": {
            "rows": 3,
            "format": {"num_format": 3, "locked": True, "left": 3, "left_color": "navy"}, #checking number & protection formatting
        }
    },
    {
        "row": {
            "rows": 5,
            "format": {"num_format": "0.00", "right": 2, "right_color": "silver"}, #checking number formatting
        }
    },
    {
        "cell": {
            "cells": (1,1),
            "format": {"text_wrap": True},
        }
    }
    ]

# or just use kwargs
kwargs = {
    "table_name": table_name,
    "title": title,
    "subtitles": subtitles,
    "units": units,
    "scope": scope,
    "source": None,
    "index_columns": index,
    "additional_formatting": additional_formatting,
    }

## Define our GPTable
iris_table = gpt.GPTable(table=iris_summary, **kwargs)

## Use produce workbook to return GPWorkbook
if __name__ == "__main__":
    output_path = parent_dir / "test_additional_formatting_gptable.xlsx"
    wb = gpt.produce_workbook(
        filename=output_path, sheets={"Iris Flower Dimensions": iris_table}
        )

    # Carry out additional modifications on the GPWorkbook or GPWorksheets
    # This supports all `XlsxWriter` package functionality
    ws = wb.worksheets()[0]
    ws.set_row(0, 30)  # Set the height of the first row

    # Finally use the close method to save the output
    wb.close()
    print("Output written at: ", output_path)