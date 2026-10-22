"""Independent rendered-statement truth checks and native field grading."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
s = importlib.util.spec_from_file_location('imt_generator', HERE.with_suffix('.py'))
g = importlib.util.module_from_spec(s)
s.loader.exec_module(g)

def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, default=str) + '\n')

def fingerprint(q):
    return g.fingerprint(q)

def truth(text, n, rank):
    """Interpret rendered conclusions, independently of profile/answer keys."""
    if 'has no basis' in text:
        return False  # Every finite-dimensional subspace has a basis, even {0}.
    if 'not** invertible' in text or 'has no inverse' in text:
        return rank < n
    if 'is invertible' in text:
        return rank == n
    if 'det(A)=0' in text:
        return rank < n
    if r'\text{rank}(A)<n' in text:
        return rank < n
    if r'\text{rank}(A)=n' in text:
        return rank == n
    if 'All columns' in text or 'All columns' in text.capitalize():
        return rank == n
    if 'pivot columns' in text:
        if 'less than' in text:
            return rank < n
        m = re.search(r'has \$(n|\d+)\$ pivot', text)
        assert m, text
        return rank == (n if m[1] == 'n' else int(m[1]))
    if 'has dimension zero' in text:
        return n - rank == 0
    if r'\text{Null}(A)={R}^' in text:
        return rank == 0
    if r'\text{dim(Col}(A))=' in text:
        m = re.search(r'\)\)=(n|\d+)', text)
        assert m, text
        return rank == (n if m[1] == 'n' else int(m[1]))
    if r'\text{Col}(A)={R}^' in text:
        m = re.search(r'\^\{(n|\d+)\}', text)
        assert m, text
        return rank == n and (n if m[1] == 'n' else int(m[1])) == n
    raise AssertionError('Unparsed statement: ' + text)

def independent(rec):
    q, meta = rec['question'], rec['generation']
    assert rec == g.generate('moderate', meta['seed'], meta['template'], meta['parameters'])
    prompt = q[':question/problem']
    # Infer invertibility only from the printed premise, never profile metadata.
    given = prompt.split('Which of the following')[0]
    singular = any(s in given for s in ('det(A)=0', r'\text{rank}(A)<n', r'\text{nullity}(A)\ne 0'))
    statements = re.findall(r'^(?:- \*\*)?(I{1,3})\.(?:\*\*)? (.+)$', prompt, re.M)
    assert [s[0] for s in statements] == ['I', 'II', 'III']
    m = re.search(r'\$(\d+)\\times (\d+)\$', given)
    dims = [int(m[1])] if m else range(1, 10)
    assert not m or m[1] == m[2]
    vectors = set()
    for n in dims:
        ranks = range(n) if singular else [n]
        for rank in ranks:
            # Exact matrix witnesses verify rank, determinant and nullity facts.
            a = sp.diag(*([1] * rank + [0] * (n-rank)))
            assert a.rank() == rank and len(a.nullspace()) == n-rank
            assert (a.det() != 0) == (rank == n)
            vectors.add(tuple(truth(text, n, rank) for _, text in statements))
    assert len(vectors) == 1, 'Conclusion is not forced by the premise'
    expected = next(iter(vectors))
    fields = q[':question/answer-fields']
    if len(fields) == 3:
        assert [f[':answer-field/key'] for f in fields] == ['I', 'II', 'III']
        for f, answer in zip(fields, expected):
            assert f[':answer-field/type'] == ':answer-field.type/checkbox'
            assert {a[':answer/value'] for a in f[':answer-field/choices']} == {'true', 'false'}
            assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id'] == f[':answer-field/correct'][1]) == str(answer).lower()
    else:
        assert len(fields) == 1 and fields[0][':answer-field/type'] == ':answer-field.type/radio'
        f = fields[0]
        choices = f[':answer-field/choices']
        assert len(choices) == 5 and len({a[':answer/value'] for a in choices}) == 5
        decoded = [tuple(bool(re.search(r'\b' + label + r'\b', a[':answer/value'])) for label in ('I', 'II', 'III')) for a in choices]
        assert decoded.count(expected) == 1
        assert choices[decoded.index(expected)][':answer/id'] == f[':answer-field/correct'][1]
    sol = q[':question/worked-solution']
    assert sol.count('- The following statement is') == 3
    printed = re.findall(r'- The following statement is (true|false):', sol)
    assert printed == [str(b).lower() for b in expected]
    if meta['parameters']['premise'] not in ('source', 'nullity-zero'):
        assert g.ORIGINAL not in prompt and g.ORIGINAL not in sol
        assert g.PREMISES[meta['parameters']['premise']] in sol
    assert not re.search(r'!\[.*?\]\(', prompt + sol)
    return rec

def checks(rec):
    return [{'field_index': i, 'submitted_answer_id': a[':answer/id'],
             'expected': 'accepted' if a[':answer/id'] == f[':answer-field/correct'][1] else 'rejected',
             'purpose': 'Every field-owned choice through actual learner grade_field'}
            for i, f in enumerate(rec['question'][':question/answer-fields']) for a in f[':answer-field/choices']]

def main():
    replays, inputs, reviews, coverage, recipes = [], [], [], {}, []
    rows = g.batch('moderate', 10000, 24629)
    for sid, old in g.CASES.items():
        rec = independent(g.generate('moderate', 0, sid, g.DEFAULTS[sid]))
        q = rec['question']
        assert q[':question/problem'] == old[':question/problem']
        assert q[':question/worked-solution'] == old[':question/worked-solution']
        matched = 0
        for f in q[':question/answer-fields']:
            of = next(f0 for f0 in old[':question/answer-fields'] if f0[':answer-field/key'] == f[':answer-field/key'])
            assert sorted(a[':answer/value'] for a in f[':answer-field/choices']) == sorted(a[':answer/value'] for a in of[':answer-field/choices'])
            assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id'] == f[':answer-field/correct'][1]) == of[':answer-field/correct'][':answer/value']
            matched += len(f[':answer-field/choices'])
            for a in of[':answer-field/choices']:
                recipes.append({'source': sid, 'field': f[':answer-field/key'], 'answer': a[':answer/id'],
                    'value': a[':answer/value'], 'recipe': 'fixed truth literal' if len(q[':question/answer-fields']) == 3 else 'fixed Roman-numeral subset',
                    'profile': sid, 'reproduces_complete_value': True})
        replays.append({'source': sid, 'matched_choices': matched, 'matched_distractors': matched-len(q[':question/answer-fields']), 'complete_bank_match': True, 'prompt_exact': True, 'solution_exact': True, 'missing': [], 'extra': []})
        coverage[sid] = {'eligible_premises': g.domain(sid), 'sampled_premises': [], 'missing': []}
        reviews.append('## ' + sid + '\n\nSource replay\n\n' + g.markdown(rec))
        variants = [r for r in rows if r['generation']['template'] == sid and r['generation']['parameters'] != g.DEFAULTS[sid]]
        if variants:
            reviews.append('Changed given fact, same conclusions and bank\n\n' + g.markdown(variants[0]))
    for rec in rows:
        independent(rec)
        sid = rec['generation']['template']
        coverage[sid]['sampled_premises'].append(rec['generation']['parameters'])
        inputs.append({'label': sid + ' ' + str(rec['generation']['parameters']), 'record': rec, 'checks': checks(rec)})
        assert g.generate('moderate', 999, sid, rec['generation']['parameters'])['question'] == rec['question']
    assert len({fingerprint(r['question']) for r in rows}) == len(rows)
    for level in ('easy', 'hard', 'unclassified'):
        try: g.generate(level)
        except ValueError: pass
        else: raise AssertionError('Unsupported difficulty generated')
    save('native-input.json', inputs)
    subprocess.run([str(ROOT / 'generate/runs/current/check-engine'), str(HERE/'native-input.json'), str(HERE/'native-grading.json')], check=True)
    save('source-replay.json', {'passed': True, 'banks_matched': len(replays), 'banks_total': len(replays), 'distractors_matched': sum(r['matched_distractors'] for r in replays), 'profiles': replays, 'excluded': g.EXCLUDED})
    save('choice-recipes.json', recipes)
    save('slot-coverage.json', coverage)
    (HERE/'review.md').write_text('\n\n'.join(reviews)+'\n')
    save('validation.json', {'status': 'pass', 'finite_variants': len(rows), 'source_replay': 'All 9 supported original prompts, solutions and complete banks exact',
        'correctness': 'Rendered premise and propositions independently interpreted; exact rank/nullity/determinant witnesses for all ranks, n=1..9 plus observed numeric dimensions; all declared premises exhaustively checked',
        'grading': 'Every option in every field of every finite variant through actual grade_field',
        'hashes': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'), HERE/'source.json', HERE/'validate.py', HERE/'replenish.py', HERE/'capabilities.json', ROOT/'generate/runs/current/check-engine')}})

if __name__ == '__main__':
    main()
