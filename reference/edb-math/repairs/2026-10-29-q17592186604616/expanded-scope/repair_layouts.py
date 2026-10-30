"""Recover source inverse answer grids, including external scalar-prefactor blanks."""
import collections,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;P=H.parent;R=H.parents[4];sys.path[:0]=[str(P),str(R/'scripts'),str(R/'reference/edb-math/repairs/2026-10-26-mixed-math-titles')]
from reconstruct import SourceRenderer
from question_capture.math_format import MATH,matrix_equation,validate_math_boundaries,validate_matrix_layouts,validate_math_structure
from math_checks import scalar,matrices,filled,fill
import sympy as sp
S=json.loads((H/'current.json').read_text());targets={q[':question/math-academy-id']:q for q in S['questions']if '<table'in q[':question/problem']or re.search(r'(?m)^\|',q[':question/problem'])};paths=collections.defaultdict(list)
for line in(R/'.local/edb/mathml-tables-work/source-paths.txt').read_text().splitlines():
 p=Path(line);m=re.search(r'(q-\d+)-(?:before|after)\.json$|history-(q-\d+)(?:-[a-f0-9]+)?\.json$',p.name)
 if m and(m[1]or m[2])in targets and p.exists():paths[m[1]or m[2]].append(p)
proposals=[];evidence=[]
for mid,q in sorted(targets.items()):
 options=[]
 for p in paths[mid]:
  raw=json.loads(p.read_text());html=raw.get('html')or raw.get('raw_html')
  if not html:continue
  soup=BeautifulSoup(html,'html.parser');node=soup.select_one('.questionText,.questionWidget-text')
  if node is None:continue
  ts=node.find_all('table');assert len(ts)==1,(mid,len(ts))
  table=ts[0];source_html=str(table);r=SourceRenderer(None);keys=[]
  for f in raw.get('fields',[]):
   if f.get('type')!='blank':continue
   control=table.find(id=f.get('dom_id'))
   if control is not None:control.replace_with('{{'+f['key']+'}}');keys.append(f['key'])
  if len(keys)!=len(q[':question/answer-fields']):continue
  def value(n):
   text=r.text(n).strip()
   return MATH.sub(lambda m:m[0][2:-2]if m[0].startswith(('$$',r'\(',r'\['))else m[0][1:-1],text).strip()
  rows=table.find_all('tr');grid=[];labels=[];spanning=rows[0].find(['td','th']).get('rowspan')==str(len(rows))
  for i,row in enumerate(rows):
   cs=row.find_all(['td','th'],recursive=False)
   if not spanning or i==0:
    label_value=value(cs.pop(0))
    if label_value:labels.append(label_value)
   assert not cs[0].get_text(strip=True)and not cs[-1].get_text(strip=True)
   entries=[value(c)for c in cs[1:-1]]
   if any(entries):
    assert all(entries),(mid,entries)
    grid.append(entries)
  assert len(labels)==1,(mid,labels)
  label=labels[0]
  assert not r.errors,(mid,r.errors)
  assert len(grid)in[2,3]and all(len(row)==len(grid)for row in grid)
  rendered=matrix_equation([label,grid]);assert collections.Counter(re.findall(r'\{\{([^{}]+)\}\}',rendered))==collections.Counter({f[':answer-field/key']:1 for f in q[':question/answer-fields']})
  options.append({'path':str(p),'html':source_html,'label':label,'grid':grid,'rendered':rendered})
 assert options,(mid,'No complete source layout');assert len({o['rendered']for o in options})==1,(mid,'Conflicting source layouts');o=options[0]
 old=q[':question/problem'];cut=re.search(r'(?m)^\|',old)
 if cut:prefix=old[:cut.start()].rstrip()
 else:prefix=old[:old.index('<table')].rstrip()
 new=prefix+'\n\n'+o['rendered']
 for fn in[validate_math_boundaries,validate_matrix_layouts,validate_math_structure]:fn(new)
 bank=filled(q);a=matrices(prefix)[0]['matrix'];g=sp.Matrix([[scalar(fill(c,bank))for c in row]for row in o['grid']]);factor=fill(o['label'].split('=')[-1],bank).strip();factor=re.sub(r'\\hspace\{[^{}]*\}|\\[,;! ]','',factor).strip();factor=scalar(factor)if factor else sp.Integer(1);actual=factor*g
 assert a*actual==sp.eye(a.rows)and actual*a==sp.eye(a.rows),(mid,a,actual,'Restored values fail inverse identity')
 proposals.append({'entity':q[':db/id'],'attribute':'question/problem','before':old,'after':new,'reason':'Restore the archived bracketed inverse answer grid and external prefactor at their exact source positions; preserve all controls and answers.'});evidence.append({'entity':q[':db/id'],'identity':mid,**o,'matching_source_layouts':len(options),'both_inverse_products_verified':True,'field_to_cell_mapping_verified':True})
(H/'layout-proposals.json').write_text(json.dumps(proposals,indent=2)+'\n');(H/'layout-source-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');print('Prepared and independently verified',len(proposals),'inverse matrix answer layouts')
