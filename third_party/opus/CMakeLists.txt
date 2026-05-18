cmake_minimum_required(VERSION 3.16)
project(opus C)

# Opus library - simplified build for WebRTC

add_compile_definitions(
    OPUS_BUILD
    OPUS_EXPORT=
    USE_ALLOCA
    HAVE_ALLOCA_H
    ENABLE_HARDENING
)

# Compile options for x86_64
if(CMAKE_SYSTEM_PROCESSOR MATCHES "x86_64" OR CMAKE_SIZEOF_VOID_P EQUAL 8)
    add_compile_definitions(
        OPUS_HAVE_RTCD
        OPUS_X86_MAY_HAVE_SSE
        OPUS_X86_MAY_HAVE_SSE2
        OPUS_X86_PRESUME_SSE
        OPUS_X86_PRESUME_SSE2
        OPUS_X86_MAY_HAVE_SSE4_1
        CPU_INFO_BY_C
        HAVE_LRINT
        HAVE_LRINTF
    )
endif()

include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/src/include
    ${CMAKE_CURRENT_SOURCE_DIR}/src
    ${CMAKE_CURRENT_SOURCE_DIR}/src/celt
    ${CMAKE_CURRENT_SOURCE_DIR}/src/silk
    ${CMAKE_CURRENT_SOURCE_DIR}/src/silk/fixed
    ${CMAKE_CURRENT_SOURCE_DIR}/src/silk/float
)

# Opus source files
set(OPUS_SOURCES
    # Main opus source
    src/src/opus.c
    src/src/opus_decoder.c
    src/src/opus_encoder.c
    src/src/opus_multistream.c
    src/src/opus_multistream_decoder.c
    src/src/opus_multistream_encoder.c
    src/src/repacketizer.c
    src/src/extensions.c
    src/src/analysis.c
    src/src/mapping_matrix.c
    src/src/mlp.c
    src/src/mlp_data.c

    # CELT source
    src/celt/bands.c
    src/celt/celt.c
    src/celt/celt_decoder.c
    src/celt/celt_encoder.c
    src/celt/celt_lpc.c
    src/celt/cwrs.c
    src/celt/entcode.c
    src/celt/entdec.c
    src/celt/entenc.c
    src/celt/kiss_fft.c
    src/celt/laplace.c
    src/celt/mathops.c
    src/celt/mdct.c
    src/celt/modes.c
    src/celt/pitch.c
    src/celt/quant_bands.c
    src/celt/rate.c
    src/celt/vq.c

    # SILK source
    src/silk/A2NLSF.c
    src/silk/CNG.c
    src/silk/LPC_analysis_filter.c
    src/silk/LPC_fit.c
    src/silk/LPC_inv_pred_gain.c
    src/silk/HP_variable_cutoff.c
    src/silk/LP_variable_cutoff.c
    src/silk/NLSF2A.c
    src/silk/NLSF_VQ.c
    src/silk/NLSF_VQ_weights_laroia.c
    src/silk/NLSF_decode.c
    src/silk/NLSF_del_dec_quant.c
    src/silk/NLSF_encode.c
    src/silk/NLSF_stabilize.c
    src/silk/NLSF_unpack.c
    src/silk/NSQ.c
    src/silk/NSQ_del_dec.c
    src/silk/PLC.c
    src/silk/VAD.c
    src/silk/VQ_WMat_EC.c
    src/silk/ana_filt_bank_1.c
    src/silk/biquad_alt.c
    src/silk/bwexpander.c
    src/silk/bwexpander_32.c
    src/silk/check_control_input.c
    src/silk/code_signs.c
    src/silk/control_SNR.c
    src/silk/control_audio_bandwidth.c
    src/silk/control_codec.c
    src/silk/debug.c
    src/silk/dec_API.c
    src/silk/decode_core.c
    src/silk/decode_frame.c
    src/silk/decode_indices.c
    src/silk/decode_parameters.c
    src/silk/decode_pitch.c
    src/silk/decode_pulses.c
    src/silk/decoder_set_fs.c
    src/silk/enc_API.c
    src/silk/encode_indices.c
    src/silk/encode_pulses.c
    src/silk/gain_quant.c
    src/silk/init_decoder.c
    src/silk/init_encoder.c
    src/silk/inner_prod_aligned.c
    src/silk/interpolate.c
    src/silk/lin2log.c
    src/silk/log2lin.c
    src/silk/pitch_est_tables.c
    src/silk/process_NLSFs.c
    src/silk/quant_LTP_gains.c
    src/silk/resampler.c
    src/silk/resampler_down2.c
    src/silk/resampler_down2_3.c
    src/silk/resampler_private_AR2.c
    src/silk/resampler_private_IIR_FIR.c
    src/silk/resampler_private_down_FIR.c
    src/silk/resampler_private_up2_HQ.c
    src/silk/resampler_rom.c
    src/silk/shell_coder.c
    src/silk/sigm_Q15.c
    src/silk/sort.c
    src/silk/stereo_LR_to_MS.c
    src/silk/stereo_MS_to_LR.c
    src/silk/stereo_decode_pred.c
    src/silk/stereo_encode_pred.c
    src/silk/stereo_find_predictor.c
    src/silk/stereo_quant_pred.c
    src/silk/sum_sqr_shift.c
    src/silk/table_LSF_cos.c
    src/silk/tables_LTP.c
    src/silk/tables_NLSF_CB_NB_MB.c
    src/silk/tables_NLSF_CB_WB.c
    src/silk/tables_gain.c
    src/silk/tables_other.c
    src/silk/tables_pitch_lag.c
    src/silk/tables_pulses_per_block.c

    # SILK fixed-point
    src/silk/fixed/LTP_analysis_filter_FIX.c
    src/silk/fixed/LTP_scale_ctrl_FIX.c
    src/silk/fixed/apply_sine_window_FIX.c
    src/silk/fixed/autocorr_FIX.c
    src/silk/fixed/burg_modified_FIX.c
    src/silk/fixed/corrMatrix_FIX.c
    src/silk/fixed/encode_frame_FIX.c
    src/silk/fixed/find_LPC_FIX.c
    src/silk/fixed/find_LTP_FIX.c
    src/silk/fixed/find_pitch_lags_FIX.c
    src/silk/fixed/find_pred_coefs_FIX.c
    src/silk/fixed/k2a_FIX.c
    src/silk/fixed/k2a_Q16_FIX.c
    src/silk/fixed/noise_shape_analysis_FIX.c
    src/silk/fixed/pitch_analysis_core_FIX.c
    src/silk/fixed/process_gains_FIX.c
    src/silk/fixed/regularize_correlations_FIX.c
    src/silk/fixed/residual_energy16_FIX.c
    src/silk/fixed/residual_energy_FIX.c
    src/silk/fixed/schur64_FIX.c
    src/silk/fixed/schur_FIX.c
    src/silk/fixed/vector_ops_FIX.c
    src/silk/fixed/warped_autocorrelation_FIX.c

    # SILK float
    src/silk/float/LPC_analysis_filter_FLP.c
    src/silk/float/LPC_inv_pred_gain_FLP.c
    src/silk/float/LTP_analysis_filter_FLP.c
    src/silk/float/LTP_scale_ctrl_FLP.c
    src/silk/float/apply_sine_window_FLP.c
    src/silk/float/autocorrelation_FLP.c
    src/silk/float/burg_modified_FLP.c
    src/silk/float/bwexpander_FLP.c
    src/silk/float/corrMatrix_FLP.c
    src/silk/float/encode_frame_FLP.c
    src/silk/float/energy_FLP.c
    src/silk/float/find_LPC_FLP.c
    src/silk/float/find_LTP_FLP.c
    src/silk/float/find_pitch_lags_FLP.c
    src/silk/float/find_pred_coefs_FLP.c
    src/silk/float/inner_product_FLP.c
    src/silk/float/k2a_FLP.c
    src/silk/float/noise_shape_analysis_FLP.c
    src/silk/float/pitch_analysis_core_FLP.c
    src/silk/float/process_gains_FLP.c
    src/silk/float/regularize_correlations_FLP.c
    src/silk/float/residual_energy_FLP.c
    src/silk/float/scale_copy_vector_FLP.c
    src/silk/float/scale_vector_FLP.c
    src/silk/float/schur_FLP.c
    src/silk/float/sort_FLP.c
    src/silk/float/warped_autocorrelation_FLP.c
    src/silk/float/wrappers_FLP.c
)

# Platform-specific optimizations
if(CMAKE_SYSTEM_PROCESSOR MATCHES "x86_64" OR CMAKE_SYSTEM_PROCESSOR MATCHES "i686" OR CMAKE_SIZEOF_VOID_P EQUAL 8)
    list(APPEND OPUS_SOURCES
        # CELT x86 optimizations
        src/celt/x86/celt_lpc_sse4_1.c
        src/celt/x86/pitch_sse.c
        src/celt/x86/pitch_sse2.c
        src/celt/x86/pitch_sse4_1.c
        src/celt/x86/pitch_avx.c
        src/celt/x86/vq_sse2.c
        src/celt/x86/x86cpu.c
        src/celt/x86/x86_celt_map.c

        # SILK x86 optimizations
        src/silk/x86/NSQ_sse4_1.c
        src/silk/x86/NSQ_del_dec_sse4_1.c
        src/silk/x86/VAD_sse4_1.c
        src/silk/x86/VQ_WMat_EC_sse4_1.c
        src/silk/x86/x86_silk_map.c

        # SILK float x86 optimizations
        src/silk/float/x86/inner_product_FLP_avx2.c
    )

    # Set SSE compile flags for specific files
    set_source_files_properties(
        src/celt/x86/pitch_sse.c
        PROPERTIES COMPILE_FLAGS "-msse"
    )

    set_source_files_properties(
        src/celt/x86/pitch_sse2.c
        src/celt/x86/vq_sse2.c
        PROPERTIES COMPILE_FLAGS "-msse2"
    )

    set_source_files_properties(
        src/celt/x86/celt_lpc_sse4_1.c
        src/celt/x86/pitch_sse4_1.c
        src/celt/x86/pitch_avx.c
        src/silk/x86/NSQ_sse4_1.c
        src/silk/x86/VAD_sse4_1.c
        src/silk/x86/VQ_WMat_EC_sse4_1.c
        src/silk/x86/NSQ_del_dec_sse4_1.c
        PROPERTIES COMPILE_FLAGS "-msse4.1"
    )

    set_source_files_properties(
        src/celt/x86/pitch_avx.c
        src/silk/float/x86/inner_product_FLP_avx2.c
        PROPERTIES COMPILE_FLAGS "-mavx2 -mfma"
    )
endif()

if(CMAKE_SYSTEM_PROCESSOR MATCHES "arm" OR CMAKE_SYSTEM_PROCESSOR MATCHES "aarch64")
    list(APPEND OPUS_SOURCES
        # ARM optimizations
        src/celt/arm/armcpu.c
        src/celt/arm/arm_celt_map.c
        src/silk/arm/arm_silk_map.c
        src/silk/arm/biquad_alt_neon_intr.c
        src/silk/arm/NSQ_neon.c
        src/silk/arm/LPC_inv_pred_gain_neon_intr.c
        src/silk/arm/NSQ_del_dec_neon_intr.c
        src/celt/arm/celt_neon_intr.c
        src/celt/arm/pitch_neon_intr.c
    )
endif()

# CPU info helper (needed for runtime detection)
list(APPEND OPUS_SOURCES
    src/cmake/cpu_info_by_c.c
)

add_library(opus STATIC ${OPUS_SOURCES})
add_library(Opus::opus ALIAS opus)
