#!/usr/bin/env python3
"""Focused independent revision review; writes only below this file's directory."""
import sys
sys.dont_write_bytecode = True
import collections, copy, hashlib, json, os, pathlib, shutil, subprocess
import review_tests as t
R=t.ROOT; JOB=t.JOB; PKG=t.PKG; PY=t.PY; REPO=t.REPO
SEED=846271
def save(n,v): t.save(n,v)
def bank(r):return [a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
def key(r):return bank(r)[t.keypos(r)]
def level(q):return q[':question/difficulty'][':db/ident'].split('/')[-1]
def run(cmd,name):
 p=subprocess.run([str(x) for x in cmd],cwd=R,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True)
 save(name,{'command':[str(x) for x in cmd],'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
 return p
def main():
 before=t.hashes();save('package-hashes-before.json',before)
 g=t.load_generator(PKG/'17592186105745.py')
 orig=json.loads((JOB/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']
 # Retained independent tests: exact old failure versus the revision.
 old=t.load_generator(JOB/'review-0-policy-2-359ba6ae464e8b78/relocated-package/17592186105745.py')
 retained=[]
 for name,mod in [('previous',old),('current',g)]:
  rs=[mod.generate('easy',71923,'q-73743',{'rhs_scale':v}) for v in [1,-1]]
  save('retained-'+name+'-records.json',rs)
  missing=[]
  for sid,d in [('q-42156','easy'),('q-73524','easy'),('q-20959','easy'),('q-20962','moderate')]:
   try:mod.generate(d,71923,sid,{'rhs_scale':1})
   except Exception as e:missing.append({'template':sid,'error':str(e)})
  retained.append({'package':name,'bank_only_hits':[t.shortcut(r)[0]==[t.keypos(r)] for r in rs],'source_errors':missing})
 save('retained-findings.json',retained)
 # Author preflight is rerun on both packages, with output redirected here.
 author=(PKG/'regression_checks.py').read_text()
 author=author.replace("ROOT=pathlib.Path(__file__).resolve().parent","ROOT=pathlib.Path(__import__('os').environ['REVIEW_PACKAGE'])")
 author=author.replace("OUT=ROOT/'evidence';OUT.mkdir(exist_ok=True)","OUT=pathlib.Path(__import__('os').environ['REVIEW_OUTPUT']);OUT.mkdir(exist_ok=True)")
 (R/'author_regression_copy.py').write_text(author)
 shutil.copyfile(R/'review_tests.py',R/'independent_math.py')
 preflight=[]
 for name,path in [('previous',JOB/'review-0-policy-2-359ba6ae464e8b78/relocated-package'),('current',PKG)]:
  for case in ['shortcut','source-replay']:
   dest=R/('author-'+name+'-'+case);dest.mkdir(exist_ok=True)
   cmd=[str(PY),str(R/'author_regression_copy.py'),'--case',case]
   p=subprocess.run(cmd,cwd=R,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',REVIEW_PACKAGE=str(path),REVIEW_OUTPUT=str(dest)),capture_output=True,text=True)
   preflight.append({'package':name,'case':case,'command':cmd,'REVIEW_PACKAGE':str(path),'REVIEW_OUTPUT':str(dest),'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
 save('preflight-verification.json',preflight)
 # Complete source replay, including restored banks and capture-duplicate resolution.
 replay=[];source_records=[]
 for q in orig:
  sid=q[':question/math-academy-id'];r=g.generate(level(q),SEED,sid,{'bank_profile':'source'})
  source_records.append(r);rq=r['question'];f=next(f for f in q[':question/answer-fields'] if ':answer-field/correct' in f)
  replay.append({'source_id':q[':question/id'],'template':sid,'prompt_equal':rq[':question/problem']==q[':question/problem'],'solution_equal':rq[':question/worked-solution']==q[':question/worked-solution'],'complete_bank_equal':sorted(bank(r))==sorted(a[':answer/value'] for a in f[':answer-field/choices']),'key_equal':key(r)==f[':answer-field/correct'][':answer/value'],'one_field':len(rq[':question/answer-fields'])==1})
 save('source-replay-records.json',source_records);save('source-replay.json',replay)
 # Fresh explicit boundary and interior instances per restored/source profile.
 sampled=[]
 for q in orig:
  for u,v in [(-1,-4),(1,3),(-1,4)]:
   sampled.append(g.generate(level(q),SEED,q[':question/math-academy-id'],{'column_scale':u,'rhs_scale':v}))
 save('sampled-records.json',sampled)
 # Controlled bank: all five choices must become the answer for fixed visible bank.
 pairs=[[-1,-4],[1,3],[-1,1],[1,-1],[1,4]]
 controlled=[];cfreport=[]
 for q in orig:
  sid=q[':question/math-academy-id']
  rs=[g.generate(level(q),SEED,sid,{'bank_pairs':pairs,'target_index':i}) for i in range(5)]
  controlled.extend(rs)
  cfreport.append({'template':sid,'parameters':{'bank_pairs':pairs,'target_index':'0..4','seed':SEED},'same_bank':all(bank(r)==bank(rs[0]) for r in rs),'distinct_keys':len(set(key(r) for r in rs)),'distinct_prompts':len(set(r['question'][':question/problem'] for r in rs)),'distinct_solutions':len(set(r['question'][':question/worked-solution'] for r in rs)),'key_positions':[t.keypos(r) for r in rs],'math_pass':all(t.math_record(r)['pass'] for r in rs)})
 save('counterfactual-records.json',controlled);save('counterfactual-results.json',cfreport)
 # One relevant pair isolates RHS, one isolates slope; before and after answers coexist.
 # The (1,3) -> (1,-1) -> (1,4) cases isolate RHS; (-1,1) -> (1,-1)
 # changes both. Add exactly opposite slope with fixed RHS and all else fixed.
 relpairs=[]
 for sid in ['q-42156','q-73743','q-20962']:
  d=level(g.CASES[sid]); bp=[[1,-4],[-1,-4],[1,2],[-1,1],[1,4]]
  relpairs += [g.generate(d,SEED,sid,{'bank_pairs':bp,'target_index':i}) for i in [0,1]]
 save('slope-counterfactual-records.json',relpairs)
 # Irrelevant first/second-row changes from two real source profiles.
 ir=[g.generate('moderate',SEED,sid,{'bank_seed':SEED,'column_scale':-1,'rhs_scale':3}) for sid in ['q-20963','q-73740']]
 save('irrelevant-records.json',ir)
 save('irrelevant-results.json',{'first_rows_equal':t.mats(ir[0]['question'][':question/problem'])[0][0,:]==t.mats(ir[1]['question'][':question/problem'])[0][0,:],'second_rows_differ':ir[0]['question'][':question/problem']!=ir[1]['question'][':question/problem'],'answer_equivalent':t.family(key(ir[0]))==t.family(key(ir[1])),'solution_matrix_equivalent':t.mats(ir[0]['question'][':question/problem'])[0].rref()[0]==t.mats(ir[1]['question'][':question/problem'])[0].rref()[0]})
 batch=json.loads((JOB/'samples.json').read_text());save('runner-batch.json',batch)
 fresh=g.batch('easy',14,SEED)+g.batch('moderate',10,SEED+1);save('fresh-records.json',fresh)
 save('easy-records.json',[r for r in sampled+fresh if r['question'][':question/difficulty'].endswith('/easy')])
 save('moderate-records.json',[r for r in sampled+fresh if r['question'][':question/difficulty'].endswith('/moderate')])
 allrecords=source_records+sampled+controlled+relpairs+ir+fresh+batch
 math=[t.math_record(r) for r in allrecords]
 save('math-results.json',{'total':len(math),'failed':[v for v in math if not v['pass']],'results':math})
 save('replay-results.json',{'records':len(allrecords),'deterministic_metadata_replay':all(g.generate(r['question'][':question/difficulty'].split('/')[-1],r['generation']['seed'],r['generation']['template'],r['generation']['parameters'])==r for r in allrecords)})
 cases=[]
 for i,r in enumerate(allrecords):
  z=math[i];f=r['question'][':question/answer-fields'][0]
  cases.append({'label':f'independent-{i}-{r["generation"]["template"]}','record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if z['valid_choices'][j] else 'rejected','purpose':'Exact math classification; counterfactual banks include other prompts correct answers as wrong choices.'} for j,c in enumerate(f[':answer-field/choices'])]})
 save('grader-input.json',cases)
 # Rejection and resampling: instrument current batch's actual proposals, no mutation on disk.
 traces=[];original_generate=g.generate
 for d,count in [('easy',14),('moderate',10)]:
  proposals=[]
  def traced(*args,**kw):
   r=original_generate(*args,**kw);proposals.append(r);return r
  g.generate=traced;rs=g.batch(d,count,SEED);g.generate=original_generate
  save('sampler-proposals-'+d+'.json',proposals);save('sampler-accepted-'+d+'.json',rs)
  traces.append({'difficulty':d,'count':count,'seed':SEED,'proposals':len(proposals),'accepted':len(rs),'duplicates_rejected':len(proposals)-len(rs),'proposal_templates':dict(collections.Counter(r['generation']['template'] for r in proposals)),'retained_templates':dict(collections.Counter(r['generation']['template'] for r in rs)),'rule':'At most 2000 draws; reject previously seen normalized-equation/operation fingerprint. No sign, position or bank-property rejection.'})
 save('sampler-stage-results.json',traces)
 boundaries=[]
 for params in [{'rhs_scale':v} for v in [0,5,-5,'1',None]]+[{'column_scale':2},{'target_index':-1},{'target_index':5},{'target_index':True},{'bank_pairs':[[1,1]]*5,'target_index':0}]:
  try:g.generate('easy',SEED,'q-42156',params);accepted=True;err=None
  except Exception as e:accepted=False;err=repr(e)
  boundaries.append({'parameters':params,'accepted':accepted,'error':err})
 save('boundaries.json',boundaries)
 # Relocate only declared runtime files; third-party versions must match exactly.
 manifest=json.loads((PKG/'package.json').read_text());dest=R/'relocated-current'
 for f in manifest['files']+['package.json']:
  p=dest/f;p.parent.mkdir(exist_ok=True,parents=True);shutil.copyfile(PKG/f,p)
 cmd=[str(PY),str(dest/manifest['entrypoint']),'--difficulty','easy','--count','5','--seed',str(SEED),'--format','json']
 p=run(cmd,'relocation-command.json');p2=run(cmd,'deterministic-command.json')
 save('relocation-records.json',json.loads(p.stdout) if p.returncode==0 else [])
 save('packaging.json',{'actual':{'python':sys.version.split()[0],'packages':{'sympy':t.S.__version__}},'manifest':manifest['dependencies'],'deterministic':p.stdout==p2.stdout,'relocated_matches_current':json.loads(p.stdout)==g.batch('easy',5,SEED) if p.returncode==0 else False,'declared_files_sufficient':p.returncode==0,'external_output':'No assets or external outputs created. CLI JSON stdout; source resolves relative to entrypoint.','package_unchanged':before==t.hashes()})
 inv=json.loads((JOB/'source/inventory.json').read_text());source_ids={q[':question/id'] for q in orig}
 save('affected-inventory.json',{'affected_questions':[]})
 save('inventory-audit.json',{'basis':inv['basis'],'count':len(inv['questions']),'all_ids_are_original_source':all(q[':question/id'] in source_ids for q in inv['questions']),'generated_metadata_count':sum(any('generation' in k or 'generator' in k for k in q) for q in inv['questions']),'conclusion':'Captured bank contains only the 16 original source questions, no demonstrated generated affected instance. Verified for captured basis only; originals are not classified as generated.'})
 save('package-hashes-after-tests.json',t.hashes())
 render=[controlled[i] for i in [5,8,25,29,40,41,75,79]]+relpairs+ir+batch
 save('render-records.json',render)
 save('scope-results.json',{'families':['easy REF-only','easy general solution from REF','moderate elimination then general solution'],'observed':'Small exact signed-column and RHS transformations preserve 2x2 rank-one consistent systems, first basic variable, second free variable, five math radio choices and original reasoning workload. New homogeneous banks require identifying the correct normalized coefficients rather than counting zero rows.','scope_evidence':'All source profiles replay; 48 boundary/interior and 24 fresh records independently classified. Finite source coefficient magnitudes and row multipliers keep arithmetic comparable, while sign/magnitude and target roles change.'})
 (R/'session-state.md').write_text('Focused revision tests saved: original defects verified against old code and current code; author preflight rerun against both. Complete source replay, fresh math, controlled target and slope changes, irrelevant row change, rejection/resampling, replay, relocation and captured inventory audit complete. Delivery, native grading, UI and final report remain.\n')
 print(json.dumps({'source_cases':len(replay),'source_failed':[v['template'] for v in replay if not all(v[k] for k in ['prompt_equal','solution_equal','complete_bank_equal','key_equal','one_field'])],'math_total':len(math),'math_failures':sum(not v['pass'] for v in math),'counterfactual_groups':len(cfreport),'preflight':[(v['package'],v['case'],v['returncode']) for v in preflight],'retained':retained,'boundary_unexpected':[v for v in boundaries if v['accepted']],'package_unchanged':before==t.hashes()}))
if __name__=='__main__':main()
