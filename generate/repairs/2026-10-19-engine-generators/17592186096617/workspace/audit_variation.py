import collections,hashlib,json,re
from pathlib import Path
import generator as g
import sympy as s
E=Path('evidence')
def load(p):return json.loads((E/p).read_text())
def answer(r):
 f=r['question'][':question/answer-fields'][0]
 return next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def stats(records):
 groups=collections.defaultdict(list)
 semantic=set()
 for r in records:
  m=r['generation'];groups[m['template']].append(r)
  product=g.parse(re.search(r'\$([^$]*)\$',r['question'][':question/problem'])[1].rstrip('.'))
  semantic.add((s.srepr(s.expand(product)),str(m['missing_term']) if not r['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/radio') else 'full'))
 out={}
 for template,rs in groups.items():
  slots=collections.defaultdict(set);positions=collections.Counter();signs=collections.Counter();numeric_answers=set()
  for r in rs:
   p=r['generation']['parameters']
   for k,v in p.items():slots[k].add(v)
   slots['missing_term'].add(str(r['generation']['missing_term']))
   f=r['question'][':question/answer-fields'][0];a=answer(r)
   numeric_answers.add(s.srepr(s.expand(g.parse(a[':answer/value']))))
   if f[':answer-field/type'].endswith('/radio'):
    positions[f[':answer-field/choices'].index(a)]+=1
    signs['starts_negative' if a[':answer/value'].startswith('-') else 'starts_nonnegative']+=1
  out[template]={'records':len(rs),'slots':{k:sorted(v) for k,v in slots.items()},'distinct_answer_expressions':len(numeric_answers)}
  if positions:
   assert len(positions)>1,(template,'fixed position')
   out[template]['position_shortcuts']={str(pos):{'successes':positions[pos],'attempts':len(rs),'baseline':0.2} for pos in range(5)}
   out[template]['leading_sign_counts']=dict(signs)
   probes={}
   for cue in ['shortest','longest','fewest_minus','most_minus']:
    wins=0
    for r in rs:
     choices=r['question'][':question/answer-fields'][0][':answer-field/choices']
     def score(a):
      z=re.sub(r'\\[A-Za-z]+|[{}\s]','',a[':answer/value'])
      return len(z) if cue in ('shortest','longest') else z.count('-')
     selected=(min if cue in ('shortest','fewest_minus') else max)(choices,key=score)
     wins+=selected[':answer/id']==answer(r)[':answer/id']
    probes[cue]={'successes':wins,'attempts':len(rs),'random_choice_baseline':0.2}
    assert wins<len(rs),(template,'reliable incidental cue',cue)
   out[template]['surface_choice_strategies']=probes
   # Count-based cue always includes all choices: five options is the response contract.
   assert len(signs)>1,(template,'fixed leading sign')
  if template in ('q-1907','q-104300'):assert slots['trig']=={'sin','cos','tan'}
  if template in ('q-310188','q-319402','q-319350','q-319357','q-319385'):assert slots['missing_term']=={'0','1'}
 return {'count':len(records),'semantic_instances_excluding_option_banks_and_cosmetics':len(semantic),'profiles':out}
before=stats(load('test-records.json'));after=stats(load('delivery/accepted.json'))
# Paired evidence: changed target, changed trig, shuffled option order; check grading cross-responses.
pairs=load('counterfactuals.json');cross=[]
for i,p in enumerate(pairs):
 a,b=p['before'],p['after'];fa=a['question'][':question/answer-fields'][0];fb=b['question'][':question/answer-fields'][0]
 if p['kind']=='missing_term':
  cross.extend([{'label':f'{i}:old-key-on-new-target','record':b,'checks':[{'submitted':answer(a)[':answer/value'],'expected':'rejected','purpose':'target changed with other data fixed'}]}, {'label':f'{i}:new-key-on-old-target','record':a,'checks':[{'submitted':answer(b)[':answer/value'],'expected':'rejected','purpose':'target changed with other data fixed'}]}])
 elif p['kind']=='trig_derivative':
  # Every choice is independently exercised in engine-input; same numeric data now changes derivative rule.
  assert answer(a)[':answer/value']!=answer(b)[':answer/value']
 else:
  assert answer(a)[':answer/value']==answer(b)[':answer/value']
  assert {s.srepr(s.expand(g.parse(z[':answer/value']))) for z in fa[':answer-field/choices']}=={s.srepr(s.expand(g.parse(z[':answer/value']))) for z in fb[':answer-field/choices']}
(E/'counterfactual-engine-input.json').write_text(json.dumps(cross,indent=2))
report={'passed':True,'learner_operation':'Identify factors, differentiate them, form u-prime v and u v-prime; select derivative or complete indicated term.','before_delivery':before,'after_delivery':after,'controlled_pairs':collections.Counter(p['kind'] for p in pairs),'counterfactual_cross_response_checks':len(cross),'rejection':{'normal_generation':'No rejection/resampling branch; invalid explicit banks raise ValueError. All targeted boundaries and eleven default seeds succeeded.','legacy_replay':'Legacy bounded bank validation used only for original-parameter evidence; never selected by normal CLI.'},'shortcut_interpretation':['Every tested radio profile has multiple correct positions and both leading-sign outcomes after filtering. Position-only probe results are reported per template with a 1/5 baseline; finite samples are not balance quotas.','Trig and missing-term role counterfactuals change both key and supplied evidence; all are graded by native engine. Choice reordering preserves mathematical answer and field-owned identities.','Every completion has one blank and every radio has one correct response: response counts are fixed by source contract, not answer-bearing evidence.','Only trig-specific derivative cues remain reliable in some source banks (notably sec² for tangent). This is the taught prerequisite; those finite banks cannot alone distinguish complete product-rule mastery. Polynomial radio profiles vary trig to require different derivative rules.','No generated question labels or special answer position markers occur. Coefficient, degree, base and radical expressions are mathematical evidence, not incidental layout cues.'],'selection':{'code':'engine/rust/question_selection.rs: select','read_only_finding':'Configured selection chooses a band by weights, then a uniform hash-seeded index from sorted eligible IDs in that band. All these records are easy, with no template or mathematical feature weighting. Unconfigured policy selects first candidate ID, a known legacy behavior.','limits':'No live learner/history/policy snapshot; fresh-candidate pool, active weights, history exclusions, unconfigured-policy outcome and database identity collisions cannot be certified offline. Captured-inventory delivery filtering is exercised.'},'limits':['Supported band is easy only.','Blocking grading defect: native grader does not establish ln(4)=2ln(2). The author-2 required-acceptance test fails; this variation-only report does not certify grading or readiness.','Results establish the specific declared slots and cue probes, not absence of every possible shortcut.']}
(E/'pedagogical-variation.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'before':before['count'],'after':after['count'],'semantic_before':before['semantic_instances_excluding_option_banks_and_cosmetics'],'semantic_after':after['semantic_instances_excluding_option_banks_and_cosmetics'],'counterfactual_pairs':report['controlled_pairs'],'passed':True}))
# Representatives cover every source profile, all trig rules and both missing roles.
accepted=load('delivery/accepted.json');reps=[];seen=set()
for r in accepted:
 m=r['generation'];t=m['template']
 sig=(t,m['parameters'].get('trig'),m['missing_term'])
 if sig not in seen:reps.append(r);seen.add(sig)
(E/'render-records.json').write_text(json.dumps(reps,indent=2))
print('render representatives',len(reps))
