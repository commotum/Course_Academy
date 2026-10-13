#!/usr/bin/env python3
"""Fail on actual displayed-array, ordered-bank, scope, fidelity or native errors."""
from pathlib import Path
import collections,copy,hashlib,importlib.util,json,re,subprocess,sys,uuid
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
source=json.loads((HERE/'source.json').read_text());sources=g.SOURCE_RECORDS
cases=json.loads((HERE/'source-cases.json').read_text())
def require(x,why):
 if not x:raise AssertionError(why)
def dimensions(prompt):
 arrays=re.findall(r'\\begin\{(?:aligned|bmatrix)\}(.*?)\\end\{(?:aligned|bmatrix)\}',prompt,re.S)
 require(len(arrays)==1,'One actual displayed matrix')
 rows=[[s.strip() for s in row.split('&')] for row in arrays[0].split(r'\\')]
 require(len({len(row) for row in rows})==1 and all(all(row) for row in rows),'Rectangular nonempty displayed matrix')
 return len(rows),len(rows[0]),rows

def pair(value):
 m=re.fullmatch(r'(\d+)\s*\\(?:times|cdot)\s*(\d+)',value)
 require(m is not None,'Ordered-dimension notation, not scalar product')
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
 require(not re.search(r'q-\d+|1759218\d+',s),'No raw IDs in learner content')

def independent(rec):
 require(set(rec['knowledge_point'])=={'db_id','id','title'},'Plain outer KP keys')
 require(rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE},'KP identity')
 q=rec['question'];gen=rec['generation'];r,c,rows=dimensions(q[':question/problem']);level=gen['level'];lo,hi=g.LEVEL_BOUNDS[level]
 require((r,c) in g.DIMENSIONS[level],'Actual printed level workload bounds')
 require(int(r>6)+int(c>6)=={'easy':0,'moderate':1,'hard':2}[level],'Actual number of extended enumeration axes')
 require(rows==gen['parameters']['entries'],'Printed array is actual parameters')
 require(gen['workload']['independent_counts']==2 and gen['workload']['rows_counted']==r and gen['workload']['columns_counted']==c,'Workload read from display')
 require(gen['draft_only'],'Separate draft only')
 formatting(q[':question/problem']);uuid.UUID(q[':question/id'])
 if ':question/worked-solution' in q:
  solution=q[':question/worked-solution'];formatting(solution)
  match=re.fullmatch(r'The matrix \$([A-Z])\$ has \$(\d+)\$ rows and \$(\d+)\$ columns\. Therefore, its dimensions are \$(\d+)\\times (\d+)\.\$',solution)
  require(match is not None and tuple(map(int,match.groups()[1:]))==(r,c,r,c),'Full count/count/ordered-pair solution stages')
  name=re.search(r'\$([A-Z])',q[':question/problem'])[1]
  require(match[1]==name or gen['evidence_only'] and gen['bank_profile']=='observed-q-139406' and name=='P' and match[1]=='R','Solution matches printed name')
 kind=q[':question/answer-fields'][0][':answer-field/type'].split('/')[-1]
 require(len(q[':question/answer-fields'])==(1 if kind=='radio' else 2),'Field layout')
 for f in q[':question/answer-fields']:
  uuid.UUID(f[':answer-field/id']);key=f[':answer-field/key'];answers=f[':answer-field/choices'];correct=f.get(':answer-field/correct')
  if correct:require(correct[0]==':answer/id' and correct[1] in [a[':answer/id'] for a in answers],'Owned correct lookup')
  require(len(set(a[':answer/id'] for a in answers))==len(answers),'Unique owned IDs')
  require(all(a[':answer/type']==':answer.type/math' and '$' not in a[':answer/value'] for a in answers),'Answer shapes')
  if kind=='radio':
   vals=[pair(a[':answer/value']) for a in answers]
   require(len(vals)==5 and len(set(vals))==5,'Complete unequal ordered bank')
   require(vals.count((r,c))==1,'Exactly one correct ordered dimension pair')
   if correct:require(next(pair(a[':answer/value']) for a in answers if a[':answer/id']==correct[1])==(r,c),'Correct designation')
   require(all(1<=x<=14 and 1<=y<=14 for x,y in vals),'Plausible positive dimensions')
  else:
   require('{{'+key+'}}' in q[':question/problem'],'Every blank placeholder')
   require(len(answers)==1 and sp.Integer(answers[0][':answer/value'])==(r if key=='field-1' else c),'Displayed count fragments')
 require(gen['parameter_fingerprint']==g.digest({'rows':r,'columns':c}),'Meaningful ordered-count fingerprint')
 expected=g.digest({'version':g.VERSION,'difficulty':level if ':question/difficulty' in q else None,'prompt':q[':question/problem'],'solution':q.get(':question/worked-solution'),'fields':[(f[':answer-field/key'],kind,sorted(a[':answer/value'] for a in f[':answer-field/choices']),':answer-field/correct' in f) for f in q[':question/answer-fields']]})
 require(expected==gen['content_fingerprint'] and g.uid(expected)==q[':question/id'],'Actual displayed identity')
 return r,c

def fidelity(src,rec):
 q=rec['question'];require(q[':question/problem']==src[':question/problem'],'Full exact prompt/layout')
 for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):
  require((key in q)==(key in src),'Source attribute presence: '+key)
 if ':question/worked-solution' in src:require(q[':question/worked-solution']==src[':question/worked-solution'],'Full solution prose/stages')
 if ':question/difficulty' in src:require(q[':question/difficulty']==src[':question/difficulty'][':db/ident'],'Observed label')
 for of,f in zip(src[':question/answer-fields'],q[':question/answer-fields']):
  require(f[':answer-field/key']==of[':answer-field/key'],'Source field collection order')
  require(f[':answer-field/type']==of[':answer-field/type'][':db/ident'],'Full source field type')
  require(collections.Counter(a[':answer/value'] for a in f[':answer-field/choices'])==collections.Counter(a[':answer/value'] for a in of[':answer-field/choices']),'Entire exact original bank')
  require((':answer-field/correct' in f)==(':answer-field/correct' in of),'Source designation presence')
  if ':answer-field/correct' in of:
   require(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'],'Original designation match')

def checks(record):
 result=[]
 for i,f in enumerate(record['question'][':question/answer-fields']):
  if ':answer-field/correct' not in f:continue
  if f[':answer-field/type'].endswith('/radio'):
   result.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Owned choice grading; ordered counts independently read from matrix'} for a in f[':answer-field/choices'])
  else:
   v=f[':answer-field/choices'][0][':answer/value']
   result.extend({'field_index':i,'submitted':x,'expected':e,'purpose':'Canonical/equivalent/wrong row or column count'} for x,e in [(v,'accepted'),('('+v+'+2)-2','accepted'),(str(int(v)+1),'rejected')])
 return result

def fail(fn,why):
 try:fn()
 except (ValueError,AssertionError):return
 raise AssertionError('Negative control accepted: '+why)

def main():
 originals=[];review=[];details=[];all_default=[];profile_domains={};tasks={};negatives=0
 for case in cases:
  src=sources[case['source_id']];rec=g.generate(case['level'],parameters=case['parameters'],template=case['template'],profile=case['bank_profile']);independent(rec);fidelity(src,rec);originals.append(rec)
  # Changed dimensions, not only incidental entries, are exercised for each bank.
  eligible=[]
  for r,c in g.DIMENSIONS['easy']:
   p={'name':'B','entries':[['2']*c for _ in range(r)]}
   try:variant=g.generate('easy',parameters=p,profile=case['bank_profile'])
   except ValueError:continue
   independent(variant);eligible.append([r,c])
  require(eligible,'Profile has valid complete bank domain');profile_domains[case['bank_profile']]=eligible
  shape=independent(rec);other=next((x for x in eligible if tuple(x)!=shape),None)
  require(other is not None,'Parameterized profile has a changed-count example')
  r,c=other;review.append(g.generate('easy',parameters={'name':'B','entries':[['2']*c for _ in range(r)]},profile=case['bank_profile']))
  details.append({'source_id':case['source_id'],'prompt_exact':True,'bank_exact':True,'attribute_presence_exact':True,'designation_matches':sum(':answer-field/correct' in f for f in src[':question/answer-fields']),'solution_exact':':question/worked-solution' in src,'evidence_only':True})
 union=set()
 for level in g.SUPPORTED_LEVELS:
  fingerprints=set()
  for r,c in g.DIMENSIONS[level]:
   p={'name':'A','entries':[[str((i*3+j)%7-3) for j in range(c)] for i in range(r)]}
   for kind in ('radio','blank'):
    rec=g.generate(level,parameters=p,field_type=kind);independent(rec);all_default.append(rec);fingerprints.add(rec['generation']['parameter_fingerprint'])
    require(rec['question'][':question/id']==g.generate(level,seed=999,parameters=p,field_type=kind)['question'][':question/id'],'Fixed explicit content independent of seed')
   for bank in ('authored-square','authored-rectangular'):
    if not g.eligible_bank(bank,r,c):continue
    independent(g.generate(level,parameters=p,profile=bank))
  require(len(fingerprints)==len(g.DIMENSIONS[level]),'Finite meaningful domain');tasks[level]=len(fingerprints);require(not union.intersection(fingerprints),'Disjoint real shape domains across difficulty');union.update(fingerprints)
  for kind in ('radio','blank'):review.append(g.generate(level,seed=21,field_type=kind))
  # Every public explicit guard rejects other bands, incomplete arrays and long cells.
  for other in g.SUPPORTED_LEVELS:
   if other==level:continue
   r,c=g.DIMENSIONS[other][0]
   fail(lambda:g.generate(level,parameters={'name':'A','entries':[['1']*c for _ in range(r)]}),level+' relabelled other level');negatives+=1
  batch=g.batch(level,len(g.DIMENSIONS[level]),20)
  require(len({r['generation']['parameter_fingerprint'] for r in batch})==len(g.DIMENSIONS[level]),'CLI batch no incidental duplicates')
  fail(lambda:g.batch(level,len(g.DIMENSIONS[level])+1), 'Finite batch bound');negatives+=1
  seen_banks=set();seen_templates=set()
  for seed in range(150):
   record=g.generate(level,seed=seed);independent(record);seen_banks.add(record['generation']['bank_profile']);seen_templates.add(record['generation']['template'])
  require(({'authored-rectangular',None} if level=='moderate' else {'authored-square','authored-rectangular',None}).issubset(seen_banks),'Whole bank/default layout coverage')
  expected=set(g.NORMAL_TEMPLATES if level=='easy' else ('display-radio','display-dual-blank'))
  require(seen_templates==expected,'Normal supported source-shaped family coverage')
  tasks[level]={'meaningful_tasks':len(fingerprints),'default_templates':sorted(seen_templates),'default_banks':sorted(str(x) for x in seen_banks)}
 require(len(union)==121,'Exactly 121 tasks, no bank/entry/name padding')
 for p in ({'name':'A','entries':[['1','2']]},{'name':'A','entries':[['1'],['2']]},{'name':'A','entries':[['1','2'],['3']]},{'name':'A','entries':[['x','2'],['3','4']]}):fail(lambda:g.generate('easy',parameters=p),'out-of-scope cell/shape');negatives+=1
 for level,r,c in [('moderate',7,2),('hard',10,10)]:
  fail(lambda:g.generate(level,parameters={'name':'A','entries':[['30']*c for _ in range(r)]}),'large cell in dense array');negatives+=1
 fail(lambda:g.generate('moderate',profile='observed-q-125528'),'False observed label');negatives+=1
 fail(lambda:g.generate('easy',profile='authored-rectangular',parameters={'name':'A','entries':[['1','2'],['3','4']]}),'Invalid complete bank');negatives+=1
 # Same ordered dimensions across names/layouts/entries/profiles = one math task.
 a=g.generate('easy',parameters={'name':'A','entries':[['1','2'],['3','4']]},field_type='radio')
 b=g.generate('easy',parameters={'name':'B','entries':[['2','2'],['3','4']]},field_type='blank')
 require(a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint'] and a['question'][':question/id']!=b['question'][':question/id'],'Incidental parameters excluded from meaningful count')
 require(pair(r'2\times 4')!=pair(r'4\times 2'),'Ordered dimensions cannot collapse to product equivalence')
 for corrupt in ('prompt','solution','answer','id'):
  bad=copy.deepcopy(originals[3]);q=bad['question']
  if corrupt=='prompt':q[':question/problem']=q[':question/problem'].replace('-1 & 1 & -5 & 1 & 0 & 2','-1 & 1 & -5 & 1 & 0')
  if corrupt=='solution':q[':question/worked-solution']=q[':question/worked-solution'].replace('$6$ rows','$5$ rows')
  if corrupt=='answer':q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='2\\times 2'
  if corrupt=='id':q[':question/answer-fields'][0][':answer-field/correct'][1]=str(uuid.uuid4())
  fail(lambda:independent(bad),corrupt);negatives+=1
 # CLI smoke checks exercise all levels and exact record shape.
 cli=subprocess.run([str(ROOT/'.venv/bin/python'),str(HERE.with_suffix('.py')),'--difficulty','all','--count','2','--format','json'],capture_output=True,text=True,check=True)
 cli_records=json.loads(cli.stdout);require(len(cli_records)==6,'Two CLI samples per level')
 for rec in cli_records:independent(rec)
 (HERE/'cli-preview.json').write_text(cli.stdout)
 engine=[{'label':str(i),'record':rec,'checks':checks(rec)} for i,rec in enumerate(originals+review+all_default) if checks(rec)]
 (HERE/'engine-input.json').write_text(json.dumps(engine,indent=2)+'\n');engine_path=ROOT/'generate/runs/current/check-engine'
 result=subprocess.run([str(engine_path),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True)
 (HERE/'engine.log').write_text(result.stdout+result.stderr);require(result.returncode==0,'Native grading failed; see engine.log')
 summary=json.loads((HERE/'engine-report.json').read_text());require(summary['documented_unresolved_checks']==0,'Unexpected/unresolved native checks')
 (HERE/'review.json').write_text(json.dumps({'original_replays':originals,'generated_variants':review},indent=2)+'\n')
 parts=['# Private matrix dimension draft review','Original profiles are raw evidence and are ineligible for default learning. Missing legacy labels/solutions/designations stay absent. Moderate/hard are authored increased-counting bands, not observed difficulty labels. This draft is not registered.']
 for case,rec in zip(cases,originals):parts+=['## Exact original replay '+case['source_id'],g.markdown(rec)]
 for rec in review:parts+=['## Generated variant — '+rec['generation']['level']+' / '+rec['generation']['template']+' / '+str(rec['generation']['bank_profile'])+(' (evidence-only opaque historical bank)' if rec['generation']['evidence_only'] else ' (authored eligible counting bank)'),g.markdown(rec)]
 (HERE/'review.md').write_text('\n\n'.join(parts)+'\n')
 baseline=json.loads((HERE/'registered-baseline.json').read_text());require(all(Path(p).is_file() and hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in baseline.items()),'Registered easy package unchanged')
 require((HERE/'source.json').read_bytes()==(ROOT/'generate/runs/current/sources/17592186087693.json').read_bytes(),'Exact captured source provenance')
 require(len(sources)==8 and len(cases)==8,'Complete captured source coverage')
 require(sum(len(q[':question/answer-fields']) for q in sources.values())==10 and sum(len(f[':answer-field/choices']) for q in sources.values() for f in q[':question/answer-fields'])==34,'Actual source-bank denominators')
 coverage={'practice_questions':8,'prompt_layouts_exact':8,'complete_question_banks_exact':8,'field_banks_exact':10,'displayed_answer_values_exact':34,'original_correct_designations_matched':8,'missing_correct_designations_preserved_absent':2,'original_solutions_exact':6,'original_solutions_available':6,'unrated_difficulty_preserved_absent':2,'raw_solution_label_errors_preserved':1,'normal_solution_label_repair':1}
 report={'status':'pass','draft_only':True,'provenance':{k:source[k] for k in ('database','basis','lineage')},'source_coverage':coverage,'mathematics':{'exhaustive_authored_records':len(all_default),'finite_tasks_per_level':tasks,'meaningful_union_across_levels':121,'observed_profile_domains':profile_domains,'negative_controls_passed':negatives,'actual_printed_arrays_checked':True},'native_grading':{'status':'pass','records':len(engine),'checks':sum(len(e['checks']) for e in engine),'binary_sha256':hashlib.sha256(engine_path.read_bytes()).hexdigest(),**{k:summary[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks','entry_point')},'ungraded_raw_missing_designations':2},'source_details':details,'difficulty_design':{'easy':'Observed 2..6 on both axes; no additional entry-number workload','moderate':'Authored exactly one 7..12 count and one 2..6 count, either orientation','hard':'Authored two 7..12 counts on unlabelled axes','evidence_limit':'No observed moderate/hard; increased counting demand is a design rationale, not empirically validated MA difficulty. Each band uses the same two-count method and bounded comparable workload.'},'registered_package_unchanged':True,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'legibility_review':{'artifact':'render-qa.png','maximum_shapes':[[2,12],[12,2],[12,12]],'reviewed':'Single-digit cells, aligned rows/columns, complete brackets and banks legible at recorded fixed-width inspection size','limitation':'Numerical typesetting inspection, not browser TeX-engine parity'},'limitations':['Finite 121 meaningful tasks; names/entries/banks/layouts cannot make new mathematical tasks.','Harder labels are authored longer enumeration, not a new mathematical technique or observed MA classifications.','Legacy raw sources have no native-gradeable correct designation; absence preserved and inferred ordered counts documented separately.','Opaque observed numerical offsets have multiple plausible proportional/count recipes; replay is evidence-only, not recovered distractor intent.','q-139406 names R in source solution but P in prompt; raw evidence preserves this; eligible normal output names its actual matrix.']}
 report['hashes']={str(HERE.with_suffix('.py').relative_to(ROOT)):hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest()}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:report[k] for k in ('status','source_coverage','native_grading','runtime')},indent=2))
if __name__=='__main__':main()
