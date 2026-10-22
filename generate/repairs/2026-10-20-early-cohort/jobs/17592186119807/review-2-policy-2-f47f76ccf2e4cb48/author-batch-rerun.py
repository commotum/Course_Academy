#!/usr/bin/env python3
"""Retained sign-shortcut regression against real generator/CLI and delivery.
No services/database writes or runtime-file mutations. Truth uses visible vectors.
"""
import collections
import json
from pathlib import Path
import subprocess
import sys
import importlib.util
spec=importlib.util.spec_from_file_location("author_current",Path(__file__).resolve().parent/"author-check-rerun.py")
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
H=c.H;E=c.E/'sign-repair';E.mkdir(exist_ok=True)
REPO=H.parents[5]
REVIEW=H.parent/'review-1-policy-2-bc476fa1f6e925b4'
def save(name,obj):(E/name).write_text(json.dumps(obj,indent=2)+'\n')
def features(r):
 nums=[c.number(a[':answer/value']) for a in c.choices(r) if a[':answer/type']==':answer.type/math']
 a,b,_=c.vecs(r)
 return {'nonpositive':any(n<=0 for n in nums),'names':'a/b' if '{a}_{1}' in r['question'][':question/problem'] else 'c/d',
         'columns':str((a,b)), 'all_negative':max(nums)<0,'has_zero':0 in nums,
         'mixed_signs':min(nums)<0<max(nums),'fractional':any(n.denominator!=1 for n in nums)}
def inspect(rs,strict=True):
 groups=collections.defaultdict(list)
 for r in rs:
  assert c.canonical(c.key(r))==c.expected(r)
  assert len(c.choices(r))==5 and len({c.canonical(a[':answer/value']) for a in c.choices(r)})==5
  meta=r['generation']
  replay=c.check(c.g.generate('moderate',meta['seed'],meta['source_id'],meta['parameters']))
  assert c.vecs(r)==c.vecs(replay) and c.canonical(c.key(r))==c.canonical(c.key(replay))
  assert r['question'][':question/worked-solution']==replay['question'][':question/worked-solution']
  for k,v in features(r).items():
   if k in ('nonpositive','names','columns') or v:groups[(k,str(v))].append(r)
 report={}
 for (k,v),items in groups.items():
  truths=[c.expected(r)!='No solution' for r in items]
  report[k+':'+v]={'count':len(items),'numeric_keys':sum(truths),'no_solution_keys':len(items)-sum(truths),
                  'ranks':[c.rank(r) for r in items]}
  if strict and len(items)>=2:assert set(truths)=={False,True},(k,v,truths)
 if strict:
  for flag in ('False','True'):
   group=groups[('nonpositive',flag)]
   assert {c.expected(r)!='No solution' for r in group}=={False,True}
  assert len({c.rank(r) for r in rs if c.expected(r)!='No solution'})>1
  assert len({next(i for i,a in enumerate(c.choices(r)) if a[':answer/value']==c.key(r)) for r in rs})>1
 return report
def main():
 # Re-run the exact retained reviewer script: the old pool MUST fail.
 original=REVIEW/'delivery-batch/accepted.json'
 old=subprocess.run([sys.executable,str(H/'batch_regression.py'),'--records',str(original)],capture_output=True,text=True)
 assert old.returncode!=0 and '3/3' in old.stderr
 oldrecords=json.loads(original.read_text());report=inspect(oldrecords,False)
 save('original-failure.json',{'command':['<context-python>','batch_regression.py','--records',str(original)],'exit_code':old.returncode,'stderr':old.stderr,'groups':report})
 save('original-records.json',oldrecords)
 # The minimal record is still supported, with the same signs and truth.
 parameters={'translation':-2,'residual':'1','rank':4,'gaps':[4,4,4]}
 bad=c.check(c.g.generate('moderate',5888234723018271144,'q-105166',parameters))
 assert {c.number(a[':answer/value']) for a in c.choices(bad) if a[':answer/type']==':answer.type/math'}=={-16,-12,-8,-4}
 assert c.expected(bad)=='No solution'
 good=c.check(c.g.generate('moderate',5888234723018271144,'q-105166',dict(parameters,residual='0')))
 assert c.expected(good)=='-4' and features(good)['nonpositive']
 assert [(a[':answer/value'],a[':answer/type']) for a in c.choices(bad)]==[(a[':answer/value'],a[':answer/type']) for a in c.choices(good)]
 controls=[bad,good];coverage=[]
 for sid in sorted(c.g.CASES):
  group=[]
  for residual in (0,1):
   pair=[c.check(c.g.generate('moderate',83,sid,{'translation':2,'residual':residual,'rank':rank,'gaps':[5,5,5]})) for rank in (1,4)]
   assert pair[0]['question'][':question/problem']==pair[1]['question'][':question/problem']
   assert pair[0]['question'][':question/worked-solution']==pair[1]['question'][':question/worked-solution']
   assert c.expected(pair[0])==c.expected(pair[1])
   assert features(pair[0])['nonpositive'] is False and features(pair[1])['nonpositive'] is True
   group+=pair
  assert {c.expected(r)!='No solution' for r in group}=={False,True}
  controls+=group
  coverage.append({'profile':sid,'both_branches_under_both_sign_conditions':True,'bank_change_preserves_prompt_solution_and_truth':True})
 save('controlled-records.json',controls);save('controlled-coverage.json',coverage)
 out=E/'delivery-controls'
 subprocess.run([sys.executable,str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(E/'controlled-records.json'),'--source',str(H.parent/'source/source.json'),'--inventory',str(H.parent/'source/inventory.json'),'--difficulty','moderate','--output',str(out),'--asset-root',str(E/'assets')],check=True,capture_output=True,text=True)
 delivered_controls=json.loads((out/'accepted.json').read_text())
 assert len(delivered_controls)==len(controls)
 for sid in c.g.CASES:
  group=[r for r in delivered_controls if r['generation']['source_id']==sid]
  for sign in (False,True):
   assert {c.expected(r)!='No solution' for r in group if features(r)['nonpositive']==sign}=={False,True}
 # Positive control adopted unchanged from reviewer except path/default.
 positive=subprocess.run([sys.executable,str(H/'batch_regression.py'),'--records',str(E/'controlled-records.json')],check=True,capture_output=True,text=True)
 batches=[];allrecords=[]
 for seed in (0,1,119807,291807):
  cmd=[sys.executable,str(H/'17592186119807.py'),'--difficulty','moderate','--count','5','--seed',str(seed),'--format','json']
  rs=json.loads(subprocess.run(cmd,check=True,capture_output=True,text=True).stdout)
  assert rs==c.g.batch('moderate',5,seed)
  assert len({tuple(c.vecs(r)) for r in rs})==5
  raw=inspect(rs);save(f'batch-{seed}.json',rs)
  out=E/f'delivery-{seed}'
  cmd=[sys.executable,str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(E/f'batch-{seed}.json'),'--source',str(H.parent/'source/source.json'),'--inventory',str(H.parent/'source/inventory.json'),'--difficulty','moderate','--output',str(out),'--asset-root',str(E/'assets')]
  subprocess.run(cmd,check=True,capture_output=True,text=True)
  accepted=json.loads((out/'accepted.json').read_text());assert len(accepted)==5
  post=inspect(accepted)
  strict=subprocess.run([sys.executable,str(H/'batch_regression.py'),'--records',str(out/'accepted.json')],check=True,capture_output=True,text=True)
  batches.append({'seed':seed,'command':['<context-python>','17592186119807.py','--difficulty','moderate','--count','5','--seed',str(seed),'--format','json'],'raw':raw,'accepted':post,'accepted_count':len(accepted),'reviewer_regression':strict.stdout.strip()})
  allrecords+=accepted
 save('batch-results.json',{'passed':True,'batches':batches,'source_evidence_changed':False,'original_regression_exit':old.returncode,'positive_control':positive.stdout.strip(),'controlled_raw':len(controls),'controlled_accepted':len(delivered_controls),'controlled_semantic_systems':len({tuple(c.vecs(r)) for r in controls}),'all_profiles_both_signs_both_branches_after_delivery':True})
 save('grading-records.json',controls[:2]+allrecords)
 # Observe actual runtime resampling separately from publication normalization.
 attempted=[];original_generate=c.g.generate
 def trace(*args,**kwargs):
  record=original_generate(*args,**kwargs);attempted.append(record);return record
 c.g.generate=trace
 try:traced=c.g.batch('moderate',5,119807)
 finally:c.g.generate=original_generate
 assert traced==json.loads((E/'batch-119807.json').read_text())
 save('resampling.json',{'seed':119807,'attempts':len(attempted),'returned':len(traced),'attempted_sign_truth':dict(collections.Counter(str((features(r)['nonpositive'],c.expected(r)!='No solution')) for r in attempted)),'returned_sign_truth':dict(collections.Counter(str((features(r)['nonpositive'],c.expected(r)!='No solution')) for r in traced)),'attempted_profiles':dict(collections.Counter(r['generation']['source_id'] for r in attempted)),'limit':'Counts combine role-witness rejection, semantic deduplication and complete-pool acceptance. No publication or learner-history selection is included. Trace wraps generate only in memory and restores it; runtime files are untouched.'})
 print(json.dumps({'passed':True,'original_shortcut_reproduced':'3/3','profiles_both_signs_both_branches':len(coverage),'cli_batches_after_delivery':len(batches),'delivered_records':len(allrecords)}))
if __name__=='__main__':main()
