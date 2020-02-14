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
            "sepal_length":"Sepal Length",
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
    ls.append(pd.DataFrame(iris_data.agg(func).rename("All")).T)

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

######################################
####### DEFINE TABLE ELEMENTS ########
######################################

title = "Iris flower dimensions"
subtitle = "1936 Fisher, R.A; The use of multiple measurements in taxonomic problems$$note1$$"
units = "cm"
scope = "Iris"
source = "Source: Office for Iris Statistics"
index = {1:0,2:1}  # Need to support referencing by col name
notes = {"note1": "I've got 99 problems and taxonomy is one.",
         "note2": "This note is not references, so should come last."}

# or just use kwargs
kwargs = {"title":title,
        "subtitles":[subtitle],
        "units":units,
        "scope": scope,
        "source":source,
        "index_columns":index,
        "notes":notes}

# define our GPTable
iris_table = gpt.GPTable(
        table=iris_summ,
        **kwargs
        )        

# additional formatting
#iris_table.format({
#        [{"headings":"All"},
#            {"bold":True,}],
#        [{"column":["Setosa","Versicolor","Virginica","All"]},
#            {"align":"right"}])

######################################
#### USE PRODUCE_WORKBOOK TO WIN #####
######################################

wb = gpt.produce_workbook(
        file="./iris_gptable.xlsx",
        sheets={"iris flower dimensions":iris_table},
        theme=gptheme
        )

wb.close()
