// Link every production object (including optional Apple audio entry points).
// This program intentionally does not open devices and can be cross-linked for iOS.
#include "rtc_base/ssl_adapter.h"

int main() {
  if (!webrtc::InitializeSSL()) return 1;
  return webrtc::CleanupSSL() ? 0 : 1;
}
