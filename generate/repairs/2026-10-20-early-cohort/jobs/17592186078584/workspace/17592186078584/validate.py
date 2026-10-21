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
    U='F' if r['generation']['template'] in ('cake','exhaust','outside') else 'C'
    for a in f[':answer-field/choices']:
        x=int(re.search(r'\d+',a[':answer/value'])[0]); vals.append(x)
        assert a[':answer/type']==':answer.type/math'
        assert a[':answer/value']==(rf'{{{x}}}^{{∘}}\text{{{U}}}' if lev=='easy' else rf'{x}\,\text{{min}}')
        if a[':answer/id']==f[':answer-field/correct'][1]: correct=x
    rounded=int(sp.floor(sp.N(exact,40)+sp.Rational(1,2))); assert correct==rounded
    assert len(set(vals))==5
    assert all(A<=x<=p['initial'] for x in vals) if lev=='easy' else all(x>=(p['time'] if lev=='moderate' else p['start']+p['gap']) for x in vals)
    if profile in g.SOURCE_Q:
        source=g.SOURCE_Q[profile]; sf=source[':question/answer-fields'][0]
        original=int(re.search(r'\d+',sf[':answer-field/correct'][':answer/value'])[0])
        expected=sorted(correct+int(re.search(r'\d+',a[':answer/value'])[0])-original for a in sf[':answer-field/choices'])
        assert sorted(vals)==expected,('Complete observed bank mismatch',vals,expected)
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
    if U=='F': assert r'\text{C}' not in solution and '}C' not in solution
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
    rr=g.generate(lev,seed=912,template=r['generation']['template'],parameters=p,profile=profile if profile in g.SOURCE_Q else None)
    assert solution==rr['question'][':question/worked-solution']
    COUNTS['records']+=1; COUNTS['displayed_options']+=5
    return rounded


def run():
    import runpy
    runpy.run_path(str(ROOT.parent/'checks/regressions.py'),run_name='__main__')
if __name__=='__main__': run()
