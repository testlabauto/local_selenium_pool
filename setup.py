from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="local_selenium_pool",
    version="0.0.1",
    description="Concurrent local selenium execution using multiprocessing_on_dill",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author_email="chris@testlabauto.com",
    author="Test Lab Automation",
    license="Apache License Version 2.0",
    url="https://github.com/testlabauto/local_selenium_pool",
    keywords=["Selenium", "Local", "Concurrent"],
    install_requires=['selenium', 'attr', 'setuptools', 'multiprocessing_on_dill'],
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        "Development Status :: 1 - Beta",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
)