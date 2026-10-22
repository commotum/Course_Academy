"""Retained strict source regression, strengthened with independent visible math witnesses."""
import copy
from fractions import Fraction
import json
from math import isqrt
from pathlib import Path
import random
import re
import sys
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import generator as g


def save(name, data):
    (ROOT / 'evidence' / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def selected(f):
    ref = f[':answer-field/correct']
    aid = ref[1] if isinstance(ref, list) else ref[':answer/id']
    return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id'] == aid)


def letters(value):
    return ''.join(s for s in 'NZQRC' if re.search(r'(?<![A-Za-z])' + s + r'(?![A-Za-z])', value))


def actual(record):
    fs = record['question'][':question/answer-fields']
    if fs[0][':answer-field/type'] == ':answer-field.type/radio':
        return letters(selected(fs[0]))
    keyed = {re.search(r'\(\$([NZQRC])\$\)', f[':answer-field/key'])[1]: selected(f) for f in fs}
    assert len(keyed) == 5
    return ''.join(s for s in 'NZQRC' if keyed[s] == 'true')


def prompt_value(record):
    return re.search(r'number \$(.*?)\$ belong', record['question'][':question/problem'])[1].strip()


def oracle(record):
    tex = prompt_value(record)
    if 'pi' in tex:
        return 'RC'
    if 'sqrt' in tex:
        n = int(re.search(r'\{(-?\d+)\}', tex)[1])
        if n < 0:
            return 'C'
        # Independent square witness by finite multiplication, no generator metadata.
        roots = [r for r in range(n + 1) if r * r == n]
        if not roots:
            return 'RC'
        x = Fraction(roots[0])
    elif 'frac' in tex:
        n, d = map(int, re.search(r'frac\{(\d+)\}\{(\d+)\}', tex).groups())
        x = Fraction(-n if tex.startswith('-') else n, d)
    else:
        x = Fraction(tex)
    if x.denominator != 1:
        return 'QRC'
    return 'NZQRC' if x > 0 else 'ZQRC'


def imaginary_witness(record):
    tex = prompt_value(record)
    magnitude = -int(re.search(r'\{(-?\d+)\}', tex)[1])
    solution = record['question'][':question/worked-solution']
    match = re.search(re.escape(tex) + r'=(.*?)\\text\{i\}', solution)
    assert match, 'missing exact imaginary equality'
    coefficient = match[1]
    # Accept exact integer, sqrt(m), and a*sqrt(m) coefficients; square it independently.
    root = re.fullmatch(r'(\d*)\\sqrt\{(\d+)\}', coefficient)
    squared = (int(root[1] or '1') ** 2 * int(root[2])) if root else int(coefficient or '1') ** 2
    assert squared == magnitude, (tex, coefficient, squared)
    assert actual(record) == oracle(record) == 'C'
    assert 'nonzero' in solution and 'N,Z,Q,' in solution


def main():
    sources = json.loads((ROOT / 'evidence/source-questions.json').read_text())
    replay = g.replay_sources()
    by_id = {r['generation']['source_replay']: r for r in replay}
    assert len(by_id) == len(replay) == len(sources), 'every supplied question must replay exactly once'
    source_results = []
    for source in sources:
        sid = source[':question/id']
        assert sid in by_id, ('supplied source absent', sid)
        record = by_id[sid]
        q = record['question']
        assert q[':question/problem'] == g.normalize_prose(source[':question/problem'])
        expected_fields = source[':question/answer-fields']
        assert len(q[':question/answer-fields']) == len(expected_fields)
        for f, sf in zip(q[':question/answer-fields'], expected_fields):
            assert f[':answer-field/key'] == sf[':answer-field/key']
            assert f[':answer-field/type'] == sf[':answer-field/type'][':db/ident']
            assert [a[':answer/value'] for a in f[':answer-field/choices']] == [a[':answer/value'] for a in sf[':answer-field/choices']], ('complete bank mismatch', sid)
            if ':answer-field/correct' in sf:
                assert selected(f) == sf[':answer-field/correct'][':answer/value'], ('source key mismatch', sid)
        assert actual(record) == oracle(record), ('math mismatch', sid)
        if source.get(':question/worked-solution'):
            assert q[':question/worked-solution'] == g.normalize_prose(source[':question/worked-solution'])
        source_results.append({'source': sid, 'memberships': actual(record), 'complete_bank_prompt_key_available_solution_match': True})
    # Source order must not assign somebody else's parameters to the retained prompt.
    original = g.DATA['questions']
    try:
        g.DATA['questions'] = list(reversed(copy.deepcopy(original)))
        reordered = g.replay_sources()
        for record in reordered:
            prior = by_id[record['generation']['source_replay']]
            assert record['question'] == prior['question']
            assert record['generation']['parameters'] == prior['generation']['parameters']
            assert actual(record) == oracle(record)
    finally:
        g.DATA['questions'] = original
    # Exact latest counterexample, then its entire bounded supported negative family.
    negatives = [g.build({'family': 'radical', 'n': -m}) for m in range(1, 145)]
    for record in negatives:
        imaginary_witness(record)
    # Exercise the sampler branch deterministically for every supported negative magnitude.
    class NegativeMagnitude:
        def __init__(self, m): self.m = m
        def choice(self, values): return 'nonreal' if 'nonreal' in values else 'radical'
        def randint(self, low, high):
            assert (low, high) == (1, 144)
            return self.m
    for m in range(1, 145):
        p = g.sample_parameters(NegativeMagnitude(m))
        record = g.build(p)
        assert prompt_value(record) == r'\sqrt{' + str(-m) + '}'
        imaginary_witness(record)
    sample = g.generate(count=40, seed=229173)
    for record in sample:
        assert actual(record) == oracle(record)
        if prompt_value(record).startswith(r'\sqrt{-'):
            imaginary_witness(record)
    assert any(re.search(r'\{-(\d+)\}', prompt_value(r)) and isqrt(int(re.search(r'\{-(\d+)\}', prompt_value(r))[1])) ** 2 != int(re.search(r'\{-(\d+)\}', prompt_value(r))[1]) for r in sample), 'ordinary sampling must exercise nonsquare negatives'
    save('source-replay-records.json', replay)
    save('negative-records.json', negatives)
    save('sample-records.json', sample)
    save('source-acceptance-results.json', {'failures': [], 'sources': source_results, 'order_independent': True, 'negative_domain_tested': [-144, -1], 'negative_records': len(negatives), 'sampler_negative_branches': 144, 'normal_sample': len(sample), 'oracle': 'visible prompt exact rational arithmetic and square witnesses; visible imaginary coefficient squared against radicand magnitude'})
    print(json.dumps({'sources': len(replay), 'negative_domain': len(negatives), 'normal_sample': len(sample), 'failures': 0}))


if __name__ == '__main__':
    main()
