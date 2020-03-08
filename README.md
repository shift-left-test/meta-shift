meta-testing
============

[![Build Status](http://10.177.233.77:8080/buildStatus/icon?job=meta-testing)](http://10.177.233.77:8080/job/meta-testing/)

> A shareable integrated testing framework for Yocto based projects


About
-----

This project aims to provide an easy way to set up a group of dev/test tools for Yocto based projects


Supported tools
---------------

* gtest (1.10.0)
* gmock (1.10.0)
* cppcheck (1.90)
* cpplint (1.4.5)
* CMakeUtils


Requirements
------------

The following meta-layer is necessary in order to install the python based tools

* meta-python (meta-openembedded)


How to add the layer to your build
----------------------------------

    $ git clone http://mod.lge.com/hub/yocto/meta-testing.git
    $ bitbake-layers add-layer meta-testing


How to run tests
----------------

The following command runs the tests of all supported Yocto versions

    $ ./test/run-test.py

The following command runs the tests for specific Yocto version

    $ VERSIONS=morty ./test/run-test.py


Licenses
--------

This project source code is available under MIT license. See [LICENSE](LICENSE).

