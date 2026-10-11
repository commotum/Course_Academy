"""Keep original source image bytes and a recoverable evidence manifest."""
from __future__ import annotations

import base64
import hashlib
import re
import xml.etree.ElementTree as ET
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


def standalone_svg(source, page=None):
    """Include only shared definitions referenced by the observed inline SVG."""
    opener = re.match(r'<svg\b[^>]*>', source, re.I)
    if not opener:
        raise ValueError("Invalid inline SVG")
    declarations = ''
    if not re.search(r'\bxmlns\s*=', opener[0]):
        declarations += ' xmlns="http://www.w3.org/2000/svg"'
    if 'xlink:' in source and 'xmlns:xlink' not in opener[0]:
        declarations += ' xmlns:xlink="http://www.w3.org/1999/xlink"'
    index = opener.end() - (2 if opener[0].endswith('/>') else 1)
    text = source[:index] + declarations + source[index:]
    root = ET.fromstring(text)
    known = {node.get('id') for node in root.iter() if node.get('id')}
    pending, added = [root], []
    while pending:
        node = pending.pop()
        references = set()
        for child in node.iter():
            for key, value in child.attrib.items():
                if key.rsplit('}', 1)[-1] == 'href' and value.startswith('#'):
                    references.add(value[1:])
                references.update(re.findall(r'url\(\s*["\']?#([^\s)"\']+)', value))
            if child.tag.rsplit('}', 1)[-1] == 'style':
                references.update(re.findall(r'url\(\s*["\']?#([^\s)"\']+)', child.text or ''))
        missing = sorted(references - known)
        if not missing:
            continue
        definitions = page.evaluate("ids => Object.fromEntries(ids.map(id => [id,document.getElementById(id)?.outerHTML || null]))", missing) if page else {}
        for identity in missing:
            if identity in known:
                continue
            html = definitions.get(identity)
            if not html:
                raise ValueError("Inline SVG is missing source definition: " + identity)
            wrapped = ET.fromstring('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">' + html + '</svg>')
            definition = wrapped[0]
            known.update(child.get('id') for child in definition.iter() if child.get('id'))
            added.append({'id': identity, 'html': html})
            pending.append(definition)
    if added:
        index = text.index('>') + 1
        text = text[:index] + '<defs>' + ''.join(item['html'] for item in added) + '</defs>' + text[index:]
    # A shared definition can introduce xlink even when the source root did not.
    if 'xlink:' in text and 'xmlns:xlink' not in text[:text.index('>')]:
        index = text.index('>')
        text = text[:index] + ' xmlns:xlink="http://www.w3.org/1999/xlink"' + text[index:]
    return text.encode('utf-8'), added


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
                    original = asset["html"].encode("utf-8")
                    data, definitions = standalone_svg(asset["html"], getattr(self.browser, "page", None))
                    mime = "image/svg+xml"
                    if data != original:
                        representation = "standalone_svg"
                        asset["source_sha256"] = hashlib.sha256(original).hexdigest()
                        asset["standalone_definitions"] = definitions
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
