# OPENSSL_ROOT_DIR, CMAKE_PREFIX_PATH and CMAKE_TOOLCHAIN_FILE remain caller
# controlled. In particular, do not bake a developer's Linux paths into cache.
find_package(OpenSSL REQUIRED)
find_package(Threads REQUIRED)
find_package(unofficial-libvpx CONFIG REQUIRED)
# Use the pinned libaom source and its platform-aware CMake build.
set(ENABLE_TESTS OFF CACHE BOOL "" FORCE)
set(ENABLE_TESTDATA OFF CACHE BOOL "" FORCE)
set(ENABLE_EXAMPLES OFF CACHE BOOL "" FORCE)
set(ENABLE_TOOLS OFF CACHE BOOL "" FORCE)
set(ENABLE_DOCS OFF CACHE BOOL "" FORCE)
set(CONFIG_AV1_DECODER 0 CACHE STRING "" FORCE)
set(CONFIG_LIBYUV 0 CACHE STRING "" FORCE)
set(CMAKE_POLICY_VERSION_MINIMUM 3.5)
add_subdirectory("${WEBRTC_ROOT}/third_party/libaom/source/libaom"
    "${CMAKE_CURRENT_BINARY_DIR}/third_party/aom" EXCLUDE_FROM_ALL)
target_include_directories(aom PUBLIC
    "$<BUILD_INTERFACE:${WEBRTC_ROOT}/third_party/libaom/source/libaom>")

# dav1d does not ship a CMake config. Keep Debug/Release libraries separate for
# MSVC runtime compatibility; CMAKE_PREFIX_PATH can point at a non-vcpkg prefix.
find_path(DAV1D_INCLUDE_DIR NAMES dav1d/dav1d.h REQUIRED)
find_library(DAV1D_LIBRARY_RELEASE NAMES dav1d libdav1d
    HINTS "${DAV1D_INCLUDE_DIR}/../lib" NO_DEFAULT_PATH)
find_library(DAV1D_LIBRARY_RELEASE NAMES dav1d libdav1d REQUIRED)
find_library(DAV1D_LIBRARY_DEBUG NAMES dav1d libdav1d
    HINTS "${DAV1D_INCLUDE_DIR}/../debug/lib" NO_DEFAULT_PATH)
include(SelectLibraryConfigurations)
select_library_configurations(DAV1D)
add_library(webrtc_dav1d INTERFACE)
target_include_directories(webrtc_dav1d INTERFACE "${DAV1D_INCLUDE_DIR}")
target_link_libraries(webrtc_dav1d INTERFACE ${DAV1D_LIBRARIES})

add_subdirectory("${WEBRTC_ROOT}/third_party/libsrtp" EXCLUDE_FROM_ALL)
set(UNIT_TEST OFF CACHE BOOL "" FORCE)
add_subdirectory("${WEBRTC_ROOT}/third_party/libyuv" EXCLUDE_FROM_ALL)
add_subdirectory("${WEBRTC_ROOT}/third_party/opus" EXCLUDE_FROM_ALL)

set(ABSL_PROPAGATE_CXX_STD ON CACHE BOOL "" FORCE)
set(ABSL_BUILD_TESTING OFF CACHE BOOL "" FORCE)
if(CMAKE_MSVC_RUNTIME_LIBRARY AND NOT CMAKE_MSVC_RUNTIME_LIBRARY MATCHES "DLL")
    set(ABSL_MSVC_STATIC_RUNTIME ON CACHE BOOL "" FORCE)
endif()
add_subdirectory("${WEBRTC_ROOT}/third_party/abseil-cpp" EXCLUDE_FROM_ALL)

set(JSONCPP_WITH_TESTS OFF CACHE BOOL "" FORCE)
set(JSONCPP_WITH_POST_BUILD_UNITTEST OFF CACHE BOOL "" FORCE)
set(JSONCPP_WITH_PKGCONFIG_SUPPORT OFF CACHE BOOL "" FORCE)
set(BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)
set(BUILD_STATIC_LIBS ON CACHE BOOL "" FORCE)
add_subdirectory("${WEBRTC_ROOT}/third_party/jsoncpp/source" EXCLUDE_FROM_ALL)

# This vendored revision predates CMake 4's minimum policy compatibility.
set(CMAKE_POLICY_VERSION_MINIMUM 3.5)
set(CRC32C_BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(CRC32C_BUILD_BENCHMARKS OFF CACHE BOOL "" FORCE)
set(CRC32C_USE_GLOG OFF CACHE BOOL "" FORCE)
add_subdirectory("${WEBRTC_ROOT}/third_party/crc32c/src" EXCLUDE_FROM_ALL)

add_library(webrtc_pffft STATIC "${WEBRTC_ROOT}/third_party/pffft/src/pffft.c")
add_library(webrtc_rnnoise STATIC "${WEBRTC_ROOT}/third_party/rnnoise/src/rnn_vad_weights.cc")
target_include_directories(webrtc_rnnoise PRIVATE "${WEBRTC_ROOT}")
