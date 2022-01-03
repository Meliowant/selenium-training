import os
from setuptools import setup


setup(
    name="Selenium WebDriver demo",
    version="0.0.1",
    description="A set of test cases as my training on Selenium usage",
    author="Andrii Borovyi",
    author_email="andrii.borovyi@gmail.com",
    packages=["selenium_demo"],
    url="https://github.com/Meliowant/selenium_demo_2021",
    install_requires=[
        "selenium",
        "pytest",
        "black",
        "flake8",
        "pylint",
        "coverage"
    ]
)
