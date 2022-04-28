from dataclasses import dataclass
from typing import List
from operator import xor
import pandas as pd

from gptables.core.gptable import GPTable

@dataclass
class Notesheet(GPTable):
    """
    Dataclass for storing notes sheet text.

    Attributes
    ----------
    table: pd.DataFrame
        notes table with reference, text and (optional) link columns
    link_text_column_name: str, optional
        name of (optional) column containing link text to display
    link_url_column_name: str, optional
        name of (optional) column contain link urls
        column entries should start with either
        `http://`, `https://`, `ftp://` or `mailto::`
    table_name: str, optional
        notes table name, defaults to "notes_table"
    title : str, optional
        notes page title, defaults to "Notes"
    subtitles: List[str], optional
        list of subtitles as strings
    instructions: str, optional
        description of the page layout
        defaults to "This worksheet contains one table."
    label: str, optional
        name of worksheet
        defaults to "Notes"
    """
    table: pd.DataFrame()
    link_text_column_name: str = None
    link_url_column_name: str = None
    table_name: str = None
    title: str = None
    subtitles: List = None
    instructions: str = None
    label: str = None

    def __post_init__(
        self
        ):
        # TODO: provide display text and url column names as list/tuple?
        if xor(
            (self.link_text_column_name is None),
            (self.link_url_column_name is None)
        ):
            msg = ("""
                Display text and url must both be provided to write hyperlinks.
                Guidance on formatting hyperlinks can be found at:
                https://gss.civilservice.gov.uk/policy-store/releasing-statistics-in-spreadsheets/#section-10
            """)
            raise ValueError(msg)

        if self.table_name is None:
            self.table_name = "notes_table"

        if self.title is None:
            self.title = "Notes"

        if self.instructions is None:
            self.instructions = "This worksheet contains one table."

        if self.label is None:
            self.label = "Notes"

        GPTable.__init__(
            self,
            table=self.table, 
            table_name=self.table_name, 
            title=self.title, 
            subtitles=self.subtitles, 
            instructions=self.instructions
        )
