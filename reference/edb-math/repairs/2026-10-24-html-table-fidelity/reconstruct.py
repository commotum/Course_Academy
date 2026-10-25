"""Recover nested table structure using only existing cell text as leaf values."""
import json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[3];A=R/'reference/edb-math/audits/2026-10-24-html-table-fidelity';sys.path.insert(0,str(A))
from tables import key,MATH,source_table,source_cell

def model(table,source):
 result=source_table(table,source['identity'],source['attribute'],source['path']);result['row_sections']=[];result['row_attrs']=[];rows=[]
 for tr in table.find_all('tr'):
  if tr.find_parent('table')is not table:continue
  result['row_sections'].append(tr.parent.name if tr.parent.name in ['thead','tbody','tfoot']else'tbody');result['row_attrs'].append(dict(tr.attrs));row=[]
  for cell in tr.find_all(['td','th'],recursive=False):
   if not cell.find('table'):row.append({'leaf':source_cell(cell)});continue
   parts=[];pending=[]
   def flush():
    if not pending:return
    text=source_cell(BeautifulSoup('<td>'+''.join(pending)+'</td>','html.parser').find('td'));pending.clear()
    if key(text):parts.append({'leaf':text})
   def walk(n):
    if getattr(n,'name',None)=='table':flush();parts.append({'table':model(n,source)});return
    if hasattr(n,'children')and n.find('table'):
     for child in n.children:walk(child)
    else:pending.append(str(n))
   for child in cell.children:walk(child)
   flush();row.append({'parts':parts})
  rows.append(row)
 result['model_rows']=rows;return result

def leaves(value):
 if'leaf'in value:return [value]
 if'table'in value:return [leaf for row in value['table']['model_rows']for cell in row for leaf in leaves(cell)]
 return [leaf for part in value['parts']for leaf in leaves(part)]

def distribute(value,current):
 wanted=leaves(value);expected=''.join(key(v['leaf'])for v in wanted);actual=key(current)
 if actual!=expected:raise ValueError('Leaf text does not exactly match flattened current cell')
 spans=[(m.start(),m.end())for m in MATH.finditer(current)];tags=[(m.start(),m.end())for m in re.finditer(r'<[^>]*>',current)];boundaries={0:0}
 for end in range(1,len(current)+1):
  if any(a<end<b for a,b in spans+tags):continue
  prefix=current[:end]
  if prefix.count('**')%2:continue
  normalized=key(prefix)
  if actual.startswith(normalized):boundaries[len(normalized)]=end
 offset=0;last=0
 for i,leaf in enumerate(wanted):
  offset+=len(key(leaf['leaf']));end=len(current)if i==len(wanted)-1 else boundaries.get(offset)
  if end is None or end<last:raise ValueError('Cannot prove a stable current-text boundary')
  leaf['current']=current[last:end];last=end
 assert ''.join(leaf['current']for leaf in wanted)==current
 def render(v):
  if'leaf'in v:return v['current']
  if'table'in v:
   s=v['table'];return {'table':{k:x for k,x in s.items()if k!='model_rows'},'rows':[[render(c)for c in row]for row in s['model_rows']]}
  return {'parts':[render(p)for p in v['parts']]}
 return render(value)

def reconstruct(match):
 source=match['source'];soup=BeautifulSoup(source['source_html'],'html.parser');spec=model(soup.find('table'),source);values=[]
 assert len(spec['model_rows'])==len(match['current_rows'])
 for i,row in enumerate(spec['model_rows']):
  current=match['current_rows'][i];assert all(not x for x in current[len(row):]);values.append([distribute(cell,current[j])for j,cell in enumerate(row)])
 return {'source':{k:v for k,v in spec.items()if k!='model_rows'},'prototype_rows':values}

if __name__=='__main__':
 matches=json.loads((A/'source-matches.json').read_text());out=[];unresolved=[]
 for m in matches:
  if m['format']!='markdown'or not m['issues']or not m['source']['features']['nested_tables']:continue
  try:rebuilt=reconstruct(m);out.append({**m,**rebuilt,'all_current_leaf_bytes_preserved':True})
  except(Exception)as e:unresolved.append({**m,'reason':str(e)})
 (H/'nested-reconstructions.json').write_text(json.dumps(out,indent=2)+'\n');(H/'nested-unresolved.json').write_text(json.dumps(unresolved,indent=2)+'\n');print('Nested reconstructed',len(out),'unresolved',len(unresolved))

def reconstruct_html(source,current):
 """Bind nested current HTML cells recursively, keeping all current leaf markup."""
 def build(s,c):
  spec=source_table(s,source['identity'],source['attribute'],source['path']);sr=[r for r in s.find_all('tr')if r.find_parent('table')is s];cr=[r for r in c.find_all('tr')if r.find_parent('table')is c];assert len(sr)==len(cr);values=[]
  for rs,rc in zip(sr,cr):
   sc=rs.find_all(['td','th'],recursive=False);cc=rc.find_all(['td','th'],recursive=False);assert len(sc)==len(cc);row=[]
   for a,b in zip(sc,cc):
    assert key(source_cell(a))==key(str(b.decode_contents()))
    an=[t for t in a.find_all('table')if t.find_parent('table')is s];bn=[t for t in b.find_all('table')if t.find_parent('table')is c];assert len(an)==len(bn)
    if not an:row.append(str(b.decode_contents()));continue
    parts=[];markup=str(b.decode_contents())
    for x,y in zip(an,bn):
     before,sep,markup=markup.partition(str(y));assert sep;parts.append(before);child=build(x,y);parts.append({'table':child['source'],'rows':child['prototype_rows']})
    parts.append(markup);row.append({'parts':parts})
   values.append(row)
  return {'source':spec,'prototype_rows':values}
 return build(BeautifulSoup(source['source_html'],'html.parser').find('table'),BeautifulSoup(current,'html.parser').find('table'))
