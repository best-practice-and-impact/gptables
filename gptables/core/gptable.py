import pandas as pd

class GPTable:
    """
    A Good Practice Table. Stores a table and metadata for writing a table
    to excel.
    
    Attributes
    ----------
    title : str
        description of the table
    subtitles : list
        subtitiles as strings
    scope : str
        description of scope/basis of data in table
    legend : list
        descriptions of special notations used in table
    notes : dict
        mapping each notes reference to the note as {ref: note}
    index_columns : dict
        mapping an index level to a 0-indexed column as {level: column}.
        Default is a level two index in the first column ({2: 0}).
    
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
                 index_columns={2:0}):
        
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
        self.notes=[]
        
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
        
    def set_table(self, new_table, new_index_columns=None):
        """
        Set the `table` and `index_columns` attributes. Overwrites existing
        values for these attributes.
        """
        if not isinstance(new_table, pd.DataFrame):
            raise ValueError("`table` must be a pandas DataFrame")
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
                msg = ("Each dict key must be a valid index level:"
                       f" {self._VALID_INDEX_LEVELS}")
                raise ValueError(msg)
            
            column_indexes = [col for col in new_index_columns.values()]
            if not all(isinstance(col, int) for col in column_indexes):
                raise ValueError("Column indexes must be single integers")
                
            valid_columns = all(self._valid_column_index(col) for col in column_indexes)
            if not valid_columns:
                msg = ("Out of range: `index_columns` must be levels mapped to"
                       " valid 0-indexed column numbers")
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
        if not isinstance(new_title, str):
            raise ValueError("`title` attribute must be a string")
            
        self.title = new_title
    
    def add_subtitle(self, new_subtitle):
        """
        Add a single subtitle to the existing list of `subtitles`.
        """
        if not isinstance(new_subtitle, str):
            raise ValueError("`subtitles` must be strings")
        self.subtitles.append(new_subtitle)
    
    def set_subtitles(self, new_subtitles, overwrite=True):
        """
        Set a list of subtitles to the `subtitles` attribute. Overwrites
        existing ist of subtitles by default. If `overwrite` is False, new list
        is appended to existing list of subtitles.
        """
        if not isinstance(new_subtitles, list):
            raise ValueError("`subtitles` must be provided as a list of strings")
            
        if overwrite:
            self.subtitles = new_subtitles
        else:
            self.subtitles += new_subtitles
            
    def set_scope(self, new_scope):
        """
        Set the `scope` attribute.
        """
        if not isinstance(new_scope, str):
            raise ValueError("`scope` attribute must be a string")
        self.scope = new_scope        

    def set_units(self, new_units):
        """
        Set the `units` attribute to the supplied str or dict. Units as a dict
        should be in the format {units:[column_indexes]}. Columns are
        0-indexed, excluding `index_columns`.
        """
        if not isinstance(new_units, (str, dict)):
            msg = ("`units` attribute must be a string or dict of str:list of ints")
            raise ValueError(msg)
            
        self.units = new_units

    def set_source(self, new_source):
        """
        Set the source attribute to the specified str.
        """
        if not isinstance(new_source, str):
            raise ValueError("`source` attribute must be a string")
            
        self.source = new_source
    
    def add_legend(self, new_legend):
        """
        Add a single legend entry to the existing `legend` list.
        """
        if not isinstance(new_legend, str):
            raise ValueError("`legend` entried must be strings")
        self.subtitles.append(new_legend)
    
    def set_legend(self, new_legend, overwrite=True):
        """
        Set a list of legend entries to the `legend` attribute. Overwrites
        existing legend entries by default. If overwrite is False, new entries 
        are appended to the `legend` list.
        """
        if not isinstance(new_legend, list):
            raise ValueError("legend must be provided as a list of strings")
            
        if overwrite:
            self.legend = new_legend
        else:
            self.legend += new_legend
            
    def add_annotation(self, new_annotation):
        """
        Add a single note to the existing `annotations` dict.
        """
        if not isinstance(new_annotation, dict):
            raise ValueError("`notes` entries must be dictionaries")
        self.annotations.update(new_annotation)
    
    def set_annotations(self, new_annotations, overwrite=True):
        """
        Set a list of notes to the `annotations` attribute. Overwrites existing
        `annotations` dict by default. If overwrite is False, new entries are
        appended to the `annotations` dict.
        """
        if not isinstance(new_annotations, dict):
            msg = ("notes must be provided as a dict of {reference: note}")
            raise ValueError(msg)
            
        if overwrite:
            self.annotations = new_annotations
        else:
            self.annotations.update(new_annotations)
            
    def add_note(self, new_note):
        """
        Add a single note to the existing `notes` list.
        """
        if not isinstance(new_note, str):
            raise ValueError("`notes` entries must be strings")
        self.notes.append(new_note)
    
    def set_notes(self, new_notes, overwrite=True):
        """
        Set a list of notes to the `notes` attribute. Overwrites existing
        `notes` list by default.If overwrite is False, new entries are
        appended to the `notes` list.
        """
        if not isinstance(new_notes, list):
            msg = ("`notes` must be provided as a list of strings")
            raise ValueError(msg)
            
        if overwrite:
            self.notes = new_notes
        else:
            self.notes += new_notes
