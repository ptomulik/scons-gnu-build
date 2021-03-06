"""`SConsGnu.CcVars`

Defines GVar variables related to C and C++ compilers.

**General Description**

Supported Variables:
====================

Programs:

    CC
        A C compiler to use
    CXX
        A C++ compiler to use
    LINK
        A linker to use
    SHCC
        A C compiler used when compiling shared libraries.
    SHCXX
        A C++ compiler used when compiling shared libraries.
    SHLINK
        A linker to use when creating shared libraries

Flags for programs:

    CFLAGS
        Flags for C compiler
    CXXFLAGS
        Flags for C++ compiler
    CCFLAGS
        Flags for both C and C++ compilers
    LINKFLAGS
        Flags for linker
    SHCFLAGS
        Flags for C compiler used when compiling shared libraries
    SHCXXFLAGS
        Flags for C++ compiler used when compiling shared libraries
    SHCCFLAGS',
        Flags for both C and C++ compilers used when compiling shared libraries
    SHLINKFLAGS',
        Flags for linker used when creating shared libraries
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

from SConsGnu import Defaults
from SCons.Util import is_Sequence, CLVar

#############################################################################
# NOTE: variable substitutions must be in curly brackets, so use ${prefix}
#       and not $prefix. This is required for proper prefixing/suffixing and
#       transforming in certain parts of library
__prog_var_tuples = [
    # Programs
    ( 'CC',     'A C compiler to use'),
    ( 'CXX',    'A C++ compiler to use'),
    ( 'LINK',   'A linker to use'),
    ( 'SHCC',   'A C compiler used when compiling shared libraries'),
    ( 'SHCXX',  'A C++ compiler used when compiling shared libraries'),
    ( 'SHLINK', 'A linker to use when creating shared libraries'),
]

__flag_var_tuples = [
    # Program flags
    ( 'CFLAGS',     'Flags for C compiler'),
    ( 'CXXFLAGS',   'Flags for C++ compiler'),
    ( 'CCFLAGS',    'Flags for both C and C++ compilers'),
    ( 'LINKFLAGS',  'Flags for linker'),
    ( 'SHCFLAGS',   'Flags for C compiler used when compiling shared libraries'),
    ( 'SHCXXFLAGS', 'Flags for C++ compiler used when compiling shared libraries'),
    ( 'SHCCFLAGS',  'Flags for both C and C++ compilers used when compiling shared libraries'),
    ( 'SHLINKFLAGS','Flags for linker used when creating shared libraries'),
]

default_env_key_prefix      = Defaults.gvar_env_key_prefix
default_env_key_suffix      = Defaults.gvar_env_key_suffix
default_env_key_transform   = Defaults.gvar_env_key_transform

default_var_key_prefix      = Defaults.gvar_var_key_prefix
default_var_key_suffix      = Defaults.gvar_var_key_suffix
default_var_key_transform   = Defaults.gvar_var_key_transform

#############################################################################
def __init_module_vars():
    # TODO: anything to be done here?
    pass
__init_module_vars()

#############################################################################
def _flag_converter(val, env=None):
    if isinstance(val, CLVar):
        return val
    else:
        return CLVar(val)

#############################################################################
def __map_prog_var_tuples(callback, name_filter = lambda x : True):
    """Map all predefined GNU variable tuples (name, desc, default) via
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
    tuples = filter(lambda t : name_filter(t[0]), __prog_var_tuples)
    return map(lambda x : callback(*x), tuples)

#############################################################################
def __map_flag_var_tuples(callback, name_filter = lambda x : True):
    """Map all predefined GNU variable tuples (name, desc, default) via
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
    tuples = filter(lambda t : name_filter(t[0]), __flag_var_tuples)
    return map(lambda x : callback(*x), tuples)

#############################################################################
def gvar_names(name_filter = lambda x : True, categories = None):
    """Return list of GVar names

    :Parameters:
        name_filter : callable
            callable object (e.g. lambda) of type ``name_filter(name) ->
            boolean`` used to filter-out unwanted variables; only these
            variables are processed, for which name_filter returns ``True``
        categories : string
            return only variable names for given categories, it may be
            ``'programs'`` for variables representing programs (``CC``, ``CXX``
            and such), ``'flags'`` for variables representing program flags
            (``CFLAGS``, ``CCFLAGS`` etc.) or ``None`` (default) to not filter
            by categories.
    :Returns:
        the list of standard GNU directory variable names
    """
    if is_Sequence(name_filter):
        seq = name_filter
        name_filter = lambda x : x in seq
    if categories and not is_Sequence(categories):
        categories = [ categories ]
    if categories:
        lst = []
        if 'programs' in categories:
            lst.extend(__prog_var_tuples)
        if 'flags' in categories:
            lst.extend(__flag_var_tuples)
    else:
        lst = __prog_var_tuples + __flag_var_tuples
    return filter(name_filter, zip(*lst)[0])

#############################################################################
def declare_gvars(defaults = {}, name_filter=lambda x : True,
                  env_key_transform=default_env_key_transform,
                  var_key_transform=default_var_key_transform):
    """Return the variables representing particular programs as
    ``GVar`` variable declarations `_GVarDecls` (see `SConsGnu.GVars`).

    :Parameters:
        defaults : dict
            User-specified default values for the GVars being declared. You'll
            usually put your SCons Environment object env here.
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
        a dictionary-like object of type `SConsGnu.GVar._GVarDecls`
    """
    from SCons.Variables.PathVariable import PathVariable
    from SConsGnu.GVars import GVarDeclsU, _undef
    def _prog_callback(name, desc, default = _undef):
        try:
            default = defaults[name]
        except KeyError:
            pass
        decl = { 'env_key'  : env_key_transform(name),
                 'var_key'  : var_key_transform(name),
                 'default'  : default,
                 'help'     : desc }
        return name, decl
    def _flag_callback(name, desc, default = _undef):
        try:
            default = defaults[name]
        except KeyError:
            pass
        decl = { 'env_key'  : env_key_transform(name),
                 'var_key'  : var_key_transform(name),
                 'default'  : default,
                 'converter': _flag_converter,
                 'help'     : desc }
        return name, decl

    if is_Sequence(name_filter):
        seq = name_filter
        name_filter = lambda x : x in seq
    return GVarDeclsU( __map_prog_var_tuples(_prog_callback, name_filter)
                     + __map_flag_var_tuples(_flag_callback, name_filter) )

##############################################################################
def GVarNames(**kw):
    """Return the names of supported particuler program variables

    :Keywords:
        name_filter : callable
            callable object (e.g. lambda) of type ``name_filter(name) ->
            boolean`` used to filter-out unwanted variables; only these
            variables are processed, for which name_filter returns ``True``
    """
    args = ['name_filter', 'categories']
    kw2 = { key : kw[key] for key in args if key in kw }
    return gvar_names(**kw2)

###############################################################################
def DeclareGVars(**kw):
    """Return the variables representing particular programs as
    ``GVar`` variable declarations `_GVarDecls` (see `SConsGnu.GVars`).

    :Keywords:
        defaults : dict
            User-specified default values for the GVars being declared. You'll
            usually put your SCons Environment object env here.
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
        a dictionary-like object of type `SConsGnu.GVar._GVarDecls`
    """
    args = ['defaults', 'name_filter', 'env_key_transform', 'var_key_transform']
    kw2 = { key : kw[key] for key in args if key in kw }
    return declare_gvars(**kw2)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
