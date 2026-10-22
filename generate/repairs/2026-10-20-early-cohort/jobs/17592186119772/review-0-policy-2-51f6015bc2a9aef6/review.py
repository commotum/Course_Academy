#!/usr/bin/env python3
"""Read-only independent review. Run with the job Python; all writes stay here."""
import sys,json,re,hashlib,importlib.util,copy,subprocess,platform,shutil
from pathlib import Path
from fractions import Fraction
E=Path(__file__).resolve().parent
J=E.parent; W=J/'workspace'; R=Path('/home/jake/Developer/Course_Academy')
sys.dont_write_bytecode=True
sys.path.insert(0,str(W))
def save(n,x): (E/n).write_text(json.dumps(x,indent=2,default=str)+'\n')
def enum(x):return x.get(':db/ident') if isinstance(x,dict) else x
def aid(x):return x[':answer/id'] if isinstance(x,dict) else x[1] if isinstance(x,list) else x
def loadmod(p):
 spec=importlib.util.spec_from_file_location('reviewed_generator',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
m=loadmod(W/'17592186119772.py')
def hashes():return {str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()}
save('package-before.json',hashes())
# This parser and predicate do not call the generator's own parser or classifier.
pat=re.compile(r'([A-E])\s*=\s*(?:\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}|\[\\begin\{aligned\}(.*?)\\end\{aligned\}\])',re.S)
def matrices(text):
 out={}
 for z in pat.finditer(text):
  body=z[2] if z[2] is not None else z[3]
  mat=[[Fraction(v.strip()) for v in row.split('&')] for row in body.split(r'\\')]
  if z[1] in out:assert out[z[1]]==mat,('inconsistent repeated display',z[1])
  out[z[1]]=mat
 return out
def target(q):return 'upper' if 'upper triangular' in q[':question/problem'] else 'lower'
def qualifies(a,t):return all(len(row)==len(a) for row in a) and all(a[i][j]==0 for i in range(len(a)) for j in range(len(a)) if (i>j if t=='upper' else i<j))
def correct(f):return next(a for a in f[':answer-field/choices'] if a[':answer/id']==aid(f[':answer-field/correct']))
def displayed(q):
 text=q[':question/problem']+'\n'+q[':question/worked-solution']
 for f in q[':question/answer-fields']:
  text+='\n'+f.get(':answer-field/key','')+'\n'+'\n'.join(a[':answer/value'] for a in f[':answer-field/choices'])
 return matrices(text)
def checked(r):
 q=r['question'];t=target(q);a=displayed(q);good=[l for l,x in a.items() if qualifies(x,t)]
 errors=[]
 for f in q[':question/answer-fields']:
  c=correct(f)[':answer/value'];kind=enum(f[':answer-field/type'])
  if kind.endswith('/checkbox'):
   label=next(iter(matrices(f[':answer-field/key'])))
   if (c=='true')!=(label in good):errors.append('wrong checkbox')
  else:
   choices=f[':answer-field/choices'];valid=[x for x in choices if any(qualifies(v,t) for v in matrices(x[':answer/value']).values())]
   if len(valid)!=1 or valid[0][':answer/id']!=aid(f[':answer-field/correct']):errors.append('wrong/ambiguous radio')
 # All witness equations are independently checked against rendered matrices.
 for z in re.finditer(r'\{([a-e])\}_\{([1-4])([1-4])\}\s*&\s*=(-?\d+)\\ne 0',q[':question/worked-solution']):
  l=z[1].upper();i=int(z[2])-1;j=int(z[3])-1;v=int(z[4]);
  if a[l][i][j]!=v or v==0 or not (i>j if t=='upper' else i<j):errors.append('invalid solution witness')
 # Check English attribution in the source-template solution.
 first=q[':question/worked-solution'].split('\n\n')[0]
 named=set(re.findall(r'\$([A-E])\$',first))
 if named!=set(good):errors.append('solution good-label prose mismatch')
 return {'id':q[':question/id'],'profile':r['generation']['profile'],'target':t,'good':sorted(good),'dimensions':{l:len(v) for l,v in sorted(a.items())},'errors':errors}
source=json.load(open(J/'source/source.json'))
qs=source['material']['kp'][':knowledge-point/questions']; profiles={sid:m.recipe(sid)['level'] for sid in m.SOURCES}
records=[]
for index,(sid,level) in enumerate(profiles.items()):
 for k in range(12 if level=='easy' else 8):records.append(m.generate(level,seed=2026102200+100*index+k,profile=sid))
save('independent-records.json',records)
easy=[r for r in records if r['question'][':question/difficulty'].endswith('/easy')];save('easy-records.json',easy)
batch=json.load(open(J/'samples.json'));save('batch-records.json',batch)
all_checks=[checked(r) for r in records+batch];save('math-results.json',{'method':'Parse learner-visible TeX with Fraction and check every forbidden-side entry, sole radio correctness, checkbox truth and solution good-label prose/nonzero witnesses.','records_checked':len(all_checks),'failures':[x for x in all_checks if x['errors']],'cases':all_checks})
# Every supplied family is attempted. Compare visible complete banks and field contracts.
replays=[];rr=[]
for q in qs:
 sid=q[':question/math-academy-id'];level=enum(q[':question/difficulty']).split('/')[-1]
 try:
  raw=m.generate(level,seed=97,profile='raw:'+sid);p=raw['generation']['parameters'];r=m.generate(level,seed=97,profile=sid,parameters=p);rr.append(r)
  fields=q[':question/answer-fields'];gfields=r['question'][':question/answer-fields'];a=displayed(q);b=displayed(r['question'])
  same=a==b and target(q)==target(r['question'])
  banks=[]
  if level=='easy':
   def bank(f):return sorted((enum(v[':answer/type']),v[':answer/value'].replace(' ','')) for v in f[':answer-field/choices'])
   banks=bank(fields[0])==bank(gfields[0])
   same=same and banks and next(iter(matrices(correct(fields[0])[':answer/value'])))==next(iter(matrices(correct(gfields[0])[':answer/value'])))
  else:
   same=same and {next(iter(matrices(f[':answer-field/key']))):correct(f)[':answer/value'] for f in fields}=={next(iter(matrices(f[':answer-field/key']))):correct(f)[':answer/value'] for f in gfields}
  replays.append({'source_id':q[':question/id'],'profile':sid,'status':'passed' if same else 'failed','complete_easy_bank_equal':banks,'matrices_equal':a==b,'raw_field_types':[enum(f[':answer-field/type']) for f in raw['question'][':question/answer-fields']],'current_source_field_types':[enum(f[':answer-field/type']) for f in fields],'normal_math':checked(r)})
 except Exception as ex:replays.append({'source_id':q[':question/id'],'profile':sid,'status':'failed','error':type(ex).__name__+': '+str(ex)})
save('source-replay-records.json',rr);save('source-replay.json',{'cases':replays,'passed':sum(x['status']=='passed' for x in replays),'total':len(replays),'canonical':'Prompt/solution only; no source answer fields captured.'})
# Minimal classification-changing label reassignment, same 2x2 workload and one correct.
base=m.generate_easy(seed=20261022,profile='q-126354');p=copy.deepcopy(base['generation']['parameters']);p['matrices']['A'],p['matrices']['E']=p['matrices']['E'],p['matrices']['A']
cf={'base':base,'requested_after_parameters':p,'expected':'Valid exactly-one easy bank with A qualifying instead of E, same matrix shapes and entries.'}
try:cf['after']=m.generate_easy(seed=20261022,profile='q-126354',parameters=p);cf['status']='passed'
except Exception as ex:cf.update(status='failed',error=type(ex).__name__+': '+str(ex))
# A same-method target transpose pair and a strictly irrelevant diagonal change.
trans=copy.deepcopy(base['generation']['parameters']);trans['criterion']='lower' if trans['criterion']=='upper' else 'upper';trans['matrices']={k:[list(row) for row in zip(*v)] for k,v in trans['matrices'].items()}
transposed=m.generate_easy(seed=20261022,profile='q-126354',parameters=trans)
irr=copy.deepcopy(base['generation']['parameters']);irr['matrices']['E'][0][0]=11 if irr['matrices']['E'][0][0]!=11 else -11
irrelevant=m.generate_easy(seed=20261022,profile='q-126354',parameters=irr)
save('counterfactuals.json',{'relevant_role_swap':cf,'transpose':{'before':checked(base),'after':checked(transposed),'expected':'Target and inspected side both reverse; label E remains sole qualifying matrix.'},'irrelevant_diagonal':{'before':checked(base),'after':checked(irrelevant),'expected':'Same correct matrix E; diagonal does not affect membership.'}})
save('counterfactual-records.json',[base,transposed,irrelevant])
# Independent dimension-only action: infer source family from labeled dimensions.
shape_rule={tuple(len(v) for l,v in sorted(displayed(r['question']).items())):checked(r)['good'][0] for r in rr if r['question'][':question/difficulty'].endswith('/easy')}
def shape_probe(rs):
 out=[]
 for r in rs:
  c=checked(r);shape=tuple(c['dimensions'].values());prediction=shape_rule.get(shape)
  out.append({'id':c['id'],'profile':c['profile'],'dimensions':shape,'prediction':prediction,'actual':c['good'],'correct':c['good']==[prediction]})
 return {'strategy':'Read sizes of labeled A,B,C,D,E; look up qualifying label without inspecting entries.','rules':[{'dimensions':k,'choose':v} for k,v in shape_rule.items()],'correct':sum(x['correct'] for x in out),'total':len(out),'baseline':0.2,'cases':out}
save('shortcut-raw.json',shape_probe(easy));save('shortcut-batch.json',shape_probe(batch))
# Bounded rejection and deterministic replay tests.
reject=[]
for name,change in [('nonsquare',lambda p:p['matrices']['A'][0].append(0)),('out_of_bounds',lambda p:p['matrices']['A'][0].__setitem__(0,12)),('zero_correct',lambda p:p['matrices']['E'].__setitem__(0,[1,1]) if p['criterion']=='lower' else p['matrices']['E'].__setitem__(1,[1,1]))]:
 p=copy.deepcopy(base['generation']['parameters']);change(p)
 try:m.generate_easy(seed=7,profile='q-126354',parameters=p);reject.append({'case':name,'rejected':False})
 except ValueError as ex:reject.append({'case':name,'rejected':True,'message':str(ex)})
save('runtime-results.json',{'python':platform.python_version(),'sympy':m.sp.__version__,'manifest':json.load(open(W/'package.json')),'deterministic_replay':all(m.generate(r['question'][':question/difficulty'].split('/')[-1],seed=r['generation']['seed'],profile=r['generation']['profile'])==r for r in records[:6]),'rejections':reject,'generator_resampling':'At most 100 full-instance collision retries; samples drawn from finite catalogs. Every profile fixes dimensions and forbidden/allowed nonzero counts per label, so retries cannot remove the dimension-only predictor. Checkbox policy is inactive for easy radio records.','catalogs':{sid:len(m.catalog(sid)) for sid in profiles}})
# Batch all native-grader choices, including all plausible wrong options.
gcases=[]
for index,r in enumerate(rr+[base,transposed,irrelevant]+batch):
 checks=[]
 for fi,f in enumerate(r['question'][':question/answer-fields']):
  for a in f[':answer-field/choices']:checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==aid(f[':answer-field/correct']) else 'rejected','purpose':'independently verified visible matrix membership; exercise every bank choice'})
 gcases.append({'label':f'case-{index}-{r["generation"]["profile"]}','record':r,'checks':checks})
save('grader-input.json',gcases)
# Inventory reproduction: reconstruct explicit displayed inputs, publish-normalize later to verify IDs.
inv=json.load(open(J/'source/inventory.json'));ir=[];attempts=[]
for q in inv['questions']:
 if ':question/math-academy-id' in q:continue
 p={'criterion':target(q),'matrices':{l:[[int(v) for v in row] for row in a] for l,a in displayed(q).items()}}
 sid='q-42090' if len(p['matrices']['A'])==4 else 'q-126351'
 try:
  r=m.generate_moderate(seed=0,profile=sid,parameters=p);ir.append(r)
  attempts.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'profile':sid,'generated_id_before_normalization':r['question'][':question/id'],'parameters':p,'visible_matrices_match':displayed(r['question'])==displayed(q),'stored':q})
 except Exception as ex:attempts.append({'question_id':q[':question/id'],'error':str(ex)})
save('inventory-reproductions.json',attempts);save('inventory-generated-raw.json',ir)
save('render-input.json',batch+[base,transposed,irrelevant]+[r for r in records if r['generation']['profile']=='q-42090'][:1])
save('package-after.json',hashes());assert hashes()==json.load(open(E/'package-before.json'))
(E/'session-state.md').write_text('Independent source account verified. Read package and captured selection rules. No history/preflight present. Completed 88 independent samples + exact batch, all 13 source replay attempts, role-swap rejection, transpose/diagonal counterfactuals, shape-only shortcuts, bounded invalid-input and runtime checks. Next: delivery filters, native grader, actual renderer, inventory identity verification and report. Package hash list unchanged.\n')
print(json.dumps({'math_failures':sum(bool(x['errors']) for x in all_checks),'source_replay':[(x['profile'],x['status']) for x in replays],'shortcut_raw':shape_probe(easy)['correct'],'shortcut_batch':shape_probe(batch)['correct'],'counterfactual_swap':cf['status'],'samples':len(records)}))
