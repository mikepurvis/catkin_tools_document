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

from typing import Any

from functools import lru_cache
import os
import yaml

from catkin_tools.common import mkdir_p


@lru_cache
def which(program):
    for path in os.environ["PATH"].split(os.pathsep):
        path = path.strip('"')
        executable = os.path.join(path, program)
        if os.path.isfile(executable):
            return executable


def yaml_dump_file(logger, event_queue, contents: Any, dest_path: str, dumper=yaml.SafeDumper) -> int:
    """
    FunctionStage functor that dumps the contents of an object, which is accepted by yaml dumper, to a file.
    In case the file exists, the file is overwritten.

    :param logger:
    :param event_queue:
    :param contents: Object which is dumped to the yaml file.
    :param dest_path: File to which the contents should be written
    :param dumper: Yaml dumper to use (default: yaml.SafeDumper)
    :return: return code
    """
    mkdir_p(os.path.dirname(dest_path))
    with open(dest_path, 'w') as f:
        yaml.dump(contents, f, dumper)

    return 0
