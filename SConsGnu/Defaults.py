"""`SConsGnu.Defaults`

Defaults for several other modules.
"""

#
# Copyright (c) 2014 by Pawel Tomulik
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


gvar_env_key_prefix     = 'GNUBLD_'
gvar_env_key_suffix     = ''
gvar_env_key_transform  = lambda x : gvar_env_key_prefix \
                        + x \
                        + gvar_env_key_suffix

gvar_var_key_prefix     = ''
gvar_var_key_suffix     = ''
gvar_var_key_transform  = lambda x : gvar_var_key_prefix \
                        + x \
                        + gvar_var_key_suffix

gvar_opt_key_prefix     = 'gnubld_'
gvar_opt_key_suffix     = ''
gvar_opt_key_transform  = lambda x : gvar_opt_key_prefix \
                        + x.lower() \
                        + gvar_opt_key_suffix

gvar_opt_prefix         = '--'
gvar_opt_name_prefix    = ''
gvar_opt_name_suffix    = ''
gvar_opt_name_transform = lambda x : gvar_opt_prefix \
                        + (gvar_opt_name_prefix \
                        + x.lower() \
                        + gvar_opt_name_suffix).replace('_','-')

gvar_declarations_var   = 'GVAR_DECLARATIONS'
# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
