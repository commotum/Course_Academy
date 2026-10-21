"""Read-only current delivery, selection and relocation audit; run after revision_audit.py and shared delivery."""
import sys
sys.dont_write_bytecode=True
import collections,copy,hashlib,json,pathlib,shutil,subprocess
import revision_audit as R
A=R.A;HERE=R.HERE
# Retained independent selection reproduction, checked against current supplied Rust.
from selection_helper import choose

def outcomes(rs):
 return {'count':len(rs),'templates':dict(collections.Counter(r['generation']['template'] for r in rs)),'signs':dict(collections.Counter('negative' if R.S.Rational(r['generation']['parameters']['a'])<0 else 'positive' for r in rs)),'double_exponent_correct':sum(A.shortcut(r)==A.key(r) for r in rs)}
def run():
 stages={};probes=[];delivered=[];delivery_math=[]
 for name,path in [('samples','easy-samples.json'),('batch','runner-batch.json'),('counterfactuals','counterfactual-records.json')]:
  before=R.load(HERE/path);after=R.load(HERE/f'delivery-{name}/accepted.json');delivered+=after
  stages[name]={'before':outcomes(before),'after':outcomes(after),'delivery_report':f'delivery-{name}/delivery.json'}
  probes+=R.probes(after,'delivered '+name)
  for r in after:delivery_math.append(A.math_check(r))
 R.save('delivery-math-results.json',delivery_math)
 R.save('delivery-shortcut-results.json',probes)
 cases=[{'label':r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==A.key(r) else 'rejected','purpose':'Delivered normalized equation independently verified; real learner UUID selection'} for a in A.field(r)[':answer-field/choices']]} for r in delivered]
 R.save('delivered-grader-input.json',cases)
 inv=R.load(R.JOB/'source/inventory.json');usable=[q for q in inv['questions'] if ':answer-field/correct' in q[':question/answer-fields'][0]];affected={q['entity_id'] for q in R.load(HERE/'affected-inventory.json')['affected_questions']};source_ids={q[':db/id'] for q in usable if ':question/math-academy-id' in q}
 scenarios=[]
 # Source/inventory selection uses real captured IDs. Prospective survivors use
 # explicit surrogate IDs because no publication or database allocation is allowed.
 prospective=[];top=max(q[':db/id'] for q in inv['questions'])+1000
 for i,r in enumerate(R.load(HERE/'delivery-samples/accepted.json')+R.load(HERE/'delivery-batch/accepted.json')):
  q=copy.deepcopy(r['question']);q[':db/id']=top+i;prospective.append(q)
 mapped={q[':db/id']:r for q,r in zip(prospective,R.load(HERE/'delivery-samples/accepted.json')+R.load(HERE/'delivery-batch/accepted.json'))}
 for label,candidates,weights,seen in [('captured easy, no history',usable,(1,0,0),set()),('captured easy, sources seen',usable,(1,0,0),source_ids),('captured illustrative 6:3:1',usable,(6,3,1),set()),('captured unconfigured policy',usable,None,set()),('prospective easy survivors, captured questions seen',usable+prospective,(1,0,0),{q[':db/id'] for q in usable})]:
  draws=[]
  for i in range(120):
   seed=f'independent-revision-741/{i}';q=choose(candidates,weights,seed,seen)
   draws.append({'seed':seed,'entity_id':q[':db/id'] if q else None,'historical_affected':q is not None and q[':db/id'] in affected,'prospective_template':mapped[q[':db/id']]['generation']['template'] if q and q[':db/id'] in mapped else None})
  scenarios.append({'scenario':label,'weights':weights,'seen':sorted(seen),'draws':draws,'historical_affected_draws':sum(x['historical_affected'] for x in draws),'prospective_templates':dict(collections.Counter(x['prospective_template'] for x in draws if x['prospective_template']))})
 R.save('delivery-selection-results.json',{'command':f'{sys.executable} pipeline_revision.py','stages':stages,'generator_rejection_trace':'generator-rejection-trace.json','captured_inventory_basis':inv['basis'],'usable_inventory_count':len(usable),'selection_reference':'engine/rust/question_selection.rs::select; seen_before_task','selection_reference_sha256':hashlib.sha256((R.REPO/'engine/rust/question_selection.rs').read_bytes()).hexdigest(),'scenarios':scenarios,'publication_preparation_present':(R.JOB/'publication/preparation.json').exists(),'limits':['No learner history or actual configured policy supplied: weights/history are explicitly conditioned scenarios.','Prospective items have surrogate IDs, not allocated database IDs; selection inspects only ID, rating and freshness, never mathematical content or correct bank position. Exact next item depends on future IDs and learner state.','Current captured inventory retains three old easy shortcut instances; these are listed in affected-inventory.json, using old generation metadata. Current construction fixes them for new instances.','No claim about future changing inventory or exhaustive absence of cues.']})
 # Relocate just the declared runtime, never the entire package evidence tree.
 mirror=HERE/'relocated-runtime';mirror.mkdir(exist_ok=True)
 manifest=R.load(R.PKG/'package.json')
 for fn in manifest['files']:
  target=mirror/fn;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R.PKG/fn,target)
 outs=[];cmds=[]
 for label,root in [('original',R.PKG),('relocated',mirror)]:
  cmd=[sys.executable,str(root/manifest['entrypoint']),'--difficulty','easy','--seed','872053','--count','5','--format','json']
  cp=subprocess.run(cmd,cwd=HERE,capture_output=True,text=True);assert cp.returncode==0,cp.stderr
  (HERE/f'{label}-cli.json').write_text(cp.stdout);(HERE/f'{label}-cli.stderr').write_text(cp.stderr);outs.append(json.loads(cp.stdout));cmds.append(cmd)
 assert outs[0]==outs[1]
 p=R.load(HERE/'packaging-results.json');p.update({'relocation_commands':cmds,'relocated_declared_files_only':True,'relocation_equal':True,'original_package_unchanged':A.snapshot()==R.load(HERE/'package-before.json')});assert p['original_package_unchanged'];R.save('packaging-results.json',p)
 print(json.dumps({'delivery_stage_counts':{k:[x['before']['count'],x['after']['count']] for k,x in stages.items()},'selection':[{'scenario':s['scenario'],'historical_affected_draws':s['historical_affected_draws'],'prospective_templates':s['prospective_templates']} for s in scenarios],'relocation_equal':True,'native_delivered_cases':len(cases)*5}))
if __name__=='__main__':run()
