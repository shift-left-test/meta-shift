python show_affected_recipes() {
    task = d.expand("do_${BB_CURRENTTASK}")
    subtask = task[:-3]
    pf = d.getVar("PF", True)
    taskdepdata = d.getVar("BB_TASKDEPDATA", True)
    recipes = [taskdepdata[dep] for dep in taskdepdata if taskdepdata[dep][1] == subtask]
    affected = len(recipes)
    if affected > 0:
        recipes.sort(key=lambda recipe: recipe[0])
        bb.plain("{pf} {task}: --------------------------------------------------".format(pf=pf, task=task))
        bb.plain("{pf} {task}: Attempted '{subtask}' task of {affected} recipes.".format(pf=pf, task=task, subtask=subtask, affected=affected))
        bb.plain("{pf} {task}: --------------------------------------------------".format(pf=pf, task=task))
        for recipe in recipes:
            bb.plain("{pf} {task}:     {recipe}".format(pf=pf, task=task, recipe=recipe[0]))
        bb.plain("{pf} {task}: --------------------------------------------------".format(pf=pf, task=task))
    else:
        bb.plain("{pf} {task}: --------------------------------------------------".format(pf=pf, task=task))
        bb.warn("No recipes found to run '{subtask}' task.".format(subtask=subtask))
        bb.plain("{pf} {task}: --------------------------------------------------".format(pf=pf, task=task))
}

addtask checkcodeall
do_checkcodeall[recrdeptask] = "do_checkcodeall do_checkcode"
do_checkcodeall[recideptask] = "do_${BB_DEFAULT_TASK}"
do_checkcodeall[nostamp] = "1"
do_checkcodeall[doc] = "Runs static analysis for all recipes required to build the target"
do_checkcodeall[postfuncs] = "show_affected_recipes"
do_checkcodeall[vardepsexclude] = "show_affected_recipes"
do_checkcodeall() {
    :
}

addtask testall
do_testall[recrdeptask] = "do_testall do_test"
do_testall[recideptask] = "do_${BB_DEFAULT_TASK}"
do_testall[nostamp] = "1"
do_testall[doc] = "Runs tests for all recipes required to build the target"
do_testall[postfuncs] = "show_affected_recipes"
do_testall[vardepsexclude] = "show_affected_recipes"
do_testall() {
    :
}

addtask coverageall
do_coverageall[recrdeptask] = "do_coverageall do_coverage"
do_coverageall[recideptask] = "do_${BB_DEFAULT_TASK}"
do_coverageall[nostamp] = "1"
do_coverageall[doc] = "Measures code coverage metrics for all recipes required to build the target"
do_coverageall[postfuncs] = "show_affected_recipes"
do_coverageall[vardepsexclude] = "show_affected_recipes"
do_coverageall() {
    :
}

addtask checktestall
do_checktestall[recrdeptask] = "do_checktestall do_checktest"
do_checktestall[recideptask] = "do_${BB_DEFAULT_TASK}"
do_checktestall[nostamp] = "1"
do_checktestall[doc] = "Runs mutation tests for all recipes required to build the target"
do_checktestall[postfuncs] = "show_affected_recipes"
do_checktestall[vardepsexclude] = "show_affected_recipes"
do_checktestall() {
    :
}

addtask reportall
do_reportall[recrdeptask] = "do_reportall do_report"
do_reportall[recideptask] = "do_${BB_DEFAULT_TASK}"
do_reportall[nostamp] = "1"
do_reportall[doc] = "Makes reports for all recipes required to build the target"
do_reportall[postfuncs] = "show_affected_recipes"
do_reportall[vardepsexclude] = "show_affected_recipes"
do_reportall() {
    :
}
