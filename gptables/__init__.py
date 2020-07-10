from gptables.core.theme import Theme
from gptables.core.gptable import GPTable
from gptables.core.wrappers import GPWorkbook

from gptables.utils.unpickle_themes import gptheme


from gptables.core.api import (
        #functions
        produce_workbook,
	    write_workbook,
        quick_and_dirty_workbook
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
operations possible. The default theme ``gptheme`` should accomodate most use
cases. However, the ``Theme`` object allows development of custom themes, where
other formatting is required.

``gptables`` is developed and maintained by the `Best Practice and Impact`_
division of the Office for National Statistics, UK.

.. _`guidance on good practice spreadsheets`: https://gss.civilservice.gov.uk/policy-store/releasing-statistics-in-spreadsheets/

.. _`Best Practice and Impact`: https://gss.civilservice.gov.uk/about-us/support-for-the-gss/



3 Simple Steps
-------------

1. You define your mapping with your data as a ``GPTable``.

2. You can define the format of your mapping with a ``Theme``, or simply use the default - gptheme.

3. You ``write_workbook()`` to win.
"""
