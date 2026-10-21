#!/usr/bin/env python3
"""Independent, read-only generator audit. Run with the job's Python interpreter.

All output goes beside this script. PYTHONDONTWRITEBYTECODE prevents package edits.
"""
import sys
sys.dont_write_bytecode = True
import collections, copy, hashlib, importlib.util, itertools, json, os, pathlib, re, shutil, subprocess

E = pathlib.Path(__file__).resolve().parent
JOB = E.parent
REPO = pathlib.Path('/home/jake/Developer/Course_Academy')
PKG = JOB / 'workspace'
PY = REPO / '.venv/bin/python'
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
def save(name, value):
    p=E/name; p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,indent=2)+'\n')
def hashes(root):
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
before=hashes(PKG)
sys.path.insert(0,str(PKG))
import generator as g
source=json.loads((JOB/'source/source.json').read_text())
inventory=json.loads((JOB/'source/inventory.json').read_text())
batch=json.loads((JOB/'samples.json').read_text())
save('runner-batch.json',batch)

def mat(text):
    bodies=re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)
    assert len(bodies)==1, ('expected one matrix',text)
    return [[int(x.strip()) for x in row.split('&')] for row in bodies[0].split('\\\\')]
def leading(a):
    return [next((i+1 for i,x in enumerate(row) if x!=0),None) for row in a]
def subset(value,n):
    if value=='All the columns are pivot':return tuple(range(1,n+1))
    return tuple(map(int,re.findall(r'\$(\d+)\$\s*(?:st|nd|rd|th)',value)))
def correct_value(f):
    ref=f[':answer-field/correct']; aid=ref[':answer/id'] if isinstance(ref,dict) else ref[1]
    return next(x[':answer/value'] for x in f[':answer-field/choices'] if x[':answer/id']==aid)
def selected(q):
    a=mat(q[':question/problem']); fields=q[':question/answer-fields']
    if len(fields)==1 and 'radio' in str(fields[0][':answer-field/type']):
        return subset(correct_value(fields[0]),len(a[0]))
    return tuple(sorted(int(re.match(r'Column (\d+):',f[':answer-field/key'])[1]) for f in fields if correct_value(f)=='true'))
def independent_check(r):
    q=r['question']; a=mat(q[':question/problem']); ls=leading(a); nz=[x for x in ls if x is not None]; n=len(a[0])
    assert ls==nz+[None]*(len(a)-len(nz)) and nz==sorted(set(nz)), 'not REF'
    assert selected(q)==tuple(nz), 'wrong answer'
    assert mat(q[':question/worked-solution'])==a, 'stale solution matrix'
    if not r['generation'].get('source_replay'):
        text=q[':question/worked-solution']; summary=text.split('We can see that',1)[1].split('column',1)[0]
        assert tuple(map(int,re.findall(r'\$(\d+)\$(?:st|nd|rd|th)',summary)))==tuple(nz), 'stale named columns'
        assert int(re.search(r'has \$(\d+)\$',summary)[1])==len(nz), 'wrong pivot count'
    fs=q[':question/answer-fields']
    if len(fs)>1:
        assert len(fs)==n
        assert {int(re.match(r'Column (\d+):',f[':answer-field/key'])[1]) for f in fs}==set(range(1,n+1))
        for f in fs:
            j=int(re.match(r'Column (\d+):',f[':answer-field/key'])[1])-1
            assert mat(f[':answer-field/key'])==[[row[j]] for row in a], 'stale answer vector'
            assert sorted(x[':answer/value'] for x in f[':answer-field/choices'])==['false','true']
    else:
        sets=[subset(x[':answer/value'],n) for x in fs[0][':answer-field/choices']]
        assert len(sets)==len(set(sets))==5 and sets.count(tuple(nz))==1
    return {'id':q[':question/id'],'shape':[len(a),n],'selected':nz,'profile':r['generation']['profile'],'template':r['generation']['template']}

# Original cases: compare problem and solution text after whitespace normalization,
# and every answer-field key, type, complete bank, and key. UUIDs are regenerated.
def plain(s):return re.sub(r'\s+',' ',s).strip()
def enum(v):return v[':db/ident'] if isinstance(v,dict) else v
def signature(q):
    fs=[]
    for f in q[':question/answer-fields']:
        fs.append((plain(f[':answer-field/key']),enum(f[':answer-field/type']),sorted(x[':answer/value'] for x in f[':answer-field/choices']),correct_value(f)))
    return sorted(fs)
replays=[]; replay_results=[]
for src in source['material']['kp'][':knowledge-point/questions']:
    profile=src[':question/math-academy-id']; r=g.generate(profile=profile,seed=82013,replay=True)
    q=r['question']; independent_check(r)
    result={'source_id':src[':question/id'],'profile':profile,'problem':plain(q[':question/problem'])==plain(src[':question/problem']), 'solution':plain(q[':question/worked-solution'])==plain(src[':question/worked-solution']), 'complete_answer_bank':signature(q)==signature(src)}
    assert all(result[k] for k in ['problem','solution','complete_answer_bank']),result
    replays.append(r); replay_results.append(result)
save('source-replays.json',replays)
save('source-replay-results.json',{'cases':replay_results,'canonical_gap':'Canonical example ccfdc303-534f-530e-810b-f475a997f5d8 has no captured answer controls or profile; same-method matrix tested separately as explicit parameters.'})

records=[]
for profile in sorted(g.SOURCES):
    for seed in [82013,97103,100019,203807,509239,777733]:
        records.append(g.generate(profile=profile,seed=seed))
    a=mat(g.SOURCES[profile][':question/problem']);m,n=len(a),len(a[0])
    # Independently construct leading/trailing/full-rank decisions; do not call g.targets.
    ts=[(1,),(n,),tuple(range(1,min(m,n)+1))] if g.kind(profile)=='checkbox' else [(1,2),(n-1,n),(1,3,5)]
    for target in ts:
        a=[[0]*n for _ in range(m)]
        for i,j in enumerate(target):
            a[i][j-1]=-9 if i%2 else 9
            for k in range(j,n):a[i][k]=(-1)**k*(k+1)
        records.append(g.generate(profile=profile,seed=91247,parameters={'matrix':a}))
for seed in range(49061,49101):records.append(g.generate(profile='q-130945',seed=seed))
many=g.generate_many('easy',64,seed=619739)
records.extend(many)
save('independent-samples.json',records)
save('many-64.json',many)
math_results=[independent_check(r) for r in records+batch+replays]
save('math-results.json',{'method':'Independent parse of displayed integer matrix; leading nonzero positions, REF invariants, vector banks, selected subsets and worked-solution claims. No generator pivots/target metadata used as oracle.','count':len(math_results),'failures':[],'cases':math_results})

# Controlled changes keep response format/profile/seed/most entries/bank fixed.
cf=[]
def pair(label,profile,a,b,kind,bank=None):
    pair=[]
    for matrix in [a,b]:
        params={'matrix':matrix}
        if bank is not None:params['bank']=bank
        pair.append(g.generate(profile=profile,seed=33071,parameters=params))
    for r in pair:independent_check(r)
    s=[selected(r['question']) for r in pair]
    assert (s[0]!=s[1]) if kind=='relevant' else (s[0]==s[1])
    cf.append({'label':label,'kind':kind,'responses':s,'records':pair})
ca=[[2,5,-1],[0,0,3],[0,0,0]]
cb=[[0,5,-1],[0,0,3],[0,0,0]]
ci=[[2,5,8],[0,0,3],[0,0,0]]
pair('checkbox-leading-position','q-35755',ca,cb,'relevant')
pair('checkbox-trailing-entry','q-35755',ca,ci,'irrelevant')
ra=[[2,5,-1,8,7],[0,4,6,-2,3],[0,0,0,-9,1],[0]*5,[0]*5]
rb=copy.deepcopy(ra);rb[1][1]=0
ri=copy.deepcopy(ra);ri[1][4]=-8
bank=[[1,2,4],[1,3,4],[1,2,5],[1,3,5],[2,3,4]]
pair('radio-leading-position','q-130945',ra,rb,'relevant',bank)
pair('radio-trailing-entry','q-130945',ra,ri,'irrelevant',bank)
canonical=source['material']['kp'][':knowledge-point/canonical-example']
canonical_record=g.generate(profile='q-73605',seed=33071,parameters={'matrix':mat(canonical[':question/problem'])})
independent_check(canonical_record)
save('canonical-matrix.json',[canonical_record])
save('counterfactuals.json',cf)
cf_records=[r for p in cf for r in p['records']]
save('counterfactual-records.json',cf_records)

# Batch all genuine learner-grade checks into a single executable invocation.
grade=[]
for label,rs in [('batch',batch),('source',replays),('counterfactual',cf_records),('boundary',[records[i*9+6] for i in range(len(g.SOURCES))])]:
    for i,r in enumerate(rs):
        checks=[];q=r['question'];a=mat(q[':question/problem']);wanted=tuple(x for x in leading(a) if x)
        for fi,f in enumerate(q[':question/answer-fields']):
            for choice in f[':answer-field/choices']:
                if enum(f[':answer-field/type']).endswith('/checkbox'):
                    col=int(re.match(r'Column (\d+):',f[':answer-field/key'])[1]);good=(choice[':answer/value']=='true')==(col in wanted)
                else:good=subset(choice[':answer/value'],len(a[0]))==wanted
                checks.append({'field_index':fi,'submitted_answer_id':choice[':answer/id'],'expected':'accepted' if good else 'rejected','purpose':'Independent visible-matrix decision; test every true/false choice or every radio distractor'})
        grade.append({'label':f'{label}-{i}','record':r,'checks':checks})
# Submit the before-answer to after-record too, using its own choice UUIDs.
for p in cf:
    old=selected(p['records'][0]['question']);after=p['records'][1];checks=[]
    for fi,f in enumerate(after['question'][':question/answer-fields']):
        if enum(f[':answer-field/type']).endswith('/checkbox'):
            col=int(re.match(r'Column (\d+):',f[':answer-field/key'])[1]);value=str(col in old).lower()
            choice=next(x for x in f[':answer-field/choices'] if x[':answer/value']==value)
            actual=selected(after['question']);good=(col in old)==(col in actual)
        else:
            choice=next(x for x in f[':answer-field/choices'] if subset(x[':answer/value'],5)==old)
            good=old==selected(after['question'])
        checks.append({'field_index':fi,'submitted_answer_id':choice[':answer/id'],'expected':'accepted' if good else 'rejected','purpose':f"{p['kind']} dependency: transfer before-response to after-record"})
    grade.append({'label':p['label']+'-transfer','record':after,'checks':checks})
save('grader-input.json',grade)
save('render-records.json',batch+cf_records+[replays[-1],canonical_record])

# Validation of explicit generator rejections, determinism, finite batch domain,
# relocation, manifest runtime, external output, and unchanged package.
reject=[]
def bad(label,fn):
    try:fn()
    except (ValueError,KeyError,TypeError) as e:reject.append({'case':label,'outcome':'rejected','error':str(e)});return
    raise AssertionError('invalid input accepted: '+label)
bad('unsupported level',lambda:g.generate(level='hard'))
bad('unknown profile',lambda:g.generate(profile='missing'))
bad('wrong response type',lambda:g.generate(profile='q-35755',field_type='radio'))
bad('zero matrix',lambda:g.generate(profile='q-35755',parameters={'matrix':[[0]*3 for _ in range(3)]}))
bad('zero row above nonzero row',lambda:g.generate(profile='q-35755',parameters={'matrix':[[0,0,0],[0,1,0],[0,0,0]]}))
bad('repeated pivot column',lambda:g.generate(profile='q-35755',parameters={'matrix':[[1,0,0],[1,1,0],[0,0,0]]}))
bad('decreasing pivot columns',lambda:g.generate(profile='q-35755',parameters={'matrix':[[0,1,0],[1,0,0],[0,0,0]]}))
bad('out of coefficient range',lambda:g.generate(profile='q-35755',parameters={'matrix':[[10,0,0],[0,0,0],[0,0,0]]}))
bad('float coefficient',lambda:g.generate(profile='q-35755',parameters={'matrix':[[1.0,0,0],[0,0,0],[0,0,0]]}))
bad('wrong shape',lambda:g.generate(profile='q-35755',parameters={'matrix':[[1,0],[0,0]]}))
bad('duplicate bank',lambda:g.generate(profile='q-130945',parameters={'matrix':ra,'bank':[[1,2,4]]*5}))
bad('bank omits target',lambda:g.generate(profile='q-130945',parameters={'matrix':ra,'bank':[[1,2,3],[1,2,5],[1,3,4],[1,3,5],[2,3,4]]}))
bad('negative count',lambda:g.generate_many('easy',-1,seed=42))
bad('over finite capacity',lambda:g.generate_many('easy',999,seed=42))
assert records[0]==g.generate(profile=records[0]['generation']['profile'],seed=82013)
assert many==g.generate_many('easy',64,seed=619739)
assert g.generate_many('easy',0,seed=9)==[]
for r in batch:
    gen=r['generation'];again=g.generate(profile=gen['profile'],seed=gen['seed'],parameters=gen['parameters']);assert again['generation']==gen and signature(again['question'])==signature(r['question']) and again['question'][':question/id']==r['question'][':question/id']

assert g.generate_many('easy',len(batch),seed=batch[0]['generation']['seed'])==batch
relocated=E/'relocated-package';relocated.mkdir(exist_ok=True)
for name in before:shutil.copyfile(PKG/name,relocated/name)
cmd=[str(PY),str(relocated/'generator.py'),'--seed','619739','--count','5']
proc=subprocess.run(cmd,env=ENV,cwd=E,capture_output=True,text=True,check=True)
relocated_records=json.loads(proc.stdout)
assert relocated_records==g.generate_many('easy',5,seed=619739)
save('relocated-records.json',relocated_records)
runtime=subprocess.run([str(PY),'-c','import sys,json;print(json.dumps({"python":sys.version.split()[0]}))'],env=ENV,capture_output=True,text=True,check=True)
versions=json.loads(runtime.stdout);manifest=json.loads((PKG/'package.json').read_text())
assert versions['python']==manifest['dependencies']['python']
assert manifest['dependencies']['packages']=={}
assert hashes(PKG)==before,'package changed'
save('packaging-results.json',{'python':versions,'manifest':manifest,'package_before':before,'package_after':hashes(PKG),'deterministic_replay':True,'runner_batch_explicit_replay':'Same content, bank and key; radio choice order changes because supplying bank skips RNG sampling. Original generate_many call reproduces exact batch.','relocation_command':cmd,'relocation_matches':True,'external_output':'CLI JSON parsed; no external assets required; relocation output and all artifacts under evidence_root','rejections':reject,'resampling':'Nonempty target chosen by construction. No rejection conditioning of randomly sampled eligible decisions; policy wrapper returns valid calls unchanged. Finite structural batch domain shuffled without replacement; oversize request raises.'})

# Inventory: inspect visible math and controls; only source-free records are generated.
# Do not invent provenance for originals or assert absent historical metadata.
inv_results=[]; reproduced=[]
for q in inventory['questions']:
    a=mat(q[':question/problem']);target=tuple(x for x in leading(a) if x)
    assert selected(q)==target,('inventory wrong key',q[':question/id'])
    if q.get(':question/math-academy-id'):
        inv_results.append({'id':q[':question/id'],'kind':'original source','correct':True});continue
    candidate=None
    for profile,src in g.SOURCES.items():
        if len(mat(src[':question/problem']))!=len(a) or len(mat(src[':question/problem'])[0])!=len(a[0]):continue
        params={'matrix':a}
        if g.kind(profile)=='radio':params['bank']=[list(subset(c[':answer/value'],len(a[0]))) for c in q[':question/answer-fields'][0][':answer-field/choices']]
        try:r=g.generate(profile=profile,seed=0,parameters=params)
        except ValueError:continue
        if r['question'][':question/id']==q[':question/id']:
            assert signature(q)==signature(r['question'])
            assert plain(q[':question/worked-solution'])==plain(r['question'][':question/worked-solution'])
            candidate=r;break
    inv_results.append({'id':q[':question/id'],'entity_id':q[':db/id'],'kind':'generated','correct':True,'current_content_identity_reproduced':candidate is not None,'provenance_limit':'Captured inventory has no historical generation metadata; seed 0 is a controlled reconstruction, not asserted historical seed.'})
    if candidate:reproduced.append(candidate)
save('inventory-reproductions.json',reproduced)
save('inventory-results.json',{'basis':inventory['basis'],'cases':inv_results,'finding_scope':'All 21 stored questions have correct pivot-selection keys. Five source-free records tested for current content replay; historical metadata absent. No affected weakness demonstrated yet.'})
save('affected-inventory.json',{'affected_questions':[]})
save('audit-summary.json',{'source_replays':len(replays),'independent_samples':len(records),'math_cases':len(math_results),'counterfactual_pairs':len(cf),'native_grader_case_count':len(grade),'render_records':len(batch+cf_records+[replays[-1],canonical_record]),'package_unchanged':hashes(PKG)==before})
(E/'session-state.md').write_text('Independent source analysis saved first. audit.py completed: original replays, independent math checks, controlled pairs, rejection/determinism/relocation/runtime and captured-inventory inspection passed. Pending delivery, actual grader, actual UI rendering, shortcut/selection analysis and final report.\n')
print(json.dumps(json.loads((E/'audit-summary.json').read_text())))
