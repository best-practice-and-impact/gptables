GPTable
=======

Mapping
-------

The ``GPTable`` Class is used to map your data and metadata to table elements.
The supported table elements are represented like this in the output `.xlsx` file:

.. figure:: static/table_mapping.png
   :figclass: align-center

Where you do not want to include an element, but no default is defined for that parameter,
pass ``None`` to the relevant parameter when creating a ``GPTable`` instance.


Notes and Annotations
---------------------

Notes are text elements that appear below the table, which refer to large
sections or all of the table.

Annotations are notes which refer to specific aspects of the table or metadata.
For annotation text to appear, it must be referenced in another text element of
the ``GPTable``. Annotation references are supported in all table elements,
expect for the table data - inserting references here would reduce the usability of the data.

Annotations are defined as a dictionary of the ``{"Reference": "Annotation text"}``.
We use double dollar symbols (``$$``) to denote annotations in text. For example,
this annotation could be references as ``"My table title $$Reference$$"``.

References in text are replaced with numbers, in increasing order down the table output.

See this in practice under :ref:`Example Usage`.


Rich Text
---------

Rich text is text that contains mixed formatting. You shouldn't use formatting
to represent data or important information, as most formatting is not machine readable.
You can still use to make things look pretty for people using their eyes.

All ``GPTable`` text elements support rich text. Where you would normally provide a string
to a parameter, you can instead provide a list of strings and dictionaries. Dictionaries
in this list should contain valid `XlsxWriter format properties`_ and values. The formatting
defined in these dictionaries will be applied to the next string in the list. This formatting is
applied in addition to the formatting of that element specified in the :class:`~.core.theme.Theme`.

.. _`XlsxWriter format properties`: https://xlsxwriter.readthedocs.io/format.html#format-methods-and-format-properties

``["It is ", {"italic": True}, "inevitable"]`` would give you "It is `inevitable`".

See this in practice under :ref:`Example Usage`.


Additional formatting
---------------------

In some cases you may want to apply one-off formatting on specific rows, columns or cells of the data.
As mentioned above, this formatting should not be used to represent data or important information.

Bespoke formatting can be applied to an individual ``GPTable`` via the ``additional_formatting`` parameter,
when creating a ``GPTable`` instance. This parameter takes a list of dictionaries, where each dictionary
defines formatting for one or more rows, columns or cells.

These dictionaries have a single key indicating the type of selection, from from "column", "row" or "cell".
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
    :members:
