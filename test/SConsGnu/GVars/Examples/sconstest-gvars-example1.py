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
Complete example involving GVars
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
from SConsGnu import GVars
decls = GVars.GVarDeclsU(
  prefix      = { 'env_key' : 'GNU_PREFIX', 'var_key' : 'PREFIX', 'opt_key' : 'opt_prefix',
                  'option' : '--prefix', 'default' : '/usr/local', 'type' : 'string',
                  'help' : 'installation prefix' },
  exec_prefix = { 'env_key' : 'GNU_EXEC_PREFIX', 'var_key' : 'EXEC_PREFIX', 'opt_key' : 'opt_exec_prefix',
                  'option' : '--exec-prefix', 'default' : '$prefix', 'type' : 'string',
                  'help' : 'installation prefix for executable files' },
  bindir      = { 'env_key' : 'GNU_BINDIR', 'var_key' : 'BINDIR', 'opt_key' : 'opt_bindir',
                  'option' : '--bindir', 'default' : '$exec_prefix/bin', 'type' : 'string',
                  'help' : 'directory for installing executable programs that users can run' }
)
env = Environment()
var = Variables()
gv = decls.Commit(env, var, True)
gv.UpdateEnvironment(env, var, True)

AddOption( '--help-variables', dest='help_variables', action='store_true',
           help='print help for CLI variables' )
if GetOption('help_variables'):
    print gv.GenerateVariablesHelpText(var, env)
    Exit(0)

# Create proxy to access GVars using their original names
proxy = gv.EnvProxy(env)

# Print values.
print proxy.subst('prefix: $prefix')
print proxy.subst('exec_prefix: $exec_prefix')
print proxy.subst('bindir: $bindir')
""")

test.run(arguments = ['-Q'])
test.must_contain_all_lines(test.stdout(), [
    'prefix: /usr/local',
    'exec_prefix: /usr/local',
    'bindir: /usr/local/bin',
])

test.run(arguments = ['-Q', "EXEC_PREFIX=$PREFIX/exec"])
test.must_contain_all_lines(test.stdout(), [
    'prefix: /usr/local',
    'exec_prefix: /usr/local/exec',
    'bindir: /usr/local/exec/bin',
])

test.run(arguments = ['-Q', "--exec-prefix=$opt_prefix/exec"])
test.must_contain_all_lines(test.stdout(), [
    'prefix: /usr/local',
    'exec_prefix: /usr/local/exec',
    'bindir: /usr/local/exec/bin',
])

test.run(arguments = ['-Q', "--exec-prefix=$opt_prefix/exec_o", "EXEC_PREFIX=$PREFIX/exec_v"])
test.must_contain_all_lines(test.stdout(), [
    'prefix: /usr/local',
    'exec_prefix: /usr/local/exec_o',
    'bindir: /usr/local/exec_o/bin',
])

test.run(arguments = ['-h'])
test.must_contain_all_lines(test.stdout(), [
    '  --exec-prefix=OPT_EXEC_PREFIX',
])

test.run(arguments = ['--help-variables'])
test.must_contain_all_lines(test.stdout(), [
    'EXEC_PREFIX: installation prefix for executable files',
    'PREFIX: installation prefix',
    'BINDIR: directory for installing executable programs that users can run'
])

test.pass_test()

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
