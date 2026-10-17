"""Source-confirmed, layout-only replacements; retain exact math and row identity."""
import json,re,sys
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import MATH,legacy_system_rows,system_tex,cells,environment
AUDIT=ROOT/'reference/mathacademy/audits/2026-10-16-system-equations-display'
findings=json.loads((AUDIT/'wide-mth341/findings.json').read_text())
snapshot=json.loads((HERE/'snapshot.json').read_text())
entities={e[':db/id']:e for group in ('questions','tutorials') for [e] in snapshot[group]}
changes=[];checks=[]
compact=lambda s:re.sub(r'\s+','',s)
counts=Counter()
for f in findings:
 before=f['value'];assert entities[f['entity']][f['attribute']]==before
 def replace(match):
  value=match[0];delim=2 if value.startswith(('$$',r'\[',r'\(')) else 1
  tex=value[delim:-delim].strip();original=tex
  # Source DOM has one operation bar; the old extractor emitted it twice.
  tex,n=re.subn(r'\\mid\s*\\mid(?=\s*\\cdot)',lambda _:r'\mid',tex)
  counts['duplicate_operation_bars']+=n
  rows=legacy_system_rows(tex)
  if rows:
   equations=[];annotations=[]
   for index,row in enumerate(rows):
    annotation=''
    if 17592186073753 in f['knowledge_points'] and f['attribute']==':question/worked-solution':
     label='('+str(index+1)+')';assert row.endswith(label),(f['entity'],row)
     row=row[:-len(label)].rstrip();annotation=label
     counts['equation_labels']+=1
    if r'\mid' in row:
     assert not annotation
     row,operation=row.split(r'\mid',1);annotation=r'\mid'+operation;row=row.rstrip()
     assert r'\mid' not in operation
    equations.append(row);annotations.append(annotation)
   tex=system_tex(equations,annotations=annotations)
   # Recover cells from the actual serialized result; math and annotations
   # must remain identical and in the same row after layout normalization.
   start=tex.index(r'\begin{aligned}');span=environment(tex,start)
   parsed=cells(tex[span[0]:span[1]])
   for i,row in enumerate(parsed):
    if row[0]=='':recovered=row[1];ann=row[3] if len(row)>3 else ''
    else:recovered=''.join(row[:2]);ann=row[3] if len(row)>3 else ''
    assert compact(recovered)==compact(equations[i]),(f['entity'],recovered,equations[i])
    assert compact(ann)==compact(annotations[i]),(f['entity'],ann,annotations[i])
   counts['flat_systems']+=1
   checks.append({'entity':f['entity'],'attribute':f['attribute'],'rows':len(rows),'math_and_annotation_tokens_preserved':True,'equations':equations,'annotations':annotations})
   # All captured standalone systems were display math in source material.
   line_before=before[:match.start()].rsplit('\n',1)[-1]
   line_after=before[match.end():].split('\n',1)[0]
   if delim==1 and not line_before.strip() and not line_after.strip():
    counts['standalone_inline_to_display']+=1
    return '$$\n'+tex+'\n$$'
  if tex==original:return value
  return value[:delim]+'\n'+tex+'\n'+value[-delim:] if delim==2 else value[:delim]+tex+value[-delim:]
 after=MATH.sub(replace,before)
 assert after!=before,(f['entity'],f['attribute'])
 assert not any(legacy_system_rows(m[0][2:-2] if m[0].startswith('$$') else m[0][1:-1]) for m in MATH.finditer(after))
 assert not re.search(r'\\mid\s*\\mid',after)
 # All text outside math is exactly unchanged (display delimiters are math).
 assert MATH.sub('<MATH>',before)==MATH.sub('<MATH>',after)
 changes.append({k:f[k] for k in ('entity','attribute','topic','topic_title','knowledge_points')}|{'before':before,'after':after,'reason':'Restore source system rows, separate source-confirmed equation labels and row operations, and remove duplicated operation bars.'})
for c in json.loads((HERE/'tutorials/changes.json').read_text()):
 assert entities[c['entity']][c['attribute']]==c['before'];changes.append(c)
assert len(changes)==177 and counts['flat_systems']==160 and counts['duplicate_operation_bars']==30 and counts['equation_labels']==22,counts
(HERE/'changes.json').write_text(json.dumps(changes,indent=2)+'\n')
(HERE/'math-preservation.json').write_text(json.dumps({'passed':True,'counts':dict(counts),'fields':177,'questions':108,'tutorials':2,'checks':checks},indent=2)+'\n')
print(json.dumps(dict(counts)))
