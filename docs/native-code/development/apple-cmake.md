# macOS / iOS CMake build

The native C++ build supports macOS x86_64/arm64, iOS arm64, and iOS simulator
x86_64/arm64. Each build directory contains exactly one SDK/architecture slice.
Windows/Linux x64 and the `WebRTC::webrtc` target remain supported.

## Prerequisites

Use Xcode with the selected Apple SDK, CMake 3.21+, make, Perl and NASM (x86 AOM).
The bundled source dependencies are built by CMake. OpenSSL, libvpx and dav1d
must be supplied for the **same SDK, architecture and deployment target**.
Run the commands below from the WebRTC repository root.

For a native macOS build, installed Homebrew dependencies can be used:

```sh
brew install cmake nasm openssl@3 libvpx dav1d
cmake --preset macos-x86_64 \
  -DOPENSSL_ROOT_DIR="$(brew --prefix openssl@3)" \
  -DCMAKE_PREFIX_PATH="$(brew --prefix libvpx);$(brew --prefix dav1d)"
cmake --build out/macos-x86_64 --target webrtc_modules peerconnection_demo matched_filter_smoke apple_link_smoke -j4
ctest --test-dir out/macos-x86_64 --output-on-failure
```

On Apple Silicon use `macos-arm64` and omit `matched_filter_smoke`, which tests
x86 AVX2/FMA specifically. An Intel Homebrew prefix cannot supply arm64 libraries.

## Build dependencies for a cross-compiled slice

The helper installs only into `out/apple-deps/<sdk>-<arch>/install`; it never
installs globally. It uses the checkout's pinned libvpx/dav1d sources and a
caller-supplied, unpacked OpenSSL source release (tested with OpenSSL 3.6.3).
Obtain and verify the OpenSSL release separately before passing its directory.
Meson and Ninja can be installed into an isolated Python environment:

```sh
python3 -m venv out/build-tools
out/build-tools/bin/pip install meson ninja
export PATH="$PWD/out/build-tools/bin:$PATH"
python3 scripts/build-apple-deps.py --sdk iphoneos --arch arm64 \
  --openssl-source /path/to/openssl-3.6.3 --jobs 4
cmake --preset ios-arm64
cmake --build --preset ios-arm64
cmake --build out/ios-arm64 --target apple_link_smoke -j4
```

Simulator example (use `arm64` on an Apple Silicon simulator host):

```sh
python3 scripts/build-apple-deps.py --sdk iphonesimulator --arch x86_64 \
  --openssl-source /path/to/openssl-3.6.3 --jobs 4
cmake --preset ios-simulator-x86_64
cmake --build --preset ios-simulator-x86_64
cmake --build out/ios-simulator-x86_64 --target apple_link_smoke -j4
```

For cross-compiling macOS arm64 on Intel, use the helper with `--sdk macosx
--arch arm64`, and pass the resulting prefix as both `CMAKE_PREFIX_PATH` and
`OPENSSL_ROOT_DIR` to `macos-arm64`.

Defaults are macOS 12.0 and iOS 13.0. If changing these, set the helper's
`--deployment-target` and CMake's `CMAKE_OSX_DEPLOYMENT_TARGET` consistently.
The helper refuses to reuse a directory with a different SDK/version/source;
use a new `--output` directory and set `CMAKE_FIND_ROOT_PATH`/`CMAKE_PREFIX_PATH`
to its install prefix. A supplied vcpkg toolchain and matching Apple triplet can
also provide the dependencies. The libvpx lookup accepts either the vcpkg
`unofficial-libvpx` package or a prefix containing `include/vpx` and `lib/libvpx.a`.

The dependency helper uses portable C libvpx/dav1d kernels to avoid legacy
libvpx Darwin presets changing the requested SDK. Opus also uses portable C on
ARM64. WebRTC NEON, libyuv NEON and libaom remain enabled on ARM64. This is a
correctness-oriented baseline; codec SIMD performance tuning is separate work.

## Modules and output contract

`cmake/modules/<name>/CMakeLists.txt` owns each module's explicit production
source list. `platform_sources.cmake` selects platform implementations and SIMD
sources; it does not glob tests/examples into the build. The old manifest's
NetEq/RTP CLI helpers, test virtual socket server and AGC curve-generation tool
are excluded: they reference test-only implementations (one also defines
`main`) and are not part of the production library.

Modules: `api`, `rtc_base`, `system_wrappers`, `common_audio`, `common_video`,
`audio_coding`, `audio_processing` (including mixer/async processing),
`audio_device`, `video_coding`, `rtp_rtcp`, `congestion_control`, `net` (dcsctp),
`p2p`, `logging`, `media`, `audio`, `video`, `call`, `pc`, `video_capture`.

```sh
cmake --build out/macos-arm64 --target webrtc_audio_processing -j4
cmake --build out/macos-arm64 --target webrtc_modules -j4
cmake --build out/macos-arm64 --target webrtc -j4
```

- `webrtc_<name>_objects`: compiles only that module's WebRTC translation units.
- `webrtc_<name>` / `WebRTC::<name>`: archives them as
  `Release/modules/libwebrtc_<name>.a` (Windows: `webrtc_<name>.lib`).
- `webrtc_modules`: builds all module archives.
- `webrtc` / `WebRTC::webrtc`: combines the same objects into
  `Release/libwebrtc.a` (Windows: `Release/webrtc.lib`), without recompiling.

Module archives are build/link building blocks, not dependency-closed SDKs:
WebRTC's internal cross-module references still require other modules. Normal
applications should link `WebRTC::webrtc`, which propagates external libraries,
frameworks, include paths and public platform definitions. Do not link both the
aggregate and its constituent archives. The aggregate still does **not** embed
third-party archives. Keep those dependencies with each SDK slice if packaging
an XCFramework; device and simulator arm64 are different platforms and must
not be merged with `lipo`.

Consumers needing source inspection can read target property
`WEBRTC_SOURCE_MANIFEST`; `SOURCES` now contains module object expressions.
Use `WEBRTC_BUILD_VIDEO_CAPTURE=OFF` before `add_subdirectory` to omit the legacy
capture module. This replaces editing the aggregate's `SOURCES` property.

## Apple behavior and verification

macOS builds include the CoreAudio ADM and AVAudioEngine implementation. iOS
builds include AudioUnit ADM, AVAudioEngine, RTCAudioSession and native audio
module factories, with ARC for Objective-C/Objective-C++. Required Apple
frameworks and the iOS `-ObjC` category-loading flag are transitive link requirements. Linux sources and x86 intrinsics
are excluded from Apple ARM64 builds; arm64 never receives `-mfpu=neon`.

This builds the native C++ library and the Objective-C audio support it needs.
It does not package the full public Objective-C/Swift WebRTC.framework API or
add camera/screen capture/hardware video codec wrappers. The legacy
`VideoCaptureFactory` returns null on Apple, as in upstream; use an application
video source or the upstream SDK capture layer for camera frames.

`peerconnection_smoke` exercises factory/data-channel startup and teardown
using a dummy audio device. `apple_link_smoke` force-links every production
object, exposing missing implementations that archive creation alone would
miss. On iOS it is a **link check**, not a device execution test. Building these
artifacts does not validate microphone permissions, audio routing/interruption,
background operation, or a real media call. Those require application/device
acceptance with the relevant usage descriptions and provisioning.

Compile database auditing is available without running any target device:

```sh
python3 scripts/check-apple-build.py out/ios-arm64 --sdk iphoneos --arch arm64
```

It checks unique compilation ownership, SDK/CPU flags, native audio source
inclusion, Objective-C ARC, and accidental Linux/x86 options on Apple ARM64.

## Verification recorded on 2026-10-26

Toolchain: Apple Clang 16.0.0, CMake 4.3.1, macOS SDK 15.0 and iOS SDK 18.0.
The iOS checks used Debug with `-O0 -g0` for C/C++/Objective-C/Objective-C++;
normal release builds continue to use the presets' Release defaults.

| Target | Verification |
| --- | --- |
| macOS x86_64, Release | Aggregate + 20 module archives; all-object link; 3/3 CTest tests passed |
| iOS arm64, Debug | Aggregate + 20 module archives; all-object executable cross-link passed; no device execution |
| iOS simulator x86_64, Debug | Aggregate + 20 module archives; all-object executable cross-link passed; no simulator execution |
| macOS arm64 | Syntax-only cross-check of 8 Apple platform translation units; full build/link not verified |
| iOS simulator arm64 | Syntax-only cross-check of 17 Apple platform translation units; full build/link not verified |

Compile databases were audited for architecture/platform flags and duplicate
compilation. Module archive members were compared against each aggregate
archive. These are automated build checks, not physical-device acceptance.
