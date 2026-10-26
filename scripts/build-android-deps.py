#!/usr/bin/env python3
"""Build static Android OpenSSL/libvpx/dav1d in an isolated NDK/ABI/API prefix.

Requires a verified, unpacked OpenSSL source, Perl, make, Meson and Ninja.
Uses this checkout's vendored libvpx and dav1d; does not install globally.
"""
import argparse
import json
import os
from pathlib import Path
import platform
import shlex
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def run(args, cwd, env):
    print('+', shlex.join(map(str, args)), flush=True)
    subprocess.run(list(map(str, args)), cwd=cwd, env=env, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ndk', type=Path, default=os.environ.get('ANDROID_NDK_HOME'))
    parser.add_argument('--abi', choices=['arm64-v8a', 'x86_64'], required=True)
    parser.add_argument('--api', type=int, default=24)
    parser.add_argument('--openssl-source', type=Path, required=True)
    parser.add_argument('--jobs', type=int, default=4)
    parser.add_argument('--output', type=Path, default=ROOT / 'out/android-deps')
    args = parser.parse_args()
    if args.ndk is None:
        parser.error('set ANDROID_NDK_HOME or pass --ndk')
    if args.api < 24 or args.jobs < 1:
        parser.error('--api must be >= 24 and --jobs must be positive')
    host = {'Darwin': 'darwin-x86_64', 'Linux': 'linux-x86_64'}.get(platform.system())
    if host is None:
        parser.error('dependency helper supports macOS and Linux hosts')
    ndk = args.ndk.resolve()
    bin_dir = ndk / 'toolchains/llvm/prebuilt' / host / 'bin'
    cpu = 'aarch64' if args.abi == 'arm64-v8a' else 'x86_64'
    triple = f'{cpu}-linux-android'
    cc = bin_dir / f'{triple}{args.api}-clang'
    cxx = bin_dir / f'{triple}{args.api}-clang++'
    openssl = args.openssl_source.resolve()
    if not cc.is_file() or not (ndk / 'source.properties').is_file():
        parser.error('NDK does not contain the requested host compiler')
    if not (openssl / 'Configure').is_file():
        parser.error('--openssl-source must contain OpenSSL Configure')
    work = args.output.resolve() / args.abi / f'api-{args.api}'
    prefix = work / 'install'
    work.mkdir(parents=True, exist_ok=True)
    identity = {'ndk': str(ndk), 'revision': (ndk / 'source.properties').read_text(),
                'abi': args.abi, 'api': args.api, 'openssl': str(openssl)}
    stamp = work / 'build-settings.json'
    if stamp.exists() and json.loads(stamp.read_text()) != identity:
        parser.error(f'{work} has different settings; use a new --output')
    stamp.write_text(json.dumps(identity, indent=2) + '\n')
    env = dict(os.environ, ANDROID_NDK_ROOT=str(ndk),
               PATH=str(bin_dir) + os.pathsep + os.environ['PATH'],
               CC=str(cc), CXX=str(cxx), AR=str(bin_dir / 'llvm-ar'),
               RANLIB=str(bin_dir / 'llvm-ranlib'), STRIP=str(bin_dir / 'llvm-strip'),
               CFLAGS='-fPIC', CXXFLAGS='-fPIC', LDFLAGS='')
    for key in ('CPPFLAGS', 'CPATH', 'C_INCLUDE_PATH', 'CPLUS_INCLUDE_PATH',
                'LIBRARY_PATH', 'PKG_CONFIG_PATH', 'SDKROOT',
                'MACOSX_DEPLOYMENT_TARGET', 'IPHONEOS_DEPLOYMENT_TARGET'):
        env.pop(key, None)
    build = work / 'openssl'
    build.mkdir(exist_ok=True)
    if not (build / 'Makefile').exists():
        target = 'android-arm64' if args.abi == 'arm64-v8a' else 'android-x86_64'
        run(['perl', openssl / 'Configure', target, f'-D__ANDROID_API__={args.api}',
             'no-shared', 'no-tests', '--prefix=' + str(prefix), '--libdir=lib'], build, env)
    run(['make', f'-j{args.jobs}', 'build_libs'], build, env)
    run(['make', 'install_dev'], build, env)

    # Private staging also restores executable modes missing in this fork.
    source = work / 'vpx-source'
    shutil.copytree(ROOT / 'third_party/libvpx/source/libvpx', source, dirs_exist_ok=True)
    for helper in source.rglob('*'):
        if helper.is_file() and (helper.suffix in ('.sh', '.pl', '.py') or helper.name == 'configure'):
            helper.chmod(helper.stat().st_mode | 0o100)
    build = work / 'vpx'
    build.mkdir(exist_ok=True)
    for header in build.glob('*rtcd.h'):
        if header.stat().st_size == 0:
            header.unlink()
    # Portable C baseline. Do not let legacy libvpx Android presets select GCC.
    run(['bash', source / 'configure', '--target=generic-gnu',
         '--prefix=' + str(prefix), '--disable-examples', '--disable-tools',
         '--disable-unit-tests', '--disable-docs', '--disable-shared',
         '--enable-static', '--enable-pic'], build, dict(env, LD=str(cc), AS=str(cc)))
    run(['make', f'-j{args.jobs}'], build, env)
    run(['make', 'install'], build, env)

    cross = work / 'dav1d-cross.ini'
    cross.write_text(f'''[binaries]
c = {str(cc)!r}
ar = {str(bin_dir / 'llvm-ar')!r}
strip = {str(bin_dir / 'llvm-strip')!r}
[host_machine]
system = 'android'
cpu_family = {cpu!r}
cpu = {cpu!r}
endian = 'little'
[properties]
needs_exe_wrapper = true
[built-in options]
c_args = ['-fPIC']
''')
    build = work / 'dav1d'
    setup = ['meson', 'setup', build, ROOT / 'third_party/dav1d/libdav1d',
             '--cross-file', cross, '--prefix', prefix, '--libdir', 'lib',
             '--default-library=static', '--buildtype=release', '-Denable_tools=false',
             '-Denable_tests=false', '-Denable_asm=false']
    if (build / 'meson-private/coredata.dat').exists():
        setup.append('--reconfigure')
    run(setup, work, env)
    run(['meson', 'compile', '-C', build, '-j', args.jobs], work, env)
    run(['meson', 'install', '-C', build], work, env)
    print(f'Android dependency prefix: {prefix}')


if __name__ == '__main__':
    main()
