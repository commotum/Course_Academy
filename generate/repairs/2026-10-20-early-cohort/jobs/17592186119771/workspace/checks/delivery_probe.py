#!/usr/bin/env python3
"""Recheck visible mathematics and incidental cues after shared delivery filtering."""
import json
from pathlib import Path
import validate as v

def main():
    before=json.loads((v.OUT/'delivery-input.json').read_text())
    after=json.loads((v.OUT/'delivery/accepted.json').read_text())
    report={'before':v.cue_report(before),'after':v.cue_report(after),
            'input_count':len(before),'accepted_count':len(after),
            'mathematics_verified':len([v.verify(r) for r in after])}
    assert len(after)==len(before)==36
    assert {v.structural(v.matrix(r['question'][':question/problem'])) for r in before}=={v.structural(v.matrix(r['question'][':question/problem'])) for r in after}
    sample=json.loads((v.OUT/'sample-delivery/accepted.json').read_text())
    assert len(sample)==5
    for r in sample: v.verify(r)
    report['requested_sample_accepted']=len(sample)
    # Read-only reproduction of select()'s within-band draw: every accepted
    # candidate is easy, so band weighting cannot distinguish orientation.
    # Probe fresh-pool draws, without pretending to know real learner history.
    import hashlib,collections
    pool=sorted(after,key=lambda r:r['question'][':question/id'])
    # Native selection sorts numeric entity IDs, unavailable prepublication.
    # Try both deterministic UUID orders to expose order-based collapse only.
    selections={}
    for ordering,candidates in (('uuid',pool),('reverse_uuid',list(reversed(pool)))):
        counts=collections.Counter()
        selected=set()
        for seed in range(64):
            digest=hashlib.sha256(f'course-academy/question-selection/v1/{seed}'.encode()).digest()
            uniform=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53)
            chosen=candidates[int(uniform*len(candidates))]
            counts[v.key(chosen['question'])]+=1
            selected.add(v.structural(v.matrix(chosen['question'][':question/problem'])))
        assert len(counts)==3
        selections[ordering]={'draws':64,'answers':dict(counts),'structural_patterns_seen':len(selected)}
    report['selection_probe']=selections
    report['selection_limits']=['Offline all-easy fresh-pool reproduction of question_selection.rs uniform within-band draw only. UUID order substitutes for unavailable future numeric entity IDs.','Real learner history, current prefix, policy weights, future database identities and live inventory were not accessed. No live selection guarantee is claimed.']
    v.save('postdelivery-variation.json',report)
    print(json.dumps({k:report[k] for k in ('input_count','accepted_count','mathematics_verified','requested_sample_accepted','selection_probe')}))

if __name__=='__main__':main()
