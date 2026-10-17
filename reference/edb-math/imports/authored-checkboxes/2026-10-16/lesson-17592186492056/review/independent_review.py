from pathlib import Path
import hashlib,importlib.util,json,re
from collections import Counter
from scripts.database.edn import loads
from sympy import symbols,Poly,simplify
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
R=Path(__file__).resolve().parents[1]
qs=[r[0] for r in loads((R/'evidence/questions.edn').read_text())]
items=loads((R/'evidence/items.edn').read_text())
scope=loads((R/'evidence/scope.edn').read_text())[0][0]
x=symbols('x')
labels=['I','II','III']
decisions=[]
def hashfile(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def subset(t):return re.findall(r'\b(?:III|II|I)\b',t)
for q in qs:
 fields=q.get(':question/answer-fields',[])
 types=sorted(set(f[':answer-field/type'][':db/ident'] for f in fields))
 d={'question_eid':q[':db/id'],'math_academy_id':q.get(':question/math-academy-id'),'kp_ids':[p[':db/id'] for p in q.get(':knowledge-point/_questions',[])],'canonical_kp_ids':[p[':db/id'] for p in q.get(':knowledge-point/_canonical-example',[])],'field_types':types,'field_count':len(fields),'problem_sha256':hashlib.sha256(q[':question/problem'].encode()).hexdigest()}
 if not fields:
  assert d['canonical_kp_ids']
  d.update(decision='retain_canonical_example',reason='Expository canonical example has no interactive answer fields to migrate; preserve lesson content.')
 elif types==[':answer-field.type/checkbox']:
  d.update(decision='retain_checkbox',reason='Finite subset task already has one independently keyed Boolean checkbox per equation.')
 elif types==[':answer-field.type/radio'] and q[':question/problem'].startswith('Which of the following equations'):
  assert len(fields)==1
  d.update(decision='convert',reason='The finite universe comprises three independently testable linear equations; combination radio answers encode selected subsets.')
  f=fields[0]
  d['old_field_eid']=f[':db/id']
  d['old_choices']=[{'answer_eid':a[':db/id'],'value':a[':answer/value'],'subset':subset(a[':answer/value'])} for a in f[':answer-field/choices']]
  d['key_eid']=f[':answer-field/correct'][':db/id']
  assert d['key_eid'] in [a['answer_eid'] for a in d['old_choices']]
  d['database_key_subset']=subset(f[':answer-field/correct'][':answer/value'])
  d['worked_solution_key_agrees']=q[':question/worked-solution'].endswith('Therefore, the correct answer is "'+f[':answer-field/correct'][':answer/value']+'."')
  assert d['worked_solution_key_agrees']
  d['difficulty']=q[':question/difficulty'][':db/ident']
  d['feedback_attributes']=[{'entity':a.get(':db/id'),'attribute':k,'value':v} for a in [q,f]+f[':answer-field/choices'] for k,v in a.items() if 'feedback' in k]
  assert not d['feedback_attributes']
  d['saved_task_items']=[row[1] for row in items if row[0]==q[':db/id']]
  d['worked_solution_disposition']='Preserve unchanged: mathematics and statement that the correct subset is I (or I and II) remain valid for checkboxes.'
 else:
  assert types in [[':answer-field.type/radio'],[':answer-field.type/blank']]
  assert 'what is the value of' in q[':question/problem']
  d.update(decision='retain_radio' if 'radio' in types[0] else 'retain_blank',reason='Question requests one numerical parameter or one scalar sum, not selection from independently testable cases.')
  if any(':answer-field/correct' not in f for f in fields):d['separate_incomplete_capture']='Existing field has no correct key; no checkbox conversion or completion repair is appropriate in this migration.'
 if d['decision'] in ['convert','retain_checkbox'] or (d['decision']=='retain_canonical_example' and 'Which of the following' in q[':question/problem']):
  equations=re.findall(r'(?:\*\*)?\b(III|II|I)\.(?:\*\*)?\s*\$([^$]+)\$',q[':question/problem'])
  assert [label for label,equation in equations]==labels,(q[':db/id'],equations)
  universe=[]
  for label,equation in equations:
   left,right=equation.split('=')
   expr=lambda t:parse_expr(t,local_dict={'x':x},transformations=standard_transformations+(implicit_multiplication_application,))
   difference=simplify(expr(left)-expr(right));identity=difference==0
   universe.append({'label':label,'equation':equation,'lhs_minus_rhs':str(difference),'infinitely_many_solutions':bool(identity),'proof':'LHS minus RHS is identically zero.' if identity else 'LHS minus RHS is a nonzero constant, so there are no solutions.' if not difference.has(x) else 'LHS minus RHS has nonzero x coefficient, so there is exactly one solution.'})
  d['universe']=universe
  expected=[u['label'] for u in universe if u['infinitely_many_solutions']]
  d['independent_true_subset']=expected
  if d['decision']=='convert':assert d['database_key_subset']==expected
  elif d['decision']=='retain_checkbox':
   assert len(fields)==3
   actual=[]
   for f in fields:
    assert {a[':answer/value'] for a in f[':answer-field/choices']}=={'false','true'}
    assert f[':answer-field/correct'][':db/id'] in [a[':db/id'] for a in f[':answer-field/choices']]
    if f[':answer-field/correct'][':answer/value']=='true':actual.append(f[':answer-field/key'])
   assert sorted(actual)==sorted(expected)
   d['database_key_subset']=actual
 decisions.append(d)
generator=Path('generate/scratch/17592186110719.py')
spec=importlib.util.spec_from_file_location('independent_generator_review',generator)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
samples=[]
for level in ['easy','moderate','hard']:
 for profile in mod.BANKS:
  record=mod.generate(level=level,seed=0,profile=profile)
  samples.append({'level':level,'profile':profile,'field_types':[f[':answer-field/type'] for f in record['question'][':question/answer-fields']]})
assert all(s['field_types']==[':answer-field.type/radio'] for s in samples)
report={'reviewer':'/root/checkbox_lesson_review','capture':json.loads((R/'capture-identity.json').read_text()),'scope':{'topic_eid':scope[':db/id'],'topic_title':scope[':topic/title'],'kp_count':len(scope[':topic/knowledge-points']),'questions_including_canonical':len(qs),'practice_questions':sum(bool(q.get(':knowledge-point/_questions')) for q in qs),'canonical_examples':sum(bool(q.get(':knowledge-point/_canonical-example')) for q in qs)},'evidence_hashes':{name:hashfile(R/'evidence'/name) for name in ['scope.edn','questions.edn','items.edn']},'summary':dict(Counter(d['decision'] for d in decisions)),'convert_ids':[d['question_eid'] for d in decisions if d['decision']=='convert'],'decisions':decisions,'generator_follow_up':{'kp_eid':17592186110719,'script':str(generator),'sha256':hashfile(generator),'version':mod.VERSION,'source_snapshot':mod.SOURCE,'behavior':'Radio-only combination banks; code accepts radio and rejects checkbox. Twelve generated samples across all difficulties and profiles remain radio. A later invocation can reintroduce radios.','samples':samples,'historical_registration_evidence':'generate/scratch/17592186110719/reference/replenishment/basis-1837/commit-intent.json','status':'Flagged for separate generator refresh; no generator or database writes made during this independent review.'}}
(R/'review/independent-review.json').write_text(json.dumps(report,indent=2,default=str)+'\n')
print(json.dumps({'summary':report['summary'],'scope':report['scope'],'convert_ids':report['convert_ids'],'generator_version':mod.VERSION}))
