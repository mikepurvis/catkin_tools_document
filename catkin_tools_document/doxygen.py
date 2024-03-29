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

from catkin_tools.common import mkdir_p

import copy
import xml.etree.ElementTree as etree
import os
import pkg_resources

from .util import output_dir_file


def _write_config(f, conf):
    for k, v in conf.items():
        if isinstance(v, bool):
            v = "YES" if v else "NO"
        f.write("%s = %s\n" % (k, v))


def generate_doxygen_config(
    logger, event_queue, conf, package, recursive_build_deps, output_path, source_path, docs_build_path
):
    header_filename = ""
    footer_filename = ""
    output_subdir = os.path.join("html", conf.get("output_dir", ""), "")
    output_dir = os.path.join(output_path, output_subdir)
    mkdir_p(output_dir)

    tagfiles = []

    # Add tags for the standard library.
    cppreference_tagfile = pkg_resources.resource_filename(
        "catkin_tools_document", "external/cppreference-doxygen-web.tag.xml"
    )
    tagfiles.append("%s=%s" % (cppreference_tagfile, "https://en.cppreference.com/w/"))

    # Link up doxygen for all in-workspace build dependencies.
    for build_depend_name in recursive_build_deps:
        depend_docs_tagfile = os.path.join(docs_build_path, "..", build_depend_name, "tags")
        if os.path.isfile(depend_docs_tagfile):
            with open(os.path.join(docs_build_path, "..", build_depend_name, output_dir_file("doxygen"))) as f:
                depend_output_dir = f.read()
            depend_docs_relative_path = os.path.relpath(depend_output_dir, output_dir)
            tagfiles.append("%s=%s" % (depend_docs_tagfile, depend_docs_relative_path))

    mdfile = conf.get("use_mdfile_as_mainpage", "")
    if mdfile:
        mdfile = os.path.join(source_path, mdfile)

    doxyfile_conf = copy.copy(_base_config)
    doxyfile_conf.update(
        {
            "ALIASES": conf.get("aliases", ""),
            "EXAMPLE_PATTERNS": conf.get("example_patterns", ""),
            "EXCLUDE_PATTERNS": conf.get("exclude_patterns", ""),
            "EXCLUDE_SYMBOLS": conf.get("exclude_symbols", ""),
            "FILE_PATTERNS": conf.get(
                "file_patterns", doxyfile_conf["FILE_PATTERNS"]
            ),  # Use predefined values as default if not defined
            "GENERATE_HTML": True,
            "GENERATE_XML": True,
            "SEARCHENGINE": True,
            "HTML_FOOTER": footer_filename,
            "HTML_HEADER": header_filename,
            "HTML_OUTPUT": output_dir,
            "IMAGE_PATH": conf.get("image_path", source_path),
            "INPUT": " ".join([source_path, mdfile]),
            "PROJECT_NAME": package.name,
            "OUTPUT_DIRECTORY": output_path,
            "TAB_SIZE": conf.get("tab_size", "8"),
            "TAGFILES": " ".join(tagfiles),
            "USE_MATHJAX": True,
            "USE_MDFILE_AS_MAINPAGE": mdfile,
        }
    )

    with open(os.path.join(docs_build_path, "Doxyfile"), "w") as f:
        _write_config(f, doxyfile_conf)
    return 0


def generate_doxygen_config_tags(logger, event_queue, conf, package, output_path, source_path, docs_build_path):
    output_subdir = os.path.join("html", conf.get("output_dir", ""), "")
    output_dir = os.path.join(output_path, output_subdir)
    tagfile_path = os.path.join(docs_build_path, "tags")

    # This is a token to let dependent packages know what the subdirectory name is for linking
    # to this package's doxygen docs (since it isn't always "html").
    with open(os.path.join(docs_build_path, output_dir_file("doxygen")), "w") as f:
        f.write(output_dir)

    doxyfile_conf = copy.copy(_base_config)

    doxyfile_conf.update(
        {
            "ALIASES": conf.get("aliases", ""),
            "EXAMPLE_PATTERNS": conf.get("example_patterns", ""),
            "EXCLUDE_PATTERNS": conf.get("exclude_patterns", ""),
            "EXCLUDE_SYMBOLS": conf.get("exclude_symbols", ""),
            "INPUT": source_path,
            "PROJECT_NAME": package.name,
            "GENERATE_TAGFILE": tagfile_path,
        }
    )

    with open(os.path.join(docs_build_path, "Doxyfile_tags"), "w") as f:
        _write_config(f, doxyfile_conf)
    return 0


def filter_doxygen_tags(logger, event_queue, docs_build_path):
    tagfile_path = os.path.join(docs_build_path, "tags")
    tree = etree.parse(tagfile_path)
    root = tree.getroot()

    for node in root.findall("./compound[@kind='page']"):
        root.remove(node)

    tree.write(tagfile_path)
    return 0


_base_config = {
    "ALLEXTERNALS": False,
    "ALPHABETICAL_INDEX": False,
    "ALWAYS_DETAILED_SEC": False,
    "AUTOLINK_SUPPORT": True,
    "BRIEF_MEMBER_DESC": True,
    "BUILTIN_STL_SUPPORT": False,
    "CALLER_GRAPH": False,
    "CALL_GRAPH": False,
    "CASE_SENSE_NAMES": True,
    "CLASS_DIAGRAMS": True,
    "CLASS_GRAPH": True,
    "COLLABORATION_GRAPH": False,
    "COLS_IN_ALPHA_INDEX": 5,
    "CPP_CLI_SUPPORT": False,
    "CREATE_SUBDIRS": False,
    "DIRECTORY_GRAPH": True,
    "DISTRIBUTE_GROUP_DOC": False,
    "DOT_FONTNAME": "Helvetica",
    "DOT_FONTSIZE": 10,
    "DOT_NUM_THREADS": 0,
    "DOXYFILE_ENCODING": "UTF-8",
    "ENABLE_PREPROCESSING": True,
    "EXAMPLE_RECURSIVE": True,
    "EXCLUDE_SYMLINKS": False,
    "EXPAND_ONLY_PREDEF": False,
    "EXTERNAL_GROUPS": False,
    "EXTERNAL_PAGES": False,
    "EXTRACT_ALL": True,
    "EXTRACT_ANON_NSPACES": False,
    "EXTRACT_LOCAL_CLASSES": True,
    "EXTRACT_LOCAL_METHODS": False,
    "EXTRACT_PACKAGE": False,
    "EXTRACT_PRIVATE": True,
    "EXTRACT_STATIC": True,
    "FILE_PATTERNS": "*.c *.cpp *.h *.cc *.hh *.hpp *.py *.dox *.java",
    "FILTER_SOURCE_FILES": False,
    "FORCE_LOCAL_INCLUDES": False,
    "FULL_PATH_NAMES": False,
    "GENERATE_BUGLIST": True,
    "GENERATE_HTML": False,
    "GENERATE_LATEX": False,
    "GENERATE_TESTLIST": True,
    "GENERATE_TODOLIST": True,
    "GENERATE_XML": False,
    "GRAPHICAL_HIERARCHY": True,
    "GROUP_GRAPHS": True,
    "HAVE_DOT": True,
    "HIDE_FRIEND_COMPOUNDS": False,
    "HIDE_IN_BODY_DOCS": False,
    "HIDE_SCOPE_NAMES": False,
    "HIDE_UNDOC_CLASSES": False,
    "HIDE_UNDOC_MEMBERS": False,
    "HIDE_UNDOC_RELATIONS": True,
    "HTML_COLORSTYLE_GAMMA": 80,
    "HTML_COLORSTYLE_HUE": 220,
    "HTML_COLORSTYLE_SAT": 100,
    "HTML_DYNAMIC_SECTIONS": False,
    "HTML_FILE_EXTENSION": ".html",
    "HTML_INDEX_NUM_ENTRIES": 100,
    "HTML_TIMESTAMP": True,
    "IDL_PROPERTY_SUPPORT": True,
    "INCLUDED_BY_GRAPH": True,
    "INCLUDE_GRAPH": True,
    "INHERIT_DOCS": True,
    "INLINE_GROUPED_CLASSES": False,
    "INLINE_INFO": True,
    "INLINE_INHERITED_MEMB": False,
    "INLINE_SIMPLE_STRUCTS": False,
    "INLINE_SOURCES": False,
    "INPUT_ENCODING": "UTF-8",
    "INTERNAL_DOCS": False,
    "JAVADOC_AUTOBRIEF": False,
    "LOOKUP_CACHE_SIZE": 0,
    "MACRO_EXPANSION": False,
    "MARKDOWN_SUPPORT": True,
    "MAX_INITIALIZER_LINES": 30,
    "MULTILINE_CPP_IS_BRIEF": False,
    "OPTIMIZE_FOR_FORTRAN": False,
    "OPTIMIZE_OUTPUT_FOR_C": False,
    "OPTIMIZE_OUTPUT_JAVA": False,
    "OPTIMIZE_OUTPUT_VHDL": False,
    "OUTPUT_LANGUAGE": "English",
    "QT_AUTOBRIEF": False,
    "QUIET": False,
    "RECURSIVE": True,
    "REFERENCED_BY_RELATION": False,
    "REFERENCES_LINK_SOURCE": True,
    "REFERENCES_RELATION": False,
    "REPEAT_BRIEF": True,
    "SEARCHENGINE": False,
    "SEARCH_INCLUDES": False,
    "SEPARATE_MEMBER_PAGES": False,
    "SHORT_NAMES": False,
    "SHOW_FILES": True,
    "SHOW_GROUPED_MEMB_INC": False,
    "SHOW_INCLUDE_FILES": True,
    "SHOW_NAMESPACES": True,
    "SHOW_USED_FILES": True,
    "SIP_SUPPORT": False,
    "SKIP_FUNCTION_MACROS": True,
    "SORT_BRIEF_DOCS": True,
    "SORT_BY_SCOPE_NAME": False,
    "SORT_GROUP_NAMES": False,
    "SORT_MEMBER_DOCS": True,
    "SOURCE_BROWSER": True,
    "SOURCE_TOOLTIPS": True,
    "STRICT_PROTO_MATCHING": False,
    "STRIP_CODE_COMMENTS": True,
    "SUBGROUPING": True,
    "TAB_SIZE": 4,
    "TEMPLATE_RELATIONS": False,
    "TYPEDEF_HIDES_STRUCT": False,
    "UML_LIMIT_NUM_FIELDS": 10,
    "UML_LOOK": False,
    "USE_HTAGS": False,
    "VERBATIM_HEADERS": False,
    "WARNINGS": True,
    "WARN_FORMAT": '"$file:$line: $text"',
    "WARN_IF_DOC_ERROR": True,
    "WARN_IF_UNDOCUMENTED": True,
    "WARN_NO_PARAMDOC": False,
    "XML_OUTPUT": "xml",
}
