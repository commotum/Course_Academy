import copy,importlib.util,json,shutil,subprocess,sys,os
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from scripts.generator_publish import stable_identities,normalized_question
from scripts.rounded_finance_batch_policy import validate_delivery_batch
summary=[]
for row in json.loads((H/'capture.json').read_text())['knowledge_points']:
 kp=row['kp'];d=H/str(kp);local=ROOT/f'generate/scratch/{kp}';target=d/'package'
 for name in [*row['files'],'rounded_finance.py']:shutil.copy2(local/name,target/name)
 fresh=json.loads(subprocess.check_output([sys.executable,str(target/'generator.py'),'--count','5','--seed','20261026','--difficulty','moderate'],text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}))
 k=json.loads((d/'before.json').read_text());old=[q for q in k[':knowledge-point/questions']if not q.get(':question/math-academy-id')and not q.get(':question/retired')];assert len(old)==5
 pool=fresh
 if kp==17592186059798:
  pool=[]
  for q in old:
   normalized=normalized_question(q)
   for f in normalized[':question/answer-fields']:f[':answer-field/correct']=[':answer/id',f[':answer-field/correct']]
   pool.append({'knowledge_point':{'db_id':kp,'id':k[':knowledge-point/id'],'title':row['title']},'question':normalized,'generation':{'batch_contract':'rounded-finance-spacing-v1','template':'annual'if 'crimes'in q[':question/problem']else'daily','retained_existing_bank':True}})
 validate_delivery_batch(pool,kp);validate_delivery_batch(fresh,kp)
 accepted=copy.deepcopy(pool)
 if kp!=17592186059798:
  for r in accepted:r['question']=stable_identities(r['question'],k[':knowledge-point/id'])
 for name,value in [('candidate-pool',pool),('accepted-pool',accepted),('fresh-samples',fresh)]:(d/(name+'.json')).write_text(json.dumps(value,indent=2)+'\n')
 summary.append({'kp':kp,'records':5,'expected_new':0 if kp==17592186059798 else 5});print(kp,'built; final-amount banks preserved'if kp==17592186059798 else'built replacement pool')
(H/'build-verification.json').write_text(json.dumps({'passed':True,'knowledge_points':summary},indent=2)+'\n')
