from setuptools import setup, find_packages

setup(
    name='API_Detector_Package',
    version='0.0.2',
    description='A library for API detection layer',
    author='Eylon Naamat & Michael Matveev',
    packages=find_packages(),
    install_requires=[
        'requests',
        'colorlog'
    ]
)
