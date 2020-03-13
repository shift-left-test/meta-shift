#!/usr/bin/python

import logging
import os
import yoctotest
import unittest
from collections import defaultdict


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%m-%d %H:%M')
logger = logging.getLogger(__name__)


class YoctoTestCase(unittest.TestCase):
    VERSIONS = []
    DATA = defaultdict(dict)

    @classmethod
    def setUpClass(cls):
        defaultVersions = "morty,zeus"
        cls.VERSIONS = os.getenv("VERSIONS", defaultVersions).split(",")

        for version in cls.VERSIONS:
            cls.DATA[version]["env"] = yoctotest.YoctoTestEnvironment(version)

    def setUp(self):
        for version in self.VERSIONS:
            logging.info("CURRENT VERSION: {}".format(version))

            ENV = self.DATA[version]
            ENV["recipes"] = ENV["env"].shell().execute("bitbake -s").stdout
            ENV["image"] = ENV["env"].parse("core-image-minimal")
            ENV["sdk"] = ENV["env"].parse("core-image-minimal -c populate_sdk")

    def testCppProjectBuildable(self):
        for version in self.VERSIONS:
            logging.info("CURRENT VERSION: {}".format(version))

            ENV = self.DATA[version]
            assert ENV["image"].packages().contains("cpp-project")

            assert ENV["env"].shell().execute("bitbake cpp-project").stderr.empty()

            project = ENV["env"].parse("cpp-project")
            assert project.packages().contains("cppcheck-native")
            assert project.packages().contains("cpplint-native")
            assert project.packages().contains("gcovr-native")
            assert project.packages().containsAny("gtest", "googletest")

            pkgs = ENV["env"].shell().execute("oe-pkgdata-util list-pkg-files cpp-project").stdout
            assert pkgs.contains("/opt/tests/cpp-project/OperatorTest")
            assert pkgs.contains("/usr/bin/program")
            assert pkgs.contains("/usr/lib/libplus.so.1")
            assert pkgs.contains("/usr/lib/libplus.so.1.0.0")

    def testCppcheckRecipe(self):
        for version in self.VERSIONS:
            logging.info("CURRENT VERSION: {}".format(version))

            ENV = self.DATA[version]
            assert ENV["recipes"].contains("cppcheck")
            assert ENV["recipes"].contains("cppcheck-native")
            assert ENV["recipes"].contains("nativesdk-cppcheck")
            assert ENV["sdk"].packages().contains("nativesdk-cppcheck")

            assert ENV["env"].shell().execute("bitbake cppcheck-native").stderr.empty()

            native = ENV["env"].parse("cppcheck-native")
            assert native.packages().contains("libpcre-native")

    def testCpplintRecipe(self):
        for version in self.VERSIONS:
            logging.info("CURRENT VERSION: {}".format(version))

            ENV = self.DATA[version]
            assert ENV["recipes"].contains("cpplint")
            assert ENV["recipes"].contains("cpplint-native")
            assert ENV["recipes"].contains("nativesdk-cpplint")
            assert ENV["sdk"].packages().contains("nativesdk-cpplint")
            assert ENV["env"].shell().execute("bitbake cpplint-native").stderr.empty()

    def testGcovrRecipe(self):
        for version in self.VERSIONS:
            logging.info("CURRENT VERSION: {}".format(version))

            ENV = self.DATA[version]
            assert ENV["recipes"].contains("gcovr")
            assert ENV["recipes"].contains("gcovr-native")
            assert ENV["recipes"].contains("nativesdk-gcovr")
            assert ENV["sdk"].packages().contains("nativesdk-gcovr")
            assert ENV["env"].shell().execute("bitbake gcovr-native").stderr.empty()

    def testGoogleTestRecipe(self):
        for version in self.VERSIONS:
            logging.info("CURRENT VERSION: {}".format(version))

            ENV = self.DATA[version]
            assert ENV["recipes"].containsAny("gtest", "googletest")
            assert ENV["recipes"].containsAny("gtest-native", "googletest-native")
            assert ENV["recipes"].containsAny("nativesdk-gtest", "nativesdk-googletest")
            assert ENV["image"].packages().containsAny("gtest", "googletest")
            assert ENV["sdk"].packages().containsAny("gtest", "googletest")

    def testDoxygenRecipe(self):
        for version in self.VERSIONS:
            logging.info("CURRENT VERSION: {}".format(version))

            ENV = self.DATA[version]
            assert ENV["recipes"].contains("doxygen")
            assert ENV["recipes"].contains("doxygen-native")
            assert ENV["recipes"].contains("nativesdk-doxygen")
            assert ENV["sdk"].packages().contains("nativesdk-doxygen")

            assert ENV["env"].shell().execute("bitbake doxygen-native").stderr.empty()

            native = ENV["env"].parse("doxygen-native")
            assert native.packages().contains("flex-native")
            assert native.packages().contains("bison-native")

    def testCMakeUtilsRecipe(self):
        for version in self.VERSIONS:
            logging.info("CURRENT VERSION: {}".format(version))

            ENV = self.DATA[version]
            assert ENV["recipes"].contains("cmake-native")

            do_install = ENV["env"].shell().execute("bitbake -e cmake-native -c install").stdout
            assert do_install.contains("file://CMakeUtils.cmake")
            assert do_install.contains("file://FindGMock.cmake")


if __name__ == "__main__":
    unittest.main()
