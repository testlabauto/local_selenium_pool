from setuptools import setup, find_packages


setup(
    name="local_selenium_pool",
    version="1.0",
    description="Concurrent local selenium execution using multiprocessing_on_dill",
    author_email="chris@testlabauto.com",
    author="Test Lab Automation",
    license="Apache License Version 2.0",
    url="https://github.com/testlabauto/local_selenium_pool",
    keywords=["Selenium", "Parallel", "Concurrent"],
    install_requires=['selenium', 'attr', 'setuptools', 'multiprocessing_on_dill'],
    packages=find_packages(),
    zip_safe=False,
    long_description="""\
    Python library for concurrent selenium testing
    """,
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