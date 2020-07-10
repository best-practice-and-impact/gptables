*******************************
Good Practice Tables (gptables)
*******************************

.. image:: https://travis-ci.org/best-practice-and-impact/gptables.svg?branch=master
    :target: https://travis-ci.org/best-practice-and-impact/gptables
    :alt: Travis build status

.. image:: https://badge.fury.io/py/gptables.svg
    :target: https://badge.fury.io/py/gptables
    :alt: PyPI release

``gptables`` produces `.xlsx` files from your ``pandas`` dataframes in
either python or R (using reticulate_). You define the mapping from your
data to elements of the table and ``gptables`` does the rest.

.. _reticulate: https://rstudio.github.io/reticulate/

Table element mapping:

.. figure:: static/table_mapping.png
   :figclass: align-center


``gptables`` uses the official `guidance on good practice spreadsheets`_
It advocates a strong adherence to the guidance by restricting the range of possible operations.
The default formatting theme ``gptheme`` accomodates many use cases.
However, the :class:`~.core.theme.Theme` Class allows development of custom themes, where alternative formatting is required.

``gptables`` is developed and maintained by the `Best Practice and Impact`_
division of the Office for National Statistics, UK.

.. _`guidance on good practice spreadsheets`: https://gss.civilservice.gov.uk/policy-store/releasing-statistics-in-spreadsheets/

.. _`Best Practice and Impact`: https://gss.civilservice.gov.uk/about-us/support-for-the-gss/


3 Simple Steps
--------------

1. You map your data to the elements of a :class:`~.core.gptable.GPTable`.

2. You can define the format of each elements with a custom :class:`~.core.theme.Theme`, or simply use the default - gptheme.

3. You :func:`~.core.api.write_workbook` to win.


.. toctree::
   :maxdepth: 2
   :hidden:
   
   doc.api.rst
   usage.rst
   doc.gptable.rst
   doc.theme.rst
   doc.wrappers.rst
   changelog.rst
   