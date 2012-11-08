"""`SConsGnuBuild.GnuDirVars`

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
__std_var_templates = [
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

#############################################################################
def __init_module_vars():
    for sec in map(lambda x : str(x), range(0,10)) + ['l', 'n']:
        __std_var_templates.append( ('man%sdir' % sec, '', '${prefix}/man/man%s' %sec) )
        __std_var_templates.append( ('man%sext' % sec, '', '.%s' %sec) )
__init_module_vars()

#############################################################################
def __process_std_var_templates(callback, **kw):
    """Feed all predefined GNU variables to callback.

    :Parameters:
      callback : callable
        function of type ``callback(name, desc, default)``, where

          - ``name:`` is the name of variable being processed,
          - ``desc:`` is short description,
          - ``default:`` is the default value for the variable.
    :Keywords:
        only : list
            list of variable names to process, others are ignored
        exclude : list
            list of variable names to exclude from processing
    """
    from SCons.Util import is_List
    try:
      only = kw['only']
      if not is_List(only): only = [ only ]
    except KeyError:
      only = None

    try:
      exclude = kw['exclude']
      if not is_List(exclude): exclude = [ exclude ]
    except KeyError:
      exclude = None

    for dvt in __std_var_templates:
        may_process = True
        name, desc, default = dvt
        if (only is not None) and (name not in only):   may_process = False
        if (exclude is not None) and (name in exclude): may_process = False
        if may_process:
          callback(name, desc, default)

#############################################################################
def AddDirVarsToSConsVariables(variables, **kw):
    """Add GNU directory variables to SCons command line variables.
       
    :Parameters:
        variables : ``SCons.Variables.Variables``
            SCons variables to which GNU directory variables will be added

    :Keywords:
        path_validator : callable
            use ``path_validator`` instead of default ``PathAccept``
            when creating SCons command line variables.
        only : list
            list of variable names to process, others are ignored
        exclude : list
            list of variable names to exclude from processing

    Returns:
        - returns updated ``variables``

    **Example:**

    .. python::
        
        from SConsGnuBuild.GnuDirVars import AddDirVarsToSConsVariables
        env = Environment()
        gnuvars = AddDirVarsToSConsVariables(Variables(),only=['prefix'])
        gnuvars.Update(env, ARGUMENTS)
        
    In the above example the ``prefix`` variable is added to scons command
    line with default value. In effect, we may interpolate the variable as:

    .. python::
        
        prefix = env.subst('${prefix}')

    and set its value from command-line: ``scons prefix=/usr``
    """
    from SCons.Variables import PathVariable

    nkw = kw.copy()
    try:
      path_validator = nkw['path_validator']
      del nkw['path_validator']
    except KeyError:
      path_validator = PathVariable.PathAccept

    def _add_variable(name, desc, default):
        variables.Add( PathVariable(name, desc, default, path_validator) )

    __process_std_var_templates(_add_variable, **nkw)

    return variables

#############################################################################
def AddDirVarsToSConsOptions(**kw):
    """Add GNU directory variables as SCons commandline options.

    This function calls ``AddOption()`` for each processed GNU directory
    variable.

    :Keywords:
        only : list
            list of variable names to process, others are ignored
        exclude : list
            list of variable names to exclude from processing

    **Example:**

    .. python::

       from SConsGnuBuild.GnuDirVars import AddDirVarsToSConsOptions
       env = Environment()
       AddDirVarsToSConsOptions( only = [ 'prefix', 'exec_prefix' ] )
       env.Replace(prefix = GetOption('prefix'))
       env.Replace(exec_prefix = GetOption('exec_prefix'))
       print "${prefix}: ", env.subst('${prefix}')
       print "${exec_prefix}: ", env.subst('${exec_prefix}')

    The above example results with two new SCons options: ``--prefix`` and
    ``--exec-prefix`` being added to command line options. The option values
    provided by user at command shell are copied to construction variables
    ``prefix`` and ``exec_prefix``.
    """
    from SCons.Script.Main import AddOption
    def _add_option(name, desc, default):
        import re
        AddOption('--%s' % re.sub('_','-',name), dest=name, type='string', 
                  nargs=1, action='store', metavar='DIR', help=desc,
                  default=default) 
    __process_std_var_templates(_add_option, **kw)

#############################################################################
def AddDirVarsToSConsEnvironment(env, **kw):
    """Add GNU directory variables to SCons construction variables.
     
    This function calls ``env.SetDefault(name = default)`` for each processed
    GNU directory variable, where ``name`` is name of the variable and 
    ``default`` is its default value.

    :Parameters:
        env
            environment (``SCons.Environment.Environment``) to update,
    :Keywords:
        only : list
            list of variable names to process, others are ignored
        exclude : list
            list of variable names to exclude from processing

    **Example:**

    .. python::

       from SConsGnuBuild.GnuDirVars import AddDirVarsToSConsEnvironment
       env = Environment()
       AddDirVarsToSConsEnvironment(env, only=['prefix','exec_prefix'])

    The above example adds ``prefix`` and ``exec_prefix`` variables to ``env``,
    so they may be used later in substitutions:
    
    .. python::

        exec_prefix = env.subst('${exec_prefix}')
        exec_prefix2 = env['exec_prefix']
    """
    def _add_variable(name, desc, default):
        env.SetDefault(name = default)
    __process_std_var_templates(_add_variable, **kw)


#############################################################################
def DirVarsAsSConsVariables(files = [], args = {}, is_global = 1, **kw):
    """Return new set of command line variables with GNU directory variables
    added. 

    **Example**:

    .. python::

        from SConsGnuBuild.GnuDirVars import DirVarsAsSConsVariables
        env = Environment()
        gnuvars = DirVarsAsSConsVariables()
        gnuvars.Update(env, ARGUMENTS)

    The above example adds all GNU directory variables to command line
    variables.

    The first three parameters to this function are identical as for
    ``SCons.Variables.Variables()``. 

    :Keywords:
        path_validator : callable
            use ``path_validator`` instead of default ``PathAccept``
            when creating SCons command line variables.
        only : list
            list of variable names to process, others are ignored
        exclude : list
            list of variable names to exclude from processing
    """
    from SCons.Variables import Variables
    return AddDirVarsToSConsVariables(Variables(files, args, is_global),**kw)

#############################################################################
def StandardDirVars():
    """Return the names of supported GNU dir variables"""
    variables = []
    for v in  __std_var_templates:
        variables.append(v[0])
    return variables

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
