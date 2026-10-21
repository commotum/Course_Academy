import json,pathlib,re,collections,hashlib,subprocess,sys
E=pathlib.Path(__file__).resolve().parent;J=E.parent;R=pathlib.Path('/home/jake/Developer/Course_Academy')
def load(p):return json.load(open(E/p))
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
def info(r):
 q=r.get('question',r);p=q[':question/problem'];body=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',p,re.S)[1]
 m=[[int(x.strip()) for x in row.split('&')] for row in body.split('\\\\')]
 rows=[int(n)-1 for n in re.findall(r'\$(\d)(?:\$|\\text\{)',p.split('rows')[0])]; v=[next(x for x in m[row] if x) for row in rows];f=q[':question/answer-fields'][0];bank=[int(a[':answer/value']) for a in f[':answer-field/choices']]
 return dict(matrix=m,rows=rows,values=v,total=sum(v),bank=bank,rank=sorted(bank).index(sum(v)),position=bank.index(sum(v)),cols=[next(i for i,x in enumerate(m[row]) if x) for row in rows])
def dist(rs):
 a=[info(r) for r in rs]
 return dict(count=len(rs),rows=dict(collections.Counter(','.join(map(str,x['rows'])) for x in a)),leading_columns=dict(collections.Counter(str(c) for x in a for c in x['cols'])),correct_rank=dict(collections.Counter(str(x['rank']) for x in a)),correct_raw_position=dict(collections.Counter(str(x['position']) for x in a)),sums=dict(collections.Counter('positive' if x['total']>0 else 'negative' if x['total']<0 else 'zero' for x in a)),profiles=dict(collections.Counter(r.get('generation',{}).get('bank_profile','unknown') for r in rs)),attempts=dict(collections.Counter(str(r.get('generation',{}).get('value_sampling_attempts',0)) for r in rs)))
raw=load('fresh-records.json');post=load('delivery-fresh/accepted.json');batch=load('batch-records.json');batchpost=load('delivery-batch/accepted.json')
coverage={name:dist(rs) for name,rs in [('fresh_before',raw),('fresh_after',post),('batch_before',batch),('batch_after',batchpost)]}
coverage['per_profile']={p:dist([r for r in raw if r['generation']['bank_profile']==p]) for p in sorted(set(r['generation']['bank_profile'] for r in raw))}
assert coverage['fresh_before']==coverage['fresh_after'];assert coverage['batch_before']==coverage['batch_after'];save('coverage-results.json',coverage)
# No source rows are designated generated: original IDs come from captured instructional evidence.
src=json.load(open(J/'source/source.json'));original={q[':question/id'] for q in src['material']['kp'][':knowledge-point/questions']};inv=json.load(open(J/'source/inventory.json'));audit=[]
for q in inv['questions']:
 a=info(q);f=q[':question/answer-fields'][0];key=f.get(':answer-field/correct');target=key.get(':answer/value') if isinstance(key,dict) else None
 audit.append(dict(question_id=q[':question/id'],entity_id=q[':db/id'],original_source=q[':question/id'] in original,independent_sum=a['total'],bank=a['bank'],key=None if target is None else int(target),key_correct=None if target is None else int(target)==a['total'],generation_metadata_available=any('generat' in k for k in q)))
assert all(a['key_correct'] is not False for a in audit)
save('inventory-audit.json',dict(basis=inv['basis'],records=audit,limitation='Captured stored records inspected for mathematical keys; 15 are original sources, including q-129207. Five other records have no generation metadata. The prior omission of a source profile is repaired. No stored generated instance was demonstrated to have this omission defect. No absence of all possible historical defects is claimed.'))
save('affected-inventory.json',{'affected_questions':[]})
# Exact read-only model of question_selection.rs::select, with captured candidate IDs.
# Only the hypothetical newly accepted db IDs are assigned consecutive values; historical provenance is not inferred.
def band(q):
 d=q.get(':question/difficulty');return d.get(':db/ident') if isinstance(d,dict) else d
candidates=[dict(id=q[':db/id'],record={'question':q},band=band(q)) for q in inv['questions'] if q[':question/answer-fields'][0].get(':answer-field/correct')]
newstart=max(q[':db/id'] for q in inv['questions'])+1
candidates += [dict(id=newstart+i,record=r,band=band(r['question'])) for i,r in enumerate(batchpost)]
def select(cs,seed,weights):
 cs=sorted(cs,key=lambda c:c['id'])
 if weights is None:return cs[0] if cs else None
 digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 u=lambda o:(int.from_bytes(digest[o:o+8],'big')>>11)/2**53
 bands=[[c for c in cs if c['band']==':question.difficulty/'+b] for b in ['easy','moderate','hard']];unrated=[c for c in cs if c['band'] is None]
 total=sum(w for p,w in zip(bands,weights) if p)
 if total>0:
  d=u(0)*total;pool=[]
  for bs,w in zip(bands,weights):
   if not bs or w==0:continue
   pool=bs
   if d<w:break
   d-=w
 else:pool=unrated
 return pool[int(u(8)*len(pool))] if pool else None
selection={}
for label,cs,weights in [('positive_easy_all_fresh',candidates,[6,3,1]),('only_new_batch_fresh',[c for c in candidates if c['id']>=newstart],[6,3,1]),('first_two_new_seen',[c for c in candidates if c['id']>=newstart+2],[6,3,1]),('unconfigured_policy',candidates,None),('easy_disabled',candidates,[0,1,1])]:
 selected=[select(cs,'independent-review-'+str(i),weights) for i in range(512)];counts=collections.Counter(str(c['id']) if c else 'none' for c in selected)
 selection[label]=dict(candidate_count=len(cs),weights=weights,draw_count=512,selected_counts=dict(counts),selected_case_counts=dict(collections.Counter(('none' if c is None else str(info(c['record'])['rank'])) for c in selected)))
save('selection-results.json',dict(implementation='faithful read-only reproduction of engine/rust/question_selection.rs::select; SHA256 bands and candidate index; source inspected',implementation_sha256=hashlib.sha256((R/'engine/rust/question_selection.rs').read_bytes()).hexdigest(),inventory_basis=inv['basis'],new_ids='hypothetical consecutive IDs above captured max; changes which seed picks which record, not reachability',scenarios=selection,limits=['Actual policy and learner history are not included in the capture; test explicit positive-easy, unconfigured and disabled-easy policies and exclusions. No prediction of a particular live learner task.','Known keyed inventory candidates only; malformed original records without keys excluded.','Zero easy weight intentionally excludes the entire easy generator, not a decision subgroup. An unconfigured policy always selects the first eligible ID. Positive easy weights permit all fresh easy candidates uniformly; histories may reduce the available set.']))
shape=lambda bank:[b-a for a,b in zip(sorted(bank),sorted(bank)[1:])]
# Surface strategy measurements, separately per template and normalized bank shape.
probes=[]
def add_probes(rs,ref,tag):
 subgroups=[('overall',tag,rs)]
 for t in ['sum_2_rows','sum_3_rows']:
  subgroup=[r for r in rs if r['generation']['template']==t]
  if subgroup:subgroups.append(('within_template',tag+'/'+t,subgroup))
 # bank shape is recognizable from learner-visible numbers; report conditional maximum fixed-rank success.
 shapes=collections.defaultdict(list)
 for r in rs:shapes[tuple(shape(info(r)['bank']))].append(r)
 for sh,rr in shapes.items():subgroups.append(('other_recognizable_subgroup',tag+'/numeric gaps '+str(sh),rr))
 strategies={**{f'choose numeric rank {k}':lambda a,k=k:sorted(a['bank'])[k] for k in range(5)},**{f'choose raw position {k}':lambda a,k=k:a['bank'][k] for k in range(5)},'sum diagonal entries of requested rows':lambda a:sum(a['matrix'][i][i] for i in a['rows']),'sum first-column entries of requested rows':lambda a:sum(a['matrix'][i][0] for i in a['rows']),'sum last-column entries of requested rows':lambda a:sum(a['matrix'][i][-1] for i in a['rows']),'ignore targets and sum all leading entries':lambda a:sum(next(x for x in row if x) for row in a['matrix'])}
 for scope,name,rr in subgroups:
  aa=[info(r) for r in rr]
  for strategy,fn in strategies.items():
   n=sum(fn(a)==a['total'] for a in aa)
   # A one-item subgroup has no evidence of a repeated shortcut. Never label it a structural predictor.
   probes.append(dict(cue=strategy,subgroup=name,scope=scope,strategy=strategy,correct=n,total=len(aa),baseline=.2,disposition='not_predictive',conclusion=f'Five radio choices give a 0.2 uniform-choice baseline. {n}/{len(aa)} in this finite subgroup; no source-backed deterministic answer rule established by this cue.'+(' Singleton subgroup is descriptive only.' if len(aa)==1 else ''),sample_refs=[ref]))
add_probes(raw,'fresh-records.json','fresh before/after delivery');add_probes(batchpost,'delivery-batch/accepted.json','exact surviving runner batch')
save('shortcut-results.json',probes)
print(json.dumps(dict(coverage={k:v for k,v in coverage.items() if k!='per_profile'},inventory_records=len(audit),shortcut_probes=len(probes)),indent=2))
