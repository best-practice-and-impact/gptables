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

class TestGPWorksheetInit(unittest.TestCase):
    """
    Test that default attributes are set when GPWorksheets are created.
    """
    def setUp(self):
        self.wb = GPWorkbook()
        self.ws = self.wb.add_worksheet()
    
    def test_subclass(self):
        """
        Test that the GPWorksheet class is a subclass of the XlsxWriter
        Worksheet class.
        """
        self.assertTrue(
                issubclass(
                        GPWorksheet,
                        xlsxwriter.worksheet.Worksheet
                        )
                )
    
    def test_default_theme_set(self):
        """
        Test that the default theme (gptheme) is used when no theme is set.
        """
        self.assertEqual(self.ws.theme, gptheme)
    
    def test_default_gridlines(self):
        """
        Test that print and screen gridlines are hidden by default.
        """
        self.assertEqual(self.ws.print_gridlines, 0)
        self.assertEqual(self.ws.screen_gridlines, 0)
        
    def test_wb_reference(self):
        """
        Test that GPWorksheets reference their parent GPWorkbook.
        """
        self.assertEqual(self.ws._workbook, self.wb)
    
    def test_invalid_write_gptable(self):
        """
        Test that write_gptable() raises a TypeError when argument is not a
        gptables.GPTable object.
        """
        tests = [dict(),
                 set(),
                 [],
                 1,
                 3.14,
                 "test_string",
                 pd.DataFrame()
                ]
        attr = "write_gptable"
        for test in tests:
            with self.subTest(
                            attr = attr,
                            test = test
                            ):
                with self.assertRaises(TypeError):
                    self.ws.write_gptable(test)

class TestGPWorksheetWriting(unittest.TestCase):
    """
    Test that additional writing methods correctly write to GPWorksheet object.
    """
    def setUp(self):
        self.fh = StringIO()
        self.wb = GPWorkbook()
        self.ws = self.wb.add_worksheet()
        self.ws._set_filehandle(self.fh)
        
        
        self.test_string = "Just a string"
        self.test_rich_string = [
                "More than ",
                {"italic": True},  # Rich element
                "just ",
                "a string"
                ]
        self.test_format = {}
    
    def test__smart_write_str(self):
        """
        Test that strings are stored in the GPWorksheet as expected.
        """
        self.ws._smart_write(0, 0, self.test_string, {})
        # Strings are stored in a lookup table for efficiency
        got_string = self.ws.str_table.string_table
        exp_string = {self.test_string: 0}
        self.assertEqual(got_string, exp_string)
        
        # String is referenced using a named tuple (string, Format)
        # Here we get first element, which references string lookup location
        got_lookup = self.ws.table[0][0][0]
        exp_lookup = 0
        self.assertEqual(got_lookup, exp_lookup)

    def test__smart_write_formatted_str(self):
        self.ws._smart_write(1, 2, self.test_string, {"bold": True})
        # Strings are stored in a lookup table for efficiency
        got_string = self.ws.str_table.string_table
        exp_string = {self.test_string: 0}
        self.assertEqual(got_string, exp_string)
        
        # String is referenced using a named tuple (string, Format)
        # Here we get first element, which references string lookup location
        cell = self.ws.table[1][2] 
        got_lookup = cell[0]
        exp_lookup = 0
        self.assertEqual(got_lookup, exp_lookup)
        
        format_obj = cell[1]
        self.assertTrue(format_obj.bold)
        

    def test__smart_write_rich_text(self):
        wb = GPWorkbook()
        wb.set_theme(Theme({}))
        ws = wb.add_worksheet()
        
        ws._smart_write(0, 0, self.test_rich_string, {})
        # Strings are stored in a lookup table for efficiency
        got_string = ws.str_table.string_table
        exp_string = {'<r><t xml:space="preserve">More than </t></r><r><rPr><i'
                      '/><sz val="11"/><color theme="1"/><rFont val="Calibri"/'
                      '><family val="2"/><scheme val="minor"/></rPr><t xml:spa'
                      'ce="preserve">just </t></r><r><rPr><sz val="11"/><color'
                      ' theme="1"/><rFont val="Calibri"/><family val="2"/><sch'
                      'eme val="minor"/></rPr><t>a string</t></r>': 0}
        self.assertEqual(got_string, exp_string)
        
        # String is referenced using a named tuple (string, Format)
        # Here we get first element, which references string lookup location
        got_lookup = ws.table[0][0][0]
        exp_lookup = 0
        self.assertEqual(got_lookup, exp_lookup)
    
    def test__smart_write_formatted_rich_text(self):
        wb = GPWorkbook()
        wb.set_theme(Theme({}))
        ws = wb.add_worksheet()
        
        ws._smart_write(1, 2, self.test_rich_string, {"bold": True})
        # Strings are stored in a lookup table for efficiency
        got_string = ws.str_table.string_table
        exp_string = {'<r><t xml:space="preserve">More than </t></r><r><rPr><b'
                      '/><i/><sz val="11"/><color theme="1"/><rFont val="Calib'
                      'ri"/><family val="2"/><scheme val="minor"/></rPr><t xml'
                      ':space="preserve">just </t></r><r><rPr><b/><sz val="11"'
                      '/><color theme="1"/><rFont val="Calibri"/><family val="'
                      '2"/><scheme val="minor"/></rPr><t>a string</t></r>': 0}

        self.assertEqual(got_string, exp_string)
        
        # String is referenced using a named tuple (string, Format)
        # Here we get first element, which references string lookup location
        cell = ws.table[1][2] 
        got_lookup = cell[0]
        exp_lookup = 0
        self.assertEqual(got_lookup, exp_lookup)
        
        format_obj = cell[1]
        self.assertTrue(format_obj.bold)

class TestGPWorksheetFooterText(unittest.TestCase):
    """
    Test that GPTable footer elements are modified correctly by GPWorksheet
    during write_gptable().
    """
    def setUp(self):
        self.ws = GPWorksheet()
        self.ordered_refs = []
        
        self.test_text_list = [
                "This has a $$reference$$",
                "This one doesn't",
                "Here's another $$one$$"
                ]
        self.exp_text_list = [
                "This has a (1)",
                "This one doesn't",
                "Here's another (2)"
                ]

    def test__enclose_text_string(self):
        """
        Test that strings are correctly flanked with parentheses.
        """
        test_string = "An example note"
        got = self.ws._enclose_text(test_string)
        exp = "(An example note)"
        self.assertEqual(got, exp)

    def test__enclose_text_list(self):
        """
        Test that rich text is flanked with parentheses.
        """
        test_list = ["An", {"bold": True}, "example", "note"]
        got = self.ws._enclose_text(test_list)
        exp = ["(", "An", {"bold": True}, "example", "note", ")"]
        self.assertEqual(got, exp)
        
    def test__replace_reference(self):
        """
        Test that references ($$ref$$ style) in strings are replaced with
        numbers, in order of appearance.
        """
        got_text = []
        for text in self.test_text_list:
            got_text.append(
                    self.ws._replace_reference(text, self.ordered_refs)
                    )
        
        got = self.ordered_refs
        exp = ["reference", "one"]
        self.assertEqual(got, exp)
        
        self.assertEqual(got_text, self.exp_text_list)

    def test__replace_reference_in_attr_str(self):
        """
        Test that references are replaced in a single string.
        """
        got_text = self.ws._replace_reference_in_attr(
                self.test_text_list[0],
                self.ordered_refs
                )
        
        got = self.ordered_refs
        exp = ["reference"]
        self.assertEqual(got, exp)

        self.assertEqual(got_text, self.exp_text_list[0])

    def test__replace_reference_in_attr_list(self):
        """
        Test that references are replaced in a list.
        """
        got_text = self.ws._replace_reference_in_attr(
                self.test_text_list,
                self.ordered_refs
                )
        
        got = self.ordered_refs
        exp = ["reference", "one"]
        self.assertEqual(got, exp)

        self.assertEqual(got_text, self.exp_text_list)

    def test__replace_reference_in_attr_dict(self):
        """
        Test that references are replaced in dictonary values, but not keys.
        """
        test_text_dict = {
                "$$key$$": "This is a value with a $$reference$$",
                "another_key": "Another value",
                "third_key": "$$one$$ more reference"
                }
        got_text = self.ws._replace_reference_in_attr(
                test_text_dict,
                self.ordered_refs
                )
        
        got = self.ordered_refs
        exp = ["reference", "one"]
        self.assertEqual(got, exp)
        
        exp_text_dict = {
                "$$key$$": "This is a value with a (1)",
                "another_key": "Another value",
                "third_key": "(2) more reference"
                }
        
        self.assertEqual(got_text, exp_text_dict)


class TestGPWorksheetFormatUpdate(unittest.TestCase):
    """
    Test that GPWorksheet format updating methods work as expected.
    """
    def setUp(self):
        self.ws = GPWorksheet()

    def test__apply_format_dict(self):
        test = dict()
        format_dict = {"bold": True}
        self.ws._apply_format(test, format_dict)
        exp = {"bold": True}
        self.assertEqual(test, exp)

    def test__apply_format_series(self):
        test = pd.Series([{} for n in range(3)])
        format_dict = {"bold": True}
        self.ws._apply_format(test, format_dict)
        exp = pd.Series([{"bold": True} for n in range(3)])
        assert_series_equal(test, exp)

    def test__apply_format_dataframe(self):
        test = pd.DataFrame(columns=[0, 1, 2], index = [0, 1])
        test.iloc[0] = [{} for n in range(3)]
        test.iloc[1] = [{} for n in range(3)]
        
        format_dict = {"bold": True}
        self.ws._apply_format(test, format_dict)
        exp = pd.DataFrame(columns=[0, 1, 2], index = [0, 1])
        exp.iloc[0] = [{"bold": True} for n in range(3)]
        exp.iloc[1] = [{"bold": True} for n in range(3)]
        assert_frame_equal(test, exp)


class TestGPWorkbook(unittest.TestCase):
    """
    Test that GPWorkbook initialisation and methods work as expected.
    """
    def setUp(self):
        self.wb = GPWorkbook("filename.xlsx")
    
    def test_subclass(self):
        """
        Test that the GPWorkbook class is a subclass of the XlsxWriter
        Workbook class.
        """
        self.assertTrue(
                issubclass(
                        GPWorkbook,
                        xlsxwriter.Workbook
                        )
                )
    
    def test_default_theme_set(self):
        """
        Test that the workbook theme is set to gptheme by default.
        """        
        self.assertEqual(self.wb.theme, gptheme)
    
    def test_valid_set_theme(self):
        """
        Test that setting a new theme with a Theme object works as expected.
        """
        theme_config = {"title": {"bold": True}}
        theme = gptables.Theme(theme_config)
        self.wb.set_theme(theme)
        
        self.assertEqual(
                self.wb.theme,
                gptables.Theme(theme_config)
                )
    
    def test_invalid_set_theme(self):
        """
        Test that setting theme with an object that is not a gptables.Theme
        raises a TypeError.
        """
        tests = [dict(),
                 set(),
                 [],
                 1,
                 3.14,
                 "test_string",
                 pd.DataFrame()
                ]
        attr = "set_theme"
        for test in tests:
            with self.subTest(
                            attr = attr,
                            test = test
                            ):
                with self.assertRaises(TypeError):
                    self.wb.set_theme(test)
