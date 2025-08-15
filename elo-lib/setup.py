import os
from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "requirements.txt"), "r") as f:
    requirements = f.read().splitlines()

setup(
    name="briefing_docs",
    version="0.1.0",
    description="Library to call ELO api, generate fixture lists and predict final results from ELO ratings",
    packages=find_packages(),
    author="Tom Jeffries",
    author_email="tom_jeffries@outlook.com",
    install_requires=requirements,
)
