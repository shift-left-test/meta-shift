meta-shift-test
===============

The files in the directory are intended to test the all features of the meta-shift project with different configurations.


Requirements
------------

* python
* py.test


How to configure
----------------

It is recommended to configure cache features to save the entire test time before running the tests.
The following commands will set the cache files under your $HOME directory.

    $ export DL_DIR=$HOME/build-res/downloads
    $ export SSTATE_DIR=$HOME/build-res/sstate-cache


How to run tests
----------------

    $ py.test
    $ py.test -s -v
    $ py.test <test filename>


How to prepare workspace
------------------------

You may use the mini-mcf tool with a configuration file to setup the workspace to reproduce any test results.

    $ ./mini-mcf.py -c conf/test.conf


pytest
------

Please refer to the [pytest website](https://docs.pytest.org/en/latest/) for more information about how to use the test runner effectively.
