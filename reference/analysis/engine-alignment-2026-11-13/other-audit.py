"""Read-only comparison of observed lesson awards and partial-credit capability.
Reuses the reproducible lesson-failure audit's order/grade projection, retaining
original capture paths. No source capture, engine, or learner data is changed.
"""
import json,re
from fractions import Fraction
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).parent
SOURCE=ROOT/'reference/analysis/lesson-failure-2026-11-13/evidence.json'

def award(text):
    m=re.search(r"awarded all of the task's (\d+) XP, plus a bonus of (\d+) XP",text)
    if m:return int(m[1])+int(m[2]),int(m[1])
    m=re.search(r"awarded (\d+) of the task's (\d+) XP",text)
    if m:return int(m[1]),int(m[2])
    m=re.search(r'(-?\d+)\s*/\s*(\d+)\s*XP',text)
    if m:return int(m[1]),int(m[2])
    return None

def predicted(base,c,n):
    p=Fraction(c,n)
    if p<Fraction(1,2):return -1
    value=Fraction(5,4)*base if c==n else base*min(1,Fraction(3,2)*p-Fraction(3,10))
    return (value+Fraction(1,2)).__floor__()

def main():
    audit=json.loads(SOURCE.read_text());rows=[];excluded=[];partial=[]
    for r in audit['lessons']:
        for i,g in enumerate(r['groups']):
            if 'P' in g['sequence']:
                partial.append(dict(task_id=r['task_id'],source=r['source'],kp=g['kp'],sequence=g['sequence'],questions=g['questions'],lesson_outcome=r['outcome'],advanced_to_later_kp=i+1<len(r['groups'])))
        seq=''.join(g['sequence'] for g in r['groups'])
        if not seq or set(seq)-set('CW'):
            excluded.append(dict(task_id=r['task_id'],reason='empty or nonbinary outcomes'));continue
        awards=[]
        for e in r['completion_evidence']:
            found=award(e['text'])
            if found:awards.append((found,e['source'],e['text']))
        # Post-activity has the explicitly displayed numerator/denominator for
        # no-XP and penalty outcomes; do not infer zero from a missing value.
        if not awards:
            post=(ROOT/r['source']).with_name('post-activity.json')
            if post.exists():
                c=json.loads(post.read_bytes()).get('completion')or{}
                found=award(c.get('source_text',''))
                if found:
                    assert found==(c.get('earned_xp'),c.get('base_xp')),(r['task_id'],found,c)
                    awards.append((found,str(post.relative_to(ROOT)),c.get('source_text','')+'\n'+c.get('text','')))
        if not awards:
            excluded.append(dict(task_id=r['task_id'],reason='no explicit award and base'));continue
        assert len({x[0] for x in awards})==1,r['task_id']
        (actual,base),ap,at=awards[0]
        c,n=seq.count('C'),len(seq);pred=predicted(base,c,n)
        rows.append(dict(task_id=r['task_id'],source=r['source'],outcome=r['outcome'],kp_sequences=[g['sequence'] for g in r['groups']],correct=c,total=n,base=base,awarded=actual,engine_prediction=pred,error=pred-actual,award_source=ap,award_text=at))
    buckets=defaultdict(list)
    for r in rows:buckets[(r['outcome'],r['base'],r['correct'],r['total'])].append(r)
    conflicts=[dict(inputs=dict(zip(['outcome','base','correct','total'],k)),examples=v) for k,v in buckets.items() if len({r['awarded'] for r in v})>1]
    summary=dict(lesson_projection=str(SOURCE.relative_to(ROOT)),qualified=len(rows),excluded=len(excluded),by_outcome={o:dict(count=sum(r['outcome']==o for r in rows),mismatches=sum(r['outcome']==o and r['error']!=0 for r in rows)) for o in sorted({r['outcome'] for r in rows})},partial_credit_kps=len(partial),partial_credit_patterns=dict(Counter(r['sequence'] for r in partial)),partial_credit_lesson_outcomes=dict(Counter(r['lesson_outcome'] for r in partial)),same_input_conflict_groups=len(conflicts),engine_policy='Accepted local approximation, explicitly adopted from frozen 168-task fit. Counterexamples disprove MA equivalence; they do not independently authorize a new XP policy.',partial_credit_policy='Binary all-fields correctness was explicitly proposed for Course Academy; staged/partial-credit capture behavior is a capability gap, not a recovered numeric credit rule.')
    proof_path=ROOT/'reference/mathacademy/question-capture-workers/differential/14040950/state.json'
    proof= json.loads(proof_path.read_bytes())['questions']['q-334064']
    proof_example=dict(source=str(proof_path.relative_to(ROOT)),question='q-334064',actual_result=proof['actual_result'],
                       stages=[{k:v for k,v in step.items() if k in ['submitted_keys','outcome']} for step in proof['proof_stages']],
                       final_field_results=[dict(key=f['key'],result=f.get('source_result')) for f in proof['after']['fields']],
                       interpretation='The final answer has all fields correct after a rejected stage was corrected. Partial Credit retains earlier error history; it does not mean an unfinished partial answer simply counted as fully correct.')
    out=dict(summary=summary,xp_mismatches=[r for r in rows if r['error']],same_input_conflicts=conflicts,partial_credit_kps=partial,
             staged_retry_example=proof_example,excluded=excluded,
             engine_sources=['engine/rust/activities.rs:169','engine/rust/learning.rs:1888','engine/rust/learning.rs:2025','schema/learner/2-2-learner-task-item.edn:32'],
             policy_sources=['reference/xp-docs/earned-xp-formula-report.md:5','reference/answer-grading-proposal.md:66'])
    (HERE/'other-evidence.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
