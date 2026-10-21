import sys;sys.dont_write_bytecode=True
import json,pathlib,collections
R=pathlib.Path(__file__).resolve().parent
load=lambda n:json.loads((R/n).read_text())
def save(n,v):(R/n).write_text(json.dumps(v,indent=2)+'\n')
accepted=load('delivery/accepted.json');inventory=load('../source/inventory.json');base=max(q[':db/id'] for q in inventory['questions'])+100
pool={base+j:r for j,r in enumerate(accepted)};trialmap={o['qid']:o for o in load('shortcut-trials.json')['delivered']};selections=load('selection-results.json');out=[];refs=[]
for scenario in selections['scenarios']:
 selected=[pool[id] for id in scenario['draws'] if id in pool];obs=[trialmap[r['question'][':question/id']] for r in selected if r['question'][':question/id'] in trialmap]
 out.append({'scenario':scenario['scenario'],'generated_selected':len(selected),'radios':len(obs),'singleton_elimination_survives':sum(o['true_row_survives'] for o in obs),'seeded_strategy_correct':sum(o['success'] for o in obs),'baseline':0.2,'exact_conditional_chance':0.25 if obs else None,'profiles':dict(collections.Counter(r['generation']['template'] for r in selected))})
 if scenario['scenario']=='positive_moderate':refs=selected
save('selected-records.json',refs);save('delivery-selection-summary.json',{'selection':out,'captured_basis':inventory['basis'],'limits':selections['limits'],'rules':'question_selection.rs: candidate dedup/sort, difficulty weights, SHA256 within-band choice; synthetic new numeric IDs, captured usable bank and explicit histories/policies. Does not certify live learner state.','filtering':{stage:load(stage+'/delivery.json') for stage in ['delivery','batch-delivery','control-delivery']},'generator_rejection':'generate() has no rejection/resampling loop; prefilters zero resulting coefficients and chooses only valid factor/offset domains; 360 requested ->360 emitted. Omitted row 0 is excluded before sampling in both radio families.'})
# Deliver native tests against normalized records, not only raw generator output.
sys.path.insert(0,str(R));from audit_math import field,answer,tex,extract,verify,S
cases=load('grader-input.json')+load('additional-grader-input.json');normalized=load('batch-delivery/accepted.json')+load('control-delivery/accepted.json')+[accepted[j] for j in [0,30,120,200,328]]
checks=[]
for j,r in enumerate(normalized):
 checks.append(verify(r));f=field(r)
 if f[':answer-field/type'].endswith('/blank'):
  v=tex(answer(r)[':answer/value']);inputs=[{'submitted':str(S.factor(v)).replace('**','^'),'expected':'accepted','purpose':'normalized delivered equivalent expression'},{'submitted':str(v+1).replace('**','^'),'expected':'rejected','purpose':'normalized delivered wrong additive constant in externally completed blank'}]
 else:inputs=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==answer(r)[':answer/id'] else 'rejected','purpose':'normalized delivered independently differentiated choice'} for a in f[':answer-field/choices']]
 cases.append({'label':'normalized delivered '+str(j),'record':r,'checks':inputs})
save('delivered-math-results.json',checks);save('grader-input-complete.json',cases)
print(json.dumps(out))
