import unittest
import pandas as pd
from pandas.testing import assert_frame_equal

from gptables import GPTable

class TestInitGPTable(unittest.TestCase):
    def setUp(self):
        self.gptable = GPTable(
                pd.DataFrame(),
                "",
                "",
                "",
                "",
                index_columns={}  # Override default, as no columns in table
                )
        
    def test_default_types(self):
        """
        Test that given a minimal input, default attributes are correct types.
        """
        # Required args
        self.assertEqual(self.gptable.title, "")
        self.assertEqual(self.gptable.scope, "")
        self.assertEqual(self.gptable.units, "")
        self.assertEqual(self.gptable.source, "")
        assert_frame_equal(
                self.gptable.table, pd.DataFrame().reset_index(drop=True)
                )
        
        # Optional args
        self.assertEqual(self.gptable.index_columns, {})
        self.assertEqual(self.gptable.subtitles, [])
        self.assertEqual(self.gptable.legend, [])
        self.assertEqual(self.gptable.annotations, {})
        self.assertEqual(self.gptable.notes, [])
        self.assertEqual(self.gptable.additional_formatting, [])
        
        # Other
        self.assertEqual(self.gptable.index_levels, 0)
        self.assertEqual(self.gptable._column_headings, set())
        self.assertEqual(self.gptable._VALID_INDEX_LEVELS, [1, 2, 3])
        

class TestAttrValidationGPTable(unittest.TestCase):
    """
    Test validation of inputs.
    """
    def setUp(self):
        self.default_kwargs = {
                "table": pd.DataFrame(),
                "title": "",
                "scope": "",
                "units": "",
                "source": "",
                "index_columns": {}
                }

        self.text_attrs = [
                "title",
                "scope",
                "units",
                "source"
                ]
        
        self.list_text_attrs = [
                "subtitles",
                "legend",
                "notes"
                ]
    
    def test_invalid_index_level(self):
        """
        Test that GPTable index_columns raises error when an index level is
        invalid.
        """
        kwargs = self.default_kwargs.copy()
        kwargs.update({
                "table": pd.DataFrame(columns=["1", "2"]),  # Table with cols,
                "index_columns": {0: 0}  # Key not a valid level
                })
        with self.assertRaises(ValueError):
            GPTable(**kwargs)
                
    def test_invalid_column_number(self):
        """
        Test that GPTable index_columns raises error when a column number
        is invalid.
        """
        kwargs = self.default_kwargs.copy()
        kwargs.update({
                "table": pd.DataFrame(columns=["1", "2"]),  # Table with cols
                # Valid index level, but non existent column
                "index_columns": {1: 3}
                })
        with self.assertRaises(ValueError):
            GPTable(**kwargs)
            
    def test_valid_column_number(self):
        """
        Test that setting GPTable index_columns with valid column numbers works
        as expected.
        """
        kwargs = self.default_kwargs.copy()
        kwargs.update({
                "table": pd.DataFrame(columns=["1", "2"]),  # Table with cols
                # Valid index level, but non existent column
                "index_columns": {1: 0}
                })

        gptable = GPTable(**kwargs)
        self.assertEqual(
                gptable.index_columns,
                {1: 0}
                )
        self.assertEqual(
                gptable.index_levels,
                1
                )
        self.assertEqual(
                gptable._column_headings,
                {1}  # First heading (iloc 0) should be an index column
                )
        
    def test_invalid_table_type(self):
        """
        Test that setting GPTable table to object that is not a
        pandas.DataFrame raises an error.
        """
        kwargs = self.default_kwargs.copy()
        kwargs.update({
                "table": "Just a fake table"  # Str table
                })
        with self.assertRaises(TypeError):
            GPTable(**kwargs)
    
    def test_invalid_text_in_str_attrs(self):
        """
        Test that setting an invalid GPTable text types raises a TypeError for
        each attribute that holds a string.
        """
        test_dict = dict()
        test_set = set()
        test_int = 1
        test_float = 3.14
        
        kwargs = self.default_kwargs.copy()
        for attr in self.text_attrs:
                kwargs = self.default_kwargs.copy()
                for test in [test_dict, test_set, test_int, test_float]:
                    with self.subTest(
                            attr = attr,
                            test = test
                            ):
                        kwargs.update({
                                attr: test
                                })
                        with self.assertRaises(TypeError):
                            GPTable(**kwargs)
    
    def test_valid_text_in_str_attrs(self):
        """
        Test that setting valid GPTable text elements works as expected. Test
        strings and list containing strings and format dicts (rich text).
        Also test that None is allowed.
        """
        test_string = "This is a string"
        test_rich_text = ["This is ", {"bold": True}, "rich", "text"]
        test_none = None
        
        for attr in self.text_attrs:
            kwargs = self.default_kwargs.copy()
            for test in [test_string, test_rich_text, test_none]:
                with self.subTest(
                        attr = attr,
                        test = test
                        ):
                    kwargs.update({
                            attr: test
                            })
                    gptable = GPTable(**kwargs)
                    self.assertEqual(
                            getattr(gptable, attr),
                            test
                            )
    
    def test_invalid_text_in_list_attrs(self):
        """
        Test that setting list of invalid text elements to GPTable list
        parameters raises a TypeError.
        """
        test_dict = dict()
        test_set = set()
        test_int = 1
        test_float = 3.14
        
        kwargs = self.default_kwargs.copy()
        for attr in self.list_text_attrs:
                kwargs = self.default_kwargs.copy()
                for test in [test_dict, test_set, test_int, test_float]:
                    test = [test, test]
                    with self.subTest(
                            attr = attr,
                            test = test
                            ):
                        kwargs.update({
                                attr: test
                                })
                        with self.assertRaises(TypeError):
                            GPTable(**kwargs)

    def test_valid_text_in_list_attrs(self):
        """
        Test that setting list of valid text elements to GPTable list
        parameters works as expected.
        """
        test_string = "This is a string"
        test_rich_text = ["This is ", {"bold": True}, "rich", "text"]
        test_none = None
        
        for attr in self.list_text_attrs:
                kwargs = self.default_kwargs.copy()
                for test in [test_string, test_rich_text, test_none]:
                    test = [test, test]
                    with self.subTest(
                            attr = attr,
                            test = test
                            ):
                        kwargs.update({
                            attr: test
                            })
                        gptable = GPTable(**kwargs)
                        self.assertEqual(
                                getattr(gptable, attr),
                                test
                                )

    def test_invalid_annotations_keys(self):
        """
        Test that setting annotations keys that are not strings raise a
        TypeError.
        """
        test_dict = dict()
        test_set = set()
        test_int = 1
        test_float = 3.14
        test_rich_text = ["This is ", {"bold": True}, "rich", "text"]
        test_none = None
        
        kwargs = self.default_kwargs.copy()
        attr = "annotations"
        for test in [test_dict,
                     test_set,
                     test_int,
                     test_float,
                     test_rich_text,
                     test_none
                     ]:
            with self.subTest(
                    test = test
                    ):
                with self.assertRaises(TypeError):
                    kwargs.update({
                        attr: {test: "valid value"}
                        })
                    GPTable(**kwargs)
    
    def test_valid_annotations_keys(self):
        """
        Test that setting annotations keys that strings works as expected.
        """
        test_string = "This is a string"
        
        kwargs = self.default_kwargs.copy()
        attr = "annotations"
        test = test_string
        with self.subTest(
                attr = attr,
                test = test
                ):
            kwargs.update({
                attr: {"valid_key": test}
                })
            gptable = GPTable(**kwargs)
            self.assertEqual(
                    getattr(gptable, attr),
                    {"valid_key": test}
                    )
    
    def test_invalid_annotations_values(self):
        """
        Test that setting annotations values that are not valid text elements
        raises a TypeError.
        """
        test_dict = dict()
        test_set = set()
        test_int = 1
        test_float = 3.14
        
        kwargs = self.default_kwargs.copy()
        attr = "annotations"
        for test in [test_dict,
                     test_set,
                     test_int,
                     test_float
                     ]:
            with self.subTest(
                    attr = attr,
                    test = test
                    ):
                kwargs.update({
                        attr: {"valid_key": test}
                        })
                with self.assertRaises(TypeError):
                    GPTable(**kwargs)
    
    def test_valid_annotations_values(self):
        """
        Test that setting annotations values that valid text elements works as
        expected.
        """
        test_string = "This is a string"
        test_rich_text = ["This is ", {"bold": True}, "rich", "text"]
        test_none = None
        
        kwargs = self.default_kwargs.copy()
        attr = "annotations"
        for test in [test_string, test_rich_text, test_none]:
            with self.subTest(
                    attr = attr,
                    test = test
                    ):
                kwargs.update({
                    "annotations": {"valid_key": test}
                    })
                gptable = GPTable(**kwargs)
                self.assertEqual(
                        getattr(gptable, attr),
                        {"valid_key": test}
                        )
    
    def test_invalid_addtional_format_keys(self):
        """
        Test that adding addional formatting with an invalid key raises an
        error.
        """
        test_string = "potatoe"
        test_int = 1
        test_float = 3.5
        
        kwargs = self.default_kwargs.copy()
        attr = "additional_formatting"
        for test in [test_string, test_int, test_float]:
            with self.subTest(
                    attr = attr,
                    test = test
                    ):
                kwargs.update({
                    "additional_formatting": [
                            {test:
                                {"format": {"bold": True}}
                                }
                                ]
                    })
                with self.assertRaises(ValueError):
                    GPTable(**kwargs)
        
    
    def test_valid_addtional_format_keys(self):
        """
        Test that adding additional formatting with a valid key (column, row or
        cell) works as expected.
        """
        valid_keys = ["cell", "row", "column"]
        kwargs = self.default_kwargs.copy()
        attr = "additional_formatting"
        for test in valid_keys:
            with self.subTest(
                    attr = attr,
                    test = test
                    ):
                kwargs.update({
                    "additional_formatting": [
                            {test: {"format": {"bold": True}}}]
                    })
                gptable = GPTable(**kwargs)
                self.assertEqual(
                        getattr(gptable, attr),
                        [{test: {"format": {"bold": True}}}]
                        )
    
    def test_invalid_addtional_format_labels(self):
        """
        Test that adding addional formatting with a format parameter that is
        not supported by XlsxWriter raises an error.
        """
        test_string = "potatoe"
        test_int = 1
        test_float = 3.5
        
        kwargs = self.default_kwargs.copy()
        attr = "additional_formatting"
        for test in [test_string, test_int, test_float]:
            with self.subTest(
                    attr = attr,
                    test = test
                    ):
                kwargs.update({
                        # Valid key, invalid format parameters
                    "additional_formatting": 
                        [
                            {"cell":
                                {"format": {test: True},
                                 "cells": (0, 0)
                                 }
                            }
                        ]
                    })
                with self.assertRaises(ValueError):
                    GPTable(**kwargs)
    
    def test_valid_addtional_format_labels(self):
        """
        Test that adding addional formatting with a format parameter that is
         supported by XlsxWriter works as expected.
        """
        valid_formatting = [
                {"bold": True},
                {"font_size": 17},
                {"align": "center"},
                {"font_color": "red"}
                ]
        kwargs = self.default_kwargs.copy()
        attr = "additional_formatting"
        for test in valid_formatting:
            with self.subTest(
                    attr = attr,
                    test = test
                    ):
                kwargs.update({
                    "additional_formatting": [
                            {"cell":
                                {"format": test,
                                 "cells": (0, 0)
                                 }
                            }
                            ]
                    })
                gptable = GPTable(**kwargs)
                self.assertEqual(
                        getattr(gptable, attr),
                        [{"cell":
                                {"format": test,
                                 "cells": (0, 0)
                                 }
                            }]
                        )

class TestOtherAttrSetting(unittest.TestCase):
    """
    Test that other GPTable attributes are indirectly set correctly.
    """
    def setUp(self):
        self.default_kwargs = {
                "table": pd.DataFrame(),
                "title": "",
                "scope": "",
                "units": "",
                "source": "",
                "index_columns": {}
                }
    
    def test_index_levels_set(self):
        """
        Test that number of index levels are set, when one, two or three
        indexes are used.
        """
        valid_index_columns = [
                {},
                {1: "one"},
                {1: "one", 2: "two"},
                {1: "one", 2: "two", 3: "three"}
                ]
        kwargs = self.default_kwargs.copy()
        kwargs.update({
                    "table": pd.DataFrame(
                            columns = [
                                    "one",
                                    "two",
                                    "three",
                                    "four"
                                    ])
                    })
        attr = "index_levels"
        for test in valid_index_columns:
            with self.subTest(
                    attr = attr,
                    index_cols = test
                    ):
                kwargs.update({"index_columns": test})
                gptable = GPTable(**kwargs)
                self.assertEqual(
                        getattr(gptable, attr),
                        len(test)
                        )
        
    def test_column_headings_set(self):
        """
        Test that non-index columns are set as column headings.
        """
        valid_index_columns = [
                {},
                {1: "one"},
                {1: "one", 2: "two"},
                {1: "one", 2: "two", 3: "three"}
                ]
        kwargs = self.default_kwargs.copy()
        kwargs.update({
                    "table": pd.DataFrame(
                            columns = [
                                    "one",
                                    "two",
                                    "three",
                                    "four"
                                    ])
                    })
        attr = "_column_headings"
        for test in valid_index_columns:
            with self.subTest(
                    attr = attr,
                    index_cols = test
                    ):
                kwargs.update({"index_columns": test})
                gptable = GPTable(**kwargs)
                
                # Expect all column numbers not set as index numbers
                exp = set(range(4)) - set(range(len(test)))
                
                self.assertEqual(
                        getattr(gptable, attr),
                        exp
                        )
