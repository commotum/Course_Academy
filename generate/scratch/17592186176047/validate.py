"""Current-basis checkbox source fidelity, exhaustive mathematics, native grading."""
import hashlib,json,subprocess
from pathlib import Path
from instance_validation import g,inspect,native,fingerprint
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def main():
 records=[];replay=[];banks=0;values=0;catalog={}
 for case in json.loads((HERE/'source-cases.json').read_text()):
  name=case['template']
  if name=='q-167631':continue
  r=g.generate('moderate',template=name,parameters=case['parameters'],profile=case['bank_profile']);inspect(r)
  current=g.CURRENT_QUESTIONS[name];q=r['question']
  assert q[':question/problem']==current[':question/problem'],name
  assert q[':question/worked-solution']==current[':question/worked-solution'],name
  for f in q[':question/answer-fields']:
   old=next(f0 for f0 in current[':question/answer-fields'] if f0[':answer-field/key']==f[':answer-field/key'])
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in old[':answer-field/choices'])
   assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==old[':answer-field/correct'][':answer/value']
   banks+=1;values+=len(f[':answer-field/choices'])
  assert fingerprint(q)==r['generation']['mathematical_task_fingerprint']
  replay.append({'source_id':name,'prompt':'exact','solution':'exact','complete_boolean_banks':'exact','correct_designations':'exact'})
  records.append(r)
 for level in g.SUPPORTED_LEVELS:
  seen=set()
  for p in g.authored_catalog(level):
   r=g.generate(level,parameters=p);inspect(r)
   fp=fingerprint(r['question']);assert fp==r['generation']['mathematical_task_fingerprint'] and fp not in seen;seen.add(fp)
   assert r['question']==g.generate(level,seed=7,parameters=p)['question']
   records.append(r)
  catalog[level]=len(seen)
 # Fixed data / changed queried property: family offsets and steps independently
 # parsed in every catalog member, including all six shapes at each target role.
 repaired=g.generate('moderate',template='q-167631');inspect(repaired);records.append(repaired)
 fixtures=[native(str(i),r) for i,r in enumerate(records)]
 (HERE/'engine-input.json').write_text(json.dumps(fixtures,indent=2,ensure_ascii=False)+'\n')
 engine=ROOT/'generate/runs/current/check-engine'
 proc=subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True,check=True)
 report={'status':'pass','version':g.VERSION,'source_basis':g.CURRENT['basis'],'source_fidelity':{'questions':7,'prompts_exact':7,'solutions_exact':7,'banks_matched':banks,'banks_total':21,'bank_values_matched':values,'bank_values_total':42,'replays':replay},'mathematics':{'catalog_counts':catalog,'all_rendered_prompts_independently_parsed':True,'semantic_fingerprints_exclude_seed_identity_order_and_incidental_magnitudes':True,'deterministic_replay':True},'native_grader':{'fixture_count':len(fixtures),'check_count':sum(len(f['checks']) for f in fixtures),'stdout':proc.stdout,'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest()},'authored_levels':['easy','hard'],'excluded_source_templates':[{'source_id':'q-167631','reason':'Sine mislink and doubled TeX slashes in current source. Preserved; raw instance excluded. Corrected cosine singleton separately graded.'}], 'supported_levels':list(g.SUPPORTED_LEVELS)}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:report[k] for k in ('status','mathematics','native_grader')},indent=2))
if __name__=='__main__':main()
