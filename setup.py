from setuptools import setup
import os


def read_readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='cntn',
    version='0.0.2',
    python_requires='>=3.3',
    description='Convert chinese written string to spoken string',
    long_description=read_readme(),
    keywords='cntn',
    url='https://github.com/open-speech/cn-text-normalizer',
    author='Meixu Song',
    author_email='meixu.asr@gmail.com',
    license='MIT',
    packages=['cntn'],
    zip_safe=False
)
