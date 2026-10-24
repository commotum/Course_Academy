"""Compare complete captured choice banks to current ownership, without writes."""
import collections,json
from pathlib import Path
from bs4 import BeautifulSoup
from source_tables import H,R,slim_dom
W=R/'.local/edb/mathml-tables-work'
owners=json.loads((W/'owners.json').read_text());meta=json.loads((W/'metadata.json').read_text())
qids={r['question/math-academy-id']:int(e) for e,r in meta.items() if 'question/math-academy-id' in r}
fields=collections.defaultdict(list);choices=collections.Counter()
for child,refs in owners.items():
 for parent,attr in refs:
  if attr=='question/answer-fields':fields[parent].append(int(child))
  elif attr=='answer-field/choices':choices[parent]+=1
sources=collections.defaultdict(set)
for r in json.loads((H/'new-capture-tables.json').read_text()):
 if r['attribute']=='answer/value':sources[r['identity']].add(r['path'])
checked=[];mismatches=[]
for mid,paths in sources.items():
 if len(fields[qids[mid]])!=1:continue
 field=fields[qids[mid]][0];counts=[]
 for path in paths:
  soup=BeautifulSoup(slim_dom((R/path).read_text()),'html.parser')
  soup=soup.find(id='step-q'+mid[2:]) or soup.find(id='question-'+mid[2:]) or soup
  parts=soup.find_all(class_=['questionWidget-choiceText','choiceText','selectListOption'])
  counts.append({'source':path,'choices':len(parts)})
 assert len({r['choices'] for r in counts})==1,(mid,counts)
 row={'question':mid,'field':field,'current_choices':choices[field],'source_choices':counts[0]['choices'],'sources':counts}
 checked.append(row)
 if choices[field]!=row['source_choices']:mismatches.append(row)
report={'questions_checked':len(checked),'mismatches':mismatches,'checks':checked}
(H/'new-choice-count-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print('New source choice banks:',len(checked),'mismatches:',json.dumps(mismatches))
