# Copyright 2016 Clearpath Robotics Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os


_which_cache = {}

def which(program):
    global _which_cache
    if program not in _which_cache:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            executable = os.path.join(path, program)
            if os.path.exists(executable):
                _which_cache[program] = executable
                break

    return _which_cache[program]
