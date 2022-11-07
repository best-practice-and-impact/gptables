from dataclasses import dataclass
from typing import List

from gptables.core.gptable import FormatList

@dataclass
class Cover():
    """
    dataclass for storing cover sheet text.

    Attributes
    ----------
    title : str
        cover page title
    intro : List[str, list], optional
        introductory text
    about : List[str, list], optional
        about/notes text
    contact : List[str, list], optional
        contact details text
    cover_label : str 
        cover page tab label, defaults to Cover
    """
    
    def __init__(self, title: str, intro: List = None, about: List = None, contact: List = None, cover_label: str = "Cover"):
    
        self.title = title
        self.intro = self.parse_formatting(intro)
        self.about = self.parse_formatting(about)
        self.contact = self.parse_formatting(contact)
        self.cover_label = cover_label
    
    
    def parse_formatting(self, attribute):
        """Check attribute for a list. If there is a list then cast the list to a FormatList in attribute.

        Parameters
        ----------
        attribute : List[str, list]
        
        Returns
        -------
        List[str, FormatList]
        """

        if attribute is not None:
            attribute = [FormatList(text) if isinstance(text, list) else text for text in attribute]
        return attribute
