from xlsxwriter.format import Format
import yaml

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
    
    Attributes
    ----------
    title_format : dict

    subtitle_format : dict
    
    scope_format : dict
    
    units_format : dict

    column_heading_format : dict
    
    index_1_format : dict
    
    index_2_format : dict
    
    index_3_format : dict
    
    data_format : dict

    source_format : dict
    
    legend_format : dict
    
    annotations_format : dict
    
    notes_format : dict
    
    footer_order : list
    
    missing_value : None or str
    
    Returns
    -------
        None
    """

    def __init__(
            self,
            config=None,
            ):
        """
        Initialise theme object
        """
        ## Formats
        self._format_attributes = [
            "title_format",
            "subtitle_format",
            "scope_format",
            "units_format",
            "column_heading_format",
            "index_1_format",
            "index_2_format",
            "index_3_format",
            "data_format",
            "source_format",
            "legend_format",
            "annotations_format",
            "notes_format"
            ]
        
        for attr in self._format_attributes:
            setattr(self, attr, {})
        
        ## Other attributes
        self.footer_order = []
        self.missing_value = None
        
        # TODO: Dynamically generate update method for each format attr to
        # avoid rep and increase extensibility
            
        if config:
            self.apply_config(config)
    
    @staticmethod
    def _parse_config(config):
        """
        Parse yaml configuration to dictionary.
        """
        if isinstance(config, str):
            if not config.endswith((".yml", ".yaml")):
                raise ValueError("Theme configuration files must be YAML")
            with open(config, "r") as file:
                cfg = yaml.safe_load(file)
                
        elif isinstance(config, dict):
            cfg = config
            
        else:
            raise ValueError("Theme configuration must be a dict or YAML file")
            
        return cfg

    def _validate_config(self, config):
        
        valid_attrs = [
                x.replace("_format", "")
                for x in self._format_attributes
                ] + [
                    "global"
                    ]
        
        valid_formats = [
                attr.replace("set_", "")
                for attr in Format().__dir__() 
                if attr.startswith('set_')
                and callable(getattr(Format(), attr))
                ]
        
        for attr in config.keys():
            if attr in valid_attrs:
                attr_config = config[attr] or {}
                for fmt in attr_config.keys():
                    if fmt not in valid_formats:
                        raise ValueError(f"{fmt} not a valid format attribute")
            elif attr not in ["footer_order", "missing_value"]:
                raise ValueError(f"{attr} not a valid config attribute")
    
    def apply_config(self, config):
        """
        Update multiple Theme attributes using a YAML or dictionary config.
        This enables extension of build in Themes.
        """
        cfg = self._parse_config(config)
        self._validate_config(cfg)
        
        # Update all when global used
        if "global" in cfg.keys():
            default_format = cfg.pop("global")
            self.update_all_formats(default_format)
        
        # Update with individual methods
        for key, value in cfg.items():
            if key in ["footer_order", "missing_value"]:
                getattr(self, "update_" + key)(value)
            elif value is not None:
                getattr(self, "update_" + key + "_format")(value)
    
    def update_all_formats(self, global_dict):
        """
        Updates all theme attributes with a global format dictionary.
        """
        obj_attr = [
                attr for attr in self.__dir__()
                if not attr.startswith('__')
                and not callable(getattr(self, attr))
                ]
        for attr in obj_attr:
            if attr.endswith("_format"):
                getattr(self, "update_" + str(attr))(global_dict)
        
            
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

    def update_data_format(self, format_dict):
        """
        Update the `data_format` attribute. Where keys already exist,
        existing items are replaced.
        """
        self.data_format.update(format_dict)
    
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
        
        
    def update_units_format(self, format_dict):
        """
        Update the `units_format` attribute. Where keys already exist, existing
        items are replaced.
        """
        self.units_format.update(format_dict)

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
    
    def update_annotations_format(self, format_dict):
        """
        Update the `annotations_format` attribute. Where keys already exist,
        existing items are replaced.
        """
        self.annotations_format.update(format_dict)

    def update_notes_format(self, format_dict):
        """
        Update the `notes_format` attribute. Where keys already exist, existing
        items are replaced.
        """
        self.notes_format.update(format_dict)
        
    def update_footer_order(self, order_list):
        """
        Update the `footer_order` attribute. Overrides existing order.
        """
        self.footer_order = order_list

    def update_missing_value(self, string):
        """
        Update the `missing_value` attribute. Overrides existing string.
        """
        if not isinstance(string, str):
            raise ValueError("Missing value representation must be a string.")
        self.missing_value = string

    def print_attributes(self):
        """
        Print all current format attributes and values to the console.
        """
        obj_attr = [
                attr for attr in self.__dir__()
                if not attr.startswith('__')
                and not callable(getattr(self, attr))
                ]
        for attr in obj_attr:
            print(attr, ":", getattr(self, attr))
        
    