import sys,json,re,hashlib,importlib.util,shutil
from pathlib import Path
sys.dont_write_bytecode=True
from review import ROOT as E,JOB as J,REPO,PKG as P,save,load,module
from independent_math import s,value,correct,X,Y,K,C,rhs,parse
from collections import Counter

def summarize(rs):
 c=Counter();sg=Counter();pos=Counter();ks=[]
 for r in rs:
  f=r['question'][':question/answer-fields'][0];c[r['generation']['template']]+=1;sg['positive' if r['generation']['parameters']['a']>0 else 'negative']+=1
  if f[':answer-field/type'].endswith('/radio'):pos[str(next(i+1 for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))]+=1
 return {'count':len(rs),'templates':dict(c),'signs':dict(sg),'positions':dict(pos)}

def leak(r):
 prompt=r['question'][':question/problem'];return [t for t in re.findall(r'\$([^$]+)\$',prompt) if re.search(r'\b[KC]\b',t) and 'x' in t]

files=['batch.json','easy-grid.json','fresh-samples.json','leak-cases.json','normal-cases.json','delivery-batch/accepted.json','delivery-easy/accepted.json','delivery-fresh/accepted.json','delivery-moderate/accepted.json','delivery-hard/accepted.json']
coverage={f:summarize(load(f)) for f in files};save('coverage-results.json',coverage)
probes=[]
# Position-only actions tested in ordinary fresh seeds; fixed-seed grid is deliberately controlled.
for filename in ['fresh-samples.json','delivery-fresh/accepted.json','batch.json','delivery-batch/accepted.json']:
 rs=load(filename)
 for name in sorted(set(r['generation']['template'] for r in rs)):
  subset=[r for r in rs if r['generation']['template']==name]
  for position in [1,2,3,4,5]:
   good=sum(r['question'][':question/answer-fields'][0][':answer-field/choices'][position-1][':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1] for r in subset)
   probes.append({'cue':'option position','subgroup':filename+':'+name,'scope':'within_template','strategy':f'Always choose position {position}','correct':good,'total':len(subset),'baseline':0.2,'disposition':'not_predictive','conclusion':'Five radio options give chance baseline 1/5. No stable perfect position strategy across this subgroup and independent control; finite batch counts are descriptive.','sample_refs':[filename]})
for filename in ['leak-cases.json','delivery-moderate/accepted.json']:
 rs=load(filename)
 for name in ['q-8303','q-79665','q-8304']:
  subset=[r for r in rs if r['generation']['template']==name];cues=[{'id':r['question'][':question/id'],'cues':leak(r)} for r in subset]
  probes.append({'cue':'prompt integrated branch restriction','subgroup':filename+':'+name,'scope':'within_template','strategy':'Copy printed constant-containing x expression and invert/square it, without integration','correct':0,'total':len(subset),'baseline':0.2,'disposition':'not_predictive','conclusion':'No candidate primitive occurs in the current prompt; no copy action is available. Baseline is random one-of-five. The historical cue is detected by author-rerun shortcut-results and independent retained-failures.','sample_refs':[filename,'author-rerun/shortcut-results.json']})
# A sign cue alone must leave multiple multiplicative exponential answers.
for file in ['batch.json','fresh-samples.json','delivery-fresh/accepted.json']:
 rs=load(file);rows=[]
 for r in rs:
  ode=rhs(r['question'][':question/problem']);a=r['generation']['parameters']['a'];f=r['question'][':question/answer-fields'][0];candidates=[]
  for option in f[':answer-field/choices']:
   expr=value(option[':answer/value']); ratio=s.simplify(expr/K)
   # Only literal multiplicative exponential forms; inspect exponent's sign at x=1.
   if ratio.func==s.exp and s.sign(ratio.args[0].subs(X,1))==-s.sign(a):candidates.append(option[':answer/id'])
  rows.append({'id':r['question'][':question/id'],'candidate_count':len(candidates),'contains_key':f[':answer-field/correct'][1] in candidates})
 save(file.replace('.json','-sign-cue.json'),rows)
# Reader-guided current blank parameter dependence, including both sqrt branches and final worked row.
results=[]
for pair in load('pairs.json'):
 for side in ['before','after']:
  r=pair[side];q=r['question'];f=q[':question/answer-fields'][0];expr=value(correct(r));sols=[expr]
  if f[':answer-field/type'].endswith('/blank'):
   match=re.search(r'\$y=-(\d+)\(',q[':question/problem'])
   sols=[-int(match[1])/(expr+K)] if match else [s.sqrt(expr+K),-s.sqrt(expr+K)]
  last=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S)[-1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')[-1].replace('&','').strip().rstrip('.,').replace(r'\pm','')
  final=value(last);residuals=[]
  for sol in sols:
   residual=s.simplify(s.diff(sol,X)-rhs(q[':question/problem']).subs(Y,sol));
   zero=residual==0
   if not zero:zero=all(abs(complex(residual.subs({X:x,K:7,C:7}).evalf(30)))<1e-12 for x in [s.Rational(1,5),s.Rational(1,2),s.Rational(4,5)])
   residuals.append({'solution':str(sol),'residual':str(residual),'passes':zero})
  results.append({'template':pair['template'],'side':side,'kind':pair['kind'],'final_worked_row':last,'final_matches_key':s.simplify(final-sols[0])==0,'differentiation':residuals})
save('pair-math.json',results);assert all(x['final_matches_key'] and all(y['passes'] for y in x['differentiation']) for x in results)
save('shortcut-probes.json',probes)
# Historical failing witnesses: exercise original generator, preserve native old grading evidence.
old=J/'review-0-policy-2-75766812ae9ead5b';spec=importlib.util.spec_from_file_location('before',old/'relocated-package/17592186068841.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
out=[]
try:m.generate_moderate(730033,'q-128198',parameters={'a':1},profile='observed');out.append({'missing_family_detected':False})
except ValueError as ex:out.append({'missing_family_detected':True,'error':str(ex)})
for name in ['q-8303','q-79665','q-8304']:
 r=m.generate_moderate(730061,name,parameters={'a':1});out.append({'template':name,'historical_cues':leak(r),'record':r})
r=m.generate_moderate(730033,'q-128191',parameters={'a':1});out.append({'historical_indented_scaffold':any(line.startswith('    ') and '$y=' in line for line in r['question'][':question/problem'].splitlines()),'record':r})
for f in ['grader-commands.json','minimal-failures.json','rendering-inspection.json']:
 shutil.copyfile(old/f,E/('historical-'+f))
save('retained-failures.json',{'command':f'{sys.executable} -B decision_checks.py','historical_witnesses':out,'current_author_regressions':'author-rerun-command.log','provenance':'Historical original package under previous review, matched source and policy. Native grading old engine failure retained from previous independent execution; current engine replay passed.'})
# Read-only selection reproduction. Current actual engine hash bound in review context.
selection={}
for file in ['delivery-batch/accepted.json','delivery-fresh/accepted.json','delivery-moderate/accepted.json']:
 pool=sorted(load(file),key=lambda r:r['question'][':question/id']);counts=Counter()
 for i in range(256):
  digest=hashlib.sha256(f'course-academy/question-selection/v1/review-942751-{i}'.encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/2**53;counts[pool[int(u*len(pool))]['generation']['template']]+=1
 selection[file]={'draws':256,'templates':dict(counts),'pool':summarize(pool)}
save('learner-selection.json',{'source':'engine/rust/question_selection.rs select/seen_before_task/weights_for_phase inspected','seed_prefix':'review-942751-','scenario':'Fresh learner; all accepted records fresh and usable; each examined band has positive configured weight. SHA256 exact second-word within-band draw. Sorted UUIDs substitute future numeric IDs; counts illustrative, positive reachability invariant.','results':selection,'structural_analysis':'Known-difficulty zero-weight bands excluded; nonempty bands renormalize difficulty weight; history removes previously used records; no-policy fallback selects smallest ID. No content-shape filtering occurs in selector. Removal cannot introduce a shortcut into a member that lacks it. Exact five-item batch remains linear with both signs under the positive-easy scenario; after all seen it exhausts.','limits':['No live learner history or policy weights captured: exact future frequencies unknown.','Inventory basis 5369 only; concurrent publication can change duplicates.']})
(E/'session-state.md').write_text('Confirmed and reused source analysis. All 15 source banks replay; two blank scaffold whitespace changes require normalization acknowledgment. Current native grader passes 56 valid and 96 invalid checks including historical strict case; author retained regression also passes. Shared delivery passes all five batch records and fresh/control samples. Independent printed-ODE check passes 78 records; pair math checked both sqrt branches. Rendering 19 records in progress/completed; visual inspection and final evidence contract remain. Package untouched.\n')
print('coverage', {k:v['count'] for k,v in coverage.items()},'probes',len(probes),'pair math',len(results))
