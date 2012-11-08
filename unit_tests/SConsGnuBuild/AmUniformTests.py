"""unittest.SConsGnuBuild.AmUniformTests

Unit tests for SConsGnuBuild.AmUniform
"""

__docformat__ = "restructuredText"

#
# Copyright (c) 2012 by Pawel Tomulik
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
from SConsGnuBuild.AmUniform import *

#############################################################################
class Test_std_primary_names(unittest.TestCase):

    def test_no_duplicates(self):
        "No duplicates in StandaredPrimaryNames()"
        self.assertEqual(len(set(StandardPrimaryNames())),
                         len(StandardPrimaryNames()))

#############################################################################
class Test_std_main_prefixes(unittest.TestCase):

    def test_no_duplicates(self):
        "No duplicates in StandaredMainPrefixes()"
        self.assertEqual(len(set(StandardMainPrefixes())),
                         len(StandardMainPrefixes()))

#############################################################################
class Test_std_add_prefixes(unittest.TestCase):

    def test_no_duplicates(self):
        "No duplicates in StandaredAddPrefixes()"
        self.assertEqual(len(set(StandardAddPrefixes())),
                         len(StandardAddPrefixes()))

#############################################################################
class Test_std_primary_main_prefixes(unittest.TestCase):

    def test_all_primary_names_covered(self):
        "All StandardPrimaryNames() appear in StandardPrimaryMainPrefixes()"
        for primary in StandardPrimaryNames():
            self.assertIn(primary,StandardPrimaryMainPrefixes())
            self.assertTrue(StandardPrimaryMainPrefixes(primary),[])

    def test_all_main_prefixes_covered(self):
        "All StandardMainPrefixes() appear in StandardPrimaryMainPrefixes()"
        prefixes_left = StandardMainPrefixes()
        for primary in StandardPrimaryNames():
            allowed = StandardPrimaryMainPrefixes(primary)
            prefixes_left = [ x for x in prefixes_left if x not in allowed ]
        self.assertEqual(prefixes_left, [])

    def test_all_primary_main_prefixes_defined(self):
        "All StandardPrimaryMainPrefixes(*) are from StandardMainPrefixes()"
        known = StandardMainPrefixes()
        unknown_prefixes = []
        for primary in StandardPrimaryNames():
            prefixes = StandardPrimaryMainPrefixes(primary)
            unknown_prefixes.extend([ x for x in prefixes if x not in known])
        self.assertEqual(unknown_prefixes, [])
            
#############################################################################
class Test_rsplit_longest_suffix(unittest.TestCase):
    
    def test_some(self):
        "rsplit_longest_suffix() works for few canonical samples."
        fixtures = [
            (   'nobase_include',
                          ['foo',
                    'se_include',
                       'include'],
             ('nobase','include')
            ),

            (          'foo_bar',
                         ['tuvw',
                           'xyz'],
                      ('foo_bar',None)
            ),

            ('nodist_my_fooexec',
                      ['fooexec',
                    'my_fooexec',
                 'st_my_fooexec'],
          ('nodist','my_fooexec')
            ),

            (          'foo_bar',
                          ['bar',
                       'foo_bar'],
                 (None,'foo_bar')
            ),
            (         '_foo_bar',
                          ['bar',
                       'foo_bar'],
                 (None,'foo_bar')
            )
        ]
        for fixture in fixtures:
            result = rsplit_longest_suffix(fixture[0],fixture[1])
            self.assertEqual(result ,fixture[2], 
              "rsplit_longest_suffix(%r, %r) returned %r but we expected %r" 
              % (fixture[0],fixture[1], result, fixture[2]))

#############################################################################
class Test_rsplit_xxx_Base(unittest.TestCase):
    
    def setUp(self):
        self.defined_xxx_fixtures = [
            ['bleah',         ['bleah'],                     (None, 'bleah')],
            ['bleah',         ['one', 'bleah'],              (None, 'bleah')],
            ['bleah',         ['bleah', 'one', 'seven'],     (None, 'bleah')],
            ['bleah',         ['seven', 'bleah', 'one'],     (None, 'bleah')],
            ['bleah',         ['one', 'seven', 'bleah'],     (None, 'bleah')],
            ['_bleah',        ['bleah'],                     (None, 'bleah')],
            ['_bleah',        ['one', 'bleah'],              (None, 'bleah')],
            ['_bleah',        ['bleah', 'one', 'seven'],     (None, 'bleah')],
            ['_bleah',        ['seven', 'bleah', 'one'],     (None, 'bleah')],
            ['_bleah',        ['one', 'seven', 'bleah'],     (None, 'bleah')],
            ['bar_bleah',     ['bleah'],                    ('bar', 'bleah')],
            ['bar_bleah',     ['one', 'bleah'],             ('bar', 'bleah')],
            ['bar_bleah',     ['bleah', 'one', 'seven'],    ('bar', 'bleah')],
            ['bar_bleah',     ['seven', 'bleah', 'one'],    ('bar', 'bleah')],
            ['bar_bleah',     ['one', 'seven', 'bleah'],    ('bar', 'bleah')],
            ['foo_bar_bleah', ['bleah'],                ('foo_bar', 'bleah')],
            ['foo_bar_bleah', ['one', 'bleah'],         ('foo_bar', 'bleah')],
            ['foo_bar_bleah', ['bleah', 'one', 'seven'],('foo_bar', 'bleah')],
            ['foo_bar_bleah', ['seven', 'bleah', 'one'],('foo_bar', 'bleah')],
            ['foo_bar_bleah', ['one', 'seven', 'bleah'],('foo_bar', 'bleah')],

            ['bl_eh',        ['bl_eh'],                     (None, 'bl_eh')],
            ['bl_eh',        ['one', 'bl_eh'],              (None, 'bl_eh')],
            ['bl_eh',        ['bl_eh', 'one', 'seven'],     (None, 'bl_eh')],
            ['bl_eh',        ['seven', 'bl_eh', 'one'],     (None, 'bl_eh')],
            ['bl_eh',        ['one', 'seven', 'bl_eh'],     (None, 'bl_eh')],
            ['_bl_eh',       ['bl_eh'],                     (None, 'bl_eh')],
            ['_bl_eh',       ['one', 'bl_eh'],              (None, 'bl_eh')],
            ['_bl_eh',       ['bl_eh', 'one', 'seven'],     (None, 'bl_eh')],
            ['_bl_eh',       ['seven', 'bl_eh', 'one'],     (None, 'bl_eh')],
            ['_bl_eh',       ['one', 'seven', 'bl_eh'],     (None, 'bl_eh')],
            ['bar_bl_eh',    ['bl_eh'],                    ('bar', 'bl_eh')],
            ['bar_bl_eh',    ['one', 'bl_eh'],             ('bar', 'bl_eh')],
            ['bar_bl_eh',    ['bl_eh', 'one', 'seven'],    ('bar', 'bl_eh')],
            ['bar_bl_eh',    ['seven', 'bl_eh', 'one'],    ('bar', 'bl_eh')],
            ['bar_bl_eh',    ['one', 'seven', 'bl_eh'],    ('bar', 'bl_eh')],
            ['foo_bar_bl_eh',['bl_eh'],                ('foo_bar', 'bl_eh')],
            ['foo_bar_bl_eh',['one', 'bl_eh'],         ('foo_bar', 'bl_eh')],
            ['foo_bar_bl_eh',['bl_eh', 'one', 'seven'],('foo_bar', 'bl_eh')],
            ['foo_bar_bl_eh',['seven', 'bl_eh', 'one'],('foo_bar', 'bl_eh')],
            ['foo_bar_bl_eh',['one', 'seven', 'bl_eh'],('foo_bar', 'bl_eh')],
        ]
        self.undefined_xxx_fixtures = [
            ['bleah',            None,               ('bleah', None)],
            ['bleah',            [],                 ('bleah', None)],
            ['bleah',            ['one'],            ('bleah', None)],
            ['bleah',            ['one', 'seven'],   ('bleah',None)],
            ['_bleah',           None,               ('_bleah', None)],
            ['_bleah',           [],                 ('_bleah', None)],
            ['_bleah',           ['one'],            ('_bleah', None)],
            ['_bleah',           ['one', 'seven'],   ('_bleah', None)],
            ['bar_bleah',        None,               ('bar_bleah', None)],
            ['bar_bleah',        [],                 ('bar_bleah', None)],
            ['bar_bleah',        ['one'],            ('bar_bleah', None)],
            ['bar_bleah',        ['one', 'seven'],   ('bar_bleah', None)],
            ['foo_bar_bleah',    None,               ('foo_bar_bleah', None)],
            ['foo_bar_bleah',    [],                 ('foo_bar_bleah', None)],
            ['foo_bar_bleah',    ['one'],            ('foo_bar_bleah', None)],
            ['foo_bar_bleah',    ['one', 'seven'],   ('foo_bar_bleah', None)],
        ]

        
#############################################################################
class Test_rsplit_primary_name(Test_rsplit_xxx_Base):

    def test_split_all_std_primaries(self):
        "rsplit_primary_name() splits-out all standard primaries"
        for primary in StandardPrimaryNames():
            for main_prefix in StandardPrimaryMainPrefixes(primary):
                for add_prefix in StandardAddPrefixes():
                    expected = ('_'.join([add_prefix, main_prefix]), primary)
                    funame = '_'.join([add_prefix, main_prefix, primary])
                    result1 = rsplit_primary_name(funame)
                    result2 = RSplitPrimaryName(funame)
                    self.assertEqual(result1, expected, 
                        "rsplit_primary_name(%r) returned %r but we " \
                        "expected %r" % (funame,result1,expected))
                    self.assertEqual(result2, expected, 
                        "RSplitPrimaryName(%r) returned %r but we " \
                        "expected %r" % (funame,result2,expected))

    def test_split_defined_primaries(self):
        "rsplit_primary_name() splits-out primaries defined by user"
        for fixture in self.defined_xxx_fixtures:
            result1 = rsplit_primary_name(fixture[0],fixture[1])
            result2 = RSplitPrimaryName(fixture[0], primary_names = fixture[1])
            expected = fixture[2]
            self.assertEqual(result1, expected,
                "rsplit_primary_name(%r,%r) returned %r but we expected %r" \
                % (fixture[0],fixture[1],result1,expected))
            self.assertEqual(result1, expected,
                "RSplitPrimaryName(%r,primary_names=%r) returned %r but we " \
                "expected %r" % (fixture[0],fixture[1],result2,expected))

    def test_dont_split_undefined_primaries(self):
        "rsplit_primary_name() doesn't split-out primaries it doesn't know"
        for fixture in self.undefined_xxx_fixtures:
            result1 = rsplit_primary_name(fixture[0],fixture[1])
            result2 = RSplitPrimaryName(fixture[0], primary_names = fixture[1])
            expected = fixture[2]
            self.assertEqual(result1, expected,
                "rsplit_primary_name(%r,%r) returned %r but we expected %r" \
                % (fixture[0],fixture[1],result1,expected))
            self.assertEqual(result1, expected,
                "RSplitPrimaryName(%r,primary_names=%r) returned %r but we " \
                "expected %r" % (fixture[0],fixture[1],result2,expected))
            
#############################################################################
class Test_rsplit_main_prefix(Test_rsplit_xxx_Base):

    def test_split_all_std_main_prefixes(self):
        "rsplit_main_prefix() splits-out all standard main prefixes"
        for main_prefix in StandardMainPrefixes():
            for add_prefix in StandardAddPrefixes():
                expected = (add_prefix, main_prefix)
                uname = '_'.join([add_prefix, main_prefix])
                result1 = rsplit_main_prefix(uname)
                result2 = RSplitMainPrefix(uname)
                self.assertEqual(result1, expected, 
                    "rsplit_main_prefix(%r) returned %r but we " \
                    "expected %r" % (uname,result1,expected))
                self.assertEqual(result2, expected, 
                    "RSplitMainPrefix(%r) returned %r but we " \
                    "expected %r" % (uname,result2,expected))

    def test_split_defined_main_prefixes(self):
        "rsplit_main_prefix() splits-out all main prefixes predefined by user"
        for fixture in self.defined_xxx_fixtures:
            result1 = rsplit_main_prefix(fixture[0],fixture[1])
            result2 = RSplitMainPrefix(fixture[0], main_prefixes = fixture[1])
            expected = fixture[2]
            self.assertEqual(result1, expected,
                "rsplit_main_prefix(%r,%r) returned %r but we expected %r" \
                % (fixture[0],fixture[1],result1,expected))
            self.assertEqual(result1, expected,
                "RSplitMainPrefix(%r,main_prefixes=%r) returned %r but we " \
                "expected %r" % (fixture[0],fixture[1],result2,expected))

    def test_dont_split_undefined_main_prefixes(self):
        "rsplit_main_prefix() doesn't split-out main prefixes it doesn't know"
        for fixture in self.undefined_xxx_fixtures:
            result1 = rsplit_main_prefix(fixture[0],fixture[1])
            result2 = RSplitMainPrefix(fixture[0], main_prefixes = fixture[1])
            expected = fixture[2]
            self.assertEqual(result1, expected,
                "rsplit_main_prefix(%r,%r) returned %r but we expected %r" \
                % (fixture[0],fixture[1],result1,expected))
            self.assertEqual(result1, expected,
                "RSplitMainPrefix(%r,main_prefixes=%r) returned %r but we " \
                "expected %r" % (fixture[0],fixture[1],result2,expected))
        
#############################################################################
class Test_rsplit_add_prefix(Test_rsplit_xxx_Base):

    def test_split_all_std_add_prefixes(self):
        "rsplit_add_prefix() splits-out all standard additional prefixes"
        for add_prefix in StandardAddPrefixes():
            expected = (None, add_prefix)
            uname = add_prefix
            result1 = rsplit_add_prefix(uname)
            result2 = RSplitAddPrefix(uname)
            self.assertEqual(result1, expected, 
                "rsplit_add_prefix(%r) returned %r but we " \
                "expected %r" % (uname,result1,expected))
            self.assertEqual(result2, expected, 
                "RSplitAddPrefix(%r) returned %r but we " \
                "expected %r" % (uname,result2,expected))
        for add_prefix2 in StandardAddPrefixes():
            for add_prefix in StandardAddPrefixes():
                if add_prefix == add_prefix2:
                    continue
                expected = (add_prefix2, add_prefix)
                uname = '_'.join([add_prefix2, add_prefix])
                result1 = rsplit_add_prefix(uname)
                result2 = RSplitAddPrefix(uname)
                self.assertEqual(result1, expected, 
                    "rsplit_add_prefix(%r) returned %r but we " \
                    "expected %r" % (uname,result1,expected))
                self.assertEqual(result2, expected, 
                    "RSplitAddPrefix(%r) returned %r but we " \
                    "expected %r" % (uname,result2,expected))

    def test_split_defined_add_prefixes(self):
        "rsplit_add_prefix() splits-out all main prefixes predefined by user"
        for fixture in self.defined_xxx_fixtures:
            result1 = rsplit_add_prefix(fixture[0],fixture[1])
            result2 = RSplitAddPrefix(fixture[0], add_prefixes = fixture[1])
            expected = fixture[2]
            self.assertEqual(result1, expected,
                "rsplit_add_prefix(%r,%r) returned %r but we expected %r" \
                % (fixture[0],fixture[1],result1,expected))
            self.assertEqual(result1, expected,
                "RSplitAddPrefix(%r,add_prefixes=%r) returned %r but we " \
                "expected %r" % (fixture[0],fixture[1],result2,expected))

    def test_dont_split_undefined_add_prefixes(self):
        "rsplit_add_prefix() doesn't split-out names it doesn't know"
        for fixture in self.undefined_xxx_fixtures:
            result1 = rsplit_add_prefix(fixture[0],fixture[1])
            result2 = RSplitAddPrefix(fixture[0], add_prefixes = fixture[1])
            expected = fixture[2]
            self.assertEqual(result1, expected,
                "rsplit_add_prefix(%r,%r) returned %r but we expected %r" \
                % (fixture[0],fixture[1],result1,expected))
            self.assertEqual(result1, expected,
                "RSplitAddPrefix(%r,add_prefixes=%r) returned %r but we " \
                "expected %r" % (fixture[0],fixture[1],result2,expected))

#############################################################################
class Test_ensure_name_sanity(unittest.TestCase):

    def test_all_std_names(self):
        "ensure_name_sanity() raises no exception for allowed standard names"
        for primary in StandardPrimaryNames():
            for main_prefix in StandardPrimaryMainPrefixes(primary):
                if main_prefix in StandardForbidPrimaryMainPrefixes(primary):
                    continue
                for add_prefix in StandardAddPrefixes():
                    if add_prefix in StandardForbidPrimaryAddPrefixes(primary):
                        continue
                    if add_prefix in StandardForbidMainAddPrefixes(main_prefix):
                        continue
                    funame = '_'.join([add_prefix, main_prefix, primary])
                    try:
                        ensure_name_sanity(funame)
                    except ValueError, e:
                        self.fail("ensure_name_sanity(%r) raised exception %r"\
                         % (funame, e))
                    try:
                        EnsureNameSanity(funame)
                    except ValueError, e:
                        self.fail("EnsureNameSanity(%r) raised exception %r" \
                        % (funame, e))

    def test_raises_unknown_primary(self):
        with self.assertRaises(ValueError):
            ensure_name_sanity('bin_FOOBAR')
        with self.assertRaises(ValueError):
            EnsureNameSanity('bin_FOOBAR')

    def test_raises_unknown_main_prefix(self):
        with self.assertRaises(ValueError):
            ensure_name_sanity('foobar_PROGRAMS')
        with self.assertRaises(ValueError):
            EnsureNameSanity('foobar_PROGRAMS')

    def test_raises_unknown_add_prefix(self):
        with self.assertRaises(ValueError):
            ensure_name_sanity('foobar_bin_PROGRAMS')
        with self.assertRaises(ValueError):
            EnsureNameSanity('foobar_bin_PROGRAMS')

    def test_raises_primary_main_prefix(self):
        # TODO:
        pass

    def test_raises_primary_add_prefix(self):
        pass

    def test_raises_main_add_prefix(self):
        with self.assertRaises(ValueError):
            ensure_name_sanity('nobase_man_MANS')
        with self.assertRaises(ValueError):
            EnsureNameSanity('nobase_man_MANS')

    def test_raises_colliding_add_prefixes(self):
        with self.assertRaises(ValueError):
            ensure_name_sanity('nodist_dist_include_HEADERS')
        with self.assertRaises(ValueError):
            EnsureNameSanity('nodist_dist_include_HEADERS')


#############################################################################
if __name__ == "__main__":
    ldr = unittest.TestLoader()
    suite = unittest.TestSuite()
    # Load tests to test suite
    tclasses = [ 
        Test_std_primary_names,
        Test_std_main_prefixes,
        Test_std_add_prefixes,
        Test_std_primary_main_prefixes,
        Test_rsplit_primary_name,
        Test_rsplit_main_prefix,
        Test_rsplit_add_prefix,
        Test_ensure_name_sanity,
    ]

    for tclass in tclasses:
        suite.addTests(ldr.loadTestsFromTestCase(tclass))

    if not unittest.TextTestRunner(verbosity = 2).run(suite).wasSuccessful():
        sys.exit(1)
#############################################################################

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
