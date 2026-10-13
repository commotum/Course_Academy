from pathlib import Path
import json
from scripts.database.edn import loads
ROOT=Path(__file__).resolve().parent
rows=json.loads((ROOT/'later-source-candidates.json').read_text()); rows.append({'account':'multivariable','directory':str(ROOT.parents[1]/'capture/multivariable/14120884/repairs/source-candidates-v1')})
if (ROOT/'later-finite-additional-candidates.json').exists():rows.extend(json.loads((ROOT/'later-finite-additional-candidates.json').read_text()))
if (ROOT/'literal-brace-final-apply-candidates.json').exists():rows.extend(json.loads((ROOT/'literal-brace-final-apply-candidates.json').read_text()))
unique={}
for row in rows:
 key=(row['account'],str(Path(row['directory']).parents[1]))
 if key not in unique:unique[key]=row
rows=list(unique.values())
held=set(json.loads(Path('reference/edb-math/imports/math-academy/2026-10-10-held-repairs/repair-plan.json').read_text()))
collisions=[];receipts=[]; errors=[]
for row in rows:
 d=Path(row['directory']).parents[1]; c=json.loads((d/'content.json').read_text())
 ids={q.get('math_academy_id',q.get('id')) for q in c.get('questions',[])+c.get('canonical_examples',[])}
 hit=sorted(ids&held)
 if hit:collisions.append({'account':row['account'],'task_id':d.name,'held_ids':hit})
 for reqp in (d/'database/requests').glob('*/request.json'):
  req=json.loads(reqp.read_text())
  if req.get('basis',0)<980 or not (reqp.parent/'receipt.edn').exists():continue
  try:
   snap=loads(req['snapshot_edn']); ident={}
   def walk(v):
    if isinstance(v,dict):
     if ':db/id' in v and ':db/ident' in v:ident[v[':db/id']]=str(v[':db/ident'])
     for x in v.values():walk(x)
    elif isinstance(v,list):
     for x in v:walk(x)
   walk(snap)
   for eid,name in loads((d/'database'/f'snapshot-{req["basis"]}'/'idents.edn').read_text()):ident[eid]=str(name)
   receipt=loads((reqp.parent/'receipt.edn').read_text())
   rets=[{'entity':x[0],'attribute':ident.get(x[1],x[1]),'source_id':x[4],'source':ident.get(x[4])} for x in receipt.get(':edb/tx-data',[]) if len(x)==6 and x[5] is False]
   nonma=[x for x in rets if x['source']!=':org/Math-Academy']
   receipts.append({'account':row['account'],'task_id':d.name,'request':str(reqp),'pre_existing_additional_archive_receipt':str(reqp) in row.get('pre_repair_requests',[]),'basis_before':req['basis'],'basis_after':receipt.get(':edb/basis-t'),'retractions':len(rets),'non_ma_retractions':nonma,'choice_retractions':[x for x in rets if x['attribute']==':answer-field/choices']})
  except Exception as e:errors.append({'request':str(reqp),'error':str(e)})
result={'held_ids':len(held),'collisions':collisions,'receipts':receipts,'non_ma_retractions':sum(len(x['non_ma_retractions']) for x in receipts),'choice_retractions':sum(len(x['choice_retractions']) for x in receipts),'errors':errors}
(ROOT/'later-attribution-receipt-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='receipts'}))
