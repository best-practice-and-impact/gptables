import gptables as gpt
import pandas as pd
import numpy as np

######################################
###### READ DATA IN AND FORMAT #######
######################################

funcs = [np.mean, np.median]
iris_data = pd.read_csv("./iris.csv")

iris_data.rename(
        columns={" class":"class",
            "sepal_length":"Sepal Length",
            " petal_length":"Petal Length",
            " petal_width":"Petal Width",
            " sepal_width":"Sepal Width"}, 
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
index = {1:"variable",2:"func"}

# or just use kwargs
kwargs = {"title":title,
        "subtitle":subtitle,
        "units":units,
        "index_columns":index}

# define our GPTable
iris_table = gpt.GPTable(
        data=iris_summ,
        **kwargs)        

# additional formatting
iris_table.format({
        [{"headings":"All"},
            {"bold":True,}],
        [{"column":["Setosa","Versicolor","Virginica","All"]},
            {"align":"right"}])

######################################
#### USE PRODUCE_WORKBOOK TO WIN #####
######################################

gpt.produce_workbook(file="/iris_gptable.xlsx",
    sheets={"iris flower dimensions":iris_table},
    theme=gptheme)
