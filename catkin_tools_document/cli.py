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

from catkin_tools.argument_parsing import add_context_args
from catkin_tools.context import Context
from catkin_tools.terminal_color import fmt

from  catkin_tools.execution import job_server


from .document import document_workspace

import sys


def main(opts):
    ctx = Context.load(opts.workspace, opts.profile, opts, append=True)

    job_server.initialize(
        max_jobs=4,
        max_load=None,
        gnu_make_enabled=False)

    return document_workspace(
        ctx,
        packages=opts.packages,
        start_with=opts.start_with,
        no_deps=opts.no_deps,
        n_jobs=int(opts.parallel_jobs or 4),
        force_color=opts.force_color,
        quiet=not opts.verbose,
        interleave_output=opts.interleave_output,
        no_status=opts.no_status,
        limit_status_rate=opts.limit_status_rate,
        no_notify=opts.no_notify,
        continue_on_failure=opts.continue_on_failure,
        summarize_build=opts.summarize)


def prepare_arguments(parser):
    add_context_args(parser)

    # What packages to document
    pkg_group = parser.add_argument_group('Packages', 'Control which packages get documented.')
    add = pkg_group.add_argument
    add('packages', metavar='PKGNAME', nargs='*',
        help='Workspace packages to document, package dependencies are documented as well unless --no-deps is used. '
             'If no packages are given, then all the packages are documented.')
    add('--this', dest='document_this', action='store_true', default=False,
        help='Build the package containing the current working directory.')
    add('--no-deps', action='store_true', default=False,
        help='Only document specified packages, not their dependencies.')

    add('-j', '--jobs', default=None,
        help='Maximum number of build jobs to be distributed across active packages. (default is cpu count)')
    add('-p', '--parallel-packages', metavar='PACKAGE_JOBS', dest='parallel_jobs', default=None,
        help='Maximum number of packages allowed to be built in parallel (default is cpu count)')

    start_with_group = pkg_group.add_mutually_exclusive_group()
    add = start_with_group.add_argument
    add('--start-with', metavar='PKGNAME', type=str,
        help='Build a given package and those which depend on it, skipping any before it.')
    add('--start-with-this', action='store_true', default=False,
        help='Similar to --start-with, starting with the package containing the current directory.')

    add = pkg_group.add_argument
    add('--continue-on-failure', '-c', action='store_true', default=False,
        help='Try to continue documenting packages whose dependencies documented successfully even if some other requested '
             'packages fail to document.')

    behavior_group = parser.add_argument_group('Interface', 'The behavior of the command-line interface.')
    add = behavior_group.add_argument
    add('--verbose', '-v', action='store_true', default=False,
        help='Print output from commands in ordered blocks once the command finishes.')
    add('--interleave-output', '-i', action='store_true', default=False,
        help='Prevents ordering of command output when multiple commands are running at the same time.')
    add('--no-status', action='store_true', default=False,
        help='Suppresses status line, useful in situations where carriage return is not properly supported.')
    add('--summarize', '--summary', '-s', action='store_true', default=None,
        help='Adds a document summary to the end of a document; defaults to on with --continue-on-failure, off otherwise')
    add('--no-summarize', '--no-summary', action='store_false', dest='summarize',
        help='Explicitly disable the end of document summary')

    def status_rate_type(rate):
        rate = float(rate)
        if rate < 0:
            raise argparse.ArgumentTypeError("must be greater than or equal to zero.")
        return rate

    add('--limit-status-rate', '--status-rate', type=status_rate_type, default=10.0,
        help='Limit the update rate of the status bar to this frequency. Zero means unlimited. '
             'Must be positive, default is 10 Hz.')
    add('--no-notify', action='store_true', default=False,
        help='Suppresses system pop-up notification.')

    return parser
