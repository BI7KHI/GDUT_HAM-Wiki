# 静态资源目录

本目录集中存放 Wiki 页面使用的图片、文档和示例文件。

> ⚠️ **路径变更（2026-10）**：原先位于仓库根目录、`avatars/`、`dmr-digi/`、`radio-indoor/`、`images-living-know-in-gdut/` 等位置的资源，已统一迁移到 `assets/`，并转换为 WebP。旧图片 URL 不再有效，请改用 `/assets/...` 路径。

## 结构

```text
assets/
├── images/                 # 页面配图
│   ├── avatars/            # 成员头像
│   ├── dmr-digi/           # DMR 注册与配置截图
│   ├── ham-tools/qrz/      # QRZ 教程截图
│   ├── living-in-gdut/     # 校园生活配图
│   ├── radio-indoor/       # 设台流程截图
│   └── legacy/             # 早期根目录图片
├── files/                  # 可下载文档
│   └── radio-indoor/
├── examples/               # 可复用代码/HTML 示例
│   └── qrz/
└── _archive/               # 未被引用的历史素材
```

## 图片规范

| 类型 | 最大尺寸 | 建议大小 | 格式 |
|------|----------|----------|------|
| 成员头像 | 200 × 200 | ≤ 60 KB | WebP |
| 截图 / 教程配图 | 1600 px 长边 | ≤ 500 KB | WebP |
| 普通照片 | 1600 px 长边 | ≤ 500 KB | WebP |

- 所有页面图片必须使用 **WebP**。
- 单张图片不得超过 **2 MB**，超过会在 CI 中报错。
- 必须填写有意义的 alt 文本。
- 不使用外链图片作为关键内容；成员头像等动态外链可作为例外。

## 命名

- 新文件使用小写英文、数字和连字符：`vna-calibration-osl.webp`。
- 同一主题放入同一子目录。
- 不使用空格和特殊符号；现有中文文件名保持兼容。

## 引用

以仓库根目录为基准：

```markdown
![VNA 校准界面](/assets/images/ham-tech/vna-calibration-osl.webp)
[说明书下载](/assets/files/radio-indoor/manual.docx)
```

## 批量优化

新增图片后运行：

```bash
python scripts/optimize_images.py
python scripts/check_wiki.py
```

脚本会：

- 将 PNG/JPEG 转为 WebP；
- 头像缩放到 200px，其他图片缩放到 1600px；
- 自动改写 Markdown 引用；
- 删除归档目录中的重复文件。

需要安装 Pillow：`pip install pillow`。

## 归档

未被任何页面引用的文件移入 `_archive/`，保留原相对路径。不要直接删除素材，除非管理员确认。
