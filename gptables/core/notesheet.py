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
    order: list, optional
        order in which to display notes table contents
        if provided, notes table will be sorted by `order`
    """
    table: pd.DataFrame()
    table_name: str = ""
    title: str = ""
    subtitles: List = []
    instructions: str = ""
    order: List = []
        
    def __post_init__(
        self, 
        table,
        table_name,
        title,
        subtitles,
        instructions,
        order
        ):
        if len(self.table_name) == 0:
            self.table_name = "notes_table"
        if len(self.title) == 0:
            self.title = "Notes"
        if len(self.instructions) == 0:
            self.instructions = "This worksheet contains one table."
        
        # TODO: order table by referencing order

        GPTable.__init__(self, table, table_name, title, subtitles, instructions, order)
