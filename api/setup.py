from setuptools import setup, find_packages

with open("requirements.txt") as f:
    REQUIREMENTS = f.read().split("\n")

setup(
    name="nivo_api",
    version="0.1",
    description="API to serve snow opendata from meteofrance",
    author="Remi Desgrange",
    author_email="remi+nivo@desgran.ge",
    url="https://nivo.desgran.ge",
    packages=find_packages(),
    install_requires=REQUIREMENTS,
)
