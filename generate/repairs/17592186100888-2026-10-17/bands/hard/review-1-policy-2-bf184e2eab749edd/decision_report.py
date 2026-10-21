import json,hashlib,sys
from pathlib import Path
from collections import Counter,defaultdict
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT));from review_tests import truth,check,g
R=lambda p:json.loads((ROOT/p).read_text())
def key(r):return ''.join('1' if t else '0' for t in truth(r))
samples=R('samples.json');accepted=[]
for band in ('easy','moderate','hard'):accepted.extend(R('delivery-'+band+'/accepted.json'))
probes=[];coverage=[]
for stage,records,ref in [('raw',samples,'samples.json'),('delivered',accepted,'packaging-delivery.json')]:
 grouped=defaultdict(list)
 for r in records:grouped[r['generation']['template']].append(r)
 for template,rs in grouped.items():
  counts=Counter(key(r) for r in rs);assert set(counts)=={'000','011','100','111'},(stage,template,counts)
  refs=[ref] if stage=='raw' else ['delivery-'+rs[0]['question'][':question/difficulty'].split('/')[-1]+'/accepted.json']
  coverage.append({'case':stage+' '+template,'sample_refs':refs,'result':str(dict(counts))+'; all4 admissible decisions retained.'})
  probes.append({'cue':'recognizable function/template shape and fixed label positions','subgroup':stage+' '+template,'scope':'within_template','strategy':'Always choose II and III; also test best constant checkbox subset in this group.','correct':counts['011'],'total':len(rs),'baseline':.25,'disposition':'not_predictive','conclusion':f"Blind uniform choice among4 mathematically admissible subsets is25%; II+III {counts['011']}/{len(rs)}; bestconstant {max(counts.values())}/{len(rs)}. No fixed template determines response.",'sample_refs':refs})
 # Explicit sign subgroup covers previous hard sign cue and constant sign families.
 groups=defaultdict(list)
 for r in records:
  p=r['generation']['parameters'];sgn='negative' if p.get('a',1)<0 or r['generation']['template'] in ('exp_none','inverse_none','cos_i') else 'positive';groups[(r['generation']['template'],sgn)].append(r)
 for (t,sign),rs in groups.items():
  counts=Counter(key(r) for r in rs);assert len(counts)>1
  probes.append({'cue':'sign of outer coefficient/derivative expression','subgroup':stage+' '+t+' '+sign,'scope':'other_recognizable_subgroup','strategy':'Use most frequent full selection pattern for this sign subgroup without calculating.','correct':max(counts.values()),'total':len(rs),'baseline':.25,'disposition':'not_predictive','conclusion':'Comparison baseline is uniform among4 admissible truth tuples. Every tested sign subgroup retains multiple tuples; same-sign false coefficients remove old sign-only shortcut. Finite empirical imbalance is reported, not equated with an exploitable deterministic rule.','sample_refs':['samples.json'] if stage=='raw' else ['delivery-'+rs[0]['question'][':question/difficulty'].split('/')[-1]+'/accepted.json']})
# Faithful reproduction of Rust select on synthetic IDs assigned to captured accepted records.
# It chooses ratedband by positive policy weights then uniform member; it never reads truth/labels.
def select(candidates,weights,seed):
 bands=[[r for r in candidates if r['question'][':question/difficulty'].endswith('/'+band)] for band in ('easy','moderate','hard')];digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();uniform=lambda off:(int.from_bytes(digest[off:off+8],'big')>>11)/(1<<53);total=sum(w for i,w in enumerate(weights) if bands[i]);draw=uniform(0)*total;chosen=None
 for i,w in enumerate(weights):
  if not bands[i] or w==0:continue
  chosen=i
  if draw<w:break
  draw-=w
 pool=bands[chosen];return pool[int(uniform(8)*len(pool))]
selection=[]
for scenario,records,weights in [('all fresh mixedbands',accepted,[1,1,1]),('every7th candidate previously seen',[r for i,r in enumerate(accepted) if i%7],[1,1,1])]+[(band+' only',accepted,[int(band==b) for b in ('easy','moderate','hard')]) for band in ('easy','moderate','hard')]:
 draws=[select(records,weights,'independent-review-'+str(i)) for i in range(1024)];counts=Counter(key(r) for r in draws);assert set(counts)=={'000','011','100','111'};selection.append({'scenario':scenario,'policy_weights':weights,'candidates':len(records),'draws':1024,'truth_counts':dict(counts),'seed_pattern':'independent-review-{0..1023}'})
selection_file=Path(g.__file__).resolve().parents[4]/'engine/rust/question_selection.rs'
(ROOT/'selection.json').write_text(json.dumps({'implementation':'faithful read-only reproduction of question_selection.rs select; candidateorder assigned stablefixture IDs in inputorder','code_sha256':hashlib.sha256(selection_file.read_bytes()).hexdigest(),'cases':selection,'limits':'No live learner history queried. Priorhistory can exhaust any decision case; testedhistory mask removes every7threcord. Policypositiveband draw+uniformquestion cannot intentionally inspect truth. Nonconfigured legacy policy returnslowestid; defaultconfiguredpolicy is weighted. EDBassignedIDs not known beforepublication.'},indent=2)+'\n')
capacity={};rejected=[]
for t in g.LEVELS:
 counts=Counter()
 for p,case in g.parameter_domain(t):g.validate_parameters(t,p);counts[str(case)]+=1
 capacity[t]=dict(counts)
for band,count in [('easy',0),('easy',1001),('moderate',513),('hard',True)]:
 try:g.batch(band,count,1)
 except ValueError as e:rejected.append({'band':band,'count':count,'error':str(e)})
 else:raise AssertionError((band,count))
(ROOT/'sampling-boundaries.json').write_text(json.dumps({'finite_domains':capacity,'rejected_requests':rejected,'inspection':'batch enumerates finite integer parameters, buckets all4 decisions, shuffles once withseed, popsunique parameter assignments. No rejection/resampling loop. Count>=4 cyclesall4 until finitebucket exhaustion; requested5 wellbelow exhaustion. Source replay is evidence_only and neverchosen bynormalbatch.'},indent=2)+'\n')
source=R('source-analysis.json');pairs=R('counterfactuals.json');counter=[]
for kind in ('relevant','irrelevant'):
 relevant=[p for p in pairs if p['kind']==kind];counter.append({'kind':kind,'change':'Independently change claimed derivative or ODE coefficient whileholding functionfixed' if kind=='relevant' else 'Scale function and claimed derivative bysame nonzeroamplitude in homogeneous powerODE','expected':'Derivative-only change111->011; ODE-only change111->100; II/III alwaysagree.' if kind=='relevant' else 'Both responses111; samepower/ODE coefficient relation remains true.','observed':str(len(relevant))+'pairs match independentlycomputed truth; exposedprompt/solution checked and nativegradercheckedall8subsets.','status':'passed','justification':'Differentiation comparison and definition of ODEsolution fromtutorial17592186102031; amplitude is not a truth-bearing feature of homogeneousverification when all dependentexpressionsscale together.','sample_refs':['counterfactuals.json','counterfactual-records.json','grader-report.json','render/rendering.json']})
report={'learner_operation':source['learner_operation'],'fixed_features':source['fixed_features'],'answer_roles':[{'role':'StatementI derivative claim','eligible_variation':'Correct or incorrect coefficient within eachfamily, sameexpression shape/sign','observed':'Both truths in each10families; independentclaim-only pairs toggleI.'},{'role':'StatementsII/III ODE identity and solution membership','eligible_variation':'Choose matching/mismatching ODE coefficient without changing taskfamily','observed':'Both truths in eachfamily; independentODE-only pairs toggleII/III together.'}],'coverage':coverage,'counterfactuals':counter,'shortcut_probes':probes,'delivery':{'stages_examined':['finite parameter buckets and deterministic batch selection, no symbolic rejection loop','publisher normalization, validation, capturedinventorydedup atbasis3683 and requestedbandfilter','each actual5record boundbatch in easy/moderate/hard','faithful weightedlearnerselection reproduction withfresh and seen-mask pools'],'sample_refs':['sampling-boundaries.json','packaging-delivery.json','bound-batches.json','selection.json'],'result':'All4 admissibledecisions survive pertemplate in independentfilteredsample and perbandin actualboundbatches. UIcontrols can encodeallfalse. No family/sign-basedconstantselection shortcut found.'},'limitations':['Hard is source-grounded authoredaffinelog extension, not an observed hardexample.','Canonical reciprocalexample independently checked; exactfullbank replay applies9capturedpracticequestions.','No finiteaudit proves absence of everyshortcut. Livehistory canlaterexhaustdecisioncases; nofutureinventoryguarantee.']}
(ROOT/'pedagogical-variation.json').write_text(json.dumps(report,indent=2)+'\n');print('Decisionreport:',len(probes),'conditionalprobes;',len(coverage),'coveragegroups;',len(selection),'selectionscenarios')
