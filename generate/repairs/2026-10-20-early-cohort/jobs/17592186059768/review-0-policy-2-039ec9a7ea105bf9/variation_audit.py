#!/usr/bin/env python3
"""Analyze delivered records without using metadata to choose a response."""
import sys
sys.dont_write_bytecode=True
import collections,hashlib,json,pathlib,re
import audit
E=audit.E
PATTERNS={
 'q-20361':[r'-x\+y=\d+',r'x\+y=\d+'],
 'q-1052':[r'\d+x-\d+=\d+y',r'\d+\+y=\d+x'],
 'q-129122':[r'\d+x-y=\d+',r'\d+x=-\d+'],
 'q-129124':[r'\d+y=\d+-x',r'\d+x-\d+y\+1=0'],
 'q-71722':[r'x-\d+=\d+y',r'1\+y=-\d+x'],
 'q-1051':[r'\d+x\+y\+z=\d+',r'x\+z=\d+'],
 'q-1065':[r'\d+x\+\d+y-z=\d+',r'\d+-\d+x=-\d+y',r'-y\+\d+x=\d+z']}
audit.SIGNATURES=audit.read(E/'shortcut-signatures.json')
def recognize(r):
 rows=[re.sub(r'\s+','',x) for x in audit.equation_blocks(r['question'][':question/problem'])[0]]
 found=[p for p,patterns in PATTERNS.items() if len(rows)==len(patterns) and all(re.fullmatch(p,x) for p,x in zip(patterns,rows))]
 assert len(found)==1,(rows,found)
 return found[0]
def predict(r):
 profile=recognize(r)
 choices=[a for a in audit.field(r)[':answer-field/choices'] if audit.sign(audit.matrix(a[':answer/value'])[0])==audit.SIGNATURES[profile]]
 return choices[0][':answer/id'] if len(choices)==1 else None

def summarize(records):
 out={}
 for profile in PATTERNS:
  group=[r for r in records if recognize(r)==profile]
  if not group:continue
  out[profile]={'total':len(group),'source_sign_mask_correct':sum(predict(r)==audit.correct_id(audit.field(r)) for r in group),'unique_negative_corner_correct':sum(audit.negative_corner(r) for r in group),'ids':[r['question'][':question/id'] for r in group]}
 return {'count':len(records),'sign_mask_correct':sum(predict(r)==audit.correct_id(audit.field(r)) for r in records),'profiles':out}
def select(pool,seed,weights=None):
 # Faithful reproduction of question_selection.rs::select; candidates fresh/usable.
 pool=sorted(pool,key=lambda x:x[0])
 if weights is None:return pool[0] if pool else None
 bands=[[p for p in pool if p[1]==level] for level in ['easy','moderate','hard']]
 digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 uniform=lambda n:(int.from_bytes(digest[n:n+8],'big')>>11)/(2**53)
 total=sum(w for w,b in zip(weights,bands) if b)
 if total<=0:return None
 draw=uniform(0)*total;chosen=None
 for w,b in zip(weights,bands):
  if not b or not w:continue
  chosen=b
  if draw<w:break
  draw-=w
 return chosen[int(uniform(8)*len(chosen))]
def main():
 inputs={n:audit.read(E/f) for n,f in [('raw','independent-samples.json'),('runner_batch','runner-batch.json'),('delivered_easy','delivery-easy/accepted.json'),('delivered_moderate','delivery-moderate/accepted.json'),('delivered_batch','delivery-batch/accepted.json'),('stored_generated','generated-records.json')]}
 result={k:summarize(v) for k,v in inputs.items()}
 result['strategy']={'recognition':'Regular-expression equation layouts; no metadata is read when choosing an answer','rule':'Select the unique choice matching the memorized source sign mask, ignoring every magnitude and every equality operation','patterns':PATTERNS,'comparison':'Randomly choose one of five radio choices: 0.2','permutations':'Choice array reversal preserves prediction; real UI choiceOrder shuffles choices and cannot remove value-based cue'}
 for rs in inputs.values():
  for r in rs:
   rev=json.loads(json.dumps(r));audit.field(rev)[':answer-field/choices'].reverse();assert predict(rev)==predict(r)
 audit.save('shortcut-results.json',result)
 # Complete pipeline input exercise: duplicate rejection actually happens, not only no-op pass.
 probe=inputs['stored_generated'][:1]+inputs['runner_batch'][:1]*2
 audit.save('delivery-duplicate-input.json',probe)
 # Inventory selection remains conditional on weights/history, neither captured. Examine allowed configurations explicitly.
 inv=audit.read(audit.JOB/'source/inventory.json');generated={r['question'][':question/id']:r for r in inputs['stored_generated']}
 all_pool=[(q[':db/id'],q[':question/difficulty'][':db/ident'].split('/')[-1],q[':question/id']) for q in inv['questions']]
 fresh=[p for p in all_pool if p[2] in generated] # exact hypothetical history excludes original sources, retains all seven generated
 trials={}
 for label,weights in [('unconfigured',None),('easy_only',[1,0,0]),('both_supported',[1,1,0])]:
  chosen=[select(fresh,'independent-review-'+str(i),weights) for i in range(64)]
  assert all(p is not None for p in chosen)
  rows=[generated[p[2]] for p in chosen]
  trials[label]={'distribution':weights,'draws':64,'selection':dict(collections.Counter(p[2] for p in chosen)),'sign_mask_correct':sum(predict(r)==audit.correct_id(audit.field(r)) for r in rows)}
 audit.save('learner-selection-results.json',{'algorithm_source':str(audit.REPO/'engine/rust/question_selection.rs')+':select lines 132–198','basis':inv['basis'],'hypothetical_fresh_usable_entity_ids':[p[0] for p in fresh],'trials':trials,'limits':'Captured inventory does not include actual policy weights, reserved items, or learner history. Results conditional on explicitly stated configurations; selection does not transform matrix contents. This is a faithful read-only reproduction, not execution against a live snapshot.'})
 # Fail acceptance directly on the simplest case, preserving a runnable repair regression.
 minimal=audit.g.generate('easy',941713401,profile='q-71722',parameters={'2':2,'3':4})
 audit.save('minimal-failing-case.json',[minimal])
 corner_cases=[r for r in inputs['raw'] if recognize(r)=='q-71722']
 accepted_test=not all(audit.negative_corner(r) for r in corner_cases)
 audit.save('regression-results.json',{'command':str(audit.PY)+' -B variation_audit.py','assertion':'A recognizable source family must not be universally answered by selecting the only matrix with a negative bottom-right entry','passed':accepted_test,'failure':{'profile':'q-71722','seed':941713401,'parameters':{'2':2,'3':4},'prompt':minimal['question'][':question/problem'],'rule':'Select sole negative bottom-right matrix','observed_correct':audit.negative_corner(minimal),'family_successes':sum(audit.negative_corner(r) for r in corner_cases),'family_attempts':len(corner_cases)},'all_probes':result})
 print(json.dumps({k:{'count':v['count'],'sign_mask_correct':v['sign_mask_correct']} for k,v in result.items() if 'count' in v}))
 assert accepted_test,'Fixed negative-corner cue answers q-71722 without transposing terms; see minimal-failing-case.json'
if __name__=='__main__':main()
