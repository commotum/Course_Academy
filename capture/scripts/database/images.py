"""Store original image bytes once and localize content references."""
from __future__ import annotations
import base64
import copy
import hashlib
import io
import json
import re
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path
from ..storage import atomic_text

class MissingImage(ValueError):
    pass


def extension(data: bytes) -> str:
    """Identify content, never trust an HTTP suffix or rewrite image bytes."""
    from PIL import Image
    try:
        with Image.open(io.BytesIO(data)) as img:
            fmt = img.format
            img.verify()
        return {'PNG': 'png', 'JPEG': 'jpg', 'GIF': 'gif', 'WEBP': 'webp'}[fmt]
    except (OSError, KeyError, SyntaxError):
        try:
            root = ET.fromstring(data)
        except ET.ParseError as error:
            raise MissingImage('Image bytes are neither a supported raster nor SVG') from error
        if root.tag.rsplit('}', 1)[-1].lower() != 'svg':
            raise MissingImage('Downloaded response is not an image')
        return 'svg'


class ImageLibrary:
    def __init__(self, math_root: Path, capture_directory: Path):
        self.root = Path(math_root)
        self.capture = Path(capture_directory)
        self.mapping: dict[str, str] = {}
        self.saved: dict[str, dict] = {}
        for name in ('assets/manifest.json', 'asset-map.json', 'images.json'):
            path = self.capture / name
            if path.is_file():
                self._manifest(json.loads(path.read_text()))

    def _manifest(self, node):
        if isinstance(node, list):
            for item in node:
                self._manifest(item)
        elif isinstance(node, dict):
            local = next((node[k] for k in ('local_path', 'path', 'file', 'saved_path', 'relative_path')
                          if isinstance(node.get(k), str)), None)
            if local:
                for key in ('url', 'source_url', 'original_url', 'src'):
                    if isinstance(node.get(key), str):
                        self.mapping[node[key]] = local
            for key, value in node.items():
                if isinstance(value, str) and (key.startswith(('http:', 'https:', '/'))):
                    self.mapping[key] = value
                elif isinstance(value, (dict, list)):
                    if isinstance(value, dict) and key.startswith(('http:', 'https:', '/')):
                        self._manifest({'url': key, **value})
                    else:
                        self._manifest(value)

    def store(self, data: bytes, source: str) -> str:
        suffix = extension(data)
        digest = hashlib.sha256(data).hexdigest()
        relative = f'images/{digest[:2]}/{digest}.{suffix}'
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        # Publish only a fully fsynced file; a crash cannot leave partial bytes
        # at the canonical hash path. Hard-link publication is atomic and exclusive.
        import os
        import tempfile
        if target.exists():
            if target.read_bytes() != data:
                raise MissingImage('Existing image differs from its hash: ' + relative)
        else:
            fd, temporary = tempfile.mkstemp(prefix='.image-', dir=target.parent)
            try:
                with os.fdopen(fd, 'wb') as stream:
                    stream.write(data)
                    stream.flush()
                    os.fsync(stream.fileno())
                try:
                    os.link(temporary, target)
                except FileExistsError:
                    if target.read_bytes() != data:
                        raise MissingImage('Existing image differs from its hash: ' + relative)
                directory_fd = os.open(target.parent, os.O_RDONLY)
                try:
                    os.fsync(directory_fd)
                finally:
                    os.close(directory_fd)
            finally:
                Path(temporary).unlink(missing_ok=True)
        self.saved[source] = {'path': relative, 'sha256': digest, 'bytes': len(data)}
        return relative

    def resolve(self, source: str) -> str:
        source = source.strip().strip('<>')
        if source.startswith('data:'):
            header, payload = source.split(',', 1)
            data = base64.b64decode(payload, validate=True) if ';base64' in header else urllib.parse.unquote_to_bytes(payload)
            return self.store(data, source[:80])
        mapped = self.mapping.get(source, source)
        parsed = urllib.parse.urlsplit(mapped)
        if parsed.scheme in ('http', 'https'):
            # Remote retrieval is Activity Capture's responsibility using its account.
            raise MissingImage('No original local bytes for ' + source)
        raw = urllib.parse.unquote(parsed.path)
        candidates = [self.capture / raw, self.capture / 'assets' / raw]
        if raw.startswith('images/'):
            candidates.insert(0, self.root / raw)
        if Path(raw).is_absolute():
            candidates.insert(0, Path(raw))
        for path in candidates:
            if path.is_file():
                return self.store(path.read_bytes(), source)
        raise MissingImage('Image file is unavailable: ' + source)

    def text(self, value: str) -> str:
        # Keep exact original SVG strings, including case-sensitive attributes.
        value = re.sub(r'<svg\b[^>]*>.*?</svg\s*>',
                       lambda m: '![](' + self.store(m[0].encode(), 'inline-svg') + ')', value,
                       flags=re.S | re.I)
        value = re.sub(r'!\[([^\]]*)\]\(([^\s)]+)(?:\s+["\'][^)]*["\'])?\)',
                       lambda m: '![' + m[1] + '](' + self.resolve(m[2]) + ')', value)
        value = re.sub(r'(<img\b[^>]*?\bsrc\s*=\s*)(["\'])(.*?)\2',
                       lambda m: m[1] + m[2] + self.resolve(m[3]) + m[2], value, flags=re.I)
        return value

    def question(self, question: dict) -> dict:
        q = copy.deepcopy(question)
        for key in ('problem', 'worked_solution', 'local_problem'):
            if isinstance(q.get(key), str):
                q[key] = self.text(q[key])
        for field in q.get('answer_fields', q.get('fields', [])):
            old_correct = field.get('correct_value')
            for choice in field.get('choices', []):
                old = choice.get('value', '')
                if choice.get('type') == 'image':
                    new = self.text(old) if '<img' in old or '![' in old else self.resolve(old)
                else:
                    new = self.text(old)
                choice['value'] = new
                if old == old_correct:
                    field['correct_value'] = new
        return q
