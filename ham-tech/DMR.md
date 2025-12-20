---
title: DMR数字通信入门
description: 
published: true
date: 2025-12-20T11:20:49.608Z
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
2. 通过 **TDMA**（时分多址） 将信道分为2个时隙（Slot）
3. Slot 1 和 Slot 2 交替传输，每个时隙30ms

物理帧总时长60ms，含发送、保护和同步序列。
## 数据链路层Data Link Layer