"""Validate refreshed evidence independently without changing captured content."""
import importlib.util,json,re
from pathlib import Path
P=Path(__file__).parent
sp=importlib.util.spec_from_file_location('replenishment',P/'replenish.py');r=importlib.util.module_from_spec(sp);sp.loader.exec_module(r)
v=r.v;s=r.s
kp=r.loads((P/'reference/initial/kp-record.edn').read_text())
rows=[]
for q in kp[':knowledge-point/questions']:
 sid=q[':db/id'];row={'source_id':sid,'bank_values':len(q[':question/answer-fields'][0][':answer-field/choices'])}
 if sid==17592186235525:
  row.update(status='context-limited',reason='Prompt refers to div V and prior parts without supplying V or its gradient. Excluded from independent fresh inventory; standalone authored completion supplies gradient.')
 elif sid==17592186125029:
  F,E,A,B,dx,dy,N,C=r.displayed(q);f=q[':question/answer-fields'][0]
  assert sum(v.equal(v.math(a[':answer/value']),C) for a in f[':answer-field/choices'])==1
  assert ':answer-field/correct' not in f and ':question/difficulty' not in q and ':question/worked-solution' not in q
  row.update(status='incomplete',answer=str(C),reason='Correct reference, difficulty and solution absent; source preserved.')
 else:
  C=r.validate_bank(q)
  blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)
  last=blocks[-1];final=last.split(r'\\')[-1].split('& =',1)[1];assert v.equal(v.math(final),C),(sid,final,C)
  if sid in (17592186446241,17592186446242,17592186518124):
   F,E,A,B,dx,dy,N,C=r.displayed(q)
   gradient=v.vectors(blocks[1].split(r'\\')[-1])[0]
   assert all(v.equal(a,b) for a,b in zip(gradient,E))
   direction=v.vectors(blocks[0]);assert all(v.equal(a-b,c) for a,b,c in zip(direction[0],direction[1],[dx,dy]))
   dot=v.vectors(last.split(r'\\')[1]);assert all(v.equal(a,b) for a,b in zip(dot[0],E)) and all(v.equal(a,b) for a,b in zip(dot[1],[dx/N,dy/N]))
   for stage in last.split(r'\\')[2:]:assert v.equal(v.math(stage.split('& =',1)[1]),C)
  row.update(status='validated',answer=str(C),level=str(q[':question/difficulty'][':db/ident']).split('/')[-1],final_solution_checked=True)
 rows.append(row)
r.save(P/'reference/initial/current-source-validation.json',{'passed':True,'basis':2640,'lineage':r.LINEAGE,'source_questions':len(rows),'source_values_accounted':sum(z['bank_values'] for z in rows),'questions':rows,'new_source_families_not_sampled':['square_x2_y','radius','square_difference'],'hard_classification_superseded':True})
print(json.dumps(rows,indent=2))
