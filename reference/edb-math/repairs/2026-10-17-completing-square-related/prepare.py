"""Prepare the authorized related-lesson repairs; this script never submits."""
import copy
import difflib
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'Cargo.toml').exists())
sys.path.insert(0, str(ROOT))
from capture.scripts.database.edn import dumps, kw, loads
from capture.scripts.database.client import QUESTION_PULL
from scripts.question_capture.math_format import _legacy_commands

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / '2026-10-17-completing-square-format'
spec = importlib.util.spec_from_file_location('base_format_repair', BASE / 'prepare.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
OP = re.compile(r'(?<![\\A-Za-z{])\b(arsinh|arcosh|artanh|arsech|arcsch|arcoth|arctan|arcsin|arccos)\b')


def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False, default=str) + '\n')


def operator_text(text):
    return OP.sub(lambda m: '\\' + m[1] if m[1] in ('arctan', 'arcsin', 'arccos')
                  else r'\operatorname{' + m[1] + '}', text)


def inline_punctuation(text):
    count = 0
    def math(match):
        nonlocal count
        value = match[0]
        if not value.startswith('$') or value.startswith('$$'):
            return value
        body = value[1:-1]
        # TeX spacing commands such as \, must stay inside the math run.
        ending = re.search(r'(?<!\\)([,.;:?!]+)\s*$', body)
        if not ending:
            return value
        count += 1
        return '$' + body[:ending.start()].rstrip() + '$' + ending[1]
    return base.MATH.sub(math, text), count


def improve_fractions(text):
    # Only the audited hyperbolic tutorial/examples contain these exact forms.
    replacements = {
        r'\int(dx)/(\sqrt{(x - 1)^{2} + 1})': r'\int\frac{\mathrm{d}x}{\sqrt{(x - 1)^{2} + 1}}',
        r'\int(1)/(1 - (\frac{1}{2}(x - 2))^{2})dx': r'\int\frac{\mathrm{d}x}{1 - (\frac{1}{2}(x - 2))^{2}}',
        r'\int(1)/(\sqrt{(\frac{x - 1}{3})^{2} - 1})dx': r'\int\frac{\mathrm{d}x}{\sqrt{(\frac{x - 1}{3})^{2} - 1}}',
        r'\int(1)/(\sqrt{(x - 5)^{2} + 9})dx': r'\int\frac{\mathrm{d}x}{\sqrt{(x - 5)^{2} + 9}}',
        r'\int(1)/(\sqrt{9[((x - 5)^{2})/(9) + 1]})dx': r'\int\frac{\mathrm{d}x}{\sqrt{9[\frac{(x - 5)^{2}}{9} + 1]}}',
        r'\int(1)/(\sqrt{(\frac{x - 5}{3})^{2} + 1})dx': r'\int\frac{\mathrm{d}x}{\sqrt{(\frac{x - 5}{3})^{2} + 1}}',
    }
    n = 0
    for old, new in replacements.items():
        n += text.count(old)
        text = text.replace(old, new)
    return text, n


def prepare():
    lesson_rows = loads((HERE / 'evidence/lessons.edn').read_text())
    question_rows = loads((HERE / 'evidence/questions.edn').read_text())
    entities = base.flatten(lesson_rows)
    for eid, value in base.flatten(question_rows).items():
        entities.setdefault(eid, {}).update(value)
    findings = json.loads((HERE / 'evidence/source-findings.json').read_text())
    additional = json.loads((HERE / 'evidence/additional-source-review.json').read_text())
    operators = {(v['entity'], v['attribute']) for v in additional['plain_operators']}
    literal = {v['entity'] for v in findings if v['code'] == 'literal_brace'}
    legacy = {v['entity'] for v in findings if v['code'] == 'legacy_command'}
    trailing = {v['entity'] for v in findings if v['code'] == 'trailing_equals'}
    separation = {v['entity'] for v in findings if v['code'] == 'missing_separation'}
    bold = {v['entity'] for v in additional['malformed_bold']}
    source = loads((HERE / 'evidence/source.edn').read_text())
    assert len(source) == 1 and source[0][0][':db/ident'] == ':agent/codex'
    source_eid = source[0][0][':db/id']
    counts = {'underbrace_solutions': 0, 'underbrace_occurrences': 0,
              'legacy_examples': 0, 'legacy_blocks': 0, 'trailing_equals_blocks': 0,
              'operator_attributes': 0, 'operator_occurrences': 0,
              'prompt_separations': 0, 'broken_bold': 0, 'sign_typos': 0,
              'slash_fraction_occurrences': 0, 'parenthesis_groups': 0,
              'inline_punctuation': 0}
    changes, chains = [], []
    for eid, v in sorted(entities.items()):
        for attr in (':question/problem', ':question/worked-solution', ':tutorial/content', ':answer/value'):
            if attr not in v:
                continue
            old, new = v[attr], v[attr]
            if attr == ':question/worked-solution' and eid in literal:
                new, n = base.repair_underbraces(new)
                assert n > 0
                counts['underbrace_solutions'] += 1
                counts['underbrace_occurrences'] += n
            if attr == ':question/worked-solution' and eid in legacy:
                n = new.count(r'\eqalign')
                assert n > 0
                new = _legacy_commands(new)
                counts['legacy_examples'] += 1
                counts['legacy_blocks'] += n
                assert not re.search(r'(?<!\\)\\\[\d+pt\]', new)
            if eid in trailing:
                def align(match):
                    if not re.search(r'&\s*=\s*\\\\', match[1]):
                        return match[0]
                    rows = [r.strip().split('&') for r in match[1].split(r'\\')]
                    assert all(len(row) == 2 for row in rows)
                    assert all(row[1].strip() == '=' for row in rows[:-1])
                    suffix = rows[-1][1].strip()
                    assert suffix in ('', '.')
                    expr = [row[0].strip() for row in rows]
                    chains.append(expr)
                    out = ['& ' + expr[0]] + ['&= ' + e for e in expr[1:]]
                    out[-1] += suffix
                    counts['trailing_equals_blocks'] += 1
                    return '\\begin{aligned}\n' + ' \\\\\n'.join(out) + '\n\\end{aligned}'
                new = base.ALIGNED.sub(align, new)
            if (eid, attr) in operators:
                n = len(OP.findall(new))
                assert n > 0
                new = operator_text(new)
                counts['operator_attributes'] += 1
                counts['operator_occurrences'] += n
            if eid in (17592186166618, 17592186166620, 17592186166621, 17592186168098):
                new, n = improve_fractions(new)
                counts['slash_fraction_occurrences'] += n
            if attr == ':question/problem' and eid in separation:
                matches = [m for m in base.MATH.finditer(new)
                           if re.search(r'[A-Za-z]\.$|\$\.$', new[:m.start()])]
                assert len(matches) == 1
                at = matches[0].start()
                new = new[:at] + '\n\n' + new[at:]
                counts['prompt_separations'] += 1
            if attr == ':tutorial/content' and eid in bold:
                assert new.count('**Step 1. **Group') == 1
                new = new.replace('**Step 1. **Group', '**Step 1.** Group')
                counts['broken_bold'] += 1
            if eid == 17592186287952 and attr == ':question/worked-solution':
                a = r'({x}^{2}+2\cdot 3x+{3}^{2})-9+10'
                assert new.count(a) == 1
                new = new.replace(a, r'({x}^{2}-2\cdot 3x+{3}^{2})-9+10')
                counts['sign_typos'] += 1
            if eid == 17592186292695 and attr == ':question/worked-solution':
                a = r'\sqrt{1+2x-{x}^{2}}'
                assert new.count(a) == 1
                new = new.replace(a, r'\sqrt{1-2x-{x}^{2}}')
                counts['sign_typos'] += 1
            if attr != ':answer/value':
                # Cosmetic cleanup remains bounded to already edited text or
                # the audited parenthesis-group attributes.
                parenthesis_flag = any(f['entity'] == eid and f['attribute'] == attr
                                       and f['code'] == 'parenthesis_group' for f in findings)
                if new != old or parenthesis_flag:
                    counts['parenthesis_groups'] += new.count('{)}')
                    new = new.replace('{)}', ')')
                    new, n = inline_punctuation(new)
                    counts['inline_punctuation'] += n
                try:
                    base.validate_math(new)
                except AssertionError as error:
                    raise AssertionError((eid, attr, old, new, str(error))) from error
            else:
                if new != old:
                    assert not v.get(':task-item/_responses'), 'Historical response values are immutable'
                    owners = [f for f in entities.values() if any(a[':db/id'] == eid for a in f.get(':answer-field/choices', []))]
                    assert len(owners) == 1
                    assert ':answer-field/correct' not in owners[0]
                    # Removing only operator markup recovers the exact old value.
                    demark = re.sub(r'\\operatorname\{([^{}]+)\}', r'\1', new)
                    demark = re.sub(r'\\(arctan|arcsin|arccos)\b', r'\1', demark)
                    assert demark == old
            if new != old:
                if attr == ':question/problem':
                    assert re.findall(r'\{\{[^}]+\}\}', new) == re.findall(r'\{\{[^}]+\}\}', old)
                changes.append({'entity': eid, 'attribute': attr, 'before': old, 'after': new})

    assert counts['underbrace_solutions'] == 63
    assert counts['legacy_examples'] == 4 and counts['legacy_blocks'] == 5
    assert counts['trailing_equals_blocks'] == 14
    assert counts['operator_attributes'] == 38 and counts['operator_occurrences'] == 43
    assert counts['prompt_separations'] == 3 and counts['broken_bold'] == 1
    assert counts['sign_typos'] == 2 and counts['slash_fraction_occurrences'] == 7

    # Independently verify the numeric rational equation chains and sign repairs.
    from sympy import expand, symbols
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
    def expression(s):
        s = s.replace('{)}', ')').replace(r'\cdot', '*').replace(r'\,', '')
        while r'\frac' in s:
            new = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', s)
            assert new != s, s
            s = new
        s = s.replace('{', '(').replace('}', ')').replace('^', '**')
        assert re.fullmatch(r'[xyztau0-9+*()./\s-]+', s), s
        return parse_expr(s, transformations=standard_transformations + (implicit_multiplication_application,))
    pairs = 0
    for chain in chains:
        for a, b in zip(chain, chain[1:]):
            assert expand(expression(a) - expression(b)) == 0, (a, b)
            pairs += 1
    x = symbols('x')
    assert expand((x*x - 2*3*x + 3**2) - 9 + 10 - (x*x - 6*x + 10)) == 0
    assert expand(1 - 2*x - x*x - (2 - (x + 1)**2)) == 0

    forms = [[kw('db/cas'), c['entity'], kw(c['attribute']), c['before'], c['after']] for c in changes]
    for eid in sorted({c['entity'] for c in changes}):
        kind = 'question' if ':question/id' in entities[eid] else 'tutorial' if ':tutorial/id' in entities[eid] else 'answer'
        forms.append([kw('db/ensure'), eid, kw(kind + '/validate')])
    text = '[\n' + '\n'.join(' ' + dumps(f) for f in forms) + '\n]\n'
    (HERE / 'transaction.edn').write_text(text)
    assert loads(text) == forms
    save('changes.json', changes)
    diff = []
    for c in changes:
        diff.extend(difflib.unified_diff([s+'\n' for s in c['before'].splitlines()],
                    [s+'\n' for s in c['after'].splitlines()],
                    fromfile=f"{c['entity']} {c['attribute']} before",
                    tofile=f"{c['entity']} {c['attribute']} repaired"))
        diff.append('\n')
    (HERE / 'changes.diff').write_text(''.join(diff))
    after = copy.deepcopy(lesson_rows)
    edits = {(c['entity'], c['attribute']): c for c in changes}
    def update(v):
        if isinstance(v, dict):
            for a in v:
                if (c := edits.get((v.get(':db/id'), str(a)))):
                    assert v[a] == c['before']
                    v[a] = c['after']
                else:
                    update(v[a])
        elif isinstance(v, list):
            for child in v:
                update(child)
    update(after)
    save('proposed-lessons.json', after)
    ids = lambda kind: sorted(e for e, v in entities.items() if ':' + kind + '/id' in v)
    groups = [['questions', QUESTION_PULL, ids('question')], ['tutorials', '[*]', ids('tutorial')],
              ['activities', '[* {:activity/steps [*]}]', ids('activity')],
              ['knowledge-points', '[* {:knowledge-point/canonical-example [:db/id]} {:knowledge-point/questions [:db/id]}]', ids('knowledge-point')]]
    (HERE / 'native-pulls.edn').write_text(dumps(groups) + '\n')
    digest = hashlib.sha256(text.encode()).hexdigest()
    plan = {'database': 'math', 'lineage': '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1',
            'snapshot_basis': 3573, 'source': ':agent/codex', 'source_eid': source_eid,
            'transaction_sha256': digest, 'changes': len(changes),
            'changed_entities': len({c['entity'] for c in changes}),
            'by_attribute': dict(__import__('collections').Counter(c['attribute'] for c in changes)),
            'counts': counts, 'algebra_chain_pairs_checked': pairs,
            'historical_responses_rewritten': 0, 'missing_material_excluded': True}
    save('plan.json', plan)
    print(json.dumps(plan, indent=2))


if __name__ == '__main__':
    prepare()
