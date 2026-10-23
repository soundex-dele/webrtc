# The current source manifest includes x86 SIMD implementations.
if(NOT CMAKE_SIZEOF_VOID_P EQUAL 8 OR
   NOT CMAKE_SYSTEM_PROCESSOR MATCHES "^(AMD64|amd64|x86_64)$")
    message(FATAL_ERROR "This CMake build currently supports x64 only.")
endif()
if(NOT WIN32 AND NOT CMAKE_SYSTEM_NAME STREQUAL "Linux")
    message(FATAL_ERROR "This CMake build supports Windows and Linux.")
endif()

if(MSVC)
    add_compile_options("$<$<COMPILE_LANGUAGE:C,CXX>:/W3;/bigobj;/utf-8>"
        "$<$<COMPILE_LANGUAGE:CXX>:/permissive->")
    set(WEBRTC_AVX2_FLAGS /arch:AVX2)
else()
    add_compile_options("$<$<COMPILE_LANGUAGE:C,CXX>:-Wall;-msse3;-fvisibility=hidden>")
    set(WEBRTC_AVX2_FLAGS -mavx2 -mfma)
endif()
if(WIN32)
    add_compile_definitions(WEBRTC_WIN WIN32_LEAN_AND_MEAN NOMINMAX
        _CRT_SECURE_NO_WARNINGS _USE_MATH_DEFINES
        _WIN32_WINNT=0x0A00 WINVER=0x0A00)
else()
    add_compile_definitions(WEBRTC_POSIX WEBRTC_LINUX WEBRTC_DUMMY_FILE_DEVICES
        _FILE_OFFSET_BITS=64 _LARGEFILE_SOURCE _LARGEFILE64_SOURCE
        HAVE_PTHREAD HAVE_NETINET_IN_H HAVE_ARPA_INET_H HAVE_UNISTD_H
        SRTP_LINUX)
endif()
