import pytest
import os
from contextlib import redirect_stdout
from pkg_resources import resource_filename
from itertools import chain, combinations

from gptables import Theme
from gptables import gptheme



valid_footer_elements = ["legend", "notes", "annotations", "source"]


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
        assert empty_theme.footer_order == []
        assert empty_theme.missing_value == None


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

        assert got == exp

class TestConfigInitTheme:
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

            "cover_title":
                {
                    'font_size': 12,
                    'bold': True
                },
            
            "cover_subtitle":
                {
                    'font_size': 10,
                    'bold': True
                },

            "cover_text": None,

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
        config = {"notes": {"font_size": 5}}
        empty_theme.apply_config(config)
        
        exp = {"font_size": 5}
        got = empty_theme.notes_format
        
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
    def test_invalid_footer_order_type(self, format_order, empty_theme):
        """
        Test that non-list footer_order entries raise a TypeError.
        """
        with pytest.raises(TypeError):
            empty_theme.update_footer_order(format_order)


    @pytest.mark.parametrize(
        "format_order",[
            ["potato"],
            [1],
            [3.14],
            [dict()],
            [[]]
            ]
        )             
    def test_invalid_footer_order_values(self, format_order, empty_theme):
        """
        Test that list footer_order entries containing invalid elements raises
        a ValueError.
        """
        with pytest.raises(ValueError):
            empty_theme.update_footer_order(format_order)
    

    @pytest.mark.parametrize("footer_order", powerset(valid_footer_elements))
    def test_valid_footer_order_values(self, footer_order, empty_theme):
        """
        Test that valid list footer_order entries are used to set
        the corresponding attribute.
        """
        empty_theme.update_footer_order(list(footer_order))
        assert getattr(empty_theme, "footer_order") == list(footer_order)
