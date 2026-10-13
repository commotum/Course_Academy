#!/usr/bin/env python3
"""Independent displayed-token QA plus exact source-presence/bank fidelity and real grading."""
import importlib.util,json,re,subprocess,sys,itertools,hashlib,platform,copy,uuid
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('column_generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
MATRIX=re.compile(r'\\begin\{bmatrix\}(-?\d+) \\\\ (-?\d+)\\end\{bmatrix\}|\[\\begin\{aligned\}(-?\d+) \\\\ (-?\d+)\\end\{aligned\}\]')
def matrices(s):return [tuple(int(x) for x in m.groups() if x is not None) for m in MATRIX.finditer(s)]
def evaluate(s):
 vs=[]
 def mask(m):
  vs.append(tuple(int(x) for x in m.groups() if x is not None));return 'V'+str(len(vs)-1)
 s=MATRIX.sub(mask,s).replace(r'\cdot','*').strip().rstrip('\\').strip()
 ans=[]
 for j in range(2):
  e=re.sub(r'V(\d+)',lambda m:'('+str(vs[int(m[1])][j])+')',s)
  ans.append(int(sp.sympify(e)))
 return tuple(ans)
def read_prompt(q):
 p=q[':question/problem'];vs=matrices(p);ex=re.search(r'Find \$(.*?)\$',p)[1].rstrip('.')
 coeff=[]
 for j in range(2):
  e=ex
  for n,key in enumerate('abc'[:len(vs)]):
   e=re.sub(r'(?<=[\d)])'+key,'*'+key,e)
   e=re.sub(key,'('+str(vs[n][j])+')',e)
  coeff.append(int(sp.sympify(e)))
 return vs,ex,tuple(coeff)
def display_check(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];uuid.UUID(q[':question/id']);vs,ex,good=read_prompt(q)
 assert len(vs)==(2 if r['generation']['level']=='easy' else 3)
 sol=q.get(':question/worked-solution')
 if sol:
  assert sol.startswith(g.OPENING+'\n\n$$\n')
  head=sol.split('&')[0].split(r'\begin{aligned}',1)[1].strip()
  assert head==ex
  tail=re.split(r'&\s*=\s*',sol,maxsplit=1)[1]
  rows=re.split(r'\\\\\s*&\s*=\s*',tail)
  rows[-1]=rows[-1].rsplit(r'\end{aligned}',1)[0]
  rows=[s.strip().rstrip('\\').strip() for s in rows]
  assert len(rows)==(3 if len(vs)==2 else 4)
  for s in rows:assert evaluate(s)==good,(s,good,evaluate(s))
  assert matrices(rows[0])==vs # actual printed operands, not metadata
  # Derive scalar inputs and signs from actual prompt expression; check each
  # individually evaluated term and collected inner component, not equality alone.
  if len(vs)==3:
   match=re.fullmatch(r'(\(-?\d+\)|\d+)?a([+-])\((\(-?\d+\)|\d+)?b([+-])(\(-?\d+\)|\d+)?c\)',ex.replace(' ',''));assert match
   k,o,qc,i,rc=match.groups();ks=[int(x.strip('()')) if x else 1 for x in [k,qc,rc]];outer=1 if o=='+' else -1;inner=1 if i=='+' else -1
   terms=[tuple(n*v for v in vec) for n,vec in zip(ks,vs)]
   assert matrices(rows[1])==terms
   actual=dict(a=list(vs[0]),b=list(vs[1]),c=list(vs[2]),k=ks[0],q=ks[1],r=ks[2]);g.validate_parameters(r['generation']['level'],r['generation']['template'],actual,r['generation']['evidence_only'])
   collected=tuple(terms[1][j]+inner*terms[2][j] for j in range(2))
   assert matrices(rows[2])==[terms[0],collected]
  else:
   qc=int(re.search(r'([0-9]+)b',ex)[1]);g.validate_parameters('easy','two_vectors',dict(a=list(vs[0]),b=list(vs[1]),q=qc));assert matrices(rows[1])==[vs[0],tuple(qc*v for v in vs[1])]
  assert matrices(rows[-1])==[good]
 for text in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices']]:
  assert text.count('$')%2==0
  assert text.count('{')==text.count('}')
  assert '--' not in text and '+-' not in text
  assert not any(x in text for x in [r'\langle',r'\mathbf{i}',r'\mathbf{j}',r'\times'])
 for f in q.get(':question/answer-fields',[]):
  uuid.UUID(f[':answer-field/id']);assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
  assert len({a[':answer/id'] for a in f[':answer-field/choices']})==5
  for a in f[':answer-field/choices']:uuid.UUID(a[':answer/id']);assert a[':answer/type']==':answer.type/math'
  values=[matrices(a[':answer/value'])[0] for a in f[':answer-field/choices']];assert len(values)==5==len(set(values))
  if not r['generation']['evidence_only']:
   assert q[':question/difficulty']==':question.difficulty/'+r['generation']['level']
   def plus(x,y,sign=1):return tuple(x[j]+sign*y[j] for j in range(2))
   if len(vs)==2:
    qb=tuple(qc*v for v in vs[1]);expected=[good,plus(vs[0],qb,-1),plus(vs[0],vs[1]),plus(vs[0],(qb[0],vs[1][1])),plus(vs[0],(vs[1][0],qb[1]))]
   else:
    ka,qb,rc=terms
    omitted=plus(vs[0],collected,outer) if r['generation']['recipe_operations'][3]=='omit_left_scalar' else plus(ka,plus(vs[1],rc,inner),outer)
    expected=[good,plus(ka,collected,-outer),plus(ka,plus(qb,rc,-inner),outer),omitted,plus(ka,plus(qb,vs[2],inner),outer)]
   assert sorted(values)==sorted(expected),'Displayed distractor does not implement published operation'
  if ':answer-field/correct' in f:
   a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert matrices(a[':answer/value'])==[good]
 return good

def main():
 cases=json.loads((D/'source-cases.json').read_text());fidelity=[];review=[];inputs=[];normal_count=0;checks=0
 for c in cases:
  original=g.ORIGINALS[c['source_id']];r=g.generate('moderate',template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);q=r['question'];display_check(r)
  for key in [':question/difficulty',':question/worked-solution',':question/answer-fields']:
   assert (key in q)==(key in original)
  assert q[':question/problem']==original[':question/problem']
  if ':question/worked-solution' in original:assert q[':question/worked-solution']==original[':question/worked-solution']
  for f,of in zip(q.get(':question/answer-fields',[]),original.get(':question/answer-fields',[])):
   assert f[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert f[':answer-field/key']==of[':answer-field/key'];assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
   assert sorted((a[':answer/value'],a[':answer/type']) for a in f[':answer-field/choices'])==sorted((a[':answer/value'],a[':answer/type'][':db/ident']) for a in of[':answer-field/choices'])
  fidelity.append({'source_id':c['source_id'],'prompt_exact':True,'attribute_presence_exact':True,'solution_exact':':question/worked-solution' in original,'bank_exact':':question/answer-fields' in original,'correct_ref_match':'not present in source'})
  review.append({'label':'Raw original replay '+c['source_id'],'record':r})
  # Changed-parameter raw replay establishes recipes are parameterized; fieldless
  # originals remain fieldless. Opaque banks never count as recovered operations.
  p=dict(c['parameters']);p['a']=[p['a'][0]+1,p['a'][1]]
  changed=g.generate('moderate',template=c['template'],parameters=p,profile=c['bank_profile']);display_check(changed);review.append({'label':'Changed raw evidence '+c['source_id'],'record':changed})
  completed=g.generate('moderate',parameters=c['parameters'],profile='completed-'+c['source_id']);display_check(completed);review.append({'label':'Inferred completion '+c['source_id'],'record':completed})
  f=completed['question'][':question/answer-fields'][0];cs=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Independently inferred source completion choice'} for a in f[':answer-field/choices']];inputs.append({'label':'completed/'+c['source_id'],'record':completed,'checks':cs});checks+=len(cs)
 for level in ['easy','moderate','hard']:
  seen=set();fingerprints=set();positions=set()
  for seed in range(150):
   r=g.generate(level,seed);display_check(r);normal_count+=1;seen.add(r['generation']['template']);fingerprints.add(r['generation']['mathematical_fingerprint'])
   same=g.generate(level,seed+997,template=r['generation']['template'],parameters=r['generation']['parameters']);assert same['question'][':question/id']==r['question'][':question/id'];assert same['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
   f=r['question'][':question/answer-fields'][0];positions.add(next(n for n,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
   cs=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Owned radio choice '+str(n)} for n,a in enumerate(f[':answer-field/choices'])]
   checks+=len(cs);inputs.append({'label':level+'/'+str(seed),'record':r,'checks':cs})
   if seed<2:review.append({'label':'Generated '+level+' example '+str(seed+1),'record':r})
  assert seen==({'two_vectors'} if level=='easy' else set(list(g.TEMPLATES)[:4]));assert len(positions)==5;assert len(fingerprints)>=140
 # Two normal changed variants for every observed template, explicit source-mask
 # families are default sampled and all receive independent actual-token checks.
 for t in list(g.TEMPLATES)[:4]:
  for seed in [710,711]:
   r=g.generate('moderate',seed,template=t);display_check(r);review.append({'label':'Generated observed mask '+t+' variant '+str(seed),'record':r})
 # Strict explicit-input negative tests, including malformed inputs and each
 # easy/moderate/hard workload collapse. Each must be rejected, never resampled.
 invalid=0
 for level,t,p in [('easy','two_vectors',dict(a=[1,-2],b=[2,3],q=1)),('moderate','nested_minus_minus',dict(a=[1,-2],b=[2,3],c=[3,2],k=2,q=2,r=3)),('hard','nested_minus_minus',dict(a=[1,-2],b=[2,3],c=[3,2],k=1,q=-2,r=3)),('hard','nested_minus_minus',dict(a=[1,-2],b=[2,3],c=[3,2],k=2,q=2,r=3)),('easy','two_vectors',dict(a=[9,-2],b=[2,3],q=2)),('easy','two_vectors',dict(a=[1,2],b=[2,3],q=2)),('easy','two_vectors',dict(a=[1,-2],b=[0,0],q=2)),('easy','two_vectors',dict(a=[1,-2],b=[2,3],q=2,unused=1)),('easy','two_vectors',dict(a=[0,-8],b=[0,7],q=5))]:
  try:g.generate(level,template=t,parameters=p)
  except ValueError:invalid+=1
  else:raise AssertionError('Invalid explicit workload accepted')
 # Corruption controls prove the displayed-stage validator catches paired
 # scalar-product errors even when they cancel and preserve the final result.
 corruption_checks=0
 base=g.generate('moderate',parameters=g.SOURCE_PARAMETERS['q-70414'],template='nested_plus_minus')
 for row,delta in [(0,1),(1,1),(2,1),(3,1)]:
  broken=copy.deepcopy(base);sol=broken['question'][':question/worked-solution'];tail=re.split(r'&\s*=\s*',sol,maxsplit=1)[1];rows=re.split(r'\\\\\s*&\s*=\s*',tail)
  target=rows[row];m=MATRIX.search(target);assert m
  nums=[int(x) for x in m.groups() if x is not None];replacement=g.matrix([nums[0]+delta,nums[1]],'aligned')
  newtarget=target[:m.start()]+replacement+target[m.end():];broken['question'][':question/worked-solution']=sol.replace(target,newtarget,1)
  try:display_check(broken)
  except AssertionError:corruption_checks+=1
  else:raise AssertionError('Displayed corruption escaped validator')
 broken=copy.deepcopy(base);sol=broken['question'][':question/worked-solution'];tail=re.split(r'&\s*=\s*',sol,maxsplit=1)[1];rows=re.split(r'\\\\\s*&\s*=\s*',tail);target=rows[1];hits=list(MATRIX.finditer(target));changed=target
 for m in reversed(hits[1:]):
  nums=[int(x) for x in m.groups() if x is not None];changed=changed[:m.start()]+g.matrix([nums[0]+1,nums[1]],'aligned')+changed[m.end():]
 assert evaluate(target)==evaluate(changed) # pair cancels, but terms are wrong
 broken['question'][':question/worked-solution']=sol.replace(target,changed,1)
 try:display_check(broken)
 except AssertionError:corruption_checks+=1
 else:raise AssertionError('Paired scalar errors escaped validator')
 broken=copy.deepcopy(base);broken['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']=g.matrix([100,100])
 try:display_check(broken)
 except AssertionError:corruption_checks+=1
 else:raise AssertionError('Wrong displayed bank escaped validator')
 # Signed scalar spellings can represent one task; they share the canonical
 # fingerprint while retaining different actual prompts/content identities.
 p=dict(a=[1,-2],b=[2,3],c=[3,2],k=-2,q=2,r=-3)
 alias=dict(p,q=-2,r=3)
 assert g.task_components('nested_minus_minus',p)==g.task_components('nested_plus_minus',alias)
 # Explicit arithmetic boundaries and zero components (not zero operands) are
 # verified through each normal family with full whole-bank validity.
 boundary_checks=0
 for level in ['easy','moderate','hard']:
  for t in (['two_vectors'] if level=='easy' else list(g.TEMPLATES)[:4]):
   _,_,ku,qu,*_=g.TEMPLATES[t]
   p=dict(a=[0,-8],b=[7,1],q=5)
   if level!='easy':p.update(c=[-8,0],k=1 if ku else 5,q=1 if qu else 5,r=5)
   if level=='hard':p.update(k=-5,q=5,r=-5)
   r=g.generate(level,template=t,parameters=p);display_check(r);boundary_checks+=1
 # Complete witness-domain enumeration. This is a counted bounded subset of
 # the public domain, not a claim of exhaustive enormous production domains.
 counts={}
 vectors=list(itertools.product([-2,1],repeat=2))
 for level in ['easy','moderate','hard']:
  unique=set();eligible=0
  for t in (['two_vectors'] if level=='easy' else list(g.TEMPLATES)[:4]):
   _,_,ku,qu,*_=g.TEMPLATES[t]
   coefficient_sets=[(q,) for q in [2,3,4,5]] if level=='easy' else (list(itertools.product([1] if ku else [2,3],[1] if qu else [2,3],[2,3])) if level=='moderate' else list(itertools.product([-3,-2,2,3],repeat=3)))
   for vs in itertools.product(vectors,repeat=2 if level=='easy' else 3):
    for cs in coefficient_sets:
     p={key:list(vec) for key,vec in zip('abc',vs)};p.update(dict(zip(['q'] if level=='easy' else ['k','q','r'],cs)))
     try:
      g.validate_parameters(level,t,p);bank,_=g.bank(t,p,g.NORMAL_PROFILE)
      if len(set(map(tuple,bank)))!=5:continue
     except ValueError:continue
     mathematical=g.task_components(t,p)
     unique.add(g.digest(mathematical));eligible+=1
  assert len(unique)>30;counts[level]={'eligible_parameter_instances':eligible,'distinct_mathematical_tasks':len(unique),'witness_component_set':[-2,1],'witness_scalars': [2,3,4,5] if level=='easy' else [1,2,3] if level=='moderate' else [-3,-2,2,3]}
 (D/'engine-input.json').write_text(json.dumps(inputs,indent=2));engine=Path('generate/runs/current/check-engine');subprocess.run([str(engine),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True,capture_output=True,text=True)
 report=json.loads((D/'engine-report.json').read_text());assert report['accepted_checks']==454 and report['rejected_checks']==1816 and report['documented_unresolved_checks']==0
 (D/'review.json').write_text(json.dumps(review,indent=2));parts=[]
 for item in review:
  parts.append('## '+item['label']+'\n\n'+g.markdown(item['record']))
 # Retain actual original raw payloads separately from regenerated records.
 original_parts=['## Captured original '+sid+'\n\n'+q[':question/problem']+'\n\n'+q.get(':question/worked-solution','[Worked solution absent in snapshot]')+'\n\n'+('\n'.join('- $'+a[':answer/value']+'$' for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices']) or '[Answer fields absent in snapshot]') for sid,q in g.ORIGINALS.items()]
 (D/'review.md').write_text('# Column vector review\n\nOriginal labels and omissions are retained. Generated and completed records are explicitly labeled. Opaque raw profiles are evidence only.\n\n'+'\n\n'.join(original_parts+parts))
 byte_runs={sid:{'max_adjacent_ord_92':max([len(m[0]) for m in re.finditer(r'\\+',q[':question/problem'])] or [0]),'matrix_separator_ord_92_count':2} for sid,q in g.ORIGINALS.items()}
 result={'status':'passed','source':{k:g.SOURCE[k] for k in ['database','basis','lineage']},'source_fidelity':{'sources':4,'prompts_exact':4,'attribute_presence_exact':4,'complete_banks_exact':2,'displayed_choices_exact':10,'distractors_exact':8,'solutions_present_exact':2,'correct_designations_present':0,'correct_designations_inferred':4,'fieldless_sources':2,'unrated_sources':2,'source_details':fidelity},'mathematics':{'normal_default_instances':normal_count,'source_replays':4,'changed_raw_instances':4,'completed_sources':4,'additional_per_template_variants':8,'independent_checks':'Actual prompt operands/expression, every scalar term, collected inner component, every displayed equality, final column, complete choice bank','invalid_explicit_inputs_rejected':invalid,'corrupted_display_controls_rejected':corruption_checks,'explicit_boundary_records':boundary_checks},'native_grading':{'records':len(inputs),'checks':checks,'expected_accepted':454,'expected_rejected':1816,'unresolved':0,'report_file':'engine-report.json','actual_accepted':report['accepted_checks'],'actual_rejected':report['rejected_checks'],'entry_point':report['entry_point'],'database_writes':report['database_writes'],'binary_sha256':hashlib.sha256(engine.read_bytes()).hexdigest()},'finite_variety_witness':counts,'decoded_escape_audit':byte_runs,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'plots':'none; matrices are mathematical notation, no assessed geometry','evidence_limits':['No observed easy or hard labels; both authored workload extensions','No source correct refs available; inferred designations are not fidelity matches','Two historical banks have underdetermined wrong-operation intent; residual recipes are evidence only','Modern fieldless sources have no authoritative captured widgets in local lesson 244; radio completion is authored, not recovered','Witness counts enumerate a subset of bounded public domain, excluding notation and bank aliases']}
 (D/'validation.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:result[k] for k in ['status','mathematics','finite_variety_witness']},indent=2))
if __name__=='__main__':main()
