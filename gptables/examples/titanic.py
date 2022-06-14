"""
gptables example using the Titanic dataset.
@author: Ramiz Farishta
"""

import gptables as gpt
import pandas as pd
import numpy as np
from pathlib import Path

parent_dir = Path(__file__).parent
titanic = pd.read_csv(parent_dir / "titanic.csv")

titanic["Child"] = np.where(titanic["Age"] < 18, 1, 0)

sex_survived = titanic.groupby("Sex")["Survived"].sum()
sex_pclass = titanic.groupby("Sex")["Pclass"].apply(lambda x: x.mode().iloc[0])
sex_child = titanic.groupby("Sex")["Child"].sum()
sex_fare = titanic.groupby("Sex")["Fare"].mean()

titanic_analysis = pd.DataFrame(
    {
        "Survived": sex_survived,
        "Pclass": sex_pclass,
        "Child": sex_child,
        "Fare": sex_fare,
    }
).reset_index()

table_name = "titanic_by_sex"
title = "Titanic$$note2$$ analysis by sex"
subtitles = ["Derived from a Kaggle competition dataset$$note1$$"]
units = {"Survived": "sum$$note3$$", 2: "mode", 3: "sum", "Fare": "mean"}
scope = "Titanic$$note2$$"
source = "Source: Kaggle"
index = {2: 0}

kwargs = {
    "table_name": table_name,
    "title": title,
    "subtitles": subtitles,
    "units": units,
    "scope": scope,
    "source": source,
    "index_columns": index,
    }

# define our GPTable
titanic_table = gpt.GPTable(table=titanic_analysis, **kwargs)

sheets = {"titanic analysis by sex": titanic_table}

## Notesheet
notes = {
    "Note reference": ["note1", "note2", "note3", "note4"],
    "Note text": ["www.kaggle.com/titanic",
                  "Celine Dion.",
                  "Total count.",
                  "This note hath no reference."],
    }
notes_table = pd.DataFrame.from_dict(notes)

if __name__ == "__main__":
    output_path = parent_dir / "python_titanic_gptable.xlsx"
    gpt.write_workbook(
        filename=output_path,
        sheets=sheets,
        notes_table=notes_table,
        contentsheet_options={"additional_elements": ["subtitles", "scope"]}
        )
    print("Output written at: ", output_path)
