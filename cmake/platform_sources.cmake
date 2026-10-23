if(WIN32)
    list(FILTER WEBRTC_SOURCES EXCLUDE REGEX "/modules/video_capture/linux/")
    list(REMOVE_ITEM WEBRTC_SOURCES
        "${WEBRTC_ROOT}/rtc_base/ifaddrs_converter.cc"
        "${WEBRTC_ROOT}/system_wrappers/source/cpu_features_linux.cc")
    list(APPEND WEBRTC_SOURCES
        "${WEBRTC_ROOT}/rtc_base/win32.cc"
        "${WEBRTC_ROOT}/rtc_base/win/scoped_com_initializer.cc"
        "${WEBRTC_ROOT}/rtc_base/win/windows_version.cc"
        "${WEBRTC_ROOT}/modules/audio_device/win/audio_device_core_win.cc"
        "${WEBRTC_ROOT}/modules/video_capture/windows/device_info_ds.cc"
        "${WEBRTC_ROOT}/modules/video_capture/windows/help_functions_ds.cc"
        "${WEBRTC_ROOT}/modules/video_capture/windows/sink_filter_ds.cc"
        "${WEBRTC_ROOT}/modules/video_capture/windows/video_capture_ds.cc"
        "${WEBRTC_ROOT}/modules/video_capture/windows/video_capture_factory_windows.cc")
endif()
