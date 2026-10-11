"""Browser timing, original document preservation, and account-level throttling."""
from __future__ import annotations

from datetime import timezone
from email.utils import parsedate_to_datetime
import hashlib
import math
import re
import time
from urllib.parse import urlparse

from ..storage import append_event, atomic_bytes, atomic_json, read_json


def retry_after_seconds(value, now=None, default=30):
    now = time.time() if now is None else now
    try:
        numeric = float(value)
        return max(0.0, numeric) if math.isfinite(numeric) else float(default)
    except (TypeError, ValueError):
        try:
            stamp = parsedate_to_datetime(value)
            if stamp.tzinfo is None:
                stamp = stamp.replace(tzinfo=timezone.utc)
            return max(0.0, stamp.timestamp() - now)
        except (TypeError, ValueError, OverflowError):
            return float(default)


def deduplicate_math_editor(html):
    """Remove only exactly identical repeated editor tags, preserving other HTML."""
    seen = set()
    def first(match):
        tag = match[0]
        if tag in seen:
            return ''
        seen.add(tag)
        return tag
    return re.sub(r'''<script\b(?=[^>]*\bsrc=["']/js/math-editor\.js(?:\?[^"']*)?["'])[^>]*>\s*</script\s*>''',
                  first, html, flags=re.I)


def academy_url(url):
    host = urlparse(url).hostname or ''
    return host == 'mathacademy.com' or host.endswith('.mathacademy.com')


class BrowserSafety:
    def __init__(self, browser):
        self.browser = browser
        self.cooldown_until = 0
        self.reconcile_required = False
        self.events = []
        self.original_documents = {}
        root = getattr(browser.config, 'state_root', None)
        self.cooldown_path = root / 'browser-cooldown.json' if root else None
        if self.cooldown_path:
            self.cooldown_until = (read_json(self.cooldown_path, {}) or {}).get('until', 0)

    def event(self, kind, **details):
        entry = {'kind': kind, 'at': time.time(), **details}
        self.events.append(entry)
        self.events = self.events[-100:]
        root = getattr(self.browser.config, 'output_root', None)
        directory = self.browser.directory or root
        if directory:
            append_event(directory / 'browser-events.jsonl', kind, **details)

    def response(self, response):
        if not academy_url(response.url):
            return
        if response.status >= 400:
            self.event('http_error', url=response.url, status=response.status,
                       resource_type=response.request.resource_type)
        if response.status == 429:
            headers = response.headers
            delay = retry_after_seconds(headers.get('retry-after'), default=getattr(self.browser.config, 'retry_delay', 30))
            self.cooldown_until = max(self.cooldown_until, time.time() + delay)
            self.reconcile_required = True
            if self.cooldown_path:
                atomic_json(self.cooldown_path, {'until': self.cooldown_until, 'url': response.url,
                                                'retry_after': headers.get('retry-after')})
            self.event('rate_limit', until=self.cooldown_until, delay=delay, url=response.url)

    def remaining_cooldown(self):
        if self.cooldown_path:
            saved = read_json(self.cooldown_path, {}) or {}
            self.cooldown_until = max(self.cooldown_until, saved.get('until', 0))
        return max(0.0, self.cooldown_until - time.time())

    def repair_document(self, route):
        """Read-only interception; always finish the route, including failures."""
        try:
            request = route.request
            if request.resource_type != 'document' or request.method != 'GET' or not academy_url(request.url):
                return route.continue_()
            response = route.fetch(max_redirects=0, timeout=self.browser.timeout_ms())
            if response.status == 429:
                # APIResponse lacks request; supply the actual intercepted request.
                from types import SimpleNamespace
                self.response(SimpleNamespace(url=request.url, status=response.status, headers=response.headers, request=request))
            if response.status in (301, 302, 303, 307, 308) or 'text/html' not in response.headers.get('content-type', '').lower():
                return route.fulfill(response=response)
            original = response.body()
            # Decode for the narrowly scoped compatibility repair only. The
            # original response bytes, including source errors, stay untouched.
            try:
                html = original.decode('utf-8')
            except UnicodeDecodeError:
                return route.fulfill(response=response)
            cleaned = deduplicate_math_editor(html)
            if cleaned != html:
                root = getattr(self.browser.config, 'output_root', None) or self.browser.directory
                if root is None:
                    return route.fulfill(response=response)  # Never repair without preserving source.
                digest = hashlib.sha256(original).hexdigest()
                target = root / 'browser-originals' / (digest + '.html')
                atomic_bytes(target, original)
                record = {'url': request.url, 'captured_at': time.time(), 'source_sha256': digest,
                          'source_file': str(target.resolve()), 'transformation': 'remove_identical_duplicate_math_editor_script_tags',
                          'rendered_sha256': hashlib.sha256(cleaned.encode()).hexdigest()}
                atomic_json(target.with_suffix('.json'), record)
                self.original_documents[request.url] = record
                self.event('document_repair', **record)
                return route.fulfill(response=response, body=cleaned)
            return route.fulfill(response=response)
        except Exception as error:
            # Playwright errors can contain request headers; retain the error
            # class and network code rather than logging authentication headers.
            code = re.search(r'net::ERR_[A-Z_]+|\b(?:EAI_AGAIN|ENOTFOUND|ECONNRESET|ETIMEDOUT)\b', str(error))
            self.event('document_request_failed', reason=code[0] if code else type(error).__name__)
            try:
                route.abort('failed')
            except Exception:
                pass
