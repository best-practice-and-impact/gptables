import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from io import StringIO
from contextlib import redirect_stdout
from pkg_resources import resource_filename

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
    
    def test_invalid_title_type(self):
        """
        Test that setting an invalid GPTable title type raises an error.
        """
        kwargs = self.default_kwargs.copy()
        kwargs.update({"title": {}})
        with self.assertRaises(TypeError):
            GPTable(**kwargs)
    
    def test_valid_title_type(self):
        """
        Test that setting valid GPTable titles works as expected. Test strings
        and list containing strings and format dicts (rich text). Also allow
        None.
        """
        kwargs = self.default_kwargs.copy()
        kwargs.update({
                "title": "This is a str title"
                })
        gptable = GPTable(**kwargs)
        self.assertEqual(
                gptable.title,
                "This is a str title"
                )
        
        kwargs.update({
                "title": ["This is a ", {"bold": True}, "rich", "text title"]
                })
        gptable = GPTable(**kwargs)
        self.assertEqual(
                gptable.title,
                ["This is a ", {"bold": True}, "rich", "text title"]
                )
        
        kwargs.update({
                "title": None
                })
        gptable = GPTable(**kwargs)
        self.assertEqual(
                gptable.title,
                None
                )
