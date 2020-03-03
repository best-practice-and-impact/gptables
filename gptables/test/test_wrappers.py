import unittest
import pandas as pd
from pandas.testing import assert_frame_equal

import xlsxwriter

import gptables
from gptables.core.wrappers import GPWorkbook
from gptables.core.wrappers import GPWorksheet
from gptables import gptheme



class TestGPWorksheetInit(unittest.TestCase):
    """
    Test that default attributes are set when GPWorksheets are created.
    """
    def setUp(self):
        self.wb = GPWorkbook("filename.xlsx")
        self.ws = self.wb.add_worksheet("worksheet_1")
    
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
                 "test_string"
                ]
        attr = "set_theme"
        for test in tests:
            with self.subTest(
                            attr = attr,
                            test = test
                            ):
                with self.assertRaises(TypeError):
                    self.wb.set_theme(test)
