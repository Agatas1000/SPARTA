########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

# Built-in Imports

# Third-party Imports

# Cloudify imports
from cloudify import ctx
from cloudify.decorators import operation
from compiler import AccessPatternCompiler

@operation
def createmodel(outputfile, **kwargs):
    f = open(outputfile, "a")

    if 'behavior' in ctx._node._node.nodes[0].properties.keys():
        for key in ctx._node._node.nodes[0].properties['behavior']._value:
            behavior = ctx._node._node.nodes[0].properties['behavior']._value[key]
            f.write("# " + ctx._node._node.nodes[0].name + "\n")
            for c in AccessPatternCompiler().compile(behavior, ctx._node._node.nodes[0]):
                print(c)
                f.write(c + "\n")

    f.close()
