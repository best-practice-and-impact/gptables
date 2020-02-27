import pickle
from pkg_resources import resource_filename

class ThemeUnpickler(pickle.Unpickler):
    """
    Points the unpickler to the Theme class. Allows unpickling for package
    init.
    """
    def find_class(self, module, name):
        if name =="Theme":
            from gptables.core.theme import Theme
            return Theme
        return super().find_class(module, name)

gptheme = ThemeUnpickler(
        open(
            resource_filename("gptables", "/themes/gptheme.pickle"),
            "rb"
            )
        ).load()