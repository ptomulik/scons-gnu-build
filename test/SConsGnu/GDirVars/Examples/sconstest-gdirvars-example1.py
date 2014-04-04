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
Using Installation Directory Variables
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
from SConsGnu import GVars, GDirVars
env = Environment()
var = Variables('.scons_variables')
decls = GDirVars.DeclareGVars()
gv = decls.Commit(env, var, True)
# Add help
AddOption( '--help-variables', dest='help_variables', action='store_true',
           help='print help for CLI variables' )
if GetOption('help_variables'):
    print gv.GenerateVariablesHelpText(var, env)
    Exit(0)

gv.UpdateEnvironment(env, var, True)
gv.SaveVariables(var, '.scons_variables', env)
""")

test.run(arguments = ['-Q', '--help'])
test.must_contain_all_lines(test.stdout(), [
    '--docdir=DIR',
    '--man1ext=DIR',
    '--sharedstatedir=DIR',
])

test.run(arguments = ['-Q', '--help-variables'])
test.must_contain_all_lines(test.stdout(), [
    'docdir:',
    'man1ext:',
    'sharedstatedir:',
])

test.run(arguments = ['-Q', '--help-variables'])
test.must_contain_all_lines(test.stdout(), [
    'docdir:',
    'man1ext:',
    'sharedstatedir:',
])

test.run(arguments = [])
test.must_exist('.scons_variables')
test.must_not_contain('.scons_variables', 'prefix')

test.run(arguments = ['prefix=/', 'exec_prefix=/usr'])
test.must_exist('.scons_variables')
test.must_match('.scons_variables', "prefix = '/'\nexec_prefix = '/usr'\n")

test.pass_test()

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
