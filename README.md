# meta-shift

**Shift-left testing for the Yocto project**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Overview

[Shift-left testing](https://en.wikipedia.org/wiki/Shift-left_testing) is an approach to software testing in which testing is performed earlier and often in the software development lifecycle. By integrating testing directly into the Bitbake build process, **meta-shift** empowers developers to catch defects where they are cheapest to fix: during the initial development phase.

The **meta-shift** layer provides a comprehensive suite of recipes and classes to test or examine software modules directly in the host build environment.

### Why meta-shift?
*   **Improved Software Quality:** Detect defects in earlier stages before they reach target hardware.
*   **Cost Effective:** Early-stage bug fixes are significantly cheaper than those found in QA or production.
*   **Increased Efficiency:** Streamline development with automated testing directly in the build loop.
*   **Faster Time to Market:** Reduce the QA bottleneck by ensuring high quality from the start.

---

## Features

*   **Unit Testing:** Support for major build systems (**CMake**, **QMake**, **Autotools**) and **Enact** (webOS JavaScript framework) via npm/jest.
*   **Code Coverage:** Measure and report code coverage using `gcovr`.
*   **Mutation Testing:** Advanced quality verification by mutating source code to test test-suite robustness.
*   **CI/CD Friendly:** Generates standard reports (JUnit XML, Cobertura, HTML) ready for CI pipelines, with a dedicated Jenkins plugin for visualization.

---

## Quick Start

1.  **Clone the repository:**
    ```bash
    git clone -b nanbield https://github.com/shift-left-test/meta-shift.git
    ```

2.  **Add the layer to your build environment:**
    ```bash
    source oe-build-init-env
    bitbake-layers add-layer ../meta-shift
    ```

3.  **Run a task for your recipe:**
    ```bash
    bitbake <recipe> -c test
    ```

> For a complete walkthrough, visit the [build-sample](https://github.com/shift-left-test/build-sample) repository.

---

## Usage

### Dependencies

| Type | Layers |
| :--- | :--- |
| **Mandatory** | `meta-oe`, `meta-python` (from meta-openembedded) |
| **Optional** | `meta-qt6` (for Qt support), `meta-clang` (for mutation testing) |

### Supported Tasks

You can execute the following tasks via `bitbake <recipe> -c <task>`:

*   **Testing**
    *   `do_test`: Executes unit tests in the host environment.
    *   `do_testall`: Recursively runs tests for all dependencies.
    *   `do_checktest`: Performs mutation testing.
    *   `do_checktestall`: Recursively performs mutation testing for all dependencies.
*   **Coverage & Metrics**
    *   `do_coverage`: Measures code coverage.
    *   `do_coverageall`: Recursively measures coverage for all dependencies.
*   **Verification**
    *   `do_verify`: Runs all test, coverage, and mutation tasks for the target.
    *   `do_verifyall`: Runs verification tasks for the target and its dependencies.

### Bitbake Tool Extensions

meta-shift extends common bitbake tools with specialized commands:
*   `devtool show`: Display detailed recipe information.
*   `bitbake-layers inspect`: Detailed layer inspection.
*   `bitbake-layers status`: Check layer status.
*   `bitbake-layers test-layers`: Show, add, or remove test-configured layers (those depending on meta-shift).
*   `bitbake-layers test-recipes`: List testable recipes.
*   `recipetool inspect`: Inspect recipe metadata.

---

## Configuration

Customize meta-shift by adding these variables to your `conf/local.conf`.

| Variable | Description | Default |
| :--- | :--- | :--- |
| `SHIFT_CHECKTEST_EXTENSIONS` | Extensions of source files to be mutated | |
| `SHIFT_CHECKTEST_FROM` | Diff base revision for scoping mutants (e.g., `HEAD~5`) | |
| `SHIFT_CHECKTEST_GENERATOR` | Mutation generator (`random`, `uniform`, or `weighted`) | `uniform` |
| `SHIFT_CHECKTEST_LIMIT` | Maximum number of mutants | `0` (Unlimited) |
| `SHIFT_CHECKTEST_OPERATORS` | Mutation operators to apply (space-separated) | |
| `SHIFT_CHECKTEST_PATTERNS` | Glob patterns to constrain mutation scope (`!` prefix to exclude) | |
| `SHIFT_CHECKTEST_SEED` | Random seed for the mutation generator | |
| `SHIFT_CHECKTEST_TIMEOUT` | Per-test timeout in seconds (default: sentinel auto = 1.5x baseline) | |
| `SHIFT_CHECKTEST_UNCOMMITTED` | Include uncommitted changes in mutation scope | `0` |
| `SHIFT_CHECKTEST_VERBOSE` | Enable verbose sentinel output while running `do_checktest` (passes `--verbose`) | `0` |
| `SHIFT_COVERAGE_BRANCH` | Show branch coverage instead of line in the text report (HTML/Cobertura always include both) | `0` |
| `SHIFT_COVERAGE_EXCLUDES` | Exclude paths from coverage (gcovr `--exclude` regexes, space-separated) | |
| `SHIFT_COVERAGE_EXTRA_OPTIONS` | Extra options passed verbatim to `gcovr` (e.g., `--gcov-ignore-errors all`) | |
| `SHIFT_PARALLEL_TASKS` | Allow shift tasks to run in parallel; set to `0` to serialize them via per-task lockfiles | `1` |
| `SHIFT_REPORT_DIR` | Directory for generated reports; each recipe writes to `<dir>/<PF>/{test,coverage,checktest}/` plus `metadata.json` (unset = reports disabled) | |
| `SHIFT_TEST_FILTER` | GoogleTest-style test filter (`:`-separated patterns, `*`/`?` wildcards, leading `-` to exclude); CMake translates it to `ctest -R/-E`, Autotools/QMake pass it via `GTEST_FILTER`, Enact ignores it | |
| `SHIFT_TEST_PARALLEL_JOBS` | Number of tests to run in parallel (CMake/ctest only; passed to `ctest --parallel`). Empty = serial; set a number or `${@oe.utils.cpu_count()}` for all host cores | |
| `SHIFT_TEST_SHUFFLE` | Randomize test execution order | `0` |
| `SHIFT_TEST_SUPPRESS_FAILURES`| Don't fail the build if tests fail | `0` |

---

## Integrations

### Jenkins
Enhance your CI/CD pipeline with [The meta-shift plugin for Jenkins](https://github.com/shift-left-test/meta-shift-plugin). It provides first-class visualization for the reports generated by meta-shift.

### Docker Development
A `Dockerfile` for a consistent build and development environment is bundled in
this repository (based on **Ubuntu 22.04**):
```bash
docker build -t meta-shift-dev .
docker run --rm -it -v "$PWD":/home/builder/meta-shift meta-shift-dev
```

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for our pull request process and code of conduct.

*   **Bugs & Features:** Submit via [GitHub Issues](https://github.com/shift-left-test/meta-shift/issues).
*   **Patches:** Submit as a [Pull Request](https://github.com/shift-left-test/meta-shift/pulls).

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
