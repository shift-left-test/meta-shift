addtask coverageall
do_coverageall[recrdeptask] = "do_coverageall do_coverage"
do_coverageall[recideptask] = "do_${BB_DEFAULT_TASK}"
do_coverageall[nostamp] = "1"
do_coverageall[doc] = "Measures code coverage metrics for all recipes required to build the target"
do_coverageall() {
    :
}
