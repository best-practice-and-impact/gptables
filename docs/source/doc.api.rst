API functions
=============

.. note:: ``auto_width`` functionality is experimental - any feedback is welcome!
    It currently does not account for alternative fonts, font sizes or font wrapping.


Table of contents
-----------------

By default, the API functions will add a table of contents sheet to your
Excel workbook. This will contain a single table with two columns. The first
column will contain the worksheet label and link for each worksheet in the
workbook. The second column will contain a description of the sheet contents.
By default, this is the title of the ``GPTable`` in that sheet. This
description can be customised by passing additional elements from the
``GPTable`` into the ``contentsheet_options`` parameter. This parameter also
allows for customisation of the table of contents ``title``, ``subtitles``,
``table_name``, ``instructions`` and ``column_names``.

To customise the worksheet label, pass the new label into the
``contentsheet_label`` parameter. This table of contents functionality can be
disabled by setting this parameter to ``False``.

See this in practice under :ref:`Example Usage`.


Notes sheet
-----------
A notes sheet will be generated if the API functions are provided with a
``notes_table``. The first column of the ``notes_table`` should contain a
meaningful reference for each note. This reference can then be used in the
worksheets - see the GPTable documentation for more details. When the notes
sheet is produced, this column will be replaced by the order the notes are
referenced in throughout the workbook.

The second column should contain the text for each note. Optional additional
columns can be used for useful links, formatted as ``"[display text](link)"``.

The notes sheet can be customised using the ``notesheet_options`` parameter.
Values for the ``title``, ``table_name`` and ``instructions`` can be provided
here. To customise the worksheet label, pass the new label into the
``notesheet_label`` parameter.

If a ``notes_table`` is not provided, the notes sheet will not be generated.

See this in practice under :ref:`Example Usage`.


``write_workbook`` function
---------------------------

.. autofunction:: gptables.core.api.write_workbook


``produce_workbook`` function
-----------------------------

.. autofunction:: gptables.core.api.produce_workbook
