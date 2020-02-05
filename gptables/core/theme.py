import yaml

# gptheme = Theme(gptheme.conf)


class Theme:
    """
    A class that defines a set of format attributes for use in xlsxwriter.

    This class associates a dict of format attributes with table elements.

    See XlsxWriter
    [format properties](https://xlsxwriter.readthedocs.io/format.html)
    for valid options.

    Parameters
    ----------
    config : dict or .yaml/.yml
        theme specification

    Returns
    -------
        None
    """

    def __init__(
            self,
            config):
        """
        Initialise theme object
        """
        # Read config file or dict
        cfg = self._parse_config(config)
        
        if "global" in cfg.keys():
            default_format = cfg.pop("global")
        else:
            default_format = {}
        
        self.title_format = default_format.copy()
        self.subtitle_format = default_format.copy()
        
        self.scope_format = default_format.copy()
        self.unit_format = default_format.copy()
        
        self.column_heading_format = default_format.copy()
        self.index_1_format = default_format.copy()
        self.index_2_format = default_format.copy()
        self.index_3_format = default_format.copy()
        self.data_format = default_format.copy()

        self.source_format = default_format.copy()
        self.legend_format = default_format.copy()
        self.note_format = default_format.copy()

        # Set attributes using methods
        for key, value in cfg.items():
            getattr(self, "update_" + key + "_format")(value)
            
    def _parse_config(self, config):
        """
        Parse yaml configuration to dictionary.
        """
        if isinstance(config, str):
            if not config.endswith((".yml", ".yaml")):
                raise ValueError("Theme configuration files must be YAML")
            with config.open() as file:
                cfg = yaml.safe_load(file)
                
        elif isinstance(config, dict):
            cfg = config
            
        else:
            raise ValueError("Theme configuration must be a dict or YAML file")
            
        return cfg
            
    def update_column_heading_format(self, format_dict):
        """
        Update the `column_heading_format` attribute. Where keys already exist,
        existing items are replaced.
        """
        self.column_heading_format.update(format_dict)

    def update_index_1_format(self, format_dict):
        """
        Update the `index_1_format` attribute. Where keys already exist, existing
        items are replaced.
        """
        self.index_1_format.update(format_dict)
        
    def update_index_2_format(self, format_dict):
        """
        Update the `index_2_format` attribute. Where keys already exist, existing
        items are replaced.
        """
        self.index_2_format.update(format_dict)
        
    def update_index_3_format(self, format_dict):
        """
        Update the `index_3_format` attribute. Where keys already exist, existing
        items are replaced.
        """
        self.index_3_format.update(format_dict)

    def data_format_format(self, format_dict):
        """
        Update the `data_format_format` attribute. Where keys already exist,
        existing items are replaced.
        """
        self.data_format_format.update(format_dict)
    
    def update_title_format(self, format_dict):
        """
        Update the `title_format` attribute. Where keys already exist, existing
        items are replaced..
        """
        self.title_format.update(format_dict)
    
    def update_subtitle_format(self, format_dict):
        """
        Update the `subtitle_format` attribute. Where keys already exist,
        existing items are replaced.
        """
        self.subtitle_format.update(format_dict)
            
    def update_scope_format(self, format_dict):
        """
        Update the `scope_format` attribute. Where keys already exist, existing
        items are replaced.
        """
        self.scope_format.update(format_dict)
        
    def update_location_format(self, format_dict):
        """
        Update the `location_format` attribute. Where keys already exist,
        existing items are replaced.
        """
        self.location_format.update(format_dict)
        
        
    def update_unit_format(self, format_dict):
        """
        Update the `unit_format` attribute. Where keys already exist, existing
        items are replaced.
        """
        self.unit_format.update(format_dict)

    def update_source_format(self, format_dict):
        """
        Update the `source_format` attribute. Where keys already exist,
        existing items are replaced.
        """
        self.source_format.update(format_dict)
    
    def update_legend_format(self, format_dict):
        """
        Update the `legend_format` attribute. Where keys already exist,
        existing items are replaced.
        """
        self.legend_format.update(format_dict)
    
    def update_note_format(self, format_dict):
        """
        Update the `note_format` attribute. Where keys already exist, existing
        items are replaced.
        """
        self.note_format.update(format_dict)
    
    def print_formats(self):
        """
        Print all current format attributes and values to the console.
        """
        obj_attr = [attr for attr in self.__dir__() if not attr.startswith('__') and not callable(getattr(self, attr))]
        for attr in obj_attr:
            print(attr, ":", getattr(self, attr))
        
    