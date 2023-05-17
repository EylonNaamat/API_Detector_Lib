from setuptools import setup, find_packages
import glob
import os

setup(
    name='API_Detector_Package',
    version='0.0.2',
    description='A library for API detection layer',
    author='Eylon Naamat & Michael Matveev',
    packages=find_packages(),
    data_files=[('rules', [f for f in glob.glob('API_Detector_Package/rules/**/*.*', recursive=True) if os.path.isfile(f)])]
)
