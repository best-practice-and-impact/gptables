import unittest
from io import StringIO
from collections import namedtuple
import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal

import xlsxwriter

import gptables
from gptables.core.wrappers import GPWorkbook
from gptables.core.wrappers import GPWorksheet
from gptables import Theme
from gptables import gptheme
import pytest

Tb = namedtuple("Testbook", "wb ws")

valid_text_elements = [  # Not None
    "This is a string",
    ["More than ", {"italic": True}, "just ", "a string"]
]

test_text_list = [
    "This has a $$reference$$",
    "This one doesn't",
    "Here's another $$one$$"
    ]

exp_text_list = [
    "This has a (1)",
    "This one doesn't",
    "Here's another (2)"
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



class TestGPWorksheetFooterText:
    """
    Test that GPTable footer elements are modified correctly by GPWorksheet
    during write_gptable().
    """


    @pytest.mark.parametrize("text,enclosed", [
        ("", "()"),
        ("This has a $$reference$$", "(This has a $$reference$$)"),
        ("(Already have some)", "((Already have some))")
        ]
    )
    def test__enclose_text_string(self, text, enclosed, testbook):
        """
        Test that strings are correctly flanked with parentheses.
        """
        test_text = testbook.ws._enclose_text(text)
        assert test_text == enclosed


    def test__enclose_text_list(self, testbook):
        """
        Test that rich text is flanked with parentheses.
        """
        test_list = ["An", {"bold": True}, "example", "note"]
        got = testbook.ws._enclose_text(test_list)
        exp = ["(", "An", {"bold": True}, "example", "note", ")"]
        assert got == exp

    @pytest.mark.parametrize("text", test_text_list)
    def test__replace_reference(self, text, testbook):
        """
        Test that references ($$ref$$ style) in strings are replaced with
        numbers, in order of appearance. Also tests replacement in lists.
        """
        got_output = []
        ordered_refs = []

        got_output = [testbook.ws._replace_reference(text, ordered_refs) for text in test_text_list]
    
        exp_refs = ["reference", "one"]
        assert ordered_refs == exp_refs
        assert got_output == exp_text_list


    @pytest.mark.parametrize("text,refs,output",
        zip(test_text_list,
        [["reference"], [], ["one"]],
        ["This has a (1)", "This one doesn't", "Here's another (1)"]
        ))
    def test__replace_reference_in_attr_str(self, text, refs, output, testbook):
        """
        Test that references are replaced in a single string.
        """
        ordered_refs = []
        got_text = testbook.ws._replace_reference_in_attr(
                text,
                ordered_refs
                )

        assert ordered_refs == refs
        assert got_text == output


    def test__replace_reference_in_attr_dict(self, testbook):
        """
        Test that references are replaced in dictionary values, but not keys.
        """
        ordered_refs = []
        test_text_dict = {
                "$$key$$": "This is a value with a $$reference$$",
                "another_key": "Another value",
                "third_key": "$$one$$ more reference"
                }
        got_text = testbook.ws._replace_reference_in_attr(
                test_text_dict,
                ordered_refs
                )
        
        assert ordered_refs == ["reference", "one"]
        
        exp_text_dict = {
                "$$key$$": "This is a value with a (1)",
                "another_key": "Another value",
                "third_key": "(2) more reference"
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


class TestGPWorkbookStatic:

    @pytest.mark.parametrize("input, expected", [
        ("no references", "no references"),
        ("ref at end$$1$$", "ref at end"),
        ("$$1$$ref at start", "ref at start"),
        ("two$$1$$ refs$$2$$", "two refs"),
        ("three$$1$$ refs$$2$$, wow$$3$$", "three refs, wow")
    ])
    def test__strip_annotation_references(self, input, expected):
        assert GPWorksheet._strip_annotation_references(input) == expected
        
        
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
