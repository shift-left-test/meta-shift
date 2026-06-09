# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**meta-shift** is a Yocto/Bitbake layer implementing shift-left testing. It provides recipes and Bitbake classes to run unit tests, code coverage, and mutation testing directly in the host build environment during the Bitbake build process.

- **License:** MIT
- **Layer compatibility:** wrynose (current), with branches for older Yocto releases
- **Dependencies:** meta-oe, meta-python (mandatory); meta-qt6, meta-clang (optional)

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

Test files follow the pattern `test/*_test.py`. Tests are integration tests that run real Bitbake builds via session-scoped fixtures (`release_build`, `test_build`, `verify_build`).

## Architecture

### Class Inheritance Chain

```
shiftutils.bbclass          # Utility functions (qemu helpers, CLI flag builders, metadata I/O, isNativeCrossSDK)
  └── shifttest.bbclass     # Base task definitions (test, coverage, checktest, verify)
        ├── cpptest.bbclass  # C/C++ implementation (gcovr, sentinel integration)
        │     ├── cmaketest.bbclass    # CMake-specific build/test logic
        │     ├── autotoolstest.bbclass # Autotools-specific build/test logic
        │     └── qmaketest.bbclass    # QMake-specific build/test logic
        └── enacttest.bbclass          # Enact (webOS JS framework) testing via npm/jest
```

`shifttasks.bbclass` is separate — it defines the recursive `*all` task variants (e.g., `do_testall`) and is globally inherited via `layer.conf`.

### Key Design Patterns

- **Task structure:** Each task (test, coverage, checktest, verify) has a `do_X` (single recipe) and `do_Xall` (recursive over dependencies) variant. All tasks are `nostamp` (always re-run).
- **Build system dispatch:** `cpptest.bbclass` implements the core C/C++ logic. Build-system-specific classes (`cmaketest`, `autotoolstest`, `qmaketest`) inherit from it and override configure/compile/test steps.
- **Verification:** `do_verify` orchestrates all other tasks by calling `exec_func("do_X", dd)` on a copied datastore. Reports go to `${SHIFT_REPORT_DIR}/${PF}/<task>/`.
- **Conditional features:** Mutation testing (`sentinel`) requires `meta-clang`. Dynamic layer recipes are in `dynamic-layers/meta-clang/`.
- **Task serialization:** When `SHIFT_PARALLEL_TASKS=0`, tasks use lockfiles to prevent concurrent execution.
- **Native/cross/SDK filtering:** Tasks skip recipes detected as native, cross, or SDK variants via `isNativeCrossSDK()`.

### Bitbake Extensions (lib/)

- `devtool/` plugins: `show` (recipe info)
- `bblayers/` plugins: `inspect`, `status`, `test-layers`, `test-recipes`
- `recipetool/` plugins: `inspect` (recipe metadata)

### Test Infrastructure (test/)

- `selftest/` module: Build environment management (`build.py`), shell execution (`shell.py`), report parsers (`parsers/`)
- `mini-mcf.py`: Multi-repo cloner that sets up a complete Yocto workspace (bitbake, OE-core, meta-openembedded, meta-qt6, meta-clang, sample projects)
- Test configs in `test/conf/`: `test.conf` (full suite), `release.conf` (core), `verify.conf` (consolidated verify task)

### Recipe Organization

- `recipes-test/`: Test tools (sentinel, compiledb, gcovr, fff) and their Python dependencies (`python/`)
- `recipes-devtools/`: Build tools (cmake, python3 packages, perl)
- `recipes-core/`: Core recipes (meta-environment)

## Configuration Variables

Most variables have defaults in `conf/layer.conf` (a few, like `SHIFT_REPORT_DIR` and `SHIFT_TEST_FILTER`, have none). Key ones:

- `SHIFT_PARALLEL_TASKS` (default: `1`) — allow parallel task execution
- `SHIFT_REPORT_DIR` (no default — set in `local.conf` to write report files; unset still runs all tasks console-only)

### Documentation
- When modifying code, always update `README.md` accordingly (feature additions/removals, configuration changes, task changes, etc.)

### Code Comments
- Keep comments concise. Explain *why* (non-obvious rationale, BitBake quirks, constraints), not *what* the code already states.
- Remove redundant or self-evident comments; trim verbose ones to the essential point.
- Don't put external sample-project proper nouns in comments; describe behavior in layer-generic terms.

### Branching
- Name topic branches `feature/<base>/<topic>` or `bugfix/<base>/<topic>`, where `<base>` is the target base branch (`<release>-next` or `master`) — e.g. `feature/scarthgap-next/junitxml`.

### Commit Messages
- Write each commit message as a single concise line that is easy to understand.
- Use `<scope>: <desc>` — scope is the affected task (`do_coverage:`, `do_checktest:`) or class/file (`cmaketest:`, `selftest:`); prefix `#NNN ` for a GitLab issue/MR.

## Bitbake Task Quick Reference

```bash
bitbake <recipe> -c test           # Unit tests
bitbake <recipe> -c coverage       # Code coverage
bitbake <recipe> -c checktest      # Mutation testing
bitbake <recipe> -c verify         # All of the above consolidated
# Add 'all' suffix for recursive variants: testall, coverageall, etc.
```
