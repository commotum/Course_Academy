"""Bind source layouts to exact current cell content, including collapsed list tables."""
import collections,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[3];A=R/'reference/edb-math/audits/2026-10-24-html-table-fidelity';W=R/'.local/edb/html-table-repair';sys.path.insert(0,str(A));sys.path.insert(0,str(H))
from tables import current_tables,grid_key,key,MATH
from reconstruct import reconstruct,reconstruct_html,model,distribute
from match_sources import differences

def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def pad(rows):
 w=max(map(len,rows),default=0);return grid_key([r+['']*(w-len(r))for r in rows])
def flat(rows):return ''.join(key(c)for row in rows for c in row)
def main():
 sources=json.loads((A/'archive-source-tables.json').read_text());meta=collections.defaultdict(dict);owners=collections.defaultdict(list);idents={};values={}
 allowed={'tutorial/content','question/problem','question/worked-solution','answer/value','answer-field/key'}
 for line in (W/'current.jsonl').open():
  d=json.loads(line)
  if d['a']in allowed:values[d['e'],d['a']]=d
  if d['a']=='db/ident':idents[str(d['e'])]=d['v']
  if d['a']in {'answer/type','answer-field/type','answer-field/correct','question/math-academy-id','tutorial/math-academy-id'}:meta[str(d['e'])][d['a']]=d['v']
  if d['a']in {'answer-field/choices','question/answer-fields'}:owners[str(d['v'])].append([d['e'],d['a']])
 save(W/'idents.json',idents);save(W/'metadata.json',meta);save(W/'owners.json',owners)
 index=collections.defaultdict(list)
 for s in sources:index[s['identity'],s['attribute']].append(s)
 def identities(e,a):
  if a=='tutorial/content':return ['tutorial:'+str(meta[str(e)].get('tutorial/math-academy-id'))]
  if a.startswith('question/'):return [meta[str(e)].get('question/math-academy-id')]
  fs=[e]if a=='answer-field/key'else[p for p,a in owners[str(e)]if a=='answer-field/choices']
  return [meta[str(q)].get('question/math-academy-id')for f in fs for q,a in owners[str(f)]if a=='question/answer-fields']
 matches=[];unresolved=[];selected_values={}
 for (e,a),record in values.items():
  opts=[s for ident in identities(e,a)for s in index.get((ident,a),[])];v=record['v']
  if not opts:continue
  tables=current_tables(v);groups=collections.defaultdict(list)
  for s in opts:groups[pad(s['rows'])].append(s)
  for grid,layouts in groups.items():
   # Repeated source captures with the same identity must agree in layout.
   byblock=collections.defaultdict(list)
   for s in layouts:byblock[s['path'],s.get('dom_id')].append(s)
   blocks=list(byblock.values());layouts=sorted(blocks[0],key=lambda s:s['table_index'])
   layoutsig=lambda s:json.dumps([s['table_attrs'],s['cells']],sort_keys=True)
   if any([layoutsig(x)for x in sorted(b,key=lambda s:s['table_index'])]!=[layoutsig(x)for x in layouts]for b in blocks[1:]):unresolved.append({'entity':e,'attribute':a,'reason':'Conflicting source captures'});continue
   candidates=[{**t,'kind':'table'}for t in tables if pad(t['rows'])==grid]
   pattern=flat(layouts[0]['rows'])
   # Raw list-table flattening removes cell separators. Require a substantial,
   # exact source-bound sequence, outside every extant HTML/Markdown table.
   if len(pattern)>=20 and sum(map(len,layouts[0]['cells']))>=4:
    outside=[];last=0
    for t in sorted(tables,key=lambda t:t['start']):
     if t['start']>=last:outside.append((last,t['start']));last=max(last,t['end'])
    outside.append((last,len(v)))
    for lo,hi in outside:
     chunk=v[lo:hi];norm=key(chunk);hits=[m.start()for m in re.finditer(re.escape(pattern),norm)]
     if not hits:continue
     spans=[(m.start(),m.end())for m in MATH.finditer(chunk)];tags=[(m.start(),m.end())for m in re.finditer('<[^>]*>',chunk)]
     wanted={z for start in hits for z in [start,start+len(pattern)]};boundaries=collections.defaultdict(list)
     for end in range(len(chunk)+1):
      if any(x<end<y for x,y in spans+tags):continue
      prefix=chunk[:end]
      if prefix.count('**')%2:continue
      length=len(key(prefix))
      if length in wanted:boundaries[length].append(end)
     for start in hits:
      begins=boundaries[start];ends=boundaries[start+len(pattern)]
      if not begins or not ends:continue
      left=max(begins);right=min(ends)
      if key(chunk[left:right])==pattern:candidates.append({'start':lo+left,'end':lo+right,'format':'flattened-text','kind':'flattened','text':chunk[left:right]})
   candidates.sort(key=lambda t:t['start'])
   # Identical successive grids with changing shading are bound by occurrence
   # order only when every source occurrence is present in the current field.
   signatures={layoutsig(s)for s in layouts}
   if len(signatures)>1 and len(candidates)!=len(layouts):
    if candidates:unresolved.append({'entity':e,'attribute':a,'reason':'Repeated source layouts require review','source_count':len(layouts),'current_count':len(candidates)})
    continue
   for i,t in enumerate(candidates):
    s=layouts[i]if len(signatures)>1 else layouts[0]
    if t['format']=='flattened-text':
     try:
      spec=model(BeautifulSoup(s['source_html'],'html.parser').find('table'),s);rich=distribute({'table':spec},t['text']);source=rich['table'];rows=rich['rows']
     except ValueError as err:unresolved.append({'entity':e,'attribute':a,'reason':str(err)});continue
     issues=['collapsed-table-in-prose'];m={'source':source,'prototype_rows':rows}
    else:
     issues=differences(t,s)
     if not issues:continue
     m={'source':s,'current_rows':t['rows']}
     if s['features']['nested_tables']:
      if t['format']=='html':m.update(reconstruct_html(s,v[t['start']:t['end']]))
      else:m.update(reconstruct(m))
     else:
      assert all(not any(row[len(s['cells'][j]):])for j,row in enumerate(t['rows']));m['prototype_rows']=[row[:len(s['cells'][j])]for j,row in enumerate(t['rows'])]
    assert not BeautifulSoup(s['source_html'],'html.parser').find('caption')
    matches.append({**m,'entity':e,'attribute':a,'format':t['format'],'span':[t['start'],t['end']],'before_table':v[t['start']:t['end']],'issues':issues,'matching':'source-identity-attribute-exact-current-cells-and-ordered-repeated-layout'});selected_values[e,a]=record
 save(H/'matches-debug.json',matches)
 matches.sort(key=lambda m:(m['entity'],m['attribute'],m['span'][0]));seen={}
 dedup=[]
 for m in sorted(matches,key=lambda m:(m['entity'],m['attribute'],m['span'][0],-m['span'][1])):
  k=m['entity'],m['attribute']
  if seen.get(k,0)>m['span'][0]:
   outer=dedup[-1];assert outer['span'][0]<=m['span'][0]and outer['span'][1]>=m['span'][1],('Partial overlap',k)
   if outer['span']==m['span']:assert outer['prototype_rows']==m['prototype_rows']and outer['source']['table_attrs']==m['source']['table_attrs']
   continue
  seen[k]=m['span'][1];dedup.append(m)
 matches=dedup
 save(W/'values.json',list(selected_values.values()));save(H/'matches.json',matches);save(H/'unresolved.json',unresolved)
 report={'tables':len(matches),'formats':dict(collections.Counter(m['format']for m in matches)),'fields':len(selected_values),'fresh_basis':7027,'unresolved':len(unresolved)};save(H/'match-preparation.json',report);print(report)
if __name__=='__main__':main()
