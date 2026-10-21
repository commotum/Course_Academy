"""Independent focused revision audit. Run with the job's Python and -B."""
import sys, json, pathlib, re, subprocess, hashlib, collections
from fractions import Fraction
sys.dont_write_bytecode = True
R=pathlib.Path(__file__).resolve().parent
B=R.parent; W=B/'workspace'; REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
sys.path.insert(0,str(W))
import generator as g
import sympy
from math_helpers import system, matrices, triple

def save(n,v): (R/n).write_text(json.dumps(v,indent=2)+'\n')
def solve(rows):
    m=[[Fraction(v) for v in row] for row in rows]
    for col in range(3):
        pivot=next(i for i in range(col,3) if m[i][col]);m[col],m[pivot]=m[pivot],m[col]
        k=m[col][col];m[col]=[v/k for v in m[col]]
        for i in range(3):
            if i!=col:
                k=m[i][col];m[i]=[x-k*y for x,y in zip(m[i],m[col])]
    assert all(v.denominator==1 for row in m for v in row)
    return [[int(v) for v in row] for row in m]

def check(r):
    q=r['question']; rows=system(q[':question/problem']); reduced=solve(rows); target=[row[3] for row in reduced]
    assert len(rows)==3 and all(len(row)==4 for row in rows)
    assert [rows[i][i] for i in range(3)]==[1]*3 and rows[1][0]==rows[2][0]==rows[2][1]==0
    ms=matrices(q[':question/worked-solution']);assert ms[0]==rows and ms[-1]==reduced
    ops=re.findall(r'R_\{(\d)\}:=R_\{(\d)\}([+-])(\d*)R_\{(\d)\}',q[':question/worked-solution'])
    assert len(ops)==len(ms)-1
    for before,after,(i,left,sign,n,j) in zip(ms,ms[1:],ops):
        assert i==left
        expected=[row[:] for row in before]; k=(int(n) if n else 1)*(1 if sign=='+' else -1)
        expected[int(i)-1]=[x+k*y for x,y in zip(before[int(i)-1],before[int(j)-1])];assert expected==after
    fields=q[':question/answer-fields'];pos=None
    if fields:
        assert len(fields)==1
        f=fields[0];assert f[':answer-field/type']==':answer-field.type/radio';choices=f[':answer-field/choices']
        vs=[triple(c[':answer/value']) for c in choices]; assert len(vs)==len(set(map(tuple,vs)))==5
        matching=[c[':answer/id'] for c,v in zip(choices,vs) if v==target];assert matching==[f[':answer-field/correct'][1]]
        for c in choices:
            cms=matrices(c[':answer/value'])
            if cms:assert [row[:3] for row in cms[0]]==[[1,0,0],[0,1,0],[0,0,1]]
        pos=next(i for i,c in enumerate(choices) if c[':answer/id']==matching[0])
    else:assert r['generation']['evidence_only'] and not r['generation']['eligible_for_learning']
    if 'So, we have the solution ' in q[':question/worked-solution']:
        assert triple(q[':question/worked-solution'].split('So, we have the solution ')[1].split(' Or,')[0])==target
    return {'id':q[':question/id'],'solution':target,'steps':len(ops),'profile':r['generation']['source_profile'],'correct_position':pos,'rows':rows}

def main():
    source=json.load(open(B/'source/source.json')); kp=source['material']['kp']; qs=kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]
    replays=[];reports=[]
    assert set(g.SOURCE_CASES)=={q[':question/math-academy-id'] for q in qs}
    for q in qs:
        p=q[':question/math-academy-id'];r=g.generate(seed=731,template=p,replay=True);checked=check(r);out=r['question']
        assert system(q[':question/problem'])==system(out[':question/problem'])
        sf=q.get(':question/answer-fields',[]);of=out[':question/answer-fields'];assert len(sf)==len(of)
        if sf:
            assert sf[0][':answer-field/type'][':db/ident']==of[0][':answer-field/type']
            assert sorted(triple(c[':answer/value']) for c in sf[0][':answer-field/choices'])==sorted(triple(c[':answer/value']) for c in of[0][':answer-field/choices'])
            assert sorted(c[':answer/type'][':db/ident'] for c in sf[0][':answer-field/choices'])==sorted(c[':answer/type'] for c in of[0][':answer-field/choices'])
        original_stages=[]
        for m in matrices(q.get(':question/worked-solution','')):
            if not original_stages or original_stages[-1]!=m:original_stages.append(m)
        if original_stages:assert original_stages==matrices(out[':question/worked-solution'])
        reports.append({'profile':p,'source_id':q[':question/id'],'status':'passed','complete_choices':len(sf[0][':answer-field/choices']) if sf else 0,'worked_stages_compared':len(original_stages),'math':checked,'source_key':sf[0].get(':answer-field/correct') if sf else None})
        replays.append(r)
    save('source-replay.json',reports);save('source-replay-records.json',replays)
    # Full role/mask coverage on restored profiles, small regression on unchanged profiles.
    controlled=[]
    for profile in ['q-20589','q-20598']:
        for role in range(5):
            for mi,mask in enumerate(g.MASKS):
                params={'role':role,'mask':list(mask),'coefficients':[(5 if (role+j+mi)%2 else -5) if active else 0 for j,active in enumerate(mask)],'translation':[5,-5,0] if role%2 else [-5,0,5],'scale':1+role%2}
                controlled.append(g.generate(seed=438790+role*13+mi,template=profile,parameters=params))
    for i,p in enumerate(sorted(set(g.PROFILES)-{'q-20589','q-20598'})):
        controlled.append(g.generate(seed=892345+i,template=p))
    raw=g.batch('easy',28,5839017);batch=json.load(open(B/'samples.json'))
    save('controlled-records.json',controlled);save('random-records.json',raw);save('runner-batch.json',batch)
    pairs=[];pairreports=[]
    for profile in ['q-20589','q-20598','q-20591']:
        params={'role':0,'mask':[1,1,1],'coefficients':[2,-3,1],'translation':[1,-2,3],'scale':2}
        base=g.generate(seed=7641,template=profile,parameters=params)
        relevant=g.generate(seed=7641,template=profile,parameters=dict(params,role=1))
        irrelevant=g.generate(seed=7641,template=profile,parameters=dict(params,coefficients=[-2,3,-1]))
        a,b,c=map(check,[base,relevant,irrelevant]);assert a['solution']!=b['solution'] and a['solution']==c['solution']
        assert [row[:3] for row in a['rows']]==[row[:3] for row in b['rows']]
        for other in [relevant,irrelevant]:assert base['question'][':question/problem']!=other['question'][':question/problem'] and base['question'][':question/worked-solution']!=other['question'][':question/worked-solution']
        assert base['question'][':question/answer-fields'][0][':answer-field/correct'][1]!=relevant['question'][':question/answer-fields'][0][':answer-field/correct'][1]
        assert sorted(triple(x[':answer/value']) for x in base['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(triple(x[':answer/value']) for x in relevant['question'][':question/answer-fields'][0][':answer-field/choices'])
        pairreports.append({'profile':profile,'seed':7641,'parameters':params,'changes':{'relevant':{'role':1},'irrelevant':{'coefficients':[-2,3,-1]}},'before':a,'relevant':b,'irrelevant':c,'status':'passed'})
        pairs.extend([base,relevant,irrelevant])
    save('counterfactual-records.json',pairs);save('counterfactual-results.json',pairreports)
    allrecords=replays+controlled+raw+batch+pairs
    results=[check(r) for r in allrecords];save('math-results.json',{'checked':len(results),'failures':[],'records':results})
    cases=[]
    for i,r in enumerate(allrecords):
        if not r['question'][':question/answer-fields']:continue
        f=r['question'][':question/answer-fields'][0];t=check(r)['solution']
        checks=[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if triple(c[':answer/value'])==t else 'rejected','purpose':'Fraction elimination of visible equations, independently compared with complete displayed choice'} for c in f[':answer-field/choices']]
        cases.append({'label':str(i)+' '+r['generation']['source_profile'],'record':r,'checks':checks})
    # Explicit old-answer submissions on each relevant/irrelevant pair; IDs differ by question.
    for j in range(0,len(pairs),3):
        base,rel,irr=pairs[j:j+3];old=check(base)['solution']
        for r,expected in [(rel,'rejected'),(irr,'accepted')]:
            f=r['question'][':question/answer-fields'][0];c=next(c for c in f[':answer-field/choices'] if triple(c[':answer/value'])==old)
            cases.append({'label':'counterfactual old solution '+r['generation']['source_profile'],'record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':expected,'purpose':'Prior response must change only for relevant evidence'}]})
    save('grader-input.json',cases)
    rejects=[]
    for kw in [{'difficulty':'hard'},{'template':'e-4709'},{'parameters':{'role':5}},{'parameters':{'mask':[0,0,0]}},{'parameters':{'mask':[1,1,1],'coefficients':[0,0,0]}},{'parameters':{'translation':[6,0,0]}},{'parameters':{'scale':0}}]:
        try:g.generate(**kw);rejects.append({'input':kw,'rejected':False})
        except (ValueError,KeyError) as e:rejects.append({'input':kw,'rejected':True,'error':repr(e)})
    assert all(x['rejected'] for x in rejects)
    manifest=json.load(open(W/'package.json'));assert manifest['dependencies']=={'python':sys.version.split()[0],'packages':{'sympy':sympy.__version__}}
    assert g.batch('easy',5,902487)==g.batch('easy',5,902487)
    def cli(path):return subprocess.run([sys.executable,'-B',str(path/'generator.py'),'--count','5','--seed','902487'],capture_output=True,text=True,cwd=R,check=True).stdout
    assert cli(W)==cli(R/'relocated')
    save('packaging.json',{'manifest':manifest,'runtime':{'python':sys.version.split()[0],'sympy':sympy.__version__},'deterministic':True,'relocation_equal':True,'invalid_inputs':rejects,'outputs':'JSON stdout; no generated assets or external paths. All Python invoked with -B.'})
    save('render-records.json',batch+pairs+[r for r in replays if r['generation']['source_profile'] in ['q-20589','q-20598','e-4709']])
    save('scope.json',{'status':'passed','examined_records':len(results),'source_refs':['tutorial f74e6075-9c2a-5495-ab21-470711559f2a','tutorial ce056e74-9707-52d3-b172-483ca14e1f8f'],'reason':'All practice systems unit-pivot upper triangular, full rank, 3 variables, two or three integer backward-elimination steps. Restored profiles preserve captured matrix/text shapes. Canonical example is replay-only and fieldless; no new learner response requirement.','workload_max_abs_input':max(abs(x) for v in results for row in v['rows'] for x in row)})
    (R/'session-state.md').write_text('Independent current tests completed: all 15 source cases, 70 complete choices and captured operative stages; restored profiles cover five roles/four masks. Independent Fraction math, counterfactual expectations, packaging and rejection checks passed. Grader input and renderer input saved. Next: native grader, actual delivery, UI rendering, conditional shortcut/delivery assessment.\n')
    print(json.dumps({'source_cases':len(replays),'complete_banks':sum(bool(r['question'][':question/answer-fields']) for r in replays),'controlled':len(controlled),'random':len(raw),'batch':len(batch),'counterfactual_records':len(pairs),'math_records':len(results),'grader_cases':len(cases)}))
if __name__=='__main__':main()
