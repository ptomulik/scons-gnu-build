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
Test whether CheckCXXFlag() doesn't display a message when invoked with
context.did_show_result set to True.
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
from SConsGnu import CcChecks

def CheckCXXFlagSilent(context, flag, **overrides):
    context.did_show_result = 1
    return CcChecks.CheckCXXFlag(context, flag, **overrides)

env = Environment()
cfg = Configure(env)
cfg.AddTests( CcChecks.Tests() )
cfg.AddTests( {'CheckCXXFlagSilent' : CheckCXXFlagSilent })
result = cfg.CheckCXXFlagSilent('-foobar', CFLAGS=['-Werror'], CXX='dummycompiler')
env = cfg.Finish()
""")

test.run()
test.must_not_contain_any_line(test.stdout(), [
    'Checking',
    'yes',
    'no'
])

test.pass_test()

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
