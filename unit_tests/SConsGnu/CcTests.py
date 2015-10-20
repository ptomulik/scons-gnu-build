""" SConsGnu.Cc

Unit tests for SConsGnu.Cc
"""

__docformat__ = "restructuredText"

#
# Copyright (c) 2012-2015 by Pawel Tomulik
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

import unittest

from SConsGnu import Cc
import re
import os
import platform
import SCons.Environment

class TestCase(unittest.TestCase):
    def test__cc_re_dict__gcc(self):
        # cc
        self.assertTrue(re.match(Cc._cc_re_dict['gcc'], 'cc'))
        self.assertTrue(re.match(Cc._cc_re_dict['gcc'], 'cc-4.6'))
        self.assertTrue(re.match(Cc._cc_re_dict['gcc'], 'cc-52.83'))
        self.assertTrue(re.match(Cc._cc_re_dict['gcc'], 'avr-cc'))
        self.assertTrue(re.match(Cc._cc_re_dict['gcc'], 'avr-cc-4.6'))
        self.assertTrue(re.match(Cc._cc_re_dict['gcc'], 'avr-cc-52.83'))
        self.assertTrue(re.match(Cc._cc_re_dict['gcc'], 'arm-none-eabi-cc'))
        self.assertTrue(re.match(Cc._cc_re_dict['gcc'], 'arm-none-eabi-cc-4.6'))
        self.assertTrue(re.match(Cc._cc_re_dict['gcc'], 'arm-none-eabi-cc-52.83'))
        # gcc
        self.assertTrue(re.match(Cc._cc_re_dict['gcc'], 'gcc'))
        self.assertTrue(re.match(Cc._cc_re_dict['gcc'], 'gcc-4.6'))
        self.assertTrue(re.match(Cc._cc_re_dict['gcc'], 'gcc-52.83'))
        self.assertTrue(re.match(Cc._cc_re_dict['gcc'], 'avr-gcc'))
        self.assertTrue(re.match(Cc._cc_re_dict['gcc'], 'avr-gcc-4.6'))
        self.assertTrue(re.match(Cc._cc_re_dict['gcc'], 'avr-gcc-52.83'))
        self.assertTrue(re.match(Cc._cc_re_dict['gcc'], 'arm-none-eabi-gcc'))
        self.assertTrue(re.match(Cc._cc_re_dict['gcc'], 'arm-none-eabi-gcc-4.6'))
        self.assertTrue(re.match(Cc._cc_re_dict['gcc'], 'arm-none-eabi-gcc-52.83'))
        # c++
        self.assertTrue(re.match(Cc._cc_re_dict['g++'], 'c++'))
        self.assertTrue(re.match(Cc._cc_re_dict['g++'], 'c++-4.6'))
        self.assertTrue(re.match(Cc._cc_re_dict['g++'], 'c++-52.83'))
        self.assertTrue(re.match(Cc._cc_re_dict['g++'], 'avr-c++'))
        self.assertTrue(re.match(Cc._cc_re_dict['g++'], 'avr-c++-4.6'))
        self.assertTrue(re.match(Cc._cc_re_dict['g++'], 'avr-c++-52.83'))
        self.assertTrue(re.match(Cc._cc_re_dict['g++'], 'arm-none-eabi-c++'))
        self.assertTrue(re.match(Cc._cc_re_dict['g++'], 'arm-none-eabi-c++-4.6'))
        self.assertTrue(re.match(Cc._cc_re_dict['g++'], 'arm-none-eabi-c++-52.83'))
        # g++
        self.assertTrue(re.match(Cc._cc_re_dict['g++'], 'g++'))
        self.assertTrue(re.match(Cc._cc_re_dict['g++'], 'g++-4.6'))
        self.assertTrue(re.match(Cc._cc_re_dict['g++'], 'g++-52.83'))
        self.assertTrue(re.match(Cc._cc_re_dict['g++'], 'avr-g++'))
        self.assertTrue(re.match(Cc._cc_re_dict['g++'], 'avr-g++-4.6'))
        self.assertTrue(re.match(Cc._cc_re_dict['g++'], 'avr-g++-52.83'))
        self.assertTrue(re.match(Cc._cc_re_dict['g++'], 'arm-none-eabi-g++'))
        self.assertTrue(re.match(Cc._cc_re_dict['g++'], 'arm-none-eabi-g++-4.6'))
        self.assertTrue(re.match(Cc._cc_re_dict['g++'], 'arm-none-eabi-g++-52.83'))

    def test__cc_re_dict__clang(self):
        # clang
        self.assertTrue(re.match(Cc._cc_re_dict['clang'], 'clang'))
        self.assertTrue(re.match(Cc._cc_re_dict['clang'], 'clang-3.5'))
        self.assertTrue(re.match(Cc._cc_re_dict['clang'], 'clang-35.67'))
        self.assertTrue(re.match(Cc._cc_re_dict['clang'], 'avr-clang'))
        self.assertTrue(re.match(Cc._cc_re_dict['clang'], 'avr-clang-3.5'))
        self.assertTrue(re.match(Cc._cc_re_dict['clang'], 'avr-clang-35.67'))
        self.assertTrue(re.match(Cc._cc_re_dict['clang'], 'arm-none-eabi-clang'))
        self.assertTrue(re.match(Cc._cc_re_dict['clang'], 'arm-none-eabi-clang-3.5'))
        self.assertTrue(re.match(Cc._cc_re_dict['clang'], 'arm-none-eabi-clang-35.67'))
        # clang++
        self.assertTrue(re.match(Cc._cc_re_dict['clang++'], 'clang++'))
        self.assertTrue(re.match(Cc._cc_re_dict['clang++'], 'clang++-3.5'))
        self.assertTrue(re.match(Cc._cc_re_dict['clang++'], 'clang++-35.67'))
        self.assertTrue(re.match(Cc._cc_re_dict['clang++'], 'avr-clang++'))
        self.assertTrue(re.match(Cc._cc_re_dict['clang++'], 'avr-clang++-3.5'))
        self.assertTrue(re.match(Cc._cc_re_dict['clang++'], 'avr-clang++-35.67'))
        self.assertTrue(re.match(Cc._cc_re_dict['clang++'], 'arm-none-eabi-clang++'))
        self.assertTrue(re.match(Cc._cc_re_dict['clang++'], 'arm-none-eabi-clang++-3.5'))
        self.assertTrue(re.match(Cc._cc_re_dict['clang++'], 'arm-none-eabi-clang++-35.67'))

    def test__cc_re_dict__cl(self):
        self.assertTrue(re.match(Cc._cc_re_dict['cl'], 'cl'))
        self.assertTrue(re.match(Cc._cc_re_dict['cl'], 'cl.exe'))

    def test__canon_cc__gcc(self):
        if platform.system == 'Windows': root = 'C:\\'
        else:                            root =  '/'
        # cc
        self.assertEqual(Cc._canon_cc('cc'), 'gcc')
        self.assertEqual(Cc._canon_cc('cc-4.6'), 'gcc')
        self.assertEqual(Cc._canon_cc('cc-52.83'), 'gcc')
        self.assertEqual(Cc._canon_cc('avr-cc'), 'gcc')
        self.assertEqual(Cc._canon_cc('avr-cc-4.6'), 'gcc')
        self.assertEqual(Cc._canon_cc('avr-cc-52.83'), 'gcc')
        self.assertEqual(Cc._canon_cc('arm-none-eabi-cc'), 'gcc')
        self.assertEqual(Cc._canon_cc('arm-none-eabi-cc-4.6'), 'gcc')
        self.assertEqual(Cc._canon_cc('arm-none-eabi-cc-52.83'), 'gcc')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','cc')), 'gcc')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','cc-4.6')), 'gcc')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','cc-52.83')), 'gcc')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','avr-cc')), 'gcc')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','avr-cc-4.6')), 'gcc')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','avr-cc-52.83')), 'gcc')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','arm-none-eabi-cc')), 'gcc')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','arm-none-eabi-cc-4.6')), 'gcc')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','arm-none-eabi-cc-52.83')), 'gcc')
        # gcc
        self.assertEqual(Cc._canon_cc('gcc'), 'gcc')
        self.assertEqual(Cc._canon_cc('gcc-4.6'), 'gcc')
        self.assertEqual(Cc._canon_cc('gcc-52.83'), 'gcc')
        self.assertEqual(Cc._canon_cc('avr-gcc'), 'gcc')
        self.assertEqual(Cc._canon_cc('avr-gcc-4.6'), 'gcc')
        self.assertEqual(Cc._canon_cc('avr-gcc-52.83'), 'gcc')
        self.assertEqual(Cc._canon_cc('arm-none-eabi-gcc'), 'gcc')
        self.assertEqual(Cc._canon_cc('arm-none-eabi-gcc-4.6'), 'gcc')
        self.assertEqual(Cc._canon_cc('arm-none-eabi-gcc-52.83'), 'gcc')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','gcc')), 'gcc')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','gcc-4.6')), 'gcc')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','gcc-52.83')), 'gcc')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','avr-gcc')), 'gcc')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','avr-gcc-4.6')), 'gcc')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','avr-gcc-52.83')), 'gcc')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','arm-none-eabi-gcc')), 'gcc')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','arm-none-eabi-gcc-4.6')), 'gcc')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','arm-none-eabi-gcc-52.83')), 'gcc')
        # c++
        self.assertEqual(Cc._canon_cc('c++'), 'g++')
        self.assertEqual(Cc._canon_cc('c++-4.6'), 'g++')
        self.assertEqual(Cc._canon_cc('c++-52.83'), 'g++')
        self.assertEqual(Cc._canon_cc('avr-c++'), 'g++')
        self.assertEqual(Cc._canon_cc('avr-c++-4.6'), 'g++')
        self.assertEqual(Cc._canon_cc('avr-c++-52.83'), 'g++')
        self.assertEqual(Cc._canon_cc('arm-none-eabi-c++'), 'g++')
        self.assertEqual(Cc._canon_cc('arm-none-eabi-c++-4.6'), 'g++')
        self.assertEqual(Cc._canon_cc('arm-none-eabi-c++-52.83'), 'g++')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','c++')), 'g++')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','c++-4.6')), 'g++')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','c++-52.83')), 'g++')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','avr-c++')), 'g++')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','avr-c++-4.6')), 'g++')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','avr-c++-52.83')), 'g++')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','arm-none-eabi-c++')), 'g++')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','arm-none-eabi-c++-4.6')), 'g++')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','arm-none-eabi-c++-52.83')), 'g++')
        # g++
        self.assertEqual(Cc._canon_cc('g++'), 'g++')
        self.assertEqual(Cc._canon_cc('g++-4.6'), 'g++')
        self.assertEqual(Cc._canon_cc('g++-52.83'), 'g++')
        self.assertEqual(Cc._canon_cc('avr-g++'), 'g++')
        self.assertEqual(Cc._canon_cc('avr-g++-4.6'), 'g++')
        self.assertEqual(Cc._canon_cc('avr-g++-52.83'), 'g++')
        self.assertEqual(Cc._canon_cc('arm-none-eabi-g++'), 'g++')
        self.assertEqual(Cc._canon_cc('arm-none-eabi-g++-4.6'), 'g++')
        self.assertEqual(Cc._canon_cc('arm-none-eabi-g++-52.83'), 'g++')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','g++')), 'g++')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','g++-4.6')), 'g++')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','g++-52.83')), 'g++')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','avr-g++')), 'g++')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','avr-g++-4.6')), 'g++')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','avr-g++-52.83')), 'g++')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','arm-none-eabi-g++')), 'g++')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','arm-none-eabi-g++-4.6')), 'g++')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','arm-none-eabi-g++-52.83')), 'g++')

    def test__canon_cc__clang(self):
        if platform.system == 'Windows': root = 'C:\\'
        else:                            root =  '/'
        # clang
        self.assertEqual(Cc._canon_cc('clang'), 'clang')
        self.assertEqual(Cc._canon_cc('clang-3.5'), 'clang')
        self.assertEqual(Cc._canon_cc('clang-35.67'), 'clang')
        self.assertEqual(Cc._canon_cc('avr-clang'), 'clang')
        self.assertEqual(Cc._canon_cc('avr-clang-3.5'), 'clang')
        self.assertEqual(Cc._canon_cc('avr-clang-35.67'), 'clang')
        self.assertEqual(Cc._canon_cc('arm-none-eabi-clang'), 'clang')
        self.assertEqual(Cc._canon_cc('arm-none-eabi-clang-3.5'), 'clang')
        self.assertEqual(Cc._canon_cc('arm-none-eabi-clang-35.67'), 'clang')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','clang')), 'clang')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','clang-3.5')), 'clang')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','clang-35.67')), 'clang')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','avr-clang')), 'clang')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','avr-clang-3.5')), 'clang')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','avr-clang-35.67')), 'clang')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','arm-none-eabi-clang')), 'clang')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','arm-none-eabi-clang-3.5')), 'clang')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','arm-none-eabi-clang-35.67')), 'clang')
        # clang++
        self.assertEqual(Cc._canon_cc('clang++'), 'clang++')
        self.assertEqual(Cc._canon_cc('clang++-3.5'), 'clang++')
        self.assertEqual(Cc._canon_cc('clang++-35.67'), 'clang++')
        self.assertEqual(Cc._canon_cc('avr-clang++'), 'clang++')
        self.assertEqual(Cc._canon_cc('avr-clang++-3.5'), 'clang++')
        self.assertEqual(Cc._canon_cc('avr-clang++-35.67'), 'clang++')
        self.assertEqual(Cc._canon_cc('arm-none-eabi-clang++'), 'clang++')
        self.assertEqual(Cc._canon_cc('arm-none-eabi-clang++-3.5'), 'clang++')
        self.assertEqual(Cc._canon_cc('arm-none-eabi-clang++-35.67'), 'clang++')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','clang++')), 'clang++')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','clang++-3.5')), 'clang++')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','clang++-35.67')), 'clang++')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','avr-clang++')), 'clang++')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','avr-clang++-3.5')), 'clang++')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','avr-clang++-35.67')), 'clang++')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','arm-none-eabi-clang++')), 'clang++')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','arm-none-eabi-clang++-3.5')), 'clang++')
        self.assertEqual(Cc._canon_cc(os.path.join(root,'path','to','arm-none-eabi-clang++-35.67')), 'clang++')

    def test__canon_cc__cl(self):
        if platform.system == 'Windows': root = 'C:\\'
        else:                            root =  '/'
        self.assertEqual(Cc._canon_cc('cl'), 'cl')
        self.assertEqual(Cc._canon_cc('cl.exe'), 'cl')
        self.assertEqual(Cc._canon_cc(os.path.join(root, 'path','to','cl')), 'cl')
        self.assertEqual(Cc._canon_cc(os.path.join(root, 'path','to','cl.exe')), 'cl')

if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ TestCase ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
