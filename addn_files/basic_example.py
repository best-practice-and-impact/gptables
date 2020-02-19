from gptables import Workbook

wb = Workbook(r"D:\gptables_test\test_doc.xlsx")
ws1 = wb.add_worksheet("Stuff that need publishing", shape=(10,10))

ws1.cells[1,2].set_data("Hello world!")
ws1.cells[1,2].update_style({"bold":True, "font_size":20})

wb.write_output_to_excel()
wb.write_cell_attributes_to_excel()