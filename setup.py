from setuptools import setup, find_packages
from typing import List

HYPHEN_e_DOT = '-e .'

def get_requirements (file_path: str) -> List[str]:
    '''This function returns the list of requirements'''
    requirements = list()
    with open(file_path) as f:
        requirements = f.readlines()
        requirements = [req.replace('\n', '') for req in requirements]

        if HYPHEN_e_DOT in requirements:
            requirements.remove(HYPHEN_e_DOT)
    return requirements

setup(
    name='Data-Cleaner',
    version='0.1',
    author='Gaurav',
    author_email='gsr094@gmail.com',
    packages=find_packages(),
    requires=get_requirements('requirements.txt')

)