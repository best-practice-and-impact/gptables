.. gptables documentation master file, created by
   sphinx-quickstart on Tue Jan 28 18:15:40 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to gptables's documentation!
====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Mission statement
=================

``gptables`` is a highly opinionated python package.
It produces ``.xlsx`` files from your ``pandas`` dataframes or using ``reticulate`` in R.
You define the mapping from your data to elements of the table.
It does the rest.

``gptables`` uses the official guidance_ on good practice spreadsheets.
It advocates a strong adherence to the guidance by restricting the range of operations possible.
The default theme ``gptheme`` should accomodate most use cases.

``gptables`` is developed and maintained by the `Best Practice and Impact`_ division of the Office for National Statistics, UK.

.. _guidance: https://gss.civilservice.gov.uk/policy-store/releasing-statistics-in-spreadsheets/
.. _`Best Practice and Impact`: https://gss.civilservice.gov.uk/about-us/support-for-the-gss/
