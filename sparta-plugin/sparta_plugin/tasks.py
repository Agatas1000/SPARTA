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

@operation
def compile(outputfile, **kwargs):
    print('output: ' + outputfile) 
    print('Node: ' + ctx._node._node.nodes[0].name)
    ctx.logger.info('Finished running the Sparta validate operation on ' + ctx._node._node.nodes[0].name)
