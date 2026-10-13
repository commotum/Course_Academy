#!/usr/bin/env python3
"""Fail closed: inspect actual rendered mathematics/prose, source banks, grading.
Independent differentiation starts from actual prompt f and r, not parameters.
Every formal operator argument, all three coordinates (including zero), every
composed/derivative vector, dot tuple and distributed/reduced row are read back.
"""
import copy,importlib.util,json,re,subprocess,hashlib,itertools
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parent; REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('g',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def balanced(s):
 assert s.count('$')%2==0,'unbalanced math delimiter'
 depth=0
 for i,ch in enumerate(s):
  if ch=='{' and (i==0 or s[i-1]!='\\'):depth+=1
  elif ch=='}' and (i==0 or s[i-1]!='\\'):depth-=1
  assert depth>=0,'closing TeX brace'
 assert depth==0,'opening TeX brace'
 assert '+-' not in s and '--' not in s,'ungrouped signed math'

def group(text,start):
 assert text[start] in '(['
 opening=text[start];closing={'(':')','[':']'}[opening];depth=0
 for end in range(start,len(text)):
  if text[end]==opening:depth+=1
  if text[end]==closing:
   depth-=1
   if depth==0:return text[start+1:end],end+1
 raise AssertionError('unbalanced operator group')

def vec(raw):return tuple(g.read_scalar(v) for v in g.vector_parts(raw))
def same_vec(actual,expected):
 assert len(actual)==len(expected)==3
 assert all(g.equal(a,b) for a,b in zip(actual,expected)),(actual,expected)

def rendered_check(rec):
 assert set(rec['knowledge_point'])=={'db_id','id','title'}
 assert rec['generation']['evidence_only']==rec['generation']['profile'].startswith('observed')
 assert rec['generation']['eligible_for_learning']!=rec['generation']['evidence_only']
 q=rec['question'];p=q[':question/problem'];solution=q.get(':question/worked-solution')
 for s in [p]+([solution] if solution is not None else []):balanced(s)
 fr,rr=g.prompt_parts(q);f=g.read_scalar(fr);r=vec(rr)
 grad=tuple(sp.diff(f,v) for v in g.VARS)
 gr=tuple(sp.expand_mul(v.subs(dict(zip(g.VARS,r)),simultaneous=True)) for v in grad)
 rd=tuple(sp.diff(v,g.T) for v in r);ans=sp.factor_terms(sp.expand(sum(a*b for a,b in zip(gr,rd))))
 if solution is not None:
  blocks=re.findall(r'\$\$\n(.*?)\n\$\$',solution,re.S);assert len(blocks)==5
  assert blocks[0]==r'\frac{\text{d}}{\text{d}t}[f(r(t))]=∇f(r(t))\cdot {r}^{′}(t).'
  allrows=[]
  for b in blocks[1:]:
   assert b.startswith(r'\begin{aligned}') and b.endswith(r'\end{aligned}')
   body=b[len(r'\begin{aligned}'):-len(r'\end{aligned}')]
   lhs,rhs=body.split(' & =',1);rows=rhs.split(r' \\  & =');allrows.append((lhs,rows))
  assert [l for l,rows in allrows]==['∇f(x,y,z)','∇f(r(t))',r'{r}^{′}(t)',r'\frac{\text{d}}{\text{d}t}[f(r(t))]']
  formal=allrows[0][1][0]
  assert formal.count(r'\frac{∂}{∂')==3
  for v in g.VARS:
   op=r'\frac{∂}{∂'+str(v)+'}';i=formal.index(op)+len(op);arg,end=group(formal,i)
   assert g.equal(g.read_scalar(arg),f),'wrong formal held-coordinate argument'
  for row in allrows[0][1][1:]:same_vec(vec(row),grad)
  for row in allrows[1][1]:same_vec(vec(row),gr)
  formal=allrows[2][1][0];op=r'\frac{\text{d}}{\text{d}t}'
  assert formal.count(op)==3
  pos=0
  for coordinate in r:
   i=formal.index(op,pos)+len(op);arg,pos=group(formal,i)
   assert g.equal(g.read_scalar(arg),coordinate),'wrong coordinate derivative argument'
  for row in allrows[2][1][1:]:same_vec(vec(row),rd)
  rows=allrows[3][1];assert rows[0]==r'∇f(r(t))\cdot {r}^{′}(t)'
  left,end=group(rows[1],0);assert rows[1][end:].startswith(r'\cdot (')
  right,pos=group(rows[1],end+len(r'\cdot '));assert pos==len(rows[1])
  same_vec(vec(left),gr);same_vec(vec(right),rd)
  assert len(rows)>=4
  for row in rows[2:]:assert g.equal(g.read_scalar(row),ans),('scalar displayed row',row,ans)
  # Prose substitution coordinates are read independently; r(t) in the target
  # gradient label is deliberately not translated.
  prose=next(p for p in solution.split('\n\n') if p.startswith('Next, we substitute'))
  before=prose.split(' into the above',1)[0]
  inline=''.join(re.findall(r'\$(.*?)\$',before)).replace(' and ','').replace(' ','')
  coordinates=re.findall(r'([xyz])=(.*?)(?=,[xyz]=|[xyz]=|$)',inline)
  assert len(coordinates)==3,(prose,coordinates)
  for (v,raw),expected in zip(coordinates,r):assert g.equal(g.read_scalar(raw.rstrip(',')),expected),('prose',v,raw,expected)
 field=q[':question/answer-fields'][0]
 assert field[':answer-field/type']==':answer-field.type/radio'
 assert len(field[':answer-field/choices'])==5
 values=[a[':answer/value'] for a in field[':answer-field/choices']]
 for v in values:balanced(v);assert '$' not in v
 expressions=[g.read_scalar(v) for v in values]
 for i,a in enumerate(expressions):
  assert all(not g.equal(a,b) for b in expressions[i+1:]),'equivalent answers'
 flags=[g.equal(e,ans) for e in expressions];assert sum(flags)==1
 correct=field[':answer-field/choices'][flags.index(True)]
 if ':answer-field/correct' in field:assert field[':answer-field/correct']==[':answer/id',correct[':answer/id']]
 else:assert rec['generation']['profile']=='observed_raw' and rec['generation']['template'] in ('pair_products','trig_product')
 digest=g.identity(p,solution,values,correct[':answer/value'] if ':answer-field/correct' in field else None,rec['generation']['domain'],q.get(':question/difficulty'));assert rec['generation']['content_fingerprint']==digest
 assert q[':question/id']==g.uid('question:'+digest)
 # Semantic identity from actual complete assessed objects, excluding profile.
 task=hashlib.sha256(json.dumps([sp.srepr(sp.expand(f)),[sp.srepr(v) for v in r],rec['generation']['domain']],sort_keys=True).encode()).hexdigest()
 assert task==rec['generation']['mathematical_fingerprint']
 return ans

def run():
 # Independent display criteria distinguish visible function powers from
 # inner argument powers; these are not metadata-derived expectations.
 for raw,expected in [
  (r'\sin{t}^{2}',sp.sin(g.T**2)),
  (r'\sin((t-2)^{2})',sp.sin((g.T-2)**2)),
  (r'\sin{(t-2)}^{2}',sp.sin(g.T-2)**2),
  (r'\sin(t-2)^2',sp.sin(g.T-2)**2),
  (r'\sin^{2}(t-2)',sp.sin(g.T-2)**2),
  (r'{sin}^{3}⁡(t-2)',sp.sin(g.T-2)**3),
 ]:assert g.equal(g.read_scalar(raw),expected),(raw,expected)
 argument_power_checks=6
 cases=[];reviews=[];grading=[];fidelity=[]
 def grade_record(rec,label):
  field=rec['question'][':question/answer-fields'][0]
  if ':answer-field/correct' not in field:return
  correct=field[':answer-field/correct'][1]
  grading.append({'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'complete radio bank native selection'} for a in field[':answer-field/choices']]})
 for name,q in g.QBY.items():
  print('Replay and rendered source-pattern variants:',name,flush=True)
  level='hard' if name=='exponential_cosine' else 'moderate';params={'c':1,'h':0}
  case={'source_id':q[':db/id'],'template':name,'level':level,'parameters':params,'bank_profile':'observed_raw'};cases.append(case)
  r=g.generate(level,template=name,parameters=params,profile='observed_raw');rendered_check(r)
  assert r['question'][':question/problem']==q[':question/problem']
  sourcefield=q[':question/answer-fields'][0];field=r['question'][':question/answer-fields'][0]
  assert sorted(a[':answer/value'] for a in field[':answer-field/choices'])==sorted(a[':answer/value'] for a in sourcefield[':answer-field/choices'])
  if ':question/worked-solution' in q:assert r['question'][':question/worked-solution']==q[':question/worked-solution']
  for attr in (':question/worked-solution',':question/difficulty'):assert (attr in r['question'])==(attr in q)
  assert (':answer-field/correct' in field)==(':answer-field/correct' in sourcefield)
  if ':answer-field/correct' in sourcefield:
   correct=next(a for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1])[':answer/value']
   assert correct==sourcefield[':answer-field/correct'][':answer/value']
  else:
   completion=g.generate(level,template=name,parameters=params,profile='observed_pattern');rendered_check(completion);grade_record(completion,'authored source completion '+name);reviews.append({'label':'Authored missing-attribute completion '+name,'record':completion})
  fidelity.append({'source_id':q[':db/id'],'prompt_exact':True,'answers_exact':5,'correct_designation_matched':':answer-field/correct' in sourcefield,'solution_exact':':question/worked-solution' in q,'source_missing_fields':[k for k in (':question/worked-solution',':question/difficulty') if k not in q]+([':answer-field/correct'] if ':answer-field/correct' not in sourcefield else [])})
  grade_record(r,'source '+name);reviews.append({'label':'Original replay '+name,'record':r})
  for index,p in enumerate([{'c':-2,'h':1},{'c':2,'h':-1}]):
   generated=g.generate(level,template=name,parameters=p,profile='observed_pattern');rendered_check(generated);grade_record(generated,'observed-pattern variant '+name+str(index));reviews.append({'label':'Generated observed-pattern variant '+name+' '+str(index),'record':generated})
 # Default operation profiles, every family; two authored examples per level.
 for level,names in g.LEVELS.items():
  for name in names:
   print('Default authored bank:',level,name,flush=True)
   for seed in [19,44]:
    r=g.generate(level,seed,template=name);rendered_check(r);grade_record(r,'authored/default '+level+' '+name+' '+str(seed));reviews.append({'label':'Generated default '+level+' '+name+' '+str(seed),'record':r})
 # All relevant operation profiles across signed boundary cases: valid complete
 # banks pass, collisions explicitly reject. Never silently drop a choice.
 boundary_pass=boundary_reject=0
 for name in g.BASE:
  print('Signed boundary checks:',name,flush=True)
  level='hard' if name in g.LEVELS['hard'] else 'moderate';maxc=4 if level=='hard' else 3
  for c,h in [(-maxc,-2),(-1,0),(1,0),(maxc,2)]:
   for profile in [None,'sign_chain']:
    try:r=g.generate(level,template=name,parameters={'c':c,'h':h},profile=profile)
    except ValueError as e:
     assert 'equivalent options' in str(e) or 'ineligible' in str(e);boundary_reject+=1;continue
    rendered_check(r);boundary_pass+=1
 for n in [1,2]:
  for a,b,d in itertools.product([-3,3],repeat=3):
   try:r=g.generate('easy',template='affine_polynomial',parameters={'a':a,'b':b,'d':d,'n':n})
   except ValueError as e:assert 'equivalent options' in str(e) or 'ineligible' in str(e);boundary_reject+=1;continue
   rendered_check(r);boundary_pass+=1
 # Invalid explicit bounds remain errors even under observed replay/profile.
 for level,name,params in [('easy','affine_polynomial',{'a':4,'b':1,'d':1,'n':1}),('easy','affine_polynomial',{'a':0,'b':1,'d':1,'n':2}),('moderate','log_product',{'c':-4,'h':0}),('hard','exponential_cosine',{'c':5,'h':0}),('hard','canonical_log',{'c':1,'h':3})]:
  try:g.generate(level,template=name,parameters=params)
  except ValueError:pass
  else:raise AssertionError('explicit bounds bypass')
 # Seed/order cannot alter content. Profile aliases with identical bank must
 # also preserve identity; changing actual bank must change presentation UUID.
 for level,names in g.LEVELS.items():
  for name in names:
   base=g.generate(level,19,template=name);p=base['generation']['parameters'];a=g.generate(level,31,template=name,parameters=p);b=g.generate(level,93,template=name,parameters=p)
   assert a['question'][':question/id']==b['question'][':question/id']
   if name in g.QBY:
    a=g.generate(level,1,template=name,parameters=p,profile='observed_raw');b=g.generate(level,2,template=name,parameters=p,profile='observed_pattern')
    assert (a['question'][':question/id']==b['question'][':question/id']) == (name not in ('pair_products','trig_product'))
    assert a['generation']['mathematical_fingerprint']==base['generation']['mathematical_fingerprint']
    assert a['question'][':question/id']!=base['question'][':question/id']
 # Intentional mutation tests establish that displayed checks catch errors,
 # including formal arguments, zero coordinate derivative and prose slots.
 rec=g.generate('moderate',template='constant_coordinate',parameters={'c':2,'h':1})
 probes=[('∂x}(2','∂x}(3'),(r'\text{d}t}(1)',r'\text{d}t}(2)'),('x={(t + 1)}','x={(t + 2)}')]
 mutation_count=0
 for old,new in probes:
  altered=copy.deepcopy(rec);s=altered['question'][':question/worked-solution'];assert old in s,(old,s)
  altered['question'][':question/worked-solution']=s.replace(old,new,1)
  try:rendered_check(altered)
  except AssertionError:mutation_count+=1
  else:raise AssertionError('display corruption undetected')
 # Positive/negative translations must keep every sin/cos inner t²
 # argument visible inside its enclosing function argument. Confirm both
 # observed expression-pattern choices and default operation banks.
 for h in (-2,-1,1,2):
  for profile in ('observed_raw','observed_pattern','paired_exp'):
   shifted=g.generate('hard',template='exponential_cosine',parameters={'c':-3,'h':h},profile=profile)
   rendered_check(shifted)
   text=shifted['question'][':question/worked-solution']+' '.join(a[':answer/value'] for a in shifted['question'][':question/answer-fields'][0][':answer-field/choices'])
   assert not re.search(r'\\operatorname\{(?:sin|cos)\}⁡\{\(t[ +\-0-9]*\)\}\^',text),'ambiguous shifted argument power'
   argument_power_checks+=1
 # Reintroduce the former ambiguous source-mask spelling. It now parses as
 # a function power and fails the composed-gradient row before identity QA.
 shifted=g.generate('hard',template='exponential_cosine',parameters={'c':-3,'h':-2},profile='observed_pattern')
 bad=copy.deepcopy(shifted)
 old=r'\operatorname{sin}⁡({(t - 2)}^{2})'
 wrong=r'\operatorname{sin}⁡{(t - 2)}^{2}'
 assert old in bad['question'][':question/worked-solution']
 bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(old,wrong,1)
 try:rendered_check(bad)
 except AssertionError as exc:
  assert isinstance(exc.args[0],tuple),'argument-power corruption must fail mathematical vector check'
  mutation_count+=1
 else:raise AssertionError('shifted argument power corruption undetected')
 (ROOT/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(ROOT/'review.json').write_text(json.dumps(reviews,indent=2,ensure_ascii=False)+'\n')
 md='# KP 17592186124470 review\n\nOriginal captured records are in source.json. Raw replay preserves original attribute absences; separately labeled records provide authored completions.\n\n'
 for item in reviews:md+='## '+item['label']+'\n\n'+g.markdown(item['record'])+'\n\n'
 (ROOT/'review.md').write_text(md)
 (ROOT/'engine-input.json').write_text(json.dumps(grading,indent=2,ensure_ascii=False)+'\n')
 subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-validation.json')],check=True)
 report={'status':'pass','frozen_version':g.VERSION,'database_writes':0,'source_provenance':{k:g.SOURCE[k] for k in ['database','basis','lineage']},'source_questions':8,'prompt_exact':8,'complete_banks_exact':8,'answer_values_exact':40,'distractors_exact':32,'correct_designations_matched':6,'correct_designations_present':6,'correct_designations_authored_completions':2,'worked_solutions_exact':6,'worked_solutions_present':6,'worked_solutions_authored_completions':2,'authored_level_assignments':2,'presentation_repairs':0,'mathematical_repairs':0,'source_fidelity':fidelity,'review_records':len(reviews),'boundary_valid_banks':boundary_pass,'boundary_whole_bank_rejections':boundary_reject,'mutation_checks':mutation_count,'trig_argument_power_checks':argument_power_checks,'native_grading':'engine-validation.json','formatting':'balanced delimiters and groups; all displayed math read back','scope':'symbolic full derivative, exactly three coordinates; no point evaluation or rate context'}
 (ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':run()
