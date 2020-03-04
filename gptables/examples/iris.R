library(dplyr)

######################################
######### SET UP RETICULATE ##########
######################################

python_env_path <- "C:\\Path\\to\\env"

reticulate::use_virtualenv(python_env_path)
gpt <- reticulate::import("gptables")
pd <- reticulate::import("pandas")

######################################
###### READ DATA IN AND FORMAT #######
######################################
iris_df <- reticulate::r_to_py(
  iris[c(5,1,2,3,4)]%>%
    group_by(Species) %>%
    dplyr::summarize("Mean Sepal Length" = mean(Sepal.Length, na.rm=TRUE),
                     "Mean Sepal Width" = mean(Sepal.Width, na.rm=TRUE)
                     )
  )

######################################
####### DEFINE TABLE ELEMENTS ########
######################################
title = list("Mean", reticulate::py_dict("italic", TRUE), " Iris", "$$note2$$ sepal dimensions")
subtitles = c("1936 Fisher, R.A; The use of multiple measurements in taxonomic problems$$note1$$",
              "Just another subtitile")
units = "cm"
scope = "Iris"
souce = "Source: Office for Iris Statistics"
index_columns  = reticulate::py_dict(reticulate::py_eval('2'), "Species")

annotations = list(note1 = "I've got 99 problems and taxonomy is one.",
                   note2 = "Goo Goo Dolls, 1998.")
notes = list("This note hath no reference.")

table = gpt$GPTable(table = iris_df,
                    title = title,
                    subtitles = subtitles,
                    units = units,
                    scope = scope,
                    source = souce,
                    index_columns = index_columns,
                    annotations = annotations,
                    notes = notes)

######################################
##### USE WRITE_WORKBOOK TO WIN ######
######################################
wb <- gpt$write_workbook(filename = "R_iris_gptable.xlsx", sheets = list("iris" = table))