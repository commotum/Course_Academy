from audit_support import *
from check_minimal import probe
import collections
rs=json.loads((E/'batch.json').read_text());checks=[];cases=[]
for r in rs:
 if r['generation']['template']=='q-126765':
  assert simplify(expr(correct(r))-(x-r['generation']['parameters']['h'])**2)==0
  checks.append({'template':'q-126765','passed':True,'witness':'differentiate sine on the stated cos-positive local branch; check_repairs.py'})
 else:
  result=math_check(r);assert result['passed'] and result['valid_choice_count']==1,result;checks.append(result)
 f=field(r)
 if f[':answer-field/type'].endswith('/radio'):
  cs=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected'} for a in f[':answer-field/choices']]
 else:cs=[{'submitted':correct(r),'expected':'accepted'},{'submitted':'0','expected':'rejected'}]
 cases.append({'label':'batch '+r['generation']['template'],'record':r,'checks':cs})
save('batch-math.json',checks);save('batch-grader-input.json',cases)
p=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(E/'batch-grader-input.json'),str(E/'batch-grader-report.json')],capture_output=True,text=True);(E/'batch-grader-console.txt').write_text(p.stdout+p.stderr);assert p.returncode==0,p.stderr
accepted=json.loads((E/'delivery-batch/accepted.json').read_text());assert len(accepted)==5
ms={}
for name,items in [('raw',rs),('accepted',accepted)]:
 trig=[r for r in items if r['generation']['template']=='q-104065'];success=0
 for r in trig:
  cand=[a for a in field(r)[':answer-field/choices'] if ('\\ln' in a[':answer/value'] or '\\operatorname{ln}' in a[':answer/value']) and '\\pi' not in a[':answer/value']]
  success+=int(len(cand)==1 and cand[0][':answer/id']==field(r)[':answer-field/correct'][1])
 assert success==0
 latest=[probe(r) for r in trig];assert not any(q['shortcut_success'] for q in latest)
 ms[name]={'records':len(items),'trig':len(trig),'old_symbol_cue_successes':success,'latest_conditional_cue_qualifying':sum(q['qualifies'] for q in latest),'latest_conditional_cue_successes':sum(q['shortcut_success'] for q in latest)}
save('batch-shortcut-results.json',ms)
# Reproduce the configured selection's conditional uniform-within-easy draw.
# Publication IDs are unknown, so proxy IDs demonstrate support, not live draws.
inv=json.loads((JOB/'source/inventory.json').read_text());old=[(q[':db/id'],'source') for q in inv['questions'] if q[':question/difficulty'][':db/ident'].endswith('/easy')];base=max(q[':db/id'] for q in inv['questions'])+1;pool=sorted(old+[(base+i,r['generation']['template']) for i,r in enumerate(accepted)]);draws=[]
for i in range(64):
 d=hashlib.sha256(('course-academy/question-selection/v1/author-'+str(i)).encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/2**53;draws.append(pool[int(u*len(pool))][1])
save('selection.json',{'basis':inv['basis'],'implementation':'engine/rust/question_selection.rs: sorted BTreeSet; sha256 bytes 8..16, 53-bit uniform index within selected band','pool_size':len(pool),'conditional_draws':dict(collections.Counter(draws)),'limits':['Conditioned on positive easy-band selection and freshness; live weights and task history are unavailable.','Unpublished generated items use proxy IDs; exact live draws are not claimed.','Every accepted easy item has nonzero conditional support. History can remove an item but does not alter its option bank or restore the repaired trig symbol cue.']})
# Count semantic IVPs separately from authored banks, seeds, IDs and option order.
allrs=json.loads((E/'current-records.json').read_text());sem=collections.defaultdict(set)
for r in allrs:sem[r['generation']['template']].add(r['question'][':question/problem'])
save('semantic-coverage.json',{'records':len(allrs),'unique_visible_mathematical_tasks':sum(map(len,sem.values())),'by_template':{k:len(v) for k,v in sem.items()},'slot_coverage':'trig: a=2,4,6; C=-pi²,-1,0,1,pi²; h boundaries and all eight old nonzero shifts. Radical: b=-2,-1,1,2. Other unchanged profiles: one small regression per profile; retained native families at h=-4,1,4.','limits':'Legacy translated profiles preserve their original integration constants and source banks. No claim that those translations cover initial-condition reassignment. Decision variation is specifically repaired in the demonstrated trig family and restored radical-branch family.'})
print(p.stdout.strip());print('batch math and delivery: 5 passed')
