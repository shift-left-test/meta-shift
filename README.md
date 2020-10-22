# meta-shift

[![Build Status](http://10.178.85.91:8080/buildStatus/icon?job=meta-shift)](http://10.178.85.91:8080/job/meta-shift/)

> Shift-left testing for the Yocto project


## About

This project aims to support the practice of [shift-left testing](https://en.wikipedia.org/wiki/Shift-left_testing) by providing a group of dev/test tools with featured tasks for the Yocto project.


## Supporting tools

* autotools (via meta)
* cmake (via meta)
* CMakeUtils (1.0.0)
* cppcheck (2.0)
* cpplint (1.4.5)
* fff (1.0)
* gcovr (3.4)
* gmock (via meta-oe)
* gtest (via meta-oe)
* lcov (via meta-oe)
* qemu-native (via meta)
* qmake5 (via meta-qt5)
* SAGE (0.2.0)


## Features

### List of tasks

* do_checkcode
* do_checkcodeall
* do_coverage
* do_coverageall
* do_test
* do_testall

### List of bitbake tools

* recipetool test-layers
* recipetool test-recipes
* recipetool check
* recipetool inspect


## Requirements

The following meta-layers are necessary in order to install the tools provided by this meta-layer

* meta-oe (meta-openembedded)
* meta-python (meta-openembedded)
* meta-qt5 (meta-qt5) [Optional]


## How to add the layer to your build

    $ git clone http://mod.lge.com/hub/yocto/meta-shift.git
    $ bitbake-layers add-layer meta-shift


## How to run tests

The following command runs all tests

    $ py.test


## How to use

Please refer to the [wiki link](http://mod.lge.com/hub/yocto/meta-shift/-/wikis/home) for more information.


## Licenses

This project source code is available under MIT license. See [LICENSE](LICENSE).
