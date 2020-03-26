addtask testall after do_populate_sysroot
do_testall[recrdeptask] = "do_testall do_test"
do_testall[recideptask] = "do_${BB_DEFAULT_TASK}"
do_testall[nostamp] = "1"
do_testall[doc] = "Runs tests for all recipes required to build the target"
do_testall() {
    :
}
