import sys
sys.dont_write_bytecode=True
from audit import *
old=module(E/'legacy/17592186059770.py')
reference=load(W/'17592186059770/reference/replenishment/basis-2349/generated.json')
inv=load(J/'source/inventory.json');byid={q[':question/id']:q for q in inv['questions']}
records=[];affected=[];tests=[]
for original in reference:
 meta=original['generation'];r=old.generate('moderate',meta['seed'],meta['template']);assert r==original,'reproduced complete legacy record differs'
 q=r['question'];stored=byid[q[':question/id']];f=q[':question/answer-fields'][0];sf=stored[':question/answer-fields'][0]
 assert q[':question/problem']==stored[':question/problem'];assert q[':question/worked-solution']==stored[':question/worked-solution']
 assert f[':answer-field/id']==sf[':answer-field/id']
 assert {a[':answer/id']:a[':answer/value'] for a in f[':answer-field/choices']}=={a[':answer/id']:a[':answer/value'] for a in sf[':answer-field/choices']}
 assert sf[':answer-field/correct'][':answer/id']==f[':answer-field/correct'][1]
 qcheck(r)
 if meta['template']=='coefficient':
  candidates=[a for a in f[':answer-field/choices'] if len(mat(a[':answer/value'])[0])==3 and mat(a[':answer/value'])[0][2]<0]
  defect='Legacy coefficient bank: choose the only 2x3 option with negative top-right entry; no equation reading needed.'
 else:
  candidates=[a for a in f[':answer-field/choices'] if len(mat(a[':answer/value'])[0])==4 and mat(a[':answer/value'])[0][3]==0 and mat(a[':answer/value'])[1][3]<0]
  defect='Legacy augmented bank: choose the 2x4 option with zero first RHS and negative second RHS; no equation reading needed.'
 assert len(candidates)==1;assert candidates[0][':answer/id']==f[':answer-field/correct'][1]
 records.append(r);tests.append({'id':q[':question/id'],'matched_stored_entity':stored[':db/id'],'strategy':defect,'correct':True,'full_metadata_replay':True})
 affected.append({'question_id':q[':question/id'],'entity_id':stored[':db/id'],'finding':defect,'reproduction':f'{PY} {E}/inventory_audit.py ; legacy.generate("moderate", {meta["seed"]}, "{meta["template"]}")','evidence_path':'generated-records.json'})
save('generated-records.json',records);save('affected-inventory.json',{'affected_questions':affected});save('inventory-audit.json',{'basis':inv['basis'],'inventory_count':len(byid),'generated_records_reproduced':tests,'original_source_questions':12,'limits':'All five non-source records are exact legacy replays. Original instructional questions are excluded from generated affected records. No database writes.'})
print(json.dumps({'matched':len(records),'affected':len(affected)}))
