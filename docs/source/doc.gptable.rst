GPTable
=======

Mapping
-------

The ``GPTable`` Class is used to map your data and metadata to table elements.
The supported table elements are represented like this in the output `.xlsx` file:

.. figure:: static/table_mapping.png
   :figclass: align-center
   :alt: Cells A1 to A6 contain the title, subtitles, instructions, legend,
   source and scope. These parameters are mapped individually. The next row
   contains the column headings. Within the same row but on a new line are the
   units. The table note references are within the same row on a new line under
   the units. In columns 1, 2 and 3 of the next row down are index levels 1, 2
   and 3. In the next columns are the data. Column headings, indices and data
   are supplied as a pandas DataFrame. Units and table note references are
   mapped individually.


Notes
---------------------

Notes are text elements that appear on the separately generated ``Notesheet``.

Notes can be referenced in the ``title``, ``subtitles``, ``scope``, ``source``
and ``legend`` elements. Notes corresponding to entries in the data can be
referenced using the ``table_notes`` element. This will add a note reference to
the relevant column heading. Note references cannot be added to data cells, as
inserting references here would reduce the usability of the data. We use double
dollar symbols (``$$``) to denote notes in text. For example, a note could be
referenced as ``"My table title $$Reference$$"``.

References in text are replaced with numbers, in increasing order from the top-
left corner of the first sheet containing a data table.

See this in practice under :ref:`Example Usage`.


Links
-----

Links can added to text using the format ``[display text](link)``. Links are
supported in the ``title``, ``subtitles``, ``scope``, ``source``and ``legend``
elements. They will also be applied to cells within the data table that use
this format. Links should start with one of the following prefixes:
``http://``, ``https://``, ``ftp://``, ``mailto::``, ``internal:`` or
``external:``. For more information about the usage of the local URIs, see the
`XlsxWriter documentation`_.

.. _`XlsxWriter documentation`: https://xlsxwriter.readthedocs.io/worksheet.html#worksheet-write-url

.. note:: Excel does not support links being applied to specific words within
      cells. The link will be applied to the whole cell, not just the
      display text.

Rich Text
---------

Rich text is text that contains mixed formatting. You shouldn't use formatting
to represent data or important information, as most formatting is neither
accessible nor machine readable. You can still use to make things look
appealing for sighted people.

Rich text is supported in the ``title``, ``subtitles``, ``scope``, ``source``
and ``legend`` elements. Where you would normally provide a string to a
parameter, you can instead provide a list of strings and dictionaries.
Dictionaries in this list should contain valid `XlsxWriter format properties`_
and values. The formatting defined in these dictionaries will be applied to the
next string in the list. This formatting is applied in addition to the
formatting of that element specified in the :class:`~.core.theme.Theme`.

.. _`XlsxWriter format properties`: https://xlsxwriter.readthedocs.io/format.html#format-methods-and-format-properties

``["It is ", {"bold": True}, "inevitable"]`` would give you "It is *inevitable*".

See this in practice under :ref:`Example Usage`.

.. note:: Rich text is not currently supported if the cell also contains note
      references or links. This may be changed in the future if there is
      sufficient user need, so please raise an issue if this is functionality
      you need.


Additional formatting
---------------------

In some cases you may want to apply one-off formatting on specific rows, columns or cells of the data.
As mentioned above, this formatting should not be used to represent data or important information.

Bespoke formatting can be applied to an individual ``GPTable`` via the ``additional_formatting`` parameter,
when creating a ``GPTable`` instance. This parameter takes a list of dictionaries, where each dictionary
defines formatting for one or more rows, columns or cells.

These dictionaries have a single key indicating the type of selection, from "column", "row" or "cell".
Their value is another dictionary, which specifies the indexing, formatting and whether row and column
indexes are included in the selection.

Indexing supports selection of columns by name or 0-indexed number, but rows and cells can only
be indexed by number. Numeric indexing refers to position within the data element of the table (column
headings, row indexes and data), not position in the output Excel sheet.


This ``additional_formatting`` parameter is best demonstrated by example:

.. code:: python

   additional_formatting = [
         # Align data center, but not column indexes
         {"column":
               {"columns": ["some_column", "another_column"],  # str, int or list of either
               "format": {"align": "center"},
               "include_names": False  # Whether to include column headings (optional)
               }
         },

         # Align column left, including column index
         {"column":
               {"columns": [3],
               "format": {"left": 1},
               "include_names": True
               }
         },

         # Underline the bottom of the table, including row index
         {"row":
               {"rows": -1,  # Numbers only, but can refer to last row using -1
               "format": {"bottom": 1},  # Underline row
               "include_names": True  # Whether to include row indexes
               }
         },

         # A bad example, turning a single cell's font red
         {"cell":
               {"cells": (3, 3),  # tuple or list of tuples (numbers only)
               "format": {"font_color": "red"}
               }
         }
   ]

For any formatting beyond this, if the package should support it then please raise an issue
or create a pull request. Otherwise, you will need to modify the underlying
:class:`~.core.wrappers.GPWorkbook` or :class:`~.core.wrappers.GPWorksheet` objects
before they are written to Excel.

See this in practice under :ref:`Example Usage`.


``GPTable`` Class
-----------------

.. automodule:: gptables.core.gptable
    :members: GPTable
