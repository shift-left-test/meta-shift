addtask docall
do_docall[recrdeptask] = "do_docall do_doc"
do_docall[recideptask] = "do_${BB_DEFAULT_TASK}"
do_docall[nostamp] = "1"
do_docall[doc] = "Generates documents for all recipes required to build the target"
do_docall() {
    :
}
