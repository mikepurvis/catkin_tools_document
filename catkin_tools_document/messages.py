# coding=utf-8
#
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
import yaml

from catkin_tools.common import mkdir_p

CONF_ENVVAR_NAME = 'CATKIN_TOOLS_DOCUMENT_CONFIG_FILE'

CONF_DEFAULT = {
   'project': 'Project',
   'copyright': 'the Authors',
   'version': '0.0',
   'master_doc': 'index',
   'html_theme': 'agogo',
   'templates_path': []
}


def _write_raw(f, msg_type):
    msg_text = re.split('^=+$', msg_type._full_text, maxsplit=1, flags=re.MULTILINE)[0]
    msg_text = re.sub('^(.*?)$', '    \\1', msg_text, flags=re.MULTILINE)
    f.write(msg_text)
    f.write('\n')


def generate_messages(logger, event_queue, package, package_path, output_path):
    try:
        msg_module = __import__(package.name + '.msg').msg
        msg_names = [ msg_name for msg_name in dir(msg_module)
                      if re.match('^[A-Z]', msg_name) ]
    except:
        msg_names = []

    if msg_names:
        mkdir_p(os.path.join(output_path, 'msg'))
        with open(os.path.join(output_path, 'msg/index.rst'), 'w') as f:
            f.write('%s » Messages\n' % package.name)
            f.write('=' * 50 + '\n')
            f.write("""
            .. toctree::
                :titlesonly:
                :glob:

                *
            """)

        for msg_name in msg_names:
            msg_type = getattr(msg_module, msg_name)
            with open(os.path.join(output_path, 'msg', '%s.rst' % msg_name), 'w') as f:
                f.write('%s\n' % msg_name)
                f.write('=' * 50 + '\n\n')
                f.write('Definition::\n\n')
                _write_raw(f, msg_type)

    return 0


def generate_services(logger, event_queue, package, package_path, output_path):
    try:
        srv_module = __import__(package.name + '.srv').srv
        srv_names = [ srv_name for srv_name in dir(srv_module)
                      if re.match('^[A-Z]', srv_name) ]
    except:
        srv_names = []

    if srv_names:
        mkdir_p(os.path.join(output_path, 'srv'))

        with open(os.path.join(output_path, 'srv/index.rst'), 'w') as f:
            f.write('%s » Services\n' % package.name)
            f.write('=' * 50 + '\n')
            f.write("""
            .. toctree::
                :titlesonly:
                :glob:

                *
            """)

        for srv_name in srv_names:
            srv_type = getattr(srv_module, srv_name)
            if hasattr(srv_type, '_request_class'):
                with open(os.path.join(output_path, 'srv', '%s.rst' % srv_name), 'w') as f:
                    f.write('%s\n' % srv_name)
                    f.write('=' * 50 + '\n\n')
                    f.write('Request Definition::\n\n')
                    _write_raw(f, srv_type._request_class)
                    f.write('Response Definition::\n\n')
                    _write_raw(f, srv_type._response_class)
    return 0


def _get_person_links(people):
    person_links = []
    for person in people:
        if str == bytes:
            # Python 2
            name = person.name.encode('utf-8')
        else:
            # Python 3
            name = person.name
        if person.email:
            person_links.append("`%s <mailto:%s>`_" % (name, person.email))
        else:
            person_links.append(name)
    return person_links


def generate_package_summary(logger, event_queue, package, package_path,
                             rosdoc_conf, output_path):
    mkdir_p(output_path)

    with open(os.path.join(output_path, 'index.rst'), 'w') as f:
        f.write('%s\n' % package.name)
        f.write('=' * 50 + '\n\n')

        if str == bytes:
            # Python 2
            description = package.description.encode('utf-8')
        else:
            # Python 3
            description = package.description
        f.write('.. raw:: html\n\n')
        f.write('    <p>' + description + '</p>\n\n')

        if package.maintainers:
            f.write('**Maintainers:** %s\n\n' % ', '.join(_get_person_links(package.maintainers)))

        if package.authors:
            f.write('**Authors:** %s\n\n' % ', '.join(_get_person_links(package.authors)))

        f.write('**License:** %s\n\n' % ', '.join(package.licenses))

        f.write('**Source:** ? \n\n')

        if rosdoc_conf:
            f.write('**API:** ')
            for conf in rosdoc_conf:
                rosdoc_link = os.path.join('html', conf.get('output_dir', ''), 'index.html')
                rosdoc_name = conf.get('name', conf['builder'])
                f.write("`%s <%s>`_ " % (rosdoc_name, rosdoc_link))
            f.write('\n\n')

        f.write("""
.. toctree::
    :titlesonly:

""")
        if os.path.exists(os.path.join(output_path, 'msg/index.rst')):
            f.write("    Messages <msg/index>\n")
        if os.path.exists(os.path.join(output_path, 'srv/index.rst')):
            f.write("    Services <srv/index>\n")
        if os.path.exists(os.path.join(output_path, 'action/index.rst')):
            f.write("    Actions <action/index>\n")

        changelog_path = os.path.join(package_path, 'CHANGELOG.rst')
        changelog_symlink_path = os.path.join(output_path, 'CHANGELOG.rst')
        if os.path.exists(changelog_path) and not os.path.exists(changelog_symlink_path):
            os.symlink(changelog_path, changelog_symlink_path)

        if os.path.exists(changelog_symlink_path):
            f.write("    Changelog <CHANGELOG>\n")

    return 0


def generate_overall_summary(logger, event_queue, output_path):
    conf = CONF_DEFAULT.copy()
    if CONF_ENVVAR_NAME in os.environ:
        with open(os.environ[CONF_ENVVAR_NAME]) as f:
            conf.update(yaml.load(f))

    with open(os.path.join(output_path, 'conf.py'), 'w') as f:
        for k, v in conf.items():
            f.write('%s = %s\n' % (k, repr(v)))

    with open(os.path.join(output_path, 'index.rst'), 'w') as f:
        f.write("""
Packages
========

.. toctree::
    :titlesonly:
    :maxdepth: 1
    :glob:

    */index
""")
    return 0

