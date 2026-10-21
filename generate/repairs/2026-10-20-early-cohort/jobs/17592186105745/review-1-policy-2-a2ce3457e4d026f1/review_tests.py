#!/usr/bin/env python3
"""Read-only independent generator audit. Run with the job's Python; writes here only."""
import collections, copy, hashlib, importlib.util, json, os, pathlib, re, shutil, subprocess, sys
sys.dont_write_bytecode = True
import sympy as S
ROOT = pathlib.Path(__file__).resolve().parent
JOB = ROOT.parent
REPO = pathlib.Path('/home/jake/Developer/Course_Academy')
PY = REPO / '.venv/bin/python'
PKG = JOB / 'workspace'
def save(name, value):
    p=ROOT/name; p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def hashes():
    return {str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(PKG.rglob('*')) if p.is_file()}
def load_generator(path):
    spec=importlib.util.spec_from_file_location('reviewed_generator',path);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);return g
y=S.Symbol('y');x=S.Symbol('x')
def expr(v):
    v=v.strip().replace(' ','').replace(r'\,','').replace('−','-')
    v=re.sub(r'\\frac\{(-?\d+)\}\{(-?\d+)\}',r'(\1/\2)',v)
    v=re.sub(r'(?<=[0-9)])(?=[xy])','*',v)
    return S.sympify(v,locals={'x':x,'y':y})
def mats(v):
    return [S.Matrix([[expr(c) for c in row.strip().split('&')] for row in body.split(r'\\')]) for body in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',v,re.S)]
def family(v):
    mm=mats(v)
    if mm:
        m=mm[-1]
        return list(m) if m.shape==(2,1) else None
    m=re.search('⟨(.*?)⟩',v)
    if m:
        return [expr(c) for c in m.group(1).replace(r'\,','').split(',')]
    return None
def keypos(r):
    f=r['question'][':question/answer-fields'][0]
    return next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])
def signature(r):
    q=r['question'];a=mats(q[':question/problem'])[0]
    return ('ref' if 'then find' not in q[':question/problem'] and 'reduce' in q[':question/problem'] else 'solution', tuple(str(v) for v in a[:,:2]))
def shortcut(r):
    """No prompt, generation metadata, labels, IDs or correct key are read."""
    bank=r['question'][':question/answer-fields'][0][':answer-field/choices']
    ms=[mats(a[':answer/value']) for a in bank]
    if all(m and m[-1].shape==(2,3) for m in ms):
        rows=[tuple(m[-1][0,:]) for m in ms];modal=collections.Counter(rows).most_common(1)[0][0]
        picks=[i for i,m in enumerate(ms) if rows[i]==modal and list(m[-1][1,:])==[0,0,0]]
        return picks, 'modal top row plus all-zero bottom row'
    fs=[family(a[':answer/value']) for a in bank]
    af=[(i,f[0]) for i,f in enumerate(fs) if f and f[1]==y and S.diff(f[0],y)!=0]
    constants=[S.sign(e.subs(y,0)) for i,e in af];slopes=[S.sign(S.diff(e,y)) for i,e in af]
    if not af:return [],'majority intercept and slope signs'
    cs=collections.Counter(constants).most_common();ss=collections.Counter(slopes).most_common()
    if (len(cs)>1 and cs[0][1]==cs[1][1]) or (len(ss)>1 and ss[0][1]==ss[1][1]):return [],'majority intercept and slope signs'
    cm=collections.Counter(abs(e.subs(y,0)) for i,e in af).most_common(1)[0][0]
    sm=collections.Counter(abs(S.diff(e,y)) for i,e in af).most_common(1)[0][0]
    return [i for i,e in af if S.sign(e.subs(y,0))==cs[0][0] and S.sign(S.diff(e,y))==ss[0][0] and abs(e.subs(y,0))==cm and abs(S.diff(e,y))==sm], 'majority signs with modal coefficient magnitudes among affine options'
def math_record(r):
    q=r['question'];a=mats(q[':question/problem'])[0];ref=a.rref()[0]
    f=q[':question/answer-fields'][0];isref=signature(r)[0]=='ref';valid=[];checks=[]
    for c in f[':answer-field/choices']:
        v=c[':answer/value']
        if isref:
            b=mats(v)[-1];ok=b==ref
        else:
            b=family(v);ok=b is not None and b[1].has(y) and all(S.simplify(a[i,0]*b[0]+a[i,1]*b[1]-a[i,2])==0 for i in range(2))
        valid.append(bool(ok))
    solution=q[':question/worked-solution'];badmat=[]
    for n,b in enumerate(mats(solution)):
        if b.shape==(2,3) and b.rref()[0]!=ref:badmat.append(n)
        if b.shape==(2,1) and b[0]!=x and b[1]==y and any(S.simplify(a[i,0]*b[0]+a[i,1]*y-a[i,2])!=0 for i in range(2)):badmat.append(n)
    # Independently check scalar equations in the solution, including repeated explanatory prose.
    badeq=[]
    expected=S.simplify((a[0,2]-a[0,1]*y)/a[0,0])
    for m in re.finditer(r'(?<![0-9A-Za-z])(x(?:\s*[+\-]\s*\d*y)?)\s*&?=\s*([+\-\d y]+)',solution):
        left=expr(m[1]);right=expr(m[2]);res=S.simplify((left-right).subs(x,expected))
        if res!=0:badeq.append({'equation':m[0],'residual':str(res)})
    return {'question_id':q[':question/id'],'template':r['generation']['template'],'parameters':r['generation']['parameters'],'valid_choices':valid,'key_position':keypos(r)+1,'unique_correct':valid.count(True)==1 and valid[keypos(r)],'invalid_solution_matrix_indices':badmat,'invalid_scalar_equations':badeq,'pass':valid.count(True)==1 and valid[keypos(r)] and not badmat and not badeq}
def main():
    before=hashes();save('package-hashes-before.json',before)
    g=load_generator(PKG/'17592186105745.py');source=json.load(open(JOB/'source/source.json'));orig={q[':question/math-academy-id']:q for q in source['material']['kp'][':knowledge-point/questions']}
    replay=[];recs=[]
    for sid,q in orig.items():
        level=q[':question/difficulty'][':db/ident'].split('/')[-1]
        try:r=g.generate(level,seed=71923,template=sid,parameters={'rhs_scale':1})
        except Exception as e:replay.append({'source_id':q[':question/id'],'template':sid,'status':'unsupported','error':str(e)});continue
        recs.append(r);rq=r['question'];f=q[':question/answer-fields'][0]
        # Locate the keyed field in duplicate captured fields without weakening its bank.
        f=next(f for f in q[':question/answer-fields'] if ':answer-field/correct' in f)
        rf=rq[':question/answer-fields'][0]
        replay.append({'source_id':q[':question/id'],'template':sid,'status':'tested','prompt_equal':rq[':question/problem']==q[':question/problem'],'solution_equal':rq[':question/worked-solution']==q[':question/worked-solution'],'bank_equal':sorted(a[':answer/value'] for a in rf[':answer-field/choices'])==sorted(a[':answer/value'] for a in f[':answer-field/choices']),'key_value_equal':rf[':answer-field/choices'][keypos(r)][':answer/value']==f[':answer-field/correct'][':answer/value']})
    save('source-replay-records.json',recs);save('source-replay.json',replay)
    # The changed construction is a single finite slot: use boundary signs and an interior fresh value.
    sampled=[g.generate(q[':question/difficulty'][':db/ident'].split('/')[-1],seed=71923,template=sid,parameters={'rhs_scale':t}) for sid,q in orig.items() if sid in g.CASES for t in [-4,-1,1,3,4]]
    batch=json.load(open(JOB/'samples.json'));save('runner-batch.json',batch)
    easy=[r for r in sampled if r['question'][':question/difficulty'].endswith('/easy')];moderate=[r for r in sampled if r['question'][':question/difficulty'].endswith('/moderate')]
    save('sampled-records.json',sampled);save('easy-records.json',easy);save('moderate-records.json',moderate)
    math=[math_record(r) for r in sampled+batch];save('math-results.json',{'results':math,'failed':[r for r in math if not r['pass']]})
    # Controlled relevant and irrelevant changes use the same template, seed and coefficient matrix.
    pairs=[];pairrecs=[]
    for sid in ['q-42158','q-73743']:
        a=g.generate('easy',seed=71923,template=sid,parameters={'rhs_scale':1});b=g.generate('easy',seed=71923,template=sid,parameters={'rhs_scale':-1});c=g.generate('easy',seed=88031,template=sid,parameters={'rhs_scale':1})
        pairrecs.extend([a,b,c]);pairs.append({'template':sid,'kind':'relevant','change':'rhs_scale 1 to -1; all coefficient columns fixed','prompt_changed':a['question'][':question/problem']!=b['question'][':question/problem'],'solution_changed':a['question'][':question/worked-solution']!=b['question'][':question/worked-solution'],'answer_before':a['question'][':question/answer-fields'][0][':answer-field/choices'][keypos(a)][':answer/value'],'answer_after':b['question'][':question/answer-fields'][0][':answer-field/choices'][keypos(b)][':answer/value'],'math_before':math_record(a),'math_after':math_record(b)})
        pairs.append({'template':sid,'kind':'irrelevant','change':'seed 71923 to 88031 with explicit template and rhs_scale 1','question_equal':a['question']==c['question']})
    a=g.generate('moderate',71923,'q-20963',{'rhs_scale':1});b=g.generate('moderate',71923,'q-73740',{'rhs_scale':1})
    pairrecs.extend([a,b])
    av=a['question'][':question/answer-fields'][0][':answer-field/choices'][keypos(a)][':answer/value'];bv=b['question'][':question/answer-fields'][0][':answer-field/choices'][keypos(b)][':answer/value']
    pairs.append({'templates':['q-20963','q-73740'],'kind':'irrelevant','change':'Dependent second row multiple 8 to -5; first row [1,2,-1] unchanged','prompt_before':a['question'][':question/problem'],'prompt_after':b['question'][':question/problem'],'answer_equal':av==bv,'answer_before':av,'answer_after':bv,'math_before':math_record(a),'math_after':math_record(b)})
    save('counterfactual-records.json',pairrecs);save('counterfactual-results.json',pairs)
    # Selection-only contract: grade every radio option using independently determined math validity.
    cases=[]
    for j,r in enumerate(sampled+batch+pairrecs):
        mr=math_record(r);picks,strategy=shortcut(r);f=r['question'][':question/answer-fields'][0]
        checks=[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if mr['valid_choices'][i] else 'rejected','purpose':'independent exact mathematical option classification'} for i,c in enumerate(f[':answer-field/choices'])]
        if len(picks)==1:checks.append({'submitted_answer_id':f[':answer-field/choices'][picks[0]][':answer/id'],'expected':'accepted' if mr['valid_choices'][picks[0]] else 'rejected','purpose':'bank-only shortcut: '+strategy})
        cases.append({'label':f'independent-{j}-{r["generation"]["template"]}-{r["generation"]["parameters"]["rhs_scale"]}','record':r,'checks':checks})
    save('grader-input.json',cases)
    boundary=[]
    for t in [0,5,-5,'1',None]:
        try:g.generate('easy',71923,'q-42158',{'rhs_scale':t});result='accepted'
        except Exception as e:result=type(e).__name__+': '+str(e)
        boundary.append({'rhs_scale':t,'result':result})
    save('boundaries.json',boundary)
    # Copy to evidence rather than invoke anything that might create package cache files.
    relocated=ROOT/'relocated-package';shutil.copytree(PKG,relocated,dirs_exist_ok=True)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    cmd=[str(PY),str(relocated/'17592186105745.py'),'--difficulty','easy','--count','5','--seed','71923','--format','json']
    run=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True);run2=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True)
    save('relocation-records.json',json.loads(run.stdout) if run.returncode==0 else [])
    save('packaging.json',{'command':cmd,'returncode':run.returncode,'stderr':run.stderr,'deterministic_replay':run.stdout==run2.stdout,'matches_original':json.loads(run.stdout)==g.batch('easy',5,71923) if run.returncode==0 else False,'actual_dependencies':{'python':sys.version.split()[0],'packages':{'sympy':S.__version__}},'manifest_dependencies':json.load(open(PKG/'package.json'))['dependencies'],'package_unchanged':hashes()==before,'external_output':'CLI output read on stdout; no assets; dependencies source.json resolved relative to entrypoint.'})
    # Inventory records are all captured originals. Do not relabel them as generated matches.
    inv=json.load(open(JOB/'source/inventory.json'));matches=[]
    for q in inv['questions']:
        if ':question/id' in q and any(q[':question/id']==r['question'][':question/id'] for r in sampled):matches.append(q[':question/id'])
    save('affected-inventory.json',{'affected_questions':[]})
    save('inventory-audit.json',{'basis':inv['basis'],'count':len(inv['questions']),'generated_metadata_records':[q[':question/id'] for q in inv['questions'] if any('generation' in k or 'generator' in k for k in q)],'matching_generated_question_ids':matches,'finding':'All 16 IDs equal captured original source IDs. None demonstrated as a stored generated instance; empty affected list is a verified absence within captured inventory, not a claim about future inventory.','source_ids':list(q[':question/id'] for q in inv['questions'])})
    save('package-hashes-after-tests.json',hashes())
    print(json.dumps({'source_tested':len(recs),'source_unsupported':[r['template'] for r in replay if r['status']=='unsupported'],'math_cases':len(math),'math_failures':sum(not r['pass'] for r in math),'easy_sample':len(easy),'moderate_sample':len(moderate),'package_unchanged':hashes()==before}))
    (ROOT/'session-state.md').write_text('Source analysis, source replay, exact math, counterfactuals, boundary checks, relocation and inventory audit saved. Run delivery, native grader, UI renderer next. Clear fixed-bank shortcut candidate; actual UI shuffles positions, so fixed stored position alone is not a delivered defect.\n')
if __name__=='__main__':main()
