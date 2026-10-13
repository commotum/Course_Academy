"""Root independently reads vectors/vertices, determinant stages and full banks."""
import importlib.util,json,re,copy,sys
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=int(sys.argv[1]);D=P.parents[2]/f'generate/scratch/{K}';positions=K==17592186105909
def module(n,path):
 sp=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_volume_readback',P/'triple-product-readback.py');g=module('root_volume_gen',D.with_suffix('.py'))
C=dict(records=0,actual_vector_triples=0,choices=0,whole_method_banks=0,evidence_banks=0,solution_blocks=0,solution_equalities=0,determinant_arrays=0,vertex_subtraction_rows=0,source_prompts=0,source_solutions=0,source_values=0,source_banks=0,source_keys=0,raw_missing_assessments=0,known_raw_basis_errors=0)
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
def check(r):
 q=r['question'];meta=r['generation'];d=p.given(q[':question/problem'],positions);a,b,c=d['vectors'];terms=[a[0]*(b[1]*c[2]-b[2]*c[1]),-a[1]*(b[0]*c[2]-b[2]*c[0]),a[2]*(b[0]*c[1]-b[1]*c[0])];volume=d['volume'];assert volume>0
 f=q[':question/answer-fields'][0];vals=[p.p.scalar(z[':answer/value']) for z in f[':answer-field/choices']];assert len(set(vals))==len(vals) and all(z>=0 for z in vals) and vals.count(volume)==1
 sid=meta['source_id'];profile=meta.get('profile',meta.get('bank_profile'));opaque=bool(sid) if positions else bool(profile and profile.startswith('observed_'));assert meta['evidence_only']==opaque and meta['eligible_for_learning']==(not opaque)
 if f.get(':answer-field/correct'):assert next(p.p.scalar(z[':answer/value']) for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1])==volume
 else:assert opaque and ':question/worked-solution' not in q and ':question/difficulty' not in q;C['raw_missing_assessments']+=1
 if ':question/worked-solution' in q:
  solution=q[':question/worked-solution']
  if positions and sid=='q-73744' and profile.startswith('raw_'):
   first=re.findall(r'\$\$(.*?)\$\$',solution,re.S)[0];rows=p.rows(first);assert len(rows)==12;wrong=p.expression(rows[10].split('=',1)[1],d);right=d['refs']['AD'];assert wrong!=right and s.expand(wrong-right)==2*c[1]*p.p.j
   before=rows[10].split('=',1)[1].strip();fixed=s.latex(right);replacement=first.replace(before,fixed);assert replacement!=first;solution=solution.replace('$$'+first+'$$','$$'+replacement+'$$',1);C['known_raw_basis_errors']+=1
  counts=p.solution(solution,d);assert counts['blocks']==(3 if positions else 2) and counts['arrays']==4
  for k,v in counts.items():C[dict(blocks='solution_blocks',equalities='solution_equalities',arrays='determinant_arrays',vector_subtraction_rows='vertex_subtraction_rows')[k]]+=v
  if positions:assert counts['vector_subtraction_rows']==3
 if opaque:
  base=p.given(sources[sid][':question/problem'],positions);old=sources[sid][':question/answer-fields'][0];expected=[volume/base['volume']*p.p.scalar(z[':answer/value']) for z in old[':answer-field/choices']];assert set(vals)==set(expected);C['evidence_banks']+=1
 else:
  if f[':answer-field/type'].endswith('/blank'):expected=[volume]
  elif not positions:expected=[volume,abs(terms[0]+terms[1]),abs(terms[0]+terms[2]),abs(terms[1]+terms[2]),abs(terms[0]-terms[1]+terms[2])]
  elif q[':question/difficulty'].endswith('/hard'):expected=[volume]+[abs(d['triple']-z) for z in terms]+[volume/6]
  else:expected=[volume,2*volume,volume/2,volume/6,abs(s.Matrix([s.Matrix([p.p.scalar(z) for z in raw.split(',')]).T for n,raw in re.findall(r'([A-Z])\(([^()]*)\)',q[':question/problem'])[1:]]).det())]
  assert set(vals)==set(expected),(vals,expected);C['whole_method_banks']+=1
  level=q[':question/difficulty'].split('/')[-1];flat=list(a)+list(b)+list(c)
  if not sid:
   if positions:
    active=sum(z!=0 for z in terms);assert active==dict(easy=1,moderate=2,hard=3)[level] and max(abs(z) for z in flat)<=dict(easy=3,moderate=4,hard=5)[level]
    if level!='easy':assert any(z<0 for z in flat) and sum(z!=0 for z in flat)>=(6 if level=='moderate' else 7)
   elif level=='easy':assert all(z.is_Integer and abs(z)<=9 for z in flat) and 1<=flat.count(0)<=3
   elif level=='moderate':assert all(z.is_Integer and 0<abs(z)<=5 for z in flat) and all(z!=0 for z in terms)
   else:assert all(z.q in (1,2,3) and 0<abs(z)<=5 for z in flat) and sum(z.q>1 for z in flat)>=3 and all(z!=0 for z in terms)
 C['records']+=1;C['actual_vector_triples']+=1;C['choices']+=len(vals);return q
for case in json.loads((D/'source-cases.json').read_text()):
 level=case.get('level',case.get('authored_generator_level'));q=check(g.generate(level,template=case['template'],parameters=case['parameters'],profile=case.get('bank_profile')));old=sources[case['source_id']];assert q[':question/problem']==old[':question/problem'] and q.get(':question/worked-solution')==old.get(':question/worked-solution');C['source_prompts']+=1;C['source_solutions']+=int(':question/worked-solution' in old);of,f=old[':question/answer-fields'][0],q[':question/answer-fields'][0];assert sorted(z[':answer/value'] for z in f[':answer-field/choices'])==sorted(z[':answer/value'] for z in of[':answer-field/choices']);C['source_values']+=len(of[':answer-field/choices']);C['source_banks']+=1
 if of.get(':answer-field/correct'):assert of[':answer-field/correct'][':answer/value']==next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);C['source_keys']+=1
 changed=copy.deepcopy(case['parameters'])
 if positions:changed['points']=[[2*z+i-1 for i,z in enumerate(row)] for row in changed['points']]
 else:changed['vectors'][1]=[str(-s.Rational(z)) for z in changed['vectors'][1]]
 check(g.generate(level,template=case['template'],parameters=changed,profile=case.get('bank_profile')))
for r in json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(r)
for level in ('easy','moderate','hard'):
 for kind in ('radio','blank'):
  for seed in range(8):check(g.generate(level,seed+5907,field_type=kind))
C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
