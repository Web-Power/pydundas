import re
import setuptools

from pydundas import __version__ as pydundas_ver

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    # 1) All lines in requirements .txt...
    y for y in
    # 3) .. after removing comments and whitespaces.
    [re.sub(r'\s*#.*', '', x).strip() for x in open('requirements.txt').readlines()]
    # 2) ... which are not empty...
    if y
]

setuptools.setup(
    name='pydundas',
    version=pydundas_ver,
    license='MIT',
    author="Guillaume Roger",
    author_email="datatech@webpower.nl",
    description="Python interface to Dundas rest api.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Web-Power/pydundas",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )
