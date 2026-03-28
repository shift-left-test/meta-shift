# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**meta-shift** is a Yocto/Bitbake layer implementing shift-left testing. It provides recipes and Bitbake classes to run static analysis, unit tests, code coverage, and mutation testing directly in the host build environment during the Bitbake build process.

- **License:** MIT
- **Layer compatibility:** wrynose (current), with branches for older Yocto releases
- **Dependencies:** meta-oe, meta-python (mandatory); meta-qt5/meta-qt6, meta-clang (optional)

## Running Tests

```bash
# All tests (uses pytest with config from pytest.ini)
pytest

# Single test module
pytest test/cmaketest_test.py

# Single test class or method
pytest test/cmaketest_test.py::ClassName::test_method

# Tests require a Yocto build workspace. Set up with:
./test/mini-mcf.py -c test/conf/test.conf

# Speed up repeated runs with cached downloads:
export DL_DIR=$HOME/build-res/downloads
export SSTATE_DIR=$HOME/build-res/sstate-cache
```

Test files follow the pattern `test/*_test.py`. Tests are integration tests that run real Bitbake builds via session-scoped fixtures (`release_build`, `test_build`, `report_build`).

## Architecture

### Class Inheritance Chain

```
shiftutils.bbclass          # Utility functions (exec_proc, check_call, qemu helpers, report I/O)
  └── shifttest.bbclass     # Base task definitions (checkcode, test, coverage, checktest, report)
        ├── cpptest.bbclass  # C/C++ implementation (sage, lcov, sentinel integration)
        │     ├── cmaketest.bbclass    # CMake-specific build/test logic
        │     ├── autotoolstest.bbclass # Autotools-specific build/test logic
        │     └── qmaketest.bbclass    # QMake-specific build/test logic
        └── enacttest.bbclass          # Enact (webOS JS framework) testing via npm/jest
```

`shifttasks.bbclass` is separate — it defines the recursive `*all` task variants (e.g., `do_testall`) and is globally inherited via `layer.conf`.

### Key Design Patterns

- **Task structure:** Each task (checkcode, test, coverage, checktest, report) has a `do_X` (single recipe) and `do_Xall` (recursive over dependencies) variant. All tasks are `nostamp` (always re-run).
- **Build system dispatch:** `cpptest.bbclass` implements the core C/C++ logic. Build-system-specific classes (`cmaketest`, `autotoolstest`, `qmaketest`) inherit from it and override configure/compile/test steps.
- **Report generation:** `do_report` orchestrates all other tasks by calling `exec_func("do_X", dd)` on a copied datastore. Reports go to `${SHIFT_REPORT_DIR}/${PF}/<task>/`.
- **Conditional features:** `clang-tidy` and mutation testing (`sentinel`) require `meta-clang`. Dynamic layer recipes are in `dynamic-layers/meta-clang/`.
- **Task serialization:** When `SHIFT_PARALLEL_TASKS=0`, tasks use lockfiles to prevent concurrent execution.
- **Native/cross/SDK filtering:** Tasks skip recipes detected as native, cross, or SDK variants via `isNativeCrossSDK()`.

### Bitbake Extensions (lib/)

- `devtool/` plugins: `show` (recipe info), `cache` (cache status)
- `bblayers/` plugins: `inspect`, `status`, `test-layers`, `test-recipes`
- `recipetool/` plugins: `inspect` (recipe metadata)

### Test Infrastructure (test/)

- `selftest/` module: Build environment management (`build.py`), shell execution (`shell.py`), report parsers (`parsers/`)
- `mini-mcf.py`: Multi-repo cloner that sets up a complete Yocto workspace (bitbake, OE-core, meta-openembedded, meta-qt5/6, meta-clang, sample projects)
- Test configs in `test/conf/`: `test.conf` (full suite), `release.conf` (core), `report.conf` (reports)

### Recipe Organization

- `recipes-test/`: Test tools (googletest, cppcheck, cpplint, sage, sentinel, metrix++, duplo, compiledb, fff)
- `recipes-devtools/`: Build tools (cmake, python3 packages, perl)
- `recipes-support/`: Support tools (lcov)
- `recipes-core/`: Core recipes (meta-environment)

## Configuration Variables

All variables have defaults in `conf/layer.conf`. Key ones:

- `SHIFT_ENABLED` (default: `0`) — master enable switch
- `SHIFT_CHECKCODE_TOOLS` (default: `cppcheck`) — static analysis tools to run
- `SHIFT_CHECKTEST_ENABLED` (default: `0`) — enable mutation testing (requires meta-clang)
- `SHIFT_COVERAGE_BRANCH` (default: `1`) — include branch coverage
- `SHIFT_PARALLEL_TASKS` (default: `1`) — allow parallel task execution
- `SHIFT_REPORT_DIR` (default: `${TMPDIR}/shift-reports`) — report output directory

## Bitbake Task Quick Reference

```bash
bitbake <recipe> -c checkcode      # Static analysis
bitbake <recipe> -c test           # Unit tests
bitbake <recipe> -c coverage       # Code coverage
bitbake <recipe> -c checktest      # Mutation testing
bitbake <recipe> -c report         # All of the above consolidated
# Add 'all' suffix for recursive variants: testall, checkcodeall, etc.
```
