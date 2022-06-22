Theme
=====

``Theme`` Configuration
-----------------------

The easiest way to design your own theme is to create a
YAML configuration file. You should take a copy of our default theme
configuration file and adjust it to suit your needs.
When designing a theme, please consult the `Analysis Function guidance`_ to
ensure your new formatting is accessible.

.. _`Analysis Function guidance`: https://analysisfunction.civilservice.gov.uk/policy-store/releasing-statistics-in-spreadsheets/

Most of the top level names in the config file represent table elements or their metadata.
The parameters passed below these names are `XlsxWriter format properties`_, so you
should check out their documentation to find the appropriate properties and valid
options for your formatting.

``global`` refers to the base format that all others will be built upon.
Any format parameter that is repeated for a specific element will override the global format for that element.
The three ``cover_`` format names refer to elements of the cover page generated from a :class:`~.core.cover.Cover`.

.. _`XlsxWriter format properties`: https://xlsxwriter.readthedocs.io/format.html#format-methods-and-format-properties

.. note:: All top levels names must exist in the config file. Where no properties need to be passed, leave empty after the colon.

The final name in the config file is a special attribute which doed not take
XlsxWriter properties. It does the following:

* ``description_order`` - specify the order of description elements.
  Must contain a list including ``instructions``, ``legend``, ``source`` and ``scope``,
  in the order that you would like them to appear.

The configuration file for our default theme looks like this:

.. literalinclude:: ../../gptables/themes/gptheme.yaml
    :language: yaml


For minor adjustments to a theme, a deepcopy can be taken before using the
``Theme`` methods below to update the ``Theme``'s attributes.

``Theme`` objects can altenatively be configured using dictionaries, with the same
structure as the configuration files.

An example using a personalised theme YAML file can be found under :ref:`Example Usage`.


``Theme`` Class
---------------

.. automodule:: gptables.core.theme
    :members:
