from dataclasses import dataclass
from typing import Dict, List
import pandas as pd
import re

from gptables.core.gptable import GPTable

@dataclass
class Contentsheet(GPTable):
    """
    Dataclass for storing table of contents.

    Attributes
    ----------
    sheets : dict
        mapping worksheet labels to gptables.GPTable objects
    column_names : List[str], optional
        table of contents column names, defaults to 
        "Sheet name", "Table description"
    additional_elements : List[str], optional
        additional GPTable elements to display in the contents table. Allowed
        elements are "subtitles", "scope", "source" and "instructions".
    table: pd.DataFrame
        notes table with reference, text and (optional) link columns
    table_name: str, optional
        notes table name, defaults to "contents_table"
    title : str, optional
        notes page title, defaults to "Table of contents"
    subtitles: List[str], optional
        list of subtitles as strings
    instructions: str, optional
        description of the page layout
        defaults to "This worksheet contains one table."
    label: str, optional
        name of worksheet
        defaults to "Contents"
    """
    sheets: Dict
    column_names: List = None
    additional_elements: List = None
    table_name: str = None
    title: str = None
    subtitles: List = None
    instructions: str = None
    label: str = None

    def __post_init__(self):
        if self.column_names is None:
            self.column_names = ["Sheet name", "Table description"]
        if self.table_name is None:
            self.table_name = "contents_table"
        if self.title is None:
            self.title = "Table of content"
        if self.instructions is None:
            self.instructions = "This worksheet contains one table."
        if self.label is None:
            self.label = "Content"

        if self.additional_elements is not None:
            valid_elements = ["subtitles", "scope", "source", "instructions"]
            if not all(element in valid_elements for element in self.additional_elements):
                msg = ("Cover `additional_elements` list can only contain"
                    "'subtitles', 'scope', 'source' and 'instructions'")
                raise ValueError(msg)

        contents = {}
        for label, gptable in self.sheets.items(): 
            contents_entry = []                   
            contents_entry.append(self._strip_annotation_references(gptable.title))

            if self.additional_elements is not None:
                for element in self.additional_elements:
                    content = getattr(gptable, element)        
                    if element == "subtitles":
                        [contents_entry.append(self._strip_annotation_references(element)) for element in content]
                    else:
                        contents_entry.append(self._strip_annotation_references(content))
            contents[label] = [contents_entry]

        contents_table = pd.DataFrame.from_dict(contents, orient="index").reset_index()

        contents_table.iloc[:, 1] = contents_table.iloc[:, 1].str.join("\n")

        contents_table.columns = self.column_names

        GPTable.__init__(
            self,
            table=contents_table, 
            table_name=self.table_name, 
            title=self.title, 
            subtitles=self.subtitles, 
            instructions=self.instructions
        )

    @staticmethod
    def _strip_annotation_references(text):
        """
        Strip annotation references (as $$ $$) from a str or list text element.
        """
        pattern = r"\$\$.*?\$\$"
        if isinstance(text, str):
            no_annotations = re.sub(pattern, "", text)
        elif isinstance(text, list):
            no_annotations = [
                re.sub(pattern, "", part)
                if isinstance(part, str) else part
                for part in text
                ]
        
        return no_annotations
