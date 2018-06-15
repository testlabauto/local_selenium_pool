from setuptools import setup


# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

EXTRAS = {}
REQUIRES = []
with open('requirements.txt') as f:
    for line in f:
        line, _, _ = line.partition('#')
        line = line.strip()
        if ';' in line:
            requirement, _, specifier = line.partition(';')
            for_specifier = EXTRAS.setdefault(':{}'.format(specifier), [])
            for_specifier.append(requirement)
        else:
            REQUIRES.append(line)

with open('test-requirements.txt') as f:
    TESTS_REQUIRES = f.readlines()

setup(
    name="selenium_gevent",
    version="1.0",
    description="Concurrent selenium with gevent",
    author_email="",
    author="Test Lab Automation",
    license="Apache License Version 2.0",
    url="https://github.com/testlabauto/selenium-gevent",
    keywords=["Swagger", "OpenAPI", "Kubernetes"],
    install_requires=REQUIRES,
    tests_require=TESTS_REQUIRES,
    extras_require=EXTRAS,
    packages=['kubernetes', 'kubernetes.client', 'kubernetes.config',
              'kubernetes.watch', 'kubernetes.client.apis',
              'kubernetes.stream', 'kubernetes.client.models'],
    include_package_data=True,
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
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)