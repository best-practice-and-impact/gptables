import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from contextlib import contextmanager


from gptables import GPTable


# TODO: These should be stored in GPTable
gptable_text_attrs = ["title", "scope", "units", "source"]

gptable_list_text_attrs = ["subtitles", "legend", "notes"]


valid_index_columns = [
    {},
    {1: "one"},
    {1: "one", 2: "two"},
    {1: "one", 2: "two", 3: "three"}
    ]

valid_text_elements = [
    "This is a string",
    ["This is ", {"bold": True}, "rich", "text"],
    None
]

invalid_text_elements = [
    dict(),
    set(),
    42,
    3.14,
    True
]


@contextmanager
def does_not_raise():
    yield


@pytest.fixture(scope="function")
def create_gptable_with_kwargs():

    def generate_gptable(format_dict=None):
        base_gptable = {
            "table": pd.DataFrame(),
            "title": "",
            "scope": "",
            "units": "",
            "source": "",
            "index_columns": {}  # Override default, as no columns in table
            }
        if format_dict is not None:
            base_gptable.update(format_dict)
        return GPTable(**base_gptable)

    return generate_gptable


def test_init_defaults(create_gptable_with_kwargs):
    """
    Test that given a minimal input, default attributes are correct types.
    """
    empty_gptable = create_gptable_with_kwargs()

    # Required args
    assert empty_gptable.title == ""
    assert empty_gptable.scope == ""
    assert empty_gptable.units == ""
    assert empty_gptable.source == ""
    assert_frame_equal(
            empty_gptable.table, pd.DataFrame().reset_index(drop=True)
            )
    
    # Optional args
    assert empty_gptable.index_columns == {}
    assert empty_gptable.subtitles == []
    assert empty_gptable.legend == []
    assert empty_gptable.annotations == {}
    assert empty_gptable.notes == []
    assert empty_gptable.additional_formatting == []
    assert empty_gptable.include_index_column_headings == False
    
    # Other
    assert empty_gptable.index_levels == 0
    assert empty_gptable._column_headings == set()
    assert empty_gptable._VALID_INDEX_LEVELS == [1, 2, 3]
    

class TestAttrValidationGPTable:
    @pytest.mark.parametrize("level", [4, 0, -1])
    def test_invalid_index_level(self, level, create_gptable_with_kwargs):
        """
        Test that GPTable index_columns raises error when an index level is
        invalid.
        """
        with pytest.raises(ValueError):
            create_gptable_with_kwargs({
                "table": pd.DataFrame(columns=["one", "two", "three"]),
                # Valid column index, but invalid level
                "index_columns": {level: 0}
                })
                

    @pytest.mark.parametrize("idx,expectation", [
        (0, does_not_raise()),
        (1, does_not_raise()),
        (3, pytest.raises(ValueError)),
        (-1, pytest.raises(ValueError))
    ])
    def test_invalid_column_index(self, idx, expectation, create_gptable_with_kwargs):
        """
        Test that GPTable index_columns raises error when a column index number
        is invalid.
        """
        with expectation:
            create_gptable_with_kwargs({
                "table": pd.DataFrame(columns=["one", "two", "three"]),  
                # Valid index level, but non existent column
                "index_columns": {1: idx}
                })
            

    @pytest.mark.parametrize("index_cols,col_headings", zip(
        valid_index_columns, [
            {0, 1, 2, 3},
            {1, 2, 3},
            {2, 3},
            {3}
            ]
        ))
    def test_set_column_index(self, index_cols, col_headings, create_gptable_with_kwargs):
        """
        Test that setting GPTable index_columns with valid column index works
        as expected.
        """
        gptable = create_gptable_with_kwargs({
            "table": pd.DataFrame(columns=["one", "two", "three", "four"]),
            "index_columns": index_cols
            })
        assert gptable.index_columns == index_cols
        assert gptable.index_levels == len(index_cols)
        assert gptable._column_headings == col_headings
        

    @pytest.mark.parametrize("not_a_table", [1, "?", [1,3,5,6]])
    def test_invalid_table_type(self, not_a_table, create_gptable_with_kwargs):
        """
        Test that setting GPTable table to object that is not a
        pandas.DataFrame raises an error.
        """
        with pytest.raises(TypeError):
            create_gptable_with_kwargs({"table": not_a_table})
    

    @pytest.mark.parametrize("attr", gptable_text_attrs)
    @pytest.mark.parametrize("not_text", invalid_text_elements)
    def test_invalid_text_in_str_attrs(self, attr, not_text, create_gptable_with_kwargs):
        """
        Test that setting an invalid GPTable text types raises a TypeError for
        each attribute that holds a string.
        """
        with pytest.raises(TypeError):
            create_gptable_with_kwargs({attr: not_text})
    

    @pytest.mark.parametrize("attr", gptable_text_attrs)
    @pytest.mark.parametrize("text", valid_text_elements)
    def test_valid_text_in_str_attrs(self, attr, text, create_gptable_with_kwargs):
        """
        Test that setting valid GPTable text elements works as expected. Test
        strings and list containing strings and format dicts (rich text).
        Also test that None is allowed.
        """
        gptable = create_gptable_with_kwargs({attr: text})
        assert getattr(gptable, attr) == text
    

    @pytest.mark.parametrize("attr", gptable_list_text_attrs)
    @pytest.mark.parametrize("text", invalid_text_elements)
    def test_invalid_text_in_list_attrs(self, attr, text, create_gptable_with_kwargs):
        """
        Test that setting list of invalid text elements to GPTable list
        parameters raises a TypeError.
        """
        text = [text, text]
        with pytest.raises(TypeError):
            create_gptable_with_kwargs({attr: text})


    @pytest.mark.parametrize("attr", gptable_list_text_attrs)
    @pytest.mark.parametrize("text", valid_text_elements)
    def test_valid_text_in_list_attrs(self, attr, text, create_gptable_with_kwargs):
        """
        Test that setting list of valid text elements to GPTable list
        parameters works as expected.
        """
        if text is not None:
            text = [text, text]
        gptable = create_gptable_with_kwargs({attr: text})
        if text is not None:
            assert getattr(gptable, attr) == text
        else:
            assert getattr(gptable, attr) == []


    @pytest.mark.parametrize("reference", [42, (0, 0), None])
    def test_invalid_annotations_keys(self, reference, create_gptable_with_kwargs):
        """
        Test that setting annotations keys that are not strings raise a
        TypeError.
        """    
        with pytest.raises(TypeError):
            create_gptable_with_kwargs({
                "annotations": {reference: "valid value"}
                })
    

    @pytest.mark.parametrize("reference", ["1", "spam"])
    def test_valid_annotations_keys(self, reference, create_gptable_with_kwargs):
        """
        Test that setting str annotation keys works.
        """
        gptable = create_gptable_with_kwargs({
            "annotations": {reference: "valid value"}
            })
        assert getattr(gptable, "annotations") == {reference: "valid value"}
    

    @pytest.mark.parametrize("text", invalid_text_elements)
    def test_invalid_annotations_values(self, text, create_gptable_with_kwargs):
        """
        Test that setting annotations values that are not valid text elements
        raises a TypeError.
        """
        with pytest.raises(TypeError):
            create_gptable_with_kwargs({
            "annotations": {"valid_key": text}
            })
    

    @pytest.mark.parametrize("text", valid_text_elements)
    def test_valid_annotations_values(self, text, create_gptable_with_kwargs):
        """
        Test that setting annotations values that valid text elements works as
        expected.
        """        
        gptable = create_gptable_with_kwargs({
            "annotations": {"valid_key": text}
            })
        assert getattr(gptable, "annotations") == {"valid_key": text}
    

    @pytest.mark.parametrize("key", invalid_text_elements[2:] + ["invalid_key"])
    def test_invalid_additional_format_keys(self, key, create_gptable_with_kwargs):
        """
        Test that adding additional formatting with an invalid key raises an
        error.
        """
        with pytest.raises(ValueError):
            create_gptable_with_kwargs({
            "additional_formatting": [{key: {"format": {"bold": True}}}]
            })
        

    @pytest.mark.parametrize("key", ["cell", "row", "column"])
    def test_valid_additional_format_keys(self, key, create_gptable_with_kwargs):
        """
        Test that adding additional formatting with a valid key (column, row or
        cell) works as expected.
        """
        gptable = create_gptable_with_kwargs({
            "additional_formatting": [
                    {key: {"format": {"bold": True}}}]
            })
        assert getattr(gptable, "additional_formatting") == [{key: {"format": {"bold": True}}}]
    

    @pytest.mark.parametrize("format_label", invalid_text_elements[2:] + ["not_a_format"])
    def test_invalid_additional_format_labels(self, format_label, create_gptable_with_kwargs):
        """
        Test that adding additional formatting with a format parameter that is
        not supported by XlsxWriter raises an error.
        """
        with pytest.raises(ValueError):
            create_gptable_with_kwargs({
                "additional_formatting": 
                    [
                        {"cell":
                            {"format": {format_label: True},
                                "cells": (0, 0)
                                }
                        }
                    ]
                })
    

    @pytest.mark.parametrize(
        "format_dict",[
            {"bold": True},
            {"font_size": 17},
            {"align": "center"},
            {"font_color": "red"},
            {"bottom": 1}
            ])
    def test_valid_additional_format_labels(self, format_dict, create_gptable_with_kwargs):
        """
        Test that adding additional formatting with a format parameter that is
         supported by XlsxWriter works as expected.
        """
        additional_formatting = [
                    {"cell":
                        {"format": format_dict,
                            "cells": (0, 0)
                            }
                        }
                    ]
        gptable = create_gptable_with_kwargs({
             "additional_formatting": additional_formatting
            })
        assert getattr(gptable, "additional_formatting") == additional_formatting


@pytest.mark.parametrize("index_cols", valid_index_columns)
class TestIndirectAttrs:
    """
    Test that non-formatting create_gptable_with_kwargs attributes are indirectly set correctly.
    """
    def test_index_levels_set(self, index_cols, create_gptable_with_kwargs):
        """
        Test that number of index levels are set, when one, two or three
        indexes are used.
        """
        gptable = create_gptable_with_kwargs({
            "table": pd.DataFrame(
                columns = [
                    "one",
                    "two",
                    "three",
                    "four"
                    ]),
            "index_columns": index_cols
            })
        assert getattr(gptable, "index_levels") == len(index_cols)
        

    def test_column_headings_set(self, index_cols, create_gptable_with_kwargs):
        """
        Test that non-index columns are set as column headings.
        """
        gptable = create_gptable_with_kwargs({
            "table": pd.DataFrame(
                columns = [
                    "one",
                    "two",
                    "three",
                    "four"
                    ]),
            "index_columns": index_cols
            })
        
        # Expect all column numbers that have no index level assigned
        exp = set(range(4)) - set(range(len(index_cols)))
        
        assert getattr(gptable, "_column_headings") == exp
