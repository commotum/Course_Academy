"""Root's independent actual prompt/domain/poles/banks and solution readback."""
import importlib.util,json,re,sys
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=int(sys.argv[1]);D=P.parents[2]/f'generate/scratch/{K}';common=K==17592186087843

def module(n,path):
 a=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(a);a.loader.exec_module(m);return m
p=module('root_rational_math',P/'rational-asymptote-readback.py');g=module('root_rational_gen',D.with_suffix('.py'));X=p.X
C=dict(records=0,choices=0,normal_method_banks=0,evidence_banks=0,solution_equalities=0,denominator_zero_conditions=0,prose_root_statements=0,source_prompts=0,source_values=0,available_source_solutions=0,original_designations=0,raw_omission_profiles=0)
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
def check(r):
 q=r['question'];m=r['generation'];z=p.function(q[':question/problem']);poles=z['poles'];domain=z['domain'];holes=domain-poles;profile=m.get('profile',m.get('bank_profile'));opaque=m['evidence_only'];assert m['eligible_for_learning']==(not opaque)
 assert poles and all(x.is_real for x in poles)
 if common:assert holes and s.degree(s.gcd(z['numerator'],z['denominator']),X)>0
 else:assert not holes and len(poles) in (2,3)
 fs=q.get(':question/answer-fields',[]);blank_values=[]
 for f in fs:
  vals=[p.rootset(a[':answer/value']) for a in f[':answer-field/choices']];C['choices']+=len(vals)
  designated=f.get(':answer-field/correct');value=next((v for a,v in zip(f[':answer-field/choices'],vals) if designated and a[':answer/id']==designated[1]),None)
  if f[':answer-field/type'].endswith('/radio'):
   assert len(vals)==5 and len(set(vals))==5 and vals.count(poles)==1
   if designated:assert value==poles
   else:assert opaque
   if not opaque:
    if common:
     reverse=frozenset(-x for x in holes) if poles==frozenset([0]) else frozenset(-x for x in poles)
     expected={poles,holes,domain,frozenset(),reverse}
    elif profile=='method_numerator':expected={poles,frozenset([min(poles)]),frozenset([max(poles)]),frozenset(),p.real_roots(z['numerator'])}
    else:expected={poles,frozenset(sorted(poles)[:-1]),frozenset(sorted(poles)[1:]),frozenset(-x for x in poles),poles|frozenset([0])}
    assert set(vals)==expected;C['normal_method_banks']+=1
   else:C['evidence_banks']+=1
  else:
   assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem'];expect=sorted(poles)[int(f[':answer-field/key'].split('-')[-1])-1];assert value==frozenset([expect]);blank_values.append(expect)
 if blank_values:assert frozenset(blank_values)==poles
 if ':question/worked-solution' in q:
  text=q[':question/worked-solution'];blocks=re.findall(r'\$\$(.*?)\$\$',text,re.S);assert len(blocks)==(1 if not common and m['template'] in ('factored_three','observed_39793') else 2)
  for block in blocks:
   body=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','');rows=body.split(r'\\');prev=None
   for row in rows:
    parts=row.strip().split('=');assert len(parts)>=2;values=[]
    for i,raw in enumerate(parts):
     raw=p.clean(raw)
     if not raw:assert i==0 and prev is not None;v=prev
     elif re.fullmatch(r'[fgh]\(x\)',raw):assert raw==z['name']+'(x)';v=z['value']
     else:v=p.expression(raw)
     values.append(v)
    if len(values)==2 and values[-1]==0 and values[0].has(X):assert p.real_roots(values[0])==poles;C['denominator_zero_conditions']+=1
    else:
     assert all(s.cancel(v-values[0])==0 for v in values[1:]),(row,values,q[':question/problem']);C['solution_equalities']+=len(values)-1
    prev=values[-1]
  prose=re.findall(r'\$x=([^$]+)\$',text);assert prose;roots=[p.expression(t.replace(r'\,','').rstrip(',')) for t in prose];assert frozenset(roots)==poles;C['prose_root_statements']+=len(roots)
 C['records']+=1;return q
cases=json.loads((D/'source-cases.json').read_text())
for case in cases:
 profile=case.get('raw_profile') or case['bank_profile']+'_raw';r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=profile);q=check(r);old=sources[case['source_id']];assert q[':question/problem']==old[':question/problem'];C['source_prompts']+=1
 for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in old),(case['source_id'],key)
 if ':question/difficulty' in old:assert q[':question/difficulty']==old[':question/difficulty'][':db/ident']
 if ':question/worked-solution' in old:assert q[':question/worked-solution']==old[':question/worked-solution'];C['available_source_solutions']+=1
 oldf={f[':answer-field/key']:f for f in old.get(':question/answer-fields',[])};newf={f[':answer-field/key']:f for f in q.get(':question/answer-fields',[])};assert set(oldf)==set(newf)
 for key,f in oldf.items():
  new=newf[key];assert new[':answer-field/type']==f[':answer-field/type'][':db/ident'];assert sorted((a[':answer/type'][':db/ident'],a[':answer/value']) for a in f[':answer-field/choices'])==sorted((a[':answer/type'],a[':answer/value']) for a in new[':answer-field/choices']);C['source_values']+=len(f[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in new)
  if ':answer-field/correct' in f:
   chosen=next(a for a in new[':answer-field/choices'] if a[':answer/id']==new[':answer-field/correct'][1]);assert chosen[':answer/value']==f[':answer-field/correct'][':answer/value'];C['original_designations']+=1
 C['raw_omission_profiles']+=1
 # Changed source maths plus all full evidence choices through same public API.
 if common:
  for key,value in case['parameters'].items():
   if key=='opaque':continue
   for change in (1,-1,2,-2):
    pp=dict(case['parameters']);pp[key]=value+change
    try:changed=g.generate(case['level'],template=case['template'],parameters=pp,profile='observed')
    except ValueError:continue
    check(changed);break
   else:continue
   break
  else:raise AssertionError('no valid changed source instance')
 else:
  pp=dict(case['parameters']);pp.update(scale=3 if case['template']=='observed_39790' else 2,function='h');check(g.generate(case['level'],template=case['template'],parameters=pp,profile=case['bank_profile']))
for r in json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(r)
for level in ('easy','moderate','hard'):
 for seed in range(30):check(g.generate(level,seed+84243))
C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
