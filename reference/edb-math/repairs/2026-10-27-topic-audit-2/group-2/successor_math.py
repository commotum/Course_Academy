import json,signal,sys
from pathlib import Path
from independent_math import one
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[4]));from scripts.generator_source_policy import reject_excluded_sources
records=json.loads((H/'successor-samples.json').read_text());excluded=json.loads((H.parent/'source-eligibility.json').read_text())['excluded_questions'];reject_excluded_sources([s['record']for s in records],excluded);out=[]
for i,s in enumerate(records):
 row={'index':i,'kp':s['kp'],'band':s['band'],'question_id':s['record']['question'][':question/id']}
 try:
  signal.setitimer(signal.ITIMER_REAL,3);checks=one(s['record']['question'],s['kp']);assert all(c['status']!='candidate'for c in checks),checks;row.update(passed=True,checks=checks)
 except Exception as ex:row.update(passed=False,error=str(ex)[:500])
 finally:signal.setitimer(signal.ITIMER_REAL,0)
 out.append(row)
(H/'successor-math-verification.json').write_text(json.dumps(out,indent=2)+'\n');print('successors math',sum(r['passed']for r in out),'/',len(out),'source exclusion hits0');print([(r['index'],r.get('error'))for r in out if not r['passed']])
