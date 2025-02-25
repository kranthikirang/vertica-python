# Copyright (c) 2018-2023 Open Text.
# Copyright (c) 2018 Uber Technologies, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Copyright (c) 2013-2017 Uber Technologies, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
CommandComplete message

The server prompt that indicates a command has completed. The command tag
string is the name of the command that was run.
"""

from __future__ import print_function, division, absolute_import

import re
import warnings

from struct import unpack

from ..message import BackendMessage


class CommandComplete(BackendMessage):
    message_id = b'C'

    def __init__(self, data):
        BackendMessage.__init__(self)
        data = unpack('{0}sx'.format(len(data) - 1), data)[0]
        try:
            self.command_tag = data.decode('utf-8')
        except Exception as e:
            # (workaround for #493) something wrong in the server, hide the problem for now
            warnings.warn("Hit a known server bug\n"
                    f"{'='*80}\n"
                    "We'd like to gather client-side information to help with the bug investigation.\n"
                    "Please leave a comment under https://github.com/vertica/vertica-python/issues/493"
                    " with the following info:\n"
                    f"{'-'*80}\n"
                    f"command tag length: {len(data)}\n"
                    f"command tag content: {data}\n"
                    f"{type(e).__name__}: {str(e)}\n"
                    "Server version: xxx\n"
                    "Query executed (if possible): xxx\n"
                    "The OS of each server node (if possible): xxx\n"
                    "The locale of each server node (if possible): xxx\n"
                    f"{'-'*80}\n"
                    f"We appreciate your help!\n"
                    f"{'='*80}\n"
                    )
            self.command_tag = 'x'

    def __str__(self):
        return 'CommandComplete: command_tag = "{}"'.format(self.command_tag)


BackendMessage.register(CommandComplete)
