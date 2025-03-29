from setuptools import find_packages,setup
from typing import List

def get_requirements(file_path:str)->List[str]: 
    """
    This function will return the list of requirements"
    """
    requirments=[]
    with open(file_path) as file_obj:
        requirments=file_obj.readlines()
        requirments = [req.replace("\n","") for req in requirments]
        if '-e .' in requirments:
            requirments.remove('-e .')
    return requirments

setup(
    name='mlproject',
    version='0.0.1',
    author='Dhiraj Singh',
    author_email='dhirajsingh0673@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
    
)