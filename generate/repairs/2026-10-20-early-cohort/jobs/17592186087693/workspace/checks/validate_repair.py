"""Targeted current-package controls, independent visible-matrix checks and evidence."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from replay_completeness import ROOT, generator as g, check_math, correct, enum, matrix, norm
E = ROOT/'evidence'

def save(name, data):
    (E/name).write_text(json.dumps(data, indent=2)+'\n')

def values(rec):
    return [correct(f) for f in rec['question'][':question/answer-fields']]

def probes(records):
    result = {}
    for t in g.TEMPLATES:
        rs = [r for r in records if r['generation']['template'] == t]
        shapes = [check_math(r) for r in rs]
        d = {'count': len(rs), 'semantic_shapes': sorted(set(shapes)), 'copy_rows_to_columns': sum(r == c for r,c in shapes), 'copy_baseline': '1/5 for uniform independent columns'}
        if t == 'radio':
            positions = Counter()
            wins = Counter()
            for rec in rs:
                q = rec['question']; f = q[':question/answer-fields'][0]; bank = f[':answer-field/choices']; key = norm(correct(f))
                positions[next(i for i,a in enumerate(bank) if norm(a[':answer/value']) == key)] += 1
                pairs = lambda a: tuple(map(int, norm(a[':answer/value']).split('\\times')))
                for cue, a in [('first', bank[0]), ('last', bank[-1]), ('smallest', min(bank,key=pairs)), ('largest', max(bank,key=pairs))]:
                    wins[cue] += norm(a[':answer/value']) == key
            d.update(correct_positions=dict(positions), cue_success=dict(wins), baseline=0.2)
        result[t] = d
    return result

controls = []
control_results = []
bank = [(2,3),(3,3),(2,4),(5,6),(6,4)]
for t in g.TEMPLATES:
    kw = {'seed': 1218, 'template': t}
    if t == 'radio': kw['bank'] = bank
    base = [[1,2,3],[4,5,6]]
    variants = [({'name':'A','entries':base},(2,3)),
                ({'name':'A','entries':base+[[7,8,9]]},(3,3)),
                ({'name':'A','entries':[[1,2,3,7],[4,5,6,8]]},(2,4)),
                ({'name':'Z','entries':[[0,-2,r'\sqrt{2}'],[0,0,r'\frac{1}{3}']]},(2,3))]
    rs = [g.generate(parameters=p, **kw) for p, shape in variants]
    assert [check_math(r) for r in rs] == [shape for p,shape in variants]
    assert values(rs[0]) == values(rs[3])
    assert values(rs[0]) != values(rs[1]) and values(rs[0]) != values(rs[2])
    controls.extend(rs)
    control_results.append({'template':t,'rows_change':True,'columns_change':True,'irrelevant_preservation':True,'values':[values(r) for r in rs]})
# Changed family: exhaustive supported shape domain with a fixed name and entries.
chelsea = [g.generate(template='chelsea-dual-blank', seed=11, parameters={'name':'P','entries':[[0]*c for _ in range(r)]}) for r in range(2,7) for c in range(2,7)]
assert {check_math(r) for r in chelsea} == {(r,c) for r in range(2,7) for c in range(2,7)}
# Small regression sample of unchanged families and the restored normal template.
samples = [g.generate(template=t, seed=47219+i) for t in g.TEMPLATES for i in range(8)]
replays = json.loads((E/'source-replays.json').read_text())
batch = json.loads((E/'prospective-batch.json').read_text())
assert len(batch) == len({check_math(r) for r in batch}) == 5
allrecs = replays + controls + chelsea + samples + batch
for rec in allrecs: check_math(rec)
save('counterfactual-records.json', controls)
save('counterfactual-results.json', control_results)
save('chelsea-domain.json', chelsea)
save('small-sample.json', samples)
# Delivery controls contain fresh normal records; replay is audited separately.
save('delivery-input.json', controls + chelsea + samples)
save('math-results.json', {'passed':True,'records':len(allrecs),'source_replays':len(replays),'chelsea_shapes':25,'prospective_shapes':[check_math(r) for r in batch]})
# Same input/output under relocation, with only declared runtime files.
manifest = json.loads((ROOT/'package.json').read_text())
actual = {'python':sys.version.split()[0],'packages':{'sympy':g.sp.__version__}}
assert manifest['dependencies'] == actual
args = ['--difficulty','easy','--count','5','--seed','928264887','--format','json']
with tempfile.TemporaryDirectory(dir=E) as tmp:
    tmp = Path(tmp)
    for name in manifest['files']:
        (tmp/name).parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/name,tmp/name)
    relocated = subprocess.run([sys.executable,'-B',str(tmp/'generator.py')]+args,cwd=tmp,capture_output=True,text=True,check=True)
    assert json.loads(relocated.stdout) == batch
save('packaging-results.json',{'relocation':True,'deterministic_cli_replay':True,'dependencies':actual,'runtime_files':manifest['files']})
# Native grader assertions: expected responses derived only from visible matrix.
cases = []
for i, rec in enumerate(replays + controls + batch):
    dims = check_math(rec); checks = []
    for j,f in enumerate(rec['question'][':question/answer-fields']):
        if enum(f[':answer-field/type']).endswith('/radio'):
            for a in f[':answer-field/choices']:
                checks.append({'field_index':j,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if norm(a[':answer/value']) == f'{dims[0]}\\times{dims[1]}' else 'rejected'})
        else:
            n = dims[j]
            for v in [str(n),f'{n}.0',f'{2*n}/2',f'\\frac{{{2*n}}}{{2}}']:
                checks.append({'field_index':j,'submitted':v,'expected':'accepted'})
            for v in set([str(n+1),'0']+([str(dims[1-j])] if dims[1-j]!=n else [])):
                checks.append({'field_index':j,'submitted':v,'expected':'rejected'})
    cases.append({'label':f'visible-matrix-{i}','record':rec,'checks':checks})
save('grader-input.json',cases)
# One restored source and its row/column/irrelevant controls, plus current radio.
source = next(r for r in replays if r['generation']['bank_profile']=='observed-q-139628')
save('render-input.json',[source]+controls[-4:]+[next(r for r in samples if r['generation']['template']=='radio')])
# Stored capture: original replay omission cannot be a generated stored defect.
inv = json.loads((ROOT.parent/'source/inventory.json').read_text())
inventory_results=[]
for q in inv['questions']:
    shape=check_math({'question':q})
    inventory_results.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'shape':shape,'retired':q.get(':question/retired',False),'original':':question/math-academy-id' in q,'dimensions_correct':True})
save('inventory-results.json',{'basis':inv['basis'],'records':inventory_results,'finding':'No stored counterpart to omitted replay profile. Captured matrix dimensions, keys and solutions independently checked. No generation provenance fabricated.'})
save('affected-inventory.json',{'affected_questions':[]})
save('pre-delivery-probes.json',{'prospective':probes(batch),'controls_and_sample':probes(controls+chelsea+samples)})
print(json.dumps({'math_records':len(allrecs),'grader_cases':len(cases),'inventory_checked':len(inventory_results),'relocation':True}))
