Theme
=====

``Theme`` Configuration
-----------------------

The easiest way to design your own theme is to create a
YAML configuration file. You should take a copy of our default theme
configuration file and adjust it to suit your needs.

Most of the top level names in the config file represent elements of the table.
The parameters passed below these names are `XlsxWriter format properties`_, so you
should check out their documentation to find the appropriate properties and valid
options for your formatting.

.. _`XlsxWriter format properties`: https://xlsxwriter.readthedocs.io/format.html#format-methods-and-format-properties

.. note:: All top levels names must exist in the config file. Where no properties need to be passed, leave empty after the colon.

The final two names in the config file are special attributes which do not take
XlsxWriter properties. They do the following:

* ``footer_order`` - specify the order of footer elements.
  Must contain a list including ``source``, ``legend``, ``annotations`` and ``notes``,
  in the order that you would like them to appear.
* ``missing_value`` - specify the string that will be use to represent missing values (``numpy.nan``).
  A legend is automatically generated for this string, when missing values are present.

The configuration file for our default theme looks like this:

.. literalinclude:: ..\..\gptables\themes\gptheme.yaml
    :language: yaml


For minor adjustments to a theme, a deepcopy can be taken before using the
``Theme`` methods below to update the ``Theme``'s attributes.

``Theme`` objects can altenatively be configured using dictionaries, with the same
structure as the configuration files.


``Theme`` Class
---------------

.. automodule:: gptables.core.theme
    :members:
