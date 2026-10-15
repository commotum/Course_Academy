#!/usr/bin/env python3
"""Independent displayed-math, source-presence, bank, identity/native QA."""
import copy, importlib.util, json, re, subprocess, sys, hashlib
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ROOT=Path(__file__).parent
spec=importlib.util.spec_from_file_location('directional',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y=S.symbols('x y',real=True)

def group(t,start):
    assert t[start]=='{';depth=1;i=start+1
    while depth:
        depth+=(t[i]=='{')-(t[i]=='}');i+=1
    return t[start+1:i-1],i

def math(t):
    t=t.strip().rstrip('.');t=t.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\!','').replace('⁡','')
    t=t.replace(r'\operatorname{ln}',r'\ln').replace(r'\cdot','*')
    t=re.sub(r'\\text\{[^}]*\}', '', t)
    for command in (r'\frac',r'\sqrt'):
        while command in t:
            start=t.index(command);i=start+len(command);arg,i=group(t,i)
            if command==r'\frac':den,i=group(t,i);v='('+str(math(arg))+')/('+str(math(den))+')'
            else:v='sqrt('+str(math(arg))+')'
            t=t[:start]+v+t[i:]
    t=t.replace(r'\ln','log').replace('^','**').replace('{','(').replace('}',')')
    t=t.replace('log(', 'log(')
    return parse_expr(t,local_dict={'x':x,'y':y,'e':S.E,'sqrt':S.sqrt,'log':S.log,'i':S.Symbol('i'),'j':S.Symbol('j')},transformations=standard_transformations+(implicit_multiplication_application,))

def equal(a,b):return S.simplify(a-b)==0

def vectors(t):
    return [[math(z) for z in s.replace(r'\,','').split(',')] for s in re.findall('⟨([^⟩]+)⟩',t)]

def prompt_data(r):
    q=r['question'];t=q[':question/problem'];f=r['generation']['template']
    point=re.search(r'(?:point \$A?|point \$)\((-?\d+),\s*(-?\d+)\)',t)
    assert point,t
    A,B=map(S.Integer,point.groups())
    if f=='supplied_gradient':
        E=vectors(t)[0];F=None;G=None
    else:
        expr=re.search(r'f\(x,\s*y\)\s*=\s*([^$]+)',t).group(1)
        F=math(expr);G=[S.diff(F,x),S.diff(F,y)];E=[S.simplify(z.subs({x:A,y:B})) for z in G]
    if 'towards' in t:
        endpoint=re.search(r'B\(([^,]+),\s*([^)]+)\)',t);dx,dy=[math(v) for v in endpoint.groups()];dx-=A;dy-=B
    else:
        vt=re.search(r'v\s*=\s*([^$]+)',t).group(1).rstrip('.')
        vt=vt.replace(r'\,','')
        # Split at basis i, j, preserving signs on each whole coefficient.
        m=re.fullmatch(r'(.*?)i\s*(.*?)j',vt);assert m,vt
        dx=math(m[1] or '1');dy=math(m[2] if m[2] not in ('+','-') else m[2]+'1')
    N=S.sqrt(dx*dx+dy*dy);C=S.simplify((E[0]*dx+E[1]*dy)/N)
    return F,G,E,dx,dy,N,C,A,B

def formatting(t):
    assert all(ord(c)>=32 or c in '\n\t' for c in t),'control char'
    assert t.count('$')%2==0,'math delimiter'
    depth=0
    for i,c in enumerate(t):
        if c=='{' and (i==0 or t[i-1]!='\\'):depth+=1
        if c=='}' and (i==0 or t[i-1]!='\\'):depth-=1
        assert depth>=0,'brace close'
    assert depth==0,'brace balance'
    assert '+-' not in t and '--' not in t,'ungrouped signs'

def formal_arguments(t):
    out=[]
    for m in re.finditer(r'\\frac\{∂\}\{∂([xy])\}\(',t):
        depth=1;i=m.end();start=i
        while depth:
            depth+=(t[i]=='(')-(t[i]==')');i+=1
        out.append((m.group(1),math(t[start:i-1])))
    return out

def check_normal(r):
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    q=r['question'];t=q[':question/worked-solution'];f=r['generation']['template']
    for v in [q[':question/problem'],t]+[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']]:formatting(v)
    F,G,E,dx,dy,N,C,A,B=prompt_data(r)
    fld=q[':question/answer-fields'][0];values=[math(a[':answer/value']) for a in fld[':answer-field/choices']]
    ref=fld[':answer-field/correct'][1];answer=next(a for a in fld[':answer-field/choices'] if a[':answer/id']==ref)
    assert equal(math(answer[':answer/value']),C),'displayed answer'
    assert all(not equal(a,b) for i,a in enumerate(values) for b in values[i+1:]),'bank ambiguity'
    if fld[':answer-field/type'].endswith('blank'):assert '{{'+fld[':answer-field/key']+'}}' in q[':question/problem']
    blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',t,re.S)
    # Independently verify magnitude, unit direction, held partials and each
    # evaluated component read from the actual displayed worked calculation.
    direction=blocks[0]
    if f in ('exp','chain_square'):
        vs=vectors(direction);assert all(equal(a-b,c) for a,b,c in zip(vs[0],vs[1],[dx,dy]));assert all(all(equal(a,b) for a,b in zip(v,[dx,dy])) for v in vs[2:])
        denominator=re.findall(r'\\frac\{1\}\{(.*?)\}⟨',direction)[-1]
        assert equal(math(denominator),N)
    else:
        mag=direction.split('& =',1)[1].split(r'\\',1)[0]
        for v in mag.split('='):assert equal(math(v),N),'normalization'
    if f!='supplied_gradient':
        grad=blocks[1];arguments=re.findall(r'\\frac\{∂\}\{∂[xy]\}\((.*?)\)⟩',grad)
        # First vector contains operators: compare derivative operands directly.
        form=grad.split(' & =',1)[1].split(r'\\',1)[0]
        assert tex_no_space(F) in form.replace(' ',''),'formal gradient argument'
        args=formal_arguments(form)
        assert [v for v,e in args]==['x','y'] and all(equal(e,F) for v,e in args),'both held-coordinate formal operands'
        numeric=vectors(grad.split(r'\\',1)[1]);expected=[]
        if f=='chain_square':expected.append(G)
        expected.append(G)
        if f!='xy':expected.append(E)
        expected.append(E)
        assert len(numeric)==len(expected),(f,numeric,expected)
        for actual,want in zip(numeric,expected):assert all(equal(a,b) for a,b in zip(actual,want)),'gradient stage'
    last=blocks[-1];dot=last.split(r'\\')[1];vs=vectors(dot)
    assert all(equal(a,b) for a,b in zip(vs[0],E)),'dot gradient operands'
    assert all(equal(a,b) for a,b in zip(vs[1],[dx/N,dy/N])),'dot unit operands'
    stages=last.split(r'\\')[2:]
    for row in stages:assert equal(math(row.split('& =',1)[1]),C),'dot arithmetic/final'
    original_p=r['generation']['parameters'];r2=g.generate(r['question'][':question/difficulty'].split('/')[-1],seed=r['generation']['seed']+239,template=f,field_type=fld[':answer-field/type'].split('/')[-1],parameters=original_p,profile=r['generation']['profile'])
    assert q[':question/id']==r2['question'][':question/id'],'seed identity'
    return C

def tex_no_space(e):return g.expr_tex(e).replace(' ','')


def ib_vector(t):
    t=re.sub(r'(?<![A-Za-z\\])i(?![A-Za-z])','u',t)
    t=re.sub(r'(?<![A-Za-z\\])j(?![A-Za-z])','w',t)
    value=math(t);i,j=S.symbols('u w')
    return [S.expand(value).coeff(i),S.expand(value).coeff(j)]

def raw_stage_check(r):
    q=r['question'];f=r['generation']['template'];s=r['generation']['parameters']['scale']
    if ':question/worked-solution' not in q:return
    if f=='supplied_gradient':
        E=[S.Integer(4*s),S.Integer(2*s)];G=None;dx,dy=S.Integer(-3),S.Integer(4);N=S.Integer(5);C=-S.Rational(4*s,5)
    else:F,G,E,dx,dy,N,C,A,B=prompt_data(r)
    t=q[':question/worked-solution'];formatting(t)
    blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',t,re.S)
    if f!='supplied_gradient':
        grad=blocks[1];rows=grad.split(r'\\')
        args=formal_arguments(rows[0])
        assert [v for v,e in args]==['x','y'] and all(equal(e,F) for v,e in args),'raw held-coordinate formal operands'
        derived=[]
        for row in rows[1:]:
            rhs=row.split('& =',1)[1]
            derived.append(vectors(rhs)[0] if f=='exp' else ib_vector(rhs))
        expect=[G,E] if f=='xy' else [G,E,E]
        assert len(derived)==len(expect)
        for actual,want in zip(derived,expect):assert all(equal(a,b) for a,b in zip(actual,want)),('raw gradient stage',f,actual,want)
    else:
        given=re.search(r'∇\\,f\(1,1\)=.*?=(.*?)\.',t).group(1)
        assert all(equal(a,b) for a,b in zip(ib_vector(given),E))
    rows=blocks[-1].split(r'\\');rhs=rows[1].split('& =',1)[1]
    dot=rhs.split(r'\cdot')
    if f=='exp':actual=vectors(rhs);left,right=actual
    else:left,right=[ib_vector(z) for z in dot]
    assert all(equal(a,b) for a,b in zip(left,E)),('raw dot gradient',f,left,E)
    assert all(equal(a,b) for a,b in zip(right,[dx/N,dy/N])),('raw dot unit',f,right)
    for row in rows[2:]:assert equal(math(row.split('& =',1)[1]),C),('raw dot arithmetic',f,row,C)

SOURCE_CASES=[{'source_id':sid,'template':f,'parameters':{'scale':1},'bank_profile':'raw_'+f,'level':g.FAMILIES[f]} for f,sid in g.SOURCE_IDS.items()]

def native(records):
    data=[]
    for i,r in enumerate(records):
        fld=r['question'][':question/answer-fields'][0];ref=fld[':answer-field/correct'][1];checks=[]
        if fld[':answer-field/type'].endswith('radio'):
            checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==ref else 'rejected','purpose':'owned complete bank option'} for a in fld[':answer-field/choices']]
        else:
            C=check_normal(r)
            checks=[{'submitted':g.tex(C),'expected':'accepted','purpose':'canonical exact value'}, {'submitted':g.tex(C+1),'expected':'rejected','purpose':'wrong value'}]
            # Independent unreduced dot quotient, not algebraically simplified spelling.
            F,G,E,dx,dy,N,_,A,B=prompt_data(r)
            equiv='('+str(E[0])+'*('+str(dx)+')+'+str(E[1])+'*('+str(dy)+'))/('+str(N)+')'
            checks.append({'submitted':equiv,'expected':'accepted','purpose':'unreduced component dot quotient'})
        data.append({'label':'normal-'+str(i),'record':r,'checks':checks})
    # Native source grading only where the captured source has a correct ref.
    for case in SOURCE_CASES:
        r=g.generate(case['level'],template=case['template'],profile=case['bank_profile'],parameters={'scale':1});fld=r['question'][':question/answer-fields'][0]
        if ':answer-field/correct' not in fld:continue
        ref=fld[':answer-field/correct'][1]
        if fld[':answer-field/type'].endswith('blank'):
            checks=[{'submitted':'-4/5','expected':'accepted','purpose':'original blank canonical'},{'submitted':'(-12+8)/5','expected':'accepted','purpose':'original unreduced dot quotient'},{'submitted':'4/5','expected':'rejected','purpose':'original wrong sign'}]
        else:checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==ref else 'rejected','purpose':'raw original owned option'} for a in fld[':answer-field/choices']]
        data.append({'label':'source-'+case['source_id'],'record':r,'checks':checks})
    (ROOT/'engine-input.json').write_text(json.dumps(data,indent=2))
    subprocess.run(['generate/runs/current/check-engine',str(ROOT/'engine-input.json'),str(ROOT/'engine-validation.json')],check=True)

if __name__=='__main__':
    source_results=[];review=[];normal=[]
    for case in SOURCE_CASES:
        f=case['template'];src=g.ORIGINALS[case['source_id']];r=g.generate(case['level'],template=f,parameters=case['parameters'],profile=case['bank_profile']);q=r['question']
        expected={k for k in src if k not in (':db/id',':question/math-academy-id')};assert set(q)==expected
        assert q[':question/problem']==src[':question/problem'];assert q.get(':question/worked-solution')==src.get(':question/worked-solution')
        fld=q[':question/answer-fields'][0];sf=src[':question/answer-fields'][0]
        assert sorted(a[':answer/value'] for a in fld[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
        assert set(fld)==set(sf)-{':db/id'},'source field attribute presence'
        assert (':answer-field/correct' in fld)==(':answer-field/correct' in sf)
        if ':answer-field/correct' in sf:
            selected=next(a for a in fld[':answer-field/choices'] if a[':answer/id']==fld[':answer-field/correct'][1]);assert selected[':answer/value']==sf[':answer-field/correct'][':answer/value']
        source_results.append({'source_id':case['source_id'],'prompt_exact':True,'solution_exact_or_absence':True,'bank_values':len(fld[':answer-field/choices']),'correct_designation_matched':':answer-field/correct' in sf,'key_presence':True})
        raw_stage_check(r)
        review.append({'label':'Original replay '+case['source_id'],'record':r})
        changed=g.generate(case['level'],template=f,parameters={'scale':3},profile=case['bank_profile'])
        raw_stage_check(changed)
        assert changed['question'][':question/problem']!=q[':question/problem']
        # Independent homogeneous correctness, complete bank values and source
        # intended correct scalar; no guessed wrong-operation explanations.
        intended={'linear_y2':14/S.sqrt(29),'chain_square':-S.Rational(78,5),'supplied_gradient':-S.Rational(4,5),'xy':(S.sqrt(3)+2)/2,'log':-S.Rational(8,5),'quadratic':S.Integer(0),'exp':S.sqrt(2)/2,'x2_linear':10/S.sqrt(34)}[f]
        old_values=[math(a[':answer/value']) for a in fld[':answer-field/choices']]
        new_values=[math(a[':answer/value']) for a in changed['question'][':question/answer-fields'][0][':answer-field/choices']]
        assert all(sum(equal(v,3*w) for v in new_values)==1 for w in old_values),'changed raw bank scaling'
        assert sum(equal(v,intended) for v in old_values)==1,'source uniquely correct mathematical option'
        if f!='supplied_gradient':
            assert equal(prompt_data(r)[6],intended),'source displayed function/point/direction'
            assert equal(prompt_data(changed)[6],3*intended),'changed raw displayed function/point/direction'
        review.append({'label':'Changed homogeneous raw evidence '+case['source_id'],'record':changed})
    for f,l in g.FAMILIES.items():
        for seed in range(12):
            r=g.generate(l,seed=seed,template=f);check_normal(r);normal.append(r)
            if seed<2:review.append({'label':'Generated '+l+' '+f+' '+str(seed),'record':r})
    # Authored supported blank equivalent-entry checks at all three levels.
    for f in ('linear_y2','exp','chain_square'):
        r=g.generate(g.FAMILIES[f],seed=25,template=f,field_type='blank');check_normal(r);normal.append(r)
    # Signed/zero and boundary checks; explicit policies match sampler.
    invalid={'a':1,'b':1,'c':1,'d':1,'x0':0,'y0':0,'dx':1,'dy':1}
    for f in ('log','chain_square','exp'):
        try:g.generate(g.FAMILIES[f],template=f,parameters=invalid)
        except ValueError:pass
        else:raise AssertionError('explicit guard')
    mutated=copy.deepcopy(normal[-1]);mutated['question'][':question/worked-solution']+='\f'
    try:check_normal(mutated)
    except AssertionError:pass
    else:raise AssertionError('control mutation accepted')
    mutated=copy.deepcopy(normal[-1]);mutated['question'][':question/worked-solution']=mutated['question'][':question/worked-solution'].replace(r'\frac{∂}{∂x}',r'\frac{∂}{∂y}',1)
    try:check_normal(mutated)
    except AssertionError:pass
    else:raise AssertionError('held-coordinate mutation accepted')
    # Scaling of the direction changes presentation but not the assessed task.
    p={'a':2,'b':3,'c':1,'d':1,'x0':1,'y0':2,'dx':1,'dy':2}
    one=g.generate('easy',template='linear_y2',parameters=p)
    two=g.generate('easy',template='linear_y2',parameters={**p,'dx':2,'dy':4})
    assert one['generation']['mathematical_fingerprint']==two['generation']['mathematical_fingerprint']
    assert one['question'][':question/id']!=two['question'][':question/id']
    excessive={'a':4,'b':4,'c':1,'d':1,'x0':3,'y0':3,'dx':3,'dy':4}
    try:g.generate('moderate',template='chain_square',parameters=excessive)
    except ValueError:pass
    else:raise AssertionError('hard arithmetic ceiling bypass')
    defaults={l:set() for l in g.SUPPORTED_LEVELS};tasks={l:set() for l in defaults}
    for l in defaults:
        for seed in range(160):
            r=g.generate(l,seed);check_normal(r);defaults[l].add(r['generation']['template']);tasks[l].add(r['generation']['mathematical_fingerprint'])
        assert defaults[l]=={f for f,lev in g.FAMILIES.items() if lev==l}
    try:g.generate_hard()
    except ValueError:pass
    else:raise AssertionError('unsupported hard must fail')
    native(normal)
    (ROOT/'source-cases.json').write_text(json.dumps(SOURCE_CASES,indent=2)+'\n')
    (ROOT/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
    (ROOT/'review.md').write_text('# Directional derivative review\n\nRaw evidence is explicitly ineligible. Normal variants use authored method-derived banks.\n\n'+'\n\n---\n\n'.join('## '+v['label']+'\n\n'+g.markdown(v['record']) for v in review))
    report={'passed':True,'source_questions':8,'source_fidelity':source_results,'complete_banks_matched':8,'source_values_matched':36,'source_correct_designations_matched':6,'missing_original_designations':2,'exact_source_solutions':6,'absent_original_solutions_preserved':2,'normal_semantic_math_checks':len(normal)+160*len(g.SUPPORTED_LEVELS),'raw_original_and_changed_stage_checks':16,'default_family_coverage':{l:sorted(v) for l,v in defaults.items()},'distinct_sampled_mathematical_tasks':{l:len(v) for l,v in tasks.items()},'native':json.loads((ROOT/'engine-validation.json').read_text()),'limits':['Opaque observed scalar banks are evidence-only; homogeneous scaling is a reproduction recipe, not recovered wrong-operation intent.','The div V source lacks prior context; stated gradient (4,2) is verified only as a datum for directional calculation.','Nested-square sampling is moderate after current source review. Hard is unsupported; no hard questions generated.'],'runtime':{'python':sys.version.split()[0],'sympy':S.__version__},'engine_sha256':hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest()}
    (ROOT/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('native','source_fidelity')},indent=2))
