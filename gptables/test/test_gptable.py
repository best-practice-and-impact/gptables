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
        assert_frame_equal(self.gptable.table, pd.DataFrame())
        
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
