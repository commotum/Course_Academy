"""Root reads actual heading order, unknown cells, directed routes and solutions."""
import importlib.util,json,re,hashlib,collections
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186087819;D=R.parents[2]/f'generate/scratch/{K}'
sp=importlib.util.spec_from_file_location('root_route_gen',D.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
# Every arrow/direction/loop inspected in the seven original diagrams.
ORIGINAL={'q-138940':[[0,1,1],[0,1,2],[1,0,0]],'q-139685':[[0,1,1],[0,0,1],[1,1,0]],'q-139689':[[1,1,0],[0,1,2],[0,1,0]],'q-139719':[[0,1,0,2],[0,0,1,0],[0,0,0,1],[0,0,1,0]],'q-319346':[[0,2,0],[1,0,3],[2,0,0]],'q-319412':[[0,1,2,0],[2,0,1,0],[1,0,0,2],[0,1,1,0]],'q-319429':[[1,1,3],[1,2,2],[0,1,1]]}
C=dict(instances=0,table_cells=0,diagram_edge_counts=0,solution_route_counts=0,displayed_values=0,source_questions=0,source_banks=0,source_values=0,source_existing_refs=0,source_missing_refs=0,source_exact_prompts_after_asset_paths=0,source_exact_solutions=0,source_repaired_solutions=0)
def table(text):
 out={};columns=None;rows=[]
 if '<table' in text:
  groups=re.findall(r'<tr>(.*?)</tr>',text,re.S)
  for line in groups:
   names=re.findall(r'<b>([A-D])</b>',line)
   if len(names)>1:columns=names;continue
   if len(names)!=1:continue
   values=re.findall(r'<td align="center">\$(.*?)\$</td>',line,re.S)
   assert columns and len(values)==len(columns);rows.append(names[0]);out.update({(names[0],col):v for col,v in zip(columns,values)})
 else:
  for line in text.splitlines():
   if not line.startswith('|'):continue
   names=re.findall(r'\*\*([A-D])\*\*',line)
   if len(names)>1:columns=names;continue
   if len(names)!=1:continue
   values=[a or b for a,b in re.findall(r'\$([^$]+)\$|(\{\{field-[123]\}\})',line)];assert columns and len(values)==len(columns),(line,values,columns)
   rows.append(names[0]);out.update({(names[0],col):v for col,v in zip(columns,values)})
 assert len(rows) in (3,4) and sorted(rows)==sorted(columns);return out,rows,columns

def check(r):
 q=r['question'];prompt=q[':question/problem'];worked=q[':question/worked-solution'];cells,rows,cols=table(prompt);path=Path(re.search(r'!\[\]\(([^)]+)\)',prompt)[1]);meta=r['generation'];n=len(rows);letters='ABCD'[:n]
 if meta['assets']['source_reuse']:
  sid=meta['source_ids'][0];matrix=ORIGINAL[sid];source=g.SOURCES[sid];ref=re.search(r'!\[\]\(([^)]+)\)',source[':question/problem'])[1];assert hashlib.sha256(path.read_bytes()).digest()==hashlib.sha256((Path('/media/jake/SSD/EDB/math')/ref).read_bytes()).digest()
 else:
  data=json.loads(path.with_suffix('.json').read_text());matrix=data['matrix'];edges=collections.Counter((z['from'],z['to']) for z in data['edges'])
  assert len(matrix)==n and all(len(row)==n for row in matrix)
  for a in range(n):
   for b in range(n):assert edges[a,b]==matrix[a][b];C['diagram_edge_counts']+=1
  assert len(data['coordinates'])==n and data['renderer'].startswith('Matplotlib')
 unknown={}
 for (a,b),value in cells.items():
  want=matrix[letters.index(a)][letters.index(b)]
  if value in 'abc' or value.startswith('{{'):assert value not in unknown;unknown[value]=(a,b,want)
  else:assert int(value)==want
  C['table_cells']+=1
 assert len(unknown)==3
 if q[':question/difficulty'].endswith('/hard'):assert n==4 and rows!=list(letters) and cols!=list(letters) and rows!=cols and sum(a==b for a,b,_ in unknown.values())==1
 for f in q[':question/answer-fields']:
  vals=[int(a[':answer/value']) for a in f[':answer-field/choices']];assert len(set(vals))==len(vals)
  want=unknown['{{'+f[':answer-field/key']+'}}'][2] if f[':answer-field/type'].endswith('/blank') else sum(v[2] for v in unknown.values())
  for a,value in zip(f[':answer-field/choices'],vals):assert (value==want)==(a[':answer/id']==f[':answer-field/correct'][1])
  if meta['bank_profile']=='authored_omissions':
   v=[unknown[z][2] for z in 'abc'];assert sorted(vals)==sorted([sum(v),v[0]+v[1],v[0]+v[2],sum(matrix[letters.index(b)][letters.index(a)] for a,b,_ in unknown.values()),sum(map(sum,matrix))])
  C['displayed_values']+=len(vals)
 complete,sol_rows,sol_cols=table(worked);assert sol_rows==rows and sol_cols==cols
 for (a,b),value in complete.items():assert int(value)==matrix[letters.index(a)][letters.index(b)]
 bullets=re.findall(r'^- .*',worked,re.M);assert len(bullets)==3
 raw_exception=meta['bank_profile']=='raw_solution_319429'
 for i,line in enumerate(bullets):
  m=re.search(r'There (?:are|is) (?:\$(\d+)\$|(?P<zero>no)) arrows? starting at Station ([A-D]) and ending at Station ([A-D])',line);assert m,line
  count=0 if m['zero'] else int(m[1]);a,b=m[3],m[4]
  if raw_exception and i==1:assert (a,b,count)==('B','C',2);b='B'
  assert (a,b,count) in unknown.values();assert count==matrix[letters.index(a)][letters.index(b)];C['solution_route_counts']+=1
  for var,num in re.findall(r'([abc])=(\d+)',line):assert unknown[var][2]==int(num)
 if 'a+b+c' in prompt:
  eq=re.search(r'a\s*\+\s*b\s*\+\s*c\s*=\s*(\d+)\+(\d+)\+(\d+)\s*=\s*(\d+)',worked);assert eq;v=[unknown[z][2] for z in 'abc'];assert list(map(int,eq.groups()))==v+[sum(v)]
 C['instances']+=1;return q
sources={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
def asset_norm(text):return re.sub(r'!\[\]\([^)]*\)','IMAGE',text)
for case in json.loads((D/'source-cases.json').read_text()):
 old=sources[case['source_id']];q=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));C['source_questions']+=1;assert asset_norm(q[':question/problem'])==asset_norm(old[':question/problem']);C['source_exact_prompts_after_asset_paths']+=1
 nf={f[':answer-field/key']:f for f in q[':question/answer-fields']}
 for of in old[':question/answer-fields']:
  fresh=nf[of[':answer-field/key']];assert sorted(z[':answer/value'] for z in fresh[':answer-field/choices'])==sorted(z[':answer/value'] for z in of[':answer-field/choices']);C['source_banks']+=1;C['source_values']+=len(of[':answer-field/choices'])
  if of.get(':answer-field/correct'):
   actual=next(z[':answer/value'] for z in fresh[':answer-field/choices'] if z[':answer/id']==fresh[':answer-field/correct'][1]);assert actual==of[':answer-field/correct'][':answer/value'];C['source_existing_refs']+=1
  else:C['source_missing_refs']+=1
 if old.get(':question/worked-solution'):
  expected=old[':question/worked-solution']
  if case['source_id']=='q-319429':
   raw=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile='raw_solution_319429'));assert asset_norm(raw[':question/worked-solution'])==asset_norm(expected);C['source_repaired_solutions']+=1
   assert asset_norm(q[':question/worked-solution'])==asset_norm(expected.replace('starting at Station B and ending at Station C','starting at Station B and ending at Station B').replace('routes from B to C','routes from B to B'))
  else:assert asset_norm(q[':question/worked-solution'])==asset_norm(expected);C['source_exact_solutions']+=1
review=json.loads((D/'review.json').read_text())
if isinstance(review,dict):review=[z for values in review.values() for z in values]
for item in review:
 rec=item.get('record',item)
 if 'question' in rec:check(rec)
for item in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(item)
C['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
