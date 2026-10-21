"""Small independent math, role-change, shortcut, and inventory checks."""
from independent import *
from collections import Counter


def probes(records):
    result = {}
    for template in sorted({r['generation']['template'] for r in records}):
        group = [r for r in records if r['generation']['template'] == template]
        positions = Counter()
        role_positions = {}
        hits = Counter()
        letters = {}
        for r in group:
            q = r['question']; cs = q[':question/answer-fields'][0][':answer-field/choices']
            k = next(n for n, c in enumerate(cs) if c[':answer/id'] == key(q))
            positions[k+1] += 1
            # Visible prompt, not instance metadata, defines the role subgroup.
            ops = operations(q[':question/problem'])
            role = str([(op[0], op[1:3] if op[0] == 'swap' else op[1]) for op in ops])
            role_positions.setdefault(role, Counter())[k+1] += 1
            letter = re.search(r'augmented matrix \$(\w)', q[':question/problem'])[1]
            letters.setdefault(letter, Counter())[k+1] += 1
            mags = [sum(abs(x) for row in matrices(c[':answer/value'])[0] for x in row) for c in cs]
            for cue, pick in [('first-position', 0), ('largest-magnitude', max(range(5), key=lambda n:mags[n])),
                              ('smallest-magnitude', min(range(5), key=lambda n:mags[n]))]:
                hits[cue] += pick == k
        assert len(positions) > 1, (template, positions)
        assert all(v < len(group) for v in hits.values()), (template, hits)
        result[template] = dict(count=len(group), key_positions=dict(positions),
                                role_positions=role_positions, letter_positions=letters,
                                shortcut_hits=dict(hits), baseline=0.2)
    return result


def main():
    rng = random.Random(846217)
    samples = [g.generate(rng, difficulty=d, seed=846217)
               for d, n in [('easy', 40), ('moderate', 8), ('hard', 10)] for _ in range(n)]
    # Controlled changes keep entries constant; independent parsing checks all keys.
    controls, findings = [], []
    for template in ('swap', 'scale', 'add'):
        base = next(r for r in samples if r['generation']['template'] == template)
        i = copy.deepcopy(base['generation']['instance'])
        a = g.build(i)
        j = copy.deepcopy(i)
        if template == 'swap':
            j['pair'] = next(p for p in [[0,1],[0,2],[1,2]] if p != j['pair'])
        else:
            j['target'] = (j['target']+1) % len(j['matrix'])
            if template == 'add' and j['target'] == j['donor']:
                j['target'], j['donor'] = i['donor'], i['target']
        b = g.build(j)
        z = dict(i, letter='B' if i['letter'] != 'B' else 'C')
        c = g.build(z)
        assert expected(a['question']) != expected(b['question'])
        assert a['question'][':question/problem'] != b['question'][':question/problem']
        assert a['question'][':question/worked-solution'] != b['question'][':question/worked-solution']
        assert expected(a['question']) == expected(c['question'])
        # Selecting another coefficient from a fixed comparison bank must move the key.
        if template != 'swap':
            w = copy.deepcopy(i)
            scalar, wrong = ('factor', 'wrong_factors') if template == 'scale' else ('coefficient', 'wrong_coefficients')
            w[scalar], w[wrong][0] = w[wrong][0], w[scalar]
            d = g.build(w)
            assert sorted(x[':answer/value'] for x in a['question'][':question/answer-fields'][0][':answer-field/choices']) == sorted(x[':answer/value'] for x in d['question'][':question/answer-fields'][0][':answer-field/choices'])
            assert key(a['question']) != key(d['question'])
            controls.append(d)
        controls += [a, b, c]
        findings.append(dict(template=template, changed_target_changes_result=True,
                             renaming_preserves_result=True))
    replays = json.load(open(OUT/'source-replays.json'))
    checks = [check(r) for r in replays + samples + controls]
    assert all(c['unique_correct'] and c['final_solution_correct'] for c in checks)
    # Guard exact source banks against silently reusing literals for new mathematics.
    repaired = json.load(open(OUT/'repaired-records.json'))
    guards = []
    for r in repaired:
        i = copy.deepcopy(r['generation']['instance']); i['matrix'][0][0] += 1
        try:
            g.build(i)
        except ValueError:
            guards.append(dict(profile=i['profile'], changed_parameters_rejected=True))
        else:
            raise AssertionError('source-only bank leaked into modified parameters')
    save('math-results.json', checks)
    save('samples.json', samples)
    save('easy-samples.json', [r for r in samples if r['generation']['difficulty'] == 'easy'])
    save('counterfactual-records.json', controls)
    save('counterfactual-results.json', findings)
    save('source-profile-guards.json', guards)
    save('shortcut-before.json', probes(samples))
    cases = []
    for n, r in enumerate(repaired + controls):
        q = r['question']; want = expected(q)
        cases.append(dict(label=f'changed-profile-or-counterfactual-{n}', record=r, checks=[
            dict(submitted_answer_id=c[':answer/id'],
                 expected='accepted' if matrices(c[':answer/value'])[0] == want else 'rejected',
                 purpose='visible prompt entrywise row-operation witness')
            for c in q[':question/answer-fields'][0][':answer-field/choices']]))
    save('grader-input.json', cases)
    inv = json.load(open(JOB/'source/inventory.json'))
    source_ids = {q[':question/id'] for q in json.load(open(JOB/'source/source.json'))['material']['kp'][':knowledge-point/questions']}
    others = [q for q in inv['questions'] if q[':question/id'] not in source_ids]
    save('affected-inventory.json', dict(affected_questions=[]))
    save('inventory-audit.json', dict(basis=inv['basis'], stored_count=len(inv['questions']),
         original_source_count=len(inv['questions'])-len(others),
         non_source_records=[dict(question_id=q[':question/id'], entity_id=q[':db/id'],
                                  has_generation_metadata=any('generation' in k for k in q)) for q in others],
         finding='The demonstrated failures are absent replay profiles, not a demonstrated defective generated stored record.',
         limits='Eight non-source records lack generation metadata. No affected generated inventory instance is demonstrated; this is not a verified absence of other inventory defects. Source originals are excluded.'))
    print(json.dumps(dict(math_records=len(checks), generated_sample=len(samples),
                         controls=len(controls), grader_cases=len(cases), retained_guards=len(guards))))


if __name__ == '__main__':
    main()
