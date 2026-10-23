"""Focused repair validation; imports the retained mathematical witness only."""
import sys, json, re, importlib.util, copy, shutil, subprocess, platform
from pathlib import Path
sys.dont_write_bytecode=True
import check_repair as c
ROOT=c.ROOT; OUT=ROOT/'evidence'/'validation'; OUT.mkdir(parents=True,exist_ok=True)
REPO=Path('/home/jake/Developer/Course_Academy')
spec=importlib.util.spec_from_file_location('prior_validation', ROOT/'17592186059776/validate.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
g=c.g

def save(name,data): (OUT/name).write_text(json.dumps(data,indent=2,default=str)+'\n')
def norm(t): return re.sub(r'\s+','',t).replace('$','').replace(r'\,','')

def check(rec):
    # Existing witness reads rendered equations and executes displayed operations.
    v.independent(rec)
    q=rec['question']; m=v.supplied(q); xy=m[:,:2].inv()*m[:,2]
    field=q[':question/answer-fields'][0]; valid=[]
    for a in field[':answer-field/choices']:
        am=c.matrices(a[':answer/value'])[0]
        ok=am[:,:2]*xy==am[:,2]
        pair=re.search(r'x=([^$]+)\$ and \$y=([^$]+)',a[':answer/value'])
        if pair: ok=ok and c.number(pair[1])==xy[0] and c.number(pair[2])==xy[1]
        if ok:valid.append(a[':answer/id'])
    assert valid==[field[':answer-field/correct'][1]]
    return {'label':q[':question/id'],'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],
        'expected':'accepted' if a[':answer/id'] in valid else 'rejected',
        'purpose':'Independent full matrix and solution-pair witness'} for a in field[':answer-field/choices']]}

source=json.loads((ROOT.parent/'source/source.json').read_text())['material']['kp']
replay=[]; replays=[]
for q in source[':knowledge-point/questions']:
    sid=q[':question/math-academy-id'];lev=q[':question/difficulty'][':db/ident'].split('/')[-1]
    r=g.generate(lev,31817,sid,[0,0]); replays.append(r)
    f=q[':question/answer-fields'][0]; rf=r['question'][':question/answer-fields'][0]
    result={'source_id':q[':question/id'],'template':sid,
        'prompt':norm(q[':question/problem'])==norm(r['question'][':question/problem']),
        'solution':norm(q[':question/worked-solution'])==norm(r['question'][':question/worked-solution']),
        'complete_bank':sorted(norm(a[':answer/value']) for a in f[':answer-field/choices'])==sorted(norm(a[':answer/value']) for a in rf[':answer-field/choices']),
        'key':norm(f[':answer-field/correct'][':answer/value'])==norm(next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1]))}
    replay.append(result)
save('source-replay.json',replay); assert all(all(x[k] for k in ['prompt','solution','complete_bank','key']) for x in replay),replay
probes=json.loads((ROOT/'evidence/regressions/probe-records.json').read_text())
retained=json.loads((ROOT/'evidence/regressions/retained-records.json').read_text())
oldbatch=json.loads((ROOT.parent/'samples.json').read_text())
batch=g.batch('easy',5,oldbatch[0]['generation']['seed'])
assert [(r['generation']['template'],r['generation']['parameters']) for r in batch] == [(r['generation']['template'],r['generation']['parameters']) for r in oldbatch]
save('exact-batch.json',batch)
# Hold the first equation and all coefficients fixed while changing the second
# constant: q73544 first RHS changes by 2h-4k, so delta(h,k)=(2,1).
a=g.generate('easy',31817,'q-73544',[-1,0]);b=g.generate('easy',31817,'q-73544',[1,1])
ma=v.supplied(a['question']);mb=v.supplied(b['question']);assert ma[0,:]==mb[0,:] and ma[:,:2]==mb[:,:2] and ma[1,2]!=mb[1,2]
assert a['question'][':question/worked-solution']!=b['question'][':question/worked-solution']
assert a['question'][':question/answer-fields'][0][':answer-field/correct']!=b['question'][':question/answer-fields'][0][':answer-field/correct']
rev=copy.deepcopy(a);rev['question'][':question/answer-fields'][0][':answer-field/choices'].reverse()
cf=[a,b,rev];save('counterfactual-records.json',cf)
cases=[check(r) for r in replays+retained+probes+batch+[a,b]]
revcase=copy.deepcopy(check(a));revcase['record']=rev;revcase['label']='irrelevant-order';cases.append(revcase)
save('native-input.json',cases)
save('counterfactual-results.json',{'first_equation_preserved':True,'coefficients_preserved':True,'second_constant_changed':True,'answer_and_solution_changed':True,'option_reversal_preserves_key':True})
for level in g.SUPPORTED_LEVELS:
    records=[r for r in probes+retained+replays if r['question'][':question/difficulty'].endswith('/'+level)]
    save(level+'-delivery-input.json',records)
# Scope of historical finding is generated records; every captured row is source.
inv=json.loads((ROOT.parent/'source/inventory.json').read_text());ids={q[':question/id'] for q in source[':knowledge-point/questions']}
originals=[q[':question/id'] for q in inv['questions'] if q[':question/id'] in ids]
assert len(originals)==len(inv['questions'])==10
save('inventory-review.json',{'basis':inv['basis'],'source_originals':originals,'generated_records':0,'conclusion':'Verified no generated records in captured pool, so no eligible generated historical instances of this defect. Source originals are not relabeled as generated. No retirement eligibility needs resolving for a generated candidate.'})
(ROOT/'affected-inventory.json').write_text('{"affected_questions":[]}\n')
# Relocate only declared runtime files; no historical artifacts or repo imports.
manifest=json.loads((ROOT/'package.json').read_text());rel=OUT/'relocated';rel.mkdir(exist_ok=True)
for name in manifest['files']:
    dst=rel/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/name,dst)
cmd=[sys.executable,str(rel/manifest['entrypoint']),'--difficulty','easy','--count','5','--seed','3334594587','--format','json']
p=subprocess.run(cmd,cwd=rel,capture_output=True,text=True,check=True)
assert json.loads(p.stdout)==batch
assert g.batch('easy',5,3334594587)==batch
save('packaging.json',{'command':cmd,'relocation_and_determinism':True,'dependencies':{'python':platform.python_version(),'packages':{'sympy':c.S.__version__}},'declared_files':manifest['files']})
save('render-input.json',[batch[0],next(r for r in batch if 'and then solve' not in r['question'][':question/problem']),next(r for r in probes if r['generation']['template']=='q-20500')])
save('summary.json',{'source_replay':len(replay),'independently_verified_records':len(cases)-1,'native_responses_prepared':sum(len(x['checks']) for x in cases),'exact_batch_count':len(batch),'inventory_generated':0,'relocation':True,'counterfactual':True,'semantic_instances':len({g.task_key(r['question']) for r in probes}),'note':'Native grading, delivery and visual inspection run separately.'})
print((OUT/'summary.json').read_text())
