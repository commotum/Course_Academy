"""Keep original source image bytes and a recoverable evidence manifest."""
from __future__ import annotations

import base64
import hashlib
import re
from pathlib import Path
from urllib.parse import unquote_to_bytes

from ..storage import atomic_bytes, atomic_json, read_json


def image_extension(data, content_type=""):
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if data.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return "gif"
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        return "webp"
    start = data[:4096].lstrip()
    if (start.startswith(b"<svg") or start.startswith(b"<?xml")) and b"<svg" in start:
        return "svg"
    raise ValueError("Source response is not a supported image: " + content_type)


def replace_markers(item, replacements):
    if isinstance(item, dict):
        return {key: value if key in ("html", "raw_html", "source_url") else replace_markers(value, replacements)
                for key, value in item.items()}
    if isinstance(item, list):
        return [replace_markers(value, replacements) for value in item]
    if isinstance(item, str):
        for before, after in replacements.items():
            item = item.replace(before, after)
    return item


def solution_image_bindings(item, prior):
    """Recover broken MA history aliases only when the entire solution matches."""
    if not prior or not prior.get("worked_solution"):
        return {}
    image = r"!\[[^\]]*\]\(([^)]+)\)"
    normalize = lambda value: re.sub(r"\s+", " ", re.sub(image, "![](@image@)", value)).strip()
    previous, current = prior["worked_solution"], item.get("worked_solution", "")
    old_paths, markers = re.findall(image, previous), re.findall(image, current)
    if not old_paths or len(old_paths) != len(markers) or normalize(previous) != normalize(current):
        return {}
    originals = {a.get("path"): a for a in prior.get("assets", [])}
    result = {}
    for path, marker in zip(old_paths, markers):
        found = re.fullmatch(r"@asset-(\d+)@", marker)
        if not found:
            continue
        index = int(found[1])
        asset = next((a for a in item.get("assets", []) if a["index"] == index), {})
        original = originals.get(path, {})
        if (re.fullmatch(r"https://mathacademy\.com/graphics/q-\d+-e-\d+", asset.get("source_url") or "")
                and Path(path).is_file() and original.get("sha256") == hashlib.sha256(Path(path).read_bytes()).hexdigest()):
            result[index] = original
    return result


class AssetCapture:
    def __init__(self, browser):
        self.browser = browser

    def _fetch(self, source):
        if source.startswith("data:"):
            header, encoded = source.split(",", 1)
            return (base64.b64decode(encoded) if ";base64" in header else unquote_to_bytes(encoded), header[5:].split(";")[0])
        response = self.browser.image_responses.get(source)
        if response is not None:
            try:
                return response.body(), response.headers.get("content-type", "")
            except Exception:
                pass  # An old Playwright response may have been discarded after navigation.
        response = self.browser.context.request.get(source, timeout=self.browser.config.timeout_ms)
        if not response.ok:
            raise ValueError("Image HTTP " + str(response.status) + ": " + source)
        return response.body(), response.headers.get("content-type", "")

    def collect(self, item, scope, directory, evidence_id, prior=None):
        directory = Path(directory)
        manifest_path = directory / "assets" / "manifest.json"
        manifest = read_json(manifest_path, {}) or {}
        replacements = {}
        recovery = solution_image_bindings(item, prior)
        for field in item.get("fields", []):
            for choice in field.get("choices", []):
                indexes = [int(i) for i in re.findall(r"@asset-(\d+)@", str(choice.get("value", "")))]
                urls = [a.get("source_url") for a in item.get("assets", []) if a["index"] in indexes and a.get("source_url")]
                if len(urls) == 1:
                    choice["source_url"] = urls[0]
                if urls:
                    choice["source_urls"] = urls
        # extract.js assigns these indices to precisely the graphics in the record.
        for asset in item.get("assets", []):
            identity = asset.get("source_url") or evidence_id + ":" + str(asset["index"])
            try:
                source = asset.get("source_url")
                representation = "original"
                if asset["tag"] == "svg":
                    data, mime = asset["html"].encode("utf-8"), "image/svg+xml"
                elif asset["tag"] == "canvas":
                    node = scope.locator("canvas").nth(asset.get("dom_index", 0))
                    encoded = node.evaluate("n => n.toDataURL('image/png')")
                    data, mime = base64.b64decode(encoded.split(",", 1)[1]), "image/png"
                    representation = "canvas_render"
                elif source:
                    data, mime = self._fetch(source)
                else:
                    raise ValueError("Source image has no URL")
                extension = image_extension(data, mime)
                digest = hashlib.sha256(data).hexdigest()
                path = directory / "assets" / (digest + "." + extension)
                if not path.exists():
                    atomic_bytes(path, data)
                asset.update(path=str(path.resolve()), sha256=digest, content_type=mime,
                             representation=representation, captured_from=evidence_id)
                replacements[f"@asset-{asset['index']}@"] = str(path.resolve())
            except Exception as error:
                original = recovery.get(asset["index"])
                if original:
                    asset.update({k: original[k] for k in ("path", "sha256", "content_type", "representation") if k in original})
                    asset["recovered_from"] = {"source_url": original.get("source_url"), "reason": "identical live and history solution with corresponding image position", "failure": str(error)}
                    replacements[f"@asset-{asset['index']}@"] = asset["path"]
                else:
                    asset["unavailable"] = str(error)
                    item.setdefault("errors", []).append("Image unavailable: " + identity)
            manifest[identity] = dict(asset)
        atomic_json(manifest_path, manifest)
        return replace_markers(item, replacements)
