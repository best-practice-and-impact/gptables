.. _Example Usage:

Example Usage
=============

This section demonstrates usage of the gptables API functions and core Classes.

For source code and data used in these examples, please see the
examples_ directory of the package.

.. _examples: https://github.com/best-practice-and-impact/gptables/tree/dev/gptables/examples

.. todo:: Replace datasets in examples with open online datasets


.. automodule:: gptables.examples.iris

.. literalinclude:: ../../gptables/examples/iris.py
    :language: python
    :lines: 15-


.. automodule:: gptables.examples.iris_cover

.. literalinclude:: ../../gptables/examples/iris_cover.py
    :language: python
    :lines: 12-


.. automodule:: gptables.examples.iris_additional_formatting

.. literalinclude:: ../../gptables/examples/iris_additional_formatting.py
    :language: python
    :lines: 24-


.. automodule:: gptables.examples.cor_multiple_sheets

.. literalinclude:: ../../gptables/examples/cor_multiple_sheets.py
    :language: python
    :lines: 16-


.. automodule:: gptables.examples.iris_quick_and_dirty

.. literalinclude:: ../../gptables/examples/iris_quick_and_dirty.py
    :language: python
    :lines: 20-


R Usage
-------

Use of ``gptables`` in R requires use of python via the `reticulate <https://rstudio.github.io/reticulate/>`_ package.

This example demonstrates basic usage of the pacakge in R. More advanced usage will
use a similar approach to python (above), but may require use of ``reticulate`` functions
to create/modify python objects.

.. literalinclude:: ../../gptables/examples/iris.R
    :language: R
