import json,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parents[1];E=W/'evidence';REPO=Path('/home/jake/Developer/Course_Academy');records=json.loads((E/'delivery/accepted.json').read_text());cases=[]
for i,r in enumerate(records):
 f=r['question'][':question/answer-fields'][0];cases.append({'label':f'delivered {i}','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual key after publication normalization'} for a in f[':answer-field/choices']]})
(E/'delivered-engine-input.json').write_text(json.dumps(cases,indent=2)+'\n')
subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(E/'delivered-engine-input.json'),str(E/'delivered-engine-report.json')],check=True)
S=REPO/'generate/repairs/2026-10-20-early-cohort/jobs/17592186172038/source'
subprocess.run([sys.executable,str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(E/'relocated-a-records.json'),'--source',str(S/'source.json'),'--inventory',str(S/'inventory.json'),'--difficulty','easy','--output',str(E/'relocated-delivery'),'--asset-root',str(E/'relocated-a-assets'),'--math-root','/media/jake/SSD/EDB/math'],check=True)
