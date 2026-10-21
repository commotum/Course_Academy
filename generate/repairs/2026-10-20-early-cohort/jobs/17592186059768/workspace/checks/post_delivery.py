"""Repeat independent probes on actual publisher-filter survivors and slot boundaries."""
import sys
sys.dont_write_bytecode=True
import json,copy,itertools,collections
from finish import *
def slot_coverage(rs):
 out={}
 for name in g.PROFILES:
  group=[r for r in rs if r['generation']['template']==name];m=answer(group[0]);cells={}
  for i,row in enumerate(m):
   for j,_ in enumerate(row):
    vals=[answer(r)[i][j] for r in group];signs=sorted({(v>0)-(v<0) for v in vals});assert -1 in signs and 1 in signs,(name,i,j,signs)
    cells[f'{i},{j}']={'signs':signs,'observed_magnitudes':sorted({abs(v) for v in vals})}
  vo={tuple(r['generation']['variable_order']) for r in group};ro={tuple(r['generation']['row_order']) for r in group}
  assert len(vo)>1 and len(ro)>1
  out[name]={'cells':cells,'variable_orders':sorted(vo),'equation_orders':sorted(ro)}
 return out

def main():
 raw=json.loads((E/'records.json').read_text());accepted=sum([json.loads((E/f'delivery-{d}/accepted.json').read_text()) for d in ('easy','moderate')],[])
 for r in accepted:check(r)
 assert len(raw)==len(accepted)==160
 assert probe(raw)==probe(accepted)
 assert extra_probes(raw)==extra_probes(accepted)
 save('shortcut-after-delivery.json',{'retained_shortcuts':probe(accepted),'surface_probes':extra_probes(accepted),'slot_coverage':slot_coverage(accepted),'input_count':len(raw),'accepted_count':len(accepted),'rejection':'No sampled-instance rejection: five distinct candidates, then choose a previously sampled uniform index; finite candidate-construction failure raises rather than silently excluding a target. All tested instances constructed. Shared filters excluded no tested decision cases.','learner_selection':'Read engine/rust/question_selection.rs lines 132-198: selection changes availability/difficulty weights, never question content. Actual history/reservations and weights absent; no claim about realized learner draw frequencies.'})
 boundaries=[];target_swaps=[]
 for name,src in g.PROFILES.items():
  r=next(r for r in raw if r['generation']['template']==name);level=r['question'][':question/difficulty'].split('/')[-1];m=answer(r);meta=r['generation'];base={'row_order':meta['row_order'],'variable_order':meta['variable_order']}
  i,j=next((i,j) for i,row in enumerate(m) for j,v in enumerate(row) if abs(v)>1)
  for bound in (-24,24):
   changed=copy.deepcopy(m);changed[i][j]=bound
   b=g.generate(level,941713211,profile=name,instance={'matrix':changed,**base});check(b);assert answer(b)[i][j]==bound;boundaries.append(b)
  # Swap the variable roles with the exact signed values and constants held fixed.
  changed=[row[:-1][::-1]+[row[-1]] for row in m];cols=meta['variable_order'][::-1]
  swap=g.generate(level,941713211,profile=name,instance={'matrix':changed,'row_order':meta['row_order'],'variable_order':cols});check(swap);assert answer(swap)!=m
  assert sorted(v for row in answer(swap) for v in row)==sorted(v for row in m for v in row)
  target_swaps.append(swap)
 save('boundary-target-records.json',boundaries+target_swaps)
 cases=[]
 for i,r in enumerate(boundaries+target_swaps):cases.append({'label':'boundary-target-'+str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key(r) else 'rejected','purpose':'Signed bound or changed variable role at fixed other data'} for a in field(r)[':answer-field/choices']]})
 save('boundary-grader-input.json',cases);save('boundary-target-results.json',{'signed_boundaries':len(boundaries),'changed_variable_roles_at_fixed_values':len(target_swaps),'visible_math':'passed','all_other_data_fixed':True})
 # Actual duplicate filtering probe uses a reproduced stored question plus a new duplicate.
 save('duplicate-input.json',[json.loads((E/'generated-records.json').read_text())[0]]+json.loads((E/'batch.json').read_text())[:1]*2)
 print('Post-delivery: all 160 retained; ten profiles pass sign/role coverage and shortcut checks; 20 boundaries and 10 fixed-data variable changes pass.')
if __name__=='__main__':main()
