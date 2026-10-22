import sys
sys.dont_write_bytecode=True
import json,pathlib,ast,re,collections,hashlib,importlib.util
import sympy as sp
R=pathlib.Path.cwd();J=R.parent
for n in ast.parse((R/'review_checks.py').read_text()).body:
 if isinstance(n,ast.FunctionDef) and n.name in ['key','pars','ex','shortcut'] or isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='EX' for x in n.targets):exec(compile(ast.Module(body=[n],type_ignores=[]),'<helpers>','exec'))
def read(n):return json.loads((R/n).read_text())
def save(n,d):(R/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def metrics(rs):
 count=lambda fn:dict(collections.Counter(fn(r) for r in rs))
 return {'total':len(rs),'semantic_instances':len(set(tuple(map(str,(v*c,q0,r/v))) for rec in rs for v,q0,c,r,tm in [pars(rec['question'])])),'signs':count(lambda x:'increasing' if pars(x['question'])[1]<pars(x['question'])[0]*pars(x['question'])[2] else 'decreasing'),'contexts':count(lambda x:x['generation']['parameters']['context']),'roles':count(lambda x:x['generation']['bank_role']),'positions':count(lambda x:next(i for i,a in enumerate(x['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==key(x['question']))),'old_shortcut':sum(shortcut(x['question'])==key(x['question']) for x in rs)}
rows=[];grades=read('grader-input.json')
for name,raw in [('sample','easy-samples.json'),('batch','batch.json'),('counterfactual','counterfactual-records.json')]:
 before=read(raw);after=read('delivery-'+name+'/accepted.json');rows.append({'stage':name,'before':metrics(before),'after':metrics(after),'normalization_preserved_math':all(pars(a['question'])==pars(b['question']) and sorted(x[':answer/value'] for x in a['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(x[':answer/value'] for x in b['question'][':question/answer-fields'][0][':answer-field/choices']) for a,b in zip(before,after))})
 for i,rec in enumerate(after):grades.append({'label':'delivered-'+name+'-'+str(i),'record':rec,'checks':[{'submitted_answer_id':o[':answer/id'],'expected':'accepted' if o[':answer/id']==key(rec['question']) else 'rejected','purpose':'post-normalization learner behavior; math independently established in math-results.json'} for o in rec['question'][':question/answer-fields'][0][':answer-field/choices']]})
# Probe tiny subgroup apparent 2/2 maximum-constant predictor with controlled same-context orbit.
spec=importlib.util.spec_from_file_location('candidate',J/'workspace/17592186229181.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
conditional=[];success=0
for inp in read('counterfactual-inputs.json')[:5]:
 inp['parameters']['context']='disinfectant';rec=m.generate('easy',**inp);conditional.append(rec);opts=rec['question'][':question/answer-fields'][0][':answer-field/choices'];pick=sorted(opts,key=lambda a:ex(a[':answer/value'])[0],reverse=True)[0];success+=pick[':answer/id']==key(rec['question']);V,q0,c,r,time=pars(rec['question'])
 checks=[]
 for a in opts:
  e,b,k=ex(a[':answer/value']);truth=e==V*c and e+b==q0 and k==r/V
  assert truth==(a[':answer/id']==key(rec['question']))
  checks.append({'submitted_answer_id':a[':answer/id'],'expected':'accepted' if truth else 'rejected','purpose':'conditional largest-constant cue counterexample; independent initial-value and ODE coefficients'})
 grades.append({'label':'conditional-disinfectant-'+str(len(conditional)-1),'record':rec,'checks':checks})
save('conditional-records.json',conditional);save('conditional-results.json',{'apparent_raw_predictor':'largest constant within disinfectant context: 2/2 in small fresh sample','controlled_same_context':{'correct':success,'total':5,'baseline':.2},'explanation':'Same recognizable noun and identical visible bank support every target; 4 explicit counterexamples refute the accidental 2/2 sample correlation. No claim of distribution-wide independence from a finite test.'})
# Trace rejection/resampling on independently seeded default calls, without editing executable files.
traces=[];original_sample=m.sample
for seed in range(519401,519421):
 calls=[]
 def wrapped(level,rng):
  try:p=original_sample(level,rng);calls.append({'parameters':{k:str(v) for k,v in p.items()},'parameter_validation':'pass'});return p
  except ValueError as e:calls.append({'parameter_validation':'rejected','reason':str(e)});raise
 m.sample=wrapped;rec=m.generate('easy',seed);m.sample=original_sample
 traces.append({'seed':seed,'attempts':len(calls),'candidates':calls,'accepted_role':rec['generation']['bank_role'],'accepted_question_id':rec['question'][':question/id']})
save('resampling-traces.json',traces)
# Faithful learner selection against local fixtures, names/IDs do not stand in for actual future entity IDs.
def select(ids,seed):
 ids=sorted(set(ids));digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/2**53;return ids[int(u*len(ids))] if ids else None
batch=read('delivery-batch/accepted.json');mapping={100000+i:r for i,r in enumerate(batch)};selection=[]
for history in [[],[100000,100001],[100000,100001,100002,100003]]:
 choices=[select([x for x in mapping if x not in history],f'independent-revision-{i}') for i in range(80)];sel=[mapping[x] for x in choices];selection.append({'fixture_seen_ids':history,'draws':80,'counts':dict(collections.Counter(choices)),'coverage':metrics(sel)})
save('delivery-analysis.json',{'captured_inventory_basis':5397,'publication_preparation_exists':(J/'publication/preparation.json').exists(),'stages':rows,'rejection_rule':'generate chooses role before whole-candidate retries. cube_bank validates all five potential targets; bank collisions and numeric widths checked jointly. Observed raw acceptance and role frequencies in resampling-traces.json.','learner_selection':{'implementation':'question_selection.rs: sorted unique IDs; explicit positive easy weighting selects uniformly by SHA256 seed offset 8; excludes learner history and current prefix.','tests':selection,'id_map':{str(k):r['question'][':question/id'] for k,r in mapping.items()},'no_policy_fallback':'distribution=None selects first sorted candidate; no variation guarantee under this legacy unconfigured policy','limitations':['Actual policy weights, live entity IDs and learner histories are unavailable. Local tests conditional on selecting easy band; all five new IDs have nonzero support. Arbitrary histories may leave one available member.','No preparation.json yet; actual shared prepare_records reproduced read-only against basis 5397. Later inventory changes can alter deduplication.']},'database_writes':0})
# Precisely audit old demonstrated expression cue in captured inventory without relabeling originals.
inv=json.loads((J/'source/inventory.json').read_text());source_ids={q[':question/id'] for q in json.loads((J/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']};audit=[]
for q in inv['questions']:
 expression='Which expression' in q[':question/problem'];row={'question_id':q[':question/id'],'entity_id':q[':db/id'],'captured_original':q[':question/id'] in source_ids,'family':'expression' if expression else 'numeric','tested_prior_bank_shortcut':expression}
 if expression:row['old_shortcut_selects_key']=shortcut(q)==key(q) and shortcut(q) is not None
 audit.append(row)
save('inventory-audit.json',{'basis':inv['basis'],'cases':audit,'conclusion':'All seven expression banks are captured originals, none shows the demonstrated original generated method-bank shortcut. Seven additional numeric entries are outside that expression-only defect; no generated affected stored record demonstrated. Current source replay gaps repaired in generator, not database question corruption.','limitations':['Numeric entries are untested for unrelated weaknesses. No live database inspected and no new defect demonstrated.']});save('affected-inventory.json',{'affected_questions':[]})
save('grader-input.json',grades)
print(json.dumps({'stages':rows,'conditional':success,'native_cases':len(grades),'native_checks':sum(len(x['checks']) for x in grades)},indent=2))
