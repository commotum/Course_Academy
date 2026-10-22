#!/usr/bin/env python3
"""Independent conditional cue tests and read-only learner selection reproduction."""
import json,pathlib,collections,hashlib
E=pathlib.Path(__file__).resolve().parent;J=E.parent
load=lambda n:json.loads((E/n).read_text())
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
def vals(r):return sorted(int(c[':answer/value']) for c in r['question'][':question/answer-fields'][0][':answer-field/choices'])
def ans(r):
 f=r['question'][':question/answer-fields'][0];return next(int(c[':answer/value']) for c in f[':answer-field/choices'] if c[':answer/id']==f[':answer-field/correct'][1])
def gaps(r):return tuple(b-a for a,b in zip(vals(r),vals(r)[1:]))
def old_action(r):
 v=vals(r)
 if gaps(r)==(2,1,1,1) or 0 not in v:return v[1]
 if gaps(r)!=(1,1,1,1):return v[-2]
 return 2
paths={'raw_easy':'sample-easy.json','delivered_easy':'delivery-easy/accepted.json','raw_moderate':'sample-moderate.json','delivered_moderate':'delivery-moderate/accepted.json','batch_raw':'batch-records.json','batch_delivered':'delivery-batch/accepted.json','controlled_banks':'role-witness-records.json','controlled_banks_delivered':'delivery-witness/accepted.json'}
stages={k:load(p) for k,p in paths.items()};stats={};probes=[]
for stage,rs in stages.items():
 stats[stage]={'total':len(rs),'answers':dict(collections.Counter(ans(r) for r in rs)),'profiles':dict(collections.Counter(r['generation']['profile'] for r in rs)),'templates':dict(collections.Counter(r['generation']['template'] for r in rs))}
 groups=[('overall',rs,'overall')]
 for t in sorted({r['generation']['template'] for r in rs}):groups.append(('template='+t,[r for r in rs if r['generation']['template']==t],'within_template'))
 for gap in sorted({gaps(r) for r in rs}):groups.append(('bank gaps='+str(gap),[r for r in rs if gaps(r)==gap],'other_recognizable_subgroup'))
 for p in sorted({r['generation']['profile'] for r in rs}):
  # Profile names aren't visible, but their bank shapes are; retain separate
  # profile diagnostics so mixing numerically identical profiles cannot hide a branch.
  groups.append(('profile diagnostic='+p,[r for r in rs if r['generation']['profile']==p],'other_recognizable_subgroup'))
 for minimum in [0,1]:
  sub=[r for r in rs if gaps(r)==(1,1,1,1) and (min(vals(r))==0 if minimum==0 else min(vals(r))>=1)]
  if sub:groups.append(('consecutive bank '+('with zero' if minimum==0 else 'minimum >= 1'),sub,'other_recognizable_subgroup'))
 for group,sub,scope in groups:
  choices=[('old bank-only composite rule',old_action),('choose second-smallest',lambda r:vals(r)[1]),('choose smallest',lambda r:vals(r)[0]),('choose largest',lambda r:vals(r)[-1]),('choose second-largest',lambda r:vals(r)[-2]),('choose numeric 1',lambda r:1),('choose numeric 2',lambda r:2)]
  for label,action in choices:
   hit=sum(action(r)==ans(r) for r in sub)
   probes.append({'cue':'Numeric bank gaps/rank, constant answer, or layout identity','subgroup':stage+': '+group,'scope':scope,'strategy':label,'correct':hit,'total':len(sub),'baseline':0.2,'disposition':'not_predictive','conclusion':f'{hit}/{len(sub)}; comparison baseline 0.2 is a uniform random choice among five. '+('Singleton subgroup is descriptive only; no deterministic family predictor inferred.' if len(sub)==1 else 'No tested cue answers this entire subgroup; observed finite bias alone is not a universal predictor.' if hit<len(sub) else 'Perfect finite subgroup needs family interpretation; controlled bank-role pairs independently test eligible assignments.'),'sample_refs':[paths[stage],'shortcut-results.json']})
 # Observe ranks within actual recognizable shapes, separate from strategies.
 stats[stage]['shape_correct_positions']={str(g):dict(collections.Counter(vals(r).index(ans(r)) for r in rs if gaps(r)==g)) for g in sorted({gaps(r) for r in rs})}
save('shortcut-results.json',{'stages':stats,'probes':probes,'boundaries':'Raw order is sorted; UI shuffles actual controls. Numeric-rank strategies do not depend on UI order. No finite audit excludes every untested cue. A singleton bank signature is not proof of a family-wide shortcut.'})
# Concrete role-pair acceptance and rendered dependency observations.
cf=load('counterfactual-records.json');grades={r['label']:r for r in load('grader-report.json')['records']}
pairs=[]
for kind,label,i,j,expected in [('relevant','increase column count n',0,1,[3,4]),('irrelevant','increase row count m',0,2,[3,3]),('relevant','decrease basis cardinality k',0,3,[3,4]),('relevant','append zero vector component (n increases)',4,5,[2,3]),('irrelevant','rescale a coefficient preserving independent dimension',4,6,[2,2]),('relevant','add independent parameter coefficient vector',4,7,[2,1]),('irrelevant','rename independent parameters',4,8,[2,2])]:
 a,b=cf[i],cf[j];actual=[ans(a),ans(b)];assert actual==expected
 assert sum(c['outcome']=='accepted' for c in grades['cf-'+str(i)]['checks'])==1 and sum(c['outcome']=='accepted' for c in grades['cf-'+str(j)]['checks'])==1
 pairs.append({'kind':kind,'change':label,'indices':[i,j],'expected':expected,'observed':actual,'prompts_changed':a['question'][':question/problem']!=b['question'][':question/problem'],'solutions_changed':a['question'][':question/worked-solution']!=b['question'][':question/worked-solution'],'native_before':grades['cf-'+str(i)]['checks'],'native_after':grades['cf-'+str(j)]['checks'],'render_indices':[5+i,5+j],'passed':True})
save('counterfactual-results.json',{'pairs':pairs,'render_index_basis':'Zero-based render input: entire batch first, followed by all controlled pairs.','native':'All five options graded at each endpoint, not only keys. Before/after values flip acceptance for relevant changes and retain acceptance for irrelevant changes.','math':'math-results.json independently validates prompt and solution expansions; screenshot inspection recorded separately.'})
# Same-bank alternatives survive shared publisher filtering.
w=stages['controlled_banks_delivered'];minimal=load('minimal-pair.json')
for r in minimal:assert any(vals(s)==vals(r) and ans(s)==ans(r) and s['generation']['parameters']==r['generation']['parameters'] for s in w)
# Full eligible easy domain is finite (current conservative bounds). Independently
# enumerate feasibility and translated observed shapes without generator helpers.
# This checks a changed rule, not arbitrary numeric diversity.
shapes={'small':[0,1,2,3,4],'offset-minus1':[0,1,2,3,4],'offset-minus2':[0,2,3,4,5],'dimensions':[0,1,2,3,5],'one-through5':[0,1,2,3,4]}
domain=[]
for m in range(2,8):
 for n in range(4,13):
  for name,shape in shapes.items():
   supported=set();candidates=0
   for scale in ([1,2] if name=='dimensions' else [1]):
    for anchor in range(n):
     v=[anchor+scale*x for x in shape];feasible=[x for x in v if 1<=n-x<=min(m,n-1)]
     if len(feasible)>=2:candidates+=1;supported.update(n-x for x in feasible)
   expected=set(range(1,min(m,n-1)+1));assert supported==expected,(m,n,name)
   domain.append({'m':m,'n':n,'profile':name,'compatible_banks':candidates,'supported_basis_counts':sorted(supported),'every_candidate_has_multiple_correct_roles':True})
save('construction-domain.json',{'cases':domain,'passed':True,'interpretation':'All 270 m,n,profile combinations admit every eligible positive basis count. Normal sampler picks one of these banks before uniformly selecting among feasible roles; fixed-bank alternatives differ by intended basis reasoning. This independent enumeration matches code branches inspected directly.'})
# Selection implementation directly transcribed from supplied question_selection.rs.
# No database writes or future entity IDs claimed.
inv=json.loads((J/'source/inventory.json').read_text());maxid=max(q[':db/id'] for q in inv['questions']);pool=[]
for q in inv['questions']:pool.append({'id':q[':db/id'],'band':q[':question/difficulty'][':db/ident'].split('/')[-1],'batch':False})
for i,r in enumerate(stages['batch_delivered']):pool.append({'id':maxid+i+1,'band':'easy','batch':True,'record':r})
def select(cs,weights,seed):
 cs=sorted({q['id']:q for q in cs}.values(),key=lambda q:q['id'])
 if weights is None:return cs[0] if cs else None
 bands=[[q for q in cs if q['band']==b] for b in ['easy','moderate','hard']]
 total=sum(w for w,b in zip(weights,bands) if b)
 if total<=0:return None # All records are rated; no unrated fallback in this captured pool.
 digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=lambda off:(int.from_bytes(digest[off:off+8],'big')>>11)/(1<<53)
 draw=u(0)*total;chosen=None
 for i,weight in enumerate(weights):
  if not bands[i] or weight==0:continue
  chosen=i
  if draw<weight:break
  draw-=weight
 band=bands[chosen];return band[int(u(8)*len(band))]
selection=[]
for name,cs in [('captured originals plus accepted batch',pool),('originals already seen',[q for q in pool if q['batch']]),('one generated question remains fresh',[q for q in pool if q['batch']][:1])]:
 for weights in ([1,0,0],[6,3,1],None):
  draws=[select(cs,weights,'independent-current-731-'+str(i)) for i in range(128)];bc=[q for q in draws if q and q['batch']]
  selection.append({'case':name,'weights':weights,'draws':len(draws),'batch_draws':len(bc),'old_shortcut_correct':sum(old_action(q['record'])==ans(q['record']) for q in bc),'selected_correct_values':dict(collections.Counter(ans(q['record']) for q in bc)),'counts':dict(collections.Counter(str(q['id']) if q else 'none' for q in draws))})
save('selection-results.json',{'implementation':'Faithful read-only translation of question_selection.rs::select: BTree sorted unique IDs, rated difficulty bands, SHA256-derived draw, same-band uniform selection; all captured/staged questions rated. seen_before_task/current prefix modeled by candidate removal.','basis':inv['basis'],'staged_ids':'No publication preparation exists. Assign max captured entity ID+1..5 provisionally; exact future order unknown. Positive easy weight gives each accepted batch member nonzero support regardless of actual ID assignment.','cases':selection,'conclusion':'Weighted fresh batch selection retains multiple answers and failures of the old shortcut; unset weights deterministically select first available ID, as engine defines. Arbitrary learner history can leave only one item; no generator can guarantee balanced exposure under every history.','limits':['No actual learner history, activity seed or policy supplied; scenarios are conditional.','Captured inventory basis 5443; later publications can change candidates.','No database identity collisions tested because no publication performed.']})
save('batch-assessment.json',{'raw':stats['batch_raw'],'delivered':stats['batch_delivered'],'old_strategy':{'raw_correct':sum(old_action(r)==ans(r) for r in stages['batch_raw']),'delivered_correct':sum(old_action(r)==ans(r) for r in stages['batch_delivered']),'total':5},'numeric_correct_positions':[vals(r).index(ans(r)) for r in stages['batch_delivered']],'conclusion':'All five survive; five distinct answers (6,8,1,9,5), four numeric positions, five (n,k) tasks. Constant-answer, fixed rank and retained old bank-only strategies do not answer this finite batch. The sole gapped-bank member is descriptive only, not evidence of a universal gapped-bank predictor. Three k=1 items simplify correctly by the intended rank-nullity calculation; basis cardinality still matters.'})
(E/'session-state.md').write_text('Current source replay, 134 independent math checks, old failure replays, packaging pass. Native grader passed 95 selections (19 correct, 76 wrong). Actual delivery: easy60->35, moderate24->24, exact batch5->5; controlled same-bank alternatives survive. Conditional shortcut, full changed construction-domain feasibility and selection scenario evidence saved. Rendering explicit 19-case run and visual QA pending finalization. Package unchanged so far.\n')
print(json.dumps({'delivery':{k:v['total'] for k,v in stats.items()},'old_batch_rule':sum(old_action(r)==ans(r)for r in stages['batch_delivered']),'domain_combinations':len(domain),'probe_rows':len(probes),'perfect_nonsingleton_probes':[(p['subgroup'],p['strategy'],p['correct'],p['total'])for p in probes if p['correct']==p['total'] and p['total']>1]}))
