""" SConsGnuBuild.GVarsTest

Unit tests for SConsGnuBuild.GVars
"""

__docformat__ = "restructuredText"

#
# Copyright (c) 2014 by Pawel Tomulik
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

from SConsGnuBuild import GVars
from SConsGnuBuild.GVars import GVarDecl, GVarDeclU, GVarDecls, GVarDeclsU

#############################################################################
class Test_module_constants(unittest.TestCase):
    """Test constants in GVars module"""
    def test_ENV(self):
        "GVars.ENV should == 0"
        self.assertEqual(GVars.ENV,0)
    def test_VAR(self):
        "GVars.VAR should == 1"
        self.assertEqual(GVars.VAR,1)
    def test_OPT(self):
        "GVars.OPT should == 2"
        self.assertEqual(GVars.OPT,2)
    def test_ALL(self):
        "GVars.ALL should == 3"
        self.assertEqual(GVars.ALL,3)
    def test__missing(self):
        "GVars._missing should be a class"
        self.assertTrue(isinstance(GVars._missing,type))
    def test__dont_create(self):
        "GVars._dont_create should be a class"
        self.assertTrue(isinstance(GVars._dont_create,type))
    def test__notfound(self):
        "GVars._notfound should be a class"
        self.assertTrue(isinstance(GVars._notfound,type))

#############################################################################
class Test__resubst(unittest.TestCase):
    """Test GVars._resubst() function"""
    def test__resubst_1(self):
        """GVars._resubst('foo bar') should be 'foo bar'"""
        self.assertEqual(GVars._resubst('foo bar'), 'foo bar')
    def test__resubst_2(self):
        """GVars._resubst('foo bar', {'foo' : 'XFOO'}) should be 'foo bar'"""
        self.assertEqual(GVars._resubst('foo bar', {'foo' : 'XFOO'}), 'foo bar')
    def test__resubst_3(self):
        """GVars._resubst('foo $bar', {'bar' : 'XBAR'}) should be 'foo XBAR'"""
        self.assertEqual(GVars._resubst('foo $bar', {'bar' : 'XBAR'}), 'foo XBAR')
    def test__resubst_4(self):
        """GVars._resubst('$foo $bar', {'foo' : 'XFOO', 'bar' : 'XBAR'}) should be 'XFOO XBAR'"""
        self.assertEqual(GVars._resubst('$foo $bar', {'foo' : 'XFOO', 'bar' : 'XBAR'}), 'XFOO XBAR')
    def test__resubst_5(self):
        """GVars._resubst('$foo $bar', {'foo' : '$bar', 'bar' : 'XBAR'}) should be '$bar XBAR'"""
        self.assertEqual(GVars._resubst('$foo $bar', {'foo' : '$bar', 'bar' : 'XBAR'}), '$bar XBAR')
    def test__resubst_6(self):
        """GVars._resubst('foo ${bar}', {'bar' : 'XBAR'}) should be 'foo XBAR'"""
        self.assertEqual(GVars._resubst('foo ${bar}', {'bar' : 'XBAR'}), 'foo XBAR')
    def test__resubst_7(self):
        """GVars._resubst('${foo} ${bar}', {'foo' : 'XFOO', 'bar' : 'XBAR'}) should be 'XFOO XBAR'"""
        self.assertEqual(GVars._resubst('${foo} ${bar}', {'foo' : 'XFOO', 'bar' : 'XBAR'}), 'XFOO XBAR')
    def test__resubst_8(self):
        """GVars._resubst('${foo} ${bar}', {'foo' : '${bar}', 'bar' : 'XBAR'}) should be '${bar} XBAR'"""
        self.assertEqual(GVars._resubst('${foo} ${bar}', {'foo' : '${bar}', 'bar' : 'XBAR'}), '${bar} XBAR')

#############################################################################
class Test__build_resubst_dict(unittest.TestCase):
    """Test GVars._build_resubst_dict() function"""
    def test__build_resubst_dict_1(self):
        """GVars._build_resubst_dict({}) should == {}"""
        self.assertEqual(GVars._build_resubst_dict({}),{})
    def test__build_resubst_dict_2(self):
        """GVars._build_resubst_dict({'xxx' : 'yyy', 'vvv' : 'www'}) should == {'xxx' : '${yyy}', 'vvv' : '${www}'}"""
        self.assertEqual(GVars._build_resubst_dict({'xxx' : 'yyy', 'vvv' : 'www'}), {'xxx' : '${yyy}', 'vvv' : '${www}'})

#############################################################################
class Test__build_iresubst_dict(unittest.TestCase):
    """Test GVars._build_iresubst_dict() function"""
    def test__build_iresubst_dict_1(self):
        """GVars._build_iresubst_dict({}) should == {}"""
        self.assertEqual(GVars._build_iresubst_dict({}),{})
    def test__build_iresubst_dict_2(self):
        """GVars._build_iresubst_dict({'xxx' : 'yyy', 'vvv' : 'www'}) should == {'yyy' : '${xxx}', 'www' : '${vvv}'}"""
        self.assertEqual(GVars._build_iresubst_dict({'xxx' : 'yyy', 'vvv' : 'www'}), {'yyy' : '${xxx}', 'www' : '${vvv}'})

#############################################################################
class Test__compose_dicts(unittest.TestCase):
    """Test GVars._compose_dicts() function"""
    def test__compose_dicts_1(self):
        """GVars._compose_dicts({},{}) should == {}"""
        self.assertEqual(GVars._compose_dicts({},{}),{})
    def test__compose_dicts_2(self):
        """GVars._compose_dicts({'uuu' : 'vvv', 'xxx' : 'yyy'} ,{ 'vvv' : 'VVV', 'yyy' : 'YYY'}) should == {'uuu' : 'VVV'}"""
        self.assertEqual(GVars._compose_dicts({'uuu' : 'vvv', 'xxx' : 'yyy'}, { 'vvv' : 'VVV', 'yyy' : 'YYY'}), {'uuu' : 'VVV', 'xxx' : 'YYY'})

#############################################################################
class Test_GVarDecl(unittest.TestCase):
    def test_gvar_decl_1(self):
        """GVarDecl() should be an instance of GVars._GVarDecl()"""
        self.assertIsInstance(GVarDecl(), GVars._GVarDecl)
    def test_gvar_decl_2(self):
        """if decl = GVarDecl() then GVarDecl(decl) should be decl"""
        decl = GVarDecl()
        self.assertIs(GVarDecl(decl), decl)
    def test_gvar_decl_3(self):
        """GVarDecl() should not be same as GVarDecl()"""
        self.assertIsNot(GVarDecl(), GVarDecl())

    def test_user_doc_example_1(self):
        """example 1 from user documentation should work"""
        decl = GVarDecl( {'xvar' : None}, None, ('--xvar', {'dest' : 'xvar', 'type' : 'string'}) )
        self.assertIsInstance(decl, GVars._GVarDecl)

#############################################################################
class Test_GVarDeclU(unittest.TestCase):
    def test_user_doc_example_2(self):
        """example 2 from user documentation should work"""
        decl = GVarDeclU(env_key = 'xvar', opt_key = 'xvar', option = '--xvar', type = 'string')
        self.assertIsInstance(decl, GVars._GVarDecl)

#############################################################################
class Test_GVarDecls(unittest.TestCase):
    def test_user_doc_example_3(self):
        """example 3 from user documentation should work"""
        # create single declarations
        foodecl = GVarDecl( {'ENV_FOO' : 'default ENV_FOO'},            # ENV
                      ('var_foo', 'var_foo help', ),                    # VAR
                      ('--foo', {'dest' : "opt_foo"}) )                 # OPT
        bardecl = GVarDecl( {'ENV_BAR' : None},                         # ENV
                      ('var_bar', 'var_bar help', 'default var_bar'),   # VAR
                      ('--bar', {'dest':"opt_bar", "type":"string"}))   # OPT
        # put them all together
        decls = GVarDecls({ 'foo' : foodecl, 'bar' : bardecl })
        self.assertIsInstance(decls, dict)
        self.assertIsInstance(decls, GVars._GVarDecls)
        self.assertIsInstance(decls['foo'], GVars._GVarDecl)
        self.assertIsInstance(decls['bar'], GVars._GVarDecl)

    def test_user_doc_example_4(self):
        """example 4 from user documentation should work"""
        # create multiple declarations at once
        decls = GVarDecls({
          # GVar 'foo'
          'foo' : ( {'ENV_FOO' : 'default ENV_FOO'},                 # ENV
                    ('var_foo', 'var_foo help', ),                   # VAR
                    ('--foo', {'dest' : "opt_foo"}) ),               # OPT
          # GVar 'bar'
          'bar' : ( {'ENV_BAR' : None},                              # ENV
                    ('var_bar', 'var_bar help', 'default var_bar'),  # VAR
                    ('--bar', {'dest':"opt_bar", "type":"string"}) ) # OPT
        })
        self.assertIsInstance(decls, dict)
        self.assertIsInstance(decls, GVars._GVarDecls)
        self.assertIsInstance(decls['foo'], GVars._GVarDecl)
        self.assertIsInstance(decls['bar'], GVars._GVarDecl)

    def test_user_doc_example_5(self):
        """example 5 from user documentation should work"""
        decls = GVarDecls([
          # GVar 'foo'
          ('foo',  ( {'ENV_FOO' : 'default ENV_FOO'},                  # ENV
                     ('var_foo', 'var_foo help', ),                    # VAR
                     ('--foo', {'dest' : "opt_foo"}) )),               # OPT
          # GVar 'bar'
          ('bar',  ( {'ENV_BAR' : None},                               # ENV
                     ('var_bar', 'var_bar help', 'default var_bar'),   # VAR
                     ('--bar', {'dest':"opt_bar", "type":"string"}) )) # OPT
        ])
        self.assertIsInstance(decls, dict)
        self.assertIsInstance(decls, GVars._GVarDecls)
        self.assertIsInstance(decls['foo'], GVars._GVarDecl)
        self.assertIsInstance(decls['bar'], GVars._GVarDecl)

    def test_user_doc_example_6(self):
        """example 6 from user documentation should work"""
        decls = GVarDecls(
          # GVar 'foo'
          foo =  ( {'ENV_FOO' : 'default ENV_FOO'},                  # ENV
                   ('var_foo', 'var_foo help', ),                    # VAR
                   ('--foo', {'dest' : "opt_foo"}) ),                # OPT
          # GVar 'bar'
          bar =  ( {'ENV_BAR' : None},                               # ENV
                   ('var_bar', 'var_bar help', 'default var_bar'),   # VAR
                   ('--bar', {'dest':"opt_bar", "type":"string"}) )  # OPT
        )
        self.assertIsInstance(decls, dict)
        self.assertIsInstance(decls, GVars._GVarDecls)
        self.assertIsInstance(decls['foo'], GVars._GVarDecl)
        self.assertIsInstance(decls['bar'], GVars._GVarDecl)

    def test_user_doc_example_7(self):
        """example 7 from user documentation should work"""
        decls = GVarDecls(
           # GVar 'foo'
           [('foo',(  {'ENV_FOO' : 'ENV default FOO'},                    # ENV
                      ('FOO',         'FOO variable help', ),             # VAR
                      ('--foo',       {'dest' : "opt_foo"})         ))],  # OPT
           # GVar 'geez'
           geez  = (  {'ENV_GEEZ' : None},                                # ENV
                      ('GEEZ', 'GEEZ variable help', 'VAR default GEEZ'), # VAR
                      ('--geez', {'dest':"opt_geez", "type":"string"}))   # OPT
        )
        self.assertIsInstance(decls, dict)
        self.assertIsInstance(decls, GVars._GVarDecls)
        self.assertIsInstance(decls['foo'], GVars._GVarDecl)
        self.assertIsInstance(decls['geez'], GVars._GVarDecl)

    # It's not a mistake, example 8 is found in Test_GVarDeclsU.
    def test_user_doc_example_9(self):
        """example 9 from user documentation should work"""
        decls = GVarDecls(
            foo = ( { 'ENV_FOO' : None }, ('VAR_FOO', 'Help for VAR_FOO', '$VAR_BAR'), None), 
           bar = ( { 'ENV_BAR' : None }, ('VAR_BAR', 'Help for VAR_BAR', 'BAR'), None),
        )
        self.assertIsInstance(decls, dict)
        self.assertIsInstance(decls, GVars._GVarDecls)
        self.assertIsInstance(decls['foo'], GVars._GVarDecl)
        self.assertIsInstance(decls['bar'], GVars._GVarDecl)

#############################################################################
class Test_GVarDeclsU(unittest.TestCase):
    def test_user_doc_example_8(self):
        """example 8 from user documentation should work"""
        decls = GVarDeclsU(
          foo = { 'env_key': 'ENV_FOO', 'var_key' : 'var_foo', 'opt_key' : 'opt_foo',
                  'option' : '--foo', 'default' : 'Default FOO',
                  'help' : 'foo help' },
          bar = { 'env_key': 'ENV_BAR', 'var_key' : 'var_bar', 'opt_key' : 'opt_bar',
                  'option' : '--bar', 'default' : 'Default VAR',  'type' : 'string',
                  'help' : 'bar help' }
        )
        self.assertIsInstance(decls, dict)
        self.assertIsInstance(decls, GVars._GVarDecls)
        self.assertIsInstance(decls['foo'], GVars._GVarDecl)
        self.assertIsInstance(decls['bar'], GVars._GVarDecl)

#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ 
        Test_module_constants,
        Test__resubst,
        Test_GVarDecl,
        Test_GVarDeclU,
        Test_GVarDecls,
        Test_GVarDeclsU,
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
