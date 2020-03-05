#!/usr/bin/python

import os
import shutil
import subprocess
import tempfile
import unittest
import re


class YoctoTestCase(unittest.TestCase):
    RUN_SH = os.path.join(os.path.dirname(__file__), "run.sh")
    BITBAKE_S_SH = os.path.join(os.path.dirname(__file__), "bitbake-s.sh")
    WORKDIR = os.path.join(tempfile.gettempdir(), "test_meta-testing")
    SDK_HOST_PACKAGES = ""
    SDK_TARGET_PACKAGES = ""
    BITBAKE_RECIPES = ""

    @classmethod
    def setUpClass(cls):
        def readFile(path):
            with open(path, "r") as f:
                return f.read()

        def execute(command):
            proc = subprocess.Popen(command, shell = True,
                                    stdout = subprocess.PIPE,
                                    stderr = subprocess.PIPE)
            return proc.communicate()

        if os.path.exists(YoctoTestCase.WORKDIR):
            print "Remove the existing work directory: %s" % YoctoTestCase.WORKDIR
            shutil.rmtree(YoctoTestCase.WORKDIR)
        
        command = "%s %s" % (YoctoTestCase.RUN_SH, YoctoTestCase.WORKDIR)
        proc = subprocess.Popen(command, shell = True)
        proc.wait()


        host_manifest = "tmp/deploy/sdk/poky-glibc-x86_64-core-image-minimal-aarch64-qemuarm64-toolchain-3.0.2.host.manifest"
        target_manifest  = "tmp/deploy/sdk/poky-glibc-x86_64-core-image-minimal-aarch64-qemuarm64-toolchain-3.0.2.target.manifest"
        YoctoTestCase.SDK_HOST_PACKAGES = readFile(os.path.join(YoctoTestCase.WORKDIR, host_manifest))
        YoctoTestCase.SDK_TARGET_PACKAGES = readFile(os.path.join(YoctoTestCase.WORKDIR, target_manifest))
        YoctoTestCase.BITBAKE_RECIPES = execute("%s %s" % (YoctoTestCase.BITBAKE_S_SH, YoctoTestCase.WORKDIR))[0]

        
    def testCppcheckRecipeAvailable(self):
        assert "cppcheck" in self.BITBAKE_RECIPES
        assert "cppcheck-native" in self.BITBAKE_RECIPES
        assert "nativesdk-cppcheck" in self.BITBAKE_RECIPES

    def testCppcheckRecipeFoundInSDKPackages(self):
        assert "nativesdk-cppcheck x86_64_nativesdk 1.90" in self.SDK_HOST_PACKAGES

    def testCpplintRecipeAvailable(self):
        assert "cpplint" in self.BITBAKE_RECIPES
        assert "cpplint-native" in self.BITBAKE_RECIPES
        assert "nativesdk-cpplint" in self.BITBAKE_RECIPES

    def testCpplintRecipeFoundInSDKPackages(self):
        assert "nativesdk-cpplint x86_64_nativesdk 1.4.5" in self.SDK_HOST_PACKAGES

    def testGcovrRecipeAvailable(self):
        assert "gcovr" in self.BITBAKE_RECIPES
        assert "gcovr-native" in self.BITBAKE_RECIPES
        assert "nativesdk-gcovr" in self.BITBAKE_RECIPES

    def testGcovrRecipeFoundInSDKPackages(self):
        assert "nativesdk-gcovr x86_64_nativesdk 4.2" in self.SDK_HOST_PACKAGES

    def testGoogleTestRecipeAvailable(self):
        assert "googletest" in self.BITBAKE_RECIPES
        assert "googletest-native" in self.BITBAKE_RECIPES
        assert "nativesdk-googletest" in self.BITBAKE_RECIPES

    @unittest.skip("WIP: googletest recipe")
    def testGoogleTestRecipeFoundInSDKPackages(self):
        assert "nativesdk-googletest x86_64_nativesdk 1.10.0" in self.SDK_HOST_PACKAGES

        
if __name__ == "__main__":
    unittest.main()
    
