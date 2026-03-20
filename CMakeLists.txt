cmake_minimum_required(VERSION 3.18)
project(webrtc_peerconnection_demo)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# ============================================================================
# Compiler flags (from compile_commands.json)
# ============================================================================
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -fPIC -pthread")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -fPIC -pthread")

# SIMD flags - SSE3 is used by most WebRTC files
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -msse3")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -msse3")

# Release optimization flags
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O2 -fdata-sections -ffunction-sections")
set(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE} -O2 -fdata-sections -ffunction-sections")

# Visibility
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fvisibility=hidden")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fvisibility=hidden")

# ============================================================================
# Compile definitions (migrated from compile_commands.json)
# ============================================================================
add_compile_definitions(
    # Basic platform definitions
    WEBRTC_POSIX
    WEBRTC_LINUX
    __STDC_CONSTANT_MACROS
    __STDC_FORMAT_MACROS
    _FILE_OFFSET_BITS=64
    _LARGEFILE_SOURCE
    _LARGEFILE64_SOURCE

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
    WEBRTC_DUMMY_FILE_DEVICES

    # Video codec support
    RTC_DAV1D_IN_INTERNAL_DECODER_FACTORY
    RTC_ENABLE_VP9
    RTC_ENABLE_H265
    HAVE_WEBRTC_VIDEO

    # LibYUV SIMD disable flags (for x86_64)
    LIBYUV_DISABLE_NEON
    LIBYUV_DISABLE_LSX
    LIBYUV_DISABLE_LASX
    LIBYUV_DISABLE_SVE
    LIBYUV_DISABLE_SME

    # System/Platform definitions
    HAVE_PTHREAD
    HAVE_PTHREAD_SETAFFINITY_NP=1
    HAVE_PTHREAD_GETAFFINITY_NP=1
    HAVE_LITTLE_ENDIAN
    HAVE_NETINET_IN_H
    HAVE_ARPA_INET_H
    HAVE_INTTYPES_H
    HAVE_STDINT_H
    HAVE_STDLIB_H
    HAVE_STRING_H
    HAVE_SYS_TYPES_H
    HAVE_UNISTD_H
    HAVE_INT8_T
    HAVE_INT16_T
    HAVE_INT32_T
    HAVE_UINT8_T
    HAVE_UINT16_T
    HAVE_UINT32_T
    HAVE_UINT64_T

    # Crypto
    OPENSSL
    SRTP_LINUX
    GCM

    # ABSL definitions
    ABSL_ALLOCATOR_NOTHROW=1
    ABSL_FLAGS_STRIP_NAMES=0

    # Build configuration
    NDEBUG
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
include_directories(
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
    ${WEBRTC_ROOT}/third_party/libaom/source/libaom
    ${WEBRTC_ROOT}/third_party/libaom/source/config
    ${WEBRTC_ROOT}/third_party/libaom/source/config/linux/x64
    ${WEBRTC_ROOT}/third_party/libvpx/source/libvpx
    ${WEBRTC_ROOT}/third_party/libvpx/source/config
    ${WEBRTC_ROOT}/third_party/libvpx/source/config/linux/x64
    ${WEBRTC_ROOT}/third_party/opus/src/include
    ${WEBRTC_ROOT}/third_party/opus/src/celt
    ${WEBRTC_ROOT}/third_party/opus/src/silk
    ${WEBRTC_ROOT}/third_party/protobuf/src
    ${WEBRTC_ROOT}/third_party/re2/src
    ${WEBRTC_ROOT}/third_party/dav1d/version
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

# Use external OpenSSL
set(OPENSSL_ROOT_DIR /home/dele/workspace/sdk/thirdpartylib/linux_x86_64/openssl)
set(OPENSSL_INCLUDE_DIR ${OPENSSL_ROOT_DIR}/include)
set(OPENSSL_CRYPTO_LIBRARY ${OPENSSL_ROOT_DIR}/lib/libcrypto.a)
set(OPENSSL_SSL_LIBRARY ${OPENSSL_ROOT_DIR}/lib/libssl.a)

find_package(OpenSSL REQUIRED)

# Add OpenSSL include directory from found package
include_directories(${OPENSSL_INCLUDE_DIR})

# ============================================================================
# WebRTC source files - Minimal PeerConnection (no media codecs)
# ============================================================================

set(WEBRTC_SOURCES)

# ----------------------------------------------------------------------------
# Third-party libraries - 使用 add_subdirectory 方式构建
# ----------------------------------------------------------------------------
set(LIBSRTP_BUILD_TESTS OFF CACHE BOOL "Build libsrtp tests" FORCE)
add_subdirectory(${WEBRTC_ROOT}/third_party/libsrtp EXCLUDE_FROM_ALL)

# Abseil - 源文件已直接包含在WEBRTC_SOURCES中，无需add_subdirectory

# libyuv - 视频格式转换库
set(UNIT_TEST OFF CACHE BOOL "" FORCE)
add_subdirectory(${WEBRTC_ROOT}/third_party/libyuv EXCLUDE_FROM_ALL)

# Opus - 音频编解码库
add_subdirectory(${WEBRTC_ROOT}/third_party/opus EXCLUDE_FROM_ALL)

# ============================================================================
# SIMD-specific compile flags for individual source files
# (from compile_commands.json - AVX2, FMA, SSSE3, SSE4.1, PCLMUL)
# ============================================================================

# AVX2 + FMA files (AVX2 implicitly enables AVX)
set_source_files_properties(
    ${WEBRTC_ROOT}/common_audio/fir_filter_avx2.cc
    ${WEBRTC_ROOT}/common_audio/resampler/sinc_resampler_avx2.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/adaptive_fir_filter_avx2.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/adaptive_fir_filter_erl_avx2.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/fft_data_avx2.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/matched_filter_avx2.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/vector_math_avx2.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/rnn_vad/vector_math_avx2.cc
    PROPERTIES COMPILE_FLAGS "-mavx2 -mfma"
)

# Create WebRTC static library

# ============================================================================
# Additional source files from compile_commands.json
# (Excluding third_party, test/, testing/)
# ============================================================================

# ----------------------------------------------------------------------------
# Abseil - 直接包含源文件到webrtc静态库中
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    # absl/base
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/base/internal/cycleclock.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/base/internal/low_level_alloc.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/base/internal/raw_logging.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/base/internal/spinlock.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/base/internal/spinlock_wait.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/base/internal/sysinfo.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/base/internal/thread_identity.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/base/internal/throw_delegate.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/base/internal/unscaledcycleclock.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/base/log_severity.cc
    # absl/strings
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/ascii.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/charconv.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/cord.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/cord_analysis.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/escaping.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/match.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/numbers.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/str_cat.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/str_replace.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/str_split.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/string_view.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/substitute.cc
    # absl/strings/internal
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/internal/charconv_bigint.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/internal/charconv_parse.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/internal/cord_internal.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/internal/cord_rep_btree.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/internal/cord_rep_btree_navigator.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/internal/cord_rep_btree_reader.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/internal/cord_rep_consume.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/internal/cord_rep_crc.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/internal/cordz_functions.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/internal/cordz_handle.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/internal/cordz_info.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/internal/cordz_sample_token.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/internal/damerau_levenshtein_distance.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/internal/escaping.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/internal/memutil.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/internal/ostringstream.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/internal/pow10_helper.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/internal/stringify_sink.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/internal/utf8.cc
    # absl/strings/internal/str_format
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/internal/str_format/arg.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/internal/str_format/bind.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/internal/str_format/extension.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/internal/str_format/float_conversion.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/internal/str_format/output.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/strings/internal/str_format/parser.cc
    # absl/numeric
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/numeric/int128.cc
    # absl/hash
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/hash/internal/hash.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/hash/internal/city.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/hash/internal/low_level_hash.cc
    # absl/container
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/container/internal/raw_hash_set.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/container/internal/hashtablez_sampler.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/container/internal/hashtablez_sampler_force_weak_definition.cc
    # absl/synchronization
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/synchronization/mutex.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/synchronization/barrier.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/synchronization/blocking_counter.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/synchronization/notification.cc
    # absl/synchronization/internal
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/synchronization/internal/create_thread_identity.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/synchronization/internal/futex_waiter.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/synchronization/internal/graphcycles.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/synchronization/internal/kernel_timeout.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/synchronization/internal/per_thread_sem.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/synchronization/internal/pthread_waiter.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/synchronization/internal/sem_waiter.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/synchronization/internal/stdcpp_waiter.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/synchronization/internal/waiter_base.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/synchronization/internal/win32_waiter.cc
    # absl/time
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/time/clock.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/time/civil_time.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/time/duration.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/time/format.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/time/time.cc
    # absl/time/internal/cctz
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/time/internal/cctz/src/civil_time_detail.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/time/internal/cctz/src/time_zone_if.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/time/internal/cctz/src/time_zone_fixed.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/time/internal/cctz/src/time_zone_libc.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/time/internal/cctz/src/time_zone_lookup.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/time/internal/cctz/src/time_zone_posix.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/time/internal/cctz/src/time_zone_info.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/time/internal/cctz/src/time_zone_impl.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/time/internal/cctz/src/time_zone_format.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/time/internal/cctz/src/zone_info_source.cc
    # absl/log (absl_log.cc doesn't exist, removed)
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/log/die_if_null.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/log/flags.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/log/globals.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/log/initialize.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/log/log_sink.cc
    # absl/log/internal
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/log/internal/check_op.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/log/internal/conditions.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/log/internal/fnmatch.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/log/internal/log_format.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/log/internal/log_message.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/log/internal/log_sink_set.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/log/internal/nullguard.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/log/internal/proto.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/log/internal/structured_proto.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/log/internal/vlog_config.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/log/internal/globals.cc
    # absl/debugging
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/debugging/stacktrace.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/debugging/symbolize.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/debugging/internal/demangle.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/debugging/internal/demangle_rust.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/debugging/internal/decode_rust_punycode.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/debugging/internal/utf8_for_code_point.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/debugging/internal/address_is_readable.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/debugging/internal/elf_mem_image.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/debugging/internal/examine_stack.cc
    ${WEBRTC_ROOT}/third_party/abseil-cpp/absl/debugging/internal/vdso_support.cc
)

# ----------------------------------------------------------------------------
# API - Additional files
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/api/audio/audio_processing.cc
    ${WEBRTC_ROOT}/api/audio/builtin_audio_processing_builder.cc
    ${WEBRTC_ROOT}/api/audio/echo_canceller3_factory.cc
    ${WEBRTC_ROOT}/api/audio/echo_detector_creator.cc
    ${WEBRTC_ROOT}/api/audio_codecs/L16/audio_decoder_L16.cc
    ${WEBRTC_ROOT}/api/audio_codecs/L16/audio_encoder_L16.cc
    ${WEBRTC_ROOT}/api/audio_codecs/audio_decoder.cc
    ${WEBRTC_ROOT}/api/audio_codecs/audio_encoder.cc
    ${WEBRTC_ROOT}/api/audio_codecs/builtin_audio_decoder_factory.cc
    ${WEBRTC_ROOT}/api/audio_codecs/builtin_audio_encoder_factory.cc
    ${WEBRTC_ROOT}/api/audio_codecs/g711/audio_decoder_g711.cc
    ${WEBRTC_ROOT}/api/audio_codecs/g711/audio_encoder_g711.cc
    ${WEBRTC_ROOT}/api/audio_codecs/g722/audio_decoder_g722.cc
    ${WEBRTC_ROOT}/api/audio_codecs/g722/audio_encoder_g722.cc
    ${WEBRTC_ROOT}/api/audio_codecs/opus/audio_decoder_multi_channel_opus.cc
    ${WEBRTC_ROOT}/api/audio_codecs/opus/audio_decoder_opus.cc
    ${WEBRTC_ROOT}/api/audio_codecs/opus/audio_encoder_multi_channel_opus.cc
    ${WEBRTC_ROOT}/api/audio_codecs/opus/audio_encoder_multi_channel_opus_config.cc
    ${WEBRTC_ROOT}/api/audio_codecs/opus/audio_encoder_opus.cc
    ${WEBRTC_ROOT}/api/audio_codecs/opus/audio_encoder_opus_config.cc
    ${WEBRTC_ROOT}/api/audio_codecs/opus_audio_decoder_factory.cc
    ${WEBRTC_ROOT}/api/audio_codecs/opus_audio_encoder_factory.cc
    # frame_crypto_transformer.cc requires BoringSSL EVP_AEAD API, excluded for OpenSSL compatibility
    ${WEBRTC_ROOT}/api/enable_media_with_defaults.cc
    ${WEBRTC_ROOT}/api/field_trials.cc
    ${WEBRTC_ROOT}/api/frame_transformer_factory.cc
    ${WEBRTC_ROOT}/api/ice_transport_factory.cc
    ${WEBRTC_ROOT}/api/neteq/custom_neteq_factory.cc
    ${WEBRTC_ROOT}/api/neteq/default_neteq_controller_factory.cc
    ${WEBRTC_ROOT}/api/test/create_frame_generator.cc
    ${WEBRTC_ROOT}/api/test/create_peer_connection_quality_test_frame_generator.cc
    ${WEBRTC_ROOT}/api/test/frame_generator_interface.cc
    ${WEBRTC_ROOT}/api/test/metrics/chrome_perf_dashboard_metrics_exporter.cc
    ${WEBRTC_ROOT}/api/test/metrics/global_metrics_logger_and_exporter.cc
    ${WEBRTC_ROOT}/api/test/metrics/metric.cc
    ${WEBRTC_ROOT}/api/test/metrics/metrics_accumulator.cc
    ${WEBRTC_ROOT}/api/test/metrics/metrics_logger.cc
    ${WEBRTC_ROOT}/api/test/metrics/metrics_set_proto_file_exporter.cc
    ${WEBRTC_ROOT}/api/test/metrics/print_result_proxy_metrics_exporter.cc
    ${WEBRTC_ROOT}/api/test/metrics/stdout_metrics_exporter.cc
    ${WEBRTC_ROOT}/api/test/neteq_simulator.cc
    ${WEBRTC_ROOT}/api/test/network_emulation/create_cross_traffic.cc
    ${WEBRTC_ROOT}/api/test/network_emulation/ecn_marking_counter.cc
    ${WEBRTC_ROOT}/api/test/network_emulation/network_emulation_interfaces.cc
    ${WEBRTC_ROOT}/api/test/network_emulation_manager.cc
    ${WEBRTC_ROOT}/api/test/pclf/media_configuration.cc
    ${WEBRTC_ROOT}/api/test/pclf/peer_configurer.cc
    ${WEBRTC_ROOT}/api/test/time_controller.cc
    ${WEBRTC_ROOT}/api/test/video/test_video_track_source.cc
    ${WEBRTC_ROOT}/api/video_codecs/builtin_video_decoder_factory.cc
    ${WEBRTC_ROOT}/api/video_codecs/builtin_video_encoder_factory.cc
    ${WEBRTC_ROOT}/api/video_codecs/libaom_av1_encoder_factory.cc
    ${WEBRTC_ROOT}/api/video_codecs/simple_encoder_wrapper.cc
    ${WEBRTC_ROOT}/api/video_codecs/video_decoder_software_fallback_wrapper.cc
    ${WEBRTC_ROOT}/api/video_codecs/video_encoder_software_fallback_wrapper.cc
    ${WEBRTC_ROOT}/api/video_codecs/vp8_frame_config.cc
    ${WEBRTC_ROOT}/api/video_codecs/vp8_temporal_layers.cc
    ${WEBRTC_ROOT}/api/video_codecs/vp8_temporal_layers_factory.cc
)

# ----------------------------------------------------------------------------
# COMMON_AUDIO - Additional files
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/common_audio/fir_filter_avx2.cc
    ${WEBRTC_ROOT}/common_audio/fir_filter_c.cc
    ${WEBRTC_ROOT}/common_audio/fir_filter_sse.cc
    ${WEBRTC_ROOT}/common_audio/resampler/sinc_resampler_avx2.cc
    ${WEBRTC_ROOT}/common_audio/resampler/sinc_resampler_sse.cc
)

# ----------------------------------------------------------------------------
# COMMON_AUDIO - Signal Processing (C files)
# ----------------------------------------------------------------------------
# Common signal processing sources (all platforms)
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/common_audio/signal_processing/auto_corr_to_refl_coef.c
    ${WEBRTC_ROOT}/common_audio/signal_processing/auto_correlation.c
    ${WEBRTC_ROOT}/common_audio/signal_processing/copy_set_operations.c
    ${WEBRTC_ROOT}/common_audio/signal_processing/cross_correlation.c
    ${WEBRTC_ROOT}/common_audio/signal_processing/division_operations.c
    ${WEBRTC_ROOT}/common_audio/signal_processing/energy.c
    ${WEBRTC_ROOT}/common_audio/signal_processing/filter_ar.c
    ${WEBRTC_ROOT}/common_audio/signal_processing/filter_ma_fast_q12.c
    ${WEBRTC_ROOT}/common_audio/signal_processing/get_hanning_window.c
    ${WEBRTC_ROOT}/common_audio/signal_processing/get_scaling_square.c
    ${WEBRTC_ROOT}/common_audio/signal_processing/levinson_durbin.c
    ${WEBRTC_ROOT}/common_audio/signal_processing/lpc_to_refl_coef.c
    ${WEBRTC_ROOT}/common_audio/signal_processing/randomization_functions.c
    ${WEBRTC_ROOT}/common_audio/signal_processing/real_fft.c
    ${WEBRTC_ROOT}/common_audio/signal_processing/refl_coef_to_lpc.c
    ${WEBRTC_ROOT}/common_audio/signal_processing/resample.c
    ${WEBRTC_ROOT}/common_audio/signal_processing/resample_48khz.c
    ${WEBRTC_ROOT}/common_audio/signal_processing/resample_by_2_internal.c
    ${WEBRTC_ROOT}/common_audio/signal_processing/resample_fractional.c
    ${WEBRTC_ROOT}/common_audio/signal_processing/spl_init.c
    ${WEBRTC_ROOT}/common_audio/signal_processing/spl_inl.c
    ${WEBRTC_ROOT}/common_audio/signal_processing/spl_sqrt.c
    ${WEBRTC_ROOT}/common_audio/signal_processing/splitting_filter.c
    ${WEBRTC_ROOT}/common_audio/signal_processing/sqrt_of_one_minus_x_squared.c
    ${WEBRTC_ROOT}/common_audio/signal_processing/vector_operations.c
    ${WEBRTC_ROOT}/common_audio/third_party/spl_sqrt_floor/spl_sqrt_floor.c
    ${WEBRTC_ROOT}/common_audio/ring_buffer.c
)

# Platform-specific signal processing sources
if(CMAKE_SYSTEM_PROCESSOR MATCHES "mips" OR CMAKE_SYSTEM_PROCESSOR MATCHES "mipsel")
    list(APPEND WEBRTC_SOURCES
        # MIPS-specific sources
        ${WEBRTC_ROOT}/common_audio/signal_processing/complex_bit_reverse_mips.c
        ${WEBRTC_ROOT}/common_audio/signal_processing/complex_fft_mips.c
        ${WEBRTC_ROOT}/common_audio/signal_processing/cross_correlation_mips.c
        ${WEBRTC_ROOT}/common_audio/signal_processing/downsample_fast_mips.c
        ${WEBRTC_ROOT}/common_audio/signal_processing/filter_ar_fast_q12_mips.c
        ${WEBRTC_ROOT}/common_audio/signal_processing/min_max_operations_mips.c
        ${WEBRTC_ROOT}/common_audio/signal_processing/resample_by_2_mips.c
        ${WEBRTC_ROOT}/common_audio/signal_processing/vector_scaling_operations_mips.c
        ${WEBRTC_ROOT}/common_audio/third_party/spl_sqrt_floor/spl_sqrt_floor_mips.c
    )
else()
    # Non-MIPS platforms use these
    list(APPEND WEBRTC_SOURCES
        ${WEBRTC_ROOT}/common_audio/signal_processing/complex_bit_reverse.c
        ${WEBRTC_ROOT}/common_audio/signal_processing/complex_fft.c
        ${WEBRTC_ROOT}/common_audio/signal_processing/downsample_fast.c
        ${WEBRTC_ROOT}/common_audio/signal_processing/filter_ar_fast_q12.c
        ${WEBRTC_ROOT}/common_audio/signal_processing/min_max_operations.c
        ${WEBRTC_ROOT}/common_audio/signal_processing/resample_by_2.c
        ${WEBRTC_ROOT}/common_audio/signal_processing/vector_scaling_operations.c
    )
endif()

if(CMAKE_SYSTEM_PROCESSOR MATCHES "arm" OR CMAKE_SYSTEM_PROCESSOR MATCHES "aarch64")
    # ARM NEON optimizations
    list(APPEND WEBRTC_SOURCES
        ${WEBRTC_ROOT}/common_audio/signal_processing/cross_correlation_neon.c
        ${WEBRTC_ROOT}/common_audio/signal_processing/downsample_fast_neon.c
        ${WEBRTC_ROOT}/common_audio/signal_processing/min_max_operations_neon.c
    )
    # Set NEON compile flags
    set_source_files_properties(
        ${WEBRTC_ROOT}/common_audio/signal_processing/cross_correlation_neon.c
        ${WEBRTC_ROOT}/common_audio/signal_processing/downsample_fast_neon.c
        ${WEBRTC_ROOT}/common_audio/signal_processing/min_max_operations_neon.c
        PROPERTIES COMPILE_FLAGS "-mfpu=neon"
    )
endif()

# ----------------------------------------------------------------------------
# COMMON_AUDIO - VAD (C files)
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/common_audio/vad/vad_core.c
    ${WEBRTC_ROOT}/common_audio/vad/vad_filterbank.c
    ${WEBRTC_ROOT}/common_audio/vad/vad_gmm.c
    ${WEBRTC_ROOT}/common_audio/vad/vad_sp.c
    ${WEBRTC_ROOT}/common_audio/vad/webrtc_vad.c
)
# ----------------------------------------------------------------------------
# COMMON_VIDEO - Additional files
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/common_video/corruption_detection_converters.cc
)
# ----------------------------------------------------------------------------
# AUDIO - Additional files
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/audio/audio_receive_stream.cc
    ${WEBRTC_ROOT}/audio/audio_send_stream.cc
    ${WEBRTC_ROOT}/audio/audio_state.cc
    ${WEBRTC_ROOT}/audio/channel_receive.cc
    ${WEBRTC_ROOT}/audio/channel_receive_frame_transformer_delegate.cc
    ${WEBRTC_ROOT}/audio/channel_send.cc
    ${WEBRTC_ROOT}/audio/channel_send_frame_transformer_delegate.cc
    ${WEBRTC_ROOT}/audio/remix_resample.cc
)
# ----------------------------------------------------------------------------
# VIDEO - Additional files
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/video/adaptation/balanced_constraint.cc
    ${WEBRTC_ROOT}/video/corruption_detection/frame_instrumentation_evaluation.cc
    ${WEBRTC_ROOT}/video/rate_utilization_tracker.cc
    ${WEBRTC_ROOT}/video/video_quality_observer2.cc
)
# ----------------------------------------------------------------------------
# CALL - Additional files
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/call/syncable.cc
    ${WEBRTC_ROOT}/call/version.cc
)
# ----------------------------------------------------------------------------
# LOGGING - Additional files
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/logging/rtc_event_log/encoder/rtc_event_log_encoder_common.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/fixed_length_encoding_parameters_v3.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_alr_state.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_audio_network_adaptation.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_audio_playout.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_audio_receive_stream_config.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_audio_send_stream_config.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_begin_log.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_bwe_update_delay_based.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_bwe_update_loss_based.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_end_log.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_frame_decoded.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_generic_ack_received.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_generic_packet_received.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_generic_packet_sent.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_neteq_set_minimum_delay.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_probe_cluster_created.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_probe_result_failure.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_probe_result_success.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_rtcp_packet_incoming.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_rtcp_packet_outgoing.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_rtp_packet_incoming.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_rtp_packet_outgoing.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_video_receive_stream_config.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_video_send_stream_config.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/rtc_stream_config.cc
)
# ----------------------------------------------------------------------------
# MEDIA - Additional files
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/media/base/adapted_video_track_source.cc
    ${WEBRTC_ROOT}/media/base/media_engine.cc
    ${WEBRTC_ROOT}/media/base/turn_utils.cc
    ${WEBRTC_ROOT}/media/engine/internal_decoder_factory.cc
    ${WEBRTC_ROOT}/media/engine/internal_encoder_factory.cc
    ${WEBRTC_ROOT}/media/engine/simulcast_encoder_adapter.cc
)
# ----------------------------------------------------------------------------
# MODULES - Additional files
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/modules/async_audio_processing/async_audio_processing.cc
    ${WEBRTC_ROOT}/modules/audio_coding/acm2/acm_remixing.cc
    ${WEBRTC_ROOT}/modules/audio_coding/acm2/acm_resampler.cc
    ${WEBRTC_ROOT}/modules/audio_coding/acm2/audio_coding_module.cc
    ${WEBRTC_ROOT}/modules/audio_coding/acm2/call_statistics.cc
    ${WEBRTC_ROOT}/modules/audio_coding/audio_network_adaptor/audio_network_adaptor_config.cc
    ${WEBRTC_ROOT}/modules/audio_coding/codecs/cng/audio_encoder_cng.cc
    ${WEBRTC_ROOT}/modules/audio_coding/codecs/cng/webrtc_cng.cc
    ${WEBRTC_ROOT}/modules/audio_coding/codecs/g711/audio_decoder_pcm.cc
    ${WEBRTC_ROOT}/modules/audio_coding/codecs/g711/audio_encoder_pcm.cc
    ${WEBRTC_ROOT}/modules/audio_coding/codecs/g722/audio_decoder_g722.cc
    ${WEBRTC_ROOT}/modules/audio_coding/codecs/g722/audio_encoder_g722.cc
    ${WEBRTC_ROOT}/modules/audio_coding/codecs/legacy_encoded_audio_frame.cc
    ${WEBRTC_ROOT}/modules/audio_coding/codecs/opus/audio_coder_opus_common.cc
    ${WEBRTC_ROOT}/modules/audio_coding/codecs/opus/audio_decoder_multi_channel_opus_impl.cc
    ${WEBRTC_ROOT}/modules/audio_coding/codecs/opus/audio_decoder_opus.cc
    ${WEBRTC_ROOT}/modules/audio_coding/codecs/opus/audio_encoder_multi_channel_opus_impl.cc
    ${WEBRTC_ROOT}/modules/audio_coding/codecs/opus/audio_encoder_opus.cc
    ${WEBRTC_ROOT}/modules/audio_coding/codecs/opus/opus_interface.cc
    ${WEBRTC_ROOT}/modules/audio_coding/codecs/pcm16b/audio_decoder_pcm16b.cc
    ${WEBRTC_ROOT}/modules/audio_coding/codecs/pcm16b/audio_encoder_pcm16b.cc
    ${WEBRTC_ROOT}/modules/audio_coding/codecs/pcm16b/pcm16b.c
    ${WEBRTC_ROOT}/modules/audio_coding/codecs/pcm16b/pcm16b_common.cc
    ${WEBRTC_ROOT}/modules/audio_coding/codecs/red/audio_encoder_copy_red.cc
    ${WEBRTC_ROOT}/modules/third_party/g711/g711.c
    ${WEBRTC_ROOT}/modules/third_party/g722/g722_decode.c
    ${WEBRTC_ROOT}/modules/third_party/g722/g722_encode.c
    ${WEBRTC_ROOT}/modules/audio_coding/codecs/g711/g711_interface.c
    ${WEBRTC_ROOT}/modules/audio_coding/codecs/g722/g722_interface.c
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/accelerate.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/audio_multi_vector.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/audio_vector.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/background_noise.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/buffer_level_filter.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/comfort_noise.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/cross_correlation.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/decision_logic.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/decoder_database.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/delay_constraints.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/delay_manager.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/dsp_helper.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/dtmf_buffer.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/dtmf_tone_generator.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/expand.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/expand_uma_logger.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/histogram.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/merge.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/nack_tracker.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/neteq_impl.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/normal.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/packet.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/packet_arrival_history.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/packet_buffer.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/preemptive_expand.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/random_vector.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/red_payload_splitter.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/reorder_optimizer.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/statistics_calculator.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/sync_buffer.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/time_stretch.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/timestamp_scaler.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/tools/audio_loop.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/tools/audio_sink.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/tools/constant_pcm_packet_source.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/tools/encode_neteq_input.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/tools/initial_packet_inserter_neteq_input.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/tools/input_audio_file.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/tools/neteq_delay_analyzer.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/tools/neteq_input.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/tools/neteq_replacement_input.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/tools/neteq_rtp_dump_input.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/tools/neteq_stats_getter.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/tools/neteq_stats_plotter.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/tools/packet.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/tools/packet_source.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/tools/resample_input_audio_file.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/tools/rtp_file_source.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/tools/rtp_generator.cc
    ${WEBRTC_ROOT}/modules/audio_coding/neteq/underrun_optimizer.cc
    ${WEBRTC_ROOT}/modules/audio_device/audio_device_buffer.cc
    ${WEBRTC_ROOT}/modules/audio_device/audio_device_data_observer.cc
    ${WEBRTC_ROOT}/modules/audio_device/audio_device_generic.cc
    ${WEBRTC_ROOT}/modules/audio_device/audio_device_impl.cc
    ${WEBRTC_ROOT}/modules/audio_device/audio_device_name.cc
    ${WEBRTC_ROOT}/modules/audio_device/dummy/audio_device_dummy.cc
    ${WEBRTC_ROOT}/modules/audio_device/dummy/file_audio_device.cc
    ${WEBRTC_ROOT}/modules/audio_device/dummy/file_audio_device_factory.cc
    ${WEBRTC_ROOT}/modules/audio_device/fine_audio_buffer.cc
    ${WEBRTC_ROOT}/modules/audio_mixer/audio_frame_manipulator.cc
    ${WEBRTC_ROOT}/modules/audio_mixer/audio_mixer_impl.cc
    ${WEBRTC_ROOT}/modules/audio_mixer/default_output_rate_calculator.cc
    ${WEBRTC_ROOT}/modules/audio_mixer/frame_combiner.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/adaptive_fir_filter.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/adaptive_fir_filter_avx2.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/adaptive_fir_filter_erl.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/adaptive_fir_filter_erl_avx2.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/aec3_common.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/aec3_fft.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/aec_state.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/alignment_mixer.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/api_call_jitter_metrics.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/block_buffer.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/block_delay_buffer.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/block_framer.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/block_processor.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/block_processor_metrics.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/clockdrift_detector.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/coarse_filter_update_gain.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/comfort_noise_generator.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/config_selector.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/decimator.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/dominant_nearend_detector.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/downsampled_render_buffer.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/echo_audibility.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/echo_canceller3.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/echo_path_delay_estimator.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/echo_path_variability.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/echo_remover.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/echo_remover_metrics.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/erl_estimator.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/erle_estimator.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/fft_buffer.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/fft_data_avx2.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/filter_analyzer.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/frame_blocker.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/fullband_erle_estimator.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/matched_filter.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/matched_filter_avx2.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/matched_filter_lag_aggregator.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/moving_average.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/multi_channel_content_detector.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/refined_filter_update_gain.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/render_buffer.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/render_delay_buffer.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/render_delay_controller.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/render_delay_controller_metrics.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/render_signal_analyzer.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/residual_echo_estimator.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/reverb_decay_estimator.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/reverb_frequency_response.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/reverb_model.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/reverb_model_estimator.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/signal_dependent_erle_estimator.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/spectrum_buffer.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/stationarity_estimator.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/subband_erle_estimator.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/subband_nearend_detector.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/subtractor.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/subtractor_output.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/subtractor_output_analyzer.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/suppression_filter.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/suppression_gain.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/transparent_mode.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec3/vector_math_avx2.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aec_dump/null_aec_dump_factory.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aecm/aecm_core.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aecm/aecm_core_c.cc
    ${WEBRTC_ROOT}/modules/audio_processing/aecm/echo_control_mobile.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc/agc.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc/agc_manager_direct.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc/legacy/analog_agc.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc/legacy/digital_agc.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc/loudness_histogram.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc/utility.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/adaptive_digital_gain_controller.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/agc2_testing_common.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/biquad_filter.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/clipping_predictor.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/clipping_predictor_level_buffer.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/compute_interpolated_gain_curve.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/cpu_features.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/fixed_digital_level_estimator.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/gain_applier.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/input_volume_controller.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/input_volume_stats_reporter.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/interpolated_gain_curve.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/limiter.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/limiter_db_gain_curve.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/noise_level_estimator.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/rnn_vad/auto_correlation.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/rnn_vad/features_extraction.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/rnn_vad/lp_residual.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/rnn_vad/pitch_search.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/rnn_vad/pitch_search_internal.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/rnn_vad/rnn.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/rnn_vad/rnn_fc.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/rnn_vad/rnn_gru.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/rnn_vad/spectral_features.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/rnn_vad/spectral_features_internal.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/rnn_vad/vector_math_avx2.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/saturation_protector.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/saturation_protector_buffer.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/speech_level_estimator.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/speech_probability_buffer.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/vad_wrapper.cc
    ${WEBRTC_ROOT}/modules/audio_processing/agc2/vector_float_frame.cc
    ${WEBRTC_ROOT}/modules/audio_processing/audio_buffer.cc
    ${WEBRTC_ROOT}/modules/audio_processing/audio_processing_impl.cc
    ${WEBRTC_ROOT}/modules/audio_processing/capture_levels_adjuster/audio_samples_scaler.cc
    ${WEBRTC_ROOT}/modules/audio_processing/capture_levels_adjuster/capture_levels_adjuster.cc
    ${WEBRTC_ROOT}/modules/audio_processing/echo_control_mobile_impl.cc
    ${WEBRTC_ROOT}/modules/audio_processing/echo_detector/circular_buffer.cc
    ${WEBRTC_ROOT}/modules/audio_processing/echo_detector/mean_variance_estimator.cc
    ${WEBRTC_ROOT}/modules/audio_processing/echo_detector/moving_max.cc
    ${WEBRTC_ROOT}/modules/audio_processing/echo_detector/normalized_covariance_estimator.cc
    ${WEBRTC_ROOT}/modules/audio_processing/gain_control_impl.cc
    ${WEBRTC_ROOT}/modules/audio_processing/gain_controller2.cc
    ${WEBRTC_ROOT}/modules/audio_processing/high_pass_filter.cc
    ${WEBRTC_ROOT}/modules/audio_processing/include/aec_dump.cc
    ${WEBRTC_ROOT}/modules/audio_processing/include/audio_frame_proxies.cc
    ${WEBRTC_ROOT}/modules/audio_processing/logging/apm_data_dumper.cc
    ${WEBRTC_ROOT}/modules/audio_processing/ns/fast_math.cc
    ${WEBRTC_ROOT}/modules/audio_processing/ns/histograms.cc
    ${WEBRTC_ROOT}/modules/audio_processing/ns/noise_estimator.cc
    ${WEBRTC_ROOT}/modules/audio_processing/ns/noise_suppressor.cc
    ${WEBRTC_ROOT}/modules/audio_processing/ns/ns_fft.cc
    ${WEBRTC_ROOT}/modules/audio_processing/ns/prior_signal_model.cc
    ${WEBRTC_ROOT}/modules/audio_processing/ns/prior_signal_model_estimator.cc
    ${WEBRTC_ROOT}/modules/audio_processing/ns/quantile_noise_estimator.cc
    ${WEBRTC_ROOT}/modules/audio_processing/ns/signal_model.cc
    ${WEBRTC_ROOT}/modules/audio_processing/ns/signal_model_estimator.cc
    ${WEBRTC_ROOT}/modules/audio_processing/ns/speech_probability_estimator.cc
    ${WEBRTC_ROOT}/modules/audio_processing/ns/suppression_params.cc
    ${WEBRTC_ROOT}/modules/audio_processing/ns/wiener_filter.cc
    ${WEBRTC_ROOT}/modules/audio_processing/residual_echo_detector.cc
    ${WEBRTC_ROOT}/modules/audio_processing/rms_level.cc
    ${WEBRTC_ROOT}/modules/audio_processing/splitting_filter.cc
    ${WEBRTC_ROOT}/modules/audio_processing/three_band_filter_bank.cc
    ${WEBRTC_ROOT}/modules/audio_processing/utility/cascaded_biquad_filter.cc
    ${WEBRTC_ROOT}/modules/audio_processing/utility/delay_estimator.cc
    ${WEBRTC_ROOT}/modules/audio_processing/utility/delay_estimator_wrapper.cc
    ${WEBRTC_ROOT}/modules/audio_processing/utility/pffft_wrapper.cc
    ${WEBRTC_ROOT}/modules/audio_processing/vad/gmm.cc
    ${WEBRTC_ROOT}/modules/audio_processing/vad/pitch_based_vad.cc
    ${WEBRTC_ROOT}/modules/audio_processing/vad/pitch_internal.cc
    ${WEBRTC_ROOT}/modules/audio_processing/vad/pole_zero_filter.cc
    ${WEBRTC_ROOT}/modules/audio_processing/vad/standalone_vad.cc
    ${WEBRTC_ROOT}/modules/audio_processing/vad/vad_audio_proc.cc
    ${WEBRTC_ROOT}/modules/audio_processing/vad/vad_circular_buffer.cc
    ${WEBRTC_ROOT}/modules/audio_processing/vad/voice_activity_detector.cc
    ${WEBRTC_ROOT}/modules/congestion_controller/receive_side_congestion_controller.cc
    ${WEBRTC_ROOT}/modules/congestion_controller/remb_throttler.cc
    ${WEBRTC_ROOT}/modules/remote_bitrate_estimator/tools/bwe_rtp.cc
    ${WEBRTC_ROOT}/modules/remote_bitrate_estimator/tools/rtp_to_text.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/include/report_block_data.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/include/rtp_rtcp_defines.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/absolute_capture_time_interpolator.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/absolute_capture_time_sender.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/active_decode_targets_helper.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/capture_clock_offset_updater.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/corruption_detection_extension.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/create_video_rtp_depacketizer.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/deprecated/deprecated_rtp_sender_egress.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/dtmf_queue.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/fec_private_tables_bursty.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/fec_private_tables_random.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/fec_test_helper.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/flexfec_03_header_reader_writer.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/flexfec_header_reader_writer.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/flexfec_receiver.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/flexfec_sender.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/forward_error_correction.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/forward_error_correction_internal.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/frame_object.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/leb128.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/ntp_time_util.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/packet_loss_stats.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/packet_sequencer.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/receive_statistics_impl.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/remote_ntp_time_estimator.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_packet/compound_packet.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_packet/congestion_control_feedback.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_packet/dlrr.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_packet/extended_reports.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_packet/fir.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_packet/loss_notification.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_packet/nack.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_packet/pli.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_packet/psfb.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_packet/rapid_resync_request.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_packet/remb.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_packet/remote_estimate.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_packet/report_block.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_packet/rrtr.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_packet/sdes.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_packet/target_bitrate.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_packet/tmmb_item.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_packet/tmmbn.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_packet/tmmbr.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_transceiver.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_transceiver_config.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_transceiver_impl.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_dependency_descriptor_extension.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_dependency_descriptor_reader.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_dependency_descriptor_writer.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_descriptor_authentication.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_format_vp8.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_format_vp9.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_generic_frame_descriptor.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_generic_frame_descriptor_extension.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_header_extension_map.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_packet_history.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_packet_received.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_packet_send_info.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_packetizer_av1.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_packetizer_av1_test_helper.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_packetizer_h265.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_rtcp_impl2.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_sender_audio.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_sender_egress.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_sender_video.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_sender_video_frame_transformer_delegate.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_sequence_number_map.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_util.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_video_header.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_video_layers_allocation_extension.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_video_stream_receiver_frame_transformer_delegate.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/source_tracker.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/tmmbr_help.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/ulpfec_generator.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/ulpfec_header_reader_writer.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/ulpfec_receiver.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/video_rtp_depacketizer.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/video_rtp_depacketizer_av1.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/video_rtp_depacketizer_generic.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/video_rtp_depacketizer_h264.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/video_rtp_depacketizer_h265.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/video_rtp_depacketizer_raw.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/video_rtp_depacketizer_vp8.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/video_rtp_depacketizer_vp9.cc
    ${WEBRTC_ROOT}/modules/video_capture/device_info_impl.cc
    ${WEBRTC_ROOT}/modules/video_capture/linux/device_info_linux.cc
    ${WEBRTC_ROOT}/modules/video_capture/linux/device_info_v4l2.cc
    ${WEBRTC_ROOT}/modules/video_capture/linux/video_capture_linux.cc
    ${WEBRTC_ROOT}/modules/video_capture/linux/video_capture_v4l2.cc
    ${WEBRTC_ROOT}/modules/video_capture/video_capture_factory.cc
    ${WEBRTC_ROOT}/modules/video_capture/video_capture_impl.cc
    ${WEBRTC_ROOT}/modules/video_capture/video_capture_options.cc
    ${WEBRTC_ROOT}/modules/video_coding/chain_diff_calculator.cc
    ${WEBRTC_ROOT}/modules/video_coding/codecs/av1/av1_svc_config.cc
    ${WEBRTC_ROOT}/modules/video_coding/codecs/av1/dav1d_decoder.cc
    ${WEBRTC_ROOT}/modules/video_coding/codecs/av1/libaom_av1_encoder.cc
    ${WEBRTC_ROOT}/modules/video_coding/codecs/h264/h264.cc
    ${WEBRTC_ROOT}/modules/video_coding/codecs/h264/h264_color_space.cc
    ${WEBRTC_ROOT}/modules/video_coding/codecs/h264/h264_decoder_impl.cc
    ${WEBRTC_ROOT}/modules/video_coding/codecs/h264/h264_encoder_impl.cc
    ${WEBRTC_ROOT}/modules/video_coding/codecs/interface/libvpx_interface.cc
    ${WEBRTC_ROOT}/modules/video_coding/codecs/vp8/default_temporal_layers.cc
    ${WEBRTC_ROOT}/modules/video_coding/codecs/vp8/libvpx_vp8_decoder.cc
    ${WEBRTC_ROOT}/modules/video_coding/codecs/vp8/libvpx_vp8_encoder.cc
    ${WEBRTC_ROOT}/modules/video_coding/codecs/vp8/screenshare_layers.cc
    ${WEBRTC_ROOT}/modules/video_coding/codecs/vp8/temporal_layers_checker.cc
    ${WEBRTC_ROOT}/modules/video_coding/codecs/vp8/vp8_scalability.cc
    ${WEBRTC_ROOT}/modules/video_coding/codecs/vp9/libvpx_vp9_decoder.cc
    ${WEBRTC_ROOT}/modules/video_coding/codecs/vp9/libvpx_vp9_encoder.cc
    ${WEBRTC_ROOT}/modules/video_coding/codecs/vp9/svc_config.cc
    ${WEBRTC_ROOT}/modules/video_coding/codecs/vp9/vp9.cc
    ${WEBRTC_ROOT}/modules/video_coding/codecs/vp9/vp9_frame_buffer_pool.cc
    ${WEBRTC_ROOT}/modules/video_coding/decoder_database.cc
    ${WEBRTC_ROOT}/modules/video_coding/deprecated/decoding_state.cc
    ${WEBRTC_ROOT}/modules/video_coding/deprecated/event_wrapper.cc
    ${WEBRTC_ROOT}/modules/video_coding/deprecated/frame_buffer.cc
    ${WEBRTC_ROOT}/modules/video_coding/deprecated/jitter_buffer.cc
    ${WEBRTC_ROOT}/modules/video_coding/deprecated/packet.cc
    ${WEBRTC_ROOT}/modules/video_coding/deprecated/receiver.cc
    ${WEBRTC_ROOT}/modules/video_coding/deprecated/stream_generator.cc
    ${WEBRTC_ROOT}/modules/video_coding/encoded_frame.cc
    ${WEBRTC_ROOT}/modules/video_coding/fec_controller_default.cc
    ${WEBRTC_ROOT}/modules/video_coding/frame_dependencies_calculator.cc
    ${WEBRTC_ROOT}/modules/video_coding/frame_helpers.cc
    ${WEBRTC_ROOT}/modules/video_coding/generic_decoder.cc
    ${WEBRTC_ROOT}/modules/video_coding/h264_sprop_parameter_sets.cc
    ${WEBRTC_ROOT}/modules/video_coding/h264_sps_pps_tracker.cc
    ${WEBRTC_ROOT}/modules/video_coding/h26x_packet_buffer.cc
    ${WEBRTC_ROOT}/modules/video_coding/histogram.cc
    ${WEBRTC_ROOT}/modules/video_coding/include/video_codec_interface.cc
    ${WEBRTC_ROOT}/modules/video_coding/include/video_error_codes_utils.cc
    ${WEBRTC_ROOT}/modules/video_coding/loss_notification_controller.cc
    ${WEBRTC_ROOT}/modules/video_coding/nack_requester.cc
    ${WEBRTC_ROOT}/modules/video_coding/rtp_frame_id_only_ref_finder.cc
    ${WEBRTC_ROOT}/modules/video_coding/rtp_frame_reference_finder.cc
    ${WEBRTC_ROOT}/modules/video_coding/rtp_generic_ref_finder.cc
    ${WEBRTC_ROOT}/modules/video_coding/rtp_seq_num_only_ref_finder.cc
    ${WEBRTC_ROOT}/modules/video_coding/rtp_vp8_ref_finder.cc
    ${WEBRTC_ROOT}/modules/video_coding/rtp_vp9_ref_finder.cc
    ${WEBRTC_ROOT}/modules/video_coding/svc/create_scalability_structure.cc
    ${WEBRTC_ROOT}/modules/video_coding/svc/scalability_mode_util.cc
    ${WEBRTC_ROOT}/modules/video_coding/svc/scalability_structure_full_svc.cc
    ${WEBRTC_ROOT}/modules/video_coding/svc/scalability_structure_key_svc.cc
    ${WEBRTC_ROOT}/modules/video_coding/svc/scalability_structure_l2t2_key_shift.cc
    ${WEBRTC_ROOT}/modules/video_coding/svc/scalability_structure_simulcast.cc
    ${WEBRTC_ROOT}/modules/video_coding/svc/scalable_video_controller_no_layering.cc
    ${WEBRTC_ROOT}/modules/video_coding/svc/simulcast_to_svc_converter.cc
    ${WEBRTC_ROOT}/modules/video_coding/svc/svc_rate_allocator.cc
    ${WEBRTC_ROOT}/modules/video_coding/timing/decode_time_percentile_filter.cc
    ${WEBRTC_ROOT}/modules/video_coding/timing/frame_delay_variation_kalman_filter.cc
    ${WEBRTC_ROOT}/modules/video_coding/timing/inter_frame_delay_variation_calculator.cc
    ${WEBRTC_ROOT}/modules/video_coding/timing/rtt_filter.cc
    ${WEBRTC_ROOT}/modules/video_coding/timing/timestamp_extrapolator.cc
    ${WEBRTC_ROOT}/modules/video_coding/utility/bandwidth_quality_scaler.cc
    ${WEBRTC_ROOT}/modules/video_coding/utility/corruption_detection_settings_generator.cc
    ${WEBRTC_ROOT}/modules/video_coding/utility/decoded_frames_history.cc
    ${WEBRTC_ROOT}/modules/video_coding/utility/frame_dropper.cc
    ${WEBRTC_ROOT}/modules/video_coding/utility/framerate_controller_deprecated.cc
    ${WEBRTC_ROOT}/modules/video_coding/utility/ivf_file_reader.cc
    ${WEBRTC_ROOT}/modules/video_coding/utility/ivf_file_writer.cc
    ${WEBRTC_ROOT}/modules/video_coding/utility/qp_parser.cc
    ${WEBRTC_ROOT}/modules/video_coding/utility/quality_scaler.cc
    ${WEBRTC_ROOT}/modules/video_coding/utility/simulcast_rate_allocator.cc
    ${WEBRTC_ROOT}/modules/video_coding/utility/simulcast_utility.cc
    ${WEBRTC_ROOT}/modules/video_coding/utility/vp8_header_parser.cc
    ${WEBRTC_ROOT}/modules/video_coding/utility/vp9_uncompressed_header_parser.cc
    ${WEBRTC_ROOT}/modules/video_coding/video_coding_defines.cc
    ${WEBRTC_ROOT}/modules/video_coding/video_coding_impl.cc
    ${WEBRTC_ROOT}/modules/video_coding/video_receiver.cc
)

# ----------------------------------------------------------------------------
# NET - Additional files
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/net/dcsctp/common/handover_testing.cc
    ${WEBRTC_ROOT}/net/dcsctp/public/dcsctp_handover_state.cc
)
# ----------------------------------------------------------------------------
# P2P - Additional files
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/p2p/test/stun_server.cc
    ${WEBRTC_ROOT}/p2p/test/turn_server.cc
)
# ----------------------------------------------------------------------------
# STATS - Additional files
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/stats/test/rtc_test_stats.cc
)
# ----------------------------------------------------------------------------
# BUILD - Additional files
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    # ${WEBRTC_ROOT}/build/sanitizers/sanitizer_options.cc
)
# ----------------------------------------------------------------------------
# SDK - Additional files
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/sdk/media_constraints.cc
)
# ----------------------------------------------------------------------------
# RTC_TOOLS - Additional files
# ----------------------------------------------------------------------------
# list(APPEND WEBRTC_SOURCES
#     ${WEBRTC_ROOT}/rtc_tools/frame_analyzer/frame_analyzer.cc
#     ${WEBRTC_ROOT}/rtc_tools/frame_analyzer/linear_least_squares.cc
#     ${WEBRTC_ROOT}/rtc_tools/frame_analyzer/reference_less_video_analysis.cc
#     ${WEBRTC_ROOT}/rtc_tools/frame_analyzer/reference_less_video_analysis_lib.cc
#     ${WEBRTC_ROOT}/rtc_tools/frame_analyzer/video_color_aligner.cc
#     ${WEBRTC_ROOT}/rtc_tools/frame_analyzer/video_geometry_aligner.cc
#     ${WEBRTC_ROOT}/rtc_tools/frame_analyzer/video_quality_analysis.cc
#     ${WEBRTC_ROOT}/rtc_tools/frame_analyzer/video_temporal_aligner.cc
#     ${WEBRTC_ROOT}/rtc_tools/psnr_ssim_analyzer/psnr_ssim_analyzer.cc
#     ${WEBRTC_ROOT}/rtc_tools/rtp_generator/main.cc
#     ${WEBRTC_ROOT}/rtc_tools/rtp_generator/rtp_generator.cc
#     ${WEBRTC_ROOT}/rtc_tools/video_encoder/encoded_image_file_writer.cc
#     ${WEBRTC_ROOT}/rtc_tools/video_encoder/video_encoder.cc
#     ${WEBRTC_ROOT}/rtc_tools/video_file_reader.cc
#     ${WEBRTC_ROOT}/rtc_tools/video_file_writer.cc
#     ${WEBRTC_ROOT}/rtc_tools/video_replay.cc
# )

# ----------------------------------------------------------------------------
# RTC base - 基础运行时
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/rtc_base/async_dns_resolver.cc
    ${WEBRTC_ROOT}/rtc_base/async_packet_socket.cc
    ${WEBRTC_ROOT}/rtc_base/async_socket.cc
    ${WEBRTC_ROOT}/rtc_base/async_tcp_socket.cc
    ${WEBRTC_ROOT}/rtc_base/async_udp_socket.cc
    ${WEBRTC_ROOT}/rtc_base/base64.cc
    ${WEBRTC_ROOT}/rtc_base/bit_buffer.cc
    ${WEBRTC_ROOT}/rtc_base/bitstream_reader.cc
    ${WEBRTC_ROOT}/rtc_base/buffer_queue.cc
    ${WEBRTC_ROOT}/rtc_base/byte_buffer.cc
    ${WEBRTC_ROOT}/rtc_base/callback_list.cc
    ${WEBRTC_ROOT}/rtc_base/checks.cc
    ${WEBRTC_ROOT}/rtc_base/copy_on_write_buffer.cc
    ${WEBRTC_ROOT}/rtc_base/crc32.cc
    ${WEBRTC_ROOT}/rtc_base/crypto_random.cc
    ${WEBRTC_ROOT}/rtc_base/event.cc
    ${WEBRTC_ROOT}/rtc_base/event_tracer.cc
    ${WEBRTC_ROOT}/rtc_base/ifaddrs_converter.cc
    ${WEBRTC_ROOT}/rtc_base/ip_address.cc
    ${WEBRTC_ROOT}/rtc_base/logging.cc
    ${WEBRTC_ROOT}/rtc_base/memory/aligned_malloc.cc
    ${WEBRTC_ROOT}/rtc_base/memory/fifo_buffer.cc
    ${WEBRTC_ROOT}/rtc_base/message_digest.cc
    ${WEBRTC_ROOT}/rtc_base/net_helpers.cc
    ${WEBRTC_ROOT}/rtc_base/network_route.cc
    ${WEBRTC_ROOT}/rtc_base/network.cc
    ${WEBRTC_ROOT}/rtc_base/network_constants.cc
    ${WEBRTC_ROOT}/rtc_base/null_socket_server.cc
    ${WEBRTC_ROOT}/rtc_base/openssl_adapter.cc
    ${WEBRTC_ROOT}/rtc_base/openssl_digest.cc
    ${WEBRTC_ROOT}/rtc_base/openssl_key_pair.cc
    ${WEBRTC_ROOT}/rtc_base/openssl_session_cache.cc
    ${WEBRTC_ROOT}/rtc_base/openssl_stream_adapter.cc
    ${WEBRTC_ROOT}/rtc_base/openssl_utility.cc
    ${WEBRTC_ROOT}/rtc_base/physical_socket_server.cc
    ${WEBRTC_ROOT}/rtc_base/platform_thread.cc
    ${WEBRTC_ROOT}/rtc_base/platform_thread_types.cc
    ${WEBRTC_ROOT}/rtc_base/race_checker.cc
    ${WEBRTC_ROOT}/rtc_base/random.cc
    ${WEBRTC_ROOT}/rtc_base/rate_tracker.cc
    ${WEBRTC_ROOT}/rtc_base/rtc_certificate_generator.cc
    ${WEBRTC_ROOT}/rtc_base/socket.cc
    ${WEBRTC_ROOT}/rtc_base/socket_address.cc
    ${WEBRTC_ROOT}/rtc_base/socket_address_pair.cc
    ${WEBRTC_ROOT}/rtc_base/socket_adapters.cc
    ${WEBRTC_ROOT}/rtc_base/ssl_adapter.cc
    ${WEBRTC_ROOT}/rtc_base/ssl_certificate.cc
    ${WEBRTC_ROOT}/rtc_base/ssl_fingerprint.cc
    ${WEBRTC_ROOT}/rtc_base/ssl_identity.cc
    ${WEBRTC_ROOT}/rtc_base/ssl_stream_adapter.cc
    ${WEBRTC_ROOT}/rtc_base/string_to_number.cc
    ${WEBRTC_ROOT}/rtc_base/strings/json.cc
    ${WEBRTC_ROOT}/rtc_base/strings/string_builder.cc
    ${WEBRTC_ROOT}/rtc_base/strings/string_format.cc
    ${WEBRTC_ROOT}/rtc_base/task_queue_stdlib.cc
    ${WEBRTC_ROOT}/rtc_base/thread.cc
    ${WEBRTC_ROOT}/rtc_base/time_utils.cc
    ${WEBRTC_ROOT}/rtc_base/unique_id_generator.cc
    ${WEBRTC_ROOT}/rtc_base/weak_ptr.cc
    ${WEBRTC_ROOT}/rtc_base/third_party/sigslot/sigslot.cc
    ${WEBRTC_ROOT}/rtc_base/bitrate_tracker.cc
    ${WEBRTC_ROOT}/rtc_base/system_time.cc
    ${WEBRTC_ROOT}/rtc_base/string_utils.cc
    ${WEBRTC_ROOT}/rtc_base/string_encode.cc
    ${WEBRTC_ROOT}/rtc_base/internal/default_socket_server.cc
    ${WEBRTC_ROOT}/rtc_base/synchronization/yield_policy.cc
    ${WEBRTC_ROOT}/rtc_base/synchronization/yield.cc
    ${WEBRTC_ROOT}/rtc_base/synchronization/sequence_checker_internal.cc
    ${WEBRTC_ROOT}/rtc_base/deprecated/recursive_critical_section.cc
    ${WEBRTC_ROOT}/rtc_base/operations_chain.cc
    ${WEBRTC_ROOT}/rtc_base/rtc_certificate.cc
    ${WEBRTC_ROOT}/rtc_base/network/sent_packet.cc
    ${WEBRTC_ROOT}/rtc_base/network/received_packet.cc
    ${WEBRTC_ROOT}/rtc_base/rate_limiter.cc
    ${WEBRTC_ROOT}/rtc_base/experiments/field_trial_parser.cc
    ${WEBRTC_ROOT}/rtc_base/experiments/field_trial_units.cc
    ${WEBRTC_ROOT}/rtc_base/experiments/field_trial_list.cc
    ${WEBRTC_ROOT}/rtc_base/numerics/event_based_exponential_moving_average.cc
    ${WEBRTC_ROOT}/rtc_base/numerics/exp_filter.cc
    ${WEBRTC_ROOT}/rtc_base/numerics/moving_average.cc
    ${WEBRTC_ROOT}/rtc_base/stream.cc
    ${WEBRTC_ROOT}/rtc_base/system/file_wrapper.cc
    ${WEBRTC_ROOT}/rtc_base/task_utils/repeating_task.cc
    ${WEBRTC_ROOT}/rtc_base/containers/flat_tree.cc
    ${WEBRTC_ROOT}/rtc_base/data_rate_limiter.cc
    ${WEBRTC_ROOT}/rtc_base/memory_usage.cc
    ${WEBRTC_ROOT}/rtc_base/proxy_server.cc
    ${WEBRTC_ROOT}/rtc_base/test_client.cc
    ${WEBRTC_ROOT}/rtc_base/test_echo_server.cc
    ${WEBRTC_ROOT}/rtc_base/test_utils.cc
    ${WEBRTC_ROOT}/rtc_base/third_party/base64/base64.cc
    ${WEBRTC_ROOT}/rtc_base/timestamp_aligner.cc
    ${WEBRTC_ROOT}/rtc_base/trace_categories.cc
    ${WEBRTC_ROOT}/rtc_base/virtual_socket_server.cc
    ${WEBRTC_ROOT}/rtc_base/zero_memory.cc
)

# ----------------------------------------------------------------------------
# System wrappers - 系统封装
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/system_wrappers/source/field_trial.cc
    ${WEBRTC_ROOT}/system_wrappers/source/metrics.cc
    ${WEBRTC_ROOT}/system_wrappers/source/sleep.cc
    ${WEBRTC_ROOT}/system_wrappers/source/cpu_info.cc
    ${WEBRTC_ROOT}/system_wrappers/source/clock.cc
    ${WEBRTC_ROOT}/system_wrappers/source/cpu_features.cc
    ${WEBRTC_ROOT}/system_wrappers/source/cpu_features_linux.cc
    ${WEBRTC_ROOT}/system_wrappers/source/rtp_to_ntp_estimator.cc
    ${WEBRTC_ROOT}/system_wrappers/source/denormal_disabler.cc
)

# ----------------------------------------------------------------------------
# Media base - 媒体基础（不含编解码器）
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/media/base/media_constants.cc
    ${WEBRTC_ROOT}/media/base/codec.cc
    ${WEBRTC_ROOT}/media/base/codec_comparators.cc
    ${WEBRTC_ROOT}/media/base/media_channel_impl.cc
    ${WEBRTC_ROOT}/media/base/stream_params.cc
    ${WEBRTC_ROOT}/media/base/codec_list.cc
    ${WEBRTC_ROOT}/media/base/sdp_video_format_utils.cc
    ${WEBRTC_ROOT}/media/base/video_source_base.cc
    ${WEBRTC_ROOT}/media/base/rid_description.cc
    ${WEBRTC_ROOT}/media/base/rtp_utils.cc
    ${WEBRTC_ROOT}/media/base/video_adapter.cc
    ${WEBRTC_ROOT}/media/base/video_common.cc
    ${WEBRTC_ROOT}/api/video_codecs/sdp_video_format.cc
    ${WEBRTC_ROOT}/api/video_codecs/video_codec.cc
    ${WEBRTC_ROOT}/api/video_codecs/scalability_mode.cc
    ${WEBRTC_ROOT}/api/video_codecs/scalability_mode_helper.cc
    ${WEBRTC_ROOT}/media/base/video_broadcaster.cc
    ${WEBRTC_ROOT}/media/sctp/dcsctp_transport.cc
    ${WEBRTC_ROOT}/media/sctp/sctp_transport_factory.cc
)

# ----------------------------------------------------------------------------
# Call layer - 调用层（最小化）
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/call/call.cc
    ${WEBRTC_ROOT}/call/call_config.cc
    ${WEBRTC_ROOT}/call/audio_state.cc
    ${WEBRTC_ROOT}/call/bitrate_allocator.cc
    ${WEBRTC_ROOT}/call/payload_type_picker.cc
    ${WEBRTC_ROOT}/call/rtp_bitrate_configurator.cc
    ${WEBRTC_ROOT}/call/rtp_config.cc
    ${WEBRTC_ROOT}/call/rtp_demuxer.cc
    ${WEBRTC_ROOT}/call/flexfec_receive_stream.cc
    ${WEBRTC_ROOT}/call/flexfec_receive_stream_impl.cc
    ${WEBRTC_ROOT}/call/audio_receive_stream.cc
    ${WEBRTC_ROOT}/call/audio_send_stream.cc
    ${WEBRTC_ROOT}/call/video_receive_stream.cc
    ${WEBRTC_ROOT}/call/video_send_stream.cc
    ${WEBRTC_ROOT}/call/rtp_transport_controller_send.cc
    ${WEBRTC_ROOT}/call/rtp_stream_receiver_controller.cc
    ${WEBRTC_ROOT}/call/rtp_video_sender.cc
    ${WEBRTC_ROOT}/call/rtx_receive_stream.cc
    ${WEBRTC_ROOT}/call/receive_time_calculator.cc
    ${WEBRTC_ROOT}/call/rtp_payload_params.cc
)

# ----------------------------------------------------------------------------
# Call adaptation - 调用适配（仅非测试文件）
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/call/adaptation/adaptation_constraint.cc
    ${WEBRTC_ROOT}/call/adaptation/broadcast_resource_listener.cc
    ${WEBRTC_ROOT}/call/adaptation/degradation_preference_provider.cc
    ${WEBRTC_ROOT}/call/adaptation/encoder_settings.cc
    ${WEBRTC_ROOT}/call/adaptation/resource_adaptation_processor.cc
    ${WEBRTC_ROOT}/call/adaptation/resource_adaptation_processor_interface.cc
    ${WEBRTC_ROOT}/call/adaptation/video_stream_adapter.cc
    ${WEBRTC_ROOT}/call/adaptation/video_stream_input_state.cc
    ${WEBRTC_ROOT}/call/adaptation/video_stream_input_state_provider.cc
    ${WEBRTC_ROOT}/call/adaptation/video_source_restrictions.cc
)

# ----------------------------------------------------------------------------
# Video - 视频基础（不含编解码）
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/video/stream_synchronization.cc
    ${WEBRTC_ROOT}/video/stats_counter.cc
    ${WEBRTC_ROOT}/video/config/encoder_stream_factory.cc
    ${WEBRTC_ROOT}/video/config/simulcast.cc
    ${WEBRTC_ROOT}/video/config/video_encoder_config.cc
    ${WEBRTC_ROOT}/video/corruption_detection/corruption_classifier.cc
    ${WEBRTC_ROOT}/video/corruption_detection/frame_instrumentation_generator.cc
    ${WEBRTC_ROOT}/video/corruption_detection/frame_pair_corruption_score.cc
    ${WEBRTC_ROOT}/video/corruption_detection/generic_mapping_functions.cc
    ${WEBRTC_ROOT}/video/corruption_detection/halton_frame_sampler.cc
    ${WEBRTC_ROOT}/video/corruption_detection/halton_sequence.cc
    ${WEBRTC_ROOT}/video/corruption_detection/utils.cc
    ${WEBRTC_ROOT}/video/adaptation/bandwidth_quality_scaler_resource.cc
    ${WEBRTC_ROOT}/video/adaptation/bitrate_constraint.cc
    ${WEBRTC_ROOT}/video/adaptation/encode_usage_resource.cc
    ${WEBRTC_ROOT}/video/adaptation/overuse_frame_detector.cc
    ${WEBRTC_ROOT}/video/adaptation/pixel_limit_resource.cc
    ${WEBRTC_ROOT}/video/adaptation/quality_scaler_resource.cc
    ${WEBRTC_ROOT}/video/adaptation/video_stream_encoder_resource.cc
    ${WEBRTC_ROOT}/video/adaptation/video_stream_encoder_resource_manager.cc
    ${WEBRTC_ROOT}/video/alignment_adjuster.cc
    ${WEBRTC_ROOT}/video/buffered_frame_decryptor.cc
    ${WEBRTC_ROOT}/video/call_stats2.cc
    ${WEBRTC_ROOT}/video/decode_synchronizer.cc
    ${WEBRTC_ROOT}/video/encoder_bitrate_adjuster.cc
    ${WEBRTC_ROOT}/video/encoder_overshoot_detector.cc
    ${WEBRTC_ROOT}/video/encoder_rtcp_feedback.cc
    ${WEBRTC_ROOT}/video/frame_cadence_adapter.cc
    ${WEBRTC_ROOT}/video/frame_decode_timing.cc
    ${WEBRTC_ROOT}/video/frame_dumping_decoder.cc
    ${WEBRTC_ROOT}/video/frame_dumping_encoder.cc
    ${WEBRTC_ROOT}/video/frame_encode_metadata_writer.cc
    ${WEBRTC_ROOT}/video/quality_convergence_controller.cc
    ${WEBRTC_ROOT}/video/quality_convergence_monitor.cc
    ${WEBRTC_ROOT}/video/quality_limitation_reason_tracker.cc
    ${WEBRTC_ROOT}/video/receive_statistics_proxy.cc
    ${WEBRTC_ROOT}/video/render/incoming_video_stream.cc
    ${WEBRTC_ROOT}/video/render/video_render_frames.cc
    ${WEBRTC_ROOT}/video/report_block_stats.cc
    ${WEBRTC_ROOT}/video/rtp_streams_synchronizer2.cc
    ${WEBRTC_ROOT}/video/rtp_video_stream_receiver2.cc
    ${WEBRTC_ROOT}/video/send_delay_stats.cc
    ${WEBRTC_ROOT}/video/send_statistics_proxy.cc
    ${WEBRTC_ROOT}/video/task_queue_frame_decode_scheduler.cc
    ${WEBRTC_ROOT}/video/transport_adapter.cc
    ${WEBRTC_ROOT}/video/unique_timestamp_counter.cc
    ${WEBRTC_ROOT}/video/video_receive_stream2.cc
    ${WEBRTC_ROOT}/video/video_receive_stream_timeout_tracker.cc
    ${WEBRTC_ROOT}/video/video_send_stream_impl.cc
    ${WEBRTC_ROOT}/video/video_source_sink_controller.cc
    ${WEBRTC_ROOT}/video/video_stream_buffer_controller.cc
    ${WEBRTC_ROOT}/video/video_stream_decoder2.cc
    ${WEBRTC_ROOT}/video/video_stream_encoder.cc
)

# ----------------------------------------------------------------------------
# Audio - 音频基础
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/audio/audio_level.cc
    ${WEBRTC_ROOT}/audio/audio_transport_impl.cc
    ${WEBRTC_ROOT}/audio/utility/audio_frame_operations.cc
    ${WEBRTC_ROOT}/audio/utility/channel_mixer.cc
    ${WEBRTC_ROOT}/audio/utility/channel_mixing_matrix.cc
)

# ----------------------------------------------------------------------------
# common_video - 通用视频
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/common_video/bitrate_adjuster.cc
    ${WEBRTC_ROOT}/common_video/frame_rate_estimator.cc
    ${WEBRTC_ROOT}/common_video/framerate_controller.cc
    ${WEBRTC_ROOT}/common_video/generic_frame_descriptor/generic_frame_info.cc
    ${WEBRTC_ROOT}/common_video/h264/h264_bitstream_parser.cc
    ${WEBRTC_ROOT}/common_video/h264/h264_common.cc
    ${WEBRTC_ROOT}/common_video/h264/pps_parser.cc
    ${WEBRTC_ROOT}/common_video/h264/sps_parser.cc
    ${WEBRTC_ROOT}/common_video/h264/sps_vui_rewriter.cc
    ${WEBRTC_ROOT}/common_video/h265/h265_bitstream_parser.cc
    ${WEBRTC_ROOT}/common_video/h265/h265_common.cc
    ${WEBRTC_ROOT}/common_video/h265/h265_inline.cc
    ${WEBRTC_ROOT}/common_video/h265/h265_pps_parser.cc
    ${WEBRTC_ROOT}/common_video/h265/h265_sps_parser.cc
    ${WEBRTC_ROOT}/common_video/h265/h265_vps_parser.cc
    ${WEBRTC_ROOT}/common_video/libyuv/webrtc_libyuv.cc
    ${WEBRTC_ROOT}/common_video/video_frame_buffer.cc
    ${WEBRTC_ROOT}/common_video/video_frame_buffer_pool.cc
)

# ----------------------------------------------------------------------------
# common_audio - 通用音频
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/common_audio/audio_converter.cc
    ${WEBRTC_ROOT}/common_audio/audio_util.cc
    ${WEBRTC_ROOT}/common_audio/channel_buffer.cc
    ${WEBRTC_ROOT}/common_audio/fir_filter_factory.cc
    ${WEBRTC_ROOT}/common_audio/real_fourier.cc
    ${WEBRTC_ROOT}/common_audio/real_fourier_ooura.cc
    ${WEBRTC_ROOT}/common_audio/resampler/push_resampler.cc
    ${WEBRTC_ROOT}/common_audio/resampler/push_sinc_resampler.cc
    ${WEBRTC_ROOT}/common_audio/resampler/resampler.cc
    ${WEBRTC_ROOT}/common_audio/resampler/sinc_resampler.cc
    ${WEBRTC_ROOT}/common_audio/signal_processing/dot_product_with_scale.cc
    ${WEBRTC_ROOT}/common_audio/smoothing_filter.cc
    ${WEBRTC_ROOT}/common_audio/third_party/ooura/fft_size_128/ooura_fft.cc
    ${WEBRTC_ROOT}/common_audio/third_party/ooura/fft_size_256/fft4g.cc
    ${WEBRTC_ROOT}/common_audio/vad/vad.cc
    ${WEBRTC_ROOT}/common_audio/wav_file.cc
    ${WEBRTC_ROOT}/common_audio/wav_header.cc
    ${WEBRTC_ROOT}/common_audio/window_generator.cc
)

# ----------------------------------------------------------------------------
# modules/audio_coding - 音频编码
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/modules/audio_coding/audio_network_adaptor/audio_network_adaptor_impl.cc
    ${WEBRTC_ROOT}/modules/audio_coding/audio_network_adaptor/bitrate_controller.cc
    ${WEBRTC_ROOT}/modules/audio_coding/audio_network_adaptor/channel_controller.cc
    ${WEBRTC_ROOT}/modules/audio_coding/audio_network_adaptor/controller.cc
    ${WEBRTC_ROOT}/modules/audio_coding/audio_network_adaptor/controller_manager.cc
    ${WEBRTC_ROOT}/modules/audio_coding/audio_network_adaptor/debug_dump_writer.cc
    ${WEBRTC_ROOT}/modules/audio_coding/audio_network_adaptor/event_log_writer.cc
    ${WEBRTC_ROOT}/modules/audio_coding/audio_network_adaptor/dtx_controller.cc
    ${WEBRTC_ROOT}/modules/audio_coding/audio_network_adaptor/fec_controller_plr_based.cc
    ${WEBRTC_ROOT}/modules/audio_coding/audio_network_adaptor/frame_length_controller.cc
    ${WEBRTC_ROOT}/modules/audio_coding/audio_network_adaptor/frame_length_controller_v2.cc
)

# ----------------------------------------------------------------------------
# modules/video_coding - 视频编码
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/modules/video_coding/timing/jitter_estimator.cc
    ${WEBRTC_ROOT}/modules/video_coding/timing/timing.cc
    ${WEBRTC_ROOT}/modules/video_coding/deprecated/session_info.cc
    ${WEBRTC_ROOT}/modules/video_coding/media_opt_util.cc
    ${WEBRTC_ROOT}/modules/video_coding/packet_buffer.cc
    ${WEBRTC_ROOT}/modules/video_coding/video_codec_initializer.cc
    ${WEBRTC_ROOT}/modules/video_coding/video_receiver2.cc
)

# ----------------------------------------------------------------------------
# Media engine - 媒体引擎
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/media/engine/adm_helpers.cc
    ${WEBRTC_ROOT}/media/engine/webrtc_media_engine.cc
    ${WEBRTC_ROOT}/media/engine/webrtc_video_engine.cc
    ${WEBRTC_ROOT}/media/engine/webrtc_voice_engine.cc
)

# ----------------------------------------------------------------------------
# RTP/RTCP module - RTP/RTCP协议
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_packet.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_packet_to_send.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_format.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_format_h264.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_format_video_generic.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_header_extension_size.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_packet.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_packet/common_header.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_packet/receiver_report.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_packet/sender_report.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_packet/bye.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_packet/app.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_packet/rtpfb.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_packet/transport_feedback.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_sender.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_rtcp_impl.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtp_header_extensions.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_nack_stats.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_receiver.cc
    ${WEBRTC_ROOT}/modules/rtp_rtcp/source/rtcp_sender.cc
    ${WEBRTC_ROOT}/modules/congestion_controller/rtp/control_handler.cc
    ${WEBRTC_ROOT}/modules/congestion_controller/rtp/transport_feedback_demuxer.cc
    ${WEBRTC_ROOT}/modules/congestion_controller/rtp/transport_feedback_adapter.cc
    ${WEBRTC_ROOT}/modules/congestion_controller/goog_cc/goog_cc_network_control.cc
    ${WEBRTC_ROOT}/modules/congestion_controller/goog_cc/acknowledged_bitrate_estimator.cc
    ${WEBRTC_ROOT}/modules/congestion_controller/goog_cc/acknowledged_bitrate_estimator_interface.cc
    ${WEBRTC_ROOT}/modules/congestion_controller/goog_cc/alr_detector.cc
    ${WEBRTC_ROOT}/modules/congestion_controller/goog_cc/bitrate_estimator.cc
    ${WEBRTC_ROOT}/modules/congestion_controller/goog_cc/congestion_window_pushback_controller.cc
    ${WEBRTC_ROOT}/modules/congestion_controller/goog_cc/delay_based_bwe.cc
    ${WEBRTC_ROOT}/modules/congestion_controller/goog_cc/inter_arrival_delta.cc
    ${WEBRTC_ROOT}/modules/congestion_controller/goog_cc/link_capacity_estimator.cc
    ${WEBRTC_ROOT}/modules/congestion_controller/goog_cc/loss_based_bandwidth_estimation.cc
    ${WEBRTC_ROOT}/modules/congestion_controller/goog_cc/loss_based_bwe_v2.cc
    ${WEBRTC_ROOT}/modules/congestion_controller/goog_cc/probe_bitrate_estimator.cc
    ${WEBRTC_ROOT}/modules/congestion_controller/goog_cc/probe_controller.cc
    ${WEBRTC_ROOT}/modules/congestion_controller/goog_cc/robust_throughput_estimator.cc
    ${WEBRTC_ROOT}/modules/congestion_controller/goog_cc/send_side_bandwidth_estimation.cc
    ${WEBRTC_ROOT}/modules/congestion_controller/goog_cc/trendline_estimator.cc
    ${WEBRTC_ROOT}/modules/pacing/bitrate_prober.cc
    ${WEBRTC_ROOT}/modules/pacing/interval_budget.cc
    ${WEBRTC_ROOT}/modules/pacing/pacing_controller.cc
    ${WEBRTC_ROOT}/modules/pacing/packet_router.cc
    ${WEBRTC_ROOT}/modules/pacing/prioritized_packet_queue.cc
    ${WEBRTC_ROOT}/modules/pacing/task_queue_paced_sender.cc
    ${WEBRTC_ROOT}/modules/remote_bitrate_estimator/aimd_rate_control.cc
    ${WEBRTC_ROOT}/modules/remote_bitrate_estimator/bwe_defines.cc
    ${WEBRTC_ROOT}/modules/remote_bitrate_estimator/congestion_control_feedback_generator.cc
    ${WEBRTC_ROOT}/modules/remote_bitrate_estimator/congestion_control_feedback_tracker.cc
    ${WEBRTC_ROOT}/modules/remote_bitrate_estimator/inter_arrival.cc
    ${WEBRTC_ROOT}/modules/remote_bitrate_estimator/overuse_detector.cc
    ${WEBRTC_ROOT}/modules/remote_bitrate_estimator/overuse_estimator.cc
    ${WEBRTC_ROOT}/modules/remote_bitrate_estimator/packet_arrival_map.cc
    ${WEBRTC_ROOT}/modules/remote_bitrate_estimator/remote_bitrate_estimator_abs_send_time.cc
    ${WEBRTC_ROOT}/modules/remote_bitrate_estimator/remote_bitrate_estimator_single_stream.cc
    ${WEBRTC_ROOT}/modules/remote_bitrate_estimator/transport_sequence_number_feedback_generator.cc
)

# ----------------------------------------------------------------------------
# jsoncpp - JSON解析
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES

)

# ----------------------------------------------------------------------------
# Stats - 统计相关
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/stats/rtcstats_objects.cc
    ${WEBRTC_ROOT}/stats/rtc_stats_report.cc
)

# ----------------------------------------------------------------------------
# Logging - 日志相关
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/logging/rtc_event_log/ice_logger.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_ice_candidate_pair.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_ice_candidate_pair_config.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_route_change.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_dtls_transport_state.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_dtls_writable_state.cc
    # ${WEBRTC_ROOT}/logging/rtc_event_log/rtc_event_log_parser.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_field_encoding.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_field_extraction.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/events/rtc_event_field_encoding_parser.cc
    # ${WEBRTC_ROOT}/logging/rtc_event_log/encoder/rtc_event_log_encoder_legacy.cc
    # ${WEBRTC_ROOT}/logging/rtc_event_log/encoder/rtc_event_log_encoder_new_format.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/encoder/rtc_event_log_encoder_v3.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/encoder/var_int.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/encoder/bit_writer.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/encoder/blob_encoding.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/encoder/delta_encoding.cc
    ${WEBRTC_ROOT}/logging/rtc_event_log/encoder/optional_blob_encoding.cc
)

# ----------------------------------------------------------------------------
# net/dcsctp - SCTP 协议
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/net/dcsctp/packet/chunk/chunk.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/chunk/abort_chunk.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/chunk/cookie_ack_chunk.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/chunk/cookie_echo_chunk.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/chunk/data_chunk.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/chunk/error_chunk.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/chunk/forward_tsn_chunk.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/chunk/heartbeat_ack_chunk.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/chunk/heartbeat_request_chunk.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/chunk/idata_chunk.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/chunk/iforward_tsn_chunk.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/chunk/init_ack_chunk.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/chunk/init_chunk.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/chunk/reconfig_chunk.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/chunk/sack_chunk.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/chunk/shutdown_ack_chunk.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/chunk/shutdown_chunk.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/chunk/shutdown_complete_chunk.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/chunk_validators.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/crc32c.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/sctp_packet.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/tlv_trait.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/parameter/add_incoming_streams_request_parameter.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/parameter/add_outgoing_streams_request_parameter.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/parameter/forward_tsn_supported_parameter.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/parameter/heartbeat_info_parameter.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/parameter/incoming_ssn_reset_request_parameter.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/parameter/outgoing_ssn_reset_request_parameter.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/parameter/parameter.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/parameter/reconfiguration_response_parameter.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/parameter/ssn_tsn_reset_request_parameter.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/parameter/state_cookie_parameter.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/parameter/supported_extensions_parameter.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/parameter/zero_checksum_acceptable_chunk_parameter.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/error_cause/error_cause.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/error_cause/cookie_received_while_shutting_down_cause.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/error_cause/invalid_mandatory_parameter_cause.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/error_cause/invalid_stream_identifier_cause.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/error_cause/missing_mandatory_parameter_cause.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/error_cause/no_user_data_cause.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/error_cause/out_of_resource_error_cause.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/error_cause/protocol_violation_cause.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/error_cause/restart_of_an_association_with_new_address_cause.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/error_cause/stale_cookie_error_cause.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/error_cause/unrecognized_chunk_type_cause.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/error_cause/unrecognized_parameter_cause.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/error_cause/unresolvable_address_cause.cc
    ${WEBRTC_ROOT}/net/dcsctp/packet/error_cause/user_initiated_abort_cause.cc
    ${WEBRTC_ROOT}/net/dcsctp/public/dcsctp_socket_factory.cc
    ${WEBRTC_ROOT}/net/dcsctp/public/text_pcap_packet_observer.cc
    ${WEBRTC_ROOT}/net/dcsctp/rx/data_tracker.cc
    ${WEBRTC_ROOT}/net/dcsctp/rx/interleaved_reassembly_streams.cc
    ${WEBRTC_ROOT}/net/dcsctp/rx/reassembly_queue.cc
    ${WEBRTC_ROOT}/net/dcsctp/rx/traditional_reassembly_streams.cc
    ${WEBRTC_ROOT}/net/dcsctp/socket/callback_deferrer.cc
    ${WEBRTC_ROOT}/net/dcsctp/socket/dcsctp_socket.cc
    ${WEBRTC_ROOT}/net/dcsctp/socket/heartbeat_handler.cc
    ${WEBRTC_ROOT}/net/dcsctp/socket/packet_sender.cc
    ${WEBRTC_ROOT}/net/dcsctp/socket/state_cookie.cc
    ${WEBRTC_ROOT}/net/dcsctp/socket/stream_reset_handler.cc
    ${WEBRTC_ROOT}/net/dcsctp/socket/transmission_control_block.cc
    ${WEBRTC_ROOT}/net/dcsctp/timer/task_queue_timeout.cc
    ${WEBRTC_ROOT}/net/dcsctp/timer/timer.cc
    ${WEBRTC_ROOT}/net/dcsctp/tx/outstanding_data.cc
    ${WEBRTC_ROOT}/net/dcsctp/tx/retransmission_error_counter.cc
    ${WEBRTC_ROOT}/net/dcsctp/tx/retransmission_queue.cc
    ${WEBRTC_ROOT}/net/dcsctp/tx/retransmission_timeout.cc
    ${WEBRTC_ROOT}/net/dcsctp/tx/rr_send_queue.cc
    ${WEBRTC_ROOT}/net/dcsctp/tx/stream_scheduler.cc
)

# ----------------------------------------------------------------------------
# API layer - 核心接口
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/api/rtc_event_log/rtc_event.cc
    ${WEBRTC_ROOT}/api/adaptation/resource.cc
    ${WEBRTC_ROOT}/api/audio_options.cc
    ${WEBRTC_ROOT}/api/candidate.cc
    ${WEBRTC_ROOT}/api/create_peerconnection_factory.cc
    ${WEBRTC_ROOT}/api/crypto/crypto_options.cc
    ${WEBRTC_ROOT}/api/data_channel_interface.cc
    ${WEBRTC_ROOT}/api/dtls_transport_interface.cc
    ${WEBRTC_ROOT}/api/enable_media.cc
    ${WEBRTC_ROOT}/api/field_trials_registry.cc
    ${WEBRTC_ROOT}/api/frame_transformer_interface.cc
    ${WEBRTC_ROOT}/api/jsep.cc
    ${WEBRTC_ROOT}/api/jsep_ice_candidate.cc
    ${WEBRTC_ROOT}/api/legacy_stats_types.cc
    ${WEBRTC_ROOT}/api/media_stream_interface.cc
    ${WEBRTC_ROOT}/api/media_types.cc
    ${WEBRTC_ROOT}/api/peer_connection_interface.cc
    ${WEBRTC_ROOT}/api/rtc_error.cc
    ${WEBRTC_ROOT}/api/rtp_packet_info.cc
    ${WEBRTC_ROOT}/api/rtp_parameters.cc
    ${WEBRTC_ROOT}/api/rtp_receiver_interface.cc
    ${WEBRTC_ROOT}/api/rtp_sender_interface.cc
    ${WEBRTC_ROOT}/api/rtp_transceiver_interface.cc
    ${WEBRTC_ROOT}/api/sctp_transport_interface.cc
    ${WEBRTC_ROOT}/api/task_queue/default_task_queue_factory_stdlib.cc
    ${WEBRTC_ROOT}/api/task_queue/pending_task_safety_flag.cc
    ${WEBRTC_ROOT}/api/task_queue/task_queue_base.cc
    ${WEBRTC_ROOT}/api/units/data_rate.cc
    ${WEBRTC_ROOT}/api/units/data_size.cc
    ${WEBRTC_ROOT}/api/units/frequency.cc
    ${WEBRTC_ROOT}/api/units/time_delta.cc
    ${WEBRTC_ROOT}/api/units/timestamp.cc
    ${WEBRTC_ROOT}/api/video/video_frame_buffer.cc
    ${WEBRTC_ROOT}/api/video/encoded_image.cc
    ${WEBRTC_ROOT}/api/video/video_frame_metadata.cc
    ${WEBRTC_ROOT}/api/video/video_timing.cc
    ${WEBRTC_ROOT}/api/video/video_frame.cc
    ${WEBRTC_ROOT}/api/video/i420_buffer.cc
    ${WEBRTC_ROOT}/api/video/i422_buffer.cc
    ${WEBRTC_ROOT}/api/video/i444_buffer.cc
    ${WEBRTC_ROOT}/api/video/nv12_buffer.cc
    ${WEBRTC_ROOT}/api/video/video_source_interface.cc
    ${WEBRTC_ROOT}/api/video/builtin_video_bitrate_allocator_factory.cc
    ${WEBRTC_ROOT}/api/video/color_space.cc
    ${WEBRTC_ROOT}/api/video/encoded_frame.cc
    ${WEBRTC_ROOT}/api/video/frame_buffer.cc
    ${WEBRTC_ROOT}/api/video/hdr_metadata.cc
    ${WEBRTC_ROOT}/api/video/i010_buffer.cc
    ${WEBRTC_ROOT}/api/video/i210_buffer.cc
    ${WEBRTC_ROOT}/api/video/i410_buffer.cc
    ${WEBRTC_ROOT}/api/video/rtp_video_frame_assembler.cc
    ${WEBRTC_ROOT}/api/video/video_adaptation_counters.cc
    ${WEBRTC_ROOT}/api/video/video_bitrate_allocation.cc
    ${WEBRTC_ROOT}/api/video/video_bitrate_allocator.cc
    ${WEBRTC_ROOT}/api/video/video_content_type.cc
    ${WEBRTC_ROOT}/api/video/yuv_helper.cc
    ${WEBRTC_ROOT}/api/environment/environment_factory.cc
    ${WEBRTC_ROOT}/api/transport/stun.cc
    ${WEBRTC_ROOT}/api/transport/bitrate_settings.cc
    ${WEBRTC_ROOT}/api/transport/field_trial_based_config.cc
    ${WEBRTC_ROOT}/api/transport/goog_cc_factory.cc
    ${WEBRTC_ROOT}/api/transport/network_types.cc
    ${WEBRTC_ROOT}/api/transport/rtp/dependency_descriptor.cc
    ${WEBRTC_ROOT}/api/audio/audio_processing_statistics.cc
    ${WEBRTC_ROOT}/api/audio/audio_frame.cc
    ${WEBRTC_ROOT}/api/audio/channel_layout.cc
    ${WEBRTC_ROOT}/api/audio/echo_canceller3_config.cc
    ${WEBRTC_ROOT}/api/audio_codecs/audio_format.cc
    ${WEBRTC_ROOT}/api/audio_codecs/audio_codec_pair_id.cc
    ${WEBRTC_ROOT}/api/video_codecs/vp9_profile.cc
    ${WEBRTC_ROOT}/api/video_codecs/av1_profile.cc
    ${WEBRTC_ROOT}/api/video_codecs/h264_profile_level_id.cc
    ${WEBRTC_ROOT}/api/video_codecs/h265_profile_tier_level.cc
    ${WEBRTC_ROOT}/api/video_codecs/sdp_video_format.cc
    ${WEBRTC_ROOT}/api/video_codecs/simulcast_stream.cc
    ${WEBRTC_ROOT}/api/video_codecs/video_codec.cc
    ${WEBRTC_ROOT}/api/video_codecs/video_decoder.cc
    ${WEBRTC_ROOT}/api/video_codecs/video_decoder_factory.cc
    ${WEBRTC_ROOT}/api/video_codecs/video_encoder.cc
    ${WEBRTC_ROOT}/api/neteq/default_neteq_factory.cc
    ${WEBRTC_ROOT}/api/neteq/neteq.cc
    ${WEBRTC_ROOT}/api/neteq/tick_timer.cc
    ${WEBRTC_ROOT}/api/numerics/samples_stats_counter.cc
    ${WEBRTC_ROOT}/api/rtc_event_log/rtc_event.cc
    ${WEBRTC_ROOT}/api/rtc_event_log/rtc_event_log.cc
    ${WEBRTC_ROOT}/api/rtc_event_log/rtc_event_log_factory.cc
    ${WEBRTC_ROOT}/api/rtc_event_log_output_file.cc
    ${WEBRTC_ROOT}/api/rtp_headers.cc
    ${WEBRTC_ROOT}/api/call/transport.cc
    ${WEBRTC_ROOT}/stats/attribute.cc
    ${WEBRTC_ROOT}/stats/rtc_stats.cc
)

# ----------------------------------------------------------------------------
# PeerConnection (pc) layer - PC实现
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/pc/audio_track.cc
    ${WEBRTC_ROOT}/pc/codec_vendor.cc
    ${WEBRTC_ROOT}/pc/connection_context.cc
    ${WEBRTC_ROOT}/pc/data_channel_utils.cc
    ${WEBRTC_ROOT}/pc/dtls_srtp_transport.cc
    ${WEBRTC_ROOT}/pc/dtls_transport.cc
    ${WEBRTC_ROOT}/pc/dtmf_sender.cc
    ${WEBRTC_ROOT}/pc/external_hmac.cc
    ${WEBRTC_ROOT}/pc/ice_server_parsing.cc
    ${WEBRTC_ROOT}/pc/ice_transport.cc
    ${WEBRTC_ROOT}/pc/jitter_buffer_delay.cc
    ${WEBRTC_ROOT}/pc/jsep_ice_candidate.cc
    ${WEBRTC_ROOT}/pc/jsep_session_description.cc
    ${WEBRTC_ROOT}/pc/jsep_transport_collection.cc
    ${WEBRTC_ROOT}/pc/jsep_transport_controller.cc
    ${WEBRTC_ROOT}/pc/jsep_transport.cc
    ${WEBRTC_ROOT}/pc/local_audio_source.cc
    ${WEBRTC_ROOT}/pc/media_options.cc
    ${WEBRTC_ROOT}/pc/media_protocol_names.cc
    ${WEBRTC_ROOT}/pc/media_stream_observer.cc
    ${WEBRTC_ROOT}/pc/peer_connection_message_handler.cc
    ${WEBRTC_ROOT}/pc/peer_connection.cc
    ${WEBRTC_ROOT}/pc/peer_connection_factory.cc
    ${WEBRTC_ROOT}/pc/remote_audio_source.cc
    ${WEBRTC_ROOT}/pc/rtcp_mux_filter.cc
    ${WEBRTC_ROOT}/pc/rtp_media_utils.cc
    ${WEBRTC_ROOT}/pc/rtp_parameters_conversion.cc
    ${WEBRTC_ROOT}/pc/rtp_transmission_manager.cc
    ${WEBRTC_ROOT}/pc/rtp_transport.cc
    ${WEBRTC_ROOT}/pc/sctp_transport.cc
    ${WEBRTC_ROOT}/pc/sctp_utils.cc
    ${WEBRTC_ROOT}/pc/sdp_munging_detector.cc
    ${WEBRTC_ROOT}/pc/sdp_offer_answer.cc
    ${WEBRTC_ROOT}/pc/sdp_utils.cc
    ${WEBRTC_ROOT}/pc/session_description.cc
    ${WEBRTC_ROOT}/pc/simulcast_description.cc
    ${WEBRTC_ROOT}/pc/simulcast_sdp_serializer.cc
    ${WEBRTC_ROOT}/pc/srtp_session.cc
    ${WEBRTC_ROOT}/pc/srtp_transport.cc
    ${WEBRTC_ROOT}/pc/track_media_info_map.cc
    ${WEBRTC_ROOT}/pc/transceiver_list.cc
    ${WEBRTC_ROOT}/pc/transport_stats.cc
    ${WEBRTC_ROOT}/pc/typed_codec_vendor.cc
    ${WEBRTC_ROOT}/pc/usage_pattern.cc
    ${WEBRTC_ROOT}/pc/video_rtp_receiver.cc
    ${WEBRTC_ROOT}/pc/video_rtp_track_source.cc
    ${WEBRTC_ROOT}/pc/video_track_source.cc
    ${WEBRTC_ROOT}/pc/video_track_source_proxy.cc
    ${WEBRTC_ROOT}/pc/webrtc_sdp.cc
    ${WEBRTC_ROOT}/pc/webrtc_session_description_factory.cc
    ${WEBRTC_ROOT}/pc/legacy_stats_collector.cc
    ${WEBRTC_ROOT}/pc/audio_rtp_receiver.cc
    ${WEBRTC_ROOT}/pc/rtp_transceiver.cc
    ${WEBRTC_ROOT}/pc/data_channel_controller.cc
    ${WEBRTC_ROOT}/pc/rtc_stats_collector.cc
    ${WEBRTC_ROOT}/pc/media_session.cc
    ${WEBRTC_ROOT}/pc/channel.cc
    ${WEBRTC_ROOT}/pc/video_track.cc
    ${WEBRTC_ROOT}/pc/media_stream.cc
    ${WEBRTC_ROOT}/pc/rtp_receiver.cc
    ${WEBRTC_ROOT}/pc/rtp_sender.cc
    ${WEBRTC_ROOT}/pc/sctp_data_channel.cc
    ${WEBRTC_ROOT}/pc/rtc_stats_traversal.cc
)

# ----------------------------------------------------------------------------
# P2P layer - P2P传输
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/p2p/base/async_stun_tcp_socket.cc
    ${WEBRTC_ROOT}/p2p/base/basic_ice_controller.cc
    ${WEBRTC_ROOT}/p2p/base/basic_packet_socket_factory.cc
    ${WEBRTC_ROOT}/p2p/base/connection.cc
    ${WEBRTC_ROOT}/p2p/base/connection_info.cc
    ${WEBRTC_ROOT}/p2p/base/ice_controller_interface.cc
    ${WEBRTC_ROOT}/p2p/base/ice_credentials_iterator.cc
    ${WEBRTC_ROOT}/p2p/base/ice_switch_reason.cc
    ${WEBRTC_ROOT}/p2p/base/ice_transport_internal.cc
    ${WEBRTC_ROOT}/p2p/base/p2p_constants.cc
    ${WEBRTC_ROOT}/p2p/base/p2p_transport_channel.cc
    ${WEBRTC_ROOT}/p2p/base/packet_transport_internal.cc
    ${WEBRTC_ROOT}/p2p/base/port_allocator.cc
    ${WEBRTC_ROOT}/p2p/base/port_interface.cc
    ${WEBRTC_ROOT}/p2p/base/port.cc
    ${WEBRTC_ROOT}/p2p/base/pseudo_tcp.cc
    ${WEBRTC_ROOT}/p2p/base/regathering_controller.cc
    ${WEBRTC_ROOT}/p2p/base/stun_dictionary.cc
    ${WEBRTC_ROOT}/p2p/base/stun_port.cc
    ${WEBRTC_ROOT}/p2p/base/stun_request.cc
    ${WEBRTC_ROOT}/p2p/base/tcp_port.cc
    ${WEBRTC_ROOT}/p2p/base/transport_description.cc
    ${WEBRTC_ROOT}/p2p/base/transport_description_factory.cc
    ${WEBRTC_ROOT}/p2p/base/turn_port.cc
    ${WEBRTC_ROOT}/p2p/base/wrapping_active_ice_controller.cc
    ${WEBRTC_ROOT}/p2p/client/basic_port_allocator.cc
    ${WEBRTC_ROOT}/p2p/client/turn_port_factory.cc
    ${WEBRTC_ROOT}/p2p/base/basic_async_resolver_factory.cc
    ${WEBRTC_ROOT}/p2p/base/default_ice_transport_factory.cc
    ${WEBRTC_ROOT}/p2p/dtls/dtls_transport.cc
    ${WEBRTC_ROOT}/p2p/dtls/dtls_stun_piggyback_controller.cc
    ${WEBRTC_ROOT}/p2p/dtls/dtls_transport_internal.cc
    ${WEBRTC_ROOT}/p2p/dtls/dtls_utils.cc
)

# ----------------------------------------------------------------------------
# RTC_BASE - Additional files
# ----------------------------------------------------------------------------
list(APPEND WEBRTC_SOURCES
    ${WEBRTC_ROOT}/rtc_base/cpu_time.cc
    ${WEBRTC_ROOT}/rtc_base/experiments/alr_experiment.cc
    ${WEBRTC_ROOT}/rtc_base/experiments/balanced_degradation_settings.cc
    ${WEBRTC_ROOT}/rtc_base/experiments/encoder_info_settings.cc
    ${WEBRTC_ROOT}/rtc_base/experiments/keyframe_interval_settings.cc
    ${WEBRTC_ROOT}/rtc_base/experiments/min_video_bitrate_experiment.cc
    ${WEBRTC_ROOT}/rtc_base/experiments/normalize_simulcast_size_experiment.cc
    ${WEBRTC_ROOT}/rtc_base/experiments/quality_scaler_settings.cc
    ${WEBRTC_ROOT}/rtc_base/experiments/quality_scaling_experiment.cc
    ${WEBRTC_ROOT}/rtc_base/experiments/rate_control_settings.cc
    ${WEBRTC_ROOT}/rtc_base/experiments/stable_target_rate_experiment.cc
    ${WEBRTC_ROOT}/rtc_base/experiments/struct_parameters_parser.cc
    ${WEBRTC_ROOT}/rtc_base/file_rotating_stream.cc
    ${WEBRTC_ROOT}/rtc_base/firewall_socket_server.cc
    ${WEBRTC_ROOT}/rtc_base/frequency_tracker.cc
    ${WEBRTC_ROOT}/rtc_base/log_sinks.cc
    ${WEBRTC_ROOT}/rtc_base/memory_stream.cc
    ${WEBRTC_ROOT}/rtc_base/net_helper.cc
    ${WEBRTC_ROOT}/rtc_base/net_test_helpers.cc
    ${WEBRTC_ROOT}/rtc_base/network_monitor.cc
    ${WEBRTC_ROOT}/rtc_base/network_monitor_factory.cc
    ${WEBRTC_ROOT}/rtc_base/numerics/event_rate_counter.cc
    ${WEBRTC_ROOT}/rtc_base/numerics/histogram_percentile_counter.cc
    ${WEBRTC_ROOT}/rtc_base/numerics/sample_counter.cc
    ${WEBRTC_ROOT}/rtc_base/numerics/sample_stats.cc
    ${WEBRTC_ROOT}/rtc_base/openssl_certificate.cc
    ${WEBRTC_ROOT}/rtc_base/openssl_identity.cc
    ${WEBRTC_ROOT}/rtc_base/rate_statistics.cc
    ${WEBRTC_ROOT}/rtc_base/server_socket_adapters.cc
)

add_library(webrtc STATIC ${WEBRTC_SOURCES})

# Link libraries for WebRTC
# 注意: Abseil符号已直接打包进webrtc静态库中，无需链接absl::目标
target_link_libraries(webrtc
    srtp                    # libsrtp
    yuv                     # libyuv
    opus                    # opus audio codec
    OpenSSL::Crypto
    OpenSSL::SSL
    pthread
    dl
    m
)

# Add demo executable
add_executable(peerconnection_demo
    demo/peerconnection_demo.cc
)

target_link_libraries(peerconnection_demo
    webrtc
    pthread
    dl
)

# Install target
install(TARGETS peerconnection_demo DESTINATION bin)
