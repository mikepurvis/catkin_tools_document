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
import time
import traceback

try:
    # Python3
    from queue import Queue
except ImportError:
    # Python2
    from Queue import Queue

from catkin_pkg.packages import find_packages
from catkin_pkg.topological_order import topological_order_packages
from catkin_pkg.package import parse_package

from catkin_tools.common import log
from catkin_tools.common import wide_log
from catkin_tools.common import get_cached_recursive_build_depends_in_workspace

from catkin_tools.execution.controllers import ConsoleStatusController
from catkin_tools.execution.executor import execute_jobs
from catkin_tools.execution.executor import run_until_complete
from catkin_tools.execution.jobs import Job
from catkin_tools.execution.stages import CommandStage
from catkin_tools.execution.stages import FunctionStage
from catkin_tools.terminal_color import fmt

from catkin_tools.jobs.utils import makedirs

from catkin_tools.verbs.catkin_build.build import determine_packages_to_be_built
from catkin_tools.verbs.catkin_build.build import verify_start_with_option


def create_job(context, package, package_path, deps):

    docs_space = os.path.join(context.build_space_abs, '..', 'docs', package.name)

    stages = []

    # Create package docs space
    stages.append(FunctionStage(
        'mkdir',
        makedirs,
        path=docs_space
    ))

    if os.path.exists(os.path.join(context.source_space_abs, package_path, 'msg')) or \
            os.path.exists(os.path.join(context.source_space_abs, package_path, 'srv')):
        stages.append(CommandStage(
            'msgsrv',
            ['/bin/sleep', '1'],
            cwd=os.path.join(context.build_space_abs, '..', 'docs')
        ))


    stages.append(CommandStage(
        'test',
        ['/bin/sleep', '1'],
        cwd=os.path.join(context.build_space_abs, '..', 'docs')
        #logger_factory=CMakeMakeIOBufferProtocol.factory
    ))

    return Job(jid=package.name, deps=deps, env={}, stages=stages)



def document_workspace(
    context,
    packages=None,
    start_with=None,
    no_deps=False,
    n_jobs=None,
    force_color=False,
    quiet=False,
    interleave_output=False,
    no_status=False,
    limit_status_rate=10.0,
    no_notify=False,
    continue_on_failure=False,
    summarize_build=None
):
    pre_start_time = time.time()

    # Get all the packages in the context source space
    # Suppress warnings since this is a utility function
    workspace_packages = find_packages(context.source_space_abs, exclude_subspaces=True, warnings=[])

    # If no_deps is given, ensure packages to build are provided
    if no_deps and packages is None:
        log(fmt("[document] @!@{rf}Error:@| With no_deps, you must specify packages to build."))
        return

    # Find list of packages in the workspace
    packages_to_be_documented, packages_to_be_documented_deps, all_packages = determine_packages_to_be_built(
        packages, context, workspace_packages)

    if not no_deps:
        # Extend packages to be documented to include their deps
        packages_to_be_documented.extend(packages_to_be_documented_deps)

    # Also re-sort
    try:
        packages_to_be_documented = topological_order_packages(dict(packages_to_be_documented))
    except AttributeError:
        log(fmt("[document] @!@{rf}Error:@| The workspace packages have a circular "
                "dependency, and cannot be documented. Please run `catkin list "
                "--deps` to determine the problematic package(s)."))
        return

    # Check the number of packages to be documented
    if len(packages_to_be_documented) == 0:
        log(fmt('[document] No packages to be documented.'))

    # Assert start_with package is in the workspace
    verify_start_with_option(
        start_with,
        packages,
        all_packages,
        packages_to_be_documented + packages_to_be_documented_deps)

    # Remove packages before start_with
    if start_with is not None:
        for path, pkg in list(packages_to_be_documented):
            if pkg.name != start_with:
                wide_log(fmt("@!@{pf}Skipping@|  @{gf}---@| @{cf}{}@|").format(pkg.name))
                packages_to_be_documented.pop(0)
            else:
                break

    # Get the names of all packages to be built
    packages_to_be_documented_names = [p.name for _, p in packages_to_be_documented]
    packages_to_be_documeted_deps_names = [p.name for _, p in packages_to_be_documented_deps]

    jobs = []

    # Construct jobs
    for pkg_path, pkg in all_packages:
        if pkg.name not in packages_to_be_documented_names:
            continue

        # Get actual execution deps
        deps = [
            p.name for _, p
            in get_cached_recursive_build_depends_in_workspace(pkg, packages_to_be_documented)
        ]

        jobs.append(create_job(context, pkg, pkg_path, deps))

    # Queue for communicating status
    event_queue = Queue()

    try:
        # Spin up status output thread
        status_thread = ConsoleStatusController(
            'document',
            ['package', 'packages'],
            jobs,
            n_jobs,
            [pkg.name for _, pkg in context.packages],
            [p for p in context.whitelist],
            [p for p in context.blacklist],
            event_queue,
            show_notifications=not no_notify,
            show_active_status=not no_status,
            show_buffered_stdout=not quiet and not interleave_output,
            show_buffered_stderr=not interleave_output,
            show_live_stdout=interleave_output,
            show_live_stderr=interleave_output,
            show_stage_events=not quiet,
            show_full_summary=(summarize_build is True),
            pre_start_time=pre_start_time,
            active_status_rate=limit_status_rate)
        status_thread.start()

        # Block while running N jobs asynchronously
        try:
            all_succeeded = run_until_complete(execute_jobs(
                'document',
                jobs,
                None,
                event_queue,
                context.log_space_abs,
                max_toplevel_jobs=n_jobs,
                continue_on_failure=continue_on_failure,
                continue_without_deps=False))
        except Exception:
            status_thread.keep_running = False
            all_succeeded = False
            status_thread.join(1.0)
            wide_log(str(traceback.format_exc()))
        status_thread.join(1.0)

    except KeyboardInterrupt:
        wide_log("[document] Interrupted by user!")
        event_queue.put(None)
