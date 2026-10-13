#!/usr/bin/env python3
"""Source fidelity, strict printed mathematics, identities, domains and native grading.
Known raw source errors are asserted exactly and reported, never counted correct.
"""
import hashlib,importlib.util,json,re,subprocess,sys,uuid
from pathlib import Path
import sympy as sp
from printed_math import validate as printed_validate,blocks,parse,equal
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('point_chain',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def write(name,value): (HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def format_check(record):
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 assert record['knowledge_point']['db_id']==g.KP_ID
 q=record['question'];uuid.UUID(q[':question/id'])
 for name in (':question/problem',':question/worked-solution'):
  text=q[name]; assert text.count('$')%2==0
  depth=0
  for ch in text:
   if ch=='{':depth+=1
   elif ch=='}':depth-=1
   assert depth>=0
  assert depth==0
  assert not re.search(r'(?<!\\)[+-]{2}',text)
 f=q[':question/answer-fields'][0];uuid.UUID(f[':answer-field/id'])
 assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 ids=[a[':answer/id'] for a in f[':answer-field/choices']]
 assert len(ids)==len(set(ids))==5
 assert f[':answer-field/correct'][0]==':answer/id' and f[':answer-field/correct'][1] in ids
 for a in f[':answer-field/choices']:
  uuid.UUID(a[':answer/id']);assert a[':answer/type']==':answer.type/math';assert '$' not in a[':answer/value']

def raw_errors(record):
 errors=printed_validate(record);source=record['generation']['source_ids'][0]
 expected=1 if source in ('q-94888','q-94891') else 0
 assert len(errors)==expected,(source,errors)
 if expected:assert errors[0]['block']==3 and errors[0]['row']==0
 return errors

def main():
 records=[];review=[];cases=[];fidelity=[];anomalies=[];distinct={};counts={};stage_checks=0
 for sid,(name,level,base) in g.SOURCE_SPECS.items():
  p=dict(base,scale=1);profile=sid+'_raw'
  record=g.generate(level,seed=17,template=name,parameters=p,profile=profile)
  source=g.SOURCES[sid];q=record['question'];format_check(record)
  assert q[':question/problem']==source[':question/problem']
  original=source.get(':question/worked-solution')
  if original:assert q[':question/worked-solution']==original
  actual=q[':question/answer-fields'][0];original_field=source[':question/answer-fields'][0]
  assert sorted(a[':answer/value'] for a in actual[':answer-field/choices'])==sorted(a[':answer/value'] for a in original_field[':answer-field/choices'])
  assert actual[':answer-field/key']==original_field[':answer-field/key']
  assert actual[':answer-field/type']==original_field[':answer-field/type'][':db/ident']
  correct=next(a[':answer/value'] for a in actual[':answer-field/choices'] if a[':answer/id']==actual[':answer-field/correct'][1])
  if ':answer-field/correct' in original_field:assert equal(parse(correct),parse(original_field[':answer-field/correct'][':answer/value']))
  errors=raw_errors(record)
  if errors:anomalies.append({'source':sid,'errors':errors,'disposition':'raw public evidence only; normal authored full formal-derivative block correct'})
  source_case_profile=profile
  if sid in ('q-36247','q-36253'):
   source_case_profile=sid+'_raw_omission'
   omission=g.generate(level,seed=17,parameters=p,profile=source_case_profile)
   assert ':question/difficulty' not in omission['question']
   assert ':question/worked-solution' not in omission['question']
   assert ':answer-field/correct' not in omission['question'][':question/answer-fields'][0]
   assert omission['question'][':question/problem']==source[':question/problem']
   assert sorted(a[':answer/value'] for a in omission['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/value'] for a in original_field[':answer-field/choices'])
   review.append({'label':'Original omission faithfully preserved '+sid,'record':omission})
  cases.append({'source_id':source[':db/id'],'source_math_academy_id':sid,'template':name,'level':level,'parameters':p,'bank_profile':source_case_profile,'completed_bank_profile':profile,'original':source,'authored_level_assignment':':question/difficulty' not in source})
  fidelity.append({'source':sid,'prompt_exact':True,'bank_exact':True,'choices_matched':5,'correct_designation_matched':':answer-field/correct' in original_field,'solution_exact':True if original else None,'solution_sequence_rows':[len(b) for b in blocks(q[':question/worked-solution'])],'source_math_errors':len(errors)})
  review.append({'label':'Original replay '+sid,'record':record});records.append(record)
  for scale in (2,4):
   variant=g.generate(level,seed=31,parameters=dict(base,scale=scale),profile=profile)
   format_check(variant);raw_errors(variant);records.append(variant)
   review.append({'label':'Generated observed-bank equivariant variant '+sid+'; error intent unresolved','record':variant})
 for name,level in g.TEMPLATES.items():
  fps=set();first=[]
  for seed in range(24):
   record=g.generate(level,seed,template=name);format_check(record)
   errors=printed_validate(record);assert not errors,(name,seed,errors)
   stage_checks+=sum(len(b) for b in blocks(record['question'][':question/worked-solution']))
   fps.add(record['generation']['parameter_fingerprint']);records.append(record)
   if seed<2:
    first.append(record);review.append({'label':'Authored '+level+' method-operation variant; '+name,'record':record})
   if seed==0:
    p=record['generation']['parameters']
    shuffled=g.generate(level,901,template=name,parameters=p)
    assert shuffled['question'][':question/id']==record['question'][':question/id']
    assert shuffled['generation']['parameter_fingerprint']==record['generation']['parameter_fingerprint']
  assert len(fps)>=20,(name,len(fps))
  distinct[name]=len(fps);counts[name]=24
 # Explicit scope guards and collisions fail rather than silently changing input.
 for name,level in g.TEMPLATES.items():
  p=g.generate(level,50,template=name)['generation']['parameters'];p=dict(p,a=0)
  try:g.generate(level,parameters=p,template=name)
  except ValueError:pass
  else:raise AssertionError('Defining coefficient zero escaped guard')
  p=dict(g.generate(level,51,template=name)['generation']['parameters'],a=-5)
  try:g.generate(level,parameters=p,template=name)
  except ValueError:pass
  else:raise AssertionError('Signed magnitude escaped guard')
 collision=dict(a=1,b=1,c=1,d=0,e=1,h=0,t0=1)
 try:g.generate('easy',template='quadratic_affine',parameters=collision)
 except g.SampleRejected:pass
 else:raise AssertionError('Whole-bank collision was accepted')
 inputs=[]
 for i,record in enumerate(records):
  f=record['question'][':question/answer-fields'][0]
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'full owned radio bank ID grading'} for a in f[':answer-field/choices']]
  inputs.append({'label':str(i)+' '+record['generation']['bank_profile'],'record':record,'checks':checks})
 write('source-cases.json',cases);write('review.json',review);write('engine-input.json',inputs)
 grader=ROOT/'generate/runs/current/check-engine'
 result=subprocess.run([str(grader),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True)
 assert result.returncode==0,(result.stdout,result.stderr)
 engine=json.loads((HERE/'engine-report.json').read_text())
 write('validation.json',{'status':'passed_with_documented_raw_source_errors','source_provenance':{k:g.CAPTURE[k] for k in ('database','basis','lineage')},'source_coverage':{'questions':8,'prompt_exact':8,'complete_banks_exact':8,'displayed_choices_exact':40,'correct_designations_matched':6,'correct_designations_missing_authored':2,'worked_solutions_present_exact':6,'worked_solutions_missing_authored':2,'raw_solutions_independently_correct_math':4,'raw_solutions_with_formal_derivative_errors':2},'fidelity':fidelity,'raw_source_anomalies':anomalies,'raw_notation_dimension_errors':{'q-36227':'intro f(x,y,z) should be f(x,y)','q-94884':'intro f(x,y,z) should be f(x,y)','q-94887':'gradient label f(x,y) should be f(x,y,z)','q-94888':'gradient label f(x,y) should be f(x,y,z)','q-94891':'gradient label f(x,y) should be f(x,y,z)'},'authored_cases_per_template':counts,'distinct_authored_tasks_per_24_seeds':distinct,'printed_authored_stage_checks':stage_checks,'native_case_count':len(inputs),'native_checks':len(inputs)*5,'native_passed':True,'native_executable_sha256':hashlib.sha256(grader.read_bytes()).hexdigest(),'engine_summary':{k:v for k,v in engine.items() if k not in ('results','records')},'public_raw_omission_profiles_tested':2,'raw_profiles_eligible_for_learning':False,'normal_profiles_eligible_for_learning':True,'identity_shuffle_checks':9,'scope_guard_checks':18,'whole_bank_collision_rejection':True,'raw_replay_generalization':'source mathematical parameters fixed except whole-function scale1..4; no inferred error intent','normal_output_mathematical_source_errors':0})
 sections=['# Rate-of-change generator review','\nAll records below are local author previews. Raw source notation errors are retained only in explicitly marked evidence profiles; consult validation.json.\n']
 for item in review:sections.extend(['## '+item['label'],'',g.markdown(item['record']),''])
 (HERE/'review.md').write_text('\n'.join(sections))
 print(json.dumps({'source_banks':'8/8','source_choices':'40/40','source_correct_refs':'6/6 present; 2 missing derived','raw_solution_exact':'6/6 present','raw_math_errors':2,'authored_cases':216,'native_checks':len(inputs)*5,'distinct':distinct},indent=2))
if __name__=='__main__':main()
