#!/usr/bin/python

import yoctotest
import unittest


class YoctoZeusTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        YoctoZeusTestCase.ENV = yoctotest.YoctoTestEnvironment("zeus")

    def setUp(self):
        self.recipes = self.ENV.shell().execute("bitbake -s").stdout
        self.sdk_buildlist = self.ENV.sdk().buildlist()

    @unittest.skip("WIP")
    def testCppProjectBuildable(self):
        assert self.ENV.shell().execute("bitbake cpp-project").stderr.empty()
        
    def testCppcheckFound(self):
        assert self.recipes.contains("cppcheck")
        assert self.recipes.contains("cppcheck-native")
        assert self.recipes.contains("nativesdk-cppcheck")
        assert "nativesdk-cppcheck" in self.sdk_buildlist

    def testCpplintFoundInRecipes(self):
        assert self.recipes.contains("cpplint")
        assert self.recipes.contains("cpplint-native")
        assert self.recipes.contains("nativesdk-cpplint")
        assert "nativesdk-cpplint" in self.sdk_buildlist

    def testGcovrFoundInRecipes(self):
        assert self.recipes.contains("gcovr")
        assert self.recipes.contains("gcovr-native")
        assert self.recipes.contains("nativesdk-gcovr")
        assert "nativesdk-gcovr" in self.sdk_buildlist

    def testGoogleTestFoundInRecipes(self):
        assert self.recipes.contains("googletest")
        assert self.recipes.contains("googletest-native")
        assert self.recipes.contains("nativesdk-googletest")
        # assert "googletest" in self.sdk_buildlist


if __name__ == "__main__":
    unittest.main()
