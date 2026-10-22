#!/usr/bin/env python3
"""Independent targeted review. All writes are relative to this evidence directory."""
import sys, json, pathlib, hashlib, subprocess, shutil, re, copy, platform, collections, os
sys.dont_write_bytecode = True
E=pathlib.Path(__file__).resolve().parent; J=E.parent; P=J/'workspace'
R=pathlib.Path('/home/jake/Developer/Course_Academy'); PREV=J/'review-0-policy-2-a6cc0b16d3cf5a91'
def save(n,v): (E/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def load(p): return json.loads(pathlib.Path(p).read_text())
def hashes(): return {str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()}
def field(r):return r['question'][':question/answer-fields'][0]
def answer(r):
 f=field(r); return next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==f[':answer-field/correct'][1])
save('package-before.json',hashes())
sys.path.insert(0,str(P)); import generator as g
sys.path.insert(0,str(R)); from scripts.generator_publish import stable_identities, content_fingerprint
commands=[]
def run(args):
 p=subprocess.run(list(map(str,args)),cwd=E,text=True,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 commands.append({'command':list(map(str,args)),'cwd':str(E),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}); return p
# Reuse unchanged source replay analysis only after comparing actual replay content.
old=load(PREV/'source-replay-records.json'); replay=[g.replay_source(t,seed=826032) for t in g.SOURCES]
rows=[]
for a,b in zip(old,replay):
 qa,qb=a['question'],b['question']
 rows.append({'template':b['generation']['template'],'source_id':b['generation']['source_question_ids'][0],
 'prompt_equal':qa[':question/problem']==qb[':question/problem'],'solution_equal':qa[':question/worked-solution']==qb[':question/worked-solution'],
 'complete_bank_equal':[c[':answer/value'] for c in field(a)[':answer-field/choices']]==[c[':answer/value'] for c in field(b)[':answer-field/choices']], 'correct_equal':answer(a)==answer(b)})
assert all(all(r[k] for k in ('prompt_equal','solution_equal','complete_bank_equal','correct_equal')) for r in rows)
save('source-replay-records.json',replay); shutil.copy2(PREV/'source-replay.json',E/'prior-source-replay.json')
shutil.copy2(PREV/'scope.json',E/'scope.json')
save('source-replay.json',{'comparison':rows,'provenance':str(PREV/'source-replay.json'),'reused_evidence':'prior-source-replay.json','all_equal':True,'scope':'Nine supported original parameter cases; unchanged prompts, complete banks, correct mathematics and worked solutions. Unsupported canonical and arctangent cases documented in prior-source-replay.json.'})
# One fresh construction per coefficient-bank window per template, not a second old-domain audit.
templates=('cube_root','affine','linear_log')
samples=[g.generate(t, g.coefficient_bank(i)[(i+ti)%5], 720219,bank_index=i) for ti,t in enumerate(templates) for i in range(18)]
randoms=g.generate_batch('easy',24,720223)
controlled=[]; pairs=[]
for t in templates:
 for bi in (0,7,17):
  group=[g.generate(t,a,720227,bank_index=bi) for a in g.coefficient_bank(bi)]
  assert len({tuple(c[':answer/value'] for c in field(r)[':answer-field/choices']) for r in group})==1
  assert len({answer(r) for r in group})==5
  controlled.extend(group)
  pairs.append({'kind':'relevant','name':f'{t} bank {bi}, change target only','before':group[0],'after':group[-1]})
 base=g.generate(t,-1,720229,bank_index=7); after=copy.deepcopy(base);field(after)[':answer-field/choices'].reverse()
 pairs.append({'kind':'irrelevant','name':t+' reverse choices','before':base,'after':after})
batch=load(J/'samples.json'); save('runner-batch.json',batch)
save('independent-samples.json',samples+randoms);save('controlled-records.json',controlled);save('counterfactuals.json',pairs)
render=[r for t in templates for p in pairs if p['name'].startswith(t) and (('bank 7' in p['name']) or p['kind']=='irrelevant') for r in (p['before'],p['after'])]
save('render-records.json',render+batch)
# Independently parse prompt/candidate strings. Do not call generator components/answer helpers.
import sympy as s
x,y,C=s.symbols('x y C',positive=True)
def visible(r):
 q=r['question'];m=re.search(r'=\\frac\{(-?\d*)(x\^3|x)\+(y\^3|2y|y)\}\{(xy\^2|x)\}',q[':question/problem']); assert m,q[':question/problem']
 def integer(z):return -1 if z=='-' else 1 if z=='' else int(z)
 a=integer(m[1]); t='cube_root' if m[2]=='x^3' else 'affine' if m[3]=='2y' else 'linear_log'
 rhs=y/x+a*x*x/(y*y) if t=='cube_root' else a+(2 if t=='affine' else 1)*y/x
 coefficients=[];derivatives=[]
 for c in field(r)[':answer-field/choices']:
  z=c[':answer/value']
  if t=='cube_root':
   mm=re.fullmatch(r'y=x\\sqrt\[3\]\{(-?\d+)\\ln\|x\|\+C\}',z);assert mm,z
   b=int(mm[1]);H=y**3/x**3-b*s.log(x)-C;coefficients.append(b/3)
  elif t=='affine':
   mm=re.fullmatch(r'y=Cx\^2([+-])(\d*)x',z);assert mm,z
   b=(1 if mm[1]=='+' else -1)*int(mm[2] or 1);H=(y-b*x)/x**2-C;coefficients.append(-b)
  else:
   mm=re.fullmatch(r'y=(-?\d*)x\\ln\|x\|\+Cx',z);assert mm,z
   b=integer(mm[1]);H=y/x-b*s.log(x)-C;coefficients.append(b)
  derivatives.append(str(s.factor(s.diff(H,x)+s.diff(H,y)*rhs)))
 true=[i for i,z in enumerate(derivatives) if z=='0']; assert len(true)==1
 assert field(r)[':answer-field/choices'][true[0]][':answer/id']==field(r)[':answer-field/correct'][1]
 assert answer(r) in q[':question/worked-solution'].replace('&','')
 return t,a,coefficients,derivatives
mathrows=[];cases=[]
allgroups={'window_sample':samples,'fresh_random':randoms,'controlled':controlled,'runner':batch,'counterfactual':[r for p in pairs for r in (p['before'],p['after'])]}
for group,records in allgroups.items():
 for i,r in enumerate(records):
  t,a,co,ds=visible(r);mathrows.append({'group':group,'index':i,'template':t,'prompt_a':a,'candidate_implied_a':co,'directional_derivatives':ds,'passed':True})
  f=field(r);cases.append({'label':f'{group} {i}','record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if d=='0' else 'rejected','purpose':'Independent implicit directional derivative of candidate along visible ODE'} for c,d in zip(f[':answer-field/choices'],ds)]})
save('math.json',{'method':'Implicit candidate H, compute H_x+H_y f(x,y) from visible equation and all candidate strings; only one vanishes identically. d ln|x|/dx=1/x on either nonzero interval; real cube root checked through y^3/x^3. Also verify solution contains independently determined keyed expression.','sympy':s.__version__,'checks':mathrows,'failures':[]})
cf=[]
for p in pairs:
 b,a=p['before'],p['after'];same=p['kind']=='irrelevant'
 row={'name':p['name'],'kind':p['kind'],'before_answer':answer(b),'after_answer':answer(a),'same_bank':sorted(c[':answer/value'] for c in field(b)[':answer-field/choices'])==sorted(c[':answer/value'] for c in field(a)[':answer-field/choices']), 'prompt_equal':b['question'][':question/problem']==a['question'][':question/problem'],'solution_equal':b['question'][':question/worked-solution']==a['question'][':question/worked-solution'],'answer_equal':answer(b)==answer(a)}
 assert row['same_bank'] and all(row[k]==same for k in ('prompt_equal','solution_equal','answer_equal'))
 # Before valid response is rejected after relevant target changes (UUIDs differ, find same math value).
 oldchoice=next(c for c in field(a)[':answer-field/choices'] if c[':answer/value']==answer(b))
 cases.append({'label':'cross-response '+p['name'],'record':a,'checks':[{'submitted_answer_id':oldchoice[':answer/id'],'expected':'accepted' if same else 'rejected','purpose':'Hold mathematical response fixed across relevant/irrelevant counterfactual'}]})
 row['passed']=True;cf.append(row)
save('counterfactual-results.json',{'pairs':cf,'grader_evidence':'grader-results.json','renderer_evidence':'render/rendering.json'})
save('grader-input.json',cases)
# Re-run retained original strict cue predictor against actual old and new records.
shutil.copy2(PREV/'reproduce_shortcut.py',E/'retained_predictor.py')
import retained_predictor
legacy=load(PREV/'minimal-failing-record.json')
if isinstance(legacy,list):legacy=legacy[0]
if 'record' in legacy:legacy=legacy['record']
assert 'question' in legacy
new=g.generate('cube_root',2,826033);oldprediction=retained_predictor.predict(field(legacy));newprediction=retained_predictor.predict(field(new))
assert oldprediction[1]==field(legacy)[':answer-field/correct'][1] and newprediction[1] is None
save('retained-counterexample.json',{'old_record':legacy,'current_record':new,'old_prediction':oldprediction,'current_prediction':newprediction,'old_strict_acceptance_would_fail':True,'current_passed':True})
# Run the supplied executable regression safely redirected into evidence; then run against old construction.
text=(P/'checks/check_shortcuts.py').read_text().replace("ROOT = pathlib.Path(__file__).resolve().parents[1]","ROOT = pathlib.Path(sys.argv[1]).resolve()")
text=text.replace("out = ROOT/'evidence'; out.mkdir(exist_ok=True)","out = pathlib.Path(sys.argv[2]); out.mkdir(exist_ok=True)")
text=text.replace("sys.path.insert(0, str(ROOT/'checks'))","sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))").replace('from reproduce_shortcut_original import predict','from retained_predictor import predict')
(E/'supplied_check_redirected.py').write_text(text)
shutil.copytree(PREV/'relocated',E/'legacy-package',dirs_exist_ok=True)
for name,path in [('current',P),('legacy',E/'legacy-package')]:
 p=run([sys.executable,E/'supplied_check_redirected.py',path,E/('supplied-'+name)])
 assert (p.returncode==0)==(name=='current')
save('repair-preflight-verification.json',{'retained_finding':'a2f26476abafae793e46','original_sha256':hashlib.sha256((P/'checks/check_shortcuts.py').read_bytes()).hexdigest(),'adaptation':'Only ROOT, output location and predictor import redirected. All assertions retained.','results':commands[-2:],'independent_minimal_evidence':'retained-counterexample.json'})
# Packaging and runtime: exact dependency contract, repeat/relocate, invalid controls.
args=[sys.executable,P/'generator.py','--difficulty','easy','--count','7','--seed','720233']; aa=run(args);bb=run(args)
rel=E/'relocated';rel.mkdir(exist_ok=True)
for f in ('generator.py','math_format.py','package.json'):shutil.copy2(P/f,rel/f)
cc=run([sys.executable,rel/'generator.py',*args[2:]])
reject=[]
for ar in (['--difficulty','hard'],['--count','-1']):reject.append(run([sys.executable,P/'generator.py',*ar]).returncode!=0)
for ar,kw in [(('cube_root',0),{}),(('affine',10),{}),(('linear_log',-10),{}),(('missing',1),{}),(('cube_root',1),{'bank_index':-1}),(('cube_root',1),{'bank_index':18}),(('cube_root',9),{'bank_index':0}),(('cube_root',2),{'source_replay':True})]:
 try:g.generate(*ar,**kw);reject.append(False)
 except ValueError:reject.append(True)
manifest=load(P/'package.json');assert manifest['dependencies']=={'python':platform.python_version(),'packages':{}}
assert aa.returncode==bb.returncode==cc.returncode==0 and aa.stdout==bb.stdout==cc.stdout and all(reject)
save('packaging.json',{'manifest':manifest,'installed_python':platform.python_version(),'deterministic':aa.stdout==bb.stdout,'relocation_identical':aa.stdout==cc.stdout,'invalid_cases_rejected':reject,'runtime':'Standard library only. SymPy used only by independent reviewer. No generated assets or external output paths; stdout JSON.','generation_rejection':'No rejection loop for valid easy inputs: choose bank, then uniform eligible target. Invalid controls fail explicitly.','commands':commands})
# Preserve proven inventory findings, reproduce complete records and fingerprint identity against same captured inventory.
inventory=load(J/'source/inventory.json'); prior_inventory=load(PREV/'affected-inventory.json'); oldrecords=load(PREV/'generated-records.json');oldbyid={r['question'][':question/id']:r for r in oldrecords};stored={q[':question/id']:q for q in inventory['questions']}
for item in prior_inventory['affected_questions']:
 q=stored[item['question_id']];r=oldbyid[item['question_id']]
 assert q[':db/id']==item['entity_id'] and content_fingerprint(q)==content_fingerprint(r['question'])
 assert retained_predictor.predict(field(r))[1]==field(r)[':answer-field/correct'][1]
 item['reproduction']='PYTHONDONTWRITEBYTECODE=1 '+sys.executable+' audit_review.py; verifies captured UUID, entity ID, full content fingerprint, and legacy bank-only prediction. Original independent reconstruction: '+item['reproduction']
save('generated-records.json',oldrecords);save('affected-inventory.json',prior_inventory)
shutil.copy2(PREV/'inventory-assessment.json',E/'inventory-assessment.json');shutil.copy2(PREV/'selection.json',E/'prior-selection.json')
save('provenance.json',{'source_hash_binding':'9e312e97b5bacd4ca007799a17d0a150fc0d3848b74583b4e781c9e642b2c17f','inventory_hash_binding':'4225cd636eb1c49f3c947f86676c253a5a5e42b7505b0bf5ecf94f193c95312e','reused_from':str(PREV),'copies':['source-analysis.json','source-images.png','prior-source-replay.json','scope.json','retained_predictor.py','legacy-package','generated-records.json','inventory-assessment.json','prior-selection.json'],'confirmation':'Source passages re-read before package inspection. All nine replay bodies equal. Five legacy generated records rechecked against captured UUID/entity ID/content fingerprint and original cue predictor. Legacy defects do not describe repaired current banks. Prior selection rules re-read from actual unchanged engine.'})
(E/'session-state.md').write_text('Completed: confirmed source account; nine exact mathematical source replays; changed-bank window/boundary/role samples; independent symbolic correctness; cross-response counterfactual inputs; supplied regression fails old and passes new; packaging, inventory legacy reproduction. Next: native grader, delivery, current shortcut and selection assessment, actual UI rendering.\n')
print(json.dumps({'math_records':len(mathrows),'source_replay':len(rows),'controlled':len(controlled),'native_cases':len(cases),'legacy_affected':len(prior_inventory['affected_questions']),'package_passed':True}))
if __name__=='__main__':pass
