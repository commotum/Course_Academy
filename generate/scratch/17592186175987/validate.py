#!/usr/bin/env python3
"""Independent displayed-TeX parser, integral-value QA, source fidelity and native grader.
No reads/writes to EDB. Fails for unexpected correctness/format/identity/grading failures.
Expected source defects are counted explicitly, not reported as correct normal banks.
"""
import importlib.util,json,re,sys,subprocess,hashlib,random
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
BASE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('gen',BASE.with_suffix('.py'));gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
X,Y,R,T=gen.X,gen.Y,gen.R,gen.T

class Tex:
 def __init__(self,text):
  text=text.replace('⁡','').replace('θ',r'\theta').replace('π',r'\pi').replace('\u00a0',' ')
  for name in ['sin','cos','ln']:
   text=text.replace(r'\operatorname{'+name+'}', '\\'+name+' ').replace('{'+name+'}', '\\'+name+' ')
  text=text.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\:','').replace(r'\ ','').replace(r'\qquad','')
  self.ts=re.findall(r'\\[A-Za-z]+|\d+|[a-zA-Z]|[^\s]',text);self.i=0
 def peek(self):return self.ts[self.i] if self.i<len(self.ts) else None
 def pop(self):t=self.peek();self.i+=1;return t
 def group(self):
  o=self.pop();c={'{':'}','(' :')','[':']'}[o];v=self.expr();assert self.pop()==c,(self.ts,self.i,c);return v
 def atom(self):
  t=self.peek()
  if t in ('{','(','['):v=self.group()
  elif t==r'\frac':self.pop();v=self.group()/self.group()
  elif t==r'\sqrt':self.pop();v=sp.sqrt(self.group())
  elif t in (r'\sin',r'\cos',r'\ln',r'\log',r'\exp'):
   self.pop();power=1
   if self.peek()=='^':self.pop();power=self.atom()
   arg=self.atom();v={r'\sin':sp.sin,r'\cos':sp.cos,r'\ln':sp.log,r'\log':sp.log,r'\exp':sp.exp}[t](arg)**power
  elif t and t.isdigit():self.pop();v=sp.Integer(t)
  elif t in ('x','y','r',r'\theta',r'\pi','e'):
   self.pop();v={'x':X,'y':Y,'r':R,r'\theta':T,r'\pi':sp.pi,'e':sp.E}[t]
  else:raise AssertionError(('unsupported actual TeX token',t,self.ts))
  if self.peek()=='^':self.pop();v=v**self.atom()
  return v
 def product(self):
  v=self.atom()
  while self.peek() not in (None,'+','-','}',')',']',',','.',':','=','?'):
   op=self.peek()
   if op in (r'\cdot','*'):self.pop();v*=self.atom()
   elif op=='/':self.pop();v/=self.atom()
   else:v*=self.atom()
  return v
 def expr(self):
  sign=1
  if self.peek() in ('+','-'):sign=-1 if self.pop()=='-' else 1
  v=sign*self.product()
  while self.peek() in ('+','-'):
   sign=-1 if self.pop()=='-' else 1;v+=sign*self.product()
  return v
 def parse(self):
  v=self.expr();assert self.peek() is None,('unconsumed',self.ts[self.i:]);return v

def expr(s):return Tex(s.strip().rstrip('.,?')).parse()
def remove_scale(text):
 m=re.match(r'^(\d+)\\left\((.*)\\right\)$',text,re.S)
 return (int(m[1]),m[2]) if m else (1,text)

def integral_parts(text):
 scale,text=remove_scale(text.strip());text=text.replace(r'{\int }',r'\int').replace(r'\,','').strip().rstrip(' .')
 assert text.startswith(r'\int'),text
 # Bounds can contain nested \frac groups.
 def bounds(text):
  assert text.startswith(r'\int_');i=len(r'\int_')
  def take(i):
   assert text[i]=='{';start=i+1;depth=1;i+=1
   while depth:
    if text[i]=='{':depth+=1
    if text[i]=='}':depth-=1
    i+=1
   return text[start:i-1],i
  lo,i=take(i);assert text[i]=='^';hi,i=take(i+1)
  return expr(lo),expr(hi),text[i:]
 a,b,rest=bounds(text);idx=rest.index(r'\int_');factor=expr(rest[:idx]) if rest[:idx].strip() else 1
 lo,hi,rest=bounds(rest[idx:]);assert lo==0
 rest=re.sub(r'\\(?:text|mathrm)\{d\}', 'd',rest)
 rest=re.sub(r'\s*dr\s*d\\theta\s*$', '',rest)
 g=expr(rest)*factor*scale
 return g,a,b,hi

def bank_math(rec):
 f=rec['question'][':question/answer-fields'][0]
 return [(a,integral_parts(a[':answer/value'])) for a in f[':answer-field/choices']]

def prompt_field(rec):
 prompt=rec['question'][':question/problem'];family=rec['generation']['template']
 if 'Given that $F(x,y)=' in prompt:
  body=re.search(r'F\(x,y\)=⟨(.*?)⟩',prompt,re.S)[1];parts=body.split(r',\,');assert len(parts)==2
  return expr(parts[0]),expr(parts[1])
 block=re.findall(r'\$\$\n(.*?)\n\$\$',prompt,re.S)[0];scale,block=remove_scale(block)
 block=re.sub(r'^(?:\{∮\}_\{C\}|\\oint_C)', '',block);block=block.strip().rstrip('?')
 # dx and dy delimit whole components; no coordinate renaming is involved.
 p,q=re.split(r'\\,dx\s*\+',block,maxsplit=1);q=re.sub(r'\\,dy(?:\\,)?\s*$', '',q)
 return scale*expr(p),scale*expr(q)

def braces(text):
 assert not any(ord(ch)<32 and ch not in '\n\t\r' for ch in text),'unexpected C0 byte'
 depth=0
 for i,ch in enumerate(text):
  if ch in '{}':
   count=0;j=i-1
   while j>=0 and text[j]=='\\':count+=1;j-=1
   if count%2:continue
   depth+=1 if ch=='{' else -1
   assert depth>=0,('brace',text)
 assert depth==0,('brace',text)
 assert text.count('$$')%2==0
 stripped=text.replace('$$','');assert stripped.count('$')%2==0
 assert '+-' not in text and '--' not in text

def integral_stage_math(text,P,Q):
 scale,text=remove_scale(text.strip().rstrip('.'))
 text=text.rstrip('.')
 qx=sp.diff(Q,X);py=sp.diff(P,Y)
 text=text.replace(r'\frac{∂Q}{∂x}', '('+gen.latex(qx)+')').replace(r'\frac{∂P}{∂y}', '('+gen.latex(py)+')')
 text=text.replace(r'\frac{\partial Q}{\partial x}', '('+gen.latex(qx)+')').replace(r'\frac{\partial P}{\partial y}', '('+gen.latex(py)+')')
 if text.startswith('{∬}_{D}') or text.startswith(r'\iint_D'):
  body=re.sub(r'^(?:\{∬\}_\{D\}|\\iint_D)', '',text)
  body=re.sub(r'\\(?:text|mathrm)\{d\}', 'd',body).replace(r'\,','').replace(r'\ ','')
  body=re.sub(r'\s*dA\s*$', '',body)
  return 'cartesian',scale*expr(body)
 if text.startswith('{∬}_{Δ}') or text.startswith(r'\iint_\Delta'):
  body=re.sub(r'^(?:\{∬\}_\{Δ\}|\\iint_\\Delta)', '',text)
  body=re.sub(r'\\(?:text|mathrm)\{d\}', 'd',body).replace(r'\,','').replace(r'\ ','')
  body=re.sub(r'\s*dr\s*d\\theta\s*$', '',body)
  return 'polar',scale*expr(body)
 if text.startswith(r'{\int }') or text.startswith(r'\int_'):
  g,a,b,radius=integral_parts(gen.scaled(text,scale))
  return 'polar',g
 if text.startswith('{∮}_{C}') or text.startswith(r'\oint_C'):
  body=re.sub(r'^(?:\{∮\}_\{C\}|\\oint_C)', '',text)
  if 'F' in body:return None
  p,q=re.split(r'\\,dx\s*\+',body,maxsplit=1);q=re.sub(r'\\,dy(?:\\,)?\s*$', '',q)
  assert sp.simplify(scale*expr(p)-P)==0 and sp.simplify(scale*expr(q)-Q)==0,('printed line-integral row disagrees with prompt',body)
  return None
 return None

def check_solution_stages(rec,P,Q,curl,expected):
 solution=rec['question'][':question/worked-solution']
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',solution,re.S)
 # Independently check actual displayed cross partials as COMPLETE RHS slots.
 for block in blocks:
  if r'\frac{∂P}{∂y}=' in block:
   py,qx=re.search(r'\\frac\{∂P\}\{∂y\}=(.*?),\\,\\frac\{∂Q\}\{∂x\}=(.*?)\.\\end',block,re.S).groups()
   assert sp.simplify(expr(py)-sp.diff(P,Y))==0
   assert sp.simplify(expr(qx)-sp.diff(Q,X))==0
  elif r'\frac{\partial P}{\partial y}=' in block:
   py,qx=re.search(r'\\frac\{\\partial P\}\{\\partial y\}=(.*?),\\qquad\\frac\{\\partial Q\}\{\\partial x\}=(.*?)\.',block,re.S).groups()
   assert sp.simplify(expr(py)-sp.diff(P,Y))==0
   assert sp.simplify(expr(qx)-sp.diff(Q,X))==0
  if not block.startswith(r'\begin{aligned}'):continue
  body=block.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}')
  stages=re.split(r'\\\\\s*&\s*=',body)
  first=stages.pop(0)
  if re.search(r'&\s*=',first):stages=re.split(r'&\s*=',first,maxsplit=1)+stages
  for stage in stages:
   result=integral_stage_math(stage,P,Q)
   if result:
    kind,v=result;target=curl if kind=='cartesian' else expected
    assert sp.trigsimp(v-target)==0,('printed operative stage disagrees with prompt',rec['generation']['template'],kind,stage,v,target)

def check_normal(rec):
 q=rec['question'];gmeta=rec['generation'];template=gmeta['template'];p=gmeta['parameters']
 assert set(rec['knowledge_point'])=={'db_id','id','title'}
 braces(q[':question/problem']);braces(q[':question/worked-solution'])
 for line in q[':question/problem'].splitlines():
  if line.strip():assert not line.startswith('    '),'normal prompt would render as an indented code block'
 for f in q[':question/answer-fields']:
  ids=[a[':answer/id'] for a in f[':answer-field/choices']];assert len(ids)==len(set(ids));assert f[':answer-field/correct'][1] in ids
  if f[':answer-field/type'].endswith('blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
  for a in f[':answer-field/choices']:braces(a[':answer/value'])
 if template=='polar_blanks':
  prompt=q[':question/problem']
  assert len(prompt.splitlines())<=9 and '\n\n\n' not in prompt,'capture whitespace retained'
  assert 'where $a=$ {{field-2}} and $b=$ {{field-3}}.' in prompt,'angular/radial placeholder roles swapped'
  for key in ('field-1','field-2','field-3'):
   marker='{{'+key+'}}';assert prompt.count(marker)==1
   assert prompt[:prompt.index(marker)].count('$')%2==0,'widget lies inside math delimiters'
  found={f[':answer-field/key']:expr(f[':answer-field/choices'][0][':answer/value']) for f in q[':question/answer-fields']}
  assert sp.trigsimp(found['field-1']+3*p['scale']*R**3*sp.sin(2*T))==0
  assert found['field-2']==2*sp.pi and found['field-3']==p['radius']
  assert '-6xy' in q[':question/problem']
  supplied=re.search(r'\{∬\}_\{D\}(.*?)\\,\\text\{d\}A',q[':question/problem'],re.S)[1]
  curl=expr(supplied);assert sp.expand(curl+6*p['scale']*X*Y)==0
  expected=sp.trigsimp(curl.subs({X:R*sp.cos(T),Y:R*sp.sin(T)})*R)
  check_solution_stages(rec,sp.Integer(0),sp.Integer(0),curl,expected)
  source=gen.QS['q-169204'][':question/worked-solution']
  for block in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',source,re.S):
   for component in re.split(r'\\\\\s*&\s*=|&\s*=',block):
    component=re.sub(r'(\{\\int \}_\{0\}\^\{)2(\})',lambda m:m[1]+str(p['radius'])+m[2],component.strip())
    assert component in q[':question/worked-solution'],('missing continuation operative component',component)
  return
 P,Q=prompt_field(rec);curl=sp.expand(sp.diff(Q,X)-sp.diff(P,Y));expected=sp.trigsimp(curl.subs({X:R*sp.cos(T),Y:R*sp.sin(T)})*R)
 check_solution_stages(rec,P,Q,curl,expected)
 if template in gen.SPECS:a,b=gen.SPECS[template][4:6]
 else:a,b=0,sp.pi/2
 f=q[':question/answer-fields'][0];vals=[]
 for option,parts in bank_math(rec):
  g,aa,bb,rr=parts;v=gen.value(g,aa,bb,rr);vals.append(v)
  if option[':answer/id']==f[':answer-field/correct'][1]:
   assert sp.trigsimp(g-expected)==0,(template,g,expected)
   assert (aa,bb,rr)==(a,b,p['radius'])
 gen.compare_values(vals)
 # Actual final displayed repeated integral agrees with prompt-derived integrand.
 solution=q[':question/worked-solution'];last=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S)[-1]
 last=last.split('&=')[-1] if '&=' in last else last.split('& =')[-1]
 last=last.strip().rstrip('.');parts=integral_parts(last)
 assert sp.trigsimp(parts[0]-expected)==0,(template,'solution',parts,expected)
 assert parts[1:]==(a,b,p['radius'])
 # Preserve the source chain structurally, even at changed parameters.
 if template in gen.SPECS:
  source=gen.QS[gen.SPECS[template][0]][':question/worked-solution']
  assert source.count(r'\\  & =')==solution.count(r'\\  & =')
  for block in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',source,re.S):
   if r'\frac{∂P}{∂y}=' in block:continue
   for component in re.split(r'\\\\\s*&\s*=|&\s*=',block):
    component=component.strip()
    component=re.sub(r'(\{\\int \}_\{0\}\^\{)'+str(gen.SPECS[template][3])+r'(\})',lambda m:m[1]+str(p['radius'])+m[2],component)
    if template=='cubic_y':component=component.replace(r'\,dx-(y{e}^{y+1}+x)',r'\,dx+(y{e}^{y+1}+x)')
    if template=='square_difference':component=component.replace('{e}^{1/y}','{e}^{y}')
    if template=='cubic_log':component=component.replace('{∬}_{D}(1-3{y}^{2})','{∬}_{D}(1-2{y}^{2})')
    assert component in solution,('missing source operative component',template,component)
  for stage in re.findall(r'\$\$\n(.*?)\n\$\$',source,re.S):
   if r'\operatorname{sin}⁡(2\theta )' in stage:assert r'\operatorname{sin}⁡(2\theta )' in solution
   if '2xy-' in stage and '\\operatorname{cos}' in stage:assert '4xy-' in solution and '(2xy-' in solution


def engine_item(rec,label):
 checks=[]
 for fi,f in enumerate(rec['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('radio'):
   for a in f[':answer-field/choices']:checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned radio identity'})
  else:
   key=f[':answer-field/key'];canonical=f[':answer-field/choices'][0][':answer/value']
   eq={'field-1':latex_equiv(rec),'field-2':'pi+pi','field-3':str(rec['generation']['parameters']['radius']*2)+'/2'}[key]
   if key=='field-1':checks.append({'field_index':fi,'submitted':str(-6*rec['generation']['parameters']['scale'])+r'r^3\sin(\theta)\cos(\theta)','expected':'unresolved','purpose':'documented native limitation: mathematically equal product/double-angle identity unsupported'})
   checks += [{'field_index':fi,'submitted':canonical,'expected':'accepted','purpose':'canonical blank'}, {'field_index':fi,'submitted':eq,'expected':'accepted','purpose':'independently expanded equivalent blank'},{'field_index':fi,'submitted':canonical+'+1','expected':'rejected','purpose':'wrong blank'}]
 return {'label':label,'record':rec,'checks':checks}
def latex_equiv(rec):
 s=rec['generation']['parameters']['scale']
 return str(-s)+r'r^3\sin(2\theta)'+str(-2*s)+r'r^3\sin(2\theta)'

def main():
 cases=[];reviews=[];engine=[];summary={'basis':gen.SOURCE['basis'],'python':sys.version.split()[0],'sympy':sp.__version__,'source_questions':len(gen.QS),'source_choices':0,'source_distractors':0,'source_banks':0,'raw_exact_prompt':0,'raw_exact_solution':0,'raw_complete_banks':0,'raw_correct_designations':0,'source_defects':[]}
 for template,specification in gen.SPECS.items():
  sid,P,Q,rad,a,b=specification;q=gen.QS[sid]
  print('source/variants '+sid,flush=True)
  params={'scale':1,'radius':rad};case={'source_id':sid,'template':template,'parameters':params,'bank_profile':'observed'};cases.append(case)
  rec=gen.generate('moderate',template=template,parameters=params,profile='observed');rq=rec['question']
  assert rq[':question/problem']==q[':question/problem'],('prompt fidelity',sid)
  assert rq[':question/worked-solution']==q[':question/worked-solution'],('solution fidelity',sid)
  summary['raw_exact_prompt']+=1;summary['raw_exact_solution']+=1
  for sf,gf in zip(q[':question/answer-fields'],rq[':question/answer-fields']):
   assert sf[':answer-field/key']==gf[':answer-field/key'];assert sf[':answer-field/type'][':db/ident']==gf[':answer-field/type']
   sv=sorted(z[':answer/value'] for z in sf[':answer-field/choices']);gv=sorted(z[':answer/value'] for z in gf[':answer-field/choices']);assert sv==gv,('bank',sid,sv,gv)
   correct=next(z[':answer/value'] for z in gf[':answer-field/choices'] if z[':answer/id']==gf[':answer-field/correct'][1]);assert correct==sf[':answer-field/correct'][':answer/value']
   summary['source_choices']+=len(sv);summary['source_distractors']+=len(sv)-1;summary['source_banks']+=1;summary['raw_complete_banks']+=1;summary['raw_correct_designations']+=1
  if template in gen.BANKS:
   parsed=[integral_parts(z[':answer/value']) for z in q[':question/answer-fields'][0][':answer-field/choices']]
   for actual,recipe in zip(parsed,gen.BANKS[template]):
    assert sp.trigsimp(actual[0]-recipe[0])==0 and actual[1:]==recipe[1:],('raw displayed option recipe mismatch',sid,actual,recipe)
   vals=[gen.value(*z) for z in parsed]
   collisions=[]
   for i,v in enumerate(vals):
    for j,w in enumerate(vals[:i]):
     if sp.simplify(v-w)==0 or abs(gen.numeric(v)-gen.numeric(w))<1e-10:collisions.append([j,i])
   if collisions:summary['source_defects'].append({'source_id':sid,'type':'integral-value ambiguity','choice_index_pairs':collisions,'values':[str(v) for v in vals]})
  engine.append(engine_item(rec,'raw:'+sid))
  evidence=gen.generate('moderate',73,template,parameters={'scale':2,'radius':rad},profile='observed')
  reviews.append(evidence);engine.append(engine_item(evidence,'changed-observed:'+sid))
  for seed in [21,37]:
   generated=gen.generate('moderate',seed,template);check_normal(generated);reviews.append(generated);engine.append(engine_item(generated,'normal:'+sid+':'+str(seed)))
 for level in ('easy','hard'):
  for seed in [21,37]:
   rec=gen.generate(level,seed);check_normal(rec);reviews.append(rec);engine.append(engine_item(rec,level+str(seed)))
 # Every supported default family is available through random normal sampling.
 families=set();unique={l:set() for l in ('easy','moderate','hard')}
 for level in unique:
  print('sampling '+level,flush=True)
  for seed in range(35):
   rec=gen.generate(level,seed);check_normal(rec);families.add(rec['generation']['template']);unique[level].add(rec['generation']['mathematical_fingerprint'])
 assert set(gen.SPECS)<=families
 # Public field-type selectors filter implicit family choice. Both plain and
 # enum-form aliases are exercised, including root's seed19 regression.
 selector_checks=0;selector_families={}
 for requested in ('radio',':answer-field.type/radio','blank',':answer-field.type/blank'):
  selected=set();expected=':answer-field.type/'+requested.split('/')[-1]
  for seed in range(25):
   rec=gen.generate_moderate(seed=seed,field_type=requested)
   assert all(f[':answer-field/type']==expected for f in rec['question'][':question/answer-fields']),('selector mismatch',requested,seed)
   check_normal(rec);selected.add(rec['generation']['template']);selector_checks+=1
  selector_families[requested]=sorted(selected)
 assert selector_families['radio']==selector_families[':answer-field.type/radio']
 assert selector_families['blank']==selector_families[':answer-field.type/blank']==['polar_blanks']
 summary['field_type_selector_checks']=selector_checks;summary['field_type_selector_families']=selector_families
 # All source families also exercise a common changed amplitude and radius.
 for template in gen.SPECS:
  for scale,radius in [(2,2),(5,4)]:
   try:r=gen.generate('moderate',99,template,parameters={'scale':scale,'radius':radius})
   except ValueError:continue # Explicit whole-bank ambiguity rejection, checked above.
   check_normal(r)
 # Mutation regressions distinguish mathematics, structure and formatting.
 import copy
 base=gen.generate('moderate',21,'mixed_cancel')
 for old,new in [(r'(4xy-\operatorname{cos}⁡x-(2xy-\operatorname{cos}⁡x))','2xy'),(r'\frac{∂P}{∂y}=','\\frac{∂P}{∂y}=1+'),('Applying Green', '\x0cpplying Green')]:
  bad=copy.deepcopy(base);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(old,new)
  assert bad['question'][':question/worked-solution']!=base['question'][':question/worked-solution']
  try:check_normal(bad)
  except AssertionError:pass
  else:raise AssertionError('mutation escaped validation')
 # Continuation presentation mutations must fail independently of field order.
 continuation=gen.generate('moderate',21,'polar_blanks')
 for broken in [continuation['question'][':question/problem'].replace('where $a=$','    where $a=$'),continuation['question'][':question/problem'].replace('{{field-2}}','{{swap}}').replace('{{field-3}}','{{field-2}}').replace('{{swap}}','{{field-3}}'),continuation['question'][':question/problem'].replace('{{field-1}}','$ {{field-1}} $')]:
  bad=copy.deepcopy(continuation);bad['question'][':question/problem']=broken
  try:check_normal(bad)
  except AssertionError:pass
  else:raise AssertionError('continuation presentation mutation escaped validation')
 # Identity seed/order and parameter alias independence; profiles are excluded
 # from mathematical fingerprints and included through actual rendered content.
 for rec in reviews:
  l=rec['question'][':question/difficulty'].split('/')[-1];gm=rec['generation'];r=gen.generate(l,99,gm['template'],parameters=gm['parameters'],profile=gm['profile'])
  assert r['question'][':question/id']==rec['question'][':question/id']
  assert r['generation']['mathematical_fingerprint']==gm['mathematical_fingerprint']
 # Invalid explicit difficulty workload inputs must be rejected, not resampled.
 for l,t,p in [('easy','easy_constant',{'radius':7,'a':1,'b':2}),('hard','hard_polynomial',{'radius':2,'a':0,'c':2}),('moderate','constant',{'scale':2,'radius':5})]:
  try:gen.generate(l,template=t,parameters=p)
  except ValueError:pass
  else:raise AssertionError('invalid explicit parameter accepted')
 summary['source_defects'] += [{'source_id':'q-125719','type':'wrong minus dy in applying row','repair':'plus dy'}, {'source_id':'q-126516','type':'undefined e^(1/y) on y=0 inside/boundary','repair':'e^y everywhere'}, {'source_id':'q-169204','type':'missing prior-part region context','repair':'add standalone sector diagram'}]
 (BASE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(BASE/'review.json').write_text(json.dumps(reviews,indent=2,ensure_ascii=False)+'\n');(BASE/'engine-input.json').write_text(json.dumps(engine,indent=2,ensure_ascii=False)+'\n')
 subprocess.run(['generate/runs/current/check-engine',str(BASE/'engine-input.json'),str(BASE/'engine-report.json')],check=True)
 report=json.loads((BASE/'engine-report.json').read_text());summary['native_grading']={k:report[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']};summary['sampled_unique_tasks']={k:len(v) for k,v in unique.items()};summary['normal_family_coverage']=sorted(families);summary['normal_review_records']=sum(r['generation']['eligible_for_learning'] for r in reviews);summary['changed_observed_evidence_records']=sum(r['generation']['evidence_only'] for r in reviews);summary['normal_correctness']='passed';summary['original_bank_fidelity']='passed all values and designations; source mathematical defects retained evidence-only';summary['source_correct_value_ambiguity_banks']=sum(any(q[':question/answer-fields'][0][':answer-field/choices'][i][':answer/id']==q[':question/answer-fields'][0][':answer-field/correct'][':answer/id'] or q[':question/answer-fields'][0][':answer-field/choices'][j][':answer/id']==q[':question/answer-fields'][0][':answer-field/correct'][':answer/id'] for i,j in d['choice_index_pairs']) for d in summary['source_defects'] if d['type']=='integral-value ambiguity' for q in [gen.QS[d['source_id']]])
 summary['source_defects'].append({'source_id':'q-126707','type':'wrong Cartesian coefficient in final substitution row','repair':'1-2y^2 replaces 1-3y^2'})
 summary['source_solution_mathematical_repairs']=3
 summary['normal_supported_full_chains']=len(gen.SPECS)
 summary['native_equivalent_entry_limitation']='Product/double-angle trig identity unresolved on integrand blank; nontrivial distributed double-angle and every canonical blank are accepted.'
 summary['raw_correct_math_banks']=summary['source_banks']-len([d for d in summary['source_defects'] if d['type']=='integral-value ambiguity']);summary['engine_sha256']=hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest()
 (BASE/'validation.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
 review='# Original and generated review\n\nSources: math basis2272 (earlier capture 1356 retained). Raw observed records remain evidence-only.\n\n'
 for case in cases:
  sid=case['source_id'];q=gen.QS[sid];review+='## '+sid+' — observed moderate\n\n'+q[':question/problem']+'\n\n'
  for f in q[':question/answer-fields']:
   review+='Field '+f[':answer-field/key']+'\n\n'
   for z in f[':answer-field/choices']:review+=('$'+z[':answer/value']+'$'+(' (keyed correct)' if z[':answer/id']==f[':answer-field/correct'][':answer/id'] else '')+'\n\n')
  review+=q[':question/worked-solution']+'\n\n'
  for rec in reviews:
   if rec['generation']['source_id']==sid:review+='### Generated variation '+('— evidence-only historical bank ' if rec['generation']['evidence_only'] else '— normal practice ')+rec['generation']['profile']+'\n\n'+gen.markdown(rec)+'\n\n'
 for rec in reviews:
  if rec['generation']['source_id'] is None:review+='## Authored '+rec['question'][':question/difficulty'].split('/')[-1]+'\n\n'+gen.markdown(rec)+'\n\n'
 (BASE/'review.md').write_text(review);print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
