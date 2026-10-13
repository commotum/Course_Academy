#!/usr/bin/env python3
"""Independent displayed-array, ordered-dimension, fidelity and native QA."""
from pathlib import Path
import collections,copy,hashlib,importlib.util,json,re,subprocess,uuid
import sympy as sp
import sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
source=json.loads((HERE/'source.json').read_text())
sources={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
cases=json.loads((HERE/'source-cases.json').read_text())
def require(x,why):
 if not x:raise AssertionError(why)
def dimensions(prompt):
 arrays=re.findall(r'\\begin\{(?:aligned|bmatrix)\}(.*?)\\end\{(?:aligned|bmatrix)\}',prompt,re.S)
 require(len(arrays)==1,'One displayed matrix')
 rows=[[s.strip() for s in row.split('&')] for row in arrays[0].split(r'\\')]
 require(len({len(row) for row in rows})==1 and all(all(row) for row in rows),'Rectangular nonempty displayed matrix')
 return len(rows),len(rows[0]),rows

def pair(value):
 m=re.fullmatch(r'(\d+)\s*\\(?:times|cdot)\s*(\d+)',value)
 require(m is not None,'Ordered-dimension notation')
 return int(m[1]),int(m[2])

def formatting(s):
 require(s.count('$')%2==0,'Balanced dollars')
 depth=0
 for c in s:
  if c=='{':depth+=1
  elif c=='}':depth-=1
  require(depth>=0,'Balanced TeX groups')
 require(depth==0,'Balanced TeX groups')
 require('@ARRAY@' not in s and '@NAME@' not in s,'No leaked mask')

def independent(rec):
 require(set(rec['knowledge_point'])=={'db_id','id','title'},'Plain outer KP keys')
 require(rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE},'KP identity')
 q=rec['question'];gen=rec['generation'];r,c,rows=dimensions(q[':question/problem'])
 require(2<=r<=6 and 2<=c<=6,'Scope excludes sibling one-row/column')
 for s in (q[':question/problem'],q[':question/worked-solution']):formatting(s)
 uuid.UUID(q[':question/id'])
 match=re.fullmatch(r'The matrix \$([A-Z])\$ has \$(\d+)\$ rows and \$(\d+)\$ columns\. Therefore, its dimensions are \$(\d+)\\times (\d+)\.\$',q[':question/worked-solution'])
 require(match is not None and tuple(map(int,match.groups()[1:]))==(r,c,r,c),'All displayed row/column/solution statements')
 name=re.search(r'\$([A-Z])',q[':question/problem'])[1]
 raw_anomaly=gen['bank_profile']=='observed-q-139406'
 require(match[1]==name or raw_anomaly and name=='P' and match[1]=='R','Solution matrix label')
 kind=q[':question/answer-fields'][0][':answer-field/type'].split('/')[-1]
 require(len(q[':question/answer-fields'])==(1 if kind=='radio' else 2),'Field layout')
 for f in q[':question/answer-fields']:
  uuid.UUID(f[':answer-field/id']);key=f[':answer-field/key'];answers=f[':answer-field/choices'];correct=f[':answer-field/correct']
  require(correct[0]==':answer/id' and correct[1] in [a[':answer/id'] for a in answers],'Owned correct lookup')
  require(len(set(a[':answer/id'] for a in answers))==len(answers),'Unique owned answer IDs')
  require(all(a[':answer/type']==':answer.type/math' and '$' not in a[':answer/value'] for a in answers),'Answer value shape')
  if kind=='radio':
   vals=[pair(a[':answer/value']) for a in answers]
   require(len(vals)==5 and len(set(vals))==5,'Complete unequal ordered bank')
   require(vals.count((r,c))==1 and next(pair(a[':answer/value']) for a in answers if a[':answer/id']==correct[1])==(r,c),'Exactly one correct ordered dimensions')
   require(all(1<=x<=8 and 1<=y<=8 for x,y in vals),'Plausible dimension options')
  else:
   require('{{'+key+'}}' in q[':question/problem'],'Blank placeholder')
   require(len(answers)==1 and sp.Integer(answers[0][':answer/value'])==(r if key=='field-1' else c),'Actual displayed blank entry')
 # Incidental entries cannot inflate the assessed task identity.
 require(gen['parameter_fingerprint']==g.digest({'rows':r,'columns':c}),'Meaningful task fingerprint')
 fields=q[':question/answer-fields']
 expected=g.digest({'version':g.VERSION,'prompt':q[':question/problem'],'solution':q[':question/worked-solution'],'fields':[(f[':answer-field/key'],kind,sorted(a[':answer/value'] for a in f[':answer-field/choices'])) for f in fields]})
 require(expected==gen['content_fingerprint'] and g.uid(expected)==q[':question/id'],'Displayed-content identity')
 return r,c

def fidelity(src,rec):
 q=rec['question'];require(q[':question/problem']==src[':question/problem'],'Full exact source prompt/layout')
 fields=q[':question/answer-fields'];original=src[':question/answer-fields']
 require([f[':answer-field/key'] for f in fields]==[f[':answer-field/key'] for f in original],'Source field ordering')
 for of,f in zip(original,fields):
  require(f[':answer-field/type']==of[':answer-field/type'][':db/ident'],'Source field type')
  require(collections.Counter(a[':answer/value'] for a in f[':answer-field/choices'])==collections.Counter(a[':answer/value'] for a in of[':answer-field/choices']),'Whole original bank exact')
  if ':answer-field/correct' in of:
   require(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'],'Original designation match')
 if ':question/worked-solution' in src:require(q[':question/worked-solution']==src[':question/worked-solution'],'Full source solution sentence and stages')

def actual_array(problem):
 return dimensions(problem)[2]

structural=independent

def checks(record):
 result=[]
 for i,f in enumerate(record['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('/radio'):
   result.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Owned choice grading; ordered dimensions independently verified'} for a in f[':answer-field/choices'])
  else:
   v=f[':answer-field/choices'][0][':answer/value']
   result.extend({'field_index':i,'submitted':x,'expected':e,'purpose':'Canonical/equivalent/wrong row or column count'} for x,e in [(v,'accepted'),('('+v+'+2)-2','accepted'),(str(int(v)+1),'rejected')])
 return result

def main():
 originals=[];details=[];review=[];engine=[];counts={'bank_values':0,'source_fields':0,'correct_designations':0,'solutions_exact':0}
 for case in cases:
  rec=g.generate(case['level'],parameters=case['parameters'],template=case['template'],profile=case['bank_profile']);independent(rec);fidelity(sources[case['source_id']],rec);originals.append(rec)
  src=sources[case['source_id']];counts['bank_values']+=sum(len(f[':answer-field/choices']) for f in src[':question/answer-fields']);counts['source_fields']+=len(src[':question/answer-fields']);counts['correct_designations']+=sum(':answer-field/correct' in f for f in src[':question/answer-fields']);counts['solutions_exact']+=(':question/worked-solution' in src)
  # Each observed bank/layout receives a changed-entry variant through normal recipes.
  p=copy.deepcopy(case['parameters']);p['name']='B';p['entries'][0][0]='8' if p['entries'][0][0]!='8' else '7'
  variant=g.generate('easy',seed=15,template=case['template'],parameters=p,profile=case['bank_profile']);independent(variant);review.append(variant)
  details.append({'source_id':case['source_id'],'prompt_exact':True,'complete_bank_exact':True,'correct_designations_matched':sum(':answer-field/correct' in f for f in src[':question/answer-fields']),'missing_keys_inferred':case['source_id'] in ('q-11454','q-7806'),'worked_solution_exact':':question/worked-solution' in src,'raw_solution_label_anomaly':case['source_id']=='q-139406'})

 # Exhaust the finite easy domain and both native response layouts.
 tasks={};profile_domains={};all_default=[]
 for level in g.SUPPORTED_LEVELS:
  fingerprints=set()
  for r in range(2,7):
   for c in range(2,7):
    p={'name':'A','entries':[[str((i*3+j)%7-3) for j in range(c)] for i in range(r)]}
    for kind in ('radio','blank'):
     rec=g.generate(level,parameters=p,field_type=kind);independent(rec);all_default.append(rec);fingerprints.add(rec['generation']['parameter_fingerprint'])
     require(rec['question'][':question/id']==g.generate(level,seed=999,parameters=p,field_type=kind)['question'][':question/id'],'Seed-independent fixed content')
  require(len(fingerprints)==25,'Exactly 25 meaningful tasks per level');tasks[level]=len(fingerprints)
  review.extend(g.generate(level,seed=s) for s in (20,21))
 for profile,specification in g.OBSERVED.items():
  eligible=[]
  for r,c in g.DIMENSIONS:
   p={'name':'M','entries':[['1']*c for _ in range(r)]}
   try:rec=g.generate('easy',parameters=p,profile=profile)
   except ValueError:continue
   independent(rec);eligible.append([r,c])
  profile_domains[profile]=eligible
  require(eligible,'Source bank has nonempty valid dimensions')
  # Exercise a changed dimension if available, not solely incidental entry variation.
  case=next(c for c in cases if c['bank_profile']==profile)
  original_dim=(len(case['parameters']['entries']),len(case['parameters']['entries'][0]))
  other=next(((r,c) for r,c in eligible if (r,c)!=original_dim),None)
  if other:
   r,c=other;p={'name':'M','entries':[['2']*c for _ in range(r)]};review.append(g.generate('easy',seed=7,parameters=p,profile=profile))
 for rec in review:independent(rec)
 # Entry/name changes affect displayed content, never mathematical task count.
 a=g.generate('easy',parameters={'name':'A','entries':[['1','2'],['3','4']]})
 b=g.generate('easy',seed=42,parameters={'name':'B','entries':[['2','2'],['3','4']]})
 require(a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint'] and a['question'][':question/id']!=b['question'][':question/id'],'Entry/name incidental math, substantive display content')
 require(a['question'][':question/id']==g.generate('easy',parameters=a['generation']['parameters'])['question'][':question/id'],'Seed changes do not multiply displayed identities')

 def fail(fn,why):
  try:fn()
  except (ValueError,AssertionError):return
  raise AssertionError('Negative control accepted: '+why)
 for p in ({'name':'A','entries':[['1','2']]},{'name':'A','entries':[['1'],['2']]},{'name':'A','entries':[['1','2'],['3']]},{'name':'A','entries':[['x','2'],['3','4']]}):fail(lambda:g.generate('easy',parameters=p),'out of scope/entry')
 fail(lambda:g.generate('moderate',profile='observed-q-125528'),'false observed difficulty')
 fail(lambda:g.generate('easy',profile='authored-rectangular',parameters={'name':'A','entries':[['1','2'],['3','4']]}),'invalid complete bank')
 for corrupt in ('prompt','solution','answer','id'):
  bad=copy.deepcopy(originals[3])
  if corrupt=='prompt':bad['question'][':question/problem']=bad['question'][':question/problem'].replace('-1 & 1 & -5 & 1 & 0 & 2','-1 & 1 & -5 & 1 & 0')
  if corrupt=='solution':bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('$6$ rows','$5$ rows')
  if corrupt=='answer':bad['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='2\\times 2'
  if corrupt=='id':bad['question'][':question/answer-fields'][0][':answer-field/correct'][1]=str(uuid.uuid4())
  fail(lambda:independent(bad),corrupt)
 for i,rec in enumerate(originals+review+all_default):
  checks=[]
  for ix,f in enumerate(rec['question'][':question/answer-fields']):
   if f[':answer-field/type'].endswith('/radio'):
    checks.extend({'field_index':ix,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Actual owned-choice grading; ordered dimensions independently verified'} for a in f[':answer-field/choices'])
   else:
    value=f[':answer-field/choices'][0][':answer/value']
    checks.extend({'field_index':ix,'submitted':entry,'expected':expected,'purpose':purpose} for entry,expected,purpose in [(value,'accepted','Canonical count'),('('+value+'+2)-2','accepted','Unevaluated equivalent count'),(str(int(value)+1),'rejected','Wrong count')])
  engine.append({'label':str(i),'record':rec,'checks':checks})
 (HERE/'engine-input.json').write_text(json.dumps(engine,indent=2)+'\n')
 engine_path=ROOT/'generate/runs/current/check-engine'
 result=subprocess.run([str(engine_path),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True)
 (HERE/'engine.log').write_text(result.stdout+result.stderr)
 require(result.returncode==0,'Native grader failed; see engine.log')
 (HERE/'review.json').write_text(json.dumps({'original_replays':originals,'generated_variants':review},indent=2)+'\n')
 parts=['# Matrix dimension review','Raw originals are in source.json. Replay preserves both legacy dot notation and the q-139406 R/P label error as evidence. Normal authored output repairs these. Only easy is supported; moderate and hard reject generation.']
 for case,rec in zip(cases,originals):parts+=['## Original replay '+case['source_id'],g.markdown(rec)]
 for rec in review:parts+=['## Generated variant — '+rec['question'][':question/difficulty'].split('/')[-1]+' / '+rec['generation']['template']+' / '+str(rec['generation']['bank_profile']),g.markdown(rec)]
 (HERE/'review.md').write_text('\n\n'.join(parts)+'\n')
 report={'status':'pass','provenance':{k:source[k] for k in ('database','basis','lineage')},'source_coverage':{'practice_questions':8,'prompt_layouts_exact':8,'complete_question_banks_exact':8,'field_banks_exact':counts['source_fields'],'displayed_answer_values_exact':counts['bank_values'],'original_correct_designations_matched':counts['correct_designations'],'missing_correct_designations_inferred':2,'original_solutions_exact':counts['solutions_exact'],'original_solutions_available':6,'authored_missing_solutions':2,'raw_exact_solution_label_errors':1,'normal_solution_label_repairs':1},'mathematics':{'exhaustive_authored_records':len(all_default),'finite_tasks_per_level':tasks,'meaningful_union_across_levels':25,'observed_profile_eligible_dimension_pairs':profile_domains,'negative_controls_passed':10},'native_grading':{'status':'pass','records':len(engine),'checks':sum(len(e['checks']) for e in engine),'binary_sha256':hashlib.sha256(engine_path.read_bytes()).hexdigest(),'report':'engine-report.json'},'source_details':details,'limitations':['Moderate/hard unsupported: no validated increase in assessed demand; earlier peer labels are archived.','Legacy q-11454/q-7806 correct refs, solutions and easy assignments are inferred/authored; absent source designations cannot count as matches.','Legacy EDB dot notation is preserved in explicit evidence profiles; authoritative q-11454 widget screenshot uses times.','q-139406 source solution names R while prompt names P; preserved in evidence replay and repaired in normal output.','Offset recipes in unusual observed banks reproduce the bank, but source distractor intent is underdetermined; authored operation banks are the defaults.']}
 report['supported_levels']=list(g.SUPPORTED_LEVELS)
 report['finite_variant_limit']=25
 report['hashes']={str(HERE.with_suffix('.py').relative_to(ROOT)):hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest()}
 engine_summary=json.loads((HERE/'engine-report.json').read_text())
 report['native_grading']['engine_details']={k:engine_summary[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks','entry_point')}
 require(report['native_grading']['engine_details']['documented_unresolved_checks']==0,'No unresolved grader checks')
 for level in ('moderate','hard'):fail(lambda:g.generate(level),'unsupported level '+level)
 batch=g.batch('easy',25,20)
 require(len({r['generation']['parameter_fingerprint'] for r in batch})==25,'Distinct finite batch')
 fail(lambda:g.batch('easy',26,20),'No duplicate padding')
 for r in batch:independent(r)
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:report[k] for k in ('status','source_coverage','native_grading')},indent=2))

if __name__=='__main__':main()
