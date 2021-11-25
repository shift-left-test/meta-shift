"""
Copyright (c) 2020 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import bb
import logging
import oe.recipeutils
import sys
from devtool import setup_tinfoil, DevtoolError


logger = logging.getLogger("devtool")
logger.setLevel(logging.WARNING)


def escape_shell_value(value):
    value = value.replace('"', r'\"')
    value = value.replace('`', r'\`')
    return value


def format_variable(data, variable, flag=None, shell=False, show_unexpanded=True):
    if flag:
        unexpanded = data.getVarFlag(variable, flag, False)
        pattern = '%s[%s]=%%s' % (variable, flag)
    else:
        unexpanded = data.getVar(variable, False)
        pattern = '%s=%%s' % variable

    if data.getVarFlag(variable, 'unexport', expand=False):
        if flag:
            return pattern % unexpanded
        else:
            return '# ' + pattern % unexpanded

    try:
        expanded = bb.data.expand(unexpanded, data)
    except BaseException:
        if flag:
            logger.exception("Expansion of '%s[%s]' failed", variable, flag)
        else:
            logger.exception("Expansion of '%s' failed", variable)
        return '# ' + pattern % unexpanded
    else:
        message = ''
        if show_unexpanded and unexpanded != expanded:
            message += '# ' + pattern % unexpanded + '\n'

        if data.getVarFlag(variable, 'export', expand=False):
            message += 'export '

        if isinstance(expanded, basestring):
            expanded = '"%s"' % escape_shell_value(expanded)
        else:
            expanded = repr(expanded)
        message += pattern % expanded
        return message


ignored_flags = ('func', 'python', 'export', 'export_func')
def print_variable_flags(data, variable, show_unexpanded=True):
    flags = data.getVarFlags(variable, expand=False)
    if not flags:
        return

    for flag, value in flags.iteritems():
        if flag.startswith('_') or flag in ignored_flags:
            continue
        value = str(value)
        print(format_variable(data, variable, flag, show_unexpanded=show_unexpanded))


def print_variable(data, variable, show_unexpanded=True):
    unexpanded = data.getVar(variable, False)
    if unexpanded is None:
        return
    unexpanded = str(unexpanded)


    flags = data.getVarFlags(variable, expand=False) or {}
    if flags.get('func'):
        if flags.get('python'):
            print("python %s () {\n%s}\n" % (variable, unexpanded))
        else:
            try:
                value = bb.data.expand(unexpanded, data)
            except BaseException:
                logger.exception("Expansion of '%s' failed", variable)
                return

            print("%s () {\n%s}\n" % (variable, value))
    else:
        print(format_variable(data, variable, shell=True, show_unexpanded=show_unexpanded))


def variable_function_deps(data, variable, deps, seen):
    variable_deps = deps and deps.get(variable) or set()
    if data.getVarFlag(variable, 'python', expand=False):
        parser = bb.codeparser.PythonParser(variable, logger)
        parser.parse_python(data.getVar(variable, False))
        variable_deps |= parser.execs
        deps[variable] = variable_deps

    for dep in variable_deps:
        if dep in seen:
            continue
        seen.add(dep)

        if data.getVarFlag(dep, 'func', expand=False):
            for _dep in variable_function_deps(data, dep, deps, seen):
                yield _dep
            yield dep


def dep_ordered_variables(data, variables, deps):
    seen = set()
    for variable in variables:
        if variable in seen:
            continue

        seen.add(variable)
        for dep in variable_function_deps(data, variable, deps, seen):
            yield dep
        yield variable

def sorted_variables(data, variables=None, show_deps=True):
    def key(v):
        if data.getVarFlag(v, 'func', expand=False):
            return int(bool(data.getVarFlag(v, 'python', expand=False))) + 2
        else:
            return int(bool(data.getVarFlag(v, 'export', expand=False)))

    all_variables = data.keys()
    if not variables:
        variables = sorted(all_variables, key=lambda v: v.lower())
        variables = filter(lambda v: not v.startswith('_'), variables)
    else:
        for variable in variables:
            if variable not in all_variables:
                logger.warn("Requested variable '%s' does not exist", variable)
        variables = sorted(variables, key=lambda v: v.lower())
        if show_deps:
            deps = bb.data.generate_dependencies(data)[1]
            variables = list(dep_ordered_variables(data, variables, deps))

    variables = sorted(variables, key=key)
    return variables


def parse_metadata(tinfoil, recipe):
    if recipe:
        tinfoil.parseRecipes()
        recipefile = oe.recipeutils.pn_to_recipe(tinfoil.cooker, recipe)
        if not recipefile:
            raise bb.BBHandledException("Failed to find the recipe file for '{}'\n".format(recipe))
        appendfiles = tinfoil.cooker.collection.get_file_appends(recipefile)
        return bb.cache.Cache.loadDataFull(recipefile, appendfiles, tinfoil.config_data)
    else:
        return tinfoil.config_data


def show(args, config, basepath, workspace):
    """Show the bitbake metadata variables
    """
    try:
        tinfoil = setup_tinfoil(config_only=True, basepath=basepath)
        data = parse_metadata(tinfoil, args.recipe)
        if not data:
            raise bb.BBHandledException("Failed to parse the bitbake metadata\n")

        args.variables = [data.expand(v) for v in args.variables]
        variables = sorted_variables(data, args.variables, args.dependencies)
        for variable in variables:
            print_variable(data, variable, show_unexpanded=args.unexpanded)
            if args.flags:
                print_variable_flags(data, variable, show_unexpanded=args.unexpanded)
        return

    except bb.BBHandledException as e:
        logger.error(str(e))
        return 2
    finally:
        tinfoil.shutdown()


def register_commands(subparsers, context):
    parser = subparsers.add_parser("show",
                                   help="Show the bitbake metadata variables",
                                   description="Show the bitbake metadata variables")
    parser.add_argument("-x", "--dependencies", action="store_true", help="Show functions the variables depend on")
    parser.add_argument("-f", "--flags", action="store_true", help="Show flags")
    parser.add_argument("-u", "--unexpanded", action="store_true", help="Show unexpanded version of variables")
    parser.add_argument("-r", "--recipe", help="Show variables of the recipe")
    parser.add_argument("variables", nargs="*", help="variables to show (default: all variables)")
    parser.set_defaults(func=show, no_workspace=True)
