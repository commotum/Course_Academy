#!/usr/bin/env python3
"""Audit assignment-owned images and Markdown references before cleanup."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote


IMAGE_EXTENSIONS = {
    ".avif",
    ".bmp",
    ".gif",
    ".heic",
    ".heif",
    ".jpeg",
    ".jpg",
    ".png",
    ".svg",
    ".tif",
    ".tiff",
    ".webp",
}
MARKDOWN_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))(?:\s+[^)]*)?\)")
WIKI_IMAGE_RE = re.compile(r"!\[\[([^]|]+)(?:\|[^\]]*)?\]\]")
REMOTE_RE = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//)", re.IGNORECASE)


@dataclass(frozen=True)
class ImageInfo:
    path: Path
    size: int
    sha256: str
    pixel_sha256: str | None
    dimensions: tuple[int, int] | None
    dhash: int | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("assignment", type=Path, help="Assignment Markdown file or folder.")
    parser.add_argument(
        "--similar-distance",
        type=int,
        default=2,
        help="Maximum dHash Hamming distance for visual candidates (default: 2).",
    )
    return parser.parse_args()


def resolve_assignment(raw: Path) -> Path:
    path = raw.expanduser().resolve()
    if path.is_file():
        if path.suffix.lower() != ".md":
            raise ValueError(f"not a Markdown file: {path}")
        return path
    if not path.is_dir():
        raise ValueError(f"path does not exist: {path}")
    preferred = path / f"{path.name}.md"
    if preferred.is_file():
        return preferred
    candidates = sorted(path.glob("*.md"))
    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        raise ValueError(f"no root Markdown file found in: {path}")
    names = ", ".join(candidate.name for candidate in candidates)
    raise ValueError(f"multiple root Markdown files found ({names}); pass one explicitly")


def is_assignment_owned(path: Path, root: Path, assignment_name: str) -> bool:
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return False
    if not parts:
        return False
    if parts[0] in {"Lessons", "Prerequisites"}:
        return False
    if parts[0] == "Source" and len(parts) >= 2 and parts[1] != assignment_name:
        return False
    return True


def image_paths(root: Path, assignment_name: str) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix.lower() in IMAGE_EXTENSIONS
        and is_assignment_owned(path, root, assignment_name)
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def decoded_image_data(path: Path) -> tuple[str | None, tuple[int, int] | None, int | None]:
    try:
        from PIL import Image
    except ImportError:
        return None, None, None
    try:
        with Image.open(path) as image:
            rgba = image.convert("RGBA")
            dimensions = rgba.size
            pixel_digest = hashlib.sha256(
                f"{dimensions[0]}x{dimensions[1]}:RGBA:".encode() + rgba.tobytes()
            ).hexdigest()
            sample = image.convert("L").resize((9, 8))
            if hasattr(sample, "get_flattened_data"):
                pixels = list(sample.get_flattened_data())
            else:
                pixels = list(sample.getdata())
            bits = 0
            for row in range(8):
                offset = row * 9
                for column in range(8):
                    bits = (bits << 1) | (
                        1 if pixels[offset + column] > pixels[offset + column + 1] else 0
                    )
            return pixel_digest, dimensions, bits
    except Exception:
        return None, None, None


def collect_info(paths: list[Path]) -> list[ImageInfo]:
    infos: list[ImageInfo] = []
    for path in paths:
        pixel_digest, dimensions, dhash = decoded_image_data(path)
        infos.append(
            ImageInfo(
                path=path,
                size=path.stat().st_size,
                sha256=sha256_file(path),
                pixel_sha256=pixel_digest,
                dimensions=dimensions,
                dhash=dhash,
            )
        )
    return infos


def extract_references(markdown: str) -> list[str]:
    refs: list[str] = []
    for match in MARKDOWN_IMAGE_RE.finditer(markdown):
        refs.append(unquote(match.group(1) or match.group(2)))
    for match in WIKI_IMAGE_RE.finditer(markdown):
        refs.append(unquote(match.group(1)))
    return refs


def related_documents(primary: Path) -> list[Path]:
    if primary.parent.name != "Source":
        return [primary]
    match = re.match(r"^(.+)-(?:PRE|LEC)$", primary.stem)
    if not match:
        return [primary]
    code = match.group(1)
    candidates = [primary.parent / f"{code}-PRE.md", primary.parent / f"{code}-LEC.md"]
    return [path for path in candidates if path.is_file()]


def resolve_reference(ref: str, markdown_dir: Path, owned: list[Path]) -> Path | None:
    if REMOTE_RE.match(ref) or ref.startswith("#"):
        return None
    candidate = (markdown_dir / ref).resolve()
    if candidate.exists():
        return candidate
    basename_matches = [path for path in owned if path.name == Path(ref).name]
    if len(basename_matches) == 1:
        return basename_matches[0]
    return candidate


def relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def print_groups(title: str, groups: list[list[ImageInfo]], root: Path) -> None:
    print(f"\n{title}: {len(groups)} group(s)")
    for index, group in enumerate(groups, start=1):
        print(f"  Group {index}:")
        for info in group:
            dimensions = (
                f"{info.dimensions[0]}x{info.dimensions[1]}"
                if info.dimensions
                else "dimensions unavailable"
            )
            print(f"    - {relative(info.path, root)} ({info.size} bytes, {dimensions})")


def grouped(infos: list[ImageInfo], key_name: str) -> list[list[ImageInfo]]:
    groups: dict[str, list[ImageInfo]] = defaultdict(list)
    for info in infos:
        value = getattr(info, key_name)
        if value:
            groups[str(value)].append(info)
    return [group for group in groups.values() if len(group) > 1]


def hamming(left: int, right: int) -> int:
    return (left ^ right).bit_count()


def similar_pairs(infos: list[ImageInfo], maximum: int) -> list[tuple[ImageInfo, ImageInfo, int]]:
    pairs: list[tuple[ImageInfo, ImageInfo, int]] = []
    for index, left in enumerate(infos):
        if left.dhash is None or left.dimensions is None:
            continue
        left_ratio = left.dimensions[0] / left.dimensions[1]
        for right in infos[index + 1 :]:
            if right.dhash is None or right.dimensions is None:
                continue
            if left.pixel_sha256 == right.pixel_sha256:
                continue
            right_ratio = right.dimensions[0] / right.dimensions[1]
            if abs(left_ratio - right_ratio) > 0.02:
                continue
            distance = hamming(left.dhash, right.dhash)
            if distance <= maximum:
                pairs.append((left, right, distance))
    return pairs


def main() -> int:
    args = parse_args()
    try:
        assignment = resolve_assignment(args.assignment)
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    root = assignment.parent
    canonical = root / "Images" if root.name == "Source" else root / "Source" / assignment.stem / "Images"
    owned = image_paths(root, assignment.stem)
    infos = collect_info(owned)
    documents = related_documents(assignment)
    refs: list[str] = []
    for document in documents:
        refs.extend(extract_references(document.read_text(encoding="utf-8")))
    ref_counts = Counter(refs)
    resolved = {ref: resolve_reference(ref, root, owned) for ref in ref_counts}
    resolved_existing = {
        path.resolve()
        for path in resolved.values()
        if path is not None and path.exists() and path.is_file()
    }

    print(f"Primary document: {assignment}")
    print("Reference scope:")
    for document in documents:
        print(f"  - {document}")
    print(f"Canonical image directory: {canonical}")
    print(f"Assignment-owned images: {len(infos)}")
    print(f"Image embeds: {sum(ref_counts.values())} ({len(ref_counts)} unique paths)")

    print("\nReferences:")
    if not ref_counts:
        print("  (none)")
    for ref, count in sorted(ref_counts.items()):
        path = resolved[ref]
        if path is None:
            status = "remote or non-file"
        elif path.exists():
            status = relative(path, root)
        else:
            status = "MISSING"
        print(f"  - {ref} x{count}: {status}")

    missing = [
        ref
        for ref, path in resolved.items()
        if path is not None and not path.exists()
    ]
    unreferenced = [info for info in infos if info.path.resolve() not in resolved_existing]
    loose = [info for info in infos if canonical not in info.path.parents]

    print(f"\nMissing local references: {len(missing)}")
    for ref in sorted(missing):
        print(f"  - {ref}")

    print(f"\nLoose/noncanonical assignment images: {len(loose)}")
    for info in loose:
        print(f"  - {relative(info.path, root)}")

    print(f"\nUnreferenced assignment images: {len(unreferenced)}")
    for info in unreferenced:
        print(f"  - {relative(info.path, root)}")

    print_groups("Exact byte duplicates", grouped(infos, "sha256"), root)
    print_groups("Exact decoded-pixel duplicates", grouped(infos, "pixel_sha256"), root)

    candidates = similar_pairs(infos, max(0, args.similar_distance))
    print(f"\nVisual-similarity candidates: {len(candidates)} pair(s)")
    for left, right, distance in candidates:
        print(
            f"  - distance {distance}: {relative(left.path, root)}"
            f" <-> {relative(right.path, root)}"
        )

    if any(info.pixel_sha256 is not None for info in infos):
        print("\nDecoded-pixel and visual checks: available (Pillow)")
    else:
        print("\nDecoded-pixel and visual checks: unavailable; install Pillow or inspect manually")

    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
