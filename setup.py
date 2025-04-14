from setuptools import setup, find_packages

setup(
    name="zoo_project",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.115.12",
        "pytest==8.3.4",
        "pytest-cov==5.0.0",
        "uvicorn==0.34.0"
    ],
)