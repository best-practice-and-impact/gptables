Good Practice Tables (gptables)
===============================

.. image:: https://github.com/best-practice-and-impact/gptables/workflows/continuous-integration/badge.svg
    :target: https://github.com/best-practice-and-impact/gptables/actions
    :alt: Actions build status
    
.. image:: https://readthedocs.org/projects/gptables/badge/?version=latest
    :target: https://gptables.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

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

``gptables`` is developed and maintained by the `Analysis Function`_. It can be
installed from `PyPI`_ or `GitHub`_. The source code is maintained on GitHub.
Users may also be interested in `a11ytables`_, an R native equivalent to
``gptables``, and `csvcubed`_, a package for turning data and metadata into
machine-readable CSV-W files.

.. _`guidance on good practice spreadsheets`: https://analysisfunction.civilservice.gov.uk/policy-store/releasing-statistics-in-spreadsheets/
.. _`Analysis Function`: https://analysisfunction.civilservice.gov.uk/
.. _`PyPI`: https://pypi.org/project/gptables/
.. _`GitHub`: https://github.com/best-practice-and-impact/gptables
.. _`a11ytables`: https://co-analysis.github.io/a11ytables/index.html
.. _`csvcubed`: https://gss-cogs.github.io/csvcubed-docs/external/


5 Simple Steps
--------------

1. You map your data to the elements of a ``GPTable``.

2. You can define the format of each element with a custom ``Theme``, or simply use the default - gptheme.

3. Optionally design a ``Cover`` page to provide information that relates to all of the tables in your Workbook.

4. Optionally upload a ``notes_table`` with information about any notes.

5. You ``write_workbook`` to win.


**Note**: This package is not intending to create perfectly accessible spreadsheets but will help with the bulk of the work needed. Users of this packages should refer back to the `main spreadsheet guidance <https://analysisfunction.civilservice.gov.uk/policy-store/releasing-statistics-in-spreadsheets/>`_ or the `spreadsheet accessibility checklist <https://analysisfunction.civilservice.gov.uk/policy-store/making-spreadsheets-accessible-a-brief-checklist-of-the-basics/>`_ after using it to make sure nothing has been missed. Please email `Analysis.Function@ons.gov.uk <mailto:Analysis.Function@ons.gov.uk>`_ if you use the package so we can monitor use and the outputs produced.
