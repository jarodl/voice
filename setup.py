#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

tests_require = [
    'Django>=1.3.1',
]

setup(
    name='Voice',
    version='0.1.0',
    author='Jarod Luebbert',
    author_email='jarodluebbert@gmail.com',
    url='http://github.com/jarodl/voice',
    description='A voting app for letting users request features.',
    packages=find_packages(exclude=("example_project",)),
    zip_safe=False,
    install_requires=[
        'Django>=1.3.1',
        'South',
        ],
    tests_require=tests_require,
    extras_require={'test':tests_require},
    test_suite = 'nose.collector',
    include_package_data=True,
    classifiers=[
      'Framework :: Django',
      'Intended Audience :: Developers',
      'Intended Audience :: End Users/Desktop',
      'Operating System :: OS Independent',
    ],
)
