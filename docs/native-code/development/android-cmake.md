# Android native CMake build

This build produces the native C++ WebRTC core for **arm64-v8a** and **x86_64**,
with Android API **24 or newer**, C++20 and one ABI per build directory.
It uses the same `WebRTC::webrtc` and `WebRTC::<module>` targets as the desktop
and Apple builds. ARMv7 and 32-bit x86 are not supported by this CMake port.

## Scope

Included: PeerConnection, ICE/DTLS/SRTP/SCTP, software audio/video codecs,
audio processing, video processing, Android logging and native interface
enumeration. ARM64 enables WebRTC/libyuv NEON and libaom optimizations. The
dependency helper uses portable C libvpx/dav1d; Opus also uses portable C on
ARM64. Performance tuning of these codecs is separate from build correctness.

The application must supply an `AudioDeviceModule` through
`PeerConnectionFactoryDependencies::adm` (or the `default_adm` argument of
`CreatePeerConnectionFactory`) for microphone/playout. The upstream Android
Java/OpenSL ES/AAudio factories require Java classes and generated JNI bindings
and are **not** linked by this native-only build. There is no automatic silent
dummy replacement for device audio. For headless tests explicitly request
`AudioDeviceModule::kDummyAudio`, as `demo/peerconnection_demo.cc` does.

Camera/screen capture, MediaCodec wrappers, Java network monitoring, JNI API,
AAR packaging and an Android application are not part of this target. Supply
video frames through an application video source. The legacy
`VideoCaptureFactory` returns null on Android, matching its upstream behavior.
Native interface enumeration is the upstream `ifaddrs_android` implementation;
application network permissions, network changes and OS restrictions still
need integration testing.

## Dependencies and build

Use an Android NDK with C++20 support, CMake 3.21+, Ninja, Python 3, Perl, make,
Meson and NASM (for x86 libaom). The dependency helper runs on macOS and Linux.
OpenSSL, libvpx and dav1d must match the **ABI and API level** of WebRTC; host
Homebrew libraries cannot be used. All commands below run in the WebRTC root.

Obtain and verify an OpenSSL source release separately, then pass its unpacked
directory. The helper uses the libvpx/dav1d sources pinned in this checkout and
installs only into `out/android-deps/<abi>/api-<api>/install`.

```sh
export ANDROID_NDK_HOME=/path/to/android-sdk/ndk/25.1.8937393
python3 -m venv out/build-tools
out/build-tools/bin/pip install meson ninja
export PATH="$PWD/out/build-tools/bin:$PATH"

python3 scripts/build-android-deps.py --abi arm64-v8a \
  --openssl-source /path/to/openssl-source --jobs 4
cmake --preset android-arm64-v8a
cmake --build --preset android-arm64-v8a
python3 scripts/check-android-build.py out/android-arm64-v8a --abi arm64-v8a

python3 scripts/build-android-deps.py --abi x86_64 \
  --openssl-source /path/to/openssl-source --jobs 4
cmake --preset android-x86_64
cmake --build --preset android-x86_64
python3 scripts/check-android-build.py out/android-x86_64 --abi x86_64
```

The helper also accepts `--ndk`, `--api`, `--output` and `--jobs`. It refuses to
reuse a dependency directory with a different NDK, ABI, API or OpenSSL source
path. To use a higher API level, build the dependencies with that `--api` and
configure a **new** build directory with matching `ANDROID_PLATFORM`,
`CMAKE_FIND_ROOT_PATH`, `CMAKE_PREFIX_PATH` and `OPENSSL_ROOT_DIR`:

```sh
cmake --preset android-arm64-v8a -B out/android-arm64-api28 \
  -DANDROID_PLATFORM=android-28 \
  -DCMAKE_FIND_ROOT_PATH="$PWD/out/android-deps/arm64-v8a/api-28/install" \
  -DCMAKE_PREFIX_PATH="$PWD/out/android-deps/arm64-v8a/api-28/install" \
  -DOPENSSL_ROOT_DIR="$PWD/out/android-deps/arm64-v8a/api-28/install"
```

The presets use the official NDK toolchain directly and restrict package,
library and include lookup to the target roots. They default to `c++_static`
for embedding WebRTC in one application shared library. Applications with
multiple C++ shared libraries should select a consistent STL strategy across
all components, such as `-DANDROID_STL=c++_shared`, and package that runtime.

## Artifacts and embedding

For each `out/android-<abi>` directory:

- `Release/libwebrtc.a`: aggregate WebRTC archive.
- `Release/modules/libwebrtc_<module>.a`: individual module archives.
- `libandroid_link_smoke.so`: full-production-object shared-library link check.

The aggregate does not embed third-party archives. Prefer linking the CMake
target, which propagates headers, platform definitions and dependencies:

```cmake
set(WEBRTC_BUILD_DEMO OFF CACHE BOOL "" FORCE)
add_subdirectory(/path/to/webrtc webrtc-build)
target_link_libraries(your_android_library PRIVATE WebRTC::webrtc)
```

Configure the enclosing project with the same NDK toolchain and target
dependency prefixes. Do not link both the aggregate and module archives.
Individual modules are building blocks, not independently dependency-closed
SDKs. Java-native declarations under `sdk/android` are not promised by the
native CMake target.

## Automated checks and device acceptance

`android_link_smoke` uses `--whole-archive` and `--no-undefined` to expose missing
production implementations and non-PIC dependencies. Its ELF load segments
use 16 KiB alignment. It is a **link check**, not a microphone/camera or call
test, and the probe `.so` is not an application SDK package. Apply the desired
page alignment to the final application's shared library as well.

`check-android-build.py` audits ABI/API triples, NDK sysroots, Android definitions,
unique module ownership, required Android/NEON sources, and accidental host
or x86-on-ARM flags. It does not run the compiled code.

For an optional headless execution test, configure with
`-DWEBRTC_BUILD_DEMO=ON`, build `peerconnection_demo` (and
`matched_filter_smoke` on x86_64), then execute those binaries on a matching
Android device/emulator, for example under `/data/local/tmp`. They use dummy
audio and do not open microphone/camera devices. Cross-built executables
cannot be run directly on the host.

Real-device acceptance remains separate: microphone permission and routing,
camera sources, network switching, codecs under load, app lifecycle and a
real end-to-end media call all require an integrating application and devices.
