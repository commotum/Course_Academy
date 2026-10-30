"""Restore actual source table cells and controls; preserve all database identities."""
import collections,copy,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path[:0]=[str(R/'scripts'),str(R/'reference/edb-math/repairs/2026-10-26-mixed-math-titles')]
from reconstruct import SourceRenderer
from question_capture.math_format import MATH,matrix_equation,system_answer,normalize_tex,validate_math_boundaries,validate_matrix_layouts,validate_math_structure
S=json.loads((H/'lesson.json').read_text());targets={q[':question/math-academy-id']:q for q in S['questions']if any(f[':answer-field/type'][':db/ident']==':answer-field.type/blank'for f in q.get(':question/answer-fields',[]))};paths=collections.defaultdict(list)
for line in(R/'.local/edb/mathml-tables-work/source-paths.txt').read_text().splitlines():
 p=Path(line);m=re.search(r'(q-\d+)-(?:before|after)\.json$|history-(q-\d+)(?:-[a-f0-9]+)?\.json$',p.name)
 if m and(m[1]or m[2])in targets and p.exists():paths[m[1]or m[2]].append(p)
proposals=[];evidence=[];rejected=[]
for mid,q in sorted(targets.items()):
 candidates=[]
 for p in paths[mid]:
  raw=json.loads(p.read_text());html=raw.get('html')or raw.get('raw_html')
  if not html:continue
  soup=BeautifulSoup(html,'html.parser');node=soup.select_one('.questionText,.questionWidget-text')
  if node is None:continue
  tables=[t for t in node.find_all('table')if t.find_parent('table')is None]
  if len(tables)!=1:continue
  table=tables[0];r=SourceRenderer(None);source_html=str(table);source_fields={}
  for field in raw.get('fields',[]):
   if field.get('type')!='blank':continue
   control=table.find(id=field.get('dom_id'))
   if control is None:continue
   shown=r.text(control).strip();spans=list(MATH.finditer(shown))
   if len(spans)==1 and spans[0][0]==shown:
    edge=2 if shown.startswith(('$$',r'\(',r'\['))else 1;shown=shown[edge:-edge].strip()
   source_fields[field['key']]={'key':field['key'],'correct_value':shown}
   control.replace_with('{{'+field['key']+'}}')
  if len(source_fields)!=len(q[':question/answer-fields']):continue
  def value(cell):
   text=r.text(cell,True).strip()
   if re.fullmatch(r'\{\{field-\d+\}\}',text):return text
   spans=list(MATH.finditer(text));assert len(spans)==1 and spans[0][0]==text,(mid,text)
   match=spans[0][0];edge=2 if match.startswith(('$$',r'\(',r'\['))else 1
   return match[edge:-edge].strip()
  nested=[t for t in table.find_all('table')if t.find_parent('table')is table]
  if len(nested)==3:
   grids=[]
   for t in nested:
    rows=[]
    for tr in t.find_all('tr'):
     cells=tr.find_all(['td','th'],recursive=False);assert len(cells)>=3
     assert not cells[0].get_text(strip=True)and not cells[-1].get_text(strip=True)
     rows.append([value(c)for c in cells[1:-1]])
    grids.append(rows)
   assert list(map(lambda x:[len(x),len(x[0])],grids))==[[2,2],[2,1],[2,1]],(mid,grids)
   assert grids[1]==[['x'],['y']]
   replacement=matrix_equation([grids[0],grids[1],'=',grids[2],'.']);kind='matrix_product';layout=grids
  else:
   assert not nested
   rows=[]
   for i,tr in enumerate(table.find_all('tr')):
    cs=tr.find_all(['td','th'],recursive=False)
    if i==0:
     assert cs[0].get_text(strip=True)=='{'and cs[0].get('rowspan')=='2'
     cs=cs[1:]
    assert len(cs)==3
    row=[value(c)for c in cs];row[2]=re.sub(r'\.$','',row[2]);rows.append(row)
   assert len(rows)==2
   rows[-1][-1]+='.'
   replacement=system_answer(rows);kind='equation_system';layout=rows
  assert not r.errors,(mid,r.errors)
  expected={f[':answer-field/key']:f for f in q[':question/answer-fields']};found=source_fields;assert expected.keys()==found.keys(),(mid,expected.keys(),found.keys())
  mismatches=[]
  for key,f in expected.items():
   a=next(a for a in f[':answer-field/choices']if a[':db/id']==f[':answer-field/correct'][':db/id'])
   if normalize_tex(a[':answer/value']).replace('−','-')!=normalize_tex(found[key]['correct_value']).replace('−','-'):mismatches.append(key)
  if mismatches:
   rejected.append({'source':str(p),'identity':mid,'result':raw.get('result'),'reason':'Observed historical inputs differ from canonical answers. Only observed widget locations are used; submitted values are never copied into the prompt.','fields':mismatches})
  assert collections.Counter(re.findall(r'\{\{([^{}]+)\}\}',replacement))==collections.Counter({k:1 for k in expected})
  candidates.append({'source':str(p),'html':source_html,'replacement':replacement,'kind':kind,'layout':layout,'source_correct_values':{k:f['correct_value']for k,f in found.items()}})
 assert candidates,(mid,'Missing archived source')
 unique={c['replacement']for c in candidates};assert len(unique)==1,(mid,'Source reconstructions disagree')
 c=candidates[0];old=q[':question/problem'];phrase='its representation using matrices is'if c['kind']=='matrix_product'else'The corresponding system of equations is';cut=old.index(phrase)+len(phrase);new=old[:cut]+'\n\n'+c['replacement']
 if q[':db/id']==17592186604616:old=json.loads((H/'preview.json').read_text())['after']
 for validator in[validate_math_boundaries,validate_matrix_layouts,validate_math_structure]:validator(new)
 proposals.append({'entity':q[':db/id'],'attribute':'question/problem','before':old,'after':new,'reason':'Restore source matrix/system cell layout and single live controls; remove flattened or nested layout-table grid artifacts.'});evidence.append({'entity':q[':db/id'],'source_identity':mid,**c,'matching_archived_sources':len(candidates),'field_UUIDs_answers_and_correct_links_unchanged':True})
(H/'rejected-source-probes.json').write_text(json.dumps(rejected,indent=2)+'\n');(H/'lesson-proposals.json').write_text(json.dumps(proposals,indent=2)+'\n');(H/'source-reconstruction.json').write_text(json.dumps(evidence,indent=2)+'\n');print('Prepared',len(proposals),'questions:',dict(collections.Counter(c['kind']for c in evidence)))
