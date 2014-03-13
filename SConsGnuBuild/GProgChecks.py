"""`SConsGnuBuild.GProgChecks`

`Alternative Programs`_. Check whether they exist, and in some cases whether
they support certain features.

.. _Alternative Programs: http://www.gnu.org/software/autoconf/manual/autoconf.html#Alternative-Programs
"""


#
# Copyright (c) 2012 by Pawel Tomulik
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

__docformat__ = 'restructuredText'


###############################################################################
class _PathProgsFeatureCheck(object):
    """Corresponds to `_AC_PATH_PROGS_FEATURE_CHECK`_

    Use this as an action for ``context.TryAction()``. This action calls
    repeatedly the provided **feature_check**  method (see `__init__`) to check
    which of the **programs** provides best support for a feature. The
    **feature_check** function checks single program at once and assigns it 
    score points. The higher score means the better support for a feature.

    **Example**

    Thi following code looks for best available ``sed`` program::

        def _check_prog_sed(context, *args, **kw):
            context.Display("Checking for a sed that does not truncate output... ")
            context.sconf.cached = 1
            # Script should not contain more than 9 commands (for HP-UX sed),
            # but more than about 7000 bytes, to cacth a limit in Solaris 8
            # /usr/ucb/sed.
            line = 's/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb/'
            script = "\\n".join(128 * [ line ]) + "\\n"
            programs = ['sed', 'gsed']
            progargs = ['-f', '$SOURCE']
            action = _PathProgsFeatureCheck(_feature_check_length, programs, progargs)
            stat, out = context.TryAction(action, text = script, extension = '.sed')
            if stat and out:
                context.Result(out)
                return out
            else:
                context.Result('not found')
                return None


    .. _`_AC_PATH_PROGS_FEATURE_CHECK`: http://git.savannah.gnu.org/cgit/autoconf.git/tree/lib/autoconf/programs.m4
    """
    def __init__(self, feature_check, programs, program_args, *args, **kw):
        """Initializes `_PathProgsFeatureCheck`.

        :Parameters:
            feature_check
                function or callable object, with the following interface::

                    feature_check(env, cmd)

                where the ``env`` is a `SCons environment`_ and ``cmd`` is
                command to be tested (program name + arguments). The
                ``feature_check`` method should check whether (and how well)
                the ``cmd`` support feature and return score representing
                feature support (0 - no support, the higher score the better
                support for feature).
            programs
                list of programs to be checked
            program_args
                list of arguments passed to each programs when checking it

        .. _SCons environment:  http://www.scons.org/doc/HTML/scons-user.html#chap-environments
        """
        self.feature_check = feature_check
        self.programs = programs
        self.program_args = program_args
        self.args = args
        self.kw = kw

    def __call__(self, target, source, env):
        from SCons.Util import CLVar
        import os
        max_score = 0
        max_score_program = None
        for program in self.programs:
            path = env.WhereIs(program)
            if not path or not os.access(path, os.X_OK):
                continue
            cmd = CLVar(program) + CLVar(self.program_args)
            cmd = env.subst(cmd, target = target, source = source)
            score = self.feature_check(env, cmd, *self.args, **self.kw)
            if score > max_score:
                max_score = score
                max_score_program = program
        if max_score_program:
            # Cache the result to the target file.
            with open(env.subst('$TARGET', target = target), 'wt') as f:
                f.write(max_score_program)
            return 0
        else:
            return 1

###############################################################################
def _feature_check_length(env, cmd, match_string = ''):
    """Corresponds to `_AC_FEATURE_CHECK_LENGTH`_.

    For use as the **feature_test** argument to `_PathProgsFeatureCheck`. On
    each iteration run **cmd** providing an auto-generated input text to its
    **stdin** and looking at its **stdout**. The input string is always one
    line, starting with only 10 characters, and doubling in length at each
    iteration until approx 10000 characters.

    .. _`_AC_FEATURE_CHECK_LENGTH`: http://git.savannah.gnu.org/cgit/autoconf.git/tree/lib/autoconf/programs.m4
    """
    from SCons.Action import _subproc
    from subprocess import PIPE
    count = 0
    # 10*(2^10) chars as input seems more than enough
    while count < 10:
        content = (2**(1+count) * '0123456789') + "\n"
        try:
            proc = _subproc(env, cmd, 'raise', stdin = PIPE, stdout = PIPE)
        except EnvironmentError:
            break
        else:
            # we ignore stderr; same way as it was in _AC_FEATURE_CHECK_LENGTH
            output = proc.communicate(content)
            if proc.wait() != 0:
                break
            #if not (output == content):
            #    break
            count += 1
    return count

###############################################################################
def _check_prog(context, prog, value_if_found=None, value_if_not_found=None,
               path=None, pathext=None, reject=[], prog_str = None):
    """Corresponds to AC_CHECK_PROG_ autoconf macro.

    Check whether program **prog** exists in **path**. If it is found, the
    function returns **value_if_found** (which defaults to **prog**). Otherwise
    it returns **value_if_not_found** (which defaults to ``None``).

    :Parameters:
        context
            SCons configuration context.
        prog
            Program name of the program to be checked.
        value_if_found
            Value to be returned, when the program is found.
        value_if_not_found
            Value to be returned, when the program is not found.
        path
            Search path.
        pathext
            Extensions used for executable files.
        reject
            List of file names to be rejected if found.
        prog_str
            Used to display 'Checking for <prog_str>...' message.

    .. _AC_CHECK_PROG: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fCHECK_005fPROG-304
    """

    if value_if_found is None:
        value_if_found = prog

    if prog_str is None:
        prog_str = prog

    context.Display("Checking for %s... " % prog_str)
    path = context.env.WhereIs(prog, path, pathext, reject)
    if path:
        context.Result(prog)
        return value_if_found
    if value_if_not_found:
        context.Result("not found, using '%s'" % value_if_not_found)
    else:
        context.Result('not found')
    return value_if_not_found

###############################################################################
def _check_progs(context, progs, value_if_not_found=None, path=None, pathext=None,
                reject=[], prog_str = None):
    """Corresponds to AC_CHECK_PROGS_ autoconf macro.

    Check for each program in **progs** list existing in **path**. If one is
    found, return the name of that program. Otherwise, continue checking the
    next program in the list. If none of the programs in the list are found,
    return the **value_if_not_found** (which defaults to ``None``).

    :Parameters:
        context
            SCons configuration context.
        progs
            Program names of the programs to be checked.
        value_if_not_found
            Value to be returned, when the program is not found.
        path
            Search path.
        pathext
            Extensions used for executable files.
        reject
            List of file names to be rejected if found.
        prog_str
            Used to display 'Checking for <prog_str>...' message.

    .. _AC_CHECK_PROGS: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fCHECK_005fPROGS-307
    """

    if prog_str is None:
        if len(progs) > 1:
            prog_str = ' or '.join([', '.join(progs[:-1]), progs[-1]])
        elif len(progs) == 1:
            prog_str = progs[0]
    context.Display("Checking for %s... " % prog_str)

    for prog in progs:
        path = context.env.WhereIs(prog, path, pathext, reject)
        if path:
            context.Result(prog)
            return prog
    if value_if_not_found:
        context.Result("not found, using '%s'" % value_if_not_found)
    else:
        context.Result('not found')
    return value_if_not_found

###############################################################################
def _check_target_tool(context, prog, value_if_not_found=None,
                     path=None, pathext=None, reject=[]):
    """Corresponds to AC_CHECK_TARGET_TOOL_ autoconf macro.

    .. _AC_CHECK_TARGET_TOOL: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fCHECK_005fTARGET_005fTOOL-310
    """
    # TODO: first I need to know how to determine AC_CANONICAL_TARGET
    raise NotImplementedError("not implemented")

###############################################################################
def _check_tool(context, prog, value_if_not_found=None,
               path=None, pathext=None, reject=[]):
    """Corresponds to AC_CHECK_TOOL_ autoconf macro.

    .. _AC_CHECK_TOOL: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fCHECK_005fTOOL-312
    """
    # TODO: first I need to know how to determine AC_CANONICAL_HOST
    raise NotImplementedError("not implemented")

###############################################################################
def _check_target_tools(context, progs, value_if_not_found=None,
                      path=None, pathext=None, reject=[]):
    """Corresponds to AC_CHECK_TARGET_TOOLS_ autoconf macro.

    .. _AC_CHECK_TARGET_TOOLS: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fCHECK_005fTARGET_005fTOOLS-314
    """
    # TODO: first I need to know how to determine AC_CANONICAL_TARGET
    raise NotImplementedError("not implemented")

###############################################################################
def _check_tools(context, progs, value_if_not_found=None,
                path=None, pathext=None, reject=[]):
    """Corresponds to AC_CHECK_TOOLS_ autoconf macro.

    .. _AC_CHECK_TOOLS: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fCHECK_005fTOOLS-316
    """
    # TODO: first I need to know how to determine AC_CANONICAL_HOST
    raise NotImplementedError("not implemented")

###############################################################################
def _check_path_prog(context, prog, value_if_not_found=None, path=None,
                   pathext=None, reject=[], prog_str=None):
    """Corresponds to AC_PATH_PROG_ autoconf macro.

    .. _AC_PATH_PROG: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPATH_005fPROG-318
    """
    if prog_str is None:
        prog_str = prog

    context.Display("Checking for %s... " % prog_str)
    path = context.env.WhereIs(prog, path, pathext, reject)
    if path:
        context.Result(path)
        return path
    if value_if_not_found:
        context.Result("not found, using '%s'" % value_if_not_found)
    else:
        context.Result('not found')
    return value_if_not_found

###############################################################################
def _check_path_progs(context, progs, value_if_not_found=None, path=None,
                    pathext=None, reject=[], prog_str=None):
    """Corresponds to AC_PATH_PROGS_ autoconf macro.

    .. _AC_PATH_PROGS: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPATH_005fPROGS-321
    """

    if prog_str is None:
        if len(progs) > 1:
            prog_str = ' or '.join([', '.join(progs[:-1]), progs[-1]])
        elif len(progs) == 1:
            prog_str = progs[0]
    context.Display("Checking for %s... " % prog_str)

    for prog in progs:
        path = context.env.WhereIs(prog, path, pathext, reject)
        if path:
            context.Result(path)
            return path
    if value_if_not_found:
        context.Result("not found, using '%s'" % value_if_not_found)
    else:
        context.Result('not found')
    return value_if_not_found

###############################################################################
def _check_path_target_tool(context, prog, value_if_not_found=None,
                         path=None, pathext=None, reject=[]):
    """Corresponds to AC_PATH_TARGET_TOOL_ autoconf macro.

    .. _AC_PATH_TARGET_TOOL: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPATH_005fTARGET_005fTOOL-329
    """
    # TODO: first I need to know how to determine AC_CANONICAL_TARGET
    raise NotImplementedError("not implemented")

###############################################################################
def _check_path_tool(context, prog, value_if_not_found=None,
                   path=None, pathext=None, reject=[]):
    """Corresponds to AC_PATH_TOOL_ autoconf macro.

    .. _AC_PATH_TOOL: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPATH_005fTOOL-331
    """
    # TODO: first I need to know how to determine AC_CANONICAL_HOST
    raise NotImplementedError("not implemented")


###############################################################################
def _check_prog_awk(context,*args,**kw):
    """Corresponds to AC_PROG_AWK_ autoconf macro

    .. _AC_PROG_AWK: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fAWK-254
    """
    kw['prog_str'] = 'awk'
    return _check_progs(context,['gawk', 'mawk', 'nawk', 'awk'], *args, **kw)

###############################################################################
def _check_prog_grep(context,*args,**kw):
    """Corresponds to AC_PROG_GREP_ autoconf macro

    .. _AC_PROG_GREP: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fGREP-258
    """
    context.Display("Checking for grep that handles long lines and -e... ")
    raise NotImplementedError("not implemented")

###############################################################################
def _check_prog_egrep(context,*args,**kw):
    """Corresponds to AC_PROG_EGREP_ autoconf macro

    .. _AC_PROG_EGREP: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fEGREP-262
    """
    context.Display("Checking for egrep... ")
    raise NotImplementedError("not implemented")

###############################################################################
def _check_prog_fgrep(context,*args,**kw):
    """Corresponds to AC_PROG_FGREP_ autoconf macro

    .. _AC_PROG_FGREP: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fFGREP-266
    """
    context.Display("Checking for fgrep... ")
    raise NotImplementedError("not implemented")

###############################################################################
def _check_prog_install(context,*args,**kw):
    """Corresponds to AC_PROG_INSTALL_ autoconf macro

    .. _AC_PROG_INSTALL: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fINSTALL-270
    """
    context.Display("Checking for a BSD-compatible install... ")
    raise NotImplementedError("not implemented")

###############################################################################
def _check_prog_mkdir_p(context,*args,**kw):
    """Corresponds to AC_PROG_MKDIR_P_ autoconf macro

    .. _AC_PROG_MKDIR_P: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fMKDIR_005fP-277
    """
    context.Display("Checking for a thread-safe mkdir -p... ")
    raise NotImplementedError("not implemented")

###############################################################################
def _check_prog_lex(context,*args,**kw):
    """Corresponds to AC_PROG_LEX_ autoconf macro

    .. _AC_PROG_LEX: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fLEX-281
    """
    kw['prog_str'] = 'lex'
    raise NotImplementedError("not implemented")
    return _check_progs(['flex', 'lex'], *args, **kw)

###############################################################################
def _check_prog_ln_s(context,*args,**kw):
    """Corresponds to AC_PROG_LN_S_ autoconf macro

    .. _AC_PROG_LN_S: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fLN_005fS-288
    """
    context.Display("Checking whether ln -s works... ")
    raise NotImplementedError("not implemented")

###############################################################################
def _checkProg_ranlib(context,*args,**kw):
    """Corresponds to AC_PROG_RANLIB_ autoconf macro

    .. _AC_PROG_RANLIB: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fRANLIB-291
    """
    raise NotImplementedError("not implemented")
    return _check_tool('ranlib',*args,**kw)

###############################################################################
def _check_prog_sed(context,*args,**kw):
    """Corresponds to AC_PROG_SED_ autoconf macro

    .. _AC_PROG_SED: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fSED-294
    """
    context.Display("Checking for a sed that does not truncate output... ")
    context.sconf.cached = 1
    # Script should not contain more than 9 commands (for HP-UX sed),
    # but more than about 7000 bytes, to cacth a limit in Solaris 8
    # /usr/ucb/sed.
    line = 's/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb/'
    script = "\n".join(128 * [ line ]) + "\n"
    programs = ['sed',  'gsed']
    progargs = ['-f', '$SOURCE']
    action = _PathProgsFeatureCheck(_feature_check_length, programs, progargs)
    stat, out = context.TryAction(action, text = script, extension = '.sed')
    if stat and out:
        context.Result(out)
        return out
    else:
        context.Result('not found')
        return None

###############################################################################
def _check_prog_yacc(context,*args,**kw):
    """Corresponds to AC_PROG_YACC_ autoconf macro

    .. _AC_PROG_YACC: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fYACC-298
    """
    raise NotImplementedError("not implemented")
    kw['prog_str'] = 'yacc'
    return _check_progs(['bison', 'byacc', 'yacc'], *args, **kw)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
