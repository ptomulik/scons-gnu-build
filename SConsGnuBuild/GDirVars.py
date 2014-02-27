"""`SConsGnuBuild.GDirVars`

Provides GNU directory variables.

**General Description**

This module provides standard `GNU directory variables`_ defined by `GNU
Coding Standards`_, for example ``$prefix``, ``$bindir`` or ``$sysconfdir``.
The variables defined here may be easilly added to:

    - SCons environment, as construction variables (``env.subst('$variable')``),
    - SCons command line variables (``scons variable=value``),
    - SCons command line options (``scons --variable=value``).


Supported variables:
====================

  prefix
      Installation prefix
  exec_prefix
      Installation prefix for executable files
  bindir
      The directory for installing executable programs that users can run.
  sbindir
      The directory for installing executable programs that can be run from the
      shell, but are only generally useful to system administrators.
  libexecdir
      The directory for installing executable programs to be run by other
      programs rather than by users.
  datarootdir
      The root of the directory tree for read-only architecture-independent
      data files.
  datadir
      The directory for installing idiosyncratic read-only
      architecture-independent data files for this program.
  sysconfdir
      The directory for installing read-only data files that pertain to a single
      machine - that is to say, files for configuring a host.
  sharedstatedir
      The directory for installing architecture-independent data files which
      the programs modify while they run.
  localstatedir
      The directory for installing data files which the programs modify while
      they run, and that pertain to one specific machine.
  includedir
      The directory for installing header files to be included by user programs
      with the C ``#include`` preprocessor directive.
  oldincludedir
      The directory for installing ``#include`` header files for use with compilers
      other than GCC.
  docdir
      The directory for installing documentation files (other than Info) for this
      package.
  infodir
      The directory for installing the Info files for this package.
  htmldir
      Directory for installing documentation files in the html format.
  dvidir
      Directory for installing documentation files in the dvi format.
  pdfdir
      Directory for installing documentation files in the pdf format.
  psdir
      Directory for installing documentation files in the ps format.
  libdir
      The directory for object files and libraries of object code.
  lispdir
      The directory for installing any Emacs Lisp files in this package.
  localedir
      The directory for installing locale-specific message catalogs for this
      package.
  mandir
      The top-level directory for installing the man pages (if any) for this
      package.
  man1dir .. man8dir
      Simmilar to mandir
  man1ext .. man8ext
      Extensions for manpage files.
  pkgdatadir
      The directory for installing idiosyncratic read-only
      architecture-independent data files for this program.
  pkgincludedir
      The directory for installing header files to be included by user programs
      with the C ``#include`` preprocessor directive.
  pkglibdir
      The directory for object files and libraries of object code.
  pkglibexecdir
      The directory for installing executable programs to be run by other
      programs rather than by users.

.. _GNU directory variables: http://www.gnu.org/prep/standards/html_node/Directory-Variables.html
.. _GNU Coding Standards: http://www.gnu.org/prep/standards/html_node/
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

#############################################################################
# NOTE: variable substitutions must be in curly brackets, so use ${prefix}
#       and not $prefix. This is required for proper prefixing/suffixing and
#       transforming in certain parts of library
__std_var_triples = [
  ( 'prefix',
    'Installation prefix',
    '/usr/local' ),
  ( 'exec_prefix',
    'Installation prefix for executable files',
    '${prefix}' ),
  ( 'bindir',
    'The directory for installing executable programs that users can run.',
    '${exec_prefix}/bin' ),
  ( 'sbindir',
    'The directory for installing executable programs that can be run from the'
  + ' shell, but are only generally useful to system administrators.',
    '${exec_prefix}/sbin' ),
  ( 'libexecdir',
    'The directory for installing executable programs to be run by other'
  + ' programs rather than by users.',
    '${exec_prefix}/libexec' ),
  ( 'datarootdir',
    'The root of the directory tree for read-only architecture-independent'
  + ' data files.',
    '${prefix}/share' ),
  ( 'datadir',
    'The directory for installing idiosyncratic read-only'
  + ' architecture-independent data files for this program.',
    '${datarootdir}' ),
  ( 'sysconfdir',
    'The directory for installing read-only data files that pertain to a single'
  + ' machine - that is to say, files for configuring a host.',
    '${prefix}/etc' ),
  ( 'sharedstatedir',
    'The directory for installing architecture-independent data files which'
  + ' the programs modify while they run.',
    '${prefix}/com' ),
  ( 'localstatedir',
    'The directory for installing data files which the programs modify while'
  + 'they run, and that pertain to one specific machine.',
    '${prefix}/var' ),
  ( 'includedir',
    'The directory for installing header files to be included by user programs'
  + ' with the C "#include" preprocessor directive.',
    '${prefix}/include' ),
  ( 'oldincludedir',
    'The directory for installing "#include" header files for use with compilers'
  + ' other than GCC.',
    '/usr/include' ),
  ( 'docdir',
    'The directory for installing documentation files (other than Info) for this'
  + ' package.',
    '${datarootdir}/doc/${install_package}' ),
  ( 'infodir',
    'The directory for installing the Info files for this package.',
    '${datarootdir}/info' ),
  ( 'htmldir',
    'Directory for installing documentation files in the html format.',
    '${docdir}' ),
  ( 'dvidir',
    'Directory for installing documentation files in the dvi format.',
    '${docdir}' ),
  ( 'pdfdir',
    'Directory for installing documentation files in the pdf format.',
    '${docdir}' ),
  ( 'psdir',
    'Directory for installing documentation files in the ps format.',
    '${docdir}' ),
  ( 'libdir',
    'The directory for object files and libraries of object code.',
    '${exec_prefix}/lib' ),
  ( 'lispdir',
    'The directory for installing any Emacs Lisp files in this package.',
    '${datarootdir}/emacs/site-lisp' ),
  ( 'localedir',
    'The directory for installing locale-specific message catalogs for this'
  + ' package.',
    '${datarootdir}/locale' ),
  ( 'mandir',
    'The top-level directory for installing the man pages (if any) for this'
  + ' package.',
    '${datarootdir}/man' ),
  ( 'pkgdatadir',
    'The directory for installing idiosyncratic read-only'
  + ' architecture-independent data files for this program.',
    '${datadir}/${package}' ),
  ( 'pkgincludedir',
    'The directory for installing header files to be included by user programs'
  + ' with the C "#include" preprocessor directive.',
    '${includedir}/${package}' ),
  ( 'pkglibdir',
    'The directory for object files and libraries of object code.',
    '${libdir}/${package}' ),
  ( 'pkglibexecdir',
    'The directory for installing executable programs to be run by other'
  + ' programs rather than by users.',
    '${libexecdir}/${package}' )
]

default_env_key_prefix = 'GNUBLD_'
default_env_key_suffix = ''
default_env_key_transform = lambda x : default_env_key_prefix \
                          + x.upper() \
                          + default_env_key_suffix
default_var_key_prefix = ''
default_var_key_suffix = ''
default_var_key_transform = lambda x : default_var_key_prefix \
                            + x.upper() \
                            + default_var_key_suffix
default_opt_key_prefix = 'gnubld_'
default_opt_key_suffix = ''
default_opt_key_transform = lambda x : default_opt_key_prefix \
                            + x.lower() \
                            + default_opt_key_suffix
default_opt_prefix = '--'
default_opt_name_prefix = ''
default_opt_name_suffix= ''
default_opt_name_transform = lambda x : default_opt_prefix \
                            + (default_opt_name_prefix \
                            + x.lower() \
                            + default_opt_name_suffix).replace('_','-')


#############################################################################
def __init_module_vars():
    from SConsGnuBuild.Common import standard_man_sections
    for sec in standard_man_sections():
        __std_var_triples.append( ('man%sdir' % sec, '', '${prefix}/man/man%s' %sec) )
        __std_var_triples.append( ('man%sext' % sec, '', '.%s' %sec) )
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
def declare_gvars(name_filter=lambda x : True,
                  env_key_transform=default_env_key_transform,
                  var_key_transform=default_var_key_transform,
                  opt_key_transform=default_opt_key_transform,
                  opt_name_transform=default_opt_name_transform):
    from SCons.Variables.PathVariable import PathVariable
    from SConsGnuBuild.GVars import GVarDeclU, GVarDeclU
    def _callback(name, desc, default):
        decl = { 'env_key'  : env_key_transform(name),
                 'var_key'  : var_key_transform(name),
                 'opt_key'  : opt_key_transform(name),
                 'default'  : default,
                 'help'     : desc,
                 'option'   : opt_name_transform(name),
                 'type'     : 'string',
                 'nargs'    : 1,
                 'metavar'  : 'DIR' }
        return name, decl

    return GVarDeclU(__map_std_var_triples(_callback, name_filter))

###############################################################################
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
        opt_key_transform : callable
            function or lambda used to transform canonical ``GVar`` names to
            keys used for corresponding SCons command-line options
            ``--option=value`` (default: `default_opt_key_transform`)
        opt_name_transform : callable
            function or lambda used to transform canonical ``GVar`` names to
            option names (default: `default_opt_name_transform`)
    :Returns:
        a dictionary-like object of type `SConsGnuBuild.GVar._GVarDecls`
    """
    args = ['name_filter', 'env_key_transform', 'var_key_transform',
            'opt_key_trasform', 'opt_name_transform']
    kw2 = { key : kw[key] for key in args if key in kw }
    return declare_gvars(**kw2)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
