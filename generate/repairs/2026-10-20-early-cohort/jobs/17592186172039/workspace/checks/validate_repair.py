#!/usr/bin/env python3
"""Source replay, independent visible-record witnesses, counterfactuals and inventory audit.
No runtime files are modified. Shared delivery/grader/render commands are separate.
"""
import collections, importlib.util, itertools, json, os, pathlib, re, sys
sys.dont_write_bytecode = True
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'evidence';OUT.mkdir(exist_ok=True)
os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(OUT/'assets')
sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location('generator',ROOT/'17592186172039.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
SOURCE=json.loads((ROOT/'../source/source.json').read_text())
INVENTORY=json.loads((ROOT/'../source/inventory.json').read_text())
WORDS=('first','second','third','fourth');COORDS=((1,1),(-1,1),(-1,-1),(1,-1))

def save(name,data): (OUT/name).write_text(json.dumps(data,indent=2)+'\n')
def correct(f):
 ref=f[':answer-field/correct'];aid=ref.get(':answer/id') if isinstance(ref,dict) else ref[1]
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==aid)
def parse(q):
 rhs=q[':question/problem'].split('$')[1].split('=',1)[1].strip().replace('{','').replace('}','')
 m=re.fullmatch(r'(-?\d*)x(\^2)?(y(\^2)?)?',rhs);assert m, rhs
 c=int(m[1]) if m[1] not in ('','-') else (-1 if m[1]=='-' else 1)
 a=2 if m[2] else 1;b=0 if not m[3] else 2 if m[4] else 1
 return c,a,b

def inspect(r,solution=True):
 q=r.get('question',r);c,a,b=parse(q)
 # x=sx*u,y=sy*v with u,v>0: c*sx^a*sy^b*u^a*v^b has this global sign.
 ss=[(1 if c>0 else -1)*x**a*y**b for x,y in COORDS]
 fields=q[':question/answer-fields'];ordinary=[];answers=[]
 for f in fields:
  key=f[':answer-field/key']
  if key=='None of the above':continue
  m=re.fullmatch(r'At every point in the (first|second|third|fourth) quadrant, the slope of the slope field is (positive|negative)',key)
  assert m,('Missing visible statement label',key)
  qi=WORDS.index(m[1]);claim=1 if m[2]=='positive' else -1
  truth=ss[qi]==claim;ordinary.append((qi,claim));answers.append(truth)
  assert correct(f)==str(truth).lower(),(key,c,a,b,correct(f))
  assert len(f[':answer-field/choices'])==2
  assert {v[':answer/value'] for v in f[':answer-field/choices']}=={'false','true'}
  if solution and 'Statement “' in q[':question/worked-solution']:
   sol=q[':question/worked-solution'];start=sol.index('Statement “'+key+'” is ')
   block=sol[start:].split('\n\n- Statement')[0].split('\n\nTherefore')[0]
   assert block.startswith('Statement “'+key+'” is '+str(truth).lower()+'.')
   assert 'f(x,y)'+('>' if ss[qi]>0 else '<')+'0.' in block
   assert ('slope of the slope field is '+('positive' if ss[qi]>0 else 'negative')+' for any point $(x,y)$ in the '+WORDS[qi]+' quadrant.') in block
 if solution:
  sol=q[':question/worked-solution']
  if 'First, we define' in sol:
   expr=sol.split('$')[1].split('=',1)[1].rstrip('.')
   assert parse({':question/problem':'Equation $d='+expr+'$'})==(c,a,b)
   assert ('when $x=0$ or $y=0.$' in sol)==(b>0)
  else:
   assert a==1 and b==2
   assert ('the opposite sign to x' in sol)==(c<0)
   for sign,names in re.findall(r'(negative|positive) in quadrants? ([IV, and]+)',sol):
    for name in re.findall(r'\b(?:IV|III|II|I)\b',names):assert ss[('I','II','III','IV').index(name)]==(1 if sign=='positive' else -1)
  # Check the displayed diagram, using independently verified source sign maps or generated sidecars.
  paths=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',sol)
  for path in paths:
   if path in SOURCE_PLOTS:assert tuple(ss)==SOURCE_PLOTS[path]
   else:
    side=OUT/'assets'/pathlib.Path(path).with_suffix('.json');data=json.loads(side.read_text())['spec']
    assert data['signs']==ss
    assert data['zero_axes']==(['x'] if b==0 else ['x','y'])
 assert len(ordinary)==3 and len(set(q for q,_ in ordinary))==3
 none=[f for f in fields if f[':answer-field/key']=='None of the above']
 if none:assert len(none)==1 and correct(none[0])==str(not any(answers)).lower()
 assert any(answers) or none,'No correct selectable checkbox'
 return {'coefficient_sign':1 if c>0 else -1,'powers':(a,b),'statements':tuple(ordinary),'truths':tuple(answers),'mask':sum(1<<i for i,v in enumerate(answers) if v)}
SOURCE_PLOTS={
'images/6e/6ef852c9c15dc6f591119906abe479949f929edb6dc26f21588b4de545d02da2.png':(1,-1,1,-1),
'images/2c/2c218c7df2bf4e159b4bffaccb4296beab8e3f44ab82d56b3589050af92ccf8e.png':(-1,1,-1,1),
'images/d1/d1e4f48450a7f2032d755a5255d1a1e8a726dd16d273dae5dc1e587826d5ce58.png':(1,1,1,1),
'images/96/96c937cf10d45d8870a4a56e257d184dcf2e4caf11312c05df9f385f9c5ee7a8.png':(-1,1,1,-1)}

def semantic(r):
 d=inspect(r);return (d['coefficient_sign'],d['powers'],tuple(sorted(d['statements'])))
def bank(q):return sorted((f[':answer-field/key'],sorted(a[':answer/value'] for a in f[':answer-field/choices']),correct(f)) for f in q[':question/answer-fields'])
def native(r,label):
 return {'label':label,'record':r,'checks':[{'field_index':i,'submitted_answer_id':v[':answer/id'],'expected':'accepted' if v[':answer/value']==correct(f) else 'rejected','purpose':'independently checked visible quadrant sign claim (or its complement)'} for i,f in enumerate(r['question'][':question/answer-fields']) for v in f[':answer-field/choices']]}

def main():
 byid={q[':question/math-academy-id']:q for q in SOURCE['material']['kp'][':knowledge-point/questions']}
 cases=json.loads((ROOT/'17592186172039/source-cases.json').read_text());replays=[];records=[];graders=[];replay_records=[]
 for case in cases:
  old=byid[case['source_id']];has_none=any(f[':answer-field/key']=='None of the above' for f in old[':question/answer-fields'])
  r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'],include_none=has_none)
  inspect(r);q=r['question']
  assert q[':question/problem']==old[':question/problem'],case['source_id']
  assert bank(q)==bank(old),case['source_id']
  assert q[':question/worked-solution']==old[':question/worked-solution'],case['source_id']
  replays.append({'source_id':case['source_id'],'prompt_exact':True,'solution_exact':True,'fields':len(bank(q)),'bank_values':2*len(bank(q)),'source_difficulty':old.get(':question/difficulty')})
  replay_records.append({'source':old,'replay':r});graders.append(native(r,case['source_id']))
 # Each recognizable presentation gets all 8 truth assignments, with other data held fixed.
 # Include both exponent orientations and uniform-sign parity as independent hard families.
 configurations=[('easy','single_coordinate',1,0),('moderate','bilinear_open_thin',1,1),('moderate','bilinear_open',1,1),('moderate','bilinear_closed',1,1),('hard','parity_open',1,2),('hard','parity_closed',2,1),('hard','parity_closed',2,2),('hard','parity_numbered',1,2)]
 counter=[]
 for level,template,a,b in configurations:
  family=[]
  for mask in range(8):
   p={'c':7,'a':a,'b':b,'quadrants':[1,2,4],'claims':[]}
   p['claims']=[(COORDS[q-1][0]**a*COORDS[q-1][1]**b)*(1 if mask&(1<<i) else -1) for i,q in enumerate(p['quadrants'])]
   r=g.generate(level,template=template,parameters=p);d=inspect(r);assert d['mask']==mask
   records.append(r);family.append(r)
   flipped=g.generate(level,template=template,parameters=p|{'c':-7});df=inspect(flipped)
   assert df['truths']==tuple(not v for v in d['truths']);records.append(flipped)
   rescaled=g.generate(level,template=template,parameters=p|{'c':1});assert inspect(rescaled)['truths']==d['truths']
   counter.append({'template':template,'powers':[a,b],'mask':mask,'sign_flip_complements_all':True,'positive_rescaling_preserves_response':True,'base_id':r['question'][':question/id'],'flipped_id':flipped['question'][':question/id']})
  for i in range(3):
   assert inspect(family[0])['truths'][i]!=inspect(family[1<<i])['truths'][i]
 # Different eligible target, holding equation/claims/remaining targets fixed.
 base={'c':1,'a':1,'b':1,'quadrants':[1,2,3],'claims':[1,1,1]}
 ra=g.generate('moderate',parameters=base);rb=g.generate('moderate',parameters=base|{'quadrants':[4,2,3]})
 assert inspect(ra)['truths']==(True,False,True) and inspect(rb)['truths']==(False,False,True)
 records.extend([ra,rb]);counter.append({'changed_target':'first to fourth quadrant','only_first_truth_changed':True,'record_ids':[r['question'][':question/id'] for r in [ra,rb]]})
 # Quadrant omission sets and statement positions vary without new reasoning.
 for qs in [(1,2,3),(2,3,4),(3,4,1),(4,1,2)]:
  records.append(g.generate('moderate',parameters=base|{'quadrants':list(qs)}))
 # A small seeded sample checks the actual sampler, rather than only explicit fixtures.
 for level in ['easy','moderate','hard']:
  for seed in range(12):records.append(g.generate(level,seed=seed))
 for r in records:inspect(r)
 for p in [base|{'c':-9},base|{'c':9}]:inspect(g.generate('moderate',parameters=p))
 rejected=[]
 for delta in [{'c':0},{'c':10},{'a':3},{'quadrants':[1,1,2]},{'claims':[0,1,1]}]:
  try:g.generate('moderate',parameters=base|delta)
  except ValueError:rejected.append(delta)
  else:raise AssertionError(('Invalid instance accepted',delta))
 # Exact source field/solution comparison already independently checked original keys.
 # Stored records are not executable packages: packaging failure alone affects no stored math.
 inv=[]
 for q in INVENTORY['questions']:
  inv.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'visible_math_and_keys_checked':True,'mask':inspect(q,solution=False)['mask']})
 save('affected-inventory.json',{'affected_questions':[],'audit':{'tested':len(inv),'untested':0,'scope':'All captured printed equations, visible statement labels, boolean keys and nonempty selection. Runtime closure does not execute in stored question records. No stored grading/math failure demonstrated.','records':inv}})
 # Native inputs test actual acceptance AND rejection for each source and controlled pair.
 graders.extend(native(r,'controlled-'+str(i)) for i,r in enumerate(records[:128]))
 save('native-input.json',graders);save('source-replays.json',replay_records);save('records.json',records);save('counterfactuals.json',counter)
 save('validation.json',{'source_fidelity':replays,'source_bank_values_matched':sum(x['bank_values'] for x in replays),'record_count':len(records),'semantic_instances':len({semantic(r) for r in records}),'mathematics':'All global signs/checkbox keys and solution claims independently checked from visible expressions and labels, not metadata.','counterfactual_pairs':len(counter),'invalid_parameter_rejections':rejected,'inventory_checked':len(inv),'retained_finding_ids':[]})
 print(json.dumps({'source_replays':len(replays),'source_values':sum(x['bank_values'] for x in replays),'records':len(records),'semantic_instances':len({semantic(r) for r in records}),'inventory_checked':len(inv)}))
if __name__=='__main__':main()
