# 贡献指南

欢迎参与 GDUT_HAM-Wiki 的编写与维护。完整的内容规范见 [docs/STRUCTURE.md](docs/STRUCTURE.md)，站内版本见 [Wiki 贡献指南](https://argdut.bi7khi.xyz/zh/wikicontribution/wiki贡献指南)。

## 快速开始

1. 加入贡献者 QQ 群 **259802400**，说明要修改的页面，避免多人同时编辑同一文件。
2. Fork 本仓库并新建分支：

   ```bash
   git switch -c docs/update-ham-tech
   ```

3. 在 `zh/` 下编辑 Markdown 页面：

   - 每页仅一个 H1，章节使用 H2/H3；
   - 站内链接使用 `/zh/<页面路径>`；
   - 图片统一使用 WebP，放入 `assets/images/<主题>/`，引用路径以 `/assets/images/...` 开头；
   - 头像 ≤ 200px、其他图片 ≤ 1600px，单张 ≤ 500KB；
   - 图片必须写 alt 文本；
   - 保留并完善 front matter。

4. 新增或替换图片后，先运行图片优化，再运行校验：

   ```bash
   python scripts/optimize_images.py
   python scripts/check_wiki.py
   ```

5. 提交并创建 Pull Request：

   ```bash
   git add .
   git commit -m "docs: 更新 VNA 校准说明"
   git push -u origin docs/update-ham-tech
   ```

## PR 检查清单

- [ ] 改动只涉及必要的页面/资源
- [ ] 本地 `python scripts/check_wiki.py` 通过
- [ ] 新增图片已放入 `assets/images/<主题>/`，已转为 WebP 且单张 ≤ 500KB
- [ ] 图片 alt 文本完整
- [ ] 站内链接可正常跳转
- [ ] 没有提交个人隐私、未授权图片或商业广告
- [ ] 引用第三方资料时已注明来源

## Front matter 模板

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

## 资源命名

- 新文件使用小写英文与连字符：`vna-calibration-open-short-load.webp`；
- 同一主题的图片放在同一目录；
- 不把图片直接放在仓库根目录；
- 未被引用的历史素材放入 `assets/_archive/`，不要直接删除。
