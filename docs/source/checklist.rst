***********************
Accessibility checklist
***********************

The tables below indicate your accessibility responsibilities when publishing
statistics in spreadsheets. It is based on the Analysis Function `checklist of
the basics`_ and heavily inspired by the `aftables documentation`_.

.. _`checklist of the basics`: https://analysisfunction.civilservice.gov.uk/policy-store/making-spreadsheets-accessible-a-brief-checklist-of-the-basics/
.. _`aftables documentation`: https://best-practice-and-impact.github.io/aftables/articles/checklist.html

.. note:: The tables show which checklist items are automatically met by
    gptables. This applies to workbooks created using the default ``gptheme``
    and may not apply if custom themes or additional formatting are used.

Table
-----

.. list-table::
    :header-rows: 1
    :widths: 24 17 19 40

    * - Description
      - Essential?
      - Status
      - Explanation
    * - Mark up tables
      - Essential
      - Implemented
      - Tables in a ``GPWorkbook``, including notes table and table of contents
        are marked as tables by default.
    * - Give tables meaningful names
      - Desirable
      - Partially implemented
      - Pass a meaningful name to the ``GPTable.table_name`` property.
    * - Remove merged cells, split cells and nested tables
      - Essential
      - Implemented
      - Merged cell, split cells and nested tables are not supported by gptables.
    * - Remove blank rows and columns within tables
      - Essential
      - Partially implemented
      - Blank rows or columns in a column will raise an error. User should
        remove them and any apply any desired additional formatting.
    * - All tables should have one tagged header row
      - Essential
      - Implemented
      - The column names in a ``GPTable.table`` will be tagged as the header.
    * - Wrap text within cells
      - Essential
      - Partially implemented
      - Using ``auto_width = True`` (default value) will enable all text to be
        visible. This feature is experimental and some customisation may be
        desired.
    * - Avoid adding filters and freeze panes
      - Desirable
      - Implemented
      - Filters and freeze panes are not supported by gptables.
    * - Only leave cells with no data empty in certain circumstances
      - Essential
      - Partially implemented
      - If cells are null or whitespace, users are prompted to explain why in the
        ``GPTables.instructions`` property. If there is more than one reason
        for missingness, use the `appropriate shorthand`_ and explain in the
        ``GPTables.legend`` property.
    * - Avoid hiding rows or columns
      - Desirable
      - Implemented
      - Hiding rows or columns is not supported by gptables.

.. _`appropriate shorthand`: https://analysisfunction.civilservice.gov.uk/policy-store/symbols-in-tables-definitions-and-help/


Footnotes
---------

.. list-table::
    :header-rows: 1
    :widths: 24 17 19 40

    * - Description
      - Essential?
      - Status
      - Explanation
    * - Do not use symbols or superscript to signpost to notes
      - Essential
      - Implemented
      - Notes marked with ``$$note_ref$$`` will be formatted as ``[note n]``,
        where ``n`` is the order the note appears in the workbook.
    * - Use the word 'note' when referring to footnotes
      - Desirable
      - Implemented
      - As mentioned above, notes are formatted as ``[note n]``.
    * - Avoid putting note markers in specific cells
      - Desirable
      - Partially implemented
      - The ``$$note_ref$$`` functionality is not supported within data cells
        in tables. It is the user's responsibility to not add notes manually to
        data cells.
    * - Put note text in a notes table on a notes worksheet
      - Desirable
      - Implemented
      - If users provide a ``notes_table`` when producing or writing a workbook,
        a notes worksheet will be created.


Formatting
----------

.. list-table::
    :header-rows: 1
    :widths: 24 17 19 40

    * - Description
      - Essential?
      - Status
      - Explanation
    * - All written content needs to meet the accessibility guidelines
      - Essential
      - Not implemented
      - It is the package user's responsibility to make sure that text follows
        the Analysis Function guidance on `making written content accessible`_.
    * - Links must be accessible
      - Essential
      - Partially implemented
      - Users should provide descriptive hyperlink text using the
        ``(display text)[link]`` syntax.
    * - Format text to make it accessible
      - Desirable
      - Implemented
      - The default theme meets the accessibility guidance on formatting text.
    * - All worksheets should have descriptive titles which are properly tagged
        and formatted
      - Essential
      - Partially implemented
      - Provide descriptive titles to the ``GPTable.title`` and ``subtitles``
        properties. Note: heading tagging in Excel does not meet the standard
        required of webpage heading tagging.
    * - Avoid using symbols in general
      - Desirable
      - Partially implemented
      - An error will be raised if table cells only contain symbols. It is the
        user's responsibility to make sure symbol use within text is appropriate.
    * - Do not use headers and footers, floating text boxes or floating toolbars
      - Essential
      - Implemented
      - These components are not supported by gptables.
    * - Do not use visual devices to divide data regions
      - Desirable
      - Implemented
      - Using gptables without additional formatting does not use such visual devices.
    * - Do not use a background fill
      - Desirable
      - Implemented
      - The gptables default theme does not apply a background fill.
    * - Do not use colour as the only way to convey a message 
      - Essential
      - Implemented
      - The default theme without additional formatting does not apply colour.
    * - When using colour for emphasis check the contrast
      - Essential
      - Not implemented
      - If using colour via additional formatting or a custom theme, it is the
        user's responsibility to check the colour contrast.
    * - Avoid images in spreadsheets
      - Desirable
      - Implemented
      - Adding images is not supported by gptables.
    * - Remove macros
      - Desirable
      - Implemented
      - Macros are not supported by gptables.

.. _`making written content accessible`: https://analysisfunction.civilservice.gov.uk/policy-store/making-analytical-publications-accessible/#section-3


Structure
---------

.. list-table::
    :header-rows: 1
    :widths: 24 17 19 40

    * - Description
      - Essential?
      - Status
      - Explanation
    * - Give worksheets unique names or numbers
      - Essential
      - Implemented
      - Worksheet names come from the ``sheets = {"label": gptable}`` property.
        If names are duplicated, the final ``label: gptable`` pair will be used.
    * - Remove blank worksheets
      - Essential
      - Implemented
      - Blank worksheets are not supported by gptables.
    * - Use cells in column A wisely
      - Essential
      - Implemented
      - ``GPTable`` attributes are written to column A. Title and subtitles are
        first. The order of the remaining descriptive attributes can be
        customised by creating a custom theme with a different ``description_order``.
    * - Position tables against the left-hand edges of each sheet
      - Essential
      - Implemented
      - gptables writes tables starting in column A.
    * - Avoid putting content below a table
      - Desirable
      - Implemented
      - Writing content below a table is not supported in gptables>=1.0.0.
    * - Avoid worksheets with multiple tables
      - Desirable
      - Implemented
      - Writing multiple tables per sheet is not supported in gptables.


Before publishing
-----------------

.. list-table::
    :header-rows: 1
    :widths: 24 17 19 40

    * - Description
      - Essential?
      - Status
      - Explanation
    * - Run a spelling and grammar check
      - Essential
      - Not implemented
      - gptables does not check spelling and grammar, this is the user's
        responsibility.
    * - Use the accessibility checker
      - Desirable
      - Not implemented
      - gptables does not have a built-in accessibility checker. Whilst all
        efforts have been taken to make outputs accessible, the final
        responsibility sits with the user.
    * - Add document information
      - Essential
      - Not implemented
      - gptables does not add title or language information to the document,
        this responsibility sits with the user. Note: the document properties
        available depend on the user's operating system and may not meet
        the standard required for webpages.
    * - Ensure the cursor is in cell A1 of the first worksheet when doing your final save
      - Essential
      - Implemented
      - Workbooks written using gptables will have the cursor in the first cell.
        Note: if the workbook is subsequently opened and saved, it is the user's
        responsibility to check that the cursor has not been moved.
