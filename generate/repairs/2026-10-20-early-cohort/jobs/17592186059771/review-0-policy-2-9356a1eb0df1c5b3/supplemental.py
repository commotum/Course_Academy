import sys
sys.dont_write_bytecode=True
import json,pathlib,collections,hashlib,re,copy,subprocess
from fractions import Fraction as F
E=pathlib.Path(__file__).resolve().parent;J=E.parent;P=J/'workspace';R=pathlib.Path('/home/jake/Developer/Course_Academy');PY=str(R/'.venv/bin/python')
sys.path.insert(0,str(P))
import generator as g,hard

def save(n,x):(E/n).write_text(json.dumps(x,indent=2,default=str)+'\n')
def mat(s):
 body=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',s,re.S)[1]
 def v(x):
  x=x.strip();z=re.fullmatch(r'(-?)\\frac\{(\d+)\}\{(\d+)\}',x)
  return F((-1 if z[1] else 1)*int(z[2]),int(z[3])) if z else F(x)
 return [[v(x) for x in row.split('&')] for row in re.split(r'\\\\',body)]
def key(q):
 f=q[':question/answer-fields'][0];a=f[':answer-field/correct'];i=a[':answer/id'] if isinstance(a,dict) else a[1]
 return next(a for a in f[':answer-field/choices'] if a[':answer/id']==i)
def q(r):return r.get('question',r)
def classify(r):return 'swap' if '\\leftrightarrow' in q(r)[':question/problem'] or '↔' in q(r)[':question/problem'] else 'scale' if 'following row operations' not in q(r)[':question/problem'] and len(re.findall(r'\{R\}',q(r)[':question/problem']))==2 else 'addition'
def probe(rs):
 out={}
 for label,strategy in [('first_position',lambda ms:0),('largest_norm',lambda ms:max(range(5),key=lambda i:sum(abs(v) for row in ms[i] for v in row))),('smallest_norm',lambda ms:min(range(5),key=lambda i:sum(abs(v) for row in ms[i] for v in row))),('most_zero_entries',lambda ms:max(range(5),key=lambda i:sum(v==0 for row in ms[i] for v in row)))]:
  correct=0
  for r in rs:
   question=q(r);field=question[':question/answer-fields'][0];choices=field[':answer-field/choices'];mats=[mat(a[':answer/value']) for a in choices];i=strategy(mats)
   correct+=choices[i][':answer/id']==key(question)[':answer/id']
  out[label]={'correct':correct,'total':len(rs),'baseline':.2,'tie_rule':'first displayed choice'}
 return out
inv=json.load(open(J/'source/inventory.json'));raw=json.load(open(E/'easy-records.json'));accepted=json.load(open(E/'delivery-control/accepted.json'));batch=json.load(open(E/'batch-records.json'));ab=json.load(open(E/'delivery-batch/accepted.json'))
probes={}
for stage,records in [('raw',raw),('accepted',accepted),('batch_raw',batch),('batch_accepted',ab)]:
 probes[stage]={'overall':probe(records)}
 for kind in ['swap','scale']:
  group=[r for r in records if classify(r)==kind]
  if group:probes[stage][kind]=probe(group)
 for profile in sorted(set(r.get('generation',{}).get('profile','normalized') for r in records)):
  group=[r for r in records if r.get('generation',{}).get('profile','normalized')==profile]
  probes[stage]['profile:'+profile]=probe(group)
save('shortcut-results.json',probes)
# Exact read-only translation of select() conditional on a positive easy weight.
# Unknown live phase weights/history are not invented; this tests the captured easy band.
existing=[x for x in inv['questions'] if x[':question/difficulty'][':db/ident'].endswith('/easy')]
def select(ids,seed):
 ids=sorted(set(ids));digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53)
 return ids[int(u*len(ids))]
counts=collections.Counter(select([x[':db/id'] for x in existing],str(i)) for i in range(256))
save('selection-results.json',{'source':'engine/rust/question_selection.rs select and seen_before_task; inspected 2026-10-21','captured_basis':inv['basis'],'existing_easy_candidates':[{'entity_id':x[':db/id'],'question_id':x[':question/id'],'kind':classify(x),'draws':counts[x[':db/id']]} for x in existing],'trials':256,'conditional_assumption':'Fresh unseen usable easy band selected with positive easy weight. Uniform hash choice within sorted entity IDs; no label/profile/answer dependence.','batch_pool':{'new_accepted':len(ab),'kind_counts':dict(collections.Counter(classify(r) for r in ab)),'prospective_easy_counts_including_inventory':dict(collections.Counter(classify(r) for r in existing+ab))},'limits':['Actual policy weights and learner histories were not captured; cannot certify a particular live learner sequence.','Batch has no assigned database entity IDs, so exact future hashed draws are unavailable. Uniform within-band rule and prospective category counts remain inspectable.','All five batch items are swaps; this is a small source-supported swap practice pool, not evidence of scaling coverage. The larger accepted control includes scaling.']})
# Explicit minimal hard same-target restriction reproducer.
p={'matrix':[[1,2,3],[4,5,6],[7,8,9]],'target':0,'donors':[1,2],'coefficients':[2,1],'candidate_pairs':[[2,1],[1,1],[-1,1],[2,2],[1,2]],'name':'C'}
base=hard.generate(614, p)
# The source-supported source role pattern is explicitly requested; current API has no operations slot.
distinct={**p,'operations':[[0,1,2],[2,1,1]]}
ignored=hard.generate(614,distinct)
save('hard-restriction-records.json',[base,ignored]);save('hard-restriction-results.json',{'command':PY+' -B supplemental.py','requested_operations':distinct['operations'],'delivered_prompt':ignored['question'][':question/problem'],'expected_result':[[9,12,15],[4,5,6],[11,13,15]],'actual_key':key(ignored['question'])[':answer/value'],'source_families':['q-130064','q-130065','q-10245'],'rule':'hard.operations always emits p[target] twice, donors is a permutation of other two rows; no production branch for two destinations.'})
# No affected inventory instance can demonstrate the absence of a generator family.
# Inspect inventory for which source families it contains and retain exact captured data.
save('inventory-inspection.json',{'basis':inv['basis'],'captured_questions':len(inv['questions']),'original_source_questions':sum(':question/math-academy-id' in x for x in inv['questions']),'remaining_records':sum(':question/math-academy-id' not in x for x in inv['questions']),'generation_metadata_captured':False,'assessment':'Demonstrated failures are missing replay/bank support and absent production role family. These are construction omissions, not erroneous existing generated records; no stored item has been demonstrated defective. Original sources are not marked generated.','limits':'No claim that all 16 non-source inventory records are defect-free; no reproduction with matching generation metadata supplied by capture.'})
save('affected-inventory.json',{'affected_questions':[]})
(E/'session-state.md').write_text('Completed: source reconstruction, 199 exact-math record checks, 9/11 source-bank replays (2 unsupported), 95 native grader outcomes, delivery 60/60 control and 5/5 batch, deterministic replay/relocation/rejection checks. Supplemental shortcut and captured selection checks saved. Counterfactual actual-UI rendering in progress. Package files unchanged.\n')
print(json.dumps({'shortcut_batch':probes['batch_accepted'],'inventory_easy':len(existing),'hard_restriction':'distinct target request ignored; complete generated records retained'},default=str))
