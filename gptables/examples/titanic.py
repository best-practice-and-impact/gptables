"""
gptables example using the Titanic dataset.
@author: Ramiz Farishta
"""

import gptables as gpt
import pandas as pd
import numpy as np
import os

parent_dir = os.path.dirname(os.path.realpath(__file__))
titanic = pd.read_csv(parent_dir + "/titanic.csv")

titanic["Child"] = np.where(titanic['Age'] < 18, 1, 0)

sex_survived = titanic.groupby("Sex")["Survived"].sum()
sex_pclass = titanic.groupby('Sex')['Pclass'].apply(lambda x: x.mode().iloc[0])
sex_child = titanic.groupby("Sex")["Child"].sum()
sex_fare = titanic.groupby("Sex")["Fare"].mean()

titanic_analysis =(
        pd.DataFrame({
                "Survived":sex_survived,
                "Pclass":sex_pclass,
                "Child":sex_child,
                "Fare":sex_fare}
        ).reset_index()
        )

title = "Titanic$$note2$$ analysis by sex"
subtitles = [
        "Derived from a Kaggle competition dataset$$note1$$"
        ]
units = {
        "Survived": "sum$$note3$$",
        "Pclass": "mode",
        "Child": "sum",
        "Sex": "mean"
        }
scope = "Titanic$$note2$$"
source = "Source: Kaggle"
index = {
        2: 0,
        }
annotations = {
        "note1": "www.kaggle.com/titanic",
        "note2": "Celine Dion.",
        "note3": "Total count."
        }
notes = [
        "This note hath no reference."
        ]

kwargs = {"title":title,
        "subtitles":subtitles,
        "units":units,
        "scope": scope,
        "source":source,
        "index_columns":index,
        "annotations":annotations,
        "notes":notes
        }

# define our GPTable
titanic_table = gpt.GPTable(
        table=titanic_analysis,
        **kwargs
        )

wb = gpt.write_workbook(
        filename= parent_dir + "/python_titanic_gptable.xlsx",
        sheets={"titanic analysis by sex":titanic_table}
        )