# 项目结构规范

本文描述仓库的目录职责、页面与资源的路径约定，以及 Wiki.js 同步时的注意事项。

## 目录职责

| 路径 | 职责 | 是否发布为页面 |
|------|------|----------------|
| `zh/` | Wiki.js 页面，Markdown 源文件 | 是，路径为 `/zh/<相对路径>` |
| `assets/images/` | 页面配图，按主题分组 | 否，作为静态资源访问 |
| `assets/files/` | 可下载文档（docx、pdf 等） | 否 |
| `assets/examples/` | 可复用示例文件（HTML 片段等） | 否 |
| `assets/_archive/` | 未被引用的历史素材 | 否 |
| `scripts/` | 本地与 CI 校验脚本 | 否 |
| `docs/` | 仓库维护文档 | 否 |
| `.github/` | CI、PR 与 Issue 模板 | 否 |
| `.well-known/` | 域名验证文件 | 否，必须保持在根目录 |

## 页面路径

Wiki.js 将 `zh/` 视为中文语言根目录：

| 源文件 | 站点路径 |
|--------|----------|
| `zh/home.md` | `/zh/home` |
| `zh/ham-tech/index.md` | `/zh/ham-tech/index` |
| `zh/ham-tech/vna.md` | `/zh/ham-tech/vna` |
| `zh/wikicontribution/wiki贡献指南.md` | `/zh/wikicontribution/wiki贡献指南` |

站内链接统一写作 `/zh/<路径>`，不带 `.md` 后缀。链接到目录页时写完整的 `index` / `main-page` 路径，避免依赖服务器默认索引行为。

## 资源路径

所有静态资源放在 `assets/` 下，引用时以仓库根目录为基准：

| 文件 | 引用写法 |
|------|----------|
| `assets/images/dmr-digi/radioid.webp` | `/assets/images/dmr-digi/radioid.webp` |
| `assets/files/radio-indoor/关于台址设置区域设置为全国的说明书.docx` | `/assets/files/radio-indoor/关于台址设置区域设置为全国的说明书.docx` |
| `assets/examples/qrz/bi7khi-page-new.html` | 代码中写相对路径 `assets/examples/qrz/bi7khi-page-new.html` |

禁止：

- 把图片放在仓库根目录；
- 使用外链图片作为关键内容（可临时使用，但需备份到 `assets/`）；
- 在 Markdown 中写本机绝对路径；
- 在仓库中提交 API Key、Token 或密码。

### 图片规范

| 类型 | 最大尺寸 | 建议大小 | 格式 |
|------|----------|----------|------|
| 成员头像 | 200 × 200 | ≤ 60 KB | WebP |
| 截图 / 教程配图 | 1600 px 长边 | ≤ 500 KB | WebP |
| 普通照片 | 1600 px 长边 | ≤ 500 KB | WebP |

单张图片超过 2 MB 会被 CI 判为错误；非 WebP 图片会给出版本提示。

### 资源优化

新增或替换图片后运行：

```bash
python scripts/optimize_images.py
```

脚本会转换 WebP、缩放尺寸、改写 Markdown 引用，并清理 `_archive/` 中的完全重复文件。需要安装 Pillow：`pip install pillow`。

## Front matter

每个页面必须包含：

```yaml
---
title: 页面标题
description: 一句话说明页面内容
published: true
date: 2026-10-22T00:00:00.000Z
tags: 标签1, 标签2
editor: markdown
dateCreated: 2026-10-22T00:00:00.000Z
---
```

- `title`、`description`、`tags` 不得为空；
- `date` 应在页面实质修改时更新；
- `dateCreated` 仅在新建页面时填写。

## 标题与格式

- 每页有且仅有一个 H1；
- 标题层级连续，不跳级（H1 → H2 → H3）；
- 不保留空标题；
- 图片必须写 alt 文本；
- 表格列数保持一致；
- 命令、路径、代码片段使用代码块或行内代码。

## Wiki.js 导航

页面文件不会自动生成侧边栏。新增栏目或页面后，需要在 Wiki.js 管理后台的 **Navigation** 中配置侧边栏入口，否则只能通过站内链接访问。

建议的侧边栏顺序：

1. 主页
2. 新手入门
3. 技术知识库
4. 工具与软件
5. 校园生活
6. 学习笔记
7. 计算机与 AI
8. 社团事务
9. Wiki 贡献指南

## CI 约束

`.github/workflows/check.yml` 运行 `python scripts/check_wiki.py`，校验：

- front matter 必填字段与日期格式；
- 唯一 H1、无空标题、无标题跳级；
- 表格列数一致；
- 行内链接、引用式链接、本地资源可解析；
- 图片 alt 非空；
- 图片格式与体积（超过 2 MB 报错）；
- 孤立页面（仅警告，不阻断）；
- 外部图片清单（INFO，不阻断）。

新增页面或资源后，请在本地先运行脚本，避免 CI 失败。

## 发布与维护

发布流程、Wiki.js 同步检查、密钥管理、分支保护与回滚步骤见 [MAINTENANCE.md](MAINTENANCE.md)。

## 素材归档

未被任何页面引用的图片或文档不直接删除，统一移入 `assets/_archive/`，保留目录结构。确认不再需要后，再由管理员清理。
