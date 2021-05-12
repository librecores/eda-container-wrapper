from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='eda-container-wrapper',
    description="Synchronize ICS to Exchange",
    packages=["edacontainerwrapper"],
    use_scm_version={
        "relative_to": __file__,
        "write_to": "edacontainerwrapper/version.py",
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/librecores/eda-container-wrapper',
    author="Stefan Wallentowitz",
    author_email='stefan.wallentowitz@hm.edu',
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Topic :: Utilities",
    ],
    entry_points={"console_scripts": ["eda-container-wrapper = edacontainerwrapper.main:main"]},
    setup_requires=[
        "setuptools_scm",
    ],
    install_requires=[
    ]
)
