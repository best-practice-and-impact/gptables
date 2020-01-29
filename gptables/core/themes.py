import xlsxwriter as xlw


gptheme = Theme(gptheme.conf)


class Theme:
    """A class that defines a set of formats in xlsxwriter.

    This class associates a set of format objects with table elements.

    Parameters
    ----------
    conf : dict or .yaml specifying your theme specification.
    
        

    Returns
    -------
        a
    """

    def __init__(
            self,
            conf):
        """Constructs theme object"""
