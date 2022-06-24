# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import alabaster
sys.path.insert(0, os.path.abspath('../'))

# -- Project information -----------------------------------------------------

project = 'gptables'
copyright = ' Crown Copyright'
author = 'David Foster, Alexander Newton, Rowan Hemsi, Jacob Cole, Dan Shiloh and Jaehee Ryoo'

# The full version, including alpha/beta/rc tags
with open(os.path.abspath("../../VERSION")) as f:
    release = f.read()

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
        'sphinx.ext.autodoc',
        'sphinx.ext.viewcode',
        'sphinx.ext.todo',
        'sphinx.ext.githubpages',
        'sphinx.ext.napoleon'
        ]


todo_include_todos = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# The master toctree document.
master_doc = 'index'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'alabaster'

custom_fonts = '"Raleway", "HelveticaNeue", "Helvetica Neue", Helvetica, Arial, sans-serif'
html_theme_options = {
    "description": "An opinionated python package for spreadsheet production.",
    'fixed_sidebar': 'true',
    'caption_font_family': custom_fonts,
    'font_family': custom_fonts,
    'head_font_family': custom_fonts,
    "github_user": "best-practice-and-impact",
    "github_repo": "gptables",
    "github_button": True,
    "github_type": "watch",
    "github_count": False,
    "sidebar_includehidden": True,
    "show_relbar_bottom": True,
    "page_width": "60rem",
    "sidebar_width": "15rem",
    }

html_show_sourcelink = False


html_sidebars = {
        '**': [
            'about.html',
            'navigation.html',
            'relations.html',
            'searchbox.html'
            ]

        }



# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []
