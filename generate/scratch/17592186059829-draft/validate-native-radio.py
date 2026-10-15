"""Additional accepted equivalent radio-ID forms, in complete native fields."""
from pathlib import Path
import json,subprocess
D=Path(__file__).resolve().parent
items=json.loads((D/'engine-input.json').read_text())
for item in items:
 f=item['record']['question'][':question/answer-fields'][0];choices=f[':answer-field/choices'];correct=f[':answer-field/correct'][1]
 ci=next(i for i,a in enumerate(choices) if a[':answer/id']==correct);wi=next(i for i,a in enumerate(choices) if a[':answer/id']!=correct)
 item['checks']=[{'submitted':'000'+str(100+ci),'expected':'accepted','purpose':'Equivalent zero-padded decimal native entity-ID entry for same correct field-owned choice'}, {'submitted':'000'+str(100+wi),'expected':'rejected','purpose':'Equivalent decimal native entity-ID entry for a mathematically incorrect field-owned choice'}]
(D/'engine-radio-equivalence-input.json').write_text(json.dumps(items,indent=2)+'\n')
subprocess.run([str(D/'check-engine'),str(D/'engine-radio-equivalence-input.json'),str(D/'engine-radio-equivalence-report.json')],check=True)
