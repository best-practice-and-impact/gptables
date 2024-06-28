import pytest
import pandas as pd
import gptables as gpt
from pathlib import Path

from gptables.test.test_utils.excel_comparison_test import ExcelComparisonTest


@pytest.fixture(scope="function")
def create_gpworkbook():

    def generate_gpworkbook(output_path):
        """
        Create GPWorkbook to be used with API tests.
        """
        table = pd.DataFrame({"columnA": ["x", "y"], "columnB": [0, 1]})

        gptable = gpt.GPTable(
            table=table,
            table_name="table_name",
            title="Title$$ref1$$",
            subtitles=["Subtitle1", "Subtitle2"],
            instructions=["Some ", {"bold": True}, "instructions"],
            legend=["s = symbol", "t = shorthand"],
            scope="Tests",
            source="My imagination",
            units={0: "Latin alphabet", "columnB": "real numbers"},
            table_notes={1: "$$ref2$$"},
            index_columns={2:0},
            additional_formatting=[{
                "column":{
                    "columns": ["columnA"],
                    "format": {"bold": True}
                }
            }]
        )

        notes_table = pd.DataFrame({
            "Note reference": ["ref1", "ref2"],
            "Note text": ["Some text", "Some more text"],
            "Link": ["[gov.uk](https://www.gov.uk)", "[Wikipedia](https://en.wikipedia.org)"]
        })

        cover = gpt.Cover(
            title="Cover title",
            intro=["Introduction"],
            about=["About"],
            contact=["Me", "[please.dont@contact.me](mailto:please.dont@contact.me)"],
            cover_label="Cover"
        )

        gpt.write_workbook( # Use defaults for theme and autowidth
            filename=output_path/"actual_workbook.xlsx",
            sheets={"Label": gptable},
            cover=cover,
            contentsheet_label="Table of contents",
            contentsheet_options={"additional_elements": ["subtitles"]},
            notes_table=notes_table,
            notesheet_label="Notes table",
            notesheet_options={"title": "Table with notes"},
            gridlines="show_all",
            cover_gridlines=False
        )

    return generate_gpworkbook


def test_end_to_end(create_gpworkbook):
    """
    Test that runs the API functions with example input to check for errors and
    expected output.
    """
    output_path = Path(__file__).parent

    create_gpworkbook(output_path)

    ect = ExcelComparisonTest()

    ect.exp_filename = output_path / "expected_workbook.xlsx"
    ect.got_filename = output_path / "actual_workbook.xlsx"
    ect.ignore_files = []
    ect.ignore_elements = {}

    ect.assertExcelEqual()
    ect.tearDown()
