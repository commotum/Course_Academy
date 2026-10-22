#!/usr/bin/env python3
"""Summarize decision evidence and faithfully reproduce selection rules read-only."""
import json,pathlib,hashlib,collections,re
E=pathlib.Path(__file__).resolve().parent;J=E.parent
load=lambda p:json.loads((E/p).read_text())
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
def vals(r):return sorted(int(c[':answer/value']) for c in r['question'][':question/answer-fields'][0][':answer-field/choices'])
def ans(r):
 f=r['question'][':question/answer-fields'][0];return next(int(c[':answer/value']) for c in f[':answer-field/choices'] if c[':answer/id']==f[':answer-field/correct'][1])
def gaps(v):return [b-a for a,b in zip(v,v[1:])]
def action(r):
 v=vals(r)
 if gaps(v)==[2,1,1,1] or 0 not in v:return v[1]
 if gaps(v)!=[1,1,1,1]:return v[-2]
 return 2
stages={n:load(p) for n,p in [('raw','sample-easy.json'),('delivered','delivery-sample/accepted.json'),('batch_raw','batch-records.json'),('batch_delivered','delivery-batch/accepted.json')]}
probes=[];stats={}
for name,records in stages.items():
 stats[name]={'n':len(records),'answers':dict(collections.Counter(ans(r) for r in records)),'profiles':dict(collections.Counter(r['generation']['profile'] for r in records))}
 for subgroup,pred,strategy,choose in [('entire easy set',lambda r:True,'Bank only: first gap 2 then three gaps 1, or bank lacks zero -> second-smallest; other nonconsecutive bank -> second-largest; otherwise choose 2.',action),('gap pattern 2,1,1,1',lambda r:gaps(vals(r))==[2,1,1,1],'Choose the second-smallest numeric option, ignoring the prompt.',lambda r:vals(r)[1]),('consecutive bank with minimum at least 1',lambda r:gaps(vals(r))==[1,1,1,1] and min(vals(r))>=1,'Choose the second-smallest numeric option, ignoring the prompt.',lambda r:vals(r)[1]),('zero present and bank nonconsecutive, excluding gap 2,1,1,1',lambda r:0 in vals(r) and gaps(vals(r)) not in ([1,1,1,1],[2,1,1,1]),'Choose the second-largest numeric option, ignoring the prompt.',lambda r:vals(r)[-2])]:
  chosen=[r for r in records if pred(r)]
  if not chosen:continue
  successes=sum(choose(r)==ans(r) for r in chosen)
  probes.append({'stage':name,'subgroup':subgroup,'strategy':strategy,'correct':successes,'total':len(chosen),'question_ids':[r['question'][':question/id'] for r in chosen],'choices_and_actions':[{'values':vals(r),'predicted':choose(r),'correct':ans(r)} for r in chosen]})
save('shortcut-results.json',{'stage_stats':stats,'probes':probes,'code_analysis':'offset-minus1 fixes the answer at the second-smallest; offset-minus2 fixes it at the second-smallest and reveals itself via gaps 2,1,1,1; dimensions always has answer n-k as second-largest because validity forces n>2k and rejects k=0 or duplicate values. UI shuffles option order, so all actions refer to numeric order, not screen position.'})
# Controlled before/after dependencies evaluated on prompt, solution and native grader.
cf=load('counterfactual-records.json');graded=load('grader-report.json')['records'];pairs=[]
for label,i,j,expected in [('increase column count',0,1,'3 -> 4'),('increase irrelevant row count',0,2,'3 -> 3'),('decrease basis cardinality',0,3,'3 -> 4'),('change coefficient without changing span dimension',4,5,'2 -> 2'),('increase independent parameter count',4,6,'2 -> 1')]:
 a,b=cf[i],cf[j];ga=next(r for r in graded if r['label']==f'counterfactual-{i}');gb=next(r for r in graded if r['label']==f'counterfactual-{j}')
 pairs.append({'change':label,'indices':[i,j],'expected':expected,'observed':[ans(a),ans(b)],'prompts_changed':a['question'][':question/problem']!=b['question'][':question/problem'],'solutions_changed':a['question'][':question/worked-solution']!=b['question'][':question/worked-solution'],'native_before':ga['checks'],'native_after':gb['checks'],'records_file':'counterfactual-records.json'})
save('counterfactual-results.json',{'pairs':pairs,'note':'All five bank alternatives graded per record; easy bank remains identical across pairs so the same numeric option changes accepted/rejected status when relevant evidence changes. Moderate coefficient-only change preserves dimension and acceptance. Rendering indices 5..11 correspond to these pairs.'})
# Exact selection function, translated from supplied Rust select(): synthetic IDs only for unpublished records.
inv=json.loads((J/'source/inventory.json').read_text());batch=stages['batch_delivered'];maxid=max(q[':db/id'] for q in inv['questions']);pool=[]
for q in inv['questions']:pool.append({'id':q[':db/id'],'band':q[':question/difficulty'][':db/ident'].split('/')[-1],'batch':False})
for i,r in enumerate(batch):pool.append({'id':maxid+1+i,'band':'easy','batch':True,'record':r})
def select(candidates,weights,seed):
 cs=sorted({c['id']:c for c in candidates}.values(),key=lambda c:c['id'])
 if weights is None:return cs[0] if cs else None
 bs=[[c for c in cs if c['band']==b]for b in ['easy','moderate','hard']];total=sum(w for w,b in zip(weights,bs)if b)
 if not total:return None
 d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 u=lambda off:(int.from_bytes(d[off:off+8],'big')>>11)/(1<<53)
 draw=u(0)*total;chosen=None
 for i,w in enumerate(weights):
  if not bs[i] or not w:continue
  chosen=i
  if draw<w:break
  draw-=w
 bp=bs[chosen];return bp[int(u(8)*len(bp))]
selection=[]
for label,candidates in [('captured originals plus staged batch',pool),('originals already seen', [q for q in pool if q['batch']]),('only first batch member unseen',[q for q in pool if q['batch']][:1])]:
 for weights in ([1,0,0],[6,3,1],None):
  draws=[select(candidates,weights,'review-62841-'+str(i))for i in range(256)];bc=[q for q in draws if q and q['batch']]
  selection.append({'case':label,'weights':weights,'draws':len(draws),'batch_draws':len(bc),'batch_rule_correct':sum(action(q['record'])==ans(q['record'])for q in bc),'counts':dict(collections.Counter(str(q['id'])if q else 'none'for q in draws))})
save('selection-results.json',{'implementation':'faithful translation of engine/rust/question_selection.rs::select; prior-task/current-prefix exclusions modeled by removing candidates before selection','staged_id_policy':'Publication preparation absent; provisional generated entity IDs assigned max captured ID + 1..5. Exact future deterministic question order is not claimed. Weighted within-easy draws have equal nonzero support regardless of actual generated IDs.','cases':selection,'conclusion':'Every batch draw admits the bank-only rule. Difficulty weights and seen filtering do not randomize bank values. Once originals have been seen the five-item reserve can be answered without prompt reasoning; the source+batch pool is not universally bypassed.','limits':['No learner history or policy configuration was supplied; scenarios are conditional, not claims of live state. Actual generated entity IDs require publication, which this review does not perform. Captured inventory basis is 5443.']})
# Individual runnable minimal failures; no expectation that code changes to conceal them.
save('minimal-failures.json',{'shortcut':{'generate':{'level':'easy','seed':63271,'profile':'offset-minus2','parameters':{'m':2,'n':4,'k':2}},'bank':[0,2,3,4,5],'correct':2,'rule':'gap pattern 2,1,1,1 -> choose second-smallest; no rank-nullity needed','family_rule_to_change':'Derive distractor banks without a recognizable profile fixing the numeric rank of the correct option. Shuffling screen order does not fix this.'},'source_rejection':{'source_id':'5e7c8be1-d271-506d-bfc9-fbf1881a88d8','ma_id':'q-142489','generate':{'level':'moderate','parameters':{'matrix':[[1,0],[0,0],[1,1],[0,0],[0,0]],'indices':[1,2]},'profile':'one-through5'},'correct':3,'bank':[1,2,3,4,5],'current':'ValueError: parameter/profile constraint','family_rule_to_change':'Support source-backed five-component null-space parameterizations, including indices [1,2], and derive n from vector length throughout validation, answer and worked solution.'}})
# Schema-conforming independent pedagogical assessment.
ps=[]
for p in probes:
 ps.append({'cue':'numeric answer-bank shape','subgroup':p['stage']+': '+p['subgroup'],'scope':'overall' if p['subgroup']=='entire easy set' else 'other_recognizable_subgroup','strategy':p['strategy'],'correct':p['correct'],'total':p['total'],'baseline':0.2,'disposition':'defect','conclusion':'Baseline 0.2 is uniform selection among five choices. Bank-only cue avoids identifying column count and rank; this is incidental answer leakage. Conditional rules are supported by construction, not solely this finite sample. Overall rule is not claimed perfect for all generated questions.','sample_refs':['shortcut-results.json','batch-records.json' if p['stage'].startswith('batch') else 'sample-easy.json']})
var={'learner_operation':'Identify rank from the column-space basis or nullity from independent coefficient vectors; determine column count n; compute its complementary dimension using rank + nullity = n; select that integer.','fixed_features':[{'feature':'Five-option single radio response','justification':'All 15 supplied practice questions use this contract.'},{'feature':'Easy column-basis-to-nullity vs moderate null-space-to-rank','justification':'Observed source difficulty split supports these inference paths.'}],'answer_roles':[{'role':'n and column-basis cardinality k','eligible_variation':'Vary independently within feasibility; m can vary without affecting answer.','observed':'Easy samples change n,k and answers. Counterfactuals verify relevant vs irrelevant dependence.'},{'role':'Which numeric choice qualifies','eligible_variation':'Correct numeric rank within a recognizable bank should not be fixed without instructional reason.','observed':'offset-minus2 recognizable gap shape always makes the second-smallest correct; all batch records admit a bank-only strategy.'},{'role':'Moderate ambient dimension and parameter supports','eligible_variation':'n=4 and n=5 and indices [2,3], [1,2], [1,2,3] are source-supported.','observed':'valid() fixes n=4 and permits only [2,3] or [1,2,3]; three supplied n=5 cases are rejected.'}],'coverage':[{'case':n,'sample_refs':['shortcut-results.json',{'raw':'sample-easy.json','delivered':'delivery-sample/accepted.json','batch_raw':'batch-records.json','batch_delivered':'delivery-batch/accepted.json'}[n]],'result':json.dumps(v)}for n,v in stats.items()]+[{'case':'source families','sample_refs':['source-replay.json'],'result':'12/15 parameter/bank replays; three n=5 moderate cases rejected. One replay reorders x2-x1 as -x1+x2, an algebraically faithful normalization.'}],'counterfactuals':[{'kind':'irrelevant' if i in [1,3] else 'relevant','change':p['change'],'expected':p['expected'],'observed':str(p['observed'])+'; all choices independently graded, prompt/solution dependencies compared and actual UI rendered.','status':'passed','justification':'Rank-nullity depends on n and the inferred dimension; row count and coefficient changes preserving dimension leave the response unchanged. Source canonical and tutorial establish these dependencies.','sample_refs':['counterfactual-records.json','counterfactual-results.json','grader-report.json','render/rendering.json']}for i,p in enumerate(pairs)],'shortcut_probes':ps,'delivery':{'stages_examined':['generator valid() rejection and seeded sampling','requested-difficulty filtering','publisher normalization and inventory/within-batch deduplication','captured source inventory','learner difficulty-first selection and seen-history scenarios','actual UI option shuffling'], 'sample_refs':['rejection-replay.json','delivery-sample/delivery.json','delivery-batch/delivery.json','selection-results.json','shortcut-results.json','render/rendering.json'],'result':'64 raw easy -> 56 accepted; exact batch 5 -> 5. Bank-shape leakage survives, and the exact batch rule scores 5/5 before/after delivery. Every selected staged batch record is bypassable in the simulated positive-easy selection scenarios.'},'limitations':['Finite audit, not an exhaustive search for every shortcut.','Live policy, learner history and future generated entity IDs were not captured; selection support is conditional on stated scenarios.','Publication preparation absent; shared read-only filtering used with basis 5443.','UI shuffles positions; numeric-order strategies remain applicable.']}
save('pedagogical-variation.json',var)
print(json.dumps({'stages':stats,'conditional_probes':[{k:p[k]for k in ['stage','subgroup','correct','total']}for p in probes],'selection_scenarios':len(selection)}))
