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

* contents page added to workbook by default. Can be disabled or customised by supplying ``contentsheet_label`` and ``contentsheet_options`` parameters to ``produce_workbook`` or ``write_workbook``.
* notes page added to workbook if ``notes_table`` is provided. Can be customised by supplying ``notesheet_label`` and ``notesheet_options`` parameters to ``produce_workbook`` or ``write_workbook``.
* ``table_name`` property added to ``GPTable`` class. This must be provided for accessibility.
* ``instructions`` property added to ``GPTable`` class. If this is not provided, a default value will be used.
* validation for ``GPTable.table`` column names - all columns must be named and the names must be unique
* ``instructions_format`` added to ``Theme``
* links formatted using the markdown format of ``"[display text](link)"`` will be rendered with the display text showing and the link applying for the corresponding cell. Links must start with ``http://``, ``https://``, ``ftp://``, ``mailto::``, ``internal:`` or ``external:``
* ``GPTable.table`` will be marked up as a worksheet table in Excel
* example added to demonstrate the use of a custom theme YAML

**Changed**

* ``auto_width`` property of ``produce_workbook`` and ``write_workbook`` now defaults to ``True`` rather than ``False``
* ``scope`` property of ``GPTable`` is now optional, as this information may be included in title or subtitles
* ``source`` property of ``GPTable`` is now optional, as this information should be included in cover sheet if it is the same across sheets
* ``units`` property of ``GPTable`` is now optional, and should be provided as ``dict`` (``str`` no longer supported)
* ``legend`` property as ``GPTable`` is now optional
* ``footer_order`` property of ``Theme`` replaced by ``description_order``, as corresponding metadata have been moved from below to above table. Valid elements are now ``instructions``, ``source``, ``legend`` and ``scope``.
* notes are now numbered according to position in workbook, starting from cell A1 of the first data sheet. Previously, notes were ordered independently for each worksheet
* ``units`` are now written on a new line with the the corresponding column heading cell, instead of above the table
* examples updated to reflect new functionality
* default theme changed to be more accessible, inparticular, font sizes increased to at least 12pt and font colour set to automatic. Note: compatibility issues with LibreOffice and automatic font colour

**Removed**

* ``notes`` and ``annotations`` properties removed from ``GPTable`` class. Notes are no longer displayed on data worksheets
* ``include_index_column_headings`` property removed from ``GPTable`` class, index column headers now always written, for accessibility
* ``quick_and_dirty`` function removed, as it is inaccessible and does not demonstrate good practice
* ``disable_footer_parentheses`` removed, as footer is inaccessible and parenetheses not good practice
* ``additional_elements`` property removed from ``Cover`` class. This is because table of contents is now generated on contentsheet not cover.
* ``annotations_format`` and ``notes_format`` options removed from ``Theme``, as ``annotations`` and ``notes`` no longer written to data worksheets
* ``missing_value`` option removed from ``Theme``. Unavailable or white-space table entries are now written as blank cells, and the user is invited to consider the GSS guidance on symbols and shorthand in spreadsheets

**Fixed**

* incorrect version numbers in changelog
* minor typos in docs



Released (PyPI)
===============

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
