from setuptools import setup, find_packages

setup(
    name='enviroments_package',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        "numpy",
        "gymnasium"
    ]
)
