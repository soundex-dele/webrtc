# Curated production sources; platform/SIMD selection is applied by webrtc_add_module.
webrtc_add_module(system_wrappers
    system_wrappers/source/clock.cc
    system_wrappers/source/cpu_features.cc
    system_wrappers/source/cpu_features_linux.cc
    system_wrappers/source/cpu_info.cc
    system_wrappers/source/denormal_disabler.cc
    system_wrappers/source/field_trial.cc
    system_wrappers/source/metrics.cc
    system_wrappers/source/rtp_to_ntp_estimator.cc
    system_wrappers/source/sleep.cc
)
