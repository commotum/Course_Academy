"""Read-only math, cue, source, grader and delivery checks for the repaired sampler."""
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import random
import re
import shutil
import subprocess
import tempfile
import generator as g

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'Cargo.toml').exists())
HERE=Path(__file__).resolve().parent
OUT=HERE/'evidence';OUT.mkdir(exist_ok=True)
def save(name,value):(OUT/name).write_text(json.dumps(value,indent=2)+'\n')
def clean(s):return s.replace('\\\\','\\')
def run(args):subprocess.run([str(a) for a in args],check=True,cwd=HERE)

records=g.generate(count=64,seed=71931)
controls=[]
for kind in [False,True]:
    roles=g.draw_roles(random.Random(883+kind),kind)
    controls.extend(g.build(roles,i) for i in range(5))
records+=controls
cases=[];coverage=Counter()
for rec in records:
    q=rec['question'];f,=q[':question/answer-fields']
    match=re.search(r'(\d+)\^\{x([+-]\d+)?\}=(\d+)',clean(q[':question/problem']))
    assert match
    base,shift,rhs=int(match[1]),int(match[2] or 0),int(match[3])
    exact=math.log(rhs)/math.log(base)-shift
    assert abs(math.exp((exact+shift)*math.log(base))-rhs)<1e-9
    correct=f[':answer-field/correct'][1]
    checks=[];matches=[]
    for a in f[':answer-field/choices']:
        m=re.fullmatch(r'x=\\log_\{(\d+)\}\((\d+)\)([+-]\d+)?',clean(a[':answer/value']))
        assert m,a[':answer/value']
        value=math.log(int(m[2]))/math.log(int(m[1]))+int(m[3] or 0)
        is_correct=abs(value-exact)<1e-10;matches.append(is_correct)
        assert is_correct==(a[':answer/id']==correct)
        checks.append({'submitted_answer_id':a[':answer/id'],'expected':'accepted' if is_correct else 'rejected'})
    assert sum(matches)==1
    coverage['direct' if shift==0 else 'positive-shift' if shift>0 else 'negative-shift']+=1
    cases.append({'label':q[':question/id'],'record':rec,'checks':checks})
save('samples.json',records);save('grader-input.json',cases)
run([ROOT/'generate/runs/current/check-engine',OUT/'grader-input.json',OUT/'grader-report.json'])
for mid in g.SOURCE_IDS:
    rec=g.replay_source(mid);fixture=json.loads((HERE/'source-fixtures.json').read_text())[mid]
    assert rec['question']==fixture
save('source-replay.json',[g.replay_source(mid) for mid in g.SOURCE_IDS])
probes=[]
for group in [controls[:5],controls[5:]]:
    banks=[[a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']] for r in group]
    assert all(bank==banks[0] for bank in banks)
    assert len({r['question'][':question/problem'] for r in group})==5
    keys=[]
    for r in group:
        field=r['question'][':question/answer-fields'][0]
        keys.append(next(a[':answer/value'] for a in field[':answer-field/choices']
                         if a[':answer/id']==field[':answer-field/correct'][1]))
    assert len(set(keys))==5
    # Any bank-only strategy has one fixed choice on this unchanged bank.
    # Every choice is right in exactly one of five same-skill counterfactuals.
    for a in group[0]['question'][':question/answer-fields'][0][':answer-field/choices']:
        assert keys.count(a[':answer/value'])==1
    probes.append({'template':group[0]['generation']['template'],'same_bank_counterfactuals':5,
        'keys':keys,'any_deterministic_bank_only_strategy_correct':1,'total':5,'baseline':0.2})
save('counterfactual-cue-proof.json',probes)
run([ROOT/'.venv/bin/python',ROOT/'generate/pipeline/check_delivery.py','--input',OUT/'samples.json',
     '--source',HERE.parent/'source/source.json','--inventory',HERE.parent/'source/inventory.json',
     '--difficulty','easy','--output',OUT/'delivery'])
accepted=json.loads((OUT/'delivery/accepted.json').read_text());assert len(accepted)>=64
manifest=json.loads((HERE/'package.json').read_text())
with tempfile.TemporaryDirectory() as d:
    for name in manifest['files']:shutil.copy2(HERE/name,Path(d)/name)
    command=[str(ROOT/'.venv/bin/python'),'-B',str(Path(d)/'generator.py'),'--difficulty','easy','--count','5','--seed','7712','--format','json']
    one=subprocess.check_output(command,cwd=d);two=subprocess.check_output(command,cwd=d)
    assert one==two;assert json.loads(one)==json.loads(json.dumps(g.generate(count=5,seed=7712)))
selected=[]
for category in ['direct','positive-shift','negative-shift']:
    selected.append(next(r for r in records if ('direct' if r['generation']['parameters']['s']==0 else 'positive-shift' if r['generation']['parameters']['s']>0 else 'negative-shift')==category))
save('render-input.json',selected+[g.replay_source(mid) for mid in g.SOURCE_IDS])
save('validation-summary.json',{'passed':True,'math_questions':len(records),'coverage':coverage,
    'grading_checks':sum(len(c['checks']) for c in cases),'source_banks':4,'retained_after_delivery':len(accepted),
    'fixed_bank_role_proofs':probes,'relocation_and_determinism':True,
    'package_files':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in manifest['files']}})
print(json.dumps({'passed':True,'questions':len(records),'delivery':len(accepted),'coverage':coverage}))
