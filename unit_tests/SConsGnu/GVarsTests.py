""" SConsGnu.GVarsTest

Unit tests for SConsGnu.GVars
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

from SConsGnu import GVars
from SConsGnu.GVars import GVarDecl, GVarDeclU, GVarDecls, GVarDeclsU
from mock import Mock, patch

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
class Test__GVars(unittest.TestCase):

    @classmethod
    def _gdecls_mock_1(cls):
        # decls0 is a substitute of _GVarDecls instance, with only keys()
        # method defined
        gdecls = Mock(name = 'gdecls0')
        gdecls.keys = Mock(name = 'keys', return_value = ['k','e','y','s'])
        return gdecls

    @classmethod
    def _gdecls_mock_2(cls):
        gdecls = cls._gdecls_mock_1()
        return cls._mock_gdecls_supp_dicts_2(gdecls)

    @classmethod
    def _gdecls_mock_3(cls):
        gdecls = cls._gdecls_mock_1()
        return cls._mock_gdecls_supp_dicts_3(gdecls)

    @classmethod
    def _gdecls_mock_4(cls):
        gdecls = cls._gdecls_mock_1()
        return cls._mock_gdecls_supp_dicts_4(gdecls)

    @classmethod
    def _gdecls_mock_5(cls):
        gdecls = cls._gdecls_mock_1()
        return cls._mock_gdecls_supp_dicts_5(gdecls)

    @classmethod
    def _gvars_mock_4_UpdateEnvironment(cls):
        gv = GVars._GVars(cls._gdecls_mock_1())
        gv.update_env_from_vars = Mock(name = 'update_env_from_vars')
        gv.update_env_from_opts = Mock(name = 'update_env_from_opts')
        return gv

    @classmethod
    def _mock_gdecls_supp_dicts_2(cls, gdecls):
        def get_xxx_rename_dict(xxx):   return "rename_dict[%d]" % xxx
        def get_xxx_resubst_dict(xxx):  return "resubst_dict[%d]" % xxx
        def get_xxx_irename_dict(xxx):  return "irename_dict[%d]" % xxx
        def get_xxx_iresubst_dict(xxx): return "iresubst_dict[%d]" % xxx
        gdecls.get_xxx_rename_dict = Mock(name = 'get_xxx_rename_dict', side_effect = get_xxx_rename_dict)
        gdecls.get_xxx_irename_dict = Mock(name = 'get_xxx_rename_dict', side_effect = get_xxx_irename_dict)
        gdecls.get_xxx_resubst_dict = Mock(name = 'get_xxx_rename_dict', side_effect = get_xxx_resubst_dict)
        gdecls.get_xxx_iresubst_dict = Mock(name = 'get_xxx_iresubst_dict',  side_effect = get_xxx_iresubst_dict)
        return gdecls

    @classmethod
    def _mock_gdecls_supp_dicts_3(cls, gdecls):
        def get_xxx_rename_dict(xxx):   return None
        def get_xxx_resubst_dict(xxx):  return None
        def get_xxx_irename_dict(xxx):  return None
        def get_xxx_iresubst_dict(xxx): return None
        gdecls.get_xxx_rename_dict = Mock(name = 'get_xxx_rename_dict', side_effect = get_xxx_rename_dict)
        gdecls.get_xxx_irename_dict = Mock(name = 'get_xxx_rename_dict', side_effect = get_xxx_irename_dict)
        gdecls.get_xxx_resubst_dict = Mock(name = 'get_xxx_rename_dict', side_effect = get_xxx_resubst_dict)
        gdecls.get_xxx_iresubst_dict = Mock(name = 'get_xxx_iresubst_dict',  side_effect = get_xxx_iresubst_dict)
        return gdecls

    @classmethod
    def _mock_gdecls_supp_dicts_4(cls, gdecls):
        def get_xxx_rename_dict(xxx):
            return  [ {'a' : 'env_a'},    {'a' : 'var_a'},    {'a' : 'opt_a'}    ][xxx]
        def get_xxx_resubst_dict(xxx):
            return  [ {'a' : '${env_a}'}, {'a' : '${var_a}'}, {'a' : '${opt_a}'} ][xxx]
        def get_xxx_irename_dict(xxx):
            return  [ {'env_a' : 'a'},    {'var_a' : 'a'},    {'opt_a' : 'a'}    ][xxx]
        def get_xxx_iresubst_dict(xxx):
            return  [ {'env_a' : '${a}'}, {'var_a' : '${a}'}, {'opt_a' : '${a}'} ][xxx]
        gdecls.get_xxx_rename_dict = Mock(name = 'get_xxx_rename_dict', side_effect = get_xxx_rename_dict)
        gdecls.get_xxx_irename_dict = Mock(name = 'get_xxx_rename_dict', side_effect = get_xxx_irename_dict)
        gdecls.get_xxx_resubst_dict = Mock(name = 'get_xxx_rename_dict', side_effect = get_xxx_resubst_dict)
        gdecls.get_xxx_iresubst_dict = Mock(name = 'get_xxx_iresubst_dict',  side_effect = get_xxx_iresubst_dict)
        return gdecls

    @classmethod
    def _mock_gdecls_supp_dicts_5(cls, gdecls):
        def get_xxx_rename_dict(xxx):
            return  [ 
                {'k' : 'env_k', 'e' : 'env_e', 'y' : 'env_y', 's' : 'env_s'}, 
                {'k' : 'var_k', 'e' : 'var_e', 'y' : 'var_y', 's' : 'var_s'},
                {'k' : 'opt_k', 'e' : 'opt_e', 'y' : 'opt_y', 's' : 'opt_s'}
            ][xxx]
        def get_xxx_resubst_dict(xxx):
            return  [ 
                {'k' : '${env_k}', 'e' : '${env_e}', 'y' : '${env_y}', 's' : '${env_s}'},
                {'k' : '${var_k}', 'e' : '${var_e}', 'y' : '${var_y}', 's' : '${var_s}'},
                {'k' : '${opt_k}', 'e' : '${opt_e}', 'y' : '${opt_y}', 's' : '${opt_s}'}
            ][xxx]
        def get_xxx_irename_dict(xxx):
            return  [
                {'env_k' : 'k', 'env_e' : 'e', 'env_y' : 'y', 'env_s' : 's' },
                {'var_k' : 'k', 'var_e' : 'e', 'var_y' : 'y', 'var_s' : 's' },
                {'opt_k' : 'k', 'opt_e' : 'e', 'opt_y' : 'y', 'opt_s' : 's' }
            ][xxx]
        def get_xxx_iresubst_dict(xxx):
            return  [
                {'env_k' : '${k}','env_e' : '${e}',  'env_y' : '${y}', 'env_s' : '${s}' },
                {'var_k' : '${k}','var_e' : '${e}',  'var_y' : '${y}', 'var_s' : '${s}' },
                {'opt_k' : '${k}','opt_e' : '${e}',  'opt_y' : '${y}', 'opt_s' : '${s}' },
            ][xxx]
        gdecls.get_xxx_rename_dict = Mock(name = 'get_xxx_rename_dict', side_effect = get_xxx_rename_dict)
        gdecls.get_xxx_irename_dict = Mock(name = 'get_xxx_rename_dict', side_effect = get_xxx_irename_dict)
        gdecls.get_xxx_resubst_dict = Mock(name = 'get_xxx_rename_dict', side_effect = get_xxx_resubst_dict)
        gdecls.get_xxx_iresubst_dict = Mock(name = 'get_xxx_iresubst_dict',  side_effect = get_xxx_iresubst_dict)
        return gdecls

    def test___init___1(self):
        """_GVars.__init__(gdecls) should call gdecls.keys() and self.__init_supp_dicts(gdecls)"""
        gdecls = self._gdecls_mock_1()
        with patch.object(GVars._GVars, '_GVars__init_supp_dicts', autospec=True) as mock:
            gv = GVars._GVars(gdecls)
            try:
                mock.assert_called_once_with(gv, gdecls)
                gdecls.keys.assert_called_once_with()
            except AssertionError as e:
                self.fail(str(e))
        self.assertIsInstance(gv, GVars._GVars)
        self.assertEqual(gv._GVars__keys, ['k', 'e', 'y', 's'])

    def test___init___2(self):
        """_GVars.__init__(gdecls) should initialize its iternal dicts"""
        gv = GVars._GVars(self._gdecls_mock_2())
        self.assertEqual(gv._GVars__rename, ['rename_dict[0]', 'rename_dict[1]', 'rename_dict[2]'])
        self.assertEqual(gv._GVars__resubst, ['resubst_dict[0]', 'resubst_dict[1]', 'resubst_dict[2]'])
        self.assertEqual(gv._GVars__irename, ['irename_dict[0]', 'irename_dict[1]', 'irename_dict[2]'])
        self.assertEqual(gv._GVars__iresubst, ['iresubst_dict[0]', 'iresubst_dict[1]', 'iresubst_dict[2]'])


    def test___reset_supp_dicts(self):
        """_GVars.__reset_supp_dicts() should reset internal dicts to {}"""
        gv = GVars._GVars(self._gdecls_mock_2())
        gv._GVars__reset_supp_dicts()
        self.assertEqual(gv._GVars__rename, [{},{},{}])
        self.assertEqual(gv._GVars__resubst, [{},{},{}])
        self.assertEqual(gv._GVars__irename, [{},{},{}])
        self.assertEqual(gv._GVars__iresubst, [{},{},{}])

    def test___init_supp_dicts(self):
        """_GVars.__init_supp_dicts(gdecls) should initialize internal dicts appropriately"""
        gdecls = self._gdecls_mock_3()
        gv = GVars._GVars(gdecls)
        self.assertEqual(gv._GVars__rename, [None, None, None])
        self.assertEqual(gv._GVars__resubst, [None, None, None])
        self.assertEqual(gv._GVars__irename, [None, None, None])
        self.assertEqual(gv._GVars__iresubst, [None, None, None])
        self._mock_gdecls_supp_dicts_2(gdecls)
        gv._GVars__init_supp_dicts(gdecls)
        self.assertEqual(gv._GVars__rename, ['rename_dict[0]', 'rename_dict[1]', 'rename_dict[2]'])
        self.assertEqual(gv._GVars__resubst, ['resubst_dict[0]', 'resubst_dict[1]', 'resubst_dict[2]'])
        self.assertEqual(gv._GVars__irename, ['irename_dict[0]', 'irename_dict[1]', 'irename_dict[2]'])
        self.assertEqual(gv._GVars__iresubst, ['iresubst_dict[0]', 'iresubst_dict[1]', 'iresubst_dict[2]'])

    def XxxEnvProxy_test(self, x):
        gv = GVars._GVars(self._gdecls_mock_4())
        env = { 'env_a' : 'A', 'env_b' : 'B'}
        with patch('SConsGnu.GVars._GVarsEnvProxy', return_value = 'ok') as ProxyClass:
            if x == 'var_':
                proxy = gv.VarEnvProxy(env)
            elif x == 'opt_':
                proxy = gv.OptEnvProxy(env)
            else:
                proxy = gv.EnvProxy(env)

            try:
                ProxyClass.assert_called_once_with(env, { '%sa' % x : 'env_a' }, {'%sa' % x : '${env_a}'}, {'env_a' : '%sa' % x}, {'env_a' : '${%sa}' % x})
            except AssertionError as e:
                self.fail(str(e))
            self.assertEqual(proxy, 'ok')

    def test_VarEnvProxy(self):
        """_GVars(gdecls).VarEnvProxy(env) should _GVarsEnvProxy() with appropriate arguments"""
        self.XxxEnvProxy_test('var_')

    def test_OptEnvProxy(self):
        """_GVars(gdecls).OptEnvProxy(env) should _GVarsEnvProxy() with appropriate arguments"""
        self.XxxEnvProxy_test('opt_')

    def test_EnvProxy(self):
        """_GVars(gdecls).EnvProxy(env) should _GVarsEnvProxy() with appropriate arguments"""
        self.XxxEnvProxy_test('')

    def test_get_keys(self):
        """_GVars(gdecls).get_keys() should return attribute __keys"""
        gv = GVars._GVars(self._gdecls_mock_1())
        self.assertEqual(gv.get_keys(), ['k','e','y','s'])
        # expect a copy of __keys, not __keys
        self.assertIsNot(gv.get_keys(), gv._GVars__keys)

    def test_get_xxx_key_ENV_x(self):
        """_GVars(gdecls).get_xxx_key(ENV, 'x') should be raise KeyError"""
        gv = GVars._GVars(self._gdecls_mock_4())
        with self.assertRaises(KeyError):
            gv.get_xxx_key(GVars.ENV, 'x')

    def test_get_xxx_key_VAR_x(self):
        """_GVars(gdecls).get_xxx_key(VAR, 'x') should be raise KeyError"""
        gv = GVars._GVars(self._gdecls_mock_4())
        with self.assertRaises(KeyError):
            gv.get_xxx_key(GVars.VAR, 'x')

    def test_get_xxx_key_OPT_x(self):
        """_GVars(gdecls).get_xxx_key(OPT, 'x') should be raise KeyError"""
        gv = GVars._GVars(self._gdecls_mock_4())
        with self.assertRaises(KeyError):
            gv.get_xxx_key(GVars.OPT, 'x')

    def test_get_xxx_key_123_a(self):
        """_GVars(gdecls).get_xxx_key(123, 'a') should be raise KeyError"""
        gv = GVars._GVars(self._gdecls_mock_4())
        with self.assertRaises(IndexError):
            gv.get_xxx_key(123, 'a')

    def test_get_xxx_key_ENV_a(self):
        """_GVars(gdecls).get_xxx_key(ENV, 'a') should == 'env_a'"""
        gv = GVars._GVars(self._gdecls_mock_4())
        self.assertEqual(gv.get_xxx_key(GVars.ENV, 'a'), 'env_a')

    def test_get_xxx_key_VAR_a(self):
        """_GVars(gdecls).get_xxx_key(VAR, 'a') should == 'var_a'"""
        gv = GVars._GVars(self._gdecls_mock_4())
        self.assertEqual(gv.get_xxx_key(GVars.VAR, 'a'), 'var_a')

    def test_get_xxx_key_OPT_a(self):
        """_GVars(gdecls).get_xxx_key(OPT, 'a') should == 'opt_a'"""
        gv = GVars._GVars(self._gdecls_mock_4())
        self.assertEqual(gv.get_xxx_key(GVars.OPT, 'a'), 'opt_a')

    def test_env_key_x(self):
        """_GVars(gdecls).env_key('x') should raise KeyError"""
        gv = GVars._GVars(self._gdecls_mock_4())
        with self.assertRaises(KeyError):
            gv.env_key('x')

    def test_env_key_a(self):
        """_GVars(gdecls).env_key('a') should == 'env_a'"""
        gv = GVars._GVars(self._gdecls_mock_4())
        self.assertEqual(gv.env_key('a'), 'env_a')

    def test_var_key_x(self):
        """_GVars(gdecls).var_key('x') should raise KeyError"""
        gv = GVars._GVars(self._gdecls_mock_4())
        with self.assertRaises(KeyError):
            gv.var_key('x')

    def test_var_key_a(self):
        """_GVars(gdecls).var_key('a') should == 'var_a'"""
        gv = GVars._GVars(self._gdecls_mock_4())
        self.assertEqual(gv.var_key('a'), 'var_a')

    def test_opt_key_x(self):
        """_GVars(gdecls).opt_key('x') should raise KeyError"""
        gv = GVars._GVars(self._gdecls_mock_4())
        with self.assertRaises(KeyError):
            gv.opt_key('x')

    def test_opt_key_a(self):
        """_GVars(gdecls).opt_key('a') should == 'opt_a'"""
        gv = GVars._GVars(self._gdecls_mock_4())
        self.assertEqual(gv.opt_key('a'), 'opt_a')

    def test_update_env_from_vars_1(self):
        """_GVars(gdecls).update_env_from_vars('env', variables)"""
        def VarEnvProxy(arg): return 'var_%s_proxy' % arg
        gv = GVars._GVars(self._gdecls_mock_1())
        gv.VarEnvProxy = Mock(name = 'VarEnvProxy', side_effect = VarEnvProxy)
        variables = Mock(name = 'variables')
        variables.Update = Mock(name = 'Update')
        gv.update_env_from_vars('env', variables)
        try:
            variables.Update.assert_called_once_with('var_env_proxy', None)
        except AssertionError as e:
            self.fail(str(e))

    def test_update_env_from_vars_2(self):
        """_GVars(gdecls).update_env_from_vars('env', variables, 'arg')"""
        def VarEnvProxy(arg): return 'var_%s_proxy' % arg
        gv = GVars._GVars(self._gdecls_mock_1())
        gv.VarEnvProxy = Mock(name = 'VarEnvProxy', side_effect = VarEnvProxy)
        variables = Mock('variables')
        variables.Update = Mock(name = 'Update')
        gv.update_env_from_vars('env', variables, 'arg')
        try:
            variables.Update.assert_called_once_with('var_env_proxy', 'arg')
        except AssertionError as e:
            self.fail(str(e))

    def test_update_env_from_opts_1(self):
        """_GVars(gdecls).update_env_from_opts('env')"""
        proxy = { 'env1' : {} }
        def OptEnvProxy(arg): return proxy[arg]
        gv = GVars._GVars(self._gdecls_mock_4())
        gv.OptEnvProxy = Mock(name = 'OptEnvProxy', side_effect = OptEnvProxy)
        with patch('SCons.Script.Main.GetOption', side_effect = lambda key : 'val_%s' % key) as GetOption:
            gv.update_env_from_opts('env1')
            try:
                GetOption.assert_called_once_with('opt_a')
            except AssertionError as e:
                self.fail(str(e))
            self.assertEqual(proxy['env1']['opt_a'], 'val_opt_a')

    def test_UpdateEnvironment_1(self):
        """_GVars(gdecls).UpdateEnvironment('env') never calls update_env_from_{vars,opts}"""
        gv = self._gvars_mock_4_UpdateEnvironment()
        gv.UpdateEnvironment('env')
        try:
            gv.update_env_from_vars.assert_never_called()
            gv.update_env_from_opts.assert_never_called()
        except AssertionError as e:
            self.fail(str(e))

    def test_UpdateEnvironment_2(self):
        """_GVars(gdecls).UpdateEnvironment('env','variables1') calls update_env_from_vars('env', 'variables1') once"""
        gv = self._gvars_mock_4_UpdateEnvironment()
        gv.UpdateEnvironment('env', 'variables1')
        try:
            gv.update_env_from_vars.assert_called_once_with('env', 'variables1', None)
            gv.update_env_from_opts.assert_never_called()
        except AssertionError as e:
            self.fail(str(e))

    def test_UpdateEnvironment_3(self):
        """_GVars(gdecls).UpdateEnvironment('env',None,True) calls update_env_from_opts('env') once"""
        gv = self._gvars_mock_4_UpdateEnvironment()
        gv.UpdateEnvironment('env', None, True)
        try:
            gv.update_env_from_vars.assert_never_called()
            gv.update_env_from_opts.assert_called_once_with('env')
        except AssertionError as e:
            self.fail(str(e))

    def test_UpdateEnvironment_4(self):
        """_GVars(gdecls).UpdateEnvironment('env','variables1',True) calls update_env_from_{opts,vars} once"""
        gv = self._gvars_mock_4_UpdateEnvironment()
        gv.UpdateEnvironment('env', 'variables1', True)
        try:
            gv.update_env_from_vars.assert_called_once_with('env', 'variables1', None)
            gv.update_env_from_opts.assert_called_once_with('env')
        except AssertionError as e:
            self.fail(str(e))

    def test_SaveVariables(self):
        """_GVars(gdecls).SaveVariables(variables, 'filename1', 'env1')"""
        def VarEnvProxy(arg): return 'var_%s_proxy' % arg
        gv = GVars._GVars(self._gdecls_mock_1())
        gv.VarEnvProxy = Mock(name = 'VarEnvProxy', side_effect = VarEnvProxy)
        variables = Mock(name = 'variables')
        variables.Save = Mock(name = 'Save')
        gv.SaveVariables(variables, 'filename1', 'env1')
        try:
            variables.Save.assert_called_once_with('filename1','var_env1_proxy')
        except AssertionError as e:
            self.fail(str(e))

    def test_GenerateVariablesHelpText_1(self):
        """_GVars(gdecls).GenerateVariablesHelpText(variables, 'env1')"""
        def VarEnvProxy(arg): return 'var_%s_proxy' % arg
        gv = GVars._GVars(self._gdecls_mock_1())
        gv.VarEnvProxy = Mock(name = 'VarEnvProxy', side_effect = VarEnvProxy)
        variables = Mock(name = 'variables')
        variables.GenerateHelpText = Mock(name = 'GenerateHelpText')
        gv.GenerateVariablesHelpText(variables, 'env1')
        try:
            variables.GenerateHelpText.assert_called_once_with('var_env1_proxy')
        except AssertionError as e:
            self.fail(str(e))

    def test_GenerateVariablesHelpText_2(self):
        """_GVars(gdecls).GenerateVariablesHelpText(variables, 'env1', 'arg1', 'arg2')"""
        def VarEnvProxy(arg): return 'var_%s_proxy' % arg
        gv = GVars._GVars(self._gdecls_mock_1())
        gv.VarEnvProxy = Mock(name = 'VarEnvProxy', side_effect = VarEnvProxy)
        variables = Mock(name = 'variables')
        variables.GenerateHelpText = Mock(name = 'GenerateHelpText')
        gv.GenerateVariablesHelpText(variables, 'env1', 'arg1', 'arg2')
        try:
            variables.GenerateHelpText.assert_called_once_with('var_env1_proxy', 'arg1', 'arg2')
        except AssertionError as e:
            self.fail(str(e))

    def test_GetCurrentValues_1(self):
        """_GVars(gdecls).GetCurrentValues(env) works as expected"""
        gv = GVars._GVars(self._gdecls_mock_5())
        env = { 'env_k' : 'K', 'env_e' : 'E', 'env_x' : 'X' }
        current = gv.GetCurrentValues(env)
        self.assertIs(current['env_k'], env['env_k'])
        self.assertIs(current['env_e'], env['env_e'])
        self.assertEqual(current, {'env_k' : 'K', 'env_e' : 'E'})


#############################################################################
class Test__GVarDecl(unittest.TestCase):
    # TODO: Write unit tests for _GVarDecl class (see GH issue #1)
    pass

#############################################################################
class Test__GVarDecls(unittest.TestCase):
    # TODO: Write unit tests for _GVarDecls class (see GH issue #1)
    pass

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
               , Test__GVars
               , Test__GVarDecl
               , Test__GVarDecls
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
