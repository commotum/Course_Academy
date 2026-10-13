#!/usr/bin/env python3
"""Explicit valid edges, whole-instance invalid guards and CLI determinism.
This supplements the sampled full validator without changing its denominators.
"""
from pathlib import Path
import hashlib,importlib.util,json,subprocess
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('validation',HERE/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
records=[]
for level,t,p in [('easy','exp',{'k':1,'candidates':[[1,1,0],[2,1,0],[3,1,0]]}),('hard','log',{'a':4,'b':'1/4','candidates':[[5,0,-1],[-5,0,1],[4,0,0]]}),('hard','affine',{'n':4,'a':-3,'candidates':[[3,-4,-1],[-3,-3,0],[1,-2,1]]})]:
    r=g.generate(level,template=t,parameters=p);v.displayed(r);records.append(r)
for sid in g.SOURCES:
    for scale in (-6,6):
        r=g.generate('moderate',profile=sid,parameters={'scale':scale});v.displayed(r);records.append(r)
rejected=0
for call in [lambda:g.generate('moderate',profile='q-141096',parameters={'scale':0}),lambda:g.generate('moderate',profile='q-141096',parameters={'scale':7}),lambda:g.generate('easy',profile='q-141096'),lambda:g.generate('hard',template='exp'),lambda:g.generate('moderate',field_type='checkbox')]:
    try:call()
    except ValueError:rejected+=1
    else:raise AssertionError('Boundary guard failed')
engine=[]
for i,r in enumerate(records):
    f=r['question'][':question/answer-fields'][0]
    engine.append({'label':'explicit valid boundary '+str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Explicit valid scope/domain boundary with complete subset criterion'} for a in f[':answer-field/choices']]})
(HERE/'boundary-engine-input.json').write_text(json.dumps(engine,indent=2,ensure_ascii=False)+'\n')
subprocess.run([str(v.ROOT/'generate/runs/current/check-engine'),str(HERE/'boundary-engine-input.json'),str(HERE/'boundary-engine-report.json')],check=True,capture_output=True,text=True)
cmd=[str(v.ROOT/'.venv/bin/python'),str(HERE.with_suffix('.py')),'--difficulty','all','--count','2','--seed','19','--format','json']
a=subprocess.check_output(cmd);b=subprocess.check_output(cmd);assert a==b and len(json.loads(a))==6
report={'pass':True,'independently_checked_boundary_records':len(records),'native_checks':sum(len(r['checks']) for r in engine),'invalid_scope_guards_rejected':rejected,'cli_deterministic_records':6,'cli_sha256':hashlib.sha256(a).hexdigest(),'native_report':json.loads((HERE/'boundary-engine-report.json').read_text())}
(HERE/'boundary-validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='native_report'},indent=2))
