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

from catkin_tools.common import mkdir_p
from catkin_tools.execution.stages import CommandStage

import doxyfile


def doxygen(conf, package, output_path, source_path, docs_build_path):
    header_filename = ''
    footer_filename = ''
    tagfiles = ''
    output_dir = os.path.join(output_path, conf.get('output_dir', 'html'))
    tagfile_path = os.path.join(output_path, '%s.tag' % package.name)

    doxyfile_conf = {
        'ALIASES': conf.get('aliases', ''),
        'EXAMPLE_PATTERNS': conf.get('example_patterns', ''),
        'EXCLUDE_PATTERNS': conf.get('exclude_patterns', ''),
        'EXCLUDE_SYMBOLS': conf.get('exclude_symbols', ''),
        'HTML_FOOTER': footer_filename,
        'HTML_HEADER': header_filename,
        'HTML_OUTPUT': output_dir,
        'IMAGE_PATH': conf.get('image_path', source_path),
        'INPUT': source_path,
        'PROJECT_NAME': package.name,
        'OUTPUT_DIRECTORY': output_path,
        'TAB_SIZE': conf.get('tab_size', '8'),
        'GENERATE_TAGFILE': tagfile_path,
        'TAGFILES': tagfiles
    }
    mkdir_p(docs_build_path)
    doxyfile_path = os.path.join(docs_build_path, 'Doxyfile')
    with open(doxyfile_path, 'w') as f:
        doxyfile.write(f, doxyfile_conf)

    return CommandStage(
        'rosdoc_doxygen',
        ['/usr/local/bin/doxygen', doxyfile_path],
        cwd=source_path
    )

def sphinx(conf, package, output_path, source_path, docs_build_path):
    root_dir = os.path.join(source_path, conf.get('sphinx_root_dir', '.'))
    output_dir = os.path.join(output_path, conf.get('output_dir', 'html'))

    return CommandStage(
        'rosdoc_sphinx',
        ['/usr/local/bin/sphinx-build', '-E', '.', output_dir],
        cwd=root_dir
    )

def epydoc():
    raise NotImplementedError

def jsdoc():
    raise NotImplementedError

def swagger():
    raise NotImplementedError

