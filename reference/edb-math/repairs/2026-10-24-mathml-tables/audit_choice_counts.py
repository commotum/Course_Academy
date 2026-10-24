import json,collections
from pathlib import Path
from source_tables import H,R
W=R/'.local/edb/mathml-tables-work';owners=json.loads((W/'owners.json').read_text());meta=json.loads((W/'metadata.json').read_text());mids={r['identity'] for r in json.loads((H/'choice-tables.json').read_text())};byid={r['question/math-academy-id']:int(e) for e,r in meta.items() if 'question/math-academy-id'in r};qfields=collections.defaultdict(list);choices=collections.Counter()
for child,refs in owners.items():
 for parent,attr in refs:
  if attr=='question/answer-fields':qfields[parent].append(int(child))
  if attr=='answer-field/choices':choices[parent]+=1
cache={};mismatches=[];checked=set()
for r in json.loads((H/'choice-tables.json').read_text()):
 mid=r['identity'];p=Path(r['path']);p=p if p.is_absolute() else R/p
 if p.name!='state.json' or mid in checked:continue
 if str(p)not in cache:cache[str(p)]=json.loads(p.read_text())
 record=cache[str(p)].get('questions',{}).get(mid,{});before=record.get('before',{});fields=before.get('fields',[]);current=qfields.get(byid[mid],[])
 if len(fields)!=1 or len(current)!=1:continue
 checked.add(mid);expected=len(fields[0].get('choices',[]));actual=choices[current[0]]
 if expected!=actual:mismatches.append({'question':mid,'field':current[0],'source_choices':expected,'current_choices':actual,'source':str(p)})
(H/'choice-count-audit.json').write_text(json.dumps({'questions_checked':len(checked),'mismatches':mismatches},indent=2)+'\n');print('choice counts checked',len(checked),'mismatches',mismatches)
