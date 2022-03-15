# Copyright 2021 Matthijs van der Burgh
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy
import os.path
import sys
import yaml

from catkin_tools.execution.events import ExecutionEvent

from .util import output_dir_file


INTERSPHINX_GENERATORS = ['pydoctor', 'sphinx']


def generate_intersphinx_mapping(logger, event_queue, output_path, root_dir, doc_deps, docs_build_path, job_env):
    intersphinx_mapping = copy.copy(_base_intersphinx_mapping)

    python_version = f'{sys.version_info.major}.{sys.version_info.minor}'
    intersphinx_mapping['python'] = (f'https://docs.python.org/{python_version}/', None)

    # Add workspace objects file
    objects_file = os.path.join(output_path, '..', 'objects.inv')
    if os.path.isfile(objects_file):
        intersphinx_mapping['workspace'] = (os.path.relpath(os.path.dirname(objects_file), root_dir),
                                            os.path.realpath(objects_file))

    # Add other dependencies in the workspace
    for index, dep in enumerate(doc_deps):
        for gen_type in INTERSPHINX_GENERATORS:
            dep_output_dir_file = os.path.join(docs_build_path, '..', dep, output_dir_file[gen_type])
            if not os.path.isfile(dep_output_dir_file):
                continue

            with open(dep_output_dir_file, 'r') as f:
                depend_output_dir = f.read()
            objects_file = os.path.join(depend_output_dir, 'objects.inv')
            if not os.path.isfile(objects_file):
                continue

            intersphinx_mapping[f'{dep}_{gen_type}'] = (os.path.relpath(depend_output_dir, root_dir),
                                                        os.path.realpath(objects_file))

        event_queue.put(ExecutionEvent(
            'STAGE_PROGRESS',
            job_id=logger.job_id,
            stage_label=logger.stage_label,
            percent=str(index/float(len(doc_deps)))
        ))

    job_env['INTERSPHINX_MAPPING'] = yaml.dump(intersphinx_mapping)

    return 0


_base_intersphinx_mapping = {
    'catkin_pkg': ('https://docs.ros.org/independent/api/catkin_pkg/html', None),
    'jenkins_tools': ('https://docs.ros.org/independent/api/jenkins_tools/html', None),
    'rosdep': ('https://docs.ros.org/independent/api/rosdep/html', None),
    'rosdistro': ('https://docs.ros.org/independent/api/rosdistro/html', None),
    'rosinstall': ('https://docs.ros.org/independent/api/rosinstall/html', None),
    'rospkg': ('https://docs.ros.org/independent/api/rospkg/html', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
    'vcstools': ('https://docs.ros.org/independent/api/vcstools/html', None),
}
