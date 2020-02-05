from gptables.core.theme import Theme

def produce_workbook(cover_sheet, gptables, theme):

    """Produces a GPWorkbook

    This is the main function that will take in data and theme information,
    It calls upon the packages to return a formatted ``.xlsx`` file, ready to
    be written using `workbook.close()`.

   Parameters
   ----------
       path: str
           Path to write final workbook to (an .xlsx file)
       cover_sheet: dict
            cover sheet data
        gptables: dict
            A dictionary mapping worksheet labels to gptables.GPTable objects
        theme: gptables.Theme
            The formatting to be applied tot GPTable elements

    Returns
    -------
        A GPWorkbook object.
    """


def write_workbook(path, cover_sheet, gptables, theme):

    """Produces a GPWorkbook

    This is an alternative main function that will take in data and theme
    information. It calls upon the packages to write a formatted ``.xlsx``
    file to the specified path.

   Parameters
   ----------
       path: str
           Path to write final workbook to (an .xlsx file)
       cover_sheet: dict
            cover sheet data
        gptables: dict
            A dictionary mapping worksheet labels to gptables.GPTable objects
        theme: gptables.Theme
            The formatting to be applied tot GPTable elements

    Returns
    -------
        None
    """