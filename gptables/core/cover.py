from dataclasses import dataclass
from typing import List

@dataclass
class Cover():
    """
    dataclass for storing cover sheet text.

    Attributes
    ----------
        cover_label (str): cover page tab label, defaults to Cover"
        title (str): cover page title
        intro (str): optional introductory text
        about (str): optional about/notes text
    """
    cover_label: str = "Cover"
    title: str
    intro: List = None
    about: List = None
