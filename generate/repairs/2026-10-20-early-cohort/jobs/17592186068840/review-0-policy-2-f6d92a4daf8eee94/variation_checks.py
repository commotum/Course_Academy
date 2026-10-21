import json,sys,importlib.util,re,collections,hashlib
from pathlib import Path
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent;B=E.parent;W=B/'workspace'
spec=importlib.util.spec_from_file_location('g',W/'17592186068840.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(n,v):(E/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def bank(r):return r['question'][':question/answer-fields'][0]
def correct(r):
 f=bank(r);return next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])[':answer/value']
# Shape-only strategy: select C plus a visibly squared x-expression inside the outer inverse/cube.
# It does not inspect the differential equation, coefficient, or translation value.
def cue(v):
 if not ('^{2}' in v and 'C +' in v):return False
 if v.startswith(r'y=\sqrt[3]{C +'):return True
 if v.startswith(r'y=\ln{\left(C +'):return True
 if v.startswith(r'y=\left(C +') and v.endswith('^{3}'):return True
 return False
def probe(rows):
 out=[]
 for i,r in enumerate(rows):
  name=r['generation']['template']
  if name not in ['reciprocal_cube','negative_exp','cube_power']:continue
  selected=[a for a in bank(r)[':answer-field/choices'] if cue(a[':answer/value'])]
  out.append({'index':i,'id':r['question'][':question/id'],'template':name,'parameters':r['generation']['parameters'],'selected_values':[a[':answer/value'] for a in selected],'correct':len(selected)==1 and selected[0][':answer/id']==bank(r)[':answer-field/correct'][1]})
 return {'successes':sum(o['correct'] for o in out),'attempts':len(out),'by_template':{t:{'correct':sum(o['correct'] for o in out if o['template']==t),'total':sum(o['template']==t for o in out)} for t in sorted(set(o['template'] for o in out))},'cases':out}
raw=json.load(open(E/'independent-easy.json'));batch=json.load(open(E/'batch-records.json'));accepted=json.load(open(E/'delivery-independent/accepted.json'));baccept=json.load(open(E/'delivery-batch/accepted.json'))
# Probe callable selector canonicalizes wrapper shape already retained by delivery helper
summary={'strategy':'Ignore ODE; choose unique candidate that nests C + [a square in x] inside cube root, logarithm, or cube. Only plus sign and exponent/layout inspected.','baseline':0.2,'raw':probe(raw),'delivered':probe(accepted),'batch':probe(batch),'batch_delivered':probe(baccept)}
save('shortcut-results.json',summary)
# Native engine validates that the shortcut succeeds as an actual response.
cases=[]
for r in baccept:
 selected=next(a for a in bank(r)[':answer-field/choices'] if cue(a[':answer/value']))
 cases.append({'label':'batch shape-only shortcut '+r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':selected[':answer/id'],'expected':'accepted','purpose':'shape-only strategy without reading differential equation'}]})
save('shortcut-grader-input.json',cases)
# Existing inventory: use captured reproduction recipes; independently replay current package.
old=json.load(open(W/'17592186068840/reference/replenishment/basis-2667/generated.json'))
inv=json.load(open(B/'source/inventory.json'));invby={q[':question/id']:q for q in inv['questions']};reproduced=[];affected=[];tested=[]
for oldr in old:
 meta=oldr['generation'];r=g.generate(oldr['question'][':question/difficulty'].split('/')[-1],meta['seed'],meta['template'],parameters=meta['parameters'],profile=meta['bank_profile'])
 qid=r['question'][':question/id'];stored=invby.get(qid);same=stored is not None and stored[':question/problem']==r['question'][':question/problem'] and stored[':question/worked-solution']==r['question'][':question/worked-solution'] and sorted(a[':answer/value'] for a in stored[':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/value'] for a in bank(r)[':answer-field/choices'])
 tested.append({'question_id':qid,'matched_complete_content':same,'metadata_matches_captured_recipe':r['generation']==meta,'template':meta['template']})
 if same:reproduced.append(r)
 if same and meta['template']=='reciprocal_cube' and probe([r])['successes']==1:
  affected.append({'question_id':qid,'entity_id':stored[':db/id'],'finding':'Fixed positive squared primitive makes the unique cube-root(C + square) choice predict the answer without inspecting the ODE; same family-wide restriction as reviewed easy batch.','reproduction':'Run .venv/bin/python -B variation_checks.py; recipe '+json.dumps(meta,sort_keys=True),'evidence_path':'generated-records.json'})
save('generated-records.json',reproduced);save('affected-inventory.json',{'affected_questions':affected})
save('inventory-audit.json',{'basis':inv['basis'],'lineage':inv['lineage'],'question_count':len(inv['questions']),'original_source_ids_excluded': [q[':question/id'] for q in inv['questions'] if ':question/math-academy-id' in q],'generated_recipes_tested':tested,'affected_count':len(affected),'limits':'All six captured generated recipes reproduced; requested easy shortcut tested only for the one stored easy generated reciprocal_cube. Other five generated hard entries are not certified shortcut-free. Original source questions are never classified as generated.'})
# Faithful selection logic for easy-only captured batch; with any positive easy weight, native select is uniform by stable question entity ids.
# Prospective entities do not exist: use synthetic monotonic IDs solely to inspect reachability and unconditional cue preservation.
ids=list(range(1,len(baccept)+1));draws=[]
for k in range(30):
 seed='independent-review-'+str(k);d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/(1<<53);idx=int(u*len(ids));draws.append({'seed':seed,'synthetic_entity':ids[idx],'question_id':baccept[idx]['question'][':question/id'],'template':baccept[idx]['generation']['template'],'shortcut_correct':probe([baccept[idx]])['successes']==1})
save('selection-analysis.json',{'source_file':'engine/rust/question_selection.rs','source_sha256':hashlib.sha256(Path('/home/jake/Developer/Course_Academy/engine/rust/question_selection.rs').read_bytes()).hexdigest(),'rules':'Caller removes prior seen and current-prefix questions; weights choose among nonempty positive bands; within-band SHA256 uniform selection. No template or answer-shape balancing. Without policy takes first candidate. Unknown-rating fallback only if no positively weighted rated bands.','capture_basis':inv['basis'],'batch_stages':{'raw':len(batch),'post_delivery':len(baccept),'difficulty':'easy','source_families':dict(collections.Counter(r['generation']['template'] for r in baccept))},'draws':draws,'reachable_ids':sorted(set(d['synthetic_entity'] for d in draws)),'all_draws_shortcut':all(d['shortcut_correct'] for d in draws),'history_effect':'Any nonempty subset of these five retains the shortcut, so removing seen items cannot cure it. A zero easy weight means these records are not delivered, not that they acquire variation.','limitations':['No publication/preparation.json exists. Only read-only delivery filter was executed.','Live learner history, policy weights, actual future entity IDs, and later inventory are not captured. Synthetic IDs demonstrate selector mechanics, not predictions for a real learner.','Changing inventory may affect deduplication and availability; supported claims are bounded to captured basis 5366.']})
# Controlled dependencies verified from prompt, solution and actual grader case files.
pairs=json.load(open(E/'counterfactual-records.json'))
checks=[]
for kind,ia,ib,relationship in [('relevant',0,1,'changed shift changes displayed ODE, complete correct family and solution'),('relevant',3,4,'a=1 ->2 changes ODE, primitive and tan argument'),('irrelevant',0,2,'seed/order changes preserve prompt, solution, correct value and mathematical identity'),('irrelevant',5,6,'ambient 25->35 changes ODE and offset but preserves requested exponential factor')]:
 a,b=pairs[ia],pairs[ib];same=correct(a)==correct(b); passed=(not same if kind=='relevant' else same)
 if kind=='irrelevant' and ia==0:passed=passed and a['question'][':question/problem']==b['question'][':question/problem'] and a['question'][':question/worked-solution']==b['question'][':question/worked-solution']
 checks.append({'kind':kind,'indices':[ia,ib],'expected':relationship,'before':correct(a),'after':correct(b),'passed':passed,'prompts_changed':a['question'][':question/problem']!=b['question'][':question/problem'],'solutions_changed':a['question'][':question/worked-solution']!=b['question'][':question/worked-solution'],'grader_evidence':'grader-supported-results.json','render_evidence':'render-pairs/rendering.json'})
save('counterfactual-results.json',checks)
print('shortcuts', {k:(summary[k]['successes'],summary[k]['attempts']) for k in ['raw','delivered','batch','batch_delivered']},'inventory affected',len(affected))
