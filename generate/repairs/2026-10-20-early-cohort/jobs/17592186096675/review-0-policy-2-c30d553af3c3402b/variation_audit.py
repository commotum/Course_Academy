import audit as a
import json,hashlib,collections,itertools,sys
from pathlib import Path
E=a.E;g=a.g;s=a.s
save=a.save
src=json.load(open(a.B/'source/source.json'));qs=src['material']['kp'][':knowledge-point/questions'];inv=json.load(open(a.B/'source/inventory.json'))
controls=[g.generate(seed=901100+i*17+role,template=q[':question/math-academy-id'],parameters={'answer_role':role,'translation':[0,0,0]}) for i,q in enumerate(qs) for role in range(5)]
save('role-controls.json',controls)
save('role-control-math.json',[a.check(r) for r in controls])
# Reconstruct the 5 stored non-source questions without inventing provenance/seed.
# Stable generator identity is seed-independent; seed below is our reproduction seed.
source_ids={q[':question/id'] for q in qs};repro=[];inventory_results=[]
for q in inv['questions']:
 storedA=a.parse_problem(q[':question/problem']);stored_bank=[a.vec(c[':answer/value']) for c in q[':question/answer-fields'][0][':answer-field/choices']];matches=[]
 if q[':question/id'] not in source_ids:
  for source in qs:
   mid=source[':question/math-academy-id'];A=a.parse_problem(source[':question/problem'])
   if A[:,:3]!=storedA[:,:3]:continue
   scale=2 if mid=='q-10644' else 1
   sv=[a.vec(c[':answer/value']) for c in source[':question/answer-fields'][0][':answer-field/choices']]
   for v in stored_bank:
    t=v-scale*sv[0]
    if any(x.q!=1 or abs(x)>3 for x in t):continue
    bank=[scale*u+t for u in sv]
    if sorted(map(str,bank))!=sorted(map(str,stored_bank)):continue
    role=next(j for j,u in enumerate(bank) if u==a.vec(a.correct(q)[':answer/value']))
    r=g.generate(seed=600021,template=mid,parameters={'translation':list(map(int,t)),'answer_role':role})
    eqid=r['question'][':question/id']==q[':question/id']
    checks=a.check(r)
    matches.append({'template':mid,'parameters':r['generation']['parameters'],'question_id_matches':eqid,'same_prompt':r['question'][':question/problem']==q[':question/problem'],'same_worked':r['question'][':question/worked-solution']==q[':question/worked-solution'],'bank_values_match':sorted(c[':answer/value'] for c in r['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(c[':answer/value'] for c in q[':question/answer-fields'][0][':answer-field/choices']),'checks':checks,'reproduction_seed':600021,'stored_seed':'not captured in inventory'})
    if eqid:repro.append(r)
 inventory_results.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'original_source':q[':question/id'] in source_ids,'mathematical_key_correct':a.vec(a.correct(q)[':answer/value'])==storedA.rref()[0][:,3],'reconstruction':matches})
save('generated-records.json',repro);save('inventory-results.json',inventory_results)
save('affected-inventory.json',{'affected_questions':[]})

# All bank-only strategies use visible choice contents and deterministic tie breaks.
def features(r):
 q=r['question'];cs=q[':question/answer-fields'][0][':answer-field/choices'];vs=[a.vec(c[':answer/value']) for c in cs]; ix=cs.index(a.correct(q));return cs,vs,ix

def pred(r,strategy):
 cs,vs,ix=features(r);q=r['question']
 if strategy.startswith('position '):return int(strategy.split()[-1])-1
 ordered=sorted(range(5),key=lambda i:tuple(vs[i]))
 if strategy=='lexicographic minimum':return ordered[0]
 if strategy=='lexicographic maximum':return ordered[-1]
 if strategy=='coordinatewise modes':
  modes=[collections.Counter(v[j] for v in vs).most_common()[0][0] for j in range(3)]
  scored=[sum(v[j]==modes[j] for j in range(3)) for v in vs]
  return next(i for i in ordered if scored[i]==max(scored))
 if strategy=='closest to zero':return min(ordered,key=lambda i:sum(x*x for x in vs[i]))
 if strategy=='first equation only':
  m=a.parse_problem(q[':question/problem']);passing=[i for i in ordered if (m[0,:3]*vs[i])[0]==m[0,3]]
  return passing[0]

def measure(name,rr,path,scope='overall'):
 out=[]
 for strategy in ['position 1','position 2','position 3','position 4','position 5','lexicographic minimum','lexicographic maximum','coordinatewise modes','closest to zero','first equation only']:
  correct=sum(pred(r,strategy)==features(r)[2] for r in rr)
  out.append({'subgroup':name,'scope':scope,'strategy':strategy,'correct':correct,'total':len(rr),'baseline':.2,'sample_refs':[path],'disposition':'intended_skill' if strategy=='first equation only' else 'not_predictive','conclusion':('Candidate substitution uses actual coefficients and constants; a mathematical alternative to elimination, not an incidental layout cue.' if strategy=='first equation only' else 'Compared with random choice success 1/5. No bank-only rule is invariant across all five fixed-bank answer roles. Small batch fluctuations are reported without treating them as universal predictors.')})
 return out
allprobes=[]
for n,fn in [('role controls','role-controls.json'),('runner actual raw','runner-batch.json'),('fresh batch raw','fresh-batch.json')]:
 rr=json.load(open(E/fn));allprobes+=measure(n,rr,fn)
 if n=='role controls':
  for mid in g.QUESTIONS:allprobes+=measure(mid,[r for r in rr if r['generation']['template']==mid],fn,'within_template')
 if n=='runner actual raw':
  for shape in ['matrix','vector']:
   group=[r for r in rr if ('then solve' in r['question'][':question/problem'])==(shape=='vector')]
   allprobes+=measure('runner '+shape,group,fn,'other_recognizable_subgroup')
save('shortcut-results.json',allprobes)

# Source canonical is instructional evidence, not a practice radio record.
canon=src['material']['kp'][':knowledge-point/canonical-example'];m=a.mats(canon[':question/worked-solution'])
save('scope-results.json',{'source_canonical_id':canon[':question/id'],'canonical_initial_matrix':m[0].tolist() if False else str(m[0]),'canonical_exact_rref':str(m[0].rref()[0]),'canonical_has_answer_fields':':question/answer-fields' in canon,'canonical_profile_supported':canon.get(':question/math-academy-id') in g.QUESTIONS,'interpretation':'Canonical example supplies the same three-pivot elimination method and optional solution reading; it has no captured answer field/bank. The explicit replay API covers all 14 practice profiles; the canonical coefficient matrix is not a separate exposed profile. Singular cases are later, separate KPs.','sample_size':len(controls),'coefficient_profiles':14,'fixed_coefficient_rationale':'A conservative finite family preserves source arithmetic and row-operation workload. Unlike fixing the correct source bank role, fixing a coefficient profile does not fix which choice is correct: all five roles are tested with exactly the same A and unordered bank. This review does not require every nonsingular coefficient matrix.','changes_in_scope':['signed and zero RHS','different solution sign/zero components','all 5 source-bank roles','common integer translations','integer scaling of q-10644 bank to avoid fractional final entries'],'unsupported':['easy','hard','singular/free-variable systems','arbitrary coefficient matrices','separate canonical e-4710 replay profile'],'math_results':'math-results.json','role_control_results':'role-control-math.json'})
# Append controls to a single aggregate native-grader invocation, also test source canonical math guide.
cases=json.load(open(E/'grader-input.json'))
for i,r in enumerate(controls):
 q=r['question'];v=a.parse_problem(q[':question/problem']).rref()[0][:,3]
 cases.append({'label':'role-control:'+str(i),'record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if a.vec(c[':answer/value'])==v else 'rejected','purpose':'fixed-bank controlled answer role'} for c in q[':question/answer-fields'][0][':answer-field/choices']]})
save('grader-input.json',cases)
render=json.load(open(E/'render-records.json'));pairs=json.load(open(E/'counterfactual-records.json'));render+=pairs[3:6];save('render-records-vector-pair.json',pairs[3:6])
print(json.dumps({'controls':len(controls),'control_math_failures':sum(bool(a.check(r)['errors']) for r in controls),'stored_generated_reproduced':len(repro),'inventory_math_failures':[x['question_id'] for x in inventory_results if not x['mathematical_key_correct']],'inventory_matching':[(x['question_id'],[m['question_id_matches'] for m in x['reconstruction']]) for x in inventory_results if not x['original_source']],'bank_rule_role_control_counts':[(x['strategy'],x['correct'],x['total']) for x in allprobes if x['subgroup']=='role controls'],'native_cases':len(cases)}))
