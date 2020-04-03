meta-shift
==========

[![Build Status](http://10.177.233.77:8080/buildStatus/icon?job=meta-testing)](http://10.177.233.77:8080/job/meta-testing/)

> A shareable integrated testing framework for Yocto based projects


About
-----

This project aims to provide an easy way to set up a group of dev/test tools for Yocto based projects


Supported tools
---------------

* cppcheck (1.90)
* cpplint (1.4.5)
* gtest (via meta-openembedded)
* gmock (via meta-openembedded)
* gcovr (3.4)
* doxygen (1.8.17)
* cmake (via meta)
* CMakeUtils


Requirements
------------

The following meta-layer is necessary in order to install the python based tools

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


Licenses
--------

This project source code is available under MIT license. See [LICENSE](LICENSE).
