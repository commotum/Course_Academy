"""Independent read-only review. Run with the job Python; outputs stay here."""
import sys
sys.dont_write_bytecode = True
import copy, hashlib, importlib.util, json, os, pathlib, re, shutil, subprocess
from collections import Counter, defaultdict
import sympy as S

ROOT = pathlib.Path(__file__).resolve().parent
JOB = ROOT.parent
REPO = pathlib.Path('/home/jake/Developer/Course_Academy')
PKG = JOB / 'workspace'
PY = REPO / '.venv/bin/python'
def save(name, value):
    (ROOT/name).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')
def read(path): return json.loads(path.read_text())
def load_generator(path):
    sys.path.insert(0,str(path))
    spec=importlib.util.spec_from_file_location('reviewed_generator',path/'generator.py')
    g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
    return g
def package_hashes():
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.iterdir() if p.is_file()}
def matrices(text):
    return [S.Matrix([[S.Rational(c.strip()) for c in r.split('&')] for r in body.split(r'\\')])
            for body in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]
def field(r):return r['question'][':question/answer-fields'][0]
def answer(r):
    f=field(r);key=f[':answer-field/correct'];key=key[':answer/id'] if isinstance(key,dict) else key[1]
    return int(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==key))
def check(r):
    q=r['question'];a=matrices(q[':question/problem'])[0];states=matrices(q[':question/worked-solution'])
    errors=[]
    if states[0]!=a:errors.append('solution starts with other matrix')
    if int(a.rank())!=answer(r):errors.append('wrong key')
    if not states[-1].is_echelon:errors.append('final not REF')
    for i,(before,after) in enumerate(zip(states,states[1:])):
        changed=[j for j in range(a.rows) if before.row(j)!=after.row(j)]
        if len(changed)!=1:errors.append('not one row replacement');continue
        j=changed[0];delta=after.row(j)-before.row(j)
        candidates=[]
        for k in range(a.rows):
            if k==j:continue
            h=next((h for h in range(a.cols) if before[k,h]),None)
            if h is not None:
                c=delta[h]/before[k,h]
                if c and delta==c*before.row(k):candidates.append((j,k,c))
        if not candidates:errors.append('not elementary row equivalent')
        # Verify the displayed annotation, independently of generation metadata.
        clean=q[':question/worked-solution'].replace(r'\left', '').replace(r'\right', '')
        annotations=re.findall(r'\{R\}_\{(\d+)\} :=\{R\}_\{\1\}\+\((.*?)\)\{R\}_\{(\d+)\}',clean)
        if i>=len(annotations):errors.append('missing operation annotation')
        else:
            dest,c,src=annotations[i]
            frac=re.fullmatch(r'(-?)\s*\\frac\{(\d+)\}\{(\d+)\}',c)
            coefficient=S.Rational((-1 if frac[1] else 1)*int(frac[2]),int(frac[3])) if frac else S.Rational(c)
            if (int(dest)-1,int(src)-1,coefficient) not in candidates:errors.append('wrong displayed operation')
    endrank=sum(any(states[-1].row(i)) for i in range(a.rows))
    if endrank!=answer(r):errors.append('pivot count inconsistent')
    if f'${answer(r)}$ pivots' not in q[':question/worked-solution']:errors.append('wrong conclusion')
    return {'id':q[':question/id'],'template':r['generation']['template'],'seed':r['generation']['seed'],
            'shape':[a.rows,a.cols],'rank':int(a.rank()),'errors':errors}

def main():
    save('package-hashes-before.json',package_hashes())
    g=load_generator(PKG);source=read(JOB/'source/source.json');batch=read(JOB/'samples.json')
    save('batch.json',batch)
    replays=[];source_results=[]
    for sq in source['material']['kp'][':knowledge-point/questions']:
        template=sq[':question/math-academy-id'];r=g.source_replay(template);replays.append(r)
        sr=check(r);sqf=sq[':question/answer-fields'][0]
        sr['source_id']=sq[':question/id']
        sr['source_matrices_equal']=matrices(sq[':question/problem'])==matrices(r['question'][':question/problem']) and matrices(sq[':question/worked-solution'])==matrices(r['question'][':question/worked-solution'])
        sr['complete_bank_equal']=sorted(a[':answer/value'] for a in sqf[':answer-field/choices'])==sorted(a[':answer/value'] for a in field(r)[':answer-field/choices'])
        sr['source_key_equal']=int(sqf[':answer-field/correct'][':answer/value'])==answer(r)
        source_results.append(sr)
    save('source-replays.json',replays)
    canonical=source['material']['kp'][':knowledge-point/canonical-example']
    save('source-replay-results.json',{'cases':source_results,'canonical':{'id':canonical[':question/id'],'rank':int(matrices(canonical[':question/problem'])[0].rank()),'answer_field_captured':False,'limitation':'No public canonical replay template; 17 assessed radio source cases replayed. Canonical matrices independently checked, no answer control invented.'},'excluded':g.EXCLUDED})
    samples=[];coverage=[];failures=[]
    for ti,t in enumerate(g.TEMPLATES):
        for offset in range(3):
            seed=926471+ti*100+offset
            try:samples.append(g.generate(seed=seed,template=t))
            except Exception as e:failures.append({'template':t,'seed':seed,'exception':str(e)})
        subset=[r for r in samples if r['generation']['template']==t]
        coverage.append({'template':t,'ranks':dict(Counter(answer(r) for r in subset)),
                         'active_rows':dict(Counter(r['generation']['parameters']['active_rows'] for r in subset)),
                         'names':dict(Counter(r['generation']['parameters']['name'] for r in subset)),
                         'source_shape':list(g.TEMPLATES[t]['states'][0].shape)})
    save('samples.json',samples)
    save('coverage.json',{'command':f'{PY} {ROOT}/audit.py','seeds':'926471 + 100*template_index + offsets 0..2; template order from source capture','coverage':coverage,'generation_failures':failures})
    p={'active_rows':3,'name':'A','echelon':[['1','1','0','0','0'],['0','0','1','1','0'],['0','0','0','0','0']],
       'operations':[[1,0,'1'],[2,0,'-1']]}
    r0=g.generate(seed=74109,template='q-130957',parameters=p)
    p1=copy.deepcopy(p);p1['echelon'][2][4]='1'
    r1=g.generate(seed=74109,template='q-130957',parameters=p1)
    p2=copy.deepcopy(p1);p2['name']='D'
    r2=g.generate(seed=74109,template='q-130957',parameters=p2)
    p3=copy.deepcopy(p1);p3['echelon'][0]=['2','2','0','0','0']
    r3=g.generate(seed=74109,template='q-130957',parameters=p3)
    cf=[r0,r1,r2,r3];save('counterfactual-records.json',cf)
    save('counterfactual-results.json',{'commands':'audit.py explicit parameters in counterfactual-records.json; replay via generate(parameters=record.generation.parameters, seed=74109, template=q-130957)',
        'relevant':{'before_rank':answer(r0),'after_rank':answer(r1),'input_cells_changed':sum(x!=y for x,y in zip(matrices(r0['question'][':question/problem'])[0],matrices(r1['question'][':question/problem'])[0])),'expectation':'one residual zero becomes nonzero; rank 2 -> 3'},
        'irrelevant_name':{'ranks':[answer(r1),answer(r2)],'matrices_equal':matrices(r1['question'][':question/problem'])==matrices(r2['question'][':question/problem'])},
        'irrelevant_row_scale':{'ranks':[answer(r1),answer(r3)]}})
    all_records=samples+batch+replays+cf
    math_results=[check(r) for r in all_records]
    save('math-results.json',{'count':len(math_results),'failures':[x for x in math_results if x['errors']],'cases':math_results})
    cases=[]
    # All authored choices for all source replays, batch and controlled pairs.
    for i,r in enumerate(replays+batch+cf):
        f=field(r);a=matrices(r['question'][':question/problem'])[0].rank()
        cases.append({'label':f'{i}: {r["question"][":question/id"]}', 'record':r,'checks':[
            {'field_index':0,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if int(c[':answer/value'])==a else 'rejected','purpose':'independent exact rank and complete radio bank'} for c in f[':answer-field/choices']]})
    save('grader-input.json',cases)
    # Representative renderer set includes exact batch, controlled pairs, widest and fractional source replay.
    render=batch+cf+[replays[0],replays[1],next(r for r in replays if len(matrices(r['question'][':question/problem'])[0].row(0))==6)]
    save('render-input.json',render)
    env=os.environ|{'PYTHONDONTWRITEBYTECODE':'1'}
    checks=[]
    for label,params in [('zero multiplier',{'operations':[[1,0,'0'],[2,0,'-1']]}),('invalid name',{'name':'Z'}),('oversized entry',{'echelon':[['41','1','0','0','0'],['0','0','1','1','0'],['0','0','0','0','0']]}),('wrong active rows',{'active_rows':2})]:
        pp=copy.deepcopy(p);pp.update(params)
        try:g.generate(seed=74109,template='q-130957',parameters=pp);checks.append({'case':label,'rejected':False})
        except ValueError as e:checks.append({'case':label,'rejected':True,'reason':str(e)})
    pp=copy.deepcopy(p);pp['echelon'][0][0]='40';boundary=g.generate(seed=74109,template='q-130957',parameters=pp)
    save('boundary-records.json',[boundary]);checks.append({'case':'entry exactly 40','accepted':not check(boundary)['errors']})
    dest=ROOT/'relocated-package';dest.mkdir(exist_ok=True)
    for f in read(PKG/'package.json')['files']+['package.json']:shutil.copyfile(PKG/f,dest/f)
    commands=[];outputs=[]
    for directory in [PKG,dest]:
        command=[str(PY),str(directory/'generator.py'),'--seed','923771','--count','5']
        result=subprocess.run(command,capture_output=True,text=True,env=env,cwd=ROOT,timeout=60)
        commands.append({'command':command,'returncode':result.returncode,'stderr':result.stderr});outputs.append(result.stdout)
    save('relocation-sample.json',json.loads(outputs[0]));
    save('packaging-results.json',{'python':sys.version.split()[0],'packages':{'sympy':S.__version__},'manifest':read(PKG/'package.json'),'commands':commands,'relocation_and_deterministic_match':outputs[0]==outputs[1],'explicit_parameter_replay':all(g.generate(seed=r['generation']['seed'],template=r['generation']['template'],parameters=r['generation']['parameters'])==r for r in samples[:4]),'boundaries':checks,'file_hashes_unchanged':package_hashes()==read(ROOT/'package-hashes-before.json')})
    save('package-hashes-after.json',package_hashes())
    (ROOT/'session-state.md').write_text('Independent source analysis saved before package inspection. Completed: 17 complete source replays, 51 freshly seeded normal samples, exact matrix/rank/row-operation checks, 4 controlled records, boundary and relocation checks. Next: shared delivery, native grader, actual UI; then shortcut and inventory analysis. The runner batch provisionally has rank = number of rows minus one in all 5 records.\n')
    print(json.dumps({'normal_count':len(samples),'math_failures':len([x for x in math_results if x['errors']]),'generation_failures':len(failures),'source_cases':len(replays),'output':str(ROOT)}))

if __name__=='__main__':main()
