# Good Practice Tables (gptables)

<!-- badges: start -->
[![Travis build status](https://travis-ci.org/best-practice-and-impact/gptables.svg?branch=master)](https://travis-ci.org/best-practice-and-impact/gptables)
<!-- badges: end -->

A wrapper for `xlsxwriter`, to write publication quality tables in Excel.

## Statement of intent

`gptables` is a package developed for python and `reticulate` in R.
It will help the production of `.xlsx` tables by automating the boring bits.
We follow the Good Practice Team [guidance](https://gss.civilservice.gov.uk/policy-store/releasing-statistics-in-spreadsheets) so that you don't have to.
We cover up the workings of `xlsxwriter` so you don't have to do it cell-by-cell.

## Installation and use

For development, clone this repository and install the package from a local repo using:

```
git clone https://github.com/best-practice-and-impact/gptables.git ./gptables/
pip install -e gptables
```

To uninstall, use:

```
pip uninstall gptables
```
