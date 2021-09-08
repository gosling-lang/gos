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
    version="0.0.4",
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
        "jsonschema",
        "jinja2",
        "numpy",
        "pandas>=0.18",
    ],
    extras_require={
        'all': data_server_requirements,
        'dev': data_server_requirements + [
            'pytest',
            'requests',
            'ipywidgets',
            'sphinx',
            'numpydoc',
            'furo',
        ],
    },
    entry_points={},
)
