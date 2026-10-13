"""Focused revalidation after preserving unsimplified basis-sum row structure."""
import importlib.util,json,subprocess,hashlib
from pathlib import Path
D=Path(__file__).parent
s=importlib.util.spec_from_file_location('v',D/'validate.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v);g=v.g
items=json.load(open(D/'engine-input.json'));count=0;stages=0
for item in items:
 r=item['record'];m=r['generation']
 if m['template']=='q-33123':
  r=g.generate(r['question'][':question/difficulty'].split('/')[-1],m['seed'],m['template'],parameters=m['parameters'],profile=m['bank_profile']);stages+=v.mathcheck(r);count+=1;item['record']=r
  f=r['question'][':question/answer-fields'][0];item['checks']=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned complete-bank choice'} for a in f[':answer-field/choices']]
assert count==23
json.dump(items,open(D/'engine-input.json','w'),indent=2)
subprocess.run(['generate/runs/current/check-engine',str(D/'engine-input.json'),str(D/'engine-results.json')],check=True)
report=json.load(open(D/'validation.json'));report['basis_preservation_delta_records']=count;report['basis_preservation_delta_math_stages']=stages;report['generator_sha256']=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest();json.dump(report,open(D/'validation.json','w'),indent=2)
review=json.load(open(D/'review.json'));review=[g.generate(r['question'][':question/difficulty'].split('/')[-1],r['generation']['seed'],r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['bank_profile']) for r in review]
json.dump(review,open(D/'review.json','w'),indent=2,ensure_ascii=False)
source=[g.generate(c['level'],0,c['template'],parameters=c['parameters'],profile=c['bank_profile']) for c in json.load(open(D/'source-cases.json'))];json.dump(source,open(D/'source-replays.json','w'),indent=2,ensure_ascii=False)
raw=json.load(open(D/'source.json'))['record'][':knowledge-point/questions'];md=['# Originals and generated variants','Raw snapshot: `source.json`, math basis 1356. All generated items below are labeled.']
for q,r in zip(raw,source):
 md+=['## Original '+q[':question/math-academy-id'],q[':question/problem'],'\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices']),q.get(':question/worked-solution','No captured worked solution.'),'## Replay (repairs explicitly recorded)',g.markdown(r)]
md+=['# Generated variants (observed profiles and authored defaults)']+[g.markdown(r) for r in review];(D/'review.md').write_text('\n\n'.join(md))
print(json.dumps({'status':'pass','updated_records':count,'displayed_math_stages':stages,'native_checks':len(items)*5}))
