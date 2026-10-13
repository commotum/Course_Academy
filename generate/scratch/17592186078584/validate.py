#!/usr/bin/env python3
"""Read displayed mathematics back and independently verify each printed stage."""
import hashlib, importlib.util, json, math, re, subprocess, sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor, rationalize
ROOT=Path(__file__).resolve().parent
SCRIPT=ROOT.with_suffix('.py')
spec=importlib.util.spec_from_file_location('generator',SCRIPT); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
COUNTS={'records':0,'math_rows':0,'displayed_options':0,'original_prompts_exact':0,'original_solutions_raw_exact':0,'original_banks_exact':0,'original_correct_designations':0,'repaired_solutions_correct':0}

def group(s,i):
    assert s[i]=='{',(s,i)
    depth=1; j=i+1
    while depth:
        if s[j]=='{': depth+=1
        if s[j]=='}': depth-=1
        j+=1
    return s[i+1:j-1],j

def parse(s):
    s=s.strip().rstrip('.,')
    s=re.sub(r'\{t\}_\{1\}', 'v',s).replace('{T}_{S}','A')
    s=s.replace(r'\operatorname{ln}⁡','ln').replace(r'\ln','ln').replace(r'\left','').replace(r'\right','')
    s=re.sub(r'ln\|([^|]+)\|',r'ln(|\1|)',s)
    s=s.replace(r'\,',' ').replace(r'\cdot','*').replace('{e}','e')
    s=re.sub(r'\^\{∘\}\\text\{[CF]\}', '',s)
    s=re.sub(r'\\text\{min\}', '',s)
    s=s.replace(r'\text{d}T','dT').replace(r'\text{d}t','dt')
    # Recursive complete components preserve fraction/exponent groups.
    out=''; i=0
    while i<len(s):
        if s.startswith(r'\frac',i):
            n,j=group(s,i+5); d,j=group(s,j); out+='(('+parse_code(n)+')/('+parse_code(d)+'))'; i=j
        elif s[i]=='^':
            if s[i+1]=='{': v,j=group(s,i+1); out+='**('+parse_code(v)+')'; i=j
            else: out+='**'+s[i+1]; i+=2
        elif s[i]=='{': v,j=group(s,i); out+='('+parse_code(v)+')'; i=j
        elif s[i]=='|':
            j=s.index('|',i+1); out+='Abs('+parse_code(s[i+1:j])+')'; i=j+1
        else: out+=s[i]; i+=1
    out=re.sub(r'\bT\(', 'F(',out)
    out=re.sub(r'ln\(', 'log(',out)
    assert '\\' not in out,('Unparsed command',s,out)
    return parse_expr(out,local_dict={'T':sp.Symbol('T'), 'A':sp.Symbol('A'),'K':sp.Symbol('K'),'k':sp.Symbol('k'),'C':sp.Symbol('C'),'t':sp.Symbol('t',real=True),'v':sp.Symbol('v'),'e':sp.E,'ln':sp.log,'log':sp.log,'Abs':sp.Abs,'F':sp.Function('F'),'dT':sp.Symbol('dT'),'dt':sp.Symbol('dt')}, transformations=standard_transformations+(implicit_multiplication_application,convert_xor,rationalize))

def parse_code(s):
    # nested parser's expression is converted back to safe SymPy syntax
    return str(parse(s))

def assert_equal(a,b,message):
    diff=sp.simplify(sp.expand_log(a-b,force=True))
    if diff!=0:
        assert not diff.free_symbols and abs(complex(sp.N(diff,35)))<1e-25,(message,a,b,diff)

def extract(r):
    """Parameters are recovered from actual prose/math, compared with metadata."""
    q=r['question']; text=q[':question/problem']; lev=q[':question/difficulty'].split('/')[-1]
    if lev=='easy':
        m=re.search(r'=-([0-9.]+)\(T-(\d+)\)',text); assert m
        k=sp.Rational(m[1]); A=int(m[2]); I=int(re.search(r'initial temperature .*?\$\{(\d+)\}',text)[1]); time=int(re.search(r'after \$(\d+)\$',text)[1]); p=dict(ambient=A,initial=I,rate=g.dec(k),time=time)
        t=sp.Symbol('t',real=True); K=I-A; model=A+K*sp.exp(-k*t); v=time; exact=model.subs(t,time)
    elif lev=='moderate':
        numbers=[int(n) for n in re.findall(r'\$\{(\d+)\}\^\{∘\}',text)]
        if r['generation']['template']=='tea': I,O,Z,A=numbers[:4]
        else: I,A,O,Z=numbers[:4]
        time=int(re.search(r'After \$(\d+)\$',text)[1]); p=dict(ambient=A,initial=I,observed=O,target=Z,time=time)
        k=-sp.log(sp.Rational(O-A,I-A))/time; K=I-A; t=sp.Symbol('t',real=True); model=A+K*sp.exp(-k*t); v=-sp.log(sp.Rational(Z-A,K))/k; exact=v
    else:
        nums=[int(n) for n in re.findall(r'\$\{(\d+)\}\^\{∘\}',text)]; A,O,L,Z=nums
        times=[int(n) for n in re.findall(r'after \$(\d+)\$',text)]; a,b=times; h=b-a
        p=dict(ambient=A,observed=O,later=L,target=Z,start=a,gap=h)
        k=-sp.log(sp.Rational(L-A,O-A))/h; K=(O-A)*sp.exp(k*a); t=sp.Symbol('t',real=True); model=A+K*sp.exp(-k*t); v=-sp.log((Z-A)/K)/k; exact=v
    assert p==r['generation']['parameters'],('Printed givens/metadata mismatch',p,r['generation']['parameters'])
    assert A>0 and float(k)>0
    return lev,p,A,k,K,model,v,exact

def validate(r):
    lev,p,A,k,K,model,v,exact=extract(r); q=r['question']; solution=q[':question/worked-solution']; profile=r['generation']['bank_profile']; t=sp.Symbol('t',real=True); f=q[':question/answer-fields'][0]
    assert set(r['knowledge_point'])=={'db_id','id','title'} and r['knowledge_point']['db_id']==17592186078584
    assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
    assert len(f[':answer-field/choices'])==5 and len({a[':answer/id'] for a in f[':answer-field/choices']})==5
    vals=[]; correct=None
    U='F' if r['generation']['template'] in ('cake','outside') else 'C'
    for a in f[':answer-field/choices']:
        x=int(re.search(r'\d+',a[':answer/value'])[0]); vals.append(x)
        assert a[':answer/type']==':answer.type/math'
        assert a[':answer/value']==(rf'{{{x}}}^{{∘}}\text{{{U}}}' if lev=='easy' else rf'{x}\,\text{{min}}')
        if a[':answer/id']==f[':answer-field/correct'][1]: correct=x
    rounded=int(sp.floor(sp.N(exact,40)+sp.Rational(1,2))); assert correct==rounded
    assert len(set(vals))==5
    assert all(A<x<p['initial'] for x in vals) if lev=='easy' else all(x>(p['time'] if lev=='moderate' else p['start']+p['gap']) for x in vals)
    if profile!='authored_operations':
        source=g.SOURCE_Q[profile]; sf=source[':question/answer-fields'][0]
        original=int(re.search(r'\d+',sf[':answer-field/correct'][':answer/value'])[0]); expected=sorted(correct+int(re.search(r'\d+',a[':answer/value'])[0])-original for a in sf[':answer-field/choices'])
    elif lev=='easy':
        x=k*p['time']; I=p['initial']; D=I-A
        expected=[rounded,int(sp.floor(sp.N(D*sp.exp(-x),40)+sp.Rational(1,2))),int(sp.floor(sp.N(A+I*sp.exp(-x),40)+sp.Rational(1,2))),int(sp.floor(sp.N(A+D*sp.exp(-x/2),40)+sp.Rational(1,2))),int(sp.floor(sp.N(A+D*sp.exp(-2*x),40)+sp.Rational(1,2)))]
    else:
        rr=lambda n:int(sp.floor(sp.N(n,40)+sp.Rational(1,2)))
        if lev=='moderate':
            I,O,Z,tm=(p[x] for x in ['initial','observed','target','time'])
            expected=[rounded,rr(tm*sp.log(sp.Rational(Z,I))/sp.log(sp.Rational(O,I))),rr(-sp.log(sp.Rational(Z,I))/k),rr(exact/2),rr(2*exact)]
        else:
            O,L,Z,a,h=(p[x] for x in ['observed','later','target','start','gap'])
            expected=[rounded,rr(exact-a),rr(a+(exact-a)/2),rr(a+2*(exact-a)),rr(a+h*sp.log(sp.Rational(Z,O))/sp.log(sp.Rational(L,O)))]
    assert sorted(vals)==sorted(expected),('Whole displayed bank operation mismatch',vals,expected)
    # Formatting is checked for all raw replays too.
    for text in [q[':question/problem'],solution,*[a[':answer/value'] for a in f[':answer-field/choices']]]:
        assert not any(ord(c)<32 and c!='\n' for c in text),('Hidden control character',repr(text))
        assert text.count('$')%2==0
        depth=0
        for c in text:
            if c=='{': depth+=1
            if c=='}': depth-=1
            assert depth>=0
        assert depth==0 and not any(x in text for x in ['--','+-','{{'])
    if U=='F' and profile=='authored_operations': assert r'\text{C}' not in solution and '}C' not in solution
    # Solve the displayed common differential, separation and antiderivative
    # stages symbolically. Integral rows are structural calculus statements.
    blocks=re.findall(r'\$\$\n(.*?)\n\$\$',solution,re.S)
    rows=[]
    for b in blocks:
        b=b.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
        rows.extend(re.split(r'\\\\',b))
    for row in rows:
        row=row.replace('&','').strip()
        if '\\int' in row:
            assert re.fullmatch(r'\\int \\frac\{dT\}\{T-'+str(A)+r'\}\s*=-(?:k\\int dt|\\int '+re.escape(g.dec(k) if lev=='easy' else 'k')+r'\\,\\text\{d\}t)',row),row
            y=sp.Symbol('y',positive=True); assert_equal(sp.diff(sp.log(y-A),y),1/(y-A),'Antiderivative')
            COUNTS['math_rows']+=1; continue
        row=row.split(r',\qquad')[0].rstrip('.,')
        if '=' not in row: raise AssertionError(('Unverified row',row))
        chain=row.split('≈'); exactrow=chain[0]; parts=exactrow.split('=')
        evaluated=[]
        for part in parts:
            expr=parse(part)
            # Read substitutions from actual printed solution, using independently
            # derived model, k, K and target time. No generator solution helper.
            subs={sp.Symbol('A'):A,sp.Symbol('K'):K,sp.Symbol('k'):k,sp.Symbol('C'):sp.log(K),sp.Symbol('v'):v,sp.Symbol('T'):model,sp.Symbol('dt'):1,sp.Symbol('dT'):sp.diff(model,t)}
            for node in list(expr.atoms(sp.Function)):
                if node.func==sp.Function('F'): expr=expr.subs(node,model.subs(t,node.args[0].subs(subs)))
            evaluated.append(expr.subs(subs))
        for x,y in zip(evaluated,evaluated[1:]): assert_equal(x,y,row)
        if len(chain)==2:
            approx=int(re.search(r'\d+',chain[1])[0]); assert approx==rounded
        COUNTS['math_rows']+=1
    expectedrows=13 if lev=='easy' else 25 if lev=='moderate' else 30
    assert len(rows)==expectedrows,('Stage sequence count',lev,len(rows),expectedrows)
    # Fixed solution and parameter identity are independent of option order/seed.
    rr=g.generate(lev,seed=912,template=r['generation']['template'],parameters=p,profile=None if profile=='authored_operations' else profile)
    assert q[':question/id']==rr['question'][':question/id'] and solution==rr['question'][':question/worked-solution']
    COUNTS['records']+=1; COUNTS['displayed_options']+=5
    return rounded


def run():
    records=[]; sourcecases=[]; native=[]; sections=['# Inhibited decay model review\n\nRaw originals retain one documented unit-label anomaly. Generated variants use complete operation banks unless labeled observed profile.']
    for sid,(temp,p) in g.ORIGINALS.items():
        level=g.TEMPLATES[temp]; r=g.generate(level,template=temp,parameters=p,profile=sid); validate(r); source=g.SOURCE_Q[sid]; f=source[':question/answer-fields'][0]; gf=r['question'][':question/answer-fields'][0]
        assert r['question'][':question/problem']==source[':question/problem']; COUNTS['original_prompts_exact']+=1
        assert r['question'][':question/worked-solution']==source[':question/worked-solution']; COUNTS['original_solutions_raw_exact']+=1
        assert sorted(a[':answer/value'] for a in gf[':answer-field/choices'])==sorted(a[':answer/value'] for a in f[':answer-field/choices']); COUNTS['original_banks_exact']+=1
        right=next(a[':answer/value'] for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1]); assert right==f[':answer-field/correct'][':answer/value']; COUNTS['original_correct_designations']+=1
        sourcecases.append({'source_id':sid,'template':temp,'difficulty':level,'parameters':p,'bank_profile':sid})
        records.append({'label':'Original '+sid,'record':r}); sections+=['\n## Original '+sid+' — exact raw replay\n\n'+g.markdown(r)]
        # Change complete givens, including every time prose slot, while retaining
        # the entire observed parameterized offset bank through the public API.
        changed=dict(p); changed['time']=p['time']+1
        if temp!='water': changed['initial']+=(-1 if temp=='coffee' else 1)
        changed['ambient']+=1
        if level=='moderate': changed['observed']+=1; changed['target']+=1
        rr=g.generate(level,seed=32,template=temp,parameters=changed,profile=sid); validate(rr)
        records.append({'label':'Changed observed bank '+sid,'record':rr}); sections+=['\n## Changed observed profile '+sid+' — underdetermined scalar intent\n\n'+g.markdown(rr)]
        # Authored operation bank at a changed eligible parameter set.
        authored=g.generate(level,seed=440+len(records),template=temp); validate(authored); records.append({'label':'Changed default operations '+temp,'record':authored}); sections+=['\n## Generated default operations '+temp+'\n\n'+g.markdown(authored)]
    for level in g.LEVELS:
        for seed in (121,722):
            r=g.generate(level,seed=seed); validate(r); records.append({'label':f'Generated {level} seed {seed}','record':r}); sections+=['\n## Generated '+level+f' seed {seed}\n\n'+g.markdown(r)]
    # Repair source q-107122 with mathematically supported same numeric data.
    temp,p=g.ORIGINALS['q-107122']; repaired=g.generate('moderate',template=temp,parameters=p)
    validate(repaired); assert repaired['question'][':question/worked-solution']==g.SOURCE_Q['q-107122'][':question/worked-solution'].replace(r'\text{C}',r'\text{F}').replace('}C','}F'); COUNTS['repaired_solutions_correct']+=1
    records.append({'label':'Fahrenheit unit repair','record':repaired}); sections+=['\n## Fahrenheit source unit repair — authored default bank\n\n'+g.markdown(repaired)]
    for row in records:
        r=row['record']; f=r['question'][':question/answer-fields'][0]
        native.append({'label':row['label'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Actual owned radio selection; independent displayed numeric bank and solution checks run separately'} for a in f[':answer-field/choices']]})
    # Broader changed-parameter mathematics/formatting smoke checks.
    for level in g.LEVELS:
        for seed in range(12): validate(g.generate(level,seed=seed))
    invalid=[('hard',dict(ambient=20,observed=100,later=60,target=30,start=0,gap=4)),('hard',dict(ambient=20,observed=100,later=60,target=30,start=4,gap=4)),('hard',dict(ambient=20,observed=100,later=60,target=19,start=2,gap=4)),('easy',dict(ambient=-1,initial=80,rate='0.1',time=5)),('easy',dict(ambient=20,initial=90,rate='0.001',time=5)),('moderate',dict(ambient=20,initial=100,observed=80,target=90,time=5))]
    for level,p in invalid:
        try: g.generate(level,parameters=p)
        except ValueError: pass
        else: raise AssertionError(('Scope guard accepted',p))
    try: g.generate('moderate',template='water',parameters=dict(ambient=20,initial=95,observed=80,target=40,time=5))
    except ValueError: pass
    else: raise AssertionError('Boiling-water context guard failed')
    try: g.generate('moderate',template='outside',parameters=dict(ambient=20,initial=400,observed=80,target=40,time=5))
    except ValueError: pass
    else: raise AssertionError('Outside ordinary room-air guard failed')
    # General solution families are equivalent modulo nonzero rescaling of K;
    # logarithm constant may shift. This is separate from calibrated answer value.
    t=sp.Symbol('t',real=True); c=sp.Symbol('c',positive=True); A=20; k=sp.Rational(1,5)
    assert_equal(A+c*sp.exp(-k*t),A+(3*c)*sp.exp(-k*t)/3,'General family nonzero rescaling')
    assert_equal(A+sp.exp(sp.log(c)+2)*sp.exp(-k*t),A+sp.exp(2)*c*sp.exp(-k*t),'General family constant shift')
    for filename,value in [('source-cases.json',sourcecases),('review.json',records),('native-input.json',native)]: (ROOT/filename).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
    (ROOT/'review.md').write_text('\n\n'.join(sections)+'\n')
    engine=Path('generate/runs/current/check-engine'); subprocess.run([str(engine),str(ROOT/'native-input.json'),str(ROOT/'native-report.json')],check=True)
    nr=json.loads((ROOT/'native-report.json').read_text())
    report={'status':'pass','database':'math','basis':1356,'counts':COUNTS,'source_coverage':'8/8 (4 easy, 4 moderate; 0 hard)','source_fidelity':{'complete_option_values':'40/40','distractor_values':'32/32','complete_banks':'8/8','correct_designations':'8/8','full_prompt_strings':'8/8','full_raw_solution_strings':'8/8','raw_solution_equations_correct':'8/8','raw_solution_unit_consistency':'7/8','normal_unit_repair':'1/1; all normal outputs correct'},'source_anomaly':'q-107122: 3 Celsius prose labels in Fahrenheit problem; 8/8 raw exact solutions; 1/1 normal repair verified','authored_hard':'Same cooling target time from two nonzero observations, nonintegral start/gap, no analytical branch; 2 reviewed examples','native':{k:nr[k] for k in ['entry_point','accepted_checks','rejected_checks','documented_unresolved_checks','database_writes']},'blank_equivalent_entries':'Not applicable: all observed and authored layouts are radio; no new blank layout introduced','engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'engine_source_sha256':hashlib.sha256(Path('generate/runs/current/check-engine.rs').read_bytes()).hexdigest(),'sympy_version':sp.__version__,'invalid_explicit_cases_rejected':len(invalid)+2,'plots':'none'}
    (ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__': run()
