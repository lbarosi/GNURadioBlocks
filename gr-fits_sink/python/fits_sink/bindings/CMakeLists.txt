# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT fits_sink_sources)
    MESSAGE(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT fits_sink_sources)

########################################################################
# Check for pygccxml
########################################################################
GR_PYTHON_CHECK_MODULE_RAW(
    "pygccxml"
    "import pygccxml"
    PYGCCXML_FOUND
    )

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND fits_sink_python_files
    python_bindings.cc)

GR_PYBIND_MAKE_OOT(fits_sink
   ../../..
   gr::fits_sink
   "${fits_sink_python_files}")

# copy in bindings .so file for use in QA test module
add_custom_target(
  copy_bindings_for_tests ALL
  COMMAND
    ${CMAKE_COMMAND} -E copy "${CMAKE_CURRENT_BINARY_DIR}/*.so"
    ${CMAKE_BINARY_DIR}/test_modules/gnuradio/fits_sink/
  DEPENDS fits_sink_python)

install(TARGETS fits_sink_python DESTINATION ${GR_PYTHON_DIR}/gnuradio/fits_sink COMPONENT pythonapi)
