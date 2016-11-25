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
import sys
from copy import copy

from catkin_tools.execution.stages import CommandStage
from catkin_tools.execution.stages import FunctionStage
from catkin_tools.jobs.utils import makedirs

from .doxygen import generate_doxygen_config, generate_doxygen_config_tags, filter_doxygen_tags
from .util import which


def doxygen(conf, package, deps, output_path, source_path, docs_build_path):
    # We run doxygen twice, once to generate the actual docs, and then a second time to generate
    # the tagfiles to link this documentation from other docs. See the following SO discussion
    # for this suggestion: http://stackoverflow.com/a/35640905/109517
    return [
        FunctionStage(
            'generate_doxygen_config', generate_doxygen_config,
            conf=conf,
            package=package,
            recursive_build_deps=deps,
            output_path=output_path,
            source_path=source_path,
            docs_build_path=docs_build_path),
        CommandStage(
            'rosdoc_doxygen',
            [which('doxygen'), os.path.join(docs_build_path, 'Doxyfile')],
            cwd=source_path),
        FunctionStage(
            'generate_doxygen_config_tags', generate_doxygen_config_tags,
            conf=conf,
            package=package,
            source_path=source_path,
            docs_build_path=docs_build_path),
        CommandStage(
            'rosdoc_doxygen_tags',
            [which('doxygen'), os.path.join(docs_build_path, 'Doxyfile_tags')],
            cwd=source_path),
        # Filter the tags XML to remove user-defined references that may appear in multiple
        # packages (like "codeapi"), since they are not namespaced.
        FunctionStage(
            'filter_doxygen_tags', filter_doxygen_tags,
            docs_build_path=docs_build_path)
    ]


def sphinx(conf, package, deps, output_path, source_path, docs_build_path):
    root_dir = os.path.join(source_path, conf.get('sphinx_root_dir', '.'))
    output_dir = os.path.join(output_path, 'html', conf.get('output_dir', ''))

    rpp = os.environ['ROS_PACKAGE_PATH'].split(':')
    rpp.insert(0, source_path)
    if os.path.exists(os.path.join(source_path, 'src')):
        rpp.insert(0, os.path.join(source_path, 'src'))
    env = {
        'PATH': os.environ['PATH'],
        'PYTHONPATH': ':'.join(sys.path),
        'ROS_PACKAGE_PATH': ':'.join(rpp),
        'LD_LIBRARY_PATH': os.environ.get('LD_LIBRARY_PATH', '')
    }

    return [
        CommandStage(
            'rosdoc_sphinx',
            [which('sphinx-build'), '-E', '.', output_dir],
            cwd=root_dir,
            env=env)
    ]


def epydoc(conf, package, deps, output_path, source_path, docs_build_path):
    output_dir = os.path.join(output_path, 'html', conf.get('output_dir', ''))

    command = [which('epydoc'), '--html', package.name, '-o', output_dir]
    for s in conf.get('exclude', []):
        command.extend(['--exclude', s])

    if 'config' in conf:
        command.extend(['--config', os.path.join(source_path, conf['config'])])
    else:
        # default options
        command.extend(['--inheritance', 'included', '--no-private'])

    env = {
        'PYTHONPATH': ':'.join(sys.path),
        'LD_LIBRARY_PATH': os.environ.get('LD_LIBRARY_PATH', '')
    }

    return [
        FunctionStage(
            'mkdir_epydoc',
            makedirs,
            path=output_dir),
        CommandStage(
            'rosdoc_epydoc',
            command,
            cwd=source_path,
            env=env)
    ]


def jsdoc():
    raise NotImplementedError


def swagger():
    raise NotImplementedError

