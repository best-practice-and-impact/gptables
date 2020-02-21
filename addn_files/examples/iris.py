import gptables as gpt
import pandas as pd
import numpy as np
import os

from gptables import gptheme

######################################
###### READ DATA IN AND FORMAT #######
######################################
funcs = [np.mean, np.median]
parent_dir = os.path.dirname(os.path.realpath(__file__))
iris_data = pd.read_csv(parent_dir + "/iris.csv")

iris_data.rename(
        columns={
            " class":"class",
            "sepal_length":"Sepal Length$$note4$$",
            " petal_length":"Petal Length",
            " petal_width":"Petal Width",
            " sepal_width":"Sepal Width"
            }, 
        inplace=True
        )

iris_data["class"] = iris_data.apply(
        lambda row: row["class"][5:].capitalize(),
        axis=1)

# calculate summaries
ls = []
for func in funcs:
    ls.append(iris_data.groupby("class").agg(func))
    ls.append(pd.DataFrame(iris_data.agg(func).rename("All$$note3$$")).T)

iris_summ = pd.concat(ls)
iris_summ["func"] = ["Mean"] * 4 + ["Median"] * 4

# reshape
iris_summ = iris_summ.reset_index()
iris_summ = iris_summ.melt(["index","func"])
iris_summ = iris_summ.pivot_table(
        index=["variable","func"],
        columns="index",
        values="value"
        ).reset_index()

# Insert nan
iris_summ.iloc[2, 3] = np.nan

######################################
####### DEFINE TABLE ELEMENTS ########
######################################

title = "Iris$$note2$$ flower dimensions"
subtitles = [
        "1936 Fisher, R.A; The use of multiple measurements in taxonomic problems$$note1$$",
        "Just another subtitile"
        ]
units = "cm$$note1$$"
scope = "Iris$$note2$$"
source = "Source: Office for Iris Statistics"
index = {
        1:0,
        2:1
        }  # Need to support referencing by col name
annotations = {
        "note1": "I've got 99 problems and taxonomy is one.",
        "note2": "Goo Goo Dolls, 1998.",
        "note3": "All species of the Iris genus.",
        "note4": "Length of the largest sepal.",
        "note5": "This annotation is not referenced, so should not appear."
        }
notes = [
        "This note hath no reference."
        ]


# additional formatting
formatting = ([
        {"column":
            {"columns": ["Setosa","Versicolor"],  # Str or list of str
             "format": {"align":"right"},
             "include_names": False  # Whether to include column headings
            }
        },
        {"row":  # As above
            {"rows": 1,
             "format": {"bold":True},
             "include_names": True
             }
        },
        {"cell":
            {"cells": (1, 5),  # tuple or list of tuples
             "format": {"italic":True, "font_color": "red"}
                }
        }
])


# or just use kwargs
kwargs = {"title":title,
        "subtitles":subtitles,
        "units":units,
        "scope": scope,
        "source":source,
        "index_columns":index,
        "annotations":annotations,
        "notes":notes,
        "additional_formatting": formatting
        }

# define our GPTable
iris_table = gpt.GPTable(
        table=iris_summ,
        **kwargs
        )        


######################################
#### USE PRODUCE_WORKBOOK TO WIN #####
######################################

wb = gpt.produce_workbook(
        file= parent_dir + "/iris_gptable.xlsx",
        sheets={"iris flower dimensions":iris_table},
        theme=gptheme
        )

wb.close()
