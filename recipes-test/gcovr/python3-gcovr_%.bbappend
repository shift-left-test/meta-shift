# meta-shift uses meta-python's upstream python3-gcovr as the coverage tool.
# Preset GCOV to the target gcov so that running gcovr inside the generated SDK
# analyses target coverage data out-of-the-box (mirrors the nativesdk behaviour
# of the previously vendored gcovr recipe).

# langdale's upstream python3-gcovr_5.2.bb pins SRC_URI to branch=master, but
# gcovr renamed its default branch from master to main and deleted master, so
# do_fetch fails with "Unable to find revision ... in branch master". langdale
# is EOL, so the upstream fix is not backported; correct the branch here. The
# SRCREV is still valid and reachable from main. (Other release branches already
# use branch=main upstream and must not be touched.)
SRC_URI = "git://github.com/gcovr/gcovr.git;branch=main;protocol=https"

FILES:${PN}:append:class-nativesdk = " ${SDKPATHNATIVE}"

do_install:append:class-nativesdk() {
    echo "export GCOV=""$""{TARGET_PREFIX}gcov" > ${WORKDIR}/gcovr.sh
    install -d ${D}${SDKPATHNATIVE}/environment-setup.d
    install -m 644 ${WORKDIR}/gcovr.sh ${D}${SDKPATHNATIVE}/environment-setup.d/gcovr.sh
}
