function(set_crosscompiling_emulator)
  if(NOT DEFINED ENV{OECORE_TARGET_ARCH})
    message(FATAL_ERROR "Environment variable not defined: OECORE_TARGET_ARCH")
  endif()

  set(QEMU_$ENV{OECORE_TARGET_ARCH} "qemu-$ENV{OECORE_TARGET_ARCH}")
  set(QEMU_i486 "qemu-i386")
  set(QEMU_i586 "qemu-i386")
  set(QEMU_i686 "qemu-i386")
  set(QEMU_powerpc "qemu-ppc")
  set(QEMU_powerpc64 "qemu-ppc64")

  separate_arguments(QEMU_EXTRAOPTIONS UNIX_COMMAND "$ENV{QEMU_EXTRAOPTIONS}")

  set(CMAKE_CROSSCOMPILING_EMULATOR "${QEMU_$ENV{OECORE_TARGET_ARCH}};${QEMU_EXTRAOPTIONS};-L;$ENV{SDKTARGETSYSROOT};-E;LD_LIBRARY_PATH=$ENV{SDKTARGETSYSROOT}/usr/lib:$ENV{SDKTARGETSYSROOT}/lib:$LD_LIBRARY_PATH" PARENT_SCOPE)
endfunction()

set_crosscompiling_emulator()
