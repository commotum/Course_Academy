"""Retain review finding 2d563278b967b4712347; test current visible records."""
import importlib.util, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from visible_math import expr, eq, mathcheck, s, x
spec = importlib.util.spec_from_file_location('generator', ROOT/'17592186087879.py')
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

def run():
    rows, results = [], []
    for a in [1, 2, 3, 4, 5, 6]:
        p = {'a': a, 'b': 2, 'h': -1}
        try:
            r = g.generate('easy', seed=991, parameters=p)
            rows.append(r)
            values = []
            for f in r['question'][':question/answer-fields']:
                values.append(expr(next(z[':answer/value'] for z in f[':answer-field/choices']
                    if z[':answer/id'] == f[':answer-field/correct'][1])))
            checked = mathcheck(r)
            passed = checked['passed'] and eq(values[0], s.exp(a*x)) and eq(values[1], 2-3*s.exp(-a*x))
            results.append({'parameters': p, 'passed': passed, 'visible_math': checked})
        except Exception as e:
            results.append({'parameters': p, 'passed': False, 'exception': str(e)})
    # Explicit-parameter support alone must not conceal a still-fixed sampler.
    from visible_math import promptdata
    normal = [g.generate('easy', seed=400+i) for i in range(36)]
    support=set(); ranks=set()
    for r in normal:
        p, q, t, h = promptdata(r)
        f = r['question'][':question/answer-fields'][0]
        values=[expr(a[':answer/value']) for a in f[':answer-field/choices']]
        right=values[next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])]
        assert eq(s.diff(right,x),p*right)
        support.add(int(p))
        slopes=[s.simplify(s.diff(v,x)/v) for v in values]
        ranks.add(sorted(slopes).index(p))
    results.append({'case':'normal sampler and IF rank shortcut',
                    'coefficients':sorted(support),'correct_exponent_ranks':sorted(ranks),
                    'passed':support==set(range(1,7)) and ranks==set(range(4))})
    (ROOT/'evidence').mkdir(exist_ok=True)
    (ROOT/'evidence/coefficient-records.json').write_text(json.dumps(rows, indent=2))
    (ROOT/'evidence/coefficient-normal-records.json').write_text(json.dumps(normal, indent=2))
    (ROOT/'evidence/coefficient-results.json').write_text(json.dumps(results, indent=2))
    print(json.dumps({'passed': all(v['passed'] for v in results), 'cases': len(results),
                      'failures': [v for v in results if not v['passed']]}))
    assert all(v['passed'] for v in results), 'Eligible easy coefficient change failed'

if __name__ == '__main__':
    run()
