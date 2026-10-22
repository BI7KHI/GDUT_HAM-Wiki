#!/usr/bin/env python3
"""Convert wiki images to WebP, resize them, and update Markdown references.

Usage:
    python scripts/optimize_images.py

Behaviour:
  * Avatars are resized to at most 200x200.
  * Other images are resized to at most 1600x1600.
  * Originals are removed after a successful conversion.
  * Markdown references are rewritten from .png/.jpg/.jpeg to .webp.
  * Unreferenced archive images are deduplicated and compressed.

Requires Pillow:  pip install pillow
"""

from __future__ import annotations

import hashlib
import os
import re
import sys

try:
    from PIL import Image, ImageOps
except ImportError:  # pragma: no cover
    print("需要 Pillow：pip install pillow", file=sys.stderr)
    sys.exit(1)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
IMAGE_EXTS = {".png", ".jpg", ".jpeg"}

# Optional semantic renames for legacy hash-named files.
RENAMES = {
    "assets/images/avatars/01609ec1169be6afdd7e7151fbb0a64b.png": "assets/images/avatars/bg7jrh.webp",
    "assets/images/avatars/20251112220553_52_452.jpg": "assets/images/avatars/bg7loy.webp",
    "assets/images/avatars/5b9decfd9208004ad69cca1168b66c4f.jpg": "assets/images/avatars/ba7ksg.webp",
    "assets/images/legacy/14389181.png": "assets/images/legacy/thanks.webp",
    "assets/images/legacy/ba7iwr_cqwpx_2025_ssb_certificate.png": "assets/images/legacy/wpx-2025-certificate.webp",
    "assets/images/legacy/kaltsit.jpg": "assets/images/legacy/40th-anniversary.webp",
}


def norm(path: str) -> str:
    return path.replace(os.sep, "/")


def rel(path: str) -> str:
    return norm(os.path.relpath(path, ROOT))


def target_path(src_rel: str) -> str:
    if src_rel in RENAMES:
        return RENAMES[src_rel]
    return os.path.splitext(src_rel)[0] + ".webp"


def settings(src_rel: str):
    if "/avatars/" in src_rel:
        return 200, 82, 60 * 1024
    if "/living-in-gdut/" in src_rel:
        return 1600, 82, 500 * 1024
    if "/radio-indoor/" in src_rel or "/dmr-digi/" in src_rel:
        return 1600, 88, 500 * 1024
    if "/ham-tools/qrz/" in src_rel:
        return 1600, 88, 500 * 1024
    return 1600, 86, 500 * 1024


def convert(src: str, dst: str, max_side: int, quality: int, max_bytes: int) -> None:
    image = Image.open(src)
    image = ImageOps.exif_transpose(image)
    has_alpha = "A" in image.getbands() or (
        image.mode == "P" and "transparency" in image.info
    )
    image = image.convert("RGBA" if has_alpha else "RGB")
    image.thumbnail((max_side, max_side), Image.LANCZOS)

    os.makedirs(os.path.dirname(dst), exist_ok=True)
    current = quality
    while True:
        image.save(dst, "WEBP", quality=current, method=6)
        if os.path.getsize(dst) <= max_bytes or current <= 60:
            break
        current -= 8


def update_markdown(old_rel: str, new_rel: str) -> int:
    changed = 0
    for dirpath, dirs, files in os.walk(ROOT):
        if ".git" in dirpath.split(os.sep):
            continue
        if "node_modules" in dirpath.split(os.sep):
            continue
        for name in files:
            if not name.endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            text = open(path, encoding="utf-8").read()
            updated = text.replace("/" + old_rel, "/" + new_rel)
            updated = updated.replace(old_rel, new_rel)
            if updated != text:
                open(path, "w", encoding="utf-8", newline="").write(updated)
                changed += 1
    return changed


def dedupe_archive() -> int:
    seen: dict[str, str] = {}
    removed = 0
    for dirpath, _, files in os.walk(ASSETS):
        for name in files:
            path = os.path.join(dirpath, name)
            if name == "README.md":
                continue
            digest = hashlib.sha256(open(path, "rb").read()).hexdigest()
            if digest not in seen:
                seen[digest] = path
                continue
            current = rel(path)
            keeper = rel(seen[digest])
            current_is_archive = "/_archive/" in "/" + current
            keeper_is_archive = "/_archive/" in "/" + keeper
            if current_is_archive:
                os.remove(path)
                removed += 1
                print(f"  duplicate removed: {current}")
            elif keeper_is_archive:
                os.remove(seen[digest])
                seen[digest] = path
                removed += 1
                print(f"  duplicate removed: {keeper}")
    return removed


def optimize_tree(root_dir: str, archive: bool = False) -> tuple[int, int]:
    converted = 0
    rewritten = 0
    for dirpath, _, files in os.walk(root_dir):
        for name in files:
            ext = os.path.splitext(name)[1].lower()
            if ext not in IMAGE_EXTS:
                continue
            src = os.path.join(dirpath, name)
            src_rel = rel(src)
            dst_rel = target_path(src_rel)
            dst = os.path.join(ROOT, dst_rel)

            if archive:
                max_side, quality, max_bytes = 1200, 75, 300 * 1024
            else:
                max_side, quality, max_bytes = settings(src_rel)

            before = os.path.getsize(src)
            convert(src, dst, max_side, quality, max_bytes)
            after = os.path.getsize(dst)
            print(f"  {src_rel} -> {dst_rel}  {before // 1024}KB -> {after // 1024}KB")
            os.remove(src)
            converted += 1
            if not archive:
                rewritten += update_markdown(src_rel, dst_rel)
    return converted, rewritten


def remove_empty_dirs() -> None:
    for dirpath, _, _ in os.walk(ASSETS, topdown=False):
        if dirpath == ASSETS:
            continue
        if not os.listdir(dirpath):
            os.rmdir(dirpath)


def main() -> int:
    if not os.path.isdir(ASSETS):
        print("assets/ 不存在", file=sys.stderr)
        return 1

    print("清理归档重复文件…")
    removed = dedupe_archive()
    print(f"  删除重复文件 {removed} 个")

    print("转换 assets/images…")
    converted, rewritten = optimize_tree(os.path.join(ASSETS, "images"))
    print(f"  转换 {converted} 张图片，更新 {rewritten} 个 Markdown 文件")

    archive_dir = os.path.join(ASSETS, "_archive")
    if os.path.isdir(archive_dir):
        print("压缩 assets/_archive…")
        archived, _ = optimize_tree(archive_dir, archive=True)
        print(f"  转换 {archived} 张归档图片")

    remove_empty_dirs()
    print("完成。请运行：python scripts/check_wiki.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
