"""`SConsGnuBuild.GProg`

`Particular Programs`_. Check whether they exist, and in some cases whether
they support certain features.

**General Description**

This module provides standard `autoconf output variables`_  which define paths
to `Particular Programs`_. Each variable may be accessed via:

    - SCons environment, as construction variables (``env.subst('$variable')``),
    - SCons command line variables (``scons variable=value``),

Supported variables:
====================

    AWK
        TODO: write short description
    EGREP
        TODO: write short description
    FGREP
        TODO: write short description
    GREP
        TODO: write short description
    INSTALL
        TODO: write short description
    INSTALL_DATA
        TODO: write short description
    INSTALL_PROGRAM
        TODO: write short description
    INSTALL_SCRIPT
        TODO: write short description
    LEX
        TODO: write short description
    LEX_OUTPUT_ROOT
        TODO: write short description
    LEXLIB
        TODO: write short description
    LN_S
        TODO: write short description
    MKDIR_P
        TODO: write short description
    RANLIB
        TODO: write short description
    SED
        TODO: write short description
    YACC
        TODO: write short description

.. _autoconf output variables: http://www.gnu.org/software/autoconf/manual/autoconf.html#Output-Variable-Index
.. _Particular Programs: http://www.gnu.org/software/autoconf/manual/autoconf.html#Particular-Programs
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

from os import path
from SConsGnuBuild import Defaults

#############################################################################
# NOTE: variable substitutions must be in curly brackets, so use ${prefix}
#       and not $prefix. This is required for proper prefixing/suffixing and
#       transforming in certain parts of library
__std_var_triples = [
    ( 'AWK',
      'TODO: write help',
      'TODO: provide default value' ),
    ( 'EGREP',
      'TODO: write help',
      'TODO: provide default value' ),
    ( 'FGREP',
      'TODO: write help',
      'TODO: provide default value' ),
    ( 'GREP',
      'TODO: write help',
      'TODO: provide default value' ),
    ( 'INSTALL',
      'TODO: write help',
      'TODO: provide default value' ),
    ( 'INSTALL_DATA',
      'TODO: write help',
      'TODO: provide default value' ),
    ( 'INSTALL_PROGRAM',
      'TODO: write help',
      'TODO: provide default value' ),
    ( 'INSTALL_SCRIPT',
      'TODO: write help',
      'TODO: provide default value' ),
    ( 'LEX',
      'TODO: write help',
      'TODO: provide default value' ),
    ( 'LEX_OUTPUT_ROOT',
      'TODO: write help',
      'TODO: provide default value' ),
    ( 'LEXLIB',
      'TODO: write help',
      'TODO: provide default value' ),
    ( 'LN_S',
      'TODO: write help',
      'TODO: provide default value' ),
    ( 'MKDIR_P',
      'TODO: write help',
      'TODO: provide default value' ),
    ( 'RANLIB',
      'TODO: write help',
      'TODO: provide default value' ),
    ( 'SED',
      'TODO: write help',
      'TODO: provide default value' ),
    ( 'YACC',
      'TODO: write help',
      'TODO: provide default value' ),
]

default_env_key_prefix      = Defaults.gvar_env_key_prefix
default_env_key_suffix      = Defaults.gvar_env_key_suffix
default_env_key_transform   = Defaults.gvar_env_key_transform

default_var_key_prefix      = Defaults.gvar_var_key_prefix
default_var_key_suffix      = Defaults.gvar_var_key_suffix
default_var_key_transform   = Defaults.gvar_var_key_transform

default_opt_key_prefix      = Defaults.gvar_opt_key_prefix
default_opt_key_suffix      = Defaults.gvar_opt_key_suffix
default_opt_key_transform   = Defaults.gvar_opt_key_transform


#############################################################################
def __init_module_vars():
    # TODO: anything to be done here?
    pass
__init_module_vars()

#############################################################################
def __map_std_var_triples(callback, name_filter = lambda x : True):
    """Map all predefined GNU variable triples (name, desc, default) via
    `callback`.

    :Parameters:
        callback : callable
            function of type ``callback(name, desc, default)``, where

                - ``name:`` is the name of variable being processed,
                - ``desc:`` is short description,
                - ``default:`` is the default value for the variable.
        name_filter : callable
            callable object (e.g. lambda) of type ``name_filter(name) ->
            boolean`` used to filter-out unwanted variables; only these
            variables are processed, for which name_filter returns ``True``

    :Returns:
        returns result of mapping through `callback`
    """
    triples = filter(lambda t : name_filter(t[0]), __std_var_triples)
    return map(lambda x : callback(*x), triples)

#############################################################################
def gvar_names(name_filter = lambda x : True):
    """Return list of standard GNU directory variable names

    By default this function returns empty list, you should provide custom
    **name_filter** to get any results. To retrieve all defined variables,
    use ``name_filter = lambda x : True``.

    :Parameters:
        name_filter : callable
            callable object (e.g. lambda) of type ``name_filter(name) ->
            boolean`` used to filter-out unwanted variables; only these
            variables are processed, for which name_filter returns ``True``
    :Returns:
        the list of standard GNU directory variable names
    """
    return filter(name_filter, zip(*__std_var_triples)[0])

#############################################################################
def declare_gvars(name_filter=lambda x : False,
                  env_key_transform=default_env_key_transform,
                  var_key_transform=default_var_key_transform):
    from SCons.Variables.PathVariable import PathVariable
    from SConsGnuBuild.GVars import GVarDeclsU
    def _callback(name, desc, default):
        decl = { 'env_key'  : env_key_transform(name),
                 'var_key'  : var_key_transform(name),
                 'default'  : default,
                 'help'     : desc,
                 'type'     : 'string',
                 'nargs'    : 1,
                 'metavar'  : 'PATH' }
        return name, decl

    return GVarDeclsU(__map_std_var_triples(_callback, name_filter))

##############################################################################
def GVarNames(**kw):
    """Return the names of supported GNU dir variables

    :Keywords:
        name_filter : callable
            callable object (e.g. lambda) of type ``name_filter(name) ->
            boolean`` used to filter-out unwanted variables; only these
            variables are processed, for which name_filter returns ``True``
    """
    args = ['name_filter']
    kw2 = { key : kw[key] for key in args if key in kw }
    return gvar_names(**kw2)

###############################################################################
def DeclareGVars(**kw):
    """Return the standard GNU directory variables as
    ``GVar`` variable declarations `_GVarDecls` (see `SConsGnuBuild.GVars`).

    :Keywords:
        name_filter : callable
            callable object (e.g. lambda) of type ``name_filter(name) ->
            boolean`` used to filter-out unwanted variables; only these
            variables are processed, for which name_filter returns ``True``
        env_key_transform : callable
            function or lambda used to transform canonical ``GVar`` names to
            keys used for corresponding construction variables in a SCons
            environment (default: `default_env_key_transform`)
        var_key_transform : callable
            function of lambda used to trasform canonical ``GVar`` names to
            keys used for corresponding SCons command-line variables
            ``variable=value`` (default: `default_var_key_transform`)
    :Returns:
        a dictionary-like object of type `SConsGnuBuild.GVar._GVarDecls`
    """
    args = ['name_filter', 'env_key_transform', 'var_key_transform']
    kw2 = { key : kw[key] for key in args if key in kw }
    return declare_gvars(**kw2)

###############################################################################
def _CheckProg(context, prog, value_if_found=None, value_if_not_found=None,
               path=None, pathext=None, reject=[]):
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

    .. _AC_CHECK_PROG: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fCHECK_005fPROG-304
    """

    if value_if_found is None:
        value_if_found = prog

    context.Display("Checking for program %s... " % prog)
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
                reject=[]):
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

    .. _AC_CHECK_PROGS: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fCHECK_005fPROGS-307
    """

    if len(progs) > 1:
        s = ' or '.join([', '.join(progs[:-1]), progs[-1]])
        context.Display("Checking for programs %s... " % s)
    elif len(progs) == 1:
        context.Display("Checking for program %s... " % progs[0])

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
                   pathext=None, reject=[]):
    """Corresponds to AC_PATH_PROG_ autoconf macro.

    .. _AC_PATH_PROG: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPATH_005fPROG-318
    """
    context.Display("Checking for program %s... " % prog)
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
                    pathext=None, reject=[]):
    """Corresponds to AC_PATH_PROGS_ autoconf macro.

    .. _AC_PATH_PROGS: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPATH_005fPROGS-321
    """

    if len(progs) > 1:
        s = ' or '.join([', '.join(progs[:-1]), progs[-1]])
        context.Display("Checking for programs %s... " % s)
    elif len(progs) == 1:
        context.Display("Checking for program %s... " % progs[0])

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
    return CheckProgs(['gawk', 'mawk', 'nawk', 'awk'], *args, **kw)

###############################################################################
def _CheckProgGrep(context,*args,**kw):
    """Corresponds to AC_PROG_GREP_ autoconf macro

    .. _AC_PROG_GREP: http://www.gnu.org/software/autoconf/manual/autoconf.html#index-AC_005fPROG_005fGREP-258
    """
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
