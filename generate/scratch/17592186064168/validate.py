#!/usr/bin/env python3
"""Independent displayed-math, full source prose/bank/presence and native QA.

The TeX reader below evaluates actual printed integrals/formal derivatives and
all unsimplified arithmetic components. It does not read generation parameters
to determine correctness. Source fidelity, inferred completions, and opaque
interpretation limits are reported with separate honest denominators.
"""
import importlib.util, json, re, hashlib, subprocess, uuid, sys, copy
sys.dont_write_bytecode=True
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('g',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x=s.Symbol('x',positive=True);c=s.Symbol('C',real=True)

def write(name,value):
 (ROOT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

class Tex:
 """Small exact recursive reader for the observed scalar root/power syntax.

 Parses groups, fractions, radicals, rational exponent arithmetic, products,
 formal derivatives and displayed integral inputs. Unknown tokens fail closed.
 """
 def __init__(self,tex):
  tex=tex.replace(r'\frac{\text{d}}{\text{d}x}','D').replace(r'\,','').replace(r'\cdot','*')
  self.tokens=re.findall(r'\\frac|\\sqrt|D|[xC]|\d+|[{}()\[\]+*/^\-]',tex)
  remainder=re.sub(r'\\frac|\\sqrt|D|[xC]|\d+|[{}()\[\]+*/^\-]|\s','',tex)
  assert not remainder,('Unparsed printed TeX',remainder,tex)
  self.pos=0
 def peek(self):return self.tokens[self.pos] if self.pos<len(self.tokens) else None
 def pop(self,token=None):
  value=self.peek();assert value is not None,'Unexpected end'
  if token is not None:assert value==token,(value,token,self.tokens)
  self.pos+=1;return value
 def expr(self):
  value=self.product()
  while self.peek() in ('+','-'):
   op=self.pop();right=self.product();value=value+right if op=='+' else value-right
  return value
 def product(self):
  value=self.pow()
  while self.peek() not in (None,'}',')',']','+','-'):
   if self.peek() in ('*','/'):
    op=self.pop();right=self.pow();value=value*right if op=='*' else value/right
   else:value*=self.pow()
  return value
 def pow(self):
  value=self.atom()
  if self.peek()=='^':self.pop();value=value**self.atom()
  return value
 def group(self):
  opening=self.pop();closing={'{':'}','(':')','[':']'}[opening]
  value=self.expr();self.pop(closing);return value
 def atom(self):
  t=self.peek()
  if t in ('{','(','['):return self.group()
  if t=='-':self.pop();return -self.atom()
  if t=='+':self.pop();return self.atom()
  if t==r'\frac':self.pop();return self.group()/self.group()
  if t==r'\sqrt':
   self.pop();index=self.group() if self.peek()=='[' else s.Integer(2);return self.group()**(1/index)
  if t=='D':self.pop();return s.diff(self.group(),x)
  self.pop()
  if t=='x':return x
  if t=='C':return c
  assert t.isdigit(),('Unknown atom',t)
  return s.Integer(t)
 def read(self):
  e=self.expr();assert self.pos==len(self.tokens);return e

def math(tex):
 tex=tex.strip().rstrip('.').replace('✓','').strip()
 if tex.startswith(r'\int '):
  body=tex[len(r'\int '):]
  assert body.endswith(r'\,\text{d}x'),('Integral differential missing',tex)
  return s.integrate(Tex(body[:-len(r'\,\text{d}x')]).read(),x)
 return Tex(tex).read()

def eq(a,b):return s.simplify(a-b)==0

def family(a,b):
 # Exact general solution comparison is modulo arbitrary constant rescaling/shift.
 # Each option is affine in C or a specific antiderivative, never mixes C and x.
 assert s.diff(a,c,x)==0 and s.diff(b,c,x)==0
 assert s.diff(a,c,2)==0 and s.diff(b,c,2)==0
 return eq(s.diff(a-b,x),0)

def balanced(text):
 assert text.count('$')%2==0,'Odd mathematical delimiters'
 depth=0
 for char in text:
  if char=='{':depth+=1
  if char=='}':depth-=1
  assert depth>=0
 assert depth==0,'Unbalanced TeX groups'
 assert '--' not in text and '+-' not in text

def task(q):
 m=re.search(r'\$([^$]+)\$',q[':question/problem']);assert m
 tex=m[1].rstrip('.')
 return math(tex)

def solution_audit(q,integrand):
 worked=q[':question/worked-solution'];balanced(worked)
 # Verify prose math independently, including radical equality and stated n.
 inline=re.findall(r'(?<!\$)\$([^$]+)\$(?!\$)',worked)
 n=None
 for formula in inline:
  formula=formula.rstrip('.')
  if formula.startswith('n='):
   n=math(formula[2:]);assert eq(x**n,integrand)
  elif '=' in formula:
   a,b=formula.split('=');assert eq(math(a),math(b));assert eq(math(a),integrand)
 assert n is not None
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',worked,re.S)
 assert len(blocks)==2
 rows=[row.strip() for row in blocks[0].split(r'\\')]
 is_root=rows[0].split('&')[0].strip().startswith(r'\int \sqrt')
 expected_integral_rows=4 if is_root else 3
 assert len(rows)==expected_integral_rows,(len(rows),expected_integral_rows)
 evaluated=[]
 for i,row in enumerate(rows):
  assert row.count('& =')==1
  lhs,rhs=row.split('& =');rhs=rhs.strip()
  if lhs.strip():assert family(math(lhs.strip()),math(rhs))
  e=math(rhs);assert eq(s.diff(e,x),integrand),('Printed primitive arithmetic wrong',rhs,e,integrand)
  evaluated.append(e)
 arithmetic=rows[1:] if is_root else rows
 # Structural guards preserve unsimplified increment, division by new exponent,
 # and final reduced coefficient: CAS equality alone cannot establish operations.
 assert re.search(r'\^\{[^}]+\+1\}',arithmetic[0])
 assert '+1)' in arithmetic[0]
 assert '+1' not in arithmetic[1] and r'}{(\frac{' in arithmetic[1]
 assert '+1' not in arithmetic[2] and r'}{(\frac{' not in arithmetic[2]
 checkrows=[row.strip() for row in blocks[1].split(r'\\')]
 assert len(checkrows)==5
 assert checkrows[0].startswith(r'\frac{\text{d}}{\text{d}x}(')
 assert r'\frac{\text{d}}{\text{d}x}(C)' in checkrows[1]
 assert r'\frac{\text{d}}{\text{d}x}(' in checkrows[2] and '+0' in checkrows[2]
 assert r'\cdot' in checkrows[3] and '-1}' in checkrows[3]
 assert '✓' in checkrows[4]
 primitive=None
 for i,row in enumerate(checkrows):
  form=row.removesuffix('& =').strip().replace('✓','').replace(r'\,','')
  assert eq(math(form),integrand),('Printed derivative operator/arithmetic wrong',i,form)
  if i==0:
   formal=form[len(r'\frac{\text{d}}{\text{d}x}('):-1]
   primitive=math(formal);assert primitive.has(c),'Formal primitive+C stage must retain C'
 assert family(primitive,evaluated[-1])
 return {'integration_rows':len(rows),'derivative_rows':5,'n':str(n),'integrand':str(integrand)}

def audit(record):
 assert set(record)=={'knowledge_point','question','generation'}
 assert record['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 q=record['question'];meta=record['generation'];uuid.UUID(q[':question/id']);balanced(q[':question/problem'])
 assert meta['evidence_only']==meta['ineligible_for_learning']==(not meta['eligible_for_learning'])
 if meta['eligible_for_learning']:assert 'Work on $x>0$.' in q[':question/problem']
 integrand=task(q)
 exponent=integrand.as_powers_dict().get(x,0);assert eq(integrand,x**exponent) and exponent>0
 actual_fingerprint=g.fingerprint({'integrand':str(exponent),'domain':'x>0','radical_to_power':r'\sqrt' in re.search(r'\$([^$]+)\$',q[':question/problem'])[1]})
 assert meta['mathematical_fingerprint']==actual_fingerprint,'Printed task fingerprint mismatch'
 actual_kind=q[':question/answer-fields'][0][':answer-field/type'].split('/')[-1] if q.get(':question/answer-fields') else None
 actual_content=g.fingerprint({'version':g.VERSION,'question':{k:q[k] for k in (':question/problem',':question/difficulty',':question/worked-solution') if k in q},'field_type':actual_kind,'values':sorted(a[':answer/value'] for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices']),'task':actual_fingerprint})
 assert meta['content_fingerprint']==actual_content and q[':question/id']==g.uid(actual_content),'Actual content identity mismatch'
 if ':question/worked-solution' in q:solution_audit(q,integrand)
 for f in q.get(':question/answer-fields',[]):
  uuid.UUID(f[':answer-field/id']);correct=f.get(':answer-field/correct')
  if correct:assert correct[0]==':answer/id'
  kind=f[':answer-field/type'].split('/')[-1]
  if kind=='blank' and meta['eligible_for_learning']:assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
  seen=[];matched=0
  for a in f[':answer-field/choices']:
   uuid.UUID(a[':answer/id']);balanced(a[':answer/value']);assert a[':answer/type']==':answer.type/math'
   value=math(a[':answer/value']);valid=eq(s.diff(value,x),integrand)
   if kind=='blank':assert not value.has(c),'Fragment must omit additive constant'
   if correct and correct[1]==a[':answer/id']:assert valid;matched+=1
   elif correct:assert not valid,('Wrong option is another valid antiderivative',a)
   for previous in seen:assert not family(value,previous),'Equivalent whole solution families'
   seen.append(value)
  if correct:assert matched==1
  else:assert meta['evidence_only']
 return str(integrand)

def normalize(value):
 """Ignore evidence/local IDs and choice order; normalize captured ref enum form.

 Missing attributes are never invented. Correct refs compare their full answer
 value/type because local identities are intentionally regenerated.
 """
 if isinstance(value,list):return [normalize(v) for v in value]
 if not isinstance(value,dict):return value
 if set(value)=={':db/ident'}:return value[':db/ident']
 out={k:normalize(v) for k,v in value.items() if k not in (':db/id',':question/id',':answer/id',':answer-field/id',':question/math-academy-id')}
 if ':answer-field/choices' in out:out[':answer-field/choices']=sorted(out[':answer-field/choices'],key=lambda a:a[':answer/value'])
 return out

def source_compare(sid,r):
 original=g.SOURCES[sid];q=r['question'];assert set(original)==set(q),('Question attribute presence',sid)
 for k in (':question/problem',':question/worked-solution'):
  assert (k in original)==(k in q)
  if k in original:assert original[k]==q[k],('Whole prose/mask fidelity',sid,k)
 if ':question/difficulty' in original:assert original[':question/difficulty'][':db/ident']==q[':question/difficulty']
 if ':question/answer-fields' in original:
  assert len(original[':question/answer-fields'])==len(q[':question/answer-fields'])
  for old,new in zip(original[':question/answer-fields'],q[':question/answer-fields']):
   assert set(old)==set(new),('Field presence',sid)
   assert old[':answer-field/type'][':db/ident']==new[':answer-field/type']
   assert old[':answer-field/key']==new[':answer-field/key']
   oldbank=old[':answer-field/choices'];newbank=new[':answer-field/choices']
   assert sorted(a[':answer/value'] for a in oldbank)==sorted(a[':answer/value'] for a in newbank),('Full bank textual fidelity',sid)
   for a in newbank:
    b=next(b for b in oldbank if b[':answer/value']==a[':answer/value']);assert set(a)==set(b)
    assert a[':answer/type']==b[':answer/type'][':db/ident'];assert eq(math(a[':answer/value']),math(b[':answer/value']))
   if ':answer-field/correct' in old:
    expected=old[':answer-field/correct'][':answer/value'];actual=next(a for a in newbank if a[':answer/id']==new[':answer-field/correct'][1])[':answer/value'];assert expected==actual
 return {'source_id':sid,'full_prompt_exact':True,'solution_present':':question/worked-solution' in original,'full_solution_exact':True if ':question/worked-solution' in original else None,'question_field_answer_key_presence':True,'complete_bank_exact':True if ':question/answer-fields' in original else None,'correct_designation_present':any(':answer-field/correct' in f for f in original.get(':question/answer-fields',[]))}

def grading_item(label,record):
 checks=[]
 for i,f in enumerate(record['question'].get(':question/answer-fields',[])):
  if ':answer-field/correct' not in f:return None
  if f[':answer-field/type'].endswith('/radio'):
   for a in f[':answer-field/choices']:
    checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'visible owned option designation'})
  else:
   answer=f[':answer-field/choices'][0][':answer/value'];value=math(answer);n=s.diff(value,x);exponent=next(iter(n.as_powers_dict().values())) if n==1 else n.as_powers_dict().get(x,0)
   # Independent actual printed power quotient: no simplification before submission.
   equivalent='x^{'+str(exponent+1)+'}/('+str(exponent)+'+1)'
   checks += [{'field_index':i,'submitted':answer,'expected':'accepted','purpose':'canonical primitive fragment'},
              {'field_index':i,'submitted':equivalent,'expected':'accepted','purpose':'unsimplified equivalent rational-power quotient'},
              {'field_index':i,'submitted':'0','expected':'rejected','purpose':'incorrect fragment'},
              {'field_index':i,'submitted':answer+'+1','expected':'rejected','purpose':'constant-free supplied fragment criterion'}]
 return {'label':label,'record':record,'checks':checks} if checks else None

def main():
 fidelity=[];raws=[];normal=[];variants=[];cases=[];all_records=[];display_count=0
 for sid,(level,template,p,d) in g.SOURCE_SPEC.items():
  case={'source_id':sid,'template':template,'parameters':{'p':p,'d':d},'level':level,'bank_profile':'raw:'+sid}
  cases.append(case)
  raw=g.generate(level,profile=case['bank_profile'],parameters=case['parameters']);audit(raw);fidelity.append(source_compare(sid,raw));raws.append(raw)
  completed=g.generate(level,profile='completed:'+sid);audit(completed);normal.append(completed)
  params=next({'p':a,'d':b} for a,b in g.domain(level,template) if (a,b)!=(p,d) and (sid!='q-29635' or a==1))
  changed=g.generate(level,seed=10,template=template,parameters=params,profile='completed:'+sid);audit(changed);variants.append(changed)
  changedraw=g.generate(level,seed=99,template=template,parameters=params,profile='raw:'+sid);audit(changedraw)
  assert changedraw['question'][':question/problem']!=raw['question'][':question/problem']
  for k in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (k in raw['question'])==(k in changedraw['question'])
 for level in g.TEMPLATES:
  for template in g.TEMPLATES[level]:
   for i,(p,d) in enumerate(g.domain(level,template)):
    r=g.generate(level,seed=i,template=template,parameters={'p':p,'d':d});audit(r);all_records.append(r);display_count+=1
    r2=g.generate(level,seed=i+700,template=template,parameters={'p':p,'d':d})
    assert r['question'][':question/id']==r2['question'][':question/id']
    assert r['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint']
   for i in (0,1):
    pairs=g.domain(level,template)
    pair=next((p,d) for p,d in reversed(pairs) if (p>d if i==1 else p<d)) if level in ('moderate','hard') else pairs[0]
    params=dict(zip(('p','d'),pair));r=g.generate(level,seed=27+i,template=template,parameters=params);audit(r);variants.append(r)
 assert len(g.MODERATE_DOMAIN)==22 and len(g.HARD_DOMAIN)==41
 for level,pairs in [('moderate',g.MODERATE_DOMAIN),('hard',g.HARD_DOMAIN)]:
  assert len({s.Rational(p,d) for p,d in pairs})==len(pairs)
  assert any(p>d for p,d in pairs) and any(p<d for p,d in pairs)
  assert all(p<=20 and p+d<=24 and s.Rational(p,d)<=5 and s.gcd(p,d)==1 for p,d in pairs)
 # Explicit guards and sampler exercise; guards apply even to raw evidence.
 invalid=[('easy','power',{'p':2,'d':4}),('easy','power',{'p':7,'d':2}),('moderate','root_moderate',{'p':1,'d':3}),('moderate','root_moderate',{'p':2,'d':5}),('hard','root_find',{'p':1,'d':5}),('hard','root_find',{'p':5,'d':5}),('moderate','root_moderate',{'p':21,'d':4}),('moderate','root_moderate',{'p':11,'d':2}),('hard','root_find',{'p':17,'d':8}),('hard','root_find',{'p':23,'d':5}),('hard','root_find',{'p':2,'d':6}),('hard','root_find',{'p':9,'d':11}),('easy','fragment_compact',{'p':3,'d':4}),('hard','root_find',{'p':2,'d':9}),('easy','power',{'p':True,'d':2}),('easy','power',{'p':0,'d':3}),('easy','power',{'p':1.0,'d':3})]
 for level,t,p in invalid:
  try:g.generate(level,template=t,parameters=p)
  except ValueError:pass
  else:raise AssertionError(('Explicit workload guard failed',level,t,p))
 try:g.generate_easy(profile='raw:q-29635',parameters={'p':2,'d':3})
 except ValueError:pass
 else:raise AssertionError('Opaque unit-power evidence guard')
 samples=[]
 for level in g.TEMPLATES:
  for seed in range(40):r=g.generate(level,seed);audit(r);samples.append(r)
 # Same mathematical task across bank/layout retains fingerprint, but content differs.
 a=g.generate_easy(template='power',parameters={'p':1,'d':3});b=g.generate_easy(template='legacy_power_radio',parameters={'p':1,'d':3})
 assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint'];assert a['question'][':question/id']!=b['question'][':question/id']
 c0=g.generate_easy(template='legacy_power_radio',profile='completed:q-29635');assert c0['generation']['evidence_only']
 assert c0['question'][':question/id']!=b['question'][':question/id']
 # Deliberate wrong printed content / designation must fail independently.
 mutation_cases=[]
 base=g.generate_easy(template='power',parameters={'p':1,'d':4})
 bad=copy.deepcopy(base);bad['question'][':question/problem']=bad['question'][':question/problem'].replace('1/4','2/4',1);mutation_cases.append(bad)
 bad=copy.deepcopy(base);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('1/4+1','1/4+2',1);mutation_cases.append(bad)
 bad=copy.deepcopy(base);bad['generation']['content_fingerprint']='false';mutation_cases.append(bad)
 rb=g.generate_moderate(template='legacy_root_radio',parameters={'p':2,'d':3});bad=copy.deepcopy(rb);f=bad['question'][':question/answer-fields'][0];f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])];mutation_cases.append(bad)
 for bad in mutation_cases:
  try:audit(bad)
  except AssertionError:pass
  else:raise AssertionError('Printed math/identity/designation fault was accepted')
 try:g.validate_bank([('correct',g.primitive(1,3,with_c=True)),('wrong',g.primitive(1,3))])
 except ValueError:pass
 else:raise AssertionError('Equivalent complete bank must reject the whole instance')
 assert g.generate_easy(template='power',parameters={'p':1,'d':3},profile='default')['question'][':question/id']==a['question'][':question/id']
 # All normal records have actual native-grader checks; raw malformed records do not.
 engine=[]
 for label,r in [(f'complete-{i}',r) for i,r in enumerate(normal)]+[(f'domain-{i}',r) for i,r in enumerate(all_records)]:
  item=grading_item(label,r)
  if item:engine.append(item)
 # Original native fragment layouts retain wording unchanged in raw evidence.
 for i,r in enumerate(raws):
  item=grading_item(f'raw-present-{i}',r)
  if item:engine.append(item)
 write('engine-input.json',engine)
 run=subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-validation.json')],capture_output=True,text=True)
 assert run.returncode==0,run.stdout+run.stderr
 print(run.stdout.strip())
 engine_report=json.loads((ROOT/'engine-validation.json').read_text())
 write('source-cases.json',cases);write('source-fidelity.json',fidelity)
 write('displayed-math-audit.json',[{'question_id':r['question'][':question/id'],'template':r['generation']['template'],'level':r['generation']['level'],'actual_printed_integrand':audit(r),'stages':solution_audit(r['question'],task(r['question'])) if ':question/worked-solution' in r['question'] else None} for r in raws+normal+all_records])
 review={'originals':raws,'completed_original_parameters':normal,'generated_variants':variants}
 write('review.json',review)
 parts=['# Review: radical antiderivative generators','Basis 1356; original evidence retains missing attributes. Correct labels below are absent where the source has no key. Completed records are explicitly authored/inferred. All normal records use x>0 and fragments exclude additive constants.']
 for sid,r,completed,variant in zip(g.SOURCE_SPEC,raws,normal,variants[:8]):
  parts += ['## '+sid+' — original evidence',g.markdown(r),'### Completed at original parameters',g.markdown(completed),'### Generated changed-parameter variant',g.markdown(variant)]
 for r in variants[8:]:parts+=['## Generated level/template example',g.markdown(r)]
 (ROOT/'review.md').write_text('\n\n'.join(parts)+'\n')
 meaningful={level:len({r['generation']['mathematical_fingerprint'] for r in all_records if r['generation']['level']==level}) for level in g.TEMPLATES}
 result={'status':'pass','database':'math','basis':1356,'database_writes':0,'source_questions':8,'rated_easy':4,'rated_hard':2,'unrated':2,'source_fidelity':{'prompts_exact':'8/8','whole_solutions_exact':'6/6 present','complete_banks_exact':'4/4 present','all_displayed_answers_exact':'12/12','correct_designations_exact':'2/2 present','missing_correct_designations':2,'missing_fields':4,'missing_solutions':2,'attribute_presence':'8/8'},'source_completion':{'inferred_radio_keys':2,'authored_fields':4,'authored_solutions':2,'opaque_banks':1,'opaque_learning_eligibility':False},'authored_extensions':['moderate root indices 2–4 with nonunit powers','moderate/hard proper and improper peers: p<=20, p+d<=24, p/d<=5; root indices 2–4 / 5–8','normal power-radio full operation bank','positive-domain and constant-free-fragment presentation'],'finite_domain_sizes':{'easy_power':len(g.POWER_DOMAIN),'easy_unit_root':len(g.UNIT_DOMAIN),'moderate':len(g.MODERATE_DOMAIN),'hard':len(g.HARD_DOMAIN)},'root_workload_bounds':{'numerator_max':20,'successor_numerator_max':24,'exponent_max':5,'moderate_root_indices':[2,3,4],'hard_root_indices':[5,6,7,8]},'proper_improper_peer_counts':{level:{'proper':sum(p<d for p,d in pairs),'improper':sum(p>d for p,d in pairs)} for level,pairs in [('moderate',g.MODERATE_DOMAIN),('hard',g.HARD_DOMAIN)]},'eligible_generated_enumeration':display_count,'eligible_meaningful_tasks_by_level':meaningful,'deliberate_printed_fault_rejections':len(mutation_cases),'whole_bank_collision_rejections':1,'seed_samples':len(samples),'guard_rejections':len(invalid)+1,'review_generated_variants':len(variants),'independent_displayed_math':'all prompt integrands, complete option families, prose conversion/n, 3/4 integral stages and 5 derivative stages','native_grading':{k:engine_report[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'native_binary_sha256':hashlib.sha256((REPO/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'unresolved_source_interpretation':'q-29635 four unrelated choice operations remain opaque, exact raw/complete evidence only; normal defaults use a separate actual-operation bank'}
 write('validation.json',result)
 print(json.dumps(result,indent=2))
 hashes={str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT.with_suffix('.py'),*sorted(ROOT.glob('*'))] if p.is_file() and p.name!='frozen-hashes.json'}
 write('frozen-hashes.json',hashes)
if __name__=='__main__':main()
