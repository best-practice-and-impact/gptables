from dataclasses import dataclass
from typing import List
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
    table_name: str = None
    title: str = None
    subtitles: List = None
    instructions: str = None
    label: str = None

    def __post_init__(
        self
        ):
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
