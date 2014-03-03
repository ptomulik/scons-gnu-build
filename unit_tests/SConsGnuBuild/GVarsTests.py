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
from mock import Mock

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
class Test__invert_dict(unittest.TestCase):
    def test__invert_dict_1(self):
        """_invert_dict({}) should == {}"""
        self.assertEqual(GVars._invert_dict({}), {})
    def test__invert_dict_2(self):
        """_invert_dict({ 'x' : 'y' }) should == { 'y' : 'x'}"""
        self.assertEqual(GVars._invert_dict({'x' : 'y'}), { 'y' : 'x'})
    def test__invert_dict_3(self):
        """_invert_dict({ 'v' : 'w', 'x' : 'y' }) should == { 'w' : 'v', 'y' : 'x'}"""
        self.assertEqual(GVars._invert_dict({'v' : 'w', 'x' : 'y'}), { 'w' : 'v', 'y' : 'x'})

#############################################################################
class Test__GVarsEnvProxy(unittest.TestCase):
    def test___init___1(self):
        """_GVarsEnvProxy.__init__(env) should set default attributes"""
        env = 'env'
        proxy = GVars._GVarsEnvProxy(env)
        self.assertIs(proxy.env, env)
        self.assertEqual(proxy._GVarsEnvProxy__rename, {})
        self.assertEqual(proxy._GVarsEnvProxy__irename, {})
        self.assertEqual(proxy._GVarsEnvProxy__resubst, {})
        self.assertEqual(proxy._GVarsEnvProxy__iresubst, {})
        self.assertEqual(proxy.is_strict(), False)

    def test___init___2(self):
        """_GVarsEnvProxy.__init__(env, arg1, arg2, arg3, arg4, True) should set attributes"""
        env = 'env'
        arg1, arg2, arg3, arg4 = 'arg1', 'arg2', 'arg3', 'arg4'
        proxy = GVars._GVarsEnvProxy(env, arg1, arg2, arg3, arg4, True)
        self.assertIs(proxy.env, env)
        self.assertIs(proxy._GVarsEnvProxy__rename,   arg1)
        self.assertIs(proxy._GVarsEnvProxy__resubst,  arg2)
        self.assertIs(proxy._GVarsEnvProxy__irename,  arg3)
        self.assertIs(proxy._GVarsEnvProxy__iresubst, arg4)
        self.assertIs(proxy.is_strict(), True)

    def test_is_strict(self):
        """Test _GVarsEnvProxy.is_strict()"""
        self.assertIs(GVars._GVarsEnvProxy('env', strict = False).is_strict(), False)
        self.assertIs(GVars._GVarsEnvProxy('env', strict = True).is_strict(), True)

    def test_set_strict_False_calls__setup_methods_False(self):
        """_GVarsEnvProxy.set_strict(False) should call _GVarsEnvProxy.__setup_methods(False)"""
        proxy = GVars._GVarsEnvProxy('env')
        proxy._GVarsEnvProxy__setup_methods = Mock(name = '__setup_methods')
        proxy.set_strict(False)
        try:
            proxy._GVarsEnvProxy__setup_methods.assert_called_with(False)
        except AssertionError as e:
            self.fail(str(e))

    def test_set_strict_True_calls__setup_methods_True(self):
        """_GVarsEnvProxy.set_strict(True) should call _GVarsEnvProxy.__setup_methods(True)"""
        proxy = GVars._GVarsEnvProxy('env')
        proxy._GVarsEnvProxy__setup_methods = Mock(name = '__setup_methods')
        proxy.set_strict(True)
        try:
            proxy._GVarsEnvProxy__setup_methods.assert_called_with(True)
        except AssertionError as e:
            self.fail(str(e))

    def test_set_strict_False(self):
        """_GVarsEnvProxy.is_strict() should be False after _GVarsEnvProxy.set_strict(False)"""
        proxy = GVars._GVarsEnvProxy('env')
        proxy.set_strict(False)
        self.assertIs(proxy.is_strict(), False)

    def test_set_strict_True(self):
        """_GVarsEnvProxy.is_strict() should be True after _GVarsEnvProxy.set_strict(True)"""
        proxy = GVars._GVarsEnvProxy('env')
        proxy.set_strict(True)
        self.assertIs(proxy.is_strict(), True)

    def test___setup_methods_True(self):
        """_GVarsEnvProxy.__setup_methods(True) should setup appropriate methods"""
        proxy = GVars._GVarsEnvProxy('env', strict = False)
        proxy._GVarsEnvProxy__setup_methods(True)
        self.assertEqual(proxy._GVarsEnvProxy__delitem__impl, proxy._GVarsEnvProxy__delitem__strict)
        self.assertEqual(proxy._GVarsEnvProxy__getitem__impl, proxy._GVarsEnvProxy__getitem__strict)
        self.assertEqual(proxy._GVarsEnvProxy__setitem__impl, proxy._GVarsEnvProxy__setitem__strict)
        self.assertEqual(proxy.get, proxy._get_strict)
        self.assertEqual(proxy.has_key, proxy._has_key_strict)
        self.assertEqual(proxy._GVarsEnvProxy__contains__impl, proxy._GVarsEnvProxy__contains__strict)
        self.assertEqual(proxy.items, proxy._items_strict)

    def test___setup_methods_False(self):
        """_GVarsEnvProxy.__setup_methods(False) should setup appropriate methods"""
        proxy = GVars._GVarsEnvProxy('env', strict = True)
        proxy._GVarsEnvProxy__setup_methods(False)
        self.assertEqual(proxy._GVarsEnvProxy__delitem__impl, proxy._GVarsEnvProxy__delitem__nonstrict)
        self.assertEqual(proxy._GVarsEnvProxy__getitem__impl, proxy._GVarsEnvProxy__getitem__nonstrict)
        self.assertEqual(proxy._GVarsEnvProxy__setitem__impl, proxy._GVarsEnvProxy__setitem__nonstrict)
        self.assertEqual(proxy.get, proxy._get_nonstrict)
        self.assertEqual(proxy.has_key, proxy._has_key_nonstrict)
        self.assertEqual(proxy._GVarsEnvProxy__contains__impl, proxy._GVarsEnvProxy__contains__nonstrict)
        self.assertEqual(proxy.items, proxy._items_nonstrict)

    def test___delitem___1(self):
        """_GVarsEnvProxy({'a' : 'A'}).__delitem__('a') should delete item 'a'"""
        env = { 'a' : 'A' }
        GVars._GVarsEnvProxy(env).__delitem__('a')
        self.assertEqual(env, {})

    def test___delitem___2(self):
        """_GVarsEnvProxy({'a' : 'A'}, strict = True).__delitem__('a') should raise KeyError"""
        with self.assertRaises(KeyError):
            GVars._GVarsEnvProxy({'a' : 'A'}, strict = True).__delitem__('a')

    def test___delitem___3(self):
        """_GVarsEnvProxy({'b' : 'B'}, rename = {'a' : 'b'}).__delitem__('a') should delete item 'b'"""
        env = { 'b' : 'B' }
        GVars._GVarsEnvProxy(env, rename = { 'a' : 'b'}).__delitem__('a')
        self.assertEqual(env, {})

    def test___delitem___4(self):
        """_GVarsEnvProxy({'b' : 'B'}, rename = {'a' : 'b'}, strict = True).__delitem__('a') should delete item 'b'"""
        env = { 'b' : 'B' }
        GVars._GVarsEnvProxy(env, rename = { 'a' : 'b'}, strict = True).__delitem__('a')
        self.assertEqual(env, {})

    def test___getitem___1(self):
        """_GVarsEnvProxy({'a' : 'A'}).__getitem__('a') should return 'A'"""
        env = { 'a' : 'A' }
        self.assertEqual(GVars._GVarsEnvProxy({'a' : 'A'}).__getitem__('a'), 'A')

    def test___getitem___2(self):
        """_GVarsEnvProxy({'a' : 'A'}, strict = True).__getitem__('a') should raise KeyError"""
        with self.assertRaises(KeyError):
            GVars._GVarsEnvProxy({'a' : 'A'}, strict = True).__getitem__('a')

    def test__getitem___3(self):
        """_GVarsEnvProxy({'b' : 'B'}, rename = {'a' : 'b'}).__getitem__('a') should return 'B'"""
        self.assertEqual(GVars._GVarsEnvProxy({'b' : 'B'}, rename = {'a' : 'b'}).__getitem__('a'), 'B')

    def test___getitem___4(self):
        """_GVarsEnvProxy({'b' : 'B'}, rename = {'a' : 'b'}, strict = True).__getitem__('a') should return 'B'"""
        self.assertEqual(GVars._GVarsEnvProxy({'b' : 'B'}, rename = {'a' : 'b'}, strict = True).__getitem__('a'), 'B')

    def test__setitem___1(self):
        """_GVarsEnvProxy({}).__setitem__('a', 'A') should set item 'a' to 'A'"""
        proxy = GVars._GVarsEnvProxy({})
        proxy.__setitem__('a', 'A')
        self.assertEqual(proxy['a'], 'A')

    def test___setitem___2(self):
        """_GVarsEnvProxy({'a' : 'B'}).__setitem__('a', 'A') should set item 'a' to 'A'"""
        env = {'a' : 'B'}
        proxy = GVars._GVarsEnvProxy(env)
        proxy.__setitem__('a', 'A')
        self.assertEqual(env['a'], 'A')

    def test__setitem___3(self):
        """_GVarsEnvProxy({'a' : 'B'}, rename = { 'a' : 'a' }, strict = True).__setitem__('a', 'A') should set item 'a' to 'A'"""
        env = {'a' : 'B'}
        proxy = GVars._GVarsEnvProxy(env, rename = { 'a' : 'a' }, strict = True)
        proxy.__setitem__('a', 'A')
        self.assertEqual(env['a'], 'A')

    def test___setitem___4(self):
        """_GVarsEnvProxy({'a' : 'B'}, strict = True).__setitem__('a', 'A') should raise KeyError"""
        env = {'a' : 'B'}
        proxy = GVars._GVarsEnvProxy(env, strict = True)
        with self.assertRaises(KeyError):
            proxy.__setitem__('a', 'A')
        self.assertEqual(env['a'], 'B')

    def test_get_1(self):
        """_GVarsEnvProxy({'a' : 'A'}).get('a') should return 'A'"""
        self.assertEqual(GVars._GVarsEnvProxy({'a' : 'A'}).get('a'), 'A')

    def test_get_2(self):
        """_GVarsEnvProxy({'a' : 'A'}).get('b') should return None"""
        self.assertEqual(GVars._GVarsEnvProxy({'a' : 'A'}).get('b'), None)

    def test_get_3(self):
        """_GVarsEnvProxy({'a' : 'A'}, rename = { 'b' : 'a' }).get('b') should return 'A'"""
        self.assertEqual(GVars._GVarsEnvProxy({'a' : 'A'}, rename = { 'b' : 'a'}).get('b'), 'A')

    def test_get_4(self):
        """_GVarsEnvProxy({'a' : 'A'}, rename = { 'b' : 'a' }).get('a') should return 'A'"""
        self.assertEqual(GVars._GVarsEnvProxy({'a' : 'A'}, rename = { 'b' : 'a'}).get('a'), 'A')

    def test_get_5(self):
        """_GVarsEnvProxy({'a' : 'A'}, strict = True).get('a') should raise KeyError"""
        with self.assertRaises(KeyError):
            GVars._GVarsEnvProxy({'a' : 'A'}, strict = True).get('a')

    def test_get_6(self):
        """_GVarsEnvProxy({'a' : 'A'}, rename = { 'b' : 'a' }, strict = True).get('b') should return 'A'"""
        self.assertEqual(GVars._GVarsEnvProxy({'a' : 'A'}, rename = { 'b' : 'a' }, strict = True).get('b'), 'A')

    def test_has_key_1(self):
        """_GVarsEnvProxy({'a' : 'A'}).has_key('a') should return True"""
        self.assertTrue(GVars._GVarsEnvProxy({'a' : 'A'}).has_key('a'))

    def test_has_key_2(self):
        """_GVarsEnvProxy({'a' : 'A'}).has_key('b') should return False"""
        self.assertFalse(GVars._GVarsEnvProxy({'a' : 'A'}).has_key('b'))

    def test_has_key_3(self):
        """_GVarsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}).has_key('a') should return True"""
        self.assertTrue(GVars._GVarsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}).has_key('a'))

    def test_has_key_4(self):
        """_GVarsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}).has_key('b') should return True"""
        self.assertTrue(GVars._GVarsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}).has_key('b'))

    def test_has_key_5(self):
        """_GVarsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).has_key('a') should return False"""
        self.assertFalse(GVars._GVarsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).has_key('a'))

    def test_has_key_6(self):
        """_GVarsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).has_key('b') should return True"""
        self.assertTrue(GVars._GVarsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).has_key('b'))

    def test_has_key_7(self):
        """_GVarsEnvProxy({'a' : 'A'}, rename = {'b' : 'c'}, strict = True).has_key('b') should return False"""
        self.assertFalse(GVars._GVarsEnvProxy({'a' : 'A'}, rename = {'b' : 'c'}, strict = True).has_key('b'))

    def test___contains___1(self):
        """_GVarsEnvProxy({'a' : 'A'}).__contains__('a') should return True"""
        self.assertTrue(GVars._GVarsEnvProxy({'a' : 'A'}).__contains__('a'))

    def test___contains___2(self):
        """_GVarsEnvProxy({'a' : 'A'}).__contains__('b') should return False"""
        self.assertFalse(GVars._GVarsEnvProxy({'a' : 'A'}).__contains__('b'))

    def test___contains___3(self):
        """_GVarsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}).__contains__('a') should return True"""
        self.assertTrue(GVars._GVarsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}).__contains__('a'))

    def test___contains___4(self):
        """_GVarsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}).__contains__('b') should return True"""
        self.assertTrue(GVars._GVarsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}).__contains__('b'))

    def test___contains___5(self):
        """_GVarsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).__contains__('a') should return False"""
        self.assertFalse(GVars._GVarsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).__contains__('a'))

    def test___contains___6(self):
        """_GVarsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).__contains__('b') should return True"""
        self.assertTrue(GVars._GVarsEnvProxy({'a' : 'A'}, rename = {'b' : 'a'}, strict = True).__contains__('b'))

    def test___contains___7(self):
        """_GVarsEnvProxy({'a' : 'A'}, rename = {'b' : 'c'}, strict = True).__contains__('b') should return False"""
        self.assertFalse(GVars._GVarsEnvProxy({'a' : 'A'}, rename = {'b' : 'c'}, strict = True).__contains__('b'))

    def test_items_1(self):
        """_GVarsEnvProxy({'a' : 'A', 'b' : 'B'}).items() should be [('a', 'A'), ('b', 'B')]"""
        self.assertEqual(GVars._GVarsEnvProxy({'a' : 'A', 'b' : 'B'}).items(), ([('a', 'A'), ('b', 'B')]))

    def test_items_2(self):
        """_GVarsEnvProxy({'a' : 'A', 'b' : 'B'}, irename = {'a' : 'c'}).items() should be [('c', 'A'), ('b', 'B')]"""
        self.assertEqual(GVars._GVarsEnvProxy({'a' : 'A', 'b' : 'B'}, irename = { 'a' : 'c'}).items(), ([('c', 'A'), ('b', 'B')]))

    def test_items_3(self):
        """_GVarsEnvProxy({'a' : 'A', 'b' : 'B'}, rename = {'c' : 'a'}, strict = True).items() should be [('c', 'A')]"""
        self.assertEqual(GVars._GVarsEnvProxy({'a' : 'A', 'b' : 'B'}, rename = { 'c' : 'a'}, strict = True).items(), ([('c', 'A')]))

    def test_items_4(self):
        """_GVarsEnvProxy({'a' : '${a}'}, irename = {'a' : 'b'}, iresubst = {'a' : '${b}'}).items() should be [('b', '${b}')]"""
        self.assertEqual(GVars._GVarsEnvProxy({'a' : '${a}'}, irename = {'a' : 'b'}, iresubst = {'a' : '${b}'}).items(), [('b', '${b}')])

    def test_items_5(self):
        """_GVarsEnvProxy({'a' : 'a'}, irename = {'a' : 'b'}, iresubst = {'a' : '${b}'}).items() should be [('b', 'a')]"""
        self.assertEqual(GVars._GVarsEnvProxy({'a' : 'a'}, irename = {'a' : 'b'}, iresubst = {'a' : '${b}'}).items(), [('b', 'a')])
    
    def test_subst_1(self):
        """_GVarsEnvProxy(env).subst('${a} ${b}') should call env.subst('${a} ${b}')"""
        env = Mock(name = 'env')
        env.subst = Mock(name = 'env.subst')
        GVars._GVarsEnvProxy(env).subst('${a} ${b}')
        try:
            env.subst.assert_called_with('${a} ${b}')
        except AssertionError as e:
            self.fail(str(e))

    def test_subst_2(self):
        """_GVarsEnvProxy(env, resubst = {'b' : '${c}}).subst('${a} ${b}') should call env.subst('${a} ${c}')"""
        env = Mock(name = 'env')
        env.subst = Mock(name = 'env.subst')
        GVars._GVarsEnvProxy(env, resubst = {'b' : '${c}'}).subst('${a} ${b}')
        try:
            env.subst.assert_called_with('${a} ${c}')
        except AssertionError as e:
            self.fail(str(e))



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
    tclasses = [ Test_module_constants
               , Test__resubst
               , Test__build_resubst_dict
               , Test__build_iresubst_dict
               , Test__compose_dicts
               , Test__invert_dict
               , Test__GVarsEnvProxy
               , Test_GVarDecl
               , Test_GVarDeclU
               , Test_GVarDecls ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
