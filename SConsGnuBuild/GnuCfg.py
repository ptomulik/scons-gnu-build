"""`SConsGnuBuild.GnuCfg`

Provides functions to implement replacement of GNU ./configure script

TODO: Write docs for XXX
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
def init_gnucfg_aliases(env, configure_alias=None, distclean_alias=None):
    from SConsGnuBuild.Common import get_configure_alias
    from SConsGnuBuild.Common import get_distclean_alias
    """Initialize certain Alias'es that are altered by GnuCfg module
    
    :Parameters:
        configure_alias : str
            name of the alias used to run configuration process (a kind of
            ``./configure``)
        distclean_alias : str
            name of the alias used to perform a kind of ``make distclean``
    """
    env.Alias(get_configure_alias(env, configure_alias))
    env.Clean(get_distclean_alias(env, distclean_alias))
             
#############################################################################
def gnucfg_distclean(env, config_cache=None, distclean_alias=None):
    """Run GnuCfg-related tasks that shall be done during `distclean`.
    
    :Parameters:
        config_cache : SCons.Node.FS.File | str
            file node or file name of the GNU config cache
    """
    from SConsGnuBuild.Common import get_distclean_alias
    from SConsGnuBuild.Common import get_config_cache
    return env.Clean(get_distclean_alias(env,distclean_alias), 
                     env.arg2nodes(get_config_cache(env,config_cache)))

#############################################################################
def gnucfg_configure(env, config_cache=None, configure_alias=None):
    """Run GnuCfg-related tasks that shall be done during `configure`.
    
    :Parameters:
        config_cache : SCons.Node.FS.File | str
            file node or file name of the GNU config cache
    """
    from SConsGnuBuild.Common import get_configure_alias
    from SConsGnuBuild.Common import get_config_cache
    config_cache = env.arg2nodes(get_config_cache(env,config_cache))

#############################################################################
def gnucfg_init_dirvars(env, only=None, exclude=None, env_prefix=None,
                        env_suffix=None, env_transform_name=None,
                        opt_prefix=None, opt_suffix=None,
                        opt_transform_name=None):
    from SConsGnuBuild.GnuDirVars import AddDirVarsToSConsEnvironment, \
                                         AddDirVarsToSConsOptions
    ar1 = { 'only'           : only,
            'exclude'        : exclude, 
            'prefix'         : env_prefix,
            'suffix'         : env_suffix,
            'transform_name' : env_transform_name } 
    ar2 = { 'only'           : only, 
            'exclude'        : exclude, 
            'prefix'         : opt_prefix, 
            'suffix'         : opt_suffix,
            'transform_name' : opt_transform_name } 
    kw1 = dict( [ item for item in ar1.iteritems() if item[1] is not None] )
    kw2 = dict( [ item for item in ar2.iteritems() if item[1] is not None] )
    AddDirVarsToSConsEnvironment(env,**kw1)
    return AddDirVarsToSConsOptions(**kw2)


#############################################################################
def gnucfg_use_dirvar_options(env, only=None, exclude=None, env_prefix='',
                               env_suffix='', env_transform_name=lambda x : x,
                               opt_prefix='', opt_suffix='',
                               opt_transform_name=lambda x : x):
    from SConsGnuBuild.GnuDirVars import StandardDirVarNames
    from SCons.Script.Main import GetOption
    def _use_option(name):
        env_name = env_transform_name(env_prefix + name + env_suffix)
        opt_name = opt_transform_name(opt_prefix + name + opt_suffix)
        opt_val = GetOption(opt_name)
        env.Append(env_name = opt_val)
        return (env_name, opt_val)
    return dict(map(_use_option, StandardDirVarNames(only=only,exclude=exclude)))
    
#############################################################################
def InitGnuCfgAliases(env,**kw):
    args = [ 'configure_alias', 'distclean_alias' ]
    kw2 = {key : kw[key] for key in args if key in kw }
    return init_gnucfg_aliases(env,**kw2)

#############################################################################
def GnuCfgConfigure(env,**kw):
    args = [ 'config_cache', 'config_alias' ]
    kw2 = {key : kw[key] for key in args if key in kw }
    return gnucfg_configure(env,**kw2)

#############################################################################
def GnuCfgDistclean(env,**kw):
    args = [ 'config_cache', 'distclean_alias' ]
    kw2 = {key : kw[key] for key in args if key in kw }
    return gnucfg_distclean(env,**kw2)

#def GnuCfgOptions(env,)

# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
