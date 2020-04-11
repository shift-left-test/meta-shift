addtask testall
do_testall[recrdeptask] = "do_testall do_test"
do_testall[recideptask] = "do_${BB_DEFAULT_TASK}"
do_testall[nostamp] = "1"
do_testall[doc] = "Runs tests for all recipes required to build the target"
do_testall() {
    :
}

addtask coverageall
do_coverageall[recrdeptask] = "do_coverageall do_coverage"
do_coverageall[recideptask] = "do_${BB_DEFAULT_TASK}"
do_coverageall[nostamp] = "1"
do_coverageall[doc] = "Measures code coverage metrics for all recipes required to build the target"
do_coverageall() {
    :
}

addtask docall
do_docall[recrdeptask] = "do_docall do_doc"
do_docall[recideptask] = "do_${BB_DEFAULT_TASK}"
do_docall[nostamp] = "1"
do_docall[doc] = "Generates documents for all recipes required to build the target"
do_docall() {
    :
}
