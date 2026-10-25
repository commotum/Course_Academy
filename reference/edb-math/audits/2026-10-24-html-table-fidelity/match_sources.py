"""Bind table comparisons to source identity, attribute and exact cell grids."""
import collections,json,re
from tables import H,R,W,grid_key,key

def identities(r,meta,owners):
 if r['a']=='tutorial/content':return ['tutorial:'+str(r['metadata'].get('tutorial/math-academy-id'))]
 if r['a'].startswith('question/'):return [r['metadata'].get('question/math-academy-id')]
 fields=[r['e']]if r['a']=='answer-field/key'else[p for p,a in owners.get(str(r['e']),[])if a=='answer-field/choices']
 return [meta.get(str(q),{}).get('question/math-academy-id')for f in fields for q,a in owners.get(str(f),[])if a=='question/answer-fields']

def differences(table,source):
 issues=[];f=source['features']
 if table['format']=='markdown':
  if not any(c['tag']=='th'for c in source['cells'][0]):issues.append('invented-header-row')
  ta=source['table_attrs'];style=str(ta.get('style','')).lower()
  positioning=ta.get('align')in ['center','right']or bool(re.search(r'margin(?:-left|-right)?\s*:\s*auto',style))
  column_align=[('center'if c.startswith(':')and c.endswith(':')else'right'if c.endswith(':')else'left')for c in table.get('alignment',[])]
  cell_alignment=False
  for i,row in enumerate(source['cells']):
   for j,c in enumerate(row):
    a=c['attrs'];match=re.search(r'text-align\s*:\s*(left|center|right)',a.get('style',''),re.I);expected=a.get('align')or(match[1].lower()if match else None)
    if expected and j<len(column_align):
     authored=column_align[j]if table['alignment'][j].startswith(':')or table['alignment'][j].endswith(':')else'center'if i==0 else'left'
     cell_alignment|=expected!=authored
  if positioning or cell_alignment:issues.append('lost-source-alignment')
  if f['shading']:issues.append('lost-source-shading')
  if f['merged_cells']:issues.append('lost-cell-spans')
  if f['nested_tables']:issues.append('flattened-nested-table')
 else:
  # HTML can retain source attributes yet still be overridden by generic UI CSS.
  if f['alignment']:issues.append('source-alignment-needs-scoped-rendering')
  if f['shading']:issues.append('source-shading-needs-theme-and-contrast-review')
 return issues

def main():
 sources=json.loads((H/'archive-source-tables.json').read_text());fields=json.loads((W/'inventory.json').read_text());meta=json.loads((W/'metadata.json').read_text());owners=json.loads((W/'owners.json').read_text());index=collections.defaultdict(list)
 def padded(rows):
  width=max(map(len,rows),default=0);return grid_key([r+['']*(width-len(r))for r in rows])
 for source in sources:index[source['identity'],source['attribute'],padded(source['rows'])].append(source)
 matched=[];unmatched=[];ambiguous=[]
 for r in fields:
  ids=identities(r,meta,owners)
  for number,t in enumerate(r['tables']):
   options=[s for identity in ids for s in index.get((identity,r['a'],padded(t['rows'])),[])]
   if not options:
    unmatched.append({'entity':r['e'],'attribute':r['a'],'table_index':number,'identities':ids,'format':t['format'],'rows':t['rows']});continue
   def signature(s):return json.dumps({'table':s['table_attrs'],'cells':[[[c['tag'],c['attrs']]for c in row]for row in s['cells']]},sort_keys=True)
   if len({signature(s)for s in options})>1:
    ambiguous.append({'entity':r['e'],'attribute':r['a'],'table_index':number,'identities':ids,'source_paths':[s['path']for s in options]});continue
   source=options[0];issues=differences(t,source)
   matched.append({'entity':r['e'],'attribute':r['a'],'table_index':number,'format':t['format'],'span':[t['start'],t['end']],'current_rows':t['rows'],'source':source,'issues':issues,'matching':'exact-cell-grid'if grid_key(t['rows'])==grid_key(source['rows'])else'exact-physical-cells-with-empty-padding'})
 (H/'source-matches.json').write_text(json.dumps(matched,indent=2)+'\n');(H/'unmatched-tables.json').write_text(json.dumps(unmatched,indent=2)+'\n');(H/'ambiguous-source-tables.json').write_text(json.dumps(ambiguous,indent=2)+'\n')
 confirmed=[r for r in matched if r['format']=='markdown'and r['issues']];report={'matched_table_occurrences':len(matched),'source_confirmed_markdown_table_fidelity_issues':len(confirmed),'affected_fields':len({(r['entity'],r['attribute'])for r in confirmed}),'affected_entities':len({r['entity']for r in confirmed}),'affected_source_topics':len({r['source'].get('topic')for r in confirmed}),'issue_counts':dict(collections.Counter(i for r in confirmed for i in r['issues'])),'matched_existing_html_tables':sum(r['format']=='html'for r in matched),'ambiguous_source_layouts':len(ambiguous),'unmatched_table_occurrences':len(unmatched)}
 (H/'match-summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
