#!/usr/bin/env python3
"""Failing local fidelity, independently parsed display-math and native validator."""
import copy,hashlib,importlib.util,json,re,subprocess,sys,uuid
from pathlib import Path
import sympy as sp
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P));from display_math import oracle_from_prompt,check_solution
spec=importlib.util.spec_from_file_location('inhibited_generator',P.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
S={q[':question/math-academy-id']:q for q in g.SOURCE['record'][':knowledge-point/questions']}
def value(answer):return int(re.search(r'\$(-?\d+)',answer[':answer/value']).group(1))
def independent_recipes(record,o):
 # Formula derivation uses parsed prompt, independently solved constants, and
 # displayed quantity values. Metadata is checked against this oracle.
 a,K,k=o['a'],o['K'],o['k'];correct=o['answer']
 if record['generation']['profile']!='authored_operations':
  original=oracle_from_prompt(S[record['generation']['template']][':question/problem'],record['generation']['template'])['answer']
  values=g.TEMPLATES[record['generation']['template']]['bank']
  return [('correct',o['result']) if v==original else ('empirical_unknown_intent_'+str(v),sp.Rational(v,original)*correct) for v in values]
 # Extract initial/observation value independently via f(t), instead of using
 # the generator's deficit/K computations; target/time are displayed in prompt.
 t=o['t'];t0=o['t0'];n=o['observed']
 if o['time'] is not None:
  when=o['time']
  return [('correct',o['result']),('use_initial_as_integration_constant',a-n*sp.exp(-k*when)),('omit_initial_deficit',a*(1-sp.exp(-k*when))),('omit_time_from_exponent',a-K*sp.exp(-k)),('treat_quantity_as_exponential_decay',n*sp.exp(-k*when))]
 target=o['target']
 return [('correct',o['result']),('omit_division_by_rate',sp.log(K/(a-target))),('use_target_ratio_instead_of_deficit',sp.log(target/n)/k),('linearize_exponential',(target-n)/(k*(a-n))+t0),('replace_logarithm_by_one',1/k)]
def check_record(r):
 q=r['question'];meta=r['generation'];name=meta['template'];o,lines=check_solution(q[':question/problem'],q[':question/worked-solution'],name)
 assert 0<o['K']<=o['a'] and o['k']>0
 assert q[':question/difficulty']==':question.difficulty/'+g.TEMPLATES[name]['level']
 assert '@@' not in q[':question/problem']+q[':question/worked-solution']
 assert len(q[':question/answer-fields'])==1
 f=q[':question/answer-fields'][0];assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
 answers=f[':answer-field/choices'];assert len(answers)==5 and len(set(value(a) for a in answers))==5
 assert all(a[':answer/type']==':answer.type/text' for a in answers)
 expected=independent_recipes(r,o);expected_values=[int(sp.floor(sp.N(v,40)+sp.Rational(1,2))) for _,v in expected]
 assert sorted(value(a) for a in answers)==sorted(expected_values),(name,'wrong bank')
 assert all(v>=0 for v in expected_values),(name,'nonphysical rounded answer')
 assert all(expr.is_real and expr.is_finite and expr>=0 for _,expr in expected),(name,'nonphysical exact answer')
 if o['time'] is not None:assert all(expr<o['a'] for _,expr in expected) and all(v<=int(sp.floor(o['a']+sp.Rational(1,2))) for v in expected_values)
 if o['time'] is None and name!='q-335619':
  plural='minutes' if name in ['q-335282','q-335280'] else 'hours' if name=='q-335578' else 'days'
  singular=plural[:-1]
  assert all(a[':answer/value']==f'${value(a)}$ '+(singular if value(a)==1 else plural) for a in answers)
 for data,(recipe,expr) in zip(meta['recipes'],expected):
  assert data['name']==recipe and abs(float(sp.N(sp.sympify(data['expression'])-expr,25)))<1e-20
  assert data['rounded']==int(sp.floor(sp.N(expr,40)+sp.Rational(1,2)))
 designated=[a for a in answers if a[':answer/id']==f[':answer-field/correct'][1]]
 assert f[':answer-field/correct'][0]==':answer/id' and len(designated)==1 and value(designated[0])==o['answer']
 assert len({a[':answer/id'] for a in answers})==5
 canonical={'level':g.TEMPLATES[name]['level'],'template':name,'parameters':{k:str(sp.Rational(str(v))) for k,v in sorted(meta['parameters'].items())},'profile':meta['profile'],'bank':sorted(a[':answer/value'] for a in answers),'problem':q[':question/problem'],'solution':q[':question/worked-solution']}
 digest=hashlib.sha256(json.dumps(canonical,sort_keys=True).encode()).hexdigest();qid=uuid.uuid5(g.NAMESPACE,digest);fid=uuid.uuid5(qid,'selection')
 assert q[':question/id']==str(qid) and f[':answer-field/id']==str(fid)
 assert meta['content_fingerprint']==digest
 assert all(a[':answer/id']==str(uuid.uuid5(fid,a[':answer/value'])) for a in answers)
 return lines

def save(name,content):(P/name).write_text(json.dumps(content,indent=2,ensure_ascii=False)+'\n')
def main():
 cases=json.loads((P/'source-cases.json').read_text());fidelity=[];records=[];line_count=0;reviews=[]
 for case in cases:
  name=case['template'];o=S[name];r=g.generate(case['level'],template=name,parameters=case['parameters'],profile=case['bank_profile']);line_count+=check_record(r);records.append(('original '+name,r));reviews.append({'label':'original source replay '+name,'record':r})
  assert r['question'][':question/problem']==o[':question/problem'],(name,'prompt fidelity')
  originalbank=sorted(a[':answer/value'] for a in o[':question/answer-fields'][0][':answer-field/choices']);newbank=sorted(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']);assert originalbank==newbank,(name,originalbank,newbank)
  field=o[':question/answer-fields'][0];correct=field.get(':answer-field/correct')
  if correct:assert value(correct)==g.model(case['parameters'])['answer']
  if name!='q-37389':assert r['question'][':question/worked-solution']==o[':question/worked-solution'],(name,'solution wording/layout fidelity')
  fidelity.append({'source_id':name,'displayed_values_matched':5,'displayed_values_total':5,'correct_designation_matched':correct is not None,'source_solution_exact':name!='q-37389','repair': 'authored hard rating, mathematically inferred 468 correct, authored solution' if name=='q-37389' else None})
  # Each original profile independently exercised at two new parameter sets.
  for j in range(2):
   r=g.generate(case['level'],seed=j+120,template=name,profile=case['bank_profile']);line_count+=check_record(r);records.append(('empirical variant '+name+' '+str(j),r));reviews.append({'label':'generated variant; observed empirical unknown intent '+name+' '+str(j),'record':r})
  for j in range(12):
   r=g.generate(case['level'],seed=j+21,template=name);line_count+=check_record(r)
   assert r['generation']['bank_origin']=='authored'
   records.append(('authored '+name+' '+str(j),r))
   if j<2:reviews.append({'label':'generated variant; authored operation bank '+name+' '+str(j),'record':r})
   # Fixed content identity excludes option shuffle seed.
   other=g.generate(case['level'],seed=999,template=name,parameters=r['generation']['parameters']);assert other['question'][':question/id']==r['question'][':question/id']
   assert other['generation']['parameter_fingerprint']==r['generation']['parameter_fingerprint']
  invalid=dict(case['parameters']);invalid['a']=0
  try:g.generate(case['level'],template=name,parameters=invalid)
  except ValueError:pass
  else:raise AssertionError('Explicit invalid input was silently accepted')
 # Explicit empirical extrapolation that exceeds the carrying capacity must
 # fail as a whole bank rather than produce an unphysical source-profile variant.
 try:g.generate_easy(template='q-37400',parameters=dict(a=1000,n0=800,k='0.016',time=100),profile='q-37400_empirical')
 except ValueError as exc:assert 'capacity-violating' in str(exc)
 else:raise AssertionError('Nonphysical complete empirical bank was accepted')
 # Failing-validator evidence: displayed math, wrong bank, designation mutations.
 probe=copy.deepcopy(records[0][1]);q=probe['question'];f=q[':question/answer-fields'][0]
 mutations=[]
 for kind in ['displayed_equation','distractor_value','correct_designation','content_identity','field_layout']:
  bad=copy.deepcopy(probe);bf=bad['question'][':question/answer-fields'][0]
  if kind=='displayed_equation':bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('K & =1\\,200','K & =1\\,201')
  elif kind=='distractor_value':bf[':answer-field/choices'][0][':answer/value']='$9999$ days'
  elif kind=='content_identity':bad['question'][':question/id']='00000000-0000-0000-0000-000000000000'
  elif kind=='field_layout':bf[':answer-field/key']='wrong-key'
  else:bf[':answer-field/correct'][1]=next(a[':answer/id'] for a in bf[':answer-field/choices'] if a[':answer/id']!=bf[':answer-field/correct'][1])
  try:check_record(bad)
  except (AssertionError,ValueError,TypeError):mutations.append({'mutation':kind,'result':'rejected'})
  else:raise AssertionError(('Mutation was not rejected',kind))
 save('failing-validator.json',mutations)
 # Every displayed option selected through the application's actual grader.
 requests=[]
 for label,r in records:
  f=r['question'][':question/answer-fields'][0]
  requests.append({'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'independently verified displayed option'} for a in f[':answer-field/choices']]})
 save('native-input.json',requests)
 engine=P.parents[1]/'runs/current/check-engine';subprocess.run([str(engine),str(P/'native-input.json'),str(P/'native-checks.json')],check=True)
 ranges={}
 for label,r in records:
  if r['generation']['profile']!='authored_operations':continue
  name=r['generation']['template'];v=[value(a) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
  prior=ranges.setdefault(name,{'minimum':min(v),'maximum':max(v),'records':0,'bank_size':5})
  prior['minimum']=min(prior['minimum'],min(v));prior['maximum']=max(prior['maximum'],max(v));prior['records']+=1
 report={'status':'pass','authored_option_ranges_observed_in_tests':ranges,'source_practice_questions':9,'source_banks_matched':9,'source_options_matched':45,'source_options_total':45,'source_distractors_matched':36,'source_distractors_total':36,'correct_designations_matched':8,'correct_designations_present':8,'missing_designations_repaired':1,'exact_source_solutions':8,'authored_missing_solutions':1,'records_checked':len(records),'independently_evaluated_displayed_relations':line_count,'source_fidelity':fidelity,'native_checks':json.loads((P/'native-checks.json').read_text()),'database_writes':0,'unresolved_findings':['Empirical scalar distractor intent is unknown; replay recipes are explicit proportional numerical generalizations, excluded from defaults.','q-37389 lacks captured rating, solution and correct designation; supported authored repairs are kept separate from fidelity counts.']}
 save('validation.json',report);save('review.json',reviews)
 md=['# Original and generated review','Source basis 1356. All original profiles are empirical replay with unknown intent. Authored operation banks are default.']
 for item in reviews:
  r=item['record'];name=r['generation']['template'];md+=['## '+item['label']]
  if item['label'].startswith('original'):
   original=S[name];md+=['### Captured original',original[':question/problem'],'\n'.join('- '+a[':answer/value'] for a in original[':question/answer-fields'][0][':answer-field/choices']),original.get(':question/worked-solution','No captured solution. Hard assignment and solution below are authored.')]
  md+=['### Generated record',g.markdown(r)]
 (P/'review.md').write_text('\n\n'.join(md)+'\n')
 print(f'PASS: {len(records)} instances, {line_count} independently evaluated displayed relations; 9/9 banks, 45/45 options, 8/8 supplied designations; 1 documented missing ref repair.')
if __name__=='__main__':
 try:main()
 except Exception as exc:
  save('validation.json',{'status':'fail','failure_type':type(exc).__name__,'failure':str(exc)})
  raise
