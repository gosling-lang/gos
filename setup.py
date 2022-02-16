#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

data_server_requirements = [
    'portpicker',
    'uvicorn',
    'starlette',
]

setuptools.setup(
    name="gosling",
    version="0.0.7",
    author="Trevor Manz",
    author_email="trevor.j.manz@gmail.com",
    description="Python bindings to generate Gosling schema.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gosling-lang/gos",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "jsonschema>=3.0,<4.0",
        "jinja2",
        "numpy",
        "pandas>=0.18",
    ] + data_server_requirements,
    extras_require={
        'dev': [
            'pytest',
            'requests',
            'sphinx',
            'numpydoc',
            'furo',
        ],
    },
    entry_points={},
)
