"""Public API boundary checks for the newly declared hard signed-row slots."""
import sys
sys.dont_write_bytecode=True
import copy,importlib.util,json
from pathlib import Path
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('kp100868_boundaries',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
cases={x['source_id']:x for x in json.loads((D/'source-cases.json').read_text())};checks=[]
def rejected(sid,profile,gains,reason):
 p=copy.deepcopy(cases[sid]['parameters']);p['row_gains']=gains
 try:g.generate(cases[sid]['level'],template=sid,parameters=p,profile=profile)
 except ValueError as e:
  assert reason in str(e),(sid,gains,str(e));checks.append({'source_id':sid,'profile':profile,'row_gains':gains,'outcome':'rejected','reason':str(e)})
 else:raise AssertionError('Invalid explicit row gains silently accepted')
for sid in g.HARD_ROW_GAINS:
 for gains in [[0,1,1],[3,1,1],[-3,1,1],[True,1,1],[1,1]]:rejected(sid,'authored-operations',gains,'Hard row gains')
 rejected(sid,'observed',[-1,1,1],'Observed profile fixes')
rejected('q-127270','authored-operations',[1,2,1],'workload')
rejected('q-127270','authored-operations',[1,1,2],'workload')
rejected('q-318591','authored-operations',[1,1,2],'workload')
rejected('q-318595','observed',[1,1,1],'hard-only')
(D/'hard-boundaries.json').write_text(json.dumps({'status':'pass','checked_public_rejections':len(checks),'checks':checks},indent=2)+'\n');print('Hard row-slot boundary checks:',len(checks))
