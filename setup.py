from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()
    
setup(
    name='gptables',
    version='0.1.0',
    author='David Foster',
    description='Simplifying good practice in statistical tables.',
    data_files=[
            ("examples", [
                    "addn_files/examples/iris.py",
                    "addn_files/examples/iris.csv"
                    ]),
            ("themes", ["addn_files/themes/gptheme.yaml"])
            ],
    packages=find_packages(),
    install_requires=required
)
