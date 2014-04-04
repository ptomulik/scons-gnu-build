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
Tests declaring variables with SConsGnu.GVar.GVarDecls() factory method.
"""

import TestSCons

##############################################################################
# GVarDeclsU(): Test 2
##############################################################################
test = TestSCons.TestSCons()
test.dir_fixture('../../../../SConsGnu', 'site_scons/SConsGnu')
test.write('SConstruct',
"""
# SConstruct
from SConsGnu.GVars import GVarDeclsU, ENV, VAR, OPT
x = { 'env_key' : 'env_x' , 'var_key' : 'var_x', 'opt_key' : 'opt_x', 'default' : 'x default', 'option' : '-x' }
y = { 'env_key' : 'env_y' , 'var_key' : 'var_y', 'opt_key' : 'opt_y', 'default' : 'y default', 'option' : '-y' }
list = []
list.append( GVarDeclsU(x = x, y = y) )
list.append( GVarDeclsU({'x' : x, 'y' : y}) )
i = 0
for v in list:
    for c in ['x', 'y']:
        print "GVARS[%d][%r].has_xxx_decl(ENV): %r" % (i, c, v[c].has_xxx_decl(ENV))
        print "GVARS[%d][%r].has_xxx_decl(VAR): %r" % (i, c, v[c].has_xxx_decl(VAR))
        print "GVARS[%d][%r].has_xxx_decl(OPT): %r" % (i, c, v[c].has_xxx_decl(OPT))
        print "GVARS[%d][%r].get_xxx_key(ENV): %r" % (i, c, v[c].get_xxx_key(ENV))
        print "GVARS[%d][%r].get_xxx_key(VAR): %r" % (i, c, v[c].get_xxx_key(VAR))
        print "GVARS[%d][%r].get_xxx_key(OPT): %r" % (i, c, v[c].get_xxx_key(OPT))
        print "GVARS[%d][%r].get_xxx_default(ENV): %r" % (i, c, v[c].get_xxx_default(ENV))
        print "GVARS[%d][%r].get_xxx_default(VAR): %r" % (i, c, v[c].get_xxx_default(VAR))
        print "GVARS[%d][%r].get_xxx_default(OPT): %r" % (i, c, v[c].get_xxx_default(OPT))
    i += 1
""")
test.run()

lines = [
        "GVARS[0]['x'].has_xxx_decl(ENV): True",
        "GVARS[0]['x'].has_xxx_decl(VAR): True",
        "GVARS[0]['x'].has_xxx_decl(OPT): True",
        "GVARS[0]['x'].get_xxx_key(ENV): 'env_x'",
        "GVARS[0]['x'].get_xxx_key(VAR): 'var_x'",
        "GVARS[0]['x'].get_xxx_key(OPT): 'opt_x'",
        "GVARS[0]['x'].get_xxx_default(ENV): 'x default'",
        "GVARS[0]['x'].get_xxx_default(VAR): 'x default'",
        "GVARS[0]['x'].get_xxx_default(OPT): None",

        "GVARS[0]['y'].has_xxx_decl(ENV): True",
        "GVARS[0]['y'].has_xxx_decl(VAR): True",
        "GVARS[0]['y'].has_xxx_decl(OPT): True",
        "GVARS[0]['y'].get_xxx_key(ENV): 'env_y'",
        "GVARS[0]['y'].get_xxx_key(VAR): 'var_y'",
        "GVARS[0]['y'].get_xxx_key(OPT): 'opt_y'",
        "GVARS[0]['y'].get_xxx_default(ENV): 'y default'",
        "GVARS[0]['y'].get_xxx_default(VAR): 'y default'",
        "GVARS[0]['y'].get_xxx_default(OPT): None",

        "GVARS[1]['x'].has_xxx_decl(ENV): True",
        "GVARS[1]['x'].has_xxx_decl(VAR): True",
        "GVARS[1]['x'].has_xxx_decl(OPT): True",
        "GVARS[1]['x'].get_xxx_key(ENV): 'env_x'",
        "GVARS[1]['x'].get_xxx_key(VAR): 'var_x'",
        "GVARS[1]['x'].get_xxx_key(OPT): 'opt_x'",
        "GVARS[1]['x'].get_xxx_default(ENV): 'x default'",
        "GVARS[1]['x'].get_xxx_default(VAR): 'x default'",
        "GVARS[1]['x'].get_xxx_default(OPT): None",

        "GVARS[1]['y'].has_xxx_decl(ENV): True",
        "GVARS[1]['y'].has_xxx_decl(VAR): True",
        "GVARS[1]['y'].has_xxx_decl(OPT): True",
        "GVARS[1]['y'].get_xxx_key(ENV): 'env_y'",
        "GVARS[1]['y'].get_xxx_key(VAR): 'var_y'",
        "GVARS[1]['y'].get_xxx_key(OPT): 'opt_y'",
        "GVARS[1]['y'].get_xxx_default(ENV): 'y default'",
        "GVARS[1]['y'].get_xxx_default(VAR): 'y default'",
        "GVARS[1]['y'].get_xxx_default(OPT): None",
]

test.must_contain_all_lines(test.stdout(), lines)

test.pass_test()

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
