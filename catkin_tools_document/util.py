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
from typing import List
from typing import Union

from functools import lru_cache
import os
import yaml

from catkin_tools.common import mkdir_p
from catkin_tools.execution.events import ExecutionEvent


def output_dir_file(builder: str) -> str:
    return f"{builder}_output"


@lru_cache
def which(program):
    for path in os.environ["PATH"].split(os.pathsep):
        path = path.strip('"')
        executable = os.path.join(path, program)
        if os.path.isfile(executable):
            return executable


def unset_env(logger, event_queue, job_env: dict, keys: Union[List[str], None] = None) -> int:
    """
    FunctionStage functor that removes keys from the job_env.
    In case no keys are provided, the job_env is cleared.

    :param logger:
    :param event_queue:
    :param job_env: Job environment
    :param keys: Keys to remove from the job environment
    :return: return code
    """
    if keys is None:
        job_env.clear()
        return 0

    for index, key in enumerate(keys):
        try:
            job_env.pop(key)
        except KeyError:
            logger.err("Could not delete missing key '{}' from the job environment".format(key))
        finally:
            event_queue.put(ExecutionEvent(
                'STAGE_PROGRESS',
                job_id=logger.job_id,
                stage_label=logger.stage_label,
                percent=str(index/float(len(keys)))
            ))

    return 0


def write_file(logger, event_queue, contents: Any, dest_path: str, mode: str = 'w') -> int:
    """
    FunctionStage functor that writes the contents to a file.
    In case the file exists, the file is overwritten.

    :param logger:
    :param event_queue:
    :param contents: Contents to write
    :param dest_path: File to which the contents should be written
    :param mode: file mode (default: 'w')
    :return: return code
    """
    mkdir_p(os.path.dirname(dest_path))
    with open(dest_path, mode) as f:
        f.write(contents)

    return 0


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
