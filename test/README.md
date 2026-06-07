meta-shift-test
===============

These files exercise the features of the meta-shift layer under different
configurations. Each test drives a **real bitbake build** (test / coverage /
mutation / the consolidated `verify` task) in the host build environment, so a
Yocto-capable Linux host with the usual build dependencies is required.


Requirements
------------

* python 3
* pytest
* a Yocto-capable host (git, the standard OE-core build host packages, network
  access to clone the layers listed in `mini-mcf.py`)


How to configure
----------------

Caching the downloads and sstate greatly reduces repeated run time:

    $ export DL_DIR=$HOME/build-res/downloads
    $ export SSTATE_DIR=$HOME/build-res/sstate-cache


How to run tests
----------------

    $ pytest
    $ pytest -s -v
    $ pytest <test filename>

Note: collection works without a build (`pytest --collect-only`), but executing
a test clones a workspace and runs bitbake, which is slow on a cold cache.


How to prepare a workspace
--------------------------

`mini-mcf.py` clones the layers and writes a build configuration so you can
reproduce a test result by hand:

    $ ./mini-mcf.py -c conf/test.conf

Configuration files in `conf/`:

* `release.conf` - core layers only (the lighter fixtures).
* `test.conf`    - full layer set with test/coverage support enabled.
* `verify.conf`  - drives the consolidated `verify` task (test + coverage +
  mutation) and the report fixtures.


pytest
------

See the [pytest website](https://docs.pytest.org/en/latest/) for details on the
test runner.
