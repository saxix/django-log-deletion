#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import imp
import codecs
from setuptools import setup, find_packages

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))
init = os.path.join(ROOT, 'src', 'log_deletion', '__init__.py')

app = imp.load_source('log_deletion', init)

reqs = 'install.py%d.pip' % sys.version_info[0]


def read(*files):
    content = ''
    for f in files:
        content += codecs.open(os.path.join(ROOT, 'src',
                                            'requirements', f), 'r').read()
    return content


tests_requires = read('testing.pip')
drf_requires = ['djangorestframework']
dev_requires = tests_requires + read('develop.pip')
install_requires = read('install.any.pip', reqs)

readme = codecs.open('README.rst').read()
history = codecs.open('CHANGES.rst').read().replace('.. :changelog:', '')

setup(name=app.NAME,
      version=app.get_version(),
      description="""diango app to log model deletion.""",
      long_description=readme + '\n\n' + history,
      author='Stefano Apostolico',
      author_email='s.apostolico@gmail.com',
      url='https://github.com/saxix/django-log-deletion',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      include_package_data=True,
      install_requires=install_requires,
      tests_require=dev_requires,
      extras_require={
          'dev': dev_requires,
          'tests': tests_requires,
          'drf': drf_requires,
      },
      license="BSD",
      zip_safe=False,
      keywords='django-log-deletion',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Natural Language :: English',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
      ])
