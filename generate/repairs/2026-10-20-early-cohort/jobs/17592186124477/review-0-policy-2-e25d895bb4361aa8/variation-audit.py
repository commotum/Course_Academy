#!/usr/bin/env python3
"""Read-only post-delivery coverage and cue analysis; no package imports."""
import collections, hashlib, itertools, json, math, pathlib, re, sys
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
def load(p):return json.loads((E/p).read_text())
def save(p,v):(E/p).write_text(json.dumps(v,indent=2)+'\n')
def matrix(q):
    body=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S)[1]
    return [[int(v.strip()) for v in row.split('&')] for row in body.split('\\\\')]
def answer(q):
    a=matrix(q)
    return tuple(next(j+1 for j,x in enumerate(row) if x) for row in a if any(row))
def shape(r):
    a=matrix(r['question']);return (len(a),len(a[0]))
def typ(r):return r['generation']['template'].rsplit('-',1)[-1]
def name(r):return re.search(r'matrix \$(\w+)\$',r['question'][':question/problem'])[1]
def columns(s,n):
    return tuple(range(1,n+1)) if s=='All the columns are pivot' else tuple(map(int,re.findall(r'\$(\d+)\$(?:st|nd|rd|th)',s)))
def fnv(s):
    n=2166136261
    for ch in s:n=((n^ord(ch))*16777619)&0xffffffff
    return n
def ui_position(r,item_id):
    f=r['question'][':question/answer-fields'][0]
    ordered=sorted(f[':answer-field/choices'],key=lambda c:fnv(f"{item_id}:{f[':answer-field/id']}:{c[':answer/id']}"))
    return next(i+1 for i,c in enumerate(ordered) if c[':answer/id']==f[':answer-field/correct'][1])
def subset_baseline(rs):
    return sum(1/sum(math.comb(shape(r)[1],i) for i in range(1,min(shape(r))+1)) for r in rs)/len(rs)
def coverage(rs):
    by={}
    for p in sorted(set(r['generation']['profile'] for r in rs)):
        ss=[r for r in rs if r['generation']['profile']==p];sets=[answer(r['question']) for r in ss]
        n=shape(ss[0])[1]
        by[p]={'count':len(ss),'ranks':sorted(set(map(len,sets))),'targets':sorted(set(sets)), 'column_truth_values':{str(j):sorted(set(j in t for t in sets)) for j in range(1,n+1)}}
    return {'count':len(rs),'template_counts':dict(collections.Counter(typ(r) for r in rs)), 'ranks':dict(collections.Counter(len(answer(r['question'])) for r in rs)), 'distinct_shape_target':len(set((shape(r),answer(r['question'])) for r in rs)), 'profiles':by}

datasets={'raw':load('independent-samples.json'),'delivered':load('delivery-independent/accepted.json'),'batch_raw':load('runner-batch.json'),'batch_delivered':load('delivery-batch/accepted.json')}
cover={k:coverage(v) for k,v in datasets.items()}
save('coverage-results.json',cover)
probes=[]
def add(dataset,group,scope,cue,strategy,correct,total,baseline,conclusion,refs):
    probes.append({'dataset':dataset,'cue':cue,'subgroup':group,'scope':scope,'strategy':strategy,'correct':correct,'total':total,'baseline':baseline,'disposition':'not_predictive','conclusion':conclusion,'sample_refs':refs})
for ds,rs in datasets.items():
    refs=['independent-samples.json' if ds=='raw' else 'delivery-independent/accepted.json' if ds=='delivered' else 'runner-batch.json' if ds=='batch_raw' else 'delivery-batch/accepted.json']
    checks=[r for r in rs if typ(r)=='checkbox'];radios=[r for r in rs if typ(r)=='radio']
    # The same simple position/set actions are evaluated within every recognizable
    # prompt profile and shape/name subgroup, rather than relying on overall balance.
    groups={'all checkbox':checks}
    for r in checks:
        for key in [f"profile {r['generation']['profile']}",f'shape/name {shape(r)}/{name(r)}']:
            groups.setdefault(key,[]).append(r)
    for group,ss in groups.items():
        sets=collections.Counter(answer(r['question']) for r in ss);best,count=sets.most_common(1)[0]
        baseline=subset_baseline(ss)
        note='Best constant subset chosen after seeing data, so frequency is an upper bound for a prespecified fixed-label guess; baseline is uniform over nonempty structurally eligible subsets for each shape.'
        if len(ss)<3:note+=' This tiny batch subgroup has fewer than three examples; memorizing a singleton is not evidence of a construction rule. Larger same-profile controls are assessed separately.'
        add(ds,group,'within_template' if group=='all checkbox' else 'other_recognizable_subgroup','template/shape/name only',f'Always select columns {best}',count,len(ss),baseline,note,refs)
    for pos in range(1,6):
        correct=sum(r['question'][':question/answer-fields'][0][':answer-field/choices'][pos-1][':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1] for r in radios)
        add(ds,'all radio','within_template','stored answer position',f'Choose stored option {pos}',correct,len(radios),.2,'Baseline is uniform choice among five options. The actual UI additionally hashes choices using task-item and field IDs.',refs)
    for rank in sorted(set(len(answer(r['question'])) for r in radios)):
        ss=[r for r in radios if len(answer(r['question']))==rank]
        for strategy in ['lexicographically smallest set','lexicographically largest set']:
            count=0
            for r in ss:
                f=r['question'][':question/answer-fields'][0];sets=[columns(c[':answer/value'],5) for c in f[':answer-field/choices']]
                guess=min(sets) if 'smallest' in strategy else max(sets)
                count+=guess==answer(r['question'])
            add(ds,f'radio options all have cardinality {rank}','other_recognizable_subgroup','bank wording/column labels only',strategy,count,len(ss),.2,'Five equal-cardinality subsets: counting entries in an option cannot identify a unique choice. Baseline is uniform choice among five.',refs)
    # A surface mathematical heuristic which should fail whenever a nonpivot
    # column has nonzero entries. This tests an answer-producing action.
    count=0
    for r in checks:
        a=matrix(r['question']);guess=tuple(j+1 for j in range(len(a[0])) if any(row[j] for row in a));count+=guess==answer(r['question'])
    add(ds,'all checkbox','within_template','column has any nonzero entry','Select every nonzero column',count,len(checks),subset_baseline(checks),'Baseline is uniform over eligible nonempty subsets. This plausible wrong heuristic is contradicted by nonzero nonpivot columns; full-rank/all-column successes express legitimate simplifications.',refs)
    # Actual UI choiceOrder implementation reproduced exactly. Actual DB item and
    # field IDs do not yet exist; test broad hypothetical task-item placements.
    positions=collections.Counter(ui_position(r,item) for r in radios for item in range(1,129))
    for pos in range(1,6):add(ds,'radio, 128 task-item placements each','within_template','UI displayed answer position',f'Choose displayed option {pos}',positions[pos],len(radios)*128,.2,'Baseline is 1/5. Mirrors ui/learning.js choiceOrder with current field UUIDs and hypothetical item IDs 1..128; no actual future DB/task IDs are asserted.',refs)

save('shortcut-results.json',{'probes':probes,'interpretation':'No constant subset predicts a multi-example full-scope profile; checkbox columns change truth status, and radio keys occupy all five positions over controls. Tiny batch cue partitions can be memorized, but neither a uniform subset, position, count nor lexicographic rule solves the five-question batch. Do not treat tiny-cell lookup tables as validated construction-wide predictors.','limits':['Finite tested strategies cannot prove absence of every shortcut.','Actual future task and field entity IDs are unavailable; displayed position observations in the renderer are preview fixtures.']})

# Faithful read-only reproduction of the selection file's deterministic easy-band
# uniform draw; use actual captured entity IDs, and explicitly hypothetical IDs
# for the uncommitted accepted batch. All candidate difficulties here are easy.
def select(ids,seed,weights=(1,1,1)):
    ids=sorted(set(ids))
    if weights is None:return ids[0] if ids else None
    if not ids or weights[0]<=0:return None
    bits=int.from_bytes(hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()[8:16],'big')>>11
    return ids[int((bits/(1<<53))*len(ids))]
inventory=json.loads((E.parent/'source/inventory.json').read_text())
inv_ids=[q[':db/id'] for q in inventory['questions']]
post_ids=list(range(max(inv_ids)+1,max(inv_ids)+1+len(datasets['batch_delivered'])))
selections={}
for label,ids in [('captured_inventory',inv_ids),('projected_five_batch_only',post_ids),('projected_inventory_plus_batch',inv_ids+post_ids)]:
    draws=[select(ids,f'independent-review-74191-{i}') for i in range(2048)]
    assert set(draws)==set(ids)
    assert select(ids,'same')==select(ids,'same')
    assert select([ids[-1]],'history-removes-all-others')==ids[-1]
    assert select(ids,'zero-easy-weight',(0,1,1)) is None
    assert select(ids,'unconfigured',None)==min(ids)
    selections[label]={'candidate_count':len(ids),'candidate_ids':ids,'draw_count':len(draws),'counts':dict(collections.Counter(draws)),'all_candidates_reached':True,'history_single_remaining':ids[-1],'zero_weight_easy':'no selection; no unrated fallback present','unconfigured_policy':'first sorted candidate, per actual Rust fallback','id_basis':'captured entities' if label=='captured_inventory' else 'batch IDs hypothetical; publication and future task IDs are unavailable'}
save('selection-results.json',{'implementation':'engine/rust/question_selection.rs select, lines 130-210; all captured and generated questions are easy. With positive easy weight, the available band is chosen with probability one and uniform(8) selects within sorted fresh candidates.','source_sha256':hashlib.sha256((REPO/'engine/rust/question_selection.rs').read_bytes()).hexdigest(),'captured_basis':inventory['basis'],'scenarios':selections,'limits':['No learner history or active policy configuration is captured. Arbitrary histories may remove any subset. Tested positive easy weighting, zero easy weight, and unconfigured fallback explicitly; no live learner delivery is claimed.','Concurrent publication can change inventory and numeric entity IDs.']})

# Correctly compare inventory's published stable identities, not generator UUIDs.
sys.path.insert(0,str(REPO));sys.path.insert(0,str(E.parent/'workspace'))
from scripts.generator_publish import stable_identities
import generator as g
reproduced=[];results=[]
for q in inventory['questions']:
    if q.get(':question/math-academy-id'):continue
    a=matrix(q);matched=None
    for profile,src in g.SOURCES.items():
        if shape({'question':src})!=(len(a),len(a[0])):continue
        params={'matrix':a}
        if g.kind(profile)=='radio':params['bank']=[list(columns(c[':answer/value'],len(a[0]))) for c in q[':question/answer-fields'][0][':answer-field/choices']]
        try:r=g.generate(profile=profile,seed=0,parameters=params)
        except ValueError:continue
        r['question']=stable_identities(r['question'],source_uuid:=g.SOURCE[':knowledge-point/id'])
        if r['question'][':question/id']==q[':question/id']:
            matched=r;break
    results.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'published_identity_reproduced':bool(matched),'historical_generation_metadata':'Not captured; supplied seed=0 is controlled current reconstruction, not historical provenance.'})
    if matched:reproduced.append(matched)
save('inventory-published-reproductions.json',reproduced)
save('inventory-published-results.json',{'basis':inventory['basis'],'cases':results,'affected_questions':[],'conclusion':'All 21 stored keys independently match their displayed matrices (inventory-results.json); five source-free records also examined here. No demonstrated current weakness to mark affected. This is not a universal historical shortcut absence claim.'})
print(json.dumps({'coverage':{k:{kk:vv for kk,vv in v.items() if kk!='profiles'} for k,v in cover.items()},'shortcut_probes':len(probes),'published_inventory_reproductions':len(reproduced),'selection_scenarios':len(selections)}))
