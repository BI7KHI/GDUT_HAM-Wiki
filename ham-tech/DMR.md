---
title: DMR数字通信入门
description: 
published: true
date: 2025-12-20T12:57:06.626Z
tags: 
editor: markdown
dateCreated: 2025-12-20T11:20:49.608Z
---

# 介绍——DMR数字通信
DMR（Digital Mobile Radio）数字集群通信标准是ETSI（欧洲通信标准协会）为了满足欧洲各国的中低端专业及商业用户对移动通信的需要而设计、制订的开放性标准。

DMR Association是DMR产品的主要生产厂商组成的一个联盟组织，主要设备供应商有Motorola、Hytera、Selex、Tait等。联盟的主要成员：**Aeroflex、CML、Democom、Funkwerk Koelleda、Fylde、Hytera、ICOM、KENWOOD、MOTOROLA、Radio Activity、Team Simoco、SELEX、Tait、Vertex、Professioneller Mobilfunk。**
![](https://bkimg.cdn.bcebos.com/pic/960a304e251f95ca8aa2e9bbc6177f3e67095263?x-bce-process=image/format,f_auto/watermark,image_d2F0ZXIvYmFpa2UyNzI,g_7,xp_5,yp_5,P_20/resize,m_lfit,limit_1,h_1080)
## 物理层Physical Layer
### 调制方式
1. 采用 **4FSK**（4级频移键控），符号速率9.6 kbd（千波特）
2. 每个符号携带2比特信息（00, 01, 10, 11对应4种频偏）
3. 频偏±1.8 kHz（低符号）和±5.4 kHz（高符号），抗噪声能力强
### 信道带宽与时隙
1. 12.5 kHz信道带宽
2. 通过 **[TDMA](/ham-tech/TDMA)**（时分多址） 将信道分为2个时隙（Slot）
3. Slot 1 和 Slot 2 交替传输，每个时隙30ms

物理帧总时长60ms，含发送、保护和同步序列。
## 数据链路层Data Link Layer
### 逻辑信道结构
**CACH（公共分配信道）**
位于时隙起始处，携带：
1. 时隙类型（语音/数据）
2. 目标地址（个人/组呼）
3. 信道占用标志（防止冲突）

**荷载类型**
|类型	|用途	|结构示例|
|--|--|--|
|语音突发|	AMBE+2编码语音（共72比特）|	前向纠错+语音数据|
|数据突发	|文本消息/GPS/控制信令	|头信息+用户数据+CRC校验|
```
// CACH数据结构示例
struct cach_header {
    uint8_t slot_type:2;   // 时隙类型：00=语音 01=数据
    uint8_t target_type:2; // 目标类型：00=个体 01=组呼 10=广播
    uint8_t color_code:4;  // 色码(0-15)
    uint24_t dst_id;       // 目标ID(24位)
};
```
**CACH（公共分配信道）**：时隙起始处的控制信道，承载路由关键信息
**双时隙协同**：Slot 1用于上行，Slot 2用于下行  (**中继模式**)

### 地址机制（完整描述一个DMR信道）
**DMR标识符（ID）**
* 24位地址空间（约1600万用户）
	* 个体ID：单用户（如123456）
	* 组ID：群组呼叫（如Group 91 46001）
  	* 广播ID：全呼
    
**色码（Color Code）**
* 4比特（0-15），类似模拟CTCSS（模拟对讲机中广泛使用的亚音技术标准），区分同频相邻系统。

# 概述——业余无线电数字通信网络
业余无线电数字通信中，DMR ID用于识别您的呼号，Brandmeister用于提供网络服务，中国BrandMaster Master节点服务器为4602，用于提供国内连接节点。
**China-Brandmaster Wiki：** https://wiki.brandmeister.network/index.php/China

## Brandmeister（BM）数字网络
BrandMeister是一款主服务器的操作软件，这个服务器用于构建全球业余无线电数字语音系统的基础设施网络。
### 核心功能介绍
* 带有IP功能的传统Tier-2 DMR模式的无线电交换系统
* 支持最常用的网络接入设备和终端用户设备，且易于扩展
* 在DMR堆栈的第3层（呼叫控制）进行交换
* 具有嵌入式数据堆栈（第4层）
* 嵌入了数据和语音应用程序
* 灵活的路由，基于存储在全球数据库、本地内存缓存和Lua脚本中的数据进行
* 事件通知，使用消息传递队列（呼叫，连接，警报，消息，位置和遥测）
* 允许人们基于网格技术建立自己的网络

BrandMeister允许您连接到MOTOROLA DMR-MARC和Hytera DMRplus网络，这意味着您可以同时与在这两种设施操作的其他DMR业余无线电操作员一起操作。


### Brandmeister允许无线电爱好者…

* 自动从中继台到中继台漫游
* 在任何时隙段进行私人QSO
* 用任何设备类型的业余DMR网络进行全球性的QSO
* 将我的位置发送到APRS
* 发送和接收SMS消息
* 发送和接收来自APRS的SMS消息
* 使用我的DMR电台作为遥控设备来控制某些电器

> 在这里我们需要明确两个概念，一个是**服务器节点（Master）**，一个是**通话组（TalkGroup,TG）**
> **服务器节点**是一个在网络上的服务器，同于和主BM网络通讯，连接世界各地的业余无线电爱好者
> **通话组**表示各地区的通话组，例如TG46001（全国多模式）、TG91（全球组）、TG46020（广州组）

# 开始
首先要进入DMR的世界，我们需要准备好操作证和电台执照的照片
业余无线电中的DMR ID 由 **RADIO ID.Inc**发放
首先进入Radioid网站 https://radioid.net/ 注册DMR ID
右上角**Register**注册












