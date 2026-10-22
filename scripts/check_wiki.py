#!/usr/bin/env python3
"""Validate the GDUT_HAM-Wiki content tree.

Checks:
  * front matter fields
  * one H1 per page, heading level jumps, empty headings
  * internal links and local assets
  * image alt text
  * orphan pages (warning only)

No third-party dependencies; safe to run locally and in GitHub Actions.
"""

from __future__ import annotations

import os
import posixpath
import re
import sys
import urllib.parse
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZH = os.path.join(ROOT, "zh")
PAGE_SUFFIXES = ("/index", "/main-page", "/main-pages")
REQUIRED_FIELDS = ("title", "description", "published", "date", "tags", "dateCreated")
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
ASSET_WARN_BYTES = 500 * 1024
ASSET_ERROR_BYTES = 2 * 1024 * 1024
DATE_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})$"
)

MD_LINK = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)(?:\s+[\"'][^\"']*[\"'])?\)")
HTML_TAG = re.compile(r"<(img|a|source|video|audio)\b[^>]*>", re.IGNORECASE)
HTML_ATTR = re.compile(r"\b(src|href)=[\"']([^\"']+)[\"']", re.IGNORECASE)
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
EMPTY_HEADING = re.compile(r"^#{1,6}\s*$")
REF_DEF = re.compile(r"^\s*\[([^\]]+)\]:\s*(\S+)")
REF_USE = re.compile(r"\[([^\]]+)\]\[([^\]]*)\]")
FRONT_MATTER = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
SKIP_PREFIXES = ("#", "http://", "https://", "mailto:", "tel:", "data:", "ftp://")


def norm(path: str) -> str:
    return path.replace(os.sep, "/")


def rel(path: str) -> str:
    return norm(os.path.relpath(path, ROOT))


def load_pages() -> dict[str, str]:
    pages: dict[str, str] = {}
    for dirpath, _, filenames in os.walk(ZH):
        for name in filenames:
            if not name.endswith(".md"):
                continue
            full = os.path.join(dirpath, name)
            key = norm(os.path.relpath(full, ZH))[:-3]
            pages[key] = full
    return pages


def parse_front_matter(text: str) -> dict[str, str] | None:
    match = FRONT_MATTER.match(text)
    if not match:
        return None
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def content_lines(text: str):
    """Yield (line_number, line) while skipping fenced code blocks."""
    in_fence = False
    fence = ""
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence, fence = True, marker
            elif marker == fence:
                in_fence, fence = False, ""
            continue
        if in_fence:
            continue
        yield number, re.sub(r"`[^`]*`", "", line)


def resolve_url(url: str, page_key: str) -> str | None:
    """Return a repo-relative path for an internal URL, or None to skip."""
    if url.startswith(SKIP_PREFIXES) or not url.strip():
        return None
    clean = urllib.parse.unquote(url.split("#", 1)[0].split("?", 1)[0]).strip()
    if not clean:
        return None
    if clean.startswith("/zh/"):
        path = "zh/" + clean[len("/zh/") :]
    elif clean.startswith("/"):
        path = clean.lstrip("/")
    else:
        base = posixpath.dirname("zh/" + page_key)
        path = posixpath.normpath(posixpath.join(base, clean))
    path = path.rstrip("/")
    return path or None


def target_exists(path: str) -> bool:
    candidate = os.path.join(ROOT, norm(path))
    if os.path.isfile(candidate):
        return True
    if os.path.isfile(candidate + ".md"):
        return True
    return any(os.path.isfile(candidate + suffix + ".md") for suffix in PAGE_SUFFIXES)


def page_key_for(path: str, pages: dict[str, str]) -> str | None:
    key = path[3:] if path.startswith("zh/") else path
    if key.endswith(".md"):
        key = key[:-3]
    if key in pages:
        return key
    for suffix in PAGE_SUFFIXES:
        if key + suffix in pages:
            return key + suffix
    return None


def check_page(key: str, full: str, pages: dict[str, str], inbound: dict[str, set[str]]):
    errors: list[str] = []
    warnings: list[str] = []
    infos: list[str] = []
    try:
        text = open(full, encoding="utf-8").read()
    except UnicodeDecodeError:
        return [f"{key}: 文件不是有效的 UTF-8 编码"], warnings, infos

    meta = parse_front_matter(text)
    if meta is None:
        errors.append(f"{key}: 缺少 front matter")
    else:
        for field in REQUIRED_FIELDS:
            if not meta.get(field):
                errors.append(f"{key}: front matter 缺少或为空的字段 `{field}`")
        if meta.get("published", "").lower() != "true":
            errors.append(f"{key}: `published` 应为 true")
        for field in ("date", "dateCreated"):
            value = meta.get(field, "")
            if value and not DATE_RE.match(value):
                errors.append(f"{key}: `{field}` 格式应为 2026-10-22T00:00:00.000Z")

    lines = list(content_lines(text))
    definitions: dict[str, tuple[int, str]] = {}
    for number, line in lines:
        match = REF_DEF.match(line)
        if match:
            definitions[match.group(1).lower()] = (number, match.group(2))

    for label, (number, url) in definitions.items():
        path = resolve_url(url, key)
        if path is not None and not target_exists(path):
            errors.append(f"{key}:{number}: 引用式链接定义不存在：{url}")

    h1_count = 0
    previous_level = 0
    table_start: int | None = None
    table_pipes: list[int] = []

    def close_table() -> None:
        nonlocal table_start, table_pipes
        if table_start is not None and len(set(table_pipes)) > 1:
            errors.append(f"{key}:{table_start}: 表格列数不一致：{table_pipes}")
        table_start = None
        table_pipes = []

    for number, line in lines:
        if EMPTY_HEADING.match(line):
            errors.append(f"{key}:{number}: 空标题")

        if line.lstrip().startswith("|"):
            if table_start is None:
                table_start = number
            table_pipes.append(line.count("|"))
        else:
            close_table()

        match = HEADING.match(line)
        if match:
            level = len(match.group(1))
            if level == 1:
                h1_count += 1
            if previous_level and level > previous_level + 1:
                errors.append(
                    f"{key}:{number}: 标题层级从 H{previous_level} 跳到 H{level}"
                )
            previous_level = level

        for match in REF_USE.finditer(line):
            label = (match.group(2) or match.group(1)).lower()
            if label not in definitions:
                errors.append(f"{key}:{number}: 引用式链接缺少定义：[{label}]")

        for match in MD_LINK.finditer(line):
            is_image, alt, url = match.group(1) == "!", match.group(2), match.group(3)
            if is_image and not alt.strip():
                errors.append(f"{key}:{number}: 图片缺少 alt 文本：{url}")
            if is_image and url.startswith(("http://", "https://")):
                infos.append(f"{key}:{number}: 外部图片：{url}")
            path = resolve_url(url, key)
            if path is None:
                continue
            if not target_exists(path):
                errors.append(f"{key}:{number}: 链接目标不存在：{url}")
                continue
            target = page_key_for(path, pages)
            if target:
                inbound[target].add(key)
            elif not path.startswith("assets/"):
                warnings.append(f"{key}:{number}: 链接未使用 /zh/ 或 /assets/ 前缀：{url}")

        for tag in HTML_TAG.finditer(line):
            raw = tag.group(0)
            if tag.group(1).lower() == "img" and not re.search(r"\balt\s*=", raw, re.I):
                errors.append(f"{key}:{number}: <img> 缺少 alt 属性")
            for attr in HTML_ATTR.finditer(raw):
                url = attr.group(2)
                if tag.group(1).lower() == "img" and url.startswith(("http://", "https://")):
                    infos.append(f"{key}:{number}: 外部图片：{url}")
                path = resolve_url(url, key)
                if path is None:
                    continue
                if not target_exists(path):
                    errors.append(f"{key}:{number}: HTML 资源不存在：{url}")

    close_table()

    if h1_count == 0:
        errors.append(f"{key}: 缺少 H1")
    elif h1_count > 1:
        errors.append(f"{key}: 有 {h1_count} 个 H1，每页只允许一个")

    return errors, warnings, infos


def main() -> int:
    pages = load_pages()
    if not pages:
        print("没有找到 zh/ 下的 Markdown 页面", file=sys.stderr)
        return 1

    inbound: dict[str, set[str]] = defaultdict(set)
    errors: list[str] = []
    warnings: list[str] = []
    infos: list[str] = []

    for key in sorted(pages):
        page_errors, page_warnings, page_infos = check_page(
            key, pages[key], pages, inbound
        )
        errors.extend(page_errors)
        warnings.extend(page_warnings)
        infos.extend(page_infos)

    for key in sorted(pages):
        if key in ("home", "README"):
            continue
        if not inbound[key]:
            warnings.append(f"{key}: 孤立的页面（没有任何站内链接指向它）")

    for dirpath, _, filenames in os.walk(os.path.join(ROOT, "assets")):
        for name in filenames:
            if name == "README.md":
                continue
            path = os.path.join(dirpath, name)
            ext = os.path.splitext(name)[1].lower()
            if ext not in IMAGE_EXTS:
                continue
            size = os.path.getsize(path)
            asset = rel(path)
            if ext not in (".webp", ".svg"):
                warnings.append(f"{asset}: 建议转换为 WebP 格式")
            if size > ASSET_ERROR_BYTES:
                errors.append(f"{asset}: 图片超过 2 MB（{size // 1024} KB）")
            elif size > ASSET_WARN_BYTES:
                warnings.append(f"{asset}: 图片超过 500 KB（{size // 1024} KB）")

    for item in errors:
        print(f"ERROR   {item}")
    for item in warnings:
        print(f"WARNING {item}")
    for item in infos:
        print(f"INFO    {item}")

    print(
        f"\n检查完成：{len(pages)} 个页面，{len(errors)} 个错误，"
        f"{len(warnings)} 个警告，{len(infos)} 个提示"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
