---
title: DMR 数字通信入门
description: DMR 标准、TDMA 帧结构、RadioID 注册与 BrandMeister 配置流程
published: true
date: 2026-10-22T00:00:00.000Z
tags: DMR, 数字通信, BrandMeister, RadioID
editor: markdown
dateCreated: 2025-12-20T11:20:49.608Z
---

# DMR 数字通信入门

**DMR**（Digital Mobile Radio）是由欧洲电信标准化协会（ETSI）制定的数字移动无线电标准，广泛应用于专业对讲、商业集群和业余无线电。业余爱好者最常接触的是 **Tier II** 常规中继模式，以及通过热点接入 BrandMeister 等网络的方式。

## 标准与层级

DMR 由 ETSI 在 **TS 102 361** 系列标准中定义，通常分为三个层级：

| 层级 | 模式 | 典型用途 |
|------|------|----------|
| Tier I | 直通模式，免许可 | PMR446 等消费级对讲 |
| Tier II | 常规中继/直通 | 业余无线电、商业常规通信 |
| Tier III | 集群模式 | 大型专业集群网络 |

主要设备厂商包括 Motorola、Hytera、Icom、Kenwood、Tait 等，DMR Association 负责推动标准互通与认证。

## 物理层

### 调制与速率

- 采用 **4FSK**（四电平频移键控）调制；
- 符号速率为 **4800 Bd**，每个符号携带 2 bit，总速率约 **9.6 kbit/s**；
- 信道带宽 **12.5 kHz**。

### 双时隙 TDMA

DMR 使用 [TDMA（时分多址）](/zh/ham-tech/TDMA) 把一个 12.5 kHz 信道划分为 **2 个时隙**：

- 每个时隙 **30 ms**，一帧 **60 ms**；
- 两个时隙可以同时承载两路独立语音或数据，相当于两个逻辑信道；
- 每个时隙由同步序列、嵌入信令和语音/数据载荷组成。

> 在中继模式下，两个时隙通常分别用于上行和下行；具体分配取决于中继台配置，并不是所有系统都固定“Slot 1 上行、Slot 2 下行”。

### 语音编码

DMR 使用 **AMBE+2** 声码器。语音业务中，每个时隙承载 2 帧、每帧 49 bit 的编码参数，并配合前向纠错和嵌入信令传输。数据业务则使用独立的协议数据单元（PDU），可承载短消息、GPS 位置和遥测等信息。

## 数据链路层

### CACH 与色码

**CACH**（Common Announcement Channel，公共通告信道）是 DMR 帧中的公共控制信息，主要用于：

- 指示时隙承载的是语音还是数据；
- 携带 **色码（Color Code）**；
- 标识接入类型（基站/终端）和低功率指示；
- 帮助接收机同步 TDMA 帧结构。

**色码**为 4 bit（0–15），作用类似模拟对讲机的 CTCSS 亚音，用于区分使用相同频率的不同系统。收发双方的色码必须一致，否则无法正常解码。

### 地址机制

DMR 使用 **24 位地址空间**：

- **个体 ID（Individual ID）**：标识单个用户，例如 1234567；
- **组 ID（Group ID）**：标识通话组，例如 TG 91；
- **全呼/广播 ID**：用于向所有终端发起呼叫。

在业余无线电中，DMR ID 与呼号绑定，由 **RadioID.net** 统一分配，并被 BrandMeister 等网络共用。

## 业余 DMR 网络与 BrandMeister

### 服务器节点与通话组

使用 DMR 网络前需要区分两个概念：

- **服务器节点（Master）**：运行 BrandMeister 软件、负责交换语音和数据的服务器。中国区常用节点号为 **4602**（以网络当前配置为准）。
- **通话组（TalkGroup，TG）**：逻辑上的“频道”，例如：
  - **TG 91**：全球组；
  - **TG 46001**：中国区常用组；
  - **TG 46020**：广州地区组；
  - **TG 9990**：回声测试（Parrot）。

只有当设备或热点当前订阅了某个 TG，并且该 TG 在该时隙处于激活状态时，才能听到对应的通话。

### BrandMeister 能做什么

BrandMeister 是构建全球业余数字语音网络的开源服务器软件，支持：

- 通过互联网连接各地中继台和热点；
- 自动漫游与跨区域通话；
- 私人呼叫、组呼、短信和 APRS 位置上报；
- 基于 Web 的 Dashboard 管理网关与通话组；
- 通过 API、Lua 脚本和事件通知扩展功能。

详细的中国区网络说明可参考 [BrandMeister China Wiki](https://wiki.brandmeister.network/index.php/China)。

## 开始使用 DMR

### 1. 准备资料

- 有效的**业余无线电台操作证书**；
- **电台执照**（用于 RadioID 审核）；
- 可用的 DMR 电台或 MMDVM 热点。

### 2. 注册 RadioID

1. 打开 <https://radioid.net/>，点击右上角 **Register** 注册账号。
2. 填写邮箱、呼号和个人信息，上传操作证与执照照片。
3. 等待人工审核（通常 24–48 小时），审核结果会发送到注册邮箱，也可在 Dashboard 查看。

![RadioID 注册页面](/assets/images/dmr-digi/radioid.webp)
![RadioID 资料填写页面](/assets/images/dmr-digi/radioid1.webp)
![RadioID 执照图片要求](/assets/images/dmr-digi/require.webp)
![RadioID 审核结果](/assets/images/dmr-digi/radioida.webp)

> 英文界面不熟悉时，可参考第三方教程；提交前务必确认呼号、姓名与执照信息一致。

### 3. 注册 BrandMeister

1. 打开 <https://brandmeister.network/>，点击 **Register**。
2. 完成邮箱验证与 AntiSpam 问题（UHF 频段波长约为 **70 cm**）。
3. 登录 Dashboard，在 **SelfCare** 中设置热点密码（Hotspot Security Password），该密码稍后要填入热点配置。

![BrandMeister 首页](/assets/images/dmr-digi/bm.webp)
![BrandMeister 注册页面](/assets/images/dmr-digi/brandmeister.webp)
![SelfCare 网关设置](/assets/images/dmr-digi/selfcare.webp)

### 4. 配置电台或热点

以 MMDVM 热点（Pi-Star / WPSD）为例：

1. 在配置页选择 **BrandMeister**，主服务器选择中国区节点（如 `BM_4602`）。
2. 填写 DMR ID、呼号、热点密码（即 SelfCare 中设置的密码）。
3. 设置热点频率、发射功率与色码，保存并重启服务。
4. 在 BrandMeister Dashboard 的 **Hotspots** 页面确认热点已上线。

以手持/车载台直连中继为例，需要在写频软件中配置：

- 接收/发射频率与色码；
- 时隙（TS1 / TS2）；
- 联系人（Contact）与通话组列表（TX Contact / RX Group List）；
- 你的 DMR ID 与呼号。

## 静态组与动态组

| 类型 | 行为 | 适用场景 |
|------|------|----------|
| **静态组（Static）** | 网关/热点始终订阅该 TG，收到即转发 | 常用区域组、常驻监听 |
| **动态组（Dynamic）** | 用户按下 PTT 时临时订阅，一段时间无活动后自动取消 | 临时加入其他地区组 |

在热点上通常可以把多个 TG 设为静态组，但要注意：**同一个时隙同一时间只能激活一个 TG**，配置过多静态组可能导致互相抢占或听不到预期通话。

## 常见问题

| 现象 | 排查方向 |
|------|----------|
| 发射后没有回音/无人响应 | 检查 TG 是否被订阅、时隙是否正确、对方是否在同一 TG |
| 完全听不到声音 | 色码、频率、时隙不匹配；热点未上线；DMR ID 未审核通过 |
| 热点显示未注册 | SelfCare 密码错误、主服务器地址错误、DMR ID 填写错误 |
| 能听到但对方听不到 | 发射频率/时隙/色码配置错误，或该 TG 未被网关订阅 |
| 通话断续 | 网络延迟、热点丢包、射频干扰或信号过弱 |

建议先用 **TG 9990（Parrot）** 做回声测试：按下 PTT 说几句话，松开后应能听到自己的录音。

## 合规提醒

- 仅在取得操作证和电台执照后发射；
- 使用符合型号核准要求的设备，遵守业余频段划分与功率限制；
- 热点和自制设备同样需要符合当地无线电管理规定。

## 相关页面

- [TDMA 时分多址技术](/zh/ham-tech/TDMA)
- [业余无线电知识库索引](/zh/ham-tech/index)
- [业余无线电工具与软件](/zh/ham-tools/main-pages)
