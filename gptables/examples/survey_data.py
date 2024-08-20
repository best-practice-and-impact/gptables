"""
Labour market overview, UK: December 2020 - Real Survey Data Example
--------------------------------------------------------------------
This example demonstrates how to replicate the Labour Market overview accessible 
example found at https://analysisfunction.civilservice.gov.uk/policy-store/further-resources-for-releasing-statistics-in-spreadsheets/
"""

import gptables as gpt
import pandas as pd
import numpy as np
from pathlib import Path

## Read data and arrange
parent_dir = Path(__file__).parent

labour_market_data = pd.read_csv(parent_dir / "survey_data.csv")
labour_market_data.dropna(axis=0, how="all", inplace=True) # Remove empty rows in the data
labour_market_data.dropna(axis=1, how="all", inplace=True) # Remove columns rows in the data
col_names = ["Time period and dataset code row",
             "Number of people", 
             "Economically active",
             "Employment level",
             "Unemployment level",
             "Economically inactive",
             "Economically active rate",
             "Employment rate",
             "Unemployment rate",
             "Economically inactive rate"]
labour_market_data.columns = col_names


## Define table elements
table_name = "Labour_market_overview_accessibility_example_Nov21"
title = "Number and percentage of population aged 16 and over in each labour market activity group, UK, seasonally adjusted"
subtitles = [
    "This worksheet contains one table. Some cells refer to notes which can be found on the notes worksheet."
    ]
units = {1:"thousands", 2:"thousands", 3:"thousands", 4:"thousands",
         5:"thousands", 6:"%", 7:"%", 8:"%", 9:"%"}
table_notes = {2:"$$note 1$$", 3:"$$note 2$$", 4:"$$note 2$$",5: "$$note 3$$",
               7:"$$note 4$$", 8:"$$note 4$$", 9:"$$note 4$$"}
scope = "Labour Market"
source = "Source: Office for National Statistics"
index = {2: 0}  # Column 0 is a level 2 index
additional_formatting = [{
        "row": {
            "rows": [1],
            "format": {"bold": True, "font_size": 14},
        }
    }]


# or use kwargs to pass these to the appropriate parameters
kwargs = {
    "table_name": table_name,
    "title": title,
    "subtitles": subtitles,
    "units": units,
    "table_notes": table_notes,
    "scope": scope,
    "source": source,
    "index_columns": index,
    "additional_formatting": additional_formatting,
    }


## Define our GPTable
survey_table = gpt.GPTable(table=labour_market_data, **kwargs)

sheets = {"sheet 1a": survey_table}

cover = gpt.Cover(
    cover_label="Cover",
    title="Labour market overview data tables, UK, December 2020 (accessibility example)",
    intro=["This spreadsheet contains a selection of the data tables published alongside the Office for National Statistics' Labour market overview for December 2020. We have edited these data tables and the accompanying cover sheet, table of contents and notes worksheet to meet the legal accessibility regulations. It is intended to be an example of an accessible spreadsheet. The data tables and accompanying information have not been quality assured. Please see the original statistical release if you are looking for accurate data.",
           "[Labour market overview, UK: December 2020](https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/bulletins/uklabourmarket/december2020)"],
    about=[[{"bold": True, "font_size": 14}, "Publication dates"],
           "This data tables in this spreadsheet were originally published at 7:00am 15 December 2020",
           "The next publication was published at 7:00am 26 January 2021.",
           [{"bold": True, "font_size": 14}, "Note on weighting methodology"],
           "Due to the coronavirus (COVID19) pandemic, all face to face interviewing for the Labour Force Survey was suspended and replaced with telephone interviewing. This change in mode for first interviews has changed the non-response bias of the survey, affecting interviews from March 2020 onwards. All data included in this spreadsheet have now been updated and are based on latest weighting methodology.",
           "More information about the impact of COVID19 on the Labour Force Survey",
           "Dataset identifier codes",
           "The four-character identification codes appearing in the tables are the ONS' references for the data series.",
           [{"bold": True, "font_size": 14}, "Comparing quarterly changes"],
           "When comparing quarterly changes ONS recommends comparing with the previous non-overlapping three-month average time period, for example, compare Apr to Jun with Jan to Mar, not with Mar to May.",
           [{"bold": True, "font_size": 14}, "Units, notes and no data"],
           "Some cells in the tables refer to notes which can be found in the notes worksheet. Note markers are presented in square brackets, for example: [note 1].",
           "Some cells have no data, when this is the case the words 'no data' are presented in square brackets, for example: '[no data]'. An explanation of why there is no data is given in the notes worksheet, see the column headings for which notes you should refer to.",
           "Some column headings give units, when this is the case the units are presented in round brackets to differentiate them from note markers.",
           [{"bold": True, "font_size": 14}, "Historic publication dates for labour market statistics", " "],
           "The monthly labour market statistics release was first published in April 1998. Prior to April 1998 there was no integrated monthly release and the Labour Force Survey estimates were published separately, on different dates, from other labour market statistics. From April 2018 the usual publication day for the release was changed from Wednesday to Tuesday.",
           [{"bold": True, "font_size": 14}, "More labour market data"],
           "Other labour market datasets are available on the ONS website.",
           "Labour market statistics time series dataset on the ONS website."
    ],
    contact=["Tel: 01633455400", "Email: [labour.market@ons.gov.uk](mailto:labour.market@ons.gov.uk)"],
)

## Notesheet
notes_table = pd.read_csv(parent_dir / "survey_data_notes.csv")
notes_table.dropna(axis=0, how="all", inplace=True) # Remove empty rows in the data
notes_table.dropna(axis=1, how="all", inplace=True) # Remove columns rows in the data
notes_table.columns = ['Note reference', 'Note text']

## Use write_workbook to win!
if __name__ == "__main__":
    output_path = parent_dir / "python_survey_data_gptable.xlsx"
    gpt.write_workbook(
        filename=output_path, 
        sheets=sheets,
        cover=cover,
        notes_table=notes_table,
        contentsheet_options={"additional_elements": ["subtitles", "scope"]},
        auto_width=True,
        gridlines="show_all",
        cover_gridlines=True
        )
    print("Output written at: ", output_path)