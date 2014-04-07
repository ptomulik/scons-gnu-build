"""`SConsGnu.Cc`

Several utility methods related to C compilers.
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
from SCons.Util import CLVar
import os
import re

_cc_re_dict = {
    'gcc'     : r'^(?:.+-)?(?:cc|gcc)(?:(?:-[0-9]+(?:\.[0-9]+)*)+)?$',
    'g++'     : r'^(?:.+-)?(?:c\+\+|g\+\+)(?:(?:-[0-9]+(?:\.[0-9]+)*)+)?$',
    'clang'   : r'^(?:.+-)?:clang(?:(?:-[0-9]+(?:\.[0-9]+)*)+)?$',
    'clang++' : r'^(?:.+-)?:clang\+\+(?:(?:-[0-9]+(?:\.[0-9]+)*)+)?$'
}

for key, expr in _cc_re_dict.items():
    _cc_re_dict[key] = re.compile(expr)

def _canon_cc(ccpath):
    ccname = os.path.basename(ccpath) 
    for cc, expr in _cc_re_dict.items():
        if expr.match(ccname):
            return cc
    return ccname

def _cc_version_cmd(env, cc, ccpath):
    if cc in ('gcc', 'g++'):
        return CLVar([ccpath, '-dumpversion'])
    elif cc in ('clang', 'clang++'):
        return CLVar([ccpath, '--version'])
    else:
        return None

def _parse_gcc_version(text):
    return text.strip()

def _parse_clang_version(text):
    found = re.search(r'clang +version +([0-9]+(?:\.[0-9]+)+)', text)
    if not found:
        return None
    return found.group(1)

def _parse_cc_version(env, cc, text):
    if cc in ('gcc', 'g++'):
        version = _parse_gcc_version(text)
    elif cc in ('clang', 'clang++'):
        version = _parse_clang_version(text)
    else:
        version = None
    if not version:
        return (None, 'unsupported compiler %s' % cc)
    else:
        return (version, None)

def _cc_target_cmd(env, cc, ccpath):
    if cc in ('gcc', 'g++'):
        return CLVar([ccpath, '-dumpmachine'])
    elif cc in ('clang', 'clang++'):
        return CLVar([ccpath, '-dumpmachine'])
    else:
        return None

def _parse_gcc_target(text):
    return text.strip()

def _parse_clang_target(text):
    return text.strip()

def _parse_cc_target(env, cc, text):
    if cc in ('gcc', 'g++'):
        target = _parse_gcc_target(text)
    elif cc in ('clang', 'clang++'):
        target = _parse_clang_target(text)
    else:
        target = None
    if not target:
        return (None, 'unsupported compiler %s' % cc)
    else:
        return (target, None)

def _run_cc_cmd(env, cmd):
    try:
        proc = _subproc(env, cmd, 'raise', stdout = PIPE)
    except EnvironmentError as e:
        stat = 1
        out = ''
        err = e.message
    else:
        out, err = proc.communicate()
        stat = proc.wait()
        if stat or not out:
            if not stat:
                stat = 1
            if err:
                err = err.strip()
            if not err:
                err = 'command %r returned status: %d' % (cmd, stat)
    return stat, out, err

def _query_cc_info(env, ccpath, cmd_fun, parse_fun):
    cc = _canon_cc(ccpath)
    cmd = cmd_fun(env, cc, ccpath)
    if not cmd:
        return (None, 'unsupported compiler %s' % cc)
    stat, out, err = _run_cc_cmd(env, cmd)
    if stat:
        return (None, err)
    return parse_fun(env, cc, out)

def _query_cc_version(env, ccpath):
    return _query_cc_info(env, ccpath, _cc_version_cmd, _parse_cc_version)

def _query_cc_target(env, ccpath):
    return _query_cc_info(env, ccpath, _cc_target_cmd, _parse_cc_target)

def CanonCC(env, **overrides):
    """Return "canonical name" of the C compiler used.

    If ``env['CC']`` is a path (``'/opt/bin/gcc'`` for example), or even
    something like ``'/opt/bin/avr-gcc-4.8'``, the function tries to properly
    recognize, that this is still the ``'gcc'`` compiler.

    **Supported compilers**:
        - ``gcc``, ``g++``
        - ``clang``, ``clang++``

    :Parameters:
        env
            SCons environment object.
        overrides
            Used to override construction variables in **env**.
    :Return:
        If recognized, then returns one of the values from the **Supported
        compilers** list . Otherwise, returns the basename of the original
        compiler (e.g. ``xyz-foo` for ``/opt/bin/xyz-foo``).
    """
    return _canon_cc(overrides.get('CC', env['CC']))

def CanonCXX(env, **overrides):
    """Return "canonical name" of the C++ compiler used.

    If ``env['CXX']`` is a path (``'/opt/bin/g++'`` for example), or even
    something like '``/opt/bin/avr-g++-4.8'``, the function tries to properly
    recognize, that this is still the ``'g++'`` compiler.

    **Supported compilers**:
        - ``gcc``, ``g++``
        - ``clang``, ``clang++``

    :Parameters:
        env
            SCons environment object.
        overrides
            Used to override construction variables in **env**.
    :Return:
        If recognized, then returns one of the values from the **Supported
        compilers** list . Otherwise, returns the basename of the original
        compiler (e.g. ``xyz-foo++` for ``/opt/bin/xyz-foo++``).
    """
    return _canon_cc(overrides.get('CXX', env['CXX']))

def QueryCCVersion(env, **overrides):
    """Retrieve version of C compiler.

    **Supported compilers**:
        - ``gcc``, ``g++``
        - ``clang``, ``clang++``

    :Parameters:
        env
            SCons environment object.
        overrides
            Used to override construction variables in **env**.
    :Return:
        Version string or ``None``.
    """
    env = env.Override(overrides)
    ver, err = _query_cc_version(env, env['CC'])
    # TODO: handle error here?
    return ver

def QueryCXXVersion(env, **overrides):
    """Retrieve version of C++ compiler

    **Supported compilers**:
        - ``gcc``, ``g++``
        - ``clang``, ``clang++``

    :Parameters:
        env
            SCons environment object.
        overrides
            Used to override construction variables in **env**.
    :Return:
        Version string or ``None``.
    """
    env = env.Override(overrides)
    ver, err = _query_cc_version(env, env['CXX'])
    # TODO: handle error here?
    return ver

def QueryCCTarget(env, **overrides):
    """Retrieve target architectore of the C compiler.

    **Supported compilers**:
        - ``gcc``, ``g++``
        - ``clang``, ``clang++``

    :Parameters:
        env
            SCons environment object.
        overrides
            Used to override construction variables in **env**.
    :Return:
        Target string or ``None``.
    """
    env = env.Override(overrides)
    tgt, err = _query_cc_target(env, env['CC'])
    # TODO: handle error here?
    return tgt

def QueryCXXTarget(env, **overrides):
    """Retrieve target architecture of the C++ compiler

    **Supported compilers**:
        - ``gcc``, ``g++``
        - ``clang``, ``clang++``

    :Parameters:
        env
            SCons environment object.
        overrides
            Used to override construction variables in **env**.
    :Return:
        Target string or ``None``.
    """
    env = env.Override(overrides)
    tgt, err = _query_cc_target(env, env['CXX'])
    # TODO: handle error here?
    return tgt

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
