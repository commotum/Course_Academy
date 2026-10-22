"""Conditional shortcut witnesses after the actual shared delivery implementation."""
from common import *
import collections,hashlib

def profile(r):return r['generation']['bank_profile']
def groups(rows):
 out=collections.defaultdict(list)
 for r in rows:
  q=r['question'];prefix=q[':question/problem'].split('and')[0]
  bank=tuple(a[':answer/value'] for a in choices(q))
  out[(profile(r),prefix,bank)].append(r)
 return out

def probe(rows):
 stats={}
 rules={
  'old_label_bank_strategy':old_shortcut,
  'minimum':lambda q:min(value(a[':answer/value']) for a in choices(q) if a[':answer/value']!='No solution'),
  'maximum':lambda q:max(value(a[':answer/value']) for a in choices(q) if a[':answer/value']!='No solution'),
  'No solution':lambda q:'No solution',
 }
 for i in range(5):rules[f'position_{i+1}']=lambda q,i=i:value(choices(q)[i][':answer/value'])
 for label,fn in rules.items():
  stats[label]={'successes':sum(fn(r['question'])==value(key(r['question'])) for r in rows),'attempts':len(rows)}
 for sign in [-1,0,1]:
  applicable=[]
  for r in rows:
   nums=[value(a[':answer/value']) for a in choices(r['question']) if a[':answer/value']!='No solution']
   hits=[v for v in nums if (v>0)-(v<0)==sign]
   if len(hits)==1:applicable.append((r,hits[0]))
  stats['only_sign_'+str(sign)]={'successes':sum(v==value(key(r['question'])) for r,v in applicable),'attempts':len(applicable)}
 return stats

def witnesses(rows,level):
 output=[]
 for sid in sorted({profile(r) for r in rows}):
  matches=[]
  for (s,prefix,bank),items in groups(rows).items():
   if s!=sid:continue
   expected={value(v) for v in bank if level=='moderate' or v!='No solution'}
   actual={verify(r) for r in items}
   if expected<=actual:
    matches.append({'visible_prompt_prefix':prefix,'ordered_bank':bank,'distinct_correct_values':sorted(map(str,actual)),'eligible_role_count':len(expected),'record_ids':[r['question'][':question/id'] for r in items],'probes':probe(items),'answers_occupy_multiple_positions':len({next(i for i,a in enumerate(choices(r['question'])) if a[':answer/value']==key(r['question'])) for r in items})>1})
  assert matches,('No full-role fixed-bank witness survives',level,sid)
  output.append({'profile':sid,'full_role_witness':matches[0]})
 return output

coverage={};all_accepted=[];selection=[]
for level in ['easy','moderate']:
 raw=json.loads((E/f'delivery-input-{level}.json').read_text())
 accepted=json.loads((E/f'delivery-{level}/accepted.json').read_text());all_accepted+=accepted
 for r in accepted:verify(r)
 before=witnesses(raw,level);after=witnesses(accepted,level)
 coverage[level]={'delivery_counts':json.loads((E/f'delivery-{level}/delivery.json').read_text()),'before_full_role_witnesses':before,'after_full_role_witnesses':after,'all_before_probes':probe(raw),'all_after_probes':probe(accepted)}
 # Faithful same-band select() reproduction: numeric ID order is unknown before
 # publication, so explicitly assign synthetic IDs by UUID order.
 ordered=sorted(accepted,key=lambda r:r['question'][':question/id'])
 for scenario,pool in [('no_history',ordered),('exclude_first_half',ordered[len(ordered)//2:])]:
  draws=[]
  for i in range(32):
   seed=f'task-{i+1}/kp-17592186119805/slot-0'
   d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
   u=(int.from_bytes(d[8:16],'big')>>11)/(1<<53)
   r=pool[int(u*len(pool))];draws.append({'question_id':r['question'][':question/id'],'answer':str(verify(r)),'old_shortcut_succeeded':old_shortcut(r['question'])==value(key(r['question']))})
  assert not all(d['old_shortcut_succeeded'] for d in draws)
  if level=='moderate':assert {'scalar','contradiction'}=={'contradiction' if d['answer']=='No solution' else 'scalar' for d in draws}
  selection.append({'band':level,'scenario':scenario,'pool_count':len(pool),'draws':draws,'old_shortcut_successes':sum(d['old_shortcut_succeeded'] for d in draws)})
batch=json.loads((E/'delivery-batch/accepted.json').read_text());all_accepted+=batch
for r in batch:verify(r)
coverage['replacement_batch']={'count':len(batch),'probes':probe(batch),'comparison':'Original exact five: 5/5 success for retained shortcut; repaired five measured here.'}
save('pedagogical-variation.json',{'passed':True,'coverage':coverage,'tested_cues':['recognizable source profile','label and equation wording','zero right-hand side','complete ordered visible bank','numeric rank','unique sign','zero option','choice position'],'reasoning':'For every source profile an entire fixed visible bank retains every eligible correct role after delivery; only the displayed vector evidence changes. Fixed-bank witness keys and residuals were independently parsed. Normal sampler role controls separately demonstrate each role is reachable via its ordinary construction. No position shuffle is used as the sole variation.','limits':['Easy source band has unique solutions: text No solution remains a distractor. Numeric roles all vary.','Sparse incidental subgroups in the ordinary sample cannot support a universal statistical claim. Controlled full-bank witnesses and normal sampler independence establish the tested role coverage.','No claim to enumerate every possible human shortcut.']})
save('selection-results.json',{'rules':'engine/rust/question_selection.rs lines 105–200: freshness exclusion; sorted numeric candidate IDs; weighted nonempty band draw; second SHA256 53-bit uniform chooses member. Same-band positive weights reduce to uniform member selection.','scenarios':selection,'limits':['Synthetic numeric ordering assigned by UUID, not actual unpublished entity IDs.','No live learner history or policy weights captured. Two assumed freshness scenarios only.','A zero-weight band is never served; arbitrary future history could leave a single answer role.','The unconfigured legacy policy picks first candidate, so no uniform-selection claim is made for that policy.']})
# Test actual normalized IDs/banks, not only the pre-delivery authored identities.
cases=[]
for i,r in enumerate(all_accepted):
 ans=verify(r)
 cases.append({'label':f'delivered-{i}','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if value(a[':answer/value'])==ans else 'rejected','purpose':'Post-delivery normalized radio identity; independent equation witness'} for a in choices(r['question'])]})
save('grader-delivered-input.json',cases)
print(json.dumps({'conditional_profiles_passed':{level:len(coverage[level]['after_full_role_witnesses']) for level in ['easy','moderate']},'replacement_batch_old_shortcut':coverage['replacement_batch']['probes']['old_label_bank_strategy'],'delivered_grader_cases':len(cases),'selection_scenarios':len(selection)}))
