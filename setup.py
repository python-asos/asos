import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="asos",
    version="1.0.0",
    author="Pavel Kim",
    author_email="hello@pavelkim.ru",
    description="A scheduler of stuff (ASOS)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pavelkim/asos",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)