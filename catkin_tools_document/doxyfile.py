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


from copy import copy


def write(f, overrides):
    fields = copy(base_config)
    fields.update(overrides)

    lines = []
    for k, v in fields.items():
        if isinstance(v, bool):
            v = "YES" if v else "NO"
        f.write("%s = %s\n" % (k, v))


base_config = {
    'DOXYFILE_ENCODING': 'UTF-8',
    'CREATE_SUBDIRS': False,
    'OUTPUT_LANGUAGE': 'English',
    'BRIEF_MEMBER_DESC': True,
    'REPEAT_BRIEF': True,
    'ALWAYS_DETAILED_SEC': False,
    'INLINE_INHERITED_MEMB': False,
    'FULL_PATH_NAMES': False,
    'SHORT_NAMES': False,
    'QT_AUTOBRIEF': False,
    'INHERIT_DOCS': True,
    'SEPARATE_MEMBER_PAGES': False,
    'TAB_SIZE': 4,
    'OPTIMIZE_OUTPUT_FOR_C': False,
    'OPTIMIZE_OUTPUT_JAVA': False,
    'OPTIMIZE_FOR_FORTRAN': False,
    'OPTIMIZE_OUTPUT_VHDL': False,
    'MARKDOWN_SUPPORT': True,
    'AUTOLINK_SUPPORT': True,
    'BUILTIN_STL_SUPPORT': False,
    'CPP_CLI_SUPPORT': False,
    'SIP_SUPPORT': False,
    'IDL_PROPERTY_SUPPORT': True,
    'DISTRIBUTE_GROUP_DOC': False,
    'SUBGROUPING': True,
    'INLINE_GROUPED_CLASSES': False,
    'INLINE_SIMPLE_STRUCTS': False,
    'TYPEDEF_HIDES_STRUCT': False,
    'LOOKUP_CACHE_SIZE': 0,
    'EXTRACT_ALL': True,
    'EXTRACT_PRIVATE': True,
    'EXTRACT_PACKAGE': False,
    'EXTRACT_STATIC': True,
    'EXTRACT_LOCAL_CLASSES': True,
    'EXTRACT_LOCAL_METHODS': False,
    'EXTRACT_ANON_NSPACES': False,
    'HIDE_UNDOC_MEMBERS': False,
    'HIDE_UNDOC_CLASSES': False,
    'HIDE_FRIEND_COMPOUNDS': False,
    'HIDE_IN_BODY_DOCS': False,
    'INTERNAL_DOCS': False,
    'CASE_SENSE_NAMES': True,
    'HIDE_SCOPE_NAMES': False,
    'SHOW_INCLUDE_FILES': True,
    'SHOW_GROUPED_MEMB_INC': False,
    'FORCE_LOCAL_INCLUDES': False,
    'INLINE_INFO': True,
    'SORT_MEMBER_DOCS': True,
    'SORT_BRIEF_DOCS': True,
    'SORT_GROUP_NAMES': False,
    'SORT_BY_SCOPE_NAME': False,
    'STRICT_PROTO_MATCHING': False,
    'GENERATE_TODOLIST': True,
    'GENERATE_TESTLIST': True,
    'GENERATE_BUGLIST': True,
    'MAX_INITIALIZER_LINES': 30,
    'SHOW_USED_FILES': True,
    'SHOW_FILES': True,
    'SHOW_NAMESPACES': True,
    'QUIET': False,
    'WARNINGS': True,
    'WARN_IF_UNDOCUMENTED': True,
    'WARN_IF_DOC_ERROR': True,
    'WARN_NO_PARAMDOC': False,
    'WARN_FORMAT': '"$file:$line: $text"',
    'INPUT_ENCODING': 'UTF-8',
    'FILE_PATTERNS': '*.c *.cpp *.h *.cc *.hh *.hpp *.py *.dox *.java',
    'RECURSIVE': True,
    'EXCLUDE_SYMLINKS': False,
    'EXAMPLE_RECURSIVE': True,
    'FILTER_SOURCE_FILES': False,
    'SOURCE_BROWSER': True,
    'INLINE_SOURCES': False,
    'STRIP_CODE_COMMENTS': True,
    'REFERENCED_BY_RELATION': False,
    'REFERENCES_RELATION': False,
    'REFERENCES_LINK_SOURCE': True,
    'SOURCE_TOOLTIPS': True,
    'USE_HTAGS': False,
    'VERBATIM_HEADERS': False,
    'ALPHABETICAL_INDEX': False,
    'COLS_IN_ALPHA_INDEX': 5,
    'GENERATE_HTML': True,
    'HTML_FILE_EXTENSION': '.html',
    'HTML_COLORSTYLE_HUE': 220,
    'HTML_COLORSTYLE_SAT': 100,
    'HTML_COLORSTYLE_GAMMA': 80,
    'HTML_TIMESTAMP': True,
    'HTML_DYNAMIC_SECTIONS': False,
    'HTML_INDEX_NUM_ENTRIES': 100,
    'ENABLE_PREPROCESSING': True,
    'MACRO_EXPANSION': False,
    'EXPAND_ONLY_PREDEF': False,
    'SEARCH_INCLUDES': True,
    'SKIP_FUNCTION_MACROS': True,
    'ALLEXTERNALS': False,
    'EXTERNAL_GROUPS': False,
    'EXTERNAL_PAGES': False,
    'PERL_PATH': '/usr/bin/perl',
    'CLASS_DIAGRAMS': True,
    'HIDE_UNDOC_RELATIONS': True,
    'HAVE_DOT': True,
    'DOT_NUM_THREADS': 0,
    'DOT_FONTNAME': 'Helvetica',
    'DOT_FONTSIZE': 10,
    'CLASS_GRAPH': True,
    'COLLABORATION_GRAPH': False,
    'GROUP_GRAPHS': True,
    'UML_LOOK': False,
    'UML_LIMIT_NUM_FIELDS': 10,
    'TEMPLATE_RELATIONS': False,
    'INCLUDE_GRAPH': True,
    'INCLUDED_BY_GRAPH': True,
    'CALL_GRAPH': False,
    'CALLER_GRAPH': False,
    'GRAPHICAL_HIERARCHY': True,
    'DIRECTORY_GRAPH': True,
    'JAVADOC_AUTOBRIEF': False,
    'MULTILINE_CPP_IS_BRIEF': False
}
