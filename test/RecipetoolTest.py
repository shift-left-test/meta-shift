#!/usr/bin/python

import constants
import os
import pytest
import unittest
import tempfile
import yocto


class Inspect(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.BARE)

    def test_default_format(self):
        o = self.build.shell.execute("recipetool inspect cpplint")
        assert o.stdout.containsAll("General Information",
                                    "-------------------",
                                    "Name: cpplint",
                                    "Summary: CPPLint - a static code analyzer for C/C++",
                                    "Description: A Static code analyzer for C/C++ written in python",
                                    "Author: Google Inc.",
                                    "Homepage: https://github.com/cpplint/cpplint",
                                    "Bugtracker: https://github.com/cpplint/cpplint/issues",
                                    "Section: devel/python",
                                    "License: BSD-3-Clause",
                                    "Version: 1.4.5",
                                    "Revision: r0",
                                    "Layer: meta-shift",
                                    "Testable: False")

    def test_json_format(self):
        o = self.build.shell.execute("recipetool inspect cpplint --json")
        assert o.stdout.containsAll('"General Information": {',
                                    '"Author": "Google Inc."',
                                    '"Homepage": "https://github.com/cpplint/cpplint"',
                                    '"Layer": "meta-shift"',
                                    '"Bugtracker": "https://github.com/cpplint/cpplint/issues"',
                                    '"Summary": "CPPLint - a static code analyzer for C/C++"',
                                    '"Name": "cpplint"',
                                    '"Version": "1.4.5"',
                                    '"Section": "devel/python"',
                                    '"Revision": "r0"',
                                    '"Testable": false',
                                    '"License": "BSD-3-Clause"',
                                    '"Description": "A Static code analyzer for C/C++ written in python"')


class InspectWithRelease(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.RELEASE)

    def test_cmake_project(self):
        o = self.build.shell.execute("recipetool inspect cmake-project")
        assert o.stdout.containsAll("Name: cmake-project",
                                    "Layer: meta-sample",
                                    "Testable: False")


class InspectWithTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.TEST)

    def test_cmake_project(self):
        o = self.build.shell.execute("recipetool inspect cmake-project")
        assert o.stdout.containsAll("Name: cmake-project",
                                    "Layer: meta-sample",
                                    "Testable: True")


class Check(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = yocto.BuildEnvironment(branch=constants.BRANCH, conf=constants.BARE)

    def check_return(self, filename):
        BASE_DIR = os.path.join(os.path.dirname(__file__), "recipetool_check_tests")
        o = self.build.shell.execute("source {} {}".format(os.path.join(BASE_DIR, filename),
                                                           self.build.builddir))
        assert o.returncode == 0, "{}:{}".format(filename, o.stdout)

    def test_rule_vars_bbclassextends_bad(self):
        self.check_return("rule_vars_bbclassextends_bad")

    def test_rule_tasks_nopythonprefix_bad(self):
        self.check_return("rule_tasks_nopythonprefix_bad")

    def test_rule_vars_notneededspace_good(self):
        self.check_return("rule_vars_notneededspace_good")

    def test_rule_tasks_no_cp_good(self):
        self.check_return("rule_tasks_no_cp_good")

    def test_rule_var_filesextrapaths_good(self):
        self.check_return("rule_var_filesextrapaths_good")

    def test_rule_file_requireinclude_bad(self):
        self.check_return("rule_file_requireinclude_bad")

    def test_rule_tasks_multiappends_bad(self):
        self.check_return("rule_tasks_multiappends_bad")

    def test_rule_var_filesextrapaths_bad(self):
        self.check_return("rule_var_filesextrapaths_bad")

    def test_rule_var_spaces_assignment_good(self):
        self.check_return("rule_var_spaces_assignment_good")

    def test_rule_tasks_addnotaskbody_bad(self):
        self.check_return("rule_tasks_addnotaskbody_bad")

    def test_rule_file_include_bad(self):
        self.check_return("rule_file_include_bad")

    def test_rule_var_homepageping_bad(self):
        self.check_return("rule_var_homepageping_bad")

    def test_rule_tasks_doc_strings_good(self):
        self.check_return("rule_tasks_doc_strings_good")

    def test_rule_var_pathhardcode_bad(self):
        self.check_return("rule_var_pathhardcode_bad")

    def test_rule_tasks_pythonprefix_good(self):
        self.check_return("rule_tasks_pythonprefix_good")

    def test_rule_var_src_uri_wildcard_good(self):
        self.check_return("rule_var_src_uri_wildcard_good")

    def test_rule_append_protvars_bad(self):
        self.check_return("rule_append_protvars_bad")

    def test_rule_tasks_pythonprefix_bad(self):
        self.check_return("rule_tasks_pythonprefix_bad")

    def test_rule_var_inconspaces_good(self):
        self.check_return("rule_var_inconspaces_good")

    def test_rule_vars_misspell_bad(self):
        self.check_return("rule_vars_misspell_bad")

    def test_rule_file_include_good(self):
        self.check_return("rule_file_include_good")

    def test_rule_file_patch_upstreamstatus_good(self):
        self.check_return("rule_file_patch_upstreamstatus_good")

    def test_rule_vars_pkgspecific_good(self):
        self.check_return("rule_vars_pkgspecific_good")

    def test_rule_nospace_line_end_good(self):
        self.check_return("rule_nospace_line_end_good")

    def test_rule_nospace_line_cont_bad(self):
        self.check_return("rule_nospace_line_cont_bad")

    def test_rule_var_section_lowercase_bad(self):
        self.check_return("rule_var_section_lowercase_bad")

    def test_rule_var_homepage_bad(self):
        self.check_return("rule_var_homepage_bad")

    def test_rule_var_src_uri_wildcard_bad(self):
        self.check_return("rule_var_src_uri_wildcard_bad")

    def test_rule_append_protvars_good2(self):
        self.check_return("rule_append_protvars_good2")

    def test_rule_tasks_nopythonprefix_good(self):
        self.check_return("rule_tasks_nopythonprefix_good")

    def test_rule_file_patch_signedoff_bad(self):
        self.check_return("rule_file_patch_signedoff_bad")

    def test_rule_var_depends_append_bad(self):
        self.check_return("rule_var_depends_append_bad")

    def test_rule_tasks_multiappends_good(self):
        self.check_return("rule_tasks_multiappends_good")

    def test_rule_var_quoted_bad(self):
        self.check_return("rule_var_quoted_bad")

    def test_rule_vars_suggested_good(self):
        self.check_return("rule_vars_suggested_good")

    def test_rule_vars_doublemodify_bad(self):
        self.check_return("rule_vars_doublemodify_bad")

    def test_rule_tasks_no_mkdir_good(self):
        self.check_return("rule_tasks_no_mkdir_good")

    def test_rule_var_src_uri_domain_bad(self):
        self.check_return("rule_var_src_uri_domain_bad")

    def test_rule_tasks_doc_strings_bad(self):
        self.check_return("rule_tasks_doc_strings_bad")

    def test_rule_tasks_addnotaskbody_good(self):
        self.check_return("rule_tasks_addnotaskbody_good")

    def test_rule_var_multilineindent_good(self):
        self.check_return("rule_var_multilineindent_good")

    def test_jetm_rule_var_depends_singleline_good(self):
        self.check_return("jetm.rule_var_depends_singleline_good")

    def test_rule_var_license_remote_good(self):
        self.check_return("rule_var_license_remote_good")

    def test_rule_var_license_remote_bad(self):
        self.check_return("rule_var_license_remote_bad")

    def test_rule_vars_bbvars_good(self):
        self.check_return("rule_vars_bbvars_good")

    def test_rule_vars_multiinherit_bad(self):
        self.check_return("rule_vars_multiinherit_bad")

    def test_rule_comment_notraling_bad(self):
        self.check_return("rule_comment_notraling_bad")

    def test_rule_var_insaneskip_bad(self):
        self.check_return("rule_var_insaneskip_bad")

    def test_rule_var_descsame_good2(self):
        self.check_return("rule_var_descsame_good2")

    def test_rule_var_descsame_good(self):
        self.check_return("rule_var_descsame_good")

    def test_rule_var_filesextrapathsop_bad(self):
        self.check_return("rule_var_filesextrapathsop_bad")

    def test_rule_var_pnusagedis_bad(self):
        self.check_return("rule_var_pnusagedis_bad")

    def test_rule_vars_order_bad(self):
        self.check_return("rule_vars_order_bad")

    def test_rule_var_homepage_good(self):
        self.check_return("rule_var_homepage_good")

    def test_rule_tasks_order_bad(self):
        self.check_return("rule_tasks_order_bad")

    def test_rule_var_autorev_good(self):
        self.check_return("rule_var_autorev_good")

    def test_rule_notabs_bad(self):
        self.check_return("rule_notabs_bad")

    def test_rule_vars_notneededspace_bad(self):
        self.check_return("rule_vars_notneededspace_bad")

    def test_rule_var_duplicates_good(self):
        self.check_return("rule_var_duplicates_good")

    def test_rule_vars_multiinherit_good(self):
        self.check_return("rule_vars_multiinherit_good")

    def test_rule_vars_improperinherit_bad(self):
        self.check_return("rule_vars_improperinherit_bad")

    def test_rule_func_machinespec_good(self):
        self.check_return("rule_func_machinespec_good")

    def test_rule_var_depends_append_good(self):
        self.check_return("rule_var_depends_append_good")

    def test_rule_vars_suggested_bad(self):
        self.check_return("rule_vars_suggested_bad")

    def test_jetm_rule_var_depends_singleline_bad(self):
        self.check_return("jetm.rule_var_depends_singleline_bad")

    def test_rule_var_appendop_good(self):
        self.check_return("rule_var_appendop_good")

    def test_rule_var_depends_ordered_bad(self):
        self.check_return("rule_var_depends_ordered_bad")

    def test_rule_vars_variable_override_good(self):
        self.check_return("rule_vars_variable_override_good")

    def test_rule_nospace_line_empty_bad(self):
        self.check_return("rule_nospace_line_empty_bad")

    def test_rule_vars_misspell_good(self):
        self.check_return("rule_vars_misspell_good")

    def test_rule_comment_notraling_good(self):
        self.check_return("rule_comment_notraling_good")

    def test_rule_var_pbpusage_bad(self):
        self.check_return("rule_var_pbpusage_bad")

    def test_rule_nospace_line_end_bad(self):
        self.check_return("rule_nospace_line_end_bad")

    def test_rule_var_multilineindent_bad(self):
        self.check_return("rule_var_multilineindent_bad")

    def test_rule_var_descsame_good3(self):
        self.check_return("rule_var_descsame_good3")

    def test_rule_var_section_lowercase_good(self):
        self.check_return("rule_var_section_lowercase_good")

    def test_rule_file_patch_signedoff_good(self):
        self.check_return("rule_file_patch_signedoff_good")

    def test_rule_var_depends_ordered_good(self):
        self.check_return("rule_var_depends_ordered_good")

    def test_rule_var_inconspaces_bad(self):
        self.check_return("rule_var_inconspaces_bad")

    def test_rule_var_bugtracker_url_bad(self):
        self.check_return("rule_var_bugtracker_url_bad")

    def test_rule_vars_order_good(self):
        self.check_return("rule_vars_order_good")

    def test_rule_vars_multiinclude_good(self):
        self.check_return("rule_vars_multiinclude_good")

    def test_rule_var_src_uri_domain_good(self):
        self.check_return("rule_var_src_uri_domain_good")

    def test_rule_vars_doublemodify_good(self):
        self.check_return("rule_vars_doublemodify_good")

    def test_rule_vars_improperinherit_good(self):
        self.check_return("rule_vars_improperinherit_good")

    def test_rule_vars_machinespec_good(self):
        self.check_return("rule_vars_machinespec_good")

    def test_rule_var_summary_linebreaks_bad(self):
        self.check_return("rule_var_summary_linebreaks_bad")

    def test_rule_vars_bbclassextends_good(self):
        self.check_return("rule_vars_bbclassextends_good")

    def test_rule_var_pnusage_bad(self):
        self.check_return("rule_var_pnusage_bad")

    def test_rule_var_descsame_bad(self):
        self.check_return("rule_var_descsame_bad")

    def test_rule_nospace_line_cont_good(self):
        self.check_return("rule_nospace_line_cont_good")

    def test_rule_var_spaces_assignment_bad(self):
        self.check_return("rule_var_spaces_assignment_bad")

    def test_rule_var_pnusagedis_good(self):
        self.check_return("rule_var_pnusagedis_good")

    def test_rule_var_descshort_good3(self):
        self.check_return("rule_var_descshort_good3")

    def test_rule_var_summary_80chars_bad(self):
        self.check_return("rule_var_summary_80chars_bad")

    def test_rule_var_homepageping_good(self):
        self.check_return("rule_var_homepageping_good")

    def test_rule_func_machinespec_bad(self):
        self.check_return("rule_func_machinespec_bad")

    def test_rule_vars_native_filename_good(self):
        self.check_return("rule_vars_native_filename_good")

    def test_rule_var_src_uri_bad(self):
        self.check_return("rule_var_src_uri_bad")

    def test_rule_newline_consec_good(self):
        self.check_return("rule_newline_consec_good")

    def test_rule_var_src_uri_good(self):
        self.check_return("rule_var_src_uri_good")

    def test_rule_nospace_line_begin_bad(self):
        self.check_return("rule_nospace_line_begin_bad")

    def test_rule_tasks_no_cp_bad(self):
        self.check_return("rule_tasks_no_cp_bad")

    def test_rule_var_summary_linebreaks_good(self):
        self.check_return("rule_var_summary_linebreaks_good")

    def test_rule_newline_eof_good(self):
        self.check_return("rule_newline_eof_good")

    def test_rule_var_pnusage_good(self):
        self.check_return("rule_var_pnusage_good")

    def test_rule_var_autorev_bad(self):
        self.check_return("rule_var_autorev_bad")

    def test_rule_vars_bbvars_bad(self):
        self.check_return("rule_vars_bbvars_bad")

    def test_rule_vars_variable_override_bad(self):
        self.check_return("rule_vars_variable_override_bad")

    def test_rule_var_summary_80chars_good(self):
        self.check_return("rule_var_summary_80chars_good")

    def test_rule_var_duplicates_bad(self):
        self.check_return("rule_var_duplicates_bad")

    def test_rule_file_require_bad(self):
        self.check_return("rule_file_require_bad")

    def test_rule_var_quoted_good(self):
        self.check_return("rule_var_quoted_good")

    def test_rule_vars_mandatory_exists_good(self):
        self.check_return("rule_vars_mandatory_exists_good")

    def test_rule_var_descshort_good2(self):
        self.check_return("rule_var_descshort_good2")

    def test_rule_vars_machinespec_bad(self):
        self.check_return("rule_vars_machinespec_bad")

    def test_rule_var_insaneskip_good(self):
        self.check_return("rule_var_insaneskip_good")

    def test_rule_vars_pkgspecific_bad(self):
        self.check_return("rule_vars_pkgspecific_bad")

    def test_rule_file_requireinclude_good(self):
        self.check_return("rule_file_requireinclude_good")

    def test_rule_append_protvars_good(self):
        self.check_return("rule_append_protvars_good")

    def test_rule_file_patch_upstreamstatus_bad(self):
        self.check_return("rule_file_patch_upstreamstatus_bad")

    def test_rule_vars_native_filename_bad(self):
        self.check_return("rule_vars_native_filename_bad")

    def test_rule_tasks_order_good(self):
        self.check_return("rule_tasks_order_good")

    def test_rule_func_machinespec_bad2(self):
        self.check_return("rule_func_machinespec_bad2")

    def test_rule_var_pathhardcode_good(self):
        self.check_return("rule_var_pathhardcode_good")

    def test_rule_nospace_line_begin_good(self):
        self.check_return("rule_nospace_line_begin_good")

    def test_rule_file_require_good(self):
        self.check_return("rule_file_require_good")

    def test_rule_tasks_no_mkdir_bad(self):
        self.check_return("rule_tasks_no_mkdir_bad")

    def test_rule_newline_consec_bad(self):
        self.check_return("rule_newline_consec_bad")

    def test_rule_var_pbpusage_good(self):
        self.check_return("rule_var_pbpusage_good")

    def test_rule_vars_machinespec_bad2(self):
        self.check_return("rule_vars_machinespec_bad2")

    def test_rule_var_descshort_bad(self):
        self.check_return("rule_var_descshort_bad")

    def test_rule_vars_multiinclude_bad(self):
        self.check_return("rule_vars_multiinclude_bad")

    def test_rule_notabs_good(self):
        self.check_return("rule_notabs_good")

    def test_rule_var_descshort_good(self):
        self.check_return("rule_var_descshort_good")

    def test_rule_var_bugtracker_url_good(self):
        self.check_return("rule_var_bugtracker_url_good")

    def test_rule_var_filesextrapathsop_good(self):
        self.check_return("rule_var_filesextrapathsop_good")

    def test_rule_var_appendop_bad(self):
        self.check_return("rule_var_appendop_bad")

    def test_rule_vars_mandatory_exists_bad(self):
        self.check_return("rule_vars_mandatory_exists_bad")

    def test_rule_nospace_line_empty_good(self):
        self.check_return("rule_nospace_line_empty_good")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
