from setuptools import setup,find_packages
from typing import List


HYPENH_E_DOT = '-e .'
def get_requirements(file_name:str)-> List[str]:
    """
    This funtion will return a list of libraries waht we need  
    """
    requirements = [] 
    with open(file_name) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace('\n','') for req in requirements]
        if HYPENH_E_DOT in requirements :
            requirements.remove(HYPENH_E_DOT)
    return requirements


setup(
name='NetworkSecurity',
author='Gad Amr',
author_email='gadelhaq.work@gmail.com',
version='0.0.1',
packages=find_packages(),
install_requires=get_requirements('requirements.txt')
)