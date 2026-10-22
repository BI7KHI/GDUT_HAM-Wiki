# GDUT_HAM-Wiki

广东工业大学无线电社 Wiki 的内容仓库。站点基于 **Wiki.js** 构建，本仓库中的 `zh/` 目录通过 Git 同步发布为站点内容，静态资源统一放在 `assets/`。

- 🌐 站点：<https://argdut.bi7khi.xyz/>
- 📦 仓库：<https://github.com/BI7KHI/GDUT_HAM-Wiki>
- 📄 内容语言：简体中文

## 仓库结构

```text
.
├── zh/                     # Wiki.js 页面（Markdown），对应站点 /zh/*
├── assets/                 # 所有静态资源
│   ├── images/             # 页面配图，按主题分组
│   ├── files/              # 可下载的文档（docx、pdf 等）
│   ├── examples/           # 可复用示例（如 QRZ 页面 HTML）
│   └── _archive/           # 暂未引用的历史素材，保留待清理
├── scripts/
│   ├── check_wiki.py       # 结构、链接、front matter 校验
│   └── optimize_images.py  # 图片转 WebP、缩放与引用更新
├── docs/
│   ├── STRUCTURE.md        # 目录与编写规范
│   └── MAINTENANCE.md      # 发布、同步、安全与回滚
├── .github/                # CI 与 PR / Issue 模板
├── .well-known/            # 域名验证文件（不要移动）
├── CONTRIBUTING.md         # 贡献入口
└── LICENSE                 # Apache-2.0
```

## 编辑与发布

1. 在 `zh/` 下编辑或新增 Markdown 页面；图片放入 `assets/images/<主题>/`。
2. 页面路径即站点路径：`zh/ham-tech/vna.md` → `/zh/ham-tech/vna`。
3. 资源路径以仓库根目录为基准：`assets/images/dmr-digi/radioid.webp` → `/assets/images/dmr-digi/radioid.webp`。
4. 新增或替换图片后，先优化资源，再运行本地校验：

   ```bash
   python scripts/optimize_images.py
   python scripts/check_wiki.py
   ```

5. 通过网页编辑或 Pull Request 提交，Wiki.js 会从 `main` 分支同步。

详细规范见 [docs/STRUCTURE.md](docs/STRUCTURE.md)、[docs/MAINTENANCE.md](docs/MAINTENANCE.md) 和 [CONTRIBUTING.md](CONTRIBUTING.md)。

## CI 校验

`.github/workflows/check.yml` 会在 Push / PR 时运行 `scripts/check_wiki.py`，检查：

- front matter 必填字段与日期格式
- 每页唯一 H1、标题层级、表格列数
- 站内链接、引用式链接与本地资源
- 图片 alt 文本、格式与体积
- 孤立页面（警告）
- 外部图片清单（提示）

## License

仓库内容与代码按 [Apache License 2.0](LICENSE) 发布。第三方图片、截图、文档的版权归原作者所有，引用时请注明来源。
