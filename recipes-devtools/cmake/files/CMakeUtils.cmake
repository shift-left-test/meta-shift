# Copyright (c) 2019 LG Electronics Inc.
# SPDX-License-Identifier: MIT

cmake_minimum_required(VERSION 3.3 FATAL_ERROR)

# Prevent from multiple inclusion
if(DEFINED CMAKEUTILS_INCLUDED)
  return()
endif()

set(CMAKEUTILS_INCLUDED ON)

include(CMakeParseArguments)
include(GNUInstallDirs)

# Save the compile commands as a file
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Set sysroot if avaiable
if(DEFINED ENV{OECORE_TARGET_SYSROOT})
  set(CMAKE_SYSROOT $ENV{OECORE_TARGET_SYSROOT})
endif()

# Show cross-compiling emulator if available
if(DEFINED CMAKE_CROSSCOMPILING_EMULATOR)
  message(STATUS "Found cross-compiling emulator: TRUE")
else()
  message(STATUS "Found cross-compiling emulator: FALSE")
endif()

# Set the default build type
macro(set_default_build_type BUILD_TYPE)
  if(NOT CMAKE_CONFIGURATION_TYPES AND NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE ${BUILD_TYPE})
  endif()
  message(STATUS "Build Type: ${CMAKE_BUILD_TYPE}")
endmacro()

# Macro to set C standard flags
macro(set_c_standard VERSION)
  set(CMAKE_C_STANDARD_REQUIRED ON)
  set(CMAKE_C_STANDARD ${VERSION})
  set(CMAKE_C_EXTENSIONS OFF)
endmacro()

# Macro to set CXX standard flags
macro(set_cxx_standard VERSION)
  set(CMAKE_CXX_STANDARD_REQUIRED ON)
  set(CMAKE_CXX_STANDARD ${VERSION})
  set(CMAKE_CXX_EXTENSIONS OFF)
endmacro()

# Macro to include all CMakeLists.txt under subdirectories.
macro(add_all_subdirectories)
  file(GLOB_RECURSE allListFiles LIST_DIRECTORIES False "CMakeLists.txt")
  list(REMOVE_ITEM allListFiles "${CMAKE_SOURCE_DIR}/CMakeLists.txt")
  foreach(listFile ${allListFiles})
    get_filename_component(listDirectory ${listFile} DIRECTORY)
    add_subdirectory(${listDirectory})
  endforeach()
endmacro()

# An helper function to build libraries
function(build_library)
  set(options EXTERNAL NO_INSTALL)
  set(oneValueArgs TYPE NAME PREFIX SUFFIX VERSION ALIAS)
  set(multiValueArgs SRCS LIBS PUBLIC_HEADERS PUBLIC_SYSTEM_HEADERS PRIVATE_HEADERS PRIVATE_SYSTEM_HEADERS INSTALL_HEADERS CFLAGS CPPFLAGS CXXFLAGS COMPILE_OPTIONS LINK_OPTIONS)
  cmake_parse_arguments(BUILD
    "${options}"
    "${oneValueArgs}"
    "${multiValueArgs}"
    ${ARGN})

  string(TOUPPER "${BUILD_TYPE}" BUILD_TYPE)
  add_library(${BUILD_NAME} ${BUILD_TYPE} ${BUILD_SRCS})

  if(BUILD_EXTERNAL)
    set(SYSTEM_HEADER_FLAG "SYSTEM")
  endif()

  if(BUILD_PUBLIC_HEADERS OR BUILD_PRIVATE_HEADERS)
    target_include_directories(${BUILD_NAME}
      ${SYSTEM_HEADER_FLAG}
      PUBLIC ${BUILD_PUBLIC_HEADERS}
      PRIVATE ${BUILD_PRIVATE_HEADERS})
  endif()

  if(BUILD_PUBLIC_SYSTEM_HEADERS OR BUILD_PRIVATE_SYSTEM_HEADERS)
    target_include_directories(${BUILD_NAME}
      "SYSTEM"
      PUBLIC ${BUILD_PUBLIC_SYSTEM_HEADERS}
      PRIVATE ${BUILD_PRIVATE_SYSTEM_HEADERS})
  endif()

  if(BUILD_INSTALL_HEADERS)
    foreach(dir ${BUILD_INSTALL_HEADERS})
      install(DIRECTORY ${dir} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
    endforeach()
  endif()

  if(NOT BUILD_NO_INSTALL)
    install(
      TARGETS ${BUILD_NAME}
      RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
      LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
      ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR})
  endif()

  if(BUILD_ALIAS)
    add_library(${BUILD_ALIAS}::lib ALIAS ${BUILD_NAME})
  else()
    add_library(${BUILD_NAME}::lib ALIAS ${BUILD_NAME})
  endif()

  if(BUILD_EXTERNAL)
    set_target_properties(
      ${BUILD_NAME} PROPERTIES
      CXX_CLANG_TIDY ""
      CXX_CPPCHECK ""
      CXX_CPPLINT ""
      CXX_INCLUDE_WHAT_YOU_USE ""
      CXX_LINK_WHAT_YOU_USE OFF
    )
  endif()

  if(BUILD_PREFIX)
    set_target_properties(${BUILD_NAME} PROPERTIES PREFIX ${BUILD_PREFIX})
  endif()

  if(BUILD_SUFFIX)
    set_target_properties(${BUILD_NAME} PROPERTIES SUFFIX ${BUILD_SUFFIX})
  endif()

  if(BUILD_VERSION)
    string(REGEX REPLACE "([0-9]+).[0-9]+.[0-9]+" "\\1" BUILD_VERSION_MAJOR
      ${BUILD_VERSION})
    set_target_properties(${BUILD_NAME} PROPERTIES
      VERSION ${BUILD_VERSION}
      SOVERSION ${BUILD_VERSION_MAJOR})
  endif()

  if(BUILD_CFLAGS)
    target_compile_definitions(${BUILD_NAME} PUBLIC ${BUILD_CFLAGS})
  endif()

  if(BUILD_CPPFLAGS)
    target_compile_definitions(${BUILD_NAME} PUBLIC ${BUILD_CPPFLAGS})
  endif()

  if(BUILD_CXXFLAGS)
    target_compile_definitions(${BUILD_NAME} PUBLIC ${BUILD_CXXFLAGS})
  endif()

  if(BUILD_COMPILE_OPTIONS)
    target_compile_options(${BUILD_NAME} PRIVATE ${BUILD_COMPILE_OPTIONS})
  endif()

  if(BUILD_LINK_OPTIONS)
    set_property(TARGET ${BUILD_NAME} APPEND_STRING PROPERTY LINK_FLAGS " ${BUILD_LINK_OPTIONS}")
  endif()

  if(BUILD_LIBS)
    target_link_libraries(${BUILD_NAME} PUBLIC ${BUILD_LIBS})
  endif()
endfunction()

macro(build_shared_library)
  build_library(TYPE shared ${ARGN})
endmacro()

macro(build_external_shared_library)
  build_library(TYPE shared EXTERNAL ${ARGN})
endmacro()

macro(build_static_library)
  build_library(TYPE static ${ARGN})
endmacro(build_static_library)

macro(build_external_static_library)
  build_library(TYPE static EXTERNAL ${ARGN})
endmacro()


# An helper function to build executables
function(build_executable)
  set(options NO_INSTALL)
  set(oneValueArgs TYPE NAME PREFIX SUFFIX VERSION ALIAS)
  set(multiValueArgs SRCS LIBS PUBLIC_HEADERS PUBLIC_SYSTEM_HEADERS PRIVATE_HEADERS PRIVATE_SYSTEM_HEADERS CFLAGS CPPFLAGS CXXFLAGS COMPILE_OPTIONS LINK_OPTIONS)
  cmake_parse_arguments(BUILD
    "${options}"
    "${oneValueArgs}"
    "${multiValueArgs}"
    ${ARGN})

  string(TOUPPER "${BUILD_TYPE}" BUILD_TYPE)

  add_executable(${BUILD_NAME} ${BUILD_SRCS})

  if(BUILD_PUBLIC_HEADERS OR BUILD_PRIVATE_HEADERS)
    target_include_directories(${BUILD_NAME}
      PUBLIC ${BUILD_PUBLIC_HEADERS}
      PRIVATE ${BUILD_PRIVATE_HEADERS})
  endif()

  if(BUILD_PUBLIC_SYSTEM_HEADERS OR BUILD_PRIVATE_SYSTEM_HEADERS)
    target_include_directories(${BUILD_NAME}
      "SYSTEM"
      PUBLIC ${BUILD_PUBLIC_SYSTEM_HEADERS}
      PRIVATE ${BUILD_PRIVATE_SYSTEM_HEADERS})
  endif()

  if(DEFINED CMAKE_CXX_STANDARD)
    set(CXX_STANDARD_VALUE ${CMAKE_CXX_STANDARD})
  else()
    set(CXX_STANDARD_VALUE 14)
  endif()

  if(BUILD_TYPE STREQUAL "TEST")
    find_package(Threads REQUIRED)
    find_package(GTest REQUIRED)
    find_package(GMock QUIET)

    if(GMock_FOUND)
      message(STATUS "Found GMock: ${GMOCK_LIBRARIES}")
      set(MAIN_LIBRARIES GMock::Main)
    else()
      message(STATUS "Found GMock: FALSE")
      set(MAIN_LIBRARIES ${GTEST_MAIN_LIBRARIES})
    endif()

    set_target_properties(${BUILD_NAME} PROPERTIES
      CXX_STANDARD ${CXX_STANDARD_VALUE}
      CXX_STANDARD_REQUIRED ON
      CXX_EXTENSIONS OFF
    )

    target_include_directories(${BUILD_NAME}
      PRIVATE ${GTEST_INCLUDE_DIRS} ${GMOCK_INCLUDE_DIRS})
    target_link_libraries(${BUILD_NAME}
      PRIVATE ${GTEST_LIBRARIES} ${GMOCK_LIBRARIES} ${MAIN_LIBRARIES} ${CMAKE_THREAD_LIBS_INIT})
    gtest_add_tests(${BUILD_NAME} "" AUTO)
  else()
    if(NOT BUILD_NO_INSTALL)
      install(
	TARGETS ${BUILD_NAME}
	RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
    endif()
  endif()

  if(BUILD_PREFIX)
    set_target_properties(${BUILD_NAME} PROPERTIES PREFIX ${BUILD_PREFIX})
  endif()

  if(BUILD_SUFFIX)
    set_target_properties(${BUILD_NAME} PROPERTIES SUFFIX ${BUILD_SUFFIX})
  endif()

  if(BUILD_VERSION)
    message(WARNING "Unsupported variable VERSION found at ${CMAKE_CURRENT_LIST_FILE}")
  endif()

  if(BUILD_ALIAS)
    message(WARNING "Unsupported variable ALIAS found at ${CMAKE_CURRENT_LIST_FILE}")
  endif()

  if(BUILD_CFLAGS)
    target_compile_definitions(${BUILD_NAME} PUBLIC ${BUILD_CFLAGS})
  endif()

  if(BUILD_CPPFLAGS)
    target_compile_definitions(${BUILD_NAME} PUBLIC ${BUILD_CPPFLAGS})
  endif()

  if(BUILD_CXXFLAGS)
    target_compile_definitions(${BUILD_NAME} PUBLIC ${BUILD_CXXFLAGS})
  endif()

  if(BUILD_COMPILE_OPTIONS)
    target_compile_options(${BUILD_NAME} PRIVATE ${BUILD_COMPILE_OPTIONS})
  endif()

  if(BUILD_LINK_OPTIONS)
    set_property(TARGET ${BUILD_NAME} APPEND_STRING PROPERTY LINK_FLAGS " ${BUILD_LINK_OPTIONS}")
  endif()

  if(BUILD_LIBS)
    target_link_libraries(${BUILD_NAME} PUBLIC ${BUILD_LIBS})
  endif()

endfunction()

macro(build_program)
  build_executable(TYPE program ${ARGN})
endmacro()

macro(build_test_program)
  build_executable(TYPE test ${ARGN})
endmacro()

# An helper function to manage header-only interfaces
function(build_interface)
  set(options EXTERNAL NO_INSTALL)
  set(oneValueArgs NAME ALIAS)
  set(multiValueArgs SRCS LIBS PUBLIC_HEADERS PUBLIC_SYSTEM_HEADERS PRIVATE_HEADERS PRIVATE_SYSTEM_HEADERS INSTALL_HEADERS CFLAGS CPPFLAGS CXXFLAGS COMPILE_OPTIONS LINK_OPTIONS)
  cmake_parse_arguments(BUILD
    "${options}"
    "${oneValueArgs}"
    "${multiValueArgs}"
    ${ARGN})

  add_library(${BUILD_NAME} INTERFACE)

  if(BUILD_EXTERNAL)
    set(SYSTEM_HEADER_FLAG "SYSTEM")
  endif()

  if(BUILD_PUBLIC_HEADERS OR BUILD_PRIVATE_HEADERS)
    target_include_directories(${BUILD_NAME}
      ${SYSTEM_HEADER_FLAG}
      INTERFACE ${BUILD_PUBLIC_HEADERS} ${BUILD_PRIVATE_HEADERS})
  endif()

  if(BUILD_PUBLIC_SYSTEM_HEADERS OR BUILD_PRIVATE_SYSTEM_HEADERS)
    target_include_directories(${BUILD_NAME}
      "SYSTEM"
      INTERFACE ${BUILD_PUBLIC_SYSTEM_HEADERS} ${BUILD_PRIVATE_SYSTEM_HEADERS})
  endif()

  if(BUILD_INSTALL_HEADERS)
    foreach(dir ${BUILD_INSTALL_HEADERS})
      install(DIRECTORY ${dir} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
    endforeach()
  endif()

  if(NOT BUILD_NO_INSTALL)
    install(
      TARGETS ${BUILD_NAME}
      RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
      LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
      ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR})
  endif()

  if(BUILD_ALIAS)
    add_library(${BUILD_ALIAS}::lib ALIAS ${BUILD_NAME})
  else()
    add_library(${BUILD_NAME}::lib ALIAS ${BUILD_NAME})
  endif()

  if(BUILD_CFLAGS)
    target_compile_definitions(${BUILD_NAME} INTERFACE ${BUILD_CFLAGS})
  endif()

  if(BUILD_CPPFLAGS)
    target_compile_definitions(${BUILD_NAME} INTERFACE ${BUILD_CPPFLAGS})
  endif()

  if(BUILD_CXXFLAGS)
    target_compile_definitions(${BUILD_NAME} INTERFACE ${BUILD_CXXFLAGS})
  endif()

  if(BUILD_COMPILE_OPTIONS)
    target_compile_options(${BUILD_NAME} PRIVATE ${BUILD_COMPILE_OPTIONS})
  endif()

  if(BUILD_LINK_OPTIONS)
    set_property(TARGET ${BUILD_NAME} APPEND_STRING PROPERTY LINK_FLAGS " ${BUILD_LINK_OPTIONS}")
  endif()

  if(BUILD_LIBS)
    target_link_libraries(${BUILD_NAME} INTERFACE ${BUILD_LIBS})
  endif()
endfunction()

macro(build_interface_library)
  build_interface(${ARGN})
endmacro()

macro(build_external_interface_library)
  build_interface(EXTERNAL ${ARGN})
endmacro()

function(build_debian_package)
  set(oneValueArgs MAINTAINER CONTACT HOMEPAGE VENDOR SUMMARY SECTION PRIORITY)
  set(multiValueArgs DEPENDS)
  cmake_parse_arguments(PKG
    ""
    "${oneValueArgs}"
    "${multiValueArgs}"
    ${ARGN})

  set(CPACK_GENERATOR DEB)

  if(PKG_MAINTAINER)
    set(CPACK_DEBIAN_PACKAGE_MAINTAINER ${PKG_MAINTAINER})
  endif()

  if(PKG_CONTACT)
    set(CPACK_DEBIAN_PACKAGE_CONTACT ${PKG_CONTACT})
  endif()

  if(PKG_HOMEPAGE)
    set(CPACK_DEBIAN_PACKAGE_HOMEPAGE ${PKG_HOMEPAGE})
  endif()

  set(CPACK_PACKAGE_NAME ${PROJECT_NAME})

  if(PKG_VENDOR)
    set(CPACK_PACKAGE_VENDOR ${PKG_VENDOR})
  endif()

  set(CPACK_PACKAGE_VERSION ${PROJECT_VERSION})

  if(PKG_SUMMARY)
    set(CPACK_PACKAGE_DESCRIPTION_SUMMARY ${PKG_SUMMARY})
  endif()

  if(PKG_SECTION)
    set(CPACK_DEBIAN_PACKAGE_SECTION ${PKG_SECTION})
  endif()

  if(PKG_PRIORITY)
    set(CPACK_DEBIAN_PACKAGE_PRIORITY ${PKG_PRIORITY})
  endif()

  if(EXISTS "${CMAKE_SOURCE_DIR}/LICENSE")
    set(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_SOURCE_DIR}/LICENSE")
  elseif(EXISTS "${CMAKE_SOURCE_DIR}/LICENSE.md")
    set(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_SOURCE_DIR}/LICENSE.md")
  endif()

  if(NOT CPACK_DEBIAN_PACKAGE_ARCHITECTURE)
    find_program(DPKG_PATH dpkg)
    if(NOT DPKG_PATH)
      set(CPACK_DEBIAN_PACKAGE_ARCHITECTURE i386)
    else()
      execute_process(
	COMMAND "${DPKG_PATH}" --print-architecture
	OUTPUT_VARIABLE CPACK_DEBIAN_PACKAGE_ARCHITECTURE
	OUTPUT_STRIP_TRAILING_WHITESPACE
	)
    endif()
  endif()

  if(PKG_DEPENDS)
    set(CPACK_DEBIAN_PACKAGE_SHLIBDEPS ON)
    set(CPACK_DEBIAN_PACKAGE_DEPENDS ${PKG_DEPENDS})
  endif()

  set(CPACK_PACKAGE_FILE_NAME
    "${CPACK_PACKAGE_NAME}-${CPACK_PACKAGE_VERSION}-${CPACK_DEBIAN_PACKAGE_ARCHITECTURE}")

  include(CPack)
endfunction()

# Register the given program if available
function(register_program)
  set(oneValueArgs NAME DEPENDS)
  set(multiValueArgs PATHS NAMES OPTIONS FILES)
  cmake_parse_arguments(ARGS
    ""
    "${oneValueArgs}"
    "${multiValueArgs}"
    ${ARGN})

  find_program(${ARGS_NAME}_PROGRAM PATHS ${ARGS_PATHS} NAMES ${ARGS_NAMES})
  if(${ARGS_NAME}_PROGRAM)
    message(STATUS "Found ${ARGS_NAME} program: TRUE")
    add_custom_target(
      ${ARGS_NAME}
      COMMAND ${${ARGS_NAME}_PROGRAM} ${ARGS_OPTIONS} ${ARGS_FILES}
      COMMENT "Running ${ARGS_NAME}..."
    )
    add_dependencies(${ARGS_DEPENDS} ${ARGS_NAME})
  else()
    message(STATUS "Found ${ARGS_NAME} program: FALSE")
  endif()
endfunction()


# Helper for enabling static analysis
function(register_checker)
  set(oneValueArgs NAME VERSION)
  set(multiValueArgs PATHS NAMES OPTIONS)
  cmake_parse_arguments(ARGS
    ""
    "${oneValueArgs}"
    "${multiValueArgs}"
    ${ARGN})

  set(MESSAGE "Found ${ARGS_NAME} code checker")

  if(${CMAKE_VERSION} VERSION_LESS ${ARGS_VERSION})
    message(STATUS "${MESSAGE}: Unsupported")
    return()
  endif()

  if(DEFINED CMAKE_CXX_${ARGS_NAME} AND DEFINED CMAKE_C_${ARGS_NAME})
    message(STATUS "${MESSAGE}: TRUE")
    return()
  endif()

  if(NOT ARGS_NAMES)
    message(STATUS "${MESSAGE}: TRUE")
    set(CMAKE_CXX_${ARGS_NAME} ON PARENT_SCOPE)
    set(CMAKE_C_${ARGS_NAME} ON PARENT_SCOPE)
    return()
  endif()

  find_program(${ARGS_NAME}_PATH PATHS ${ARGS_PATHS} NAMES ${ARGS_NAMES})
  if(${ARGS_NAME}_PATH)
    message(STATUS "${MESSAGE}: TRUE")
    set(CMAKE_CXX_${ARGS_NAME}
      ${${ARGS_NAME}_PATH}
      ${ARGS_OPTIONS}
      PARENT_SCOPE)
    set(CMAKE_C_${ARGS_NAME}
      ${${ARGS_NAME}_PATH}
      ${ARGS_OPTIONS}
      PARENT_SCOPE)
  else()
    message(STATUS "${MESSAGE}: FALSE")
  endif()
endfunction()

# Enable static analysis
macro(enable_static_analysis)
  set(options clang-tidy cppcheck cpplint iwyu lwyu)
  cmake_parse_arguments(CHECKER
    "${options}"
    ""
    ""
    ${ARGN})

  if(CHECKER_clang-tidy)
    register_checker(
      NAME CLANG_TIDY
      NAMES clang-tidy
      VERSION 3.6.3)
  endif()

  if(CHECKER_cppcheck)
    register_checker(
      NAME CPPCHECK
      NAMES cppcheck
      VERSION 3.10.0
      OPTIONS --enable=warning,style,performance,portability --library=googletest --error-exitcode=1)
  endif()

  if(CHECKER_cpplint)
    register_checker(
      NAME CPPLINT
      NAMES cpplint cpplint.py
      VERSION 3.8.2)
  endif()

  if(CHECKER_iwyu)
    register_checker(
      NAME INCLUDE_WHAT_YOU_USE
      NAMES iwyu
      VERSION 3.3.2)
  endif()

  if(CHECKER_lwyu)
    register_checker(
      NAME LINK_WHAT_YOU_USE
      VERSION 3.7.0)
  endif()
endmacro()

# Enable gcovr for test coverage
function(enable_test_coverage)
  add_custom_target(coverage)

  # Set code coverage flags
  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -O0 -fprofile-arcs -ftest-coverage" PARENT_SCOPE)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O0 -fprofile-arcs -ftest-coverage" PARENT_SCOPE)

  set(options BRANCH)
  cmake_parse_arguments(ENABLE
    "${options}"
    ""
    ""
    ${ARGN})

  if(ENABLE_BRANCH)
    set(GCOVR_BRANCH_OPTION "-b")
  endif()

  register_program(
    NAME gcovr
    DEPENDS coverage
    PATHS /usr/local/bin $ENV{HOME}/.local/bin
    NAMES gcovr
    OPTIONS ${GCOVR_BRANCH_OPTION} -s -r ${CMAKE_SOURCE_DIR} --object-directory ${CMAKE_BINARY_DIR}
    FILES ""
    )
endfunction()

# Enable doxygen
function(enable_doxygen)
  find_package(Doxygen)

  if(NOT DOXYGEN_FOUND)
    message(WARNING "Unable to locate the doxygen executable")
    add_custom_target(doc)
  elseif(NOT EXISTS ${CMAKE_SOURCE_DIR}/Doxyfile)
    message(WARNING "Unable to locate the Doxyfile")
    add_custom_target(doc)
  else()
    add_custom_target(doc
      COMMAND ${DOXYGEN_EXECUTABLE} ${CMAKE_SOURCE_DIR}/Doxyfile
      WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
      COMMENT "Generating API documentation with Doxygen"
      VERBATIM
      )
  endif()
endfunction()
