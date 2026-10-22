#!/usr/bin/env python3
"""Offline regression and independent visible-record witnesses. No runtime writes."""
import collections
import importlib.util
import itertools
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'evidence'
SOURCE = ROOT.parent / 'source' / 'source.json'
INVENTORY = ROOT.parent / 'source' / 'inventory.json'

def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')

def matrix(text):
    match = re.search(r'\\begin\{(bmatrix|aligned)\}(.*?)\\end\{\1\}', text, re.S)
    assert match, text
    return [[int(x.strip()) for x in row.split('&')] for row in match[2].split(r'\\')]

def expected(m):
    n = len(m)
    assert all(len(row) == n for row in m)
    above = any(m[i][j] != 0 for i in range(n) for j in range(n) if i < j)
    below = any(m[i][j] != 0 for i in range(n) for j in range(n) if i > j)
    if not above and not below:
        return 'Identity matrix' if all(m[i][i] == 1 for i in range(n)) else 'Diagonal matrix'
    if not above: return 'Lower triangular matrix'
    if not below: return 'Upper triangular matrix'
    return 'Other'

def key(q):
    field = q[':question/answer-fields'][0]
    correct = field.get(':answer-field/correct')
    if correct is None: return None
    cid = correct[':answer/id'] if isinstance(correct, dict) else correct[1]
    return next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id'] == cid)

def structural(m):
    return (len(m), tuple(int(v != 0) for i, row in enumerate(m) for j, v in enumerate(row) if i != j))

def verify(rec):
    q = rec['question']; m = matrix(q[':question/problem']); answer = expected(m)
    assert key(q) == answer, (m, key(q), answer)
    assert matrix(q[':question/worked-solution']) == m
    assert 'it is '+('an ' if answer.startswith('Upper') else 'a ')+answer.lower()+'.' in q[':question/worked-solution']
    if answer in ('Lower triangular matrix', 'Upper triangular matrix'):
        witness = re.search(r'_\{(\d)(\d)\}=(-?\d+)', q[':question/worked-solution'])
        assert witness
        i,j,v = map(int,witness.groups())
        assert m[i-1][j-1] == v != 0
        assert (i > j) == answer.startswith('Lower')
    assert len(q[':question/answer-fields']) == 1
    f = q[':question/answer-fields'][0]
    assert f[':answer-field/type'] == ':answer-field.type/radio'
    assert sorted(a[':answer/value'] for a in f[':answer-field/choices']) == sorted(LABELS)
    return answer

LABELS = ['Identity matrix','Diagonal matrix','Upper triangular matrix','Lower triangular matrix','Other']

def normalize(text):
    return re.sub(r'\s+', '', text.replace(r'\neq', r'\ne').replace('$','').replace('{','').replace('}',''))

def cue_report(records):
    groups = collections.defaultdict(list)
    positions = collections.defaultdict(list)
    for r in records:
        q=r['question']; text=q[':question/problem']; m=matrix(text)
        letter=re.search(r'([AC])\s*=',text)[1]
        answer=key(q)
        groups[f'n={len(m)},letter={letter},layout=bmatrix'].append(answer)
        f=q[':question/answer-fields'][0]
        pos=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/value']==answer)
        positions[f'n={len(m)}'].append(pos)
    report={}
    for cue,answers in groups.items():
        counts=collections.Counter(answers)
        report[cue]={'n':len(answers),'answer_counts':dict(counts),'best_constant_successes':max(counts.values())}
        assert len(counts)>1, ('incidental cue perfectly predicts answer',cue)
    for cue,values in positions.items():
        assert len(set(values))>1, ('fixed answer position',cue)
        report[cue+',correct_position_counts']=dict(collections.Counter(values))
    return report

def main():
    OUT.mkdir(exist_ok=True)
    spec=importlib.util.spec_from_file_location('candidate', ROOT/'17592186119771.py')
    g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
    # Exact latest counterexample: execute the real CLI, not a metadata assertion.
    cmd=[sys.executable,str(ROOT/'17592186119771.py'),'--difficulty','easy','--count','5','--seed','0','--format','json']
    result=subprocess.run(cmd,capture_output=True,text=True)
    assert result.returncode==0,result.stderr
    sample=json.loads(result.stdout)
    assert len(sample)==5 and len({structural(matrix(r['question'][':question/problem'])) for r in sample})==5
    for r in sample: verify(r)
    assert result.stdout==subprocess.run(cmd,capture_output=True,text=True,check=True).stdout
    save('samples.json',sample)
    # Whole restored structural family, independently enumerated expected supports.
    easy=g.batch('easy',12,41)
    observed={structural(matrix(r['question'][':question/problem'])) for r in easy}
    wanted=set()
    for n in (2,3):
        cells=[(i,j) for i in range(n) for j in range(n) if i!=j]
        for bits in itertools.product((0,1),repeat=len(cells)):
            above=sum(b for b,(i,j) in zip(bits,cells) if i<j)
            below=sum(b for b,(i,j) in zip(bits,cells) if i>j)
            minimum=(n*(n-1)+3)//4
            if (above==below==0) or (above==0 and below>=minimum) or (below==0 and above>=minimum):
                wanted.add((n,bits))
    assert observed==wanted and len(observed)==12
    for r in easy: verify(r)
    # Finite exhaustion and exclusions remain real, never cosmetic duplication.
    try: g.batch('easy',13,0)
    except ValueError: pass
    else: raise AssertionError('finite limit concealed')
    excluded=[r['generation']['parameter_fingerprint'] for r in easy[:7]]
    remaining=g.batch('easy',5,2,exclude_fingerprints=excluded)
    assert {structural(matrix(r['question'][':question/problem'])) for r in remaining} == observed-{structural(matrix(r['question'][':question/problem'])) for r in easy[:7]}
    # Replay every supplied source, including the newly supplied entry 10.
    s=json.loads(SOURCE.read_text()); replays=[];banks=0;choices=0
    for q in s['material']['kp'][':knowledge-point/questions']:
        sid=q[':question/math-academy-id'];p=g.parse_matrix(q[':question/problem'])
        level=q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/easy').split('/')[-1]
        replay=g.generate(level,profile='raw:'+sid,parameters=p);rq=replay['question']
        assert matrix(rq[':question/problem'])==matrix(q[':question/problem'])
        assert normalize(rq[':question/problem'])==normalize(q[':question/problem']),sid
        assert len(rq[':question/answer-fields'])==len(q[':question/answer-fields'])
        for original,field in zip(q[':question/answer-fields'],rq[':question/answer-fields']):
            assert sorted(a[':answer/value'] for a in original[':answer-field/choices'])==sorted(a[':answer/value'] for a in field[':answer-field/choices'])
            assert original[':answer-field/type'][':db/ident']==field[':answer-field/type']
            banks+=1;choices+=len(field[':answer-field/choices'])
        assert key(rq)==key(q)
        assert (':question/difficulty' in rq)==(':question/difficulty' in q)
        if ':question/difficulty' in q: assert rq[':question/difficulty']==q[':question/difficulty'][':db/ident']
        assert (':question/worked-solution' in rq)==(':question/worked-solution' in q)
        if ':question/worked-solution' in q: assert normalize(rq[':question/worked-solution'])==normalize(q[':question/worked-solution']),sid
        # Normal source parameters now retain the easy 3x3 and zero diagonal cases.
        normal=g.generate(level,profile='source:'+sid,parameters=p)
        assert verify(normal)==expected(matrix(q[':question/problem']))
        replays.append(replay)
    save('source-replay.json',replays)
    # Relevant evidence changes and irrelevant changes with answer order fixed.
    controls=[];relations=[]
    for n in (2,3):
        for letter in ('A','C'):
            low=[[(-2 if i==0 else i+2) if i==j else 5 if i>j else 0 for j in range(n)] for i in range(n)]
            upper=[list(row) for row in zip(*low)]
            diag=[[v if i==j else 0 for j,v in enumerate(row)] for i,row in enumerate(low)]
            trio=[]
            for m in (low,upper,diag):
                r=g.generate('easy',seed=17+n,parameters={'matrix':m,'letter':letter,'layout':'bmatrix'})
                verify(r);trio.append(r);controls.append(r)
                altered=[[0 if i==j else -v for j,v in enumerate(row)] for i,row in enumerate(m)]
                other=g.generate('easy',seed=17+n,parameters={'matrix':altered,'letter':'C' if letter=='A' else 'A','layout':'bmatrix'})
                verify(other); assert key(other['question'])==key(r['question']);controls.append(other)
                relations.append({'kind':'irrelevant sign/diagonal/letter','before':r['question'][':question/id'],'after':other['question'][':question/id'],'response_preserved':True})
            assert [key(r['question']) for r in trio]==['Lower triangular matrix','Upper triangular matrix','Diagonal matrix']
            relations.append({'kind':'transpose then clear off-diagonal','questions':[r['question'][':question/id'] for r in trio],'answers':[key(r['question']) for r in trio]})
    small=[g.generate('moderate',11,template='diagonal'),g.generate('hard',12,template='upper'),g.generate('hard',13,template='lower')]
    for r in small: verify(r)
    delivery=easy+controls
    save('easy-catalog.json',easy);save('counterfactuals.json',controls);save('delivery-input.json',delivery)
    save('pedagogical-variation.json',{'semantic_easy_patterns':len(observed),'counterfactuals':relations,'before_delivery':cue_report(delivery),'limits':['Support pattern determines the zero-region classification by mathematics; no independence from that decisive evidence is claimed.','Finite 12-pattern easy family; numerical changes do not enlarge it.','Identity and Other are source distractors, not sampled correct families.']})
    # All radio alternatives go through the real native grader in one batch.
    cases=[]
    for idx,r in enumerate(sample+easy+controls+small):
        answer=expected(matrix(r['question'][':question/problem']))
        cases.append({'label':str(idx),'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==answer else 'rejected','purpose':'independent zero-region classification'} for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]})
    save('grader-input.json',cases)
    # Inventory inspection is read-only; batch exhaustion has no per-record witness.
    inv=json.loads(INVENTORY.read_text());inventory=[]
    for q in inv['questions']:
        correct=key(q);exp=expected(matrix(q[':question/problem']))
        assert correct is None or correct==exp,(q[':question/id'],correct,exp)
        inventory.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'classification':exp,'stored_key':correct,'key_checked':correct is not None,'batch_failure_applicability':'not a per-record defect','generation_metadata_present':any('generation' in k for k in q)})
    save('inventory-audit.json',{'basis':inv['basis'],'records':inventory,'limitation':'No stored generation metadata is supplied; individual generator replay attribution is unavailable. Missing source key is ungraded evidence, not marked generated.'})
    (ROOT/'affected-inventory.json').write_text(json.dumps({'affected_questions':[]},indent=2)+'\n')
    summary={'latest_failure_reproduced_before':'evidence/before.stderr','cli_five_distinct':'passed','easy_structural_instances':len(observed),'source_banks':banks,'source_choices':choices,'normal_source_parameters':len(replays),'controlled_records':len(controls),'grader_cases_prepared':len(cases),'inventory_records_inspected':len(inventory),'inventory_missing_keys':sum(not r['key_checked'] for r in inventory)}
    save('validation.json',summary);print(json.dumps(summary))

if __name__=='__main__': main()
