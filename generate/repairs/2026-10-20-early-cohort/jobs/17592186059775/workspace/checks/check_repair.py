"""Executable CLI/runtime, source fidelity, mathematical and decision regressions.

Only imports local code, invokes local tools, and writes evidence. No services or DB.
"""
import sys
sys.dont_write_bytecode = True
import collections
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

W = Path(__file__).resolve().parents[1]
REPO = Path('/home/jake/Developer/Course_Academy')
JOB = REPO/'generate/repairs/2026-10-20-early-cohort/jobs/17592186059775'
E = W/'evidence'
sys.path.insert(0, str(W))
spec = importlib.util.spec_from_file_location('readback', W/'17592186059775/validate.py')
v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
g = v.g

def save(name, obj):
    (E/name).write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n')

def key(record):
    f = record['question'][':question/answer-fields'][0]
    return next(a for a in f[':answer-field/choices'] if a[':answer/id'] == f[':answer-field/correct'][1])

def probes(records):
    groups = collections.defaultdict(list)
    for r in records: groups[r['generation']['template']].append(r)
    report = {}
    for sid, rows in groups.items():
        positions = collections.Counter(); ranks = collections.Counter(); signs = collections.Counter()
        consistency_selectors = 0
        for r in rows:
            f = r['question'][':question/answer-fields'][0]; bank = f[':answer-field/choices']
            selected = key(r); matrices = [v.printed_matrices(a[':answer/value'])[0] for a in bank]
            correct = v.printed_matrices(selected[':answer/value'])[0]
            positions[next(i for i,a in enumerate(bank) if a == selected)] += 1
            ranks[sorted(m[1,2] for m in matrices).index(correct[1,2])] += 1
            signs[str(v.sp.sign(correct[1,2]))] += 1
            # Uniform coefficient/top-RHS structure removes a unique layout cue.
            assert len({tuple(m[:,:2]) for m in matrices}) == 1
            assert len({m[0,2] for m in matrices}) == 1
            if 'and then solve' in r['question'][':question/problem']:
                consistent = [i for i,a in enumerate(bank)
                              if matrices[i][:,:2]*v.sp.Matrix(v.pair(a[':answer/value'])) == matrices[i][:,2]]
                consistency_selectors += len(consistent)==1
                assert len(consistent)==5, (sid, 'internal-consistency shortcut')
        assert len(ranks) >= 2 and len(positions) >= 2, (sid, ranks, positions)
        report[sid] = {'records':len(rows),'correct_positions':dict(positions),
                       'correct_numeric_ranks':dict(ranks),'correct_y_signs':dict(signs),
                       'best_fixed_position':max(positions.values())/len(rows),
                       'best_fixed_rank':max(ranks.values())/len(rows),
                       'unique_consistency_selector':consistency_selectors,
                       'random_choice_baseline':0.2,
                       'sign_limitation':'Some banks have one shared sign; it cannot identify one option.'}
    return report

def main():
    E.mkdir(exist_ok=True)
    manifest = json.loads((W/'package.json').read_text())
    assert manifest['dependencies'] == {'python':sys.version.split()[0], 'packages':{'sympy':v.sp.__version__}}
    # Reproduce the exact reported command in a relocated runtime-only closure.
    with tempfile.TemporaryDirectory() as td:
        dest = Path(td)
        for name in manifest['files']:
            p = dest/name; p.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(W/name,p)
        cmd = [sys.executable,str(dest/manifest['entrypoint']),'--difficulty','easy','--count','5','--seed','0','--format','json']
        run = subprocess.run(cmd, cwd=td, env={**os.environ,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(dest/'assets')},capture_output=True,text=True)
        assert run.returncode==0,run.stderr
        batch=json.loads(run.stdout)['instances']; assert len(batch)==5
        repeat=subprocess.run(cmd,cwd=td,capture_output=True,text=True,check=True)
        assert repeat.stdout==run.stdout,'Seeded CLI replay mismatch'
        for r in batch: v.independent(r)
        assert all(r['question'][':question/difficulty']==':question.difficulty/easy' for r in batch)
        save('cli-regression.json',{'command':['python',manifest['entrypoint']]+cmd[2:],'exit_code':0,'count':5,'runtime_only_relocation':True,'deterministic':True})
        save('runner-sample.json',batch)
    # Exact complete source-bank replay includes the known ambiguous source.
    supplied = json.loads((JOB/'source/source.json').read_text())['material']['kp']
    replay=[]
    for source in supplied[':knowledge-point/questions']:
        sid=source[':question/math-academy-id']
        if sid not in g.CASES: continue
        r=g.source_replay(sid); q=r['question']; f=q[':question/answer-fields'][0]; orig=source[':question/answer-fields'][0]
        assert q[':question/problem']==source[':question/problem']
        assert q[':question/worked-solution']==source[':question/worked-solution']
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in orig[':answer-field/choices'])
        assert key(r)[':answer/value']==orig[':answer-field/correct'][':answer/value']
        if sid in g.EXCLUDED_PROFILES:
            keyed=v.printed_matrices(key(r)[':answer/value'])[0].rref()[0]
            assert sum(v.printed_matrices(a[':answer/value'])[0].rref()[0]==keyed for a in f[':answer-field/choices'])==2
        else: v.independent(r)
        replay.append({'source':sid,'question_id':source[':question/id'],'complete_bank_matched':True,'choices':5,'distractors':4,'legacy_ambiguity':sid in g.EXCLUDED_PROFILES})
    save('source-replay-current.json',{'complete_banks':len(replay),'matched_choices':5*len(replay),'matched_distractors':4*len(replay),'profiles':replay})
    records=[]; counterfactual=[]; permutation=[]; coverage={}
    for sid in g.CASES:
        level=g.level(sid); ks=[p[1] for p in g.domain(sid)]
        family=[g.generate(level,31,parameters=[sid,ks[0],t]) for t in range(5)]
        common_bank = {a[':answer/value'] for a in family[0]['question'][':question/answer-fields'][0][':answer-field/choices']}
        ordered_bank = [a[':answer/value'] for a in family[0]['question'][':question/answer-fields'][0][':answer-field/choices']]
        top=None; bottoms=[]; keys=[]
        for r in family:
            v.independent(r)
            assert common_bank=={a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']}
            assert ordered_bank==[a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
            m=v.printed_matrices(r['question'][':question/problem'])[0]
            if top is None: top=tuple(m[0,:])
            assert top==tuple(m[0,:]), 'Controlled upper row changed'
            bottoms.append(str(m[1,2]));keys.append(key(r)[':answer/value'])
        assert len(set(bottoms))==len(set(keys))==5
        counterfactual.append({'profile':sid,'parameters':[r['generation']['parameters'] for r in family], 'fixed_bank':True,'fixed_upper_row':list(map(str,top)),'decisive_input_rhs':bottoms,'distinct_correct_objects':len(set(keys))})
        # Irrelevant seed changes only order; input, solution and key object stay fixed.
        before=family[2];after=g.generate(level,32,parameters=[sid,ks[0],2])
        assert before['question'][':question/problem']==after['question'][':question/problem']
        assert before['question'][':question/worked-solution']==after['question'][':question/worked-solution']
        assert key(before)==key(after)
        assert before['question'][':question/answer-fields'][0][':answer-field/choices']!=after['question'][':question/answer-fields'][0][':answer-field/choices']
        permutation.append({'profile':sid,'seed_pair':[31,32],'preserved_answer':True})
        records.extend(family)
        for target in (0,4):
            r=g.generate(level,31,parameters=[sid,ks[-1],target]);v.independent(r);records.append(r)
        records.append(after)
        coverage[sid]={'eligible_k':ks,'tested_k':[ks[0],ks[-1]],'candidate_ranks':list(range(5)),'response':'REF-and-solution' if 'and then solve' in family[0]['question'][':question/problem'] else 'REF'}
    for level in ('hard','unclassified'):
        try: g.generate(level)
        except ValueError:pass
        else:raise AssertionError('Unsupported level accepted')
    assert len({g.fingerprint(r['question']) for r in records})>5
    save('test-records.json',records)
    save('pedagogical-variation.json',{'coverage':coverage,'counterfactuals':counterfactual,'irrelevant_permutations':permutation,'raw_probes':probes(records),'semantic_instances':len({g.fingerprint(r['question']) for r in records}),'limits':['RHS variation within source coefficient profiles; no claim of broad coefficient transfer.','Finite bounded k and candidate constants.']})
    native=[{'label':str(r['generation']['parameters'])+' seed '+str(r['generation']['seed']),'record':r,'checks':v.checks(r)} for r in records]
    save('native-input-current.json',native)
    subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(E/'native-input-current.json'),str(E/'native-report-current.json')],check=True)
    previews=[g.generate('easy',31,parameters=[sid,g.domain(sid)[-1][1],target]) for sid,target in [('q-1059',0),('q-130910',4),('q-130909',0),('q-73439',4)]]
    save('render-records.json',previews)
    save('check-summary.json',{'passed':True,'source_banks':len(replay),'generated_readback_cases':len(records),'native_responses':5*len(records),'semantic_instances':len({g.fingerprint(r['question']) for r in records})})
    print(json.dumps(json.loads((E/'check-summary.json').read_text())))

if __name__=='__main__':main()
