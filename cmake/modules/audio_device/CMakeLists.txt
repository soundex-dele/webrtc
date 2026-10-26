# Curated production sources; platform/SIMD selection is applied by webrtc_add_module.
webrtc_add_module(audio_device
    modules/audio_device/audio_device_buffer.cc
    modules/audio_device/audio_device_data_observer.cc
    modules/audio_device/audio_device_generic.cc
    modules/audio_device/audio_device_impl.cc
    modules/audio_device/audio_device_name.cc
    modules/audio_device/dummy/audio_device_dummy.cc
    modules/audio_device/dummy/file_audio_device.cc
    modules/audio_device/dummy/file_audio_device_factory.cc
    modules/audio_device/fine_audio_buffer.cc
)
