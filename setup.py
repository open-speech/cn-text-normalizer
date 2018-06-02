import setuptools

version = int(setuptools.__version__.split('.')[0])
assert version > 30, "installation requires setuptools > 30"
from setuptools import setup
import os
import shutil

# produce rst readme for pypipst
try:
    import pypandoc

    long_description = pypandoc.convert_file('README.md', 'rst')
except ImportError:
    long_description = open('README.md').read()


setup(
    name='cntn',
    version='0.0.1',
    description='Convert chinese written string to read string',
    long_description=long_description,
    keywords='cntn',
    # url='http://github.com/...',
    author='Meixu Song',
    author_email='meixu.asr@gmail.com',
    license='MIT',
    packages=['cntn'],
    zip_safe=False
)
