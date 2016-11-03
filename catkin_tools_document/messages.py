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
import re

from catkin_tools.common import mkdir_p



def generate_messages(logger, event_queue, package, output_path):
    try:
        package_module = __import__(package.name + '.msg')
    except ImportError:
        # No messages in this package, that's cool.
        return 0

    mkdir_p(os.path.join(output_path, 'msg'))
    msg_names = [ msg_name for msg_name in dir(package_module.msg)
                  if re.match('^[A-Z]', msg_name) ]
    for msg_name in msg_names:
        msg_type = getattr(package_module.msg, msg_name)
        with open(os.path.join(output_path, 'msg', '%s.rst' % msg_name), 'w') as f:
            f.write('%s/%s.msg\n' % (package.name, msg_name))
            f.write('=' * (len(msg_name) + len(package.name) + 5) + '\n\n')
            f.write('Raw definition::\n\n')

            msg_text = re.split('^=+$', msg_type._full_text, maxsplit=1, flags=re.MULTILINE)[0]
            msg_text = re.sub('^(.*?)$', '    \\1', msg_text, flags=re.MULTILINE)
            f.write(msg_text)

            # f.write('.. rst-class:: msg\n\n')

    return 0


def generate_package_summary(logger, event_queue, package, package_path,
                             rosdoc_conf, output_path):
    mkdir_p(output_path)
    with open(os.path.join(output_path, 'conf.py'), 'w') as f:
        f.write('project = %s\n' % repr(package.name))
        f.write('copyright = "Clearpath Robotics"\n')
        f.write('author = %s\n' % repr(', '.join([person.name for person in package.authors])))

        f.write("version = %s\n" % repr(package.version))
        f.write("release = %s\n" % repr(package.version))

        f.write("""
master_doc = 'index'
html_theme = 'traditional'

templates_path = []

#html_sidebars = {
#   '**': ['sidebartoc.html', 'sourcelink.html', 'searchbox.html']
#}
""")

    with open(os.path.join(output_path, 'index.rst'), 'w') as f:
        f.write('%s\n' % package.name)
        f.write('=' * len(package.name) + '\n\n')
        f.write("""
.. toctree::
    :titlesonly:
    :glob:

""")
        for conf in rosdoc_conf:
            rosdoc_output_dir = conf.get('output_dir', 'html')
            f.write("    %s/index\n" % rosdoc_output_dir)
            mkdir_p(os.path.join(output_path, rosdoc_output_dir))
            with open(os.path.join(output_path, rosdoc_output_dir, 'index.rst'), 'w') as g:
                g.write("API Docs (%s)\n" % conf['builder'])
                g.write('=' * (len(conf['builder']) + 11) + '\n')

        if os.path.exists(os.path.join(output_path, 'msg')):
            f.write("    msg/*\n")
        if os.path.exists(os.path.join(output_path, 'srv')):
            f.write("    srv/*\n")
        if os.path.exists(os.path.join(output_path, 'action')):
            f.write("    action/*\n")

        changelog_path = os.path.join(package_path, 'CHANGELOG.rst')
        changelog_symlink_path = os.path.join(output_path, 'CHANGELOG.rst')
        if os.path.exists(changelog_path) and not os.path.exists(changelog_symlink_path):
            os.symlink(changelog_path, changelog_symlink_path)

        if os.path.exists(changelog_symlink_path):
            f.write("    CHANGELOG\n")


    return 0


