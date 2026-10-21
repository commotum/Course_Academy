from audit import *
import collections
inv=json.loads((E.parent/'source/inventory.json').read_text());rs=json.loads((E/'delivery/accepted.json').read_text());batch=json.loads((E/'batch-delivery/accepted.json').read_text())
# Include captured existing candidates, respecting usable-key and rating requirements.
old=[]
for q in inv['questions']:
 fs=q.get(':question/answer-fields',[]);usable=bool(fs) and all(f.get(':answer-field/correct') is not None for f in fs)
 diff=q.get(':question/difficulty');diff=diff.get(':db/ident') if isinstance(diff,dict) else diff
 old.append({'db_id':q[':db/id'],'question_id':q[':question/id'],'difficulty':diff,'has_captured_keys':usable})
selection=json.loads((E/'selection.json').read_text());selection['captured_inventory_candidates']=old;selection['combined_inventory_cases']=[]
nextid=max(q['db_id'] for q in old)+1
for label,new in [('independent',rs),('runner-batch',batch)]:
 pool=[dict(q,origin='captured') for q in old if q['has_captured_keys'] and q['difficulty']==':question.difficulty/easy']+[{'db_id':nextid+i,'question_id':r['question'][':question/id'],'difficulty':':question.difficulty/easy','origin':'generated','template':r['generation']['template'],'target':r['generation']['target']} for i,r in enumerate(new)]
 pool.sort(key=lambda q:q['db_id']);draws=[]
 for i in range(256):
  seed='combined-inventory-803c-'+str(i);d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/(1<<53);draws.append(dict(seed=seed,**pool[int(u*len(pool))]))
 selection['combined_inventory_cases'].append({'case':label,'fresh_existing_count':sum(q['origin']=='captured' for q in pool),'fresh_generated_count':len(new),'probability_per_easy_candidate':1/len(pool),'selected_origins':dict(collections.Counter(q['origin'] for q in draws)),'draws':draws})
selection['limitations']=['No learner history is captured: tested all-candidates-fresh and existing-candidates-already-seen scenarios.','Captured source q-1933 and q-47966 lack correct references and ratings, so they are not asserted to be usable eligible easy questions.','New database entity IDs are unavailable; synthetic consecutive IDs above captured IDs preserve ordering but cannot predict live sequences.','In a configured pool with positive easy weight every fresh usable easy item has equal probability; policy without a configured distribution deterministically chooses the first ID.','Later publication and learner history can remove cases. No guarantee for those unavailable states.']
save('selection.json',selection)
probes=json.loads((E/'shortcut-results.json').read_text());cp=[]
for p in probes:
 if p['stage']=='batch':continue # One item per family does not test reproducibility.
 copy=p['strategy'].startswith('copy')
 cp.append({'cue':p['strategy'],'subgroup':p['stage']+' / '+p['template'],'scope':'within_template','strategy':p['strategy'],'correct':p['correct'],'total':p['total'],'baseline':p['baseline'],'disposition':'not_predictive','conclusion':(p.get('baseline_explanation','Uniform selection among five radio choices has success probability 0.2.'))+' No reproducible perfect surface predictor in this conditional sample; limited counts do not prove absence of all cues.','sample_refs':['shortcut-results.json',p['records_file']]})
coverage=json.loads((E/'coverage.json').read_text());c=[]
for t,data in coverage['delivered'].items():c.append({'case':t,'sample_refs':['requests.json','samples.json','delivery/accepted.json','coverage.json'],'result':f"Delivered {data['count']}; targets {data['targets']}; exponent scales {data['signs']}. Both target roles survive for every blank family."})
c.append({'case':'canonical monomial ln family','sample_refs':['packaging.json','source-analysis.json'],'result':'FAIL: e-3635 x^2 ln x is excluded by h>=1 in the only polynomial-ln family. No instructional need for a nonzero additive constant.'})
cf=[]
for label,kind,change,expected,observed,justification in [
 ('target','relevant','Hold b=7 and 7^x cos(x) fixed; switch omitted left term to right term.','Answer changes from 7^x ln7 cos(x) to positive 7^x sin(x), with printed subtraction.','Prompts switch mask, solutions preserve full derivative and sign, both correct entries accepted and cross entries rejected.','q-319421/q-319425/q-311231 specify product-rule fragments; either contribution is eligible.'),
 ('sign','relevant','Hold b=5,d=7 and left target fixed; replace 5^x by 5^-x.','Answer changes sign and exponential; supplied second term changes exponential too.','Both prompts and solution reflect the sign; native own-key accepts and opposite-key rejects.','q-320816 demonstrates negative linear exponent and unequal bases.'),
 ('relevant-h','relevant','Hold n=3 and right target fixed; h=1 ->5 in (x^3+h)ln x.','Missing term changes from (x^3+1)/x to (x^3+5)/x.','Native grader accepts each own answer and rejects the other; solutions and UI follow h.','q-320824 requires retaining the undifferentiated polynomial in uv\u2032.'),
 ('irrelevant-h','irrelevant','Hold n=3 and left target fixed; h=1 ->5 in (x^3+h)ln x.','Missing term stays 3x^2 ln x while the known term changes.','Responses preserve exact equality; native cross answers accept in both directions; rendered prompts and explanations show changed h.','Derivative of constant h is zero, as the source factor-derivative stages imply.')]:
 cf.append({'kind':kind,'change':change,'expected':expected,'observed':observed,'status':'passed','justification':justification,'sample_refs':['counterfactuals.json','grader-complete-input.json','grader-complete-report.json','render-all/input.json','render-all/rendering.json','visual-inspection.json']})
ped={'learner_operation':json.loads((E/'source-analysis.json').read_text())['learner_operation'],
'fixed_features':[{'feature':'Two-factor first derivative and source-style fragment or five-choice response','justification':'Tutorial 2622 and the 17 practice questions establish u\u2032v+uv\u2032, with no point evaluation.'},{'feature':'Easy-sized atomic factors and small parameter bounds','justification':'Sources use powers, simple exponent scales, trig factors and log bases. Root-order and nonlinear nesting changes would add derivative/simplification workload.'},{'feature':'One missing product-rule term per blank','justification':'Source scaffolds supply the other contribution; full derivative is not a valid missing fragment.'}],
'answer_roles':[{'role':'Missing differentiated-factor contribution','eligible_variation':'Either left u\u2032v or right uv\u2032 at fixed factors, with printed minus for a negative second contribution.','observed':'Both targets in each blank family before and after deduplication; controlled cosine swap passes native grading and UI checks.'},{'role':'Exponential sign and relative exponential/logarithmic bases','eligible_variation':'Positive/negative simple scales and equal/unequal bases as in q-320814/815/816.','observed':'Sampling code independently draws b,d and k; both signs retained. Controlled sign change is consistent.'},{'role':'Correct radio option position and coefficients','eligible_variation':'Correct pair can change with c,n,k,b; bank directions/placement and option order may change.','observed':'Conditional position and length probes do not establish a reproducible perfect predictor; log-log scalar doubling is intended product-rule simplification, not an incidental label.'},{'role':'Natural-log polynomial factor','eligible_variation':'Allow zero additive constant to include canonical x^2 ln x; h also changes the right target without changing the left.','observed':'h=1..5 only; canonical h=0 is rejected. Relevant/irrelevant h changes within admitted range behave correctly.'}],
'coverage':c,'counterfactuals':cf,'shortcut_probes':cp,
'delivery':{'stages_examined':['explicit parameter guards and absence of rejection/resampling loop','128 fresh/boundary records -> shared normalization/validation, difficulty and captured-inventory deduplication ->112 accepted','runner batch 5 ->shared delivery ->5 accepted','configured learner-selection hash draw for fresh generated pool and combined captured usable easy pool; existing-seen scenario; legacy no-distribution branch'], 'sample_refs':['requests.json','packaging.json','delivery/delivery.json','delivery/accepted.json','batch-delivery/delivery.json','batch-delivery/accepted.json','selection.json','shortcut-results.json'],'result':'All 16 implemented identifiers and both blank targets survive captured filtering; selection within configured easy band is uniform. Source canonical family is already absent before delivery. No publication preparation file existed, so actual shared read-only preparation was used.'},
'limitations':['Finite conditional samples cannot prove absence of every shortcut.','Source replay observed banks are explicit replay only; native practice uses authored banks.','Canonical source monomial-ln product is missing; variation check cannot pass overall despite healthy tested target variation.','A valid logarithm-identity entry fails native grading; separate grading failure is retained.','Only captured basis3950 and source/selection code were available, with no live learner history, new database IDs or future inventory.','Renderer uses preview answer controls and revealed solutions; native grading is tested separately.']}
save('pedagogical-variation.json',ped)
save('visual-inspection.json',{'renderer':'actual unmodified UI via render_preview.py','passed':True,'screenshots_inspected':['render-all/question-%03d.png'%i for i in range(1,15)],'contact_sheets':['render-all/contact-batch.png','render-all/contact-pairs.png','render-all/contact-radical.png'],'observations':['Read all five runner prompts, answer controls and worked solutions. Negative powers and logarithm bases render correctly.','Cosine target pair has consistent printed subtraction and positive missing magnitude.','Positive/negative exponent pair changes factor, answer, known contribution and solution.','Both h pairs display correct known and missing contributions; same left answer and changed right answer.','Radical exponential coefficient-bank options and full solution fit the layout; no missing glyphs, clipping, broken images or MathJax errors observed.'],'automated_report':'render-all/rendering.json','limits':'Desktop 1280px viewport; no claim for every screen width or every generated instance.'})
# Structural contract check; source schema has no dependencies and jsonschema is unavailable.
schema=json.loads((ROOT/'generate/pipeline/pedagogical-variation.schema.json').read_text())
def check(v,sch,path='$'):
 if 'enum' in sch:assert v in sch['enum'],path
 typ=sch.get('type')
 if typ=='object':
  assert isinstance(v,dict),path
  assert all(k in v for k in sch.get('required',[])),path
  if sch.get('additionalProperties') is False:assert set(v)<=set(sch['properties']),path
  for k,x in v.items():
   if k in sch.get('properties',{}):check(x,sch['properties'][k],path+'.'+k)
 if typ=='array':
  assert isinstance(v,list) and len(v)>=sch.get('minItems',0),path
  for i,x in enumerate(v):check(x,sch['items'],path+f'[{i}]')
 if typ=='string':assert isinstance(v,str) and len(v)>=sch.get('minLength',0),path
 if typ=='integer':assert isinstance(v,int) and not isinstance(v,bool) and v>=sch.get('minimum',-1e99),path
 if typ=='number':assert isinstance(v,(int,float)) and sch.get('minimum',-1e99)<=v<=sch.get('maximum',1e99),path
check(ped,schema)
refs=[]
def walk(v):
 if isinstance(v,dict):
  for k,x in v.items():
   if k=='sample_refs':refs.extend(x)
   else:walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)
walk(ped)
for ref in refs:assert not Path(ref).is_absolute() and (E/ref).is_file() and (E/ref).stat().st_size>0,ref
save('evidence-contract.json',{'schema':'generate/pipeline/pedagogical-variation.schema.json','structural_validation':'passed via local recursive validator for schema-used keywords; jsonschema is not installed','sample_refs_checked':len(refs),'unique_nonempty_evidence_files':len(set(refs))})
now=hashes();before=json.loads((E/'package-before.json').read_text());save('package-integrity.json',{'unchanged':before==now,'before_count':len(before),'after_count':len(now),'changed':[p for p in set(before)|set(now) if before.get(p)!=now.get(p)],'before_manifest':'package-before.json','after':now})
(E/'session-state.md').write_text('Review complete: revise. Independent math all160 checks passed; 17 practice source banks (43 valid entries) replayed, but canonical e-3635 product excluded by h>=1. Native grader:268 accepted427 rejected, one valid-equivalent response unresolved (failure of required acceptance). Both target roles survive 128->112 filtering; runner batch5->5.14 actual UI screenshots inspected and passed. Runtime relocation/version/guard/integrity checks passed. Pedagogical variation report and evidence contract saved. No package, database or published assets modified.\n')
print('pedagogical schema and refs passed; package unchanged',before==now,'combined candidates',[(v['case'],v['fresh_existing_count'],v['fresh_generated_count']) for v in selection['combined_inventory_cases']])
