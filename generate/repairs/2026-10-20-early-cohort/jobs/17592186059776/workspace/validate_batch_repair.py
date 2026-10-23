"""Affected selection validation: source replay, math, grader, relocation inputs."""
import copy, json, re, shutil, subprocess, sys, platform
from pathlib import Path
sys.dont_write_bytecode=True
import check_batch_selection as b
c,v,g=b.c,b.v,b.c.g
OUT,ROOT=b.OUT,b.ROOT
save=b.save

def norm(t): return re.sub(r'\s+','',t).replace('$','').replace(r'\,','')
records=[]
for name in ['exact','easy','moderate']:
    records+=json.loads((OUT/(name+'-records.json')).read_text())
source=json.loads((ROOT.parent/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']
replay=[]
for q in source:
    sid=q[':question/math-academy-id']; level=q[':question/difficulty'][':db/ident'].split('/')[-1]
    r=g.generate(level,31817,sid,[0,0]); records.append(r)
    f=q[':question/answer-fields'][0];rf=r['question'][':question/answer-fields'][0]
    assert all(norm(q[k])==norm(r['question'][k]) for k in [':question/problem',':question/worked-solution'])
    assert sorted(norm(a[':answer/value']) for a in f[':answer-field/choices'])==sorted(norm(a[':answer/value']) for a in rf[':answer-field/choices'])
    assert norm(f[':answer-field/correct'][':answer/value'])==norm(next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1]))
    replay.append({'source_id':q[':question/id'],'complete_bank_prompt_solution_key':True})
save('source-replay.json',replay)
a=g.generate('easy',31817,'q-73544',[-1,0]); z=g.generate('easy',31817,'q-73544',[1,1])
ma,mz=v.supplied(a['question']),v.supplied(z['question'])
assert ma[0,:]==mz[0,:] and ma[:,:2]==mz[:,:2] and ma[1,2]!=mz[1,2]
assert ma[:,:2].inv()*ma[:,2]!=mz[:,:2].inv()*mz[:,2]
assert a['question'][':question/worked-solution']!=z['question'][':question/worked-solution']
records += [a,z]
cases=[]
for r in records:
    v.independent(r)
    cases.append({'label':r['question'][':question/id'],'record':r,'checks':v.checks(r)})
rev=copy.deepcopy(a);rev['question'][':question/answer-fields'][0][':answer-field/choices'].reverse()
cases.append({'label':'irrelevant-choice-order','record':rev,'checks':v.checks(a)})
save('counterfactual-records.json',[a,z,rev]);save('native-input.json',cases)
exact=json.loads((OUT/'exact-records.json').read_text())
old=json.loads((ROOT.parent/'samples.json').read_text())
assert [(r['generation']['template'],r['generation']['parameters']) for r in old]==[(r['generation']['template'],r['generation']['parameters']) for r in exact]
manifest=json.loads((ROOT/'package.json').read_text());rel=OUT/'relocated';rel.mkdir(exist_ok=True)
for f in manifest['files']:
    dst=rel/f;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/f,dst)
cmd=[sys.executable,str(rel/manifest['entrypoint']),'--difficulty','easy','--count','5','--seed','3334594587','--format','json']
p=subprocess.run(cmd,cwd=rel,capture_output=True,text=True,check=True)
assert json.loads(p.stdout)==exact==g.batch('easy',5,3334594587)
assert manifest['dependencies']=={'python':platform.python_version(),'packages':{'sympy':c.S.__version__}}
save('packaging.json',{'command':cmd,'determinism_and_relocation':True,'dependencies':manifest['dependencies']})
save('render-input.json',[r for r in exact if r['generation']['template']=='q-73544'])
summary={'source_replay':10,'independent_math_records':len(records),'native_cases':len(cases),'native_responses':sum(len(x['checks']) for x in cases),
         'exact_batch_same_mathematical_tasks':True,'counterfactual_constant_and_order_checks':True,'relocation_and_determinism':True}
save('validation-summary.json',summary);print(json.dumps(summary))
