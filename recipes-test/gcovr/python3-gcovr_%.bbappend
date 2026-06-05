# meta-shift uses meta-python's upstream python3-gcovr as the coverage tool.
# Preset GCOV to the target gcov so that running gcovr inside the generated SDK
# analyses target coverage data out-of-the-box (mirrors the nativesdk behaviour
# of the previously vendored gcovr recipe).
FILES:${PN}:append:class-nativesdk = " ${SDKPATHNATIVE}"

do_install:append:class-nativesdk() {
    echo "export GCOV=""$""{TARGET_PREFIX}gcov" > ${WORKDIR}/gcovr.sh
    install -d ${D}${SDKPATHNATIVE}/environment-setup.d
    install -m 644 ${WORKDIR}/gcovr.sh ${D}${SDKPATHNATIVE}/environment-setup.d/gcovr.sh
}
