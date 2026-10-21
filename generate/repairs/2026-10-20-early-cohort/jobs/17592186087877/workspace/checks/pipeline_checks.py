"""Probe actual filtered records and verify relocatable runtime, without services."""
import hashlib,json,pathlib,shutil,subprocess,sys
import repair_checks as C
A=C.A; E=C.E
rows=A.load(E/'records.json');accepted=A.load(E/'delivery/accepted.json')
for r in accepted:A.math_check(r)
probes=C.probes(accepted)
assert len(accepted)==37
orbits=[]
for t in ['constant_cos','scaled_constant_power','signed_constant_power','constant_exp']:
    # First 20 records are the four five-target orbits. Compare by visible bank,
    # not publisher-assigned question/answer identities.
    originals=[r for r in rows[:20] if r['generation']['template']==t]
    survivors=[r for r in accepted if r['generation']['template']==t and C.bank(r)==C.bank(originals[0])]
    assert len({C.correct_value(r) for r in survivors})==5
    orbits.append({'template':t,'same_bank_distinct_keys_after_delivery':5})
# Reproduce question_selection.rs select() for a single rated easy candidate
# band with positive weight; entity IDs are synthetic because not published.
# Weight magnitude cancels within that band; second SHA256 draw selects pool.
selected=[]
for seed in range(64):
    digest=hashlib.sha256(f'course-academy/question-selection/v1/{seed}'.encode()).digest()
    u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53)
    selected.append(accepted[int(u*len(accepted))])
selection={'source':'engine/rust/question_selection.rs:122-200','engine_sha256':hashlib.sha256((A.REPO/'engine/rust/question_selection.rs').read_bytes()).hexdigest(),'candidate_count':len(accepted),'draws':len(selected),'distinct_selected':len({r['question'][':question/id'] for r in selected}),'probes':C.probes(selected),'limits':'Read-only synthetic fresh all-easy candidate pool, positive easy weight. No actual published entity IDs or learner history. Zero easy weight excludes this band; unconfigured policy deterministically selects first candidate. No claim about uncaptured/live inventory.'}
C.save('delivery-selection-results.json',{'input_probes':C.probes(rows),'accepted_probes':probes,'retained_counterfactual_orbits':orbits,'selection':selection})
# Native grading after normalization uses independently checked complete choices.
cases=[{'label':r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==A.key(r) else 'rejected','purpose':'Filtered printed equation equivalence'} for a in A.field(r)[':answer-field/choices']]} for r in accepted]
C.save('delivered-grader-input.json',cases)
manifest=A.load(A.PKG/'package.json');target=E/'relocated-runtime';target.mkdir(exist_ok=True)
for f in manifest['files']:
    p=target/f;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(A.PKG/f,p)
cli=['--difficulty','easy','--count','5','--seed','8173','--format','json']
def call(p):return subprocess.run([sys.executable,str(p)]+cli,capture_output=True,text=True,check=True).stdout
original=call(A.PKG/manifest['entrypoint']);relocated=call(target/manifest['entrypoint'])
assert original==relocated==call(target/manifest['entrypoint'])
(E/'cli-five-records.json').write_text(original)
for r in json.loads(original):A.math_check(r)
assert all('..' not in pathlib.Path(f).parts and not pathlib.Path(f).is_absolute() for f in manifest['files'])
assert manifest['dependencies']=={'python':sys.version.split()[0],'packages':{'sympy':A.S.__version__}}
rejections=[]
for label,kwargs in [('zero',{'parameters':{'a':'0','b':1}}),('large',{'parameters':{'a':'5','b':1}}),('wrong_band',{'template':'linear_sin'}),('wrong_field',{'field_type':'free'}),('invalid_bank',{'bank_coefficients':[1]*5})]:
    args={'template':'constant_cos',**kwargs}
    try:A.G.generate('easy',3,**args)
    except ValueError:rejections.append(label)
    else:raise AssertionError(label)
C.save('packaging-results.json',{'relocation_identical':True,'determinism_identical':True,'record_count':5,'dependencies_verified':manifest['dependencies'],'rejected_invalid_cases':rejections,'runtime_files':manifest['files'],'runtime_sha256':{f:hashlib.sha256((A.PKG/f).read_bytes()).hexdigest() for f in manifest['files']},'outputs':'stdout only; no assets required. Declared source files and SymPy are the only runtime dependencies.'})
print(json.dumps({'accepted_math_checked':len(accepted),'same_bank_orbits_retained':len(orbits),'relocated_cli_records':5,'selection_draws':len(selected),'distinct_selected':selection['distinct_selected']}))
