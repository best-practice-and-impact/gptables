import pandas as pd
from xlsxwriter.format import Format

class GPTable:
    """
    A Good Practice Table. Stores a table and metadata for writing a table
    to excel.
    
    Attributes
    ----------
    table : pandas.DataFrame
        table to be written to an Excel workbook
    title : str
        description of the table
    subtitles : list
        subtitiles as a list of strings
    scope : str
        description of scope/basis of data in table
    units : str or dict
        units used in all (str) or each (dict) column of `table`
    legend : list
        descriptions of special notation used in `table`
    annotations : dict
        notes that are referenced in header or table elements (excluding data)
    notes : list
        notes that are not referenced
    index_columns : dict
        mapping an index level to a 0-indexed column as {level: column}.
        Default is a level two index in the first column ({2: 0}).
    additional_formatting : dict
        table-specific formatting for columns, rows or individual cells
    
    Methods
    -------
    
    """  
    def __init__(self,
                 table,
                 title,
                 scope,
                 units,
                 source,
                 subtitles=[],
                 legend=[],
                 annotations={},
                 notes=[],
                 index_columns={2:0},
                 additional_formatting=[]
                 ):
        
        # Attributes
        self.title = None
        self.subtitles = []
        
        self.scope = None
        self.units = None  # str or {units (str):column index (int)} dict
        
        self._VALID_INDEX_LEVELS = [1, 2, 3]
        self.index_levels = 0
        self.index_columns = {}  # {index level (int): column index (int)}
        self._column_headings = set() # Non-index column headings
        self.table = pd.DataFrame()
        
        self.source = None
        self.legend = []
        self.annotations = {}
        self.notes = []
        
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
        self.set_scope(scope)
        self.set_units(units)
        self.set_table(table, index_columns)
        self.set_source(source)
        self.set_legend(legend)
        self.set_annotations(annotations)
        self.set_notes(notes)
        self.set_additional_formatting(additional_formatting)
        
    def set_table(self, new_table, new_index_columns=None):
        """
        Set the `table` and `index_columns` attributes. Overwrites existing
        values for these attributes.
        """
        if not isinstance(new_table, pd.DataFrame):
            raise TypeError("`table` must be a pandas DataFrame")
        self.table = new_table
        
        if new_index_columns is None:
            new_index_columns = self.index_columns
        self.set_index_columns(new_index_columns)
        
    def set_index_columns(self, new_index_columns):
        """
        Set the `index_columns` attribute. Overwrites any existing values.
        An dict must be supplied. This dict should map index level to a
        single 0-indexed column number. All other columns will be considered
        as data columns.
        """
        if isinstance(new_index_columns, dict):
            # Check if levels and values are valid
            valid_levels = all(level in self._VALID_INDEX_LEVELS for level in new_index_columns.keys())
            if not valid_levels:
                msg = ("Each `index_columns` dict key must be a valid index"
                       f" level: {self._VALID_INDEX_LEVELS}")
                raise ValueError(msg)
            
            column_indexes = [col for col in new_index_columns.values()]
            if not all(isinstance(col, int) for col in column_indexes):
                raise TypeError("column_indexes must be integers")
                
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
        
    def _set_column_headings(self):
        """
        Sets the `column_headings` attribute to the set of column indexes that
        are not assigned to `index_columns`.
        """
        index_cols = set(self.index_columns.values())
        self._column_headings = {x for x in range(self.table.shape[1])} - index_cols
    
    def set_title(self, new_title):
        """
        Set the `title` attribute.
        """
        self._validate_text(new_title, "title")
        self.title = new_title
    
    def add_subtitle(self, new_subtitle):
        """
        Add a single subtitle to the existing list of `subtitles`.
        """
        self._validate_text(new_subtitle, "subtitles")
        self.subtitles.append(new_subtitle)
    
    def set_subtitles(self, new_subtitles, overwrite=True):
        """
        Set a list of subtitles to the `subtitles` attribute. Overwrites
        existing ist of subtitles by default. If `overwrite` is False, new list
        is appended to existing list of subtitles.
        """
        if not isinstance(new_subtitles, list):
            msg =("`subtitles` must be provided as a list containing strings"
                  " and/or lists of strings and format dictionaries"
                  " (rich text)")
            raise TypeError(msg)
        for text in new_subtitles:
            self._validate_text(text, "subtitles")
            
        if overwrite:
            self.subtitles = new_subtitles
        else:
            self.subtitles += new_subtitles
            
    def set_scope(self, new_scope):
        """
        Set the `scope` attribute.
        """
        self._validate_text(new_scope, "scope")
        self.scope = new_scope        

    def set_units(self, new_units):
        """
        Set the `units` attribute to the supplied str or dict. Units as a dict
        should be in the format {units:[column_indexes]}. Columns are
        0-indexed, excluding `index_columns`.
        """            
        if isinstance(new_units, (str, list)) or new_units is None:
            self._validate_text(new_units, "units")
        elif isinstance(new_units, dict) and len(new_units) > 0:
            for text in new_units.keys():
                self._validate_text(text, "units")
        else:
            msg = ("`units` attribute must be a string or dictionary of"
                   " {text: list of 0-indexed columns}")
            raise TypeError(msg)
            
        self.units = new_units

    def set_source(self, new_source):
        """
        Set the source attribute to the specified str.
        """
        self._validate_text(new_source, "source")
            
        self.source = new_source
    
    def add_legend(self, new_legend):
        """
        Add a single legend entry to the existing `legend` list.
        """
        self._validate_text(new_legend, "legend")
        self.subtitles.append(new_legend)
    
    def set_legend(self, new_legend, overwrite=True):
        """
        Set a list of legend entries to the `legend` attribute. Overwrites
        existing legend entries by default. If overwrite is False, new entries 
        are appended to the `legend` list.
        """
        if not isinstance(new_legend, list):
            msg = ("`legend` must be provided as a list of text elements")
            raise TypeError(msg)
        for text in new_legend:
            self._validate_text(text, "legend")
        
        if overwrite:
            self.legend = new_legend
        else:
            self.legend += new_legend
            
    def add_annotation(self, new_annotation):
        """
        Add one or more annotations to the existing `annotations` dictionary.
        """
        if not isinstance(new_annotation, dict):
            raise TypeError("`annotations` entries must be dictionaries")
        for text in new_annotation.values():
            self._validate_text(text, "annotations")
        self.annotations.update(new_annotation)
    
    def set_annotations(self, new_annotations, overwrite=True):
        """
        Set a list of notes to the `annotations` attribute. Overwrites existing
        `annotations` dict by default. If overwrite is False, new entries are
        appended to the `annotations` dict.
        """
        if not isinstance(new_annotations, dict):
            msg = ("annotations must be provided as a dictionary of"
                   " {reference: note}")
            raise TypeError(msg)
        
        if not all(isinstance(key, str) for key in new_annotations.keys()):
            raise TypeError("`annotations` keys must be strings")
        
        for text in new_annotations.values():
            self._validate_text(text, "annotations")
            
        if overwrite:
            self.annotations = new_annotations
        else:
            self.annotations.update(new_annotations)
            
    def add_note(self, new_note):
        """
        Add a single note to the existing `notes` list.
        """
        self._validate_text(new_note, "notes")
        self.notes.append(new_note)
    
    def set_notes(self, new_notes, overwrite=True):
        """
        Set a list of notes to the `notes` attribute. Overwrites existing
        `notes` list by default.If overwrite is False, new entries are
        appended to the `notes` list.
        """
        if not isinstance(new_notes, list):
            msg = ("`notes` must be a list of text elements")
            raise TypeError(msg)
        for text in new_notes:
            self._validate_text(text, "notes")
            
        if overwrite:
            self.notes = new_notes
        else:
            self.notes += new_notes
            
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
                  for label in item[key].keys()
                  ]
        for label in labels:
            if label not in self._valid_format_labels:
                msg = ("`{label}` is not a valid XlsxWriter Format property")
                raise ValueError(msg)
    
    @staticmethod
    def _validate_text(obj, attr):
        """
        Validate that an object contains valid text elements. These are either
        strings or list of strings and dictionaries.
        """
        if isinstance(obj, str) or obj is None:
            return None
        
        msg = (f"{attr} text should be provided as strings or lists of"
                   f" strings and dictionaries (rich-text). {type(obj)} are"
                   " not valid text elements.")
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
