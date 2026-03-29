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

*   **Unit Testing:** Support for major build systems (**CMake**, **QMake**, **Autotools**).
*   **Code Coverage:** Measure and report code coverage using `lcov` and `gcovr`.
*   **Mutation Testing:** Advanced quality verification by mutating source code to test test-suite robustness.
*   **Metrics:** Track lines of code, cyclomatic complexity, and duplication.
*   **Cache Analysis:** Monitor shared state and source cache hit ratios.
*   **Seamless Integration:** Native support for **SDK** generation and **Jenkins** CI/CD.

---

## Quick Start

1.  **Clone the repository:**
    ```bash
    git clone -b scarthgap https://github.com/shift-left-test/meta-shift.git
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
| **Optional** | `meta-qt5`/`meta-qt6` (for Qt support), `meta-clang` (for clang-tidy & mutation testing) |

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
*   **Reporting**
    *   `do_report`: Generates a consolidated quality report.
    *   `do_reportall`: Generates reports for the target and its dependencies.

### Bitbake Tool Extensions

meta-shift extends common bitbake tools with specialized commands:
*   `devtool show`: Display detailed recipe information.
*   `bitbake-layers inspect`: Detailed layer inspection.
*   `bitbake-layers status`: Check layer status.
*   `bitbake-layers test-layers`: Run tests across layers.
*   `bitbake-layers test-recipes`: List testable recipes.
*   `recipetool inspect`: Inspect recipe metadata.

---

## Configuration

Customize meta-shift by adding these variables to your `conf/local.conf`.

| Variable | Description | Default |
| :--- | :--- | :--- |
| `SHIFT_CHECKTEST_ENABLED` | Enable mutation testing | `0` (Disabled) |
| `SHIFT_CHECKTEST_EXCLUDES` | Excludes paths from mutation testing | |
| `SHIFT_CHECKTEST_EXTENSIONS` | Extensions of source files to be mutated | |
| `SHIFT_CHECKTEST_GENERATOR` | Mutation generator (`random`, `uniform`, or `weighted`) | |
| `SHIFT_CHECKTEST_LIMIT` | Maximum limit of mutants | |
| `SHIFT_CHECKTEST_MAX_TIMEOUT`| Maximum timeout duration of each test | |
| `SHIFT_CHECKTEST_SCOPE` | Scope of mutation (`all` or `commit`) | `all` |
| `SHIFT_CHECKTEST_SEED` | Random seed for the mutation generator | |
| `SHIFT_CHECKTEST_VERBOSE` | Silence the test output while running `do_checktest` | |
| `SHIFT_COVERAGE_EXCLUDES` | Exclude paths from code coverage analysis | |
| `SHIFT_COVERAGE_BRANCH` | Enable branch coverage generation | `0` |
| `SHIFT_REPORT_DIR` | Directory to store generated reports | `${TMPDIR}/shift-reports` |
| `SHIFT_TEST_FILTER` | Regex to filter tests to run | |
| `SHIFT_TEST_SHUFFLE` | Randomize test execution order | `0` |
| `SHIFT_TEST_SUPPRESS_FAILURES`| Don't fail the build if tests fail | `0` |

---

## Integrations

### Jenkins
Enhance your CI/CD pipeline with [The meta-shift plugin for Jenkins](https://github.com/shift-left-test/meta-shift-plugin). It provides first-class visualization for the reports generated by meta-shift.

### Docker Development
We provide pre-configured Dockerfiles for a consistent development environment:
```bash
git clone https://github.com/shift-left-test/dockerfiles.git
cd dockerfiles
docker build -f yocto-dev/20.04/Dockerfile -t yocto-dev-20.04 .
docker run --rm -it yocto-dev-20.04
```

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for our pull request process and code of conduct.

*   **Bugs & Features:** Submit via [GitHub Issues](https://github.com/shift-left-test/meta-shift/issues).
*   **Patches:** Submit as a [Pull Request](https://github.com/shift-left-test/meta-shift/pulls).

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
