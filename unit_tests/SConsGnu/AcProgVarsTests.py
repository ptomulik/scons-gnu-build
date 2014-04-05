""" SConsGnu.GProgVarsTests

Unit tests for SConsGnu.AcProgVars
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

from mock import Mock, patch
from SConsGnu import AcProgVars
from SConsGnu import GVars
from SConsGnu import Defaults

class Test_default_env_key_transform(unittest.TestCase):
    def test_default_env_key_prefix(self):
        self.assertIs(AcProgVars.default_env_key_prefix, Defaults.gvar_env_key_prefix)
    def test_default_env_key_suffix(self):
        self.assertIs(AcProgVars.default_env_key_suffix, Defaults.gvar_env_key_suffix)
    def test_default_env_key_transform(self):
        self.assertIs(AcProgVars.default_env_key_transform, Defaults.gvar_env_key_transform)

class Test_default_var_key_transform(unittest.TestCase):
    def test_default_var_key_prefix(self):
        self.assertIs(AcProgVars.default_var_key_prefix, Defaults.gvar_var_key_prefix)
    def test_default_var_key_suffix(self):
        self.assertIs(AcProgVars.default_var_key_suffix, Defaults.gvar_var_key_suffix)
    def test_default_var_key_transform(self):
        self.assertIs(AcProgVars.default_var_key_transform, Defaults.gvar_var_key_transform)

class Test_gvar_names(unittest.TestCase):
    def test_AWK_in_names(self):
        """AcProgVars.gvar_names() should contain 'AWK'"""
        self.assertIn('AWK', AcProgVars.gvar_names())
    def test_EGREP_in_names(self):
        """AcProgVars.gvar_names() should contain 'EGREP'"""
        self.assertIn('EGREP', AcProgVars.gvar_names())
    def test_FGREP_in_names(self):
        """AcProgVars.gvar_names() should contain 'FGREP'"""
        self.assertIn('FGREP', AcProgVars.gvar_names())
    def test_GREP_in_names(self):
        """AcProgVars.gvar_names() should contain 'GREP'"""
        self.assertIn('GREP', AcProgVars.gvar_names())
    def test_INSTALL_in_names(self):
        """AcProgVars.gvar_names() should contain 'INSTALL'"""
        self.assertIn('INSTALL', AcProgVars.gvar_names())
    def test_INSTALL_DATA_in_names(self):
        """AcProgVars.gvar_names() should contain 'INSTALL_DATA'"""
        self.assertIn('INSTALL_DATA', AcProgVars.gvar_names())
    def test_INSTALL_PROGRAM_in_names(self):
        """AcProgVars.gvar_names() should contain 'INSTALL_PROGRAM'"""
        self.assertIn('INSTALL_PROGRAM', AcProgVars.gvar_names())
    def test_INSTALL_SCRIPT_in_names(self):
        """AcProgVars.gvar_names() should contain 'INSTALL_SCRIPT'"""
        self.assertIn('INSTALL_SCRIPT', AcProgVars.gvar_names())
    def test_LEX_in_names(self):
        """AcProgVars.gvar_names() should contain 'LEX'"""
        self.assertIn('LEX', AcProgVars.gvar_names())
    def test_LEX_OUTPUT_ROOT_in_names(self):
        """AcProgVars.gvar_names() should contain 'LEX_OUTPUT_ROOT'"""
        self.assertIn('LEX_OUTPUT_ROOT', AcProgVars.gvar_names())
    def test_LEXLIB_in_names(self):
        """AcProgVars.gvar_names() should contain 'LEXLIB'"""
        self.assertIn('LEXLIB', AcProgVars.gvar_names())
    def test_LN_S_in_names(self):
        """AcProgVars.gvar_names() should contain 'LN_S'"""
        self.assertIn('LN_S', AcProgVars.gvar_names())
    def test_MKDIR_P_in_names(self):
        """AcProgVars.gvar_names() should contain 'MKDIR_P'"""
        self.assertIn('MKDIR_P', AcProgVars.gvar_names())
    def test_RANLIB_in_names(self):
        """AcProgVars.gvar_names() should contain 'RANLIB'"""
        self.assertIn('RANLIB', AcProgVars.gvar_names())
    def test_SED_in_names(self):
        """AcProgVars.gvar_names() should contain 'SED'"""
        self.assertIn('SED', AcProgVars.gvar_names())
    def test_YACC_in_names(self):
        """AcProgVars.gvar_names() should contain 'YACC'"""
        self.assertIn('YACC', AcProgVars.gvar_names())

class Test_declare_gvars(unittest.TestCase):
    def check_decl(self, name, val):
        gdecl = AcProgVars.declare_gvars(lambda x : True)[name]
        self.assertEqual(gdecl.get_xxx_default(GVars.VAR), val)
        self.assertEqual(gdecl.get_xxx_key(GVars.ENV), "GVAR_%s" % name)
        self.assertEqual(gdecl.get_xxx_key(GVars.VAR), name)
    def test_AWK(self):
        """test AcProgVars.declare_gvars(lambda x : True)['AWK']"""
        self.check_decl('AWK', AcProgVars._auto)
    def test_EGREP(self):
        """test AcProgVars.declare_gvars(lambda x : True)['EGREP']"""
        self.check_decl('EGREP', AcProgVars._auto)
    def test_FGREP(self):
        """test AcProgVars.declare_gvars(lambda x : True)['FGREP']"""
        self.check_decl('FGREP', AcProgVars._auto)
    def test_GREP(self):
        """test AcProgVars.declare_gvars(lambda x : True)['GREP']"""
        self.check_decl('GREP', AcProgVars._auto)
    def test_INSTALL(self):
        """test AcProgVars.declare_gvars(lambda x : True)['INSTALL']"""
        self.check_decl('INSTALL', AcProgVars._auto)
    def test_INSTALL_DATA(self):
        """test AcProgVars.declare_gvars(lambda x : True)['INSTALL_DATA']"""
        self.check_decl('INSTALL_DATA', AcProgVars._auto)
    def test_INSTALL_PROGRAM(self):
        """test AcProgVars.declare_gvars(lambda x : True)['INSTALL_PROGRAM']"""
        self.check_decl('INSTALL_PROGRAM', AcProgVars._auto)
    def test_INSTALL_SCRIPT(self):
        """test AcProgVars.declare_gvars(lambda x : True)['INSTALL_SCRIPT']"""
        self.check_decl('INSTALL_SCRIPT', AcProgVars._auto)
    def test_LEX(self):
        """test AcProgVars.declare_gvars(lambda x : True)['LEX']"""
        self.check_decl('LEX', AcProgVars._auto)
    def test_LEX_OUTPUT_ROOT(self):
        """test AcProgVars.declare_gvars(lambda x : True)['LEX_OUTPUT_ROOT']"""
        self.check_decl('LEX_OUTPUT_ROOT', AcProgVars._auto)
    def test_LEXLIB(self):
        """test AcProgVars.declare_gvars(lambda x : True)['LEXLIB']"""
        self.check_decl('LEXLIB', AcProgVars._auto)
    def test_LN_S(self):
        """test AcProgVars.declare_gvars(lambda x : True)['LN_S']"""
        self.check_decl('LN_S', AcProgVars._auto)
    def test_MKDIR_P(self):
        """test AcProgVars.declare_gvars(lambda x : True)['MKDIR_P']"""
        self.check_decl('MKDIR_P', AcProgVars._auto)
    def test_RANLIB(self):
        """test AcProgVars.declare_gvars(lambda x : True)['RANLIB']"""
        self.check_decl('RANLIB', AcProgVars._auto)
    def test_SED(self):
        """test AcProgVars.declare_gvars(lambda x : True)['SED']"""
        self.check_decl('SED', AcProgVars._auto)
    def test_YACC(self):
        """test AcProgVars.declare_gvars(lambda x : True)['YACC']"""
        self.check_decl('YACC', AcProgVars._auto)

class Test_GVarNames(unittest.TestCase):
    def test_GVarNames_1(self):
        """AcProgVars.GVarNames() should invoke AcProgVars.gvar_names() once"""
        with patch('SConsGnu.AcProgVars.gvar_names') as gvar_names:
            AcProgVars.GVarNames()
            try:
                gvar_names.assert_called_once_with()
            except AssertionError as e:
                self.fail(str(e))
    def test_GVarNames_2(self):
        """AcProgVars.GVarNames(foo = 'FOO', name_filter = 'NAME_FILTER') should invoke AcProgVars.gvar_names(name_filter = 'NAME_FILTER') once"""
        with patch('SConsGnu.AcProgVars.gvar_names') as gvar_names:
            AcProgVars.GVarNames(foo = 'FOO', name_filter = 'NAME_FILTER')
            try:
                gvar_names.assert_called_once_with(name_filter = 'NAME_FILTER')
            except AssertionError as e:
                self.fail(str(e))

class Test_DeclareGVars(unittest.TestCase):
    def test_DeclareGVars_1(self):
        """AcProgVars.DeclareGVars() should invoke AcProgVars.declare_gvars() once"""
        with patch('SConsGnu.AcProgVars.declare_gvars', return_value = 'ok') as declare_gvars:
            decls = AcProgVars.DeclareGVars()
            try:
                declare_gvars.assert_called_once_with()
            except AssertionError as e:
                self.fail(str(e))
            self.assertIs(decls, 'ok')

    def test_DeclareGVars_2(self):
        """AcProgVars.DeclareGVars(foo = 'FOO', name_filter = 'NF', env_key_transform = 'EKT', var_key_transform = 'VKT')"""
        with patch('SConsGnu.AcProgVars.declare_gvars', return_value = 'ok') as declare_gvars:
            decls = AcProgVars.DeclareGVars(foo = 'FOO', name_filter = 'NF', env_key_transform = 'EKT', var_key_transform = 'VKT')
            try:
                declare_gvars.assert_called_once_with(name_filter = 'NF', env_key_transform = 'EKT', var_key_transform = 'VKT')
            except AssertionError as e:
                self.fail(str(e))
            self.assertIs(decls, 'ok')


if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ Test_default_env_key_transform
               , Test_default_var_key_transform
               , Test_gvar_names
               , Test_declare_gvars
               , Test_GVarNames
               , Test_DeclareGVars ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTest_default_env_key_transform(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
