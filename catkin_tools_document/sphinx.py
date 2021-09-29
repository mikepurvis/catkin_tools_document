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


def generate_intersphinx_mapping(docs_space, root_dir):
    intersphinx_mapping = copy.copy(_base_intersphinx_mapping)

    python_version = f'{sys.version_info.major}.{sys.version_info.minor}'
    intersphinx_mapping['python'] = (f'https://docs.python.org/{python_version}/', None)
    
    if os.path.isfile(os.path.join(docs_space, 'objects.inv')):
        intersphinx_mapping['workspace'] = (os.path.relpath(docs_space, root_dir), None)

    return intersphinx_mapping


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
