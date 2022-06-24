from gptables.core.theme import Theme
from gptables.core.cover import Cover
from gptables.core.gptable import GPTable
from gptables.core.wrappers import GPWorkbook

from gptables.utils.unpickle_themes import gptheme


from gptables.core.api import (
        # API functions
        produce_workbook,
	    write_workbook,
        )

__doc__ = """
*******************************
Good Practice Tables (gptables)
*******************************

.. image:: https://travis-ci.org/best-practice-and-impact/gptables.svg?branch=master
    :target: https://travis-ci.org/best-practice-and-impact/gptables
    :alt: Travis build status

.. image:: https://badge.fury.io/py/gptables.svg
    :target: https://badge.fury.io/py/gptables
    :alt: PyPI release


``gptables`` is an opinionated python package for spreadsheet production.
It produces ``.xlsx`` files from your ``pandas`` dataframes or using
``reticulate`` in R. You define the mapping from your data to elements of the
table. It does the rest.

``gptables`` uses the official `guidance on good practice spreadsheets`_
It advocates a strong adherence to the guidance by restricting the range of
operations possible. The default theme ``gptheme`` should accommodate most use
cases. However, the ``Theme`` object allows development of custom themes, where
other formatting is required.

``gptables`` is developed and maintained by the `Analysis Function`_.

.. _`guidance on good practice spreadsheets`: https://analysisfunction.civilservice.gov.uk/policy-store/releasing-statistics-in-spreadsheets/

.. _`Analysis Function`: https://analysisfunction.civilservice.gov.uk/



5 Simple Steps
--------------

1. You map your data to the elements of a ``GPTable``.

2. You can define the format of each element with a custom ``Theme``, or simply use the default - gptheme.

3. Optionally design a ``Cover`` page to provide information that relates to all of the tables in your Workbook.

4. Optionally upload a ``notes_table`` with information about any notes.

5. You ``write_workbook`` to win.
"""
