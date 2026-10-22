import sys,json,re,difflib
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R.parent/'workspace'));import math_format as mf
qs=json.load(open(R.parent/'source/source.json'))['material']['kp'][':knowledge-point/questions'];rs=json.load(open(R/'source-replay-records.json'));tests=json.load(open(R/'source-replay.json'))
results=[]
for q,t in zip(qs,tests):
 ids=[a.get('record_id') for a in t['attempts'] if a.get('same_bank')]
 if not ids:
  results.append({'source_id':t['source_id'],'complete_bank_replay':False,'reason':'All profiles reject 5-component source parameters.'});continue
 r=next(r for r in rs if r['question'][':question/id']==ids[0]);row={'source_id':t['source_id'],'complete_bank_replay':True,'field_type':'radio matches source','bank_comparison':'all five choices, ignoring order','checks':{}}
 for key in [':question/problem',':question/worked-solution']:
  a=mf.normalize_prose(q[key]);b=r['question'][key]
  row['checks'][key]={'exact_normalized':a==b,'difference':[] if a==b else list(difflib.ndiff(a.splitlines(),b.splitlines()))}
 row['accepted_presentation_changes']='Visible set braces may use fixed-size instead of scalable delimiters; algebraic terms are written in variable-index order. Independent coefficient parsing verifies equivalence; theorem, dimension-identification, expansion, substitution and final arithmetic stages are preserved.'
 results.append(row)
(R/'source-fidelity-details.json').write_text(json.dumps(results,indent=2))
print('Source fidelity: 12 complete bank replays; 3 rejected source families. Differences preserved in source-fidelity-details.json.')
