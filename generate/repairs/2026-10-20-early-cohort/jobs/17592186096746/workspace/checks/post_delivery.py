"""Probe visible decisions before/after real publication filters, read-only selection limits."""
import collections,hashlib,json,sys
from pathlib import Path
W=Path(__file__).resolve().parents[1]
from visible_math import equations,matrix,rref
from shortcut import measure

def read(n):return json.loads((W/'evidence'/n).read_text())
def visible_profile(r):
    rows=[matrix(a[':answer/value'])[0][1:] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
    varies=[len({row[j] for row in rows})>1 for j in range(3)]
    return ''.join(c for c,v in zip('bcd',varies) if v)
def inspect(rs):
    summary=measure(rs);groups={};semantic=set()
    for r in rs:
        f=r['question'][':question/answer-fields'][0];choices=f[':answer-field/choices'];key=f[':answer-field/correct'][1]
        rows=[matrix(a[':answer/value'])[0] for a in choices];ci=next(i for i,a in enumerate(choices) if a[':answer/id']==key)
        first=equations(r['question'][':question/problem'])[0];profile=visible_profile(r)
        name=profile+'/'+('positive' if first[0]>0 else 'negative')
        x=groups.setdefault(name,{'n':0,'positions':collections.Counter(),'magnitude_ranks':{},'raw_first_row_match':0,'unit_pivot_present':0})
        x['n']+=1;x['positions'][ci]+=1
        assert all(matrix(a[':answer/value'])==rref(matrix(a[':answer/value'])) for a in choices)
        assert len({str(rows[i][0]) for i in range(5)})==1
        for j,col in enumerate('bcd',1):
            vals=sorted({abs(v[j]) for v in rows})
            if len(vals)>1:x['magnitude_ranks'].setdefault(col,collections.Counter())[vals.index(abs(rows[ci][j]))]+=1
        x['raw_first_row_match']+=first==rows[ci]
        x['unit_pivot_present']+=any(row[0]==1 for row in equations(r['question'][':question/problem']))
        semantic.add(tuple(rref(equations(r['question'][':question/problem']))[0]))
    summary.update(visible_groups=groups,distinct_normalized_rows=len(semantic))
    assert summary['successes']==summary['same_absolute_bank']==0
    return summary
sets={'raw_batch':read('batch.json'),'delivered_batch':read('delivery-batch/accepted.json'),'raw_fresh':read('fresh-easy.json'),'delivered_fresh':read('delivery-fresh/accepted.json'),'raw_counterfactual':read('counterfactual-easy.json'),'delivered_counterfactual':read('delivery-counterfactual/accepted.json')}
results={k:inspect(v) for k,v in sets.items()}
for raw,out in [('raw_batch','delivered_batch'),('raw_fresh','delivered_fresh'),('raw_counterfactual','delivered_counterfactual')]:
    assert results[raw]['count']==results[out]['count']
    # Publication changes IDs; compare actual prompt, bank and mathematical key.
    def signature(r):
        f=r['question'][':question/answer-fields'][0]
        return (r['question'][':question/problem'],tuple(a[':answer/value'] for a in f[':answer-field/choices']),next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]))
    assert {signature(r) for r in sets[raw]}=={signature(r) for r in sets[out]}
# For the very same visible bank all positions and all numerical ranks are eligible,
# independently read from delivered records. No key/position/magnitude rank is frozen.
controlled={}
for r in sets['delivered_counterfactual']:
    f=r['question'][':question/answer-fields'][0];ci=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])
    controlled.setdefault(visible_profile(r),set()).add(ci)
assert set(controlled)=={'b','c','d','bcd'}
assert all(s==set(range(5)) for s in controlled.values())
# Use the engine's documented all-easy within-band draw rule on a UUID ordering.
# Published entity IDs/order and live learner histories are unavailable.
pool=sorted(sets['delivered_batch'],key=lambda r:r['question'][':question/id']);draws=collections.Counter()
for i in range(25):
    digest=hashlib.sha256(f'course-academy/question-selection/v1/repair-{i}'.encode()).digest()
    u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53)
    draws[pool[int(u*len(pool))]['question'][':question/id']]+=1
report={'passed':True,'sets':results,'controlled_delivered_correct_positions':{k:sorted(v) for k,v in controlled.items()},'baseline':'A fixed candidate position or magnitude rank succeeds on 1/5 controlled members. Signs, rank, zero rows and constant entries cannot distinguish any of the five.','legitimate_simplification':'A supplied unit-pivot row may be copied after recognizing proportionality; that is a source-supported row swap, not the reported sign-only shortcut. Nonunit first pivots cannot be copied directly.','selection':{'engine_file':'engine/rust/question_selection.rs','all_easy_positive_weight':'Uniform within eligible easy pool, hash bytes 8..16. UUID order used as permutation because published entity IDs unavailable.','fallback':'Unconfigured policy selects first eligible entity; zero-weight easy band is unavailable. All surviving members resist the sign probe regardless of order.','draw_count':25,'draws':dict(draws),'limits':['No live learner histories or policy distribution accessed.','Prior-task/current-prefix exclusion can remove candidates; any remaining single question still has five same-sign numerical options.','Live inventory may differ from captured basis 5370.']}}
(W/'evidence/post-delivery-probes.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'passed':True,'sets':{k:{'count':v['count'],'distinct_normalized_rows':v['distinct_normalized_rows'],'sign_success':v['successes']} for k,v in results.items()},'controlled_positions':report['controlled_delivered_correct_positions']}))
