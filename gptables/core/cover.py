from dataclasses import dataclass
from typing import List

@dataclass
class Cover():
    """
    dataclass for storing cover sheet text.

    Attributes
    ----------
    title str: cover page title
    intro List[str], optional: introductory text
    about List[str], optional: about/notes text
    contact List[str], optional: contact details text
    cover_label (str): cover page tab label, defaults to Cover
    additional_elements List[str], optional: additional GPTable elements to
        display in the contents table. Allowed elements are "subtitles",
        "scope" and "source".
    """
    title: str
    intro: List = None
    about: List = None
    contact: List = None
    cover_label: str = "Cover"
    additional_elements: List = None
