Cover
=====

Cover sheets can be used to provide information that is general to all tables in a Workbook.

.. note::

   Cover sheets are added as the first sheet in the Worbook when written by ``gptables``.
   This is important when applying additional formatting to other Worksheets by their index in the Workbook.

Mapping
-------

To include a cover sheet, map your text elements to the attributes of a ``Cover`` object and pass this object to the ``cover`` parameter of either :func:`~.core.api.produce_workbook` or :func:`~.core.api.write_workbook`.
Text attributes which take a list (most except for title) will write one element per cell vertically in the Worksheet.

Formatting
----------

Formatting of cover sheet text is managed by the ``cover_`` attributes of the Workbook's :class:`~.core.theme.Theme`.

``Cover`` Class
---------------

.. automodule:: gptables.core.cover
    :members:
