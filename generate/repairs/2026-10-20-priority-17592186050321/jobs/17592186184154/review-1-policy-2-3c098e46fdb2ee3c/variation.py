import sys,os,json,pathlib,collections,hashlib,re,importlib.util
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;J=E.parent;W=J/'workspace'
sys.path.insert(0,str(W));import generator as g
save=lambda n,d:(E/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
original=g.generate;raw=[]
def traced(*a,**kw):
 r=original(*a,**kw);raw.append(r);return r
g.generate=traced;st={};post=g.sample(240,867530921,audit=st);g.generate=original
save('raw-attempts.json',raw)
def group(r):
 f=r['generation']['template'];p=r['question'][':question/problem']
 if f=='radical':return 'radical-reciprocal' if r'\sqrt{x}}' in p else 'radical-product'
 if f=='quotient':return 'quotient-denominator-'+re.search(r'\}\{x\^\{(\d+)\}\}',p)[1]
 return 'blank'
def choices(r):return r['question'][':question/answer-fields'][0][':answer-field/choices']
def keyid(r):return r['question'][':question/answer-fields'][0][':answer-field/correct'][1]
def keyindex(r):return [a[':answer/id'] for a in choices(r)].index(keyid(r))
def counts(rs):
 return {'total':len(rs),'templates':dict(collections.Counter(r['generation']['template'] for r in rs)),'roles':dict(collections.Counter(r['generation']['template']+':'+str(r['generation']['parameters']['target']) for r in rs)),'visible_groups':dict(collections.Counter(group(r) for r in rs)),'signs':dict(collections.Counter(r['generation']['template']+':'+str((r['generation']['parameters']['a']>0,r['generation']['parameters']['b']>0)) for r in rs))}
def probes(rs,ref):
 out=[];radios=[r for r in rs if len(choices(r))==5]
 groups={'all':radios}
 for t in ['quotient','radical']:groups[t]=[r for r in radios if r['generation']['template']==t]
 for name in sorted(set(map(group,radios))):groups[name]=[r for r in radios if group(r)==name]
 for subgroup,rr in groups.items():
  if not rr:continue
  for strategy in ['first','last','shortest','longest']:
   def pred(r):
    if strategy=='first':return choices(r)[0]
    if strategy=='last':return choices(r)[-1]
    return (min if strategy=='shortest' else max)(choices(r),key=lambda a:len(a[':answer/value']))
   correct=sum(pred(r)[':answer/id']==keyid(r) for r in rr)
   out.append({'cue':'choice position' if strategy in ['first','last'] else 'visible TeX length','subgroup':subgroup,'scope':'overall' if subgroup=='all' else ('within_template' if subgroup in ['quotient','radical'] else 'other_recognizable_subgroup'),'strategy':strategy,'correct':correct,'total':len(rr),'baseline':.2,'disposition':'defect' if correct==len(rr) else 'not_predictive','conclusion':f'{correct}/{len(rr)} vs uniform five-choice rate 0.20. This surface strategy is not uniformly correct in this tested subgroup.' if correct<len(rr) else 'Perfect surface predictor, inspect whether mathematical skill is involved.','sample_refs':[ref]})
 return out
accepted=json.load(open(E/'delivery-sample/accepted.json'));batch=json.load(open(E/'runner-batch.json'));ba=json.load(open(E/'delivery-batch/accepted.json'))
# Same-band learner selection faithful to question_selection.rs: synthetic new db IDs,
# sorted BTreeSet pool and SHA256 u53 from bytes 8..16 once moderate chosen.
inv=json.load(open(J/'source/inventory.json'))
old=[];excluded=[]
for q in inv['questions']:
 fs=q.get(':question/answer-fields',[])
 # Match the captured necessary eligibility conditions: canonical key and fields.
 if not fs or any(not f.get(':answer-field/correct') for f in fs):excluded.append(q[':db/id']);continue
 band=q.get(':question/difficulty',{}).get(':db/ident','unrated').split('/')[-1]
 old.append({'id':q[':db/id'],'band':band,'source_question_id':q[':question/id']})
start=max(q[':db/id'] for q in inv['questions'])+1
new={start+i:r for i,r in enumerate(accepted)}
pool=sorted([q['id'] for q in old if q['band']=='moderate']+list(new))
def select(pool,seed):
 b=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 u=(int.from_bytes(b[8:16],'big')>>11)/(1<<53)
 return pool[int(u*len(pool))]
selected=[];draws=[]
for t in range(12000):
 seed=f'independent-review-{t}';q=select(pool,seed)
 draws.append({'seed':seed,'db_id':q,'new':q in new})
 if q in new:selected.append(new[q])
save('selection-draws.json',draws)
selection={'method':'Faithful read-only same-band reproduction of Rust BTreeSet ordering and SHA256 high-53-bit uniform selection. Candidate ID assignment is synthetic and explicit, not a claim about future allocated EDB IDs.','source':'engine/rust/question_selection.rs:select; learning.rs:validate_practice_question and fresh-candidate selection','captured_basis':inv['basis'],'eligible_old_records':old,'excluded_missing_fields_or_key':excluded,'synthetic_new_ids':{'first':start,'last':start+len(accepted)-1},'policy':'Conditioned on a positive moderate weight; all new records are moderate, so weights change band frequency but not relative probabilities inside band. Unknown/live weights and learner histories cannot be reconstructed. Zero moderate weight correctly makes these records unavailable. Unconfigured None policy chooses first sorted candidate, not uniform; capture supplies no active policy.','new_record_selection':counts(selected),'pool_size':len(pool),'draws':len(draws),'history':'Tested fresh empty history. Previously seen questions are removed without template-specific weighting; cannot promise case coverage for an arbitrary exhausted learner.','all_new_records_selected':len(set(r['question'][':question/id'] for r in selected))==len(accepted)}
save('selection-results.json',selection)
report={'seed':867530921,'raw':counts(raw),'resampled':counts(post),'delivery':counts(accepted),'runner_batch':counts(batch),'runner_delivery':counts(ba),'selection':counts(selected),'rejection':st,'limits':selection['policy'],'probes':{'raw':probes(raw,'raw-attempts.json'),'resampled':probes(post,'sample.json'),'delivery':probes(accepted,'delivery-sample/accepted.json'),'selection':probes(selected,'selection-draws.json')}}
save('variation-results.json',report)
# Directed mathematically meaningful shape probes. The answer is determined by power rules here.
intended=[]
for den,pattern in [('3',r'x^{2}'),('4',r'x^{3}')]:
 rr=[r for r in accepted if group(r)=='quotient-denominator-'+den]
 hits=0
 for r in rr:
  matching=[a for a in choices(r) if pattern in a[':answer/value'].split('}{')[-1]]
  # Use explicit reciprocal denominator shape across answer strings; not numerator powers.
  matching=[a for a in choices(r) if re.search(r'\\frac\{[^{}]+\}\{x\^\{'+str(int(den)-1)+r'\}\}',a[':answer/value'])]
  hits+=len(matching)==1 and matching[0][':answer/id']==keyid(r)
 intended.append({'cue':'reciprocal exponent in prompt denominator','subgroup':'quotient-denominator-'+den,'scope':'other_recognizable_subgroup','strategy':'Select primitive whose reciprocal exponent is denominator exponent minus one','correct':int(hits),'total':len(rr),'baseline':.2,'disposition':'intended_skill','conclusion':f'{hits}/{len(rr)} vs uniform 0.20. This derives a necessary antiderivative exponent by the assessed power rule; it is a valid mathematical simplification, not a label or position cue. Source q-49059 similarly allows elimination by one exponent.','sample_refs':['delivery-sample/accepted.json']})
report['intended_probes']=intended;save('variation-results.json',report)
print(json.dumps({'stages':{k:report[k]['visible_groups'] for k in ['raw','resampled','delivery','runner_batch','selection']},'perfect_surface_probes':[p for p in report['probes']['delivery'] if p['correct']==p['total']],'intended':intended,'selection_all_new':selection['all_new_records_selected']}))
