"""Check every captured complete bank against current output, not runtime tables."""
from independent import *


def instance(q):
    ops = operations(q[':question/problem'])
    i = dict(matrix=[[int(x) for x in r] for r in matrices(q[':question/problem'])[0]],
             letter=re.search(r'augmented matrix \$(\w)', q[':question/problem'])[1])
    sid = q[':question/id']
    if len(ops) == 1:
        op = ops[0]
        i['template'] = op[0]
        if op[0] == 'swap':
            i['pair'] = list(op[1:])
        elif op[0] == 'scale':
            i.update(target=op[1], factor=str(op[2]))
            if sid == 'afe0707b-0259-50d7-a719-7a8d24334500':
                i['profile'] = 'source:' + sid
            else:
                i.update(columns=[0, 1, 2], extra_row=0)
        else:
            i.update(target=op[1], donor=op[2], coefficient=int(op[3]), profile='source:' + sid)
    else:
        a, b = ops
        i.update(template=a[0]+'-add', target=b[1], donor=b[2], coefficient=int(b[3]))
        if a[0] == 'swap':
            i.update(pair=list(a[1:]), profile='swap-donor' if b[2] in a[1:] else 'swap-recipient')
        else:
            i.update(scale=str(a[2]), profile='scale-donor')
    return i


def main():
    kp = json.load(open(JOB/'source/source.json'))['material']['kp']
    sources = [kp[':knowledge-point/canonical-example']] + kp[':knowledge-point/questions']
    results, records = [], []
    for q in sources:
        try:
            r = g.build(instance(q))
            got = r['question']; fields = q.get(':question/answer-fields', [])
            assert matrices(got[':question/problem'])[0] == matrices(q[':question/problem'])[0]
            assert operations(got[':question/problem']) == operations(q[':question/problem'])
            if fields:
                original = fields[0][':answer-field/choices']
                generated = got[':question/answer-fields'][0][':answer-field/choices']
                sb = [matrices(c[':answer/value'])[0] for c in original]
                gb = [matrices(c[':answer/value'])[0] for c in generated]
                assert len(sb) == len(gb) == 5
                assert sorted(map(str, sb)) == sorted(map(str, gb)), 'complete bank mismatch'
                if ':answer-field/correct' in fields[0]:
                    source_correct = next(c for c in original if c[':answer/id'] == key(q))
                    current_correct = next(c for c in generated if c[':answer/id'] == key(got))
                    assert matrices(source_correct[':answer/value']) == matrices(current_correct[':answer/value'])
            result = check(r)
            assert result['unique_correct'] and result['final_solution_correct'], result
            # Intermediate expanded calculations agree, including the new source.
            if q.get(':question/worked-solution'):
                old_stages = matrices(q[':question/worked-solution'], True)
                new_stages = matrices(got[':question/worked-solution'], True)
                assert old_stages == new_stages, 'worked-solution stages mismatch'
            records.append(r)
            results.append(dict(source_id=q[':question/id'], passed=True,
                                bank_size=len(fields[0][':answer-field/choices']) if fields else 0,
                                key_inferred=bool(fields and ':answer-field/correct' not in fields[0])))
        except Exception as e:
            results.append(dict(source_id=q[':question/id'], passed=False, error=repr(e)))
    save('source-replay-results.json', results)
    save('source-replays.json', records)
    repaired = {'afe0707b-0259-50d7-a719-7a8d24334500', '337ae2e1-4641-5c8b-9b2a-9435340f0134'}
    save('repaired-records.json', [r for r in records if set(r['generation']['source_question_ids']) & repaired])
    print(json.dumps(dict(tested=len(results), passed=sum(x['passed'] for x in results),
                         failures=[x for x in results if not x['passed']])))
    return int(not all(x['passed'] for x in results))


if __name__ == '__main__':
    raise SystemExit(main())
