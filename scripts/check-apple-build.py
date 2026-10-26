#!/usr/bin/env python3
"""Audit an Apple CMake compile database for platform/architecture contamination."""
import argparse
from collections import Counter
import json
from pathlib import Path
import shlex


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('build_dir', type=Path)
    parser.add_argument('--sdk', choices=['macosx', 'iphoneos', 'iphonesimulator'], required=True)
    parser.add_argument('--arch', choices=['x86_64', 'arm64'], required=True)
    args = parser.parse_args()
    entries = json.loads((args.build_dir / 'compile_commands.json').read_text())
    own = []
    errors = []
    for entry in entries:
        words = entry.get('arguments') or shlex.split(entry['command'])
        if '-DWEBRTC_LIBRARY_IMPL' not in words:
            # WebRTC-only definitions must not contaminate vendored libraries.
            if '/third_party/' in entry['file'] and any(
                    x in words for x in ['-DWEBRTC_LINUX', '-DWEBRTC_MAC', '-DWEBRTC_IOS']):
                errors.append(f'WebRTC platform definitions leaked into {entry["file"]}')
            continue
        own.append(entry)
        file = entry['file']
        if not all(x in words for x in ['-DWEBRTC_MAC', '-DWEBRTC_POSIX']):
            errors.append(f'Apple definitions missing: {file}')
        if ('-DWEBRTC_IOS' in words) != (args.sdk != 'macosx'):
            errors.append(f'iOS definition mismatch: {file}')
        if any(x in words for x in ['-DWEBRTC_LINUX', '-DWEBRTC_WIN', '-mfpu=neon']):
            errors.append(f'Foreign platform/ARM32 options: {file}')
        if '/linux/' in file or '/windows/' in file or file.endswith('cpu_features_linux.cc'):
            errors.append(f'Foreign implementation: {file}')
        if '-arch' not in words or words[words.index('-arch') + 1] != args.arch:
            errors.append(f'Architecture mismatch: {file}')
        if args.arch == 'arm64':
            if any(x.startswith(('-msse', '-mavx', '-mfma')) for x in words):
                errors.append(f'x86 instruction flags on ARM64: {file}')
            if file.endswith(('_avx2.cc', '_sse.cc', '_sse2.cc')):
                errors.append(f'x86 implementation on ARM64: {file}')
            if '-DWEBRTC_HAS_NEON' not in words:
                errors.append(f'NEON dispatch disabled on ARM64: {file}')
        if Path(file).suffix in ('.m', '.mm') and '-fobjc-arc' not in words:
            errors.append(f'ARC missing: {file}')
        if '-isysroot' not in words:
            if args.sdk != 'macosx':
                errors.append(f'Explicit cross SDK missing: {file}')
        else:
            sdk = words[words.index('-isysroot') + 1].lower()
            if args.sdk not in sdk:
                errors.append(f'SDK mismatch: {file}: {sdk}')
    if not own:
        errors.append('No WebRTC module translation units found')
    for file, count in Counter(e['file'] for e in own).items():
        if count != 1:
            errors.append(f'{file} compiled {count} times instead of once')
    files = [e['file'] for e in own]
    required = ['rtc_base/mac_ifaddrs_converter.cc', 'modules/audio_device/audio_engine_device.mm']
    required += (['sdk/objc/native/src/audio/audio_device_ios.mm',
                  'sdk/objc/components/audio/RTCAudioSession.mm'] if args.sdk != 'macosx'
                 else ['modules/audio_device/mac/audio_device_mac.cc'])
    for suffix in required:
        if not any(f.endswith(suffix) for f in files):
            errors.append(f'Missing native implementation: {suffix}')
    if errors:
        raise SystemExit('\n'.join(errors[:30]) + f'\n{len(errors)} error(s)')
    print(f'PASS: {len(own)} unique WebRTC translation units, {args.sdk}/{args.arch}')


if __name__ == '__main__':
    main()
