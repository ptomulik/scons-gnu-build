"""`SConsGnuBuild.GProgChecks`

`Alternative Programs`_. Check whether they exist, and in some cases whether
they support certain features.

.. _autoconf output variables: http://www.gnu.org/software/autoconf/manual/autoconf.html#Output-Variable-Index
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
def _CheckProg(context, prog, value_if_found=None, value_if_not_found=None,
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
def _CheckProgs(context, progs, value_if_not_found=None, path=None, pathext=None,
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
def _CheckTargetTool(context, prog, value_if_not_found=None,
                     path=None, pathext=None, reject=[]):
    """Corresponds to AC_CHECK_TARGET_TOOL_ autoconf macro.
    
    .. _AC_CHECK_TARGET_TOOL: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fCHECK_005fTARGET_005fTOOL-310
    """
    # TODO: first I need to know how to determine AC_CANONICAL_TARGET
    raise NotImplementedError("not implemented")

###############################################################################
def _CheckTool(context, prog, value_if_not_found=None,
               path=None, pathext=None, reject=[]):
    """Corresponds to AC_CHECK_TOOL_ autoconf macro.

    .. _AC_CHECK_TOOL: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fCHECK_005fTOOL-312
    """
    # TODO: first I need to know how to determine AC_CANONICAL_HOST
    raise NotImplementedError("not implemented")

###############################################################################
def _CheckTargetTools(context, progs, value_if_not_found=None,
                      path=None, pathext=None, reject=[]):
    """Corresponds to AC_CHECK_TARGET_TOOLS_ autoconf macro.

    .. _AC_CHECK_TARGET_TOOLS: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fCHECK_005fTARGET_005fTOOLS-314
    """
    # TODO: first I need to know how to determine AC_CANONICAL_TARGET
    raise NotImplementedError("not implemented")

###############################################################################
def _CheckTools(context, progs, value_if_not_found=None,
                path=None, pathext=None, reject=[]):
    """Corresponds to AC_CHECK_TOOLS_ autoconf macro.

    .. _AC_CHECK_TOOLS: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fCHECK_005fTOOLS-316
    """
    # TODO: first I need to know how to determine AC_CANONICAL_HOST
    raise NotImplementedError("not implemented")

###############################################################################
def _CheckPathProg(context, prog, value_if_not_found=None, path=None,
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
def _CheckPathProgs(context, progs, value_if_not_found=None, path=None,
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
def _CheckPathTargetTool(context, prog, value_if_not_found=None,
                         path=None, pathext=None, reject=[]):
    """Corresponds to AC_PATH_TARGET_TOOL_ autoconf macro.

    .. _AC_PATH_TARGET_TOOL: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPATH_005fTARGET_005fTOOL-329
    """
    # TODO: first I need to know how to determine AC_CANONICAL_TARGET
    raise NotImplementedError("not implemented")

###############################################################################
def _CheckPathTool(context, prog, value_if_not_found=None,
                   path=None, pathext=None, reject=[]):
    """Corresponds to AC_PATH_TOOL_ autoconf macro.

    .. _AC_PATH_TOOL: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPATH_005fTOOL-331
    """
    # TODO: first I need to know how to determine AC_CANONICAL_HOST
    raise NotImplementedError("not implemented")


###############################################################################
def _CheckProgAwk(context,*args,**kw):
    """Corresponds to AC_PROG_AWK_ autoconf macro

    .. _AC_PROG_AWK: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fAWK-254
    """
    kw['prog_str'] = 'awk'
    return _CheckProgs(context,['gawk', 'mawk', 'nawk', 'awk'], *args, **kw)

###############################################################################
def _CheckProgGrep(context,*args,**kw):
    """Corresponds to AC_PROG_GREP_ autoconf macro

    .. _AC_PROG_GREP: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fGREP-258
    """
    context.Display("Checking for grep that handles long lines and -e... " % prog_str)
    raise NotImplementedError("not implemented")

###############################################################################
def _CheckProgEgrep(context,*args,**kw):
    """Corresponds to AC_PROG_EGREP_ autoconf macro

    .. _AC_PROG_EGREP: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fEGREP-262
    """
    raise NotImplementedError("not implemented")

###############################################################################
def _CheckProgFgrep(context,*args,**kw):
    """Corresponds to AC_PROG_FGREP_ autoconf macro

    .. _AC_PROG_FGREP: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fFGREP-266
    """
    raise NotImplementedError("not implemented")

###############################################################################
def _CheckProgInstall(context,*args,**kw):
    """Corresponds to AC_PROG_INSTALL_ autoconf macro

    .. _AC_PROG_INSTALL: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fINSTALL-270
    """
    raise NotImplementedError("not implemented")

###############################################################################
def _CheckProgMkdirP(context,*args,**kw):
    """Corresponds to AC_PROG_MKDIR_P_ autoconf macro

    .. _AC_PROG_MKDIR_P: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fMKDIR_005fP-277
    """
    raise NotImplementedError("not implemented")

###############################################################################
def _CheckProgLex(context,*args,**kw):
    """Corresponds to AC_PROG_LEX_ autoconf macro

    .. _AC_PROG_LEX: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fLEX-281
    """
    raise NotImplementedError("not implemented")

###############################################################################
def _CheckProgLnS(context,*args,**kw):
    """Corresponds to AC_PROG_LN_S_ autoconf macro

    .. _AC_PROG_LN_S: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fLN_005fS-288
    """
    raise NotImplementedError("not implemented")

###############################################################################
def _CheckProgRanlib(context,*args,**kw):
    """Corresponds to AC_PROG_RANLIB_ autoconf macro

    .. _AC_PROG_RANLIB: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fRANLIB-291
    """
    raise NotImplementedError("not implemented")

###############################################################################
def _CheckProgSed(context,*args,**kw):
    """Corresponds to AC_PROG_SED_ autoconf macro

    .. _AC_PROG_SED: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fSED-294
    """
    raise NotImplementedError("not implemented")

###############################################################################
def _CheckProgYacc(context,*args,**kw):
    """Corresponds to AC_PROG_YACC_ autoconf macro

    .. _AC_PROG_YACC: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fYACC-298
    """
    raise NotImplementedError("not implemented")

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
