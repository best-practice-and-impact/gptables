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
    """
    title: str
    intro: List = None
    about: List = None
    contact: List = None
    cover_label: str = "Cover"
