"""Replace the hinted easy questions without changing their mathematics."""
import importlib.util,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(H/'package'))
from generate.matrix_product_prompt_policy import validate_delivery_batch,KP
spec=importlib.util.spec_from_file_location('matrix_fixed',H/'package/generator.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
before=json.loads((H/'before.json').read_text());records=[];pairs=[]
for q in before[':knowledge-point/questions']:
 if q.get(':question/math-academy-id') or q.get(':question/retired') or 'Use a row' not in q[':question/problem']:continue
 prompt=q[':question/problem'];slash=re.escape(chr(92));parts=re.findall(slash+r'+begin[{]bmatrix[}](.*?)'+slash+r'+end[{]bmatrix[}]',prompt,re.S)
 assert len(parts)==2
 matrices=[[[int(v.strip()) for v in row.split('&')] for row in re.split(slash+r'{2,}',body)] for body in parts]
 rows=re.findall(r'<tr>(.*?)</tr>',prompt,re.S);targets=[]
 for i,row in enumerate(rows):
  for j,cell in enumerate(re.findall(r'<td>(.*?)</td>',row)):
   if '{{field-' in cell:targets.append((i,j))
 if not rows:
  for i,row in enumerate(re.findall(r'^\| Row \d \|(.*?)\|$',prompt,re.M)):
   for j,cell in enumerate(row.split('|')):
    if '{{field-' in cell:targets.append((i,j))
 level=q[':question/difficulty'][':db/ident'].split('/')[-1];r=g.build(*matrices,targets,level)
 old_prompt=re.sub(r'\n\nUse a row.*?\n\nComplete the product\.', '\n\nComplete the product.',prompt,flags=re.S)
 if rows:
  assert r['question'][':question/problem']==old_prompt
  assert r['question'][':question/worked-solution']==q[':question/worked-solution']
 assert [f[':answer-field/correct'][':answer/value'] for f in sorted(q[':question/answer-fields'],key=lambda f:f[':answer-field/key'])]==[f[':answer-field/choices'][0][':answer/value'] for f in r['question'][':question/answer-fields']]
 records.append(r);pairs.append({'old':q[':db/id'],'replacement_uuid':r['question'][':question/id'],'parameters':r['generation']['parameters']})
assert len(records)==5
validate_delivery_batch(records,KP)
used={q[':db/id'] for q in json.loads((H/'capture.json').read_text())['usage'] if q.get(':task-item/_content')}
pool=[r for r,pair in zip(records,pairs) if pair['old'] not in used]
pool+=g.generate('easy',5-len(pool),20261027)
validate_delivery_batch(pool,KP)
for name,value in [('candidate-pool',pool),('corrected-examples',records),('replacement-inputs',pairs)]:
 (H/(name+'.json')).write_text(json.dumps(value,indent=2)+'\n')
print('Built',len(records),'corrected examples;',len(pool),'available replacements, including',5-len(used),'unused original calculations')
