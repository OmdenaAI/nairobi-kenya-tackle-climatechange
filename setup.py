from setuptools import find_packages, setup
from typing import List

REQUIREMENT_FILE_NAME = "requirements.txt"
HYPHEN_E_DOT = "-e ."


# List[str] is just to tell the user that this particular function will return the list of strings
def get_requirements() -> List[str]:
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirement_list = requirement_file.readlines()
    requirement_list = [requirement_name.replace("\n", "") for requirement_name in requirement_list]

    if HYPHEN_E_DOT in requirement_list:
        requirement_list.remove(HYPHEN_E_DOT)
    return requirement_list


setup(
    name='OCO2',
    version='1.0.0',
    author='dhananjai14',
    author_email='dhananjai.eee@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()
)
