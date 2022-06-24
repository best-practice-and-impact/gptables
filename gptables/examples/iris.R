
#Iris - R Example
#----------------------

#This example demonstrates use of the ``gptables.write_workbook`` function in R.
#This API function is designed for production of consistently structured and formatted tables.

#Summary statistics from the classic iris dataset are used to build a ``gptables$GPTable``
#object. Elements of metadata are provided to the corresponding parameters of the class.
#Where you wish to provide no metadata in required parameters, use ``None``.

#Table formatting can be defined as a ``gptable$Theme``, which is passed to the API functions
# using the ``theme`` parameter. Or you can reply on our default - gptheme.


# Reticulate example works on R version 4.0.1 or less
source("gptables/examples/R_install_dependency_file.R")

packagesReq <- c("dplyr", "reticulate", "magrittr")
packageRefresh(packagesReq)

library("magrittr")

gpt <- reticulate::import("gptables")
pd <- reticulate::import("pandas")

iris_df <- reticulate::r_to_py(
  iris[c(5,1,2,3,4)]%>%
    dplyr::group_by(Species) %>%
    dplyr::summarize("Mean Sepal Length" = mean(Sepal.Length, na.rm=TRUE),
                     "Mean Sepal Width" = mean(Sepal.Width, na.rm=TRUE)
    )
)

table_name = "iris_statistics"
title = "Mean Iris $$note2$$ sepal dimensions"
subtitles = c("1936 Fisher, R.A; The use of multiple measurements in taxonomic problems$$note1$$",
              "Just another subtitile $$note3$$")
units = reticulate::dict(list("1" = "cm", "2" = "cm"), convert = FALSE)
table_notes = reticulate::dict(list("0" = "$$note1$$", "2" = "$$note3$$"), convert = FALSE)
scope = "Iris"
souce = "Source: Office for Iris Statistics"
index_columns  = reticulate::py_dict(reticulate::py_eval('2'), "Species")


table = gpt$GPTable(table = iris_df,
                    table_name = table_name,
                    title = title,
                    subtitles = subtitles,
                    units = units,
                    scope = scope,
                    source = souce,
                    index_columns = index_columns)

notes = reticulate::dict(list("Note reference" = c("note1", "note2", "note3"),
                              "Note text" = c("I've got 99 problems and taxonomy is one.", "Goo Goo Dolls, 1998.", "Just another note"),
                              "Useful link" = c("[google](https://www.google.com)", "[duckduckgo](https://duckduckgo.com/)", "[ONS](https://www.ons.gov.uk)")),
                         convert = FALSE)

notes_table = pd$DataFrame$from_dict(notes)

output_path <- "gptables/examples/R_iris_gptable.xlsx"

gpt$write_workbook(filename = output_path,
                         sheets = reticulate::dict(list("iris" = table)),
                         notes_table = notes_table,
                         contentsheet_options = reticulate::dict(list("additional_elements" = c("subtitles", "scope")))
                         )
