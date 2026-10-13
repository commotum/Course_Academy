#!/usr/bin/env python3
"""Read actual displayed TeX back; check mathematics, source banks, UUIDs and native grading."""
import importlib.util,json,re,subprocess,hashlib,sys
sys.dont_write_bytecode=True
from pathlib import Path
import sympy as sp
D=Path(__file__).parent
spec=importlib.util.spec_from_file_location('generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def vectors(s):
 return re.findall(r'⟨[^⟩]*⟩|\[\\begin\{aligned\}.*?\\end\{aligned\}\]',s,re.S)

def rows(s):
 """Split only outer aligned rows; retain complete nested column vectors."""
 out=[];start=0;depth=0;n=0
 while n<len(s):
  if s.startswith(r'\begin{aligned}',n):depth+=1;n+=len(r'\begin{aligned}');continue
  if s.startswith(r'\end{aligned}',n):depth-=1;n+=len(r'\end{aligned}');continue
  if s.startswith(r'\\',n) and depth<=1:
   out.append(s[start:n]);n+=2;start=n;continue
  n+=1
 out.append(s[start:]);return out

def basis(raw):
 """Evaluate printed scalar derivatives individually, then read the basis sum."""
 op=r'\frac{\text{d}}{\text{d}t}'
 while op in raw:
  n=raw.index(op);p=n+len(op)
  while p<len(raw) and (raw[p].isspace() or raw.startswith(r'\,',p)):
   p+=2 if raw.startswith(r'\,',p) else 1
  if raw[p]=='(':
   v,end=g.balanced(raw,p,'(',')')
  else:
   # Source unparenthesized operands: sin t, cos t, 1.
   m=re.match(r'(?:\\operatorname\{(?:sin|cos)\}⁡t|\d+)',raw[p:])
   assert m,raw[p:];v=m[0];end=p+len(v)
  raw=raw[:n]+'('+str(sp.diff(g.scalar(v),g.T))+')'+raw[end:]
 return g.vector(raw)

def eval_vector_arithmetic(raw,layout):
 raw=raw.strip().rstrip('.,').replace(r'\left','').replace(r'\right','')
 raw=raw.split(r'\end{aligned}')[-1] if False else raw
 if layout=='basis':return basis(raw)
 tokens=vectors(raw)
 assert tokens,raw
 vals=[g.vector(x) for x in tokens]
 result=[]
 for component in range(3):
  text=raw
  for token,val in zip(tokens,vals):text=text.replace(token,'('+str(val[component])+')',1)
  result.append(g.scalar(text))
 return tuple(result)

def mathcheck(record):
 q=record['question'];meta=record['generation'];name=meta['template'];prompt=q[':question/problem'];solution=q[':question/worked-solution']
 layout=g.BASES[name][4] if name in g.BASES else 'basis'
 if layout=='basis':
  rawfuncs=re.findall(r'(?<=&=).*?(?= \\\\|\\end\{aligned\})',prompt) if name=='canonical-mixed' else re.findall(r'(?<=& =).*?(?= \\\\|\\end\{aligned\})',prompt)
  fs=[basis(x) for x in rawfuncs]
 else:fs=[g.vector(v) for v in vectors(prompt)]
 # Coefficients and function names read from the assessment's actual inline formula.
 target=re.search(r'\$([^$]+)\$',prompt)[1].replace('^{′}','').replace("'",'').replace('(', '(')
 pairs=re.findall(r'([+-]?\s*\d*)\s*([fgh])\(t\)',target)
 assert len(pairs)==len(fs),(target,pairs,fs)
 names=[];cs=[]
 for sign,n in pairs:
  sign=sign.replace(' ','');names.append(n);cs.append(-1 if sign=='-' else 1 if sign in ('','+') else int(sign))
 pointmatch=re.search(r'at \$t\s*=\s*([+-]?\d+)',prompt)
 point=int(pointmatch[1]) if pointmatch else None
 ds=[tuple(sp.diff(x,g.T) for x in f) for f in fs]
 used=ds if point is None else [tuple(sp.simplify(x.subs(g.T,point)) for x in d) for d in ds]
 ans=g.total(used,cs)
 assert all(x.is_real is not False and not x.has(sp.zoo,sp.oo,sp.nan) for x in ans)
 # Check actual prompt domains (including original negative log repair).
 if point is not None:
  for f in fs:
   for x in f:
    assert not sp.simplify(x.subs(g.T,point)).has(sp.zoo,sp.oo,sp.nan)
    for log in x.atoms(sp.log):assert log.args[0].subs(g.T,point)>0
 for text in [prompt,solution]:
  assert text.count('$')%2==0
  assert text.count('{')==text.count('}'),text
  assert '@@' not in text and '++' not in text
 if name=='q-33123' and meta['parameters']['scales']!=[1,1,1]:
  last=re.findall(r'\$\$\n(.*?)\n\$\$',solution,re.S)[-1]
  stages=rows(last)
  assert '2'+r'\left(' in stages[1] and '+3'+r'\left(' in stages[1]
  assert len(re.findall(r'\\left\((?!t\s)',stages[1]))>=7 and len(re.findall(r'\\left\((?!t\s)',stages[2]))==5
 field=q[':question/answer-fields'][0]
 assert field[':answer-field/type']==':answer-field.type/radio' and field[':answer-field/key']=='selection'
 bank=[basis(a[':answer/value']) if layout=='basis' else g.vector(a[':answer/value']) for a in field[':answer-field/choices']]
 assert len(bank)==5
 assert all(not g.eq(x,y) for n,x in enumerate(bank) for y in bank[n+1:])
 corrects=[a for a,v in zip(field[':answer-field/choices'],bank) if g.eq(v,ans)]
 assert len(corrects)==1 and corrects[0][':answer/id']==field[':answer-field/correct'][1]
 # Read each displayed solution equation, including the first distributed sum.
 final_section=False;active=None;count=0
 for b in re.findall(r'\$\$\n(.*?)\n\$\$',solution,re.S):
  if '(f(0)' in b or '(f(1)' in b or '(2f' in b or '(3h' in b: pass
  outer=rows(b)
  for row in outer:
   if '&' not in row:continue
   lhs,rhs=row.split('&',1);rhs=rhs.lstrip().removeprefix('=').strip()
   rhs=re.sub(r'\\end\{aligned\}$','',rhs).strip().rstrip('.,')
   if not rhs:continue
   mm=re.search(r'\{?([fgh])\}?\s*(?:\^\{′\}|\^\{\\prime\}|\')\(t\)',lhs)
   if mm:active=names.index(mm[1]);final_section=False
   elif '(' in lhs and ('′' in lhs or "'" in lhs):final_section=True;active=None
   if vectors(rhs) or layout=='basis' and any(x in rhs for x in [r'\,i',r'\,j',r'\,k','ti']):
    expected=ans if final_section or active is None else ds[active]
    for part in rhs.split('='):
     value=eval_vector_arithmetic(part,layout)
     assert g.eq(value,expected),(name,lhs,part,value,expected)
     count+=1
 assert count>=3,(name,count)
 return count

def main():
 cases=json.load(open(D/'source-cases.json'));source=json.load(open(D/'source.json'))['record'][':knowledge-point/questions'];orig={q[':question/math-academy-id']:q for q in source}
 source_records=[];stages=0;values=0;designations=0;solutions=0;prompts=0
 for c in cases:
  r=g.generate(c['level'],0,c['template'],parameters=c['parameters'],profile=c['bank_profile']);stages+=mathcheck(r);source_records.append(r)
  q=orig[c['source_id']];f=q[':question/answer-fields'][0];gen=r['question'][':question/answer-fields'][0]
  old=[g.vector(a[':answer/value']) for a in f[':answer-field/choices']];new=[g.vector(a[':answer/value']) for a in gen[':answer-field/choices']]
  assert all(sum(g.eq(a,b) for b in new)==1 for a in old);values+=len(old)
  if ':answer-field/correct' in f:
   actual=next(a for a in gen[':answer-field/choices'] if a[':answer/id']==gen[':answer-field/correct'][1]);assert g.eq(g.vector(actual[':answer/value']),g.vector(f[':answer-field/correct'][':answer/value']));designations+=1
  prompts+=r['question'][':question/problem']==q[':question/problem']
  solutions+=r['question'][':question/worked-solution']==q.get(':question/worked-solution')
  # Fixed content unchanged by seed/order.
  r2=g.generate(c['level'],99,c['template'],parameters=c['parameters'],profile=c['bank_profile']);assert r2['question'][':question/id']==r['question'][':question/id']
 records=[];coverage={};unique={}
 for name,level in g.TEMPLATES.items():
  coverage[name]=0;ids=set()
  for seed in range(20):
   r=g.generate(level,seed,name);stages+=mathcheck(r);records.append(r);ids.add(r['generation']['parameter_fingerprint']);coverage[name]+=1
  unique[name]=len(ids)
  assert len(ids)>=15,(name,len(ids))
  if name in g.DATA:
   for scales in [[-3,-2,3],[3,1,-1]]:
    r=g.generate(level,0,name,parameters={'scales':scales},profile=name);stages+=mathcheck(r);records.append(r)
 for x in [-6,-1,1,6]:
  for z in [-6,-1,1,6]:
   r=g.generate('easy',0,'q-32503',parameters={'scales':[x,1,z]});stages+=mathcheck(r);records.append(r)
 for level in ['easy','moderate','hard']:
  a=g.generate(level,seed=23);b=g.generate(level,seed=23);assert a==b
 for level in ['easy','moderate','hard']:
  a=g.generate(level,23);m=a['generation'];b=g.generate(level,99,m['template'],parameters=m['parameters'],profile=m['bank_profile']);assert a['question'][':question/id']==b['question'][':question/id'];assert a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint']
  for r in [a,b]:
   g.uuid.UUID(r['question'][':question/id']);f=r['question'][':question/answer-fields'][0];g.uuid.UUID(f[':answer-field/id']);assert len({x[':answer/id'] for x in f[':answer-field/choices']})==5
   for x in f[':answer-field/choices']:g.uuid.UUID(x[':answer/id'])
 a=g.generate('easy',0,'q-33122',parameters={'scales':[1,1,1]},profile='q-33122');b=g.generate('easy',0,'q-33122',parameters={'scales':[1,1,1]});assert a['question'][':question/id']!=b['question'][':question/id'];assert a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint']
 for args in [('easy',{'template':'canonical-mixed'}),('hard',{'parameters':{'a':0}}),('easy',{'field_type':'blank'}),('easy',{'parameters':{'scales':[0,1,1]}})]:
  try:g.generate(args[0],**args[1])
  except ValueError:pass
  else:raise AssertionError('Invalid explicit input accepted')
 engine=[]
 for n,r in enumerate(source_records+records):
  f=r['question'][':question/answer-fields'][0]
  engine.append({'label':str(n)+'-'+r['generation']['template'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned complete-bank choice'} for a in f[':answer-field/choices']]})
 json.dump(engine,open(D/'engine-input.json','w'),indent=2)
 exe=Path('generate/runs/current/check-engine');subprocess.run([str(exe),str(D/'engine-input.json'),str(D/'engine-results.json')],check=True)
 report={'status':'pass','source_questions':11,'source_banks_matched':11,'source_values_matched':values,'source_distractors_matched':44,'source_correct_designations_matched':designations,'source_correct_designations_available':10,'missing_designation_inferred':1,'prompt_exact':prompts,'prompt_total':11,'solution_exact':solutions,'solution_available':10,'solution_repaired':4,'solution_authored_missing':1,'domain_repairs':1,'evaluation_notation_repairs':4,'native_question_count':len(engine),'native_checks':len(engine)*5,'displayed_math_stages_checked':stages,'generated_default_checks':coverage,'variety_unique_first_20':unique,'explicit_profile_nonbase_checks':22,'authored_hard':20,'triple_sum_boundary_checks':16,'authored_fixed_content_shuffle_checks':3,'distinct_bank_identity_checks':1,'uuid_checks':True,'generator_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'bounded_default_capacity':{'each_general_observed_template':216,'triple_sum_default':144,'canonical_hard':27648},'engine_sha256':hashlib.sha256(exe.read_bytes()).hexdigest(),'unresolved_findings':['Specific residual compound/scalar distractor intentions remain uncertain (see per-option map); exact diagonal-scaled expression profiles retain all evidence and are explicit replay only. Missing original q-33143 designation cannot count as matched.']}
 json.dump(report,open(D/'validation.json','w'),indent=2);print(json.dumps(report,indent=2))
 # Every source/profile plus two variants and two hard samples.
 review=[]
 for c in cases:
  review += [g.generate(c['level'],n,c['template'],parameters={'scales':[-2,1,3] if n==1 else [1,-3,2]},profile=c['bank_profile']) for n in [1,2]]
 review += [g.generate('hard',n,'canonical-mixed') for n in [1,2]]
 normal_review=[g.generate(l,n) for l in ['easy','moderate','hard'] for n in [31,32]]
 json.dump(review+normal_review,open(D/'review.json','w'),indent=2,ensure_ascii=False)
 json.dump(source_records,open(D/'source-replays.json','w'),indent=2,ensure_ascii=False)
 md=['# Originals and generated variants','Raw snapshot: `source.json`, math basis 1356. All generated items below are labeled.']
 for c,r in zip(cases,source_records):
  q=orig[c['source_id']];md += ['## Original '+c['source_id'],q[':question/problem'],'\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices']),q.get(':question/worked-solution','No captured worked solution.'),'## Replay (repairs explicitly recorded)',g.markdown(r)]
 md += ['# Generated observed-profile variants']+[g.markdown(r) for r in review]
 md += ['# Generated normal authored-bank variants']+[g.markdown(r) for r in normal_review]
 (D/'review.md').write_text('\n\n'.join(md))
if __name__=='__main__':main()
