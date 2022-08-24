from setuptools import setup, find_packages
from typing import List

PROJECT_NAME="Premium-Predictor"
VERSION="0.0.1"
AUTHOR="Anuj"
DESCRIPTION="This is an app for predicting insurance premium"
PACKAGES=["premium"]
REQUIREMENT_FILE_NAME="requirements.txt"

def get_requirements_list()->List[str]:
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        return requirement_file.readlines().remove("-e .")


setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    package=find_packages(),
    install_requires=get_requirements_list()
)