import pytest
from collections import namedtuple
import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal

import xlsxwriter

import gptables
from gptables.core.wrappers import GPWorkbook
from gptables.core.wrappers import GPWorksheet
from gptables.core.gptable import FormatList
from gptables import Theme
from gptables import gptheme
from gptables.test.test_gptable import create_gptable_with_kwargs, does_not_raise

Tb = namedtuple("Testbook", "wb ws")

valid_text_elements = [  # Not None
    "This is a string",
    FormatList(["More than ", {"italic": True}, "just ", "a string"])
]

test_text_list = [
    "This has a $$reference$$",
    "This one doesn't",
    "Here's another $$one$$"
    ]

exp_text_list = [
    "This has a [note 1]",
    "This one doesn't",
    "Here's another [note 2]"
    ]


invalid_text_elements = [
    dict(),
    set(),
    42,
    3.14,
    True
]

@pytest.fixture()
def testbook():
    # See https://github.com/jmcnamara/XlsxWriter/issues/746#issuecomment-685869888
    wb = GPWorkbook(options={'in_memory': True})
    ws = wb.add_worksheet()
    yield Tb(wb, ws)
    wb.fileclosed = 1


class TestGPWorksheetInit:
    """
    Test that default attributes are set when GPWorksheets are created.
    """
    
    def test_subclass(self):
        """
        Test that the GPWorksheet class is a subclass of the XlsxWriter
        Worksheet class.
        """
        assert issubclass(
                        GPWorksheet,
                        xlsxwriter.worksheet.Worksheet
                        )
    

    def test_default_theme_set(self, testbook):
        """
        Test that the default theme (gptheme) is used when no theme is set.
        """
        assert testbook.wb.theme == gptheme
    

    def test_default_gridlines(self, testbook):
        """
        Test that print and screen gridlines are hidden by default.
        """
        assert testbook.ws.print_gridlines == 0
        assert testbook.ws.screen_gridlines == 0
        

    def test_wb_reference(self, testbook):
        """
        Test that GPWorksheets reference their parent GPWorkbook.
        """
        assert testbook.ws._workbook == testbook.wb
    

    @pytest.mark.parametrize("not_a_gptable", [
        dict(),
        set(),
        [],
        1,
        3.14,
        "test_string",
        pd.DataFrame()
    ])
    def test_invalid_write_gptable(self, not_a_gptable, testbook):
        """
        Test that write_gptable() raises a TypeError when argument is not a
        gptables.GPTable object.
        """
        with pytest.raises(TypeError):
            testbook.ws.write_gptable(not_a_gptable)


class TestGPWorksheetWriting:
    """
    Test that additional writing methods correctly write to GPWorksheet object.
    """

    def test__smart_write_str(self, testbook):
        """
        Test that strings are stored in the GPWorksheet as expected.
        """
        testbook.ws._smart_write(0, 0, valid_text_elements[0], {})
        # Strings are stored in a lookup table for efficiency
        got_string = testbook.ws.str_table.string_table
        exp_string = {valid_text_elements[0]: 0}
        assert got_string == exp_string
        
        # String is referenced using a named tuple (string, Format)
        # Here we get first element, which references string lookup location
        got_lookup = testbook.ws.table[0][0][0]
        exp_lookup = 0
        assert got_lookup == exp_lookup


    def test__smart_write_formatted_str(self, testbook):
        testbook.ws._smart_write(1, 2, valid_text_elements[0], {"bold": True})
        # Strings are stored in a lookup table for efficiency
        got_string = testbook.ws.str_table.string_table
        exp_string = {valid_text_elements[0]: 0}
        assert got_string == exp_string
        
        # String is referenced using a named tuple (string, Format)
        # Here we get first element, which references string lookup location
        cell = testbook.ws.table[1][2] 
        got_lookup = cell[0]
        exp_lookup = 0
        assert got_lookup == exp_lookup
        
        format_obj = cell[1]
        assert format_obj.bold
        

    def test__smart_write_rich_text(self, testbook):
        testbook.wb.set_theme(Theme({}))
        
        testbook.ws._smart_write(0, 0, valid_text_elements[1], {})
        # Strings are stored in a lookup table for efficiency
        got_string = testbook.ws.str_table.string_table
        exp_string = {'<r><t xml:space="preserve">More than </t></r><r><rPr><i'
                      '/><sz val="11"/><color theme="1"/><rFont val="Calibri"/'
                      '><family val="2"/><scheme val="minor"/></rPr><t xml:spa'
                      'ce="preserve">just </t></r><r><rPr><sz val="11"/><color'
                      ' theme="1"/><rFont val="Calibri"/><family val="2"/><sch'
                      'eme val="minor"/></rPr><t>a string</t></r>': 0}
        assert got_string == exp_string
        
        # String is referenced using a named tuple (string, Format)
        # Here we get first element, which references string lookup location
        got_lookup = testbook.ws.table[0][0][0]
        exp_lookup = 0
        assert got_lookup == exp_lookup
    


    def test__smart_write_formatted_rich_text(self, testbook):
        testbook.wb.set_theme(Theme({}))
        
        testbook.ws._smart_write(1, 2, valid_text_elements[1], {"bold": True})
        # Strings are stored in a lookup table for efficiency
        got_string = testbook.ws.str_table.string_table
        exp_string = {'<r><t xml:space="preserve">More than </t></r><r><rPr><b'
                      '/><i/><sz val="11"/><color theme="1"/><rFont val="Calib'
                      'ri"/><family val="2"/><scheme val="minor"/></rPr><t xml'
                      ':space="preserve">just </t></r><r><rPr><b/><sz val="11"'
                      '/><color theme="1"/><rFont val="Calibri"/><family val="'
                      '2"/><scheme val="minor"/></rPr><t>a string</t></r>': 0}

        assert got_string == exp_string
        
        # String is referenced using a named tuple (string, Format)
        # Here we get first element, which references string lookup location
        cell = testbook.ws.table[1][2] 
        got_lookup = cell[0]
        exp_lookup = 0
        assert got_lookup == exp_lookup
        
        format_obj = cell[1]
        assert format_obj.bold


    def test__smart_write_link(self, testbook):
        testbook.wb.set_theme(Theme({}))

        display_text = "gov.uk"
        url = "https://www.gov.uk/"

        testbook.ws._smart_write(0, 0, {display_text: url}, {})

        got_string = testbook.ws.str_table.string_table
        exp_string = {display_text: 0}
        assert got_string == exp_string

        got_hyperlink = testbook.ws.hyperlinks[0][0]["url"]
        exp_hyperlink = url
        assert got_hyperlink == exp_hyperlink

        # String is referenced using a named tuple (string, Format)
        # Here we get first element, which references string lookup location
        cell = testbook.ws.table[0][0]

        got_lookup = cell[0]
        exp_lookup = 0
        assert got_lookup == exp_lookup

        format_obj = cell[1]
        assert format_obj.underline == True
        assert format_obj.font_color == "#0000FF" # aka Blue


    def test__smart_write_null_cell(self, testbook):
        testbook.ws._smart_write(0, 0, None, {})
        # Strings are stored in a lookup table for efficiency
        got_string = testbook.ws.str_table.string_table
        exp_string = {}
        assert got_string == exp_string

        # Strings referenced using a named tuple (string, Format)
        # When cell has no content, tuple only contains Format
        cell = testbook.ws.table[0][0]
        assert len(cell) == 1


    @pytest.mark.parametrize("cell_value1,cell_value2,expectation", [
        (None, None, pytest.raises(ValueError)),
        (None, "valid text", pytest.warns(UserWarning)),
        ("", "valid text", pytest.warns(UserWarning)),
        (" ", "valid text", pytest.warns(UserWarning)),
        ("    ", "valid text", pytest.warns(UserWarning)),
        ("_", "valid text", pytest.raises(ValueError)),
        (" *", "valid text", pytest.raises(ValueError)),
        (" Hello_World! ", "valid text", does_not_raise()),
    ])
    def test__write_table_elements_validation(self, testbook,
        create_gptable_with_kwargs, cell_value1, cell_value2, expectation):
        gptable = create_gptable_with_kwargs({
            "table": pd.DataFrame({"col": [cell_value1, cell_value2]})
        })

        with expectation:
            testbook.ws._write_table_elements([0,0], gptable, auto_width=True)



class TestGPWorksheetFooterText:
    """
    Test that GPTable footer elements are modified correctly by GPWorksheet
    during write_gptable().
    """


    @pytest.mark.parametrize("text", test_text_list)
    def test__replace_reference(self, text, testbook):
        """
        Test that references ($$ref$$ style) in strings are replaced with
        [note n], in order of appearance. Also tests replacement in lists.
        """
        got_output = []
        reference_order = ["reference", "one"]

        got_output = [testbook.ws._replace_reference(text, reference_order) for text in test_text_list]
    
        exp_refs = ["reference", "one"]
        assert reference_order == exp_refs
        assert got_output == exp_text_list


    @pytest.mark.parametrize("text,refs,output",
        zip(test_text_list,
        [["reference"], [], ["one"]],
        ["This has a [note 1]", "This one doesn't", "Here's another [note 2]"]
        ))
    def test__replace_reference_in_attr_str(self, text, refs, output, testbook):
        """
        Test that references are replaced in a single string.
        """
        reference_order = ["reference", "one"]
        got_text = testbook.ws._replace_reference_in_attr(
                text,
                reference_order
                )

        assert got_text == output


    def test__replace_reference_in_attr_dict(self, testbook):
        """
        Test that references are replaced in dictionary values, but not keys.
        """
        reference_order = ["reference", "one"]
        test_text_dict = {
                "$$key$$": "This is a value with a $$reference$$",
                "another_key": "Another value",
                "third_key": "$$one$$more reference"
                }
        got_text = testbook.ws._replace_reference_in_attr(
                test_text_dict,
                reference_order
                )
                
        exp_text_dict = {
                "$$key$$": "This is a value with a [note 1]",
                "another_key": "Another value",
                "third_key": "more reference[note 2]"
                }
        
        assert got_text == exp_text_dict



class TestGPWorksheetFormatUpdate:
    """
    Test that GPWorksheet format updating methods work as expected.
    """
    def test__apply_format_dict(self, testbook):
        test = dict()
        format_dict = {"bold": True}
        testbook.ws._apply_format(test, format_dict)
        exp = {"bold": True}
        assert test == exp


    def test__apply_format_series(self, testbook):
        test = pd.Series([{} for n in range(3)])
        format_dict = {"bold": True}
        testbook.ws._apply_format(test, format_dict)
        exp = pd.Series([{"bold": True} for n in range(3)])
        assert_series_equal(test, exp)


    def test__apply_format_dataframe(self, testbook):
        test = pd.DataFrame(columns=[0, 1, 2], index = [0, 1])
        test.iloc[0] = [{} for n in range(3)]
        test.iloc[1] = [{} for n in range(3)]
        
        format_dict = {"bold": True}
        testbook.ws._apply_format(test, format_dict)
        exp = pd.DataFrame(columns=[0, 1, 2], index = [0, 1])
        exp.iloc[0] = [{"bold": True} for n in range(3)]
        exp.iloc[1] = [{"bold": True} for n in range(3)]
        assert_frame_equal(test, exp)



class TestGPWorksheetTable:
    """
    Test that the table property inherited from `xlsxwriter.Worksheet` is set correctly.
    """
    def test__mark_data_as_worksheet_table(
        self, testbook, create_gptable_with_kwargs
    ):
        df = pd.DataFrame({"col1": ["x", "y"], "col2": [0, 1]})
        table_name = "table_name"

        gptable = create_gptable_with_kwargs({
            "table": df,
            "table_name": table_name
        })
        gptable._set_data_range()

        table_format = pd.DataFrame({"col1": [{}, {}], "col2": [{}, {}]})

        testbook.ws._write_array([0, 2], df, table_format) # First two rows reserved for title and instructions

        column_heading_format = testbook.ws.theme.column_heading_format
        testbook.ws._mark_data_as_worksheet_table(gptable, column_heading_format)

        assert len(testbook.ws.tables) == 1

        table = testbook.ws.tables[0]

        got_table_range = table["a_range"]
        exp_table_range = xlsxwriter.utility.xl_range(*gptable.data_range)

        assert got_table_range == exp_table_range

        assert table["name"] == table_name

        got_number_of_columns = len(table["columns"])
        exp_number_of_columns = df.shape[0]
        assert got_number_of_columns == exp_number_of_columns

        for n in range(got_number_of_columns):
            got_column_name = table["columns"][n]["name"]
            exp_column_name = df.columns[n]
            assert got_column_name == exp_column_name

            got_heading_format = table["columns"][n]["name_format"]
            exp_heading_format = testbook.wb.add_format(column_heading_format)
            assert got_heading_format.__dict__ == exp_heading_format.__dict__



class TestGPWorkbook:
    """
    Test that GPWorkbook initialisation and methods work as expected.
    """ 
    def test_subclass(self):
        """
        Test that the GPWorkbook class is a subclass of the XlsxWriter
        Workbook class.
        """
        assert issubclass(
                        GPWorkbook,
                        xlsxwriter.Workbook
                        )
    

    def test_default_theme_set(self, testbook):
        """
        Test that the workbook theme is set to gptheme by default.
        """        
        assert testbook.wb.theme == gptheme
    

    def test_valid_set_theme(self, testbook):
        """
        Test that setting a new theme with a Theme object works as expected.
        Essentially, make sure that gptheme is not used.
        """
        theme_config = {"title": {"bold": True}}
        theme = gptables.Theme(theme_config)
        testbook.wb.set_theme(theme)
        
        assert testbook.wb.theme == gptables.Theme(theme_config)
    
    @pytest.mark.parametrize("not_a_theme", [
        dict(),
        set(),
        [],
        1,
        3.14,
        "test_string",
        pd.DataFrame()
    ])
    def test_invalid_set_theme(self, not_a_theme, testbook):
        """
        Test that setting theme with an object that is not a gptables.Theme
        raises a TypeError.
        """
        with pytest.raises(TypeError):
            testbook.wb.set_theme(not_a_theme)
            
    def test_make_notesheet(self, testbook):
        """
        Test that creating a notes table sheet using `make_notesheet` generates
        the same gptables.GPTable object as expected.
        """
        gp_workbook = testbook.wb
        gp_workbook._annotations = [1, 2]
        dummy_table = pd.DataFrame(data={"Note number":[1, 2], "Note text":[3, 4]})
        
        notes_name = "Just_a_notesheet"
        notes_title = "Are these the notes you're looking for?"
        notes_instructions = "These are not the notes you're looking for"
        
        got_notesheet = gp_workbook.make_notesheet(notes_table=dummy_table,
                                                   table_name=notes_name,
                                                   title=notes_title,
                                                   instructions=notes_instructions)
        exp_notesheet = gptables.GPTable(table=dummy_table,
                                         table_name=notes_name,
                                         title=notes_title,
                                         instructions=notes_instructions,
                                         index_columns={})
        
        assert_frame_equal(got_notesheet.table, exp_notesheet.table)
        
        got_notesheet.table = None
        exp_notesheet.table = None
        
        assert got_notesheet.__dict__ == exp_notesheet.__dict__