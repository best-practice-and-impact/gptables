import unittest
from io import StringIO
from contextlib import redirect_stdout
from pkg_resources import resource_filename

from gptables import Theme
from gptables import gptheme

class TestCleanInitTheme(unittest.TestCase):
    """
    Test initialisation of the Theme class without config.
    """

    def setUp(self):
        self.fh = StringIO()
        self.theme = Theme()

    
    def test_default_types(self):  
        """Test Theme attribute default types"""
        for attr in self.theme._format_attributes:
            exp = {}
            got = getattr(self.theme, attr)
            self.assertEqual(exp, got)
        
        self.assertEqual(self.theme.footer_order, [])
        self.assertEqual(self.theme.missing_value, None)

    def test_print_attributes(self):
        """Test Theme print_attributes()"""
        
        with redirect_stdout(self.fh):
            self.theme.print_attributes()
        
        got = self.fh.getvalue()

        exp = (
"""title_format : {}
subtitle_format : {}
scope_format : {}
units_format : {}
column_heading_format : {}
index_1_format : {}
index_2_format : {}
index_3_format : {}
data_format : {}
source_format : {}
legend_format : {}
annotations_format : {}
notes_format : {}
footer_order : []
missing_value : None
"""
                )

        self.assertEqual(got, exp)

class TestConfigInitTheme(unittest.TestCase):
    """
    Test initialisation of the Theme class using a config dictionary.
    """

    def test_dict_init(self):
        config = {
            "global":
                {
                 "font_size": 9,
                "font_name": "Arial"
                }, 

            "title":
                {
                 "bold": True,
                "font_size": 11
                },
     
            "subtitle":
                {"font_size": 10},
            
            "scope": None,
            
            "units":
                {
                "align": "right",
                "italic": True
                },
            
            "column_heading":
                {
                "bold": True,
                "bottom": 1
                },
            
            "index_1":
                {"bold": True},
            
            "index_2": None,
            
            "index_3":
                {"italic": True},
            
            "data": None,
            
            "source":
                {"font_size": 7},
            
            "legend":
                {"font_size": 7},
            
            "annotations":
                {"font_size": 7},
            
            "notes":
                {"font_size": 7},
            
            "footer_order":
                [
                "source",
                "legend",
                "annotations",
                "notes",
                ],
            
            "missing_value": ':'
                }
        self.theme = Theme(config)
        
        exp = gptheme
        
        got = self.theme
        
        self.assertEqual(exp, got)
        
    def test_file_init(self):
        """
        Test initialisation of Theme using yaml config file.
        """
        config_file = resource_filename(
                "gptables",
                "themes/gptheme.yaml"
                )
        self.theme = Theme(config_file)
        
        exp = gptheme
        
        got = self.theme
        
        self.assertEqual(exp, got)


class TestFormatValidationTheme(unittest.TestCase):
    """
    Test validation of format dictionaries.
    """
    
    def setUp(self):
        self.theme = Theme()

    def test_invalid_attribute_config(self):
        """
        Test that invalid attribute names in config raises a ValueError.
        """
        config = {"potatoe": {"font_size": 9}}
        with self.assertRaises(ValueError):
            self.theme.apply_config(config)

    def test_invalid_format_label_config(self):
        """
        Test that invalid format labels in config raises a ValueError.
        """
        config = {"notes": {"font_bigness": 5}}
        with self.assertRaises(ValueError):
            self.theme.apply_config(config)
        
    def test_invalid_format_label_single_attr(self):
        """
        Test that `validate_single_format` decorator catches invalid format
        labels in individual format dictionaries.
        """
        format_dict = {"font_bigness": 5}
        
        for format_attr in self.theme._format_attributes:
            with self.subTest(
                    attr = format_attr,
                    test = format_dict
                    ): 
                with self.assertRaises(ValueError):
                    getattr(self.theme, "update_" + format_attr)(format_dict)
    
    def test_valid_format_label(self):
        """
        Test that Theme attribute is correctly updated when valid format label
        is used.
        """
        self.theme.update_annotations_format({"font_size": 9})
        
        exp = {"font_size": 9}
        got = self.theme.annotations_format
        
        self.assertEqual(exp, got)
    
    def test_valid_format_label_config(self):
        """
        Test that valid format labels in config changes specified format attr
        but not an unrelated attr.
        """
        config = {"notes": {"font_size": 5}}
        self.theme.apply_config(config)
        
        exp = {"font_size": 5}
        got = self.theme.notes_format
        
        self.assertEqual(exp, got)
        
        got2 = self.theme.title_format
        
        self.assertEqual({}, got2)


class TestOtherValidationTheme(unittest.TestCase):
    """
    Test validation of non-format Theme attributes.
    """
    def setUp(self):
        self.theme = Theme()

    def test_invalid_footer_order_type(self):
        """
        Test that non-list footer_order entries raise a TypeError.
        """
        tests = [
                "notes",
                {"annotations": 2},
                1,
                3.14,
                False,
                None
                ]
        attr = "footer_order"
        for test in tests:
            with self.subTest(
                    attr = attr,
                    test = test
                    ):
                with self.assertRaises(TypeError):
                    self.theme.update_footer_order(test)
                    
    def test_invalid_footer_order_values(self):
        """
        Test that list footer_order entries containing invalid elements raises
        a ValueError.
        """
        tests = [
                ["potatoe"],
                [1],
                [3.14],
                [dict()],
                [[]]
                ]
        attr = "footer_order"
        for test in tests:
            with self.subTest(
                    attr = attr,
                    test = test
                    ):
                with self.assertRaises(ValueError):
                    self.theme.update_footer_order(test)
    
    def test_valid_footer_order_values(self):
        """
        Test that valid list footer_order entries are used to set
        the corresponding attribute.
        """
        tests = [
                [],
                ["notes"],
                ["legend", "notes", "annotations", "source"]
                ]
        attr = "footer_order"
        for test in tests:
            with self.subTest(
                    attr = attr,
                    test = test
                    ):
                self.theme.update_footer_order(test)
                self.assertEqual(
                        getattr(self.theme, attr),
                                test
                                )
