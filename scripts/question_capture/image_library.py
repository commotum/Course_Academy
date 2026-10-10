"""Content-addressed Math Academy graphics; source evidence stays in captures.

Only image bytes are written below ``math_root/images``. All returned references
are relative to ``math_root``. Preparation raises ImagePreparationError rather
than leaving a missing, remote, or placeholder image in transactable content.
"""
from copy import deepcopy
import base64
import hashlib
from html.parser import HTMLParser
from functools import lru_cache
from io import BytesIO
import json
import os
from pathlib import Path
import re
import tempfile
from urllib.parse import unquote, unquote_to_bytes, urljoin, urlsplit
import xml.etree.ElementTree as ET

DEFAULT_MATH_ROOT = Path('/media/jake/SSD/EDB/math')
_CANONICAL = re.compile(r'images/([0-9a-f]{2})/([0-9a-f]{64})\.(png|jpg|gif|webp|svg)')
_MARKDOWN_IMAGE = re.compile(r'(!\[[^\]\n]*\]\()(?P<url><[^>]+>|[^\s)]+)(?P<title>\s+["\'][^\n]*?["\'])?(\))')
_CONTENT_KEYS = {'problem', 'worked_solution', 'content', 'context', 'description',
                 'shared_context', 'tutorial_content', 'instructions', 'title'}
_EVIDENCE_KEYS = {'assets', 'source_url', 'source_html', 'input_html', 'html',
                  'evidence', 'provenance', 'source_evidence', 'locator'}
_MIMES = {'png':'image/png', 'jpg':'image/jpeg', 'gif':'image/gif',
          'webp':'image/webp', 'svg':'image/svg+xml'}


class ImagePreparationError(ValueError):
    """An image needs source recovery before this content can be transacted."""


def _svg_root(data):
    if re.search(br'<!DOCTYPE|<!ENTITY', data, re.I):
        raise ImagePreparationError('SVG declarations are unsupported')
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise ImagePreparationError('Invalid SVG: ' + str(exc)) from exc
    if root.tag.split('}')[-1] != 'svg':
        raise ImagePreparationError('Image is not an SVG')
    ids = {node.attrib['id'] for node in root.iter() if 'id' in node.attrib}
    refs = set()
    for node in root.iter():
        if node.tag.split('}')[-1] in ('script', 'foreignObject'):
            raise ImagePreparationError('Unsupported active SVG content')
        for name, value in node.attrib.items():
            if name.lower().startswith('on'):
                raise ImagePreparationError('Unsupported SVG event handler')
            if name.split('}')[-1] == 'href':
                if value.startswith('#'):
                    refs.add(value[1:])
                elif not value.startswith('data:image/'):
                    raise ImagePreparationError('SVG has an unresolved external image/reference: ' + value)
            for target in re.findall(r'url\(\s*[\"\']?([^\s)\"\']+)', value):
                if not target.startswith('#'):
                    raise ImagePreparationError('SVG has an external URL: ' + target)
                refs.add(target[1:])
    if refs - ids:
        raise ImagePreparationError('SVG references missing definitions: ' + ', '.join(sorted(refs - ids)))
    return root


def image_format(data, content_type=None):
    """Validate complete image bytes without recompressing them."""
    if not isinstance(data, bytes) or not data:
        raise ImagePreparationError('Image response is empty or is not bytes')
    stripped = data.lstrip(b'\xef\xbb\xbf \t\r\n')
    if stripped.startswith((b'<svg', b'<?xml', b'<!--')):
        _svg_root(data)
        extension = 'svg'
    else:
        from PIL import Image, UnidentifiedImageError
        try:
            with Image.open(BytesIO(data)) as original:
                extension = {'PNG':'png', 'JPEG':'jpg', 'GIF':'gif', 'WEBP':'webp'}.get(original.format)
                if extension is None:
                    raise ImagePreparationError('Unsupported raster format: ' + str(original.format))
                original.verify()
            with Image.open(BytesIO(data)) as original:
                original.load()
        except (UnidentifiedImageError, OSError, SyntaxError, ValueError) as exc:
            raise ImagePreparationError('Invalid image bytes: ' + str(exc)) from exc
    mime = (content_type or '').split(';', 1)[0].lower().strip()
    if mime and mime not in (_MIMES[extension], 'application/octet-stream', 'binary/octet-stream'):
        raise ImagePreparationError('Image MIME type disagrees with bytes: ' + mime)
    return extension


class ImageLibrary:
    def __init__(self, math_root=DEFAULT_MATH_ROOT):
        self.math_root = Path(math_root).resolve()
        self.root = self.math_root / 'images'
        self._files = {}

    def put_bytes(self, data, *, content_type=None):
        extension = image_format(data, content_type)
        digest = hashlib.sha256(data).hexdigest()
        relative = f'images/{digest[:2]}/{digest}.{extension}'
        target = self.math_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        # Publish one complete file atomically. Multiple capture workers can race
        # safely: link() never overwrites a winner, and their bytes must agree.
        if target.exists():
            if target.is_symlink() or target.read_bytes() != data:
                raise ImagePreparationError('Existing hash image has different bytes: ' + str(target))
            return relative
        descriptor, temporary = tempfile.mkstemp(prefix='.image-', dir=target.parent)
        try:
            with os.fdopen(descriptor, 'wb') as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            try:
                os.link(temporary, target)
            except FileExistsError:
                if target.is_symlink() or target.read_bytes() != data:
                    raise ImagePreparationError('Concurrent hash image has different bytes: ' + str(target))
        finally:
            Path(temporary).unlink(missing_ok=True)
        return relative

    def put_file(self, path, *, expected_sha256=None, content_type=None):
        path = Path(path).resolve()
        if not path.is_file():
            raise ImagePreparationError('Missing captured image: ' + str(path))
        stat = path.stat()
        stamp = (str(path), stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns, expected_sha256, content_type)
        if stamp in self._files:
            relative, target_stamp = self._files[stamp]
            target = self.math_root / relative
            if target.is_file() and not target.is_symlink():
                current = target.stat()
                if (current.st_size, current.st_mtime_ns, current.st_ctime_ns) == target_stamp:
                    return relative
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if expected_sha256 and digest != expected_sha256:
            raise ImagePreparationError('Captured image SHA256 mismatch: ' + str(path))
        relative = self.put_bytes(data, content_type=content_type)
        written = (self.math_root / relative).stat()
        self._files[stamp] = (relative, (written.st_size, written.st_mtime_ns, written.st_ctime_ns))
        return relative

    def reference(self, value, *, capture_dir=None, aliases=None):
        if not isinstance(value, str) or not value:
            raise ImagePreparationError('Image reference is empty')
        value = value.strip().removeprefix('<').removesuffix('>')
        aliases = aliases or {}
        if value in aliases:
            metadata = aliases[value]
            if isinstance(metadata, str):
                value = metadata
            else:
                return self.put_file(metadata['path'], expected_sha256=metadata.get('sha256'),
                                     content_type=metadata.get('content_type'))
        if value.startswith('data:'):
            try:
                header, encoded = value.split(',', 1)
                data = base64.b64decode(encoded, validate=True) if header.endswith(';base64') else unquote_to_bytes(encoded)
                return self.put_bytes(data, content_type=header[5:].split(';')[0])
            except (ValueError, TypeError) as exc:
                raise ImagePreparationError('Invalid image data URL') from exc
        if value.startswith('@asset-'):
            raise ImagePreparationError('Unresolved captured image placeholder: ' + value)
        parsed = urlsplit(value)
        if parsed.scheme in ('http', 'https') or value.startswith('//'):
            raise ImagePreparationError('Image was not downloaded: ' + value)
        if parsed.scheme and parsed.scheme != 'file':
            raise ImagePreparationError('Unsupported image URL: ' + value)
        if parsed.query or parsed.fragment:
            raise ImagePreparationError('Unresolved image URL: ' + value)
        path = Path(unquote(parsed.path))
        expected = None
        if value.startswith('images/'):
            match = _CANONICAL.fullmatch(value)
            if not match or match[1] != match[2][:2]:
                raise ImagePreparationError('Malformed library image reference: ' + value)
            path = self.math_root / value
            expected = match[2]
        elif not path.is_absolute():
            if capture_dir is None:
                raise ImagePreparationError('Relative image lacks a capture directory: ' + value)
            path = Path(capture_dir) / path
        relative = self.put_file(path, expected_sha256=expected)
        if expected and relative != value:
            raise ImagePreparationError('Library extension disagrees with image bytes: ' + value)
        return relative

    def prepare_content(self, payload, capture_dir=None):
        """Return a copy with content image references normalized; keep evidence intact."""
        aliases = {}
        capture_dir = Path(capture_dir) if capture_dir is not None else None
        manifest = capture_dir / 'assets/manifest.json' if capture_dir else None
        if manifest and manifest.is_file():
            for key, item in json.loads(manifest.read_text()).items():
                if isinstance(item, dict) and item.get('path'):
                    aliases[key] = item
                    aliases[item['path']] = item
        def gather(value):
            if isinstance(value, dict):
                for item in value.get('assets', []):
                    if isinstance(item, dict) and item.get('path'):
                        aliases[item['path']] = item
                        if item.get('source_url'):
                            aliases[item['source_url']] = item
                for item in value.values():
                    gather(item)
            elif isinstance(value, list):
                for item in value:
                    gather(item)
        gather(payload)
        def reference(value):
            return self.reference(value, capture_dir=capture_dir, aliases=aliases)
        def content_text(value):
            if '@asset-' in value:
                raise ImagePreparationError('Content still has an unresolved image placeholder')
            if len(re.findall(r'!\[[^\]\n]*\]\(', value)) != len(list(_MARKDOWN_IMAGE.finditer(value))):
                raise ImagePreparationError('Malformed Markdown image reference')
            value = _MARKDOWN_IMAGE.sub(lambda m: m[1] + reference(m['url']) + (m['title'] or '') + ')', value)
            if re.search(r'<(?:img|svg|canvas)\b', value, re.I):
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(value, 'html.parser')
                if soup.find(['svg', 'canvas']):
                    raise ImagePreparationError('Content contains an unprepared SVG or canvas')
                for img in soup.find_all('img'):
                    img['src'] = reference(img.get('src', ''))
                    img.attrs.pop('srcset', None)
                value = str(soup)
            # Reference-style images need the converter to resolve definitions.
            if re.search(r'!\[[^\]]*\]\[', value):
                raise ImagePreparationError('Unresolved reference-style Markdown image')
            return value
        def visit(value, key=None, parent=None):
            if isinstance(value, dict):
                return {k: deepcopy(v) if k in _EVIDENCE_KEYS else visit(v, k, value)
                        for k, v in value.items()}
            if isinstance(value, list):
                return [visit(v, key, parent) for v in value]
            if not isinstance(value, str):
                return value
            if key in ('value', 'correct_value') and parent:
                image_type = parent.get('type') == 'image' or parent.get('value_type') == 'image'
                image_type |= key == 'correct_value' and any(c.get('type') == 'image' and c.get('value') == value
                                                            for c in parent.get('choices', []))
                if image_type:
                    return reference(value)
            if key in _CONTENT_KEYS or key in ('value', 'correct_value'):
                return content_text(value)
            return value
        return visit(payload)


class _SVGSpans(HTMLParser):
    """Locate original SVG source without lowercasing viewBox or path attributes."""
    def __init__(self, html):
        super().__init__(convert_charrefs=False)
        self.html, self.spans, self.depth = html, [], 0
        self.lines = [0]
        self.lines.extend(m.end() for m in re.finditer('\n', html))
        self.feed(html)
        if self.depth:
            raise ImagePreparationError('Unclosed inline SVG')

    def source_offset(self):
        row, column = self.getpos()
        return self.lines[row - 1] + column

    def handle_starttag(self, tag, attrs):
        if tag == 'svg':
            if not self.depth:
                self.start = self.source_offset()
            self.depth += 1

    def handle_startendtag(self, tag, attrs):
        if tag == 'svg' and not self.depth:
            start = self.source_offset()
            self.spans.append((start, start + len(self.get_starttag_text())))

    def handle_endtag(self, tag):
        if tag == 'svg' and self.depth:
            self.depth -= 1
            if not self.depth:
                end = self.html.index('>', self.source_offset()) + 1
                self.spans.append((self.start, end))


def _xml_svg(text):
    # Browser outerHTML need not include declarations inherited from the page.
    opener = re.match(r'<svg\b[^>]*>', text, re.I)
    if not opener:
        raise ImagePreparationError('Invalid inline SVG')
    declarations = ''
    if not re.search(r'\bxmlns\s*=', opener[0]):
        declarations += ' xmlns="http://www.w3.org/2000/svg"'
    if 'xlink:' in text and 'xmlns:xlink' not in opener[0]:
        declarations += ' xmlns:xlink="http://www.w3.org/1999/xlink"'
    insert = opener.end() - (2 if opener[0].endswith('/>') else 1)
    return text[:insert] + declarations + text[insert:]


@lru_cache(maxsize=2)
def _svg_definitions(document_html):
    definitions = {}
    for start, end in _SVGSpans(document_html).spans:
        try:
            other = ET.fromstring(_xml_svg(document_html[start:end]))
        except ET.ParseError:
            continue
        for node in other.iter():
            if node.get('id'):
                definitions.setdefault(node.get('id'), node)
    return definitions


def standalone_svg(svg_html, document_html=''):
    """Retain the original inline SVG and include any referenced shared definitions."""
    text = _xml_svg(svg_html)
    try:
        root = ET.fromstring(text)
        definitions = _svg_definitions(document_html)
        known = {node.get('id') for node in root.iter() if node.get('id')}
        added = []
        pending = [root]
        while pending:
            node = pending.pop()
            for child in node.iter():
                references = set()
                for key, value in child.attrib.items():
                    if key.split('}')[-1] == 'href' and value.startswith('#'):
                        references.add(value[1:])
                    references.update(re.findall(r'url\(\s*[\"\']?#([^\s)\"\']+)', value))
                for identity in references - known:
                    if identity not in definitions:
                        raise ImagePreparationError('Inline SVG is missing definition: ' + identity)
                    definition = definitions[identity]
                    known.update(n.get('id') for n in definition.iter() if n.get('id'))
                    added.append(ET.tostring(definition, encoding='unicode'))
                    pending.append(definition)
        if added:
            end = text.index('>') + 1
            text = text[:end] + '<defs>' + ''.join(added) + '</defs>' + text[end:]
        data = text.encode('utf-8')
        _svg_root(data)
        return data
    except ET.ParseError as exc:
        raise ImagePreparationError('Invalid inline SVG: ' + str(exc)) from exc


def capture_html_images(html, *, page_url, fetch_response, library,
                        evidence_dir=None, document_html=None):
    """Prepare observed HTML images using the caller's authenticated response reader.

    ``fetch_response(url)`` returns ``(bytes, content_type)``. The caller can reuse
    observed browser responses or perform an authenticated GET. It is invoked
    only for image URLs present in this HTML. Original downloaded bytes can also
    be preserved under ``evidence_dir/assets``. Return HTML with library paths.
    """
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    spans = _SVGSpans(html).spans
    svgs = [node for node in soup.find_all('svg') if node.find_parent('svg') is None]
    if len(spans) != len(svgs):
        raise ImagePreparationError('Cannot match inline SVG source nodes')
    replacements = []
    for (start, end), node in zip(spans, svgs):
        math_parent = node.find_parent(lambda n: n.name == 'mjx-container' or
                                      any(c in ('MathJax', 'mjpage') for c in n.get('class', [])))
        if math_parent and (math_parent.find('math') or node.find('title')):
            continue  # The Markdown converter can retain the actual formula.
        if not node.find(['path', 'use', 'text', 'line', 'polyline', 'polygon', 'circle', 'ellipse', 'rect', 'image'], recursive=False) and all(
                n.name in ('defs', 'title', 'desc', 'style') for n in node.find_all(recursive=False)):
            replacements.append((start, end, ''))
            continue
        data = standalone_svg(html[start:end], document_html or html)
        relative = library.put_bytes(data, content_type='image/svg+xml')
        if evidence_dir is not None:
            _save_evidence(evidence_dir, relative, data)
        replacements.append((start, end, '<img src="' + relative + '" alt=""/>'))
    for start, end, replacement in reversed(replacements):
        html = html[:start] + replacement + html[end:]
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find('canvas'):
        raise ImagePreparationError('Canvas requires a rendered capture before tutorial preparation')
    for node in soup.find_all('img'):
        source = node.get('src', '')
        if not source:
            raise ImagePreparationError('HTML image is missing src')
        if _CANONICAL.fullmatch(source):
            relative = library.reference(source)
        elif source.startswith('data:'):
            relative = library.reference(source)
        else:
            url = urljoin(page_url, source)
            if urlsplit(url).scheme not in ('http', 'https'):
                raise ImagePreparationError('Unsupported captured image URL: ' + url)
            # Preserve the caller's network/access exceptions so its existing
            # rate-limit and blocked-account handling remains in control.
            data, mime = fetch_response(url)
            relative = library.put_bytes(data, content_type=mime)
            if evidence_dir is not None:
                _save_evidence(evidence_dir, relative, data)
        node['src'] = relative
        node.attrs.pop('srcset', None)
    return str(soup)


def _save_evidence(directory, relative, data):
    target = Path(directory) / 'assets' / Path(relative).name
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.read_bytes() != data:
        raise ImagePreparationError('Captured image evidence differs: ' + str(target))
    if not target.exists():
        target.write_bytes(data)
