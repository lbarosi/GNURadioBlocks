find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_FITS_SINK gnuradio-fits_sink)

FIND_PATH(
    GR_FITS_SINK_INCLUDE_DIRS
    NAMES gnuradio/fits_sink/api.h
    HINTS $ENV{FITS_SINK_DIR}/include
        ${PC_FITS_SINK_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_FITS_SINK_LIBRARIES
    NAMES gnuradio-fits_sink
    HINTS $ENV{FITS_SINK_DIR}/lib
        ${PC_FITS_SINK_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-fits_sinkTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_FITS_SINK DEFAULT_MSG GR_FITS_SINK_LIBRARIES GR_FITS_SINK_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_FITS_SINK_LIBRARIES GR_FITS_SINK_INCLUDE_DIRS)
