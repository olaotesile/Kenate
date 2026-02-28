from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext
import os
import sys

# READ README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

class PybindBuildExt(build_ext):
    """A custom build extension for pybind11."""
    def build_extensions(self):
        # Add compiler flags here if needed
        for ext in self.extensions:
            ext.include_dirs.append("include")
            # In a real pybind11 setup, we would use get_include()
            # For now, we assume the environment has pybind11 installed
        super().build_extensions()

class get_pybind_include(object):
    """Helper class to determine the pybind11 include path
    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the `get_include()`
    method can be invoked. """

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)

setup(
    name="kenate",
    version="1.0.6",
    author="Euretix Labs",
    author_email="founder@euretix.io",
    description="Professional C++/Python Robotics Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/euretix/kenate",
    packages=find_packages(where="python"),
    package_dir={"": "python"},
    ext_modules=[
        Extension(
            "kenate.bindings",
            ["python/bindings.cpp"],
            include_dirs=[
                "include",
                # The include path for pybind11
                str(get_pybind_include()),
                str(get_pybind_include(user=True))
            ],
            language='c++'
        ),
    ],
    install_requires=[
        "pybind11>=2.6.0",
    ],
    cmdclass={
        'build_ext': PybindBuildExt
    },
    package_data={
        'kenate': ['templates/*'],
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'kenate=kenate.cli:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Development Status :: 4 - Beta",
    ],
    python_requires='>=3.7',
)
