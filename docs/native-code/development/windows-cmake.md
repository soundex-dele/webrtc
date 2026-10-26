# Windows CMake build (m137_dev)

This branch builds WebRTC and `peerconnection_demo` directly with CMake. It does
not require GN, Ninja, depot_tools, or a Chromium dependency checkout.

## Requirements

- Windows x64, Visual Studio 2022 with **Desktop development with C++**, MSVC v143,
  and a Windows 10/11 SDK.
- CMake 3.21 or newer for the supplied presets.
- [vcpkg](https://github.com/microsoft/vcpkg) for OpenSSL, libvpx and dav1d.
  Their first build also downloads the tools needed by those libraries.
- [NASM](https://www.nasm.us/) on `PATH`, for the bundled libaom assembly.
  Alternatively pass `-DCMAKE_ASM_NASM_COMPILER=C:/path/to/nasm.exe`.
- Perl on `PATH` for libaom's generated headers (for example Strawberry Perl,
  or pass `-DPERL_EXECUTABLE=C:/path/to/perl.exe`).

The CMake source manifests support x64 Windows/Linux and macOS/iOS Apple
slices. See [Apple builds and module targets](apple-cmake.md) for the platform
matrix and independent module archive commands. Unsupported architectures are
rejected at configure time.

## Build from PowerShell

Run these commands in the repository root. Adjust the vcpkg path to your machine:

```powershell
$env:VCPKG_ROOT = 'D:\vcpkg'
& "$env:VCPKG_ROOT\vcpkg.exe" install openssl:x64-windows-static libvpx:x64-windows-static dav1d:x64-windows-static
cmake --preset windows-x64
cmake --build --preset windows-release
ctest --preset windows-release
```

Outputs:

- `out/windows-x64/Release/webrtc.lib`
- `out/windows-x64/Release/peerconnection_demo.exe`
- `out/windows-x64/webrtc_peerconnection_demo.sln` for Visual Studio.

Debug uses the same generated solution:

```powershell
cmake --build --preset windows-debug
ctest --preset windows-debug
```

The presets use the static MSVC runtime (`/MT`, `/MTd`) to match
`x64-windows-static`. Do not mix these libraries with `/MD` dependencies. For a
DLL runtime build, use a separate build directory and a matching vcpkg triplet
and `CMAKE_MSVC_RUNTIME_LIBRARY` setting.

The smoke test creates and closes a PeerConnection and a data channel, and checks startup/teardown
with the built-in media factories and a dummy audio device, without a remote
signaling or STUN server. It does not establish a media call.
Winsock and SSL are initialized before creating WebRTC threads. A second test
compares the AVX2 matched filter against the scalar implementation (skipped on
CPUs without AVX2/FMA).

## Dependencies and features

The repository builds its bundled Abseil, Opus, libyuv, libsrtp, JsonCpp, CRC32C,
PFFFT, RNNoise and libaom (AV1 encoding) sources. Video codecs link to the
external libvpx (VP8/VP9) and dav1d (AV1 decoding) libraries and use their matching
headers. Windows uses WASAPI audio and DirectShow video capture source files.
The existing OpenSSL build still excludes the BoringSSL-specific frame cryptor;
this change does not enable H.264 encoding/decoding.

Applications in the same CMake build should link `WebRTC::webrtc` so that required
third-party libraries, Windows system libraries and public compile settings are
propagated. `webrtc.lib` alone is not a merged SDK containing every dependency.
Use `-DWEBRTC_BUILD_DEMO=OFF` if only the library target is needed.

For dependencies outside vcpkg, configure without the preset and supply
`CMAKE_PREFIX_PATH` and/or `OPENSSL_ROOT_DIR`. libvpx must provide the
`unofficial-libvpx` CMake package, and dav1d must have installed headers and libraries. OpenSSL paths are never
overwritten by the project.
