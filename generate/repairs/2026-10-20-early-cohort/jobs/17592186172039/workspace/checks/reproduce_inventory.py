"""Reproduce archived generation metadata and current captured storage representation.
The stored migration renamed I/II/III keys but retained IDs and truth values.
No database writes or external services; only the current generator emits new assets.
"""
import copy, importlib.util, json, pathlib, re, sys
sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parents[1]

def reproduce(current):
 archive=json.loads((ROOT/'17592186172039/reference/replenishment/basis-2772/generated.json').read_text())
 inv=json.loads((ROOT/'../source/inventory.json').read_text())['questions']
 original=next(r for r in archive if r['question'][':question/id']=='0dbda9ea-eb5b-5de0-b271-e71696078d9a')
 oldpath=ROOT/'evidence/historical-generator.py'
 # Historical replay executes only the definition section, before its old repository
 # policy wrapper. This is precisely the raw response shape that was stored.
 source=oldpath.read_text().split('# Every learner-facing checkbox question')[0]
 namespace={'__file__':str(oldpath),'__name__':'historical_evidence'}
 exec(compile(source,str(oldpath),'exec'),namespace)
 namespace['HERE']=ROOT/'17592186172039'
 gen=original['generation'];r=namespace['generate'](gen['level'],seed=gen['seed'],template=gen['template'],parameters=gen['parameters'],profile=gen['legacy_bank_profile'])
 assert r['question'][':question/id']==original['question'][':question/id']
 assert json.loads(json.dumps(r['generation']))==gen, 'Historical replay metadata differs'
 # Reproduce known storage presentation migration, comparing every served field.
 q=r['question'];lines=q[':question/problem'].splitlines();claims=[x[x.index('At every point'):] for x in lines if 'At every point' in x]
 q[':question/problem']=lines[0]+'\n\nSelect all that apply.'
 for roman,key,f in zip(('I','II','III'),claims,q[':question/answer-fields']):
  f[':answer-field/key']=key
  q[':question/worked-solution']=q[':question/worked-solution'].replace('Statement '+roman+' is','Statement “'+key+'” is')
 for old,asset in original.get('assets',{}).items():q[':question/worked-solution']=q[':question/worked-solution'].replace(old,asset['path'])
 stored=next(x for x in inv if x[':question/id']==q[':question/id'])
 def clean(x):
  if isinstance(x,list):return [clean(v) for v in x]
  if isinstance(x,dict):
   if ':db/ident' in x:return x[':db/ident']
   if ':answer-field/id' not in x and ':answer/id' in x and ':answer/value' in x:return {k:clean(v) for k,v in x.items() if k!=':db/id'}
   return {k:clean(v) for k,v in x.items() if k!=':db/id'}
  return x
 normal=clean(stored)
 for f in normal[':question/answer-fields']:
  f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
  f[':answer-field/choices'].sort(key=lambda v:v[':answer/value'])
 normal[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
 q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
 assert q==normal, 'Replayed storage representation differs from snapshot'
 # Independent evidence: -6x<0 in I, >0 in II and III; all three claims false.
 assert all(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])=='false' for f in q[':question/answer-fields'])
 assert not any(f[':answer-field/key']=='None of the above' for f in q[':question/answer-fields'])
 r['reproduction']={'archived_generator':'evidence/historical-generator.py','seed':gen['seed'],'parameters':gen['parameters'],'storage_migration':'Roman labels expanded to statements and local plot localized; all IDs, answers and original generation metadata preserved. Full stored question comparison passed.','stored_entity_id':stored[':db/id']}
 fixed=current.generate(gen['level'],seed=gen['seed'],template=gen['template'],parameters=gen['parameters'])
 fields=fixed['question'][':question/answer-fields'];none=next(f for f in fields if f[':answer-field/key']=='None of the above')
 assert next(a[':answer/value'] for a in none[':answer-field/choices'] if a[':answer/id']==none[':answer-field/correct'][1])=='true'
 assert len(fields)==4
 (ROOT/'evidence/generated-records.json').write_text(json.dumps([r],indent=2)+'\n')
 (ROOT/'evidence/inventory-repair-counterfactual.json').write_text(json.dumps([fixed],indent=2)+'\n')
 return stored
