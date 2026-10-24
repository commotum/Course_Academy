"""Independent bounded-domain and current-bank checks for calculator practice."""
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP
import importlib.util
import json
import math
from pathlib import Path
import re
import sys

H=Path(__file__).resolve().parent
sys.path.insert(0,str(H/'package'))
spec=importlib.util.spec_from_file_location('change_base',H/'package/generator.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)


def rational_shortcut(a,x):
    # Independent exhaustive integer-power relation for this bounded domain.
    return x==1 or any(a**p==x**q for p in range(1,7) for q in range(1,7))


def main():
    for a in range(3,23):
        for x in range(4,46):
            assert g.requires_change_of_base(a,x)==(a!=10 and not rational_shortcut(a,x)),(a,x)
    for a,x in [(17,17),(17,1),(3,27),(4,8),(27,9),(10,19)]:
        try:g.generate(a,x,3)
        except ValueError:pass
        else:raise AssertionError(('shortcut accepted',a,x))
    rows=g.sample(150,8675309);assert rows==g.sample(150,8675309)
    coverage=Counter();ranks=set();grader=[]
    for row in rows:
        meta=row['generation'];p=meta['parameters'];a,x,places=(p[k] for k in ('a','x','places'))
        assert a!=10 and not rational_shortcut(a,x)
        coverage[meta['profile'],meta['region']]+=1
        if meta['correct_rank'] is not None:ranks.add((meta['profile'],meta['correct_rank']))
        f=row['question'][':question/answer-fields'][0];correct=next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==f[':answer-field/correct'][1])
        expected=Decimal(str(math.log(x)/math.log(a))).quantize(Decimal(1).scaleb(-places),rounding=ROUND_HALF_UP)
        assert Decimal(correct)==expected,(a,x,correct,expected)
        assert len(set(c[':answer/value'] for c in f[':answer-field/choices']))==len(f[':answer-field/choices'])
        if len(grader)<12 and f[':answer-field/type']==':answer-field.type/blank':
            grader.append({'label':f'nontrivial {a},{x},{places}','record':row,'checks':[
                {'submitted':correct,'expected':'accepted'},
                {'submitted':format(Decimal(correct),'f')+'0','expected':'accepted'},
                {'submitted':str(Decimal(correct)+Decimal(1).scaleb(-places)),'expected':'rejected'}]})
    assert set(coverage)=={(p,c) for p in ('blank','p2','p3') for c in ('below','above')}
    assert ranks=={(p,i) for p in ('p2','p3') for i in range(5)}
    source_rows=g.replay();assert len(source_rows)==len(json.loads((H/'package/source-data.json').read_text()))
    data=json.loads((H/'kp-before.json').read_text());dispositions=[]
    for q in data['kp'][':knowledge-point/questions']:
        if q.get(':question/math-academy-id'):continue
        m=re.search(r'\\log_\{(\d+)\}\((\d+)\)',q[':question/problem']);assert m,q[':db/id']
        a,x=map(int,m.groups());bad=a==10 or rational_shortcut(a,x)
        dispositions.append({'entity':q[':db/id'],'uuid':q[':question/id'],'a':a,'x':x,
            'decision':'retire' if bad else 'retain','reason':'The input bypasses change of base' if bad else 'Numerical base conversion is still required'})
    assert [q['entity'] for q in dispositions if q['decision']=='retire']==[17592186576201]
    (H/'dispositions.json').write_text(json.dumps(dispositions,indent=2)+'\n')
    (H/'grader-input.json').write_text(json.dumps(grader,indent=2)+'\n')
    (H/'render-input.json').write_text(json.dumps([next(r for r in rows if r['generation']['profile']==p) for p in ('blank','p2','p3')],indent=2)+'\n')
    report={'sampled':len(rows),'source_replays':len(source_rows),'bounded_pairs_checked':840,
        'profiles_and_regions':{str(k):v for k,v in coverage.items()},'all_radio_ranks_covered':True,
        'existing_generated_audited':len(dispositions),'withdrawals':[q['entity'] for q in dispositions if q['decision']=='retire'],
        'integer_power_negative_controls':6,'sampler_deterministic':True}
    (H/'generator-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))


if __name__=='__main__':main()
