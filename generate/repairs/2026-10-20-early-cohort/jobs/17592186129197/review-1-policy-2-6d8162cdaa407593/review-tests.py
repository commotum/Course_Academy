from oracle import *
import collections,subprocess
P=E.parent/'review-0-policy-2-ab126a3860059c06'
# Reuse the author's executable assertions only as a regression, after independent source reconstruction.
text=(E.parent/'workspace/evidence/repair_checks.py').read_text()
text=text.replace('W=E.parent','W=E/"runtime"').replace("from independent_oracle import",'from oracle import')
text=text.replace("W.parent/'source/source.json'","E.parent/'source/source.json'")
text=text.replace('seed=8191','seed=25031').replace('[701,911,1237]','[20261,20263]')
# Output and all imports now resolve inside review evidence.
(E/'retained-checks.py').write_text(text)
import runpy
ns=runpy.run_path(str(E/'retained-checks.py'));ns['source_check']();ns['shortcut_check']()
# Validate retained findings against concrete old failures, not solely repaired witnesses.
old=json.loads((P/'regression-record.json').read_text());old_replay=json.loads((P/'source-replay-records.json').read_text())
assert probe(old)['success'];assert len(next(r for r in old_replay if r['generation']['template']=='q-82874')['question'][':question/answer-fields'])==2
save('previous-failing-records.json',[old]+old_replay)
fixed=g.generate('easy',8191,template='simple',parameters={'a':1,'h':1,'k':0})
assert not probe(fixed)['success'];save('minimal-regression.json',{'before':old,'after':fixed,'old_signed_pair_success':True,'current_signed_pair_success':False})
save('retained-finding-verification.json',{'preflight_read':True,'all_retained_findings':['bfb40e768b17052babbc','2185805fc9fcc95ab6b5','1ce536ab6304867dd083'],'old_shortcut_detected':True,'old_q82874_field_count':2,'current_shortcut_blocked':True,'current_source_checks':'source-replay.json','author_script_adaptation':'retained-checks.py changes only import paths, output location and witness seeds; does not alter assertions','limitation':'Old generator lacks bank_parameters, so the new common-bank assertion alone cannot diagnose the previous bug. The independently reproduced old signed-pair detector and old field-contract mismatch supply semantic negative controls.'})
records=json.loads((E/'samples.json').read_text());batch=json.loads((E/'batch.json').read_text());checks=[];math=[]
for group,rs in [('sample',records),('batch',batch)]:
 for index,r in enumerate(rs):
  q=r['question'];o=oracle(q);key=correct(q);choices=q[':question/answer-fields'][0][':answer-field/choices'];vs=[parse(a[':answer/value']) for a in choices]
  assert s.simplify(parse(key[':answer/value'])-o['area'])==0
  assert len(vs)==5 and all(s.simplify(z-w)!=0 for j,z in enumerate(vs) for w in vs[:j])
  final=q[':question/worked-solution'].split('&=')[-1].split(r'\end{aligned}')[0].strip();assert s.simplify(parse(final)-o['area'])==0
  math.append({'group':group,'index':index,'oracle':o,'key':key[':answer/value'],'solution_final':final,'passed':True})
  checks.append({'label':f'{group}-{index}','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if s.simplify(parse(a[':answer/value'])-o['area'])==0 else 'rejected','purpose':'Independent integral of visible boundaries'}for a in choices]})
save('math.json',math);save('grader-input.json',checks)
# Independently chosen controlled height and irrelevant shear pairs: bank seed fixed.
pairs=[g.generate('easy',25031,template='simple',parameters=p)for p in [{'a':1,'h':1,'k':0},{'a':1,'h':4,'k':0},{'a':8,'h':1,'k':0}]]
save('counterfactual-records.json',pairs)
cf=[]
for r in pairs:
 q=r['question'];cf.append({'parameters':r['generation']['parameters'],'oracle':oracle(q),'key':correct(q)[':answer/value'],'plot_sha256':hashlib.sha256(pathlib.Path(r['generation']['plot']).read_bytes()).hexdigest(),'prompt':q[':question/problem'],'solution':q[':question/worked-solution']})
assert cf[0]['key']!=cf[1]['key'] and cf[0]['plot_sha256']!=cf[1]['plot_sha256'];assert cf[0]['key']==cf[2]['key'] and cf[0]['plot_sha256']==cf[2]['plot_sha256']
for index,r in enumerate(pairs):
 choices=r['question'][':question/answer-fields'][0][':answer-field/choices'];checks.append({'label':f'controlled-{index}','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if s.simplify(parse(a[':answer/value'])-oracle(r['question'])['area'])==0 else 'rejected'}for a in choices]})
save('grader-input.json',checks);save('counterfactual-results.json',cf)
# Guards, deterministic package relocation, versions, and external-output behavior.
guards=[]
for band,f,p in [('easy','simple',{'a':0,'h':1,'k':0}),('easy','simple',{'a':1,'h':2,'k':0}),('hard','quartic',{'a':1,'h':4,'k':0}),('hard','hyper_y',{'a':1,'h':9,'k':3})]:
 try:g.generate(band,71,template=f,parameters=p);raise AssertionError('invalid accepted')
 except ValueError as ex:guards.append({'band':band,'template':f,'parameters':p,'rejected':str(ex)})
assert g.generate('easy',25031,template='simple',parameters={'a':1,'h':1,'k':0})==pairs[0]
installed={'python':sys.version.split()[0],'packages':{k:__import__(k).__version__ for k in ['sympy','matplotlib','numpy']}};declared=json.loads((E.parent/'workspace/package.json').read_text())['dependencies'];assert installed==declared
save('packaging-tests.json',{'relocated_declared_files_only':True,'deterministic':True,'guards':guards,'installed':installed,'declared':declared,'all_assets_under_evidence':all(pathlib.Path(r['generation']['plot']).is_relative_to(E)for r in records),'finite_cli_limit':'49 easy requested against declared 48 capacity; see finite-limit.json'})
result=subprocess.run([sys.executable,str(E/'runtime/17592186129197.py'),'--difficulty','easy','--count','49','--format','json'],capture_output=True,text=True);assert result.returncode!=0 and 'finite catalog limit' in result.stderr
save('finite-limit.json',{'command':result.args,'exit':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
# Current captured inventory: all formerly affected records explicitly retired.
inv=json.loads((E.parent/'source/inventory.json').read_text());prior=json.loads((P/'affected-inventory.json').read_text())['affected_questions'];by={q[':question/id']:q for q in inv['questions']};iv=[]
for z in prior:
 q=by[z['question_id']];assert q.get(':question/retired') is True;iv.append({'id':z['question_id'],'entity_id':q[':db/id'],'retired':True,'old_defect_preserved_as_history':True})
sourceids={q[':question/id'] for q in json.loads((E.parent/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']}
assert all(q[':question/id'] in sourceids or q.get(':question/retired') is True for q in inv['questions'])
save('inventory-results.json',{'basis':inv['basis'],'previously_affected':iv,'remaining_eligible_generated':0,'all_remaining_active_records_original_source':True,'captured_questions':len(inv['questions'])});save('affected-inventory.json',{'affected_questions':[]})
render=pairs+[next(r for r in records if r['generation']['template']==f)for f in ['mixed','quartic','hyper_y','down','up','vertical','hyper_x']]+batch[:1]
save('render-input.json',render)
(E/'session-state.md').write_text('Current source replay: 12 complete banks pass. Previous signed-pair counterexample blocked; all eight common-bank target witnesses pass. Fresh prompt-derived math and source checks saved. All 11 formerly affected inventory records retired at basis 5602. Next: actual grader, delivery, UI render, final shortcut and selection analysis.\n')
print('Independent math records',len(math),'grader checks',sum(len(r['checks'])for r in checks),'render cases',len(render))
