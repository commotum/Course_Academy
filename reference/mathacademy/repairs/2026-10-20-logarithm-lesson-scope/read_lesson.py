import runpy,json
from pathlib import Path
R=runpy.run_path('reference/mathacademy/repairs/2026-10-20-log-product-quotient/read.py')
HERE=Path(__file__).resolve().parent
DB=R['DB']; Q=R['QUESTION']; ITEM=R['ITEM']
def save(name,value): (HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False,default=str)+'\n')
if __name__=='__main__':
 identity=DB.status();save('identity.json',identity)
 pattern='[* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '+Q+'} {[:knowledge-point/questions :limit nil] '+Q+'}]'
 rows=DB.query('[:find ?kp (pull ?kp '+pattern+') :in $ [?kp ...] :where [?kp :knowledge-point/id _]]',[[17592186054622,17592186054623,17592186054624,17592186054625]],HERE/'evidence','kps',identity['basis'])
 save('kps.json',rows)
 for eid,kp in rows:
  d=HERE/str(eid);d.mkdir(exist_ok=True)
  (d/'kp.json').write_text(json.dumps(kp,indent=2,ensure_ascii=False,default=str)+'\n')
  qids=[q[':db/id'] for q in kp[':knowledge-point/questions']]
  items=DB.query('[:find ?q (pull ?i '+ITEM+') :in $ [?q ...] :where [?i :task-item/content ?q]]',[qids],d/'evidence','items',identity['basis']);(d/'items.json').write_text(json.dumps(items,indent=2,default=str)+'\n')
  gen=kp.get(':knowledge-point/question-generator')
  if gen and eid!=17592186054624 and not(d/'original').exists(): R['materialize_package'](gen[':question-generator/script'],Path(DB.config.math_root),d/'original')
  print(json.dumps({'kp':eid,'generator':gen,'questions':len(qids),'items':len(items)},default=str))
