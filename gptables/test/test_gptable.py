import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from contextlib import contextmanager


from gptables import GPTable


# TODO: These should be stored in GPTable
gptable_compulsory_text_attrs = ["title", "instructions"]

gptable_optional_text_attrs = ["scope", "source"]

gptable_list_text_attrs = ["subtitles", "legend"]


valid_index_columns = [
    {},
    {1: "one"},
    {1: "one", 2: "two"},
    {1: "one", 2: "two", 3: "three"}
    ]

valid_text_elements_excl_none = [
    "This is a string",
    ["This is ", {"bold": True}, "rich", "text"],
]

valid_text_elements_incl_none = valid_text_elements_excl_none.copy()
valid_text_elements_incl_none.append(None)

invalid_text_elements_excl_none = [
    dict(),
    set(),
    42,
    3.14,
    True
]

invalid_text_elements_incl_none = invalid_text_elements_excl_none.copy()
invalid_text_elements_incl_none.append(None)

@contextmanager
def does_not_raise():
    yield


@pytest.fixture(scope="function")
def create_gptable_with_kwargs():

    def generate_gptable(format_dict=None):
        base_gptable = {
            "table": pd.DataFrame(),
            "table_name": "table_name",
            "title": "",
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
    assert empty_gptable.table_name == "table_name"

    assert_frame_equal(
            empty_gptable.table, pd.DataFrame().reset_index(drop=True)
            )

    # Optional args
    assert empty_gptable.scope == None
    assert empty_gptable.source == None
    assert empty_gptable.units == None
    assert empty_gptable.index_columns == {}
    assert empty_gptable.subtitles == []
    assert empty_gptable.legend == []
    assert empty_gptable.additional_formatting == []
    assert empty_gptable.instructions == "This worksheet contains one table. Some cells may refer to notes, which can be found on the notes worksheet."

    # Other
    assert empty_gptable.index_levels == 0
    assert empty_gptable._column_headings == set()
    assert empty_gptable._VALID_INDEX_LEVELS == [1, 2, 3]
    assert empty_gptable._annotations == []
    assert empty_gptable.data_range == [2, 0, 2, -1]


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


    def test_set_table_name(self, create_gptable_with_kwargs):
        """
        Test that setting GPTable table name with a valid string works as expected
        """
        gptable = create_gptable_with_kwargs({"table_name": "table_name"})
        assert gptable.table_name == "table_name"


    @pytest.mark.parametrize("invalid_name", invalid_text_elements_incl_none)
    def test_invalid_type_table_name(self, invalid_name, create_gptable_with_kwargs):
        """
        Test that setting GPTable table name to object other than string raises
        an error.
        """
        with pytest.raises(TypeError):
            create_gptable_with_kwargs({"table_name": invalid_name})


    def test_table_name_not_list(self, create_gptable_with_kwargs):
        """
        Test that setting GPTable table name to a list, eg with rich text,
        raises an error.
        """
        with pytest.raises(TypeError):
            create_gptable_with_kwargs({"table_name": []})


    @pytest.mark.parametrize("invalid_name", [" ", "  "])
    def test_invalid_characters_table_name(self, invalid_name, create_gptable_with_kwargs):
        """
        Test that setting GPTable table name to string with whitespace raises
        an error.
        """
        with pytest.raises(ValueError):
            create_gptable_with_kwargs({"table_name": invalid_name})


    @pytest.mark.parametrize("attr", gptable_compulsory_text_attrs)
    @pytest.mark.parametrize("not_text", invalid_text_elements_incl_none)
    def test_invalid_text_in_compulsory_str_attrs(self, attr, not_text, create_gptable_with_kwargs):
        """
        Test that setting an invalid GPTable text types raises a TypeError for
        each attribute that holds a string.
        """
        with pytest.raises(TypeError):
            create_gptable_with_kwargs({attr: not_text})

    @pytest.mark.parametrize("attr", gptable_optional_text_attrs)
    @pytest.mark.parametrize("not_text", invalid_text_elements_excl_none)
    def test_invalid_text_in_optional_str_attrs(self, attr, not_text, create_gptable_with_kwargs):
        """
        Test that setting an invalid GPTable text types raises a TypeError for
        each attribute that holds a string.
        """
        with pytest.raises(TypeError):
            create_gptable_with_kwargs({attr: not_text})
    

    @pytest.mark.parametrize("attr", gptable_compulsory_text_attrs)
    @pytest.mark.parametrize("text", valid_text_elements_excl_none)
    def test_valid_text_in_compulsory_str_attrs(self, attr, text, create_gptable_with_kwargs):
        """
        Test that setting valid GPTable text elements works as expected. Test
        strings and list containing strings and format dicts (rich text).
        Also test that None is allowed.
        """
        gptable = create_gptable_with_kwargs({attr: text})

        if isinstance(text, list):
            assert getattr(gptable, attr).list == text
        else:
            assert getattr(gptable, attr) == text

    @pytest.mark.parametrize("attr", gptable_optional_text_attrs)
    @pytest.mark.parametrize("text", valid_text_elements_incl_none)
    def test_valid_text_in_compulsory_str_attrs(self, attr, text, create_gptable_with_kwargs):
        """
        Test that setting valid GPTable text elements works as expected. Test
        strings and list containing strings and format dicts (rich text).
        Also test that None is allowed.
        """
        gptable = create_gptable_with_kwargs({attr: text})

        if isinstance(text, list):
            assert getattr(gptable, attr).list == text
        else:
            assert getattr(gptable, attr) == text


    @pytest.mark.parametrize("attr", gptable_list_text_attrs)
    @pytest.mark.parametrize("text", invalid_text_elements_incl_none)
    def test_invalid_text_in_list_attrs(self, attr, text, create_gptable_with_kwargs):
        """
        Test that setting list of invalid text elements to GPTable list
        parameters raises a TypeError.
        """
        text = [text, text]
        with pytest.raises(TypeError):
            create_gptable_with_kwargs({attr: text})


    @pytest.mark.parametrize("attr", gptable_list_text_attrs)
    @pytest.mark.parametrize("text", valid_text_elements_excl_none)
    def test_valid_text_in_list_attrs(self, attr, text, create_gptable_with_kwargs):
        """
        Test that setting list of valid text elements to GPTable list
        parameters works as expected.
        """
        text_list = [text, text]
        gptable = create_gptable_with_kwargs({attr: text_list})

        if isinstance(text, list):
            assert all([element.list == text for element in getattr(gptable, attr)])
        else:
            assert getattr(gptable, attr) == text_list


    @pytest.mark.parametrize("key", invalid_text_elements_incl_none[2:] + ["invalid_key"])
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
    

    @pytest.mark.parametrize("format_label", invalid_text_elements_incl_none[2:] + ["not_a_format"])
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


    @pytest.mark.parametrize("unit_text", valid_text_elements_excl_none)
    @pytest.mark.parametrize("column_id", ["columnA", 0])
    def test_units_placement(self, unit_text, column_id, create_gptable_with_kwargs):
        """
        Test that units are placed correctly under column headers.
        """
        table_with_units = pd.DataFrame(columns=[f"columnA\n({unit_text})"])

        gptable = create_gptable_with_kwargs({
            "table": pd.DataFrame(columns=["columnA"]),
        })

        gptable.set_units(new_units = {column_id: unit_text})

        assert gptable.table.columns == table_with_units.columns


    @pytest.mark.parametrize("column_id", ["columnA", 0])
    def test_table_notes_placement(self, column_id, create_gptable_with_kwargs):
        """
        Test that units are placed correctly under column headers.
        """
        table_with_notes = pd.DataFrame(columns=[f"columnA\n$$note_reference$$"])

        gptable = create_gptable_with_kwargs({
            "table": pd.DataFrame(columns=["columnA"])
        })

        gptable.set_table_notes(
            new_table_notes = {column_id: "$$note_reference$$"}
        )

        assert gptable.table.columns == table_with_notes.columns


    @pytest.mark.parametrize("column_id", ["columnA", 0])
    def test_table_units_and_notes_placement(self, column_id, create_gptable_with_kwargs):
        """
        Test that units and notes are placed correctly under column headers.
        """
        table_with_units_and_notes = pd.DataFrame(
            columns=[f"columnA\n(unit)\n$$note_reference$$"]
        )

        gptable = create_gptable_with_kwargs({
            "table": pd.DataFrame(columns=["columnA"])
        })

        gptable.set_units(new_units = {column_id: "unit"})
        gptable.set_table_notes(new_table_notes = {column_id: "$$note_reference$$"})

        assert gptable.table.columns == table_with_units_and_notes.columns


    def test_additional_formatting_with_units(self, create_gptable_with_kwargs):
        """
        Test that units are placed correctly under column headers.
        """

        gptable = create_gptable_with_kwargs({
            "table": pd.DataFrame(columns=["columnA"]),
            "units": {"columnA": "unit"},
            "additional_formatting": [{"column": {
                    "columns": ["columnA"],
                    "format": {"bold": True}
                    }}]
        })

        assert gptable.additional_formatting == [{"column": {
            "columns": ["columnA\n(unit)"],
            "format": {"bold": True}
        }}]


    def test_additional_formatting_with_table_notes(self, create_gptable_with_kwargs):
        """
        Test that units are placed correctly under column headers.
        """

        gptable = create_gptable_with_kwargs({
            "table": pd.DataFrame(columns=["columnA"]),
            "table_notes": {"columnA": "$$ref$$"},
            "additional_formatting": [{"column": {
                    "columns": ["columnA"],
                    "format": {"bold": True}
                    }}]
        })

        assert gptable.additional_formatting == [{"column": {
            "columns": ["columnA\n$$ref$$"],
            "format": {"bold": True}
        }}]


    def test_additional_formatting_with_units_and_table_notes(self, create_gptable_with_kwargs):
        """
        Test that units are placed correctly under column headers.
        """

        gptable = create_gptable_with_kwargs({
            "table": pd.DataFrame(columns=["columnA"]),
            "units": {"columnA": "unit"},
            "table_notes": {"columnA": "$$ref$$"},
            "additional_formatting": [{"column": {
                    "columns": ["columnA"],
                    "format": {"bold": True}
                    }}]
        })

        assert gptable.additional_formatting == [{"column": {
            "columns": ["columnA\n(unit)\n$$ref$$"],
            "format": {"bold": True}
        }}]


    @pytest.mark.parametrize("column_names,expectation", [
        (["columnA", "columnB"], does_not_raise()),
        (["columnA", ""], pytest.raises(ValueError)),
        ([None, "columnB"], pytest.raises(ValueError))
    ])
    def test__validate_all_column_names_have_text(self, column_names, expectation, create_gptable_with_kwargs):
        """
        Test that GPTable raises error when there are null values or empty strings for column names.
        """
        with expectation:
            create_gptable_with_kwargs({
                "table": pd.DataFrame(columns=column_names)
                })


    @pytest.mark.parametrize("column_names,expectation", [
        (["columnA", "columnB", "columnC"], does_not_raise()),
        (["columnA", "columnB", "columnB"], pytest.raises(ValueError))
    ])
    def test__validate_no_duplicate_column_names(self, column_names, expectation, create_gptable_with_kwargs):
        """
        Test that GPTable raises error when there are duplicate column names in table data.
        """
        with expectation:
            create_gptable_with_kwargs({
                "table": pd.DataFrame(columns=column_names)
                })



class TestIndirectAttrs:
    """
    Test that non-formatting create_gptable_with_kwargs attributes are indirectly set correctly.
    """
    @pytest.mark.parametrize("index_cols", valid_index_columns)
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


    @pytest.mark.parametrize("index_cols", valid_index_columns)
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


    def test__annotations_set(self, create_gptable_with_kwargs):
        """
        Test that annotation references in `gptable` attributes are found and
        added to `_annotations` as expected.
        """
        table = pd.DataFrame(columns=["col"])

        kwargs = {
            "title": "Title$$1$$",
            "subtitles": ["Subtitle$$2$$"],
            "instructions": "Instructions$$3$$",
            "source": "Source$$4$$",
            "scope": "Scope$$5$$",
            "legend": ["Legend$$6$$"],
            "units": {0: "Unit$$7$$"},
            "table_notes": {0: "Note$$8$$"},
            "table": table
        }

        gptable = create_gptable_with_kwargs(kwargs)

        description_order = ["instructions", "source", "scope", "legend"]
        gptable._set_annotations(description_order)

        assert gptable._annotations == ["1", "2", "3", "4", "5", "6", "7", "8"]
