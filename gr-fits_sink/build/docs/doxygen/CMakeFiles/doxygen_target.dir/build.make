# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.25

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /opt/miniconda3/envs/gnuradio310/bin/cmake

# The command to remove a file.
RM = /opt/miniconda3/envs/gnuradio310/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/bingo/clones/GNURadioBlocks/gr-fits_sink

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/bingo/clones/GNURadioBlocks/gr-fits_sink/build

# Utility rule file for doxygen_target.

# Include any custom commands dependencies for this target.
include docs/doxygen/CMakeFiles/doxygen_target.dir/compiler_depend.make

# Include the progress variables for this target.
include docs/doxygen/CMakeFiles/doxygen_target.dir/progress.make

docs/doxygen/CMakeFiles/doxygen_target: docs/doxygen/xml
docs/doxygen/CMakeFiles/doxygen_target: docs/doxygen/html

docs/doxygen/xml:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/bingo/clones/GNURadioBlocks/gr-fits_sink/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Generating documentation with doxygen"
	cd /home/bingo/clones/GNURadioBlocks/gr-fits_sink/build/docs/doxygen && /usr/bin/doxygen /home/bingo/clones/GNURadioBlocks/gr-fits_sink/build/docs/doxygen/Doxyfile

docs/doxygen/html: docs/doxygen/xml
	@$(CMAKE_COMMAND) -E touch_nocreate docs/doxygen/html

doxygen_target: docs/doxygen/CMakeFiles/doxygen_target
doxygen_target: docs/doxygen/html
doxygen_target: docs/doxygen/xml
doxygen_target: docs/doxygen/CMakeFiles/doxygen_target.dir/build.make
.PHONY : doxygen_target

# Rule to build all files generated by this target.
docs/doxygen/CMakeFiles/doxygen_target.dir/build: doxygen_target
.PHONY : docs/doxygen/CMakeFiles/doxygen_target.dir/build

docs/doxygen/CMakeFiles/doxygen_target.dir/clean:
	cd /home/bingo/clones/GNURadioBlocks/gr-fits_sink/build/docs/doxygen && $(CMAKE_COMMAND) -P CMakeFiles/doxygen_target.dir/cmake_clean.cmake
.PHONY : docs/doxygen/CMakeFiles/doxygen_target.dir/clean

docs/doxygen/CMakeFiles/doxygen_target.dir/depend:
	cd /home/bingo/clones/GNURadioBlocks/gr-fits_sink/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/bingo/clones/GNURadioBlocks/gr-fits_sink /home/bingo/clones/GNURadioBlocks/gr-fits_sink/docs/doxygen /home/bingo/clones/GNURadioBlocks/gr-fits_sink/build /home/bingo/clones/GNURadioBlocks/gr-fits_sink/build/docs/doxygen /home/bingo/clones/GNURadioBlocks/gr-fits_sink/build/docs/doxygen/CMakeFiles/doxygen_target.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : docs/doxygen/CMakeFiles/doxygen_target.dir/depend

