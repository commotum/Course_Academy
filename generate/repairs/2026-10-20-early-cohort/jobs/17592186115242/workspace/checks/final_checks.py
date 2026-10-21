"""Post-filter witnesses, controlled template pairs, relocation, and selection.

Run after validate_repair.py and the shared delivery checks.
"""
import collections
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
sys.dont_write_bytecode = True
from validate_repair import W,E,g,s,field,value,root,probes,printed_check,write

PY = sys.executable
sample = json.loads((E/'samples.json').read_text())
accepted = json.loads((E/'delivery/accepted.json').read_text())
batch = json.loads((E/'delivery-batch/accepted.json').read_text())
before = probes([r for r in sample if r['question'][':question/difficulty'].endswith('/easy')])
after = probes(accepted)
assert before == after
for name,z in after.items():
    assert z['sign_extremum_successes'] < z['total']
    assert len(z['numeric_ranks']) == 5
assert next(iter(probes(batch).values()))['sign_extremum_successes'] < len(batch)
write('post-delivery-shortcuts.json',dict(passed=True,before=before,after=after,batch=probes(batch),interpretation='All five numeric roles survive filtering in both easy sign groups. No fixed rank, position, template or sign-extremum rule solves the sampled family. These finite probes do not establish absence of every possible shortcut.'))

coverage = {}; pairs = []; pair_report = []
for level, templates in g.TEMPLATES.items():
    for template in templates:
        records = [r for r in sample if r['generation']['template']==template]
        coverage[template] = dict(samples=len(records),semantic_instances=len({r['generation']['math_fingerprint'] for r in records}),slot_values={slot:sorted({r['generation']['parameters'][slot] for r in records}) for slot in 'a b c d u v e'.split()},numeric_roles=probes(records))
        base = records[0]; p = base['generation']['parameters']; new = g.generate(level,seed=base['generation']['seed'],template=template,parameters=dict(p,b=-p['b']))
        assert printed_check(base) != printed_check(new)
        assert all(p[slot]==new['generation']['parameters'][slot] for slot in 'a c d u v e'.split())
        assert base['question'][':question/problem'] != new['question'][':question/problem']
        assert base['question'][':question/worked-solution'] != new['question'][':question/worked-solution']
        pair_report.append(dict(template=template,change='negate b; all other coefficients and seed fixed',roots=[str(root(base)),str(root(new))],passed=True))
        pairs += [base,new]
write('template-counterfactual-records.json',pairs)
write('coverage.json',dict(passed=True,templates=coverage,counterfactuals=pair_report))

# Observe actual sampler attempts without altering files or replacing validation.
original_sample = g.sample
rejection = []
for level,templates in g.TEMPLATES.items():
    for template in templates:
        attempted=[];accepted_roots=[];invalid=collections.Counter()
        def traced(l,t,rng):
            p=original_sample(l,t,rng);attempted.append(p)
            try:g.validate_parameters(l,t,p)
            except ValueError as exc:invalid[str(exc)]+=1
            return p
        g.sample=traced
        try:
            for seed in range(4):
                r=g.generate(level,seed=seed,template=template)
                accepted_roots.append(str(printed_check(r)))
        finally:g.sample=original_sample
        assert len(attempted)-sum(invalid.values())==4
        rejection.append(dict(template=template,attempts=len(attempted),delivered=4,domain_rejections=dict(invalid),bank_rejections=0,roots=accepted_roots))
write('rejection-results.json',dict(passed=True,cases=rejection,zero_root_reachability='All shift-capable templates separately exercised in boundary-records.json; bank collisions never reject these valid systems.'))

# Reproduce the selector's conditional within-easy draw; exact future entity IDs
# and actual learner policy/history do not exist in this offline author context.
inventory=json.loads((E/'generated-records.json').read_text())
inv_ids={q[':question/id']:q[':db/id'] for q in json.loads((W.parent/'source/inventory.json').read_text())['questions']}
old=sorted(inventory,key=lambda r:inv_ids[r['question'][':question/id']])
pool=old+accepted
selection=[]
for seen_prefix in [0,5,9]:
    candidates=pool[seen_prefix:];drawn=[]
    for n in range(64):
        seed=f'author-repair-{n}'
        digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
        u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53)
        drawn.append(candidates[int(u*len(candidates))])
    z=next(iter(probes(drawn).values()))
    selection.append(dict(seen_prefix=seen_prefix,candidate_count=len(candidates),draws=64,sign_extremum_successes=z['sign_extremum_successes'],numeric_roles=z['numeric_ranks']))
write('selection-results.json',dict(cases=selection,source='engine/rust/question_selection.rs:select and seen_before_task, inspected read-only',limits=['Conditional on a positive easy-band weight; actual policy/history unavailable.','Future IDs approximated by append order, so these are sensitivity probes, not predictions of actual reservations.','Five existing weak easy records remain unchanged for runner review; their selection can still expose the historical weakness. Unconfigured policies select the first candidate.']))

manifest=json.loads((W/'package.json').read_text())
assert manifest['dependencies']==dict(python='3.13.5',packages={'sympy':s.__version__})
assert set(manifest['files'])=={'17592186115242.py','math_format.py','17592186115242/recipes.json','requirements.txt'}
args=['--difficulty','easy','--count','5','--seed','1475864943','--format','json']
run=subprocess.run([PY,'-B',str(W/manifest['entrypoint']),*args],check=True,capture_output=True,text=True,cwd='/tmp')
assert json.loads(run.stdout)==json.loads((E/'batch.json').read_text())
with tempfile.TemporaryDirectory(prefix='course-academy-relocation-',dir=E) as tmp:
    dest=pathlib.Path(tmp)
    for rel in manifest['files']:
        p=dest/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/rel,p)
    # Clear PYTHONPATH and run outside the repository; helpers resolve from
    # the relocated entrypoint directory through normal Python script imports.
    relocated=subprocess.run([PY,'-B',str(dest.resolve()/manifest['entrypoint']),*args],check=True,capture_output=True,text=True,cwd='/tmp',env={**os.environ,'PYTHONPATH':'','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str((E/'assets').resolve())})
    assert json.loads(relocated.stdout)==json.loads(run.stdout)
hashes={rel:hashlib.sha256((W/rel).read_bytes()).hexdigest() for rel in manifest['files']}
write('packaging.json',dict(passed=True,deterministic_relocated_cli=True,manifest_dependencies=manifest['dependencies'],runtime_hashes=hashes,working_directory='/tmp',count=5,seed=1475864943))

grader=json.loads((E/'grader-input.json').read_text())
for i,r in enumerate(batch+pairs):
    t=root(r)
    grader.append(dict(label=f'post-delivery-or-template-pair-{i}',record=r,checks=[dict(submitted_answer_id=a[':answer/id'],expected='accepted' if value(a)==t else 'rejected',purpose='independent printed-system witness after delivery or controlled coefficient change') for a in field(r)[':answer-field/choices']]))
write('grader-complete-input.json',grader)
print(json.dumps(dict(passed=True,delivery_accepted=len(accepted),batch_accepted=len(batch),template_pairs=len(pair_report),grader_records=len(grader),packaging=True)))
