---
title: Wiki 贡献指南
description: 如何通过网页或 GitHub 参与广工无线电社 Wiki 的编写、配图与维护
published: true
date: 2026-10-22T00:00:00.000Z
tags: 贡献指南, Wiki.js, GitHub
editor: markdown
dateCreated: 2025-11-11T09:27:31.780Z
---

# Wiki 贡献指南

本 Wiki 由社团成员共同维护，内容托管在 GitHub，并通过 Wiki.js 同步发布。欢迎补充技术教程、校园生活经验、项目记录和社团历史。

## 本站技术结构

| 项目 | 信息 |
|------|------|
| 站点地址 | <https://argdut.bi7khi.xyz/> |
| 源码仓库 | <https://github.com/BI7KHI/GDUT_HAM-Wiki> |
| 内容目录 | 仓库中的 `zh/` 目录 |
| 技术结构 | Wiki.js + Git 同步 |
| 贡献群 | QQ 群 **259802400** |

## 参与方式

### 方式一：网页在线编辑

适合快速修改错别字或补充一小段内容：

1. 联系管理员开通 Contributor 账号（可先在贡献群说明要编辑的页面）。
2. 登录 Wiki 站点，打开目标页面。
3. 点击页面右下角的 ✏️ **编辑**，使用 Markdown 修改内容。
4. 提交变更并填写简短的修改说明。

### 方式二：通过 GitHub 提交 PR

适合新增页面、批量整理或需要讨论的改动：

1. Fork [GDUT_HAM-Wiki](https://github.com/BI7KHI/GDUT_HAM-Wiki) 仓库。
2. 克隆到本地并新建分支：

   ```bash
   git clone https://github.com/<你的用户名>/GDUT_HAM-Wiki.git
   cd GDUT_HAM-Wiki
   git switch -c docs/update-ham-tech
   ```

3. 在 `zh/` 下修改或新增 Markdown 文件。
4. 提交并推送：

   ```bash
   git add .
   git commit -m "docs: 补充 VNA 校准说明"
   git push -u origin docs/update-ham-tech
   ```

5. 在 GitHub 上发起 Pull Request，说明改动内容和原因。

> 不熟悉 Git 的话，请先阅读 [Git 与 GitHub 操作教程](/zh/computer-indoor/Git)。

## 内容规范

- **一个页面只用一个一级标题（H1）**，章节使用 H2/H3，避免跳级。
- 新增页面时保留 Wiki.js 的 front matter（`title`、`description`、`published` 等），并填写有意义的 `description`。
- 站内链接统一使用 `/zh/<页面路径>`，例如 `/zh/ham-tech/vna`，不要带 `.md` 后缀。
- 图片使用绝对路径引用，例如 `/assets/images/dmr-digi/radioid.webp`；为图片补充简短的 alt 文本。
- 表格、代码块、引用块保持格式完整；命令与代码使用代码块包裹。
- 引用他人资料时注明来源，不直接复制受版权保护的整篇文章。
- 涉及个人信息（呼号、学院、照片）时，请先征得本人同意。

## 图片与文件存放

所有静态资源统一放在 `assets/` 下，按主题分组：

```text
assets/
├── images/
│   ├── avatars/            # 成员头像
│   ├── dmr-digi/           # DMR 注册与配置截图
│   ├── ham-tools/qrz/      # QRZ 教程截图
│   ├── living-in-gdut/     # 校园生活配图
│   ├── radio-indoor/       # 设台流程截图
│   └── legacy/             # 早期根目录图片
├── files/
│   └── radio-indoor/       # 可下载文档
├── examples/
│   └── qrz/                # 可复用 HTML 示例
└── _archive/               # 未被引用的历史素材
```

引用时以仓库根目录为基准，例如文件 `assets/images/dmr-digi/radioid.webp` 写作：

```markdown
![RadioID 注册页面](/assets/images/dmr-digi/radioid.webp)
```

不要直接把图片放在仓库根目录；未被引用的历史素材移入 `assets/_archive/`，不要直接删除。

## 可以贡献什么

- 📡 技术教程：无线电、射频、数字通信、天线与测量
- 🔧 设备操作与维修记录、写频软件说明
- 🎓 课程笔记、学习资源与竞赛经验
- 🏫 校园生活指南：食堂、交通、就医、办事流程
- 🧠 社团历史、老照片、活动记录
- 🛠️ 对现有页面的纠错、补充和排版整理

内容需合法合规，不发布商业广告、侵权内容或与社团无关的敏感信息。

## 协作与审核

- 修改前先加入 QQ 群 **259802400**，说明要编辑的页面，避免多人同时修改同一文件。
- 管理员会审核 Pull Request 或网页编辑，必要时提出修改意见。
- 发现页面错误但不会编辑时，可以在群内反馈，或提交 GitHub Issue。

## 常见问题

| 问题 | 处理方式 |
|------|----------|
| 图片显示为裂图 | 检查文件是否已提交、路径是否以 `/` 开头、文件名大小写是否一致 |
| 站内链接 404 | 确认路径为 `/zh/...`，并与仓库中的文件名完全一致 |
| 网页编辑与 GitHub 同步冲突 | 先联系管理员，暂停同一页面的编辑，合并后再继续 |
| 新增页面未出现在导航 | Wiki.js 导航需在后台配置，可联系管理员加入对应栏目 |

## 相关页面

- [Git 与 GitHub 操作教程](/zh/computer-indoor/Git)
- [wiki.js 编辑器文档](https://docs.requarks.io/editors)
- [返回 Wiki 首页](/zh/home)
