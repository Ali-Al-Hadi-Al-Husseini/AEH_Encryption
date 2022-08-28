from setuptools import setup
from Cython.Build import cythonize

# file_name = input("file name: ")

setup(
    ext_modules=cythonize("ency.pyx")
)