#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ["Jinja2"]

test_requirements = []

setup(
    author="Tuan-Phong Nguyen",
    author_email='tuanphong94@gmail.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    description="A TestRunner for use with the Python unittest framework, which generates report in nice HTML files.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords=['html_reporter', 'unittest', 'testrunner',
              'html-reporter', 'html-test-runner', 'htmltestrunner'],
    name='html_reporter',
    packages=find_packages(include=['html_reporter', 'html_reporter.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/phongnt570/html-reporter',
    version='0.2.6',
    zip_safe=False,
)
