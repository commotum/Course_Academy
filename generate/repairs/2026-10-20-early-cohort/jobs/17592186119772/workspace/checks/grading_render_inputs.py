import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
# Load helpers without executing the regression suite.
from visible_records import E,g,inspect,parse,kind,correct
normal=json.loads((E/'normal-records.json').read_text());controlled=json.loads((E/'controlled-records.json').read_text())
selected=[];seen=set()
for r in normal:
 profile=r['generation']['profile']
 if profile not in seen:selected.append(r);seen.add(profile)
selected.extend(r for r in controlled if r['generation']['profile']=='q-126354')
selected.extend(controlled[-3:])
selected.append(json.loads((E/'regression-results.json').read_text())['exact_counterexample'])
# Include current diagonal/zero and decimals, plus retained subset-radio source bank.
selected.extend(g.generate('moderate',seed=1,profile=p,parameters={'criterion':g.recipe(p)['criterion'],'matrices':g.recipe(p)['matrices']}) for p in ['q-42111','q-42141'])
cases=[]
for n,r in enumerate(selected):
 st=inspect(r);good=set(st['answer']);fields=r['question'][':question/answer-fields'];checks=[]
 for index,f in enumerate(fields):
  checkbox=kind(f[':answer-field/type']).endswith('/checkbox')
  for a in f[':answer-field/choices']:
   value=a[':answer/value']
   if checkbox:expected=(value=='true')==(next(iter(parse(f[':answer-field/key']))) in good)
   elif parse(value):expected=set(parse(value))==good
   else:
    import re
    expected=set(re.findall(r'\$([A-E])\$',value))==good
   checks.append({'field_index':index,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if expected else 'rejected','purpose':'independent forbidden-side zero test on visible objects'})
 cases.append({'label':str(n)+' '+r['generation']['profile'],'record':r,'checks':checks})
(E/'grader-input.json').write_text(json.dumps(cases,indent=2)+'\n')
preview=[normal[0],selected[-3],g.generate_easy(seed=4,profile='q-68743'),selected[-2],selected[-1],next(r for r in normal if r['generation']['profile']=='q-126346')]
(E/'render-records.json').write_text(json.dumps(preview,indent=2)+'\n')
print(json.dumps({'grader_records':len(cases),'grader_responses':sum(len(c['checks']) for c in cases),'render_records':len(preview)}))
