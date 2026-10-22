---
title: Git 与 GitHub 操作教程
description: 从安装、首次配置到提交、分支与 Pull Request 的 Git 入门教程
published: true
date: 2026-10-22T00:00:00.000Z
tags: Git, GitHub, 版本控制, 教程
editor: markdown
dateCreated: 2025-11-10T01:57:24.774Z
---

# Git 与 GitHub 操作教程

Git 是由 Linus Torvalds 于 2005 年创建的分布式版本控制系统，用于记录文件的修改历史、支持多人协作和版本回退。GitHub 则是基于 Git 的代码托管平台。

本教程面向第一次接触 Git 的同学，覆盖安装、配置、日常命令和参与本 Wiki 的完整流程。

## Git 能解决什么问题

- **版本管理**：记录每一次修改，随时回滚到任意历史版本。
- **多人协作**：不同成员在各自分支上工作，通过合并整合修改。
- **代码审查**：通过 Pull Request 在合并前讨论和检查改动。
- **备份与恢复**：每个开发者本地都有完整仓库副本。
- **自动化集成**：配合 CI/CD 工具完成构建、测试和部署。

## 安装 Git

- **Windows**：从 <https://git-scm.com/download/win> 下载安装包，安装时保持默认选项即可；也可以使用 `winget install Git.Git`。
- **macOS**：运行 `xcode-select --install`，或使用 Homebrew：`brew install git`。
- **Linux（Debian/Ubuntu）**：`sudo apt install git`。

安装完成后打开终端，确认版本：

```bash
git --version
```

## 首次配置

设置提交时显示的用户名和邮箱（建议与 GitHub 账号一致）：

```bash
git config --global user.name "你的名字"
git config --global user.email "you@example.com"
```

查看当前配置：

```bash
git config --global --list
```

## 三种状态与基本工作流

Git 中的文件通常处于三种状态：

| 状态 | 含义 |
|------|------|
| 已修改（modified） | 工作区文件有改动，尚未加入暂存区 |
| 已暂存（staged） | 改动已标记，会进入下一次提交 |
| 已提交（committed） | 快照已安全保存到本地仓库 |

一次完整的提交流程：

```bash
git status              # 查看当前改动
git add <文件或目录>     # 将改动加入暂存区；git add . 表示全部
git commit -m "说明"    # 提交到本地仓库
```

## 常用命令

| 命令 | 作用 |
|------|------|
| `git init` | 在当前目录初始化新仓库 |
| `git clone <url>` | 克隆远程仓库到本地 |
| `git status` | 查看工作区和暂存区状态 |
| `git diff` | 查看未暂存的改动 |
| `git log --oneline` | 查看提交历史 |
| `git add <file>` | 暂存指定文件 |
| `git commit -m "msg"` | 提交暂存内容 |
| `git pull` | 拉取并合并远程更新 |
| `git push` | 推送本地提交到远程 |
| `git switch -c <branch>` | 新建并切换到分支 |
| `git switch <branch>` | 切换分支 |
| `git merge <branch>` | 将指定分支合并到当前分支 |

## 参与本 Wiki 的 Git 流程

1. 在 GitHub 上 Fork [GDUT_HAM-Wiki](https://github.com/BI7KHI/GDUT_HAM-Wiki)。
2. 克隆自己的 Fork：

   ```bash
   git clone https://github.com/<你的用户名>/GDUT_HAM-Wiki.git
   cd GDUT_HAM-Wiki
   ```

3. 新建分支并修改内容：

   ```bash
   git switch -c docs/fix-links
   # 使用编辑器修改 zh/ 下的 Markdown 文件
   git status
   git diff
   ```

4. 提交并推送：

   ```bash
   git add .
   git commit -m "docs: 修复工具页链接"
   git push -u origin docs/fix-links
   ```

5. 在 GitHub 页面点击 **Compare & pull request**，填写改动说明，等待审核。

更详细的内容规范见 [Wiki 贡献指南](/zh/wikicontribution/wiki贡献指南)。

## 分支与冲突

- **分支**用于隔离不同任务：一个分支只做一件事，合并后删除。
- 合并时若两个分支修改了同一文件的同一位置，Git 会标记为**冲突**：

  ```text
  <<<<<<< HEAD
  当前分支的内容
  =======
  另一分支的内容
  >>>>>>> docs/fix-links
  ```

  手动保留需要的内容，删除冲突标记后重新 `git add` 并 `git commit`。

- 推送被拒绝时，通常需要先 `git pull` 合并远程更新，再重新推送。

## 学习资源

- [Pro Git 中文版（官方书籍）](https://git-scm.com/book/zh/v2)
- [GitHub 官方文档](https://docs.github.com/zh)
- [Learn Git Branching（交互式练习）](https://learngitbranching.js.org/?locale=zh_CN)

## 相关页面

- [Wiki 贡献指南](/zh/wikicontribution/wiki贡献指南)
- [你缺失的那门计算机课](/zh/computer-indoor/你缺失的那门计算机课——主页)
- [返回 Wiki 首页](/zh/home)
