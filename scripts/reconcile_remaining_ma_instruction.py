#!/usr/bin/env python3
"""Stage source-backed repairs to remaining MA tutorials and worked examples.

This reads an offline live-database export and captured MathML, checks vault
copies, and writes CAS-guarded EDN only. It never opens a database writer.
Run with the MA Python environment (BeautifulSoup is an existing dependency).
"""

import argparse
import collections
import difflib
import hashlib
import importlib.util
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

import reconcile_ma_instruction as original


EXTRACTOR = Path('/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/3-JSON/lesson-json.py')
SPEC = importlib.util.spec_from_file_location('captured_ma_extractor', EXTRACTOR)
CAPTURE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CAPTURE
SPEC.loader.exec_module(CAPTURE)
MATH = re.compile(r'\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])*?(?<!\\)\$')
MATHML = re.compile(r'<math\b[\s\S]*?</math>')
STEP = re.compile(r'<div\b[^>]*\bid="step-(\d+)"[^>]*>')
BROKEN_MATH = re.compile(r'∑_|∫_|lim_\(|√\(|(?<![A-Za-z\\])(?:sqrt|root|overline)\(|[_^]\([^)]*[→∞][^)]*\)')
COMMANDS = {
    '∑': r'\sum', '∏': r'\prod', '∫': r'\int', '∬': r'\iint', '∭': r'\iiint',
    '∞': r'\infty', '∂': r'\partial', '∇': r'\nabla', '−': '-', '⋅': r'\cdot',
    '·': r'\cdot', '×': r'\times', '÷': r'\div', '±': r'\pm', '∓': r'\mp',
    '≤': r'\le', '≥': r'\ge', '≠': r'\ne', '≈': r'\approx', '≡': r'\equiv',
    '∈': r'\in', '∉': r'\notin', '⊂': r'\subset', '⊆': r'\subseteq',
    '∪': r'\cup', '∩': r'\cap', '∅': r'\emptyset', '→': r'\to',
    '↦': r'\mapsto', '⇒': r'\Rightarrow', '⇔': r'\Leftrightarrow',
    '⟹': r'\Longrightarrow', '⟺': r'\Longleftrightarrow', '↔': r'\leftrightarrow',
    '…': r'\ldots', '⋯': r'\cdots', '⋮': r'\vdots', '⋱': r'\ddots',
    '∧': r'\land', '∨': r'\lor', '¬': r'\neg', '∀': r'\forall', '∃': r'\exists',
    '∘': r'\circ', '∥': r'\Vert', '‖': r'\Vert', '⟨': r'\langle', '⟩': r'\rangle',
    '⌊': r'\lfloor', '⌋': r'\rfloor', '⌈': r'\lceil', '⌉': r'\rceil',
    'α': r'\alpha', 'β': r'\beta', 'γ': r'\gamma', 'δ': r'\delta', 'ε': r'\epsilon',
    'θ': r'\theta', 'λ': r'\lambda', 'μ': r'\mu', 'ν': r'\nu', 'ξ': r'\xi',
    'π': r'\pi', 'ρ': r'\rho', 'σ': r'\sigma', 'τ': r'\tau', 'φ': r'\phi',
    'ϕ': r'\varphi', 'χ': r'\chi', 'ψ': r'\psi', 'ω': r'\omega',
    'Γ': r'\Gamma', 'Δ': r'\Delta', 'Θ': r'\Theta', 'Λ': r'\Lambda', 'Σ': r'\Sigma',
    'Φ': r'\Phi', 'Ψ': r'\Psi', 'Ω': r'\Omega', 'ℕ': r'\mathbb{N}',
    'ℤ': r'\mathbb{Z}', 'ℚ': r'\mathbb{Q}', 'ℝ': r'\mathbb{R}', 'ℂ': r'\mathbb{C}',
    'ℵ': r'\aleph', '∝': r'\propto', '⊥': r'\perp', '∠': r'\angle',
    '′': r'\prime', '″': r'\prime\prime', '‴': r'\prime\prime\prime',
    '{': r'\{', '}': r'\}', '%': r'\%', '&': r'\&', '#': r'\#',
    '\u2061': '', '\u2062': '', '\u2063': '', '\u2064': '', '\u200b': '',
}


def tex_chars(text):
    return ''.join(COMMANDS.get(c, c) + (' ' if c in COMMANDS and COMMANDS[c].startswith('\\') else '') for c in text)


def text_chars(text):
    return ''.join({'\\': r'\textbackslash{}', '{': r'\{', '}': r'\}', '$': r'\$',
                    '%': r'\%', '&': r'\&', '#': r'\#', '_': r'\_', '^': r'\^{}'}.get(c, c) for c in text)


def to_tex(node):
    """Translate a deliberately limited MathML subset; unknown structures fail closed."""
    if isinstance(node, NavigableString):
        if not str(node).strip():
            return ''
        raise ValueError('unwrapped MathML text')
    name = node.name
    if any(node.has_attr(a) for a in ('mathcolor', 'mathbackground', 'style')):
        raise ValueError('unsupported significant MathML style')
    for attr in ('rowlines', 'columnlines', 'frame'):
        if node.has_attr(attr) and any(v != 'none' for v in node[attr].split()):
            raise ValueError(f'unsupported MathML {attr}')
    children = [c for c in node.children if isinstance(c, Tag)]
    inner = lambda: ' '.join(to_tex(c) for c in node.children).strip()
    if name in ('math', 'mrow') and len(children) >= 2 and children[0].name == 'mo' and any(c.name == 'mtable' for c in children):
        opening = children[0].get_text().strip()
        if opening in ('{', '[', '('):
            closing = children[-1].get_text().strip() if children[-1].name == 'mo' else ''
            expected = {'{': '}', '[': ']', '(': ')'}[opening]
            if closing == expected:
                body = ' '.join(to_tex(c) for c in children[1:-1])
                right = tex_chars(closing)
            else:
                body = ' '.join(to_tex(c) for c in children[1:])
                right = '.'
            return r'\left' + tex_chars(opening) + ' ' + body + r'\right' + right
    if name in ('math', 'mrow', 'mtd'):
        return inner()
    if name == 'mphantom':
        return r'\phantom{' + inner() + '}'
    if name == 'semantics':
        return to_tex(children[0])
    if name == 'mstyle':
        value = inner()
        variant = node.get('mathvariant')
        if variant:
            styles = {'normal': 'mathrm', 'bold': 'mathbf', 'italic': 'mathit', 'double-struck': 'mathbb', 'script': 'mathcal', 'fraktur': 'mathfrak'}
            if variant not in styles:
                raise ValueError(f'unsupported mathvariant {variant}')
            value = '\\' + styles[variant] + '{' + value + '}'
        return value
    if name == 'mspace':
        return r'\,'
    if name in ('mi', 'mn', 'mo', 'mtext', 'ms'):
        value = node.get_text()
        if name in ('mtext', 'ms'):
            if '[math]' in value or '\\' in value:
                raise ValueError('unrendered markup inside MathML literal text')
            return r'\text{' + text_chars(value) + '}' if value else ''
        if name == 'mi' and value in CAPTURE.MATHML_TEX_OPERATOR_NAMES:
            return '\\' + value + ' '
        result = tex_chars(value)
        variant = node.get('mathvariant')
        if variant:
            styles = {'normal': 'mathrm', 'bold': 'mathbf', 'italic': 'mathit', 'double-struck': 'mathbb', 'script': 'mathcal', 'fraktur': 'mathfrak'}
            if variant not in styles:
                raise ValueError(f'unsupported mathvariant {variant}')
            result = '\\' + styles[variant] + '{' + result + '}'
        return result
    if name == 'mfrac' and len(children) == 2:
        if node.get('linethickness') in ('0', '0px'):
            return r'\genfrac{}{}{0pt}{}{' + to_tex(children[0]) + '}{' + to_tex(children[1]) + '}'
        return r'\frac{' + to_tex(children[0]) + '}{' + to_tex(children[1]) + '}'
    if name in ('msup', 'msub', 'msubsup') and len(children) == (3 if name == 'msubsup' else 2):
        value = '{' + to_tex(children[0]) + '}'
        marks = ('_', '^') if name == 'msubsup' else ('^' if name == 'msup' else '_',)
        return value + ''.join(mark + '{' + to_tex(c) + '}' for mark, c in zip(marks, children[1:]))
    if name == 'msqrt':
        return r'\sqrt{' + inner() + '}'
    if name == 'mroot' and len(children) == 2:
        return r'\sqrt[' + to_tex(children[1]) + ']{' + to_tex(children[0]) + '}'
    if name in ('munder', 'mover', 'munderover') and len(children) == (3 if name == 'munderover' else 2):
        base = to_tex(children[0])
        decoration = children[1].get_text().strip()
        if name == 'mover' and node.get('accent') == 'true':
            accents = {'¯': 'overline', '‾': 'overline', '―': 'overline', '^': 'hat', 'ˆ': 'hat', '→': 'vec', '˙': 'dot', '.': 'dot', '~': 'tilde', '˜': 'tilde'}
            if decoration not in accents:
                raise ValueError(f'unsupported accent {decoration}')
            return '\\' + accents[decoration] + '{' + base + '}'
        if name == 'munderover':
            return base + '_{' + to_tex(children[1]) + '}^{' + to_tex(children[2]) + '}'
        if children[0].get_text().strip() in ('∑', '∏', '∫', 'lim', 'max', 'min'):
            return base + ('_' if name == 'munder' else '^') + '{' + to_tex(children[1]) + '}'
        return ('\\underset' if name == 'munder' else '\\overset') + '{' + to_tex(children[1]) + '}{' + base + '}'
    if name == 'mtable':
        if any(c.name != 'mtr' for c in children):
            raise ValueError('unsupported table rows')
        rows = [[c for c in row.children if isinstance(c, Tag)] for row in children]
        if not rows or any(c.name != 'mtd' for row in rows for c in row):
            raise ValueError('unsupported table cells')
        width = max(len(row) for row in rows)
        aligns = node.get('columnalign', 'center').split()
        align = ''.join({'right': 'r', 'left': 'l', 'center': 'c'}[aligns[min(i, len(aligns) - 1)]] for i in range(width))
        return r'\begin{array}{' + align + '}' + r' \\ '.join(' & '.join(to_tex(c) for c in row) for row in rows) + r'\end{array}'
    if name == 'mfenced':
        separators = ''.join(node.get('separators', ',').split())
        return tex_chars(node.get('open', '(')) + ''.join((tex_chars(separators[min(i - 1, len(separators) - 1)]) if i and separators else '') + to_tex(c) for i, c in enumerate(children)) + tex_chars(node.get('close', ')'))
    raise ValueError(f'unsupported MathML {name}')


def canonical(value):
    return re.sub(r'\s+', '', value.replace('sqrt(', '√('))


def strip_vault_footer(value):
    return re.split(r'\n(?:```update-progress\b|<!-- lesson-nav:start -->)', value, maxsplit=1)[0].strip()


def lossy_features(math):
    """Only propose formulas with information lost by the text extractor."""
    features = {n.name for n in math.find_all(('mfrac', 'msqrt', 'mroot', 'munder', 'mover', 'munderover', 'mphantom'))}
    for table in math.find_all('mtable'):
        rows = table.find_all('mtr', recursive=False)
        if len(rows) > 1 or any(len(r.find_all('mtd', recursive=False)) > 1 for r in rows):
            features.add('table-layout')
    if any(len(n.get_text().strip()) > 1 for n in math.find_all('mtext')):
        features.add('literal-text')
    return sorted(features)


class SourceMathParser(HTMLParser):
    """Keep only complete MathML directly in its own instruction component.

    An SVG title may contain a complete MathML formula, or only MathML for a
    boxed blank embedded in a larger TeX string. Accept the former only when
    the title has no text outside its MathJax container.
    """

    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack = []
        self.active = None
        self.rows = []
        self.title_start = None
        self.title_has_outer_text = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        context = self.stack[-1][1] if self.stack else (None, None, False)
        sid, field, in_svg = context
        if tag == 'div' and re.fullmatch(r'step-\d+', attrs.get('id', '')):
            sid = attrs['id'][5:]
            field = 'content' if attrs.get('steptype') == 'tutorial' else None
        if tag == 'div' and attrs.get('id', '').startswith('question-'):
            sid, field = None, None
        classes = attrs.get('class', '').split()
        if 'exampleQuestion' in classes:
            field = 'problem'
        if 'exampleExplanation' in classes:
            field = 'explanation'
        in_svg = in_svg or tag == 'svg'
        if tag == 'title' and in_svg:
            self.title_start = len(self.rows)
            self.title_has_outer_text = False
        if tag == 'math' and sid and field and (not in_svg or self.title_start is not None):
            assert self.active is None
            self.active = ((sid, field), [])
        if self.active is not None:
            self.active[1].append(self.get_starttag_text())
        if tag not in self.VOID:
            self.stack.append((tag, (sid, field, in_svg)))

    def handle_endtag(self, tag):
        if self.active is not None:
            self.active[1].append('</' + tag + '>')
            if tag == 'math':
                self.rows.append((self.active[0], ''.join(self.active[1])))
                self.active = None
        if tag == 'title' and self.title_start is not None:
            if self.title_has_outer_text:
                del self.rows[self.title_start:]
            self.title_start = None
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, value):
        if self.title_start is not None and value.strip() and not any(t == 'mjx-container' for t, _ in self.stack):
            self.title_has_outer_text = True
        if self.active is not None:
            self.active[1].append(value)

    def handle_entityref(self, name):
        self.handle_data('&' + name + ';')

    def handle_charref(self, name):
        self.handle_data('&#' + name + ';')


def source_formulas(path):
    parser = SourceMathParser()
    parser.feed(path.read_text())
    out = collections.defaultdict(lambda: collections.defaultdict(list))
    for key, occurrence in parser.rows:
            candidates = out[key]
            subnodes = out[(key[0], key[1], 'subnodes')]
            math = BeautifulSoup(occurrence, 'html.parser').find('math')
            old = CAPTURE.mathml_to_text(math)
            features = lossy_features(math)
            try:
                new = to_tex(math)
                error = None
            except (ValueError, KeyError) as exc:
                new, error = None, str(exc)
            candidates[canonical(old)].append({'before': old, 'after': new, 'error': error, 'lossy_features': features,
                                               'mathml_sha256': hashlib.sha256(occurrence.encode()).hexdigest()})
            # DATA Markdown already repairs some surrounding aligned layouts.
            # Match the still-broken bounds or radicals independently inside
            # that layout, using exactly the captured MathML subtree.
            for subnode in math.find_all(('munder', 'mover', 'munderover', 'msqrt', 'mroot')):
                old_subnode = CAPTURE.mathml_to_text(subnode)
                if not BROKEN_MATH.search(old_subnode):
                    continue
                try:
                    new_subnode = to_tex(subnode)
                except (ValueError, KeyError):
                    continue
                subnodes[canonical(old_subnode)].append({'before': old_subnode, 'after': new_subnode,
                                                        'mathml_sha256': hashlib.sha256(str(subnode).encode()).hexdigest(),
                                                        'lossy_features': [subnode.name]})
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scope', type=Path, default=Path('.local/edb/remaining-courses/scope.json'))
    parser.add_argument('--snapshot', type=Path, default=Path('.local/edb/remaining-courses/before.jsonl'))
    parser.add_argument('--output', type=Path, default=Path('.local/edb/remaining-courses/instruction'))
    parser.add_argument('--batch-size', type=int, default=50)
    args = parser.parse_args()
    scope = json.loads(args.scope.read_text())
    current = collections.defaultdict(dict)
    identities = {}
    canonical_examples = set()
    for line in args.snapshot.open():
        row = json.loads(line)
        if row['a'] == 'knowledge-point/canonical-example':
            canonical_examples.add(row['ref_eid'])
        if row['a'] in ('tutorial/id', 'question/id'):
            identities[(row['a'].split('/')[0], row['uuid'])] = row['e']
        if row['a'] in ('tutorial/content', 'question/problem', 'question/worked-solution'):
            current[row['e']][row['a']] = row['raw_string'] if row['raw_string'] is not None else row['value_edn']
    content_counts = collections.Counter()
    for path in original.DATA.glob('*/Source/*.json'):
        data = json.loads(path.read_text())
        content_counts.update((s['step_type'], s['content_id']) for s in data['lesson']['items'] if s['item_type'] == 'step')
    collisions = {key for key, count in content_counts.items() if count > 1}
    vault_index = original.candidates_index()
    report = {'snapshot': str(args.snapshot), 'scope_topics': len(scope['topic_ids']), 'selected': [],
              'unresolved': [], 'remaining_malformed': [], 'protected_current': [], 'source_errors': [], 'vault_differences': [], 'counts': {}}
    counts = collections.Counter()
    course_by_topic = {t: c for c, ts in scope['topics_by_first_course'].items() for t in ts}
    forms = collections.defaultdict(list)
    formulas_for_check = []
    for topic in sorted(scope['topic_ids'], key=int):
        course = course_by_topic[topic]
        data_path = original.DATA / topic / 'Source' / f'{topic}.json'
        html_path = data_path.with_suffix('.html')
        if not data_path.exists():
            report['source_errors'].append({'topic': topic, 'reason': 'capture missing'})
            continue
        data = json.loads(data_path.read_text())
        base, error = original.extract(original.DATA / topic / f'{topic}.md', data, topic)
        if error:
            report['source_errors'].append({'topic': topic, 'reason': error})
            continue
        counts['topics_reviewed'] += 1
        steps = [s for s in data['lesson']['items'] if s['item_type'] == 'step']
        anchors = [(s['step_id'], s['step_type'], s['content_id'], s['title']) for s in steps]
        for json_path in vault_index[topic]:
            markdown = original.source_markdown(json_path)
            if markdown is None:
                report['source_errors'].append({'topic': topic, 'source': str(json_path), 'reason': 'vault Markdown missing'})
                continue
            vd = json.loads(json_path.read_text())
            va = [(s['step_id'], s['step_type'], s['content_id'], s['title']) for s in vd['lesson']['items'] if s['item_type'] == 'step']
            if va != anchors:
                report['source_errors'].append({'topic': topic, 'source': str(json_path), 'reason': 'vault step identity mismatch'})
                continue
            copies, error = original.extract(markdown, vd, topic)
            if error:
                report['source_errors'].append({'topic': topic, 'source': str(markdown), 'reason': error})
                continue
            counts['vault_copies_reviewed'] += 1
            for key, value in copies.items():
                if original.cleaned(strip_vault_footer(value)) != original.cleaned(base[key]):
                    report['vault_differences'].append({'topic': topic, 'step_id': key[0], 'field': key[1], 'source': str(markdown),
                                                      'diff': '\n'.join(difflib.unified_diff(base[key].splitlines(), strip_vault_footer(value).splitlines()))})
        source = source_formulas(html_path)
        html_sha = hashlib.sha256(html_path.read_bytes()).hexdigest()
        for step in steps:
            sid, cid, kind = step['step_id'], step['content_id'], step['step_type']
            uid = str(original.ident(kind, sid if (kind, cid) in collisions else cid))
            entity = 'tutorial' if kind == 'tutorial' else 'question'
            eid = identities[(entity, uid)]
            if kind == 'example':
                assert eid in canonical_examples, (topic, sid, eid)
            for field in (('content',) if kind == 'tutorial' else ('problem', 'explanation')):
                attr = entity + '/' + ('worked-solution' if field == 'explanation' else field)
                before = current[eid].get(attr)
                assert before, (topic, sid, attr)
                counts['components_reviewed'] += 1
                if original.cleaned(before) != original.cleaned(base[(sid, field)]):
                    report['protected_current'].append({'topic': topic, 'step_id': sid, 'eid': eid, 'attribute': attr, 'reason': 'live text differs from captured Markdown'})
                    continue
                replacements = []
                unresolved = []

                def replace(match):
                    wrapped = match[0]
                    n = 2 if wrapped.startswith(('$$', r'\(', r'\[')) else 1
                    latex = wrapped[n:-n]
                    candidates = source.get((sid, field), {}).get(canonical(latex), [])
                    unique = {c['after'] for c in candidates if c['after'] is not None}
                    if not candidates:
                        new = latex
                        for key, parts in sorted(source.get((sid, field, 'subnodes'), {}).items(), key=lambda x: -len(x[0])):
                            texts = {p['after'] for p in parts}
                            if len(texts) != 1:
                                continue
                            pattern = r'(?<!\\)' + r'\s*'.join('(?:sqrt|√)' if c == '√' else re.escape(c) for c in key)
                            value = next(iter(texts))
                            def replace_part(part):
                                replacements.append({'before': part[0], 'after': value,
                                                     'mathml_sha256': sorted({p['mathml_sha256'] for p in parts}),
                                                     'lossy_features': sorted({f for p in parts for f in p['lossy_features']}),
                                                     'subtree_match': True})
                                return value
                            new = re.sub(pattern, replace_part, new)
                        return wrapped[:n] + new + wrapped[-n:]
                    if not any(c['lossy_features'] for c in candidates):
                        return wrapped
                    if any(c['lossy_features'] == ['mphantom'] for c in candidates):
                        return wrapped
                    if len(unique) != 1 or any(c['error'] for c in candidates):
                        unresolved.append({'latex': latex, 'reason': 'ambiguous or unsupported source MathML', 'candidates': candidates})
                        return wrapped
                    new = next(iter(unique))
                    if canonical(new) == canonical(latex):
                        return wrapped
                    replacements.append({'before': latex, 'after': new, 'mathml_sha256': sorted({c['mathml_sha256'] for c in candidates}),
                                         'lossy_features': sorted({f for c in candidates for f in c['lossy_features']})})
                    return wrapped[:n] + new + wrapped[-n:]

                after = MATH.sub(replace, before)
                remaining = []
                for match in MATH.finditer(after):
                    if BROKEN_MATH.search(match[0]):
                        remaining.append(match[0])
                if remaining:
                    report['remaining_malformed'].append({'topic': topic, 'step_id': sid, 'attribute': attr, 'expressions': remaining,
                                                         'reason': 'No supported, unambiguous original MathML replacement matched the live formula.'})
                if unresolved:
                    report['unresolved'].append({'topic': topic, 'step_id': sid, 'attribute': attr, 'details': unresolved})
                if after == before:
                    continue
                assert MATH.sub('<math>', before) == MATH.sub('<math>', after)
                ref = f'[:{entity}/id #uuid "{uid}"]'
                form = (f'[:db/cas {ref} :{attr} {original.json_string(before)} {original.json_string(after)}]\n'
                        f' {{:db/id {ref} :db/ensure [:{entity}/validate]}}')
                forms[course].append(form)
                selected = {'topic': topic, 'course': course, 'step_id': sid, 'content_id': cid, 'eid': eid, 'entity_id': uid,
                            'attribute': attr, 'source': str(html_path), 'source_sha256': html_sha,
                            'before': before, 'after': after, 'replacements': replacements,
                            'diff': '\n'.join(difflib.unified_diff(before.splitlines(), after.splitlines(), fromfile='live', tofile='repaired'))}
                report['selected'].append(selected)
                counts[attr] += 1
                counts['formulas_repaired'] += len(replacements)
                for j, replacement in enumerate(replacements):
                    formulas_for_check.append({'topic': topic, 'eid': eid, 'attribute': attr, 'index': j, 'latex': replacement['after'], 'display': True})
    args.output.mkdir(parents=True, exist_ok=True)
    for old in args.output.glob('repairs-*.edn'):
        old.unlink()
    report['apply_batches_in_order'] = []
    for course, entries in forms.items():
        for i, start in enumerate(range(0, len(entries), args.batch_size), 1):
            name = f'repairs-{course}-{i:04}.edn'
            (args.output / name).write_text('[\n ' + '\n '.join(entries[start:start + args.batch_size]) + '\n]\n')
            report['apply_batches_in_order'].append(name)
    report['counts'] = dict(counts)
    report['course_update_counts'] = dict(collections.Counter(r['course'] for r in report['selected']))
    report['topic_update_counts'] = dict(collections.Counter(r['topic'] for r in report['selected']))
    (args.output / 'report.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    (args.output / 'latex.json').write_text(json.dumps(formulas_for_check, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'counts': report['counts'], 'courses': report['course_update_counts'], 'vault_differences': len(report['vault_differences']),
                      'unresolved_components': len(report['unresolved']), 'protected_current': len(report['protected_current']),
                      'remaining_malformed_components': len(report['remaining_malformed']),
                      'source_errors': len(report['source_errors']), 'output': str(args.output)}, indent=2))


if __name__ == '__main__':
    main()
