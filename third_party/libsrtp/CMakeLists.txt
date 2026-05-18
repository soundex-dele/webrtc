cmake_minimum_required(VERSION 3.10)
project(libsrtp C)

# ============================================================================
# Build Configuration
# ============================================================================

# Package identity
set(PACKAGE_STRING "860492290f7d1f25e2bd45da6471bfd4cd4d7add")
set(PACKAGE_VERSION "860492290f7d1f25e2bd45da6471bfd4cd4d7add")

# ============================================================================
# Compile Definitions
# ============================================================================
add_compile_definitions(
    PACKAGE_STRING="${PACKAGE_STRING}"
    PACKAGE_VERSION="${PACKAGE_VERSION}"
    HAVE_CONFIG_H
    OPENSSL
    GCM

    # Basic types
    HAVE_STDLIB_H
    HAVE_STRING_H
    HAVE_STDINT_H
    HAVE_INTTYPES_H
    HAVE_INT16_T
    HAVE_INT32_T
    HAVE_INT8_T
    HAVE_UINT16_T
    HAVE_UINT32_T
    HAVE_UINT64_T
    HAVE_UINT8_T
)

# Platform-specific definitions
if(UNIX AND NOT APPLE)
    add_compile_definitions(
        HAVE_ARPA_INET_H
        HAVE_NETINET_IN_H
        HAVE_SYS_TYPES_H
        HAVE_UNISTD_H
    )
elseif(APPLE)
    add_compile_definitions(
        HAVE_ARPA_INET_H
        HAVE_NETINET_IN_H
        HAVE_SYS_TYPES_H
        HAVE_UNISTD_H
    )
elseif(WIN32)
    add_compile_definitions(HAVE_WINSOCK2_H)
endif()

# ============================================================================
# Include Directories
# ============================================================================
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/config
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/crypto/include
)

# Find OpenSSL (use parent project's OpenSSL if available)
if(NOT TARGET OpenSSL::Crypto)
    find_package(OpenSSL REQUIRED)
endif()

# ============================================================================
# Source Files
# ============================================================================

# Common headers
set(LIBSRTP_HEADERS
    # Public headers
    include/srtp.h

    # Crypto headers
    crypto/cipher/cipher_test_cases.h
    crypto/hash/auth_test_cases.h
    crypto/include/aes.h
    crypto/include/aes_gcm.h
    crypto/include/aes_icm.h
    crypto/include/aes_icm_ext.h
    crypto/include/alloc.h
    crypto/include/auth.h
    crypto/include/cipher.h
    crypto/include/cipher_priv.h
    crypto/include/cipher_types.h
    crypto/include/crypto_kernel.h
    crypto/include/crypto_types.h
    crypto/include/datatypes.h
    crypto/include/err.h
    crypto/include/integers.h
    crypto/include/key.h
    crypto/include/null_auth.h
    crypto/include/null_cipher.h
    crypto/include/rdb.h
    crypto/include/rdbx.h
    include/srtp_priv.h
)

# Source files
set(LIBSRTP_SOURCES
    srtp/srtp.c

    # Math
    crypto/math/datatypes.c

    # Kernel
    crypto/kernel/alloc.c
    crypto/kernel/crypto_kernel.c
    crypto/kernel/err.c
    crypto/kernel/key.c

    # Replay
    crypto/replay/rdb.c
    crypto/replay/rdbx.c

    # Hash
    crypto/hash/auth.c
    crypto/hash/null_auth.c
    crypto/hash/hmac_ossl.c

    # Cipher
    crypto/cipher/cipher.c
    crypto/cipher/null_cipher.c
    crypto/cipher/aes_icm_ossl.c
    crypto/cipher/aes_gcm_ossl.c
    crypto/cipher/cipher_test_cases.c
    crypto/hash/auth_test_cases.c
)

# ============================================================================
# Build Static Library
# ============================================================================
add_library(srtp STATIC ${LIBSRTP_SOURCES} ${LIBSRTP_HEADERS})

# Link OpenSSL
if(TARGET OpenSSL::Crypto AND TARGET OpenSSL::SSL)
    target_link_libraries(srtp PUBLIC OpenSSL::Crypto OpenSSL::SSL)
else()
    target_link_libraries(srtp PUBLIC ${OPENSSL_LIBRARIES})
endif()

# ============================================================================
# Compiler Flags
# ============================================================================
if(WIN32)
    target_compile_options(srtp PRIVATE /wd4018)  # Signed/unsigned mismatch
else()
    target_compile_options(srtp PRIVATE -Wall -Wextra)
endif()

# ============================================================================
# Optional Tests
# ============================================================================
option(BUILD_LIBSRTP_TESTS "Build libsrtp tests" OFF)

if(BUILD_LIBSRTP_TESTS)
    # Test utility files
    set(TEST_UTIL_SOURCES
        test/getopt_s.c
        test/getopt_s.h
        test/ut_sim.c
        test/ut_sim.h
        test/util.c
        test/util.h
    )

    # Test applications
    add_executable(rdbx_driver test/rdbx_driver.c ${TEST_UTIL_SOURCES})
    target_link_libraries(rdbx_driver srtp)

    add_executable(replay_driver test/replay_driver.c ${TEST_UTIL_SOURCES})
    target_link_libraries(replay_driver srtp)

    add_executable(roc_driver test/roc_driver.c ${TEST_UTIL_SOURCES})
    target_link_libraries(roc_driver srtp)

    add_executable(srtp_driver test/srtp_driver.c ${TEST_UTIL_SOURCES})
    target_link_libraries(srtp_driver srtp)

    add_executable(test_srtp test/test_srtp.c test/cutest.h ${TEST_UTIL_SOURCES})
    target_link_libraries(test_srtp srtp)

    add_executable(cipher_driver crypto/test/cipher_driver.c ${TEST_UTIL_SOURCES})
    target_link_libraries(cipher_driver srtp)

    add_executable(datatypes_driver crypto/test/datatypes_driver.c ${TEST_UTIL_SOURCES})
    target_link_libraries(datatypes_driver srtp)

    add_executable(kernel_driver crypto/test/kernel_driver.c ${TEST_UTIL_SOURCES})
    target_link_libraries(kernel_driver srtp)

    # RTP word test
    add_executable(rtpw
        test/rtpw.c
        test/rtp.c
        test/rtp.h
        test/getopt_s.c
        test/util.c
        test/util.h
        crypto/math/datatypes.c
    )
    target_link_libraries(rtpw srtp)
    if(UNIX)
        target_compile_definitions(rtpw PRIVATE HAVE_SYS_SOCKET_H)
    endif()
endif()

# ============================================================================
# Install
# ============================================================================
install(TARGETS srtp
    ARCHIVE DESTINATION lib
    LIBRARY DESTINATION lib
)

install(FILES
    include/srtp.h
    include/srtp_priv.h
    crypto/include/crypto_types.h
    DESTINATION include/srtp
)
