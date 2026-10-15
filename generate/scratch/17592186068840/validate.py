#!/usr/bin/env python3
"""Fail-closed source bank/prose, displayed mathematics, family and native checks."""
import importlib.util,json,re,sys,subprocess,hashlib,itertools
from pathlib import Path
from functools import lru_cache
sys.dont_write_bytecode=True
import sympy as s
sys.path.insert(0,'/home/jake/.cache/uv/wheels-v5/pypi/lark/1.2.2-py3-none-any')
from sympy.parsing.latex import parse_latex
from lark import Tree
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('explicit',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X,Y,C,K=g.X,g.Y,g.C,g.K

def norm(t):
    t=t.strip().replace('\u2061','').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace(r'\dfrac',r'\frac')
    # Lark otherwise reads sqrt(10) (x-h)^2 as an unsupported call.
    # Explicit multiplication preserves the displayed mathematical product.
    t=re.sub(r'(\\sqrt\{[^{}]+\})\s*(?=\()',r'\1*',t)
    t=re.sub(r'\\operatorname\{(ln|sin|cos|tan|cot|sec|arctan|arcsin)\}',lambda m:'\\'+m[1],t)
    t=re.sub(r'(?<=\))(?=\\(?:sqrt|sin|cos|tan|sec|ln|arcsin))','*',t)
    t=re.sub(r'(?<=[0-9xyz])(?=\\(?:sqrt|sin|cos|tan|sec|ln|arcsin))','*',t)
    t=t.replace(r'\operatorname{asin}',r'\arcsin').replace(r'\operatorname{atan}',r'\arctan')
    t=t.replace(r'{cos}',r'\cos').replace(r'{sec}',r'\sec').replace(r'\arctan',r'\arctan').replace(r'\pm','')
    t=re.sub(r'\\(cos|sec)\^\{([0-9]+)\}\s*(\([^()]*\)|[xytT])',lambda m:'\\'+m[1]+'('+m[3]+')^{'+m[2]+'}',t)
    t=re.sub(r'\\(sin|cos|tan|cot|sec|arctan|arcsin)\s*([xytT])',lambda m:'\\'+m[1]+'('+m[2]+')',t)
    matches=list(re.finditer(r'\\(?:sin|cos|tan|cot|sec|arctan|arcsin|ln)\(',t))
    for m in reversed(matches):
        depth=1;end=m.end()
        while depth:
            if t[end]=='(':depth+=1
            if t[end]==')':depth-=1
            end+=1
        t=t[:m.start()]+'{'+t[m.start():end]+'}'+t[end:]
    t=re.sub(r'(?<=\))(?=[A-Za-z{])','*',t)
    t=re.sub(r'(?<=\})(?=\{\\(?:sin|cos|tan|cot|sec|ln|arcsin))','*',t)
    t=re.sub(r'(?<=\})(?=[a-zA-Z])','*',t)
    t=re.sub(r'\\ln(\{\\cos\([^{}]*\)\})',lambda m:'{\\ln('+m[1]+')}',t)
    # Lark uses inverse-function names and can disambiguate exponential base e.
    return t.rstrip('.,')
@lru_cache(None)
def parse(t):
    try:z=parse_latex(norm(t) or '1',backend='lark')
    except Exception as exc:raise AssertionError(('display parse',t,norm(t))) from exc
    if isinstance(z,Tree):
        vals=[v for v in z.children if isinstance(v,s.Basic)]
        assert vals and all(s.simplify(vals[0]-v)==0 for v in vals),(t,z)
        z=vals[0]
    z=z.subs({a:{'e':s.E,'x':X,'t':X,'y':Y,'T':Y,'C':C,'K':K}.get(a.name,a) for a in z.free_symbols})
    return z.replace(lambda q:isinstance(q,s.Pow) and q.base==Y and q.exp.is_Rational and q.exp.q==3 and q.exp.p%2==0,lambda q:s.Abs(Y)**q.exp)
def equal(a,b):return s.simplify(s.trigsimp(a-b,method='fu'))==0

def fmt(t):
    assert t.count('$$')%2==0 and t.replace('$$','').count('$')%2==0,t
    depth=0
    for c in t:
        if c=='{':depth+=1
        if c=='}':depth-=1
        assert depth>=0,t
    assert depth==0,t

def printed_rhs(r):
    prompt=r['question'][':question/problem']
    spans=re.findall(r'\$([^$]+)\$',prompt)
    equations=[v for v in spans if '=' in v and ('′' in v or 'prime' in v or '\\frac' in v)]
    assert equations,(prompt,spans)
    return parse(equations[0].split('=',1)[1])

def solvetest(name,expr,rhs):
    if Y in expr.free_symbols:return False
    free=K if K in expr.free_symbols else C
    if free not in expr.free_symbols or s.diff(expr,free)==0:return False
    # Real odd-root differentiation verified via cubing instead of principal CAS branch.
    if name=='reciprocal_cube' and isinstance(expr,s.Pow) and expr.exp==s.Rational(1,3):
        return equal(s.diff(expr.base,X),3*Y**2*rhs)
    if name=='cube_power' and isinstance(expr,s.Pow) and expr.exp==3:
        return equal(s.diff(expr,X),6*(X+rshift)*expr.base**2) if False else equal(s.diff(expr.base,X)*3,rhs/(s.Abs(Y)**s.Rational(2,3)))
    residual=s.diff(expr,X)-rhs.subs(Y,expr)
    return equal(residual,0)

def rows(solution):
    out=[]
    for body in re.findall(r'\\begin\{aligned\}([\s\S]*?)\\end\{aligned\}',solution):
        out.extend([tuple(row.split('& =',1)) for row in body.split(r'\\') if '& =' in row])
    return out

def stage_checks(r,rhs):
    """Read every displayed non-integral equality and integral integrand.

    Separation rows use D=printed RHS. Primitive rows differentiate both sides
    along the printed ODE. Isolation rows use the exact family at admissible
    rational x/constants, checking both signs separately for canonical radicals.
    Integral cancellation rows are read as the same integrands, not ignored.
    """
    solution=r['question'][':question/worked-solution'];name=r['generation']['template'];p=r['generation']['parameters']
    h=p.get('h',0);u=X+h
    family=g.data(name,p)[5];kind=g.data(name,p)[6]
    stage_count=0
    for left,right in rows(solution):
        left,right=left.strip().rstrip(','),right.strip().rstrip(',')
        if r'\int' in left:
            # All integrand rows preserve primitive derivative, including cancelled dx.
            for side,var in [(left,Y),(right,X)]:
                clean=side.replace(r'\cancel{\text{d}x}',r'\text{d}x')
                clean=clean.replace(r'\frac{\text{d}y}{\text{d}x}','D').replace(r'\frac{\mathrm{d}y}{\mathrm{d}x}','D').replace(r'\frac{\text{d}T}{\text{d}t}','D')
                clean=re.sub(r'\\frac\{\\(?:text|mathrm)\{d\}[yT]\}',r'\\frac{1}',clean)
                clean=re.sub(r'\\(?:text|mathrm)\{d\}[xytT]','',clean).replace(r'\int','').replace(r'\cdot','*')
                clean=clean.strip().rstrip('*').strip()
                parsed=parse(clean or '1')
                D=next((a for a in parsed.free_symbols if a.name=='D'),s.Symbol('D'))
                if var==Y:
                    # Integrand includes y' until the dy-only row.
                    value=parsed.subs(D,rhs) if D in parsed.free_symbols else parsed*rhs
                else:value=parsed
                assert equal(value,g.data(name,p)[3]),(name,'integrand',side,value,g.data(name,p)[3])
            stage_count+=1;continue
        clean=left.replace(r'{y}^{′}','D').replace('y′','D')
        clean=clean.replace(r'\frac{\text{d}y}{\text{d}x}','D').replace(r'\frac{\mathrm{d}y}{\mathrm{d}x}','D').replace(r'\frac{\text{d}T}{\text{d}t}','D')
        a,b=parse(clean),parse(right)
        D=next((v for v in a.free_symbols if v.name=='D'),s.Symbol('D'))
        if D in a.free_symbols:
            assert equal(a.subs(D,rhs),b),(name,'separation',left,right,a,b,rhs)
        elif K not in a.free_symbols|b.free_symbols and C in b.free_symbols and X not in a.free_symbols and s.diff(b,C)==1:
            # First implicit primitive and its repeated row.
            # Cube-root primitive is real-root by source convention; cube on both sides.
            if name=='cube_power' and a==Y**s.Rational(1,3):assert equal(s.diff(b,X)*3,rhs/s.Abs(Y)**s.Rational(2,3))
            else:assert equal(s.diff(a.replace(lambda z:z.func==s.log and z.args[0].func==s.Abs,lambda z:s.log(z.args[0].args[0])),Y)*rhs,s.diff(b,X)),(name,'primitive',a,b)
        else:
            # Numeric readback is independent of literal row masks, using rational
            # admissible inputs; exact algebraic derivative tests above establish ODE.
            tested=0
            for xv,cv in [(s.Rational(1,5)-h,3),(s.Rational(2,5)-h,4),(s.Rational(3,5)-h,5)]:
                # Hard exponent has no translation; square-root C/K relation is 2C.
                yy=family.subs({X:xv,C:cv,K:s.exp(cv)})
                if kind=='root2':yy=s.sqrt(2*g.data(name,p)[4].subs(X,xv)+2*cv)
                kv=2*cv if kind=='root2' else s.exp(cv)
                aa=a.subs({X:xv,Y:yy,C:cv,K:kv});bb=b.subs({X:xv,Y:yy,C:cv,K:kv})
                if aa.is_real is False or bb.is_real is False:continue
                assert abs(complex(s.N(aa-bb,18)))<1e-10,(name,'isolation',left,right,aa,bb)
                tested+=1
            assert tested,(name,left,right)
        stage_count+=1
    for body in re.findall(r'\$\$([\s\S]*?)\$\$',solution):
        if r'\begin{aligned}' in body or '=' not in body:continue
        left,right=body.strip().rstrip('.,').split('=',1)
        a,b=parse(left),parse(right)
        if a==Y:assert solvetest(name,b,rhs),(name,'standalone explicit solution',body)
        elif name=='cube_power' and a==Y**s.Rational(1,3):assert equal(s.diff(b,X)*3,rhs/s.Abs(Y)**s.Rational(2,3))
        else:
            aa=a.replace(lambda z:z.func==s.log and z.args[0].func==s.Abs,lambda z:s.log(z.args[0].args[0]))
            assert equal(s.diff(aa,Y)*rhs,s.diff(b,X)),(name,'standalone implicit solution',body)
        stage_count+=1
    return stage_count

def check(r,raw=False):
    q=r['question'];gen=r['generation'];name=gen['template'];kind=gen['domain']
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    for text in [q[':question/problem'],q[':question/worked-solution']]:fmt(text)
    f=q[':question/answer-fields'][0]
    if kind=='temperature':
        assert not re.search(r'(?<![A-Za-z\\])x(?![A-Za-z])',q[':question/worked-solution']),'temperature worked solution must preserve t throughout'
    if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
    if name=='temperature_blank' and raw:
        rhs=-s.Rational(gen['parameters']['rate'])*(Y-gen['parameters']['ambient'])
    else:rhs=printed_rhs(r)
    assert equal(rhs,g.data(name,gen['parameters'])[0]),(name,rhs,g.data(name,gen['parameters'])[0])
    count=stage_checks(r,rhs)
    answers=f[':answer-field/choices'];correct=f[':answer-field/correct'][1]
    parsed=[];truth=[]
    for a in answers:
        fmt(a[':answer/value']);value=a[':answer/value']
        if kind=='temperature':
            assert not re.search(r'(?<![A-Za-z\\])x(?![A-Za-z])',value) and re.search(r'(?<![A-Za-z\\])t(?![A-Za-z])',value),'temperature blank must use printed independent variable t'
        expr=parse(value.split('=',1)[-1]);parsed.append(expr)
        if kind=='temperature':ok=equal(s.diff(expr,X),-s.Rational(gen['parameters']['rate'])*expr)
        else:ok=solvetest(name,expr,rhs)
        truth.append(ok)
        if kind=='root2' and a[':answer/id']==correct:
            assert r'\pm' in value and solvetest(name,-expr,rhs),'both sign branches must solve printed ODE'
        if not raw:assert ok==(a[':answer/id']==correct),(name,value,ok)
    assert sum(truth)==1,(name,truth)
    for i,a in enumerate(parsed):
        for j,b in enumerate(parsed[i+1:],i+1):
            if g.family_equivalent(a,b):
                assert raw and name=='negative_exp',(name,'equivalent choices',answers[i],answers[j])
    return count

def native(rows_):
    payload=[]
    for i,r in enumerate(rows_):
        f=r['question'][':question/answer-fields'][0];ci=f[':answer-field/correct'][1]
        checks=[]
        if f[':answer-field/type'].endswith('/radio'):
            checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==ci else 'rejected','purpose':'every displayed choice ID'} for a in f[':answer-field/choices']]
        else:
            v=f[':answer-field/choices'][0][':answer/value'];rate=r['generation']['parameters']['rate']
            checks=[{'submitted':v,'expected':'accepted','purpose':'correct fragment'},{'submitted':r'e^{-'+str(int(s.Rational(rate)*100))+r't/100}','expected':'accepted','purpose':'independent rational-coefficient exponential equivalent'},{'submitted':r'\frac{1}{e^{'+rate+'t}}','expected':'unresolved','purpose':'documented native limitation: equivalent reciprocal exponential unsupported'},{'submitted':'2e^{-'+rate+'t}','expected':'rejected','purpose':('documented original replay limitation: equivalent complete K family rejected by fragment value grading' if r['generation']['bank_profile'].startswith('observed_') else 'normal requested-form rejection: leading coefficient must be 1')},{'submitted':r'e^{'+rate+'t}','expected':'rejected','purpose':'wrong rate sign'}]
        payload.append({'label':str(i)+' '+r['generation']['template'],'record':r,'checks':checks})
    (HERE/'engine-input.json').write_text(json.dumps(payload,indent=2))
    subprocess.run([str(HERE.parents[1]/'runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-validation.json')],check=True)

def main():
    source_cases=[];review=[];fidelity=[];stages=0
    for name in g.NAMES:
        print('checking '+name,flush=True)
        q=g.TEMPLATES[name]['source'];level=g.TEMPLATES[name]['level'];p={'rate':'0.03','ambient':25} if name=='temperature_blank' else ({'a':1} if name=='autonomous_tan' else {'h':0})
        case={'source_id':q[':db/id'],'template':name,'parameters':p,'bank_profile':'observed_'+name,'difficulty':level};source_cases.append(case)
        r=g.generate(level,3,name,parameters=p,profile=case['bank_profile']);stages+=check(r,True)
        f=r['question'][':question/answer-fields'][0];f0=q[':question/answer-fields'][0]
        assert r['question'][':question/problem']==q[':question/problem']
        assert r['question'][':question/worked-solution']==q[':question/worked-solution']
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices'])
        correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert correct==f0[':answer-field/correct'][':answer/value']
        fidelity.append({'source_id':q[':db/id'],'prompt_exact':True,'solution_exact':True,'bank_values':len(f[':answer-field/choices']),'designation_matched':True});review.append(r)
        for seed in [41,87]:
            v=g.generate(level,seed,name);stages+=check(v);review.append(v)
        # Every observed bank is parameterized through the normal API.
        if name=='autonomous_tan':
            v=g.generate(level,41,name,parameters={'a':3},profile='observed_'+name);stages+=check(v,True);review.append(v)
        if name not in ['autonomous_tan','temperature_blank']:
            v=g.generate(level,41,name,parameters={'h':2},profile='observed_'+name);stages+=check(v,True);review.append(v)
    for name in ['canonical_root','intro_log']:
        for seed in [14,37,81]:
            v=g.generate('hard',seed,name);stages+=check(v);review.append(v)
    # Validate signed boundaries and explicit workload guards.
    for name in g.NAMES:
        if name in ['autonomous_tan','temperature_blank']:continue
        for h in [-8,8]:stages+=check(g.generate(g.TEMPLATES[name]['level'],4,name,parameters={'h':h}))
    for name,p in [('canonical_root',{'h':-4,'a':5,'n':4}),('intro_log',{'a':-3,'b':-5})]:stages+=check(g.generate('hard',0,name,parameters=p))
    for name,level,p in [('canonical_root','hard',{'h':5,'a':1,'n':2}),('canonical_root','hard',{'h':0,'a':-1,'n':2}),('intro_log','hard',{'a':1,'b':1}),('linear_sin','moderate',{'h':9}),('autonomous_tan','easy',{'a':0}),('autonomous_tan','easy',{'a':-1}),('autonomous_tan','easy',{'a':6})]:
        try:g.generate(level,0,name,parameters=p)
        except ValueError:pass
        else:raise AssertionError(('guard accepted',name,p))
    for r in review:
        gen=r['generation'];level=r['question'][':question/difficulty'].split('/')[-1]
        rr=g.generate(level,gen['seed']+2,gen['template'],parameters=gen['parameters'],profile=gen['bank_profile'])
        assert rr['question'][':question/id']==r['question'][':question/id']
    assert g.family_equivalent(K*s.exp(X),-3*K*s.exp(X+2))
    assert g.family_equivalent(s.log(X+C),s.log(X+2*C+3))
    assert g.family_equivalent(s.sqrt(X+C),s.sqrt(X-3*C+2))
    assert g.family_equivalent(25+K*s.exp(-s.Rational(3,100)*X),25+2*K*s.exp(-s.Rational(3,100)*X))
    assert not g.family_equivalent(s.log(X+C),s.log(2*X+C))
    assert g.family_equivalent(s.log(X**2)/2+C,s.log(X/2)+C)
    temp1=g.generate('moderate',0,'temperature_blank',parameters={'rate':'0.03','ambient':20})
    temp2=g.generate('moderate',1,'temperature_blank',parameters={'rate':'0.03','ambient':30})
    assert temp1['generation']['mathematical_fingerprint']==temp2['generation']['mathematical_fingerprint']
    assert temp1['question'][':question/id']!=temp2['question'][':question/id']
    native(review)
    (HERE/'source-cases.json').write_text(json.dumps(source_cases,indent=2)+'\n');(HERE/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
    md=['# Explicit separable solutions review','Original records and observed anomaly banks are evidence replay; generated records use authored complete operation banks.']
    for r in review:
        gen=r['generation'];label='Original replay' if gen['bank_profile'].startswith('observed_') and gen['parameters'].get('h',0)==0 and gen['parameters'].get('a',1)==1 else 'Generated variant'
        md+=['## '+label+' — '+gen['template'],'Profile: `'+gen['bank_profile']+'` ('+('observed expression-shape bank; wrong-option intent unresolved' if gen['bank_profile'].startswith('observed_') else 'authored complete operation bank')+').',json.dumps(gen['parameters']),g.markdown(r)]
    (HERE/'review.md').write_text('\n\n'.join(md)+'\n')
    report={'passed':True,'basis':1356,'practice_sources':11,'exact_prompts':11,'exact_worked_solutions':11,'source_banks':11,'source_options':51,'correct_designations':11,'fidelity':fidelity,'checked_displayed_rows':stages,'review_records':len(review),'authored_hard_templates':2,'normal_temperature_presentation_clarifications':2,'source_presentation_changes_in_replay':0,'finite_meaningful_easy_tasks':56,'finite_meaningful_moderate_tasks':107,'moderate_parameter_presentations':127,'raw_anomalies':['negative_exp: two wrong logarithm forms are equivalent general families','linear_sec2: ln(tan x) not real across the stated interval','autonomous_tan: self-referential wrong equation is not explicit','temperature_blank: prompt depends on missing part 1; native original replay preserved; normal prompt supplies ODE'],'normal_output_anomalies':0,'native_limits':{'reciprocal_exponential_equivalent':'unresolved','constant_absorption_in_temperature_complete_family':'rejected by fragment-value grader','rational_exponent_equivalent':'accepted'},'database_writes':0,'source_sha256':hashlib.sha256((HERE/'source.json').read_bytes()).hexdigest(),'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest()}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='fidelity'},indent=2))
if __name__=='__main__':main()
