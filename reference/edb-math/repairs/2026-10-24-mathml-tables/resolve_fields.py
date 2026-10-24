"""Resolve layouts by source identity, field and repeated-table occurrence order."""
import collections,json,re
from pathlib import Path
from bs4 import BeautifulSoup
from source_tables import H,R,LegacyRenderer
from enrich_bound import get_doc
from enrich_sources import fences
from layout import grid_key,mathml_ruled_table,key_cell
W=R/'.local/edb/mathml-tables-work'

def layout_signature(rows,attrs):
 try:
  tex=mathml_ruled_table([['V'+str(j) for j in range(len(row))] for row in rows],attrs)
 except ValueError:return 'unsupported'
 return tex

def clean_rows(rows):
 out=[list(r) for r in rows]
 for row in out:
  if row:row[0]=re.sub(r'^\s*\\hline\s*','',row[0])
 if out and all(not c.strip() for c in out[-1]) and any(r'\hline' in c for c in rows[-1]):out.pop()
 return out

def context_records(source):
 out=[]
 for doc in get_doc(source):
  if source['attribute']=='answer/value':
   doc_parts=[doc]
  else:doc_parts=[doc]
  occurrences=[];seen=set()
  for part in doc_parts:
   for table in part.find_all('mtable'):
    # A capture may retain parallel MathML trees under one MathJax wrapper.
    math=table.find_parent('math');outer=table.find_parent(['mjx-container'])
    if outer and math is not outer.find('math'):continue
    old=LegacyRenderer(None);rows=[[old.m(c) for c in tr.find_all('mtd',recursive=False)] for tr in table.find_all('mtr',recursive=False)]
    if not rows:continue
    occurrences.append({'identity':source['identity'],'attribute':source['attribute'],'path':source['path'],'source_attributes':dict(table.attrs),'rows':rows,'source_fences':fences(table),'source_mathml':str(table),'errors':old.errors})
  if occurrences:out.append(occurrences)
 return out

def main():
 sources=sum([json.loads((H/f).read_text()) for f in ['archived-tables.json','capture-tables.json','choice-tables.json','new-capture-tables.json']],[])
 registry=collections.defaultdict(dict)
 for s in sources:
  registry[s['identity'],s['attribute']][s['path'],s.get('step_id'),s.get('option_dom_id')]=s
 fields=json.loads((W/'inventory-all.json').read_text());answer_owners=json.loads((W/'answer-question-identities.json').read_text());resolved=[];unresolved=[];retained=[];context_cache={}
 for number,r in enumerate(fields):
  identity='tutorial:'+str(r['metadata']['tutorial/math-academy-id']) if 'tutorial/math-academy-id' in r['metadata'] else r['metadata'].get('question/math-academy-id')
  identities=answer_owners.get(str(r['e']),[]) if r['a']=='answer/value' else [identity]
  possible=[s for ident in identities for s in registry.get((ident,r['a']),{}).values()]
  if not possible:continue
  current=collections.defaultdict(list)
  for span in r['spans']:current[grid_key(span['rows'])].append(span)
  options=collections.defaultdict(list)
  for source in possible:
   ck=(source['identity'],source['attribute'],source['path'],source.get('step_id'),source.get('option_dom_id'))
   if ck not in context_cache:context_cache[ck]=context_records(source)
   for sequence in context_cache[ck]:
    grouped=collections.defaultdict(list)
    for s in sequence:grouped[grid_key(s['rows'])].append(s)
    for key,spans in current.items():
     if key not in grouped:continue
     source_spans=grouped[key];kinds=[layout_signature(s['rows'],s['source_attributes']) for s in source_spans]
     # Ordered pairing preserves the difference between a plain matrix and
     # repeated copies partitioned in several different ways in one solution.
     if len(spans)==len(source_spans):pairs=list(zip(spans,source_spans));confidence=2
     elif len(set(kinds))==1 and len({tuple(s['source_fences']) for s in source_spans})==1:pairs=[(span,source_spans[0]) for span in spans];confidence=1
     else:continue
     for span,s in pairs:
      strict=lambda rows:tuple(tuple(key_cell(c.replace(r'\,','CASPACEPOS').replace(r'\!','CASPACENEG')) for c in row) for row in rows)
      score=confidence+(10 if strict(span['rows'])==strict(s['rows']) else 0)
      options[span['start'],span['end']].append((score,s))
  for span in r['spans']:
   possible_options=options.get((span['start'],span['end']),[])
   if not possible_options:continue
   best=max(c for c,s in possible_options);choices=[s for c,s in possible_options if c==best]
   # Prefer complete archive sections to incidental history fragments when
   # equally strong matches disagree; exact repeated occurrences remain bound.
   kinds={(layout_signature(s['rows'],s['source_attributes']),tuple(s['source_fences'])) for s in choices}
   if len(kinds)>1:
    archives=[s for s in choices if '/MA/DATA/Lessons/' in s['path']]
    archive_kinds={(layout_signature(s['rows'],s['source_attributes']),tuple(s['source_fences'])) for s in archives}
    if len(archive_kinds)==1:choices=archives;kinds=archive_kinds
   if len(kinds)>1:unresolved.append({'e':r['e'],'a':r['a'],'span':span,'options':choices});continue
   s=choices[0];new=mathml_ruled_table(clean_rows(span['rows']),s['source_attributes'])
   if new is None:retained.append({'e':r['e'],'a':r['a'],'span':span,'reason':'source-table-is-unruled'});continue
   if span['env'] in ['bmatrix','pmatrix','Bmatrix','vmatrix','Vmatrix']:
    f=s['source_fences']
    if f:new=r'\left'+f[0]+new+r'\right'+f[1]
   if re.sub(r'\s+','',new)==re.sub(r'\s+','',span['tex']):retained.append({'e':r['e'],'a':r['a'],'span':span,'reason':'source-rules-already-preserved'});continue
   resolved.append({'e':r['e'],'a':r['a'],'span':span,'source':s,'new_tex':new,'confidence':'ordered-source-occurrence' if best%10==2 else 'uniform-source-layout'})
  if number%4000==0:print('Fields',number,'resolved',len(resolved),flush=True)
 (H/'resolved-layouts.json').write_text(json.dumps(resolved,indent=2)+'\n');(H/'unresolved-layouts.json').write_text(json.dumps(unresolved,indent=2)+'\n');(H/'retained-layouts.json').write_text(json.dumps(retained,indent=2)+'\n');print('Resolved',len(resolved),'fields',len({(r['e'],r['a']) for r in resolved}),'retained',len(retained),'unresolved',len(unresolved),'contexts',len(context_cache));print('attrs',dict(collections.Counter(r['a'] for r in resolved)))
if __name__=='__main__':main()
