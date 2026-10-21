#!/usr/bin/env python3
"""Measure delivered shortcuts, bank counterfactuals and read-only learner selection."""
import sys
sys.dont_write_bytecode=True
import collections, copy, hashlib, json, pathlib, re
import review_tests as t
ROOT=t.ROOT
def measure(records, name):
    tests=[]
    for r in records:
        picks,rule=t.shortcut(r)
        tests.append({'question_id':r['question'][':question/id'],'template':r['generation']['template'],'parameters':r['generation']['parameters'],'cue':rule,'picked_positions':[i+1 for i in picks],'correct_position':t.keypos(r)+1,'success':picks==[t.keypos(r)]})
    groups=[]
    for sid in sorted({r['template'] for r in tests}):
        sub=[r for r in tests if r['template']==sid]
        groups.append({'subgroup':sid,'correct':sum(r['success'] for r in sub),'total':len(sub),'cue':sub[0]['cue']})
    return {'stage':name,'correct':sum(r['success'] for r in tests),'total':len(tests),'baseline':0.2,'groups':groups,'cases':tests}
def selection(candidates, seed, distribution):
    # Exact algorithm from engine/rust/question_selection.rs: select(), lines 125-197.
    bands=[[],[],[]];unrated=[]
    for entity,level in sorted(set(candidates)):
        (bands[['easy','moderate','hard'].index(level)] if level else unrated).append(entity)
    dig=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
    uniform=lambda offset:(int.from_bytes(dig[offset:offset+8],'big')>>11)/(1<<53)
    total=sum(w for i,w in enumerate(distribution) if bands[i]);pool=unrated
    if total>0:
        draw=uniform(0)*total
        for i,w in enumerate(distribution):
            if not bands[i] or not w:continue
            pool=bands[i]
            if draw<w:break
            draw-=w
    return pool[int(uniform(8)*len(pool))] if pool else None
def main():
    stages=[]
    for name in ['easy-records.json','runner-batch.json','delivery-easy/accepted.json','delivery-batch/accepted.json']:
        stages.append(measure(json.load(open(ROOT/name)),name))
    t.save('shortcut-results.json',{'strategy':'Read answer bank only. Matrix banks: choose the unique all-zero-bottom-row option with modal top row. Affine banks: choose majority intercept/slope signs and modal coefficient magnitudes, ignoring isolated points. No original matrix, stored key, UUID, option order or generation metadata is used.','results':stages,'interpretation':'Bottom-row consistency alone is a valid mathematical simplification; using answer-bank frequency to choose the numerical top row or affine signs is an incidental cue. There is no mathematical implication from distractor repetition to correctness. UI choice shuffling leaves this cue unchanged.'})
    selected={};selectionreports=[]
    for name in ['delivery-easy/accepted.json','delivery-batch/accepted.json']:
        rs=json.load(open(ROOT/name));mapping={100000+i:r for i,r in enumerate(rs)}
        candidates=[(i,'easy') for i in mapping];traces=[]
        for j in range(100):
            seed=f'review-independent-task-{71923+j}/kp-17592186105745/slot-0'
            entity=selection(candidates,seed,[1.,0.,0.]);r=mapping[entity];picks,rule=t.shortcut(r)
            traces.append({'seed':seed,'stand_in_entity_id':entity,'question_id':r['question'][':question/id'],'template':r['generation']['template'],'shortcut_success':picks==[t.keypos(r)]})
        # Freshness: removing any previously seen records cannot repair a bank-local cue.
        no_repeat=[];seen=set()
        for j in range(len(candidates)):
            entity=selection([c for c in candidates if c[0] not in seen],f'review-71923/slot-{j}',[1.,0.,0.]);seen.add(entity);no_repeat.append(mapping[entity])
        t.save('selection-'+name.split('/')[0]+'-records.json',no_repeat)
        selectionreports.append({'input':name,'stand_in_entity_ids':True,'weights':[1,0,0],'trials':traces,'freshness_sequence_ids':[r['question'][':question/id'] for r in no_repeat],'all_shortcuts_succeed':all(z['shortcut_success'] for z in traces)})
    t.save('selection-results.json',{'implementation':'Faithful read-only reproduction of engine/rust/question_selection.rs select; candidates sorted by entity ID, difficulty band weighted draw, then SHA256 second draw within band. learning.rs lines 598-622 excludes seen and invalid candidates before select.','cases':selectionreports,'limitations':['No learner history or active policy snapshot supplied; exact production next-question probabilities are unavailable. Tested easy-only positive-weight pool and a no-repeat sequence using explicit stand-in new entity IDs.','Selection can remove or reorder items but cannot cure an item-local bank cue: all surviving easy records have it, regardless of future entity IDs, ordering or histories.','Original inventory source questions are captured originals, not generated records; no generated records found in captured bank.']})
    # Check the visible actual-UI DOM order, rather than assuming authored order is served.
    rendered=json.load(open(ROOT/'render/input.json'));dom=[]
    for i,r in enumerate(rendered):
        html=(ROOT/'render'/f'question-{i+1:03d}.html').read_text()
        ids=re.findall(r'<input[^>]*type="radio"[^>]*value="([^"]+)"',html)
        f=r['question'][':question/answer-fields'][0];bank=f[':answer-field/choices'];lookup={a[':answer/id']:a for a in bank}
        # Only field radios; each ID must occur exactly once.
        ids=[j for j in ids if j in lookup]
        rr=copy.deepcopy(r)
        if len(ids)==5:rr['question'][':question/answer-fields'][0][':answer-field/choices']=[lookup[j] for j in ids]
        picks,rule=t.shortcut(rr)
        dom.append({'render_index':i+1,'template':r['generation']['template'],'radio_ids':ids,'authored_order_changed':ids!=[a[':answer/id'] for a in bank],'shortcut_unique':len(picks)==1,'shortcut_correct':picks==[t.keypos(rr)],'radio_count':len(ids)})
    t.save('ui-shortcut-results.json',{'cases':dom,'result':'Actual rendered radio ordering read from HTML; bank-only cue re-evaluated after UI shuffle, independent of visible correct markers.'})
    # Identify actual before/after submissions for the relevant affine pair.
    recs=json.load(open(ROOT/'counterfactual-records.json'));a,b=recs[:2]
    av=a['question'][':question/answer-fields'][0][':answer-field/choices'][t.keypos(a)][':answer/value']
    bv=b['question'][':question/answer-fields'][0][':answer-field/choices'][t.keypos(b)][':answer/value']
    controls=[]
    for r,old,new in [(a,bv,av),(b,av,bv)]:
        bank=r['question'][':question/answer-fields'][0][':answer-field/choices']
        controls.append({'label':'controlled RHS reversal '+str(r['generation']['parameters']), 'record':r,'checks':[{'submitted_answer_id':next(c[':answer/id'] for c in bank if all(t.S.simplify(u-w)==0 for u,w in zip(t.family(c[':answer/value']),t.family(v)))),'expected':outcome,'purpose':purpose} for v,outcome,purpose in [(new,'accepted','new derived solution accepted'),(old,'rejected','other counterfactual solution rejected in this prompt')]]})
    t.save('counterfactual-grader-input.json',controls)
    t.save('scope-results.json',{'source_families':['easy normalized REF selection','easy solution from given REF','moderate reduction plus solution'],'observed':'All sampled items remain rank-one consistent 2x2 systems, preserve the appropriate five-choice radio response and same reasoning stages. Scaling range 1..4 changes only small exact constants; fractions occur in original q-73743. No unsupported operator, free-entry requirement, target or prerequisite introduced.','limitations':'This scope pass does not justify suppressing source profiles or fixed bank construction.'})
    (ROOT/'session-state.md').write_text('Completed source replay (12 exact banks; 4 unsupported), math (65 passing), packaging/dependencies/relocation, read-only filtering (25→20 easy; batch 5→3), bank-only shortcut measurements, selection reproduction, inventory audit and 13 actual UI renders. Final native controlled grader and extra irrelevant-row-pair renders, visual inspection and final evidence audit remain.\n')
    print(json.dumps({'shortcut_stage_totals':[(z['stage'],z['correct'],z['total']) for z in stages],'ui_cases':len(dom),'dom_radio_counts':collections.Counter(z['radio_count'] for z in dom)}))
if __name__=='__main__':main()
