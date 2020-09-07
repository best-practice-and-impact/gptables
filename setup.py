from setuptools import setup, find_packages

def read_requirements(file):
    with open(file) as f:
        return f.read().splitlines()

def read_file(file):
   with open(file) as f:
        return f.read()
    
long_description = read_file("README.rst")
version = read_file("VERSION")
requires = read_requirements("requirements.txt")

docs_requires = [
    "sphinx>=2",
    "sphinx_rtd_theme"
    ] + requires

test_requires = [
    "coverage",
    "pytest>=3.6,<4",
    "pytest-cov"
] + docs_requires

setup(
    name = 'gptables',
    version = version,
    author = 'David Foster',
    author_email = 'david.foster@ons.gov.uk',
    url = 'https://best-practice-and-impact.github.io/gptables/',
    keywords="reproducible tables excel xlsxwriter reproducible-analytical-pipelines",
    description = 'Simplifying good practice in statistical tables.',
    long_description_content_type = "text/x-rst",
    long_description = long_description,
    license = "MIT license",
    packages = find_packages(exclude=["test"]),
    include_package_data = True,
    install_requires = requires,
    extras_require = {
        "docs": docs_requires,
        "testing": test_requires
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires = '>=3.6',
)
