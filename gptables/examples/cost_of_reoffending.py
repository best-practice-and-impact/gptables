import gptables as gpt
import pandas as pd
import os
######################################
###### READ DATA IN AND FORMAT #######
######################################
parent_dir = os.path.dirname(os.path.realpath(__file__))
core_data = pd.read_csv(parent_dir + "/coreB.csv")

# 3 tables: summary, children and young people, and adults

summ = core_data.loc[:,['age','total_cost']]
summ = summ.groupby('age').sum().reset_index()

# this returns adults first as per the data
ages = core_data.age.unique()

dct = {ages[0]:pd.DataFrame(), ages[1]:pd.DataFrame()}
for key in dct:
    frame = core_data.loc[core_data.age == key, ["reoffence_group", "total_cost"]]
    frame = frame.groupby("reoffence_group").sum().reset_index()
    dct[key] = frame

dct['summary'] = summ 

######################################
####### DEFINE TABLE ELEMENTS ########
######################################
elements = {'summary':
        {
            "title":"",
            "subtitles":[""],
            "units":"£",
            "scope":"England and Wales, 12-month follow-up period for the 2016 offender cohort",
            "source":"ONS",
            "index_columns":{
                1:0,
                2:1
                },
            "annotations":{
                
                },
            "notes":["this is a note"]
        },
        'Adults':{
            "title":"",
            "subtitles":[""],
            "units":"£",
            "scope":"England and Wales, 12-month follow-up period for the 2016 offender cohort",
            "source":"ONS",
            "index_columns":{
                1:0,
                2:1
                },
            "annotations":{
                
                },
            "notes":["this is a note"]
        },
        'Children and young people':{
            "title":"",
            "subtitles":[""],
            "units":"£",
            "scope":"England and Wales, 12-month follow-up period for the 2016 offender cohort",
            "source":"ONS",
            "index_columns":{
                1:0,
                2:1
                },
            "annotations":{
                
                },
            "notes":["this is a note"]
        }
    }

gptables = {name:gpt.GPTable(dct[name], **elements[name]) for name in dct}

######################################
##### USE WRITE_WORKBOOK TO WIN ######
######################################
wb = gpt.write_workbook(
        filename=parent_dir+"/python_core_gptable.xlsx",
        sheets=gptables
        )
