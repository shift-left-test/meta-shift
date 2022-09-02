FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI:append = " \
    file://0001-fix-clang-tidy-failure-by-target-option.patch \
    file://0002-fix-cpplint-return-non-zero-exit-code.patch \
"
