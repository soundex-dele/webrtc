# Curated production sources; platform/SIMD selection is applied by webrtc_add_module.
webrtc_add_module(audio
    audio/audio_level.cc
    audio/audio_receive_stream.cc
    audio/audio_send_stream.cc
    audio/audio_state.cc
    audio/audio_transport_impl.cc
    audio/channel_receive.cc
    audio/channel_receive_frame_transformer_delegate.cc
    audio/channel_send.cc
    audio/channel_send_frame_transformer_delegate.cc
    audio/remix_resample.cc
    audio/utility/audio_frame_operations.cc
    audio/utility/channel_mixer.cc
    audio/utility/channel_mixing_matrix.cc
)
