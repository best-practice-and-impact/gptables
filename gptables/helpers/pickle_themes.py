import gptables.core.theme
import pickle
import glob
from os.path import abspath, dirname, join, basename, splitext

def pickle_themes():
    package_dir = dirname(dirname(dirname(abspath(__file__))))
    theme_configs = glob.glob(join(
            package_dir,
            "gptables",
            "theme_configs",
            "*.yaml")
    )

    pickled_output_dir = join(package_dir, "gptables", "themes")

    for cfg in theme_configs:
        file, ext = splitext(basename(cfg))
        out_file = join(pickled_output_dir, (file + ".pickle"))

        theme = gptables.core.theme.Theme(cfg)

        pickle.dump(
            theme,
            open(out_file, "wb")
            )

if __name__ == "__main__":
    pickle_themes()