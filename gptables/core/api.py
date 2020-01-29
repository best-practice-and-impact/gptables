from gptables.core.themes import create_theme
from gptables.core.themes import gptheme
from gptables.core.themes import import_theme

def produce_table(data, theme=gptheme, **kwargs):

    """Produces worksheet

    This is the main function that will take in data, theme information,
    and keyword arguments. It calls upon the packages to return a formatted
    ``.xlsx`` file.

   Parameters
   ----------
        data: A pandas dataframe object
        theme: A gptables theme object
        **kwargs: Other arguments such as ``headings``, ``index``, ``source``
            that map features of the data to table elements.

    Returns
    -------
        A worksheet object.
    """


