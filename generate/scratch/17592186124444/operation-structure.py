#!/usr/bin/env python3
"""Check source ordered operation masks; equal CAS rows cannot replace stages."""
import json,re
from pathlib import Path
D=Path(__file__).resolve().parent
originals=json.loads((D/'source.json').read_text())['record'][':knowledge-point/questions'];byid={q[':question/id']:q for q in originals}
counts={'faithful_operation_chains':0,'equal_row_deletion_mutations_rejected':0,'zero_or_explicit_product_mutations_rejected':0}
def blocks(t):return re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',t,re.S)
def signature(b):
 return [(row.count(r'\frac'),row.count(r'\cdot'),row.count(r'\sqrt'),row.count(r'\operatorname'),len(re.findall(r'\+0|0\+',row)),row.count('^')) for row in b.split(r'\\')]
for fixture in json.loads((D/'native-input.json').read_text()):
 r=fixture['record'];m=r['generation']
 if not m['source_ids']:continue
 a=blocks(byid[m['source_ids'][0]][':question/worked-solution']);b=blocks(r['question'][':question/worked-solution'])
 assert list(map(lambda t:len(t.split(r'\\')),a))==list(map(lambda t:len(t.split(r'\\')),b))
 # Point-only numerical arithmetic can vary notation (fractions versus integers),
 # but the full formal-partial block remains the original operation chain.
 paired=zip(a[:1],b[:1]) if m['template'].endswith('_point') else zip(a,b)
 for old,new in paired:
  assert signature(old)==signature(new),(fixture['label'],'operation chain replaced')
  rows=new.split(r'\\');removed=r'\\'.join(rows[:1]+rows[2:]);assert signature(removed)!=signature(old);counts['equal_row_deletion_mutations_rejected']+=1
  for mask in ('+0','0+',r'\cdot'):
   if mask in new:
    changed=new.replace(mask,'' if mask!=r'\cdot' else ' ',1)
    assert len(changed.split(r'\\'))==len(new.split(r'\\'))
    assert signature(changed)!=signature(old);counts['zero_or_explicit_product_mutations_rejected']+=1;break
 counts['faithful_operation_chains']+=1
(D/'operation-structure-report.json').write_text(json.dumps({'status':'pass',**counts},indent=2)+'\n');print(counts)
