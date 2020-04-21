from setuptools import setup
import sys
import json


with open('metadata.json', encoding='utf-8') as fp:
    metadata = json.load(fp)


setup(
    name='lexibank_wanghmongmien',
    description=metadata['title'],
    license=metadata.get('license', ''),
    url=metadata.get('url', ''),
    py_modules=['lexibank_wanghmongmien'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'lexibank.dataset': [
            'wanghmongmien=lexibank_wanghmongmien:Dataset',
        ],
        'cldfbench.commands': [
            'wanghmongmien=wanghmongmiencommands',
        ],
    },
    install_requires=[
        'pylexibank>=1.1.1',
    ],
    extras_require={"test": ["pytest-cldf"]},

)
