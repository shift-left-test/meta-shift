meta-shift
==========

[![Build Status](http://10.177.233.77:8080/buildStatus/icon?job=meta-testing)](http://10.177.233.77:8080/job/meta-testing/)

> Shift-left testing project for the Yocto project


About
-----

This project aims to support the practice of [shift-left testing](https://en.wikipedia.org/wiki/Shift-left_testing) by providing a group of dev/test tools for the Yocto project.


Supported tools
---------------

* cppcheck (1.90)
* cpplint (1.4.5)
* gtest (via meta-openembedded)
* gmock (via meta-openembedded)
* qemu-native (via meta)
* gcovr (3.4)
* doxygen (1.8.17)
* cmake (via meta)
* CMakeUtils


Requirements
------------

The following meta-layers are necessary in order to install the tools provided by this meta-layer

* meta-oe (meta-openembedded)
* meta-python (meta-openembedded)


How to add the layer to your build
----------------------------------

    $ git clone http://mod.lge.com/hub/yocto/meta-shift.git
    $ bitbake-layers add-layer meta-shift


How to run tests
----------------

The following command runs all tests

    $ py.test test/

You may also run an individual test suite by executing the python test script directly


Licenses
--------

This project source code is available under MIT license. See [LICENSE](LICENSE).
