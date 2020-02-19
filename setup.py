from setuptools import setup, find_packages
from distutils.command.develop import develop
from distutils.command.install import install
import pickle

with open('requirements.txt') as f:
    required = f.read().splitlines()


class PostInstall(install):
    @staticmethod
    def pickle_gptheme():
        import gptables
        theme = gptables.Theme("./themes/gptheme.yaml")
        pickle.dump(theme, open("./gptables/themes/gptheme.pickle", "wb"))

    def run(self):
        install.run(self)
        
        #Post install actions
        self.pickle_gptheme()
        
class PostInstallDev(develop):
    @staticmethod
    def pickle_gptheme():
        import gptables
        theme = gptables.Theme("./themes/gptheme.yaml")
        pickle.dump(theme, open("./gptables/themes/gptheme.pickle", "wb"))

    def run(self):
        install.run(self)
        
        #Post install actions
        self.pickle_gptheme()

setup(
    name='gptables',
    version='0.1.0',
    author='David Foster',
    description='Simplifying good practice in statistical tables.',
    data_files=[
            ("examples", ["addn_files/demos/iris.py", "addn_files/demos/iris.csv"]),
            ("themes", ["addn_files/themes/gptheme.yaml"])
            ],
    cmdclass={
        'develop': PostInstallDev,
        'install': PostInstall,
    },
    packages=find_packages(),
    install_requires=required
)
