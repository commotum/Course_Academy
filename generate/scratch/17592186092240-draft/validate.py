#!/usr/bin/env python3
"""Standalone draft checks. Never writes EDB, baseline, registration or shared QA."""
import copy, hashlib, importlib.util, json, platform, subprocess, sys
from pathlib import Path
import sympy as s
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from readback import validate as readback,scalar,eq
z=importlib.util.spec_from_file_location('normal_draft',H.with_suffix('.py'));G=importlib.util.module_from_spec(z);z.loader.exec_module(G)
ENGINE=H.parents[1]/'runs/current/check-engine';EXPECTED='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,data):(H/name).write_text(json.dumps(data,indent=2)+'\n')
def original_cases():return [{'source_id':sid,'template':sid,'profile':'observed_raw','level':'moderate','parameters':{'shift':0},'difficulty_provenance':'authored moderate assignment' if sid=='q-47406' else 'captured moderate'} for sid,c in G.T.items()]
def checks_for(record):
 checks=[]
 for i,f in enumerate(record['question'][':question/answer-fields']):
  correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);value=scalar(correct[':answer/value'])
  if f[':answer-field/type'].endswith('/radio'):
   for a in f[':answer-field/choices']:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a==correct else 'rejected','purpose':'every owned source bank ID'})
   for wrong in ['0','1','99999','foreign-answer-id']:
    checks.append({'field_index':i,'submitted':wrong,'expected':'unresolved','purpose':'ordinary wrong numeric ID or foreign ID (native ownership error)' })
  else:
   canonical=correct[':answer/value'];equiv=r'\frac{'+s.latex(value*2)+'}{2}'
   for text,purpose in [(canonical,'canonical'),(equiv,'independently unreduced equivalent')]:checks.append({'field_index':i,'submitted':text,'expected':'accepted','purpose':purpose})
   for wrong in ['0','1',s.latex(value+1)]:
    if not eq(scalar(wrong),value):checks.append({'field_index':i,'submitted':wrong,'expected':'rejected','purpose':'ordinary wrong 0/1/correct+1'})
   checks.append({'field_index':i,'submitted':'foreign-answer-id','expected':'unresolved','purpose':'foreign ID'})
 return checks

def run():
 assert sha(ENGINE)==EXPECTED
 baseline=json.loads((H/'baseline.json').read_text())['files'];assert all(Path(p).is_file() and sha(Path(p))==h for p,h in baseline.items());assert {str(Path(p).resolve()) for p in baseline}=={str(p) for p in [H.with_name(H.name.replace('-draft','')).with_suffix('.py')]+list(H.with_name(H.name.replace('-draft','')).rglob('*')) if p.is_file()}
 cases=original_cases();save('source-cases.json',cases);source=G.K[':knowledge-point/questions'];byid={q[':question/math-academy-id']:q for q in source};fidelity=[];bank_total=bank_matched=values_total=values_matched=correct_total=correct_matched=distractors=0;records=[];counts={};totals={'equalities':0,'formal_operands':0,'normal_lines':0,'bank_values':0};preview=[]
 for level in ['easy','moderate','hard']:
  for params in G.authored_parameters(level):
   r=G.generate(level,parameters=params);c=readback(r)
   for k,v in c.items():totals[k]+=v
   assert r==G.generate(level,parameters=params)
   r2=G.generate(level,seed=72,parameters=params);assert r['question']==r2['question']
   records.append({'label':level+':'+json.dumps(params,sort_keys=True),'record':r,'checks':checks_for(r)})
  counts[level]=len({r['record']['generation']['mathematical_key'] for r in records if r['record']['question'][':question/difficulty']==':question.difficulty/'+level})
  preview.extend(G.generate(level,seed=i) for i in [7,19])
 for sid in G.T:
  for params in G.source_parameters(sid):
   r=G.generate('moderate',profile=sid,parameters=params);c=readback(r)
   for k,v in c.items():totals[k]+=v
   assert r['question'][':question/id']==G.generate('moderate',seed=33,profile=sid,parameters=params)['question'][':question/id']
   records.append({'label':sid+':'+str(params),'record':r,'checks':checks_for(r)})
  original=byid[sid];raw=G.generate('moderate',template=sid,profile='observed_raw',parameters={'shift':0});assert raw['question']==original and raw['generation']['evidence_only'] and not raw['generation']['eligible_for_learning'];r=G._source('moderate',0,sid,{'shift':0},raw=True);served=G.generate('moderate',profile=sid,parameters={'shift':0});out={f[':answer-field/key']:f for f in r['question'][':question/answer-fields']};fieldrows=[]
  for field in original.get(':question/answer-fields',[]):
   bank_total+=1;f=out[field[':answer-field/key']];aa=[scalar(a[':answer/value']) for a in field[':answer-field/choices']];bb=[scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert len(aa)==len(bb) and all(sum(eq(a,b) for b in bb)==1 for a in aa);bank_matched+=1;values_total+=len(aa);values_matched+=len(aa)
   assert field[':answer-field/type'][':db/ident']==f[':answer-field/type']
   if ':answer-field/correct' in field:
    correct_total+=1;v=scalar(field[':answer-field/correct'][':answer/value']);got=scalar(next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])[':answer/value']);assert eq(v,got);correct_matched+=1;distractors+=len(aa)-1
   fieldrows.append({'key':field[':answer-field/key'],'complete_bank':True,'values':len(aa),'original_correct_ref':':answer-field/correct' in field})
  prompt_exact=r['question'][':question/problem']==original[':question/problem'];solution_exact=r['question'][':question/worked-solution']==original.get(':question/worked-solution')
  assert prompt_exact or sid=='q-47405';assert solution_exact or sid=='q-47406'
  fidelity.append({'source_id':sid,'full_raw_attributes_exact':True,'raw_prompt_exact':prompt_exact,'raw_solution_exact':solution_exact,'served_prompt_exact':served['question'][':question/problem']==original[':question/problem'],'fields':fieldrows,'repair':'added missing blank' if sid=='q-47405' else 'inferred correct 74; authored missing solution' if sid=='q-47406' else 'supplied omitted prior-part bindings' if G.T[sid].get('context') else None})
  preview.append(served)
  varied=next((p for p in G.source_parameters(sid) if p['shift']!=0),None)
  if varied is not None:preview.append(G.generate('moderate',profile=sid,parameters=varied))
 # Negative controls corrupt the displayed curve, formal operand, point, slope, normal equation and key independently.
 sample=G.generate('easy',parameters={'a':2,'c':1,'point':2});controls=[]
 for name,location,old,new in [('given','problem','2 x^{2} + 1','3 x^{2} + 1'),('point','problem','(2,9)','(3,9)'),('formal operand','worked-solution',r'\left(2 x^{2} + 1\right)',r'\left(2 x^{2} + 2\right)'),('evaluation','worked-solution',"f'(2)=8","f'(2)=7"),('normal','worked-solution',r'x + 8 y&=74',r'x + 7 y&=74')]:
  bad=copy.deepcopy(sample);key=':question/'+location;assert old in bad['question'][key],old;bad['question'][key]=bad['question'][key].replace(old,new)
  try:readback(bad)
  except (AssertionError,ValueError):controls.append(name)
  else:raise AssertionError('Missed negative control '+name)
 bad=copy.deepcopy(sample);bad['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='9'
 try:readback(bad)
 except AssertionError:controls.append('key')
 else:raise AssertionError('Missed answer corruption')
 bad=G.generate('moderate',profile='q-47410',parameters={'shift':0});wrong=next(a for a in bad['question'][':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']!=bad['question'][':question/answer-fields'][0][':answer-field/correct'][1]);wrong[':answer/value']=s.latex(scalar(wrong[':answer/value'])+2)
 try:readback(bad)
 except AssertionError:controls.append('complete wrong bank algebra')
 else:raise AssertionError('Missed bank recipe corruption')
 for level in ['easy','moderate','hard']:
  for p in [dict(G.authored_parameters(level)[0],a=99),dict(G.authored_parameters(level)[0],point=99),dict(G.authored_parameters(level)[0],extraneous=1)]:
   try:G.generate(level,parameters=p)
   except ValueError:pass
   else:raise AssertionError('Explicit parameter escaped public bounds')
 save('fidelity.json',fidelity);save('capacity.json',{'authored_defaults':counts,'source_profile_parameter_cases':sum(len(G.source_parameters(p)) for p in G.T),'meaningful_slots':['polynomial coefficients','constant term','evaluation point','source vertical translation'],'scope':'finite mathematical tasks; seeds/options never inflate capacity'});save('engine-input.json',records)
 subprocess.run([str(ENGINE),str(H/'engine-input.json'),str(H/'engine-report.json')],check=True)
 native=json.loads((H/'engine-report.json').read_text());save('review.json',preview)
 save('validation.json',{'passed':True,'status':'working; root independent QA pending','source_basis':2275,'source_questions':len(source),'source_complete_banks_matched':bank_matched,'source_complete_banks_total':bank_total,'source_values_matched':values_matched,'source_values_total':values_total,'source_correct_designations_matched':correct_matched,'source_correct_designations_total':correct_total,'source_distractors_matched':distractors,'source_distractors_total_known':distractors,'source_distractors_without_captured_correct_designation':4,'source_correct_missing':1,'source_fieldless':1,'math_readback':totals,'negative_controls':controls,'native':{k:native[k] for k in ['entry_point','accepted_checks','rejected_checks','documented_unresolved_checks']},'capacities':counts,'generator_sha256':sha(H.with_suffix('.py')),'engine_sha256':sha(ENGINE),'runtime':{'python':platform.python_version(),'sympy':s.__version__},'baseline_unchanged':True})
 print(json.dumps(json.loads((H/'validation.json').read_text()),indent=2))
if __name__=='__main__':run()
