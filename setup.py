from setuptools import setup
import os

def load(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name="sregex",
    version="0.1",
    description="Structural Regular Expressions in Python",
    long_description=load('README.txt'),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
        ],
    keywords='regex structured regular expression',
    author='Joe Gregorio',
    author_email='joe@bitworking.org',
    url='http://sregex.googlecode.com',
    license='Apache Software License (v2)',
    packages=['sregex'],
    )

