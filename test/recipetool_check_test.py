#-*- coding: utf-8 -*-
#!/usr/bin/python3

"""
MIT License

Copyright (c) 2020 Sung Gon Kim

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import os
import json
import shutil
import tempfile
import pytest


filenames = [
    "rule_vars_bbclassextends_bad",
    "rule_tasks_nopythonprefix_bad",
    "rule_vars_notneededspace_good",
    "rule_tasks_no_cp_good",
    "rule_var_filesextrapaths_good",
    "rule_file_requireinclude_bad",
    "rule_tasks_multiappends_bad",
    "rule_var_filesextrapaths_bad",
    "rule_var_spaces_assignment_good",
    "rule_tasks_addnotaskbody_bad",
    "rule_file_include_bad",
    "rule_var_homepageping_bad",
    "rule_tasks_doc_strings_good",
    "rule_var_pathhardcode_bad",
    "rule_tasks_pythonprefix_good",
    "rule_var_src_uri_wildcard_good",
    "rule_append_protvars_bad",
    "rule_tasks_pythonprefix_bad",
    "rule_var_inconspaces_good",
    "rule_vars_misspell_bad",
    "rule_file_include_good",
    "rule_file_patch_upstreamstatus_good",
    "rule_vars_pkgspecific_good",
    "rule_nospace_line_end_good",
    "rule_nospace_line_cont_bad",
    "rule_var_section_lowercase_bad",
    "rule_var_homepage_bad",
    "rule_var_src_uri_wildcard_bad",
    "rule_append_protvars_good2",
    "rule_tasks_nopythonprefix_good",
    "rule_file_patch_signedoff_bad",
    "rule_var_depends_append_bad",
    "rule_tasks_multiappends_good",
    "rule_var_quoted_bad",
    "rule_vars_suggested_good",
    "rule_vars_doublemodify_bad",
    "rule_tasks_no_mkdir_good",
    "rule_var_src_uri_domain_bad",
    "rule_tasks_doc_strings_bad",
    "rule_tasks_addnotaskbody_good",
    "rule_var_multilineindent_good",
    "jetm.rule_var_depends_singleline_good",
    "rule_var_license_remote_good",
    "rule_var_license_remote_bad",
    "rule_vars_bbvars_good",
    "rule_vars_multiinherit_bad",
    "rule_comment_notraling_bad",
    "rule_var_insaneskip_bad",
    "rule_var_descsame_good2",
    "rule_var_descsame_good",
    "rule_var_filesextrapathsop_bad",
    "rule_var_pnusagedis_bad",
    "rule_vars_order_bad",
    "rule_var_homepage_good",
    "rule_tasks_order_bad",
    "rule_var_autorev_good",
    "rule_notabs_bad",
    "rule_vars_notneededspace_bad",
    "rule_var_duplicates_good",
    "rule_vars_multiinherit_good",
    "rule_vars_improperinherit_bad",
    "rule_func_machinespec_good",
    "rule_var_depends_append_good",
    "rule_vars_suggested_bad",
    "jetm.rule_var_depends_singleline_bad",
    "rule_var_appendop_good",
    "rule_var_depends_ordered_bad",
    "rule_vars_variable_override_good",
    "rule_nospace_line_empty_bad",
    "rule_vars_misspell_good",
    "rule_comment_notraling_good",
    "rule_var_pbpusage_bad",
    "rule_nospace_line_end_bad",
    "rule_var_multilineindent_bad",
    "rule_var_descsame_good3",
    "rule_var_section_lowercase_good",
    "rule_file_patch_signedoff_good",
    "rule_var_depends_ordered_good",
    "rule_var_inconspaces_bad",
    "rule_var_bugtracker_url_bad",
    "rule_vars_order_good",
    "rule_vars_multiinclude_good",
    "rule_var_src_uri_domain_good",
    "rule_vars_doublemodify_good",
    "rule_vars_improperinherit_good",
    "rule_vars_machinespec_good",
    "rule_var_summary_linebreaks_bad",
    "rule_vars_bbclassextends_good",
    "rule_var_pnusage_bad",
    "rule_var_descsame_bad",
    "rule_nospace_line_cont_good",
    "rule_var_spaces_assignment_bad",
    "rule_var_pnusagedis_good",
    "rule_var_descshort_good3",
    "rule_var_summary_80chars_bad",
    "rule_var_homepageping_good",
    "rule_func_machinespec_bad",
    "rule_vars_native_filename_good",
    "rule_var_src_uri_bad",
    "rule_newline_consec_good",
    "rule_var_src_uri_good",
    "rule_nospace_line_begin_bad",
    "rule_tasks_no_cp_bad",
    "rule_var_summary_linebreaks_good",
    "rule_newline_eof_good",
    "rule_var_pnusage_good",
    "rule_var_autorev_bad",
    "rule_vars_bbvars_bad",
    "rule_vars_variable_override_bad",
    "rule_var_summary_80chars_good",
    "rule_var_duplicates_bad",
    "rule_file_require_bad",
    "rule_var_quoted_good",
    "rule_vars_mandatory_exists_good",
    "rule_var_descshort_good2",
    "rule_vars_machinespec_bad",
    "rule_var_insaneskip_good",
    "rule_vars_pkgspecific_bad",
    "rule_file_requireinclude_good",
    "rule_append_protvars_good",
    "rule_file_patch_upstreamstatus_bad",
    "rule_vars_native_filename_bad",
    "rule_tasks_order_good",
    "rule_func_machinespec_bad2",
    "rule_var_pathhardcode_good",
    "rule_nospace_line_begin_good",
    "rule_file_require_good",
    "rule_tasks_no_mkdir_bad",
    "rule_newline_consec_bad",
    "rule_var_pbpusage_good",
    "rule_vars_machinespec_bad2",
    "rule_var_descshort_bad",
    "rule_vars_multiinclude_bad",
    "rule_notabs_good",
    "rule_var_descshort_good",
    "rule_var_bugtracker_url_good",
    "rule_var_filesextrapathsop_good",
    "rule_var_appendop_bad",
    "rule_vars_mandatory_exists_bad",
    "rule_nospace_line_empty_good",
]


@pytest.mark.parametrize("filename", filenames)
def test_rule(bare_build, filename):
    BASE_DIR = os.path.join(os.path.dirname(__file__), "recipetool_check_tests")
    o = bare_build.shell.execute("source {} {}".format(os.path.join(BASE_DIR, filename),
                                                       bare_build.build_dir))
    assert o.returncode == 0, "{}:{}".format(filename, o.stdout)


def test_check_save_as_file(bare_build):
    d = tempfile.mkdtemp()
    try:
        temp = os.path.join(d, "output.json")
        o = bare_build.shell.execute("recipetool check cmake-native --output {}".format(temp))
        with open(temp, "r") as f:
            data = json.load(f)
            assert isinstance(data["issues"], list)
            assert len(data["issues"]) > 0
            for issue in data["issues"]:
                assert isinstance(issue, dict)
                assert isinstance(issue["file"], str)
                assert isinstance(issue["line"], int)
                assert isinstance(issue["severity"], str)
                assert isinstance(issue["rule"], str)
                assert isinstance(issue["description"], str)
    finally:
        shutil.rmtree(d)

