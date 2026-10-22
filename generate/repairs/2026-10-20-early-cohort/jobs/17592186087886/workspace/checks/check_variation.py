"""Audit positions and content-changing witnesses before/after actual delivery filtering."""
import json
from pathlib import Path
import re
import sys
from collections import Counter,defaultdict
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from math_reader import rate,prompt_rhs,x,y,v
import sympy as sp

def audit(records):
    groups=defaultdict(list)
    for r in records:groups[r['generation']['template']].append(r)
    result={}
    for t,rows in groups.items():
        positions=Counter();length_probes={'shortest':0,'longest':0};op_counts=Counter();rates=set();params=set()
        for r in rows:
            q=r['question'];f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];correct=next(i for i,a in enumerate(choices) if a[':answer/id']==f[':answer-field/correct'][1]);positions[correct]+=1
            # Remove TeX presentation commands so these are math-text size cues, not UUIDs.
            sizes=[len(re.sub(r'\\(?:left|right|operatorname)|[{}\s]|\u2061','',a[':answer/value'])) for a in choices]
            for name,fn in [('shortest',min),('longest',max)]:
                target=fn(sizes)
                if sizes.count(target)==1 and sizes[correct]==target:length_probes[name]+=1
            lhs,rhs=choices[correct][':answer/value'].split('=')
            actual=rate(choices[correct][':answer/value']);expected=(prompt_rhs(q[':question/problem']).subs(y,v*x)-v)/x
            assert sp.trigsimp(sp.cancel(actual-expected))==0
            rates.add(sp.srepr(sp.cancel(actual)));params.add(r['generation']['parameters']['k']);op_counts[len(choices)]+=1
        assert len(rates)==len(rows),f'No meaningful numerical variation in {t}'
        assert len(positions)>1,f'Fixed correct-choice position within {t}'
        result[t]={'records':len(rows),'semantic_rates':len(rates),'k_values':sorted(params),'correct_positions':dict(sorted(positions.items())),'best_fixed_position_hits':max(positions.values()),'fixed_position_baseline':0.2,'choice_counts':dict(op_counts),'unique_extreme_length_hits':length_probes,'length_probe_trials':len(rows)}
    return result

def main():
    raw=json.loads((ROOT/'evidence/records.json').read_text());accepted=json.loads((ROOT/'evidence/delivery/accepted.json').read_text())
    report={'before_delivery':audit(raw),'after_delivery':audit(accepted),'before_semantic_instances':len(raw),'after_semantic_instances':len(accepted),'generator_rejection':'Explicit finite 48-task domain; no rejection sampler. Outside-domain values and unsupported bands are tested by validate_math.py. Batch samples without replacement.', 'selection_limits':'Actual shared publisher normalization, validation, difficulty and inventory/batch deduplication tested. Native question_selection.rs groups by rated band and draws within band for configured policies; unconfigured legacy policies use first candidate. Live history/reservations and policy state are unavailable and not simulated. All generated questions are easy; selection has no template-specific band distinction.', 'source_bank_limits':'Retained source-owned distractors have deliberate mathematical shape differences. A recognizer for reciprocal(F(v)-v) performs the assessed transformation, even when cancellation makes a short result. Numerical substitutions change every answer within each family. Length probes are reported separately; a perfect incidental cue requires repair or unsupported status.'}
    (ROOT/'evidence/pedagogical-variation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'records_before':len(raw),'records_after':len(accepted),'perfect_length_cues':[(stage,t,name) for stage in ['before_delivery','after_delivery'] for t,c in report[stage].items() for name,hits in c['unique_extreme_length_hits'].items() if hits==c['records']]}))
if __name__=='__main__':main()
