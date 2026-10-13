"""Parent QA of actual triangle-generator content and immutable source banks."""
import importlib.util,json,hashlib,sys,re,math,itertools
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=int(sys.argv[1]);D=P.parents[2]/f'generate/scratch/{K}';kind={17592186105732:'vectors',17592186105733:'vertices',17592186105734:'altitude'}[K]
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('parent_triangle_reader',P/'triangle-readback.py');g=module('parent_triangle_worker',D.with_suffix('.py'))
C=dict(instances=0,choices=0,solution_sides=0,determinants=0,blocks=0,source_banks=0,source_values=0,source_prompts=0,source_exact_solutions=0,source_repaired_solutions=0,source_designations=0,source_missing_designations=0,raw_duplicate_pairs=0)
def check(r):
 q=r['question'];d,c=p.check(q,kind);C['instances']+=1
 for name in ('choices','solution_sides','determinants','blocks'):C[name]+=c[name]
 for f in q[':question/answer-fields']:
  vs=[p.p.scalar(z[':answer/value']) for z in f[':answer-field/choices']];pairs=sum(s.simplify(v-w)==0 for i,v in enumerate(vs) for w in vs[:i]);raw=(r['generation'].get('bank_profile') or '').startswith('raw/');assert pairs==(1 if raw else 0),(r['generation'],vs,pairs);C['raw_duplicate_pairs']+=pairs
 level=q[':question/difficulty'].split('/')[-1]
 # Workload reads actual vector differences rather than unreduced vertices.
 if level=='hard' and kind!='altitude':
  assert all(z!=0 for z in list(d['u'])+list(d['v'])) and all(z!=0 for z in d['w'])
  if kind=='vectors':assert all(math.gcd(*map(int,z))==1 for z in (d['u'],d['v'])) and sum(bool(abs(z)>=2) for z in list(d['u'])+list(d['v']))>=4 and max(map(abs,d['w']))>=8
  elif kind=='vertices':assert max(abs(z) for z in list(d['u'])+list(d['v'])) in (6,7)
 if kind=='vectors' and r['generation'].get('bank_origin')=='authored':
  f=q[':question/answer-fields'][0];factor=2 if d['triangle'] else 1;N=d['w'].dot(d['w']);expected=[d['answer'],d['norm'] if d['triangle'] else d['norm']/2]+[s.sqrt(N-z*z)/factor for z in d['w']];actual=[p.p.scalar(z[':answer/value']) for z in f[':answer-field/choices']];assert set(actual)==set(expected)
 if kind=='vectors':assert c['blocks']==(3 if d['triangle'] else 2)
 elif kind=='vertices':assert c['blocks']==4
 elif kind=='altitude':assert c['blocks']==7
 return q,d
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 level=case.get('level',case.get('difficulty'));r=g.generate(level,template=case['template'],parameters=case['parameters'],profile=case.get('bank_profile'));q,d=check(r);old=sources[case['source_id']];assert q[':question/problem']==old[':question/problem'];C['source_prompts']+=1
 for of,f in zip(old[':question/answer-fields'],q[':question/answer-fields']):
  unused=list(range(len(f[':answer-field/choices'])));vs=[p.p.scalar(z[':answer/value']) for z in f[':answer-field/choices']]
  for choice in of[':answer-field/choices']:
   matches=[i for i in unused if s.simplify(vs[i]-p.p.scalar(choice[':answer/value']))==0];assert matches,(case,choice,vs);unused.remove(matches[0]);C['source_values']+=1
  assert not unused;C['source_banks']+=1
  if of.get(':answer-field/correct'):assert s.simplify(p.p.scalar(of[':answer-field/correct'][':answer/value'])-d['answer'])==0;C['source_designations']+=1
  else:C['source_missing_designations']+=1
 if old.get(':question/worked-solution'):
  if K==17592186105734 and case['source_id']=='q-128008':assert q[':question/worked-solution']==old[':question/worked-solution'].replace('-i+3j-3j','-i+3j-3k');C['source_repaired_solutions']+=1
  else:assert q[':question/worked-solution']==old[':question/worked-solution'];C['source_exact_solutions']+=1
for r in json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(r)
review=json.loads((D/'review.json').read_text())
for r in review:
 r=r.get('record',r)
 if 'question' in r:check(r)
for template,spec in g.TEMPLATES.items():
 level=spec[0] if isinstance(spec,(list,tuple)) else spec if isinstance(spec,str) else spec['level']
 for seed in range(30,42):check(g.generate(level,seed,template=template))
C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
