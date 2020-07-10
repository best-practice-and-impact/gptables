"""
Iris - Quick and Dirty Example
------------------------------

This example demonstrates use of the ``gptables.quick_and_dirty_workbook`` function.
This function is intended for use when only data, and no metadata, is required.
It should **not** be used for production of reference statistical tables for publication.

This function takes a list of ``pandas.DataFrame`` objects and writes each to a
separate sheet of the specified output `.xlsx` file. Formatting is taken from
the default ``gptables.Theme`` - gptheme - unless an alternative theme is provided
using the ``theme`` parameter. Column widths are automatically adjusted,
unless the ``auto_width`` parameter is set to False.

Unlike the other API functions, ``quick_and_dirty_workbook`` does not require
the user to specify table metadata or indicate which columns are row indexes.
Up to 3 row index levels are automatically detected. However, as with the other
API functions, row indices must be columns in the table instead of set as a ``pandas.Index``.
"""
import gptables as gpt
import pandas as pd
import numpy as np
import os


## Read data and arrange
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


## Write using quick and dirty method
output_path = parent_dir + "/python_iris_quick_and_dirty.xlsx"
gpt.quick_and_dirty_workbook(
        filename = output_path,
        tables = [iris_summary_0, iris_summary, iris_summary_2, iris_summary_3]
        )
print("Output written at: ", output_path)

