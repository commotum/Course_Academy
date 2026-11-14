#!/usr/bin/env python3
"""Read-only census and extraction of original capture math presentations.

Only original HTML (including JSON-embedded HTML) is evidence. Normalized
problem/solution strings are never read as source. The scanner preserves exact
MathML style scopes and authored mspace widths, and reconstructs hybrid legacy
SVG titles without flattening nested MathJax. It writes no database facts.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
import time

from bs4 import BeautifulSoup, NavigableString, Tag
from import_historical_question_content import Renderer
from question_capture.math_format import normalize_source_tex

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / 'reference/edb-math/audits/2026-11-13-source-math-style-loss'
SOURCE_ROOTS = ['capture', 'question-capture', 'question-capture-workers',
                'diagnostic-capture', 'review-13925710', 'sum-rule-13925458',
                'factorials-13831129', 'multistep-13931219', 'assessment-13930620',
                'progress-history-2026-10-04']
EXCLUDED_PARTS = {'solver', 'edb-import', 'database', 'normalized', 'repairs',
                  'capture-repair', 'repair-staging', 'queue', 'knowledge-state'}
STYLE = re.compile(r'mathvariant|mathcolor|mathbackground|<mspace\b|\\(?:math(?:bf|bb|cal|frak|sf|tt|it|rm|bfit)|boldsymbol|color|textcolor|bbox|quad|qquad|hspace|kern|mkern|checkmark)\b', re.I)
STYLE_BYTES = re.compile(STYLE.pattern.encode(), re.I)
HTML_VALUE = re.compile(r'<(?:div|span|math|mjx-container|svg|body|html|p|table)\b', re.I)
STRIP = re.compile(r'<(script|style)\b[^>]*>[\s\S]*?</\1\s*>', re.I)
TOKENS = re.compile(r'<math\b[^>]*>[\s\S]*?</math\s*>|<svg\b[^>]*>[\s\S]*?</svg\s*>|</?(?:div|span|p|li|td|section|article|body)\b[^>]*>|\$\$[\s\S]*?\$\$|(?<![\\$])\$(?!\$)(?:\\.|[^$])*?\$(?!\$)|\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)', re.I)
ATTR = re.compile(r'([\w:-]+)\s*=\s*(?:"([^"]*)"|\x27([^\x27]*)\x27|([^\s>]+))')
TITLE = re.compile(r'<title\b[^>]*>([\s\S]*?)</title\s*>', re.I)
IDENTITY = re.compile(r'(?:^|[^\w])(?:step-)?([qet])-?(\d+)(?:$|[^\d])')
QUESTION_ID = re.compile(r'^(?:question|questionExplanation|questionText|questionSolution|answerChoices?)-(\d+)$', re.I)


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def dump(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))


def canon_id(value, kind=None):
    s = str(value or '')
    if s.isdigit():
        return ('tutorial-' if kind == 'tutorial' else 'e-' if kind == 'example' else 'q-') + s
    if s.startswith('tutorial-'):
        return s
    m = IDENTITY.search(s)
    return (('tutorial-' if m[1] == 't' else m[1] + '-') + m[2]) if m else None


class FaithfulRenderer(Renderer):
    def math_node(self, node):
        if isinstance(node, Tag) and node.name == 'mspace':
            width = node.get('width', '')
            if re.fullmatch(r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:em|ex|px|pt|mu|in|cm|mm|pc|%)', width):
                return r'\hspace{' + width + '}'
            named = {'veryverythinmathspace': '0.0556em', 'verythinmathspace': '0.1111em',
                     'thinmathspace': '0.1667em', 'mediummathspace': '0.2222em',
                     'thickmathspace': '0.2778em', 'verythickmathspace': '0.3333em',
                     'veryverythickmathspace': '0.3889em'}
            if width in named:
                return r'\hspace{' + named[width] + '}'
            self.errors.append('Unsupported source mspace width: ' + width)
        return super().math_node(node)


def render_formula(raw, form):
    renderer = FaithfulRenderer(None)
    raw_mathml = None
    features = {'variants': [], 'colors': [], 'backgrounds': [], 'spaces': []}
    if form == 'tex':
        tex = raw[2:-2] if raw.startswith(('$$', r'\[', r'\(')) else raw[1:-1]
    else:
        fragment = raw if form == 'mathml' else (TITLE.search(raw)[1] if TITLE.search(raw) else '')
        if not fragment:
            return None
        soup = BeautifulSoup(fragment, 'html.parser')
        def visit(node):
            if isinstance(node, NavigableString):
                return str(node)
            if node.name == 'mjx-container':
                math = node.find('math')
                if math is None:
                    renderer.errors.append('SVG-title MathJax has no assistive MathML')
                    return ''
                return renderer.m(math)
            return ''.join(visit(child) for child in node.children)
        if form == 'mathml':
            raw_mathml = raw
            tex = renderer.m(soup.find('math'))
        else:
            tex = visit(soup)
            raw_mathml = '\n'.join(str(m) for m in soup.find_all('math')) or None
        for attr, key in [('mathvariant', 'variants'), ('mathcolor', 'colors'), ('mathbackground', 'backgrounds')]:
            features[key] = sorted(set(n.get(attr) for n in soup.find_all(attrs={attr: True})))
        features['spaces'] = sorted(set(n.get('width', '') for n in soup.find_all('mspace')))
    try:
        tex = normalize_source_tex(tex)
    except Exception as exc:
        renderer.errors.append('Source TeX normalization: ' + repr(exc))
    return {'source_tex': tex, 'raw_mathml': raw_mathml, 'features': features,
            'errors': sorted(set(renderer.errors)), 'form': form,
            'styled': bool(STYLE.search(raw))}


def identity_and_role(stack, fallback, mappings):
    identity = None
    role = None
    locator = []
    for tag, attrs in reversed(stack):
        ident = attrs.get('id', '')
        classes = attrs.get('class', '').lower()
        ident_l = ident.lower()
        if ident:
            locator.append('#' + ident)
        if role is None:
            if any(x in classes or x in ident_l for x in ('questionexplanation', 'exampleexplanation', 'workedsolution', 'worked-solution', 'examplesolution')):
                role = 'worked-solution'
            elif any(x in classes for x in ('answerchoice', 'selectlist', 'freeresponsetextbox', 'radiooption', 'checkboxoption')):
                role = 'answer'
            elif any(x in classes for x in ('questiontext', 'questionwidget-text', 'examplequestion', 'question-text')):
                role = 'problem'
        if identity is None:
            m = QUESTION_ID.match(ident)
            identity = ('q-' + m[1]) if m else mappings.get(ident) or canon_id(ident)
    identity = identity or fallback.get('identity')
    role = role or fallback.get('role')
    if identity and identity.startswith('tutorial-'):
        role = 'tutorial'
    return identity, role or 'unknown', '/'.join(reversed(locator[:3]))


def extract_html(content, fallback, mappings, cache):
    content = STRIP.sub('', content)
    stack = []
    formulas = []
    index = 0
    for match in TOKENS.finditer(content):
        raw = match[0]
        lower = raw[:12].lower()
        if lower.startswith('<math'):
            form = 'mathml'
        elif lower.startswith('<svg'):
            form = 'svg-title'
            if not TITLE.search(raw):
                continue
        elif raw[0] != '<':
            form = 'tex'
        else:
            tag = re.match(r'</?([^\s>]+)', raw)[1].lower()
            if raw.startswith('</'):
                for i in range(len(stack) - 1, -1, -1):
                    if stack[i][0] == tag:
                        del stack[i:]
                        break
            elif not raw.endswith('/>'):
                stack.append((tag, {m[1].lower(): html.unescape(next(v for v in m.groups()[1:] if v is not None)) for m in ATTR.finditer(raw)}))
            continue
        index += 1
        identity, role, locator = identity_and_role(stack, fallback, mappings)
        key = digest(form + raw)
        if key not in cache:
            cache[key] = render_formula(raw, form)
        result = cache[key]
        if result is not None and result['source_tex'].strip():
            formulas.append({**result, 'math_academy_id': identity, 'role': role,
                             'locator': locator + f'/{form}[{index}]', 'source_formula_hash': key})
    return formulas


def walk_html(value, locator='$', fallback=None, mappings=None):
    """Yield only original HTML-valued fields, never flattened content strings."""
    fallback = dict(fallback or {})
    mappings = mappings if mappings is not None else {}
    if isinstance(value, dict):
        kind = 'tutorial' if '.tutorials[' in locator else 'example' if '.canonical_examples[' in locator else None
        identity = canon_id(value.get('math_academy_id') or value.get('ma_id'), kind)
        identity = identity or canon_id(value.get('dom_id')) or canon_id(value.get('source_example_id'), 'example')
        if identity:
            fallback['identity'] = identity
            for dom in [value.get('dom_id'), (value.get('source_step') or {}).get('dom_id') if isinstance(value.get('source_step'), dict) else None]:
                if dom:
                    mappings[dom] = identity
        for key, child in value.items():
            loc = locator + '.' + str(key)
            if isinstance(child, str) and HTML_VALUE.search(child) and ('html' in key.lower() or key in ('body', 'response', 'data', 'content')):
                yield child, loc, fallback.copy(), mappings
            elif isinstance(child, (dict, list)):
                yield from walk_html(child, loc, fallback, mappings)
    elif isinstance(value, list):
        for i, child in enumerate(value):
            yield from walk_html(child, f'{locator}[{i}]', fallback, mappings)


def paths(roots):
    args = ['rg', '--files', '--hidden', '--no-ignore', *map(str, roots), '-g', '*.html', '-g', '*.json', '-g', '*.json.gz', '-g', '*.html.gz', '-g', '*.previous.gz']
    proc = subprocess.Popen(args, cwd=ROOT, stdout=subprocess.PIPE, text=True)
    for line in proc.stdout:
        yield Path(line.rstrip('\n'))
    if proc.wait():
        raise RuntimeError('Source file inventory failed')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=DEFAULT_OUT)
    parser.add_argument('--roots', nargs='+', type=Path)
    parser.add_argument('--limit', type=int)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    roots = args.roots or [ROOT / 'reference/mathacademy' / name for name in SOURCE_ROOTS]
    roots = [p.resolve() for p in roots if p.exists()]
    counts = Counter()
    root_counts = defaultdict(Counter)
    records = {}
    fragment_cache = {}
    math_cache = {}
    inode_cache = {}
    start = time.time()
    handles = {name: (args.out / name).open('w') for name in ['source-inventory.jsonl', 'source-unknowns.jsonl', 'source-evidence.jsonl']}
    def ledger(name, obj):
        handles[name].write(dump(obj) + '\n')
    try:
        for p in paths(roots):
            if args.limit and counts['files_enumerated'] >= args.limit:
                break
            rel = str(p.relative_to(ROOT)) if p.is_absolute() and p.is_relative_to(ROOT) else str(p)
            counts['files_enumerated'] += 1
            group = next((str(root.relative_to(ROOT)) for root in roots if p.is_relative_to(root)), 'other')
            inv = {'path': rel}
            excluded = next((part for part in p.parts if part in EXCLUDED_PARTS), None)
            if excluded:
                inv['status'] = 'excluded-derived-directory'
                inv['reason'] = excluded
                counts[inv['status']] += 1
                ledger('source-inventory.jsonl', inv)
                continue
            try:
                stat = p.stat()
                inv['bytes'] = stat.st_size
                counts['eligible_files'] += 1
                counts['eligible_bytes'] += stat.st_size
                inode = (stat.st_dev, stat.st_ino)
                if inode in inode_cache:
                    inv.update(status='duplicate-inode', duplicate_of=inode_cache[inode])
                    ledger('source-inventory.jsonl', inv)
                    counts['duplicate_inode'] += 1
                    continue
                inode_cache[inode] = rel
                data = gzip.open(p, 'rb').read() if p.suffix == '.gz' else p.read_bytes()
                counts['bytes_examined'] += len(data)
                if not STYLE_BYTES.search(data):
                    inv['status'] = 'no-style-prefilter-match'
                    ledger('source-inventory.jsonl', inv)
                    counts[inv['status']] += 1
                    continue
                text = data.decode('utf-8', errors='replace')
                fallback = {'identity': canon_id(p.name), 'role': 'worked-solution' if 'solution' in p.name else None}
                if '.html' in p.name:
                    fragments = [(text, '$', fallback, {})]
                else:
                    try:
                        doc = json.loads(text)
                    except ValueError as exc:
                        raise ValueError('Cannot parse original JSON: ' + str(exc))
                    fragments = walk_html(doc, fallback=fallback)
                inv['fragments'] = 0
                inv['formulas'] = 0
                for content, loc, context, mappings in fragments:
                    if not STYLE.search(content):
                        continue
                    inv['fragments'] += 1
                    counts['style_bearing_html_occurrences'] += 1
                    fragment_key = digest(dump([content, context, mappings]))
                    if fragment_key not in fragment_cache:
                        fragment_cache[fragment_key] = extract_html(content, context, mappings, math_cache)
                        counts['unique_html_contexts'] += 1
                    else:
                        counts['duplicate_html_contexts'] += 1
                    formulas = fragment_cache[fragment_key]
                    inv['formulas'] += len(formulas)
                    if not formulas:
                        counts['style_html_without_formula'] += 1
                        ledger('source-unknowns.jsonl', {'reason': 'style-bearing-html-no-extracted-formula', 'source_path': rel, 'locator': loc})
                    for formula in formulas:
                        identity = formula['math_academy_id']
                        evidence = {'path': rel, 'locator': loc + formula['locator'], 'role': formula['role']}
                        if not identity:
                            counts['unknown_identity_occurrences'] += 1
                            ledger('source-unknowns.jsonl', {'reason': 'unknown-identity', **formula, 'source_path': rel, 'locator': evidence['locator']})
                            continue
                        # Preserve conflicting presentations and role differences.
                        key = digest(dump([identity, formula['role'], formula['source_tex'], formula['errors']]))
                        if key not in records:
                            records[key] = {**formula, 'formula_hash': key, 'kind': 'tutorial' if identity.startswith('tutorial-') else 'example' if identity.startswith('e-') else 'question',
                                            'source_path': rel, 'locator': evidence['locator'], 'evidence': [], 'evidence_count': 0,
                                            'coverage': 'all formulas within style-bearing original HTML fragments'}
                        record = records[key]
                        record['evidence_count'] += 1
                        if len(record['evidence']) < 12 and evidence not in record['evidence']:
                            record['evidence'].append(evidence)
                        ledger('source-evidence.jsonl', {'formula_hash': key, **evidence})
                        counts['identified_formula_occurrences'] += 1
                inv['status'] = 'processed-original-html' if inv['fragments'] else 'style-match-no-original-html'
                counts[inv['status']] += 1
                root_counts[group][inv['status']] += 1
            except Exception as exc:
                inv.update(status='error', error=repr(exc))
                counts['errors'] += 1
                ledger('source-unknowns.jsonl', {'reason': 'source-file-error', **inv})
            ledger('source-inventory.jsonl', inv)
            if counts['files_enumerated'] % 5000 == 0:
                print(dump({'seconds': round(time.time() - start), 'files': counts['files_enumerated'], 'eligible': counts['eligible_files'], 'unique_formulas': len(records), 'unknown': counts['unknown_identity_occurrences']}), flush=True)
        with (args.out / 'source-formulas.jsonl').open('w') as output:
            for key in sorted(records):
                output.write(dump(records[key]) + '\n')
        summary = {'complete': not args.limit, 'elapsed_seconds': round(time.time() - start, 2), 'roots': list(map(str, roots)),
                   'counts': dict(counts), 'root_counts': {k: dict(v) for k, v in root_counts.items()},
                   'unique_formulas': len(records), 'unique_styled_formulas': sum(r['styled'] for r in records.values()),
                   'identities': len({r['math_academy_id'] for r in records.values()}),
                   'formula_errors': sum(bool(r['errors']) for r in records.values()),
                   'by_role': dict(Counter(r['role'] for r in records.values())),
                   'limitations': ['Source completeness is limited to enumerated roots and extensions.', 'Style-free-only HTML fragments are prefiltered out; all formulas inside style-bearing fragments are included.',
                                   'Per-formula evidence array is capped at 12; source-evidence.jsonl contains every occurrence.',
                                   'Unknown identities and unsupported rendering remain explicit in source-unknowns.jsonl / formula errors.',
                                   'Normalized content, solver/EDB/repair outputs are excluded; original HTML within content.json is included.'],
                   'excluded_path_components': sorted(EXCLUDED_PARTS)}
        (args.out / 'source-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
        print(json.dumps(summary, indent=2))
    finally:
        for handle in handles.values():
            handle.close()


if __name__ == '__main__':
    main()
