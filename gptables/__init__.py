from gptables.core.theme import Theme
from gptables.core.gptable import GPTable
from gptables.core.wrappers import GPWorkbook

from gptables.utils.unpickle_themes import gptheme


from gptables.core.api import (
        #datatypes



        #classes



        #functions
        produce_workbook,
	    write_workbook
        )

__doc__ = """
gptables - a highly opinionated package for spreadsheet production
==================================================================

``gptables`` is a highly opinionated python package.
It produces ``.xlsx`` files from your ``pandas`` dataframes or using
``reticulate`` in R. You define the mapping from your data to elements of the
table. It does the rest.

``gptables`` uses the official guidance_ on good practice spreadsheets.
It advocates a strong adherence to the guidance by restricting the range of operations possible.
The default theme ``gptheme`` should accomodate most use cases.

``gptables`` is developed and maintained by the `Best Practice and Impact`_ division of the Office for National Statistics, UK.

.. _guidance: https://gss.civilservice.gov.uk/policy-store/releasing-statistics-in-spreadsheets/
.. _`Best Practice and Impact`: https://gss.civilservice.gov.uk/about-us/support-for-the-gss/


Main Features
-------------
You define your mapping with your data as a ``GPTable``.

You define the format of your mapping with a ``Theme``, the default is gptheme.

You ``write_workbook()`` to win.
"""
