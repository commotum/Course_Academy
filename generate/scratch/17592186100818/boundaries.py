"""Actual rendered validation of every corner of both independent slots."""
import sys
sys.dont_write_bytecode=True
import importlib.util,itertools,json
from pathlib import Path
H=Path(__file__).parent;z=importlib.util.spec_from_file_location('kp00818_boundarygen',H.with_suffix('.py'));G=importlib.util.module_from_spec(z);z.loader.exec_module(G);R=G.R
rows=[];tasks=set()
for sid in G.QS:
 for m,d,k in itertools.product((1,6),repeat=3):
  p={'coefficient_num':m,'coefficient_den':d,'x_scale':k};r=G.generate(G.CONFIG[sid],template=sid,parameters=p);expected,checks=R.stages(r['question']);f=r['question'][':question/answer-fields'][0];last=R.blocks(r['question'][':question/problem'])[-1];mult=R.scalar(last.lstrip(')').strip())if last.startswith(')')else 1;key=next(a for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1]);assert R.equal(R.scalar(key[':answer/value'])*mult,expected)
  tasks.add(r['generation']['math_fingerprint']);rows.append({'source_id':sid,'parameters':p,'math_fingerprint':r['generation']['math_fingerprint'],'operative_checks':checks,'key_verified':True})
(H/'boundaries.json').write_text(json.dumps({'records':len(rows),'actual_distinct_math_tasks':len(tasks),'boundary_values':'Every1/6 corner of coefficient numerator, denominator, and x_scale; roles independent','cases':rows},indent=2)+'\n');print(len(rows),len(tasks))
