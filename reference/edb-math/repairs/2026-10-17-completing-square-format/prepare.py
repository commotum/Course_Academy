"""Prepare (never submit) the Completing the Square presentation repair."""
from __future__ import annotations

import copy
import difflib
import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'Cargo.toml').exists())
sys.path.insert(0, str(ROOT))
from capture.scripts.database.edn import dumps, kw, loads
from capture.scripts.database.client import QUESTION_PULL

HERE = Path(__file__).resolve().parent
SOURCE = ':agent/codex'
SOURCE_TEMP = 'codex-format-repair'
ATTRS = (':question/problem', ':question/worked-solution', ':tutorial/content')
MATH = re.compile(r'\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])*?(?<!\\)\$')
ALIGNED = re.compile(r'\\begin\{aligned\}([\s\S]*?)\\end\{aligned\}')


def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False, default=str) + '\n')


def flatten(value):
    entities = {}

    def visit(v):
        if isinstance(v, dict):
            if ':db/id' in v:
                entities.setdefault(v[':db/id'], {}).update(v)
            for child in v.values():
                visit(child)
        elif isinstance(v, list):
            for child in v:
                visit(child)

    visit(value)
    return entities


def repair_underbraces(text):
    count = 0
    marker = '_{⏟}'
    while marker in text:
        end = text.index(marker)
        assert text[end - 1] == '}'
        depth, start = 0, None
        for pos in range(end - 1, -1, -1):
            if text[pos] == '}':
                depth += 1
            elif text[pos] == '{':
                depth -= 1
                if depth == 0:
                    start = pos
                    break
        assert start is not None
        # Reuse the entire original braced expression as the command argument.
        text = text[:start] + r'\underbrace' + text[start:end] + text[end + len(marker):]
        count += 1
    return text, count


def repair_alignment(text, chains):
    def aligned(match):
        rows = [row.strip() for row in match[1].split(r'\\')]
        if len(rows) == 1:
            return match[0]
        parts = [row.split('&') for row in rows]
        assert all(len(part) == 2 for part in parts), match[0]
        assert all(right.strip() == '=' for _, right in parts[:-1]), match[0]
        suffix = parts[-1][1].strip()
        assert suffix in ('', '.', r'\,✓'), suffix
        expressions = [left.strip() for left, _ in parts]
        chains.append(expressions)
        output = [expressions[0] + ' &= ' + expressions[1]]
        output += ['&= ' + expr for expr in expressions[2:]]
        output[-1] += suffix
        return '\\begin{aligned}\n' + ' \\\\\n'.join(output) + '\n\\end{aligned}'

    return ALIGNED.sub(aligned, text)


def normalize_inline_punctuation(text):
    count = 0

    def math(match):
        nonlocal count
        value = match[0]
        if not value.startswith('$') or value.startswith('$$'):
            return value
        body = value[1:-1]
        ending = re.search(r'([,.;:?!]+)\s*$', body)
        if ending:
            count += 1
            return '$' + body[:ending.start()].rstrip() + '$' + ending[1]
        return value

    return MATH.sub(math, text), count


def validate_math(text):
    remaining = MATH.sub('', text)
    assert not re.search(r'(?<!\\)\$|\\[\[\]()]', remaining), remaining
    for match in MATH.finditer(text):
        depth = 0
        for char in re.sub(r'\\[{}]', '', match[0]):
            depth += (char == '{') - (char == '}')
            assert depth >= 0, match[0]
        assert depth == 0, match[0]


def prepare():
    snapshot = loads((HERE / 'evidence/lesson.edn').read_text())
    entities = flatten(snapshot)
    questions = sorted(e for e, v in entities.items() if ':question/id' in v)
    tutorials = sorted(e for e, v in entities.items() if ':tutorial/id' in v)
    assert len(questions) == 77 and len(tutorials) == 2
    source_rows = loads((HERE / 'evidence/source.edn').read_text())
    assert len(source_rows) in (0, 1)
    source_eid = source_rows[0][0][':db/id'] if source_rows else None
    changes, chains, counts = [], [], {'underbraces': 0, 'aligned_environments': 0,
                                     'prompt_separations': 0, 'wording': 0,
                                     'parenthesis_groups': 0, 'inline_punctuation': 0}
    after = copy.deepcopy(snapshot)
    for eid in questions + tutorials:
        entity = entities[eid]
        for attr in ATTRS:
            if attr not in entity:
                continue
            old = entity[attr]
            new = old
            # These groups are valid TeX; remove only the captured closing-paren grouping.
            counts['parenthesis_groups'] += new.count('{)}')
            new = new.replace('{)}', ')')
            new, n = repair_underbraces(new)
            counts['underbraces'] += n
            n = len(chains)
            new = repair_alignment(new, chains)
            counts['aligned_environments'] += len(chains) - n
            new, n = normalize_inline_punctuation(new)
            counts['inline_punctuation'] += n
            if attr == ':question/problem':
                if eid in (17592186069187, 17592186511861, 17592186069188):
                    assert new.count('constant.$') == 1
                    new = new.replace('constant.$', 'constant.\n\n$')
                    counts['prompt_separations'] += 1
                if eid == 17592186069169:
                    assert new.count('$.$') == 1
                    new = new.replace('$.$', '$.\n\n$')
                    counts['prompt_separations'] += 1
                if eid == 17592186532655:
                    before = 'the sum of a perfect square and a constant'
                    assert new.count(before) == 1
                    new = new.replace(before, 'the difference between a perfect square and a constant')
                    counts['wording'] += 1
                assert re.findall(r'\{\{[^}]+\}\}', new) == re.findall(r'\{\{[^}]+\}\}', old)
            validate_math(new)
            assert '⏟' not in new and '{)}' not in new
            if old != new:
                changes.append({'entity': eid, 'attribute': attr, 'before': old, 'after': new})

    assert counts['underbraces'] == 30
    assert counts['aligned_environments'] == 67
    assert counts['prompt_separations'] == 4 and counts['wording'] == 1

    # Check the algebra of each regrouped equation chain independently.
    from sympy import expand
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
    algebra_pairs = 0
    for expressions in chains:
        parsed = []
        for expr in expressions:
            expr = expr.replace(r'\cdot', '*').replace(r'\,', '').replace('{', '(').replace('}', ')').replace('^', '**')
            assert re.fullmatch(r'[xyzta0-9+*().\s-]+', expr), expr
            parsed.append(parse_expr(expr, transformations=standard_transformations + (implicit_multiplication_application,)))
        for left, right in zip(parsed, parsed[1:]):
            assert expand(left - right) == 0, expressions
            algebra_pairs += 1

    forms = []
    if source_eid is None:
        # This identity is already the Codex contributor convention used by
        # capture/scripts/prepare_encompassing_weights.py; math has not installed it.
        forms.append({kw('db/id'): SOURCE_TEMP, kw('db/ident'): kw(SOURCE),
                      kw('db/doc'): 'Codex agent contributions to Course Academy content.'})
    forms += [[kw('db/cas'), c['entity'], kw(c['attribute']), c['before'], c['after']] for c in changes]
    for eid in sorted({c['entity'] for c in changes}):
        spec = 'question/validate' if eid in questions else 'tutorial/validate'
        forms.append([kw('db/ensure'), eid, kw(spec)])
    transaction = '[\n' + '\n'.join(' ' + dumps(form) for form in forms) + '\n]\n'
    (HERE / 'transaction.edn').write_text(transaction)
    assert loads(transaction) == forms
    save('changes.json', changes)
    diffs = []
    for c in changes:
        diffs += difflib.unified_diff([line + '\n' for line in c['before'].splitlines()],
                                      [line + '\n' for line in c['after'].splitlines()],
                                      fromfile=f"{c['entity']} {c['attribute']} before",
                                      tofile=f"{c['entity']} {c['attribute']} proposed", lineterm='\n')
        diffs.append('\n')
    (HERE / 'changes.diff').write_text(''.join(diffs))

    def replace(v):
        if isinstance(v, dict):
            for c in changes:
                if v.get(':db/id') == c['entity'] and c['attribute'] in v:
                    assert v[c['attribute']] == c['before']
                    v[c['attribute']] = c['after']
            for child in v.values():
                replace(child)
        elif isinstance(v, list):
            for child in v:
                replace(child)
    replace(after)
    save('proposed-lesson.json', after)
    (HERE / 'proposed-lesson.edn').write_text(dumps(after) + '\n')
    # Verify the snapshot changed only at the intended scalar attributes.
    actual = flatten(after)
    # Nested refs in the flattened map can be repeated projections. The native
    # preview below verifies the full question/answer subtrees independently.
    for c in changes:
        assert actual[c['entity']][c['attribute']] == c['after']
    assert all(actual[e] == entities[e] for e in entities if ':answer/id' in entities[e] or ':answer-field/id' in entities[e])

    (HERE / 'native-pulls.edn').write_text(dumps([
        ['questions', QUESTION_PULL, questions],
        ['tutorials', '[*]', tutorials],
        ['activity', '[* {:activity/steps [*]}]', [17592186068977]],
        ['knowledge-points', '[* {:knowledge-point/canonical-example [:db/id]} {:knowledge-point/questions [:db/id]}]',
         sorted(e for e, v in entities.items() if ':knowledge-point/id' in v)],
    ]) + '\n')
    digest = hashlib.sha256(transaction.encode()).hexdigest()
    plan = {'database': 'math', 'lineage': '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1',
            'read_basis': 3519, 'source_ident': SOURCE, 'source_eid': source_eid,
            'source_argument_edn': dumps(SOURCE_TEMP) if source_eid is None else SOURCE,
            'bootstraps_codex_contributor': source_eid is None,
            'source_tempid': SOURCE_TEMP if source_eid is None else None,
            'endpoint': '/tmp/edb-math/writer.sock',
            'request_key': f'completing-square-format-b3519-{digest}',
            'transaction_sha256': digest, 'changed_attributes': len(changes),
            'changed_entities': len({c['entity'] for c in changes}),
            'by_attribute': {attr: sum(c['attribute'] == attr for c in changes) for attr in ATTRS},
            'fix_counts': counts, 'verified_algebra_pairs': algebra_pairs,
            'preserved_answers': 264, 'preserved_answer_fields': 102,
            'excluded': 'Missing worked solutions and answer keys; answer-value normalization; generator edits',
            'committed': False}
    save('plan.json', plan)
    print(json.dumps(plan, indent=2))


if __name__ == '__main__':
    prepare()
