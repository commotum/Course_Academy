"""Source replay plus a small regression sample for the unchanged easy scope.
Independent parsing, native grading, delivery and relocation; evidence only.
"""
import sys
sys.dont_write_bytecode=True
import json,re,hashlib,shutil,subprocess,tempfile
from collections import Counter
from pathlib import Path
from regressions import W,REPO,JOB,EV,module,save,call,verify_math,leakage
from printed_math import value,correct,rhs,s,X,Y,K,C

def source_replay(m):
 source=json.loads((JOB/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions'];results=[];records=[]
 for q in source:
  n=q[':question/math-academy-id'];level=q[':question/difficulty'][':db/ident'].split('/')[-1];a=m.SOURCE_DEFAULTS[n]
  r=m.generate(level,730033,n,parameters={'a':a},profile='observed');records.append(r);g=r['question'];f=g[':question/answer-fields'][0];sf=q[':question/answer-fields'][0]
  got=[value(a[':answer/value']) for a in f[':answer-field/choices']];wanted=[value(a[':answer/value']) for a in sf[':answer-field/choices']]
  # Bijective matching preserves duplicate source distractors as separate entries.
  remaining=list(got);matched=0
  for v in wanted:
   i=next((i for i,w in enumerate(remaining) if s.simplify(v-w)==0),None)
   if i is not None:remaining.pop(i);matched+=1
  prompt_match=re.sub(r'\s+','',g[':question/problem'])==re.sub(r'\s+','',q[':question/problem'])
  solution_match=g[':question/worked-solution']==q[':question/worked-solution']
  key_match=s.simplify(value(correct(r))-value(sf[':answer-field/correct'][':answer/value']))==0
  shape_match=f[':answer-field/type']==sf[':answer-field/type'][':db/ident'] and f[':answer-field/key']==sf[':answer-field/key']
  result={'template':n,'source_question_id':q[':question/id'],'source_entity_id':q[':db/id'],'matched_choices':matched,'source_choices':len(wanted),'extra_choices':len(remaining),'prompt_equal_ignoring_whitespace':prompt_match,'worked_solution_exact':solution_match,'correct_value_equal':key_match,'field_contract_equal':shape_match}
  results.append(result)
 save('source-replay-records.json',records);save('source-replay-results.json',results)
 assert all(x['matched_choices']==x['source_choices'] and not x['extra_choices'] and all(x[k] for k in ['prompt_equal_ignoring_whitespace','worked_solution_exact','correct_value_equal','field_contract_equal']) for x in results),results
 # Small current normal sample across every source route checks prior repairs.
 normal=[m.generate(q[':question/difficulty'][':db/ident'].split('/')[-1],730033,q[':question/math-academy-id'],parameters={'a':m.SOURCE_DEFAULTS[q[':question/math-academy-id']]}) for q in source]
 verify_math(normal,'source-normal-math.json');save('source-normal-records.json',normal)
 print('source replay: 15/15 complete banks, fields, normalized prompts and exact worked solutions; normal math 15/15',flush=True)

def coverage(records):
 report={}
 for template in sorted({r['generation']['template'] for r in records}):
  rs=[r for r in records if r['generation']['template']==template];group=[]
  for r in rs:
   q=r['question'];f=q[':question/answer-fields'][0];v=value(correct(r));group.append({'id':q[':question/id'],'a':r['generation']['parameters']['a'],'correct_position':next(i+1 for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]),'printed_rhs':str(rhs(q[':question/problem'])),'answer':str(v)})
  # Each of the tested sign and boundary cases must have a different primitive.
  assert len({g['answer'] for g in group})==len(group)
  assert {1 if g['a']>0 else -1 for g in group}=={-1,1}
  positions=Counter(g['correct_position'] for g in group)
  assert len(positions)>1,(template,positions)
  # None of these incidental structural choices can select the exact key:
  # template alone, printed position, or number of choices. Constant output
  # transform is justified by the fixed y logarithmic primitive, not a cue.
  report[template]={'semantic_odes':len({g['printed_rhs'] for g in group}),'correct_positions':dict(positions),'correct_choice_count':1,'option_count':5,'fixed_position_best_successes':max(positions.values()),'trials':len(group),'cases':group}
 return report

def main():
 m=module();source_replay(m)
 easy=[m.generate_easy(730111+i,n,parameters={'a':a}) for n in ['easy_linear','easy_constant'] for i,a in enumerate([-12,-2,2,12])]
 verify_math(easy,'easy-math.json')
 batch=[m.generate_easy(1492179634+i) for i in range(5)];save('batch.json',batch)
 save('easy-records.json',easy)
 for name,records in [('easy',easy),('batch',batch)]:
  inp=save(name+'-delivery-input.json',records)
  call([sys.executable,REPO/'generate/pipeline/check_delivery.py','--input',inp,'--source',JOB/'source/source.json','--inventory',JOB/'source/inventory.json','--difficulty','easy','--output',EV/('delivery-'+name)],name+'-delivery-command.json')
 raw=coverage(easy);delivered=json.loads((EV/'delivery-easy/accepted.json').read_text());assert len(delivered)==6;after=coverage(delivered)
 save('easy-coverage.json',{'raw':raw,'delivered':after,'finite_supported_domain':{'easy_linear':24,'easy_constant':24},'sampling_scope':'8 sign/boundary semantic ODEs, not permutations; prior independent review tested all 48 unchanged easy ODEs. Requested five-question batch separately filtered.','selection':'Positive-weight requested band: all accepted fresh usable members have positive probability. engine/rust/question_selection.rs sorts/deduplicates candidates and samples difficulty then item. Learner history and live policy weights are not available; no exact future frequencies claimed. An unconfigured distribution selects the first sorted eligible candidate.'})
 cases=[]
 for r in easy+batch:
  f=r['question'][':question/answer-fields'][0]
  cases.append({'label':'independently differentiated easy bank','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'independent differentiation checked the key; native ID grading checks whole bank'} for a in f[':answer-field/choices']]})
 # Relevant change under fixed seed: coefficient sign, power in a blank, and
 # coefficient of the restored blank. Irrelevant change: order-only random seed.
 pairs=[]
 for level,name,a,b in [('easy','easy_linear',2,-2),('easy','easy_constant',2,-2),('moderate','q-128191',1,4),('moderate','q-128198',1,8),('moderate','q-79665',1,2),('moderate','q-8303',1,2),('moderate','q-8304',1,2)]:
  first=m.generate(level,730061,name,parameters={'a':a});second=m.generate(level,730061,name,parameters={'a':b});assert s.simplify(value(correct(first))-value(correct(second)))!=0
  assert rhs(first['question'][':question/problem'])!=rhs(second['question'][':question/problem'])
  assert first['question'][':question/worked-solution']!=second['question'][':question/worked-solution']
  f=second['question'][':question/answer-fields'][0];old=correct(first)
  if f[':answer-field/type'].endswith('/blank'):
   cases.append({'label':f'changed {name} rejects stale answer','record':second,'checks':[{'submitted':old,'expected':'rejected','purpose':'same presentation settings, changed differential equation requires changed blank'}]})
  else:
   # Check the native key for the changed bank. Math change checked above.
   cases.append({'label':f'changed {name} actual grading','record':second,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'changed relevant evidence, coherent new answer bank'} for a in f[':answer-field/choices']]})
  pairs.append({'kind':'relevant','before':first,'after':second})
 for level,name in [('easy','easy_linear'),('easy','easy_constant'),('moderate','q-128198')]:
  first=m.generate(level,730061,name,parameters={'a':2});second=m.generate(level,730067,name,parameters={'a':2});assert first['question'][':question/problem']==second['question'][':question/problem'];assert first['question'][':question/worked-solution']==second['question'][':question/worked-solution'];assert correct(first)==correct(second)
  pairs.append({'kind':'irrelevant','before':first,'after':second})
 save('counterfactual-records.json',pairs)
 inp=save('easy-counterfactual-grader-input.json',cases);call([REPO/'generate/runs/current/check-engine',inp,EV/'easy-counterfactual-grader-report.json'],'easy-counterfactual-grader-command.json')
 # Actual source-backed context, no runtime files besides the manifest's list.
 manifest=json.loads((W/'package.json').read_text());assert manifest['dependencies']=={'python':sys.version.split()[0],'packages':{'sympy':s.__version__}}
 with tempfile.TemporaryDirectory(dir=EV) as tmp:
  dest=Path(tmp)
  for name in manifest['files']:
   target=dest/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/name,target)
  cmd=[sys.executable,'-B',dest/manifest['entrypoint'],'--difficulty','easy','--count','5','--seed','1492179634','--format','json']
  p=subprocess.run([str(x) for x in cmd],cwd='/tmp',text=True,capture_output=True);assert p.returncode==0,p.stderr;relocated=json.loads(p.stdout);assert relocated==batch
  save('relocation.json',{'command':[str(x) for x in cmd],'returncode':p.returncode,'identical_to_original':True,'runtime_files':manifest['files'],'dependencies':manifest['dependencies'],'generated_assets':0})
 # Order-only seed changes cannot be counted as new semantic instances. They
 # also must not encode a fixed label/position strategy within a template.
 order=[]
 for name in ['easy_linear','easy_constant','q-8303','q-79665','q-8304']:
  level='easy' if name.startswith('easy') else 'moderate';positions=[]
  for seed in range(730131,730141):
   r=m.generate(level,seed,name,parameters={'a':2});f=r['question'][':question/answer-fields'][0];positions.append(next(i+1 for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]));assert not leakage(r)
  assert len(set(positions))>1
  order.append({'template':name,'same_semantic_instance':True,'seeds':[730131,730140],'correct_positions':positions})
 save('position-probes.json',order)
 print('easy: 8 semantic sign/boundary cases, 6 delivered (2 inventory duplicates); batch: 5; counterfactuals, grading and relocation pass',flush=True)
if __name__=='__main__':main()
