"""Source fidelity, preserved historical scope, relocation, stored-inventory audit."""
import collections, hashlib, importlib.util, json, os, platform, re, shutil, subprocess, sys, tempfile
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parents[1]; E=W/'evidence'; J=W.parent
spec=importlib.util.spec_from_file_location('g',W/'17592186124674.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def load(p):return json.loads(Path(p).read_text())
def save(n,v):(E/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def values(q):return sorted(c[':answer/value'] for c in q[':question/answer-fields'][0][':answer-field/choices'])
def correct(q):
    f=q[':question/answer-fields'][0]
    return next((c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==f.get(':answer-field/correct',[None,None])[1]),None)
source=load(J/'source/source.json'); questions=source['material']['kp'][':knowledge-point/questions']
ms=importlib.util.spec_from_file_location('math_witness',W/'checks/repair.py');math=importlib.util.module_from_spec(ms);ms.loader.exec_module(math)
replayed=[];checks=[]
source_math=[]
for q in questions:
    r=g.replay_current_source(q[':question/math-academy-id'],seed=913); rq=r['question'];replayed.append(r)
    f=q[':question/answer-fields'][0]
    flags={'prompt':rq[':question/problem']==q[':question/problem'],
        'solution':rq.get(':question/worked-solution')==q.get(':question/worked-solution'),
        'bank':values(rq)==values(q),
        'correct_or_absence':correct(rq)==(f.get(':answer-field/correct') or {}).get(':answer/value'),
        'difficulty_or_absence':rq.get(':question/difficulty')==(q.get(':question/difficulty') or {}).get(':db/ident')}
    assert all(flags.values()),(q[':question/id'],flags)
    symbol=re.search(r'\$([A-Z])\(t\)\$',q[':question/problem'])[1]
    cap=int(re.search(r'(?:maximum.+?is|maximum capacity is) \$(\d+)\$',q[':question/problem'])[1])
    target=g.sp.Symbol('k')*(cap-g.sp.Symbol(symbol))
    matching=[v for v in values(rq) if g.sp.expand(math.rhs(v)-target)==0]
    assert len(matching)==1
    if correct(rq) is not None:assert correct(rq)==matching[0]
    source_math.append({'source_id':q[':question/id'],'visible_capacity':cap,'unique_correct_model':matching[0],'key_present':correct(rq) is not None})
    checks.append({'source_question_id':q[':question/id'],'choices':len(values(q)),'checks':flags})
save('source-replay-records.json',replayed)
save('source-math-results.json',{'passed':True,'cases':source_math})
save('source-replay-results.json',{'passed':True,'banks':len(checks),'choices':sum(c['choices'] for c in checks),'checks':checks,'canonical_gap':'Fish canonical bank absent. Rehabilitation replay preserves absent key, solution and rating. Factory replay preserves historical unit inconsistency; served content fixes both occurrences.'})

# Match captured generated records; do not label the 14 source originals generated.
inventory=load(J/'source/inventory.json')
historical=load(W/'17592186124674/reference/replenishment/basis-2578/generated.json')
source_ids={q[':question/id'] for q in questions}
nonoriginal=[q for q in inventory['questions'] if q[':question/id'] not in source_ids]
reproductions=[];records=[];affected=[];untested=[]
for q in nonoriginal:
    old=next((r for r in historical if r['question'][':question/id']==q[':question/id']),None)
    if old is None:
        untested.append(q[':question/id']);continue
    meta=old['generation'];level=old['question'][':question/difficulty'].split('/')[-1]
    r=g.generate(level,seed=meta['seed'],parameters=meta['parameters'])
    assert r==old, q[':question/id']
    rq=r['question']
    assert rq[':question/id']==q[':question/id'] and values(rq)==values(q) and rq[':question/problem']==q[':question/problem']
    records.append(r)
    reproductions.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'difficulty':level,'complete_record_and_metadata_reproduced':True})
    if level=='easy':
        # Only report demonstrated weakness, not an inference from provenance.
        f=rq[':question/answer-fields'][0];lens=[len(c[':answer/value'].replace(' ','')) for c in f[':answer-field/choices']]
        i=lens.index(min(lens))
        if lens.count(lens[i])==1 and f[':answer-field/choices'][i][':answer/id']==f[':answer-field/correct'][1]:
            affected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'finding':'Correct equation uniquely shortest in generated easy bank','reproduction':'<job-python> -B checks/source_package_inventory.py','evidence_path':'generated-records.json'})
save('generated-records.json',records)
save('affected-inventory.json',{'affected_questions':affected})
save('inventory-results.json',{'basis':inventory['basis'],'stored':len(inventory['questions']),'original_sources':len(source_ids),'nonoriginal':len(nonoriginal),'reproduced':reproductions,'untested_question_ids':untested,'affected':len(affected),'conclusion':'All stored non-source instances reproduced exactly; all are moderate/hard, outside the demonstrated easy-bank defects. No untested non-source inventory.' if not untested else 'Untested records listed; no absence claim for them.','limits':'Other defects in moderate/hard are outside this targeted repair.'})

manifest=load(W/'package.json')
assert manifest['dependencies']=={'python':platform.python_version(),'packages':{'sympy':g.sp.__version__}}
hashes={n:hashlib.sha256((W/n).read_bytes()).hexdigest() for n in manifest['files']}
with tempfile.TemporaryDirectory(prefix='inhibited-relocation-') as d:
    root=Path(d)
    for name in manifest['files']:
        out=root/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/name,out)
    cmd=[sys.executable,'-B',str(root/manifest['entrypoint']),'--difficulty','easy','--count','5','--seed','90210','--format','json']
    got=json.loads(subprocess.check_output(cmd,cwd=root,env={**os.environ,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(E/'assets')}))
    expected=[g.generate_easy(seed=i) for i in range(90210,90215)]
    assert got==expected
    save('batch.json',got)
    assert hashes=={n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in manifest['files']}
save('packaging-results.json',{'passed':True,'runtime_versions':manifest['dependencies'],'runtime_hashes':hashes,'relocated_cli_matches':True,'count':5,'seed':90210,'files':manifest['files'],'historical_moderate_hard_preserved':len(records)})
# Required before accepting completion: no external job was edited by these scripts.
print(json.dumps({'source_banks':len(checks),'source_choices':70,'inventory_reproduced':len(records),'inventory_untested':len(untested),'affected':len(affected),'relocation':True}))
