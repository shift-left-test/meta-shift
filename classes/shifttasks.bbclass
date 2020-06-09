def show_affected_recipes(task, d):
    pf = d.getVar("PF", True)
    taskdepdata = d.getVar("BB_TASKDEPDATA", False)
    recipes = [taskdepdata[dep] for dep in taskdepdata if taskdepdata[dep][1] == task]
    affected = len(recipes)
    if affected > 0:
        recipes.sort(key=lambda recipe: recipe[0])
        bb.plain("{0} {1}all: --------------------------------------------------".format(pf, task))
        bb.plain("{0} {1}all: Attempted '{1}' task of {2} recipes.".format(pf, task, affected))
        bb.plain("{0} {1}all: --------------------------------------------------".format(pf, task))
        for recipe in recipes:
            bb.plain("{0} {1}all:     {2}".format(pf, task, recipe[0]))
        bb.plain("{0} {1}all: --------------------------------------------------".format(pf, task))
    else:
        bb.plain("{0} {1}all: --------------------------------------------------".format(pf, task))
        bb.warn("{0} {1}all: No recipes found to run '{1}' task.".format(pf, task))
        bb.plain("{0} {1}all: --------------------------------------------------".format(pf, task))


python show_recipes_with_do_checkcode() {
    show_affected_recipes("do_checkcode", d)
}

addtask checkcodeall
do_checkcodeall[recrdeptask] = "do_checkcodeall do_checkcode"
do_checkcodeall[recideptask] = "do_${BB_DEFAULT_TASK}"
do_checkcodeall[nostamp] = "1"
do_checkcodeall[doc] = "Runs static analysis for all recipes required to build the target"
do_checkcodeall[postfuncs] = "show_recipes_with_do_checkcode"
do_checkcodeall[vardepsexclude] = "show_recipes_with_do_checkcode"
do_checkcodeall() {
    :
}

python show_recipes_with_do_test() {
    show_affected_recipes("do_test", d)
}

addtask testall
do_testall[recrdeptask] = "do_testall do_test"
do_testall[recideptask] = "do_${BB_DEFAULT_TASK}"
do_testall[nostamp] = "1"
do_testall[doc] = "Runs tests for all recipes required to build the target"
do_testall[postfuncs] = "show_recipes_with_do_test"
do_testall[vardepsexclude] = "show_recipes_with_do_test"
do_testall() {
    :
}

python show_recipes_with_do_coverage() {
    show_affected_recipes("do_coverage", d)
}

addtask coverageall
do_coverageall[recrdeptask] = "do_coverageall do_coverage"
do_coverageall[recideptask] = "do_${BB_DEFAULT_TASK}"
do_coverageall[nostamp] = "1"
do_coverageall[doc] = "Measures code coverage metrics for all recipes required to build the target"
do_coverageall[postfuncs] = "show_recipes_with_do_coverage"
do_coverageall[vardepsexclude] = "show_recipes_with_do_coverage"
do_coverageall() {
    :
}

addtask purgeall
do_purgeall[recrdeptask] = "do_purgeall do_cleanall"
do_purgeall[recideptask] = "do_${BB_DEFAULT_TASK}"
do_purgeall[nostamp] = "1"
do_purgeall[doc] = "Removes all output files, shared state cache, and downloaded source files for all recipes required to build the target"
do_purgeall() {
    :
}
