import gptables as gpt

######################################
###### READ DATA IN AND FORMAT #######
######################################
iris_data = pd.read_csv("./iris.csv")

iris_data = do_things(iris_data)




######################################
####### DEFINE TABLE ELEMENTS ########
######################################
headings = {}
index = {}


# or just use kwargs
kwargs = {"headings":headings,
          "index":index
         }



######################################
###### USE PRODUCE_TABLE TO WIN ######
######################################
gpt.produce_table(data=iris_data,
                  theme=gpttheme,
                  **kwargs)


