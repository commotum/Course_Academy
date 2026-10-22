"""Executable regression for 6900891930e4bdc756fa; no runtime mutations.

Replays the exact reviewed candidate prefix through the current sampler, then
checks ordinary seeded batches before and after the actual delivery filter.
Truth and cue groups come from visible matrices, never generation rank metadata.
"""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

from validate_content import ROOT, JOB, REPO, g, inspect, visible_bank, fidelity

E = ROOT/'evidence/repair-2'

def save(name, value):
    (E/name).write_text(json.dumps(value, indent=2)+'\n')

def audit(records):
    groups = defaultdict(list)
    for rec in records:
        w, _ = inspect(rec)
        bank = visible_bank(rec['question'])
        excluded = tuple(k for k, m in sorted(bank.items())
                         if min(len(m), len(m[0])) < w['target'])
        # Three-matrix source layouts differ in visible coefficients/zero masks;
        # source profile is an additional condition, not a substitute for shapes.
        key = (rec['generation']['source_id'], w['target'],
               tuple(sorted((len(m), len(m[0])) for m in bank.values())),
               excluded, w['field_count'], rec['generation']['choice_profile'])
        groups[key].append((rec, w, sorted(set(bank)-set(excluded))))
    report = []; failures = []
    for key, rows in groups.items():
        truths = [set(w['truth']) for _, w, _ in rows]
        forced = [{'label': k, 'qualifies': k in truths[0]}
                  for k in rows[0][2] if len({k in t for t in truths}) == 1]
        positions = Counter(tuple(w['positions']) for _, w, _ in rows)
        outcomes = Counter(tuple(w['truth']) for _, w, _ in rows)
        row = {'group': str(key), 'count': len(rows),
               'eligible': rows[0][2], 'forced_eligible_roles': forced,
               'outcomes': {','.join(k) or 'None': v for k,v in outcomes.items()},
               'correct_positions': {str(k):v for k,v in positions.items()},
               'correct_counts': sorted({len(t) for t in truths}),
               'modal_complete_response_successes': max(outcomes.values()),
               'singleton': len(rows)==1}
        report.append(row)
        if len(rows)>1 and (forced or len(positions)==1): failures.append(row)
    return {'passed': not failures, 'records': len(records),
            'groups': report, 'failures': failures,
            'singleton_limit': 'Singleton groups do not establish conditional variation.'}

def delivery(name, records):
    save(name+'.json', records)
    command = [sys.executable, '-B', str(REPO/'generate/pipeline/check_delivery.py'),
               '--input', str(E/(name+'.json')), '--source', str(JOB/'source/source.json'),
               '--inventory', str(JOB/'source/inventory.json'), '--difficulty', 'easy',
               '--output', str(E/(name+'-delivery')), '--math-root', '/media/jake/SSD/EDB/math']
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode==0, result.stdout+result.stderr
    accepted = json.loads((E/(name+'-delivery')/'accepted.json').read_text())
    before, after = audit(records), audit(accepted)
    assert before['passed'] and after['passed'], (name, before, after)
    assert len(accepted)==len(records), 'Captured inventory removed a decision case'
    return accepted, {'command': command, 'before': before, 'after': after,
                      'delivery': json.loads((E/(name+'-delivery')/'delivery.json').read_text())}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--input', type=Path)
    parser.add_argument('--report', type=Path)
    args=parser.parse_args()
    if args.input:
        report=audit(json.loads(args.input.read_text()))
        if args.report:args.report.write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({'passed':report['passed'], 'failures':len(report['failures'])}))
        raise SystemExit(0 if report['passed'] else 1)

    E.mkdir(exist_ok=True)
    old=json.loads((E/'previous-batch.json').read_text())
    old_audit=audit(old)
    assert not old_audit['passed'], 'Negative control lost the reported failure'
    save('previous-batch-audit.json', old_audit)
    catalog=g.catalog();live={r['question'][':question/id']:r for r in catalog}
    old_ids=[r['question'][':question/id'] for r in old]
    # Preserve source/identity evidence, rather than silently replacing the old
    # counterexample with a new question. The unchanged catalog reproduces it.
    assert all(live[r['question'][':question/id']]==r for r in old)
    def replay_shuffle(_rng, rows):
        indexed={r['question'][':question/id']:r for r in rows}
        rows[:]=[indexed[k] for k in old_ids]+[r for r in rows if r['question'][':question/id'] not in old_ids]
    with patch.object(g.random.Random, 'shuffle', replay_shuffle):
        repaired=g.batch('easy',5,0)
    # Non-vacuous: same repeated subgroup remains; C-only must defeat A-always.
    affected=[r for r in repaired if r['generation']['source_id']=='q-139965']
    assert len(affected)==2
    assert {tuple(inspect(r)[0]['truth']) for r in affected}=={('A',),('C',)}
    assert all('B' not in inspect(r)[0]['truth'] for r in affected)
    accepted, replay_report=delivery('replayed-prefix-repaired',repaired)

    # Targeted sampler controls; exercise size boundaries and complete semantic
    # coverage without running a large unrelated seed sweep.
    sampler=[]
    capacity=len({r['generation']['mathematical_fingerprint'] for r in catalog})
    for seed,count in [(0,5),(7,5),(119848,5),(7,2),(7,3),(7,4),(7,capacity)]:
        batch=g.batch('easy',count,seed)
        a=audit(batch)
        assert a['passed'], (seed,count,a)
        assert len({r['generation']['mathematical_fingerprint'] for r in batch})==count
        sampler.append({'seed':seed,'count':count,'audit':a})
        if count==5:
            _,d=delivery('seed-'+str(seed),batch)
            sampler[-1]['delivery']=d
        if count==capacity:
            _,d=delivery('capacity',batch)
            sampler[-1]['delivery']=d

    # Source replay plus affected current items, all selectable answers; batch
    # correct and wrong responses through the real native learner grader once.
    native=[];replays=[];choices=0
    supplied=json.loads((JOB/'source/source.json').read_text())
    originals={q[':question/math-academy-id']:q for q in supplied['material']['kp'][':knowledge-point/questions']}
    for sid,source in sorted(g.CASES.items()):
        assert source==originals[sid], 'Bundled source differs from supplied evidence'
        rec=g.generate('easy',0,sid,{'matches':list(g.original_matches(sid))},source_replay=True)
        choices+=fidelity(source,rec);_,checks=inspect(rec);replays.append(rec)
        native.append({'label':'source '+sid,'record':rec,'checks':checks})
    for rec in accepted:
        _,checks=inspect(rec)
        native.append({'label':'repaired prefix','record':rec,'checks':checks})
    # Hold labels, shapes, coefficients and dimension-excluded B fixed; only
    # qualifying pivot evidence changes. Also retain an irrelevant scale control.
    controlled=[g.generate('easy',0,'q-139965',{'matches':m,'assignment':['C','A','B']})
                for m in [['A'],['C'],['A','C']]]
    banks=[visible_bank(r['question']) for r in controlled]
    assert all(b['B']==banks[0]['B'] for b in banks)
    assert all(inspect(r)[0]['truth']==m for r,m in zip(controlled,[['A'],['C'],['A','C']]))
    for rec in controlled:
        _,checks=inspect(rec)
        native.append({'label':'controlled pivot evidence','record':rec,'checks':checks})
    scaled=g.generate('easy',0,'q-139965',{'matches':['C'],'assignment':['C','A','B'],'scale':1})
    assert inspect(scaled)[0]['truth']==inspect(controlled[1])[0]['truth']
    assert visible_bank(scaled['question'])!=banks[1]
    _,checks=inspect(scaled)
    native.append({'label':'irrelevant nonzero scale','record':scaled,'checks':checks})
    save('counterfactual-records.json',controlled+[scaled])
    save('render-records.json',controlled[:2])
    shortcuts=[]
    for rec in affected:
        w,_=inspect(rec)
        # Independently compute C; hardcode A true, then choose matching bank item.
        guess={'A'} | ({'C'} if 'C' in w['truth'] else set())
        f=rec['question'][':question/answer-fields'][0]
        import re
        choice=next(a for a in f[':answer-field/choices']
                    if set(re.findall(r'\$([A-E])\$',a[':answer/value']))==guess)
        expected='accepted' if guess==set(w['truth']) else 'rejected'
        native.append({'label':'hardcode A, inspect C','record':rec,'checks':[
            {'submitted_answer_id':choice[':answer/id'],'expected':expected,
             'purpose':'retained conditional shortcut; independently computed C rank'}]})
        shortcuts.append({'question_id':rec['question'][':question/id'],'truth':w['truth'],
                          'strategy_response':sorted(guess),'expected_grade':expected})
    assert {s['expected_grade'] for s in shortcuts}=={'accepted','rejected'}
    save('source-replays.json',replays);save('grader-input.json',native)
    command=[str(REPO/'generate/runs/current/check-engine'),str(E/'grader-input.json'),str(E/'grader-results.json')]
    result=subprocess.run(command,capture_output=True,text=True)
    assert result.returncode==0,result.stdout+result.stderr
    grades=json.loads((E/'grader-results.json').read_text())
    assert grades['documented_unresolved_checks']==0
    report={'passed':True,'finding':'6900891930e4bdc756fa',
            'negative_control':old_audit,'exact_prefix_replay':replay_report,
            'source_replay':{'questions':len(replays),'choices':choices},
            'sampler_controls':sampler,'shortcut_grades':shortcuts,
            'native_grader_command':command,
            'grades':{k:grades[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},
            'limits':['Captured inventory only; no database writes.',
                      'Learner histories and reservations are unavailable; uniform fresh selection does not guarantee an alternating sequence.',
                      'The recorded candidate prefix is replayed explicitly: per-record seed 0 is not the unknown runner batch shuffle seed.']}
    save('batch-regression.json',report)
    print(json.dumps({'passed':True,'negative_control_failed':True,'source_replays':len(replays),
                      'sampler_controls':len(sampler),'shortcut_grades':shortcuts,'grades':report['grades']}))

if __name__=='__main__':main()
