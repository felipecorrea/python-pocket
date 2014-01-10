#!/usr/bin/env python
#
# vim: sw=4 ts=4 st=4
#
#  Copyright 2013 Felipe Borges <felipe10borges@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = 'felipe10borges@gmail.com'
__version__ = '0.1'

METADATA = dict(
    name = "python-getpocket",
    version = __version__,
    py_modules = ['getpocket'],
    author = 'Felipe Borges',
    author_email = 'felipe10borges@gmail.com',
    description = 'A Python wrapper around the Pocket API.',
    license = 'Apache License 2.0',
    url = 'https://github.com/felipeborges/python-getpocket',
    keywords = 'getpocket pocket api',
)

SETUPTOOLS_METADATA = dict(
    install_requires = ['setuptools', 'simplejson'],
    include_package_data = True,
)

def build_long_description():
    return '\n'.join([open('README.md').read(), open('CHANGES').read()])

if __name__ == '__main__':
    METADATA['long_description'] = build_long_description()

    # Use setuptools if available, otherwise fallback and use distutils
    try:
        import setuptools
        METADATA.update(SETUPTOOLS_METADATA)
        setuptools.setup(**METADATA)
    except ImportError:
        print "Could not import setuptools, using distutils"
        print "NOTE: You will need to install dependencies manualy" 
        import distutils.core
        distutils.core.setup(**METADATA)
