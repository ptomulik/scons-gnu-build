"""`SConsGnuBuild.GProgVars`

Variables for `Alternative Programs`_.

**General Description**

This module provides standard `autoconf output variables`_  which define paths
to `Alternative Programs`_. Each variable may be accessed via:

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

from os import path
from SConsGnuBuild import Defaults

#############################################################################
# NOTE: variable substitutions must be in curly brackets, so use ${prefix}
#       and not $prefix. This is required for proper prefixing/suffixing and
#       transforming in certain parts of library
__std_var_triples = [
    ( 'AWK',
      'TODO: write help',
      None ),
    ( 'EGREP',
      'TODO: write help',
      None ),
    ( 'FGREP',
      'TODO: write help',
      None ),
    ( 'GREP',
      'TODO: write help',
      None ),
    ( 'INSTALL',
      'TODO: write help',
      None ),
    ( 'INSTALL_DATA',
      'TODO: write help',
      None ),
    ( 'INSTALL_PROGRAM',
      'TODO: write help',
      None ),
    ( 'INSTALL_SCRIPT',
      'TODO: write help',
      None ),
    ( 'LEX',
      'TODO: write help',
      None ),
    ( 'LEX_OUTPUT_ROOT',
      'TODO: write help',
      None ),
    ( 'LEXLIB',
      'TODO: write help',
      None ),
    ( 'LN_S',
      'TODO: write help',
      None ),
    ( 'MKDIR_P',
      'TODO: write help',
      None ),
    ( 'RANLIB',
      'TODO: write help',
      None ),
    ( 'SED',
      'TODO: write help',
      None ),
    ( 'YACC',
      'TODO: write help',
      None ),
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
