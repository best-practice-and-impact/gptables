Good Practice Tables (gptables)
===============================

.. image:: https://github.com/best-practice-and-impact/gptables/workflows/continuous-integration/badge.svg
    :target: https://github.com/best-practice-and-impact/gptables/actions
    :alt: Actions build status

.. image:: https://badge.fury.io/py/gptables.svg
    :target: https://badge.fury.io/py/gptables
    :alt: PyPI release


``gptables`` is an opinionated python package for spreadsheet production.
It produces ``.xlsx`` files from your ``pandas`` dataframes or using
``reticulate`` in R. You define the mapping from your data to elements of the
table. It does the rest.

``gptables`` uses the official `guidance on good practice spreadsheets`_.
It advocates a strong adherence to the guidance by restricting the range of operations possible.
The default theme ``gptheme`` should accommodate most use cases.
However, the ``Theme`` object allows development of custom themes, where other formatting is required.

``gptables`` is developed and maintained by the `Best Practice and Impact`_
division of the Office for National Statistics, UK.

.. _`guidance on good practice spreadsheets`: https://gss.civilservice.gov.uk/policy-store/releasing-statistics-in-spreadsheets/

.. _`Best Practice and Impact`: https://gss.civilservice.gov.uk/about-us/support-for-the-gss/


4 Simple Steps
--------------

1. You map your data to the elements of a ``GPTable``.

2. You can define the format of each element with a custom ``Theme``, or simply use the default - gptheme.

3. Optionally design a ``Cover`` page to provide information that relates to all of the tables in your Workbook.

4. You ``write_workbook`` to win.
