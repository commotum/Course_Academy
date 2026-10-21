"""Bounded independent review. Run with job Python, PYTHONDONTWRITEBYTECODE=1.
Reads displayed equations; reuses prior independent parser and attack with provenance.
"""
import json,sys,re,importlib.util,collections,hashlib,subprocess,os,pathlib,shutil
import audit as a
E=a.BASE; J=a.JOB; W=J/'workspace'; REPO=a.REPO
COEFS=(-2,-1,1,2,3)
def save(n,v):
 p=E/n;p.parent.mkdir(exist_ok=True,parents=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def load_module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def key(r):return next(z[':answer/value'] for z in a.field(r)[':answer-field/choices'] if z[':answer/id']==a.answer_id(a.field(r)))
def bank(r):return [z[':answer/value'] for z in a.field(r)[':answer-field/choices']]
def stages(r):
 rhs=a.parse(r['question'][':question/problem'].split('=')[1].split('$')[0].rstrip('., '));p=r['generation']['parameters']
 u,v=a.s.symbols('u v',positive=True);sub={a.x:u-p.get('h',0),a.y:v-p.get('k',0)};out=[]
 for block in re.findall(r'\\begin\{aligned\}([\s\S]*?)\\end\{aligned\}',r['question'][':question/worked-solution']):
  for row in block.split(r'\\'):
   if r'\int' in row:continue
   l,rr=row.split('& =');l=l.strip();rr=rr.strip().rstrip('.,').replace('K','C')
   if a.g.D in l:res=a.parse(l.replace(a.g.D,'').strip() or '1')*rhs-a.parse(rr)
   else:res=a.s.diff(a.parse(l).subs(sub,simultaneous=True),v)*rhs.subs(sub,simultaneous=True)-a.s.diff(a.parse(rr).subs(sub,simultaneous=True),u)
   out.append({'row':row,'valid':a.zero(res)})
 return out

def main():
 legacy=load_module('legacy',E/'legacy.py');failing=legacy.generate_easy(101,'exp_linear',parameters={'h':0,'k':0})
 old_hit=a.shortcut(failing)==[a.answer_id(a.field(failing))]
 fixed=a.g.generate_easy(101,'exp_linear',parameters={'h':0,'k':0})
 new_hit=a.shortcut(fixed)==[a.answer_id(a.field(fixed))]
 save('regression-sensitivity.json',{'old_record':failing,'new_record':fixed,'old_unique_shortcut':old_hit,'new_unique_shortcut':new_hit,'passed':old_hit and not new_hit})
 # Demonstrate retained executable preflight rejects the actual old failure.
 spec=importlib.util.spec_from_file_location('author_preflight',E/'author-check.py');check=importlib.util.module_from_spec(spec);spec.loader.exec_module(check)
 current=a.g;a.g=legacy
 try:check.main();negative={'rejected_old':False}
 except AssertionError as ex:negative={'rejected_old':True,'assertion':str(ex)}
 finally:a.g=current
 save('preflight-negative-control.json',negative);assert negative['rejected_old'] and old_hit and not new_hit
 source=json.load(open(J/'source/source.json'))['material']['kp']; records=[];observed=[];replay=[];pairs=[];coverage=[]
 for i,(t,(level,sid)) in enumerate(a.g.TEMPLATES.items()):
  if level!='easy':continue
  p={'h':0 if 'autonomous' in t else -2,'k':3}
  group=[a.g.generate_easy(seed=661019+i,template=t,parameters={**p,'c':c}) for c in COEFS]
  assert len({tuple(bank(r)) for r in group})==1
  assert len({key(r) for r in group})==5
  assert len({r['question'][':question/problem'] for r in group})==5
  assert len({r['question'][':question/worked-solution'] for r in group})==5
  coverage.append({'template':t,'coefficients':list(COEFS),'ordered_bank_identical':True,'distinct_prompts_keys_solutions':5})
  # c=1 -> c=3: same choices, same coordinates; grader must reverse the keys.
  pairs.append({'template':t,'before':group[2],'relevant_after':group[4],'irrelevant_after':a.g.generate_easy(seed=661020+i,template=t,parameters={**p,'c':1})})
  records+=group
  q=next(q for q in source[':knowledge-point/questions'] if q[':question/math-academy-id']==sid)
  r=a.g.generate_easy(seed=660031+i,template=t,parameters={'h':0,'k':0},profile='observed');f=a.field(r);sf=q[':question/answer-fields'][0]
  row={'source_id':q[':question/id'],'template':t,'prompt':r['question'][':question/problem']==q[':question/problem'],'solution':r['question'][':question/worked-solution']==q[':question/worked-solution'],'complete_bank':sorted(bank(r))==sorted(z[':answer/value'] for z in sf[':answer-field/choices']),'correct':key(r)==sf[':answer-field/correct'][':answer/value']}
  replay.append(row);observed.append(r)
  for h,c in [(-6,-2),(6,3)]: records.append(a.g.generate_easy(seed=662231+i,template=t,parameters={'h':0 if 'autonomous' in t else h,'k':h,'c':c}))
 fresh=[a.g.generate_easy(seed=z) for z in range(731871,731882)]
 batch=json.load(open(J/'samples.json'));save('batch-records.json',batch)
 records+=fresh
 # One regression case per unchanged authored band; revised builder/bank applies here too.
 poly=[a.g.generate(level,seed=663019,parameters={'a':6,'b':-5,'c':-2,**({'d':5} if level=='hard' else {})}) for level in ('moderate','hard')]
 allrs=observed+records+batch+poly+[p['irrelevant_after'] for p in pairs]
 results=[a.inspect_record(r) for r in allrs]
 step_results=[{'id':r['question'][':question/id'],'rows':stages(r)} for r in records+batch+poly]
 assert all(r['passed'] for r in results)
 assert all(z['valid'] for row in step_results for z in row['rows'])
 assert all(all(row[k] for k in ('prompt','solution','complete_bank','correct')) for row in replay)
 save('source-replay.json',replay);save('observed-records.json',observed);save('independent-records.json',records);save('controlled-pairs.json',pairs);save('math-results.json',results);save('solution-stage-results.json',step_results);save('coefficient-coverage.json',coverage)
 cases=[]
 for i,r in enumerate(allrs):
  f=a.field(r);cases.append({'label':str(i)+' '+r['generation']['template'],'record':r,'checks':[{'submitted_answer_id':z[':answer/id'],'expected':'accepted' if z[':answer/id']==a.answer_id(f) else 'rejected','purpose':'displayed equation checked by independent differentiation'} for z in f[':answer-field/choices']]})
 pair_results=[]
 for p in pairs:
  b,after,sh=p['before'],p['relevant_after'],p['irrelevant_after']
  # IDs legitimately depend on the instance, so map same displayed choice into new bank.
  old_in_new=next(z[':answer/id'] for z in a.field(after)[':answer-field/choices'] if z[':answer/value']==key(b))
  new_in_old=next(z[':answer/id'] for z in a.field(b)[':answer-field/choices'] if z[':answer/value']==key(after))
  cases += [{'label':'relevant changed role '+p['template'],'record':after,'checks':[{'submitted_answer_id':old_in_new,'expected':'rejected','purpose':'former correct equation now wrong'},{'submitted_answer_id':a.answer_id(a.field(after)),'expected':'accepted','purpose':'new correct coefficient'}]},{'label':'reverse changed role '+p['template'],'record':b,'checks':[{'submitted_answer_id':new_in_old,'expected':'rejected','purpose':'new equation wrong in original ODE'}]},{'label':'irrelevant shuffle '+p['template'],'record':sh,'checks':[{'submitted_answer_id':a.answer_id(a.field(b)),'expected':'accepted','purpose':'unchanged key under option shuffle'}]}]
  row={'template':p['template'],'before_key':key(b),'after_key':key(after),'relevant_bank_preserved':bank(b)==bank(after),'relevant_prompt_solution_key_changed':all(b['question'][k]!=after['question'][k] for k in (':question/problem',':question/worked-solution')) and key(b)!=key(after),'irrelevant_prompt_solution_key_preserved':all(b['question'][k]==sh['question'][k] for k in (':question/problem',':question/worked-solution')) and key(b)==key(sh),'option_order_changed':bank(b)!=bank(sh)}
  assert row['relevant_bank_preserved'] and row['relevant_prompt_solution_key_changed'] and row['irrelevant_prompt_solution_key_preserved']
  pair_results.append(row)
 save('counterfactual-results.json',pair_results);save('grader-input.json',cases)
 save('delivery-input.json',records+batch)
 # All batch and a visually representative subset including counterfactuals and new builder trig/log notation.
 chosen=[p['before'] for p in pairs]+[pairs[0][k] for k in ('before','relevant_after','irrelevant_after')]+batch
 save('render-records.json',chosen)
 invalid=[]
 for kw in [dict(parameters={'h':0,'k':0,'c':0}),dict(parameters={'h':0,'k':0,'c':True}),dict(parameters={'h':0,'k':0,'c':4}),dict(parameters={'h':7,'k':0}),dict(template='arcsin_autonomous',parameters={'h':1,'k':0}),dict(profile='observed',parameters={'h':0,'k':0,'c':2}),dict(field_type='free'),dict(template='two_x_terms')]:
  try:a.g.generate_easy(**kw);ok=False;msg='accepted'
  except ValueError as ex:ok=True;msg=str(ex)
  invalid.append({'arguments':kw,'rejected':ok,'message':msg})
 assert all(z['rejected'] for z in invalid)
 assert all(r==a.g.generate_easy(seed=r['generation']['seed']) for r in fresh)
 rel=E/'relocated';rel.mkdir(exist_ok=True)
 for f in json.load(open(W/'package.json'))['files']:
  dst=rel/f;dst.parent.mkdir(exist_ok=True,parents=True);shutil.copyfile(W/f,dst)
 cmd=[str(a.PY),str(rel/'17592186068844.py'),'--difficulty','easy','--seed','731871','--count','3','--format','json']
 run=subprocess.run(cmd,cwd='/tmp',env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
 assert run.returncode==0,run.stderr
 relrs=json.loads(run.stdout);save('relocation-records.json',relrs);assert relrs==fresh[:3]
 deps={'python':sys.version.split()[0],'packages':{'sympy':a.s.__version__}}
 declared=json.load(open(W/'package.json'))['dependencies'];assert deps==declared
 save('packaging-results.json',{'commands':[cmd],'relocation_equal':True,'exact_declared_versions':declared,'actual_versions':deps,'deterministic_fresh_seeds':list(range(731871,731882)),'boundary_rejections':invalid,'runtime_outputs':'JSON stdout; no external images or database access; declared source fixture loaded relative to entrypoint','resampling':'No stochastic rejection/resampling loop exists; valid c,h,k yield five algebraically distinct equations. Independent boundary and controlled samples check this.'})
 # Reuse and reverify all previously demonstrated legacy affected inventory; no originals labeled generated.
 inv=json.load(open(J/'source/inventory.json'));prior=J/'review-0-policy-2-555bf50a221eb6e3'
 originals={q[':question/id'] for q in source[':knowledge-point/questions']};oldrecords=json.load(open(prior/'generated-records.json'));captured={q[':question/id']:q for q in inv['questions']};generated=[];affected=[]
 for r0 in oldrecords:
  m=r0['generation'];r=legacy.generate(r0['question'][':question/difficulty'].split('/')[-1],m['seed'],parameters=m['parameters'],profile=m['bank_profile']);q=captured[r['question'][':question/id']]
  assert r==r0 and q[':question/id'] not in originals
  assert all(r['question'][k]==q[k] for k in (':question/id',':question/problem',':question/worked-solution'))
  assert sorted(bank(r))==sorted(z[':answer/value'] for z in q[':question/answer-fields'][0][':answer-field/choices'])
  assert a.answer_id(a.field(r))==q[':question/answer-fields'][0][':answer-field/correct'][':answer/id']
  assert a.shortcut(r)==[a.answer_id(a.field(r))]
  generated.append(r);affected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'finding':'Retained legacy R,-R,2R choice-only shortcut; current v2 construction does not reproduce this defect.','reproduction':'PYTHONDONTWRITEBYTECODE=1 '+str(a.PY)+' independent-review.py; legacy.generate('+repr(r['question'][':question/difficulty'].split('/')[-1])+', seed='+repr(m['seed'])+', parameters='+repr(m['parameters'])+', profile='+repr(m['bank_profile'])+')','evidence_path':'generated-records.json'})
 assert len(generated)==len(set(captured)-originals)==10
 save('generated-records.json',generated);save('affected-inventory.json',{'affected_questions':affected})
 save('inventory-results.json',{'basis':inv['basis'],'source_originals_excluded':len(originals),'non_source_tested':len(generated),'legacy_affected':len(affected),'untested_non_source':0,'versions':'All affected are existing v1 moderate/hard records, none are v2 or requested easy. Reproduced using unchanged failing implementation with complete generated metadata; stored capture omits generation metadata but IDs, key, complete bank, prompt, solution match.','current_package_result':'Legacy findings retained for bank cleanup; not evidence of current construction failure.'})
 summary={'source_banks':len(replay),'math_records':len(results),'math_choices':sum(len(z['choices']) for z in results),'solution_rows':sum(len(z['rows']) for z in step_results),'controlled_easy_families':len(pairs),'fresh_seeds':11,'boundaries':22,'exact_batch':len(batch),'grader_checks':sum(len(z['checks']) for z in cases),'legacy_inventory_affected':len(affected),'passed':True}
 save('independent-summary.json',summary);print(json.dumps(summary))
 (E/'session-state.md').write_text('Independent current-package milestone complete. Source replay, displayed-equation differentiation, intermediate rows, all five coefficient decisions per easy family, boundaries, relocation, parameter rejection and prior-failure sensitivity passed. Saved grader inputs, render inputs, delivery inputs. Actual native grading, delivery and renderer remain. Legacy inventory: ten captured moderate/hard v1 records retain prior defect; current v2 counterexample no longer exposes key.\n')
if __name__=='__main__':main()
