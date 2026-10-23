"""Retained shortcut regression; parses current rendered options, no services."""
import sys, json, importlib.util, re
from pathlib import Path
from collections import defaultdict, Counter
import sympy as S
sys.dont_write_bytecode = True
ROOT = Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186059776/review-0-policy-2-b8c258069e86f407/relocated')
OUT = Path(__file__).resolve().parent / 'author-regression'
OUT.mkdir(parents=True, exist_ok=True)
spec = importlib.util.spec_from_file_location('generator', ROOT/'17592186059776.py')
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)

def number(t):
    return S.sympify(re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}', r'(\1/\2)', t.strip().replace(' ','')))

def matrices(t):
    return [S.Matrix([[number(c) for c in row.split('&')] for row in b.split(r'\\')])
            for b in re.findall(r'\\begin\{array\}\{cc\|c\}(.*?)\\end\{array\}', t, re.S)]

def features(r):
    f = r['question'][':question/answer-fields'][0]
    choices = f[':answer-field/choices']; key = f[':answer-field/correct'][1]
    ys = [matrices(a[':answer/value'])[0][1,2] for a in choices]
    pos = next(i for i,a in enumerate(choices) if a[':answer/id'] == key)
    hits = [a[':answer/id'] for a,y in zip(choices,ys) if y == sorted(ys)[1]] == [key]
    return {'template':r['generation']['template'], 'parameters':r['generation']['parameters'],
            'id':r['question'][':question/id'], 'rank':sorted(ys).index(ys[pos])+1,
            'position':pos+1, 'second_smallest_correct':hits, 'values':list(map(str,ys))}

def summarize(records):
    groups = defaultdict(list)
    for r in records:
        if r['generation']['parameters'] != [0,0]: groups[r['generation']['template']].append(features(r))
    return {sid:{'n':len(rows),'ranks':dict(Counter(x['rank'] for x in rows)),
                 'positions':dict(Counter(x['position'] for x in rows)),
                 'second_smallest_hits':sum(x['second_smallest_correct'] for x in rows)}
            for sid,rows in groups.items()}

def main():
    retained = [g.generate('easy',31817,sid,p)
                for sid in ['q-73544','q-73551','q-73554','q-73555']
                for p in [[0,0],[1,1],[2,3],[-3,-3],[3,-3],[-3,3]]]
    rows = [features(r) for r in retained]
    failures = [sid for sid in {x['template'] for x in rows}
                if all(x['second_smallest_correct'] for x in rows if x['template']==sid)]
    # Fixed seeds and parameters, independent of the implementation's RNG.
    # Boundary/zero/positive/negative cases cover the whole construction rule.
    params = [[-3,-3],[-3,3],[3,-3],[3,3],[0,1],[1,0],[2,3],[-2,2],[2,-2],[-1,-1],[1,1],[-3,0]]
    probes = [g.generate(q[':question/difficulty'][':db/ident'].split('/')[-1],31817+i,sid,p)
              for sid,q in g.CASES.items() for i,p in enumerate(params)]
    for r in probes:
        if 'and then solve' in r['question'][':question/problem']:
            pairs = [re.search(r'x=([^$]+)\$ and \$y=([^$]+)', a[':answer/value'])
                     for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
            assert len({(number(p[1]).q, number(p[2]).q) for p in pairs}) == 1, 'Number form leaks the key'
    summary = summarize(probes)
    (OUT/'retained-records.json').write_text(json.dumps(retained,indent=2))
    (OUT/'probe-records.json').write_text(json.dumps(probes,indent=2))
    (OUT/'results.json').write_text(json.dumps({'retained':rows,'families':summary,'failing_families':failures},indent=2))
    assert not failures, 'Retained numerical-rank shortcut: '+str(failures)
    for sid,s in summary.items():
        assert len(s['ranks']) > 1, (sid,'fixed correct numerical rank')
        assert len(s['positions']) > 1, (sid,'fixed correct authored position')
        assert s['second_smallest_hits'] < s['n'], (sid,'second-smallest shortcut')
    print(json.dumps({'retained':len(rows),'retained_shortcut_hits':sum(x['second_smallest_correct'] for x in rows),
                      'probe_count':len(probes),'families':summary,'passed':True}))

if __name__ == '__main__': main()
