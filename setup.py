import setuptools
from version import version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="asos",
    version=version,
    author="Pavel Kim",
    author_email="hello@pavelkim.ru",
    description="A scheduler of stuff (ASOS)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/python-asos/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)