"""Root reads actual conceptual claims, never the generator's truth metadata."""
import importlib.util,re,json,hashlib,itertools,functools
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=17592186176047;D=P.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('root_cosine_scalar',P/'polar-setup-readback.py');g=module('root_cosine_properties',D.with_suffix('.py'));N=p.p.p.z
C=dict(instances=0,claims=0,solution_verdicts=0,solution_evaluations=0,complete_radio_banks=0,blank_fragments=0,source_question_banksets=0,source_field_banks=0,source_values=0,source_refs=0,source_missing_refs=0,source_exact_prompts=0,source_exact_full_solutions=0)
def scalar(raw):
 raw=re.sub(r'\\[A-Za-z]+|n',lambda m:'z' if m[0]=='n' else m[0],raw)
 return p.scalar(raw)
@functools.lru_cache(maxsize=1024)
def claim(line):
 if 'range' in line:
  a,b=re.search(r'\[([^\]]+)\]',line)[1].split(',');return (scalar(a)==-1 and scalar(b)==1,('range',str(scalar(a)),str(scalar(b))))
 if 'output' in line:
  value=scalar(re.search(r'\$y=(.*?)\$',line)[1]);return (bool(-1<=value<=1),('output',str(value)))
 if 'passes through' in line:
  raw=re.search(r'\$\((.*?)\)\$',line)[1];a,b=raw.split(',');a,b=scalar(a),scalar(b);return (s.cos(a)==b,('point',str(s.Mod(a,2*s.pi)),str(b)))
 if '$y$-axis' in line:
  value=scalar(re.search(r'\$y=(.*?)\$',line)[1]);return (value==1,('intercept',str(value)))
 angle=scalar(re.search(r'\$x\s*=\s*(.*?)\$',line)[1].rstrip('.'))
 kind='max' if 'maximum' in line else 'min' if 'minimum' in line else 'zero'
 if angle.has(N):
  step=s.simplify(angle.diff(N)/s.pi);offset=s.simplify(angle.subs(N,0)/s.pi);assert not step.has(N) and s.diff(angle,N,2)==0
  valid=abs(step)==(1 if kind=='zero' else 2) and s.Mod(offset-(s.Rational(1,2) if kind=='zero' else 1 if kind=='min' else 0),1 if kind=='zero' else 2)==0
  return (bool(valid),(kind+'_family',str(s.Mod(offset,abs(step))),str(abs(step))))
 return (s.cos(angle)=={'zero':0,'max':1,'min':-1}[kind],(kind,str(s.Mod(angle,2*s.pi))))
def label(raw):return tuple(z in re.findall(r'\bI{1,3}\b',raw) for z in ('I','II','III'))
def check(rec):
 q=rec['question'];prompt=q[':question/problem'];solution=q[':question/worked-solution'];fields=q[':question/answer-fields'];level=q[':question/difficulty'].split('/')[-1]
 if fields[0][':answer-field/type'].endswith('/blank'):
  assert len(fields)==5;expected={'field-1':r'-\infty','field-2':r'\infty','field-3':'-1','field-4':'1','field-5':r'2\pi'}
  fn=lambda text:set(re.findall(r'\\(sin|cos)\b|\b(sin|cos)⁡',re.sub(r'!\[\]\([^)]*\)','',text)))
  assert fn(prompt)==fn(solution)
  for f in fields:
   assert '{{'+f[':answer-field/key']+'}}' in prompt and len(f[':answer-field/choices'])==1
   assert f[':answer-field/choices'][0][':answer/value'].strip()==expected[f[':answer-field/key']] and f[':answer-field/correct'][1]==f[':answer-field/choices'][0][':answer/id'];C['blank_fragments']+=1
 else:
  lines=[re.sub(r'^\s*(?:[-*]|I{1,3}\.|[123]\.)\s*','',z) for z in prompt.splitlines() if re.match(r'^\s*(?:[-*]|I{1,3}\.|[123]\.)\s*',z)];assert len(lines)==3,prompt
  results=[claim(z) for z in lines];bits=tuple(bool(z[0]) for z in results);C['claims']+=3
  f=fields[0];labels=[label(z[':answer/value']) for z in f[':answer-field/choices']];assert len(labels)==len(set(labels))==5
  assert [z[':answer/id'] for z,b in zip(f[':answer-field/choices'],labels) if b==bits]==[f[':answer-field/correct'][1]];C['complete_radio_banks']+=1
  verdict={}
  for m in re.finditer(r'Statements?\s+([IVand ,]+)\s+(?:is|are)\s+(true|false)',solution):
   for roman in re.findall(r'\bI{1,3}\b',m[1]):verdict[roman]=m[2]=='true'
  assert tuple(verdict[z] for z in ('I','II','III'))==bits;C['solution_verdicts']+=len(verdict)
  for raw in re.findall(r'\$(.*?)\$',solution,re.S):
   m=re.fullmatch(r'\\cos\((.*?)\)=(.*?)',raw.rstrip('.,'))
   if m:assert scalar(r'\cos('+m[1]+')')==scalar(m[2]);C['solution_evaluations']+=1
  semantic=[z[1] for z in results]
  if level=='easy':
   assert all(z[0] in ('zero','min','max','intercept') for z in semantic);locations=[s.S.Zero if z[0]=='intercept' else s.sympify(z[1]) for z in semantic];assert len(set(locations))==3
  if level=='hard':assert {z[0] for z in semantic}=={'zero_family','max_family','min_family'}
 C['instances']+=1;return q,tuple(sorted(z[1] for z in results)) if fields[0][':answer-field/type'].endswith('/radio') else ('facts',)
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 q,_=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));old=sources[case['source_id']];assert q[':question/problem']==old[':question/problem'];C['source_exact_prompts']+=1
 nf={z[':answer-field/key']:z for z in q[':question/answer-fields']}
 for of in old[':question/answer-fields']:
  f=nf[of[':answer-field/key']];assert sorted(z[':answer/value'] for z in of[':answer-field/choices'])==sorted(z[':answer/value'] for z in f[':answer-field/choices']);C['source_field_banks']+=1;C['source_values']+=len(of[':answer-field/choices'])
  if of.get(':answer-field/correct'):assert next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];C['source_refs']+=1
  else:C['source_missing_refs']+=1
 C['source_question_banksets']+=1
 if old.get(':question/worked-solution'):assert q[':question/worked-solution']==old[':question/worked-solution'];C['source_exact_full_solutions']+=1
tasksets={}
for level,n in (('easy',32),('moderate',72),('hard',216)):
 actual=set()
 for params in g.authored_catalog(level):
  _,key=check(g.generate(level,parameters=params));actual.add(key)
 assert len(actual)==n,(level,len(actual));tasksets[level]=len(actual)
for rec in json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(rec)
for name in g.RECIPES:
 for seed in range(80,92):check(g.generate('moderate',seed,template=name))
for asset in json.loads((D/'plot-provenance.json').read_text())['assets']:
 assert hashlib.sha256(Path(asset['source']).read_bytes()).hexdigest()==asset['sha256']==hashlib.sha256((D/asset['copy']).read_bytes()).hexdigest()
freeze=json.loads((D/'freeze.json').read_text())
for path,digest in freeze['files'].items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
C['finite_semantic_catalog_counts']=tasksets;C['frozen_hashes_verified']=len(freeze['files']);C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
