#!/usr/bin/env python3
"""Supplemental exact displayed-math/native checks at permitted boundaries."""
import importlib.util,json,subprocess
from pathlib import Path
root=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('v',root/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
fixtures=[];checked=[]
for family,spec in v.g.FAMILIES.items():
    if family=='helix':ps=[{'m':6,'lo':0,'hi':'pi/12'},{'m':-6,'lo':'5*pi/12','hi':'pi/2'}]
    elif family=='linear_cubic':ps=[{'m':6,'lo':-2,'hi':1},{'m':-6,'lo':'-1/2','hi':3}]
    elif family.startswith('hard'):ps=[{'a':1,'b':1,'d':1,'c':1,'e':1,'m':1,'lo':0,'hi':'3/2'},{'a':3,'b':3,'d':3,'c':-3,'e':3,'m':-3,'lo':1,'hi':3}]
    else:ps=[{'m':6,'lo':0,'hi':6},{'m':-6,'lo':'sqrt(2)','hi':'sqrt(3)'}]
    for i,p in enumerate(ps):
        record=v.g.generate(spec[0],i,family,parameters=p);v.check(record)
        label=family+'/explicit-boundary/'+str(i)
        fixtures.append(v.engine_fixture(record,label))
        checked.append({'label':label,'parameters':p,'question_id':record['question'][':question/id']})
        print(label,flush=True)
(root/'boundary-native-input.json').write_text(json.dumps(fixtures,indent=2)+'\n')
subprocess.run([str(v.REPO/'generate/runs/current/check-engine'),str(root/'boundary-native-input.json'),str(root/'boundary-native-report.json')],check=True)
(root/'boundary-validation.json').write_text(json.dumps({'status':'passed','explicit_boundary_instances':checked,'normal_mathematics_readback':14,'native':json.loads((root/'boundary-native-report.json').read_text())},indent=2)+'\n')
