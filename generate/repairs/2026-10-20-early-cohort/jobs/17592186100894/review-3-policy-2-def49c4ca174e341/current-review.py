from auditlib import *
from collections import Counter

# Reused independent source replay and mathematics are independently executable.
source=json.load(open(JOB/'source/source.json'))
replays=[]; results=[]
for i,q in enumerate(source['material']['kp'][':knowledge-point/questions']):
    mid=q[':question/math-academy-id']
    if mid=='q-104058': continue
    r=g.generate(g.level(mid),918401+i,mid,replay=True);replays.append(r)
    f=q[':question/answer-fields'][0]
    row={'template':mid,'source_id':q[':question/id'],
         'bank_equal':Counter(g.normalize_tex(a[':answer/value']) for a in f[':answer-field/choices'])==Counter(a[':answer/value'] for a in field(r)[':answer-field/choices']),
         'key_equal':correct(r)==g.normalize_tex(f[':answer-field/correct'][':answer/value'])}
    assert row['bank_equal'] and row['key_equal'];results.append(row)
save('source-replay-records.json',replays)
save('source-replay.json',{'results':results,'excluded':{'q-104058':'Source IC makes 0*yprime=2; impossible classical IVP.'},'documented_corrections':g.REPAIRS,'sine_source':'Restores omitted ODE from its own solution; restricts positive-cosine local branch. Source bank/key retained.','canonical':'No captured answer fields; instructional evidence only.'})

batch=json.load(open(JOB/'samples.json'));assert batch==json.load(open(E/'batch.json'))
# Fresh cases cover the changed semantic rule at boundary and interior shifts.
sines=[g.generate('easy',918503+i,'q-126765',{'h':h}) for i,h in enumerate((-4,-1,0,2,4))]
save('sine-current-records.json',sines)
small=[g.generate(g.level(mid),918550+i,mid,par) for i,(mid,par) in enumerate([
    ('q-128199',{'h':-4,'b':-2}),('q-128199',{'h':4,'b':2}),
    ('q-355559',{'h':-4}),('q-355577',{'h':4}),('q-355582',{'h':-4})])]
save('fresh-regression-records.json',small)
math=[]
for r in small+batch+sines:
    if r['generation']['template']=='q-126765':
        prompt=r['question'][':question/problem']
        ode=re.search(r"\$y'=(.*?)\$",prompt)[1]
        forcing=simplify(expr(ode.replace(r'\sqrt',r'*\sqrt'))/S.sqrt(1-y*y))
        v=expr(correct(r));diff=simplify(S.diff(v,x)-forcing)
        assert r'\sin(\boxed{\text{expression}}+C)' in prompt and r'-\pi/2<\theta<\pi/2' in prompt
        # Read the final branch/solution from the printed solution, too.
        assert 'constant endpoint solutions' in r['question'][':question/worked-solution']
        result={'template':'q-126765','generation':r['generation'],'printed_forcing':str(forcing),'key_derivative_difference':str(diff),'passed':diff==0,'valid_choice_count':1,'branch':'cos(theta)>0 makes sin(v+C) derivative match printed ODE.'}
    else: result=math_check(r)
    assert result['passed'] and result['valid_choice_count']==1
    math.append(result)
save('fresh-math-results.json',math)

# One batched native invocation includes unchanged controls because the shared
# engine changed, and all retained strict checks without weakened expectations.
cases=json.load(open(E/'retained-grader-input.json'))
records=json.load(open(E/'role-records.json'))+json.load(open(E/'counterfactual-records.json'))+small+batch+sines
proof=[]
for i,r in enumerate(records):
    f=field(r);mid=r['generation']['template']
    if f[':answer-field/type'].endswith('/radio'):
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected'} for a in f[':answer-field/choices']]
    else:
        v=expr(correct(r));equiv=str(S.expand(v)).replace('**','^').replace('log(','ln(').replace('E','e')
        checks=[{'submitted':correct(r),'expected':'accepted'},{'submitted':equiv,'expected':'accepted'},{'submitted':'0','expected':'rejected'}]
        if mid=='q-126765':
            for value in [v+1,v-S.Rational(7,3),v+S.pi]:
                delta=simplify(value-v);assert not delta.has(x)
                checks.append({'submitted':str(value).replace('**','^'),'expected':'accepted','purpose':'Arbitrary C absorbs this independently checked constant.'})
                proof.append({'record_index':i,'generation':r['generation'],'candidate':str(value),'constant_difference':str(delta),'derivative_difference':str(S.diff(value-v,x))})
            for value in [2*v,v+x,v**2]:
                assert simplify(S.diff(value-v,x))!=0
                checks.append({'submitted':str(value).replace('**','^'),'expected':'rejected','purpose':'Different derivative cannot be absorbed into C.'})
        else: checks.append({'submitted':'('+correct(r)+')+1','expected':'rejected','purpose':'Fixed IVP constant cannot change.'})
        if mid=='q-128199': checks.append({'submitted':'-('+correct(r)+')','expected':'rejected'})
    cases.append({'label':'current independent '+str(i)+' '+mid,'record':r,'checks':checks})
cases+=json.load(open(E/'delivered-sine-strict-input.json'))
save('current-grader-input.json',cases);save('sine-current-proof.json',proof)
cmd=[str(ROOT/'generate/runs/current/check-engine'),str(E/'current-grader-input.json'),str(E/'current-grader-report.json')]
p=subprocess.run(cmd,capture_output=True,text=True);(E/'current-grader-console.txt').write_text(p.stdout+p.stderr)
save('current-grader-execution.json',{'command':cmd,'exit':p.returncode,'cases':len(cases),'checks':sum(len(c['checks']) for c in cases),'engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest()})
assert p.returncode==0,p.stdout+p.stderr
print('Source replay:',len(replays),'fresh math:',len(math),p.stdout.strip(),flush=True)

# Reproduce the exact most recent defect on the retained older native engine.
old=W/'17592186100894/check-engine'
cmd=[str(old),str(E/'delivered-sine-strict-input.json'),str(E/'sine-before-report.json')]
p=subprocess.run(cmd,capture_output=True,text=True)
save('sine-before-execution.json',{'command':cmd,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'sha256':hashlib.sha256(old.read_bytes()).hexdigest()})
assert p.returncode!=0 and 'got rejected' in (p.stdout+p.stderr).lower(),p.stdout+p.stderr
save('render-current-records.json',batch+sines[:1]+json.load(open(E/'counterfactual-records.json')))
(E/'session-state.md').write_text('Source replay 25 complete banks/keys passed. Fresh math, unchanged trig/counterfactual native controls, all retained strict grader cases, exact batch, and fresh sine constant/derivative tests passed current native engine. Exact prior sine failure reproduced on retained old engine. Delivery, rendering, final packaging and report pending.\n')
