"""`SConsGnu.CCompilerChecks`

Configure checks for several features of C compilers. They're not covered by
autoconf.
"""

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

from SCons.Action import _subproc
from subprocess import PIPE
from SCons.Util import is_String, CLVar
import os
import re

from SConsGnu.CCVars import gvar_names, declare_gvars
from SConsGnu.CCVars import GVarNames, DeclareGVars

def _get_cc_version(env, cc):
    ccname = os.path.basename(cc) # because cc may be (an absolute) path
    if re.match(r'^(?:[a-z0-9_-]+-)?(?:cc|gcc|c\+\+|g\+\+)$', ccname):
        cmd = CLVar([cc, '-dumpversion'])
        ccfamily = 'gcc'
    elif re.match(r'^(?:[a-z0-9_-]+-)?(?:clang|clang\+\+)$', ccname):
        cmd = CLVar([cc, '-dumpversion'])
        ccfamily = 'clang'
    else:
        return 'unsupported compiler'

    try:
        proc = _subproc(env, cmd, 'raise', stdout = PIPE)
    except EnvironmentError:
        pass
    out, err = proc.communicate()
    stat = proc.wait()
    if stat:
        return 'failed'

    # this gives rise to eventual postprocessing if some compiler needs it
    if ccfamily == 'gcc' or ccfamily == 'clang':
        out = out.strip()
        return out
    else:
        out = out.strip()
        return out

def _check_cc_version(context, cc):
    context.Display('Checking for %s version... ' % cc)
    ver = _get_cc_version(context.env, cc)
    if ver:
        context.Result(str(ver))
        if ver in ['unsupported compiler', 'failed']:
            ver = None
    else:
        context.Result('none')
    return ver

def CheckCCVersion(context, cc = None):
    if cc is None:
        cc = context.env['CC']
    return _check_cc_version(context, cc)

def CheckCXXVersion(context, cxx = None):
    if cxx is None:
        cxx = context.env['CXX']
    return _check_cc_version(context, cxx)

def Tests():
    """Returns all the checks implemented in CCompilerChecks as a dictionary."""
    return { 'CheckCCVersion'  : CheckCCVersion
           , 'CheckCXXVersion' : CheckCXXVersion }

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=scons expandtab tabstop=4 shiftwidth=4:
