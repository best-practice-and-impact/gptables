import os
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()
    
setup(
    name='gptables',
    version='0.1.0',
    author='David Foster',
    description='A wrapper for xlsxwriter, to write statistical tables for publication.',
    packages=find_packages(),    
    install_requires=required
)