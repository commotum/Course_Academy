"""Strict API, finite semantic batch, and prior graded-record compatibility.

This check preserves the prior bounded mathematics/native input and reports.
"""
import hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
import sympy as s
D=Path(__file__).resolve().parent
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('definite_interface_generator',D.with_suffix('.py'));reader=module('definite_interface_reader',D/'readback.py')
def rejects(fn,*args,**kwargs):
 try:fn(*args,**kwargs)
 except (TypeError,ValueError):return
 raise AssertionError(('invalid public input accepted',args,kwargs))
def actual_task(record):
 q=record['question'];given=next(z for z in reader.blocks(q[':question/problem']) if r'\int' in z).strip().rstrip('= .')
 c,F,var,lo,hi,after=reader.integral_parts(given);assert not after
 F=(c*F).replace(lambda v:isinstance(v,s.Pow) and not v.base.has(var) and v.exp.has(var),lambda v:s.exp(s.expand(v.exp*s.expand_log(s.log(v.base),force=True))))
 return g.digest([s.srepr(s.cancel(F)),s.srepr(lo),s.srepr(hi)])
def main():
 retained=['native-input.json','native-report.json','diagnostic-input.json','diagnostic-report.json','source.json','source-cases.json','capacity.json','review.json']
 retained_hashes={fn:hashlib.sha256((D/fn).read_bytes()).hexdigest() for fn in retained}
 strict=0
 for value in (True,False,1.0,'1',None):
  for fn in (g.generate,g.generate_easy,g.generate_moderate,g.generate_hard):
   if fn==g.generate:rejects(fn,'easy',seed=value)
   else:rejects(fn,seed=value)
   strict+=1
  rejects(g.generate_batch,'easy',seed=value);strict+=1
 for value in (True,False,1.0,'1',None,0,-1):rejects(g.generate_batch,'easy',count=value);strict+=1
 for name,anchor in g.ANCHORS.items():
  for slot in anchor:
   for value in (True,False,float(anchor[slot]),str(anchor[slot]),None):
    params=dict(anchor);params[slot]=value
    rejects(g.generate,g.DIFFICULTY[name],template=name,parameters=params);strict+=1
  for params in ({},dict(anchor,unexpected=1),list(anchor.items())):
   rejects(g.generate,g.DIFFICULTY[name],template=name,parameters=params);strict+=1
 capacity={};batch_digests={};actual_fingerprints=set()
 for level in g.LEVELS:
  descriptors=g.semantic_catalog(level);cap=g.capacity(level);assert len(descriptors)==cap
  batch=g.generate_batch(level,count=cap,seed=9231)
  keys=[r['generation']['task_fingerprint'] for r in batch];assert len(set(keys))==cap
  actual=[actual_task(r) for r in batch];assert actual==keys and len(set(actual))==cap
  actual_fingerprints.update(actual)
  assert {r['generation']['template'] for r in batch}=={r['template'] for r in descriptors}
  assert g.generate_batch(level,count=cap,seed=9231)==batch
  rejects(g.generate_batch,level,count=cap+1)
  batch_digests[level]=g.digest([r['question'] for r in batch]);capacity[level]=cap
  print(level,cap,'distinct full-capacity batch cases',flush=True)
 # Alternate bases, denominator scaling, blank wording, and entire banks do
 # not make a second semantic task. Compare independently read actual givens.
 alias_pairs=[
  (g.generate('moderate',template='quadratic_scaled_base_radio',parameters=dict(b=4,k=2)),g.generate('moderate',template='quadratic_scaled_base_radio',parameters=dict(b=2,k=4))),
  (g.generate('moderate',template='square_base_radio',parameters=dict(b=2)),g.generate('moderate',template='quadratic_scaled_base_radio',parameters=dict(b=2,k=2))),
  (g.generate('hard',template='exponential_ratio_blank',parameters=dict(a=2,c=2,h=2,l=2,r=5)),g.generate('hard',template='exponential_ratio_blank',parameters=dict(a=3,c=2,h=3,l=2,r=5))),
  (g.generate('hard',template='exponential_ratio_blank',parameters=g.ANCHORS['exponential_ratio_blank'],profile='source_blank'),g.generate('hard',template='exponential_ratio_blank',parameters=g.ANCHORS['exponential_ratio_blank'],profile='source_presentation')),
  (g.generate('easy',template='natural_integer_radio',parameters=g.ANCHORS['natural_integer_radio'],profile='source_bank'),g.generate('easy',template='natural_integer_radio',parameters=g.ANCHORS['natural_integer_radio'],profile='authored_method_bank')),
 ]
 for a,b in alias_pairs:assert actual_task(a)==actual_task(b)==a['generation']['task_fingerprint']==b['generation']['task_fingerprint']
 profile_capacities={}
 for profile in ('authored_method_bank','source_bank','source_blank','source_presentation'):
  profile_capacities[profile]={}
  for level in g.LEVELS:
   try:descriptors=g.semantic_catalog(level,profile=profile)
   except ValueError:continue
   n=len(descriptors);profile_capacities[profile][level]=n
   b=g.generate_batch(level,count=n,seed=41,profile=profile);assert len({actual_task(r) for r in b})==n
   rejects(g.generate_batch,level,count=n+1,profile=profile)
 compatible=0
 for item in json.loads((D/'native-input.json').read_text()):
  prior=item['record'];meta=prior['generation'];new=g.generate(prior['question'][':question/difficulty'].split('/')[-1],seed=meta['seed'],template=meta['template'],parameters=meta['parameters'],profile=meta['bank_profile'])
  assert new['question']==prior['question'] and new['knowledge_point']==prior['knowledge_point']
  assert actual_task(new)==new['generation']['task_fingerprint']==meta['task_fingerprint'];compatible+=1
 cli=[sys.executable,str(D.with_suffix('.py')),'--format','json']
 one=json.loads(subprocess.check_output(cli+['--difficulty','all','--count','1'],text=True));assert len(one)==3 and all(isinstance(r,dict) for r in one)
 many=json.loads(subprocess.check_output(cli+['--difficulty','all','--count','4','--seed','42'],text=True));assert len(many)==12
 for level in g.LEVELS:
  records=[r for r in many if r['question'][':question/difficulty'].endswith('/'+level)];assert len(records)==4 and len({actual_task(r) for r in records})==4
 for extra in (['--difficulty','all','--count',str(capacity['easy']+1)],['--difficulty','easy','--count','true'],['--seed','true'],['--count','0']):
  failure=subprocess.run(cli+extra,capture_output=True,text=True);assert failure.returncode!=0 and not failure.stdout.strip()
 assert retained_hashes=={fn:hashlib.sha256((D/fn).read_bytes()).hexdigest() for fn in retained}
 report={'status':'passed','generator_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'strict_invalid_inputs_rejected':strict,'default_semantic_capacity':capacity,'profile_semantic_capacity':profile_capacities,'batch_question_digests':batch_digests,'independently_read_full_capacity_tasks':len(actual_fingerprints),'semantic_alias_pairs_verified':len(alias_pairs),'prior_graded_question_records_unchanged':compatible,'retained_evidence_sha256':retained_hashes,'cli_all_count1_records':len(one),'cli_all_count4_records':len(many),'database_writes':0,'mathematics_changed':False,'native_limitation':'Prior documented valid logarithm-difference equivalence remains unresolved; this interface revision makes no engine or answer changes.'}
 (D/'interface-cli.json').write_text(json.dumps(many,indent=2,ensure_ascii=False)+'\n');(D/'interface-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
