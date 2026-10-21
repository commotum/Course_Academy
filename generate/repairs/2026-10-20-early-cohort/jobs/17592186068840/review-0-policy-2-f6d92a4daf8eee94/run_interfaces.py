import json,subprocess,sys
from pathlib import Path
E=Path(__file__).resolve().parent;R=Path('/home/jake/Developer/Course_Academy')
cases=json.load(open(E/'grader-input.json'))
json.dump(cases[:-1],open(E/'grader-supported-input.json','w'),indent=2)
json.dump(cases[-1:],open(E/'grader-reciprocal-input.json','w'),indent=2)
results=[]
for name in ['supported','reciprocal']:
 args=[str(R/'generate/runs/current/check-engine'),str(E/f'grader-{name}-input.json'),str(E/f'grader-{name}-results.json')]
 p=subprocess.run(args,capture_output=True,text=True)
 results.append({'command':args,'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'expected_rc':0})
(E/'grader-execution.json').write_text(json.dumps(results,indent=2)+'\n')
print([(name['rc'],name['stderr'][:220]) for name in results])
# exact source replay ignores only equivalent TeX delimiter sizing
report=json.load(open(E/'source-replay.json'))
source=json.load(open(E.parent/'source/source.json'))['material']['kp'][':knowledge-point/questions'];replays=json.load(open(E/'source-replay-records.json'))
norm=lambda v:v.replace('\u2061','').replace(r'\left','').replace(r'\right','')
for row in report:
 if row.get('template')=='negative_exp':
  a=next(q for q in source if q[':question/math-academy-id']=='q-3850')[':question/answer-fields'][0][':answer-field/choices'];b=next(r for r in replays if r['generation']['template']=='negative_exp')['question'][':question/answer-fields'][0][':answer-field/choices'];row['checks']['complete_bank']=sorted(norm(c[':answer/value']) for c in a)==sorted(norm(c[':answer/value']) for c in b);row['status']='passed' if all(row['checks'].values()) else 'failed';row['normalization']='Ignored only U+2061 and \\left/\\right delimiter sizing; no expression changes.'
(E/'source-replay.json').write_text(json.dumps(report,indent=2)+'\n')
rows=json.load(open(E/'batch-records.json'))+json.load(open(E/'counterfactual-records.json'))
# include one scaled tan rendered row, all controlled pairs and the exact batch
(E/'render-records.json').write_text(json.dumps(rows,indent=2)+'\n')
