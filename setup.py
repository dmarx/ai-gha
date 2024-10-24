from setuptools import setup, find_packages

setup(
    name="readme-generator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "jinja2",
        "tomli",
    ],
)
