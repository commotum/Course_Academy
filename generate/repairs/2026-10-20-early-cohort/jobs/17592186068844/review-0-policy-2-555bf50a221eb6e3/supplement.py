import os, json, pathlib, hashlib, shutil, subprocess, sys
import audit as a
R=a.BASE
def save(n,o):(R/n).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
inventory=json.load(open(a.JOB/'source/inventory.json'))
source=json.load(open(a.JOB/'source/source.json'))
originals={q[':question/id'] for q in source['material']['kp'][':knowledge-point/questions']}
generated=[];affected=[];comparison=[]
for q in inventory['questions']:
 if q[':question/id'] in originals:continue
 level=q[':question/difficulty'][':db/ident'].split('/')[-1]
 rhs=a.parse(q[':question/problem'].split('=')[1].split('$')[0].rstrip('., '))
 num,den=a.s.fraction(rhs)
 p={'a':int(num.expand().coeff(a.x,2)),'b':int(num.subs(a.x,0))}
 if level=='hard':p['d']=int(den.subs(a.y,0))
 r=a.g.generate(level,seed=0,parameters=p)
 assert r['question'][':question/id']==q[':question/id']
 assert r['question'][':question/problem']==q[':question/problem']
 assert r['question'][':question/worked-solution']==q[':question/worked-solution']
 stored_bank=sorted(v[':answer/value'] for v in q[':question/answer-fields'][0][':answer-field/choices'])
 assert stored_bank==sorted(v[':answer/value'] for v in a.field(r)[':answer-field/choices'])
 picks=a.shortcut(r);hit=picks==[a.answer_id(a.field(r))]
 generated.append(r);comparison.append({'id':q[':question/id'],'entity_id':q[':db/id'],'parameters':p,'level':level,'id_prompt_solution_bank_match':True,'shortcut_selected':picks,'shortcut_correct':hit,'metadata_note':'Stored capture has no generation field. Seed 0 is a replay seed; question identity is seed/order independent. Parameters and bank profile reproduce stored ID, prompt, solution and all options.'})
 if hit:affected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'finding':'Standard bank exposes the keyed relation from R, -R, 2R option structure without inspecting the differential equation.','reproduction':'PYTHONDONTWRITEBYTECODE=1 '+str(a.PY)+' supplement.py; replay '+level+' parameters='+json.dumps(p,sort_keys=True)+' seed=0','evidence_path':'generated-records.json'})
save('generated-records.json',generated);save('affected-inventory.json',{'affected_questions':affected});save('inventory-results.json',{'basis':inventory['basis'],'total_questions':len(inventory['questions']),'original_source_excluded':len(originals),'generated_replayed':len(generated),'comparisons':comparison,'scope':'All ten non-source captured records replayed. Original source records not classified as generated. Applies to captured basis only.'})
# Package relocation and exact runtime contract. Copies reside only in evidence.
rel=R/'relocated';rel.mkdir(exist_ok=True);(rel/'17592186068844').mkdir(exist_ok=True)
for src,dst in [(a.JOB/'workspace/17592186068844.py',rel/'17592186068844.py'),(a.JOB/'workspace/17592186068844/source.json',rel/'17592186068844/source.json')]:shutil.copyfile(src,dst)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
cmd=[str(a.PY),str(rel/'17592186068844.py'),'--difficulty','easy','--seed','829331','--count','3','--format','json']
run=subprocess.run(cmd,cwd='/tmp',env=env,text=True,capture_output=True)
assert run.returncode==0,run.stderr
relrs=json.loads(run.stdout);save('relocation-records.json',relrs)
same=relrs==[a.g.generate_easy(seed=829331+i) for i in range(3)]
manifest=json.load(open(a.JOB/'workspace/package.json'))
save('packaging-results.json',{'command':cmd,'cwd':'/tmp','returncode':run.returncode,'deterministic_equal_after_relocation':same,'dependencies_declared':manifest['dependencies'],'dependencies_actual':{'python':sys.version.split()[0],'packages':{'sympy':a.s.__version__}},'dependencies_exact':manifest['dependencies']=={'python':sys.version.split()[0],'packages':{'sympy':a.s.__version__}},'output_contract':'JSON stdout; no external assets or database writes; source fixture is declared in manifest.','manifest_files_present':all((a.JOB/'workspace'/p).is_file() for p in manifest['files']),'repair_history_present':(a.JOB/'repair-history.json').exists(),'repair_preflight_present':(a.JOB/'repair-preflight.json').exists()})
# Counterfactuals generated through the public API; valid shift and irrelevant shuffle.
before=a.g.generate_easy(seed=101,template='exp_linear',parameters={'h':0,'k':0})
after=a.g.generate_easy(seed=101,template='exp_linear',parameters={'h':1,'k':0})
shuffle=a.g.generate_easy(seed=102,template='exp_linear',parameters={'h':0,'k':0})
save('counterfactual-records.json',[before,after,shuffle])
save('counterfactual-results.json',{'relevant':{'change':'h:0 -> 1, fixed k=0, seed=101, exp_linear','before_response':'e^y=x^2+C','after_response':'e^y=(x+1)^2+C','prompt_changed':before['question'][':question/problem']!=after['question'][':question/problem'],'solution_changed':before['question'][':question/worked-solution']!=after['question'][':question/worked-solution'],'old_equation_residual_after_change':'2, nonzero','math':[a.inspect_record(before),a.inspect_record(after)]},'irrelevant':{'change':'seed:101 -> 102 with fixed mathematical parameters and template','prompt_preserved':before['question'][':question/problem']==shuffle['question'][':question/problem'],'solution_preserved':before['question'][':question/worked-solution']==shuffle['question'][':question/worked-solution'],'correct_answer_identity_preserved':a.answer_id(a.field(before))==a.answer_id(a.field(shuffle)),'option_order_changed':[v[':answer/id'] for v in a.field(before)[':answer-field/choices']]!=[v[':answer/id'] for v in a.field(shuffle)[':answer-field/choices']]}})
print(json.dumps({'inventory_replayed':len(generated),'affected':len(affected),'relocation_matches':same}))
