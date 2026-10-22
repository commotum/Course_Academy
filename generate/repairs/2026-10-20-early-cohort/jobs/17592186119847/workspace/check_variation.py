"""Measure visible cues before/after shared delivery filtering."""
import collections,json
from pathlib import Path
from check_repair import E,inspect,save

def summarize(records):
    groups=collections.defaultdict(list)
    for r in records:groups[r['generation']['bank_profile']].append(inspect(r))
    out={}
    for profile,facts in groups.items():
        counts={key:dict(collections.Counter(str(f[key]) for f in facts)) for key in ['position','numerical_order','rank','rows','columns','count']}
        for cue in ['position','numerical_order','rank']:
            assert len(counts[cue])>1,(profile,cue,counts[cue])
        out[profile]={'records':len(facts),'semantic_tasks':len({f['semantic'] for f in facts}),'cues':counts,'best_fixed_position_successes':max(counts['position'].values()),'best_fixed_numerical_order_successes':max(counts['numerical_order'].values()),'chance_position_baseline':0.2}
    return out

def main():
    raw=json.loads((E/'probe-records.json').read_text());accepted=[]
    for level in ['easy','moderate']:accepted+=json.loads((E/f'delivery-{level}/accepted.json').read_text())
    before=summarize(raw);after=summarize(accepted);assert set(before)==set(after)
    save('pedagogical-variation.json',{'before_delivery':before,'after_delivery':after,'claims':{'fidelity':'11 complete source banks matched; q-34825 missing key/solution independently repaired','correctness':'110 distinct semantic task records independently read and checked plus replay and controlled cases','grading':'Native check-engine on source, counterfactual and boundary records: all authored options tested','variation':'No fixed position, numerical ordering, rank, or bank profile alone determines the tested keys. Count reading for easy and subtraction for moderate remain intended operations.'},'limitations':['Signed distractor distances are authored extensions; evidence does not establish psychological misconceptions.','Numerical-order baseline is constrained by nonnegative choices and repeated distances; it is not uniformly 1/5.','Actual publisher delivery filtering does not deduplicate the conservative semantic identity used by this generator: report semantic tasks separately from records.','question_selection.rs selects fresh eligible records by difficulty weights, then within band using a seeded draw; it does not inspect bank profile or key. No live learner histories or policies were queried.','Unconfigured selection uses the first eligible entity; per-learner received variation is therefore not established.','Finite domains intentionally repeat the rank definition and one-subtraction method; these are not evidence of broad rank mastery.']})
    rs=[]
    # Representative accepted easy boundary/normal and moderate subtraction.
    for level in ['easy','moderate']:
        group=json.loads((E/f'delivery-{level}/accepted.json').read_text())
        rs += [min(group,key=lambda r:inspect(r)['rank']),max(group,key=lambda r:inspect(r)['rank'])]
    save('render-records.json',rs)
    cases=[]
    for r in rs:
        fact=inspect(r);f=r['question'][':question/answer-fields'][0]
        cases.append({'label':'after-delivery-'+r['question'][':question/id'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if int(a[':answer/value'])==fact['rank'] else 'rejected','purpose':'Verify normalized records retain native grading'} for a in f[':answer-field/choices']]})
    save('delivery-grader-input.json',cases)
    print(json.dumps({'status':'pass','raw_records':len(raw),'accepted_records':len(accepted),'profiles':len(after),'semantic_easy':len({inspect(r)['semantic'] for r in accepted if r['question'][':question/difficulty'].endswith('/easy')}),'semantic_moderate':len({inspect(r)['semantic'] for r in accepted if r['question'][':question/difficulty'].endswith('/moderate')})}))
if __name__=='__main__':main()
