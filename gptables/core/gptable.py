import pandas as pd
import re
from xlsxwriter.format import Format

class GPTable:
    """
    A Good Practice Table. Stores a table and metadata for writing a table
    to excel.

    .. note:: Deprecated in v1.1.0: Ability to reference notes within
        ``GPTable.table.columns`` will be removed in v2 of gptables. Please use
        ``GPTable.table_notes`` to ensure references are correctly placed and ordered.

    Attributes
    ----------
    table : pandas.DataFrame
        table to be written to an Excel workbook
    table_name : str
        name for table. Should be unique with no spaces and always begin with a 
        letter, an underscore character, or a backslash. Use letters, numbers, 
        periods, and underscore characters for the rest of the name.
    title : str
        title of the table
    subtitles : List[str], optional
        subtitles as a list of strings
    instructions : str, optional
        instructions on how to read the sheet. If not provided, defaults to
        "This worksheet contains one table. Some cells may refer to notes,
        which can be found on the notes worksheet."
    scope : str, optional
        description of scope/basis of data in table if not included in title
    source : str, optional
        description of the source of the data in table if not included in cover
    units : dict, optional
        units used in each (dict) column of table
    legend : list, optional
        descriptions of special notation used in table
    index_columns : dict, optional
        mapping an index level to a 0-indexed column as {level: column}.
        Default is a level two index in the first column ({2: 0}).
    additional_formatting : dict, optional
        table-specific formatting for columns, rows or individual cells
    """

    def __init__(self,
                 table,
                 table_name,
                 title,
                 scope=None,
                 source=None,
                 units=None,
                 table_notes=None,
                 subtitles=[],
                 instructions="",
                 legend=[],
                 index_columns={2:0},
                 additional_formatting=[],
                 ):
        
        # Attributes
        self.title = None
        self.subtitles = []
        
        self.units = None  # str or {units (str):column index (int)} dict
        self.table_notes = None  # str or {units (str):column index (int)} dict
        
        self._VALID_INDEX_LEVELS = [1, 2, 3]
        self.index_levels = 0
        self.index_columns = {}  # {index level (int): column index (int)}
        self._column_headings = set() # Non-index column headings
        self.table = pd.DataFrame()
        self.table_name = None
        self.data_range = [0] * 4
        
        self.scope = None
        self.source = None
        self.legend = []
        self._annotations = []
        
        self.additional_formatting = []
        
        # Valid format labels from XlsxWriter
        self._valid_format_labels = [
                attr.replace("set_", "")
                for attr in Format().__dir__() 
                if attr.startswith('set_')
                and callable(getattr(Format(), attr))
                ]
        
        # Call methods to set attributes        
        self.set_title(title)
        self.set_subtitles(subtitles)
        self.set_instructions(instructions)
        self.set_additional_formatting(additional_formatting)
        self.set_table(table, index_columns, units, table_notes)
        self.set_table_name(table_name)
        self.set_scope(scope)
        self.set_source(source)
        self.set_legend(legend)
        self._set_data_range()
        

    def set_table(self, new_table, new_index_columns = None, new_units = None, new_table_notes = None):
        """
        Set the `table`, `index_columns`, `units` and `table_notes` attributes. Overwrites
        existing values for these attributes.
        """
        if not isinstance(new_table, pd.DataFrame):
            raise TypeError("`table` must be a pandas DataFrame")
        
        default_index = pd.Index(range(new_table.shape[0]))
        if not all(new_table.index == default_index) and not new_table.empty:
            msg = ("`table` index must not contain index data. It can be reset"
                   " before adding to a GPTable (see DataFrame.reset_index())."
                   " Please ensure that index data is stored in the first 1-3"
                   " columns of `table` and is indicated in `index_columns`.")
            raise ValueError(msg)

        self.table = new_table.reset_index(drop=True)

        self._validate_all_column_names_have_text()
        self._validate_no_duplicate_column_names()

        if new_index_columns is None:
            new_index_columns = self.index_columns
        self.set_index_columns(new_index_columns)

        if new_units is None:
            new_units = self.units
        self.set_units(new_units)

        if new_table_notes is None:
            new_table_notes = self.table_notes
        self.set_table_notes(new_table_notes)


    def set_index_columns(self, new_index_columns):
        """
        Set the `index_columns` attribute. Overwrites any existing values.
        A dict must be supplied. This dict should map index level to a
        single 0-indexed column number. All other columns will be considered
        as data columns.
        """
        if isinstance(new_index_columns, dict):
            # Check if levels and values are valid
            valid_levels = all(level in self._VALID_INDEX_LEVELS for level in new_index_columns.keys())
            if not valid_levels:
                msg = ("`index_columns` dictionary keys must be valid index"
                       f" levels: {self._VALID_INDEX_LEVELS}")
                raise ValueError(msg)
            
            if not all(isinstance(col, int) for col in new_index_columns.values()):
                # Convert col name to numeric index
                for key, value in new_index_columns.items():
                    col_iloc = self.table.columns.get_loc(value)
                    new_index_columns.update({key: col_iloc})
                    
            column_indexes = [col for col in new_index_columns.values()]
                
            valid_columns = all(self._valid_column_index(col) for col in column_indexes)
            if not valid_columns:
                msg = ("Out of range - `index_columns` dictionary values must"
                       "be valid, 0-indexed column numbers")
                raise ValueError(msg)
            
            self.index_levels = len(new_index_columns.keys())
            
            self.index_columns = new_index_columns
            self._set_column_headings()
        else:
            msg = ("`index_columns` must be a dict mapping a valid index level"
                   " to a 0-indexed column number")
            raise ValueError(msg)
    

    def _valid_column_index(self, column_index):
        """
        Check if `column_index` is valid, given the `table` shape.
        """
        return column_index in range(self.table.shape[1])
        

    def _set_column_headings(self): # TODO: check custom formatting in headers
        """
        Sets the `column_headings` attribute to the set of column indexes that
        are not assigned to `index_columns`.
        """
        index_cols = set(self.index_columns.values())
        self._column_headings = {x for x in range(self.table.shape[1])} - index_cols


    def _validate_all_column_names_have_text(self):
        """
        Validate that all column names in header row have text.
        """
        for column_name in self.table.columns:
            if pd.isna(column_name):
                msg = ("Null column name found in table data - column names must all have text")
                raise ValueError(msg)
            elif len(column_name) > 0:
                continue
            else:
                msg = ("Empty column name found in table data - column names must all have text")
                raise ValueError(msg)


    def _validate_no_duplicate_column_names(self):
        """
        Validate that there are no duplicate column names in table data.
        """
        if len(self.table.columns) != len(set(self.table.columns)):
            msg = ("Duplicate column names found in table data - column names must be unique")
            raise ValueError(msg)


    def set_table_name(self, new_table_name):
        """
        Set the `table_name` attribute.
        """
        if not isinstance(new_table_name, str):
            msg = ("table_name should be provided as a string")
            raise TypeError(msg)

        elif len(new_table_name) != len("".join(new_table_name.split())):
            msg = ("Whitespace found in table_name, remove or replace with underscores")
            raise ValueError(msg)

        else:
            self.table_name = new_table_name


    def set_title(self, new_title):
        """
        Set the `title` attribute.
        """
        self._validate_text(new_title, "title")

        if isinstance(new_title, list):
            new_title = FormatList(new_title)

        self.title = new_title


    def add_subtitle(self, new_subtitle):
        """
        Add a single subtitle to the existing list of `subtitles`.
        """
        self._validate_text(new_subtitle, "subtitles")

        if isinstance(new_subtitle, list):
            new_subtitle = FormatList(new_subtitle)

        self.subtitles.append(new_subtitle)


    def set_subtitles(self, new_subtitles, overwrite=True):
        """
        Set a list of subtitles to the `subtitles` attribute. Overwrites
        existing ist of subtitles by default. If `overwrite` is False, new list
        is appended to existing list of subtitles.
        """
        if new_subtitles is None:
            new_subtitles = []

        if not isinstance(new_subtitles, (list)):
            msg =("`subtitles` must be provided as a list containing strings"
                  " and/or lists of strings and format dictionaries"
                  " (rich text)")
            raise TypeError(msg)

        for text in new_subtitles:
            self._validate_text(text, "subtitles")

        new_subtitles = [FormatList(text) if isinstance(text, list) else text for text in new_subtitles]

        if overwrite:
            self.subtitles = new_subtitles
        else:
            self.subtitles += new_subtitles
            
    def set_instructions(self, new_instructions):
        """
        Set `instructions` attribute.
        """
        self._validate_text(new_instructions, "instructions")

        if len(new_instructions) == 0:
            self.instructions = "This worksheet contains one table. Some cells may refer to notes, which can be found on the notes worksheet."
        elif isinstance(new_instructions, list):
            self.instructions = FormatList(new_instructions)
        else:
            self.instructions = new_instructions


    def set_scope(self, new_scope):
        """
        Set the `scope` attribute.
        """
        if new_scope == None:
            new_scope = ""
            return

        self._validate_text(new_scope, "scope")

        if isinstance(new_scope, list):
            new_scope = FormatList(new_scope)

        self.scope = new_scope


    def set_units(self, new_units): # TODO: custom formatting in units?
        """
        Adds units to column headers.
        Units should be in the format {column: units_text}. Column can be column name or 0-indexed column
        number in `table`. 
        """    
        if isinstance(new_units, dict) and len(new_units) > 0:
            for value in new_units.values():
                self._validate_text(value, "units")

            headers = self.table.columns.values.tolist()

            # Check if notes have already been added to headers...
            unmodified_headers = [header.split("\n")[0] for header in headers]

            # ...if so, apply any units applied to headers without notes, to headers with notes
            for n in range(len(unmodified_headers)):
                if unmodified_headers[n] in list(new_units.keys()):
                    new_units[n] = new_units.pop(unmodified_headers[n])

            # Convert numeric keys to column names
            new_headers_keys = [headers[key] if isinstance(key, int) else key for key in new_units.keys()]
            new_headers_values = [f"{key}\n({value})" for key, value in zip(new_headers_keys, new_units.values())]
            new_headers = dict(zip(new_headers_keys, new_headers_values))

            self.table = self.table.rename(columns = new_headers)

            if len(self.additional_formatting) > 0:
                self._update_column_names_in_additional_formatting(new_headers)

        elif not new_units is None:
            msg = ("`units` attribute must be a dictionary or None"
                   " ({column: units_text})")
            
            raise TypeError(msg)

        self.units = new_units

    def _update_column_names_in_additional_formatting(self, col_names):
        """
        Parameters
        ----------
        col_names: dict
            with keys old names and values new names, where new names are old names plus units
        Return
        ------
        None
        """
        formatting_list = self.additional_formatting
        for dictionary in formatting_list:
            if list(dictionary.keys()) == ["column"]:
                format = list(dictionary.values())[0]

                # new_name if name==old_name else name for name in col_names
                format["columns"] = [col_names[name] if name in list(col_names.keys()) else name for name in format["columns"]]

        self.additional_formatting = formatting_list

    def set_table_notes(self, new_table_notes): # TODO: custom formatting in column headers?
        """
        Adds note references to column headers.
        `table_notes` should be in the format {column: "$$note_reference$$"}.
        Column can be column name or 0-indexed column number in `table`.
        """
        if isinstance(new_table_notes, dict) and len(new_table_notes) > 0:
            for value in new_table_notes.values():
                self._validate_text(value, "table_notes")

            headers = self.table.columns.values.tolist()

            # Check if units have already been added to headers...
            unmodified_headers = [header.split("\n")[0] for header in headers]

            # ...if so, apply any notes applied to headers without units, to headers with units
            for n in range(len(unmodified_headers)):
                if unmodified_headers[n] in list(new_table_notes.keys()):
                    new_table_notes[n] = new_table_notes.pop(unmodified_headers[n])

            # Convert numeric keys to column names
            new_headers_keys = [headers[key] if isinstance(key, int) else key for key in new_table_notes.keys()]
            new_headers_values = [f"{key}\n{value}" for key, value in zip(new_headers_keys, new_table_notes.values())]
            new_headers = dict(zip(new_headers_keys, new_headers_values))

            self.table = self.table.rename(columns = new_headers)

            if len(self.additional_formatting) > 0:
                self._update_column_names_in_additional_formatting(new_headers)

        elif not new_table_notes is None:
            msg = ("`table_notes` attribute must be a dictionary or None"
                   " ({column: '$$note_reference$$'})")
            raise TypeError(msg)

        self.table_notes = new_table_notes


    def set_source(self, new_source):
        """
        Set the source attribute to the specified str.
        """
        if new_source == None:
            new_source = ""
            return

        self._validate_text(new_source, "source")

        if isinstance(new_source, list):
            new_source = FormatList(new_source)

        self.source = new_source
    

    def add_legend(self, new_legend):
        """
        Add a single legend entry to the existing `legend` list.
        """
        self._validate_text(new_legend, "legend")

        if isinstance(new_legend, list):
            new_legend = FormatList(new_legend)

        self.legend.append(new_legend)
    

    def set_legend(self, new_legend, overwrite=True):
        """
        Set a list of legend entries to the `legend` attribute. Overwrites
        existing legend entries by default. If overwrite is False, new entries 
        are appended to the `legend` list.
        """
        if new_legend is None:
            self.legend = []
            return
        if not isinstance(new_legend, list):
            msg = ("`legend` must be provided as a list of text elements")
            raise TypeError(msg)
        for text in new_legend:
            self._validate_text(text, "legend")

        new_legend = [FormatList(text) if isinstance(text, list) else text for text in new_legend]

        if overwrite:
            self.legend = new_legend
        else:
            self.legend += new_legend

    def _set_annotations(self, description_order):
        """
        Set a list of note references to the `_annotations` attribute.
        """
        elements = [
                "title",
                "subtitles",
                *description_order,
                "units",
                "table_notes",
                ]

        ordered_refs = []

        for attr in elements:
            attr_current = getattr(self, attr)
            references = self._get_references_from_attr(attr_current)
            ordered_refs.extend(references)

        # Deprecated as of v1.1.0 - instead use `table_notes` to add references to column headers
        table_refs = self._get_references_from_table()
        ordered_refs.extend(table_refs)

        # remove duplicates from ordered_refs and assign to self._annotations
        self._annotations = list(dict.fromkeys(ordered_refs))


    def _get_references_from_attr(self, data):
        """
        Finds references in a string or list/dict of strings. Works
        recursively on list elements and dict values. Other types are ignored.
        Returns ordered list of references from attribute.
        
        Parameters
        ----------
        data : string or list/dict of strings
            object containing strings to replace references in

        Returns
        -------
        list of str
        """
        ordered_refs = []
        if isinstance(data, str):
            ordered_refs.extend(self._get_references(data))
        if isinstance(data, list):
            for n in range(len(data)):
                ordered_refs.extend(self._get_references_from_attr(data[n]))
        if isinstance(data, dict):
            for key in data.keys():
                ordered_refs.extend(self._get_references(data[key]))
        if isinstance(data, FormatList):
            data_list = data.list
            for n in range(len(data_list)):
                if isinstance(data_list[n], str):
                    ordered_refs.extend(self._get_references(data_list[n]))

        return ordered_refs

    # Deprecated as of v1.1.0 - instead use `table_notes` to add references to column headers
    def _get_references_from_table(self):
        """
        Get note references in the table column headings and index columns.
        """
        table = self.table
        
        ordered_refs = []
        column_references = self._get_references_from_attr(table.columns.to_list())
        ordered_refs.extend(column_references)

        index_columns = self.index_columns.values()
        for col in index_columns:
            index_column = table.iloc[:, col]
            index_column_references = self._get_references_from_attr(index_column.to_list())
            ordered_refs.extend(index_column_references)

        return ordered_refs


    @staticmethod
    def _get_references(string):
        """
        Given a single string, return occurrences of note references (denoted by
        flanking dollar signs [$$reference$$]).
        
        Parameters
        ----------
        string : str
            the string to find references within

        Returns
        -------
        list of str
            list of note references
        """
        ordered_refs = []
        refs_raw = re.findall(r"[$]{2}.*?[$]{2}", string)
        refs_clean = [w.replace("$", "") for w in refs_raw]
        ordered_refs.extend(refs_clean)

        return ordered_refs


    def set_additional_formatting(self, new_formatting):
        """
        Set a dictionary of additional formatting to be applied to this table.
        """
        if not isinstance(new_formatting, list):
            msg = ("`additional_formatting` must be a list of dictionaries")
            raise TypeError(msg)
        keys = [key for item in new_formatting for key in item.keys()]
        for key in keys:
            if key not in ["column", "row", "cell"]:
                msg = (f"`{key}` is not a supported format type. Please use"
                       " `column`, `row` or `cell`")
                raise ValueError(msg)
        
        self._validate_format_labels(new_formatting)
            
        self.additional_formatting = new_formatting
    

    def _validate_format_labels(self, format_list):
        """
        Validate that format labels are valid property of XlsxWriter Format.
        """
        labels = [label
                  for item in format_list
                  for key in item.keys()
                  for label in item[key]["format"]
                  ]
        for label in labels:
            if label not in self._valid_format_labels:
                msg = (f"`{label}` is not a valid XlsxWriter Format property")
                raise ValueError(msg)


    def _set_data_range(self):
        """
        Get the top-left and bottom-right cell reference of the table data.
        """
        #TODO: ugly code
        row_offset = sum([
            int(self.title is not None),
            int(self.scope is not None),
            int(self.source is not None),
        ]) + 1 #corresponds to instructions which are included by default

        if self.subtitles is not None:
            row_offset += len(self.subtitles)
        if self.legend is not None:
            row_offset += len(self.legend)
        
        self.data_range = [
            row_offset,
            0,
            self.table.shape[0] + row_offset,
            self.table.shape[1] - 1
        ]

    @staticmethod
    def _validate_text(obj, attr):
        """
        Validate that an object contains valid text elements. These are either
        strings or list of strings and dictionaries.
        """
        if isinstance(obj, str):
            return None

        if isinstance(obj, list):
            for element in obj:
                if not isinstance(element, (str, dict)):
                    msg = (f"{attr} text should be provided as strings or"
                           " lists of strings and dictionaries (rich-text)."
                           f" {type(element)} are not valid rich text"
                           " elements.")
                    raise TypeError(msg)
        else:
            msg = (f"{attr} text should be provided as strings or lists of"
                   f" strings and dictionaries (rich-text). {type(obj)} are"
                   " not valid text elements.")
            raise TypeError(msg)

class FormatList:
    """
    Class for storing list of alternating string and dictionary objects.
    Dictionaries specify additional formatting to be applied to the following string.
    """
    def __init__(self, list):
        self.list = list
        self._set_string_property()

    def _set_string_property(self):
        string = ""
        for entry in self.list:
            if isinstance(entry, str):
                string += entry

        self.string = string
