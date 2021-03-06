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
Tests declaring variables with SConsGnu.GVar.GVarDeclU() factory method.
"""

import TestSCons

##############################################################################
# GVarDeclU(): Test 4 - declare GVar that is bound to OPT only.
##############################################################################
test = TestSCons.TestSCons()
test.dir_fixture('../../../../SConsGnu', 'site_scons/SConsGnu')
test.write('SConstruct',
"""
# SConstruct
from SConsGnu.GVars import GVarDeclU, ENV, VAR, OPT
list = []
list.append( GVarDeclU(None, None, 'opt_x', None, None, None, None, ('-x', '--xvar'), None, 'opt x default') )
list.append( GVarDeclU(opt_key = 'opt_x', option = ('-x', '--xvar'), opt_default = 'opt x default') )

i = 0
for v in list:
    print "GVAR[%d].has_xxx_decl(ENV): %r" % (i, v.has_xxx_decl(ENV))
    print "GVAR[%d].has_xxx_decl(VAR): %r" % (i, v.has_xxx_decl(VAR))
    print "GVAR[%d].has_xxx_decl(OPT): %r" % (i, v.has_xxx_decl(OPT))
    print "GVAR[%d].get_xxx_key(OPT): %r" % (i, v.get_xxx_key(OPT))
    print "GVAR[%d].get_xxx_default(OPT): %r" % (i, v.get_xxx_default(OPT))
    i += 1
""")
test.run()

lines = [
  "GVAR[0].has_xxx_decl(ENV): False",
  "GVAR[0].has_xxx_decl(VAR): False",
  "GVAR[0].has_xxx_decl(OPT): True",
  "GVAR[0].get_xxx_key(OPT): 'opt_x'",
  "GVAR[0].get_xxx_default(OPT): 'opt x default'",

  "GVAR[1].has_xxx_decl(ENV): False",
  "GVAR[1].has_xxx_decl(VAR): False",
  "GVAR[1].has_xxx_decl(OPT): True",
  "GVAR[1].get_xxx_key(OPT): 'opt_x'",
  "GVAR[1].get_xxx_default(OPT): 'opt x default'",
]

test.must_contain_all_lines(test.stdout(), lines)

test.pass_test()

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
