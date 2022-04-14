from dataclasses import dataclass, field
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
    order: list, optional
        order in which to display notes table contents
        if provided, notes table will be sorted by `order`
    """
    table: pd.DataFrame()
    table_name: str = ""
    title: str = ""
    subtitles: list = field(default_factory=list)
    instructions: str = ""
    label: str = ""
    order: list = field(default_factory=list)

    def __post_init__(
        self
        ):
        if len(self.table_name) == 0:
            self.table_name = "notes_table"
        if len(self.title) == 0:
            self.title = "Notes"
        if len(self.instructions) == 0:
            self.instructions = "This worksheet contains one table."
        if len(self.label) == 0:
            self.label = "Notes"

        GPTable.__init__(
            self,
            table=self.table, 
            table_name=self.table_name, 
            title=self.title, 
            subtitles=self.subtitles, 
            instructions=self.instructions
        )

    def order_notes_table(self):
        pass # TODO: order table by referencing order
