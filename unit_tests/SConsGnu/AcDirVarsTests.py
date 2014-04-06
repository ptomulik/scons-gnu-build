""" SConsGnu.AcDirVarsTests

Unit tests for SConsGnu.AcDirVars
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
from SConsGnu import AcDirVars
from SConsGnu import GVars
from SConsGnu import Defaults

class Test_default_env_key_transform(unittest.TestCase):
    def test_default_env_key_prefix(self):
        self.assertIs(AcDirVars.default_env_key_prefix, Defaults.gvar_env_key_prefix)
    def test_default_env_key_suffix(self):
        self.assertIs(AcDirVars.default_env_key_suffix, Defaults.gvar_env_key_suffix)
    def test_default_env_key_transform(self):
        self.assertIs(AcDirVars.default_env_key_transform, Defaults.gvar_env_key_transform)

class Test_default_var_key_transform(unittest.TestCase):
    def test_default_var_key_prefix(self):
        self.assertIs(AcDirVars.default_var_key_prefix, Defaults.gvar_var_key_prefix)
    def test_default_var_key_suffix(self):
        self.assertIs(AcDirVars.default_var_key_suffix, Defaults.gvar_var_key_suffix)
    def test_default_var_key_transform(self):
        self.assertIs(AcDirVars.default_var_key_transform, Defaults.gvar_var_key_transform)

class Test_default_opt_key_transform(unittest.TestCase):
    def test_default_opt_key_prefix(self):
        self.assertIs(AcDirVars.default_opt_key_prefix, Defaults.gvar_opt_key_prefix)
    def test_default_opt_key_suffix(self):
        self.assertIs(AcDirVars.default_opt_key_suffix, Defaults.gvar_opt_key_suffix)
    def test_default_opt_key_transform(self):
        self.assertIs(AcDirVars.default_opt_key_transform, Defaults.gvar_opt_key_transform)

class Test_default_opt_name_transform(unittest.TestCase):
    def test_default_opt_prefix(self):
        self.assertIs(AcDirVars.default_opt_prefix, Defaults.gvar_opt_prefix)
    def test_default_opt_name_prefix(self):
        self.assertIs(AcDirVars.default_opt_name_prefix, Defaults.gvar_opt_name_prefix)
    def test_default_opt_name_suffix(self):
        self.assertIs(AcDirVars.default_opt_name_suffix, Defaults.gvar_opt_name_suffix)
    def test_default_opt_name_transform(self):
        self.assertIs(AcDirVars.default_opt_name_transform, Defaults.gvar_opt_name_transform)

class Test_gvar_names(unittest.TestCase):
    def test_prefix_in_names(self):
        """AcDirVars.gvar_names() should contain 'prefix'"""
        self.assertIn('prefix', AcDirVars.gvar_names())
    def test_exec_prefix_in_names(self):
        self.assertIn('exec_prefix', AcDirVars.gvar_names())
    def test_bindir_in_names(self):
        """AcDirVars.gvar_names() should contain 'bindir'"""
        self.assertIn('bindir', AcDirVars.gvar_names())
    def test_sbindir_in_names(self):
        """AcDirVars.gvar_names() should contain 'sbindir'"""
        self.assertIn('sbindir', AcDirVars.gvar_names())
    def test_libexecdir_in_names(self):
        """AcDirVars.gvar_names() should contain 'libexecdir'"""
        self.assertIn('libexecdir', AcDirVars.gvar_names())
    def test_datarootdir_in_names(self):
        """AcDirVars.gvar_names() should contain 'datarootdir'"""
        self.assertIn('datarootdir', AcDirVars.gvar_names())
    def test_datadir_in_names(self):
        """AcDirVars.gvar_names() should contain 'datadir'"""
        self.assertIn('datadir', AcDirVars.gvar_names())
    def test_sysconfdir_in_names(self):
        """AcDirVars.gvar_names() should contain 'sysconfdir'"""
        self.assertIn('sysconfdir', AcDirVars.gvar_names())
    def test_sharedstatedir_in_names(self):
        """AcDirVars.gvar_names() should contain 'sharedstatedir'"""
        self.assertIn('sharedstatedir', AcDirVars.gvar_names())
    def test_localstatedir_in_names(self):
        """AcDirVars.gvar_names() should contain 'localstatedir'"""
        self.assertIn('localstatedir', AcDirVars.gvar_names())
    def test_includedir_in_names(self):
        """AcDirVars.gvar_names() should contain 'includedir'"""
        self.assertIn('includedir', AcDirVars.gvar_names())
    def test_oldincludedir_in_names(self):
        """AcDirVars.gvar_names() should contain 'oldincludedir'"""
        self.assertIn('oldincludedir', AcDirVars.gvar_names())
    def test_docdir_in_names(self):
        """AcDirVars.gvar_names() should contain 'docdir'"""
        self.assertIn('docdir', AcDirVars.gvar_names())
    def test_infodir_in_names(self):
        """AcDirVars.gvar_names() should contain 'infodir'"""
        self.assertIn('infodir', AcDirVars.gvar_names())
    def test_htmldir_in_names(self):
        """AcDirVars.gvar_names() should contain 'htmldir'"""
        self.assertIn('htmldir', AcDirVars.gvar_names())
    def test_dvidir_in_names(self):
        """AcDirVars.gvar_names() should contain 'dvidir'"""
        self.assertIn('dvidir', AcDirVars.gvar_names())
    def test_pdfdir_in_names(self):
        """AcDirVars.gvar_names() should contain 'pdfdir'"""
        self.assertIn('pdfdir', AcDirVars.gvar_names())
    def test_psdir_in_names(self):
        """AcDirVars.gvar_names() should contain 'psdir'"""
        self.assertIn('psdir', AcDirVars.gvar_names())
    def test_libdir_in_names(self):
        """AcDirVars.gvar_names() should contain 'libdir'"""
        self.assertIn('libdir', AcDirVars.gvar_names())
    def test_lispdir_in_names(self):
        """AcDirVars.gvar_names() should contain 'lispdir'"""
        self.assertIn('lispdir', AcDirVars.gvar_names())
    def test_localedir_in_names(self):
        """AcDirVars.gvar_names() should contain 'localedir'"""
        self.assertIn('localedir', AcDirVars.gvar_names())
    def test_mandir_in_names(self):
        """AcDirVars.gvar_names() should contain 'mandir'"""
        self.assertIn('mandir', AcDirVars.gvar_names())
    def test_pkgdatadir_in_names(self):
        """AcDirVars.gvar_names() should contain 'pkgdatadir'"""
        self.assertIn('pkgdatadir', AcDirVars.gvar_names())
    def test_pkgincludedir_in_names(self):
        """AcDirVars.gvar_names() should contain 'pkgincludedir'"""
        self.assertIn('pkgincludedir', AcDirVars.gvar_names())
    def test_pkglibdir_in_names(self):
        """AcDirVars.gvar_names() should contain 'pkglibdir'"""
        self.assertIn('pkglibdir', AcDirVars.gvar_names())
    def test_pkglibexecdir_in_names(self):
        """AcDirVars.gvar_names() should contain 'pkglibexecdir'"""
        self.assertIn('pkglibexecdir', AcDirVars.gvar_names())
    def test_manNdir_in_names(self):
        """AcDirVars.gvar_names() should contain 'man1dir' .. 'man9dir'"""
        for d in range(1,10):
            self.assertIn('man%sdir' % d, AcDirVars.gvar_names())
    def test_manNext_in_names(self):
        """AcDirVars.gvar_names() should contain 'man1ext' .. 'man9ext'"""
        for d in range(1,10):
            self.assertIn('man%sext' % d, AcDirVars.gvar_names())
    def test_gvar_names_filter(self):
        """AcDirVars.gvar_names(filter) should use the filter"""
        self.assertIn('datarootdir', AcDirVars.gvar_names(lambda x : x.startswith('data')))
        self.assertIn('datarootdir', AcDirVars.gvar_names(lambda x : x.startswith('data')))
        self.assertNotIn('bindir', AcDirVars.gvar_names(lambda x : x.startswith('data')))
        self.assertNotIn('pkglibdir', AcDirVars.gvar_names(lambda x : x.startswith('data')))

class Test_declare_gvars(unittest.TestCase):
    def check_decl(self, name, val):
        gdecl = AcDirVars.declare_gvars()[name]
        self.assertEqual(gdecl.get_xxx_default(GVars.VAR), val)
        self.assertEqual(gdecl.get_xxx_key(GVars.ENV), name)
        self.assertEqual(gdecl.get_xxx_key(GVars.VAR), name)
        self.assertEqual(gdecl.get_xxx_key(GVars.OPT), name)
    def test_prefix(self):
        """test AcDirVars.declare_gvars()['prefix']"""
        self.check_decl('prefix', '/usr/local')
    def test_exec_prefix(self):
        """test AcDirVars.declare_gvars()['exec_prefix']"""
        self.check_decl('exec_prefix', '${prefix}')
    def test_bindir(self):
        """test AcDirVars.declare_gvars()['bindir']"""
        self.check_decl('bindir', '${exec_prefix}/bin')
    def test_sbindir(self):
        """test AcDirVars.declare_gvars()['sbindir']"""
        self.check_decl('sbindir', '${exec_prefix}/sbin')
    def test_libexecdir(self):
        """test AcDirVars.declare_gvars()['libexecdir']"""
        self.check_decl('libexecdir', '${exec_prefix}/libexec')
    def test_datarootdir(self):
        """test AcDirVars.declare_gvars()['datarootdir']"""
        self.check_decl('datarootdir', '${prefix}/share')
    def test_datadir(self):
        """test AcDirVars.declare_gvars()['datadir']"""
        self.check_decl('datadir', '${datarootdir}')
    def test_sysconfdir(self):
        """test AcDirVars.declare_gvars()['sysconfdir']"""
        self.check_decl('sysconfdir', '${prefix}/etc')
    def test_sharedstatedir(self):
        """test AcDirVars.declare_gvars()['sharedstatedir']"""
        self.check_decl('sharedstatedir', '${prefix}/com')
    def test_localstatedir(self):
        """test AcDirVars.declare_gvars()['localstatedir']"""
        self.check_decl('localstatedir', '${prefix}/var')
    def test_includedir(self):
        """test AcDirVars.declare_gvars()['includedir']"""
        self.check_decl('includedir', '${prefix}/include')
    def test_oldincludedir(self):
        """test AcDirVars.declare_gvars()['oldincludedir']"""
        self.check_decl('oldincludedir', '/usr/include')
    def test_docdir(self):
        """test AcDirVars.declare_gvars()['docdir']"""
        self.check_decl('docdir', '${datarootdir}/doc/${install_package}')
    def test_infodir(self):
        """test AcDirVars.declare_gvars()['infodir']"""
        self.check_decl('infodir', '${datarootdir}/info')
    def test_htmldir(self):
        """test AcDirVars.declare_gvars()['htmldir']"""
        self.check_decl('htmldir', '${docdir}')
    def test_dvidir(self):
        """test AcDirVars.declare_gvars()['dvidir']"""
        self.check_decl('dvidir', '${docdir}')
    def test_pdfdir(self):
        """test AcDirVars.declare_gvars()['pdfdir']"""
        self.check_decl('pdfdir', '${docdir}')
    def test_psdir(self):
        """test AcDirVars.declare_gvars()['psdir']"""
        self.check_decl('psdir', '${docdir}')
    def test_libdir(self):
        """test AcDirVars.declare_gvars()['libdir']"""
        self.check_decl('libdir', '${exec_prefix}/lib')
    def test_lispdir(self):
        """test AcDirVars.declare_gvars()['lispdir']"""
        self.check_decl('lispdir', '${datarootdir}/emacs/site-lisp')
    def test_localedir(self):
        """test AcDirVars.declare_gvars()['localedir']"""
        self.check_decl('localedir', '${datarootdir}/locale')
    def test_mandir(self):
        """test AcDirVars.declare_gvars()['mandir']"""
        self.check_decl('mandir', '${datarootdir}/man')
    def test_pkgdatadir(self):
        """test AcDirVars.declare_gvars()['pkgdatadir']"""
        self.check_decl('pkgdatadir', '${datadir}/${package}')
    def test_pkgincludedir(self):
        """test AcDirVars.declare_gvars()['pkgincludedir']"""
        self.check_decl('pkgincludedir', '${includedir}/${package}')
    def test_pkglibdir(self):
        """test AcDirVars.declare_gvars()['pkglibdir']"""
        self.check_decl('pkglibdir', '${libdir}/${package}')
    def test_pkglibexecdir(self):
        """test AcDirVars.declare_gvars()['pkglibexecdir']"""
        self.check_decl('pkglibexecdir', '${libexecdir}/${package}')

class Test_GVarNames(unittest.TestCase):
    def test_GVarNames_1(self):
        """AcDirVars.GVarNames() should invoke AcDirVars.gvar_names() once"""
        with patch('SConsGnu.AcDirVars.gvar_names') as gvar_names:
            AcDirVars.GVarNames()
            try:
                gvar_names.assert_called_once_with()
            except AssertionError as e:
                self.fail(str(e))
    def test_GVarNames_2(self):
        """AcDirVars.GVarNames(foo = 'FOO', name_filter = 'NAME_FILTER') should invoke AcDirVars.gvar_names(name_filter = 'NAME_FILTER') once"""
        with patch('SConsGnu.AcDirVars.gvar_names') as gvar_names:
            AcDirVars.GVarNames(foo = 'FOO', name_filter = 'NAME_FILTER')
            try:
                gvar_names.assert_called_once_with(name_filter = 'NAME_FILTER')
            except AssertionError as e:
                self.fail(str(e))

class Test_DeclareGVars(unittest.TestCase):
    def test_DeclareGVars_1(self):
        """AcDirVars.DeclareGVars() should invoke AcDirVars.declare_gvars() once"""
        with patch('SConsGnu.AcDirVars.declare_gvars', return_value = 'ok') as declare_gvars:
            decls = AcDirVars.DeclareGVars()
            try:
                declare_gvars.assert_called_once_with()
            except AssertionError as e:
                self.fail(str(e))
            self.assertIs(decls, 'ok')

    def test_DeclareGVars_2(self):
        """AcDirVars.DeclareGVars(foo = 'FOO', name_filter = 'NF', env_key_transform = 'EKT', var_key_transform = 'VKT', opt_key_transform = 'OKT', opt_name_transform = 'ONT')"""
        with patch('SConsGnu.AcDirVars.declare_gvars', return_value = 'ok') as declare_gvars:
            decls = AcDirVars.DeclareGVars(foo = 'FOO', name_filter = 'NF', env_key_transform = 'EKT', var_key_transform = 'VKT', opt_key_transform = 'OKT', opt_name_transform = 'ONT')
            try:
                declare_gvars.assert_called_once_with(name_filter = 'NF', env_key_transform = 'EKT', var_key_transform = 'VKT', opt_key_transform = 'OKT', opt_name_transform = 'ONT')
            except AssertionError as e:
                self.fail(str(e))
            self.assertIs(decls, 'ok')
        
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses =  [ Test_default_env_key_transform
                , Test_default_var_key_transform
                , Test_default_opt_key_transform
                , Test_default_opt_name_transform
                , Test_gvar_names
                , Test_declare_gvars
                , Test_GVarNames
                , Test_DeclareGVars ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
