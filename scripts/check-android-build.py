#!/usr/bin/env python3
"""Audit Android compile commands for ABI/API, SIMD and host contamination."""
import argparse
from collections import Counter
import json
from pathlib import Path
import shlex


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('build_dir', type=Path)
    parser.add_argument('--abi', choices=['arm64-v8a', 'x86_64'], required=True)
    parser.add_argument('--api', type=int, default=24)
    args = parser.parse_args()
    cpu = 'aarch64' if args.abi == 'arm64-v8a' else 'x86_64'
    triple = f'{cpu}-none-linux-android{args.api}'
    entries = json.loads((args.build_dir / 'compile_commands.json').read_text())
    own = []
    errors = []
    for entry in entries:
        words = entry.get('arguments') or shlex.split(entry['command'])
        file = entry['file']
        # The NDK CMake toolchain supplies explicit triples and sysroots to all
        # C/C++ compilations, including the vendored third-party libraries.
        if Path(file).suffix not in ('.c', '.cc', '.cpp', '.cxx'):
            continue
        if f'--target={triple}' not in words:
            errors.append(f'ABI/API target mismatch: {file}')
        if not any(w.startswith('--sysroot=') and '/toolchains/llvm/' in w for w in words):
            errors.append(f'NDK sysroot missing: {file}')
        if any('/opt/homebrew/' in w or '/usr/local/include' in w or
               '/Applications/Xcode' in w or '/apple-deps/' in w for w in words):
            errors.append(f'Host dependency/SDK contamination: {file}')
        if '-DWEBRTC_LIBRARY_IMPL' not in words:
            if '/third_party/' in file and '-DWEBRTC_ANDROID' in words:
                errors.append(f'WebRTC definitions leaked into dependency: {file}')
            continue
        own.append(file)
        if not all(w in words for w in ['-DWEBRTC_ANDROID', '-DWEBRTC_LINUX', '-DWEBRTC_POSIX']):
            errors.append(f'Android definitions missing: {file}')
        if any(w in words for w in ['-DWEBRTC_MAC', '-DWEBRTC_IOS', '-DWEBRTC_WIN',
                                     '-DWEBRTC_DUMMY_FILE_DEVICES', '-mfpu=neon']):
            errors.append(f'Foreign platform or implicit dummy audio: {file}')
        if any(p in file for p in ['/linux/', '/windows/', '/sdk/objc/']):
            errors.append(f'Foreign platform source: {file}')
        if args.abi == 'arm64-v8a':
            if any(w.startswith(('-msse', '-mavx', '-mfma')) for w in words):
                errors.append(f'x86 SIMD flags on ARM64: {file}')
            if file.endswith(('_sse.cc', '_sse2.cc', '_avx2.cc')):
                errors.append(f'x86 SIMD source on ARM64: {file}')
            if '-DWEBRTC_HAS_NEON' not in words:
                errors.append(f'NEON dispatch missing: {file}')
        elif '-DWEBRTC_HAS_NEON' in words or file.endswith(('_neon.cc', '_neon.c')):
            errors.append(f'ARM SIMD on x86_64: {file}')
    if not own:
        errors.append('No WebRTC translation units found')
    for file, count in Counter(own).items():
        if count != 1:
            errors.append(f'{file} compiled {count} times')
    required = ['rtc_base/ifaddrs_android.cc', 'modules/audio_device/audio_device_impl.cc']
    if args.abi == 'arm64-v8a':
        required += ['common_audio/fir_filter_neon.cc',
                     'common_audio/resampler/sinc_resampler_neon.cc']
    for suffix in required:
        if not any(f.endswith(suffix) for f in own):
            errors.append(f'Missing implementation: {suffix}')
    if errors:
        raise SystemExit('\n'.join(errors[:30]) + f'\n{len(errors)} error(s)')
    print(f'PASS: {len(own)} unique WebRTC translation units, Android {args.abi}/API {args.api}')


if __name__ == '__main__':
    main()
