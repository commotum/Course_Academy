"""Strict current-CLI and historical-pool checks for the latest review findings.

Only evidence is written. No service, publication, database, or runtime edits.
The historical check intentionally fails while the captured defective pool exists.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
from validate_repair import W, g, probes, printed_check, field, value, root

E = W/'evidence/repair-2'
E.mkdir(parents=True, exist_ok=True)
REPO = W.parents[5]
SOURCE = W.parent/'source/source.json'
INVENTORY = W.parent/'source/inventory.json'
COMMANDS = []

def write(name, data):
    (E/name).write_text(json.dumps(data, indent=2, default=str)+'\n')

def run(args):
    COMMANDS.append([str(a) for a in args])
    p = subprocess.run(args, capture_output=True, text=True, cwd=W)
    assert p.returncode == 0, (args, p.stdout[-1000:], p.stderr[-1000:])
    return p.stdout

def contrasts(records):
    # All evidence comes from printed prompt, banks, key and worked solution.
    # No generator acceptance flag, rank or fingerprint supplies the witness.
    for r in records:
        printed_check(r)
    report = probes(records)
    groups = {n:z for n,z in report.items() if n.count(':') == 2}
    assert len(groups) == 2, report
    for n,z in groups.items():
        ranks = {int(rank) for rank in z['numeric_ranks']}
        assert z['total'] >= 2 and z['distinct_roots'] >= 2, (n,z)
        assert ranks & {0,4} and ranks & {1,2,3}, (n,z)
        assert z['fixed_rank_best'] < z['total'], (n,z)
        assert z['fixed_position_best'] < z['total'], (n,z)
        assert z['sign_extremum_successes'] < z['total'], (n,z)
    return report

def batch_check():
    old = [g.generate('easy', seed=n) for n in [1475864945,1475864946]]
    assert old == json.loads((E/'baseline-records.json').read_text())
    # Retain the exact counterexample; fixing selection must not erase replay.
    z = probes(old)['easy:unit_bare:opposite_sign']
    assert z['total'] == z['sign_extremum_successes'] == 2
    trials = []; primary = None
    for seed,count in [(1475864943,5),(0,4),(20261021,5)]:
        args = [sys.executable,'-B',str(W/'17592186115242.py'),
                '--difficulty','easy','--count',str(count),'--seed',str(seed),'--format','json']
        records = json.loads(run(args))
        assert len(records) == count
        assert len({r['question'][':question/id'] for r in records}) == count
        for r in records:
            assert r == g.generate('easy', seed=r['generation']['seed'])
        before = contrasts(records)
        name = f'batch-{seed}-{count}.json'
        write(name, records)
        dest = E/f'delivery-{seed}-{count}'
        run([sys.executable,'-B',str(REPO/'generate/pipeline/check_delivery.py'),
             '--input',str(E/name),'--source',str(SOURCE),'--inventory',str(INVENTORY),
             '--difficulty','easy','--output',str(dest),'--asset-root',str(E/'assets'),
             '--math-root','/media/jake/SSD/EDB/math'])
        accepted = json.loads((dest/'accepted.json').read_text())
        assert len(accepted) == count, 'Filtering removed a required contrasting witness'
        after = contrasts(accepted)
        assert before == after
        trials.append(dict(seed=seed,count=count,selected_seeds=[r['generation']['seed'] for r in records],
                           skipped_windows=records[0]['generation']['seed']-seed,
                           before=before,after=after))
        if primary is None:
            primary = records
            write('batch.json',records)
            write('accepted.json',accepted)
    base = primary[0];p = base['generation']['parameters'];seed = base['generation']['seed']
    relevant = g.generate('easy',seed=seed,parameters=dict(p,b=-p['b']))
    alternate_e = next(e for e in range(-8,9) if e != p['e'] and e != p['d']*p['c'])
    irrelevant = g.generate('easy',seed=seed,parameters=dict(p,e=alternate_e))
    for r in [relevant,irrelevant]: printed_check(r)
    assert root(base) != root(relevant) and root(base) == root(irrelevant)
    assert base['question'][':question/worked-solution'] != relevant['question'][':question/worked-solution']
    assert base['question'][':question/worked-solution'] != irrelevant['question'][':question/worked-solution']
    write('counterfactual-records.json',[base,relevant,irrelevant])
    grader_records = primary + [relevant,irrelevant]
    write('grader-input.json',[dict(label=f'finite-batch-{i}',record=r,checks=[
        dict(submitted_answer_id=a[':answer/id'],expected='accepted' if value(a)==root(r) else 'rejected',
             purpose='Independent displayed-system determinant and rank')
        for a in field(r)[':answer-field/choices']]) for i,r in enumerate(grader_records)])
    write('batch-results.json',dict(passed=True,trials=trials,
          exact_old_seed_replay_retained=True,counterfactual_roots=[root(r) for r in [base,relevant,irrelevant]],
          limits=['Four is the minimum batch size admitting both sign-group contrasts.',
                  'These finite checks do not prove absence of every possible shortcut.',
                  'Shared delivery is read-only; publication and actual learner history are unavailable.']))
    print(json.dumps(dict(finding='41b3562c0b46bafedeed',passed=True,batches=len(trials),delivered=sum(t['count'] for t in trials))))
    return 0

def inventory_check():
    run([sys.executable,'-B',str(W/'checks/inventory_audit.py')])
    historic = json.loads((W/'evidence/generated-records.json').read_text())
    inventory = json.loads(INVENTORY.read_text())
    stored = {q[':question/id']:q for q in inventory['questions']}
    affected = []; counterparts = []
    for r in historic:
        q = r['question'];saved = stored[q[':question/id']]
        # Audit verifies complete captured IDs, choices, key, prompt, solution,
        # and archival generation replay before this strict selection probe.
        printed_check(r)
        p = r['generation']['parameters']
        current = g.generate('easy',seed=r['generation']['seed'],parameters=p)
        printed_check(current)
        assert root(current) == root(r)
        counterparts.append(current)
        z = probes([r])['easy:unit_bare']
        if z['sign_extremum_successes'] == 1:
            affected.append(dict(question_id=q[':question/id'],entity_id=saved[':db/id']))
    # Exact conditional within-easy selection, after a learner has seen the new
    # batch but none of the old questions. Entity ordering is known for old pool.
    pool = sorted(historic,key=lambda r:stored[r['question'][':question/id']][':db/id'])
    draws = []
    for i in range(64):
        digest=hashlib.sha256(f'course-academy/question-selection/v1/author-repair-{i}'.encode()).digest()
        u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53)
        draws.append(pool[int(u*len(pool))])
    selection=probes(draws)
    passed = not affected
    write('historical-current-counterparts.json',counterparts)
    write('inventory-results.json',dict(passed=passed,affected_questions=affected,
          inventory_basis=inventory['basis'],selection=selection,
          source='engine/rust/question_selection.rs: select, conditional on positive easy weight',
          limits=['Captured inventory remains selectable; this author cannot change database content.',
                  'Actual learner history and configured policy are not supplied.',
                  'The 64/64 witness is a possible new-seen history, not a prediction of all histories.']))
    print(json.dumps(dict(finding='591f580cadb749294588',passed=passed,affected=len(affected),
                         selection_successes=selection['easy:unit_bare']['sign_extremum_successes'],draws=64)))
    return 0 if passed else 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--finding', choices=['batch','inventory'], required=True)
    args = parser.parse_args()
    try:
        status = batch_check() if args.finding == 'batch' else inventory_check()
    finally:
        write('commands-'+args.finding+'.json',COMMANDS)
    raise SystemExit(status)
