# 维护与发布

本文面向 Wiki 管理员，说明发布、资源更新、安全与回滚流程。

## 发布前检查

```bash
python scripts/check_wiki.py
git status --short
git diff --check
```

要求：

- `check_wiki.py` 为 0 个错误；
- 新增图片已经运行 `python scripts/optimize_images.py`；
- 没有把 `assets/_archive/` 中的素材重新引用；
- 没有提交明文密钥、个人隐私或未授权素材。

## 提交与 Wiki.js 同步

1. 提交并推送到 `main`：

   ```bash
   git add -A
   git commit -m "chore: 更新 Wiki 结构与资源"
   git push origin main
   ```

2. 在 Wiki.js 管理后台等待 Git 同步完成，或手动触发同步。
3. 同步后抽查以下页面：

   | 页面 | 检查点 |
   |------|--------|
   | `/zh/home` | 首图、证书、贡献者徽章 |
   | `/zh/ham-tech/DMR` | 7 张注册/配置截图 |
   | `/zh/ham-quickstart/get-license` | 设台流程截图与 docx 下载 |
   | `/zh/ham-tools/qrz-tutorial` | QRZ 截图 |
   | `/zh/Knowledge_living-in-GDUT/old_deng-quickstart` | 地图链接、琴房照片 |
   | `/zh/members` | 本地头像与外部头像 |

4. 浏览器强制刷新（Ctrl+F5），确认没有 404 或裂图。
5. 若图片仍指向旧路径，检查 Wiki.js 的 Git 同步是否完成，或清理站点缓存后重试。

## 资源更新流程

1. 将新图片放入 `assets/images/<主题>/`。
2. 运行：

   ```bash
   python scripts/optimize_images.py
   python scripts/check_wiki.py
   ```

3. 检查脚本输出的体积变化与 Markdown 引用替换结果。
4. 提交时同时包含图片文件和被更新的 Markdown。

> 不要直接在 `zh/` 中引用仓库根目录或旧 `avatars/`、`dmr-digi/` 路径。

## 导航配置

Wiki.js 的侧边栏不在本仓库中。新增栏目后，需要在后台 **Navigation** 中配置入口。推荐顺序见 [STRUCTURE.md](STRUCTURE.md)。

## 安全与密钥

- 仓库中禁止提交 API Key、Token、密码或私钥。
- 历史版本中曾出现高德静态地图 Key；该 Key 已被服务端回收。若未来重新启用地图 API：
  - 使用域名/Referer 白名单；
  - 不要把 Key 写进 Markdown；
  - 优先使用本地截图或普通地图链接。
- 成员个人信息（呼号、学院、头像）由本人授权维护，可应本人要求移除。

## 外部链接与图片

- `check_wiki.py` 会列出外部图片（INFO，不阻断 CI）。
- 建议每季度抽查一次外部链接；关键教程中的外链图片应本地化到 `assets/`。
- 成员头像、contrib.rocks 徽章等动态外链可以保留。

## 归档清理

- `assets/_archive/` 保存未引用素材，便于回溯。
- 每学期检查一次；确认不再需要后由管理员删除。
- 归档文件不参与页面引用，也不应重新加入正文。

## 回滚

1. 使用 `git revert` 撤销对应提交，或恢复到上一个稳定提交。
2. 推送后等待 Wiki.js 同步。
3. 若 CSS/图片缓存导致显示异常，清理浏览器缓存并重新同步。

## 分支保护建议

在 GitHub 仓库设置中：

- 保护 `main` 分支；
- 要求 Pull Request 审核；
- 将 `Wiki checks` 设为必需状态检查；
- 禁止直接向 `main` 强制推送。

## 待决策

- **内容许可证**：当前仓库使用 Apache-2.0（适合代码），Wiki 文字内容是否改为 CC BY-SA 4.0 需社团负责人确认。
- **成员头像本地化**：是否统一镜像到 `assets/images/avatars/`，需征得成员同意。
