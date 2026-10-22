#!/usr/bin/env python3
import sys
sys.dont_write_bytecode=True
import json,re,pathlib,collections,hashlib,itertools
R=pathlib.Path(__file__).resolve().parent;J=R.parent
def load(p):return json.loads(pathlib.Path(p).read_text())
def save(n,x):(R/n).write_text(json.dumps(x,indent=2))
def val(f):
 ref=f[':answer-field/correct'];aid=ref.get(':answer/id') if isinstance(ref,dict) else ref[1]
 return next(a[':answer/value']=='true' for a in f[':answer-field/choices'] if a[':answer/id']==aid)
def norm(s):return re.sub(r'[{}\s$]','',s)
def signature(q):
 body=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S)[1]
 return (re.search(r'([A-E])\s*=',q[':question/problem'])[1],len(body.split(r'\\')),tuple(sorted(norm(f[':answer-field/key']) for f in q[':question/answer-fields'] if f[':answer-field/key']!='None of the above')))
def pattern(q):return tuple((norm(f[':answer-field/key']),val(f)) for f in q[':question/answer-fields'])
def semantic(q):return tuple(v for _,v in pattern(q))
def zero_case(q):
 body=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S)[1]
 m=[[int(v) for v in row.split('&')] for row in body.split(r'\\')];n=len(m)
 upper=any(m[i][j]!=0 for i in range(n) for j in range(n) if i<j);lower=any(m[i][j]!=0 for i in range(n) for j in range(n) if i>j)
 return 'neither' if upper and lower else 'upper' if upper else 'lower' if lower else 'diagonal'
source=load(J/'source/source.json')['material']['kp'][':knowledge-point/questions'];mapping={}
for q in source:mapping[signature(q)]={norm(f[':answer-field/key']):val(f) for f in q[':question/answer-fields'] if f[':answer-field/key']!='None of the above'}
stages={name:load(R/path) for name,path in [('raw-controls','controls.json'),('raw-fresh','fresh.json'),('raw-moderate','moderate.json'),('delivered-moderate','delivery-moderate/accepted.json'),('delivered-hard','delivery-hard/accepted.json'),('runner-batch','batch.json'),('delivered-batch','delivery-batch/accepted.json')]}
probes=[];stage_results={}
def source_prediction(q):
 p=mapping.get(signature(q),{})
 return tuple(not any(p.values()) if f[':answer-field/key']=='None of the above' else p.get(norm(f[':answer-field/key'])) for f in q[':question/answer-fields'])
def summarize(rs):
 groups=collections.defaultdict(list)
 for r in rs:groups[str(signature(r['question']))].append(r)
 return {'count':len(rs),'matrix_region_cases':dict(collections.Counter(zero_case(r['question']) for r in rs)),'truth_vectors':dict(collections.Counter(str(semantic(r['question'])) for r in rs)),'source_signature_hits':sum(source_prediction(r['question'])==semantic(r['question']) for r in rs),'conditional_signatures':[{'signature':s,'total':len(rows),'truth_patterns':len(set(semantic(r['question']) for r in rows)),'source_signature_hits':sum(source_prediction(r['question'])==semantic(r['question']) for r in rows)} for s,rows in groups.items()]}
for stage,rs in stages.items():stage_results[stage]=summarize(rs)
def add_probe(cue,subgroup,scope,rs,predict,refs,conclusion,disposition='not_predictive'):
 hits=sum(tuple(predict(r['question']))==semantic(r['question']) for r in rs);counts=collections.Counter(semantic(r['question']) for r in rs);baseline=max(counts.values())/len(rs)
 probes.append({'cue':cue,'subgroup':subgroup,'scope':scope,'strategy':conclusion.split(';')[0],'correct':hits,'total':len(rs),'baseline':baseline,'disposition':disposition,'conclusion':conclusion+'; baseline is empirical best single fixed complete selection in this subgroup. A hit means the entire response, including None, is correct.','sample_refs':refs})
for stage,path in [('delivered-moderate','delivery-moderate/accepted.json'),('delivered-hard','delivery-hard/accepted.json'),('delivered-batch','delivery-batch/accepted.json')]:
 rs=stages[stage]
 add_probe('label + dimension + statement wording',stage,'overall',rs,source_prediction,[path,'shortcut-results.json'],'Use the source-example selection for each visible signature; fails on changed answer-bearing assignments')
 add_probe('answer position',stage,'overall',rs,lambda q:[i in (1,2) for i in range(len(q[':question/answer-fields']))],[path,'shortcut-results.json'],'Always select ordinary positions 2 and 3; does not answer the complete pool')
 add_probe('selection count / all ordinary',stage,'overall',rs,lambda q:[f[':answer-field/key']!='None of the above' for f in q[':question/answer-fields']],[path,'shortcut-results.json'],'Always select all three ordinary statements; diagonal cases make this mathematically correct but other cases defeat it')
 groups=collections.defaultdict(list)
 for r in rs:groups[str(signature(r['question']))].append(r)
 for sig,rows in groups.items():
  add_probe('recognizable template signature',stage+':'+sig,'within_template',rows,source_prediction,[path,'shortcut-results.json'],'Use the original source selection within this visible signature; controlled same-signature matrices demonstrate multiple complete responses' if stage!='delivered-batch' else 'Use the original source selection within this batch signature; singleton signatures are observations, not evidence of a stable generator rule')
# Include an actual mathematical shortcut so simplification is not confused with a defect.
diagonal=[r for r in stages['delivered-moderate'] if zero_case(r['question'])=='diagonal']
add_probe('diagonal zero regions','delivered moderate diagonal matrices','other_recognizable_subgroup',diagonal,lambda q:[f[':answer-field/key']!='None of the above' for f in q[':question/answer-fields']],['delivery-moderate/accepted.json','shortcut-results.json'],'Inspect zeros on both off-diagonal halves, then select all three ordinary statements; this is the intended definition applied correctly','intended_skill')
save('shortcut-results.json',{'method':'Strategies fixed from source and previous review, not fitted to metadata or answers. Signatures use only label, dimension and visible statement wording.','stages':stage_results,'probes':probes,'batch_assessment':'All five survive. Two diagonal and three lower-only matrices, so two complete response vectors remain. Position-2/3 strategy solves 3/5 and select-all solves 2/5. Source signature lookup solves 3/5. This small batch lacks upper-only/neither; it does not by itself prove broad coverage. Duplicate diagonal decision profiles are legitimate practice instances, not a new universal answer rule. Both 4x4 batch items happen to be lower-only; the same 4x4 visible banks have all four outcomes in the independent delivered controls. No all-batch surface strategy in the preregistered probes succeeds.'})
# Read-only reproduction of the inspected Rust selection, with explicit hypothetical IDs.
inv=load(J/'source/inventory.json');accepted=stages['delivered-batch'];captured=inv['questions'];pool=[(q.get(':db/id'),q,'captured') for q in captured]+[(10**18+i,r['question'],'hypothetical-new') for i,r in enumerate(accepted)]
def enum(x):return x.get(':db/ident') if isinstance(x,dict) else x
def select(candidates,weights,seed):
 candidates=sorted({i:(i,q,origin) for i,q,origin in candidates}.values(),key=lambda a:a[0])
 if weights is None:return candidates[0] if candidates else None
 bands=[[c for c in candidates if enum(c[1].get(':question/difficulty'))==':question.difficulty/'+level] for level in ['easy','moderate','hard']]
 unrated=[c for c in candidates if not c[1].get(':question/difficulty')]
 d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=lambda off:(int.from_bytes(d[off:off+8],'big')>>11)/2**53
 total=sum(w for w,b in zip(weights,bands) if b)
 if total:
  draw=u(0)*total;b=None
  for w,band in zip(weights,bands):
   if not band or not w:continue
   b=band
   if draw<w:break
   draw-=w
 else:b=unrated
 return b[int(u(8)*len(b))] if b else None
selection=[]
for name,candidates in [('all-captured-plus-new',pool),('new-batch-only',[c for c in pool if c[2]=='hypothetical-new']),('earlier-batch-prefix-seen',[c for c in pool if c[0] not in [10**18,10**18+1]])]:
 for weights in [None,[0,1,0],[1,1,1],[0,0,1]]:
  draws=[select(candidates,weights,'revision-check-'+str(i)) for i in range(32)]
  selection.append({'history_scenario':name,'weights':weights,'draws':[{'seed':'revision-check-'+str(i),'question_id':c[1][':question/id'] if c else None,'origin':c[2] if c else None,'case':zero_case(c[1]) if c else None} for i,c in enumerate(draws)],'cases':dict(collections.Counter(zero_case(c[1]) if c else 'none' for c in draws))})
# Enumerate every freshness subset of five new batch entries: exact support, not Monte Carlo.
batch_subsets=[]
for mask in range(32):
 fresh=[c for i,c in enumerate(pool[-5:]) if mask&(1<<i)]
 batch_subsets.append({'fresh_mask':mask,'eligible_count':len(fresh),'conditional_moderate_cases':dict(collections.Counter(zero_case(c[1]) for c in fresh)),'uniform_probability_per_item':1/len(fresh) if fresh else 0,'unconfigured_first_id':select(fresh,None,'fixed')[1][':question/id'] if fresh else None})
save('selection-results.json',{'implementation':'engine/rust/question_selection.rs:107-201 inspected; exact SHA256, sorted unique IDs, positive-weight rated bands then unrated fallback; zero-weight rated bands excluded.','captured_basis':inv['basis'],'captured_count':len(captured),'new_count':len(accepted),'scenarios':selection,'all_batch_freshness_subsets':batch_subsets,'limits':['Actual learner seen-history and active policy weights unavailable; scenarios explicitly conditional.','No publication occurred, so assigned new entity IDs are hypothetical. Conditional uniform per-band support is independent of that assignment.','An unconfigured policy selects the lowest fresh entity and need not display every outcome. Selection does not guarantee balanced coverage to an individual learner.','Concurrent inventory changes can alter deduplication and selection.'],'conclusion':'The examined selection stage introduces no answer-based restriction. With positive moderate weight, all fresh delivered moderate records have positive probability. Freshness can remove outcomes, explicitly shown for every batch subset. Existing inventory remains a mixture of source items and one unprovenanced stored question, not newly certified generated material.'})
save('stage-coverage.json',stage_results)
(R/'session-state.md').write_text('106 independent exact-arithmetic records pass; all 12 source replays match complete captured banks. Native grader: 280 accepted and 280 rejected. Real delivery: 42 moderate, 54 hard, and 5 batch records accepted with no duplicates. Conditional surface probes and read-only Rust selection reproduction saved. Actual renderer succeeded; screenshot inspection and final evidence contract pending.\n')
print(json.dumps({k:{a:v for a,v in x.items() if a!='conditional_signatures'} for k,x in stage_results.items()},indent=2))
