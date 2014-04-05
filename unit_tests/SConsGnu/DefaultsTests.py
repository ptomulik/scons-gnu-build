""" SConsGnu.DefaultsTests

Unit tests for SConsGnu.Defaults
"""

__docformat__ = "restructuredText"

#
# Copyright (c) 2012-2014 by Pawel Tomulik
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

from SConsGnu import Defaults

class Test_gvar_env_key(unittest.TestCase):
    def test_gvar_env_key_prefix(self):
        self.assertEqual(Defaults.gvar_env_key_prefix, 'GVAR_')
    def test_gvar_env_key_suffix(self):
        self.assertEqual(Defaults.gvar_env_key_suffix, '')
    def test_gvar_env_key_transform(self):
        self.assertEqual(Defaults.gvar_env_key_transform('Key'), 'GVAR_Key')

class Test_gvar_var_key(unittest.TestCase):
    def test_gvar_var_key_prefix(self):
        self.assertEqual(Defaults.gvar_var_key_prefix, '')
    def test_gvar_var_key_suffix(self):
        self.assertEqual(Defaults.gvar_var_key_suffix, '')
    def test_gvar_var_key_transform(self):
        self.assertEqual(Defaults.gvar_var_key_transform('Key'), 'Key')

class Test_gvar_opt_key(unittest.TestCase):
    def test_gvar_opt_key_prefix(self):
        self.assertEqual(Defaults.gvar_opt_key_prefix, '')
    def test_gvar_opt_key_suffix(self):
        self.assertEqual(Defaults.gvar_opt_key_suffix, '')
    def test_gvar_opt_key_transform(self):
        self.assertEqual(Defaults.gvar_opt_key_transform('Key'), 'key')

class Test_gvar_opt(unittest.TestCase):
    def test_gvar_opt_prefix(self):
        self.assertEqual(Defaults.gvar_opt_prefix, '--')
    def test_gvar_opt_name_prefix(self):
        self.assertEqual(Defaults.gvar_opt_name_prefix, '')
    def test_gvar_opt_name_suffix(self):
        self.assertEqual(Defaults.gvar_opt_name_suffix, '')
    def test_gvar_opt_name_transform(self):
        self.assertEqual(Defaults.gvar_opt_name_transform('FOo_bAr'), '--foo-bar')

class Test_gvar_declarations_var(unittest.TestCase):
    def test_gvar_declarations_var(self):
        self.assertEqual(Defaults.gvar_declarations_var, 'GDECLS')

if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test_gvar_env_key
               , Test_gvar_var_key
               , Test_gvar_opt_key
               , Test_gvar_opt
               , Test_gvar_declarations_var
               ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
