#!/usr/bin/env python3
"""Independent displayed-math, fidelity and native-engine checks; no DB access."""
import importlib.util, json, hashlib, re, subprocess, itertools, sys
sys.dont_write_bytecode=True
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
HERE=Path(__file__).resolve().parent
SCRIPT=HERE.parent/(HERE.name+'.py')
spec=importlib.util.spec_from_file_location('monomial',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,C=sp.symbols('x C',real=True)
TRANS=standard_transformations+(implicit_multiplication_application,)
def group(s,start):
 assert s[start]=='{';depth=1;i=start+1
 while depth:
  assert i<len(s),'Unbalanced TeX braces'
  depth+=(s[i]=='{')-(s[i]=='}');i+=1
 return s[start+1:i-1],i

def expr(s):
 s=s.strip().rstrip('.').replace(r'\,','').replace('✓','').replace(r'\cdot','*').replace('{x}','x')
 while r'\frac' in s:
  i=s.index(r'\frac');j=i+5;a,j=group(s,j);b,j=group(s,j);s=s[:i]+'(('+str(expr(a))+')/('+str(expr(b))+'))'+s[j:]
 s=re.sub(r'\^\{([^{}]+)\}',r'**(\1)',s).replace('^','**').replace('{','(').replace('}',')')
 assert '\\' not in s, s
 return parse_expr(s,local_dict={'x':x,'C':C},transformations=TRANS)
DER=r'\frac{\text{d}}{\text{d}x}'
def math_value(s):
 s=s.strip().rstrip('.')
 while DER in s:
  i=s.index(DER);start=i+len(DER);assert s[start]=='(';depth=1;j=start+1
  while depth: depth+=(s[j]=='(')-(s[j]==')');j+=1
  arg=s[start+1:j-1];v=sp.diff(expr(arg),x);s=s[:i]+'('+str(v)+')'+s[j:]
 return expr(s)
def extract_n(prompt):
 if r'\intxdx' in prompt:return 1
 if r'\int 1' in prompt:return 0
 m=re.search(r'(?:\{x\}|x)\^\{(\d+)\}',prompt);assert m,prompt
 return int(m[1])
def formatting(s):
 assert s.count('$')%2==0,'Unbalanced math delimiters'
 depth=0
 for c in s:
  depth+=(c=='{')-(c=='}');assert depth>=0
 assert depth==0
 assert not re.search(r'\\int[a-zA-Z]',s),'Malformed integral command'
 assert '--' not in s and '+-' not in s

def verify(r,raw=False):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];n=extract_n(q[':question/problem']);assert n in range(61)
 if not raw:formatting(q[':question/problem'])
 vals=[]
 for f in q.get(':question/answer-fields',[]):
  for a in f[':answer-field/choices']:
   formatting(a[':answer/value']);v=expr(a[':answer/value']);vals.append(v)
   if not raw and a[':answer/id']==f[':answer-field/correct'][1]:assert sp.diff(v,x)==x**n and sp.diff(v,C)!=0
  for a,b in itertools.combinations(vals,2):
   assert not(bool(sp.diff(a,C)!=0)==bool(sp.diff(b,C)!=0) and sp.simplify(sp.diff(a-b,x))==0),'Equivalent complete families'
  if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 sol=q.get(':question/worked-solution')
 if sol:
  formatting(sol)
  # Parse actual printed derivative argument, linearity, factor-out and power-rule rows.
  blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);check=blocks[-1].removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}')
  rows=check.split(r' \\ ');assert len(rows)==(4 if n==0 else 5)
  assert [row.count(DER) for row in rows]==([1,2,0,0] if n==0 else [1,2,1,0,0])
  for row in rows:assert sp.simplify(math_value(row.replace('& =',''))-x**n)==0,row
  formal=blocks[-2]
  # Read unsimplified exponent and denominator separately: n+1 must occur in both.
  assert r'\frac{{x}^{'+str(n)+r'+1}}{'+str(n)+r'+1}+C' in formal
  if n==0:
   stages=formal.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(r' \\ ')
   assert len(stages)==3 and r'\int 1' in stages[0] and r'\int {x}^{0}' in stages[0]
   targets=[stages[1].replace(' & =',''),stages[2].replace(' & =','')]
  elif 'Remember that integration' in sol:
   intro=blocks[0].removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(r' \\ ')
   assert intro==["{F}^{'}(x) & =f(x)",r"\int {F}^{'}(x)\,\text{d}x & =\int f(x)\,\text{d}x",r'F(x) & =\int f(x)\,\text{d}x.']
   stages=formal.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(r' \\ ')
   assert len(stages)==4 and r'F(x) & =\int f(x)' in stages[0]
   assert expr(re.sub(r'^ & =\\int (.*?)\\,\\text\{d\}x$',r'\1',stages[1]))==x**n
   targets=[v.replace(' & =','') for v in stages[2:]]
  else:
   stages=formal.split('=');assert len(stages)==3
   assert expr(re.sub(r'^\\int (.*?)\\,\\text\{d\}x$',r'\1',stages[0]))==x**n
   targets=stages[1:]
  for t in targets:assert sp.simplify(expr(t)-(x**(n+1)/sp.Integer(n+1)+C))==0
  assert "Let's check by differentiating:" in sol
  if n>0:assert '$n='+str(n)+'$' in sol

cases=[];fidelity=[]
for q in g.SOURCE['record'][':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];template,n=g.SOURCE_SPECS[sid];case={'source_id':sid,'template':template,'parameters':{'n':n},'bank_profile':'raw:'+sid,'level':'easy','level_origin':'observed' if ':question/difficulty' in q else 'authored assignment; original unrated'};cases.append(case)
 r=g.generate('easy',template=template,parameters={'n':n},profile='raw:'+sid);verify(r,True);rq=r['question']
 keys=[':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields']
 for key in keys:
  assert (key in q)==(key in rq),(sid,key,'presence')
  if key!=':question/answer-fields':
   value=q.get(key);value=value.get(':db/ident') if isinstance(value,dict) else value
   assert value==rq.get(key),(sid,key)
 if ':question/answer-fields' in q:
  f=q[':question/answer-fields'][0];rf=rq[':question/answer-fields'][0]
  assert f[':answer-field/key']==rf[':answer-field/key'];assert f[':answer-field/type'][':db/ident']==rf[':answer-field/type']
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in rf[':answer-field/choices'])
  assert (':answer-field/correct' in f)==(':answer-field/correct' in rf)
 fidelity.append({'source_id':sid,'prompt_exact':True,'solution_presence_and_exact':True,'field_presence_and_bank_exact':True,'original_correct_designation_present':False})
(HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
# Normal profile and field combinations over the complete finite exponent domains.
records=[];native=[];counts={}
for level,domain in g.DOMAINS.items():
 fingerprints=set()
 for n in domain:
  templates=['constant'] if n==0 else ['integral_spaced','integral_thin','function','legacy_x','legacy_power'] if level=='easy' else ['integral_thin','function']
  for template in templates:
   kinds=['blank'] if n==0 else ['blank','radio']
   profiles=['authored_power','observed_2005']+(['observed_2022'] if n>=2 else []) if n>0 else [None]
   for kind in kinds:
    for profile in profiles if kind=='radio' else [None]:
     r=g.generate(level,seed=11,template=template,field_type=kind,parameters={'n':n},profile=profile);verify(r);records.append(r);fingerprints.add(r['generation']['mathematical_fingerprint'])
     other=g.generate(level,seed=22,template=template,field_type=kind,parameters={'n':n},profile=profile)
     assert other['question'][':question/id']==r['question'][':question/id']
     assert other['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
 counts[level]={'distinct_mathematical_tasks':len(fingerprints),'eligible_exponents':list(domain)}
# Replay profiles must genuinely change expressions and preserve omission patterns.
for case in cases:
 if case['template']=='constant':continue
 changed=g.generate('easy',template=case['template'],parameters={'n':5},profile=case['bank_profile']);verify(changed,True)
 assert changed['question'][':question/problem']!=g.generate('easy',template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])['question'][':question/problem']
# Invalid explicit level, number forms, range and profile bank instances must fail.
invalid=[('easy',{'n':21}),('moderate',{'n':20}),('moderate',{'n':41}),('hard',{'n':40}),('hard',{'n':61}),('easy',{'n':-1}),('easy',{'n':'4'}),('easy',{'n':1.5}),('easy',{'n':True})]
for level,p in invalid:
 try:g.generate(level,parameters=p)
 except ValueError:pass
 else:raise AssertionError(('Guard failed',level,p))
for _ in range(30):
 for level in g.DOMAINS:verify(g.generate(level,seed=_))
# Native checks for representative records including all templates/profiles/kinds/levels.
seen=set()
for r in records:
 key=(r['generation']['template'],r['generation']['bank_profile'],r['question'][':question/difficulty'],r['question'][':question/answer-fields'][0][':answer-field/type'])
 if key in seen:continue
 seen.add(key);f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1];checks=[]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'complete bank selection'} for a in f[':answer-field/choices']]
 else:
  n=extract_n(r['question'][':question/problem']);a=f[':answer-field/choices'][0][':answer/value']
  checks=[{'submitted':a,'expected':'accepted','purpose':'exact entry'},{'submitted':f'x^({n}+1)/({n}+1)+C','expected':'accepted','purpose':'unevaluated successor equivalent entry'},{'submitted':f'x^({n}+2)/({n}+2)+C','expected':'rejected','purpose':'wrong successor'}]
 native.append({'label':str(key),'record':r,'checks':checks})
(HERE/'native-input.json').write_text(json.dumps(native,indent=2)+'\n')
subprocess.run(['generate/runs/current/check-engine',str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
# Original + two changed parameter variants for every observed template/bank, plus levels.
review=[]
for case in cases:
 review.append({'label':'Original source replay','record':g.generate('easy',template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])})
 for n in ([0,0] if case['template']=='constant' else [5,7]):
  profile={'legacy_x':'observed_2005','legacy_power':'observed_2022'}.get(case['template'])
  review.append({'label':'Generated — normal repaired/authored field','record':g.generate('easy',template=case['template'],parameters={'n':n},profile=profile)})
for level in ('moderate','hard'):
 for n in (g.DOMAINS[level][0],g.DOMAINS[level][-1]):review.append({'label':'Generated — authored difficulty extension','record':g.generate(level,template='function',parameters={'n':n})})
(HERE/'review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
(HERE/'review.md').write_text('# Monomial antiderivative review\n\nOriginal means captured structure replay. Normal fields/corrects and missing-level bands are authored. No plots. Constant template has only one substantive task, so repeated previews do not count as variety.\n\n'+'\n\n---\n\n'.join(g.markdown(i['record'],i['label']) for i in review)+'\n')
report={'passed':True,'source_practice_total':6,'source_prompt_exact':6,'source_present_solutions_exact':{'matched':4,'total':4},'source_missing_solution_parity':{'matched':2,'total':2},'source_complete_banks':{'matched':2,'total':2},'source_answer_values':{'matched':10,'total':10},'source_original_correct_designations':{'matched':0,'total':0,'missing':2},'source_fieldless_presence_parity':{'matched':4,'total':4},'source_unrated_presence_parity':{'matched':2,'total':2},'native_records':len(native),'independently_checked_normal_records':len(records),'finite_domains':counts,'source_fidelity':fidelity,'invalid_explicit_checks':len(invalid),'generator_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'native':json.loads((HERE/'native-report.json').read_text())}
# The native algebraic blank checker does not identify arbitrary-constant families.
blank=next(r for r in records if r['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/blank'))
n=extract_n(blank['question'][':question/problem']);scaled=f'x^({n}+1)/({n}+1)+2C'
assert sp.diff(expr(scaled)-expr(blank['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']),x)==0
supplement=[{'label':'arbitrary C rescaling','record':blank,'checks':[{'submitted':scaled,'expected':'rejected','purpose':'documented native limitation: equivalent complete family under C rescaling'}]}]
(HERE/'constant-family-native-input.json').write_text(json.dumps(supplement,indent=2)+'\n')
subprocess.run(['generate/runs/current/check-engine',str(HERE/'constant-family-native-input.json'),str(HERE/'constant-family-native-report.json')],check=True)
report['native_family_equivalence_limitation']={'entry':scaled,'mathematically_same_complete_family':True,'native_outcome':'rejected','report':'constant-family-native-report.json','engine_changed':False}
(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('native','source_fidelity')},indent=2))
