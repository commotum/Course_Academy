"""Root reads complete cooling stories, scalar banks and every printed stage."""
import importlib.util,json,re,hashlib
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=17592186078584;D=P.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('root_cooling_solve',D.with_suffix('.py'));p=module('root_cooling_readback',P/'cooling-stage-readback.py')
C=dict(instances=0,choices=0,source_prompts=0,source_values=0,source_full_banks=0,source_keys=0,source_full_solutions=0,raw_unit_error_solutions=0,normal_unit_repairs=0,actual_method_banks=0)
def round_(x):return int(s.floor(s.N(x,45)+s.Rational(1,2)))
def check(r,raw=False):
 q=r['question'];d=p.question(q);f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];assert f[':answer-field/type']==':answer-field.type/radio' and len(choices)==5
 values=[int(re.search(r'\d+',z[':answer/value'])[0]) for z in choices];assert len(set(values))==5
 assert [z[':answer/id'] for z,v in zip(choices,values) if v==d['rounded']]==[f[':answer-field/correct'][1]]
 prompt=q[':question/problem'];temps=[int(m[1]) for m in p.TEMP.finditer(prompt)];A=d['ambient']
 if d['level']=='easy':
  I=temps[0];time=d['target_time'];k=d['rate'];delta=I-A
  expected=[d['rounded'],round_(delta*s.exp(-k*time)),round_(A+I*s.exp(-k*time)),round_(A+delta*s.exp(-k*time/2)),round_(A+delta*s.exp(-2*k*time))]
  if not raw:assert all(A<v<I for v in values)
  if 'coffee' in prompt:assert I<=100
  if 'cake' in prompt:assert 180<=I<=400 and d['unit']=='F'
  if 'compressor' in prompt:assert I<=140
 elif d['level']=='moderate':
  I=d['times'][0][1];time,O=d['times'][1];Z=temps[3] if not prompt.startswith('Simon') else temps[2];k=d['rate'];x=d['exact']
  expected=[d['rounded'],round_(time*s.log(s.Rational(Z,I))/s.log(s.Rational(O,I))),round_(-s.log(s.Rational(Z,I))/k),round_(x/2),round_(2*x)]
  if not raw:assert min(values)>time
  if 'water boils' in prompt:assert I==100
  if 'Simon' in prompt or 'water bath' in prompt:assert I<=100
  if 'brought outside' in prompt:assert 50<=I<=90 and d['unit']=='F'
 else:
  (a,O),(b,L)=d['times'];Z=temps[-1];gap=b-a;x=d['exact']
  assert 0<a<b and a%gap and s.Rational(1,3)<=s.Rational(L-A,O-A)<=s.Rational(4,5)
  expected=[d['rounded'],round_(x-a),round_(a+(x-a)/2),round_(a+2*(x-a)),round_(a+gap*s.log(s.Rational(Z,O))/s.log(s.Rational(L,O)))]
  assert min(values)>b and 'metal body' in prompt
 if not raw:assert sorted(values)==sorted(expected),(q,values,expected);C['actual_method_banks']+=1
 for v in choices:
  if d['level']=='easy':assert next(iter({m[2] or m[3] for m in p.TEMP.finditer(v[':answer/value'])}))==d['unit']
  else:assert '\\text{min}' in v[':answer/value']
 if not raw:
  assert '\t' not in q[':question/worked-solution']
  assert all((m[2] or m[3])==d['unit'] for m in p.TEMP.finditer(q[':question/worked-solution']))
 counts=p.stages(q,d)
 for key,n in counts.items():C[key]=C.get(key,0)+n
 C['instances']+=1;C['choices']+=5
 return q
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 q=check(g.generate(case['difficulty'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']),True);old=sources[case['source_id']]
 assert q[':question/problem']==old[':question/problem'];assert q[':question/worked-solution']==old[':question/worked-solution'];C['source_prompts']+=1;C['source_full_solutions']+=1
 f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0];actual=sorted(z[':answer/value'] for z in f[':answer-field/choices']);original=sorted(z[':answer/value'] for z in of[':answer-field/choices']);assert actual==original;C['source_values']+=len(actual);C['source_full_banks']+=1
 assert of[':answer-field/correct'][':answer/value']==next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);C['source_keys']+=1
 C['raw_unit_error_solutions']+=int(case['source_id']=='q-107122')
 try:normal=check(g.generate(case['difficulty'],template=case['template'],parameters=case['parameters']))
 except ValueError:
  C['original_parameters_rejected_default_bank']=C.get('original_parameters_rejected_default_bank',0)+1;normal=None
 if case['source_id']=='q-107122':assert normal[':question/worked-solution']!=old[':question/worked-solution'];C['normal_unit_repairs']+=1
 for seed in range(8):check(g.generate(case['difficulty'],seed+111,template=case['template'],profile=case['bank_profile']),True)
for item in json.loads((D/'review.json').read_text()):
 r=item.get('record',item);check(r,bool(r['generation'].get('bank_profile') in sources))
for level in ('easy','moderate','hard'):
 for seed in range(24):check(g.generate(level,seed+900))
C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
