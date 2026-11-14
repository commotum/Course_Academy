"""Read-only audit of captured review stopping against the local controller.

Actual recorded grades are used, never intended answer policy. Completion text,
not earned XP or a generic Completed card, determines an explicit source result.
"""
import json
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'reference/mathacademy'
OUT = Path(__file__).with_suffix('.json')
GRADES = {'Correct': 'C', 'Full Credit': 'C', 'Incorrect': 'W', 'No Credit': 'W', 'Partial Credit': 'P'}


def load(p):
    return json.loads(p.read_bytes())


def text(c):
    return c if isinstance(c, str) else (c or {}).get('text') or (c or {}).get('source_text') or ''


def classify(t):
    if 'halted due to poor performance' in t or "didn't pass" in t:
        return 'failed'
    if "Congratulations! You've completed the review" in t:
        return 'completed_message'
    return 'unknown'


def terminal(seq):
    if not seq or set(seq)-set('CW'):
        return None
    for i in range(1, len(seq)+1):
        if i >= 3 and seq[i-2:i] == 'CC' or i == 5:
            return i
    return None


def candidate(seq):
    """Observed-fit hypothesis, not an accepted Course Academy policy."""
    if not seq or set(seq)-set('CW'):
        return None
    for i in range(1,len(seq)+1):
        prefix=seq[:i]
        if prefix.count('W')==3:
            return (i,'failed')
        if i>=3 and prefix.endswith('CC') and prefix.count('C')>prefix.count('W'):
            return (i,'completed_message')
        if i==5:
            return (i,'completed_message' if prefix.endswith('C') else 'failed')
    return None


def candidate_summary(rows):
    eligible=[r for r in rows if r['outcome']!='unknown' and r['sequence'] and not(set(r['sequence'])-set('CW'))]
    mismatches=[dict(task_id=r['task_id'],source=r['source'],sequence=r['sequence'],outcome=r['outcome'],predicted=candidate(r['sequence']))
                for r in eligible if candidate(r['sequence']) != (len(r['sequence']),r['outcome'])]
    return dict(hypothesis='At >=3 questions, early CC requires C>W. A third miss halts immediately. At five, final correct completes and final incorrect fails. This is an exploratory fit, not recovered server code or current local policy.',
                eligible_records=len(eligible),exact=len(eligible)-len(mismatches),mismatches=mismatches)


def extract(pair):
    family, p = pair
    if family == 'legacy':
        d = load(p)
        if d.get('task_type') != 'review':
            return None
        qs = [dict(id=key, result=q.get('actual_result') or (q.get('after') or {}).get('result'),
                   kp=q.get('kp_id')) for key,q in d.get('questions',{}).items()]
        messages = [dict(source=str(p.relative_to(ROOT)), text=text(d.get('completion')))]
        account = p.parent.parent.name if 'question-capture-workers' in p.parts else 'foundations'
        task_id = p.parent.name
        source = p
        title = None
        issues = []
    else:
        a = load(p)
        if a.get('kind') != 'review':
            return None
        source = p.with_name('history-content.json')
        if not source.exists():
            source = p.with_name('content.json')
        d = load(source) if source.exists() else {}
        qs = [dict(id=q.get('math_academy_id') or q.get('dom_id'), result=q.get('result') or q.get('source_grade') or q.get('grade'),
                   kp=q.get('knowledge_point'), position=q.get('sequence_position')) for q in d.get('questions',[])]
        messages = [dict(source=str(source.relative_to(ROOT)),text=text(d.get('completion')))]
        post = p.with_name('post-activity.json')
        if post.exists():
            messages.append(dict(source=str(post.relative_to(ROOT)),text=text(load(post).get('completion'))))
        account = p.parent.parent.name
        task_id = p.parent.name
        title = a.get('title')
        issues = d.get('evidence_errors', [])
        if not d:
            issues = ['missing history/content']
    seq = ''.join(GRADES.get(q['result'],'?') for q in qs)
    conclusions = {classify(m['text']) for m in messages} - {'unknown'}
    result = next(iter(conclusions)) if len(conclusions) == 1 else 'unknown'
    if len(conclusions)>1:
        issues.append('conflicting completion messages')
    stop = terminal(seq)
    row = dict(task_id=task_id,account=account,family=family,source=str(source.relative_to(ROOT)),
                title=title,sequence=seq,questions=qs,messages=messages,outcome=result,
                engine_terminal=stop,continued_after_engine_stop=stop is not None and stop<len(seq),
                source_stopped_before_engine=result!='unknown' and bool(seq) and stop is None and not(set(seq)-set('CW')),
                issues=issues)
    if family == 'modern' and (result == 'failed' or row['continued_after_engine_stop']):
        checkpoint = p.with_name('checkpoint.json')
        live = load(checkpoint).get('presentations',{}) if checkpoint.exists() else {}
        grades = {key.removeprefix('step-q'):v.get('grade') for key,v in live.items()}
        checks=[]
        for q, observed in zip(d.get('questions',[]),qs):
            soup=BeautifulSoup(q.get('raw_html') or q.get('html') or '', 'html.parser')
            span=soup.select_one('.answerResult')
            html=span.get_text(' ',strip=True) if span else None
            qid=str(observed['id']).removeprefix('question-').removeprefix('q-')
            check=dict(question_id=observed['id'],history=observed['result'],live=grades.get(qid),html=html)
            checks.append(check)
            values={GRADES.get(check[k],check[k]) for k in ['history','live','html'] if check[k] is not None}
            if len(values)>1:
                issues.append('grade mismatch: '+str(observed['id']))
        row['grade_crosschecks']=checks
    return row


def main():
    legacy = sorted((BASE/'question-capture').glob('*/state.json')) + sorted((BASE/'question-capture-workers').glob('*/*/state.json'))
    modern = sorted((BASE/'capture').glob('*/*/activity.json'))
    work = [('legacy',p) for p in legacy] + [('modern',p) for p in modern]
    rows=[]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for i,r in enumerate(pool.map(extract,work),1):
            if r: rows.append(r)
            if i%1000==0: print('Scanned',i,flush=True)
    seen={r['task_id'] for r in rows}
    assert len(rows)==len(seen),'Duplicate source task IDs need reconciliation'
    historical=[]
    for t in load(BASE/'progress-history-2026-10-04/observations.json')['tasks']:
        if t['activity-type']!='Review': continue
        p=ROOT/t['source_file']; d=load(p)
        seq=''.join(GRADES.get(q.get('result'),'?') for q in d['questions'])
        stop=terminal(seq)
        historical.append(dict(task_id=t['task-id'],source=t['source_file'],family='historical',
                               sequence=seq,engine_terminal=stop,outcome=classify(d.get('task_text','')),
                               continued_after_engine_stop=stop is not None and stop<len(seq),
                               questions=[{k:q.get(k) for k in ('id','result','ordinal','kp_title')} for q in d['questions']]))
    summary=dict(generated_at=datetime.now(timezone.utc).isoformat(),
                 scope='All legacy states and modern activity descriptors; separate personal history sample. Actual C/W grades; partial-credit P is excluded from binary stopping comparisons.',
                 local_policy='Review stops on final CC at >=3 presentations, otherwise completes successfully at five. The November 1 rule is an explicit Course Academy policy, not inferred MA pass/fail.',
                 review_records=len(rows), historical_reviews=len(historical),
                 outcomes=dict(Counter(r['outcome'] for r in rows)),
                 lengths=dict(sorted(Counter(len(r['sequence']) for r in rows).items())),
                 sequences=dict(Counter(r['sequence'] for r in rows).most_common()),
                 continued_after_engine_stop=sum(r['continued_after_engine_stop'] for r in rows),
                 stopped_before_engine=sum(r['source_stopped_before_engine'] for r in rows),
                 failures=dict(Counter(r['sequence'] for r in rows if r['outcome']=='failed')),
                 crosschecked_questions=sum(len(r.get('grade_crosschecks',[])) for r in rows),
                 evidence_issues=[dict(task_id=r['task_id'],issues=r['issues']) for r in rows if r['issues']],
                 grade_crosscheck_mismatches=[dict(task_id=r['task_id'],issues=r['issues']) for r in rows if any('grade mismatch:' in s for s in r['issues'])],
                 candidate_controller=candidate_summary(rows),
                 historical_continued_after_engine_stop=sum(r['continued_after_engine_stop'] for r in historical))
    OUT.write_text(json.dumps(dict(summary=summary,reviews=rows,historical=historical),indent=2)+'\n')
    print(json.dumps(summary,indent=2),flush=True)


if __name__=='__main__':
    main()
