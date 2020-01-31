import pandas as pd

class GPTable:
    def __init__(self,
                 table,
                 title,
                 subtitles,
                 scope,
                 units,
                 source,
                 notes=[],
                 index_columns={2:0}):
        """
        Initialise GPTable object object
        """  
        self.multilevel_index = False
        self.VALID_INDEX_LEVELS = [1, 2, 3]
        
        self.table_shape = (0, 0)
         
        self.index_columns = {}  # 0-indexed column mapped to index level
        self._column_headings = [] # All other columns
        self.table = pd.DataFrame()
        
        self.title = None
        self.subtitles = []
        self.scope = None
        self.units = None  # Dict for units to columns, or single str
        
        self.source = None
        self.legend = []
        self.notes = []
        
        # Set attributes using methods
#        # Locals method uses an unordered dict, so best to do this manually
#        for key, value in locals():
#            getattr(self, 'set_' + key)(value)
        
        self.set_table(table, index_columns)
        self.set_title(title)
        self.set_subtitles(subtitles)
        self.set_scope(scope)
        self.set_units(units)
        self.set_source(source)
        self.set_notes(notes)
        
    def set_table(self, new_table, new_index_columns=None):
        """
        Set the `table`, `table_shape`, `index_columns` attributes. Overwrites
        existing values for these attributes.
        """
        if not isinstance(new_table, pd.DataFrame):
            raise ValueError("`table` must be a pandas DataFrame")
        self.table = new_table
        self._set_table_shape()
        
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
            valid_levels = all(level in self.VALID_INDEX_LEVELS for level in new_index_columns.keys())
            if not valid_levels:
                msg = ("Each dict key must be a valid index level:"
                       f" {VALID_INDEX_LEVELS}")
                raise ValueError(msg)
            
            column_indexes = [col for col in new_index_columns.values()]
            if not all(isinstance(int, col) for col in column_indexes):
                raise ValueError("Column indexes must be single integers")
                
            valid_columns = all(self._valid_column_index(col) for col in column_indexes)
            if not valid_columns:
                msg = ("Out of range: `index_columns` must be levels mapped to"
                       " valid 0-indexed column numbers")
                raise ValueError(msg)
            
            if len(new_index_columns.keys() > 1):
                self.multilevel_index = True
            else:
                self.multilevel_index = False
            
            self.index_columns = new_index_columns
            self._set_column_headings()
        else:
            msg = ("`index_columns` must be a dict mapping a valid index level"
                   " to a 0-indexed column number")
            raise ValueError(msg)
    
    def _valid_column_index(self, column_index):
        """
        Check if `column_index` is valid, given the `table_shape`.
        """
        return column_index in range(self.table_shape[1])
        
    def _set_column_headings(self):
        """
        Sets the `column_headings` attribute to the list of column indexes that
        are not set as `index_columns`.
        """
        index_cols = list(self.index_columns.values())
        self._column_headings = [x for x in range(self.table_shape[1])] - index_cols

    def _set_table_shape(self):
        """
        Subsequently resets the `index_columns` and `column_headings` attributes
        to verify that they are valid for the new tables shape.
        """
        self.table_shape = self.table.shape
        self.table_shape[0] + 1  # Account for column headings
        self.set_index_columns(self, self.index_columns)
    
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
        self.demographic = new_scope        

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
            self.subtitles = new_legend
        else:
            self.subtitles += new_legend
            
    def add_note(self, new_note):
        """
        Add a single note to the existing `notes` list.
        """
        if not isinstance(new_note, str):
            raise ValueError("`notes` entries must be strings")
        self.subtitles.append(new_note)
    
    def set_notes(self, new_notes, overwrite=True):
        """
        Set a list of notes to the `notes` attribute. Overwrites existing
        `notes` list by default.If overwrite is False, new entries are
        appended to the `notes` list.
        """
        if not isinstance(new_notes, list):
            raise ValueError("notes must be provided as a list of strings")
            
        if overwrite:
            self.subtitles = new_notes
        else:
            self.subtitles += new_notes