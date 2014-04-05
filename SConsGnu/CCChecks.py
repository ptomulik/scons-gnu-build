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

_empty_prog = """
int main() { return 0; }

"""

def _get_cc_version(env, cc):
    ccname = os.path.basename(cc) # because cc may be (an absolute) path
    if re.match(r'^(?:[a-z0-9_-]+-)?(?:cc|gcc|c\+\+|g\+\+)$', ccname):
        cmd = CLVar([cc, '-dumpversion'])
        ccswitch = 'gcc'
    elif re.match(r'^(?:[a-z0-9_-]+-)?(?:clang|clang\+\+)$', ccname):
        cmd = CLVar([cc, '--version'])
        ccswitch = 'clang'
    else:
        return 'failed (unsupported compiler)'

    try:
        proc = _subproc(env, cmd, 'raise', stdout = PIPE)
    except EnvironmentError:
        pass
    out, err = proc.communicate()
    stat = proc.wait()
    if stat:
        return 'failed (output status: %d)' % stat

    # this gives rise to eventual postprocessing if some compiler needs it
    if ccswitch == 'gcc':
        ver = out.strip()
    elif ccswitch == 'clang':
        found = re.search(r'clang +version +([0-9]+(?:\.[0-9]+)+)', out)
        if not found:
            return 'failed (can not parse version string)'
        ver = found.group(1)
    else:
        ver = 'failed (unsupported compiler)'
    return ver

def _check_cc_version(context, env, cc):
    context.Display('Checking for %s version... ' % cc)
    ver = _get_cc_version(env, cc)
    if ver:
        context.Result(str(ver))
        if ver.startswith('failed'):
            ver = None
    else:
        context.Result('none')
    return ver

def _add_flags_to_overrides(env, overrides, name, newflags):
    newflags = CLVar(newflags)
    flags = overrides.get(name, env.get(name,[]))[:]
    flags =  CLVar(flags)
    for nf in newflags:
        if not nf in flags:
            flags.append(nf)
    overrides[name] = flags
    
def check_cc_flag(context, cc, flag, text, extension, **overrides):
    flag = CLVar(flag)
    context.Display('Checking whether %s supports %s... ' % (cc, str(flag)))
    context.sconf.cached = 1
    res = context.sconf.TryCompileWO(text, extension, **overrides)
    context.Result(res)
    return res


def CheckCCVersion(context, **overrides):
    """Check the version of C compiler
    
    :Parameters:
        context
            SCons configure context
        overrides
            Used to override current construction variables (e.g. CC) in
            context.env.
    :Return:
        String representing version of the current compiler or ``None``.
    """
    env = context.env.Override(overrides)
    return _check_cc_version(context, env, env['CC'])

def CheckCXXVersion(context, **overrides):
    """Check the version of C++ compiler
    
    :Parameters:
        context
            SCons configure context
        overrides
            Used to override current construction variables (e.g. CXX) in
            context.env.
    :Return:
        String representing version of the current compiler or ``None``.
    """
    env = context.env.Override(overrides)
    return _check_cc_version(context, env, env['CXX'])

def TryCompileWO(context, text=None, extension='.c', **overrides):
    """Try compile a program in a modified environment.
    
    This test temporarily applies **overrides** to context.sconf.env and runs
    ``context.sconf.TryCompile(text, extension)``.

    :Parameter:
        context
            SCons configure context
        text
            Source code of the C/C++ program to be compiled.
        extension
            Extension of the test source file to be generated.
        overrides
            Used to override construction variables in context.sconf.env.
    :Return:
        Compilation status. If success, it evaluates to True.
    """
    global _empty_prog
    context.did_show_result = 1
    env = context.sconf.env
    context.sconf.env = env.Clone(**overrides)
    if text is None:
        text = _empty_prog
    try:
        out = context.sconf.TryCompile(text, extension)
    finally:
        context.sconf.env = env
    return out

def TryLinkWO(context, text=None, extension='.c', **overrides):
    """Try compile and link a program in a modified environment.
    
    This test temporarily applies **overrides** to context.sconf.env and runs
    ``context.sconf.TryLink(text, extension)``.

    :Parameter:
        context
            SCons configure context
        text
            Source code of the C/C++ program to be compiled.
        extension
            Extension of the test source file to be generated.
        overrides
            Used to override construction variables in context.sconf.env.
    :Return:
        Compilation status. If success, it evaluates to True.
    """
    global _empty_prog
    context.did_show_result = 1
    env = context.sconf.env
    context.sconf.env = env.Clone(**overrides)
    if text is None:
        text = _empty_prog
    try:
        out = context.sconf.TryLink(text, extension)
    finally:
        context.sconf.env = env
    return out

def TryRunWO(context, text=None, extension='.c', **overrides):
    """Try to compile, link and run a program in a modified environment.
    
    This test temporarily applies **overrides** to context.sconf.env and runs
    ``context.sconf.TryRun(text, extension)``.

    :Parameter:
        context
            SCons configure context
        text
            Source code of the C/C++ program to be compiled.
        extension
            Extension of the test source file to be generated.
        overrides
            Used to override construction variables in context.sconf.env.
    :Return:
        Compilation status. If success, it evaluates to True.
    """
    global _empty_prog
    context.did_show_result = 1
    env = context.sconf.env
    context.sconf.env = env.Clone(**overrides)
    if text is None:
        text = _empty_prog
    try:
        out = context.sconf.TryRun(text, extension)
    finally:
        context.sconf.env = env
    return out

def CheckCCFlag(context, flag, text=None, extension='.c', **overrides):
    """Check whether C compiler supports given flag(s)

    This test adds **flag** to current set of 'CFLAGS' and tries to compile a
    program contained in **text**.

    :Parameter:
        context
            SCons configure context
        text
            Source code of the C/C++ program to be compiled.
        extension
            Extension of the test source file to be generated.
        overrides
            Used to override construction variables in context.sconf.env.
    :Return:
        Compilation status. If success, it evaluates to True.
    """
    cc = overrides.get('CC') or context.env['CC']
    _add_flags_to_overrides(context.env, overrides, 'CFLAGS', flag)
    return check_cc_flag(context, cc, flag, text, extension, **overrides)
    
def CheckCXXFlag(context, flag, text=None,extension='.cpp', **overrides):
    """Check whether C++ compiler supports given flag(s)

    This test adds **flag** to current set of 'CFLAGS' and tries to compile a
    program contained in **text**.

    :Parameter:
        context
            SCons configure context
        text
            Source code of the C/C++ program to be compiled.
        extension
            Extension of the test source file to be generated.
        overrides
            Used to override construction variables in context.sconf.env.
    :Return:
        Compilation status. If success, it evaluates to True.
    """
    cc = overrides.get('CXX') or context.env['CXX']
    _add_flags_to_overrides(context.env, overrides, 'CXXFLAGS', flag)
    return check_cc_flag(context, cc, flag, text, extension, **overrides)

def Tests():
    """Returns all the checks implemented in CCompilerChecks as a dictionary."""
    return { 'CheckCCVersion'  : CheckCCVersion
           , 'CheckCXXVersion' : CheckCXXVersion
           , 'TryCompileWO'    : TryCompileWO
           , 'TryLinkWO'       : TryLinkWO
           , 'TryRunWO'        : TryRunWO
           , 'CheckCCFlag'     : CheckCCFlag
           , 'CheckCXXFlag'    : CheckCXXFlag
           }

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=scons expandtab tabstop=4 shiftwidth=4:
