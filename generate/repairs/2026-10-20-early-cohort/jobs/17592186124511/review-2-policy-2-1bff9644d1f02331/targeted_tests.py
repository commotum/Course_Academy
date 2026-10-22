"""Changed-rule review; all writes are relative to this evidence directory.
Run: PYTHONDONTWRITEBYTECODE=1 <job-python> targeted_tests.py
"""
import collections,copy,hashlib,importlib.util,json,os,pathlib,subprocess,sys
sys.dont_write_bytecode=True
from audit import E,P,B,REPO,load_generator,visible,correct,save,native,summary
prev=B/'review-1-policy-2-3b53743f6e315249'
g=load_generator()
# Retained independent assertion fails the old version and passes the current one.
oldroot=E/'historical-package';oldroot.mkdir(exist_ok=True)
m=json.load(open(P/'package.json'))
import shutil
for rel in m['files']:
 src=prev/'relocated'/rel
 if src.exists():
  (oldroot/rel).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,oldroot/rel)
old=load_generator(oldroot)
def source_assert(module):
 r=module.generate(template='q-142367',replay=True)
 f=r['question'][':question/answer-fields'][0]
 assert correct(f)=='I only' and [x[':answer/value'] for x in f[':answer-field/choices']]==['II and III only','III only','I and II only','II only','I only']
 return r
def cue(r):return all((correct(f)=='true')==('invertible' in f[':answer-field/key']) for f in r['question'][':question/answer-fields'])
def batch_assert(rows):
 sub=[r for r in rows if len(r['question'][':question/answer-fields'])==3]
 assert len(sub)>=2
 assert not all(map(cue,sub)),'Select only the invertibility claim solves all recurring three-checkbox items.'
 return {'successes':sum(map(cue,sub)),'total':len(sub)}
retained=[]
for name,func in [('source',lambda mod,rows:source_assert(mod)),('batch',lambda mod,rows:batch_assert(rows))]:
 for stage,mod,rows in [('historical',old,json.load(open(prev/'runner-batch.json'))),('current',g,json.load(open(E/'delivery-batch/accepted.json')))]:
  try:func(mod,rows)
  except Exception as ex:result={'passed':False,'error':type(ex).__name__+': '+str(ex)}
  else:result={'passed':True}
  assert result['passed']==(stage=='current'),(name,stage,result)
  retained.append({'finding':name,'stage':stage,**result})
save('retained-independent-results.json',{'command':sys.argv,'results':retained,'preflight':json.load(open(B/'repair-preflight.json')),'historical_source':'historical-package/17592186124511.py','historical_batch':'historical-batch.json'})
save('historical-batch.json',json.load(open(prev/'runner-batch.json')))
# Run the executable retained author checks on historical counterexamples,
# using identical assertions and meaningful failures rather than missing helpers.
author=E/'author-current/checks/check_repairs.py';spec=importlib.util.spec_from_file_location('retained_author',author);a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
checks=[]
for label,fn in [('source',lambda: a.g.generate(template='q-142367',replay=True)),('batch',lambda:a.audit_batch(json.load(open(E/'historical-batch.json'))))]:
 if label=='source':
  current=a.g;a.g=old
 try:fn()
 except Exception as ex:checks.append({'case':label,'historical_return':'failed as required','error':type(ex).__name__+': '+str(ex)})
 else:raise AssertionError('retained assertion did not fail historical '+label)
 finally:
  if label=='source':a.g=current
save('retained-author-historical-results.json',checks)
# Trace actual rejection/resampling of one full profile cycle. Interception only
# observes records in this process; no generator file is changed.
attempts=[];original=g.generate
def observe(*args,**kwargs):
 r=original(*args,**kwargs);visible(r);attempts.append(r);return r
g.generate=observe
cycle=g.batch('moderate',len(g.TEMPLATES),947103)
g.generate=original
assert len(cycle)==16 and {r['generation']['template'] for r in cycle}==set(g.TEMPLATES)
assert cycle==g.batch('moderate',16,947103)
for r in cycle:visible(r)
save('sampling-candidates.json',attempts);save('sampling-cycle.json',cycle)
save('sampling-cycle-results.json',{'seed':947103,'requested_count':16,'attempts':len(attempts),'accepted':len(cycle),'all_complete_profiles_reached':True,'deterministic_replay':True,'before':summary(attempts),'after':summary(cycle),'rejected_ids':[r['question'][':question/id'] for r in attempts if r['question'][':question/id'] not in {x['question'][':question/id'] for x in cycle}]})
# Current independent data after actual shared preparation, plus valid boundaries.
raw=json.load(open(E/'samples.json'));survivors=json.load(open(E/'delivery-samples/accepted.json'));batch=json.load(open(E/'delivery-batch/accepted.json'));pairs=json.load(open(E/'delivery-counterfactual/accepted.json'));bounds=json.load(open(E/'boundary-records.json'))
for r in survivors+batch+pairs+bounds:visible(r)
save('postdelivery-native-input.json',[native(r,'delivered-'+str(i)) for i,r in enumerate(survivors+batch+pairs+bounds+cycle)])
save('postdelivery-analysis.json',{'fresh_samples':[len(raw),len(survivors)],'runner_batch':[5,len(batch)],'controlled_records':[6,len(pairs)],'sample_coverage':summary(survivors),'runner_batch_coverage':summary(batch),'batch_content_cue':batch_assert(batch),'source_correction':'q-142367 only: lI only -> II only; all five choices, correct I-only key, prompt and solution preserved'})
# Capture scope and inventory independently (never call the sources generated).
inventory=json.load(open(B/'source/inventory.json'));source=json.load(open(B/'source/source.json'))
ids={r[':question/id'] for r in source['material']['kp'][':knowledge-point/questions']}
assert all(r[':question/id'] in ids and r.get(':question/math-academy-id') and not r.get(':question/generation') for r in inventory['questions'])
save('inventory-assessment.json',{'basis':inventory['basis'],'inspected':len(inventory['questions']),'generated':0,'source_originals':len(inventory['questions']),'status':'Verified absence of stored generated instances in this captured inventory; no future/live inventory claim.','publication_preparation_exists':(B/'publication/preparation.json').exists()})
save('affected-inventory.json',{'affected_questions':[]})
print(json.dumps({'retained_assertions':retained,'traced_sampling':{'attempts':len(attempts),'accepted':len(cycle)},'delivery_samples':[len(raw),len(survivors)],'batch':batch_assert(batch)}))
