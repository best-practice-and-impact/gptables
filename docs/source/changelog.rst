*********
Changelog
*********

All notable changes to the master branch of this project should be documented
clearly in this file. In progress (or intended changes) can also be listed
below under Unreleased.

The changelog format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project tries its very best to adhere to
`Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

------------------------------------------------------------------------

Unreleased
===================

**Added**

* New tests for ``GPTable`` attributes.
* New end-to-end test.
* New test for marking table as Excel worksheet table.

**Changed**

* Running package tests now requires pytest>=6.2.5, to support Python 3.10
* CI now runs tests on both Linux and Windows with Python 3.6-3.10
* Validation of GPTable text attributes. Error will be raised if ``title`` or
  ``instructions`` is ``None``, or if an entry in the ``subtitle`` or
  ``legend`` lists is ``None``.
* Restructure and rewording of changelog

**Deprecated**

* ``contentsheet`` parameter of ``write_workbook`` will be removed in v2 of
  gptables. Please use ``contentsheet_label`` instead.

**Fixed**

* ``auto_width`` now functions as expected for columns with links or rich text
  columns using Python 3.6 and 3.7, as well as for numeric columns using
  Python>=3.6
* ``contentsheet_label`` parameter added to ``write_workbook``. Previously
  parameter was included in documentation but not in function.
* Rich text in ``instructions`` property will no longer raise an error.
* Image alt text in user documentation
* Deployment of docs in CI


Released (PyPI)
===============

v1.0.0
------
:Date: 2022-06-04

**Added**

Cover:

* links formatted using the markdown format of ``"[display text](link)"`` will be rendered with the display text showing and the link applying for the corresponding cell. Links must start with ``http://``, ``https://``, ``ftp://``, ``mailto:``, ``internal:`` or ``external:``

Table of contents:

* contents page added to workbook by default. Can be disabled or customised by supplying ``contentsheet_label`` and ``contentsheet_options`` parameters to ``produce_workbook`` or ``write_workbook``.
* links can be used in text elements passed to ``contentsheet_options``, see above

Notes:

* notes page added to workbook if ``notes_table`` is provided. Can be customised by supplying ``notesheet_label`` and ``notesheet_options`` parameters to ``produce_workbook`` or ``write_workbook``.
* links can be used in ``notes_table`` and text elements passed to ``notesheet_options``, see above

Data tables:

* ``GPTable.table`` will be marked up as a worksheet table in Excel
* ``table_name`` property added to ``GPTable`` class. This must be provided for accessibility.
* ``instructions`` property added to ``GPTable`` class. If this is not provided, a default value will be used.
* ``table_notes`` property added to ``GPTable`` class. This allows note references to be added to the column header row. If used, they will be positioned below the column name and units.
* validation for ``GPTable.table`` column names - all columns must be named and the names must be unique
* links can be used in ``GPTable.table`` and text elements

Theme:

* ``instructions_format`` added to ``Theme``. This can be used to customise the format of the ``GPTable.instructions`` element.

Examples:

* example added to demonstrate the use of a custom theme YAML


**Changed**

API functions:

* ``auto_width`` property of ``produce_workbook`` and ``write_workbook`` now defaults to ``True`` rather than ``False``

Notes:

* notes are now numbered according to position in workbook, starting from cell A1 of the first data sheet. Previously, notes were ordered independently for each worksheet
* note references in text elements are moved to the end of the text. This is to make them more accessible and avoid disrupting the text.

Data tables:

* ``units`` are now written on a new line with the the corresponding column heading cell, instead of above the table
* ``units`` property of ``GPTable`` is now optional, and should be provided as ``dict`` (``str`` no longer supported)
* ``scope`` property of ``GPTable`` is now optional, as this information may be included in title or subtitles
* ``source`` property of ``GPTable`` is now optional, as this information should be included in cover sheet if it is the same across sheets
* ``legend`` property as ``GPTable`` is now optional

Theme:

* default theme changed to be more accessible, inparticular, font sizes increased to at least 12pt and font colour set to automatic. Note: compatibility issues with LibreOffice and automatic font colour
* ``footer_order`` property of ``Theme`` replaced by ``description_order``, as corresponding metadata have been moved from below to above table. Valid elements are now ``instructions``, ``source``, ``legend`` and ``scope``.

Examples:

* examples updated to reflect new functionality

**Removed**

API functions:

* ``quick_and_dirty`` function removed, as it is inaccessible and does not demonstrate good practice
* ``disable_footer_parentheses`` removed, as footer is inaccessible and parenetheses not good practice

Cover:

* ``additional_elements`` property removed from ``Cover`` class. This is because table of contents is now generated on contentsheet not cover.

Notes:

* ``notes`` and ``annotations`` properties removed from ``GPTable`` class. Notes are no longer displayed on data worksheets

Data tables:

* ``include_index_column_headings`` property removed from ``GPTable`` class, index column headers now always written, for accessibility

Theme:

* ``annotations_format`` and ``notes_format`` options removed from ``Theme``, as ``annotations`` and ``notes`` no longer written to data worksheets
* ``missing_value`` option removed from ``Theme``. Unavailable or white-space table entries are now written as blank cells, and the user is invited to consider the GSS guidance on symbols and shorthand in spreadsheets

**Fixed**

* incorrect version numbers in changelog
* minor typos in docs


v0.4.0
------
:Date: 2021-01-30

**Fixed**

* bug where setting a GPTable's scope to ``None`` resulted in the units also not being displayed
* depreciation warning when running tests

**Added**

* ``include_index_column_headings`` option to ``GPTable``, so that users can display index column headers if they wish. Defaults to ``False`` for backwards compatibility.


v0.3.2
------
:Date: 2020-08-24


**Fixed**

* bug in Cover post_init where ``additional_elements`` is None (it's default value...)
* more minor typos in docs
* incorrect version numbers in changelog


v0.3.1
------
:Date: 2020-08-24


**Fixed**

* incorrect ``if __name__ == "__main__"`` in example files 
* minor typos in docs


v0.3.0
------
:Date: 2020-08-24

**Added**

* ``Cover`` dataclass, to provide text elements for cover pages. Provided via ``cover`` parameter of API functions.
* ``write_cover`` and associated ``GPWorksheet`` methods, for writing a cover page as the first sheet in a GPWorkbook
* additional ``Theme`` attributes for ``Cover`` text elements
* documentation for ``Cover`` class and example usage

**Fixed**

* loads of typos in documentation
* broken CI deployment of docs - code includes were not working


v0.2.0
------
:Date: 2020-07-10

**Fixed**

* stacking of parentheses around footer elements when a ``GPTable`` was used more than once
* duplication of ``missing_value`` in legend when multiple missing values were present
* rst syntax in docs and readme (some bits of Markdown were hanging around)

**Added**

* "quick and dirty" API function, for when you just want tables and you want them now
* functionality to automatically determine column widths - available via ``auto_width`` parameter in API functions
* ability to disable addition of parenetheses to footer element text

**Changed**

* removed ``num_format`` property from ``data`` element of default theme
* Updated documentation of examples
* Completely updated online documentation, so that the package might actually be usable


v0.1.3
------
:Date: 2020-03-06

**Fixed**

* missing files in binary distribution. v0.1.1 and v0.1.2 will be deleted from
  PyPI to prevent use of broken distributions.
  
**Added**

* this changelog to the documentation!


**Changed**

* README to reflect description of package. Dropped developer install
  instructions.


v0.1.1
------
:Date: 2020-03-05

**Added**

* gptables package - see README and documentation for usage
* build and deployment of `documentation <https://best-practice-and-impact.github.io/gptables/>`_
* deployment to `PyPI <https://pypi.org/project/gptables/>`_
