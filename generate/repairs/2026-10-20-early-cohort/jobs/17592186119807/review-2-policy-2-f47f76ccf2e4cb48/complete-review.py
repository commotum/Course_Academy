import json,pathlib,sys,re,itertools,collections,hashlib
from fractions import Fraction as F
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;J=E.parent;P=J/'workspace';REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
def load(p):return json.loads(pathlib.Path(p).read_text())
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
t=(E/'review.py').read_text();exec(t[t.index('def num(s):'):t.index('source=load(J/')])
source=load(J/'source/source.json');kp=source['material']['kp'];analysis=load(E/'source-analysis.json')
save('source-math-results.json',[{'id':q[':question/id'],'truth':truth(q),'captured_key':q.get(':question/answer-fields',[{}])[0].get(':answer-field/correct',{}).get(':answer/value'),'canonical_inferred_sum':q==kp[':knowledge-point/canonical-example']} for q in [kp[':knowledge-point/canonical-example']]+kp[':knowledge-point/questions']])
# Parse the actual written solution rather than metadata or generator variables.
results=[]
for r in load(E/'raw-records.json')+load(E/'batch.json')+load(E/'sign-counterfactual-records.json'):
 q=r['question'];sol=q[':question/worked-solution'];a,c,b=vectors(r)
 m=re.search(r'Finally, we substitute \$\{x\}_\{1\}=([^$]+)\$ and \$\{x\}_\{2\}=([^$]+)\$ into the (first|second|third) equation',sol)
 if m:
  x,y=num(m[1]),num(m[2]);k=('first','second','third').index(m[3]);lhs=a[k]*x+c[k]*y
  assert sum(ai*x+ci*y==bi for ai,ci,bi in zip(a,c,b))>=2
  body=sol[m.end():];aligned=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',body,re.S)[1]
  left,right=aligned.split(r'\\')[-1].strip().split('&=');assert num(left)==lhs and num(right)==b[k]
  assert ('true statement.' in body)==(lhs==b[k])
  results.append({'id':q[':question/id'],'candidate':[str(x),str(y)],'check_row':k,'concrete_check':[str(lhs),str(b[k])],'passed':True})
 else:
  assert a[0]==c[0]==0 and b[0]!=0 and 'first equation is a false statement' in sol
  results.append({'id':q[':question/id'],'immediate_contradiction':str(b[0]),'passed':True})
save('solution-math-results.json',{'command':'<context-python> complete-review.py','method':'Parse candidate coefficients and final concrete check from written TeX; independent Fraction arithmetic on prompt. Source methods checked separately.','records':results})
r=load(E/'render-final/rendering.json');assert r['passed'] and len(r['cases'])==17
save('render-inspection.json',{'passed':True,'renderer':'Actual unmodified UI via render_preview.py --limit 17','screenshots_inspected':[f'render-final/question-{n:03}.png' for n in range(1,18)],'inspection_sheets':[f'ui-sheet-{n:02}.png' for n in range(1,18,2)],'observations':['All five delivered prompts, radio controls, component equations, elimination and final checks display correctly.','q-34568 controlled RHS5->7 flips No solution to2 with displayed7=5->7=7. Seed reorder preserves2.','Four formerly omitted source cases and q-105163 corrected fractional contradiction display correctly.','q-105166 final target component -29->-30 changes No solution to-4 while keeping bank fixed.','q-105165 distractor-rank change changes positive-only to mixed-sign bank while preserving prompt, solution and accepted10.','Actual UI reorders choices; sign and numeric-order probes do not rely on raw ordering.'],'math_errors':sum(len(c['mathErrors']) for c in r['cases']),'javascript_errors':sum(len(c['javascriptErrors']) for c in r['cases'])})
# Independently probe actual finite pools separately from broad controls.
sets=[('raw','raw-records.json'),('post-filter','delivery/accepted.json'),('exact batch','delivery-batch/accepted.json'),('fresh104729','delivery-fresh-104729/accepted.json'),('fresh20261021','delivery-fresh-20261021/accepted.json')]
probes=[];summaries={}
def nums(r):return sorted(num(a[':answer/value']) for a in choices(r) if a[':answer/type']==':answer.type/math')
def groups(rs):
 out=collections.defaultdict(list)
 for r in rs:
  ns=nums(r);profile=r['generation']['source_id'];name='a/b' if '{a}_{1}' in r['question'][':question/problem'] else 'c/d'
  features={'all_negative':max(ns)<0,'zero':0 in ns,'mixed_signs':min(ns)<0<max(ns),'fractional':any(n.denominator!=1 for n in ns)}
  for k in [('profile',profile),('names',name),('nonpositive',str(min(ns)<=0))]+[('bank',k) for k,v in features.items() if v]:out[k].append(r)
 return out
for label,ref in sets:
 rs=load(E/ref);summaries[label]={'metrics':metrics(rs),'groups':{str(k):{'n':len(v),'consistent':sum(truth(r)!='No solution' for r in v)} for k,v in groups(rs).items()}}
 if label.startswith('fresh') or label=='exact batch':
  for sign in ('False','True'):
   items=groups(rs)[('nonpositive',sign)];assert {truth(r)=='No solution' for r in items}=={False,True}
 for subgroup,items in [(('overall',label),rs)]+list(groups(rs).items()):
  scope='overall' if subgroup[0]=='overall' else 'within_template' if subgroup[0]=='profile' else 'other_recognizable_subgroup'
  strategies=[('No solution',lambda r:'No solution'),('smallest numeric',lambda r:str(nums(r)[0])),('largest numeric',lambda r:str(nums(r)[-1])),('second-largest numeric',lambda r:str(nums(r)[-2]))]
  if subgroup[0]=='overall':strategies += [(f'raw position {pos+1}',lambda r,p=pos:choices(r)[p][':answer/value']) for pos in range(5)]
  for strategy,predict in strategies:
   correct=sum(canon(predict(r))==truth(r) for r in items)
   diagnostic=len(items)>1
   assert not (diagnostic and correct==len(items)),(label,subgroup,strategy)
   probes.append({'cue':subgroup[0],'subgroup':label+' '+subgroup[1],'scope':scope,'strategy':'Select '+strategy+' without vector solving.','correct':correct,'total':len(items),'baseline':.2,'disposition':'not_predictive','conclusion':f'{correct}/{len(items)}; baseline .2 is uniform choice among five radio alternatives. '+('Counterexamples observed in this subgroup.' if correct<len(items) else 'Singleton is not diagnostic; no absence claim for this small subgroup. Controlled per-template pairs test the dependency.'),'sample_refs':[ref]})
# Essential mathematical simplification must not be mislabeled a surface shortcut.
zero=[r for r in load(E/'controlled-records.json') if vectors(r)[0][0]==vectors(r)[1][0]==0 and vectors(r)[2][0]!=0]
assert zero and all(truth(r)=='No solution' for r in zero)
probes.append({'cue':'zero coefficient row with nonzero target','subgroup':'controlled q-34242 contradiction','scope':'within_template','strategy':'Select No solution from 0 = nonzero.','correct':len(zero),'total':len(zero),'baseline':.2,'disposition':'intended_skill','conclusion':'Direct component contradiction is the source-supported mathematical decision in 8179ffc2-2381-5ec9-a386-111d6e4cae85; baseline .2 is random among five choices.','sample_refs':['controlled-records.json']})
save('shortcut-results.json',{'command':'<context-python> complete-review.py','summaries':summaries,'probes':probes,'limits':'No finite probe set establishes absence of every shortcut; singletons do not establish a cue family.'})
selection=load(E/'selection-results.json');selection['new_fresh_batches']={name:summaries[name] for name in ('fresh104729','fresh20261021')};selection['limits']=['All items moderate. Positive moderate weights give uniform within-band draws over fresh eligible questions; zero moderate weight excludes this band.','Unconfigured policy chooses smallest entity ID; actual new entity IDs and learner histories are unavailable. Synthetic-ID draw/history tests reproduce inspected source rules; exact future draws are not asserted.','Captured basis5400 contains14 source originals; concurrent writes can change deduplication. A later history can remove counterexamples from any finite pool.'];save('selection-results.json',selection)
grade=load(E/'grader-report.json');assert grade['accepted_checks']==161 and grade['rejected_checks']==644
assert grade.get('unexpected_checks',0)==0
variation={
 'learner_operation':analysis['skill'],
 'fixed_features':analysis['fixed_features']+[{'feature':'Finite source coefficient-column and substitution/elimination profiles','justification':'Conservative moderate family preserves small arithmetic and source methods. Columns do not fix consistency, coefficient sum or correct numeric rank; every profile has controlled counterexamples. This is practice of the stated finite family, not a claim to all real systems.'}],
 'answer_roles':[
 {'role':'Target membership in span','eligible_variation':'Change decisive target component to allow consistent or contradictory equations within each profile and label family.','observed':'All14 profiles support both; relevant pairs update written checks and native accepted choice.'},
 {'role':'Coefficient sum and numeric key rank','eligible_variation':'Vary bounded candidate translations and independent distractor gaps/rank, retaining x1+x2 as the response target.','observed':'All four numeric ranks at fixed evidence in each controlled profile. Exact batch numeric keys10 and-2 occupy ranks1 and3.'},
 {'role':'Incidental answer-bank signs and labels','eligible_variation':'Signs or names cannot replace consistency checks; changing irrelevant distractors must preserve truth.','observed':'Exact batch has both outcomes under both sign cases. q-105165 distractor-only pair preserves10 across positive-only and mixed-sign banks. Finite label groups controlled separately.'}],
 'coverage':[
 {'case':'All complete source exercises','sample_refs':['source-records.json','source-replay.json','source-math-results.json'],'result':'14/14 complete five-choice banks and ordered worked solutions reproduced, with verified q-105163 arithmetic correction; canonical sum-10 independently confirmed.'},
 {'case':'Both outcomes and four numeric ranks in every source coefficient profile','sample_refs':['controlled-records.json','counterfactual-results.json','delivery/accepted.json'],'result':'Observed before/after delivery; raw138->136 preserves both branches and ranks in all14 profiles.'},
 {'case':'Runner exact delivered batch','sample_refs':['batch.json','delivery-batch/accepted.json','shortcut-results.json'],'result':'5->5. Nonpositive banks:2 No solution and1 numeric; positive-only banks:1 No solution and1 numeric. Earlier sign strategy fails on a counterexample; second-largest succeeds1/5.'},
 {'case':'Fresh requested-size batch resampling and delivery','sample_refs':['resampling-results.json','trace-104729-attempts.json','trace-20261021-attempts.json','delivery-fresh-104729/accepted.json','delivery-fresh-20261021/accepted.json'],'result':'21 and192 generated attempts respectively produce5 accepted records; each has all four sign/consistency cases after delivery. Retrying changes distribution but retains relevant cases.'}],
 'counterfactuals':[
 {'kind':'relevant','change':'q-34568 seed509: hold columns, t0/rank2/gaps[1,2,3] fixed; residual-2->0 changes d=(3,4,5)->(3,4,7).','expected':'No solution->2; prompt and final7=5->7=7 check and accepted radio choice follow.','observed':'Exact relationship holds in prompts, written checks, native grading of all five choices and actual UI questions6/7.','status':'passed','justification':'Source q-34568 checks contradiction; canonical e-4791 is a consistent c/d case. Labels are incidental.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-report.json','render-final/rendering.json','solution-math-results.json']},
 {'kind':'irrelevant','change':'q-34568 seed509->510 with explicit parameters fixed.','expected':'Choice order changes, truth2 and prompt/solution stay the same.','observed':'Preserved in text, actual UI questions7/8 and native grading.','status':'passed','justification':'Radio order does not change vector equality or coefficient sum.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-report.json','render-final/rendering.json']},
 {'kind':'relevant','change':'Retained q-105166 t-2/rank4/gaps[4,4,4], seed5888234723018271144: residual1->0.','expected':'Only final target component-29->-30 changes; identical all-negative bank must change No solution->-4.','observed':'Native grader accepts the new mathematical key in each and rejects all alternatives; actual UI questions14/15 and written checks show-30=-29 vs-30=-30.','status':'passed','justification':'This is the exact retained minimal sign-shortcut member; membership, not bank signs, decides the response.','sample_refs':['sign-counterfactual-records.json','sign-counterfactual-results.json','grader-report.json','render-final/rendering.json']},
 {'kind':'irrelevant','change':'q-105165 seed104729,t1,residual0,gaps[5,5,5]: rank1->4 changes only numeric distractors and their order/signs.','expected':'Prompt, solution and accepted sum10 stay fixed across positive-only and mixed-sign banks.','observed':'Native grader and actual UI questions16/17 preserve accepted10 and identical solution.','status':'passed','justification':'Source asks coefficient sum; irrelevant distractor signs cannot determine consistency.','sample_refs':['sign-counterfactual-records.json','sign-counterfactual-results.json','grader-report.json','render-final/rendering.json']}],
 'shortcut_probes':probes,
 'delivery':{'stages_examined':['ordinary slot validation','new batch role rejection, semantic deduplication and whole-pool retries','requested moderate difficulty','actual publisher normalization/identity validation','captured-inventory and within-batch deduplication','learner difficulty-band weighting and history exclusion','UI option reordering','native learner grading'],'sample_refs':['resampling-results.json','delivery/delivery.json','delivery/accepted.json','delivery-batch/delivery.json','delivery-batch/accepted.json','selection-results.json','grader-report.json','render-final/rendering.json'],'result':'All applicable read-only stages examined. Exact5->5, controls138->136, fresh batches5->5 each. Both sign branches survive. Publication preparation is absent; shared actual prepare_records adapter used. Learner draws are conditional on fresh moderate eligibility and supplied histories are absent.'},
 'limitations':['Captured inventory basis5400 contains only14 original source questions; no stored generated records are available to reproduce. Originals were not marked generated.','Top-level runner batch seed is unavailable; each exact saved item replays from complete generation metadata. Fresh traces exercise batch rejection directly.','Future entity IDs, learner history and configured policy weights unavailable; rules and conditional synthetic-ID selection checked, exact future sequences unknown.','Finite source coefficient profiles are conservative; no claim to every real-valued vector system or every possible shortcut. Singleton surface groups in five-item pools are not independent evidence of defects.','Canonical lacks a captured answer field; the14 exercises supply the five-choice radio contract. Numeric-only source banks are reproduced in replay; the normal sampler adds a No solution distractor to both branches.']}
save('pedagogical-variation.json',variation)
# Evidence contract uses real files; validate schema with installed validator if present.
for item in variation['coverage']+variation['counterfactuals']+variation['shortcut_probes']+[variation['delivery']]:
 for ref in item['sample_refs']:assert not pathlib.Path(ref).is_absolute() and (E/ref).is_file() and (E/ref).stat().st_size>0,ref
import subprocess
subprocess.run(['python3','-c','import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2])))',str(E/'pedagogical-variation.json'),str(REPO/'generate/pipeline/pedagogical-variation.schema.json')],check=True)
before=load(E/'package-hashes-before.json');after={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()};assert before==after
save('package-integrity.json',{'unchanged':True,'files':len(before),'method':'SHA256 every file under package_root before and after tests. Bytecode writes disabled. All authored files under evidence_root.'})
save('evidence-contract.json',{'pedagogical_schema_validated':True,'all_sample_refs_nonempty_relative':True,'native_accepted':161,'native_rejected':644,'actual_ui_cases':17})
# Bind all results and retain action commands.
save('review-binding.json',{'policy_version':2,'package_hash':'4606a2ad29de149fe347662787fb0e2b356e433ec1ba73d399c6e787ce9a63e9','batch_hash':'70305c694366f365232e3c81cbb2439209424a556c67dba5c20794ee83ef5fce','source_hash':'3cd73cb967e03612563d4e0b39954104a97675b48eaed18a095e4e8748765224','inventory_hash':'2c9a3473838ed2ff3ec306a15664c2bd2cde60d999218bf4d08e5bb6a9fca535','engine_hash':'dc1e0a8583ca33c6028bc0a641128ecc8e7896742189dd42b292170c9726bad9'})
(E/'session-state.md').write_text('Completed: source14/14 and math157 pass; displayed-solution checks147 pass; native grader161 accepted/644 rejected; actual UI17 screenshots inspected; delivery138->136 and exact5->5; fresh requested-size traces21/192 attempts retain all four sign/consistency cases after delivery. Retained original sign regression fails3/3; current/control pass. All package hashes unchanged. No demonstrated current defect; final accepted report pending serialization.\n')
print(json.dumps({'solution_checks':len(results),'probes':len(probes),'schema_valid':True,'native':[161,644],'rendered':17,'package_unchanged':True}))
