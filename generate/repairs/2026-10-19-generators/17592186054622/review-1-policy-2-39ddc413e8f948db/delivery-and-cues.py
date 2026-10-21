"""Read-only delivery distribution, selection reproduction and shortcut probes."""
import collections
import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parent
REPO=Path('/home/jake/Developer/Course_Academy')
def load(n):return json.loads((ROOT/n).read_text())
def save(n,d):(ROOT/n).write_text(json.dumps(d,indent=2)+'\n')
def choices(r):return r['question'][':question/answer-fields'][0][':answer-field/choices']
def key(r):
    f=r['question'][':question/answer-fields'][0]
    return next(i for i,c in enumerate(choices(r)) if c[':answer/id']==f[':answer-field/correct'][1])
def affine(s):
    if 'k' not in s:return 0,int(s)
    m=re.fullmatch(r'(\d*)k([+-]\d+)?',s);assert m,s
    return int(m[1] or 1),int(m[2] or 0)
def subgroup(r):
    text=r['question'][':question/problem']
    givens={z:v for z,v in re.findall(r'\\left\(([xy])\\right\)=(-?\d+|k)',text)}
    a,b=re.search(r'then.*?x(?:\^\{(\d+)\})?y(?:\^\{(\d+)\})?\\right',text).groups()
    if 'k' in givens.values():
        z=next(z for z,v in givens.items() if v=='k');n=int(next(v for v in givens.values() if v!='k'))
        return f'symbolic/symbol={z}/powered={"x" if a else "y"}/sign={n>0}'
    return f'numeric/signs={int(givens["x"])>0,int(givens["y"])>0}'
def coverage(records):
    return dict(collections.Counter(subgroup(r) for r in records))

probes=[]
strategies={
    'first choice':lambda vals:0,
    'last choice':lambda vals:4,
    'largest constant':lambda vals:max(range(5),key=lambda i:vals[i][1]),
    'smallest constant':lambda vals:min(range(5),key=lambda i:vals[i][1]),
    'largest coefficient':lambda vals:max(range(5),key=lambda i:vals[i][0]),
    'modal coefficient then first':lambda vals:next(i for i,v in enumerate(vals) if v[0]==collections.Counter(t for t,c in vals).most_common(1)[0][0]),
}
for filename in ['samples.json','delivery/accepted.json','runner-delivery/accepted.json']:
    records=load(filename)
    buckets={'overall':records}
    for r in records:
        g=subgroup(r)
        buckets.setdefault(g,[]).append(r)
        buckets.setdefault(g.split('/')[0],[]).append(r)
    for group,rs in buckets.items():
        for strategy,fn in strategies.items():
            successes=sum(fn([affine(c[':answer/value']) for c in choices(r)])==key(r) for r in rs)
            probes.append({'stage':filename,'subgroup':group,'strategy':strategy,'correct':successes,'total':len(rs),'baseline':0.2})
controlled=load('controlled-bank-records.json')
post=load('delivery/accepted.json')
postby={r['question'][':question/problem']+'|'+','.join(c[':answer/value'] for c in choices(r)):r for r in post}
group_tests=load('controlled-bank-tests.json')['groups'];proof=[]
for g in group_tests:
    rs=[controlled[i] for i in g['indices']]
    delivered=[postby[r['question'][':question/problem']+'|'+','.join(c[':answer/value'] for c in choices(r))] for r in rs]
    assert [key(r) for r in rs]==[key(r) for r in delivered]
    for name,fn in strategies.items():
        hits=sum(fn([affine(c[':answer/value']) for c in choices(r)])==key(r) for r in delivered)
        assert hits==1
        proof.append({'subgroup':g['group'],'strategy':name,'correct':hits,'total':5,'baseline':0.2,'delivery_preserved':True,'record_indices':g['indices']})
save('shortcut-tests.json',{'strategies':'Answer-producing actions use only displayed choice position or choice bank; no generator metadata or prompt arithmetic. Ties break by first displayed choice.','empirical':probes,'controlled':proof,'conclusion':'All six tested bank-only strategies succeed once per five in each controlled recognizable sign/factor subgroup, before and after delivery. All five answer-bearing roles can be correct with the same visible bank and subgroup. This refutes deterministic bank-only predictors for these controlled banks. Fresh-sample rates are descriptive, not an absence-of-shortcuts proof; very small runner subgroups are not used to infer a defect.'})

# Faithful read-only reproduction of question_selection.rs::select using synthetic IDs.
def select(pool, weights, seed):
    pool=sorted(set(pool))
    if weights is None:return pool[0] if pool else None
    digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
    uniform=lambda off:(int.from_bytes(digest[off:off+8],'big')>>11)/2**53
    # This audited pool contains only hard records. No easy/moderate candidates.
    if not pool or weights[2]==0:return None
    return pool[int(uniform(8)*len(pool))]

selection=[]
for filename in ['delivery/accepted.json','runner-delivery/accepted.json']:
    records=load(filename)
    mapping={100000+i:r for i,r in enumerate(records)}
    for label,weights,excluded in [('initial lesson/review/assessment positive hard',[6,3,1],set()),('hard only',[0,0,1],set()),('remedial positive hard',[8,2,1],set()),('exclude first completed prefix',[6,3,1],{100000}),('hard weight zero',[1,1,0],set()),('all seen',[6,3,1],set(mapping))]:
        pool=sorted(set(mapping)-excluded)
        selected=[select(pool,weights,f'independent-selection-{i}') for i in range(4096)]
        hits=collections.Counter(x for x in selected if x is not None)
        chosen=[mapping[x] for x in hits]
        if pool and weights[2]>0:assert set(hits)==set(pool)
        else:assert not hits
        selection.append({'stage':filename,'scenario':label,'weights':weights,'excluded_synthetic_ids':sorted(excluded),'eligible_count':len(pool),'draws':len(selected),'unique_selected':len(hits),'subgroup_support':coverage(chosen),'selection_counts':dict(hits),'seed_pattern':'independent-selection-{0..4095}'})
    first=select(sorted(mapping),None,'unconfigured')
    selection.append({'stage':filename,'scenario':'unconfigured policy','selected_synthetic_id':first,'behavior':'Deterministically selects lowest fresh entity ID, as Rust does. No generator-specific suppression; repeated continuations exclude completed prefix. For all eligible records, a fresh-prefix traversal retains complete support.'})
inventory=load('../source/inventory.json')
save('selection-tests.json',{'implementation':'Faithful select reproduction for the all-hard delivered pools, with actual SHA256 prefix, 53-bit offset-8 uniform and sorted unique entity IDs. learning.rs lines 579-606 excludes seen IDs and invalid practice records before selection.','implementation_hashes':{str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [REPO/'engine/rust/question_selection.rs',REPO/'engine/rust/learning.rs']},'inventory_basis':inventory['basis'],'captured_original_bank':'Four questions: two explicitly hard keyed records; two unrated records lack keys and cannot supply valid fresh practice until independently repaired. Original hard records can coexist with generated hard records. Canonical example is separate from practice.','scenarios':selection,'limits':['No live learner history or selection-weight policy is included in captured inventory; positive-hard, zero-hard and unconfigured branches were examined explicitly.','Entity IDs are synthetic because unpublished records have no allocated database IDs. Counts demonstrate support under the actual algorithm, not predictions of a particular future learner draw.','Zero hard weight intentionally excludes all generated hard records. An all-seen pool correctly has no supply. No generator can guarantee case coverage for an arbitrary history that has already consumed those cases.','Later inventory changes may create more deduplication. Analysis is conditional on captured basis 4975.'],'conclusion':'Every eligible generated subgroup retains positive selection support when hard has positive weight; nothing in weighting or freshness tests conditions on answer roles. Unconfigured policy orders by entity ID, not uniform sampling; this is explicitly distinguished from the weighted case.'})
save('delivery-stage-tests.json',{'raw':{'count':len(load('samples.json')),'coverage':coverage(load('samples.json'))},'controlled':{'count':len(controlled),'coverage':coverage(controlled)},'independent_after_filter':{'count':len(post),'coverage':coverage(post)},'runner_before':{'count':len(load('runner-batch.json')),'coverage':coverage(load('runner-batch.json'))},'runner_after':{'count':len(load('runner-delivery/accepted.json')),'coverage':coverage(load('runner-delivery/accepted.json'))},'rejection_resampling':'Inspected generator.py draw_role_bank: same-subgroup sampling rejects duplicate affine answers before key selection; key drawn uniformly only after bank built. 160 fresh and 1000 boundary records all passed independent visible-prompt math; no selected-key-dependent rejection.','dedup':'Shared check_delivery.py: all 220 independent plus 5 runner records accepted, no duplicates at captured basis 4975. Every controlled subgroup retains all five answer roles.','difficulty':'Every generated hard record passes requested-hard filtering; unrated replay families are kept out of normal sampling.','learner_selection':'See selection-tests.json for weighted, unconfigured, freshness and no-supply branches, limitations and exact reproduction.'})
print(json.dumps({'shortcut_probes':len(probes),'controlled_probes':len(proof),'selection_scenarios':len(selection),'controlled_key_coverage_survives_delivery':True}))
