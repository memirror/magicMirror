# -*- coding: utf-8 -*-
# @Author: xiaodong
# @Date  : 2021/6/4

from setuptools import setup, find_packages


def long_description():
    with open("README.md", encoding="utf-8") as desc:
        description = desc.read()
    return description


with open("requirements/base.txt") as file:
    requirements = [
        obj.strip() for obj in file.readlines() if obj.strip()
    ]

setup(
    name="magicmirror",
    version="0.1.2",
    description="A Simple Automatic Question and Answering System",
    long_description=long_description(),
    url="https://github.com/memirror/magicMirror",
    author="xiaodong",
    author_email="xiaodongliang@outlook.com",
    data_files=[
            ("config", [
                "magicmirror/config/default.cfg",
                "magicmirror/config/universal.cfg",
                "magicmirror/config/realtimesearch.yaml",
                "magicmirror/config/elasticsearch.yaml",
            ]),
        ],
    package_data={
        "": [
            "requirements/base.txt",
        ],
    },
    packages=find_packages(),
    include_package_data=False,
    install_requires=requirements,
    entry_points={
            "console_scripts": [
                "magicmirror = magicmirror.runme:main",
            ],
        },
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities",
    ],
    keywords="auto question&answer autoQA QA Q&A",
)
