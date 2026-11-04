#!/usr/bin/env python3
"""Read-only independent visible-TeX witnesses plus purpose-sensitive regressions."""
import collections,importlib.util,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
BASE=Path(__file__).resolve().parent
AUDIT=ROOT/'reference/edb-math/audits/2026-11-04-four-trig-lessons'
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(AUDIT))
from numeric_audit import audit,field_key,Numeric,nodes,MATH
# Import only the pure checker definition: the old module's top-level report writer
# deliberately is not executed, preserving the source-capture directory read-only.
solution_scope={'__file__':str(AUDIT/'solutions_audit.py'),'__name__':'validation_helper'}
exec((AUDIT/'solutions_audit.py').read_text().split('\nresults=[]')[0],solution_scope)
check_solution=solution_scope['check']
KIDS=['17592186059665','17592186059666','17592186059821','17592186059662','17592186059663','17592186059820']

def call(kid,band,count,seed):
 argv=[sys.executable,str(BASE/kid/'generator.py'),'--difficulty',band,'--count',str(count),'--seed',str(seed),'--format','json']
 r=subprocess.run(argv,capture_output=True,text=True)
 if r.returncode:raise RuntimeError(r.stderr)
 return json.loads(r.stdout),argv

def purpose(q,kid,band):
 prompt=q[':question/problem'];errors=[]
 if kid in ('17592186059665','17592186059820'):
  if any(t in prompt for t in ('Use the formula','exact values','\\sin u','\\cos u')):errors.append('radian prompt gives assessed recall')
 if kid in ('17592186059821','17592186059662'):
  target=next(m[0] for m in MATH.finditer(prompt) if r'\cos' in m[0] or r'\sin' in m[0])
  if len(re.findall(r'\\(?:sin|cos)\s*(?:\\left)?\(',target))!=1:errors.append('more than one shifted function')
 if kid=='17592186059666':
  if not ('Using the fact' in prompt or 'Hint: Use the fact' in prompt):errors.append('missing source-supported decomposition')
  if 'reverse' in q[':question/worked-solution'].lower():errors.append('reverse identity task')
 if kid=='17592186059663':
  if band=='hard' and ('Hint:' in prompt or 'Using the fact' in prompt):errors.append('hard supplies decomposition')
  if band!='hard' and not ('Hint:' in prompt or 'Using the fact' in prompt):errors.append('source-supported split removed')
 # The printed operator between blanks must not require a negative second entry.
 if re.search(r'\\sin\s+x\s*-\$',prompt):
  f=next(f for f in q[':question/answer-fields'] if f[':answer-field/key']=='field-2')
  if Numeric(nodes(field_key(f)),{}).evaluate()<0:errors.append('decorative double negative')
 return errors

def semantic(r,kid):
 p=r['generation']['parameters']
 if kid=='17592186059665':return (p['angle_twelfths'],p['sign'])
 if kid=='17592186059820':return (p['n'],p['d'],p['operator'])
 if kid=='17592186059821':return (p['sign'],p['angle'])
 if kid=='17592186059662':return p['t']
 if kid=='17592186059666':return (p['p'],p['q'],p['s'])
 if r['question'][':question/difficulty'].endswith('hard'):return p['target']
 return (p['a'],p['b'],p['op'])

def run():
 failures=[];summary=[];results=[]
 for kid in KIDS:
  folder=BASE/kid;ev=folder/'validation';ev.mkdir(exist_ok=True)
  for band in ('easy','moderate','hard'):
   for seed in (7,31,113):
    records,argv=call(kid,band,5,seed)
    (ev/f'{band}-seed-{seed}.json').write_text(json.dumps(records,indent=2)+'\n')
    signatures=[semantic(r,kid) for r in records]
    assert len(signatures)==len(set(signatures)),(kid,band,'semantic repeat')
    for i,r in enumerate(records):
     label=f'{band}-seed-{seed}/{i}';q=r['question']
     n=audit(q,label,kid);s=check_solution(q,label,kid);p=purpose(q,kid,band)
     result={'label':label,'kp':kid,'numeric':n,'solution':s,'purpose_errors':p}
     results.append(result)
     if n['status']!='match' or n.get('choice_ambiguities') or s.get('suspected_bad_equalities') or s.get('unparsed_equalities') or p:failures.append(result)
   # Determinism uses original complete records, including IDs and banks.
   a,_=call(kid,band,5,7);b,_=call(kid,band,5,7)
   assert a==b,(kid,band,'nondeterministic')
   summary.append({'kp':kid,'band':band,'records':15,'seeded_replay':'passed'})
  own=[r for r in results if r['kp']==kid]
  (ev/'numeric-solution-results.json').write_text(json.dumps(own,indent=2)+'\n')
  # Every source/canonical prompt remains available for concrete review.
  anchors=json.loads((folder/'source-anchors.json').read_text())
  matched=[]
  for band in ('easy','moderate','hard'):
   generated=json.loads((ev/f'{band}-seed-7.json').read_text())[0]
   imports=[q for q in anchors['imports'] if (q.get(':question/difficulty') or {}).get(':db/ident','').endswith('/'+band)]
   if not imports:imports=anchors['imports']
   source=next((q for q in imports if '{{field-1}}' in q[':question/problem']),imports[0])
   matched.append({'band':band,'imported_db_id':source[':db/id'],'imported_id':source[':question/math-academy-id'],'imported_prompt':source[':question/problem'],'generated_prompt':generated['question'][':question/problem'],'generated_key':[field_key(f) for f in generated['question'][':question/answer-fields']],'canonical_prompt':anchors['canonical'][':question/problem'],'judgment':'See instructional-account.md; missing imported bands are authored overlap, not imported calibration.'})
  (ev/'source-comparisons.json').write_text(json.dumps(matched,indent=2)+'\n')
 # Independent reader negative controls: visibly wrong key and duplicate correct option.
 q=json.loads(json.dumps(call(KIDS[0],'easy',1,7)[0][0]['question']))
 f=q[':question/answer-fields'][0];correct=field_key(f)
 wrong=next(a for a in f[':answer-field/choices'] if a[':answer/value']!=correct)
 f[':answer-field/correct']=[':answer/id',wrong[':answer/id']]
 wrong_detected=audit(q,'wrong-key-negative-control',KIDS[0])['status']=='mismatch'
 q=json.loads(json.dumps(call(KIDS[0],'easy',1,7)[0][0]['question']));f=q[':question/answer-fields'][0]
 correct=field_key(f);next(a for a in f[':answer-field/choices'] if a[':answer/value']!=correct)[':answer/value']=r'1\cdot\left('+correct+r'\right)'
 ambiguous_detected=bool(audit(q,'equal-option-negative-control',KIDS[0]).get('choice_ambiguities'))
 assert wrong_detected and ambiguous_detected
 report={'summary':summary,'records':len(results),'equality_checks':sum(r['solution']['checks'] for r in results),'negative_controls':{'wrong_key_rejected':wrong_detected,'equal_valued_wrong_option_rejected':ambiguous_detected},'failures':failures,'limits':['Numeric witnesses use displayed TeX at three independent variable assignments; they do not prove every future output.','No live registration, publication or learner grading was changed.','Source captures are read-only; no imported questions were edited.','Root will do final shared rendering and independent publication review.']}
 (BASE/'validation-summary.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k not in ('summary','failures','limits')},indent=2));print('failures',len(failures))
 for f in failures[:10]:print(json.dumps(f)[:1800])
 return bool(failures)
if __name__=='__main__':sys.exit(run())
