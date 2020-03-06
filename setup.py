from setuptools import setup, find_packages

def read_requirements(file):
    with open(file) as f:
        return f.read().splitlines()

def read_file(file):
   with open(file) as f:
        return f.read()
    
long_description = read_file("README.rst")
version = read_file("VERSION")
license_contents = read_file("LICENSE")
required = read_requirements("requirements.txt")

setup(
    name = 'gptables',
    version = version,
    author = 'David Foster',
    author_email = 'david.foster@ons.gov.uk',
    url = 'https://best-practice-and-impact.github.io/gptables/',
    description = 'Simplifying good practice in statistical tables.',
    long_description = long_description,
    license = license_contents,
    packages = find_packages(exclude=["test"]),
    include_package_data = True,
    install_requires = required,
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires = '>=3.6',
)
