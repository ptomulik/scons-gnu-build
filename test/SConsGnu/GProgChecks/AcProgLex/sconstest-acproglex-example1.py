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
TODO: write description
"""

import TestSCons

##############################################################################
# 
##############################################################################
test = TestSCons.TestSCons()
test.dir_fixture('../../../../SConsGnu', 'site_scons/SConsGnu')
test.write('SConstruct',
"""
# SConstruct
from SConsGnu import GProgChecks
env = Environment()               # create an environment
cfg = Configure(env)              # create SConf object
cfg.AddTests(GProgChecks.Tests()) # add tests for alternative programs
lex, lexroot, lexlibs, yytextptr = cfg.AcProgLex()      # perform the check
env = cfg.Finish()                # finish configuration
# print the returned values
print "lex:       %r" % lex 
print "lexroot:   %r" % lexroot
print "lexlibs:   %r" % lexlibs
print "yytextptr: %r" % yytextptr
""")

test.run()
test.must_contain_all_lines(test.stdout(), [
    'Checking for flex... ',
    'Checking for lex output file root... ',
    'Checking for lex library... ',
    'Checking whether yytext is a pointer... ',
    'lex: ',
    'lexroot: ',
    'lexlibs: ',
    'yytextptr: '
])
test.pass_test()

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
