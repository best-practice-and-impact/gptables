class GPTable:
    def __init__(self, table, title, subtitle, population, units, source, notes):
        """
        Initialise GPTable object object
        """           
        self.table = None
        
        self.title = None
        self.subtitles = []
        self.demographic = None
        self.location = None
        self.units = None
        
        self.source = None
        self.legend = []
        self.notes = []
        
        # Set attributes using methods
        for key, value in kwargs.items():
            getattr(self, 'set_' + key)(value)
        
    def set_table(self, new_table):
        """
        Set the table attribute. Overwrites any existing table.
        """
        self.table = new_table
    
    def set_title(self, new_title):
        """
        Set the title attribute.
        """
        if not isinstance(new_title, str):
            raise ValueError("title attribute must be a string")
            
        self.title = new_title
    
    def add_subtitle(self, new_subtitle):
        """
        Add a single subtitle to the existing list of subtitles.
        """
        if not isinstance(new_subtitle, str):
            raise ValueError("subtitle attributes must be strings")
        self.subtitles.append(new_subtitle)
    
    def set_subtitles(self, new_subtitles, overwrite=True):
        """
        Set a list of subtitles to the subtitles attribute. Overwrites existing
        list of subtitles by default.
        """
        if not isinstance(new_subtitles, list):
            raise ValueError("subtitles must be provided as a list of strings")
            
        if overwrite:
            self.subtitles = new_subtitles
        else:
            self.subtitles += new_subtitles
            
    def set_demographic(self, new_demographic):
        """
        Set the demographic attribute.
        """
        if not isinstance(new_demographic, str):
            raise ValueError("demographic attribute must be a string")
            
        self.demographic = new_demographic
        
    def set_location(self, new_location):
        """
        Set the location attribute.
        """
        if not isinstance(new_location, str):
            raise ValueError("location attribute must be a string")
            
        self.location = new_location
        
        
    def set_units(self, new_units):
        """
        Set the units attribute.
        """
        if not isinstance(new_units, str):
            raise ValueError("units attribute must be a string")
            
        self.units = new_units

    def set_source(self, new_source):
        """
        Set the source attribute.
        """
        if not isinstance(new_source, str):
            raise ValueError("source attribute must be a string")
            
        self.source = new_source
    
    def add_legend(self, new_legend):
        """
        Add a single subtitle to the existing list of subtitles.
        """
        if not isinstance(new_legend, str):
            raise ValueError("legend attributes must be strings")
        self.subtitles.append(new_legend)
    
    def set_legend(self, new_legend, overwrite=True):
        """
        Set a list of subtitles to the subtitles attribute. Overwrites existing
        list of subtitles by default.
        """
        if not isinstance(new_legend, list):
            raise ValueError("legend must be provided as a list of strings")
            
        if overwrite:
            self.subtitles = new_legend
        else:
            self.subtitles += new_legend
            
    def add_note(self, new_note):
        """
        Add a single subtitle to the existing list of subtitles.
        """
        if not isinstance(new_note, str):
            raise ValueError("note attributes must be strings")
        self.subtitles.append(new_note)
    
    def set_notes(self, new_notes, overwrite=True):
        """
        Set a list of subtitles to the subtitles attribute. Overwrites existing
        list of subtitles by default.
        """
        if not isinstance(new_notes, list):
            raise ValueError("notes must be provided as a list of strings")
            
        if overwrite:
            self.subtitles = new_notes
        else:
            self.subtitles += new_notes