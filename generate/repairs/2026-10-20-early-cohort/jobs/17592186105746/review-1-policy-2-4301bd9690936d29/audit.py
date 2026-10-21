"""Independent revision audit. Run with the job Python; all writes stay here."""
import os, sys, json, re, hashlib, platform, shutil, subprocess
from pathlib import Path
sys.dont_write_bytecode = True
import review as R
from math_format import normalize_tex
E, J, P, g = R.ROOT, R.JOB, R.PKG, R.g
S, x, y = R.S, R.x, R.y
save = R.save

def key(r):
    f=r['question'][':question/answer-fields'][0]
    return f[':answer-field/choices'][R.correct_index(r)][':answer/value']

def canonical(s):
    s=normalize_tex(s)
    s=s.replace(r'\left[\begin{array}{cc|c}',r'\begin{bmatrix}').replace(r'\end{array}\right]',r'\end{bmatrix}')
    return R.normalize(s)

def check(r):
    result=R.mathcheck(r)
    assert result['passed'], result
    q=r['question']; a=R.equations(q); f=q[':question/answer-fields'][0]
    assert a.shape==(2,3) and a[:,:2].rank()==1 and a[0,0]!=0
    assert f[':answer-field/type']==':answer-field.type/radio' and len(f[':answer-field/choices'])==5
    signatures=[]
    for c in f[':answer-field/choices']:
        v=c[':answer/value']
        signatures.append(('none',) if v=='No solution' else tuple(S.expand(z) for z in R.mats(v)[1]))
    assert len(set(signatures))==5
    expected=a[1,2]-a[1,0]*a[0,2]/a[0,0]
    ms=[m for m in R.mats(q[':question/worked-solution']) if m.shape==(2,3)]
    assert ms[-1]==S.Matrix([[1,a[0,1]/a[0,0],a[0,2]/a[0,0]],[0,0,expected]])
    for before,after in zip(ms,ms[1:]):
        norm=before.copy(); norm[0,:]=before[0,:]/before[0,0]
        elim=before.copy(); elim[1,:]-=before[1,0]/before[0,0]*before[0,:]
        assert after==before or after==norm or after==elim
    assert len(result['reduced_scalar_checks'])>=1
    meta=r['generation']
    replay=g.generate(q[':question/difficulty'].split('/')[-1],meta['seed'],meta['template'],meta['parameters'])
    assert replay==r, 'generation metadata must exactly replay authored record'
    result['consistent']=bool(expected==0)
    return result

def main():
    sources=json.loads((J/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']
    replay=[]; replay_results=[]
    for old in sources:
        sid=old[':question/math-academy-id'];level=old[':question/difficulty'][':db/ident'].split('/')[-1]
        r=g.generate(level,7331,sid,{'rhs_scale':1}); q=r['question'];sf=old[':question/answer-fields'][0]
        assert canonical(q[':question/problem'])==canonical(old[':question/problem'])
        assert sorted(canonical(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices'])==sorted(canonical(a[':answer/value']) for a in sf[':answer-field/choices'])
        assert canonical(key(r))==canonical(sf[':answer-field/correct'][':answer/value'])
        expected=old[':question/worked-solution']
        if sid=='q-42159':expected=expected.replace(r'1 & 7 & 4 \\ 6 & 42 & -24',r'1 & 7 & 4 \\ 6 & 42 & 24')
        if sid=='q-130924':expected=expected.replace(r'-3 & 10 & 6',r'-3 & 12 & 6')
        assert canonical(q[':question/worked-solution'])==canonical(expected),sid
        replay.append(r);replay_results.append({'source_id':old[':question/id'],'template':sid,'prompt':True,'complete_bank':True,'key':True,'corrected_solution':True})
    save('source-replay-records.json',replay);save('source-replay.json',replay_results)
    controlled=[]; pairs=[]; random_records=[]
    for old in sources:
        sid=old[':question/math-academy-id'];level=old[':question/difficulty'][':db/ident'].split('/')[-1]
        for c in [-7,0,7]:
            pair=[g.generate(level,92871,sid,{'intercept':c,'residual':delta}) for delta in [0,-5 if c<0 else 5]]
            a,b=[R.equations(r['question']) for r in pair]
            assert a[:,:2]==b[:,:2] and a[0,:]==b[0,:] and a[1,2]!=b[1,2]
            assert pair[0]['question'][':question/answer-fields']==pair[1]['question'][':question/answer-fields'] or [a[':answer/value'] for a in pair[0]['question'][':question/answer-fields'][0][':answer-field/choices']]==[a[':answer/value'] for a in pair[1]['question'][':question/answer-fields'][0][':answer-field/choices']]
            assert key(pair[0])!='No solution' and key(pair[1])=='No solution'
            pairs.append({'template':sid,'intercept':c,'records':[len(controlled),len(controlled)+1],'changed':'only second RHS; fixed coefficients, first RHS, seed, and complete ordered bank','outcomes':['infinite','none']})
            controlled.extend(pair)
        random_records.extend(g.generate(level,seed,sid) for seed in [92871,92872,92873,92874])
    exact=[g.generate('easy',7331,'q-42157',{'intercept':2,'second_rhs':v}) for v in [-10,-8,-5]]
    assert [key(r)=='No solution' for r in exact]==[True,False,True]
    assert key(exact[0])==key(exact[2]) and R.mats(key(exact[1]))[1]==S.Matrix([2+6*y,y])
    scale=[g.generate('easy',7331,'q-42157',{'rhs_scale':t}) for t in [-4,-3,-2,-1,1,2,3,4]]
    assert {key(r)=='No solution' for r in scale}=={True,False}
    bounds=[g.generate('easy',19387,'q-20964',{'intercept':c,'residual':d}) for c,d in [(-32,-32),(32,32),(0,0)]]
    constructor=g.batch('easy',72,92871)
    prefix=[]
    for i in range(1440):
        prefix.append(g.generate('easy',92871+i*104729))
        if len({r['generation']['mathematical_fingerprint'] for r in prefix})==72:break
    assert [r for i,r in enumerate(prefix) if r['generation']['mathematical_fingerprint'] not in {z['generation']['mathematical_fingerprint'] for z in prefix[:i]}]==constructor
    batch=json.loads((J/'samples.json').read_text())
    save('controlled-records.json',controlled);save('random-records.json',random_records);save('counterfactual-records.json',exact);save('scale-records.json',scale);save('boundary-records.json',bounds);save('constructor-records.json',constructor);save('constructor-prefix.json',prefix);save('batch-records.json',batch)
    save('counterfactual-results.json',{'command':f'{sys.executable} {E}/audit.py','controlled_pairs':pairs,'exact_relevant_pair':{'before_index':0,'after_index':1,'expected':'No solution -> x=2+6y, y free','passed':True},'irrelevant_pair':{'before_index':0,'after_index':2,'expected':'Changing nonzero residual -2 to +3 preserves No solution','passed':True},'scale_regression':{'outcomes':sorted({key(r)=='No solution' for r in scale}),'passed':True}})
    all_records=replay+controlled+random_records+exact+scale+bounds+constructor+batch
    checked=[check(r) for r in all_records]
    save('math-results.json',{'command':f'{sys.executable} {E}/audit.py','count':len(checked),'passed':True,'checks':checked})
    grade=[]
    for i,(r,c) in enumerate(zip(all_records,checked)):
        f=r['question'][':question/answer-fields'][0]
        grade.append({'label':f'independent {i} {r["generation"]["template"]}','record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if j==c['key_index'] else 'rejected','purpose':'independently solved complete radio bank'} for j,a in enumerate(f[':answer-field/choices'])]})
    save('grader-input.json',grade)
    easy=[r for r in controlled if r['question'][':question/difficulty'].endswith('/easy')]
    save('delivery-input.json',easy+constructor)
    save('scope-results.json',{'records':len(checked),'singular_2x2':True,'easy_pivot_one':all(R.equations(r['question'])[0,0]==1 for r in all_records if r['question'][':question/difficulty'].endswith('/easy')),'response':'one five-choice radio field; x basic, y free','ordinary_domain':'intercept -8..8, independent zero or nonzero integer residual -6..6; same one elimination at easy; moderate includes first-pivot normalization','boundaries':'explicit overrides up to magnitude 32 retain same method; not ordinary random workload','passed':True})
    invalid=[]
    for params in [{'intercept':33},{'intercept':'1/2'},{'residual':33},{'residual':'1/2'},{'rhs_scale':0},{'rhs_scale':5},{'residual':0,'second_rhs':0},{'unknown':1}]:
        try:g.generate('easy',1,'q-20964',params);ok=False
        except ValueError as exc:ok=True
        invalid.append({'parameters':params,'rejected':ok})
    assert all(v['rejected'] for v in invalid)
    rel=E/'relocated-package';rel.mkdir(exist_ok=True)
    manifest=json.loads((P/'package.json').read_text())
    for name in ['package.json']+manifest['files']:
        dest=rel/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/name,dest)
    command=[sys.executable,str(rel/manifest['entrypoint']),'--difficulty','easy','--seed','92871','--count','5','--output',str(E/'relocated-records.json')]
    run=subprocess.run(command,cwd=E,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    assert run.returncode==0 and json.loads((E/'relocated-records.json').read_text())==g.batch('easy',5,92871)
    assert g.batch('easy',5,92871)==g.batch('easy',5,92871)
    actual={'python':platform.python_version(),'packages':{'sympy':S.__version__}}
    assert actual==manifest['dependencies']
    save('packaging-results.json',{'manifest_dependencies':manifest['dependencies'],'actual_versions':actual,'deterministic_replay':True,'invalid_parameters':invalid,'relocation_command':command,'relocation_exit':run.returncode,'relocation_matches':True,'declared_files_sufficient':True,'assets':'No external generated output assets; only declared bundled source JSON read.','internal_batch':{'raw_prefix':len(prefix),'accepted':len(constructor),'deduplicated':len(prefix)-len(constructor)},'passed':True})
    render=exact+[g.generate('easy',7331,'q-20964',{'rhs_scale':1}),g.generate('easy',92871,'q-42157',{'intercept':0,'residual':0}),g.generate('moderate',92871,'q-130924',{'intercept':-7,'residual':-5})]+batch
    save('render-records.json',render)
    (E/'session-state.md').write_text('Completed matched-source account, old-package failure reproduction (2 defects), current retained regressions (pass), redirected author preflight (17 sources/51 pairs), independent source replay (17/17), fresh controlled pairs (51), exact math, metadata replay, boundary rejection and relocation. Next: shared delivery, native grader, UI rendering, conditional shortcuts and selection evidence.\n')
    print(json.dumps({'source_replay':len(replay),'controlled_pairs':len(pairs),'math_records':len(checked),'native_checks_prepared':len(grade)*5,'constructor_raw':len(prefix),'constructor_unique':len(constructor),'render_records':len(render)}))

if __name__=='__main__':main()
