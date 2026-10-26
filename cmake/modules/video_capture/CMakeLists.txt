# Curated production sources; platform/SIMD selection is applied by webrtc_add_module.
webrtc_add_module(video_capture
    modules/video_capture/device_info_impl.cc
    modules/video_capture/linux/device_info_linux.cc
    modules/video_capture/linux/device_info_v4l2.cc
    modules/video_capture/linux/video_capture_linux.cc
    modules/video_capture/linux/video_capture_v4l2.cc
    modules/video_capture/video_capture_factory.cc
    modules/video_capture/video_capture_impl.cc
    modules/video_capture/video_capture_options.cc
)
