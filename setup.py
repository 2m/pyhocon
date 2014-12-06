#!/usr/bin/env python

from setuptools import setup

setup(
    name='pyhocon',
    version='0.1.0',
    description='HOCON parser',
    keywords='hocon parser',
    license='Apache License 2.0',
    author="Francois Dang Ngoc",
    author_email='francois.dangngoc@gmail.com',
    url='http://github.com/chimpler/pyhocon/',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=[
        'pyhocon',
    ],
    install_requires=[
        'pyparsing==2.0.3'
    ],
)