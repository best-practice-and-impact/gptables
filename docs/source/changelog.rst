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

Unreleased (master)
===================

Nothing to see here.


Released (PyPI)
===============

v0.3.2
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
