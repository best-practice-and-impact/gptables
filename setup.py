from setuptools import setup, find_packages

def read_requirements(file):
    with open(file) as f:
        return f.read().splitlines()

def read_file(file):
   with open(file) as f:
        return f.read()
    
long_description = read_file("Readme.md")
licence = read_file("./LICENSE")
required = read_requirements("requirements.txt")


setup(
    name='gptables',
    version='0.1.0',
    author='David Foster',
    author_email='david.foster@ons.gov.uk',
    url='https://github.com/best-practice-and-impact/gptables/issues',
    description='Simplifying good practice in statistical tables.',
    long_description=long_description,
    licence=licence,
    packages=find_packages(exclude=["test"]),
    include_package_data=True,
    install_requires=required
)
