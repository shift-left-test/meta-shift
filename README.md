meta-shift
==========

[![Build Status](http://10.177.233.77:8080/buildStatus/icon?job=meta-shift)](http://10.177.233.77:8080/job/meta-shift/)

> Shift-left testing project for the Yocto project


About
-----

This project aims to support the practice of [shift-left testing](https://en.wikipedia.org/wiki/Shift-left_testing) by providing a group of dev/test tools for the Yocto project.


Supported tools
---------------

* cppcheck (2.0)
* cpplint (1.4.5)
* fff (1.0)
* gtest (via meta-oe)
* gmock (via meta-oe)
* qemu-native (via meta)
* gcovr (3.4)
* lcov (via meta-oe)
* autotools (via meta)
* cmake (via meta)
* qmake5 (via meta-qt5)
* CMakeUtils


Features
--------

List of the tasks supported

* do_test
* do_testall
* do_coverage
* do_coverageall
* do_checkcode
* do_checkcodeall
* do_purgeall

List of bitbake tools supported

* bitbake-layers test-layers
* recipetool check
* recipetool inspect


Requirements
------------

The following meta-layers are necessary in order to install the tools provided by this meta-layer

* meta-oe (meta-openembedded)
* meta-python (meta-openembedded)
* meta-qt5 (meta-qt5)


How to add the layer to your build
----------------------------------

    $ git clone http://mod.lge.com/hub/yocto/meta-shift.git
    $ bitbake-layers add-layer meta-shift


How to run tests
----------------

The following command runs all tests

    $ py.test


Documentation
-------------

Please refer to the [wiki link](http://mod.lge.com/hub/yocto/meta-shift/-/wikis/home) for more useful information.


Licenses
--------

This project source code is available under MIT license. See [LICENSE](LICENSE).
