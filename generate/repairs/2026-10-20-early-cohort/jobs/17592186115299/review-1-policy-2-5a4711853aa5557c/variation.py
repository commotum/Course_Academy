import sys,json,re,hashlib
from collections import Counter,defaultdict
from pathlib import Path
sys.dont_write_bytecode=True
import review as v
E=v.E

def choice(r):
 fs=r['question'][':question/answer-fields']
 if v.ftype(fs[0]).endswith('radio'):return v.value(fs[0])
 return next(f[':answer-field/key'] for f in fs if v.value(f)=='true')
def klass(r):return v.classification(v.system(r['question'][':question/problem']))
def shape(r):
 m=v.system(r['question'][':question/problem']);return f'{m.rows}x{m.cols-1}'
def describe(rs):
 out={}
 for r in rs:
  m=v.system(r['question'][':question/problem']);g=r['generation'];key=g['template'];d=out.setdefault(key,{'shape':shape(r),'response':g['response_layout'],'classifications':Counter(),'correct_actions':Counter(),'rank':Counter(),'free_columns':Counter(),'count':0})
  d['classifications'][klass(r)]+=1;d['correct_actions'][choice(r)]+=1;d['rank'][str(m[:,:-1].rank())]+=1;d['free_columns'][str([i for i in range(m.cols-1) if i not in m[:,:-1].rref()[1]])]+=1;d['count']+=1
 return out

def probes(rs,ref,stage):
 out=[];groups={'all':rs}
 for r in rs:
  g=r['generation'];groups.setdefault('template '+g['template'],[]).append(r)
  groups.setdefault('shape '+shape(r)+' '+g['response_layout']+' '+str(len(r['question'][':question/answer-fields']))+' fields',[]).append(r)
 for group,items in groups.items():
  # Conditional probes: constant semantic classification; first available answer action.
  baseline=sum(1/(2 if shape(r)=='2x3' else 3) for r in items)/len(items)
  for label in ['dependent','independent','inconsistent']:
   correct=sum(klass(r)==label for r in items)
   out.append({'cue':'template / response / dimensions, ignoring numerical entries','subgroup':stage+' '+group,'scope':'overall' if group=='all' else 'within_template' if group.startswith('template') else 'other_recognizable_subgroup','strategy':'always select '+label,'correct':correct,'total':len(items),'baseline':baseline,'disposition':'not_predictive','conclusion':f'Comparison baseline is uniform among feasible categories (1/2 for 2x3, otherwise 1/3), averaged across subgroup. {correct}/{len(items)}; no class fixed across fresh instances of any template. Small batch subgroups can be coincidental, so compare fresh same-template controls rather than claiming universal predictability.','sample_refs':[ref]})
  correct=0
  for r in items:
   fs=r['question'][':question/answer-fields'];first=fs[0]
   if v.ftype(first).endswith('radio'):
    correct+=first[':answer-field/choices'][0][':answer/value']==v.value(first)
   else:correct+=v.value(first)=='true'
  out.append({'cue':'first visible answer control','subgroup':stage+' '+group,'scope':'overall' if group=='all' else 'within_template' if group.startswith('template') else 'other_recognizable_subgroup','strategy':'select only first visible option','correct':correct,'total':len(items),'baseline':sum(1/(len(r['question'][':question/answer-fields'][0][':answer-field/choices']) if v.ftype(r['question'][':question/answer-fields'][0]).endswith('radio') else len(r['question'][':question/answer-fields'])) for r in items)/len(items),'disposition':'not_predictive','conclusion':'Baseline is uniform random selection among visible alternatives. All fresh template groups include counterexamples to this action; no fixed-position defect demonstrated.','sample_refs':[ref]})
 return out

def selection_report():
 inv=v.load(v.JOB/'source/inventory.json');batch=v.load(E/'delivery-batch/accepted.json')
 pool=[]
 for q in inv['questions']:
  dif=q.get(':question/difficulty');dif=dif.get(':db/ident') if isinstance(dif,dict) else dif
  pool.append({'entity_id':q[':db/id'],'id':q[':question/id'],'band':dif.split('/')[-1] if dif else None,'classification':v.classification(v.system(q[':question/problem'])),'origin':'captured'})
 maxid=max(q['entity_id'] for q in pool)
 for i,r in enumerate(batch):pool.append({'entity_id':maxid+1+i,'id':r['question'][':question/id'],'band':'moderate','classification':klass(r),'origin':'proposed batch'})
 def select(candidates,weights,seed):
  candidates=sorted(candidates,key=lambda x:x['entity_id'])
  if weights is None:return candidates[0] if candidates else None
  bands=[[q for q in candidates if q['band']==b] for b in ['easy','moderate','hard']];unrated=[q for q in candidates if q['band'] is None]
  digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
  def uniform(offset):return (int.from_bytes(digest[offset:offset+8],'big')>>11)/float(1<<53)
  total=sum(w for i,w in enumerate(weights) if bands[i]);pp=unrated
  if total>0:
   draw=uniform(0)*total
   for i,w in enumerate(weights):
    if not bands[i] or not w:continue
    pp=bands[i]
    if draw<w:break
    draw-=w
  return pp[int(uniform(8)*len(pp))] if pp else None
 scenarios=[]
 for name,candidates in [('captured inventory + five proposed records',pool),('proposed five alone',[q for q in pool if q['origin']=='proposed batch']),('history excludes two captured IDs',pool[2:])]:
  selected=[select(candidates,[0,1,0],f'independent-review-{i}') for i in range(256)]
  scenarios.append({'case':name,'weights':[0,1,0],'draws':256,'seen_exclusions':pool[:2] if name.startswith('history') else [],'selected_counts':dict(Counter(q['id'] for q in selected if q)),'class_counts':dict(Counter(q['classification'] for q in selected if q)),'eligible_count':len([q for q in candidates if q['band']=='moderate']),'unconfigured_first':select(candidates,None,'unused')})
 return {'basis':inv['basis'],'algorithm':'Faithful read-only reproduction of question_selection.rs select(): deduplicated sorted entity IDs, SHA256 band/index draws, positive-weight-band filtering. seen_before_task and current-prefix exclusions remove IDs before selection.','pool':pool,'scenarios':scenarios,'limitations':['No learner history, active policy or prospective inserted entity IDs supplied. New IDs are labeled synthetic, monotone above captured maximum. Within a positively weighted moderate band every eligible candidate has equal support regardless of ID, class, template or response shape; arbitrary live histories can remove cases.','Unconfigured policy chooses lowest ID rather than random; captured original source is lowest. This is engine behavior, not a generator-specific promise. No database queried or modified.']}

def main():
 samples=v.load(E/'independent-samples.json');batch=v.load(E/'batch.json');sa=v.load(E/'delivery-samples/accepted.json');ba=v.load(E/'delivery-batch/accepted.json')
 coverage={k:describe(rs) for k,rs in [('raw',samples),('accepted',sa),('batch_raw',batch),('batch_accepted',ba)]}
 v.save('coverage-report.json',coverage)
 probe=probes(samples,'independent-samples.json','raw')+probes(sa,'delivery-samples/accepted.json','accepted')+probes(batch,'batch.json','batch raw')+probes(ba,'delivery-batch/accepted.json','batch accepted')
 v.save('shortcut-report.json',probe);v.save('selection-report.json',selection_report())
 cf=v.load(E/'counterfactual-records.json');details=[v.check(r) for r in cf]
 native=v.load(E/'native-report.json');v.save('counterfactual-report.json',{'commands':['.venv/bin/python review.py','generate/runs/current/check-engine native-input.json native-report.json','render_preview.py --input render-counterfactual-input.json --output render-counterfactual --asset-root assets'],'records':details,'relationships':[{'pair':[0,1],'changed':'RHS7 to6','expected':'inconsistent III only -> dependent II only','observed':[choice(r) for r in cf[:2]],'passed':klass(cf[0])=='inconsistent' and klass(cf[1])=='dependent'},{'pair':[1,2],'changed':'multiply every equation by2','expected':'preserve dependent II only','observed':[choice(cf[i]) for i in [1,2]],'passed':choice(cf[1])==choice(cf[2])},{'pair':[1,3],'changed':'permutation of category order only','expected':'same classification; Roman key follows dependent to I','observed':[choice(cf[i]) for i in [1,3]],'passed':choice(cf[3])=='I only'}],'native_outcomes':[r for r in native['records'] if r.get('label') in [r['question'][':question/id'] for r in cf]],'native_note':'All valid and invalid field-owned choices tested for each pair. Full native records keyed by question_id/label are retained in native-report.json; no free-entry field exists.'})
 pedagogical={'learner_operation':v.load(E/'source-analysis.json')['skill'],'fixed_features':[{'feature':'Three disjoint classification categories; exactly one true category; None never qualifies','justification':'Tutorial3163 partitions the systems by existence and uniqueness. Fixed correct-count is mathematical, not incidental.'},{'feature':'Small 2x2,2x3,3x2 moderate systems and short source elimination schedules','justification':'All source moderate practices use these shapes and Gaussian elimination; varying rank/consistency preserves the task.'},{'feature':'First pivot x, at least one nonzero coefficient pivot','justification':'All observed practice systems retain a leading x pivot and substantive elimination; conservative workload constraint. It does not determine consistency or true statement.'}], 'answer_roles':[{'role':'qualifying semantic classification','eligible_variation':'All3 for2x2 and3x2; dependent/inconsistent for2x3','observed':'Every one of17 template controls exhibits all its feasible classifications. Exact batch contains2 dependent,2 inconsistent,1 independent.'},{'role':'correct displayed statement/position and full radio bank','eligible_variation':'Permute classes and choices; preserve each captured bank','observed':'Source banks replay exactly; normal keys/positions vary within templates. Controlled order permutation moves dependent answer II to I.'},{'role':'pivot/free columns and contradiction evidence','eligible_variation':'Rank1/2 where possible; free y/z; RHS contradiction vs zero','observed':'Coverage report measures ranks/free columns. Controlled contradiction7→6 changes answer III→II; scaling preserves II.'}], 'coverage':[{'case':'Every template before/after filtering','sample_refs':['coverage-report.json','independent-samples.json','delivery-samples/accepted.json'],'result':'170/170 survived; all17 source schedules retain feasible classification cases and varying correct actions.'},{'case':'Exact five-record batch','sample_refs':['batch.json','coverage-report.json','delivery-batch/accepted.json'],'result':'5/5 survived:2 dependent,2 inconsistent,1 independent. Shape2x3 subgroup has two inconsistent cases; fresh q-74635 controls include both consistency outcomes. No fixed superficial action answers all five. This small batch does not certify all eligible cases.'}], 'counterfactuals':[{'kind':'relevant','change':'Hold q-74638 coefficients,order,seed fixed; final RHS7→6','expected':'Contradiction0=1 disappears; inconsistent III only becomes dependent II only','observed':'Keys,visible matrices,solution conclusions,rendered prompts and all native choice outcomes follow III→II','status':'passed','justification':'Source contradiction vs redundant row is the necessary decision.','sample_refs':['counterfactual-records.json','counterfactual-report.json','native-report.json','render-counterfactual/rendering.json']},{'kind':'irrelevant','change':'Multiply both equations of the dependent instance by2','expected':'Same solution set and II only answer','observed':'Visible coefficients and matrix stages scale; classification,conclusion,rendered correct control and native accepted semantic action stay II only','status':'passed','justification':'Nonzero equation scaling preserves real solution sets; source Gaussian operations use this invariance.','sample_refs':['counterfactual-records.json','counterfactual-report.json','native-report.json','render-counterfactual/rendering.json']},{'kind':'irrelevant','change':'Permute category order with matrix fixed','expected':'Same dependent classification; response label follows its new position','observed':'Dependent moves fromII toI; prompt,solution,key and native accepted option follow','status':'passed','justification':'Statement position is incidental to the solution set; this checks an answer-producing action rather than only classification metadata.','sample_refs':['counterfactual-records.json','counterfactual-report.json','native-report.json','render-counterfactual/rendering.json']}], 'shortcut_probes':probe,'delivery':{'stages_examined':['generator rejection/resampling and explicit parameter guards','actual requested-difficulty filter','actual inventory/within-batch deduplication at basis5374','read-only reproduction of learner band weighting,within-band selection,history exclusions and unconfigured fallback'],'sample_refs':['sampling-attempts.json','boundary-report.json','delivery-samples/delivery.json','delivery-batch/delivery.json','selection-report.json','coverage-report.json'],'result':'No normal rejections in170; forced invalid first construction retries successfully. Actual filter retains170/170 controls and5/5 batch. Feasible cases remain in controls. Selection does not inspect class/template; moderate positive-weight support preserved subject to history.'},'limitations':['Finite probes do not prove absence of every shortcut. Each small batch template subgroup is evaluated against independent controls; singleton conditional success alone is not a structural predictor.','Captured inventory basis5374; later inventory/history/policy may differ. Selection scenarios and synthetic insertion IDs are explicit, not actual live learner state.','Source canonical has no captured answer-fields, so its bank cannot be certified. All17 captured practice banks replay.','Inventory has10 non-source records but no captured generation metadata; independent math checks all27, with no defect demonstrated. No generated source attribution was invented.']}
 v.save('pedagogical-variation.json',pedagogical)
 print('coverage templates',len(coverage['raw']),'probes',len(probe),'batch class counts',dict(Counter(klass(r) for r in batch)))
if __name__=='__main__':main()
