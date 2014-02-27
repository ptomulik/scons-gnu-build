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

from SConsGnuBuild.GVars import GVarDecls
env = Environment()
Export(['env'])
VariantDir('build/doc', 'doc', duplicate = 0)
SConscript('build/doc/SConscript')

examples = {
  'ex1' : 'examples/GnuDirVars/ex1/SConscript',
  'ex2' : 'examples/GnuDirVars/ex2/SConscript',
  'ex3' : 'examples/GnuDirVars/ex3/SConscript',
  'ex4' : 'examples/AmUniform/ex4/SConscript',
  'ex5' : 'examples/AmUniform/ex5/SConscript'
}

# Run particular example
for tgt in examples.keys():
    env.AlwaysBuild(env.Alias(tgt))
    if tgt in COMMAND_LINE_TARGETS:
        env.SConscript(examples[tgt])

env.AlwaysBuild(env.Alias('unittest'))
if 'unit-test' in COMMAND_LINE_TARGETS:
    import sys
    python = env.Detect('python')
    if python:
        path = ':'.join(sys.path)
        #unittestflags = "-v"
        unittestflags = ""
        discoverflags = "-p '*Tests.py'"
        testcom = 'PYTHONPATH=%s %s -m unittest discover %s %s' \
                % (path, python, unittestflags, discoverflags)
        env.Execute(testcom, "Running unit tests")
