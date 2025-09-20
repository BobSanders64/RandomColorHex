from pathlib import Path
from setuptools import setup, find_packages

README=Path(__file__).with_name("README.txt")
long_description=README.read_text(encoding="utf-8")

setup(
    name="random_color_hex",
    version="1.0.9",
    author="Nathan Honn",
    author_email="randomhexman@gmail.com",
    description="Generate random CSS-style hex colors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BobSanders64/RandomColorHex",
    packages=find_packages(),
    license="Unlicense",
    license_files=("LICENSE.txt",),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.13.2",
)
