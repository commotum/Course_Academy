"""Keep original source image bytes and a recoverable evidence manifest."""
from __future__ import annotations

import base64
import hashlib
import re
import time
from types import SimpleNamespace
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote_to_bytes

from ..storage import atomic_bytes, atomic_json, read_json
from ..runtime import StopRequested, check_stop, wait


# Snapshot every graphic in one read so a page with many diagrams pays one
# settling interval. A valid canvas PNG alone does not establish that it drew.
GRAPHIC_STATE = r'''(root, assets) => assets.map(asset => {
  const n = root.querySelectorAll(asset.tag)[asset.dom_index || 0];
  if (!n) return {index:asset.index, ready:false, reason:'Graphic detached'};
  const box = n.getBoundingClientRect();
  const visible = !!n.getClientRects().length && box.width > 0 && box.height > 0 &&
    getComputedStyle(n).visibility !== 'hidden';
  let ready = visible, signature = n.outerHTML, encoded = null, broken = false;
  if (asset.tag === 'img') {
    broken = n.complete && !n.naturalWidth;
    ready = ready && n.complete && n.naturalWidth > 0;
    signature = [n.currentSrc || n.src, n.naturalWidth, n.naturalHeight].join('|');
  } else if (asset.tag === 'canvas') {
    try {
      encoded = n.toDataURL('image/png');
      const blank = document.createElement('canvas');
      blank.width = n.width; blank.height = n.height;
      ready = ready && n.width > 0 && n.height > 0 && encoded !== blank.toDataURL('image/png');
      signature = encoded;
    } catch (error) { return {index:asset.index,ready:false,reason:String(error)}; }
  } else {
    ready = ready && !!n.querySelector('path,use,text,line,polyline,polygon,circle,ellipse,rect,image,foreignObject');
  }
  return {index:asset.index, ready, broken, signature, encoded, html:n.outerHTML,
    reason:!visible ? 'Graphic is not visible' : broken ? 'Image did not load' : 'Graphic has not finished rendering'};
})'''


class ImageFetchError(ValueError):
    def __init__(self, status, source):
        super().__init__("Image HTTP " + str(status) + ": " + source)
        self.retryable = status in (408, 425, 429) or status >= 500


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

    def _check_stop(self):
        if getattr(self.browser, "stop_event", None) is not None:
            check_stop(self.browser.stop_event)

    def _sleep(self, seconds):
        self._check_stop()
        deadline = getattr(self.browser, "deadline_at", None)
        if deadline is not None:
            seconds = min(seconds, max(0, deadline - time.time()))
        if getattr(self.browser, "pacer", None) is not None:
            self.browser.pacer.sleep(seconds, deadline=deadline)
        elif getattr(self.browser, "stop_event", None) is not None:
            wait(self.browser.stop_event, seconds)
        else:
            time.sleep(seconds)

    def _timeout_ms(self, maximum=None):
        timeout = self.browser.timeout_ms() if hasattr(self.browser, "timeout_ms") else getattr(
            getattr(self.browser, "config", None), "timeout_ms", 10000)
        if maximum is not None:
            timeout = min(timeout, maximum)
        deadline = getattr(self.browser, "deadline_at", None)
        if deadline is not None:
            timeout = min(timeout, max(1, (deadline - time.time()) * 1000))
        return max(1, int(timeout))

    def _rendered_assets(self, item, scope):
        assets = item.get("assets", [])
        if scope is None or not assets:
            return {}
        config = getattr(self.browser, "config", None)
        timeout = min(float(getattr(config, "timeout_ms", 10000)) / 1000, 10.0)
        minimum = max(.5, float(getattr(config, "ui_delay_ms", 500)) / 1000)
        deadline = time.monotonic() + timeout
        stable, completed, last, reloaded = {}, {}, {}, set()
        while True:
            self._check_stop()
            absolute = getattr(self.browser, "deadline_at", None)
            if time.monotonic() >= deadline or absolute is not None and time.time() >= absolute:
                break
            try:
                snapshots = scope.evaluate(GRAPHIC_STATE, assets,
                                           timeout=self._timeout_ms((deadline - time.monotonic()) * 1000))
            except StopRequested:
                raise
            except Exception as error:
                return {a["index"]: {"error": str(error)} for a in assets}
            now = time.monotonic()
            for state in snapshots:
                index = state["index"]
                # Recheck earlier graphics too: a late update must reset stability.
                previous = last.get(index, {})
                if state.get("ready") and state.get("signature") == previous.get("signature"):
                    if now - stable.setdefault(index, now) >= minimum:
                        completed[index] = state
                else:
                    stable[index] = now
                    completed.pop(index, None)
                last[index] = state
                if state.get("broken") and index not in reloaded:
                    # The old engine retried one completed-but-broken DOM image.
                    # Keep its source unchanged and use the shared cooldown first.
                    reloaded.add(index)
                    self._sleep(minimum)
                    if hasattr(self.browser, "_wait_cooldown"):
                        self.browser._wait_cooldown()
                    self._check_stop()
                    if time.monotonic() >= deadline or absolute is not None and time.time() >= absolute:
                        break
                    asset = next(a for a in assets if a["index"] == index)
                    try:
                        scope.locator("img").nth(asset.get("dom_index", 0)).evaluate("n => { n.src = n.src; }",
                            timeout=self._timeout_ms((deadline - time.monotonic()) * 1000))
                    except StopRequested:
                        raise
                    except Exception as error:
                        state["reason"] = str(error)
            if len(completed) == len(assets) or now >= deadline:
                break
            self._sleep(min(.1, max(0, deadline - now)))
        return {a["index"]: completed.get(a["index"], {
            "error": last.get(a["index"], {}).get("reason", "Graphic readiness deadline expired")}) for a in assets}

    @staticmethod
    def _cached(record, directory):
        """A URL match alone is insufficient: the stored original must still hash."""
        if not record or record.get("representation") != "original" or not record.get("path") or not record.get("sha256"):
            return None
        path = Path(record["path"])
        if not path.is_absolute():
            path = Path(directory) / path
        try:
            data = path.read_bytes()
            if hashlib.sha256(data).hexdigest() != record["sha256"]:
                return None
            image_extension(data, record.get("content_type", ""))
            return data, record.get("content_type", "")
        except (OSError, ValueError):
            return None

    def _fetch(self, source, cached=None):
        self._check_stop()
        if source.startswith("data:"):
            header, encoded = source.split(",", 1)
            return (base64.b64decode(encoded) if ";base64" in header else unquote_to_bytes(encoded), header[5:].split(";")[0])
        response = getattr(self.browser, "image_responses", {}).get(source)
        if response is not None:
            try:
                return response.body(), response.headers.get("content-type", "")
            except StopRequested:
                raise
            except Exception:
                pass  # An old Playwright response may have been discarded after navigation.
        if cached is not None:
            return cached
        for attempt in range(2):
            self._check_stop()
            if hasattr(self.browser, "_wait_cooldown"):
                self.browser._wait_cooldown()
            try:
                response = self.browser.context.request.get(source, timeout=self._timeout_ms())
                if getattr(self.browser, "safety", None) is not None:
                    self.browser.safety.response(SimpleNamespace(status=response.status, headers=response.headers,
                        url=getattr(response, "url", source), request=SimpleNamespace(resource_type="image")))
                if not response.ok:
                    raise ImageFetchError(response.status, source)
                return response.body(), response.headers.get("content-type", "")
            except StopRequested:
                raise
            except Exception as error:
                if attempt or isinstance(error, ImageFetchError) and not error.retryable:
                    raise
                self._sleep(max(.5, float(getattr(self.browser.config, "retry_delay", 2))))

    def collect(self, item, scope, directory, evidence_id, prior=None):
        directory = Path(directory)
        manifest_path = directory / "assets" / "manifest.json"
        manifest = read_json(manifest_path, {}) or {}
        replacements = {}
        recovery = solution_image_bindings(item, prior)
        rendered = self._rendered_assets(item, scope)
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
            self._check_stop()
            identity = asset.get("source_url") or evidence_id + ":" + str(asset["index"])
            try:
                source = asset.get("source_url")
                representation = "original"
                state = rendered.get(asset["index"], {})
                if state.get("error"):
                    # Downloading original bytes remains useful even when the DOM
                    # image fails. Keep that failure distinct from missing bytes.
                    asset["render_unavailable"] = state["error"]
                    item.setdefault("errors", []).append("Graphic rendering unavailable: " + identity)
                elif state:
                    asset.pop("render_unavailable", None)
                    asset["render_ready"] = True
                if asset["tag"] == "svg":
                    source_html = state.get("html", asset["html"])
                    if source_html != asset["html"]:
                        asset["observed_html"] = source_html
                    original = source_html.encode("utf-8")
                    data, definitions = standalone_svg(source_html, getattr(self.browser, "page", None))
                    mime = "image/svg+xml"
                    if data != original:
                        representation = "standalone_svg"
                        asset["source_sha256"] = hashlib.sha256(original).hexdigest()
                        original_path = directory / "assets" / (asset["source_sha256"] + ".svg")
                        atomic_bytes(original_path, original)
                        asset["original_svg_path"] = str(original_path.resolve())
                        asset["original_svg_sha256"] = asset["source_sha256"]
                        asset["standalone_definitions"] = definitions
                elif asset["tag"] == "canvas":
                    if state.get("error"):
                        raise ValueError(state["error"])
                    encoded = state.get("encoded")
                    if not encoded:
                        node = scope.locator("canvas").nth(asset.get("dom_index", 0))
                        encoded = node.evaluate("n => n.toDataURL('image/png')", timeout=self._timeout_ms())
                    data, mime = base64.b64decode(encoded.split(",", 1)[1]), "image/png"
                    representation = "canvas_render"
                elif source:
                    data, mime = self._fetch(source, self._cached(manifest.get(identity), directory))
                else:
                    raise ValueError("Source image has no URL")
                extension = image_extension(data, mime)
                digest = hashlib.sha256(data).hexdigest()
                path = directory / "assets" / (digest + "." + extension)
                if not path.exists():
                    atomic_bytes(path, data)
                asset.update(path=str(path.resolve()), sha256=digest, content_type=mime,
                             representation=representation, captured_from=evidence_id)
                asset.pop("unavailable", None)
                replacements[f"@asset-{asset['index']}@"] = str(path.resolve())
            except StopRequested:
                raise
            except Exception as error:
                original = recovery.get(asset["index"])
                if original:
                    asset.update({k: original[k] for k in ("path", "sha256", "content_type", "representation") if k in original})
                    asset["recovered_from"] = {"source_url": original.get("source_url"), "reason": "identical live and history solution with corresponding image position", "failure": str(error)}
                    replacements[f"@asset-{asset['index']}@"] = asset["path"]
                else:
                    asset["unavailable"] = str(error)
                    item.setdefault("errors", []).append("Image unavailable: " + identity)
            # A failed later rendering must not erase the verified source bytes
            # needed to recover after a browser restart.
            if asset.get("unavailable") and self._cached(manifest.get(identity), directory):
                manifest[evidence_id + ":" + str(asset["index"])] = dict(asset)
            else:
                manifest[identity] = dict(asset)
        atomic_json(manifest_path, manifest)
        return replace_markers(item, replacements)
