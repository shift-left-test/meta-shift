meta-testing
============

[![build status](http://mod.lge.com:40000/hub/yocto/meta-testing/badges/master/build.svg)](http://mod.lge.com:40000/hub/yocto/meta-testing/commits/master)

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


How to add the layer to your build
----------------------------------

    $ git clone http://mod.lge.com/hub/yocto/meta-testing.git
    $ bitbake-layers add-layer meta-testing


Licenses
--------

This project source code is available under MIT license. See [LICENSE](LICENSE).

