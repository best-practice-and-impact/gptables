library(dplyr)

python_env_path <- "D:\\Repos\\crime-tables-python\\env"

reticulate::use_virtualenv(python_env_path)
gpt <- reticulate::import("gptables")
pd <- reticulate::import("pandas")

iris_df <- reticulate::r_to_py(
  iris[c(5,1,2,3,4)]%>%
    group_by(Species) %>%
    dplyr::summarize(Mean.Sepal.Length = mean(Sepal.Length, na.rm=TRUE),
                     Mean.Sepal.Width = mean(Sepal.Width, na.rm=TRUE)
                     )
  )

title = "Iris dataset$$one$$"
subtitles = c("One subtitle",
              "Another subtitle")
units = "cm"
scope = "Iris"
sauce = "Source: Office for Iris Statistics"
index_columns  = reticulate::py_dict(reticulate::py_eval('2'), "Species")

annotations = list(one = "Presented using gptables")
notes = c("This is not referenced", "Also not referenced")

table = gpt$GPTable(table = iris_df,
                    title = title,
                    subtitles = subtitles,
                    units = units,
                    scope = scope,
                    source = sauce,
                    index_columns = index_columns,
                    annotations = annotations,
                    notes = notes)

wb <- gpt$produce_workbook(filename = "test.xlsx", sheets = list("iris" = table))
wb$close()