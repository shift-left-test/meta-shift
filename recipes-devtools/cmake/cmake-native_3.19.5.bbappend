FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI_append = " \
    file://0001-fix-clang-tidy-failure-by-target-option.patch \
"
