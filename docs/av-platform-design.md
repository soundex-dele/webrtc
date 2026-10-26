# WebRTC 在 AV Platform 中的集成设计

版本：v0.1；日期：2026-10-26；本地读取版本：`40200b3d88`。这是本项目对 WebRTC fork 的使用、构建和升级设计，原生模块完整设计仍以上游文档和源码为准。

平台职责见 [总体设计](../../docs/architecture/platform-design.md)。原生补丁说明记录的 M137 基线为 `aad183504be13d5a9c529581a27c53767570b5d6`；它与当前派生仓库 HEAD 是不同层次的版本标识，发布时应同时记录。

## 1. 职责与使用方

WebRTC 为 SDK 和媒体服务提供 PeerConnection、ICE/DTLS/SRTP、媒体编解码、RTP/RTCP、反馈与重传、拥塞控制、pacing、音频处理和平台设备基础。

| 使用方 | 使用方式 | 边界 |
| --- | --- | --- |
| `livekit-sdk-cpp` | 原生客户端 PeerConnection、输入/输出和统计 | 公开 SDK 不泄露原生类型 |
| `livekit-cpp` | 原生传输、收包/组帧/重打包、发送控制 | 依赖部分内部接口，升级需强回归 |
| `livekit-app` | 通过 SDK 间接使用 | 不直接链接原生内部类 |
| `livekit-server` | 通过媒体管理 API 协作 | 业务进程不引入原生媒体库 |

用户、项目、计费、会议业务状态和图调度不进入 WebRTC fork。对原生改动尽量限制为构建适配、已定位缺陷修复或明确的后端适配点。

## 2. 源码模块与依赖边界

| 目录 | 在本项目中的定位 |
| --- | --- |
| `api/` | PeerConnection、帧、编解码工厂、统计等 API |
| `pc/`、`p2p/` | 协商、连接、ICE 与传输 |
| `media/`、`call/`、`audio/`、`video/` | 媒体引擎、会话和音视频管线 |
| `modules/rtp_rtcp/`、`modules/pacing/` | RTP/RTCP、重传和发送排队 |
| `modules/congestion_controller/` | 原生拥塞控制实现 |
| `modules/audio_processing/` | AEC 等音频处理 |
| `rtc_base/`、`system_wrappers/` | 线程、任务、安全与时钟基础 |
| `cmake/`、`CMakeLists.txt`、`CMakePresets.json` | 当前 fork 的本地构建适配 |
| `third_party/` | 编解码、SRTP 与基础依赖，各自保留许可证 |

媒体服务内部适配器不得通过复制原生实现形成另一个长期维护的 RTP/拥塞控制栈。必要的映射与路由放在 `livekit-cpp`，通用原生 bug 修复保留最小补丁和可复现测试。

## 3. 构建与二进制契约

本地 CMake 工程支持 Windows/Linux x64、macOS x86_64/arm64、iOS arm64 与模拟器 x86_64/arm64，以及 Android API 24+ 的 arm64-v8a/x86_64。Apple 每个构建目录只选择一个 SDK/架构切片，Android 每个目录只选择一个 ABI/API 组合。Android 当前提供原生 C++ 核心，设备音频由应用注入 ADM，不包含 Java/JNI、AAR 或设备采集封装。源码按职责拆成 20 个模块，每个模块独立生成静态库，聚合库复用同一批对象。

Windows 以 VS 2022、MSVC v143、CMake 与静态 CRT `/MT` 为基线，Debug 为 `/MTd`；外部 OpenSSL/libvpx/dav1d 依赖须使用一致架构、配置与 CRT。Linux 服务端已使用 Clang 15 + libc++ 的适配路径，不能直接混用不同 C++ 标准库产物。

对下游暴露 `WebRTC::webrtc`，携带系统库和第三方链接设置；`webrtc.lib` 不是包含全部依赖的合并 SDK。SDK 和媒体服务在同一产品发布中固定同一源码/补丁基线，但不同构建选项仍可能产生不同产物，必须分别记录哈希。

依赖源码不由构建过程静默修改。每组工具链与构建配置使用独立输出目录；预编译包清单记录源码提交、补丁哈希、编译器、架构、CRT/标准库、编译选项、外部依赖版本、库哈希和许可证。

构建入口与依赖详情见 [Windows CMake 说明](native-code/development/windows-cmake.md)、[Apple 与模块构建说明](native-code/development/apple-cmake.md)、[Android CMake 说明](native-code/development/android-cmake.md)，Linux 消费端适配见 [媒体服务 README](../../livekit-cpp/README.md)。

## 4. 线程、时钟与资源

原生 network/worker/signaling 线程及 TaskQueue 保留各自归属。上层通过任务投递桥接控制循环，禁止从 UI/HTTP 线程直接操作要求指定线程的原生状态。关闭按反向依赖顺序撤销任务、停止来源、释放会话与工厂，再结束线程。

回调捕获使用安全标记或弱引用，确保任务执行时对象仍有效；不能只用“对象即将析构”标志代替任务取消和排空。音频设备回调保持非阻塞，磁盘和 UI 操作转交上层有界队列。

拥塞控制、排队、TTL 使用单调时钟语义；业务 Token 使用 UTC 墙钟。测试日志对齐需标注时钟来源，不能用墙钟变化推导媒体处理耗时。跨 Windows/WSL 计时差已是诊断线索，仍需在时钟稳定环境重测。

Windows 服务端显式集成原生 Windows 定时队列，以避免通用队列粒度影响探测簇；这属于消费端构建选择，不能假定只更新本仓库就自动改变所有下游计时行为。

## 5. 原生补丁管理

当前关键补丁为 `PrioritizedPacketQueue` 暂停后 TTL 的时钟域修复，源说明与补丁保存在 [媒体服务 patches](../../livekit-cpp/patches/README.md)。平均排队统计使用扣除暂停的时间，而 TTL/调度比较真实驻留时间，两者不能混用。

补丁恢复原始入队时间用于 TTL 和调度；不延长 TTL、不改变原生队列优先级、不替换 pacer。当前仓库已包含派生改动，应用或检查补丁前应判断是否已经合入，禁止重复应用。

媒体服务 `CheckWebRTCPatches.cmake` 校验源码，`native-send` 回归校验实际链接库；两者都需要。只复制更新后的头文件或通过源码检查不能证明旧 `.lib` 已修复。测试应覆盖空队列暂停后新包、音频优先级、真实过期、平均队列时间及多次暂停。

新增补丁记录问题、复现、上游基线、修改理由和测试证据；升级时检查是否已被上游修复，不能为通过构建简单删除 guard。

## 6. 能力声明与编解码

底层编译入 VP9/AV1、frame cryptor 或其他能力，与产品协议是否支持是两回事。当前 C++ SFU 只宣告已接入的 Opus/VP8/RTX；客户端读取 H.264 文件后转为 VP8 发布不表示 SFU 支持 H.264 转发。

现有 OpenSSL CMake 路径排除 BoringSSL 特定 frame cryptor；不能由 fork README 的上游特性推导本产物 E2EE 可用。更多编码、FEC/RED、SVC 和硬件能力分别经过工厂、协商、传输、平台与真实媒体测试后再向上层开放。

设备支持同样以实际编入模块与运行环境为准。摄像头、屏幕、系统音频和输入注入分别查询能力；媒体服务可以排除本地采集模块，SDK 则按平台需要构建。

## 7. 升级流程

1. 固定候选上游与现有基线，记录 API/ABI、协议与第三方差异。
2. 审计全部本地补丁、CMake 源清单和下游内部接口调用，确认原生队列修复仍有效。
3. 在新输出目录构建库及 smoke tests，保留工具链和产物信息。
4. 构建 SDK 与媒体服务，运行原生单测和 `native-send`；检查重复 RTCP/反馈、线程与销毁行为。
5. 执行固定官方 SDK/原生 SDK 的真实媒体、选层、静音、重订、TURN、弱网和关闭回归。
6. 记录性能与已知差异，最后更新聚合仓库依赖版本；失败时回退整套兼容产物，不能只回退一个头文件。

## 8. 验收层次

本仓库 smoke test 验证 PeerConnection/data channel 的创建与关闭，不建立真实远端通话；matched filter 测试比较 AVX2 与标量，特性不足会跳过。它们不能替代媒体集成验收。

下游 SDK 验证采集/发布/订阅/解码与回调；媒体服务验证原生发送控制、编解码零调用、真实媒体与队列；平台验证端到端时延、网络故障和资源回收。当前跨系统和文件四轨失败保留，升级验收不得降低原门槛。本文只记录设计，没有新增编译或测试结论。
