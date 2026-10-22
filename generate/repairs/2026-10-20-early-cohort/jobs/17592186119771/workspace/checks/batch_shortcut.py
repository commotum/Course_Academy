#!/usr/bin/env python3
"""Strict visible-record batch regression, real delivery and native grading.
No services, runtime writes, publication or database mutations.
"""
import collections
import copy
import importlib.util
import json
import re
import subprocess
import sys
import validate as v

REPO = v.ROOT.parents[5]
# Exact reviewed batch seed; additional seeds test the construction rule.
SEEDS = (4251183390, 0, 19, 71, 991, 20261022)


def heuristic(m):
    return ('Diagonal matrix' if len(m) == 2 else
            'Upper triangular matrix' if m[0][0] < 0 else 'Lower triangular matrix')


def inspect(records):
    groups = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    positions = collections.Counter()
    size_answers = collections.defaultdict(set)
    size_positions = collections.defaultdict(set)
    orientation_order = collections.defaultdict(list)
    rows = []
    hits = 0
    first_orientation = 0
    for r in records:
        q = r['question']; m = v.matrix(q[':question/problem']); answer = v.verify(r)
        sign = (m[0][0] > 0)-(m[0][0] < 0)
        letter = re.search(r'([AC])\s*=', q[':question/problem'])[1]
        for name, cue in [('size', (len(m),)), ('sign', (sign,)), ('letter', (letter,)),
                          ('size/sign', (len(m), sign)), ('size/letter', (len(m), letter)),
                          ('size/sign/letter', (len(m), sign, letter))]:
            groups[name][cue][answer] += 1
        f = q[':question/answer-fields'][0]
        index = next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/value'] == answer)
        positions[index] += 1
        size_positions[len(m)].add(index)
        first_orientation += next(a[':answer/value'] for a in f[':answer-field/choices']
                                  if a[':answer/value'] in ('Upper triangular matrix','Lower triangular matrix')) == answer
        if answer in ('Upper triangular matrix','Lower triangular matrix'):
            orientation_order[len(m)].append(next(a[':answer/value'] for a in f[':answer-field/choices']
                if a[':answer/value'] in ('Upper triangular matrix','Lower triangular matrix')) == answer)
        size_answers[len(m)].add(answer)
        hits += heuristic(m) == answer
        rows.append({'size':len(m),'sign':sign,'letter':letter,'answer':answer,'position':index})
    # The exact strict review acceptance criterion is retained.
    assert hits < len(records), 'Reported size/sign strategy still answers every delivered record'
    report = {'reported_rule_hits':hits,'total':len(records),'groups':{},
              'correct_positions':dict(positions),'first_orientation_hits':first_orientation}
    for name, cues in groups.items():
        successes = sum(max(counts.values()) for counts in cues.values())
        assert successes < len(records), (name, 'perfect incidental classifier', rows)
        report['groups'][name] = {'best_lookup_hits':successes,'total':len(records),
            'cue_groups':[{'cue':list(cue),'answers':dict(counts)} for cue,counts in sorted(cues.items())]}
    assert len(positions) > 1
    assert 0 < first_orientation < len(records)
    assert all(len(answers)>1 for answers in size_answers.values()), rows
    # Within each recognizable size, opposite orientations must retain a joint
    # sign/letter collision. This goes beyond defeating one fitted heuristic.
    for n, answers in size_answers.items():
        assert len(size_positions[n])>1, ('fixed position within size',n,rows)
        if {'Upper triangular matrix','Lower triangular matrix'} <= answers:
            assert len(set(orientation_order[n]))>1, ('first/last orientation cue within size',n,rows)
            collision = any('Upper triangular matrix' in counts and 'Lower triangular matrix' in counts
                for cue, counts in groups['size/sign/letter'].items() if cue[0] == n)
            assert collision, ('within-size orientation shortcut', n, rows)
    report['size_positions']={n:sorted(values) for n,values in size_positions.items()}
    report['orientation_order']={n:{'first_correct':sum(values),'triangular_count':len(values)}
                                for n,values in orientation_order.items()}
    return report


def main():
    out = v.OUT/'batch-repair'; out.mkdir(exist_ok=True)
    batches = []
    for seed in SEEDS:
        cmd = [sys.executable,str(v.ROOT/'17592186119771.py'),'--difficulty','easy',
               '--count','5','--seed',str(seed),'--format','json']
        result = subprocess.run(cmd,capture_output=True,text=True,check=True)
        records = json.loads(result.stdout)
        assert len(records) == len({v.structural(v.matrix(r['question'][':question/problem'])) for r in records}) == 5
        batches.append(records)
    records = [r for batch in batches for r in batch]
    (out/'input.json').write_text(json.dumps(records,indent=2)+'\n')
    before = [inspect(batch) for batch in batches]
    command = [sys.executable,str(REPO/'generate/pipeline/check_delivery.py'),
        '--input',str(out/'input.json'),'--source',str(v.SOURCE),'--inventory',str(v.INVENTORY),
        '--difficulty','easy','--output',str(out/'delivery'),'--asset-root',str(v.OUT),
        '--math-root','/media/jake/SSD/EDB/math']
    result = subprocess.run(command,capture_output=True,text=True)
    (out/'delivery.stdout').write_text(result.stdout); (out/'delivery.stderr').write_text(result.stderr)
    assert result.returncode == 0, result.stderr
    accepted = json.loads((out/'delivery/accepted.json').read_text())
    assert len(accepted) == len(records)
    assert [(v.matrix(r['question'][':question/problem']),v.key(r['question'])) for r in accepted] == [(v.matrix(r['question'][':question/problem']),v.key(r['question'])) for r in records]
    after = [inspect(accepted[i:i+5]) for i in range(0,len(accepted),5)]
    assert before == after
    # Exact review sign-change control, generated afresh with one entry changed.
    spec = importlib.util.spec_from_file_location('candidate',v.ROOT/'17592186119771.py')
    g = importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
    original = {'matrix':[[-9,-9,-6],[0,5,-7],[0,0,-10]],'letter':'C','layout':'bmatrix'}
    flipped = copy.deepcopy(original);flipped['matrix'][0][0] = 9
    transposed = copy.deepcopy(flipped);transposed['matrix'] = list(map(list,zip(*flipped['matrix'])))
    controls = [g.generate('easy',4251183390,parameters=p) for p in (original,flipped,transposed)]
    assert [v.verify(r) for r in controls] == ['Upper triangular matrix','Upper triangular matrix','Lower triangular matrix']
    assert [heuristic(v.matrix(r['question'][':question/problem'])) for r in controls[:2]] == ['Upper triangular matrix','Lower triangular matrix']
    (out/'controls.json').write_text(json.dumps(controls,indent=2)+'\n')
    cases = []
    for idx,r in enumerate(accepted+controls):
        m=v.matrix(r['question'][':question/problem']); answer=v.expected(m)
        choices=r['question'][':question/answer-fields'][0][':answer-field/choices']
        checks=[{'field_index':0,'submitted_answer_id':a[':answer/id'],
                 'expected':'accepted' if a[':answer/value']==answer else 'rejected',
                 'purpose':'independent classification of batch or sign/transpose control'} for a in choices]
        checks.append({'field_index':0,'submitted_answer_id':next(a[':answer/id'] for a in choices if a[':answer/value']==heuristic(m)),
                       'expected':'accepted' if heuristic(m)==answer else 'rejected','purpose':'exact reviewed shortcut submission'})
        cases.append({'label':f'batch-repair-{idx}','record':r,'checks':checks})
    (out/'grader-input.json').write_text(json.dumps(cases,indent=2)+'\n')
    command = [str(REPO/'generate/runs/current/check-engine'),str(out/'grader-input.json'),str(out/'grader-report.json')]
    result = subprocess.run(command,capture_output=True,text=True)
    assert result.returncode == 0, result.stderr+result.stdout
    # Snapshot provenance cannot establish a historical generator batch.
    inv=json.loads(v.INVENTORY.read_text()); reviewed=[]
    for q in inv['questions']:
        m=v.matrix(q[':question/problem'])
        reviewed.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],
                         'size':len(m),'top_left':m[0][0],'classification':v.expected(m),
                         'generation_keys':[k for k in q if 'generation' in k.lower()]})
    (out/'inventory-audit.json').write_text(json.dumps({'inspected':len(reviewed),'records':reviewed,
        'attributable_generated_cohorts':0,'affected_questions':[],
        'limitation':'All captured matrices inspected. No generation metadata or batch membership supplied; historical batch shortcut incidence is untestable, not verified absent.'},indent=2)+'\n')
    (out/'results.json').write_text(json.dumps({'finding':'5ce68a5d357d6c68c196','seeds':list(SEEDS),
        'before':before,'after':after,'accepted':len(accepted),'native_cases':len(cases),
        'exact_sign_control':'Upper accepted, heuristic Lower rejected after only -9 -> 9 at a11',
        'relevant_control':'same diagonal and transposed off-diagonal region changes Upper to Lower'},indent=2)+'\n')
    print(json.dumps({'seeds':list(SEEDS),'delivered':len(accepted),'reported_rule_hits':[r['reported_rule_hits'] for r in after],
                      'all_joint_cue_tests':'passed','native_cases':len(cases)}))

if __name__ == '__main__': main()
