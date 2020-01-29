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
        if isinstance(config, str):
            if not config.endswith((".yml", ".yaml")):
                raise ValueError("Theme configuration files must be YAML")
            with config.open() as file:
                cfg = yaml.safe_load(file)
        elif isinstance(config, dict):
            cfg = config
        
        if "global" in cfg.keys():
            default_format = cfg.pop("global")
        else:
            default_format = {}
        
        self.table_format = default_format

        self.title_format = default_format
        self.subtitle_format = default_format
        self.demographic_format = default_format
        self.location_format = default_format
        self.unit_format = default_format

        self.source_format = default_format
        self.legend_format = default_format
        self.note_format = default_format

        # Set attributes using methods
        for key, value in cfg.items():
            getattr(self, "update_" + key + "_format")(value)

    def update_table_format(self, format_dict):
        """
        Update the `table_format` attribute. Where keys already exist, existing
        items are replaced.
        """
        self.table_format.update(format_dict)
    
    def update_title_format(self, format_dict):
        """
        Update the `title_format` attribute. Where keys already exist, existing
        items are replaced..
        """
        self.title_format.update(format_dict)
    
    def update_subtitle_format(self, format_dict):
        """
        Update the `subtitle_format` attribute. Where keys already exist, existing
        items are replaced.
        """
        self.subtitle_format.update(format_dict)
            
    def update_demographic_format(self, format_dict):
        """
        Update the `demographic_format` attribute. Where keys already exist, existing
        items are replaced.
        """
        self.demographic_format.update(format_dict)
        
    def update_location_format(self, format_dict):
        """
        Update the `location_format` attribute. Where keys already exist, existing
        items are replaced.
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
        Update the `source_format` attribute. Where keys already exist, existing
        items are replaced.
        """
        self.source_format.update(format_dict)
    
    def update_legend_format(self, format_dict):
        """
        Update the `legend_format` attribute. Where keys already exist, existing
        items are replaced.
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
        attributes = [a for a in self.__dir__() if not a.startswith('__')]
        for attr in attributes:
            print(attr, getattr(Theme, attr))
        
    