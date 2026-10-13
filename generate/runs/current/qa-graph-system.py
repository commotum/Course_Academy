"""Root verifies printed systems, paired answers and linked plot specifications."""
import importlib.util,json,re
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186138428;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('root_graph_system_readback',R/'graph-system-parser.py');g=module('reviewed_graph_system',D.with_suffix('.py'))
counts={'printed_instances':0,'displayed_equations':0,'blank_values':0,'linked_plot_specs':0,'source_systems':0,'source_missing_values_derived':0,'source_correct_refs_matched':0,'source_available_practice_solutions':0}
def check(r):
 q=r['question'];rows,answer=p.system(q[':question/problem']);fields={f[':answer-field/key']:f for f in q[':question/answer-fields']};assert set(fields)=={'field-1','field-2'}
 for key,value in zip(('field-1','field-2'),answer):
  f=fields[key];assert f[':answer-field/type']==':answer-field.type/blank' and '{{'+key+'}}' in q[':question/problem'];assert len(f[':answer-field/choices'])==1
  a=f[':answer-field/choices'][0];assert a[':answer/id']==f[':answer-field/correct'][1] and p.p.scalar(a[':answer/value'])==value;counts['blank_values']+=1
 points=p.solution_points(q[':question/worked-solution']);assert len(points)==2 and all(v==answer for v in points)
 for role,text in (('prompt',q[':question/problem']),('solution',q[':question/worked-solution'])):
  refs=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',text);assert len(refs)==1;png=Path(refs[0]);assert png.is_file() and png.with_suffix('.json').is_file();side=json.loads(png.with_suffix('.json').read_text());data=side.get('data',side)
  assert tuple(data['intersection'])==answer;assert tuple(tuple(v) for v in data['rows'])==rows
  assert tuple(p.row(v) for v in data['labels'])==rows;lo,hi,bot,top=data['bounds'];assert lo<answer[0]<hi and bot<answer[1]<top
  level=q[':question/difficulty'].rsplit('/',1)[-1];assert data['tick_increment']==(2 if level=='hard' else 1) and data['unit_grid'];counts['linked_plot_specs']+=1
  assert side['role']==role and side['renderer']=='Matplotlib' and len(side['plotted_equations'])==2
  for equation,(A,B,C) in zip(side['plotted_equations'],rows):
   assert (equation['a'],equation['b'],equation['c'])==(A,B,C)
   for X,Y in equation['samples']:assert abs(A*X+B*Y-C)<1e-9
  for axis in ('x','y'):assert all(t%data['tick_increment']==0 for t in side['major_ticks'][axis])
 counts['printed_instances']+=1;counts['displayed_equations']+=2;return rows,answer
sources={key:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions'] for key in (q[':question/math-academy-id'],q[':db/id'],q[':question/id'])}
for case in json.loads((D/'source-cases.json').read_text()):
 old=sources[case.get('source_ma_id',case['source_id'])];r=g.generate(case.get('level',case.get('difficulty','moderate')),template=case['template'],parameters=case['parameters'],profile=case.get('bank_profile',case.get('profile')));rows,answer=check(r);original,correct=p.system(old[':question/problem']);assert rows==original and answer==correct;counts['source_systems']+=1;counts['source_missing_values_derived']+=2
 assert {f[':answer-field/key'] for f in old[':question/answer-fields']}=={'field-1','field-2'}
for item in json.loads((D/'review.json').read_text()):check(item.get('record',item))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
