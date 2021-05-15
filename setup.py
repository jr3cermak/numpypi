from setuptools import find_packages, setup
import numpypi

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="numpypi",
    version=numpypi.__version__,
    author="Alistair Adcroft",
    author_email="alistair.adcroft@noaa.gov",
    maintainer="Rob Cermak",
    maintainer_email="rob.cermak@gmail.com",
    description="Portable intrinsics for numpy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adcroft/numpypi",
    project_urls={
        "Bug Tracker": "https://github.com/adcroft/numpypi/issues",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
    ],
    packages=find_packages(exclude=['notebooks','tests']),
    python_requires=">=3.6",
    install_requires=['numpy'],
)
