"""`SConsGnu.GProgChecks`

Autoconf-like checks for `Alternative Programs`_. Check whether they exist, and
in some cases whether they support certain features.

**Example**::

    from SConsGnu import GProgChecks

    env = Environment()
    cfg = Configure(env, config_h = 'config.h')
    cfg.AddTests(GProgChecks.Tests())

    install = cfg.CheckProgInstall()



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

from SCons.Script import Delete, Mkdir
from SCons.Action import _subproc
from SCons.Util import CLVar, AppendPath, PrependPath, is_Sequence, is_String
from subprocess import PIPE
import re, os, fnmatch

from SConsGnu.GProgVars import _auto, gvar_names, declare_gvars
from SConsGnu.GProgVars import GVarNames, DeclareGVars

try:
    import cPickle as pickle
except ImportError:
    import pickle

#################################################################################
class _WriteTarget(object):
    """TODO: write documentation"""
    def __init__(self, value):
        """TODO: write documentation"""
        self.value = value
    def __call__(self, target, source, env):
        with open(env.subst("$TARGET", target = target), 'wt') as f:
            f.write(pickle.dumps(self.value))
        return 0
    def strfunction(self, target, source, env):
        objstr = "%s(%r)" % (self.__class__.__name__, self.value)
        tgt = env.subst(target, target = target, source = source)
        src = env.subst(source, target = target, source = source)
        return "%s(%r, %r)" % (objstr, tgt, src)

###############################################################################
class _PathProgsFeatureCheck(object):
    """Corresponds to `_AC_PATH_PROGS_FEATURE_CHECK`_

    Use this as an action for ``context.TryAction()``. This action calls
    the provided **feature_check**  method (see `__init__`) once for each
    program from **programs** to check which of the **programs** provides best
    support for the feature. The **feature_check** function checks single
    program at once and assigns it a score - the higher score, the better is
    support for a feature.

    **Example**

    The following code looks for "best" available ``sed`` program. We select
    the version which accepts longest lines at input::

        def CheckProgSed(context):
            context.Display("Checking for a sed that does not truncate output... ")
            context.sconf.cached = 1
            # Script should not contain more than 9 commands (for HP-UX sed),
            # but more than about 7000 bytes, to cacth a limit in Solaris 8
            # /usr/ucb/sed.
            script = 128 * 's/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb/\\n'
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

                    feature_check(env, cmd [, ...] )

                where the ``env`` is a `SCons environment`_ and ``cmd`` is
                command to be tested (program name + arguments). The method may
                optionally accept additional arguments.

                The ``feature_check`` method should check whether (and how
                well) the ``cmd`` command supports certain feature and return
                score representing feature support (0 - no support, the higher
                score the better support for feature),
            programs
                list of programs to be checked,
            program_args
                list of arguments passed to each program when checking it,
            args
                positional arguments to be passed as additional arguments to
                the **feature_check** function,
            kw
                keyword arguments to be passed as additional arguments to the
                **feature_check** function,

        .. _SCons environment:  http://www.scons.org/doc/HTML/scons-user.html#chap-environments
        """
        self.feature_check = feature_check
        self.programs = programs
        self.program_args = program_args
        self.args = args
        self.kw = kw

    def __call__(self, target, source, env):
        max_score = 0
        max_score_program = None
        for program in self.programs:
            program_path = env.WhereIs(program)
            if not program_path or not os.access(program_path, os.X_OK):
                continue
            cmd = CLVar(program_path) + CLVar(self.program_args)
            cmd = env.subst(cmd, target = target, source = source)
            score = self.feature_check(env, cmd, *self.args, **self.kw)
            if score > max_score:
                max_score = score
                max_score_program = CLVar(program_path)
        if max_score_program:
            # Cache the result to the target file.
            with open(env.subst('$TARGET', target = target), 'wt') as f:
                f.write(pickle.dumps(max_score_program))
            return 0
        else:
            return 1

    def strfunction(self, target, source, env):
        objstr = "%s(%s, %r, %r" % (self.__class__.__name__,
                self.feature_check.__name__, self.programs, self.program_args)
        if self.args:
            objstr = ', '.join([objstr] + map(repr, self.args))
        if self.kw:
            objstr = ', '.join([objstr] + ["%s=%r" % (k,v) for (k,v) in self.kw.iteritems()])
        objstr = objstr + ")"
        tgt = env.subst(target, target = target, source = source)
        src = env.subst(source, target = target, source = source)
        return "%s(%r, %r)" % (objstr, tgt, src)

###############################################################################
class _ProgGrep(object):
    """Corresponds to `_AC_PROG_GREP`_

    This is an action to be used in `CheckProgGrep`, `CheckProgEgrep` and
    `CheckProgFgrep`. It selects the **grep** program which supports longest
    lines at stdin. Additionally it may check if the **grep** program supports
    special flags such as ``-E`` or ``-F`` and if not it may select alternative
    programs such as **egrep** (instead of ``grep -E``) or **fgrep** (instead
    of ``grep -F``). For `CheckProgEgrep` and `CheckProgFgrep` it first tries
    "standard" grep command (discovered previously by `CheckProgGrep`) with
    appropriate arguments (**grep_args**, see `__init__`) and if the command
    fails, it selects a program from **programs** list, the one which supports
    longest lines.

    .. _`_AC_PROG_GREP`: http://git.savannah.gnu.org/cgit/autoconf.git/tree/lib/autoconf/programs.m4
    """
    def __init__(self, grep = None, grep_args = None, grep_input = '\n',
                 programs = None, program_args = None, *args, **kw):
        """
        **Example**:

        The following code checks for grep::

            args = ['-e', 'GREP$', '-e', '-(cannot match)-']
            action = _ProgGrep(None, None, None, ['grep', 'ggrep'], args, 'GREP')
            stat, out = context.TryAction(action)

        **Example**:

        The following code checks for egrep::

            grep = '/bin/grep'
            action = _ProgGrep(grep, ['-E', '(a|b)'], 'a\\n', ['egrep'], ['EGREP$'],'EGREP')
            stat, out = context.TryAction(action)

        **Example**:

        The following code checks for fgrep::

            grep = '/bin/grep'
            action = _ProgGrep(grep, ['-F', 'ab*c'], 'ab*c\\n', ['fgrep'], ['FGREP'],'FGREP')
            stat, out = context.TryAction(action)

        :Parameters:
            grep
                absolute path to grep program discovered by `CheckProgGrep`
            grep_args
                arguments to necessary to check egrep or fgrep behavior of the
                "standard" grep program, for egrep set it to ``['-E',
                '(a|b)']``, for fgrep set ``['-F', 'ab*c']``,
            grep_input
                input string necessary to check egrep or fgrep behavior of the
                "standard" grep command, for egrep set it to ``"a\\n"``, for
                fgrep set it to ``"ab*c"``
            programs
                alternative programs to check, for egrep set it to
                ``['egrep']``, for fgrep set it to ``['fgrep']``,
            program_args
                arguments necessary to check the **programs** for either egrep
                or fgrep behavior, for egrep set it to ``['EGREP$']``, for
                fgrep set it to ``['FGREP']``.
            args
                passed directly to `_feature_check_length`
            kw
                passed directly to `_feature_check_length`
        """
        self.grep = grep
        self.grep_args = grep_args
        self.grep_input = grep_input
        self.programs = programs
        self.program_args = program_args
        self.args = args
        self.kw = kw

    def __call__(self, target, source, env):
        if self.grep:
            grep = env.subst(self.grep, target = target, source = source)
            if is_Sequence(grep):
                grep_prog = grep[0]
            else:
                grep_prog = grep
            path = env['ENV'].get('PATH','')
            path = AppendPath(path, '/usr/xpg4/bin')
            grep_path = env.WhereIs(grep_prog, path = path)
            if grep_path:
                cmd = CLVar(grep_path)
                if self.grep_args is not None:
                    cmd.extend(CLVar(self.grep_args))
                try:
                    proc = _subproc(env, cmd, 'raise', stdin = PIPE, stdout = PIPE)
                except EnvironmentError:
                    pass
                else:
                    # we ignore stderr; same way as it was in _AC_FEATURE_CHECK_LENGTH
                    out, err = proc.communicate(self.grep_input)
                    stat = proc.wait()
                    if stat == 0:
                        tgt = env.subst('$TARGET', target = target)
                        with open(tgt, 'wt') as f:
                            f.write(pickle.dumps(cmd[:2]))
                        return 0
        if self.programs:
            programs = self.programs
            progargs = self.program_args
            if progargs is None:
                progargs = []
            action = _PathProgsFeatureCheck(_feature_check_length, programs, progargs, *self.args, **self.kw)
            return action(target,source, env)
        return 1

    def strfunction(self, target, source, env):
        objstr = "%s(%r, %r, %r, %r, %r" % (self.__class__.__name__,
                    self.grep, self.grep_args, self.grep_input, self.programs,
                    self.program_args)
        if self.args:
            objstr = ', '.join([objstr] + map(repr, self.args))
        if self.kw:
            objstr = ', '.join([objstr] + ["%s=%r" % (k,v) for (k,v) in self.kw.iteritems()])
        objstr = objstr + ")"
        tgt = env.subst(target, target = target, source = source)
        src = env.subst(source, target = target, source = source)
        return "%s(%r, %r)" % (objstr, tgt, src)

###############################################################################
class _ProgInstall(object):
    """Finds a good install program.

    This is an action to be used in `CheckProgInstall`. It finds a good install
    program avoiding broken or incompatible versions:

    - SysV ``/etc/install``, ``/usr/sbin/install``
    - SunOS ``/usr/etc/install``
    - IRIX ``/sbin/install``
    - AIX ``/bin/install``
    - AmigaOS ``/C/install``, which installs bootblocks on floppy discs
    - AIX 4 ``/usr/bin/installbsd``, which doesn't work without a ``-g`` flag
    - AFS ``/usr/afsws/bin/install``, which mishandles nonexistent args
    - SVR4 ``/usr/ucb/install``, which tries to use the nonexistent group "staff"
    - OS/2's system ``install``, which has a completely different semantic
    - ``./install``, which can be erroneously created by make from ``./install.sh``.
    """
    def __init__(self, programs=None, reject_paths=None):
        """Initialize ``_ProgInstall`` object.

        :Parameters:
            programs
                list of programs to be checked for, if ``None``,  the action
                will check for ``ginstall``, ``scoinst``, and ``install`` in
                this order,
            reject_paths
                a list of globs to be excluded from search path when looking
                for ``install`` program,

        """
        self.programs = programs
        self.reject_paths = reject_paths

    def _check_install_prog(self, target, source, env, prog_path):
        install_dir = env.subst("${TARGET}.dir", target = target, source = source)
        base_names = ["${TARGET.file}.one", "${TARGET.file}.two"]
        base_names = env.subst(base_names, target = target, source = source)
        to_install = [ os.path.join("${TARGET.dir}", x) for x in base_names ]
        to_install = env.subst(to_install, target = target, source = source)
        installed = [ os.path.join(install_dir, x) for x in base_names ]
        installed = env.subst(installed, target = target, source = source)

        temps = to_install + installed + [install_dir]
        delete_temps = Delete(temps)

        # Delete files that could be left by previous (interrupted) action
        env.Execute(delete_temps)

        for ti in to_install:
            with open(ti, 'w') as f:
                f.write(ti + "\n")

        env.Execute(Mkdir(install_dir))

        install_dir_abs = env.Dir(install_dir).abspath
        cmd = CLVar(prog_path) + CLVar('-c') + CLVar(to_install) + CLVar(install_dir_abs)

        try:
            if env.Execute(str(cmd)):
                return None
            # Verify the size of the installed files
            for f in installed:
                try:
                    if os.stat(f).st_size <= 0:
                        return None
                except OSError:
                    return None
        finally:
            # Delete temporary files
            env.Execute(delete_temps)
        return cmd[:2]

    def __call__(self, target, source, env):
        path = env.get('ENV',{}).get('PATH','').split(os.pathsep)

        programs = self.programs
        reject_paths = self.reject_paths
        if programs is None:
            programs = ['ginstall', 'scoinst', 'install']
        if reject_paths is None:
            reject_paths =  [
                './', './/', '/[cC]/*', '/etc/*', '/usr/sbin/*', '/usr/etc/*',
                '/sbin/*', '/usr/afsws/bin/*', '?:[\\/]os2[\\/]install[\\/]*',
                '?:[\\/]OS2[\\/]INSTALL[\\/]*', '/usr/ucb/*'
            ]
        for dir in path:
            matches = False
            for glob in reject_paths:
                if fnmatch.fnmatch(dir, glob):
                    matches = True
                    break
            if not matches:
                for prog in programs:
                    prog_path = env.WhereIs(prog, path = dir)
                    if prog_path:
                        with open(prog_path, 'r') as prog_fd:
                            content = prog_fd.read()
                        if prog == 'install' and (0 <= content.find('dspmsg')):
                            # AIX install. It has an incomplete calling convention.
                            return 1 # Failed
                        elif prog == 'install' and (0 <= content.find('pwplus')):
                            # program-specific install script used by HP pwplus--don't use.
                            return 1 # Failed
                        else:
                            result = self._check_install_prog(target, source, env, prog_path)
                            if result:
                                with open(env.subst('$TARGET', target = target), 'w') as f:
                                    f.write(pickle.dumps(result))
                                return 0 # Success
        return 1 # Failed

    def strfunction(self, target, source, env):
        objstr = "%s(%r, %r)" % (self.__class__.__name__, self.programs, self.reject_paths)
        tgt = env.subst(target, target = target, source = source)
        src = env.subst(source, target = target, source = source)
        return "%s(%r, %r)" % (objstr, tgt, src)

###############################################################################
class _ProgMkdirP(object):
    """Check whether ``mkdir -p`` is known to be thread-safe, and fall back to
    ``install-sh -d`` otherwise.

    This action object is to be used by `CheckProgMkdirP` method.

    We cannot accept any implementation of ``mkdir`` that recognizes ``-p``.
    Some implementation (such as Solaris 8's) are vulnerable to race
    conditions: if a parallel make tries to run ``mkdir -p a/b`` and ``mkdir -p
    a/c`` concurrently, both versions can detect that ``a/`` is missing, but
    only one can create it and the other will error out. Consequently we
    restrict ourselves to known race-free implementations.
    """
    def __init__(self, programs = None):
        """Initialize _ProgMkdirP object.

        :Parameters:
            programs
                list of program names to be checked, if ``None``, the default
                list ``[ 'mkdir', 'gmkdir' ]`` is used
        """
        self.programs = programs

    def _check_mkdir_prog(self, target, source, env, prog_path):
        from SCons.Script import Delete
        from SCons.Action import _subproc
        from SCons.Util import CLVar
        from subprocess import PIPE
        import re, os
        cmd = CLVar(prog_path) + CLVar('--version')
        try:
            proc = _subproc(env, cmd, 'raise', stdin = PIPE, stdout = PIPE)
        except EnvironmentError:
            return None
        else:
            out, err = proc.communicate()
            xpr = r'mkdir (\(GNU coreutils\)|\(coreutils\)|\(fileutils\) 4\.1)'
            if re.findall(xpr, out):
                return CLVar([prog_path, '-p'])
        finally:
            if os.path.isdir("./--version"):
                env.Execute(Delete("./--version"))
        return None


    def __call__(self, target, source, env):
        path = env.get('ENV',{}).get('PATH','').split(os.pathsep) + [ '/opt/sfw/bin' ]

        programs = self.programs
        if programs is None:
            programs = ['mkdir', 'gmkdir']

        for dir in path:
            for prog in programs:
                prog_path = env.WhereIs(prog, path = dir)
                if prog_path:
                    result = self._check_mkdir_prog(target, source, env, prog_path)
                    if result:
                        with open(env.subst('$TARGET', target = target), 'w') as f:
                            f.write(pickle.dumps(result))
                        return 0 # Success

        # FIXME: actually we should return '$ac_install_sh -d' here.
        return 1 # Failed

    def strfunction(self, target, source, env):
        objstr = "%s(%r)" % (self.__class__.__name__, self.programs)
        tgt = env.subst(target, target = target, source = source)
        src = env.subst(source, target = target, source = source)
        return "%s(%r, %r)" % (objstr, tgt, src)

###############################################################################
class _ProgSed(object):
    """Check for a fully functional sed program that truncates as few
    characters as possible. Prefer GNU sed if found.

    This action object is to be used by `CheckProgSed` method.
    """
    def __init__(self, programs):
        """Initialize _ProgSed object.

        :Parameters:
            programs
                list of program names to be checked, if ``None``, the default
                list ``[ 'sed', 'gsed' ]`` will be used.
        """
        self.programs = programs

    def __call__(self, target, source, env):
        # Script should not contain more than 9 commands (for HP-UX sed),
        # but more than about 7000 bytes, to cacth a limit in Solaris 8
        # /usr/ucb/sed.
        script = 128 * 's/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb/\n'
        script_file = env.subst("${TARGET}.sed", target = target, source = source)
        programs = self.programs
        if programs is None:
            programs = ['sed', 'gsed']
        progargs = ['-f', script_file]

        with open(script_file,'w') as f:
            f.write(script)
        try:
            action = _PathProgsFeatureCheck(_feature_check_length, programs, progargs)
            result = action(target, source, env)
        finally:
            env.Execute(Delete(script_file))

        return result

    def strfunction(self, target, source, env):
        objstr = "%s(%r)" % (self.__class__.__name__, self.programs)
        tgt = env.subst(target, target = target, source = source)
        src = env.subst(source, target = target, source = source)
        return "%s(%r, %r)" % (objstr, tgt, src)

###############################################################################
_lex_script = """
%%
a { ECHO; }
b { REJECT; }
c { yymore (); }
d { yyless (1); }
e { /* IRIX 6.5 flex 2.5.4 underquotes its yyless argument.  */
    yyless ((input () != 0)); }
f { unput (yytext[0]); }
. { BEGIN INITIAL; }
%%
#ifdef YYTEXT_POINTER
extern char *yytext;
#endif
int
main (void)
{
  return ! yylex () + ! yywrap ();
}
"""

###############################################################################
class _LexExe(object):
    """Look for the flex of lex.

    This action object is to be used by `CheckLexExe` method.
    """

    def __init__(self, programs):
        """Initialize _LexExe object.

        :Parameters:
            programs
                list of program names to be checked, if ``None``, the default
                list ``[ 'flex', 'lex' ]`` will be used,
        """
        self.programs = programs

    def __call__(self, target, source, env):
        programs = self.programs
        if programs is None:
            programs = ['flex', 'lex']
        path = env['ENV'].get('PATH')
        for prog in programs:
            path = env.WhereIs(prog, path = path)
            if path:
                lex = CLVar(prog)
                with open(env.subst('$TARGET', target = target), 'wt') as f:
                    f.write(pickle.dumps(lex))
                return 0
        return 1

    def strfunction(self, target, source, env):
        objstr = "%s(%r)" % (self.__class__.__name__, self.programs)
        tgt = env.subst(target, target = target, source = source)
        src = env.subst(source, target = target, source = source)
        return "%s(%r, %r)" % (objstr, tgt, src)

###############################################################################
class _LexFeatureCheck(object):
    def __init__(self, lex, script):
        self.lex = lex
        self.script = script

    def _check_lex_feature(self, target, source, env, **kw):
        global _lex_script
        lexdir = env.subst('${TARGET}.dir', target = target, source = source)
        lexfile = env.subst("${TARGET.file}.l", target = target, source = source)
        lexcmd = str(CLVar(self.lex) + CLVar(lexfile))

        script = self.script
        if script is None:
            script = _lex_script

        env.Execute(Mkdir(lexdir))
        with open(os.path.join(lexdir, lexfile) ,'w') as f:
            f.write(script)

        try:
            err = env.Execute(lexcmd, chdir = lexdir)
            if not err:
                kw2 = kw.copy()
                kw2.update({ 'lexdir' : lexdir,
                             'lexfile' : lexfile,
                             'lexcmd' : lexcmd,
                             'script' : script })
                err = self._lex_feature(target, source, env, **kw2)
        finally:
            env.Execute(Delete(env.Glob(os.path.join(lexdir,'*'))))
            env.Execute(Delete(lexdir))

        return err

###############################################################################
class _LexFileRoot(_LexFeatureCheck):
    """TODO: write documentation
    """
    def __init__(self, lex, lexroots, script):
        """Initialize _LexFileRoot object.

        TODO: write documentation
        """
        self.lexroots = lexroots
        super(_LexFileRoot,self).__init__(lex, script)

    def __call__(self, target, source, env):
        lexroots = self.lexroots
        if lexroots is None:
            lexroots = [ 'lex.yy', 'lexyy' ]
        return self._check_lex_feature(target, source, env, lexroots = lexroots)

    def _lex_feature(self, target, source, env, lexroots, lexdir,  **kw):
        for lexroot in lexroots:
            lexcfile = os.path.join(lexdir, '%s.c' % lexroot)
            if os.path.isfile(lexcfile):
                with open(env.subst('$TARGET', target = target), 'wt') as f:
                    f.write(pickle.dumps(lexroot))
                return 0
        return 1

    def strfunction(self, target, source, env):
        objstr = "%s(%r,%r,%r)" % (self.__class__.__name__, self.lex, self.lexroots, self.script)
        tgt = env.subst(target, target = target, source = source)
        src = env.subst(source, target = target, source = source)
        return "%s(%r, %r)" % (objstr, tgt, src)

###############################################################################
class _LexOutput(_LexFeatureCheck):
    """TODO: write documentation
    """
    def __init__(self, lex, lexroot, script):
        """Initialize _LexLibs object.

        TODO: write documentation
        """
        self.lexroot = lexroot
        super(_LexOutput,self).__init__(lex, script)

    def __call__(self, target, source, env):
        return self._check_lex_feature(target, source, env)

    def _lex_feature(self, target, source, env, lexdir, **kw):
        lexcfile = os.path.join(lexdir, '%s.c' % self.lexroot)
        with open(lexcfile, 'r') as f:
            text = f.read()
        with open(env.subst('$TARGET', target = target), 'wt') as f:
            f.write(pickle.dumps(text))
        return 0

    def strfunction(self, target, source, env):
        objstr = "%s(%r,%r,%r)" % (self.__class__.__name__, self.lex, self.lexroot, self.script)
        tgt = env.subst(target, target = target, source = source)
        src = env.subst(source, target = target, source = source)
        return "%s(%r, %r)" % (objstr, tgt, src)

###############################################################################
class _ProgLnS(object):
    """TODO: Write documentation"""
    def __call__(self, target, source, env):
        import SCons.Errors
        import traceback
        import sys

        tmpdir = env.subst('${TARGET}.dir', target = target, source = source)
        tmpconf = os.path.join(tmpdir, 'conf')
        confdir = "%s.dir" % tmpconf
        confile = "%s.file" % tmpconf

        ln_s = CLVar(['cp','-pR'])
        if not env.Execute(Mkdir(tmpdir)):
            try:
                with open(confile, 'w') as f:
                    f.write('')
                try:
                    if not env.Execute('ln -s %s %s' %(confile, tmpconf)):
                        try:
                            if not env.Execute(Mkdir(confdir)):
                                try:
                                    if not env.Execute('ln -s %s %s' %(confile, confdir)):
                                        try:
                                            if not os.path.isfile('%s.exe' % tmpconf):
                                                ln_s = CLVar(['ln','-s'])
                                        finally:
                                            glob = os.path.join(confdir,'*')
                                            env.Execute(Delete(env.Glob(glob)))
                                finally:
                                    env.Execute(Delete(confdir))
                        finally:
                            env.Execute(Delete(tmpconf))
                    else:
                        if env.Execute('ln %s %s' % (confile, tmpconf)) == 0:
                            ln_s = CLVar('ln')
                            env.Execute(Delete(tmpconf))
                finally:
                    env.Execute(Delete(confile))
            finally:
                env.Execute(Delete(tmpdir))

        with open(env.subst('$TARGET', target = target), 'w') as f:
            f.write(pickle.dumps(ln_s))

        return 0 
    def strfunction(self, target, source, env):
        objstr = "%s()" % (self.__class__.__name__)
        tgt = env.subst(target, target = target, source = source)
        src = env.subst(source, target = target, source = source)
        return "%s(%r, %r)" % (objstr, tgt, src)


###############################################################################
class _ActionWrapper(object):
    """Wrapper used to handle properly the **selection** argument present in
    most of the program checks.
    """
    def __init__(self, check):
        self.check = check

    def __call__(self, target, source, env):
        try:
            with open(env.subst("$SOURCE", source = source), 'r')  as sf:
                args = pickle.loads(sf.read())
                try:
                    selection = args.get('selection', _auto)
                except AttributeError:
                    selection = _auto
        except IOError:
            selection = _auto

        if selection is _auto:
            return self.check(target, source, env)
        else:
            with open(env.subst("$TARGET", target = target), 'w') as tf:
                selection = CLVar(selection)
                tf.write(pickle.dumps(selection))
            return 0

    def __getattr__(self, name):
        return getattr(self.check, name)

    def strfunction(self, target, source, env):
        if hasattr(self.check, 'strfunction'):
            return self.check.strfunction(target, source, env)
        else:
            return str(self.check) + "(%r,%r,%r)" % (target, source, env)

###############################################################################
def _path_prog_flavor_gnu(env, program):
    """Corresponds to `_AC_PATH_PROG_FLAVOR_GNU`_.

    Check if **program** is a GNU program.

    :Parameters:
        program
            path to the program

    :Returns:
        `True` if **program** is a GNU program or `False` othrewise.

    .. _`_AC_PATH_PROG_FLAVOR_GNU`: http://git.savannah.gnu.org/cgit/autoconf.git/tree/lib/autoconf/programs.m4
    """
    cmd = CLVar(program) + CLVar('--version')
    try:
        proc = _subproc(env, cmd, 'raise', stdin = PIPE, stdout = PIPE)
    except EnvironmentError:
        return False
    else:
        out, err = proc.communicate()
        if re.findall(r'GNU', out):
            return True
    return False


###############################################################################
def _feature_check_length(env, cmd, match_string = None):
    """Corresponds to `_AC_FEATURE_CHECK_LENGTH`_.

    For use as the **feature_test** argument to `_PathProgsFeatureCheck`. On
    each iteration run **cmd** providing an auto-generated input text to its
    **stdin** and looking at its **stdout**. The input string is always one
    line, starting with only 10 characters, and doubling in length at each
    iteration until approx 10000 characters.

    .. _`_AC_FEATURE_CHECK_LENGTH`: http://git.savannah.gnu.org/cgit/autoconf.git/tree/lib/autoconf/programs.m4
    """
    score = 0
    score_max = 10 # 10*(2^10) chars as input seems more than enough

    prog = CLVar(cmd)[0]
    if _path_prog_flavor_gnu(env, prog):
        # seems like autoconf trust all GNU programs.
        return score_max

    while score < score_max:
        content = (2**(1+score) * '0123456789')
        if match_string: content = content + match_string
        content = content + '\n'
        try:
            proc = _subproc(env, cmd, 'raise', stdin = PIPE, stdout = PIPE)
        except EnvironmentError:
            break
        else:
            # we ignore stderr; same way as it was in _AC_FEATURE_CHECK_LENGTH
            out, err = proc.communicate(content)
            if proc.wait() != 0:
                break
            if not (out == content):
                break
            score += 1
    return score

###############################################################################
def CheckProg(context, program, selection=_auto, value_if_found=None,
              value_if_not_found=None, path=None, pathext=None, reject=[],
              prog_str=None):
    """Corresponds to AC_CHECK_PROG_ autoconf macro.

    Check whether **program** exists in **path**. If it is found, the function
    returns **value_if_found** (which defaults to **prog**). Otherwise
    it returns **value_if_not_found** (which defaults to ``None``).

    :Parameters:
        context
            SCons configuration context.
        program
            Program name of the program to be checked.
        selection
            If `_auto` (default), the program will be found automatically,
            otherwise the method will return the value of **selection**.
        value_if_found
            Value to be returned, when the program is found.
        value_if_not_found
            Value to be returned, when the program is not found.
        path
            Search path. If ``None``, then ``context.env['ENV']['PATH']`` will
            be used.
        pathext
            Extensions used for executable files.
        reject
            List of file names to be rejected if found.
        prog_str
            Used to display 'Checking for <prog_str>...' message.

    .. _AC_CHECK_PROG: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fCHECK_005fPROG-304
    """
    # Extract the first word of program, so it can be a program name with args.
    progname = CLVar(program)[0]

    if prog_str is None:
        prog_str = progname

    context.Display("Checking for %s... " % prog_str)
    if selection is _auto:

        if value_if_found is None:
            value_if_found = program

        path = context.env.WhereIs(progname, path, pathext, reject)
        if path:
            context.Result(program)
            return value_if_found
        if value_if_not_found:
            context.Result("not found, using '%s'" % value_if_not_found)
        else:
            context.Result('no')
        return value_if_not_found
    else:
        context.Result(str(selection))
        return selection

###############################################################################
def CheckProgs(context, programs, selection=_auto, value_if_not_found=None,
               path=None, pathext=None, reject=[]):
    """Corresponds to AC_CHECK_PROGS_ autoconf macro.

    Check for each program in **programs** list existing in **path**. If one is
    found, return the name of that program. Otherwise, continue checking the
    next program in the list. If none of the programs in the list are found,
    return the **value_if_not_found** (which defaults to ``None``).

    :Parameters:
        context
            SCons configuration context.
        programs
            Program names of the programs to be checked.
        selection
            If `_auto` (default), the program will be found automatically,
            otherwise the method will return the value of **selection**.
        value_if_not_found
            Value to be returned, when the program is not found.
        path
            Search path.
        pathext
            Extensions used for executable files.
        reject
            List of file names to be rejected if found.

    .. _AC_CHECK_PROGS: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fCHECK_005fPROGS-307
    """

    context.did_show_result = 1
    result = None
    if selection is _auto:
        sconf = context.sconf
        for program in programs:
            result = sconf.CheckProg(program, _auto, None, None, path, pathext, reject)
            if result:
                return result
        return value_if_not_found
    else:
        return selection

###############################################################################
def CheckTargetTool(context, prog, value_if_not_found=None, path=None,
                    pathext=None, reject=[]):
    """Corresponds to AC_CHECK_TARGET_TOOL_ autoconf macro.

    .. _AC_CHECK_TARGET_TOOL: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fCHECK_005fTARGET_005fTOOL-310
    """
    # TODO: first I need to know how to determine AC_CANONICAL_TARGET
    raise NotImplementedError("not implemented")

###############################################################################
def CheckTool(context, prog, value_if_not_found=None,
                path=None, pathext=None, reject=[]):
    """Corresponds to AC_CHECK_TOOL_ autoconf macro.

    .. _AC_CHECK_TOOL: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fCHECK_005fTOOL-312
    """
    # TODO: first I need to know how to determine AC_CANONICAL_HOST
    raise NotImplementedError("not implemented")

###############################################################################
def CheckTargetTools(context, programs, value_if_not_found=None,
                     path=None, pathext=None, reject=[]):
    """Corresponds to AC_CHECK_TARGET_TOOLS_ autoconf macro.

    .. _AC_CHECK_TARGET_TOOLS: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fCHECK_005fTARGET_005fTOOLS-314
    """
    # TODO: first I need to know how to determine AC_CANONICAL_TARGET
    raise NotImplementedError("not implemented")

###############################################################################
def CheckTools(context, programs, value_if_not_found=None,
                 path=None, pathext=None, reject=[]):
    """Corresponds to AC_CHECK_TOOLS_ autoconf macro.

    .. _AC_CHECK_TOOLS: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fCHECK_005fTOOLS-316
    """
    # TODO: first I need to know how to determine AC_CANONICAL_HOST
    raise NotImplementedError("not implemented")

###############################################################################
def CheckPathProg(context, program, selection=_auto, value_if_not_found=None,
                  path=None, pathext=None, reject=[], prog_str=None):
    """Corresponds to AC_PATH_PROG_ autoconf macro.

    :Parameters:
        context
            SCons configuration context.
        program
            Name of the program to be checked.
        selection
            If `_auto` (default), the program will be found automatically,
            otherwise the method will return the value of **selection**.
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

    .. _AC_PATH_PROG: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPATH_005fPROG-318
    """
    if prog_str is None:
        prog_str = program

    context.Display("Checking for %s... " % prog_str)

    if selection is _auto:
        progpath = context.env.WhereIs(program, path, pathext, reject)
        if progpath:
            context.Result(progpath)
        else:
            if value_if_not_found:
                progpath = value_if_not_found
                context.Result("not found, using '%s'" % progpath)
            else:
                context.Result('no')
        return progpath
    else:
        context.Result(str(selection))
        return selection

###############################################################################
def CheckPathProgs(context, programs, selection=_auto, value_if_not_found=None,
                   path=None, pathext=None, reject=[]):
    """Corresponds to AC_PATH_PROGS_ autoconf macro.

    :Parameters:
        context
            SCons configuration context.
        programs
            List of program names to be checked.
        selection
            If `_auto` (default), the program will be found automatically,
            otherwise the method will return the value of **selection**.
        value_if_not_found
            Value to be returned, when the program is not found.
        path
            Search path.
        pathext
            Extensions used for executable files.
        reject
            List of file names to be rejected if found.

    .. _AC_PATH_PROGS: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPATH_005fPROGS-321
    """
    context.did_show_result = 1
    result = None
    if selection is _auto:
        sconf = context.sconf
        for program in programs:
            result = sconf.CheckPathProg(program, _auto, None, path, pathext, reject)
            if result:
                return result
        return value_if_not_found
    else:
        return selection

###############################################################################
def CheckPathTargetTool(context, program, value_if_not_found=None,
                        path=None, pathext=None, reject=[]):
    """Corresponds to AC_PATH_TARGET_TOOL_ autoconf macro.

    .. _AC_PATH_TARGET_TOOL: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPATH_005fTARGET_005fTOOL-329
    """
    # TODO: first I need to know how to determine AC_CANONICAL_TARGET
    raise NotImplementedError("not implemented")

###############################################################################
def CheckPathTool(context, program, selection=_auto, value_if_not_found=None,
                   path=None, pathext=None, reject=[]):
    """Corresponds to AC_PATH_TOOL_ autoconf macro.

    :Parameters:
        context
            SCons configuration context.
        selection
            If `_auto` (default), the program will be found automatically,
            otherwise the method will return the value of **selection**.

    .. _AC_PATH_TOOL: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPATH_005fTOOL-331
    """
    # TODO: first I need to know how to determine AC_CANONICAL_HOST
    raise NotImplementedError("not implemented")


###############################################################################
def CheckProgAwk(context, selection=_auto, programs=None):
    """Corresponds to AC_PROG_AWK_ autoconf macro

    :Parameters:
        context
            SCons configuration context.
        selection
            If `_auto` (default), the program will be found automatically,
            otherwise the method will return the value of **selection**.

    .. _AC_PROG_AWK: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fAWK-254
    """
    if programs is None:
        programs = ['gawk', 'mawk', 'nawk', 'awk']
    prog = CheckProgs(context, programs, selection, prog_str = 'awk')
    if prog:
        prog = CLVar(prog)
    return prog


###############################################################################
def CheckProgEgrep(context, grep, selection=_auto):
    """Corresponds to AC_PROG_EGREP_ autoconf macro

    :Parameters:
        context
            SCons configuration context.
        grep
            Path to ``grep`` program as found by `CheckProgGrep`.
        selection
            If `_auto` (default), the program will be found automatically,
            otherwise the method will return the value of **selection**.

    .. _AC_PROG_EGREP: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fEGREP-262
    """
    context.Display("Checking for egrep... ")
    context.sconf.cached = 1
    action = _ProgGrep(grep, ['-E', '(a|b)'], 'a\n', ['egrep'], ['EGREP$'],'EGREP')
    action = _ActionWrapper(action)
    args = pickle.dumps({'grep' : grep, 'selection' : selection})
    stat, out = context.TryAction(action, args, '.arg')
    if stat and out:
        out = pickle.loads(out)
        context.Result(str(out))
        return out
    else:
        context.Result('not found')
        return None

###############################################################################
def CheckProgFgrep(context, grep, selection=_auto):
    """Corresponds to AC_PROG_FGREP_ autoconf macro

    :Parameters:
        context
            SCons configuration context.
        grep
            Path to ``grep`` program as found by `CheckProgGrep`.
        selection
            If `_auto` (default), the program will be found automatically,
            otherwise the method will return the value of **selection**.

    .. _AC_PROG_FGREP: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fFGREP-266
    """
    context.Display("Checking for fgrep... ")
    context.sconf.cached = 1
    action = _ProgGrep(grep, ['-F', 'ab*c'], 'ab*c\n', ['fgrep'], ['FGREP'],'FGREP')
    action = _ActionWrapper(action)
    args = pickle.dumps({'grep' : grep, 'selection' : selection})
    stat, out = context.TryAction(action, args, '.arg')
    if stat and out:
        out = pickle.loads(out)
        context.Result(str(out))
        return out
    else:
        context.Result('not found')
        return None

###############################################################################
def CheckProgGrep(context, selection=_auto, programs = None):
    """Corresponds to AC_PROG_GREP_ autoconf macro

    :Parameters:
        context
            SCons configuration context.
        selection
            If `_auto` (default), the program will be found automatically,
            otherwise the method will return the value of **selection**.
        programs
            List of program names to look for. If ``None`` (default), the
            default list ``[ 'grep', 'ggrep' ]`` will be used.

    Check for a fully functional grep program that handles the longest lines
    possibla and which respoects multiple -e options.

    .. _AC_PROG_GREP: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fGREP-258
    """
    context.Display("Checking for grep that handles long lines and -e... ")
    context.sconf.cached = 1
    args = ['-e', 'GREP$', '-e', '-(cannot match)-']
    if programs is None:
        programs = ['grep', 'ggrep']
    action = _ProgGrep(None, None, None, programs, args, 'GREP')
    action = _ActionWrapper(action)
    args = pickle.dumps({'selection' : selection })
    stat, out = context.TryAction(action, args, '.arg')
    if stat and out:
        out = pickle.loads(out)
        context.Result(str(out))
        return out
    else:
        context.Result('not found')
        return None


###############################################################################
def CheckProgInstall(context, selection=_auto, programs=None, reject_paths=None):
    """Corresponds to AC_PROG_INSTALL_ autoconf macro

    Find a good install program. We prefer a C program (faster), so one script
    is as good as another. But avoid the broken or incompatible versions:

        - SysV ``/etc/install``, ``/usr/sbin/install``
        - SunOS ``/usr/etc/install``
        - IRIX ``/sbin/install``
        - AIX ``/bin/install``
        - AmigaOS ``/C/install``, which installs bootblocks on floppy discs
        - AIX 4 ``/usr/bin/installbsd``, which doesn't work without a ``-g`` flag
        - AFS ``/usr/afsws/bin/install``, which mishandles nonexistent args
        - SVR4 ``/usr/ucb/install``, which tries to use the nonexistent group "staff"
        - OS/2's system ``install``, which has a completely different semantic
        - ``./install``, which can be erroneously created by make from ``./install.sh``.
        - Reject ``install`` programs that cannot install multiple files.

    :Parameters:
        context
            SCons configuration context.
        selection
            If `_auto` (default), the program will be found automatically,
            otherwise the method will return the value of **selection**.
        programs
            List of program names to look for. If ``None`` (default), the
            default list ``[ 'ginstall', 'scoinst', 'install' ]`` will be used.
        reject_paths
            List of paths to be rejected from search path. If ``None``, a
            default list will be used which excludes all the broken versions
            described above.

    .. _AC_PROG_INSTALL: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fINSTALL-270
    """
    context.Display("Checking for a BSD-compatible install... ")
    context.sconf.cached = 1
    action = _ActionWrapper(_ProgInstall(programs,reject_paths))
    args = pickle.dumps({ 'selection' : selection,
                          'programs' : programs,
                          'reject_paths' : reject_paths })
    stat, out = context.TryAction(action, args, '.arg')
    if stat and out:
        out = pickle.loads(out)
        context.Result(str(out))
        return out
    else:
        context.Result('not found')
        return None

###############################################################################
def CheckProgMkdirP(context, selection=_auto, programs=None):
    """Corresponds to AC_PROG_MKDIR_P_ autoconf macro

    Check whether ``mkdir -p`` is known to be thread-safe, and fall back to
    ``install-sh -d`` otherwise.

    We cannot accept any implementation of ``mkdir`` that recognizes ``-p``.
    Some implementations (such as Solaris 8's) are vulnerable to race
    conditions: if a parallel build tries to run ``mkdir -p a/b`` and
    ``mkdir -p a/c`` concurrently, both version can detect that ``a/`` is
    missing, but only one can create it and the other will error out.
    Consequently we restrict ourselves to known race-free implementations.

    Automake used to define ``mkdir_p`` as ``mkdir -p .``, in order to
    allow ``$(mkdir_p)`` to be used without argument. As in ``$(mkdir_p) $(somedir)``
    where ``$(somedir)`` is conditionally defined. However we don't do
    that for ``MKDIR_P``.

    On NextStep and OpenStep, the ``mkdir`` command does not recognize any
    option.  It will interpret all options as directories to create.

    :Parameters:
        context
            SCons configuration context.
        selection
            If `_auto` (default), the program will be found automatically,
            otherwise the method will return the value of **selection**.
        programs
            List of program names to look for. If ``None`` (default), the
            default list ``[ 'mkdir', 'gmkdir' ]`` will be used.

    .. _AC_PROG_MKDIR_P: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fMKDIR_005fP-277
    """
    context.Display("Checking for a thread-safe mkdir -p... ")
    context.sconf.cached = 1
    action = _ActionWrapper(_ProgMkdirP(programs))
    args = pickle.dumps({ 'selection' : selection, 'programs' : programs })
    stat, out = context.TryAction(action, args, '.arg')
    if stat and out:
        out = pickle.loads(out)
        context.Result(str(out))
        return out
    else:
        context.Result('not found')
        return None

###############################################################################
def CheckLexExe(context, selection=_auto, programs=None):
    """Check for lex executable

    :Parameters:
        selection
            List of program names to look for (in order). If None (default),
            the default list[ 'flex', 'lex' ]will be used,
        programs
            List of program names to look for (in order). If None (default),
            the default list ``[ 'flex', 'lex' ]`` will be used.
    """
    context.Display("Checking for flex... ")
    context.sconf.cached = 1
    action = _ActionWrapper(_LexExe(programs))
    args = pickle.dumps({ 'selection' : selection, 'programs'  : programs })
    stat, out = context.TryAction(action, args, '.arg')
    if not stat or not out:
        context.Result('not found')
        return None
    out = pickle.loads(out)
    context.Result(str(out))
    return out

###############################################################################
def CheckLexFileRoot(context, lex, selection=_auto, lexroots=None, script=None):
    """Determine the root of the file name produced by lex by default.

    :Parameters:
        lexroots
            List of known lex roots to choose from. If ``None`` (default) the
            default list ``[ 'lex.yy', 'lexyy' ]`` is used.
    """
    context.Display("Checking for lex output file root... ")
    context.sconf.cached = 1
    action = _ActionWrapper(_LexFileRoot(lex, lexroots, script))
    args = pickle.dumps({ 'lex'  : lex,
                          'selection' : selection,
                          'lexroots' : lexroots,
                          'script' : script })
    stat, out = context.TryAction(action, args, '.arg')
    if not stat or not out:
        context.Result('not found')
        return None
    out = pickle.loads(out)
    context.Result(str(out))
    return out

#################################################################################
def CheckLexOutput(context, lex, lexroot, script=None, silent=True):
    """TODO: write documentation"""
    if not silent:
        context.Display("Checking for lex output... ")
        context.sconf.cached = 1
    else:
        context.did_show_result = 1

    action = _ActionWrapper(_LexOutput(lex, lexroot, script))
    args = pickle.dumps({ 'lex' : lex,
                          'lexroot' : lexroot,
                          'script' : script })
    stat, out = context.TryAction(action, args, '.arg')
    if not stat or not out:
        if not silent:
            context.Result('failed')
        return None
    out = pickle.loads(out)

    if not silent:
        context.Result("done")
    return out

#################################################################################
def CheckLexLibs(context, text, selection=_auto, lexlibs=None):
    """Determine libraries required do link C programs generated by lex.

    TODO: write documentation
    """

    from SCons.SConf import _ac_build_counter

    context.Display("Checking for lex library... ")
    context.sconf.cached = 1

    if lexlibs is None:
        lexlibs = [ None, 'fl', 'l' ]

    out = None
    for lexlib in lexlibs:
        # note: we must perform all iterations to be "indempotent",
        #       the number of times TryLink is invoked should depend only on
        #       input arguments to function (the size of 'lexlibs' in fact) and
        #       nothing else.
        if lexlib is None:
            libs = CLVar()
        else:
            libs = CLVar(lexlib)
        env = context.sconf.env
        context.sconf.env = env.Clone()
        context.sconf.env['LIBS'] = libs
        try:
            if context.TryLink(text, '.c') and out is None:
                out = libs
                # Don't break here! even if you think you could actually...
                # See note at the beginning of the loop, instead.
        finally:
            context.sconf.env = env

    action = _ActionWrapper(_WriteTarget(out))
    args = pickle.dumps({ 'text' : text, 'selection' : selection, 'lexlibs' : lexlibs })
    stat, out = context.TryAction(action, args, '.arg')
    if not stat or not out:
        context.Result('failed')
        return None
    out = pickle.loads(out)
    if out is None:
        context.Result('failed')
        return None
    if len(out):
        context.Result(' '.join(['-l%s' % p for p in out]))
    else:
        context.Result('none needed')
    return out

###############################################################################
def CheckLexYytextPtr(context, text, lexlibs, selection=_auto):
    """TODO: write documentation"""
    from SCons.Conftest import _YesNoResult
    context.Display('Checking whether yytext is a pointer... ')
    context.sconf.cached = 1

    env = context.sconf.env
    context.sconf.env = env.Clone()
    context.sconf.env['LIBS'] = lexlibs
    text2 = '#define YYTEXT_POINTER 1\n' + text
    ret = 1
    try:
        if context.TryLink(text2, '.c'):
            ret = 0
    finally:
        context.sconf.env = env

    _YesNoResult(context, ret, 'YYTEXT_POINTER', text)
    context.did_show_result = 1
    return (not ret)

###############################################################################
def CheckProgLex(context, selection=_auto, programs=None, lexroots=None, lexlibs=None, script=None):
    """Corresponds to AC_PROG_LEX_ autoconf macro

    :Parameters:
        context
            SCons configuration context.
        selection
            If `_auto` (default), the program will be found automatically,
            otherwise the method will return the value of **selection**.
        programs
            List of program names to look for (in order). If None (default),
            the default list ``[ 'flex', 'lex' ]`` will be used
        lexroots
            When lex is invoked without ``-o`` option, it writes its output to
            default file named ``lex.yy.c`` or ``lexyy.c`` depending on
            implementation. In such case, the string ``lex.yy`` or ``lexyy`` is
            called the lex file root. The `CheckProgLex` method determines this
            root and returns it as ``lexroot``. The **lexroots** parameter
            lists possible choices to pickup from. If it is set to ``None`` the
            default list ``[ 'lex.yy.c', 'lexyy.c' ]`` is used.
        lexlibs
            The function tries to link a ``*.c`` file generated by lex against
            each of the libraries from **lexlibs** list. The first library, for
            which the compilation succeeds, is returned as ``lexlibs``.
    :Return:
        lex
            Name of the lex program detected.
        lexroot
            Root part of the ``*.c`` file name generated by lex when invoked
            without ``-o`` option.
        lexlibs
            List of libraries needed to compile and link a program generated
            with ``lex``.
        yytextptr
             True if ``yytext`` is defined as pointer. Lex can declare
             ``yytext`` either as a pointer or an array. The default is
             implementation-dependent. This return value allows to figure out
             which it is, since not all implementations provide ``%pointer``
             and ``%array`` declarations. 


    .. _AC_PROG_LEX: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fLEX-281
    """
    context.did_show_result = 1
    sconf = context.sconf
    lex = sconf.CheckLexExe(selection, programs)
    lexroot = sconf.CheckLexFileRoot(lex, _auto, lexroots, script)
    text = sconf.CheckLexOutput(lex, lexroot, script)
    lexlibs = sconf.CheckLexLibs(text, _auto, lexlibs)
    yytextptr = sconf.CheckLexYytextPtr(text, lexlibs)
    return lex, lexroot, lexlibs, yytextptr


###############################################################################
def CheckProgLnS(context, selection=_auto):
    """Corresponds to AC_PROG_LN_S_ autoconf macro

    :Parameters:
        context
            SCons configuration context.
        selection
            If `_auto` (default), the program will be found automatically,
            otherwise the method will return the value of **selection**.
        
    .. _AC_PROG_LN_S: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fLN_005fS-288
    """
    context.Display("Checking whether ln -s works... ")
    context.sconf.cached = 1
    action = _ActionWrapper(_ProgLnS())
    args = pickle.dumps({ 'selection' : selection })
    stat, out = context.TryAction(action, args, '.arg')
    if not out:
        context.Result('failure')
        return None
    out = pickle.loads(out)
    if out == ['ln', '-s']:
        context.Result('yes')
    else:
        context.Result('no, using %s' % str(out))
    return out

###############################################################################
def CheckProgRanlib(context, selection=_auto):
    """Corresponds to AC_PROG_RANLIB_ autoconf macro

    :Parameters:
        context
            SCons configuration context.
        selection
            If `_auto` (default), the program will be found automatically,
            otherwise the method will return the value of **selection**.

    .. _AC_PROG_RANLIB: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fRANLIB-291
    """
    raise NotImplementedError("not implemented")

###############################################################################
def CheckProgSed(context, selection=_auto, programs=None):
    """Corresponds to AC_PROG_SED_ autoconf macro

    :Parameters:
        context
            SCons configuration context.
        selection
            If `_auto` (default), the program will be found automatically,
            otherwise the method will return the value of **selection**.
        programs
            List of program names to look for. If ``None`` (default), the
            default list ``[ 'sed', 'gsed' ]`` will be used.

    .. _AC_PROG_SED: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fSED-294
    """
    context.Display("Checking for a sed that does not truncate output... ")
    context.sconf.cached = 1
    action = _ActionWrapper(_ProgSed(programs))
    args = pickle.dumps({ 'selection' : selection, 'programs' : programs})
    stat, out = context.TryAction(action, args, '.arg')
    if stat and out:
        out = pickle.loads(out)
        context.Result(str(out))
        return out
    else:
        context.Result('not found')
        return None

###############################################################################
def CheckProgYacc(context, selection=_auto, programs=None):
    """Corresponds to AC_PROG_YACC_ autoconf macro

    :Parameters:
        context
            SCons configuration context.
        selection
            If `_auto` (default), the program will be found automatically,
            otherwise the method will return the value of **selection**.

    .. _AC_PROG_YACC: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fYACC-298
    """
    context.did_show_result = 1
    if programs is None:
        programs = ['bison -y', 'byacc']
    prog = context.sconf.CheckProgs(programs, selection, value_if_not_found = 'yacc')
    if prog:
        prog = CLVar(prog)
    return prog

###############################################################################
def Tests():
    """Get the program checks as a dictionary.
    """
    return { 'CheckProg': CheckProg
           , 'CheckProgs': CheckProgs
           , 'CheckTargetTool': CheckTargetTool
           , 'CheckTool': CheckTool
           , 'CheckTargetTools': CheckTargetTools
           , 'CheckTools': CheckTools
           , 'CheckPathProg': CheckPathProg
           , 'CheckPathProgs': CheckPathProgs
           , 'CheckPathTargetTool': CheckPathTargetTool
           , 'CheckPathTool': CheckPathTool
           , 'CheckProgAwk': CheckProgAwk
           , 'CheckProgEgrep': CheckProgEgrep
           , 'CheckProgFgrep': CheckProgFgrep
           , 'CheckProgGrep': CheckProgGrep
           , 'CheckProgInstall': CheckProgInstall
           , 'CheckProgMkdirP': CheckProgMkdirP
           , 'CheckProgLex': CheckProgLex
           , 'CheckLexExe': CheckLexExe
           , 'CheckLexFileRoot': CheckLexFileRoot
           , 'CheckLexOutput': CheckLexOutput
           , 'CheckLexLibs': CheckLexLibs
           , 'CheckLexYytextPtr' : CheckLexYytextPtr
           , 'CheckProgLnS': CheckProgLnS
           , 'CheckProgRanlib': CheckProgRanlib
           , 'CheckProgSed': CheckProgSed
           , 'CheckProgYacc': CheckProgYacc }



# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=scons expandtab tabstop=4 shiftwidth=4:
