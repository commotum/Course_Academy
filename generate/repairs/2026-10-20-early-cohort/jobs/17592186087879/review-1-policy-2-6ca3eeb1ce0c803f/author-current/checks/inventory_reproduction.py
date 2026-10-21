"""Reconstruct historical affected records using the retained reviewed code.

The current easy banks intentionally differ; this script demonstrates which
stored questions had the reviewed weakness, without changing their identities.
"""
import json, sys, types
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'evidence'
sys.path.insert(0,str(Path(__file__).resolve().parent))
from visible_math import promptdata,expr,eq,s,x
old=types.ModuleType('reviewed_generator');old.__file__=str(ROOT/'17592186087879.py')
exec(compile((E/'reviewed-entrypoint.py').read_text(),str(E/'reviewed-entrypoint.py'),'exec'),old.__dict__)
source=json.loads((ROOT.parent/'source/source.json').read_text())
inv=json.loads((ROOT.parent/'source/inventory.json').read_text())
sourceids={q[':question/id'] for q in source['material']['kp'][':knowledge-point/questions']}
records=[];affected=[];checks=[]
for q in inv['questions']:
 if q[':question/id'] in sourceids:continue
 difficulty=q.get(':question/difficulty');difficulty=difficulty.get(':db/ident') if isinstance(difficulty,dict) else difficulty
 if difficulty!=':question.difficulty/easy':
  checks.append({'id':q[':question/id'],'tested':False,'reason':'Outside reported easy-family weakness'});continue
 p,forcing,t,h=promptdata({'question':q})
 assert p==1 and t==0 and not forcing.free_symbols
 params={'a':1,'b':int(forcing),'h':int(h)}
 r=old.generate('easy',seed=0,parameters=params)
 rq=r['question']
 assert rq[':question/id']==q[':question/id']
 assert rq[':question/problem']==q[':question/problem']
 assert rq[':question/worked-solution']==q[':question/worked-solution']
 for f in rq[':question/answer-fields']:
  stored=next(z for z in q[':question/answer-fields'] if z[':answer-field/key']==f[':answer-field/key'])
  assert {(a[':answer/id'],a[':answer/value']) for a in f[':answer-field/choices']}=={(a[':answer/id'],a[':answer/value']) for a in stored[':answer-field/choices']}
 assert all(eq(s.diff(expr(a[':answer/value']),x),expr(a[':answer/value'])) == (a[':answer/id']==rq[':question/answer-fields'][0][':answer-field/correct'][1]) for a in rq[':question/answer-fields'][0][':answer-field/choices'])
 records.append(r)
 affected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],
  'finding':'Reviewed easy_constant fixes I=e^x for all normal easy questions; first field can be answered without reading the ODE.',
  'reproduction':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python checks/inventory_reproduction.py; reviewed snapshot seed=0, parameters='+json.dumps(params,sort_keys=True),
  'evidence_path':'../workspace/evidence/generated-records.json'})
 checks.append({'id':q[':question/id'],'tested':True,'reproduced':True,'parameters':params})
(E/'generated-records.json').write_text(json.dumps(records,indent=2))
(E/'affected-inventory.json').write_text(json.dumps({'affected_questions':affected},indent=2))
(E/'inventory-results.json').write_text(json.dumps({'basis':inv['basis'],'inventory_count':len(inv['questions']),'source_questions_excluded':len(sourceids),'checks':checks,'limitation':'Inventory does not retain historical generation metadata. Records match stored UUIDs, exact prompts, solutions, answer UUID/value sets. Seed 0 is a reconstruction seed, not recovered historical seed; parameters derive from displayed ODE. Non-easy records are untested for other weaknesses.'},indent=2))
print(json.dumps({'affected':len(affected),'inventory':len(inv['questions'])}))
