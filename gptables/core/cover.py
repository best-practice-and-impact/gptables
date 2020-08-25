from dataclasses import dataclass
from typing import List

@dataclass
class Cover():
    """
    dataclass for storing cover sheet text.

    Attributes
    ----------
    title : str
        cover page title
    intro : List[str, dict], optional
        introductory text
    about : List[str, dict], optional
        about/notes text
    contact : List[str, dict], optional
        contact details text
    cover_label : str 
        cover page tab label, defaults to Cover
    additional_elements : List[str], optional
        additional GPTable elements to display in the contents table. Allowed
        elements are "subtitles", "scope", "source" and "notes".
    """
    title: str
    intro: List = None
    about: List = None
    contact: List = None
    cover_label: str = "Cover"
    additional_elements: List = None

    def __post_init__(self):
        if self.additional_elements is not None:
            valid_elements = ["subtitles", "scope", "source", "notes"]
            if not all(element in valid_elements for element in self.additional_elements):
                msg = ("Cover `additional_elements` list can only contain"
                    "'subtitles', 'scope', 'source' and 'notes'")
                raise ValueError(msg)
