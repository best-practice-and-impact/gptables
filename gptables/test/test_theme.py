import pytest
import os
from contextlib import redirect_stdout
from pkg_resources import resource_filename
from itertools import chain, combinations

from gptables import Theme
from gptables import gptheme



valid_description_elements = ["legend", "instructions", "scope", "source"]


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

@pytest.fixture()
def empty_theme():
    yield Theme()


class TestCleanInitTheme:
    """
    Test initialisation of the Theme class without config.
    """ 
    @pytest.mark.parametrize("attr", Theme()._format_attributes)
    def test_default_format_attrs(self, attr, empty_theme):  
        """Test Theme attribute default types"""
        exp = {}
        got = getattr(empty_theme, attr)
        assert exp == got
    

    def test_default_other_attrs(self, empty_theme):
        assert empty_theme.description_order == []


    def test_print_attributes(self, empty_theme):
        """Test Theme print_attributes()"""
        from io import StringIO

        file_handler = StringIO()
        with redirect_stdout(file_handler):
            empty_theme.print_attributes()
        
        got = file_handler.getvalue()

        exp = (
"""cover_title_format : {}
cover_subtitle_format : {}
cover_text_format : {}
title_format : {}
subtitle_format : {}
instructions_format : {}
scope_format : {}
column_heading_format : {}
index_1_format : {}
index_2_format : {}
index_3_format : {}
data_format : {}
source_format : {}
legend_format : {}
description_order : []
"""
                )

        assert got == exp

class TestConfigInitTheme:
    """
    Test initialisation of the Theme class using a config dictionary.
    """
    def test_dict_init(self):
        config = {
            "global":
                {
                    "font_size": 12,
                    "font_name": "Arial",
                    "font_color": "automatic"                                 
                },

            "cover_title":
                {
                    'font_size': 16,
                    'bold': True,
                    'text_wrap': True,
                },
            
            "cover_subtitle":
                {
                    'font_size': 14,
                    'bold': True,
                    'text_wrap': True,
                },

            "cover_text":
                {
                    'text_wrap': True,
                },

            "title":
                {
                 "bold": True,
                "font_size": 16
                },
     
            "subtitle":
                {"font_size": 14},

            "instructions": None,

            "scope": None,

            "column_heading":
                {
                "bold": True,
                "bottom": 1,
                "text_wrap": 1,
                "valign": "top"
                },
            
            "index_1":
                {
                "bold": True,
                "text_wrap": 1
                },
            
            "index_2": {"text_wrap": 1},
            
            "index_3": {"text_wrap": 1},
            
            "data": {"text_wrap": 1},
            
            "source":
                {"font_size": 12},
            
            "legend":
                {"font_size": 12},
            
            "description_order":
                [
                    "instructions",
                    "legend",
                    "source",
                    "scope"
                ],
                }
        got = Theme(config)
        
        exp = gptheme
            
        assert exp == got
        
    def test_file_init(self):
        """
        Test initialisation of Theme using default theme yaml config file.
        """
        config_file = resource_filename(
            "gptables",
            "themes/gptheme.yaml"
            )
        got = Theme(config_file)
        
        exp = gptheme
                
        assert exp == got


class TestFormatValidationTheme:
    """
    Test validation of format dictionaries.
    """
    def test_invalid_attribute_config(self, empty_theme):
        """
        Test that invalid attribute names in config raises a ValueError.
        """
        config = {"potato": {"font_size": 9}}
        with pytest.raises(ValueError):
            empty_theme.apply_config(config)


    def test_invalid_format_label_config(self, empty_theme):
        """
        Test that invalid format labels in config raises a ValueError.
        """
        config = {"notes": {"not_a_format": 5}}
        with pytest.raises(ValueError):
            empty_theme.apply_config(config)
        

    @pytest.mark.parametrize("attr", Theme()._format_attributes)
    def test_invalid_format_label_single_attr(self, attr, empty_theme):
        """
        Test that `validate_single_format` decorator catches invalid format
        labels in individual format dictionaries.
        """
        format_dict = {"not_a_format": 5}
        with pytest.raises(ValueError):
            getattr(empty_theme, "update_" + attr)(format_dict)
    

    @pytest.mark.parametrize("attr", Theme()._format_attributes)
    def test_valid_format_label(self, attr, empty_theme):
        """
        Test that Theme attribute is correctly updated when valid format label
        is used.
        """
        getattr(empty_theme, "update_" + attr)({"font_size": 9})
        
        exp = {"font_size": 9}
        got = getattr(empty_theme, attr)
        
        assert exp == got

    
    def test_valid_format_label_config(self, empty_theme):
        """
        Test that valid format labels in config changes specified format attr
        but not an unrelated attr. Previous bug updated all formats whenever
        one was updated.
        """
        config = {"source": {"font_size": 5}}
        empty_theme.apply_config(config)
        
        exp = {"font_size": 5}
        got = empty_theme.source_format
        
        assert exp == got
        
        got2 = empty_theme.title_format
        
        assert {} == got2


class TestOtherValidationTheme:
    """
    Test validation of non-format Theme attributes.
    """
    @pytest.mark.parametrize(
        "format_order",[
            "notes",
            {"annotations": 2},
            1,
            3.14,
            False,
            None
            ]
        )
    def test_invalid_description_order_type(self, format_order, empty_theme):
        """
        Test that non-list description_order entries raise a TypeError.
        """
        with pytest.raises(TypeError):
            empty_theme.update_description_order(format_order)


    @pytest.mark.parametrize(
        "format_order",[
            ["potato"],
            [1],
            [3.14],
            [dict()],
            [[]]
            ]
        )             
    def test_invalid_description_order_values(self, format_order, empty_theme):
        """
        Test that list description_order entries containing invalid elements raises
        a ValueError.
        """
        with pytest.raises(ValueError):
            empty_theme.update_description_order(format_order)
    

    @pytest.mark.parametrize("description_order", powerset(valid_description_elements))
    def test_valid_description_order_values(self, description_order, empty_theme):
        """
        Test that valid list description_order entries are used to set
        the corresponding attribute.
        """
        empty_theme.update_description_order(list(description_order))
        assert getattr(empty_theme, "description_order") == list(description_order)
