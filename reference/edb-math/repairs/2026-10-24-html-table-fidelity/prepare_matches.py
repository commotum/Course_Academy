"""Rebase source-bound matches on T7027; resolve repeated layouts by full order."""
import collections,json,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[3];A=R/'reference/edb-math/audits/2026-10-24-html-table-fidelity';W=R/'.local/edb/html-table-repair';sys.path.insert(0,str(A));sys.path.insert(0,str(H))
from tables import current_tables,grid_key
from reconstruct import reconstruct
from match_sources import differences

def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def pad(rows):
 w=max(map(len,rows),default=0);return grid_key([r+['']*(w-len(r))for r in rows])
def main():
 matches=json.loads((A/'source-matches.json').read_text());inventory={(r['e'],r['a']):r for r in json.loads((R/'.local/edb/html-table-fidelity/inventory.json').read_text())};sources=json.loads((A/'archive-source-tables.json').read_text());resolved=[]
 for a in json.loads((A/'ambiguous-source-tables.json').read_text()):
  old=inventory[a['entity'],a['attribute']];tables=old['tables'];t=tables[a['table_index']];options=[s for s in sources if s['identity']in a['identities']and s['attribute']==a['attribute']and pad(s['rows'])==pad(t['rows'])]
  groups=collections.defaultdict(list)
  for s in sources:
   if s['identity']in a['identities']and s['attribute']==a['attribute']:groups[s['path'],s.get('dom_id')].append(s)
  proven=[]
  for group in groups.values():
   group.sort(key=lambda s:s['table_index'])
   if len(group)==len(tables)and [pad(s['rows'])for s in group]==[pad(t['rows'])for t in tables]:proven.append(group[a['table_index']])
  assert proven,('No proven ordered source',a)
  def sig(s):return json.dumps([s['table_attrs'],s['cells']],sort_keys=True)
  assert len({sig(s)for s in proven})==1
  s=proven[0];m={'entity':a['entity'],'attribute':a['attribute'],'table_index':a['table_index'],'format':t['format'],'span':[t['start'],t['end']],'current_rows':t['rows'],'source':s,'issues':differences(t,s),'matching':'entire-source-block-exact-grid-sequence'};resolved.append(m)
 matches+=resolved;save(H/'resolved-ambiguous.json',resolved)
 wanted={(m['entity'],m['attribute'])for m in matches};values={};meta=collections.defaultdict(dict);owners=collections.defaultdict(list);idents={}
 for line in (W/'current.jsonl').open():
  d=json.loads(line);k=d['e'],d['a']
  if k in wanted:values[k]=d
  if d['a']=='db/ident':idents[str(d['e'])]=d['v']
  if d['a']in {'answer/type','answer-field/type','answer-field/correct','question/math-academy-id','tutorial/math-academy-id'}:meta[str(d['e'])][d['a']]=d['v']
  if d['a']in {'answer-field/choices','question/answer-fields'}:owners[str(d['v'])].append([d['e'],d['a']])
 save(W/'idents.json',idents);save(W/'metadata.json',meta);save(W/'owners.json',owners);save(W/'values.json',list(values.values()))
 selected=[];rebased=[]
 for m in matches:
  if not m['issues']:continue
  current=values[m['entity'],m['attribute']]['v'];old=inventory[m['entity'],m['attribute']]['v'];table=inventory[m['entity'],m['attribute']]['tables'][m['table_index']]
  if current!=old:
   found=[t for t in current_tables(current)if pad(t['rows'])==pad(m['current_rows'])]
   if len(found)!=1:
    assert current[m['span'][0]:m['span'][1]]==old[m['span'][0]:m['span'][1]],('Concurrent table edit',m['entity'],m['attribute'])
   else:table=found[0];m={**m,'span':[table['start'],table['end']],'current_rows':table['rows']};rebased.append([m['entity'],m['attribute']])
  if m['source']['features']['nested_tables']:
   assert m['format']=='markdown',('Nested existing html requires review',m['entity']);m={**m,**reconstruct(m)}
  else:
   rows=m['current_rows'];assert all(not any(row[len(m['source']['cells'][i]):])for i,row in enumerate(rows));m['prototype_rows']=[row[:len(m['source']['cells'][i])]for i,row in enumerate(rows)]
  assert not BeautifulSoup(m['source']['source_html'],'html.parser').find('caption')
  m['before_table']=current[m['span'][0]:m['span'][1]];selected.append(m)
 save(H/'matches.json',selected);save(H/'match-preparation.json',{'tables':len(selected),'resolved_ambiguous':len(resolved),'rebased_fields':rebased,'fresh_basis':7027});print('Prepared',len(selected),'tables; resolved',len(resolved),'ordered ambiguities; rebased',len(rebased))
if __name__=='__main__':main()
