"""Bounded per-slot profile applicability and independent rendered edge QA."""
import sys
sys.dont_write_bytecode=True
import json
from pathlib import Path
H=Path(__file__).parent;ns={'__file__':str(H/'validate.py')};exec((H/'validate.py').read_text().split('source=[]')[0],ns);G=ns['G'];check=ns['check'];out={};checked=0
for sid,cfg in G.CONFIG.items():
 bounds={'k':[2,3,5,6,7,10,11]if cfg[1]=='radical'else list(range(1,13)),'a':list(range(2,7))if cfg[3]!=1 else[1],'n':[2,3,4]if cfg[4]!=1 else[1],'p_num':[1,2,3]if cfg[0]=='easy'else[G.original(sid)['p_num']],'p_den':[G.original(sid)['p_den']]};slots={}
 for slot,domain in bounds.items():
  valid=[];invalid=[];rows=[]
  for value in domain:
   params=G.original(sid);params[slot]=value
   try:r=G.generate(cfg[0],template=sid,parameters=params)
   except ValueError as e:invalid.append({'value':value,'reason':str(e)})
   else:valid.append(value);rows.append(r)
  for r in(rows[:1]+rows[-1:]if len(rows)>1 else rows):check(r);checked+=1
  slots[slot]={'declared_values':domain,'valid_holding_other_slots_original':valid,'ineligible_whole_profile_instances':invalid,'rendered_boundary_values':valid[:1]+valid[-1:]if len(valid)>1 else valid}
 out[sid]=slots
(H/'boundary-checks.json').write_text(json.dumps({'profiles':out,'independent_rendered_boundary_records':checked},indent=2)+'\n');print(checked)
