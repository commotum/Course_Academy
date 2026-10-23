"""Independent focused revision audit. Run with the context Python; all output here."""
import sys
sys.dont_write_bytecode=True
import audit as h
import collections, hashlib, json, os, pathlib, random, re, shutil, subprocess
import sympy as s
R=pathlib.Path(__file__).resolve().parent; J=R.parent; W=J/'workspace'; REPO=h.REPO
read=h.read; save=h.save
m=h.load(W)
def hashes():return {str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()}
def norm(v):return re.sub(r'\s+','',v.replace(r'\ln',r'\operatorname{ln}').replace(r'\mid','|').replace('⁡',''))
def parts(v):
 p=re.fullmatch(r'(.*?)\\operatorname\{ln\}\|([^|]+)\|\+C',norm(v));assert p,v
 return h.coeff(p[1]),p[2]
def value(r):return next(c[':answer/value'] for c in h.field(r)[':answer-field/choices'] if c[':answer/id']==h.key(h.field(r)))
def run(cmd,output):
 p=subprocess.run(list(map(str,cmd)),capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(R/'assets')))
 save(output,{'command':list(map(str,cmd)),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr});return p

def main():
 save('package-hashes-before.json',hashes())
 source=read(J/'source/source.json')['material']['kp']; replays=[]; sr=[]
 params=[[2,1,1],[2,3,5],[1,1,-1],[1,-3,2],[3,1,4],[1,1,3]]
 for q,p in zip(source[':knowledge-point/questions'],params):
  r=m.generate(template=q[':question/math-academy-id'],parameters=p,seed=70519);replays.append(r)
  sr.append({'source_id':q[':question/id'],'parameters':p,'prompt_exact':q[':question/problem']==r['question'][':question/problem'],'bank_exact':sorted(c[':answer/value'] for c in q[':question/answer-fields'][0][':answer-field/choices'])==sorted(c[':answer/value'] for c in h.field(r)[':answer-field/choices']),'solution_exact':q.get(':question/worked-solution')==r['question'][':question/worked-solution'] if q.get(':question/worked-solution') else None,'reconstruction':'Missing q-49511 solution and key independently inferred as (2/3)ln|3x+5|+C.' if not q.get(':question/worked-solution') else None})
 canon=m.generate(template='e-449',parameters=[3,5,2],seed=70519);replays.append(canon)
 sr.append({'source_id':source[':knowledge-point/canonical-example'][':question/id'],'prompt_exact':canon['question'][':question/problem']==source[':knowledge-point/canonical-example'][':question/problem'],'solution_exact':canon['question'][':question/worked-solution']==source[':knowledge-point/canonical-example'][':question/worked-solution'],'bank':'No captured bank; extension assessed mathematically.'})
 save('source-replay.json',sr);save('source-replay-records.json',replays)
 samples=[m.generate(seed=k) for k in range(70519,70539)]
 # Small whole-batch controls examine changed batch construction, using fresh seeds.
 controls=m.batch('easy',5,70519)+m.batch('easy',5,70520)
 batch=read(J/'samples.json');save('batch.json',batch);save('samples.json',samples);save('controls.json',controls)
 boundary_parameters=[[1,1,-12],[9,1,12],[1,1,0],[9,1,0],[1,-1,0],[9,9,0],[1,-9,-12],[9,9,12]]
 boundaries=[m.generate(parameters=p,seed=70519) for p in boundary_parameters];save('boundary-records.json',boundaries)
 # Identical banks with changed numerator/argument targets; irrelevant option-order changes.
 cf=[]; cfrows=[]
 for profile in ['coefficient-choice','argument-choice']:
  _,pars=m.candidates(random.Random(70519),[2,3,5],profile)
  group=[m.from_candidates(pars,t,70519,profile) for t in range(5)]
  shuffled=m.from_candidates(pars,0,70520,profile)
  cfrows.append({'profile':profile,'parameters':pars,'relevant_answers':[value(r) for r in group],'distinct_answers':len(set(value(r) for r in group)),'distinct_prompts':len(set(r['question'][':question/problem'] for r in group)),'distinct_solutions':len(set(r['question'][':question/worked-solution'] for r in group)),'irrelevant_answer_preserved':value(shuffled)==value(group[0]),'irrelevant_prompt_preserved':shuffled['question'][':question/problem']==group[0]['question'][':question/problem'],'irrelevant_solution_preserved':shuffled['question'][':question/worked-solution']==group[0]['question'][':question/worked-solution'],'option_order_changed':h.field(shuffled)[':answer-field/choices']!=h.field(group[0])[':answer-field/choices']})
  cf.extend(group+[shuffled])
 save('counterfactual-records.json',cf);save('counterfactuals.json',cfrows)
 # Search only construction parameters to demonstrate the confirmed boundary reaches the normal CLI.
 natural=None
 for seed in range(2000):
  _,pars=m.candidates(random.Random(seed))
  if any(a==1 and b==0 for n,a,b in pars):natural=(seed,m.batch('easy',5,seed));break
 assert natural
 save('natural-boundary.json',{'seed':natural[0],'searched_seeds':[0,natural[0]],'records':natural[1]});save('natural-boundary-records.json',natural[1])
 minimal=m.generate(seed=70519,parameters=[2,1,0]);save('minimal-failure.json',[minimal])
 allrecords=replays+samples+controls+batch+boundaries+cf+natural[1]+[minimal]
 math=[];grader=[]
 for r in allrecords:
  q=r['question']; f=h.field(r); pm=re.search(r'\\d?frac\{(\d+)\}\{([^}]+)\}',q[':question/problem']);assert pm,q
  malformed=bool(re.search(r'x0\b',q[':question/problem']+' '+q[':question/worked-solution']+' '+' '.join(c[':answer/value'] for c in f[':answer-field/choices'])))
  integ=s.Integer(pm[1])/h.expr(pm[2]);answers=[];gchecks=[]
  for ch in f[':answer-field/choices']:
   c,arg=parts(ch[':answer/value']);arg=h.expr(arg);res=s.cancel(c*s.diff(arg,s.Symbol('x'))/arg-integ)
   valid=res==0
   answers.append({'value':ch[':answer/value'],'derivative_residual':str(res),'valid':bool(valid),'key_agrees':bool(valid==(ch[':answer/id']==h.key(f)))})
   if not malformed:gchecks.append({'submitted_answer_id':ch[':answer/id'],'expected':'accepted' if valid else 'rejected','purpose':'Independent exact derivative of visible answer'})
  row={'id':q[':question/id'],'parameters':r['generation']['parameters'],'prompt':q[':question/problem'],'malformed_x0':malformed,'answers':answers,'unique_correct':sum(a['valid'] for a in answers)==1,'solution_final_agrees':norm(value(r)) in norm(q[':question/worked-solution'])}
  row['passed']=not malformed and row['unique_correct'] and all(a['key_agrees'] for a in answers) and row['solution_final_agrees'];math.append(row)
  if gchecks:grader.append({'label':q[':question/id'],'record':r,'checks':gchecks})
 save('math.json',{'records':math,'failures':[r for r in math if not r['passed']],'record_count':len(math)})
 save('grader-input.json',grader)
 # This confirms native radio routing on the defective record; no claim of a correct antiderivative.
 save('malformed-grader-input.json',[{'label':'Malformed display still accepted by native radio routing','record':minimal,'checks':[{'submitted_answer_id':h.key(h.field(minimal)),'expected':'accepted','purpose':'Does the native grader expose the malformed content or merely accept the declared UUID?'}]}])
 render=[minimal]+cf[:2]+[cf[5]]+[cf[6],cf[8],cf[11]]+batch
 save('render-records.json',render)
 inv=read(J/'source/inventory.json');ids={q[':question/id'] for q in source[':knowledge-point/questions']}
 save('inventory-review.json',{'basis':inv['basis'],'records':[{'id':q[':question/id'],'entity_id':q[':db/id'],'original_source':q[':question/id'] in ids,'generation':q.get(':question/generation'),'retired':q.get(':question/retired',False),'has_key':bool(q[':question/answer-fields'][0].get(':answer-field/correct'))} for q in inv['questions']],'generated_count':sum(q[':question/id'] not in ids for q in inv['questions']),'conclusion':'All six stored records are original sources. No historical generated records are present; malformed zero-intercept record is a runtime defect only.'})
 save('affected-inventory.json',{'affected_questions':[]})
 rejects=[]
 for p in [[1,0,0],[0,1,0],[10,1,0],[1,10,0],[1,1,13],[1,1,-13],[True,1,1]]:
  try:m.generate(parameters=p);ok=False
  except ValueError:ok=True
  rejects.append({'parameters':p,'rejected':ok})
 relocated=R/'relocated';relocated.mkdir(exist_ok=True)
 for fn in read(W/'package.json')['files']:
  dest=relocated/fn;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/fn,dest)
 result=run([sys.executable,relocated/'17592186064206.py','--count','5','--seed','994860459','--difficulty','easy'],'relocation-command.json')
 rr=json.loads(result.stdout);save('relocated-batch.json',rr)
 save('packaging.json',{'dependencies':read(W/'package.json')['dependencies'],'installed':{'python':sys.version.split()[0],'packages':{'sympy':s.__version__}},'relocation_exact':rr==batch,'batch_deterministic':m.batch('easy',5,994860459)==batch,'replay_exact':all(m.replay(r['generation'])==r for r in allrecords),'invalid_parameter_rejection':rejects,'output_dir':'No asset-producing code; COURSE_ACADEMY_GENERATOR_OUTPUT_DIR directed into evidence_root.','source_provenance':'Reused helper parsers from independent review 0; current independent inputs and expected derivatives recomputed.'})
 save('scope.json',{'source_refs':h.read(R/'source-analysis.json')['source_refs'],'result':'Construction still aims at one constant over affine denominator, small integer arithmetic, five radio choices, one substitution. Zero intercept is supported by the source reciprocal prerequisite, but emitted x0 is invalid. No additional integration operations introduced. Difficulty remains easy; other levels intentionally unsupported.'})
 print(json.dumps({'records':len(math),'math_failures':len([r for r in math if not r['passed']]),'natural_boundary_seed':natural[0],'boundary_prompt':minimal['question'][':question/problem'],'source_replay_passed':all(r.get('prompt_exact') and r.get('bank_exact',True) and r.get('solution_exact') is not False for r in sr)}))
 (R/'session-state.md').write_text('Independent source replay, math, boundaries, counterfactual records and package relocation complete. Confirmed x0 formatting defect at [2,1,0]; natural batch seed saved. Native grader, delivery and UI checks pending.\n')
if __name__=='__main__':main()
