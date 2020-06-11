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

iris_summary = iris_data.groupby("class").agg(np.mean)
iris_summary.index = [_[5:].capitalize() for _ in iris_summary.index]
iris_summary.rename(
        columns={
            "class":"class",
            "sepal_length":"Mean Sepal Length",
            "sepal_width":"Mean Sepal Width"
            }, 
        inplace=True
        )

# Drop index into table
iris_summary.reset_index(inplace=True)

# Make tables with varying numbers of index levels - up to 3 supported
iris_summary_0 = iris_summary.copy().iloc[:, 1:]

iris_summary_2 = iris_summary.copy()
iris_summary_2.insert(0, "top_index", ["A", "B", "C"])

iris_summary_3 = iris_summary_2.copy()
iris_summary_3.insert(2, "bottom_index", ["x", "y", "z"])


#################################################
###### WRITE USING QUICK AND DIRTY METHOD #######
#################################################
gpt.quick_and_dirty_workbook(
        filename = parent_dir + "/python_iris_quick_and_dirty.xlsx",
        tables = [iris_summary_0, iris_summary, iris_summary_2, iris_summary_3]
        )
