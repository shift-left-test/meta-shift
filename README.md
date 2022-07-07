# meta-shift

> Shift-left testing for the Yocto project

## About

[Shift-left testing](https://en.wikipedia.org/wiki/Shift-left_testing) is an approach to software testing in which testing is performed earlier and often in the software development lifecycle.

The benefits of the shift-left testing approach are:

* Improved software quality since defects are detected in earlier stages
* Cost effective as early detected defects are cheaper to fix
* Increased efficiency in the software development process
* Reduced time to market since the QA stage does not take much time

The **meta-shift** layer is a set of recipes and classes for the Bitbake build system, which allows developers to test or examine their software modules in the host build environment. By enabling meta-shift, developers are able to easily use various tasks for their recipes via the bitbake command, such as:

* Lines of code
* Cache hit ratio
* Static analysis
* Comments
* Cyclomatic complexity
* Duplication
* Unit testing
* Code coverage
* Mutation testing

### Features

The main purpose of meta-shift is to provide the shift-left testing tools to the Yocto build environment satisfying the following needs.

* Easy to configure
* Host-based testing
* Supports major build systems (cmake, qmake, autotools)
* Supports SDK
* Supports various Yocto releases and BSPs
* Jenkins integration


## Quick start

Please visit a [build-sample](https://github.com/shift-left-test/build-sample) repository to find more information about how to configure and use features provided by the meta-shift layer.


## Usage

This is a meta layer for the Yocto project. Please find more information about the [meta layer](https://docs.yoctoproject.org/overview-manual/concepts.html#layers) if you are not familiar with.

### Dependencies

**Mandatory layers**

* meta-oe (meta-openembedded)
* meta-pyton (meta-openembedded)

**Optional layers**

* meta-qt5: To support QT5 based recipes
* meta-qt6: To support QT6 based recipes
* meta-clang: To use clang-tidy and the mutation testing

### Installation

Clone this repository and add the layer to your *bblayer.conf*

    $ git clone -b dunfell https://github.com/shift-left-test/meta-shift.git
    $ source oe-build-init-env
    $ bitbake-layers add-layer ../meta-shift

### Supported tasks

List of tasks via the bitbake command

* do_checkcache
* do_checkcacheall
* do_checkcode
* do_checkcodeall
* do_checkrecipe
* do_checkrecipeall
* do_checktest
* do_checktestall
* do_coverage
* do_coverageall
* do_report
* do_reportall
* do_test
* do_testall

### Supported bitbake tools

List of bitbake tool commands

* devtool cache
* devtool show
* bitbake-layers inspect
* bitbake-layers status
* bitbake-layers test-layers
* bitbake-layers test-recipes
* recipetool check
* recipetool inspect

### Configuration

These options can be used by adding to *conf/local.conf*.

* **SHIFT_CHECKCODE_EXCLUDES**: Paths to exclude from the static analysis
* **SHIFT_CHECKCODE_TOOLS**: Indicates which static analysis tools to use (cppcheck, cpplint, and clang-tidy)
* **SHIFT_CHECKRECIPE_SUPPRESS_RULES**: Exclude rules from bitbake script analysis (A list of rules can be found at https://github.com/priv-kweihmann/oelint-adv)
* **SHIFT_CHECKTEST_EXCLUDES**: Excludes paths from mutation testing
* **SHIFT_CHECKTEST_EXTENSIONS**: Extensions of source files to be mutated
* **SHIFT_CHECKTEST_GENERATOR**: Set the mutation generator (random, uniform, or weighted)
* **SHIFT_CHECKTEST_LIMIT**: Set the maximum limit of mutants
* **SHIFT_CHECKTEST_SCOPE**: Indicate which source code to mutate (all or commit)
* **SHIFT_CHECKTEST_SEED**: Random seed for the mutation generator
* **SHIFT_CHECKTEST_VERBOSE**: Silence the test ouput while running the `do_checktest` task
* **SHIFT_COVERAGE_EXCLUDES**: Exclude paths from code coverage analysis
* **SHIFT_REPORT_DIR**: A path to store report files
* **SHIFT_TEST_FILTER**: Run tests matching regular expression
* **SHIFT_TEST_SHUFFLE**: Randomize the order of tests
* **SHIFT_TEST_SUPPRESS_FAILURES**: Do not return non-zero exit code when tests fail

### Jenkins integration

It is recommended to set up [The meta-shift plugin for Jenkins](https://github.com/shift-left-test/meta-shift-plugin) for your Jenkins instance.


## Development

To prepare the meta-shift development environment via Docker:

    $ git clone https://github.com/shift-left-test/dockerfiles.git
    $ cd dockerfiles
    $ docker build -f yocto-dev/18.04/Dockerfile -t yocto-dev-18.04 .
    $ docker run --rm -it yocto-dev-18.04

To run all tests:

    $ pytest


## Contributing

This project is open to any patches. The patches can be submitted as Github pull request in https://github.com/shift-left-test/meta-shift or to the project mailing list.


## License

This project source code is available under MIT license. See [LICENSE](LICENSE).
