"""Independent parent arc-length oracle: actual curves, complete integrals and stages."""
import argparse,importlib.util,json,re,sys
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
p=module('parent_arc_vector',R/'arc-vector-parser.py');t=p.p.t
ap=argparse.ArgumentParser();ap.add_argument('kp',type=int);K=ap.parse_args().kp;assert K==17592186119743
D=R.parents[2]/f'generate/scratch/{K}';g=module('parent_arc_generator',D.with_suffix('.py'))
counts=dict(source_questions=0,source_banks=0,source_values=0,source_designations=0,source_missing_designations=0,source_prompts=0,source_solutions=0,source_solution_repairs=0,printed_instances=0,derivative_operator_components=0,derivative_components=0,norm_stages=0,integral_stages=0)
def rows(text):return [re.split(r'\\\\',b) for b in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S)]
def clean(raw):return raw.strip().rstrip('.,?').replace('&','').strip()
def speednorm(raw,speed):
 raw=re.sub(r'(?:‖\{?[rfgh]\}?(?:\^\{′\}|\x27)\(t\)‖|\\\|[rfgh]\x27\(t\)\\\|)',lambda _: '('+s.latex(speed)+')',raw)
 return raw

def derivative_operator(raw):
 values=[]
 pattern=r'\\frac\{\\(?:mathrm|text)\{d\}\}\{\\(?:mathrm|text)\{d\}t\}\('
 for m in re.finditer(pattern,raw):
  start=m.end();i=start;depth=1
  while depth:
   assert i<len(raw),raw;depth+=(raw[i]=='(')-(raw[i]==')');i+=1
  values.append(p.math(raw[start:i-1]))
 assert values,raw
 return tuple(values)

def stages(text,curve,bounds):
 expected_der=tuple(s.diff(z,t) for z in curve);speed=p.speed(curve);groups=rows(text);assert len(groups)==2
 roles=[]
 for n,row in enumerate(groups[0]):
  rhs=clean(row.split('=',1)[1])
  if n==0:
   values=derivative_operator(rhs);assert len(values)==len(curve) and all(p.same(a,b) for a,b in zip(values,curve));role='operator';counts['derivative_operator_components']+=len(values)
  elif n==1:
   values=p.vector(rhs);assert len(values)==len(curve) and all(p.same(a,b) for a,b in zip(values,expected_der)),(rhs,expected_der);role='derivative';counts['derivative_components']+=len(values)
  else:
   val=p.math(rhs);assert p.same_on(val,speed,bounds),(rhs,val,speed,bounds);role='norm';counts['norm_stages']+=1
  roles.append(role)
 for row in groups[1]:
  for rhs in row.split('=')[1:]:
   rhs=speednorm(clean(rhs),speed);lo,hi,fn=p.integral(rhs);assert (lo,hi)==bounds and p.same_on(fn,speed,bounds),(rhs,fn,speed);counts['integral_stages']+=1
 roles.extend(['integral']*sum(len(row.split('='))-1 for row in groups[1]));return tuple(roles)

def integral_same(a,b):return a[:2]==b[:2] and p.same(a[2],b[2])
def check(record):
 q=record['question'];curve,bounds=p.prompt(q[':question/problem']);speed=p.speed(curve);fs=q[':question/answer-fields'];assert len(fs)==1
 for f in fs:
  bank=f[':answer-field/choices'];assert len(bank)==5;values=[p.integral(a[':answer/value']) for a in bank]
  assert all(not integral_same(v,w) for i,v in enumerate(values) for w in values[:i])
  matches=[a[':answer/id'] for a,v in zip(bank,values) if v[:2]==bounds and p.same_on(v[2],speed,bounds)];assert matches==[f[':answer-field/correct'][1]],(q[':question/problem'],values,speed)
 roles=stages(q[':question/worked-solution'],curve,bounds);counts['printed_instances']+=1;return curve,bounds,roles

def mask(text):
 text=re.sub(r'!\[[^\]]*\]\([^)]*\)','IMAGE',text)
 return re.sub(r'\s+',' ',p.MATH.sub('$MATH$',text)).strip()
qs={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 sid=case['source_id'];old=qs[sid];record=g.generate(case.get('level',case.get('difficulty')),template=case['template'],parameters=case['parameters'],profile=case.get('bank_profile',case.get('profile')));curve,bounds,roles=check(record)
 oc,ob=p.prompt(old[':question/problem']);assert len(oc)==len(curve) and all(p.same(a,b) for a,b in zip(oc,curve)) and ob==bounds
 assert mask(old[':question/problem'])==mask(record['question'][':question/problem']),(sid,'prompt');counts['source_prompts']+=1
 sol=old[':question/worked-solution']
 if sid=='q-33857':sol=sol.replace(r'{\int }_{1}^{2}',r'{\int }_{0}^{1}');counts['source_solution_repairs']+=1
 assert mask(sol)==mask(record['question'][':question/worked-solution']),(sid,'solution prose')
 assert stages(sol,oc,ob)==roles,(sid,'sequence');counts['source_solutions']+=1
 # Duplicate legacy bank is compared against the separately designated replay profile.
 oldfields=old[':question/answer-fields']
 f=oldfields[0] if case.get('bank_profile','').endswith('legacy') else oldfields[-1]
 nf=record['question'][':question/answer-fields'][0];remaining=[p.integral(v[':answer/value']) for v in nf[':answer-field/choices']]
 for answer in f[':answer-field/choices']:
  val=p.integral(answer[':answer/value']);indices=[n for n,v in enumerate(remaining) if integral_same(val,v)];assert len(indices)==1,(sid,answer,remaining);remaining.pop(indices[0]);counts['source_values']+=1
 assert not remaining;counts['source_banks']+=1
 if f.get(':answer-field/correct'):
  selected=next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]);assert integral_same(p.integral(selected),p.integral(f[':answer-field/correct'][':answer/value']));counts['source_designations']+=1
 else:counts['source_missing_designations']+=1
 counts['source_questions']+=1
for item in json.loads((D/'review.json').read_text()):check(item.get('record',item))
for item in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(item)
counts['source_replay_cases']=counts['source_questions'];counts['source_questions']=len(qs);counts['source_prompts']=len(qs);counts['source_solutions']=len(qs)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
