XlsxWriter wrappers
===================

These Classes are only likely used following use
of the :func:`~.core.api.produce_workbook` API function,
which returns a :class:`~.core.wrappers.GPWorkbook` object.

You may use these objects to carry out modification of any aspects of the
workbook or individual worksheets that are outside of the scope of ``GPTables``.
To see this in practice, see the additional formatting example under `usage`.
Please also see the XlsxWriter documentation on their Workbook_ and Worksheet_ Classes,
which are super-classses of those below, for details on further modfication.

.. _Workbook: https://xlsxwriter.readthedocs.io/workbook.html
.. _Worksheet: https://xlsxwriter.readthedocs.io/worksheet.html


The methods which we've extended these Classes with are not shown here, but feel
free to check out the source code to see how ``gptables`` works under the hood.


``GPWorkbook`` Class
--------------------

.. autoclass:: gptables.core.wrappers.GPWorkbook


``GPWorksheet`` Class
---------------------

.. autoclass:: gptables.core.wrappers.GPWorksheet