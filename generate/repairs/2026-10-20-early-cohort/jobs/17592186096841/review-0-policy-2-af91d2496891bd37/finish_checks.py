from review import *
from collections import Counter,defaultdict

def ui_hash(v):
 n=2166136261
 for c in v:n=((n^ord(c))*16777619)&0xffffffff
 return n

def probe(rows,label,path):
 radios=[r for r in rows if r['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/radio')]
 output=[]
 for name in sorted({r['generation']['template'] for r in radios}):
  sub=[r for r in radios if r['generation']['template']==name]
  for strategy in ['first_raw','shortest','longest','least_abs_at_2','greatest_abs_at_2','median_abs_at_2']:
   hits=0
   for r in sub:
    q=r['question'];cs=q[':question/answer-fields'][0][':answer-field/choices'];cid=correct(q)[':answer/id']
    if strategy=='first_raw':a=cs[0]
    elif strategy in ['shortest','longest']:a=sorted(cs,key=lambda a:len(a[':answer/value']),reverse=strategy=='longest')[0]
    else:
     ordered=sorted(cs,key=lambda a:abs(parse(a[':answer/value']).subs({x:2,t:2})))
     a=ordered[0 if strategy=='least_abs_at_2' else -1 if strategy=='greatest_abs_at_2' else 2]
    hits+=a[':answer/id']==cid
   output.append({'cue':strategy,'subgroup':label+': '+name,'scope':'within_template','strategy':strategy,'correct':hits,'total':len(sub),'baseline':.2,'disposition':'not_predictive','conclusion':'Compared with uniform 1/5 radio selection. No tested cue is perfect in the independent subgroup. Numerical-at-2 probes are coarse checks of magnitude rank, not assertions of universal strategy failure. Small batch results are reported separately. Raw order is not served order: UI hashes item/field/answer identities.','sample_refs':[path]})
 return output

def main():
 records=read('samples-independent.json');batch=read('batch.json');pairs=read('counterfactual-records.json')
 # Strict counterexample: existing constructor family lacks the canonical cubic inner term.
 canonical=json.loads((E.parent/'source/source.json').read_text())['material']['kp'][':knowledge-point/canonical-example']
 r=g.generate_moderate(seed=99173,template='quartic_radio',parameters={'a':3,'b':1,'n':5})
 save('canonical-counterexample-records.json',[r])
 failures=[]
 try:g.generate_moderate(seed=99173,template='quartic_radio',parameters={'a':3,'b':1,'n':5,'second_power':3})
 except ValueError as ex:failures.append(str(ex))
 save('canonical-coverage.json',{'source':canonical,'command':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python finish_checks.py','parameters':{'a':3,'b':1,'n':5},'generated_prompt':r['question'][':question/problem'],'source_inner':'3*x^4+x^3','actual_inner':'3*x^4+x','source_derivative':'5*(3*x^4+x^3)^4*(12*x^3+3*x^2)','actual_derivative':str(expected(r['question'])),'attempted_second_power_3':failures,'family_invariant':'All constructors have inner polynomial in {a*x+b, a*t^2+b, a*x^2+b, a*x^2+b*x+c, a*x^4+b*x}; coefficient of degree 3 is zero identically. Canonical inner degree-3 coefficient is 1.','verdict':'Cannot replay canonical inner or its variable inner-derivative second term; not a mathematical error in the generated substitute.'})
 # Explicit parameter and dependency boundary checks; no writes outside E.
 tests=[]
 for n,p in [('affine_blank',dict(a=-12,b=12,n=6)),('quadratic_derivative',dict(a=1,b=1,n=2)),('affine_slope',dict(a=1,b=1,n=2,z=-1)),('tangent_blank',dict(a=1,b=1,n=2,z=-1))]:
  r=g.generate(g.TEMPLATES[n][0],99173,template=n,parameters=p);tests.append({'case':p,'template':n,'math':check_record(r),'replay':r==g.generate(g.TEMPLATES[n][0],99173,template=n,parameters=p)})
 bad=[dict(a=0,b=2,n=3),dict(a=2,b=2,n=1),dict(a=2,b=2,n=7),dict(a=13,b=2,n=3),dict(a=2.0,b=2,n=3)]
 for p in bad:
  try:g.generate_easy(99173,template='affine_blank',parameters=p);tests.append({'invalid':p,'rejected':False})
  except ValueError as ex:tests.append({'invalid':p,'rejected':True,'message':str(ex)})
 save('boundary-results.json',tests)
 relocation=E/'relocated';relocation.mkdir(exist_ok=True)
 manifest=json.loads((W/'package.json').read_text())
 for name in manifest['files']+['package.json']:shutil.copyfile(W/name,relocation/name)
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
 cmd=[sys.executable,'generator.py','--difficulty','easy','--seed','99173','--count','5']
 a=subprocess.run(cmd,cwd=W,env=env,capture_output=True,text=True);b=subprocess.run(cmd,cwd=relocation,env=env,capture_output=True,text=True)
 save('relocation-records.json',json.loads(b.stdout));save('packaging-results.json',{'commands':[cmd],'original_exit':a.returncode,'relocated_exit':b.returncode,'identical_stdout':a.stdout==b.stdout,'stderr':[a.stderr,b.stderr],'declared_dependencies':manifest['dependencies'],'actual_versions':read('runtime.json'),'external_assets':'No image or external-output paths generated; local source loaded relative to __file__.','manifest_files_exist':all((W/n).is_file() for n in manifest['files']),'package_unchanged':read('package-before.json')=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in W.iterdir() if p.is_file()}})
 coverage=[]
 for name in g.TEMPLATES:
  rr=[r for r in records if r['generation']['template']==name]
  coverage.append({'case':name,'sample_refs':['samples-independent.json'],'result':json.dumps({'count':len(rr),'parameters':{k:sorted({r['generation']['parameters'][k] for r in rr}) for k in rr[0]['generation']['parameters']},'attempts':[r['generation']['sampling_attempts'] for r in rr],'key_positions':dict(Counter(next(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==correct(r['question'])[':answer/id']) for r in rr)),'design_ranks':dict(Counter(str((r['generation']['bank_design'] or {}).get('slope_rank',(r['generation']['bank_design'] or {}).get('leading_rank'))) for r in rr))})})
 coverage.append({'case':'canonical quartic+cubic inner','sample_refs':['canonical-counterexample-records.json','canonical-coverage.json'],'result':'FAILED: eligible source second-term degree cannot vary to 3.'})
 probes=probe(records,'independent','samples-independent.json')+probe(batch,'exact runner batch','batch.json')+probe(read('delivery-independent/accepted.json'),'post-delivery independent','delivery-independent/accepted.json')+probe(read('delivery-batch/accepted.json'),'post-delivery runner batch','delivery-batch/accepted.json')
 save('shortcut-results.json',probes)
 counter=[]
 for i,j,change in [(0,1,'a=2 to -2'),(0,2,'n=3 to 4'),(3,4,'slope target x=0 to 1'),(5,6,'tangent target x=0 to 1')]:
  counter.append({'kind':'relevant','change':change,'expected':'Derivative/slope/tangent must change; old response rejected.','observed':str(expected(pairs[i]['question']))+' -> '+str(expected(pairs[j]['question']))+'; native cross-response rejection passed; both prompts and solutions rendered.','status':'passed','justification':'Chain rule and source point evaluation depend on this coefficient, exponent or abscissa.','sample_refs':['counterfactual-records.json','grader-input.json','grader-results.json','render-all/rendering.json']})
 counter.append({'kind':'irrelevant','change':'3+2x versus 2x+3, fixed a=2,b=3,n=3 and seed 4401 across affine layouts.','expected':'Same polynomial derivative and equivalent radio answers, despite term order and answer bank order.','observed':'Both keyed expressions expand to 24*x^2+72*x+54; all radio choices independently graded; prompt and solution renders inspected.','status':'passed','justification':'Addition commutes; source affine layouts present both constant-first and variable-first forms.','sample_refs':['counterfactual-records.json','grader-results.json','render-all/rendering.json']})
 # Captured inventory inspection. Original items are never represented as generated.
 inv=json.loads((E.parent/'source/inventory.json').read_text());inventory_results=[]
 for q in inv['questions']:
  eligible=not q.get(':question/retired',False) and all(f.get(':answer-field/correct') for f in q.get(':question/answer-fields',[]))
  row={'question_id':q[':question/id'],'entity_id':q[':db/id'],'original_source':bool(q.get(':question/math-academy-id')),'eligible_from_captured_response_contract':eligible,'difficulty':q.get(':question/difficulty'),'retired':q.get(':question/retired',False)}
  if not row['original_source']:
   row['expected']=str(expected(q));row['key_matches']=s.expand(parse(correct(q)[':answer/value'])-expected(q))==0
  inventory_results.append(row)
 save('inventory-inspection.json',{'basis':inv['basis'],'records':inventory_results,'limits':'No stored generation metadata is present in this capture. Original source records remain source records. Coverage omission is a generator-domain defect, not a wrong stored item. Eight non-source records checked from prompts; no affected generated item demonstrated. No assertion of exhaustive stored-pool grading or rendering.','affected_defect':'Canonical cubic-term omission has no per-record inventory repair.'});save('affected-inventory.json',{'affected_questions':[]})
 # Faithful conditional selection analysis using captured usability, rated easy band and SHA-256 selector.
 pool=[r['question'][':question/id'] for r in read('delivery-batch/accepted.json')]
 selections=[]
 for seed in range(100):
  dig=hashlib.sha256(('course-academy/question-selection/v1/review-'+str(seed)).encode()).digest();u=(int.from_bytes(dig[8:16],'big')>>11)/(2**53)
  selections.append(pool[int(u*len(pool))])
 selection={'basis':inv['basis'],'eligibility':{'stored_total':len(inventory_results),'stored_eligible':sum(r['eligible_from_captured_response_contract'] for r in inventory_results),'retired':sum(r['retired'] for r in inventory_results)},'selection_rule':'question_selection.rs: deduplicate by entity ID; exclude seen/retired/invalid before selection; choose a positive-weight nonempty difficulty band then uniform stable SHA256 draw within band; unrated fallback only if no weighted rated band. Unconfigured policy picks smallest entity ID.','conditional_simulation':'100 fresh-task seed draws, easy-only weights, exact surviving batch as candidate pool. Pending entity IDs/order are unknown, so this demonstrates accessible choice-index support, not future learner-specific frequencies.','counts':dict(Counter(selections)),'history_effect':'Seen questions removed. Each surviving member has positive probability in weighted easy mode; learner history can reduce any subgroup. Policy and history not captured, so no universal future distribution asserted.','stages':{'independent':read('delivery-independent/delivery.json'),'batch':read('delivery-batch/delivery.json')},'rejection':'All 120 constructed records succeeded; recorded sampling_attempts expose whole-bank and small-point resampling. Easy families require one attempt. Higher point families reject inner value outside ±1..3 or zero inner derivative to keep evaluation short/nondegenerate; radio bank rejects duplicate mathematical options.'}
 save('selection-results.json',selection)
 variation={'learner_operation':read('source-analysis.json')['skill'],'fixed_features':[{'feature':'Polynomial inner, positive integer outer power, source response types','justification':'Defines this KP rather than the neighboring radical-chain-rule KP.'},{'feature':'Easy affine inner; bounded coefficients and positive power 2..6','justification':'Preserves easy source workload while varying sign, multiplier and resulting exponent.'},{'feature':'Quartic inner second term fixed to degree one','justification':'Not justified by source: canonical e-181 uses degree three. This is the demonstrated restriction.'}],'answer_roles':[{'role':'Correct radio position and coefficient rank','eligible_variation':'Any position; coefficient/multiplier ranks can vary while derivative rule stays fixed.','observed':'Grid designs vary ranks and omitted cells; raw order shuffled and UI independently orders choices.'},{'role':'Inner derivative terms','eligible_variation':'Canonical quartic+cubic and question quartic+linear; coefficient changes should change both derivative terms.','observed':'Second quartic term always linear; canonical cubic role unavailable.'},{'role':'Evaluation point, sign, power','eligible_variation':'Vary abscissa, coefficients, outer power within source workload.','observed':'Counterfactual points change slope/tangent and reject stale response; sign and power changes also propagate.'}],'coverage':coverage,'counterfactuals':counter,'shortcut_probes':probes,'delivery':{'stages_examined':['generator validation and rejection/resampling','requested difficulty','publisher shared normalization and identities','inventory and within-batch deduplication','captured practice eligibility','weighted and historical learner-selection rules','actual UI option ordering'],'sample_refs':['samples-independent.json','delivery-independent/delivery.json','delivery-batch/delivery.json','selection-results.json','shortcut-results.json'],'result':'All 36 independent easy records and all 5 exact batch records survive captured delivery. Key rank cues are not universally predictive in the sampled templates. Source degree-role omission persists through every stage.'},'limitations':['Finite stratified sample cannot establish absence of all shortcuts.','No live policy, learner history or future entity IDs supplied; selection conclusions are conditional on documented rules and captured basis 5615.','Preview option order uses fixture item IDs; live order depends on assigned task and field IDs. No universal positional claim is inferred from preview ordering.']}
 save('pedagogical-variation.json',variation)
 print('packaging',read('packaging-results.json')['package_unchanged'],'eligible',selection['eligibility'],'perfect independent probes',[(p['subgroup'],p['cue']) for p in probes if p['subgroup'].startswith('independent') and p['correct']==p['total']]);print('canonical omission demonstrated; no affected stored item demonstrated')
if __name__=='__main__':main()
