"""Root actual tangent claims, subset banks and every displayed identity."""
import importlib.util,re,json,sys,hashlib,itertools,functools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186176049;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','root_tangent_scalar');x,N=p.x,p.z
def math(raw):
 raw=re.sub(r'\\[A-Za-z]+|n',lambda m:m[0] if m[0].startswith('\\') else 'z',raw);return p.scalar(raw)
def period_identity(left,right):
 difference=s.expand((math(left)-math(right))/s.pi);assert s.diff(difference,x)==0 and s.diff(difference,N,2)==0;return bool(difference.coeff(N).is_integer and difference.subs(N,0).is_integer)
def family_at(raw,offset):
 expression=math(raw);step=s.simplify(s.diff(expression,N)/s.pi);shift=s.simplify(expression.subs(N,0)/s.pi);assert s.diff(expression,N,2)==0
 return bool(abs(step)==1 and s.Mod(shift-offset,1)==0)
@functools.lru_cache(maxsize=1024)
def claim(line):
 line=line.replace(r'\operatorname{tan}⁡',r'\tan ').replace('tan⁡',r'\tan ')
 if '\\tan' in line or 'tan⁡' in line:
  normalized=line.replace('tan⁡',r'\tan').replace(r'\operatorname{tan}⁡',r'\tan');args=re.findall(r'\\tan\s*\((.*?)\)',normalized);assert len(args)==2;return period_identity(*args),'identity'
 if 'range' in line:return bool(re.search(r'\(-\\infty\s*,\s*\\infty\s*\)',line)),'range'
 if 'domain' in line:
  if 'except' not in line:return False,'domain'
  raw=re.search(r'\$x\s*=\s*(.*?)\$',line)[1];return family_at(raw,s.Rational(1,2)),'domain'
 if 'least positive period' in line:
  return math(re.search(r'\$(.*?)\$',line)[1])==s.pi,'period'
 if 'no positive period' in line:return False,'period'
 if 'positive' in line or 'negative' in line:
  raw=re.search(r'\$\((.*?),(.*?)\)',line);assert raw;lo,hi=map(math,raw.groups());assert eq(s.diff(lo,N),s.pi) and eq(s.diff(hi,N),s.pi)
  a,b=[s.simplify(z.subs(N,0)/s.pi) for z in (lo,hi)];return ((a,b)==((0,s.Rational(1,2)) if 'positive' in line else (-s.Rational(1,2),0))),'sign'
 if 'passes through' in line:
  a,b=map(math,re.search(r'\$\((.*?),(.*?)\)',line).groups());return eq(s.tan(a),b),'point'
 raw=re.search(r'\$x\s*=\s*(.*?)\$',line)[1].rstrip('.,');return family_at(raw,s.Rational(1,2) if 'asymptote' in line else 0),'asym' if 'asymptote' in line else 'zero'
def eq(a,b):return s.simplify(a-b)==0
def labels(raw):return tuple(z in re.findall(r'\bI{1,3}\b',raw) for z in ('I','II','III'))
C=dict(records=0,actual_claims=0,verdicts=0,complete_banks=0,displayed_identity_links=0,source_prompts=0,source_solutions=0,source_fields=0,source_values=0,source_refs=0,source_missing_refs=0,source_missing_ratings=0)
def check(rec):
 q=rec['question'];prompt=q[':question/problem'];sol=q.get(':question/worked-solution','');lines=[re.sub(r'^\s*(?:[-*]|I{1,3}\.|[123]\.)\s*','',line) for line in prompt.splitlines() if re.match(r'^\s*(?:[-*]|I{1,3}\.|[123]\.)\s*',line)];assert len(lines)==3;truths,kinds=zip(*(claim(line) for line in lines));truths=tuple(bool(t) for t in truths);C['actual_claims']+=3
 f=q[':question/answer-fields'][0];values=[labels(a[':answer/value']) for a in f[':answer-field/choices']];assert len(values)==len(set(values))==5
 if ':answer-field/correct' in f:assert [a[':answer/id'] for a,val in zip(f[':answer-field/choices'],values) if val==truths]==[f[':answer-field/correct'][1]]
 else:assert rec['generation']['evidence_only']
 verdict={}
 for m in re.finditer(r'Statements?\s+([IVand ,]+)\s+(?:is|are)\s+(true|false)',sol):
  for roman in re.findall(r'\bI{1,3}\b',m[1]):verdict[roman]=m[2]=='true'
 if sol:assert tuple(verdict[r] for r in ('I','II','III'))==truths;C['verdicts']+=3
 for raw in re.findall(r'\$(.*?)\$',sol.replace(r'\operatorname{tan}⁡',r'\tan ').replace('tan⁡',r'\tan '),re.S):
  args=re.findall(r'\\tan\s*\((.*?)\)',raw)
  if len(args)>1:
   for a,b in zip(args,args[1:]):assert period_identity(a,b),(raw,a,b);C['displayed_identity_links']+=1
 if ':question/difficulty' in q and not rec['generation']['evidence_only']:
  level=q[':question/difficulty'].rsplit('/',1)[1]
  if level=='easy':assert kinds==('zero','asym','range')
  if level=='moderate':assert kinds==('domain','sign','period')
  if rec['generation']['template']=='two_identity_properties':assert kinds[:2]==('identity','identity')
 C['complete_banks']+=1;C['records']+=1;return truths
if __name__=='__main__':
 g=load(D.with_suffix('.py'),'root_tangent_properties');old={q[':question/math-academy-id']:q for q in json.load(open(R/f'sources/{K}.json'))['record'][':knowledge-point/questions']}
 for case in json.load(open(D/'source-cases.json')):
  rec=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);q=rec['question'];o=old[case['math_academy_id']];check(rec)
  for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):assert (key in q)==(key in o)
  assert q[':question/problem']==o[':question/problem'];C['source_prompts']+=1
  if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];C['source_solutions']+=1
  C['source_missing_ratings']+=int(':question/difficulty' not in o)
  for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);C['source_fields']+=1;C['source_values']+=len(of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
   if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];C['source_refs']+=1
   else:C['source_missing_refs']+=1
 records=json.load(open(R/f'qa/{K}-sampled.json'))
 for level in ('easy','moderate'):
  for parameters in g.catalogs(level):records.append(g.generate(level,parameters=parameters))
 for parameters in g.hard_catalog():records.append(g.generate('hard',template='two_identity_properties',parameters=parameters))
 for family in g.OBSERVED:
  for seed in (771,772,773):records.append(g.generate('hard',template=family,seed=seed))
 for rec in records:check(rec)
 out=dict(status='passed',readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
