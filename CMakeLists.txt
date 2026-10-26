cmake_minimum_required(VERSION 3.18)
project(webrtc_peerconnection_demo LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD_REQUIRED ON)

# WebRTC M137 uses C++20 (including designated initializers).
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
include(cmake/platform.cmake)
if(APPLE)
    enable_language(OBJC OBJCXX)
    set(CMAKE_OBJCXX_STANDARD 20)
    set(CMAKE_OBJCXX_STANDARD_REQUIRED ON)
endif()

# ============================================================================
set(WEBRTC_PRIVATE_DEFINITIONS
    # Basic platform definitions
    __STDC_CONSTANT_MACROS
    __STDC_FORMAT_MACROS

    # WebRTC core definitions
    RTC_DISABLE_TRACE_EVENTS
    WEBRTC_APM_DEBUG_DUMP=0
    WEBRTC_ALLOW_DEPRECATED_NAMESPACES
    WEBRTC_ENABLE_PROTOBUF=0
    WEBRTC_HAVE_SCTP
    WEBRTC_INCLUDE_INTERNAL_AUDIO_DEVICE
    WEBRTC_LIBRARY_IMPL
    WEBRTC_NON_STATIC_TRACE_EVENT_HANDLERS=0
    WEBRTC_STRICT_FIELD_TRIALS=0
    WEBRTC_USE_BUILTIN_OPUS=1
    WEBRTC_OPUS_VARIABLE_COMPLEXITY=0
    WEBRTC_OPUS_SUPPORT_120MS_PTIME=1
    WEBRTC_CODEC_OPUS

    # Video codec support
    WEBRTC_EXTERNAL_DAV1D
    RTC_USE_LIBAOM_AV1_ENCODER
    RTC_DAV1D_IN_INTERNAL_DECODER_FACTORY
    RTC_ENABLE_VP9
    RTC_ENABLE_H265
    HAVE_WEBRTC_VIDEO

    # Disable extensions not used by this build.
    LIBYUV_DISABLE_LSX
    LIBYUV_DISABLE_LASX
    LIBYUV_DISABLE_SVE
    LIBYUV_DISABLE_SME

    # System/Platform definitions
    HAVE_LITTLE_ENDIAN
    HAVE_INTTYPES_H
    HAVE_STDINT_H
    HAVE_STDLIB_H
    HAVE_STRING_H
    HAVE_SYS_TYPES_H
    HAVE_INT8_T
    HAVE_INT16_T
    HAVE_INT32_T
    HAVE_UINT8_T
    HAVE_UINT16_T
    HAVE_UINT32_T
    HAVE_UINT64_T

    # Crypto
    OPENSSL
    GCM

    # ABSL definitions
    ABSL_ALLOCATOR_NOTHROW=1
    ABSL_FLAGS_STRIP_NAMES=0

    # Build configuration
    NVALGRIND
    DYNAMIC_ANNOTATIONS_ENABLED=0
    PROTOBUF_ENABLE_DEBUG_LOGGING_MAY_LEAK_PII=0

    # Logging/Debug
    CONFIG_LOG=1
)

# Set include directories
set(WEBRTC_ROOT ${CMAKE_CURRENT_SOURCE_DIR})

# ============================================================================
# Include directories (migrated from compile_commands.json)
# ============================================================================
set(WEBRTC_INCLUDE_DIRS
    ${WEBRTC_ROOT}
    ${WEBRTC_ROOT}/api
    ${WEBRTC_ROOT}/api/crypto
    ${WEBRTC_ROOT}/api/transport
    ${WEBRTC_ROOT}/api/transport/rtp
    ${WEBRTC_ROOT}/audio
    ${WEBRTC_ROOT}/call
    ${WEBRTC_ROOT}/pc
    ${WEBRTC_ROOT}/p2p
    ${WEBRTC_ROOT}/p2p/base
    ${WEBRTC_ROOT}/rtc_base
    ${WEBRTC_ROOT}/rtc_base/third_party/sigslot
    ${WEBRTC_ROOT}/rtc_base/synchronization
    ${WEBRTC_ROOT}/rtc_base/memory
    ${WEBRTC_ROOT}/rtc_base/network
    ${WEBRTC_ROOT}/rtc_base/strings
    ${WEBRTC_ROOT}/rtc_base/internal
    ${WEBRTC_ROOT}/rtc_base/deprecated
    ${WEBRTC_ROOT}/rtc_base/numerics
    ${WEBRTC_ROOT}/system_wrappers/include
    ${WEBRTC_ROOT}/modules
    ${WEBRTC_ROOT}/modules/include
    ${WEBRTC_ROOT}/modules/audio_coding/include
    ${WEBRTC_ROOT}/modules/rtp_rtcp/include
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source
    ${WEBRTC_ROOT}/third_party/abseil-cpp
    ${WEBRTC_ROOT}/third_party/jsoncpp/source/include
    ${WEBRTC_ROOT}/third_party/jsoncpp/source/src/lib_json
    ${WEBRTC_ROOT}/third_party/libsrtp/include
    ${WEBRTC_ROOT}/third_party/libsrtp/crypto/include
    ${WEBRTC_ROOT}/third_party/libsrtp/config
    # ${WEBRTC_ROOT}/third_party/perfetto/include
    # ${WEBRTC_ROOT}/third_party/perfetto/build_config
    # ${WEBRTC_ROOT}/third_party/perfetto
    ${WEBRTC_ROOT}/third_party/libyuv/include
    ${WEBRTC_ROOT}/third_party/opus/src/include
    ${WEBRTC_ROOT}/third_party/protobuf/src
    ${WEBRTC_ROOT}/third_party/re2/src
    ${WEBRTC_ROOT}/common_audio
    ${WEBRTC_ROOT}/common_audio/resampler
    ${WEBRTC_ROOT}/common_audio/signal_processing
    ${WEBRTC_ROOT}/common_audio/third_party/ooura/fft_size_128
    ${WEBRTC_ROOT}/common_audio/vad
    ${WEBRTC_ROOT}/common_video
    ${WEBRTC_ROOT}/common_video/h264
    ${WEBRTC_ROOT}/common_video/h265
    ${WEBRTC_ROOT}/net/dcsctp/public
    ${WEBRTC_ROOT}/net/dcsctp/packet
    ${WEBRTC_ROOT}/net/dcsctp/packet/chunk
    ${WEBRTC_ROOT}/net/dcsctp/packet/parameter
    ${WEBRTC_ROOT}/logging
    ${WEBRTC_ROOT}/logging/rtc_event_log
    ${WEBRTC_ROOT}/logging/rtc_event_log/events
    ${WEBRTC_ROOT}/stats
    ${WEBRTC_ROOT}/video
    ${WEBRTC_ROOT}/video/config
    ${WEBRTC_ROOT}/video/adaptation
    ${WEBRTC_ROOT}/video/corruption_detection
    ${WEBRTC_ROOT}/media
)

include(cmake/dependencies.cmake)

# Shared usage requirements do not leak WebRTC macros into third-party builds.
add_library(webrtc_config INTERFACE)
target_compile_features(webrtc_config INTERFACE cxx_std_20)
target_include_directories(webrtc_config INTERFACE
    "${WEBRTC_ROOT}"
    "${WEBRTC_ROOT}/third_party/abseil-cpp"
    "${WEBRTC_ROOT}/third_party/libyuv/include")
target_compile_definitions(webrtc_config INTERFACE
    WEBRTC_ALLOW_DEPRECATED_NAMESPACES ${WEBRTC_PLATFORM_DEFINITIONS})
add_library(webrtc_dependencies INTERFACE)
target_link_libraries(webrtc_dependencies INTERFACE webrtc_config)
target_link_libraries(webrtc_dependencies INTERFACE
    srtp yuv opus OpenSSL::SSL OpenSSL::Crypto
    absl::base absl::flags absl::flags_parse absl::flat_hash_map
    absl::flat_hash_set absl::log absl::check absl::strings
    absl::str_format absl::synchronization absl::time absl::optional
    absl::any_invocable absl::bind_front absl::crc32c
    crc32c jsoncpp_static webrtc_pffft webrtc_rnnoise
    unofficial::libvpx::libvpx aom webrtc_dav1d Threads::Threads)
if(WIN32)
    target_link_libraries(webrtc_dependencies INTERFACE
        ws2_32 winmm iphlpapi secur32 crypt32 bcrypt
        dmoguids wmcodecdspuuid amstrmid msdmo ole32 oleaut32
        strmiids user32 advapi32 shell32)
elseif(ANDROID)
    target_link_libraries(webrtc_dependencies INTERFACE log android ${CMAKE_DL_LIBS} m)
elseif(APPLE)
    target_link_libraries(webrtc_dependencies INTERFACE ${WEBRTC_APPLE_FRAMEWORKS})
    if(CMAKE_SYSTEM_NAME STREQUAL "iOS")
        # RTCAudioSession uses NSString/UIDevice categories in separate archive
        # members. ObjC message sends alone do not make ld pull those members in.
        target_link_options(webrtc_dependencies INTERFACE -ObjC)
    endif()
else()
    target_link_libraries(webrtc_dependencies INTERFACE ${CMAKE_DL_LIBS} m)
endif()


include(cmake/modules.cmake)

# Keep the existing archive/API: each module is compiled once, then its objects
# are reused by both its own archive and the aggregate libwebrtc archive.
add_library(webrtc STATIC ${WEBRTC_MODULE_OBJECTS})
add_library(WebRTC::webrtc ALIAS webrtc)
set_target_properties(webrtc PROPERTIES
    ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/$<CONFIG>"
    WEBRTC_SOURCE_MANIFEST "${WEBRTC_ALL_SOURCES}")
target_link_libraries(webrtc PUBLIC webrtc_dependencies)

if(CMAKE_SYSTEM_NAME STREQUAL "iOS" OR ANDROID)
    set(_webrtc_demo_default OFF)
else()
    set(_webrtc_demo_default ON)
endif()

# Cross-link all production objects into an Android shared library. This also
# checks PIC and undefined references, which static archive creation cannot do.
if(ANDROID)
    add_library(android_link_smoke SHARED EXCLUDE_FROM_ALL test/cmake/android_link_smoke.cc)
    target_link_libraries(android_link_smoke PRIVATE
        -Wl,--whole-archive webrtc -Wl,--no-whole-archive)
    target_link_options(android_link_smoke PRIVATE "LINKER:--no-undefined"
        "LINKER:-z,max-page-size=16384")
endif()
option(WEBRTC_BUILD_DEMO "Build the PeerConnection smoke test" ${_webrtc_demo_default})
if(WEBRTC_BUILD_DEMO)
    add_executable(peerconnection_demo demo/peerconnection_demo.cc)
    set_target_properties(peerconnection_demo PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/$<CONFIG>")
    target_link_libraries(peerconnection_demo PRIVATE WebRTC::webrtc)
    enable_testing()
    if(NOT ANDROID OR CMAKE_CROSSCOMPILING_EMULATOR)
        add_test(NAME peerconnection_smoke COMMAND peerconnection_demo)
        set_tests_properties(peerconnection_smoke PROPERTIES TIMEOUT 30)
    endif()
    if(WEBRTC_ARCH_X64)
        add_executable(matched_filter_smoke test/cmake/matched_filter_smoke.cc)
        target_link_libraries(matched_filter_smoke PRIVATE WebRTC::webrtc)
        if(NOT ANDROID OR CMAKE_CROSSCOMPILING_EMULATOR)
            add_test(NAME matched_filter_smoke COMMAND matched_filter_smoke)
            set_tests_properties(matched_filter_smoke PROPERTIES TIMEOUT 30 SKIP_RETURN_CODE 77)
        endif()
    endif()
    install(TARGETS peerconnection_demo DESTINATION bin)
endif()

# A static archive alone cannot detect missing platform implementations. Force
# every object into a link-only smoke binary, also usable with an iOS toolchain.
if(APPLE)
    add_executable(apple_link_smoke EXCLUDE_FROM_ALL test/cmake/apple_link_smoke.cc)
    if(WEBRTC_BUILD_DEMO)
        set_target_properties(apple_link_smoke PROPERTIES EXCLUDE_FROM_ALL OFF)
    endif()
    # force_load supplies the archive itself. Listing it a second time through
    # target_link_libraries can load ObjC members twice when -ObjC is enabled.
    add_dependencies(apple_link_smoke webrtc)
    target_link_libraries(apple_link_smoke PRIVATE webrtc_dependencies)
    target_link_options(apple_link_smoke PRIVATE "LINKER:-force_load,$<TARGET_FILE:webrtc>")
    if(WEBRTC_BUILD_DEMO AND NOT CMAKE_CROSSCOMPILING)
        add_test(NAME apple_link_smoke COMMAND apple_link_smoke)
    endif()
endif()
