addtask coverageall after do_poplulate_sysroot
do_coverageall[recrdeptask] = "do_coverageall do_coverage"
do_coverageall[recideptask] = "do_${BB_DEFAULT_TASK}"
do_coverageall() {
    :
}
do_coverageall[nostamp] = "1"
