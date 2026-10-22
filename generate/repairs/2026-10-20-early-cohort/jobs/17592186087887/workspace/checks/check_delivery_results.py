#!/usr/bin/env python3
"""Check visible math, shortcut probes and controlled roles after actual delivery."""
import collections
import hashlib
import json
import pathlib
import sys
sys.dont_write_bytecode=True
W=pathlib.Path(__file__).resolve().parents[1];E=W/'evidence'
sys.path.insert(0,str(W/'checks'))
from check_shortcuts import visible,field,probes

def load(p):return json.loads(p.read_text())
def save(n,v):(E/n).write_text(json.dumps(v,indent=2)+'\n')

def fnv(s):
    h=2166136261
    for c in s:h=((h^ord(c))*16777619)&0xffffffff
    return h

def main():
    stages={};delivered=[]
    for name,input_name in [('census','census-records'),('controlled','controlled-records'),('batch','current-batch')]:
        before=load(E/(input_name+'.json'));after=load(E/('delivery-'+name)/'accepted.json')
        assert len(before)==len(after)
        # Publisher may replace owned UUIDs; compare mathematics independently of IDs.
        def sig(r):
            t,a,cs=visible(r)
            return t,a,tuple(sorted(cs)),r['question'][':question/problem'],r['question'][':question/worked-solution']
        assert sorted(map(sig,before))==sorted(map(sig,after))
        rows=probes(after)
        assert all(z['attempts']==0 for z in rows if z['strategy']=='retained review predictor')
        stages[name]={'input':len(before),'accepted':len(after),'math_preserved':True,'probes':rows,'coverage':{t:{'prompt_coefficients':sorted({visible(r)[1] for r in after if visible(r)[0]==t}),'keyed_positions':sorted({visible(r)[2].index(visible(r)[1]) for r in after if visible(r)[0]==t})} for t in ('cube_root','affine','linear_log')}}
        if name=='controlled':
            for t in ('cube_root','affine','linear_log'):
                rs=[r for r in after if visible(r)[0]==t]
                assert len(rs)==5
                assert len({tuple(sorted(visible(r)[2])) for r in rs})==1
                assert len({visible(r)[1] for r in rs})==5
                for z in rows:
                    if z['family']==t and z['strategy'] not in ('retained review predictor','smallest UUID','largest UUID'):
                        assert z['correct']==1,z
        if name in ('controlled','batch'):delivered.extend(after)
    # Actual UI FNV sorting; item/field database entities are unavailable before publication.
    # Test position cues with three fixed hypothetical item IDs, clearly conditional.
    positions=[]
    census=load(E/'delivery-census/accepted.json')
    for item_id in ('offline-preview', '1', '17592186090000'):
        for t in ('cube_root','affine','linear_log'):
            counts=collections.Counter()
            for r in census:
                if visible(r)[0]!=t:continue
                f=field(r);fid=f[':answer-field/id'];choices=f[':answer-field/choices']
                ordered=sorted(choices,key=lambda a:fnv(f"{item_id}:{fid}:{a[':answer/id']}"))
                index=next(i for i,a in enumerate(ordered) if a[':answer/id']==f[':answer-field/correct'][1])
                counts[index]+=1
            assert max(counts.values())<18
            positions.append({'family':t,'assumed_item_id':item_id,'correct_position_counts':dict(counts),'n':18})
    cases=[]
    for i,r in enumerate(delivered):
        f=field(r);key=f[':answer-field/correct'][1]
        cases.append({'label':f'delivery survivor {i}','record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key else 'rejected','purpose':'Normalized ownership and keyed identity preserve independently verified solution.'} for a in f[':answer-field/choices']]})
    save('grader-delivered-input.json',cases)
    inv=load(W.parent/'source/inventory.json')
    easy=[q for q in inv['questions'] if q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/easy']
    ids=sorted(q[':db/id'] for q in easy)
    def select(seed,pool):
        digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
        return pool[int(((int.from_bytes(digest[8:16],'big')>>11)/(1<<53))*len(pool))]
    sequential=[];remaining=ids[:]
    while remaining:
        selected=select('repair-readonly-'+str(len(sequential)),remaining)
        remaining.remove(selected);sequential.append(selected)
    assert set(sequential)==set(ids)
    save('selection.json',{'reviewed_code':'engine/rust/question_selection.rs::select and seen_before_task; ui/learning.js::choiceOrder','captured_easy_entities':ids,'sequential_without_replacement':sequential,'rule':'Positive easy weight selects uniformly within the sorted/deduplicated fresh easy entity IDs using the second SHA-256 draw. There is no family or bank-content rejection. Seen history/current prefix are excluded; unconfigured policy chooses first entity.','limits':'Actual learner history, configured weights, future database entity IDs and task-item IDs are absent. No live selection frequencies or future exact UI positions asserted. Conditional on a positively weighted easy band, delivered records have no bank-based exclusion. Inventory contains legacy affected entries that this author did not edit.','conditional_ui_position_probes':positions})
    save('post-delivery-variation.json',{'passed':True,'stages':stages,'controlled_conclusion':'Same choice mathematics supports all five different prompt coefficients in every affected family after real delivery filtering. Fixed-bank rank/shape/string/author-position probes score 1/5. UUID probes are recorded separately; no perfect rule observed.','rejection':'Easy generator derives valid nonzero parameters directly; no rejection/resampling or bank-profile fallback. Independent normal draws may repeat, and actual delivery deduplicates content.','semantic_domain':54,'semantic_count_definition':'Three ODE families times 18 signed nonzero coefficients; bank or seed changes are not counted as new ODE instances.','sampler_support':'Each of 18 bank windows has positive sampling probability; target is independently uniform among its five coefficients. Every a occurs in five windows, so the full signed domain has equal marginal probability. Within a fixed visible bank, each candidate is equally eligible to be correct.'})
    print(json.dumps({'passed':True,'stages':{k:(v['input'],v['accepted']) for k,v in stages.items()},'native_delivered_responses':len(cases)*5}))
if __name__=='__main__':main()
