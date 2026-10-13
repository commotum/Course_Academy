"""Root reads complete challenging systems, tuple banks and substitution stages."""
import importlib.util,json,re
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186073753;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_challenging_reader',R/'system-readback.py');g=module('root_challenging_generator',D.with_suffix('.py'));s=p.s
C=dict(instances=0,values=0,equation_equalities=0,univariate_equivalences=0,actual_substitution_operations=0,source_values=0,source_banks=0,source_missing_refs=0,raw_invalid_banks=0,source_normalized_prompts=0)
def system(prompt):
 body=next(z for z in p.blocks(prompt) if ';' in z);body=body.strip().removeprefix(r'\{').removeprefix('{')
 plain=re.sub(r'\\[A-Za-z]+','',body);names=tuple(sorted(set(re.findall('[a-z]',plain))));assert len(names)==2,(body,names)
 equations=[p.eq(z,names) for z in body.split(';')];assert len(equations)==2
 A,b=s.linear_eq_to_matrix(equations,(p.p.x,p.p.y));assert A.det();sol=dict(zip((p.p.x,p.p.y),A.inv()*b));return names,equations,sol
def value(raw,names):
 if '=' not in raw:return p.scalar(raw,names)
 assignments=[z.strip().split('=') for z in raw.split(',')];assert len(assignments)==2
 assert [z[0].strip() for z in assignments]==list(names),(raw,names)
 return tuple(p.scalar(z[1],names) for z in assignments)
def normalize(text):return re.sub(r'\s+','',text.replace('${',r'$\{').replace(r'\dfrac',r'\frac'))
def check(record):
 q=record['question'];names,equations,sol=system(q[':question/problem']);symbols=(p.p.x,p.p.y);worked=q[':question/worked-solution']
 groups=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',worked,re.S);parsed=[]
 for group in groups:
  rows=group.split(chr(92)*2);residuals=[]
  for row in rows:
   parts=row.replace('&','').strip().rstrip('.,').split('=');vals=[p.scalar(z,names) for z in parts];assert len(vals)==2
   residual=s.expand(vals[0]-vals[1]);assert s.simplify(residual.subs(sol))==0,(row,sol)
   if len(residual.free_symbols)==1:
    variable=next(iter(residual.free_symbols));assert s.solve(residual,variable)==[sol[variable]];C['univariate_equivalences']+=1
   residuals.append(residual);C['equation_equalities']+=1
  parsed.append(residuals)
 # Recover the actual isolated variable and affine expression from the printed
 # last row, independently of generator metadata or declared template.
 first=groups[0].split(chr(92)*2)[-1].replace('&','').split('=');isolated=p.scalar(first[0],names);replacement=p.scalar(first[1],names)
 assert isolated in symbols and not replacement.has(isolated)
 reference=next(e for e in equations if s.simplify(e.subs(isolated,replacement))==0)
 for row in parsed[0]:assert s.simplify(row/reference).free_symbols==set()
 following=parsed[1];assert any(s.expand(following[0]-e)==0 for e in equations)
 assert s.expand(following[0].subs(isolated,replacement)-following[1])==0;C['actual_substitution_operations']+=1
 for before,after in zip(following[1:-2],following[2:-1]):assert s.expand(before-after)==0;C['actual_substitution_operations']+=1
 if len(parsed)==3:
  back=parsed[2];other=next(z for z in symbols if z!=isolated);assert any(s.expand(back[0]-e)==0 for e in equations)
  assert s.expand(back[0].subs(other,sol[other])-back[1])==0;C['actual_substitution_operations']+=1
  for before,after in zip(back[1:-2],back[2:-1]):assert s.expand(before-after)==0;C['actual_substitution_operations']+=1
 pair=tuple(sol[z] for z in symbols);is_difference='what is the value of' in q[':question/problem'];wanted=pair[0]-pair[1] if is_difference else pair
 f=q[':question/answer-fields'][0];values=[value(z[':answer/value'],names) for z in f[':answer-field/choices']];assert len(set(values))==len(values)==5
 good=[z==wanted for z in values];raw=record['generation']['profile']=='source_q12457_raw'
 if raw:assert sum(good)==0 and ':answer-field/correct' not in f;C['raw_invalid_banks']+=1
 else:assert sum(good)==1 and good[next(n for n,z in enumerate(f[':answer-field/choices']) if z[':answer/id']==f[':answer-field/correct'][1])]
 if not is_difference:
  final=re.findall(r'\\left\(([^\n]+)\\right\)',worked)[-1];assert tuple(p.scalar(z,names) for z in final.split(','))==pair
 else:assert p.scalar(worked.rsplit('=',1)[1].strip(' $.\n'),names)==wanted
 if record['generation']['profile']=='method':
  A,b=s.linear_eq_to_matrix(equations,symbols);coeffs=list(A);level=record['generation']['level']
  if level=='easy':assert max(map(abs,coeffs))<=6 and all(z.is_Integer for z in pair)
  elif level=='moderate':assert all(2<=abs(z)<=9 for z in coeffs) and all(z.is_Integer for z in pair)
  else:assert all(2<=abs(z)<=10 for z in coeffs) and any(not z.is_Integer for z in pair) and max(z.q for z in pair)<=12
 C['instances']+=1;C['values']+=len(values);return q
sources={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 old=sources[case['source_id']];new=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));assert normalize(old[':question/problem'])==normalize(new[':question/problem']);C['source_normalized_prompts']+=1
 names,_,_=system(new[':question/problem'])
 for of,nf in zip(old[':question/answer-fields'],new[':question/answer-fields']):
  assert sorted(value(z[':answer/value'],names) for z in of[':answer-field/choices'])==sorted(value(z[':answer/value'],names) for z in nf[':answer-field/choices']);assert not of.get(':answer-field/correct');C['source_missing_refs']+=1;C['source_values']+=len(of[':answer-field/choices']);C['source_banks']+=1
for r in json.loads((D/'review.json').read_text()):check(r.get('record',r))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
C['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
