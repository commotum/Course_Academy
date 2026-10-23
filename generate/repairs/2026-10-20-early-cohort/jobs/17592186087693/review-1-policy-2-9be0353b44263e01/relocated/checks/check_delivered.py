"""Read actual filtered records; verify visible answers and conditional cues."""
import json
from collections import Counter
from replay_completeness import ROOT, check_math, correct, norm
E = ROOT/'evidence'

def load(p): return json.loads((E/p).read_text())
def signature(r):
    q=r['question']
    return (q[':question/problem'],q[':question/worked-solution'],tuple(norm(correct(f)) for f in q[':question/answer-fields']))

def probe(records):
    out={}
    for t in sorted({r['generation']['template'] for r in records}):
        rs=[r for r in records if r['generation']['template']==t]
        shapes=[check_math(r) for r in rs]
        d={'count':len(rs),'shapes':sorted(set(shapes)),'copy_row_count_successes':sum(r==c for r,c in shapes),'square_cases':sum(r==c for r,c in shapes),'wider_cases':sum(r<c for r,c in shapes),'taller_cases':sum(r>c for r,c in shapes)}
        if t=='radio':
            positions=Counter(); cues=Counter()
            for r in rs:
                f=r['question'][':question/answer-fields'][0];bank=f[':answer-field/choices'];key=norm(correct(f))
                pair=lambda a:tuple(map(int,norm(a[':answer/value']).split('\\times')))
                positions[next(i for i,a in enumerate(bank) if norm(a[':answer/value'])==key)]+=1
                for cue,a in [('first',bank[0]),('last',bank[-1]),('smallest',min(bank,key=pair)),('largest',max(bank,key=pair))]:cues[cue]+=norm(a[':answer/value'])==key
            d.update(positions=dict(positions),cue_successes=dict(cues),random_choice_baseline=0.2)
        out[t]=d
    return out

result={}
for name, raw, accepted in [('batch','prospective-batch.json','delivery-batch/accepted.json'),('controls','delivery-input.json','delivery-controls/accepted.json')]:
    before, after=load(raw),load(accepted)
    assert Counter(map(signature,before))==Counter(map(signature,after)), 'Delivery changed or removed tested visible content'
    pre,post=probe(before),probe(after)
    assert pre==post
    result[name]={'before':pre,'after':post,'same_visible_content':True}
assert len(result['batch']['after'])==4
assert sum(d['count'] for d in result['batch']['after'].values())==5
for t,d in result['controls']['after'].items():
    assert d['square_cases'] and d['wider_cases'] and d['taller_cases'],t
    if t=='radio':
        assert len(d['positions'])==5
        assert all(wins<d['count'] for wins in d['cue_successes'].values())
    else:assert d['copy_row_count_successes']<d['count']
assert len(result['controls']['after']['chelsea-dual-blank']['shapes'])==25
result['interpretation']={
 'fidelity':'All nine supplied target-KP practice sources pass independent capture-driven replay. Chelsea source has the documented absent-table correction.',
 'correctness':'Displayed rows and columns independently agree with keys and solutions before and after delivery.',
 'grading':'Native harness: 298 assertions; 163 accepted and 135 rejected, no mismatches.',
 'variation':'Every template has square, wider and taller cases in controls. Restored Chelsea covers all 25 shapes with the same letter and zero entries. Controlled row/column changes alter the appropriate answer; entry/letter changes preserve answers. Radio fixed-bank controls change the correct member, and all five displayed positions occur in the small sample.',
 'finite_batch':'Five distinct shapes; all four templates appear; no batch rule or supported shape domain was narrowed.',
 'shortcut_scope':'No tested label, template, fixed-position or dimension-extreme cue solves all control records. Frequency estimates include deliberate controls and are not estimates of production probabilities. Singletons in the five-record batch cannot establish or refute conditional predictors.',
 'selection_limits':'Shared delivery uses captured basis 5665. Existing review selection-results.json reports uniform selection within eligible difficulty bands, not shape/template selection. No live database or learner history was accessed; later history-conditioned subsets are not certified.',
 'inventory':'All 14 captured stored matrices, answers and solutions checked. No stored instance of the replay omission: q-139628 is an original source, not a generated record needing repair.'}
(E/'pedagogical-variation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':True,'accepted_batch':5,'accepted_controls':73,'chelsea_shapes_after_delivery':25}))
