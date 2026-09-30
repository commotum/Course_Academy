#!/usr/bin/env python3
"""Audit every deferred MC question and stage only fully evidenced answer keys."""

import collections
import csv
import hashlib
import json
import re
from pathlib import Path

import reconcile_ma_questions as prior

ROOT = Path('.local/edb/reconciliation')
OUT = ROOT / 'followup-mc'
VAULT_INDEX = ROOT / 'vault-audit/index.json'
ORIGINAL = ROOT / 'questions/manifest.json'
REPAIRS = Path('/home/jake/Developer/study/util/ma_missing_answer_repairs.json')
LEDGER = Path('/home/jake/Developer/study/vault/MA/Questions.csv')
IMAGE = re.compile(r'!\[[^]]*\]\((<[^>]+>|[^\n]*?\.(?:png|jpe?g|gif|webp|svg))\)', re.I)
COURSES = prior.COURSES
MATH_VERIFIED_ADDED = {
    ('487', '12457'), ('1762', '12430'), ('1762', '12419'), ('2975', '88686'),
    ('1869', '47586'), ('3819', '95299'), ('3819', '94772'), ('4151', '38941'),
    ('3705', '124871'), ('2522', '106074'), ('3950', '148766'),
}
MATH_REJECTED_ADDED = {('759', '49796')}
REVIEWED_PROMPTS = {
    ('982', '49646'): ('f0b840ff7d463d0c65dcc7613640a4dfd4fbb522cf22792e9d3da38fdb38378c', '715ed9b9b808da01d4e61ed05505609aaf8e1f13ac22fe095d820d2896074e62'),
    ('982', '49648'): ('c32dddff2a6282ce3854007275f16ba0947d8d6f0a180af266324fba55ce02d5', '8768e0991898677f09221466aea49c9dc0437303295582866de7b6b99e8b677f'),
    ('1281', '49111'): ('b84ec16eb9f36308b9494334d97a48af880ec3cdc7ded9649cc3284de35faa4d', '0cd3c6a299d29d25b72492ef660b0a38770018d3c008cba61611803fc23331fc'),
    ('626', '5046'): ('90068afdba9fe2e3169b14837daa9fee38ca4aca61b33f06973b74325b650e98', '392cab80c22c83019bff2fcf91af8e31284b0e9ef2b3c7eba13ce9763ebc25c0'),
    ('626', '29741'): ('d0535f3edd7e79d57e31427e8fb7887287003644561ca72d66519829bff48f11', '83719a35e32e2e44a4485ecc51e32c38620ede475489a43f0d4b15e1b03b17c0'),
    ('1940', '37517'): ('b3ca9f94be53ff8ee9424f297f09aef3c0c4fe36a19e48613599ab4f2fdb1792', 'efa0a737b0f63401b295714e62a02f2da617e1055928b72b7d4503652773951b'),
    ('1173', '138974'): ('874e100ade653f630d198a4e82ea7b0279432576d6a271ef49c432025fb84fb9', 'e3bee8a60289bb558775e96a0e0a9603cf8a50aaec5890fbb0fb19951b4d2394'),
}
SET_REPAIRS = {('45', '1150'), ('1976', '180825'), ('1976', '180812'),
               ('1976', '180814'), ('1869', '140766'), ('1962', '141207')}
MANUAL_OVERRIDES = {
    ('1794', '33096'): ('1b513c23840c04e15e1120a409f3ccd19c30281bc0994e619adc5763970e1dd3', 1, 'mathml-tangent'),
    ('2056', '162226'): ('a7a72514d026580b2eb882f9cec4f02e9d3bfa5ecaf7be9401b084edf09fdf54', 4, 'mathml-integral'),
    ('2056', '161525'): ('538317b565cb5d7e24237f9876f34054cdfb539d6f47f74a528d9215cc724761', 1, 'mathml-integral'),
    ('2076', '121237'): ('29bd1e080a737d992b433aec95bce235f2cb912b857cab733aea5273ddfef80b', 2, 'full-sign-table'),
    ('2076', '121086'): ('c16126715f33b6e2bc8b26ac7e72db7b57bbc80e6c78f9d268686a9210f0beab', 1, 'full-sign-table'),
    ('3684', '121087'): ('c0c9552e1ca8c3e6f7bf44ae8d868142b2726ff4e0e8a94d5feb8d495a47e415', 4, 'full-sign-table'),
    ('3684', '120973'): ('bfd83de43ec8d11bae20823c1b501bae13cc1e4cf267c22bf36f6dc9310f8864', 3, 'full-sign-table'),
}
MATHML_CHOICES = {
    ('1794', '33096'): {
        2: r'\frac{2\sqrt{5}}{5}j - \frac{\sqrt{5}}{5}k',
        5: r'\frac{2\sqrt{5}}{5}i - \frac{\sqrt{5}}{5}k',
    },
    ('2056', '162226'): {
        1: r'\int_{0}^{1}\int_{0}^{\sqrt{y}}\int_{0}^{x^{2}+y}f(x,y,z)\,dz\,dx\,dy',
        2: r'\int_{0}^{1}\int_{y^{2}}^{\sqrt{y}}\int_{0}^{x^{2}+y}f(x,y,z)\,dz\,dx\,dy',
        3: r'\int_{0}^{1}\int_{\sqrt{y}}^{1}\int_{0}^{\sqrt{x^{2}+y}}f(x,y,z)\,dz\,dx\,dy',
        4: r'\int_{0}^{1}\int_{\sqrt{y}}^{1}\int_{0}^{x^{2}+y}f(x,y,z)\,dz\,dx\,dy',
        5: r'\int_{0}^{1}\int_{0}^{\sqrt{y}}\int_{0}^{\sqrt{x^{2}+y}}f(x,y,z)\,dz\,dx\,dy',
    },
    ('2056', '161525'): {
        1: r'\int_{0}^{1}\int_{\sqrt{z}}^{2-z}\int_{-z}^{x/3}f(x,y,z)\,dy\,dx\,dz',
        2: r'\int_{0}^{1}\int_{z}^{2-z}\int_{-z}^{x/3}f(x,y,z)\,dy\,dx\,dz',
        3: r'\int_{0}^{2}\int_{z^{2}}^{z}\int_{-z}^{x/3}f(x,y,z)\,dy\,dx\,dz',
        4: r'\int_{0}^{1}\int_{-z}^{z^{2}}\int_{-z}^{x/3}f(x,y,z)\,dy\,dx\,dz',
        5: r'\int_{0}^{2}\int_{\sqrt{z}}^{2-z}\int_{-z}^{x/3}f(x,y,z)\,dy\,dx\,dz',
    },
}


def _balanced_group(s, start):
    if start >= len(s) or s[start] != '{':
        return None
    depth = 0
    for i in range(start, len(s)):
        if s[i] == '{':
            depth += 1
        elif s[i] == '}':
            depth -= 1
            if depth == 0:
                return s[start + 1:i], i + 1
    return None


def normalize_fraction_commands(s):
    """Rewrite only syntactic TeX fractions, including nested braced groups."""
    for command in ('\\dfrac', '\\tfrac', '\\frac'):
        pos = 0
        while True:
            at = s.find(command, pos)
            if at < 0:
                break
            first = _balanced_group(s, at + len(command))
            second = _balanced_group(s, first[1]) if first else None
            if not second:
                pos = at + len(command)
                continue
            replacement = '(' + normalize_fraction_commands(first[0]) + ')/(' + normalize_fraction_commands(second[0]) + ')'
            s = s[:at] + replacement + s[second[1]:]
            pos = at + len(replacement)
    return s


def normalize_limit_subscripts(s):
    command = '\\lim_'
    pos = 0
    while True:
        at = s.find(command, pos)
        if at < 0:
            return s
        group = _balanced_group(s, at + len(command))
        if not group:
            pos = at + len(command)
            continue
        replacement = 'lim_(' + group[0] + ')'
        s = s[:at] + replacement + s[group[1]:]
        pos = at + len(replacement)


def normalized_content(s):
    s = normalize_fraction_commands(s)
    s = normalize_limit_subscripts(s)
    s = s.strip().replace('\u2212', '-').replace('−', '-').replace('\\,', '')
    s = re.sub(r'\[MATH:\s*(.*?)\]', r'\1', s, flags=re.S)
    s = re.sub(r'\$+', '', s)
    s = re.sub(r'\\(?:displaystyle|textstyle|left|right|limits)\b', '', s)
    for source, target in (('\\infty', '∞'), ('\\pi', 'π'), ('\\theta', 'θ'),
                           ('\\Delta', 'Δ'), ('\\cdot', '⋅'), ('\\int', '∫'),
                           ('\\pm', '±'), ('\\lvert', '|'), ('\\rvert', '|'),
                           ('\\mid', '|')):
        s = s.replace(source, target)
    s = re.sub(r'\\text\{([^{}]+)\}', r'\1', s)
    s = re.sub(r'\\sum_\{([^{}]+)\}\^\{([^{}]+)\}', r'∑_(\1)^(\2)', s)
    s = re.sub(r'\\(?:to|rightarrow)', '→', s)
    s = re.sub(r'\\(?:,|;|!|\s)', '', s)
    s = re.sub(r'\s+', '', s)
    # Braces around a one-character script are TeX formatting. Literal set
    # braces elsewhere are mathematical content and must remain significant.
    s = re.sub(r'([_^])\{([A-Za-z0-9])\}', r'\1\2', s)
    return s


def canonical_json(topic):
    return prior.DATA / topic / 'Source' / f'{topic}.json'


def companion_json(md, topic):
    return md.parent.parent / 'Source' / md.stem / f'{topic}.json'


def bridge_ready(md, topic, cache):
    key = (str(md), topic)
    if key not in cache:
        path = companion_json(md, topic)
        try:
            cache[key] = json.loads(path.read_text()) == json.loads(canonical_json(topic).read_text())
        except (OSError, ValueError):
            cache[key] = False
    return cache[key]


def source_asset_names(record):
    names = {Path(p.strip('<>')).name for p in IMAGE.findall(record['prompt'])}
    for t, value in record['options']:
        if t == 'image':
            names.add(Path(value).name)
        names.update(Path(p.strip('<>')).name for p in IMAGE.findall(value))
    return names


def asset_signature(text, md, record, cache):
    refs = IMAGE.findall(text)
    result = []
    provenance = []
    topic = record['topic']
    allowed = source_asset_names(record)
    for ref in refs:
        rel = Path(ref.strip('<>'))
        actual = rel if rel.is_absolute() else md.parent / rel
        if actual.is_file():
            result.append(hashlib.sha256(actual.read_bytes()).hexdigest())
            provenance.append({'path': str(actual.resolve()), 'mode': 'file-hash'})
            continue
        name = actual.name
        expected = md.parent.parent / 'Source' / md.stem / 'Images' / name
        canonical = prior.DATA / topic / 'Source' / 'Images' / name
        # A missing exported asset is bridged only when the exact expected vault
        # path is referenced, its companion capture equals DATA, the question
        # itself cites the same asset name, and the canonical bytes exist.
        if (actual.resolve() != expected.resolve() or name not in allowed or
                not bridge_ready(md, topic, cache) or not canonical.is_file()):
            return None, provenance
        result.append(hashlib.sha256(canonical.read_bytes()).hexdigest())
        provenance.append({'path': str(canonical), 'mode': 'verified-json-export-bridge',
                           'missing_vault_path': str(actual.resolve()),
                           'companion_json': str(companion_json(md, topic))})
    return tuple(result), provenance


def value_signature(text, md, record, cache):
    text = prior.clean_option(text)
    assets, evidence = asset_signature(text, md, record, cache)
    if assets is None:
        return None, evidence
    if record['topic'] == '2022' and record['id'] == '51466' and text.lstrip().startswith('|'):
        lines = [line for line in text.splitlines() if line.strip().startswith('|')]
        rows = [[re.sub(r'\s+', '', c.strip().strip('$').replace('−', '-'))
                 for c in line.strip().strip('|').split('|')] for line in lines]
        expected_x = ['-3', '-2', '-1', '0', '1', '2', '3']
        if len(rows) == 2 and rows[0] == ['x'] + expected_x and rows[1][0] == 'f(x)' and len(rows[1]) == 8:
            return ('table-values', tuple(rows[1][1:])), evidence
        if (len(rows) == 3 and rows[0] == [f'f({v})' for v in expected_x] and
                all(set(c) <= {'-', ':', ' '} for c in rows[1]) and len(rows[2]) == 7):
            return ('table-values', tuple(rows[2])), evidence
    return (normalized_content(IMAGE.sub('[image]', text)), assets), evidence


def source_choice_signature(t, value, record, cache):
    text = f'${value}$' if t == 'math' else f'![](<{value}>)' if t == 'image' else value
    md = prior.DATA / record['topic'] / f'{record["topic"]}.md'
    return value_signature(text, md, record, cache)[0]


def verify_added_option(quiz, md, record, registry, cache):
    opts = quiz.get('options') or []
    marked = [o for o in opts if o.get('correct') is True]
    if (len(opts) != len(record['options']) + 1 or len(marked) != 1 or
            registry.get('correct') != 'f' or marked[0].get('id') != 'f' or
            registry.get('add_option') != marked[0].get('content')):
        return {'diagnosis': 'registered-option-structure-mismatch'}
    source_sigs = [source_choice_signature(t, v, record, cache) for t, v in record['options']]
    existing = [o for o in opts if o is not marked[0]]
    vault_sigs = [value_signature(str(o.get('content', '')), md, record, cache)[0] for o in existing]
    if None in source_sigs or None in vault_sigs or collections.Counter(source_sigs) != collections.Counter(vault_sigs):
        return {'diagnosis': 'registered-option-existing-choices-mismatch'}
    source_md = prior.DATA / record['topic'] / f'{record["topic"]}.md'
    source_assets, _ = asset_signature(record['prompt'], source_md, record, cache)
    vault_assets, asset_evidence = asset_signature(quiz.get('content', ''), md, record, cache)
    if source_assets is None or vault_assets is None or source_assets != vault_assets:
        return {'diagnosis': 'registered-option-prompt-asset-mismatch'}
    if normalized_content(IMAGE.sub('[image]', record['prompt'])) != normalized_content(IMAGE.sub('[image]', quiz.get('content', ''))):
        return {'diagnosis': 'registered-option-prompt-text-mismatch'}
    return {'diagnosis': 'registered-added-option-fully-matched', 'asset_evidence': asset_evidence,
            'added_option': marked[0]['content']}


def candidate_evidence(entry, record, cache, repairs):
    quiz = entry['quiz']; md = Path(entry['path'])
    output = {'path': entry['path'], 'line': entry['line'], 'quiz_id': quiz.get('id'),
              'quiz_type': quiz.get('type')}
    if quiz.get('type') != 'radio':
        output['diagnosis'] = 'non-radio-quiz'
        return output
    options = quiz.get('options') or []
    marked = [o for o in options if o.get('correct') is True]
    output['key_markers'] = [o.get('id') for o in marked]
    if not marked:
        output['diagnosis'] = 'explicitly-unkeyed-radio'
        return output
    if len(marked) != 1:
        output['diagnosis'] = 'nonunique-key-marker'
        return output
    registry = repairs.get(f'{record["topic"]}:ma-{record["id"]}', {})
    if len(options) != len(record['options']):
        checked = verify_added_option(quiz, md, record, registry, cache) if registry else {'diagnosis': 'option-count-mismatch'}
        output.update(checked)
        output['registry'] = registry if registry else None
        return output
    src = [source_choice_signature(t, v, record, cache) for t, v in record['options']]
    vals = [value_signature(str(o.get('content', '')), md, record, cache) for o in options]
    output['asset_evidence'] = [e for _, ev in vals for e in ev]
    if any(v is None for v in src):
        output['diagnosis'] = 'missing-canonical-choice-asset'
        return output
    if any(v is None for v, _ in vals):
        output['diagnosis'] = 'unverified-vault-choice-asset'
        return output
    got = [v for v, _ in vals]
    if collections.Counter(src) != collections.Counter(got):
        output['diagnosis'] = 'choice-content-mismatch'
        output['source_choices'] = [list(x) if x else None for x in src]
        output['vault_choices'] = [list(x) if x else None for x in got]
        return output
    s_md = prior.DATA / record['topic'] / f'{record["topic"]}.md'
    s_assets, _ = asset_signature(record['prompt'], s_md, record, cache)
    q_assets, evidence = asset_signature(quiz.get('content', ''), md, record, cache)
    output['asset_evidence'].extend(evidence)
    if s_assets is None:
        output['diagnosis'] = 'missing-canonical-prompt-asset'
        return output
    if q_assets is None:
        output['diagnosis'] = 'unverified-vault-prompt-asset'
        return output
    if s_assets != q_assets:
        output['diagnosis'] = 'prompt-asset-content-mismatch'
        return output
    source_stem = normalized_content(IMAGE.sub('[image]', record['prompt']))
    vault_stem = normalized_content(IMAGE.sub('[image]', quiz.get('content', '')))
    reviewed = False
    if source_stem != vault_stem:
        pair = (record['topic'], record['id'])
        digests = (hashlib.sha256(record['prompt'].encode()).hexdigest(),
                   hashlib.sha256(quiz.get('content', '').encode()).hexdigest())
        reviewed = REVIEWED_PROMPTS.get(pair) == digests
        if not reviewed:
            output['diagnosis'] = 'prompt-content-mismatch'
            output['source_prompt'] = record['prompt']
            output['vault_prompt'] = quiz.get('content', '')
            return output
    correct_sig, _ = value_signature(str(marked[0].get('content', '')), md, record, cache)
    positions = [i for i, sig in enumerate(src, 1) if sig == correct_sig]
    if len(positions) != 1:
        output['diagnosis'] = 'ambiguous-duplicate-choice-value'
        output['matching_positions'] = positions
        return output
    output['diagnosis'] = 'matched-keyed-reviewed-prompt' if reviewed else 'matched-keyed-content'
    if reviewed:
        output['reviewed_prompt_source_sha256'], output['reviewed_prompt_vault_sha256'] = digests
    output['choice_index'] = positions[0]
    output['bridge_count'] = sum(e['mode'] == 'verified-json-export-bridge' for e in output['asset_evidence'])
    output['match'] = {'choice': positions[0], 'prompt': quiz.get('content', '').strip(),
                       'option_updates': {str(src.index(sig) + 1): str(o.get('content', '')).strip()
                                          for sig, o in zip(got, options)}}
    return output


def added_choice_forms(record, added):
    key = record['key']; aid = prior.uid('answer', f'{key}:1:6')
    temp = f'added-answer-{key}-6'
    fref = f'[:answer-field/id {prior.uid("field", f"{key}:1")}]'
    qref = f'[:question/id {prior.uid("question", key)}]'
    representation = 'math' if added.startswith('$') and added.endswith('$') else 'text'
    value = added[1:-1].strip() if representation == 'math' else added
    return [
        f'{{:db/id {prior.quote(temp)} :answer/id {aid} :answer/type :answer.type/{representation} :answer/value {prior.quote(value)} :db/ensure :answer/validate}}',
        f'{{:db/id {fref} :answer-field/choices [{prior.quote(temp)}]}}',
        f'{{:db/id {fref} :answer-field/correct {prior.quote(temp)}}}',
        f'{{:db/id {fref} :db/ensure :answer-field/validate}}',
        f'{{:db/id {qref} :db/ensure :question/validate}}',
    ]


def anchored_source_digest(record):
    return hashlib.sha256(json.dumps([record['prompt'], record['options']], ensure_ascii=False,
                                     separators=(',', ':')).encode()).hexdigest()


def set_repair_forms(record, choice):
    key = record['key']; forms = prior.forms(record, {'match': {'choice': choice, 'prompt': record['prompt']}})
    for ci, (kind, raw) in enumerate(record['options'], 1):
        if prior.seeded_choice_index(record, 1, ci) != ci:
            continue
        value = prior.clean_option(raw)
        if kind == 'text' and re.fullmatch(r'\$[^$]+\$', value, re.S):
            value = value[1:-1]
        if not value.startswith('{'):
            continue
        value = value.replace('{', r'\{').replace('}', r'\}')
        aref = f'[:answer/id {prior.uid("answer", f"{key}:1:{ci}")}]'
        if kind != 'math':
            forms.append(f'{{:db/id {aref} :answer/type :answer.type/math}}')
        forms.append(f'{{:db/id {aref} :answer/value {prior.quote(value)}}}')
        forms.append(f'{{:db/id {aref} :db/ensure :answer/validate}}')
    if (record['topic'], record['id']) in {('45', '1150'), ('1976', '180825'), ('1976', '180812'), ('1976', '180814')}:
        qref = f'[:question/id {prior.uid("question", key)}]'
        visible = record['prompt'].replace('{', r'\{').replace('}', r'\}')
        forms.append(f'{{:db/id {qref} :question/problem {prior.quote(visible)}}}')
    return forms


def manual_override_forms(record, choice, mode):
    key = record['key']; forms = prior.forms(record, {'match': {'choice': choice, 'prompt': record['prompt']}})
    if mode == 'full-sign-table':
        values = {}
        for ci, (_, raw) in enumerate(record['options'], 1):
            rows = [r for r in raw.splitlines() if r.strip().startswith('|')]
            if len(rows) != 2 or any(len(r.strip().strip('|').split('|')) != 2 for r in rows):
                raise ValueError(f'Unexpected sign table {record["topic"]}/{record["id"]}/{ci}')
            values[ci] = '|  |  |\n| --- | --- |\n' + '\n'.join(rows)
    else:
        values = MATHML_CHOICES[(record['topic'], record['id'])]
    canonical_values = {}
    for ci, value in values.items():
        canonical = prior.seeded_choice_index(record, 1, ci)
        if canonical in canonical_values and canonical_values[canonical] != value:
            raise ValueError(f'Conflicting repairs for duplicate answer {key}:1:{canonical}')
        canonical_values[canonical] = value
    for ci, value in canonical_values.items():
        aref = f'[:answer/id {prior.uid("answer", f"{key}:1:{ci}")}]'
        forms.append(f'{{:db/id {aref} :answer/value {prior.quote(value)}}}')
        forms.append(f'{{:db/id {aref} :db/ensure :answer/validate}}')
    return forms


def main():
    original = json.loads(ORIGINAL.read_text())
    index = json.loads(VAULT_INDEX.read_text())
    scope = json.loads((ROOT / 'scope.json').read_text())
    course_by_topic = {topic: course for course, topics in scope['topics_by_first_course'].items()
                       for topic in topics}
    repairs = json.loads(REPAIRS.read_text())
    ledger = {(r['topic-id'], r['question-id']): r for r in csv.DictReader(LEDGER.open(newline=''))}
    candidates = collections.defaultdict(list)
    for entry in index['quizzes']:
        qid = str(entry['quiz'].get('id', ''))
        if qid.startswith('ma-'):
            candidates[qid].append(entry)
    cache = {}
    records = {}
    pending = []
    for u in original['unresolved']:
        if u['reason'] != 'unmatched':
            continue
        topic = u['topic']
        if topic not in records:
            records[topic] = {r['id']: r for r in prior.topic_records(topic, {'56649', '156726'})}
        rec = records[topic][u['question']]
        if rec['format'] == 'multiple-choice':
            pending.append((u, rec))
    out = []
    staged = collections.defaultdict(list)
    counts = collections.Counter()
    for u, rec in pending:
        key = (rec['topic'], rec['id'])
        # ID retrieves possible copies. Topic membership and actual prompt plus
        # all option values are still checked before any key is transferred.
        files = set(index['topic_files'].get(rec['topic'], [])) | set(u['candidate_files'])
        entries = [e for e in candidates.get(f'ma-{rec["id"]}', []) if e['path'] in files]
        evidence = [candidate_evidence(e, rec, cache, repairs) for e in entries]
        good = [e for e in evidence if e['diagnosis'] in ('matched-keyed-content', 'matched-keyed-reviewed-prompt')]
        registered = [e for e in evidence if e['diagnosis'] == 'registered-added-option-fully-matched']
        keys = {e['choice_index'] for e in good}
        row = ledger.get(key, {})
        item = {'topic': rec['topic'], 'question': rec['id'], 'course': course_by_topic[rec['topic']],
                'format': 'multiple-choice', 'source_json': str(canonical_json(rec['topic'])),
                'candidate_count': len(entries), 'candidates': evidence,
                'ledger': {k: row.get(k, '') for k in ('quiz-status', 'quiz-answer-source', 'quiz-answer-labels', 'quiz-answer-rule')},
                'registry': repairs.get(f'{rec["topic"]}:ma-{rec["id"]}')}
        if len(keys) == 1:
            chosen = min(good, key=lambda e: (0 if '/MA/' in e['path'] else 1, len(e['path']), e['path']))
            item['classification'] = ('recoverable-reviewed-prompt-key' if
                                      chosen['diagnosis'] == 'matched-keyed-reviewed-prompt' else
                                      'recoverable-exact-content-key')
            item['choice_index'] = chosen['choice_index']
            item['selected'] = {'path': chosen['path'], 'line': chosen['line'], 'quiz_id': chosen['quiz_id']}
            # The same prior UUID and one-attribute update rules apply.
            course = item['course'] or 'unknown'
            staged[course].append(set_repair_forms(rec, chosen['choice_index']) if key in SET_REPAIRS
                                  else prior.forms(rec, {'match': chosen['match']}))
        elif registered and key in MATH_VERIFIED_ADDED:
            selected = min(registered, key=lambda e: (0 if '/MA/' in e['path'] else 1, e['path']))
            item['classification'] = 'recoverable-math-verified-added-choice'
            item['choice_index'] = 6
            item['selected'] = {'path': selected['path'], 'line': selected['line'], 'quiz_id': selected['quiz_id']}
            item['math_verification'] = 'independently checked against the captured problem and explicit repair registry'
            staged[item['course']].append(added_choice_forms(rec, selected['added_option']))
        elif registered and key in MATH_REJECTED_ADDED:
            item['classification'] = 'recoverable-corrected-original-choice'
            item['choice_index'] = 5
            item['selected'] = {'path': registered[0]['path'], 'line': registered[0]['line'], 'quiz_id': registered[0]['quiz_id']}
            item['math_verification'] = ('Topic 759 defines second-kind improper integrals with finite endpoint limits; '
                                         'only statement II qualifies. Registry-added f is mathematically wrong for this topic.')
            staged[item['course']].append(prior.forms(rec, {'match': {'choice': 5, 'prompt': rec['prompt']}}))
        elif key in MANUAL_OVERRIDES:
            digest, choice, mode = MANUAL_OVERRIDES[key]
            label = chr(ord('a') + choice - 1)
            markers = [e for e in evidence if e['key_markers'] == [label] and e['quiz_type'] == 'radio']
            if anchored_source_digest(rec) == digest and markers:
                item['classification'] = 'recoverable-html-mathml-reviewed'
                item['choice_index'] = choice
                item['selected'] = {'path': markers[0]['path'], 'line': markers[0]['line'],
                                    'quiz_id': markers[0]['quiz_id']}
                item['source_digest'] = digest
                item['math_verification'] = ('Independent review of original MathML and captured option values; '
                                             'vault choice rendering lost content.')
                staged[item['course']].append(manual_override_forms(rec, choice, mode))
            else:
                item['classification'] = 'manual-override-guard-failed'
        elif len(keys) > 1:
            item['classification'] = 'conflicting-keys-for-same-content'
        elif not evidence:
            item['classification'] = 'no-topic-matched-quiz-copy'
        else:
            diagnoses = collections.Counter(e['diagnosis'] for e in evidence)
            item['classification'] = min(diagnoses, key=lambda s: (-diagnoses[s], s))
        counts[item['classification']] += 1
        out.append(item)
    OUT.mkdir(parents=True, exist_ok=True)
    for p in OUT.glob('bulk-*.edn'):
        p.unlink()
    files = []
    for ci, course in enumerate(COURSES, 1):
        groups = staged[course]
        chunk = []; n = 1
        for group in groups:
            if chunk and len(chunk) + len(group) > 1000:
                name = f'bulk-{ci:02d}-{course}-{n:04d}.edn'
                (OUT / name).write_text('[\n' + '\n'.join(chunk) + '\n]\n')
                files.append(name); chunk = []; n += 1
            chunk.extend(group)
        if chunk:
            name = f'bulk-{ci:02d}-{course}-{n:04d}.edn'
            (OUT / name).write_text('[\n' + '\n'.join(chunk) + '\n]\n')
            files.append(name)
    report = {'total': len(out), 'counts': dict(counts), 'batch_files': files, 'questions': out}
    (OUT / 'manifest.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'total': len(out), 'counts': dict(counts), 'batch_files': len(files)}))


if __name__ == '__main__':
    main()
