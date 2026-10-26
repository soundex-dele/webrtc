# Amend each curated module manifest without pulling tests or examples in via glob.
function(webrtc_select_platform_sources module result)
    set(sources ${${result}})
    if(NOT WEBRTC_ARCH_X64)
        list(FILTER sources EXCLUDE REGEX "_(avx2|sse|sse2)\\.cc$")
    endif()
    if(NOT CMAKE_SYSTEM_NAME STREQUAL "Linux")
        list(FILTER sources EXCLUDE REGEX "/linux/|/cpu_features_linux\\.cc$")
    endif()
    if(module STREQUAL "common_audio" AND WEBRTC_ARCH_ARM64)
        list(APPEND sources common_audio/fir_filter_neon.cc
            common_audio/resampler/sinc_resampler_neon.cc
            common_audio/signal_processing/cross_correlation_neon.c
            common_audio/signal_processing/downsample_fast_neon.c
            common_audio/signal_processing/min_max_operations_neon.c
            common_audio/third_party/ooura/fft_size_128/ooura_fft_neon.cc)
    endif()
    if(module STREQUAL "audio_processing" AND WEBRTC_ARCH_ARM64)
        list(APPEND sources modules/audio_processing/aecm/aecm_core_neon.cc)
    endif()
    if(ANDROID AND module STREQUAL "rtc_base")
        list(APPEND sources rtc_base/ifaddrs_android.cc)
    endif()
    if(WIN32)
        list(REMOVE_ITEM sources rtc_base/ifaddrs_converter.cc)
        if(module STREQUAL "rtc_base")
            list(APPEND sources rtc_base/win32.cc rtc_base/win/scoped_com_initializer.cc
                rtc_base/win/windows_version.cc)
        elseif(module STREQUAL "audio_device")
            list(APPEND sources modules/audio_device/win/audio_device_core_win.cc)
        elseif(module STREQUAL "video_capture")
            list(APPEND sources
                modules/video_capture/windows/device_info_ds.cc
                modules/video_capture/windows/help_functions_ds.cc
                modules/video_capture/windows/sink_filter_ds.cc
                modules/video_capture/windows/video_capture_ds.cc
                modules/video_capture/windows/video_capture_factory_windows.cc)
        endif()
    endif()
    if(APPLE)
        if(module STREQUAL "rtc_base")
            list(APPEND sources rtc_base/mac_ifaddrs_converter.cc
                rtc_base/system/cocoa_threading.mm)
        elseif(module STREQUAL "audio_device")
            list(APPEND sources modules/audio_device/audio_engine_device.mm)
            if(CMAKE_SYSTEM_NAME STREQUAL "iOS")
                list(APPEND sources
                    sdk/objc/native/api/audio_device_module.mm
                    sdk/objc/native/src/audio/audio_device_ios.mm
                    sdk/objc/native/src/audio/audio_device_module_ios.mm
                    sdk/objc/native/src/audio/voice_processing_audio_unit.mm
                    sdk/objc/native/src/audio/helpers.mm
                    sdk/objc/components/audio/RTCAudioSession.mm
                    sdk/objc/components/audio/RTCAudioSession+Configuration.mm
                    sdk/objc/components/audio/RTCAudioSessionConfiguration.m
                    sdk/objc/components/audio/RTCNativeAudioSessionDelegateAdapter.mm
                    sdk/objc/base/RTCLogging.mm
                    sdk/objc/helpers/NSString+StdString.mm
                    sdk/objc/helpers/RTCDispatcher.m
                    sdk/objc/helpers/UIDevice+RTCDevice.mm)
            else()
                list(APPEND sources
                    modules/audio_device/mac/audio_device_mac.cc
                    modules/audio_device/mac/audio_device_utils_mac.cc
                    modules/audio_device/mac/audio_mixer_manager_mac.cc
                    modules/third_party/portaudio/pa_ringbuffer.c)
            endif()
        endif()
    endif()
    set(${result} ${sources} PARENT_SCOPE)
endfunction()
