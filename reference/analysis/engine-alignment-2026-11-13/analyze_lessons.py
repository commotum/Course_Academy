"""Compare the saved, source-linked lesson audit with current stopping policy.
Does not write engine or live learner data. Run from the repository root.
"""
import hashlib
import json
from collections import Counter
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / 'reference/analysis/lesson-failure-2026-11-13/evidence.json'
LABELS = {'Correct':'C','Full Credit':'C','Incorrect':'W','No Credit':'W','Partial Credit':'P'}

def terminal(sequence, majority=False):
    correct = wrong = streak = 0
    for n, answer in enumerate(sequence, 1):
        correct += answer == 'C'
        wrong += answer == 'W'
        streak = streak + 1 if answer == 'C' else 0
        if streak == 2 and (not majority or correct > wrong):
            return n, 'passed'
        if wrong == 3:
            return n, 'failed'
        if n == 5:
            return n, 'passed'
    return None, 'continue'

def main():
    d = json.loads(SOURCE.read_text())
    findings = []
    candidate_conflicts = []
    populations = {}
    for family, records in [('accounts',d['lessons']),('historical',d['historical_lessons']),('pilot',d['standalone_history'])]:
        patterns = Counter()
        for r in records:
            for index,g in enumerate(r['groups']):
                seq = g['sequence']
                if not seq or set(seq)-set('CW') or g['kp'] is None:
                    continue
                patterns[seq] += 1
                actual_terminal = 'failed' if r['outcome']=='failed' and index==len(r['groups'])-1 else ('passed' if index < len(r['groups'])-1 or r['outcome']=='passed' else 'unknown')
                local = terminal(seq)
                candidate = terminal(seq,majority=True)
                detail = dict(task_id=r['task_id'],source=r['source'],family=family,kp=g['kp'],sequence=seq,questions=g['questions'],observed_terminal=actual_terminal,local_terminal_question=local[0],local_terminal_state=local[1])
                if local[0] != len(seq) or actual_terminal!='unknown' and local[1]!=actual_terminal:
                    findings.append(detail)
                if candidate[0] != len(seq) or actual_terminal!='unknown' and candidate[1]!=actual_terminal:
                    candidate_conflicts.append(detail)
        populations[family]=dict(binary_kp_groups=sum(patterns.values()),patterns=dict(patterns))
    for row in findings:
        if row['family']!='accounts':
            continue
        p=ROOT/row['source']
        h=json.loads(p.read_text())
        checkpoint=json.loads(p.with_name('checkpoint.json').read_text())
        live={str(k).replace('step-q',''):v.get('grade') for k,v in checkpoint['presentations'].items()}
        qs={str(q.get('math_academy_id') or q.get('dom_id')).replace('question-','').replace('q-',''):q for q in h['questions']}
        checks=[]
        for compact in row['questions']:
            q=qs[compact['id']]
            soup=BeautifulSoup(q.get('raw_html') or q.get('html') or '', 'html.parser')
            span=soup.select_one('.answerResult')
            html=span.get_text(' ',strip=True) if span else None
            check=dict(id=compact['id'],history=q.get('result'),live=live.get(compact['id']),source_html=html)
            check['agrees']=len({LABELS.get(v,v) for k,v in check.items() if k!='id' and v is not None})==1
            checks.append(check)
        row['grade_crosschecks']=checks
        assert all(x['agrees'] for x in checks),row['task_id']
    summary=dict(input=str(SOURCE.relative_to(ROOT)),input_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),populations=populations,
        mismatch_count=len(findings),account_mismatch_count=sum(r['family']=='accounts' for r in findings),
        mismatch_sequences=dict(Counter(r['sequence'] for r in findings)),
        candidate='Observed-equivalent candidate: require both final CC and more correct than incorrect for early advancement; third W fails; otherwise cap at five.',
        candidate_counterexamples=len(candidate_conflicts),
        boundary='The candidate fits the observed binary sequences but does not identify the private algorithm. Partial credit and unfinished groups are excluded. Do not infer success from generic Completed history labels.')
    output=Path(__file__).with_name('lessons.json')
    output.write_text(json.dumps(dict(summary=summary,mismatches=findings,candidate_counterexamples=candidate_conflicts),indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
