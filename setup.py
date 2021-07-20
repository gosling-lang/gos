#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gosling",
    version="0.0.0",
    author="Trevor Manz",
    author_email="trevor.j.manz@gmail.com",
    description="Python bindings to generate gosling schema.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manzt/goslingpy-experimental",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.9",
    install_requires=[],
    entry_points={},
)
