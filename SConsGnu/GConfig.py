"""`SConsGnu.GConfig`

TODO: Write docs for XXX
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


class _GConfig(object):
    """
    **Example**

    ..python::

        from SConsGnu.GConfig import _GConfig
        env = Environment()
        conf = _GConfig(env)
        gdecls = conf.DeclareGVars()
        # TODO: finish the example

    :IVariables:
        env : SCons environment
            Environment used to store values of configuration variables
            as construction variables,
        file : string | None
            File name of a file used to store/restore configuration variables,
        variables
            An instance of `SCons.Variables.Variables`_ used as command-line
            variables and to store/restore variables.
        dir_var_options
            May be ``True`` (default) or ``False`` to determine whether we want
            to have the "GNU directory variables" (``prefix``, ``exec_prefix``,
            ``bindir`` and so on); it may be a dict with default values of
            keyword arguments to `SConsGnu.GDirVars.DeclareGVars()`

    .. _SCons.Variables.Variables: http://www.scons.org/doc/latest/HTML/scons-api/SCons.Variables.Variables-class.html
    """
    def __init__(self, env, filename=None, gvar_decls=None, variables=None,
                 options=True, args={}, is_global=1):
        """Constructor for `_GConfig`.

        :Parameters:
            env
                SCons environment object (`SCons.Environment.Environment`_);
                during configuration, contruction variables in `env` may be
                created or updated,
            filename : string
                name of the file used to store/restore configuration variables,
            gvar_decls : `_GVarDecls` | None
                declarations of additional ``GVar`` variables to be used as
                configuration variables,
            variables
                SCons Variables (`SCons.Variables.Variables`_) object or
                ``None``; if ``None``, an instance of ``Variables`` will be
                created internally by `__init__()`,
            options : Boolean
                whether to define and use command-line options
                (``--option=value``) for configuration process,
            args : dict
                passed to `SCons.Variables.Variables.__init__()`_ as the
                ``args`` argument in case we are supposed to create variables;
                used only if the `variables` are not provided an we are
                supposed to create them by ourselves,
            is_global
                passed to `SCons.Variables.Variables.__init__()`_ as the
                ``is_global`` argument; used only if the `variables` are not
                provided an we are supposed to create them by ourselves,

        .. _SCons.Environment.Environment: http://www.scons.org/doc/latest/HTML/scons-api/SCons.Environment.Base-class.html
        .. _SCons.Variables.Variables: http://www.scons.org/doc/latest/HTML/scons-api/SCons.Variables.Variables-class.html
        .. _SCons.Variables.Variables.__init__(): http://www.scons.org/doc/latest/HTML/scons-api/SCons.Variables.Variables-class.html#__init__
        """
        self.env = env
        self.filename = filename
        self.dir_var_options = True
        self.__init_gvar_decls(gvar_decls)
        self.__init_variables(variables, file, args, is_global)

    def __init_gvar_decls(self, gvar_decls):
        "For internal use only"
        from SConsGnu.GVars import GVarDecls
        if gvar_decls is None:
            gvar_decls = GVarDecls()
        self.gvar_decls = gvar_decls

    def __init_variables(self, variables, file, args, is_global):
        "For internal use only"
        from SCons.Variables import Variables
        if variables is None:
            variables = Variables(file, args, is_global)
        self.variables = variables

    @staticmethod
    def _mix_kwargs(defaults, **kw):
        from SCons.Util import is_Dict
        if is_Dict(defaults):
            kw2 = defaults.copy()
            kw2.update(kw)
            return kw2
        elif defaults:
            return kw
        else:
            return None

    def DeclareGVars(self, **kw):
        """Declare ``GVar`` variables provided by all relevant modules"""
        from SConsGnu import GDirVars
        # 1. GDirVars
        kw2 = _GConfig._mix_kwargs(self.dir_var_options, **kw)
        self.gvar_decls.update(GDirVars.DeclareGVars(**kw2))
        # Append other declarations if necessary
        return self.gvar_decls

    def Configure(self, **kw):
        pass

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
