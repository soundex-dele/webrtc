// Numerical regression coverage for the MSVC-compatible AVX2 lane access.
#include <algorithm>
#include <cmath>
#include <iostream>
#include <random>
#include <vector>

#include "modules/audio_processing/aec3/matched_filter.h"
#include "system_wrappers/include/cpu_features_wrapper.h"

int main() {
  if (!webrtc::GetCPUInfo(webrtc::kAVX2) ||
      !webrtc::GetCPUInfo(webrtc::kFMA3)) {
    std::cout << "AVX2/FMA unavailable; skipped\n";
    return 77;
  }
  std::mt19937 random(42);
  std::uniform_real_distribution<float> sample(-1000.f, 1000.f);
  for (bool accumulated : {false, true}) {
    for (size_t block_size : {8, 16, 32}) {
      std::vector<float> x(2000), y(block_size);
      std::vector<float> reference(512), optimized(512), scratch(512);
      std::vector<float> ref_accumulated(128), avx_accumulated(128);
      for (auto& value : x) value = sample(random);
      for (size_t iteration = 0; iteration < 300; ++iteration) {
        for (auto& value : y) value = sample(random);
        // Include saturation and ring-buffer wrapping, as well as both paths
        // through the optional accumulated-error calculation.
        if (iteration % 17 == 0) y[0] = 32000.f;
        const size_t start = (iteration * block_size) % x.size();
        bool ref_updated = false, avx_updated = false;
        float ref_error = 0, avx_error = 0;
        webrtc::aec3::MatchedFilterCore(
            start, 512.f * 150.f * 150.f, 0.7f, x, y, reference,
            &ref_updated, &ref_error, accumulated, ref_accumulated);
        webrtc::aec3::MatchedFilterCore_AVX2(
            start, 512.f * 150.f * 150.f, 0.7f, x, y, optimized,
            &avx_updated, &avx_error, accumulated, avx_accumulated, scratch);
        if (ref_updated != avx_updated || !std::isfinite(avx_error) ||
            std::abs(ref_error - avx_error) > std::max(1.f, ref_error) * 1e-5f) {
          std::cerr << "Filter error mismatch at iteration " << iteration << '\n';
          return 1;
        }
        for (size_t i = 0; i < reference.size(); ++i) {
          if (!std::isfinite(optimized[i]) ||
              std::abs(reference[i] - optimized[i]) > 1e-5f) {
            std::cerr << "Filter coefficient mismatch\n";
            return 1;
          }
        }
        if (accumulated) {
          for (size_t i = 0; i < ref_accumulated.size(); ++i) {
            if (!std::isfinite(avx_accumulated[i]) ||
                std::abs(ref_accumulated[i] - avx_accumulated[i]) >
                    std::max(1.f, ref_accumulated[i]) * 1e-5f) {
              std::cerr << "Accumulated error mismatch at lane " << i << '\n';
              return 1;
            }
          }
        }
      }
    }
  }
  std::cout << "AVX2 and scalar matched filters agree\n";
  return 0;
}
