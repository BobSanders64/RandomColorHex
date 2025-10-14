from pathlib import Path
from setuptools import setup, find_packages

README=Path(__file__).with_name("README.txt")
long_description=README.read_text(encoding="utf-8")

setup(
    name="random_color_hex",
    version="2.1.4",
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
        #Language/OS
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",

        #Free-threading (PEP 703+)
        "Programming Language :: Python :: Free Threading",
        "Programming Language :: Python :: Free Threading :: 4 - Resilient",

        #Maturity
        "Development Status :: 5 - Production/Stable",

        #Audiance
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Science/Research",

        #What it can be used for (topics)
        "Topic :: Games/Entertainment",
        "Topic :: Multimedia",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Scientific/Engineering",

        #What its designed (but not required) to be used with (ecosystem)
        "Framework :: Matplotlib",
    ],
    python_requires=">=3.11.0",
)



