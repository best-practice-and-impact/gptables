from gptables.core.theme import Theme

def produce_table(gptable, theme, **kwargs):

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


