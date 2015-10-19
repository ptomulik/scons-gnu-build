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

__docformat__ = "restructuredText"

"""
Tests GVars default values handling
"""

import TestSCons

##############################################################################
# GVarDeclsU(): Test 1 - declare empty dict
##############################################################################
test = TestSCons.TestSCons()
test.dir_fixture('../../../SConsGnu', 'site_scons/SConsGnu')
test.write('SConstruct',
"""
# SConstruct
from SConsGnu.GVars import GVarDeclsU, _undef
env = Environment(tools = [])
var = Variables()
decls = GVarDeclsU(
    foo = {'env_key' : 'FOO', 'var_key' : 'FOO', 'opt_key' : 'foo', 'option' : '--foo'},
    bar = {'env_key' : 'BAR', 'var_key' : 'BAR', 'opt_key' : 'bar', 'option' : '--bar', 'default' : None},
    gez = {'env_key' : 'GEZ', 'var_key' : 'GEZ', 'opt_key' : 'gez', 'option' : '--gez', 'default' : _undef }
)
gvars = decls.Commit(env, var, True)
gvars.Postprocess(env, var, True)
for key in ['FOO', 'BAR', 'GEZ']:
    try: print "env['%s']: %s" % (key, env[key])
    except KeyError: pass
""")

# Default values
test.run()
test.must_contain_all_lines(test.stdout(), ["env['BAR']: None"])
test.must_not_contain_any_line(test.stdout(), ["env['FOO']:", "env['GEZ']:"])

# Variables
test.run(arguments = ['FOO=1', 'BAR=2', 'GEZ=3'])
test.must_contain_all_lines(test.stdout(), ["env['FOO']: 1", "env['BAR']: 2", "env['GEZ']: 3"])

# Options
test.run(arguments = ['--foo=a', '--bar=b', '--gez=c'])
test.must_contain_all_lines(test.stdout(), ["env['FOO']: a", "env['BAR']: b", "env['GEZ']: c"])

test.pass_test()

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
