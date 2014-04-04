"""`SConsGnu.Common`

Functions and objects used by more than one modules.
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



#############################################################################
class __null(object) : pass
#############################################################################

###############################################################################
##def map_named_tuples(callback, tuples, only=None, exclude=None):
##    """Map a list of tuples via callback optionally transforming tuple name.
##
##    For each ``t`` in `tuples`, the ``t[0]`` must be a string and we call
##    ``t[0]`` the name of the tuple. The tuple ``t`` is then called ``named
##    tuple``. The function maps all the `tuples` through `callback`. Each
##    tuple name is optionaly prefixed with `prefix`, suffixed with `suffix` and
##    then transformed by `transform` function before passing the tuple to
##    `callback`.
##
##    **Example**:
##
##        >>> from SConsGnu.Common import map_named_tuples
##        >>> tuples = [ ('foo', 1), ('bar', 2), ('geez', 3) ]
##        >>> map_named_tuples(lambda *x : x, tuples, only = ('foo', 'geez'), prefix='PFX_')
##        [('PFX_foo', 1), ('PFX_geez', 3)]
##
##    :Parameters:
##        callback : callable
##            function of type ``callback(name, *args)``, where
##
##                - ``name``: is the name of variable being processed,
##                - ``*args``: are the remaining tuple elements
##
##        tuples : list
##            list of named tuples to be mapped,
##        only : sequence | None
##            tuple names of the tuples to be mapped, others are skipped,
##        exclude : sequence | None
##            tuple names of the tuples to exclude from mapping,
##    :Returns:
##        returns result of mapping
##    """
##    if only is not None:
##        tuples = filter(lambda t : t[0] in only, tuples)
##    if exclude is not None:
##        tuples = filter(lambda t : t[0] not in exclude, tuples)
##    return map(lambda t : callback(*t), tuples)
##
###############################################################################
##def find_orig_name(orig_names, name, only=None, exclude=None, prefix=None,
##                   suffix=None, transform=None):
##    if only is not None:
##        orig_names = filter(lambda x : x in only, orig_names)
##    if exclude is not None:
##        orig_names = filter(lambda x : x not in exclude, orig_names)
##    # We'll end-up with dictionary of type { name1 : orig_name1, ... }
##    ndict = dict(zip(orig_names, orig_names))
##    if prefix is not None:
##        ndict = { prefix+key : ndict[key] for key in ndict.keys }
##    if suffix is not None:
##        orig_names = map(lambda x : (x + suffix,) + x, orig_names)
##    if callable(transform):
##        orig_names = map(lambda x : (transform(x),) +  x, orig_names)

#############################################################################
__std_man_sections = map(lambda x : str(x), range(0,10)) + ['n', 'l']
#############################################################################
def standard_man_sections():
    """Return list of standard man sections (manpage sections)

    **Description**

    The function returns a list of man page sections as defined in the section
    `Man pages`_ of automake documentation.

    .. _Man pages: http://www.gnu.org/software/automake/manual/automake.html#Man-Pages
    """
    return __std_man_sections

#############################################################################
def invert_dict(_dict):
    return dict(map(lambda (k,v) : (v,k), _dict.iteritems()))

#############################################################################
def __get_var(env, key, default, override=__null, *args):
    """Return `override` if given, or value env.subst("$key",*args) if defined
    or return `default` value othervise."""
    if override is not __null: return override
    if env.has_key(key): return env.subst('${%s}' % key, *args)
    return default

#############################################################################
def get_envvar_prefix(env, override=__null, *args):
    """Get the prefix prepended to new construction variables (e.g. to GNU
    directory variables when they are added to environment as construction
    variables)."""
    key = 'GNUBLD_ENVVAR_PREFIX'
    default = 'GNUBLD_'
    return __get_var(env, key, default, override, *args)

#############################################################################
def get_configure_alias(env, override=__null, *args):
    key = 'GNUBLD_CONFIGURE_ALIAS'
    default = 'configure'
    return __get_var(env, key, default, override, *args)

#############################################################################
def get_distclean_alias(env, override=__null, *args):
    key = 'GNUBLD_DISTCLEAN_ALIAS'
    default = 'distclean'
    return __get_var(env, key, default, override, *args)

#############################################################################
def get_config_cache(env, override=__null, *args):
    key = 'GNUBLD_CONFIG_CACHE'
    default = '.scons.config.cache'
    return __get_var(env, key, default, override, *args)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
