# CMake generated Testfile for 
# Source directory: /home/lbarosi/BAROSI/HOME/6000_PYTHONIA/2_Doing/Clones/GNURadioBlocks/gr-fits_sink/python/fits_sink
# Build directory: /home/lbarosi/BAROSI/HOME/6000_PYTHONIA/2_Doing/Clones/GNURadioBlocks/gr-fits_sink/build/python/fits_sink
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(qa_fits_sink "/usr/bin/sh" "qa_fits_sink_test.sh")
set_tests_properties(qa_fits_sink PROPERTIES  _BACKTRACE_TRIPLES "/opt/miniconda3/envs/gnuradio310/lib/cmake/gnuradio/GrTest.cmake;116;add_test;/home/lbarosi/BAROSI/HOME/6000_PYTHONIA/2_Doing/Clones/GNURadioBlocks/gr-fits_sink/python/fits_sink/CMakeLists.txt;42;GR_ADD_TEST;/home/lbarosi/BAROSI/HOME/6000_PYTHONIA/2_Doing/Clones/GNURadioBlocks/gr-fits_sink/python/fits_sink/CMakeLists.txt;0;")
subdirs("bindings")
