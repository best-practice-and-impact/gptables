import pytest

from gptables.core.cover import Cover
from gptables.core.gptable import FormatList

class TestCover:
    
    @pytest.mark.parametrize("input_data", [
        None,
        ["text"],
        [[{"bold":True}, "richtext"]],
        [[{"bold":True}, "richtext", " "]],
        [[{"bold":True}, "richtext", " "], "text"],
        "text",
        42,
        [15]
    ])
    
    def test_parse_formatting(self, input_data):
        
        got = Cover._parse_formatting(input_data)
        
        if isinstance(input_data, list):
            assert all([got_element.list == input_element for input_element, got_element in zip(input_data, got) if isinstance(input_element, list)])
            
        else:
            assert got == input_data
