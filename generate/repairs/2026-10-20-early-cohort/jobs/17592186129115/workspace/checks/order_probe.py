"""Visible-record coordinate-order probe; no runtime mutation or services."""
import collections, json, math, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
from regressions import W, check_record, coords, matrix

def probe(records):
    out={}
    groups={'all': records}
    for z in (False, True):
        groups['bottom_zero_'+str(z)]=[r for r in records if any(not any(row) for row in matrix(r['question'][':question/problem']))==z]
    for label,rs in groups.items():
        ranks=[];positions=[]
        for r in rs:
            check_record(r)
            f=r['question'][':question/answer-fields'][0]
            ci=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])
            b=[coords(a[':answer/value']) for a in f[':answer-field/choices']]
            ranks.append(sorted(range(5),key=lambda i:b[i]).index(ci));positions.append(ci)
        n=len(rs);h=ranks.count(2)
        out[label]={'n':n,'lex_ranks':dict(collections.Counter(ranks)),'positions':dict(collections.Counter(positions)),'median_hits':h,'median_binomial_tail':sum(math.comb(n,k)*.2**k*.8**(n-k) for k in range(h,n+1))}
    return out
if __name__=='__main__':
    target=Path(sys.argv[1]);target.mkdir(parents=True,exist_ok=True)
    rs=json.loads(subprocess.check_output([sys.executable,str(W/'generator.py'),'--difficulty','moderate','--seed','932611','--count','64','--format','json'],text=True))
    (target/'cli-records.json').write_text(json.dumps(rs,indent=2)+'\n')
    result=probe(rs)
    (target/'order-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
    assert result['all']['median_binomial_tail'] >= .01, 'Reproducible matrix-blind median advantage'
