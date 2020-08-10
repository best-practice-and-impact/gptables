from dataclasses import dataclass

@dataclass
class Cover():
    """
    Class for storing cover sheet text.

    Attributes
    ----------
        title (str): cover page title
        intro (str): optional introductory text
        about (str): optional about/notes text
    """
    title: str
    intro: str = None
    about: str = None