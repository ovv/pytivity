#!/usr/bin/env python
import codecs
from pathlib import Path
from setuptools import setup, convert_path


def parse_readme():
    """Parse contents of the README."""
    readme_file = str(Path(__file__).parent / 'README.md')
    with codecs.open(readme_file, encoding='utf-8') as handle:
        long_description = handle.read()
    return long_description


def load_package_meta():
    meta_path = convert_path('./pytivity/__meta__.py')
    meta_ns = {}
    with open(meta_path) as f:
        exec(f.read(), meta_ns)
    return meta_ns['METADATA']


PKG_META = load_package_meta()

setup(
    keywords=[
        'kde',
        'activity',
    ],
    packages=[
        'pytivity',
    ],
    entry_points={
        'console_scripts': [
            'pytivity=pytivity.cli:main'
        ]
    },
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'terminaltables',
        'xdg',
        'pydbus'
    ],
    tests_require=[
        'flake8'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Environment :: Console',
    ],
    author=PKG_META['author'],
    author_email=PKG_META['author_email'],
    description=PKG_META['description'],
    long_description=parse_readme(),
    license=PKG_META['license'],
    name=PKG_META['name'],
    url=PKG_META['url'],
    version=PKG_META['version'],
)
