"""`SConsGnuBuild.GVars`

This module provides an implementation of what we call ``GVars`` (abbreviation
of "gluing variables"). A ``GVar`` variable correlates single construction
variable in SCons environment (``env['NAME'], env.subst('$NAME')``), single
SCons command-line variable (``variable=value``) and single SCons command-line
option (``--option=value``). Some (or all) of them may be missing in ``GVar``
definition, so we may for example correlate only construction variable and some
command-line option (no command-line variable in definition).

With ``GVars`` you use separate namespaces for environment variables,
command-line variables and command-line options. So, for example, you may
create a ``GVar`` variable  ``foo`` which correlates a construction variable
``ENV_FOO``, command-line variable ``VAR_FOO`` and command-line option
identified by key ``opt_foo`` (we use ``dest`` attribute of command line option
as its identifying key, see `option attributes`_ of python ``optparse``). At
certain point, you may request ``GVars`` to update your SCons environment
``env`` by populating it with values taken from command-line variables and/or
options.  At this point, value taken from command-line variable ``VAR_FOO`` or
value from command-line option ``opt_foo`` may be passed to construction
variable ``ENV_FOO``. If both, command-line variable and command-line option
are set, then command-line option takes precedence.

If a command-line value is a string, it may contain substitutions (e.g.
``VAR_FOO`` may be a string in form ``"bleah bleah ${VAR_BAR}"``).
Placeholders in text are assumed to be variable/option names in "local
namespace". It means, that if we have a command-line variable, and its value is
a string containing placeholder ``"$VVV"``, then ``VVV`` is assumed to be the
name of another command-line variable (and not, for example,
construction/environment variable). When passing strings from command-line
variables and options to an environment, the placeholders are renamed to
represent corresponding construction variables in SCons environment. This is
shown in the example below.

**Example**

Assume, we have following three ``GVar``'s defined::

    .               (1)         (2)         (3)
    GVars:          foo         bar         geez
    Environment:    ENV_FOO     ENV_BAR     ENV_GEEZ
    Variables:      VAR_FOO     VAR_BAR     VAR_GEEZ
    Options:        opt_foo     opt_bar     opt_geez
    .             --opt-foo   --opt-bar   --opt-geez


and we invoked scons as follows::

    # Command line:
    scons VAR_FOO='${VAR_BAR}' VAR_BAR='${foo}' --opt-geez='${opt_foo}'

then after updating a SCons environment ``env`` with command-line variables
and options corresponding to ``GVar`` variables, the environment will have
following construction variables set::

    env['ENV_FOO'] = '${ENV_BAR}'   # VAR_FOO -> ENV_FOO,  VAR_BAR -> ENV_BAR
    env['ENV_BAR'] = '${foo}'       # VAR_BAR -> ENV_BAR,  foo -*-> foo
    env['ENV_GEEZ'] = '${ENV_FOO}'  # opt_geez-> ENV_GEEZ, opt_foo -> ENV_FOO

The ``-*->`` arrow means, that there was no command-line variable named
``foo``, so the ``"${foo}"`` placeholder was left unaltered.

Now, as we know the general idea, let's see some code examples.

**Example**

Consider following ``SConsctruct`` file

.. python::

    from SConsGnuBuild.GVars import GVarDecls
    env = Environment()
    gdecls = GVarDecls(
       # GVar 'foo'
       foo =  (   {'ENV_FOO' : 'ENV_FOO default'},                  # ENV
                  ('VAR_FOO',  'VAR_FOO help'),                     # VAR
                  ('--foo',       {'dest' : "opt_foo"})         ),  # OPT
       # GVar 'bar'
       bar = (   {'ENV_BAR' : None},                                # ENV
                 ('VAR_BAR', 'VAR_BAR help', 'VAR_BAR default'),    # VAR
                 ('--bar', {'dest':"opt_bar", "type":"string"})),   # OPT
       # GVar 'geez'
       geez =(   {'ENV_GEEZ' : None},                               # ENV
                 ('VAR_GEEZ', 'VAR_GEEZ help', 'VAR_GEEZ default'), # VAR
                 ('--geez', {'dest':"opt_geez", "type":"string"}))  # OPT
    )
    variables = Variables()
    gvars = gdecls.Commit(env, variables, True)
    gvars.UpdateEnvironment(env, variables, True)

    print "env['ENV_FOO']: %r" %  env['ENV_FOO']
    print "env['ENV_BAR']: %r" %  env['ENV_BAR']
    print "env['ENV_GEEZ']: %r" %  env['ENV_GEEZ']

In above we define three ``GVar`` variables: ``foo``, ``bar`` and ``geez``.
Corresponding construction variables (environment) are named ``ENV_FOO``,
``ENV_BAR`` and ``ENV_GEEZ`` respectively. Corresponding command-line variables
are: ``VAR_FOO``, ``VAR_BAR`` and ``VAR_GEEZ``. Finally, the command-line
options that correspond to our ``GVar`` variables are named ``opt_foo``,
``opt_bar`` and ``opt_geez`` (note: these are actually keys identifying options
within SCons script, they may be different from the option names that user sees
on its screen - here we have key ``opt_foo`` and command-line option ``--foo``).

To learn details about ``GVar`` variables and possible ways to declare them
start with `GVarDecls()` and `GVarDecl()` documentation.

Running scons several times, you may obtain different output depending on
command-line variables and options provided. Let's do some experiments, first
show the help message to see available command-line options::

    user@host:$ scons -Q -h
    env['ENV_FOO']: 'ENV_FOO default'
    env['ENV_BAR']: 'VAR_BAR default'
    env['ENV_GEEZ']: 'VAR_GEEZ default'
    usage: scons [OPTION] [TARGET] ...

    SCons Options:
       <.... lot of output here ...>
    Local Options:
      --geez=OPT_GEEZ
      --foo=OPT_FOO
      --bar=OPT_BAR

then play with them a little bit (as well as with command-line variables)::

    user@host:$ scons -Q --foo='OPT FOO'
    env['ENV_FOO']: 'OPT FOO'
    env['ENV_BAR']: 'VAR_BAR default'
    env['ENV_GEEZ']: 'VAR_GEEZ default'
    scons: `.' is up to date.

    user@host:$ scons -Q VAR_FOO='VAR_FOO cmdline'
    env['ENV_FOO']: 'VAR_FOO cmdline'
    env['ENV_BAR']: 'VAR_BAR default'
    env['ENV_GEEZ']: 'VAR_GEEZ default'
    scons: `.' is up to date.

    user@host:$ scons -Q VAR_FOO='VAR_FOO cmdline' --foo='opt_foo cmdline'
    env['ENV_FOO']: 'opt_foo cmdline'
    env['ENV_BAR']: 'VAR_BAR default'
    env['ENV_GEEZ']: 'VAR_GEEZ default'
    scons: `.' is up to date.

    user@host:$ scons -Q VAR_FOO='VAR_FOO and ${VAR_BAR}'
    env['ENV_FOO']: 'VAR_FOO and ${ENV_BAR}'
    env['ENV_BAR']: 'VAR_BAR default'
    env['ENV_GEEZ']: 'VAR_GEEZ default'
    scons: `.' is up to date.

    user@host:$ scons -Q --foo='opt_foo with ${opt_geez}'
    env['ENV_FOO']: 'opt_foo with ${ENV_GEEZ}'
    env['ENV_BAR']: 'VAR_BAR default'
    env['ENV_GEEZ']: 'VAR_GEEZ default'
    scons: `.' is up to date.

You may decide to not create corresponding command-line variable or
command-line option for a particular ``GVar``. In following example we declare
two ``GVar`` variables named ``foo`` and ``bar``. Variable ``foo`` has no
corresponding command-line variable and variable ``bar`` has no corresponding
command-line option.

**Example**

Consider following ``SConstruct`` file:

.. python::

    from SConsGnuBuild.GVars import GVarDecls
    env = Environment()
    gdecls = GVarDecls(
       # GVar 'foo'
       foo =  (   {'ENV_FOO' : 'ENV_FOO default'},                  # ENV
                  None,                                             # no VAR
                  ('--foo',       {'dest' : "opt_foo"})         ),  # OPT
       # GVar 'bar'
       bar = (   {'ENV_BAR' : None},                                # ENV
                 ('VAR_BAR', 'VAR_BAR help', 'VAR_BAR default'),    # VAR
                 None                                           ),  # no OPT
    )
    variables = Variables()
    gvars = gdecls.Commit(env, variables, True)
    gvars.UpdateEnvironment(env, variables, True)

    print "env['ENV_FOO']: %r" %  env['ENV_FOO']
    print "env['ENV_BAR']: %r" %  env['ENV_BAR']

Some experiments with command-line yield following output::

    user@host:$ scons -Q VAR_FOO='VAR_FOO cmdline'
    env['ENV_FOO']: 'ENV_FOO default'
    env['ENV_BAR']: 'VAR_BAR default'
    scons: `.' is up to date.

    user@host:$ scons -Q --bar='opt_bar cmdline'
    env['ENV_FOO']: 'ENV_FOO default'
    env['ENV_BAR']: 'VAR_BAR default'
    usage: scons [OPTION] [TARGET] ...

    SCons error: no such option: --bar

    user@host:$ scons -Q --foo='opt_foo and ${opt_bar}'
    env['ENV_FOO']: 'opt_foo and ${opt_bar}'
    env['ENV_BAR']: 'VAR_BAR default'
    scons: `.' is up to date.

    user@host:$ scons -Q --foo='opt_foo and ${opt_foo}'
    env['ENV_FOO']: 'opt_foo and ${ENV_FOO}'
    env['ENV_BAR']: 'VAR_BAR default'
    scons: `.' is up to date.

    user@host:$ scons -Q VAR_BAR='VAR_BAR and ${VAR_FOO}'
    env['ENV_FOO']: 'ENV_FOO default'
    env['ENV_BAR']: 'VAR_BAR and ${VAR_FOO}'
    scons: `.' is up to date.

    user@host:$ scons -Q VAR_BAR='VAR_BAR and ${VAR_BAR}'
    env['ENV_FOO']: 'ENV_FOO default'
    env['ENV_BAR']: 'VAR_BAR and ${ENV_BAR}'
    scons: `.' is up to date.


For more details we refer you to the documentation of `GVarDecls()`,
`GVarDecl()` functions and `_GVarDecls`, `_GVars`, and `_GVarDecl` classes.

.. _option attributes: http://docs.python.org/2/library/optparse.html#option-attributes
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

__docformat__ = "restructuredText"

#############################################################################
ENV = 0
"""Represents selection of construction variable corresponding to particular
``GVar`` variable."""

VAR = 1
"""Represents selection of command-line variable corresponding to particular
``GVar`` variable."""

OPT = 2
"""Represents selection of command-line option related to particular ``GVar``
variable."""

ALL = 3
"""Number of all namespaces (currently there are three: ``ENV``, ``VAR``,
``OPT``)"""
#############################################################################


#############################################################################
class _missing(object):
    "Represents missing argument to function."
    pass

#############################################################################
class _dont_create(object):
    "Represents the fact, that a variable shouldn't be created."
    pass

#############################################################################
class _notfound(object):
    "Something that has not been found."
    pass # represents a key that is never present in dict

#############################################################################
def _resubst(value, resubst_dict = {}):
    """Rename placeholders (substrings like ``$name``) in a string value.

    :Parameters:
        value
            the value to process; if it is string it is passed through
            placeholder renaming procedure, otherwise it is returned unaltered,
        resubst_dict
            a dictionary of the form ``{ "xxx" : "${yyy}", "vvv" : "${www}",
            ...}`` used to rename placeholders within ``value`` string; with
            above dictionary, all occurrences of ``$xxx`` or ``${xxx}`` within
            `value` string will be replaced with ``${yyy}``, all occurrences of
            ``$vvv`` or ``${vvv}`` with ``${www}`` and so on; see also
            `_build_resubst_dict()`,
    :Returns:
        returns the ``value`` with placeholders renamed.
    """
    from string import Template
    from SCons.Util import is_String
    if is_String(value):
        # make substitution in strings only
        return Template(value).safe_substitute(**resubst_dict)
    else:
        return value

#############################################################################
def _build_resubst_dict(rename_dict):
    """Build dictionary for later use with `_resubst()`.

    **Example**

    .. python::

        >>> from SConsGnuBuild.GVars import _build_resubst_dict
        >>> _build_resubst_dict( {"xxx":"yyy", "vvv":"www", "zzz":"zzz" })
        {'vvv': '${www}', 'xxx': '${yyy}'}

    :Parameters:
        rename_dict : dict
            dictionary of the form ``{"xxx":"yyy", "vvv":"www", ...}``
            mapping variable names from one namespace to another,

    :Returns:
        returns dictionary of the form ``{"xxx":"${yyy}", "vvv":"${www}"}``
        created from `rename_dict`; items ``(key, val)`` with ``key==val`` are
        ignored, so the entries of type ``"zzz":"zzz"`` do not enter the
        result.
    """
    return dict(map(lambda (k,v): (k, '${' + v + '}'),
                    filter(lambda (k,v) : k != v, rename_dict.iteritems())))

#############################################################################
def _build_iresubst_dict(rename_dict):
    """Build inverted dictionary for later use with `_resubst()`.

    **Example**

    .. python::

        >>> from SConsGnuBuild.GVars import _build_resubst_dict
        >>> _build_iresubst_dict( {"xxx":"yyy", "vvv":"www", "zzz":"zzz" })
        {'www': '${vvv}', 'yyy': '${xxx}'}

    :Parameters:
        rename_dict : dict
            dictionary of the form ``{"xxx":"yyy", "vvv":"www", ...}``
            mapping variable names from one namespace to another

    :Returns:
        returns dictionary of the form ``{"yyy":"${xxx}", "www":"${vvv}",
        ...}`` created from inverted dictionary `rename_dict`; items ``(key,
        val)`` with ``key==val`` are ignored, so the entries of type
        ``"zzz":"zzz"`` do not enter the result;
    """
    return dict(map(lambda (k,v): (v, '${' + k + '}'),
                    filter(lambda (k,v) : k != v, rename_dict.iteritems())))

#############################################################################
def _compose_dicts(dict1, dict2):
    """Compose two mappings expressed by dicts ``dict1`` and ``dict2``.

    :Parameters:
        dict1, dict2
            dictionaries to compose

    :Returns:
        returns a dictionary such that for each item ``(k1,v1)`` from `dict1`
        and ``v2 = dict2[v1]`` the corresponding item in returned dictionary is
        ``(k1,v2)``
    """
    return dict(map(lambda (k,v) : (k, dict2[v]), dict1.iteritems()))

#############################################################################
def _invert_dict(_dict):
    return dict(map(lambda (k,v) : (v,k), _dict.iteritems()))

#############################################################################
class _GVarsEnvProxy(object):
    #========================================================================
    """Proxy used to get/set construction variables in `SCons environment`_
    while operating on mapped variable names.

    This object reimplements several methods of SCons
    ``SubstitutionEnvironment`` used to access environment's construction
    variables. The variable names (and placeholders found in their values) are
    translated forth and backk from/to ``GVars`` namespace when accessing the
    variables.

    **Example**::

        user@host:$ scons -Q -f -

        from SConsGnuBuild.GVars import _GVarsEnvProxy
        env = Environment()
        proxy = _GVarsEnvProxy(env, {'foo':'ENV_FOO'}, {'foo':'${ENV_FOO}'},
                                    {'ENV_FOO':'foo'}, {'ENV_FOO':'${foo}'})
        proxy['foo'] = "FOO"
        print "proxy['foo'] is %r" % proxy['foo']
        print "env['ENV_FOO'] is %r" % env['ENV_FOO']
        <Ctl+D>
        proxy['foo'] is 'FOO'
        env['ENV_FOO'] is 'FOO'
        scons: `.' is up to date.

    .. _SCons environment:  http://www.scons.org/doc/HTML/scons-user.html#chap-environments
    """
    #========================================================================
    def __init__(self, env, rename={}, resubst={}, irename={}, iresubst={},
                 strict=False):
        # -------------------------------------------------------------------
        """Initializes `_GVarsEnvProxy` object.

        :Parameters:
            env
                a SCons environment object to be proxied,
            rename
                dictionary used for mapping variable names from user namespace
                to environment namespace (used by `__setitem__()` and
                `__getitem__()`),
            resubst
                dictionary used by to rename placeholders in values passed
                from user to environment  (used by `__setitem__()` and
                `subst()`)
            irename
                dictionary used for mapping variable names from environment
                to user namespace (used by ``items()``),
            iresubst
                dictionary used by to rename placeholders in values passed
                back from environment to user (used by `__getitem__()` for
                example)
            strict
                if ``True`` only the keys defined in rename/resubst
                dictionaries are allowed, otherwise the original variables
                from ``env`` are also accessible via their keys
        """
        # -------------------------------------------------------------------
        self.env = env
        self.__rename = rename
        self.__irename = irename
        self.__resubst = resubst
        self.__iresubst = iresubst
        self.set_strict(strict)

    #========================================================================
    def is_strict(self):
        return self.__strict

    #========================================================================
    def set_strict(self, strict):
        self.__setup_methods(strict)
        self.__strict = strict

    #========================================================================
    def __setup_methods(self, strict):
        if strict:
            self.__delitem__impl = self.__delitem__strict
            self.__getitem__impl = self.__getitem__strict
            self.__setitem__impl = self.__setitem__strict
            self.get = self._get_strict
            self.has_key = self._has_key_strict
            self.__contains__impl = self.__contains__strict
            self.items = self._items_strict
        else:
            self.__delitem__impl = self.__delitem__nonstrict
            self.__getitem__impl = self.__getitem__nonstrict
            self.__setitem__impl = self.__setitem__nonstrict
            self.get = self._get_nonstrict
            self.has_key = self._has_key_nonstrict
            self.__contains__impl = self.__contains__nonstrict
            self.items = self._items_nonstrict

    #========================================================================
    def __delitem__(self, key):
        self.__delitem__impl(key)

    #========================================================================
    def __delitem__strict(self, key):
        self.env.__delitem__(self.__rename[key])

    #========================================================================
    def __delitem__nonstrict(self, key):
        self.env.__delitem__(self.__rename.get(key,key))

    #========================================================================
    def __getitem__(self, key):
        return self.__getitem__impl(key)

    #========================================================================
    def __getitem__strict(self, key):
        env_key = self.__rename[key]
        return _resubst(self.env[env_key], self.__iresubst)

    #========================================================================
    def __getitem__nonstrict(self, key):
        env_key = self.__rename.get(key,key)
        return _resubst(self.env[env_key], self.__iresubst)

    #========================================================================
    def __setitem__(self, key, value):
        return self.__setitem__impl(key, value)

    #========================================================================
    def __setitem__strict(self, key, value):
        env_key = self.__rename[key]
        env_value = _resubst(value, self.__resubst)
        self.env[env_key] = env_value

    #========================================================================
    def __setitem__nonstrict(self, key, value):
        env_key = self.__rename.get(key,key)
        env_value = _resubst(value, self.__resubst)
        self.env[env_key] = env_value

    #========================================================================
    def _get_strict(self, key, default=None):
        env_key = self.__rename[key]
        return _resubst(self.env.get(env_key, default), self.__iresubst)

    #========================================================================
    def _get_nonstrict(self, key, default=None):
        env_key = self.__rename.get(key,key)
        return _resubst(self.env.get(env_key, default), self.__iresubst)

    #========================================================================
    def _has_key_strict(self, key):
        return key in self.__rename

    #========================================================================
    def _has_key_nonstrict(self, key):
        return self.env.has_key(self.__rename.get(key,key))

    #========================================================================
    def __contains__(self, key):
        return self.__contains__impl(key)

    #========================================================================
    def __contains__strict(self, key):
        return self.env.__contains__(self.__rename[key])

    #========================================================================
    def __contains__nonstrict(self, key):
        return self.env.__contains__(self.__rename.get(key,key))

    #========================================================================
    def _items_strict(self):
        iresubst = lambda v : _resubst(v, self.__iresubst)
        return [ (k, self[k]) for k in self.__rename ]

    #========================================================================
    def _items_nonstrict(self):
        iresubst = lambda v : _resubst(v, self.__iresubst)
        irename = lambda k : self.__irename.get(k,k)
        return [ (irename(k), iresubst(v)) for (k,v) in self.env.items() ]

    #========================================================================
    def subst(self, string, *args):
        env_string = _resubst(string, self.__resubst)
        return self.env.subst(env_string, *args)


#############################################################################
class _GVars(object):
    #========================================================================
    """Correlates construction variables from SCons environment with
    command-line variables (``variable=value``) and command-line options
    (``--option=value``).

    **Note**:

        In several places we use ``xxx`` as placeholder for one of the ``ENV``,
        ``VAR`` or ``OPT`` constants which represent selection of
        "corresponding Environment construction variable", "corresponding SCons
        command-line variable" or "corresponding SCons command-line option"
        respectively.  So, for example the call
        ``gvars.get_xxx_key(ENV,"foo")`` returns the key of construction
        variable in SCons environment (``ENV``) which is related to our
        ``GVar`` variable ``foo``.

    In fact, the only internal data the object holds is a list of supplementary
    dictionaries to map the names of variables from one namespace (e.g ``ENV``)
    to another (e.g. ``OPT``).
    """
    #========================================================================

    #========================================================================
    def __init__(self, gdecls):
        # -------------------------------------------------------------------
        """Initializes `_GVars` object according to declarations `gdecls` of
        ``GVar`` variables.

        :Parameters:
            gdecls : `_GVarDecls`
                declarations of ``GVar`` variables,
        """
        # -------------------------------------------------------------------
        self.__keys = gdecls.keys()
        self.__init_supp_dicts(gdecls)

    #========================================================================
    def __reset_supp_dicts(self):
        """Initialize empty supplementary dictionaries to empty state"""
        self.__rename = [{} for n in range(0,ALL)]
        self.__irename = [{} for n in range(0,ALL)]
        self.__resubst = [{} for n in range(0,ALL)]
        self.__iresubst = [{} for n in range(0,ALL)]

    #========================================================================
    def __init_supp_dicts(self, gdecls):
        """Initialize supplementary dictionaries according to variable
        declarations."""
        self.__reset_supp_dicts()
        if gdecls is not None:
            for xxx in range(0,ALL):
                self.__rename[xxx] = gdecls.get_xxx_rename_dict(xxx)
                self.__irename[xxx] = gdecls.get_xxx_irename_dict(xxx)
                self.__resubst[xxx] = gdecls.get_xxx_resubst_dict(xxx)
                self.__iresubst[xxx] = gdecls.get_xxx_iresubst_dict(xxx)

    #========================================================================
    def VarEnvProxy(self, env, *args, **kw):
        """Return proxy to SCons environment `env` which uses keys from
        `VAR` namespace to access corresponding environment construction
        variables"""
        rename = _compose_dicts(self.__irename[VAR], self.__rename[ENV])
        irename = _invert_dict(rename)
        resubst = _build_resubst_dict(rename)
        iresubst = _build_resubst_dict(irename)
        return _GVarsEnvProxy(env, rename, resubst, irename, iresubst, *args,
                              **kw)

    #========================================================================
    def OptEnvProxy(self, env, *args, **kw):
        """Return proxy to SCons environment `env` which uses keys from
        `OPT` namespace to access corresponding environment construction
        variables"""
        rename = _compose_dicts(self.__irename[OPT], self.__rename[ENV])
        irename = _invert_dict(rename)
        resubst = _build_resubst_dict(rename)
        iresubst = _build_resubst_dict(irename)
        return _GVarsEnvProxy(env, rename, resubst, irename, iresubst, *args,
                              **kw)

    #========================================================================
    def EnvProxy(self, env, *args, **kw):
        """Return proxy to SCons environment `env` which uses original keys
        identifying ``GVar`` variables to access construction variables"""
        return _GVarsEnvProxy(env, self.__rename[ENV], self.__resubst[ENV],
                                   self.__irename[ENV], self.__iresubst[ENV],
                                   *args, **kw)

    #========================================================================
    def get_keys(self):
        """Return the list of keys identifying ``GVar`` variables defined in
        this object (list of ``GVar`` variable names)."""
        from copy import copy
        return copy(self.__keys)

    #========================================================================
    def get_xxx_key(self, xxx, key):
        #--------------------------------------------------------------------
        """Get the key identifying a variable related to ``GVar`` identified by
        ``key``

        :Parameters:
            xxx : int
                one of `ENV`, `VAR` or `OPT`,
            key : string
                the key identifying ``GVar`` variable of choice.
        """
        #--------------------------------------------------------------------
        return self.__rename[xxx][key]

    #========================================================================
    def env_key(self, key):
        return self.__rename[ENV][key]

    #========================================================================
    def var_key(self, key):
        return self.__rename[VAR][key]

    #========================================================================
    def opt_key(self, key):
        return self.__rename[OPT][key]

    #========================================================================
    def update_env_from_vars(self, env, variables, args=None):
        #--------------------------------------------------------------------
        """Update construction variables in SCons environment
        (``env["VARIABLE"]=VALUE``) according to values stored in their
        corresponding command-line variables (``variable=value``).

        **Note**:

            This function calls the `variables.Update(proxy[,args])`_ method
            passing proxy to `env` (see `_GVarsEnvProxy`) to introduce mappings
            between ``ENV`` and ``VAR`` namespaces.

        :Parameters:
            env
                `SCons environment`_ object to update
            variables
                `SCons variables`_ object to take values from

        .. _SCons environment:  http://www.scons.org/doc/HTML/scons-user.html#chap-environments
        .. _SCons variables: http://www.scons.org/doc/HTML/scons-user.html#sect-command-line-variables
        .. _variables.Update(proxy[,args]): http://www.scons.org/doc/latest/HTML/scons-api/SCons.Variables.Variables-class.html#Update
        """
        #--------------------------------------------------------------------
        proxy = self.VarEnvProxy(env)
        variables.Update(proxy, args)

    #========================================================================
    def update_env_from_opts(self, env):
        #--------------------------------------------------------------------
        """Update construction variables in SCons environment
        (``env["VARIABLE"]=VALUE``) according to values stored in their
        corresponding `command-line options`_ (``--option=value``).

        :Parameters:
            env
                `SCons environment`_ object to update

        .. _SCons environment:  http://www.scons.org/doc/HTML/scons-user.html#chap-environments
        .. _command-line options: http://www.scons.org/doc/HTML/scons-user.html#sect-command-line-options
        """
        #--------------------------------------------------------------------
        from SCons.Script.Main import GetOption
        proxy = self.OptEnvProxy(env)
        for opt_key in self.__irename[OPT]:
            opt_value = GetOption(opt_key)
            if opt_value is not None:
                proxy[opt_key] = opt_value

    #========================================================================
    def UpdateEnvironment(self, env, variables=None, options=False, args=None):
        #--------------------------------------------------------------------
        """Update construction variables in SCons environment
        (``env["VARIABLE"]=VALUE``) according to values stored in their
        corresponding `command-line variables`_ (``variable=value``) and/or
        `command-line options`_ (``--option=value``).

        :Parameters:
            env
                `SCons environment`_ object to update,
            variables : ``SCons.Variables.Variables`` | None
                if not ``None``, it should be a `SCons.Variables.Variables`_
                object with `SCons variables`_ to retrieve values from,
            options : boolean
                if ``True``, `command-line options`_ are taken into account
                when updating `env`.
            args
                if not ``None``, passed verbatim to `update_env_from_vars()`.

        .. _SCons.Variables.Variables: http://www.scons.org/doc/latest/HTML/scons-api/SCons.Variables.Variables-class.html
        .. _SCons environment:  http://www.scons.org/doc/HTML/scons-user.html#chap-environments
        .. _command-line variables: http://www.scons.org/doc/HTML/scons-user.html#sect-command-line-variables
        .. _SCons variables: http://www.scons.org/doc/HTML/scons-user.html#sect-command-line-variables
        .. _command-line options: http://www.scons.org/doc/HTML/scons-user.html#sect-command-line-options
        """
        #--------------------------------------------------------------------
        # TODO: implement priority?
        if variables is not None:
            self.update_env_from_vars(env, variables, args)
        if options:
            self.update_env_from_opts(env)

    def SaveVariables(self, variables, filename, env):
        #--------------------------------------------------------------------
        """Save the `variables` to file mapping appropriately their names.

        :Parameters:
            variables : ``SCons.Variables.Variables``
                if not ``None``, it should be an instance of
                `SCons.Variables.Variables`_; this object is used to save
                SCons variables,
            filename : string
                name of the file to save into
            env
                `SCons environment`_ object to update,

        .. _SCons.Variables.Variables: http://www.scons.org/doc/latest/HTML/scons-api/SCons.Variables.Variables-class.html
        .. _SCons environment:  http://www.scons.org/doc/HTML/scons-user.html#chap-environments
        """
        #--------------------------------------------------------------------
        proxy = self.VarEnvProxy(env)
        variables.Save(filename, proxy)

    def GenerateVariablesHelpText(self, variables, env, *args):
        #--------------------------------------------------------------------
        """Save help text for `variables` using
        ``variables.GenerateHelpText()``.

        Note:
            this function handles properly mapping names between namespaces
            where SCons command line variables and construction variables live.

        :Parameters:
            variables : ``SCons.Variables.Variables``
                if not ``None``, it should be an instance of
                `SCons.Variables.Variables`_; this object is used to save
                SCons variables,
            env
                `SCons environment`_ object to update,
            args
                other arguments passed verbatim to ``GenerateHelpText()``

        .. _SCons.Variables.Variables: http://www.scons.org/doc/latest/HTML/scons-api/SCons.Variables.Variables-class.html
        .. _SCons environment:  http://www.scons.org/doc/HTML/scons-user.html#chap-environments
        """
        #--------------------------------------------------------------------
        proxy = self.VarEnvProxy(env)
        return variables.GenerateHelpText(proxy, *args)

#############################################################################
class _GVarDecl(object):
    #========================================================================
    """Declaration of single ``GVar`` variable.

    This object holds information necessary to create construction variable in
    SCons Environment, SCons command-line variable (``variable=value``) and
    SCons command-line option (``--option=value``) corresponding to a given
    ``GVar`` variable (it for example holds the names and default values of
    these variables/options before they get created).

    **Note**:

        In several places we use ``xxx`` as placeholder for one of the ``ENV``,
        ``VAR`` or ``OPT`` constants which represent selection of
        "corresponding Environment construction variable", "corresponding SCons
        command-line variable" or "corresponding SCons command-line option"
        respectively.  So, for example the call ``decl.set_xxx_decl(ENV,decl)``
        stores the declaration of corresponding construction variable in a
        SCons environment (``ENV``).
    """
    #========================================================================


    #========================================================================
    def __init__(self, *args):
        #--------------------------------------------------------------------
        """Constructor for _GVarDecl object

        :Parameters:
            args
                a tuple ``(env_decl, var_decl, opt_decl)``, where:

                - ``env_decl`` - parameters used later to create related
                  construction variable in `SCons environment`_, same as
                  ``decl`` argument to `_set_env_decl()`,
                - ``var_decl`` - parameters used later to create related
                  `SCons command-line variable`_, same as ``decl``
                  argument to `_set_var_decl()`,
                - ``opt_decl`` - parameters used later to create related
                  `SCons command-line option`_, same as  ``decl``
                  argument to `_set_opt_decl()`.

                all arguments are optional, missing argument is represented by
                ``None``.

        .. _SCons environment:  http://www.scons.org/doc/HTML/scons-user.html#chap-environments
        .. _SCons command-line option: http://www.scons.org/doc/HTML/scons-user.html#sect-command-line-options
        .. _SCons command-line variable: http://www.scons.org/doc/HTML/scons-user.html#sect-command-line-variables
        """
        #--------------------------------------------------------------------
        self.__xxx_args = [None,None,None]
        for xxx in range(0,min(ALL,len(args))):
            if args[xxx] is not None: self.set_xxx_decl(xxx, args[xxx])

    #========================================================================
    def set_xxx_decl(self, xxx, decl):
        #--------------------------------------------------------------------
        """Set declaration of related `xxx` variable, where `xxx` is one of
        `ENV`, `VAR` or `OPT`.

        This functions just dispatches the job between `_set_env_decl()`,
        `_set_var_decl()` and `_set_opt_decl()` according to `xxx` argument.

        :Parameters:
            xxx : int
                one of `ENV`, `VAR` or `OPT`,
            decl
                declaration parameters passed to particular setter function.
        """
        #--------------------------------------------------------------------
        if xxx == ENV:     self._set_env_decl(decl)
        elif xxx == VAR:   self._set_var_decl(decl)
        elif xxx == OPT:   self._set_opt_decl(decl)
        else:               raise IndexError("index out of range")

    #========================================================================
    def _set_env_decl(self, decl):
        #--------------------------------------------------------------------
        """Set parameters for later creation of the related construction
        variable in `SCons environment`_.

        :Parameters:
            decl : tuple | dict
                may be a tuple in form ``(name, default)``, or one-entry
                dictionary ``{name: default}``; later, when requested,
                this data is used to create construction variable for
                user provided `SCons environment`_ ``env`` with
                ``env.SetDefault(name = default)``

        .. _SCons environment:  http://www.scons.org/doc/HTML/scons-user.html#chap-environments
        """
        #--------------------------------------------------------------------
        from SCons.Util import is_Dict, is_Tuple, is_List, is_String
        if is_Tuple(decl):
            if not len(decl) == 2:
                raise ValueError("tuple 'decl' must have 2 elements but " \
                                 "has %d" % len(decl))
            else:
                decl = {decl[0] : decl[1]}
        elif is_Dict(decl):
            if not len(decl) == 1:
                raise ValueError("dictionary 'decl' must have 1 item but " \
                                 "has %d" % len(decl))
        elif is_String(decl):
            decl = { decl : _dont_create }
        else:
            raise TypeError("'decl' must be tuple, dictionary or string, %r " \
                            "is not allowed" % type(decl).__name__)
        self.__xxx_args[ENV] = decl

    #========================================================================
    def _set_var_decl(self, decl):
        #--------------------------------------------------------------------
        """Set parameters for later creation of the related `SCons command-line
        variable`_.

        :Parameters:
            decl : tuple | dict
                declaration parameters used later to add the related `SCons
                command-line variable`_; if `decl` is a tuple, it must have
                the form::

                    ( key [, help, default, validator, converter, kw] ),

                where entries in square brackets are optional; the consecutive
                elements  are interpreted in order shown above as ``key``,
                ``help``, ``default``, ``validator``, ``converter``, ``kw``;
                the meaning of these arguments is same as for
                `SCons.Variables.Variables.Add()`_; the ``kw``, if present,
                must be a dictionary;

                if `decl` is a dictionary, it should have the form::

                    { 'key'         : "file_name",
                      'help'        : "File name to read", ...  }

                the ``'kw'`` entry, if present, must be a dictionary; the
                arguments enclosed in the dictionary are later passed verbatim
                to `SCons.Variables.Variables.Add()`_.

        .. _SCons.Variables.Variables.Add(): http://www.scons.org/doc/latest/HTML/scons-api/SCons.Variables.Variables-class.html#Add
        .. _SCons command-line variable: http://www.scons.org/doc/HTML/scons-user.html#sect-command-line-variables
        """
        #--------------------------------------------------------------------
        from SCons.Util import is_Dict, is_Tuple, is_List
        if is_Tuple(decl) or is_List(decl):
            keys = [ 'key', 'help', 'default', 'validator', 'converter', 'kw' ]
            if len(decl) > len(keys):
                raise ValueError('len(decl) should be less or greater than ' \
                                 '%d, but is %d' % (len(keys),len(decl) ))
            args = dict(zip(keys, decl))
        elif is_Dict(decl):
            args = decl.copy()
        else:
            raise TypeError("'decl' must be a list, tuple or dict, %r " \
                            "is not allowed" % type(decl).__name__)
        try:
            kw = args['kw']
            del args['kw']
        except KeyError:
            kw = {}
        if not is_Dict(kw):
            raise TypeError("decl['kw'] must be a dictionary, %r is not " \
                            "allowed" % type(kw).__name__)
        kw.update(args)
        self.__xxx_args[VAR] = kw

    #========================================================================
    def _set_opt_decl(self, decl):
        #--------------------------------------------------------------------
        """Set parameters for later creation of the related `SCons command-line
        option`_.

        :Parameters:
            decl : tuple | list | dict
                declaration parameters used later when creating the related
                `SCons command-line option`_; if it is a tuple or list, it
                should have the form::

                        (names, args) or [names, args]

                where ``names`` is a string or tuple of option names (e.g.
                ``"-f --file"`` or ``('-f', '--file')``) and ``args`` is a
                dictionary defining the remaining `option attributes`_; the
                entire `decl` may be for example::

                    ( ('-f','--file-name'),
                      { 'action'         : "store",
                        'dest'           : "file_name" } )

                if `decl` is a dictionary, it should have following form
                (keys are important, values are just examples)::

                    { 'names'          : ("-f", "--file-name")
                      'action'         : "store",
                      'type'           : "string",
                      'dest'           : "file_name", ... }

                the parameters enclosed in ``decl`` dictionary are later
                passed verbatim to `SCons.Script.Main.AddOption()`_.
                Note, that we require the ``dest`` parameter.

        .. _SCons.Script.Main.AddOption(): http://www.scons.org/doc/latest/HTML/scons-api/SCons.Script.Main-module.html#AddOption
        .. _SCons command-line option: http://www.scons.org/doc/HTML/scons-user.html#sect-command-line-options
        .. _option attributes: http://docs.python.org/2/library/optparse.html#option-attributes
        """
        #--------------------------------------------------------------------
        from SCons.Util import is_String, is_Dict, is_Tuple, is_List
        if is_Tuple(decl) or is_List(decl):
            try:
                if is_String(decl[0]):
                    names = tuple(decl[0].split())
                elif is_Tuple(decl[0]):
                    names = decl[0]
                else:
                    raise TypeError("decl[0] must be a string or tuple, %r "\
                                    "is not allowed" % type(decl[0]).__name__)
            except IndexError:
                raise ValueError("'decl' must not be empty, got %r" % decl)
            try:
                kw  = decl[1]
            except IndexError:
                kw = {}
        elif is_Dict(decl):
            names = decl['names']
            try:
                kw = decl['kw']
            except KeyError:
                kw = {}
        else:
            raise TypeError("'decl' must be a tuple list or dictionary, %r " \
                            "is not allowed" % type(decl).__name__)
        if 'dest' not in kw:
            raise ValueError("'dest' parameter is missing")
        self.__xxx_args[OPT] = (names, kw)

    #========================================================================
    def has_xxx_decl(self, xxx):
        #--------------------------------------------------------------------
        """Test if declaration of corresponding `xxx` variable was provided,
        where `xxx` is one of `ENV`, `VAR` or `OPT`.

        :Parameters:
            xxx : int
                one of `ENV`, `VAR` or `OPT`
        :Returns:
            ``True`` if the declaration exists, or ``False`` otherwise.
        """
        #--------------------------------------------------------------------
        return self.__xxx_args[xxx] is not None

    #========================================================================
    def get_xxx_key(self, xxx):
        #--------------------------------------------------------------------
        """Get the declaration parameters for the related `xxx` variable, where
        `xxx` is one of `ENV`, `VAR` or `OPT`.

        :Parameters:
            xxx : int
                one of `ENV`, `VAR` or `OPT`
        :Returns:
            ``decl`` parameters stored by last call `set_xxx_decl(xxx,decl)`.
        """
        #--------------------------------------------------------------------
        if xxx == ENV:     return self.__xxx_args[ENV].keys()[0]
        elif xxx == VAR:   return self.__xxx_args[VAR]['key']
        elif xxx == OPT:   return self.__xxx_args[OPT][1]['dest']
        else:               raise IndexError("index out of range")

    #========================================================================
    def _set_xxx_key(self, xxx, key):
        #--------------------------------------------------------------------
        """Define the identifying key of corresponding `xxx` variable, where
        `xxx` is one of `ENV`, `VAR` or `OPT`.

        **Warning**
            This function should not be used by users. To change the key of
            corresponding `xxx` variable, use `_GVarDecls.set_xxx_key()`.

        :Parameters:
            xxx : int
                one of `ENV`, `VAR` or `OPT`
            key : string
                new key for the corresponding variable.
        """
        #--------------------------------------------------------------------
        if xxx == ENV:
            old_key = self.get_env_key()
            self.__xxx_args[ENV] = { key : self.__xxx_args[ENV][old_key] }
        elif xxx == VAR:
            self.__xxx_args[VAR]['key'] = key
        elif xxx == OPT:
            self.__xxx_args[OPT][1]['dest'] = key
        else:
            raise IndexError("index out of range")

    def get_xxx_default(self, xxx):
        #--------------------------------------------------------------------
        """Get the default value of corresponding `xxx` variable, where `xxx`
        is one of `ENV`, `VAR`, `OPT`.

        :Parameters:
            xxx : int
                one of `ENV`, `VAR` or `OPT`
        """
        #--------------------------------------------------------------------
        if xxx == ENV:
            return self.__xxx_args[ENV].values()[0]
        elif xxx == VAR:
            args = self.__xxx_args[VAR]
            try:             return args['default']
            except KeyError: return None
        elif xxx == OPT:
            args = self.__xxx_args[OPT]
            kw = args[1]
            try: return kw['default']
            except KeyError: return None
        else:
            raise IndexError("index out of range")

    #========================================================================
    def set_xxx_default(self, xxx, default):
        #--------------------------------------------------------------------
        """Define the default value of corresponding `xxx` variable, where
        `xxx` is one of `ENV`, `VAR`, `OPT`.

        :Parameters:
            xxx : int
                one of `ENV`, `VAR` or `OPT`
            default
                the new default value
        """
        #--------------------------------------------------------------------
        if xxx == ENV:
            self.__xxx_args[ENV] = { self.get_xxx_key(xxx) : default }
        elif xxx == VAR:
            self.__xxx_args[VAR]['default'] = default
        elif xxx == OPT:
            self.__xxx_args[OPT][1]['default'] = default
        else:
            raise IndexError("index out of range")

    #========================================================================
    def _add_to_xxx(self, xxx, *args,**kw):
        #--------------------------------------------------------------------
        """Add new corresponding `xxx` variable, where `xxx` is one of `ENV`,
        `VAR` or `OPT`; use declaration stored in this `_GVarDecl` object.

        **Examples**:

            - ``decl._add_to_xxx(ENV,env)`` creates new construction variable
              in `SCons environment`_ ``env``,
            - ``decl._add_to_xxx(VAR,vars)`` creates new command-line variable
              in `SCons variables`_ ``vars``
            - ``decl._add_to_xxx(OPT)`` creates a corresponding SCons
              `command-line option`_.

        :Parameters:
            xxx : int
                one of `ENV`, `VAR` or `OPT`
            args, kw
                additional arguments and keywords, depend on `xxx`:

                - if ``xxx == ENV``, then ``env=args[0]`` is assumed to be
                  a `SCons environment`_ to create construction variable for,
                - if ``xxx == VAR`, then ``vars=args[0]`` is assumed to be
                  a SCons `Variables`_ object, ``*args[1:]`` are used as
                  positional arguments to `vars.Add()`_ and ``**kw`` are
                  passed to `vars.Add()`_ as additional keywords,
                - if ``xxx == OPT``, the arguments and keywords are not used.

        .. _SCons environment:  http://www.scons.org/doc/HTML/scons-user.html#chap-environments
        .. _SCons variables: http://www.scons.org/doc/HTML/scons-user.html#sect-command-line-variables
        .. _Variables: http://www.scons.org/doc/latest/HTML/scons-api/SCons.Variables.Variables-class.html
        .. _vars.Add(): http://www.scons.org/doc/latest/HTML/scons-api/SCons.Variables.Variables-class.html#Add
        .. _command-line option: http://www.scons.org/doc/HTML/scons-user.html#sect-command-line-options
        """
        #--------------------------------------------------------------------
        from SCons.Script.Main import AddOption
        if xxx == ENV:
            if self.__xxx_args[ENV].values()[0] is not _dont_create:
                env = args[0]
                env.SetDefault(**self.__xxx_args[ENV])
        elif xxx == VAR:
            variables = args[0]
            kw2 = self.__xxx_args[VAR].copy()
            kw2.update(kw)
            return variables.Add(*args[1:],**kw2)
        elif xxx == OPT:
            AddOption(*self.__xxx_args[OPT][0], **self.__xxx_args[OPT][1])
        else:
            raise IndexError("index out of range")

    #========================================================================
    def _safe_add_to_xxx(self, xxx, *args):
        #--------------------------------------------------------------------
        """Same as `_add_to_xxx()`, but does not raise exceptions when the
        corresponding `xxx` variable is not declared in this `_GVarDecl`
        object.

        :Parameters:
            xxx : int
                one of `ENV`, `VAR` or `OPT`

        :Returns:
            returns ``True`` is new variable has been created or ``False`` if
            there is no declaration for corresponding `xxx` variable in this
            object.
        """
        #--------------------------------------------------------------------
        if self.has_xxx_decl(xxx):
            self._add_to_xxx(xxx, *args)
            return True
        else:
            return False

#############################################################################
def GVarDecl(*args, **kw):
    #------------------------------------------------------------------------
    """Convert input arguments to `_GVarDecl` instance.

   :Returns:
        - if ``args[0]`` is an instance of `_GVarDecl`, then returns
          ``args[0]`` unaltered,
        - otherwise returns result of `_GVarDecl(*args,**kw)`
    """
    #------------------------------------------------------------------------
    if len(args) > 0 and isinstance(args[0], _GVarDecl):
        return args[0]
    else:
        return _GVarDecl(*args, **kw)

#############################################################################
def GVarDeclU(env_key=None, var_key=None, opt_key=None, default=None,
              help=None, validator=None, converter=None, option=None,
              type=None, opt_default=None, metavar=None, nargs=None,
              choices=None, action=None, const=None, callback=None,
              callback_args=None, callback_kwargs=None):
    #------------------------------------------------------------------------
    """Convert unified set of arguments to `_GVarDecl` instance.

    This function accepts minimal set of parameters to declare consistently a
    ``GVar`` variable and its corresponding `ENV`, `VAR` and `OPT`
    counterparts.  If the first argument named `env_key` is an instance of
    `_GVarDecl`, then it is returned unaltered. Otherwise the arguments are
    mapped onto following attributes of corresponding `ENV`, `VAR` and `OPT`
    variables/options::

        ARG                 ENV         VAR         OPT
        ----------------+-----------------------------------------
        env_key         |   key         -           -
        var_key         |   -           key         -
        opt_key         |   -           -           dest
        default         |   default     default     -
        help            |   -           help        help
        validator       |   -           validator   -
        converter       |   -           converter   -
        option          |   -           -           option strings
        type            |   -           -           type
        opt_default     |   -           -           default
        metavar         |   -           -           metavar
        nargs           |   -           -           nargs
        choices         |   -           -           choices
        action          |   -           -           action
        const           |   -           -           const
        callback        |   -           -           callback
        callback_args   |   -           -           callback_args
        callback_kwargs |   -           -           callback_kwargs
        ----------------+------------------------------------------

    :Parameters:
        env_key : `_GVarDecl` | string | None
            if an instance of `_GVarDecl`, then this object is returned to the
            caller, key used to identify corresponding construction variable
            (`ENV`); if ``None`` the ``GVar`` variable  has no corresponding
            construction variable,
        var_key : string | None
            key used to identify corresponding command-line variable (`VAR`);
            if ``None``, the ``GVar`` variable  has no corresponding
            command-line variable,
        opt_key : string | None
            key used to identify corresponding command-line option (`OPT`);
            if ``None`` the ``GVar`` variable  has no corresponding
            command-line option,
        default
            default value used to initialize corresponding construction
            variable (`ENV`) and command-line variable (`VAR`);
            note that there is separate `opt_default` argument for command-line
            option,
        help : string | None
            message used to initialize help in corresponding command-line
            variable (`VAR`) and command-line option (`OPT`),
        validator
            same as for `SCons.Variables.Variables.Add()`_,
        converter
            same sd for `SCons.Variables.Variables.Add()`_,
        option
            option string, e.g. ``"--option"`` used for corresponding
            command-line option,
        type
            same as `type` in `optparse option attributes`_,
        opt_default
            same as `default` in `optparse option attributes`_,
        metavar
            same as `metavar` in `optparse option attributes`_,
        nargs
            same as `nargs` in `optparse option attributes`_,
        choices
            same as `choices` in `optparse option attributes`_,
        action
            same as `action` in `optparse option attributes`_,
        const
            same as `const` in `optparse option attributes`_,
        callback
            same as `callback` in `optparse option attributes`_,
        callback_args
            same as `callback_args` in `optparse option attributes`_,
        callback_kwargs
            same as `callback_kwargs` in `optparse option attributes`_,

    :Returns:
        - if `env_key` is present and it is an instance of `_GVarDecl`, then it
          is returned unaltered,
        - otherwise returns new `_GVarDecl` object initialized according to
          rules given above.

    .. _SCons.Variables.Variables.Add(): http://www.scons.org/doc/latest/HTML/scons-api/SCons.Variables.Variables-class.html#Add
    .. _optparse option attributes: http://docs.python.org/2/library/optparse.html#option-attributes
    """
    #------------------------------------------------------------------------
    if isinstance(env_key, _GVarDecl):
        return env_key
    else:
        # --- ENV ---
        if env_key is not None:
            env_decl = { env_key : default }
        else:
            env_decl = None
        # --- VAR ---
        if var_key is not None:
            items = [ (var_key, 'key'), (default, 'default'), (help, 'help'),
                      (validator, 'validator'), (converter, 'converter') ]
            var_decl = { k : v for (v,k) in items if v is not None }
        else:
            var_decl = None
        # --- OPT ---
        if opt_key and option is not None:
            items = [   (opt_key, 'dest'), (opt_default, 'default'),
                        (help, 'help'), (type, 'type'), (metavar, 'metavar'),
                        (nargs, 'nargs'), (choices, 'choices'),
                        (action, 'action'), (const, 'const'),
                        (callback, 'callback'),
                        (callback_args, 'callback_args'),
                        (callback_kwargs, 'callback_kwargs') ]
            opt_decl = (option, { k : v for (v,k) in items if v is not None })
        else:
            opt_decl = None
        return _GVarDecl(env_decl, var_decl, opt_decl)

#############################################################################
class _GVarDecls(dict):
    #========================================================================
    """Dictionary-like object to hold declarations of ``GVar`` variables.

    The `_GVarDecls` object is a subclass of ``dict`` with keys being strings
    identifying declared ``GVar`` variables and values being instances of
    `_GVarDecl` objects. The `_GVarDecls` dictionary also maintains internally
    *supplementary dictionaries* used to map names of registered variables
    between four namespaces: `ENV` (construction variables in SCons
    environment), `VAR` (command-line variables ``variable=value``), `OPT`
    (command-line options ``--option=value``) and ``GVar`` (the keys used to
    identify the ``GVar`` variables declared within `_GVarDecls` dictionary).

    The usage of `_GVarDecls` may be split into three stages:

        - declaring ``GVar`` variables; this may be done during object
          creation, see `__init__()`; further declarations may be added or
          existing ones may be modified via dictionary interface, see
          `__setitem__()`, `update()` and others,
        - committing declared variables, see `commit()`; after commit, the
          contents of `_GVarDecls` is frozen and any attempts to modifications
          end-up with a `RuntimeError` exception being raised,
        - creating related construction variables (``env["VARIABLE"]=VALUE``),
          command-line variables (``variable=value``) and command-line options
          (``--option=value``) according to committed `_GVarDecls`
          declarations, see `add_to()`; this may be performed by `commit()` as
          well.

    After that, an instance of `_GVars` should be created from `_GVarDecls` to
    keep track of created ``GVar`` variables (and corresponding construction
    variables, command-line variables and command-line options). The dictionary
    `_GVarDecls` may be then disposed.

    **Note**:

        In several places we use ``xxx`` as placeholder for one of the ``ENV``,
        ``VAR`` or ``OPT`` constants which represent selection of
        "corresponding Environment construction variable", "corresponding SCons
        command line variable" or "corresponding SCons command line option"
        respectively.  So, for example the call
        ``decls.set_xxx_key(ENV,"foo","ENV_FOO")`` defines the name
        ``"ENV_FOO"`` to be used for construction variable in SCons environment
        (``ENV``) that will correspond to our ``GVar`` variable named ``foo``.
    """
    #========================================================================



    #========================================================================
    def __init__(self, *args, **kw):
        #--------------------------------------------------------------------
        """Constructor for `_GVarDecls`.

        ``__init__()`` initializes an empty `_GVarDecls` dictionary,

        ``__init__(mapping)`` initializes `_GVarDecls` dictionary from a
        mapping object's ``(key,value)`` pairs, each ``value`` must be
        instance of `_GVarDecl`,

        ``__init__(iterable)`` initializes the `_GVarDecls` dictionary as if
        via ``d = { }`` followed by ``for k, v in iterable: d[k] = v``.
        Each value ``v`` from ``iterable`` must be an instance of `_GVarDecl`,

        ``__init__(**kw)`` initializes the `_GVarDecls` dictionary with
        ``name=value`` pairs in the keyword argument list ``**kw``, each
        ``value`` must be an instance of `_GVarDecl`,
        """
        #--------------------------------------------------------------------
        self.__committed = False
        self.__validate_values(*args,**kw)
        super(_GVarDecls, self).__init__(*args,**kw)
        self.__update_supp_dicts()

    #========================================================================
    def __reset_supp_dicts(self):
        """Reset supplementary dictionaries to empty state"""
        self.__rename = [{} for n in range(0,ALL)]
        self.__irename = [{} for n in range(0,ALL)]
        self.__resubst = [{} for n in range(0,ALL)]
        self.__iresubst = [{} for n in range(0,ALL)]

    #========================================================================
    def __update_supp_dicts(self):
        """Update supplementary dictionaries to be in sync with the
        declarations contained in main dictionary"""
        self.__reset_supp_dicts()
        for x in self.iteritems(): self.__append_decl_to_supp_dicts(*x)

    #========================================================================
    def __replace_xxx_key_in_supp_dicts(self, xxx, key, xxx_key):
        #--------------------------------------------------------------------
        """Replace in the supplementary dicts the key identifying corresponding
        `xxx` variable (where `xxx` is one of `ENV`, `VAR` or `OPT`).

        If the corresponding `xxx` variable identified by ``xxx_key`` already
        exists in the supplementary dictionaries, the supplementary
        dictionaries are left unaltered.

        :Parameters:
            xxx : int
                selector of the corresponding variable being renamed; one of
                `ENV`, `VAR` or `OPT`,
            key : string
                the key identifying ``GVar`` variable declared within this
                `_GVarDecls` dictionary, which subject to modification,
            xxx_key : string
                new name for the corresponding `xxx` variable.
        """
        #--------------------------------------------------------------------
        try: old_key = self.__rename[xxx][key]
        except KeyError: old_key = _notfound
        if xxx_key != old_key:
            self.__append_xxx_key_to_supp_dicts(xxx, key, xxx_key)
            try: del self.__irename[xxx][old_key]
            except KeyError: pass

    #========================================================================
    def __append_xxx_key_to_supp_dicts(self, xxx, key, xxx_key):
        #--------------------------------------------------------------------
        """Add to supplementary dictionaries the new `xxx` variable
        corresponding to ``GVar`` identified by `key`.

        If the corresponding `xxx` variable identified by ``xxx_key`` already
        exists in the supplementary dictionaries, a ``RuntimeError`` is raised.

        :Parameters:
            xxx : int
                selector of the corresponding variable being renamed; one of
                `ENV`, `VAR` or `OPT`,
            key : string
                the key identifying ``GVar`` variable within this `_GVarDecls`
                dictionary, which subject to modification,
            xxx_key : string
                new name for the corresponding `xxx` variable.
        """
        #--------------------------------------------------------------------
        if xxx_key in self.__irename[xxx]:
            raise RuntimeError("variable %r is already declared" % xxx_key)
        self.__rename[xxx][key] = xxx_key
        self.__irename[xxx][xxx_key] = key

    #========================================================================
    def __append_decl_to_supp_dicts(self, key, decl):
        for xxx in range(0,ALL):
            if decl.has_xxx_decl(xxx):
                xxx_key = decl.get_xxx_key(xxx)
                self.__append_xxx_key_to_supp_dicts(xxx, key, xxx_key)
        return decl

    #========================================================================
    def __del_from_supp_dicts(self, key):
        for xxx in range(0,ALL):
            if key in self.__rename[xxx]:
                xxx_key = self.__rename[xxx][key]
                del self.__rename[xxx][key]
                del self.__irename[xxx][xxx_key]

    #========================================================================
    @staticmethod
    def __validate_values(initializer=_missing,**kw):
        if initializer is not _missing:
            try: keys = initializer.keys()
            except AttributeError:
                for (k,v) in iter(initializer): _GVarDecls.__validate_value(v)
            else:
                for k in keys: _GVarDecls.__validate_value(initializer[k])
        for k in kw: _GVarDecls.__validate_value(kw[k])

    #========================================================================
    @staticmethod
    def __validate_value(value):
        if not isinstance(value, _GVarDecl):
            raise TypeError("value must be instance of _GVarDecl, %r is not "\
                            "allowed"  % type(value).__name__)
    #========================================================================
    def setdefault(self, key, value = _missing):
        if value is _missing:
            return super(_GVarDecls,self).setdefault(key)
        else:
            self.__ensure_not_committed()
            value = self.__validate_value(value)
            return super(_GVarDecls,self).setdefault(key, value)

    #========================================================================
    def update(self, *args, **kw):
        self.__ensure_not_committed()
        _GVarDecls.__validate_values(*args,**kw)
        super(_GVarDecls,self).update(*args,**kw)
        self.__update_supp_dicts()

    #========================================================================
    def clear(self, *args, **kw):
        self.__ensure_not_committed()
        super(_GVarDecls,self).clear(*args,**kw)
        self.__update_supp_dicts()

    #========================================================================
    def pop(self, key, *args, **kw):
        self.__ensure_not_committed()
        self.__del_from_supp_dicts(key)
        return super(_GVarDecls,self).pop(key,*args,**kw)

    #========================================================================
    def popitem(self, *args, **kw):
        self.__ensure_not_committed()
        (k,v) = super(_GVarDecls,self).popitem(*args,**kw)
        self.__del_from_supp_dicts(k)
        return (k,v)

    #========================================================================
    def copy(self):
        print "Kalabanka!"
        return _GVarDecls(self)

    #========================================================================
    def __setitem__(self, key, value):
        self.__ensure_not_committed()
        value = self.__validate_value(value)
        self.__append_decl_to_supp_dicts(key, value)
        return super(_GVarDecls,self).__setitem__(key, decl)

    #========================================================================
    def __delitem__(self, key):
        self.__ensure_not_committed()
        self.__del_from_supp_ducats(key)
        return super(_GVarDecls,self).__delitem__(key)

    #========================================================================
    def get_xxx_rename_dict(self, xxx):
        #--------------------------------------------------------------------
        """Get the dictionary mapping variable names from ``GVar`` namespace to
        `xxx` (where `xxx` is one of `ENV`, `VAR` or `OPT`).

        :Parameters:
            xxx : int
                selector of the corresponding namespace; one of `ENV`, `VAR` or
                `OPT`,
        :Returns:
            dictionary with items ``(key, xxx_key)``, where ``key`` is the key
            from ``GVar`` namespace and ``xxx_key`` is variable name in the
            `xxx` (`ENV`, `VAR` or `OPT`) namespace
        """
        #--------------------------------------------------------------------
        return self.__rename[xxx].copy()

    #========================================================================
    def get_xxx_irename_dict(self, xxx):
        #--------------------------------------------------------------------
        """Get the dictionary mapping variable names from `xxx` namespace to
        ``GVar`` namespace (where `xxx` is one of `ENV`, `VAR` or `OPT`).

        :Parameters:
            xxx : int
                selector of the corresponding namespace; one of `ENV`, `VAR` or
                `OPT`,
        :Returns:
            dictionary with items ``(xxx_key, key)``, where ``key`` is the key
            from ``GVar`` namespace and ``xxx_key`` is variable name in the
            `xxx` (`ENV`, `VAR` or `OPT`) namespace

        """
        #--------------------------------------------------------------------
        return self.__irename[xxx].copy()

    #========================================================================
    def get_xxx_resubst_dict(self,xxx):
        #--------------------------------------------------------------------
        """Get the dictionary mapping variable names from ``GVar`` namespace to
        placeholders for variable values from `xxx` namespace (where `xxx` is
        one of `ENV`, `VAR` or `OPT`).

        **Note**:

            The declarations must be committed before this function may be
            called.

        :Parameters:
            xxx : int
                selector of the corresponding namespace; one of `ENV`, `VAR` or
                `OPT`,
        :Returns:
            dictionary with items ``(key, "${" + xxx_key + "}")``, where
            ``key`` is the key from ``GVar`` namespace and ``xxx_key`` is
            variable name in the `xxx` (`ENV`, `VAR` or `OPT`) namespace

        """
        #--------------------------------------------------------------------
        self.__ensure_committed()
        return self.__resubst[xxx].copy()

    #========================================================================
    def get_xxx_iresubst_dict(self, xxx):
        #--------------------------------------------------------------------
        """Get the dictionary mapping variable names from `xxx` namespace to
        placeholders for variable values from ``GVar`` namespace (where `xxx`
        is one of `ENV`, `VAR` or `OPT`).

        **Note**:

            The declarations must be committed before this function may be
            called.

        :Parameters:
            xxx : int
                selector of the corresponding namespace; one of `ENV`, `VAR` or
                `OPT`,
        :Returns:
            dictionary with items ``(xxx_key, "${" + key + "}")``, where
            ``key`` is the key from ``GVar`` namespace and ``xxx_key`` is
            variable name in the `xxx` (`ENV`, `VAR` or `OPT`) namespace

        """
        #--------------------------------------------------------------------
        self.__ensure_committed()
        return self.__iresubst[xxx].copy()

    #========================================================================
    def get_xxx_key(self, xxx, key):
        #--------------------------------------------------------------------
        """Get the key identifying corresponding `xxx` variable  (where `xxx`
        is one of `ENV`, `VAR` or `OPT`).

        If the corresponding `xxx` variable is not declared, the function
        raises an exception.

        :Parameters:
            xxx : int
                selector of the corresponding namespace; one of `ENV`, `VAR` or
                `OPT`,
            key : string
                key identifying an already declared ``GVar`` variable to which
                the queried `xxx` variable corresponds,

        :Returns:
            the key (name) identifying `xxx` variable corresponding to our
            ``GVar`` variable identified by `key`

        """
        #--------------------------------------------------------------------
        return self[key].get_xxx_key(xxx)

    #========================================================================
    def set_xxx_key(self, xxx, key, xxx_key):
        #--------------------------------------------------------------------
        """Change the key identifying a corresponding `xxx` variable (where
        `xxx` is one of `ENV`, `VAR` or `OPT`).

        If the corresponding `xxx` variable is not declared, the function
        raises an exception.

        :Parameters:
            xxx : int
                selector of the corresponding namespace; one of `ENV`, `VAR` or
                `OPT`,
            key : string
                key identifying an already declared ``GVar`` variable to which
                the queried `xxx` variable corresponds,

        :Returns:
            the key (name) identifying `xxx` variable corresponding to our
            ``GVar`` variable identified by `key`

        """
        #--------------------------------------------------------------------
        self.__ensure_not_committed()
        self[key]._set_xxx_key(xxx_key)
        self.__replace_xxx_key_in_supp_dicts(xxx, key, xxx_key)

    #========================================================================
    def _add_to_xxx(self, xxx, *args):
        """Invoke `_GVarDecl._add_to_xxx()` for each ``GVar`` variable declared
        in this dictionary."""
        for (k,v) in self.iteritems(): v._add_to_xxx(xxx,*args)

    #========================================================================
    def _safe_add_to_xxx(self, xxx, *args):
        """Invoke `_GVarDecl._safe_add_to_xxx()` for each ``GVar`` variable
        declared in this dictionary."""
        for (k,v) in self.iteritems(): v._safe_add_to_xxx(xxx, *args)

    #========================================================================
    def _build_resubst_dicts(self):
        """Build supplementary dictionaries used to rename placeholders in
        values (forward, from ``GVar`` namespace to ``xxx`` namespaces)"""
        for xxx in range(0,ALL):
            self.__resubst[xxx] = _build_resubst_dict(self.__rename[xxx])

    #========================================================================
    def _build_iresubst_dicts(self):
        """Build supplementary dictionaries used to rename placeholders in
        values (inverse, from ``xxx`` namespaces to ``GVar`` namespace)"""
        for xxx in range(0,ALL):
            self.__iresubst[xxx] = _build_iresubst_dict(self.__rename[xxx])

    #========================================================================
    def _resubst_decl_defaults(self, decl):
        """Rename placeholders found in the declarations of default values of
        ``xxx`` corresponding variables for the given declaration ``decl``.

        :Parameters:
            decl : _GVarDecl
                the ``GVar`` declaration to modify
        """
        for xxx in range(0,ALL):
            if decl.has_xxx_decl(xxx):
                val = _resubst(decl.get_xxx_default(xxx), self.__resubst[xxx])
                decl.set_xxx_default(xxx,val)

    #========================================================================
    def __resubst_defaults(self):
        """Rename placeholders found in the declarations of default values of
        ``xxx`` corresponding variables for all declared ``GVar`` variables.
        """
        for (k,v) in self.iteritems():
            self._resubst_decl_defaults(v)

    #========================================================================
    def __ensure_not_committed(self):
        """Raise exception if the object was already committed"""
        if self.__committed:
            raise RuntimeError("declarations are already committed, can't " \
                               "be modified")
    #========================================================================
    def __ensure_committed(self):
        """Raise exception if the object was not jet committed"""
        if not self.__committed:
            raise RuntimeError("declarations must be committed before " \
                               "performing this operation")

    #========================================================================
    def commit(self, *args):
        #--------------------------------------------------------------------
        """Commit the declaration and optionally add appropriate variables to a
        SCons construction environment, command-line variables and command-line
        options.

        The function finishes declaration stage, freezes the dictionary and
        makes call to `add_to()` with ``*args`` passed verbatim to it.

        :Parameters:
            args
                positional arguments passed verbatim do `add_to()`.
        """
        #--------------------------------------------------------------------
        if not self.__committed:
            self._build_resubst_dicts()
            self._build_iresubst_dicts()
            self.__resubst_defaults()
            self.__committed = True
            self.add_to(*args)

    #========================================================================
    def add_to(self, *args):
        #--------------------------------------------------------------------
        """Create and initialize the corresponding ``xxx`` variables (where
        ``xxx`` is one of `ENV`, `VAR` or `OPT`).

        This function calls `_safe_add_to_xxx()` for each ``xxx`` from ``(ENV,
        VAR, OPT)``.

        :Parameters:
            args
                positional arguments interpreted in order as ``env``,
                ``variables``, ``options`` where:

                    - ``env`` is a SCons environment object to be updated with
                      ``GVar`` variables defined here and their defaults,
                    - ``variables`` is a SCons Variables object for which new
                      command-line variables will be defined,
                    - ``options`` is a Boolean deciding whether the
                      corresponding command-line options should be created or
                      not (default ``False`` means 'do not create').

                All the arguments are optional. ``None`` may be used to
                represent missing argument and skip the creation of certain
                variables/options.
        """
        #--------------------------------------------------------------------
        self.__ensure_committed()
        for xxx in range(0,min(len(args),ALL)):
            if args[xxx]: self._safe_add_to_xxx(xxx, args[xxx])

    #========================================================================
    def Commit(self, env=None, variables=None, options=False, gvars=True,
              *args):
        """User interface to `commit()`, optionally returns newly created
        `_GVars` object.

        :Parameters:
            env
                a SCons environment object to populate with default values of
                construction variables defined by ``GVar`` variables declared
                here,
            variables
                a `SCons.Variables.Variables`_ object to be populated with new
                variables defined by ``GVar`` variables declared here,
            options : Boolean
                if ``True``, the command-line options declared by ``GVar``
                variables are created,
            gvars
                if ``True`` (default) create and return a `_GVars` object for
                further operation on variables and their values,

        :Returns:
            if `gvars` is ``True``, returns newly created `_GVars` object,
            otherwise returns ``None``.

        .. _SCons.Variables.Variables: http://www.scons.org/doc/latest/HTML/scons-api/SCons.Variables.Variables-class.html
        """
        self.commit(env, variables, options, *args)
        if gvars:   return _GVars(self)
        else:       return None

#############################################################################
def __dict_converted(convert, initializer=_missing, **kw):
    """Generic algorithm for dict initialization while converting the values
    provided within initializers"""
    if initializer is _missing:
        decls = {}
    else:
        try: keys = initializer.keys()
        except AttributeError:
            decls = { k : convert(v) for (k,v) in iter(initializer) }
        else:
            decls = { k : convert(initializer[k]) for k in keys }
    decls.update({ k : convert(kw[k]) for k in kw })
    return decls

#############################################################################
def GVarDecls(*args, **kw):
    """Create `_GVarDecls` dictionary with ``GVar`` variable declarations.

    The function supports several forms of invocation, see the section
    **Returns** to find systematic description. Here we give just a couple of
    examples.

    If the first positional argument is a mapping (a dictionary for example)
    then values from the dictionary are passed through `GVarDecl()` and the
    resultant dictionary is used as initializer to `GVarDecl`. You may for
    example pass a dictionary of the form ``{ 'foo' : (env, var, opt)}``,
    where ``env``, ``var`` and ``opt`` are parameters accepted by
    `_GVarDecl._set_env_decl()`, `_GVarDecl._set_var_decl()` and
    `_GVarDecl._set_opt_decl()` respectively.

    **Example**

    .. python::

        gdecls = {
           # GVar 'foo'
          'foo' : (   {'ENV_FOO' : 'default ENV_FOO'},                  # ENV
                      ('VAR_FOO', 'VAR_FOO help', ),                    # VAR
                      ('--foo', {'dest' : "opt_foo"})               ),  # OPT

           # GVar 'bar'
          'bar' : (   {'ENV_BAR' : None},                               # ENV
                      ('VAR_BAR', 'VAR_BAR help', 'default VAR_BAR'),   # VAR
                      ('--bar', {'dest':"opt_bar", "type":"string"}))   # OPT
        }
        gdecls = GVarDecls(gdecls)

    The first positional argument may be iterable as well, in which case it
    should yield tuples in form ``(key, value)``, where ``value`` is any value
    convertible to `_GVarDecl`.

    **Example**

    .. python::

        gdecls = [
           # GVar 'foo'
          'foo' , (   {'ENV_FOO' : 'default ENV_FOO'},                  # ENV
                      ('VAR_FOO', 'VAR_FOO help', ),                    # VAR
                      ('--foo', {'dest' : "opt_foo"})               ),  # OPT

           # GVar 'bar'
          'bar' , (   {'ENV_BAR' : None},                               # ENV
                      ('VAR_BAR', 'VAR_BAR help', 'default VAR_BAR'),   # VAR
                      ('--bar', {'dest':"opt_bar", "type":"string"}))   # OPT
        ]
        gdecls = GVarDecls(gdecls)

    You may also define variables via keyword arguments to `GVarDecls()`.

    **Example**

    .. python::

        gdecls = GVarDecls(
           # GVar 'foo'
           foo  = (   {'ENV_FOO' : 'ENV default FOO'},                  # ENV
                      ('FOO',         'FOO variable help', ),           # VAR
                      ('--foo',       {'dest' : "opt_foo"})         ),  # OPT

           # GVar 'bar'
           bar  = (   {'ENV_BAR' : None},                               # ENV
                      ('BAR', 'BAR variable help', 'VAR default BAR'),  # VAR
                      ('--bar', {'dest':"opt_bar", "type":"string"}))   # OPT
        )

    You may of course append keyword arguments to normal arguments to pass
    extra declarations.

    **Example**

    .. python::

        gdecls = GVarDecls(
           # GVar 'foo'
           [('foo',(   {'ENV_FOO' : 'ENV default FOO'},                 # ENV
                      ('FOO',         'FOO variable help', ),           # VAR
                      ('--foo',       {'dest' : "opt_foo"})         ))],# OPT
           # GVar 'geez'
           geez  = (   {'ENV_GEEZ' : None},                             # ENV
                      ('GEEZ', 'GEEZ variable help', 'VAR default GEEZ'),# VAR
                      ('--geez', {'dest':"opt_geez", "type":"string"})) # OPT
        )

    or

    **Example**

    .. python::

        gdecls = GVarDecls(
           # GVar 'bar'
           {'bar':(   {'ENV_BAR' : None},                               # ENV
                      ('BAR', 'BAR variable help', 'VAR default BAR'),  # VAR
                      ('--bar', {'dest':"opt_bar", "type":"string"}))}, # OPT
           # GVar 'geez'
           geez  = (   {'ENV_GEEZ' : None},                             # ENV
                      ('GEEZ', 'GEEZ variable help', 'VAR default GEEZ'),# VAR
                      ('--geez', {'dest':"opt_geez", "type":"string"})) # OPT
        )

    This function

    :Returns:

        - `GVarDecls()` returns an empty `_GVarDecls` dictionary ``{}``,
        - `GVarDecls(mapping)` returns `_GVarDecls` dictionary initialized
          with ``{k : GVarDecl(mapping[k]) for k in mapping.keys()}``
        - `GVarDecls(iterable)` returns `_GVarDecls` dictionary initialized
          with ``{k : GVarDecl(v) for (k,v) in iter(initializer)}``

        In any case, the keyword arguments ``**kw`` are appended to the
        initializer.

    """
    convert = lambda x : x if isinstance(x, _GVarDecl)  \
                           else GVarDecl(**x) if hasattr(x, 'keys') \
                           else GVarDecl(*tuple(x))
    return _GVarDecls(__dict_converted(convert, *args, **kw))

#############################################################################
def GVarDeclsU(*args, **kw):
    convert = lambda x : x if isinstance(x, _GVarDecl) \
                           else GVarDeclU(**x) if hasattr(x, 'keys') \
                           else GVarDeclU(*tuple(x))
    return _GVarDecls(__dict_converted(convert, *args, **kw))


# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
