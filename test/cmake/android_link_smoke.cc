// Whole-archive shared-library link probe; no JNI or device access.
#include "rtc_base/ssl_adapter.h"

extern "C" __attribute__((visibility("default"))) int WebRtcAndroidLinkSmoke() {
  if (!webrtc::InitializeSSL()) return 1;
  return webrtc::CleanupSSL() ? 0 : 1;
}
