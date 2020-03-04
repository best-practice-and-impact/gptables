import gptables as gpt
import pandas as pd
import numpy as np
import os

######################################
###### READ DATA IN AND FORMAT #######
######################################
funcs = [np.mean, np.median]
parent_dir = os.path.dirname(os.path.realpath(__file__))

iris_data = pd.read_csv(parent_dir + "/iris.csv")
iris_data = iris_data.loc[:, ["class", "sepal_length", "sepal_width"]]

iris_summ = iris_data.groupby("class").agg(np.mean)
iris_summ.index = [_[5:].capitalize() for _ in iris_summ.index]
iris_summ.rename(
        columns={
            "class":"class",
            "sepal_length":"Mean Sepal Length",
            "sepal_width":"Mean Sepal Width"
            }, 
        inplace=True
        )
# Drop index into table
iris_summ.reset_index(inplace=True)

######################################
####### DEFINE TABLE ELEMENTS ########
######################################
title = ["Mean", {"italic": True}, " Iris", "$$note2$$ sepal dimensions"]
subtitles = [
        "1936 Fisher, R.A; The use of multiple measurements in taxonomic problems$$note1$$",
        "Just another subtitile"
        ]
units = "cm"
scope = "Iris"
source = "Source: Office for Iris Statistics"
index = {2: 0}  # Column 0 is a level 2 index
annotations = {
        "note1": "I've got 99 problems and taxonomy is one.",
        "note2": "Goo Goo Dolls, 1998."
        }
notes = [
        "This note hath no reference."
        ]

# or just use kwargs
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
iris_table = gpt.GPTable(
        table=iris_summ,
        **kwargs
        )        

######################################
##### USE WRITE_WORKBOOK TO WIN ######
######################################
wb = gpt.write_workbook(
        filename= parent_dir + "/python_iris_gptable.xlsx",
        sheets={"iris flower dimensions":iris_table}
        )