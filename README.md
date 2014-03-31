scons-gnu-build
===============

[![Build Status](https://travis-ci.org/ptomulik/scons-gnu-build.png?branch=master)](https://travis-ci.org/ptomulik/scons-gnu-build)

Welcome to ``scons-gnu-build``.

The ``scons-gnu-build`` extension makes ``SCons`` behaving more like GNU
build system (autotools based). The purpose is to achieve better
interoperability with several external tools (especially external packaging
tools, e.g. debian's dh) that normally use GNU build system.

CURRENT STATUS
--------------

It's the very beginning.

  * implemented ``GVar`` variables to glue construction variables, command-line
    variables and command-line options; GNU directory variables currently use
    them
  * implemented GNU directory variables (available as SCons command line flags
    or variable and also via SCons Environment)
  * initially implemented automake-like uniform naming,

comming soon:

  * project configuration,
  * package definition format,
  * installation of defined packages,

INSTALLATION
------------

There are two method for installation:

### Installation by simple copy

Copy recursively the entire directory ``SConsGnu`` to your
``site_scons/`` directory

    cp -r scons-gnu-build/SConsGnu your/projects/site_scons/

### Installation as a submodule in git-based projects

Add the repository as a submodule to your project

```shell
git submodule add git://github.com/ptomulik/scons-gnu-build.git 3rd/scons-gnu-build
```

In your `site_scons/site_init.py` add the following lines:

```python
# site_scons/site_init.py
import sys
sys.path.append(Dir('#3rd/scons-gnu-build').abspath)
```

DOCUMENTATION
-------------

### API documentation

API documentation can be generated from the top level directory with the
following command (see also requirements below)

```shell
scons api-doc
```

The generated documentation is located within ``build/doc/api`` directory.

#### Requirements for api-doc

To generate API documentation, you may need following packages on your system:

  * epydoc <http://epydoc.sourceforge.net/>
  * python-docutils <http://pypi.python.org/pypi/docutils>
  * python-pygments <http://pygments.org/>


### User documentation

User documentation can be generated from the top level directory with the
following command (see also requirements below)

```shell
scons user-doc
```
The generated documentation is located in ``build/doc/user``.

#### Requirements for user-doc

To generate user's documentation, you'll need following packages on your
system:

  * docbook5-xml <http://www.oasis-open.org/docbook/xml/>
  * xsltproc <ftp://xmlsoft.org/libxslt/>
  * imagemagick <http://www.imagemagick.org/>

You also must install locally the SCons docbook tool by Dirk Baechle:

  * scons docbook tool <https://bitbucket.org/dirkbaechle/scons_docbook/>

this is easilly done by running the following bash script

```
bin/download-devel-deps.sh
```

from the top level directory.


TESTING
-------

We provide unit tests and end-to-end tests.

### Running unit tests

To run unit tests type

```shell
scons unit-test
```

### Requirements for unit tests

  * python-unittest2 <https://pypi.python.org/pypi/unittest2>
  * python-mock <https://pypi.python.org/pypi/mock>

On Debian install them with:

```shell
apt-get install python-unittest2 python-mock
```

### Running end-to-end tests

To run end-to-end tests, type

```shell
SCONS_EXTERNAL_TEST=1 python runtest.py -a
```

### Requirements for end-to-end tests

  * SCons testing framework

Download the SCons testing framework with:

```shell
./bin/download-test-framework.sh
```

or

```shell
./bin/download-deps.sh
```

LICENSE
-------

Copyright (c) 2014 by Pawel Tomulik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE
