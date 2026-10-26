#!/usr/bin/env python3
"""Build an isolated static dependency prefix for one Apple SDK/CPU slice.

Uses the vendored libvpx/dav1d revisions and a caller-supplied OpenSSL source
checkout. Requires Xcode, make, Perl, Meson and Ninja on PATH. No global install.
"""
import argparse
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def run(args, cwd, env=None):
    print('+', shlex.join(map(str, args)), flush=True)
    subprocess.run(list(map(str, args)), cwd=cwd, env=env, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sdk', choices=['macosx', 'iphoneos', 'iphonesimulator'], required=True)
    parser.add_argument('--arch', choices=['arm64', 'x86_64'], required=True)
    parser.add_argument('--openssl-source', type=Path, required=True)
    parser.add_argument('--deployment-target')
    parser.add_argument('--jobs', type=int, default=4)
    parser.add_argument('--output', type=Path, default=ROOT / 'out/apple-deps')
    args = parser.parse_args()
    if args.sdk == 'iphoneos' and args.arch != 'arm64':
        parser.error('iphoneos requires arm64')
    openssl = args.openssl_source.resolve()
    if not (openssl / 'Configure').is_file():
        parser.error('--openssl-source must contain OpenSSL Configure')
    sdk = subprocess.check_output(['xcrun', '--sdk', args.sdk, '--show-sdk-path'], text=True).strip()
    minimum = args.deployment_target or ('12.0' if args.sdk == 'macosx' else '13.0')
    platform = 'macos' if args.sdk == 'macosx' else 'ios'
    triple = f'{args.arch}-apple-{platform}{minimum}'
    if args.sdk == 'iphonesimulator':
        triple += '-simulator'
    flags = ['-target', triple, '-isysroot', sdk, '-fPIC']
    work = args.output.resolve() / f'{args.sdk}-{args.arch}'
    prefix = work / 'install'
    work.mkdir(parents=True, exist_ok=True)
    # Reusing a build with different SDK/version/source must not silently reuse objects.
    identity = {'sdk': sdk, 'arch': args.arch, 'minimum': minimum, 'openssl': str(openssl)}
    stamp = work / 'build-settings.json'
    if stamp.exists() and json.loads(stamp.read_text()) != identity:
        parser.error(f'{work} has different settings; select a new --output directory')
    stamp.write_text(json.dumps(identity, indent=2) + '\n')
    cc = subprocess.check_output(['xcrun', '--sdk', args.sdk, '-f', 'clang'], text=True).strip()
    cxx = subprocess.check_output(['xcrun', '--sdk', args.sdk, '-f', 'clang++'], text=True).strip()
    env = dict(os.environ, CC=cc, CXX=cxx, CFLAGS=shlex.join(flags),
               CXXFLAGS=shlex.join(flags), LDFLAGS=shlex.join(flags), SDKROOT=sdk)
    for key in ('CPPFLAGS', 'CPATH', 'C_INCLUDE_PATH', 'CPLUS_INCLUDE_PATH',
                'OBJC_INCLUDE_PATH', 'LIBRARY_PATH', 'PKG_CONFIG_PATH'):
        env.pop(key, None)
    build = work / 'openssl'
    build.mkdir(exist_ok=True)
    target = (f'darwin64-{args.arch}-cc' if args.sdk == 'macosx' else
              'ios64-xcrun' if args.sdk == 'iphoneos' else f'iossimulator-{args.arch}-xcrun')
    if not (build / 'Makefile').exists():
        run(['perl', openssl / 'Configure', target, 'no-shared', 'no-tests',
             '--prefix=' + str(prefix), '--libdir=lib'], build, env)
    run(['make', f'-j{args.jobs}', 'build_libs'], build, env)
    run(['make', 'install_dev'], build, env)

    # This fork stores vendored helper scripts without executable mode bits.
    # Stage a private copy so fixing modes never dirties the source checkout.
    vpx_source = work / 'vpx-source'
    shutil.copytree(ROOT / 'third_party/libvpx/source/libvpx', vpx_source,
                    dirs_exist_ok=True)
    for helper in vpx_source.rglob('*'):
        if helper.is_file() and (helper.suffix in ('.sh', '.pl', '.py') or helper.name == 'configure'):
            helper.chmod(helper.stat().st_mode | 0o100)
    build = work / 'vpx'
    build.mkdir(exist_ok=True)
    # Failed generator commands can leave empty headers that make considers current.
    for header in build.glob('*rtcd.h'):
        if header.stat().st_size == 0:
            header.unlink()
    # Portable C avoids libvpx's legacy Darwin presets overriding the requested
    # SDK/minimum version (especially arm64 simulator). WebRTC keeps its SIMD.
    vpxenv = dict(env, LD=cc, AR='ar', AS=cc)
    run(['bash', vpx_source / 'configure', '--target=generic-gnu',
         '--prefix=' + str(prefix), '--disable-examples', '--disable-tools',
         '--disable-unit-tests', '--disable-docs', '--disable-shared',
         '--enable-static', '--enable-pic'], build, vpxenv)
    run(['make', f'-j{args.jobs}'], build, vpxenv)
    run(['make', 'install'], build, vpxenv)

    cross = work / 'dav1d-cross.ini'
    cpu = 'aarch64' if args.arch == 'arm64' else 'x86_64'
    cross.write_text(f'''[binaries]
c = {cc!r}
ar = 'ar'
strip = 'strip'
[host_machine]
system = 'darwin'
cpu_family = {cpu!r}
cpu = {cpu!r}
endian = 'little'
[properties]
needs_exe_wrapper = true
[built-in options]
c_args = {flags!r}
c_link_args = {flags!r}
''')
    build = work / 'dav1d'
    setup = ['meson', 'setup', str(build), str(ROOT / 'third_party/dav1d/libdav1d'),
             '--cross-file', str(cross), '--prefix', str(prefix), '--libdir', 'lib',
             '--default-library=static', '--buildtype=release', '-Denable_tools=false',
             '-Denable_tests=false', '-Denable_asm=false']
    if (build / 'meson-private/coredata.dat').exists():
        setup.append('--reconfigure')
    run(setup, work)
    run(['meson', 'compile', '-C', build, '-j', str(args.jobs)], work)
    run(['meson', 'install', '-C', build], work)
    print(f'Apple dependency prefix: {prefix}')


if __name__ == '__main__':
    main()
