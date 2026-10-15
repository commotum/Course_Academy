"""Independent rendered nested-operator parser and native application grading.

Parser reads displayed operands rather than generator model/slot metadata.
Source equality and common-sentence stage checks are separate from calculus.
"""
import copy,hashlib,importlib.util,json,re,subprocess,sys,uuid
from functools import lru_cache
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=load(HERE.with_suffix('.py'),'g');F=load(ROOT/'generate/runs/current/root-source-fidelity.py','F')
x=s.Symbol('x',real=True);u=s.Symbol('u',real=True)
def save(n,o):(HERE/n).write_text(json.dumps(o,indent=2,default=str)+'\n')

@lru_cache(None)
def expr(text):
    """Recursive actual TeX: full function arguments, powers, signed factors.

    Unsupported tokens fail closed. In particular trig argument scope is read
    recursively; sin(cos x), cos(sin x) and factors cannot be confused.
    """
    text=text.strip().rstrip('.,').replace('⁡','')
    text=re.sub(r'\\operatorname\{(sin|cos|tan|cot|sec|csc)\}',lambda m:'\\'+m[1],text)
    text=re.sub(r'\{(sin|cos|tan|cot|sec|csc)\}',lambda m:'\\'+m[1],text)
    for old,new in ((r'\left',''),(r'\right',''),(r'\,',''),(r'\qquad',''),(r'\cdot','*'),(r'\dfrac',r'\frac')):text=text.replace(old,new)
    text=re.sub(r'\s+','',text);i=0
    def atom():
        nonlocal i
        assert i<len(text),('missing operand',text)
        if text[i] in '({':
            close=')' if text[i]=='(' else '}';i+=1;v=add();assert i<len(text) and text[i]==close,('group',text,i);i+=1;return v
        if text[i].isdigit():
            j=i
            while i<len(text) and (text[i].isdigit() or text[i]=='.'):i+=1
            return s.Rational(text[j:i])
        if text[i] in 'xu':v={'x':x,'u':u}[text[i]];i+=1;return v
        if text.startswith(r'\pi',i):i+=3;return s.pi
        if text.startswith(r'\frac',i):i+=5;a=atom();b=atom();return a/b
        if text.startswith(r'\sqrt',i):i+=5;return s.sqrt(atom())
        if text[i]=='\\':
            match=re.match(r'\\(sin|cos|tan|cot|sec|csc)',text[i:]);assert match,('unsupported macro',text[i:]);i+=len(match[0]);pow=1
            if i<len(text) and text[i]=='^':i+=1;pow=atom()
            arg=unary() if i<len(text) and text[i] in '+-' else atom()
            return getattr(s,match[1])(arg,evaluate=False)**pow
        raise AssertionError(('unsupported token',text,i))
    def unary():
        nonlocal i
        if i<len(text) and text[i] in '+-':sign=text[i];i+=1;return unary()*(1 if sign=='+' else -1)
        v=atom()
        while i<len(text) and text[i]=='^':i+=1;v=v**atom()
        return v
    def mul():
        nonlocal i
        v=unary()
        while i<len(text) and text[i] not in '+-)}':
            if text[i]=='*':i+=1;v*=unary()
            elif text[i]=='/':i+=1;v/=unary()
            else:v*=unary()
        return v
    def add():
        nonlocal i
        v=mul()
        while i<len(text) and text[i] in '+-':op=text[i];i+=1;v+=mul()*(1 if op=='+' else -1)
        return v
    ans=add();assert i==len(text),('unconsumed',text,i);return ans

@lru_cache(None)
def eq(a,b):
    d=a-b
    if d==0:return True
    if not d.free_symbols:return s.simplify(d)==0
    if d.is_polynomial(x,u):return s.expand(d)==0
    # A finite value disproves equivalence, so do costly identity simplification
    # only for expressions that agree at every ordinary domain witness.
    for point in (s.Rational(1,5),s.Rational(2,5),s.Rational(4,5)):
        v=d.subs({x:point,u:point}).evalf(18)
        if v.is_finite and abs(complex(v))>1e-12:return False
    return s.trigsimp(s.simplify(d))==0 or s.trigsimp(s.simplify(d.rewrite(s.cos)))==0

def formulas(text):
    # Canonical displays and immutable legacy source delimiters/environments.
    text=re.sub(r'\\\\\[[^\]]*pt\]',lambda m:r'\\',text)
    text=re.sub(r'\\\[(.*?)\\\]',lambda m:'$$'+m[1]+'$$',text,flags=re.S)
    text=re.sub(r'(?<!\$)\\begin\{align\*?\}(.*?)\\end\{align\*?\}',lambda m:'$$'+r'\begin{aligned}'+m[1]+r'\end{aligned}'+'$$',text,flags=re.S)
    return re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)\$(?!\$)',text,re.S)
def spans(text):return [a or b for a,b in formulas(text)]
def derivative_targets(t):
    t=re.sub(r'\\(?:dfrac|frac)\{\\(?:text|textrm|mathrm)\s*\{?d\}?\s*([yfu])\}\{\\(?:text|textrm|mathrm)\s*\{?d\}?\s*([xu])\}',lambda m:'D'+m[1]+m[2],t)
    # Captured du/dx has \textrm{d}u, while df/du has \textrm d f.
    return t

def displayed(r):
    q=r['question'];md=r['generation'];m=md['template'];raw=md['evidence_only'];hard=m=='q-48644';prompt=q[':question/problem']
    source_formula=next(t for t in spans(prompt) if t.strip().startswith('y') and '=' in t)
    curve=expr(source_formula.split('=',1)[1]);deriv=s.diff(curve,x)
    assert set(r['knowledge_point'])=={'db_id','id','title'} and r['knowledge_point']['db_id']==g.KP_ID
    fields=q.get(':question/answer-fields',[]);answers={}
    for f in fields:
        vals=[expr(a[':answer/value']) for a in f[':answer-field/choices']]
        assert len(set(a[':answer/id'] for a in f[':answer-field/choices']))==len(vals)
        assert all(not eq(a,b) for i,a in enumerate(vals) for b in vals[i+1:]),(m,'complete bank ambiguity')
        if f[':answer-field/type'].endswith('/radio'):
            # Independently read every bank pattern from printed function
            # operands. Each expected pattern must map exactly once; not only
            # the correct derivative or an option count.
            a,fun=curve.as_coeff_Mul();inside=fun.args[0];z=inside.args[0];S=s.sin(z);C=s.cos(z)
            patterns={
                'authored-easy':(),
                'q-31356':tuple(a*v for v in (S*s.cot(C)**2,S*s.csc(C)**2,s.csc(z)*s.sin(C)**2,S*s.cos(s.csc(z))**2,s.csc(z)*s.cos(S)**2)),
                'q-48643':tuple(a*v for v in (-C*s.sin(C),-S*s.cos(C),-S*s.cos(S),-C*s.cos(S),-S*s.sin(C))),
                'q-72161':tuple(a*v for v in (-C*s.csc(C)**2,-C*s.csc(S)**2,-s.csc(S)**2,s.csc(C)**2,C*s.csc(C)**2)),
                'q-72173':(a*s.sec(z)*s.tan(-S),a*S*s.sec(-S)*s.tan(-S),a*C*s.sec(C)*s.tan(C),a*S*s.sec(z)*s.tan(C),-a*S*s.sec(C)*s.tan(C))}
            if m=='authored-easy':
                # Both operator identities and every argument are read from
                # the printed curve; generator operator metadata is unused.
                assert fun.func in (s.sin,s.cos) and inside.func in (s.sin,s.cos) and z==x
                outer_primitive=fun.func(u);od=s.diff(outer_primitive,u);id=s.diff(inside,x);correct=a*od.subs(u,inside)*id
                other=(s.cos if inside.func==s.sin else s.sin)(x)
                patterns[m]=(correct,a*od.subs(u,inside),-correct,a*outer_primitive.subs(u,inside)*id,a*od.subs(u,other)*id)
            assert len(vals)==len(patterns[m])==5
            assert all(sum(eq(v,w) for w in vals)==1 for v in patterns[m]),(m,'full rendered whole-bank pattern')

        if ':answer-field/correct' in f:
            aid=f[':answer-field/correct'][1];selected=next(a for a in f[':answer-field/choices'] if a[':answer/id']==aid);answers[f[':answer-field/key']]=expr(selected[':answer/value'])
        elif raw:
            assert m=='q-31356';assert sum(eq(v,deriv) for v in vals)==1
        else:raise AssertionError('Missing served correct designation')
        if f[':answer-field/type'].endswith('/blank'):assert prompt.count('{{'+f[':answer-field/key']+'}}')==1
    if hard:
        point_text=next(t for t in spans(prompt) if t.strip().startswith(r'\left('));point_parts=point_text.replace(r'\left','').replace(r'\right','').rstrip('.').strip()[1:-1].split(',');assert len(point_parts)==2
        point=expr(point_parts[0]);height=expr(point_parts[1]);assert eq(curve.subs(x,point),height)
        slope=s.simplify(deriv.subs(x,point));rhs=s.expand(slope*(x-point)+height)
        if answers:assert eq(answers['field-1'],rhs)
        assert md['tangent']['point_x']==point and eq(expr(md['tangent']['point_y']),height) and eq(expr(md['tangent']['slope']),slope)
    elif fields and (fields[0][':answer-field/type'].endswith('/radio') or m in ('q-72163','q-72170')):
        if answers:assert eq(next(iter(answers.values())),deriv)
        vals=[expr(a[':answer/value']) for a in fields[0][':answer-field/choices']];assert sum(eq(v,deriv) for v in vals)==1
    elif answers:
        # Insert answers into the actual supplied blank skeleton, then parse
        # the full printed derivative with nested arguments and chain factors.
        reconstructed=prompt
        for f in fields:
            a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);reconstructed=reconstructed.replace('{{'+f[':answer-field/key']+'}}',a[':answer/value'])
        after=reconstructed.split('we have',1)[1];printed=after.replace('$','').strip();printed=derivative_targets(printed);assert printed.startswith('Dyx=')
        assert eq(expr(printed.split('=',1)[1]),deriv),(m,'actual blank recomposition',printed)
    if ':question/worked-solution' in q:
        sol=q[':question/worked-solution'];parts=spans(sol)
        definitions=next(t for t in parts if ('y=' in t or 'y =' in t or 'f =' in t) and 'u' in t and 'u' in t.split('=',1)[1])
        defs=re.split(r',\s*\\(?:qquad|,)',definitions);assert len(defs)==2,(m,'outer/inner binding',definitions)
        expected_target='f' if hard else 'y';assert defs[0].split('=')[0].strip()==expected_target;assert defs[1].split('=')[0].strip()=='u'
        outer=expr(defs[0].split('=',1)[1]);inner=expr(defs[1].split('=',1)[1]);assert eq(outer.subs(u,inner),curve)
        formal=next(t for t in parts if derivative_targets(t).strip().startswith('D'+expected_target+'u=' ) or derivative_targets(t).strip().startswith('D'+expected_target+'u ='))
        formal=derivative_targets(formal);lhsrhs=re.split(r',\s*\\(?:qquad|,)',formal);assert len(lhsrhs)==2
        assert lhsrhs[0].split('=')[0].strip()=='D'+expected_target+'u' and lhsrhs[1].split('=')[0].strip()=='Dux'
        od=expr(lhsrhs[0].split('=',1)[1]);id=expr(lhsrhs[1].split('=',1)[1]);assert eq(od,s.diff(outer,u)) and eq(id,s.diff(inner,x)),(m,'every formal derivative target/operand')
        blocks=re.findall(r'\\begin\{(?:aligned|align\*?)\}(.*?)\\end\{(?:aligned|align\*?)\}',sol,re.S);chain=blocks[0]
        rows=re.sub(r'\\\\\[[^\]]*pt\]',lambda m:r'\\',chain).split(r'\\');assert len(rows)==3
        first=derivative_targets(rows[0]);assert re.sub(r'\s|&','',first)=='D'+expected_target+'x=D'+expected_target+'u'+r'\cdotDux'
        middle=rows[1].split('=',1)[1];assert r'\cdot' in middle;factors=middle.split(r'\cdot');assert len(factors)==2
        # Parse actual precedence before treating text as named factors. A
        # split at cdot must never implicitly group a preceding sum.
        printed_product=expr(middle)
        assert eq(printed_product,od*id),(m,'actual chain-product precedence',middle)
        assert eq(printed_product.subs(u,inner),deriv),(m,'actual evaluated-factor stage after substitution',middle)
        assert eq(expr(factors[0]),od) and eq(expr(factors[1]),id)
        assert eq(expr(rows[2].split('=',1)[1]),deriv),(m,'full substituted final derivative')
        if hard:
            assert len(blocks)==(2 if raw else 3)
            evaluation=next(t for t in parts if "f'(" in t and '&=' in t)
            assert re.search(r"f'\("+re.escape(str(point))+r'\)\s*&=',evaluation)
            rows=re.sub(r'\\\\\[[^\]]*pt\]',lambda m:r'\\',evaluation).split(r'\\');assert len(rows)==3
            # Raw eqalign contributes one outer wrapper, removed exactly.
            for index,row in enumerate(rows):
                val=row.split('=',1)[1].strip()
                if index==2:val=val.split(r'\end')[0].rstrip('} \n\t')
                assert eq(expr(val),slope),(m,'tangent evaluation row',row)
            tangent_rows=re.sub(r'\\\\\[[^\]]*pt\]',lambda m:r'\\',blocks[-1]).split(r'\\');assert len(tangent_rows)==3
            assert re.sub(r'\s|&','',tangent_rows[0])=='y-y_1=m(x-x_1)'
            # Actual second point-slope equation: parse y's subtracted height,
            # and require equality with slope*(x-point), including signed point.
            left,right=tangent_rows[1].replace('&','').split('=');assert left.strip().startswith('y-')
            assert eq(expr(left.strip()[2:]),height) and eq(expr(right),slope*(x-point))
            assert tangent_rows[2].replace('&','').split('=')[0].strip()=='y';assert eq(expr(tangent_rows[2].split('=',1)[1]),rhs)
            assert f'$x = {point}$' in sol and f'$x={point},$' in sol
        assert sol.count('Differentiating gives')==1 and sol.count('We now apply the chain rule, and get')==1
        if not hard:assert sol.startswith('First, we express $y$ as the composite function')
    # Domains are independently inferred from actual nested printed curve.
    restrictions=[]
    for fun in s.preorder_traversal(curve):
        if isinstance(fun,s.Function):
            if fun.func in (s.tan,s.sec):restrictions.append(s.cos(fun.args[0],evaluate=False))
            if fun.func in (s.cot,s.csc):restrictions.append(s.sin(fun.args[0],evaluate=False))
    domain=md['domain']['restriction']
    if not restrictions:assert domain=='all real x'
    else:
        ds=domain.split('; ');assert len(ds)==len(restrictions)
        vals=[expr(t.removesuffix(' != 0').replace('cos(',r'\cos(').replace('sin(',r'\sin(')) for t in ds]
        assert all(any(eq(v,w) for w in vals) for v in restrictions)
    if not raw:
        g.math_format.validate_generated_record(r)
        for t in [prompt,q[':question/worked-solution']]+[a[':answer/value'] for f in fields for a in f[':answer-field/choices']]:assert all(ord(c)>=32 or c in '\n\t' for c in t)
    return curve

def native_checks(r):
    checks=[]
    for i,f in enumerate(r['question'].get(':question/answer-fields',[])):
        if ':answer-field/correct' not in f:continue
        correct=f[':answer-field/correct'][1]
        if f[':answer-field/type'].endswith('/radio'):
            checks += [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'Every field-owned complete source-bank option'} for a in f[':answer-field/choices']]
        else:
            a=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct)
            # Equivalent factor structure differs from canonical text.
            checks += [{'field_index':i,'submitted':v,'expected':e,'purpose':'Canonical, unreduced equivalent, wrong expression'} for v,e in ((a,'accepted'),('2('+a+')/2','accepted'),('0','rejected'),('2('+a+')','rejected'),('('+a+')+1','rejected'))]
    return checks

def failure(fn):
    try:fn()
    except (AssertionError,ValueError,StopIteration):return
    raise AssertionError('Fail-closed negative control was accepted')

def main():
    originals,counts=F.check(g,str(g.KP_ID),HERE);assert len(originals)==11
    raw=[g.generate(g.LEVELS[m],template=m,parameters=g.DEFAULTS[m],profile='observed_raw') for m in g.SOURCES]
    for r in raw:displayed(r)
    normal=[];reviews=[];coverage={};fingerprints={l:set() for l in g.SUPPORTED_LEVELS}
    for m in g.LEVELS:
        if m in g.EVIDENCE_ONLY_TEMPLATES:
            coverage[m]={'status':'observed_raw only; explicit native ordinary wrong-probe exclusion','original_parameters':g.DEFAULTS[m]}
            failure(lambda:g.generate(g.LEVELS[m],template=m,parameters=g.DEFAULTS[m]))
            for p in (g.parameters_for(m)[0],g.parameters_for(m)[-1]):displayed(g.generate(g.LEVELS[m],template=m,parameters=p,profile='observed_raw'))
            continue
        print('Checking complete bounded domain',m,flush=True)
        ps=g.parameters_for(m);local=[]
        for i,p in enumerate(ps):
            r=g.generate(g.LEVELS[m],i,template=m,parameters=p);displayed(r);local.append(r);fingerprints[g.LEVELS[m]].add(r['generation']['mathematical_fingerprint'])
        normal+=local;reviews += [local[0],local[-1]]
        if m=='authored-easy':
            for outer in ('sin','cos'):
                for inner in ('sin','cos'):
                    same_amplitude=g.generate('easy',template=m,parameters={'a':4,'b':0,'outer':outer,'inner':inner});displayed(same_amplitude);reviews.append(same_amplitude)
        coverage[m]={'records':len(local),'slot_values':{k:sorted({p[k] for p in ps},key=str) for k in ps[0]},'source_anchor_in_domain':(g.DEFAULTS[m] in ps or dict(g.DEFAULTS[m],a=g.DEFAULTS[m].get('a',1)) in ps)}
        if m in g.SOURCES:
            for p in (ps[0],ps[-1]):displayed(g.generate(g.LEVELS[m],template=m,parameters=p,profile='observed_raw'))
    seeds={}
    for l in g.SUPPORTED_LEVELS:
        ds=[g.generate(l,i) for i in range(110)];[displayed(r) for r in ds];seeds[l]=sorted({r['generation']['template'] for r in ds});assert set(seeds[l])=={m for m in g.SERVED_TEMPLATES if g.LEVELS[m]==l}
    negatives=0
    for m in g.LEVELS:
        failure(lambda:g.generate(g.LEVELS[m],template=m,parameters={'b':99}));negatives+=1
        failure(lambda:g.generate(next(l for l in g.SUPPORTED_LEVELS if l!=g.LEVELS[m]),template=m));negatives+=1
        if m in g.EVIDENCE_ONLY_TEMPLATES:continue
        a=g.generate(g.LEVELS[m],0,template=m,parameters=g.DEFAULTS[m]);b=g.generate(g.LEVELS[m],65,template=m,parameters=g.DEFAULTS[m]);assert a['question'][':question/id']==b['question'][':question/id']
    failure(lambda:g.generate('moderate',template='q-48643',parameters={'b':True}));failure(lambda:g.generate('moderate',template='q-341223',parameters={'a':0,'b':0}));negatives+=2
    for m in g.SERVED_TEMPLATES:
        for nonzero in (-3,1,3):
            par=dict(g.parameters_for(m)[0],b=nonzero);failure(lambda:g.generate(g.LEVELS[m],template=m,parameters=par));negatives+=1
    easy=g.generate('easy',template='authored-easy',parameters={'a':4,'b':0,'outer':'sin','inner':'sin'})
    for target in ('outer','inner'):
        r=copy.deepcopy(easy);ptext=r['question'][':question/problem']
        old='y=4 '+r'\sin' if target=='outer' else r'\sin{\left(x \right)}'
        new='y=4 '+r'\cos' if target=='outer' else r'\cos{\left(x \right)}'
        r['question'][':question/problem']=ptext.replace(old,new,1);assert r!=easy
        failure(lambda:displayed(r));negatives+=1
    base=g.generate('moderate',template='q-341223',parameters={'a':7,'b':0})
    for slot in ('prompt','inner-binding','outer-binding','formal-outer','formal-inner','formal-target','chain-factor','substitution','key','placeholder','domain','control'):
        r=copy.deepcopy(base);q=r['question'];sol=q[':question/worked-solution']
        if slot=='prompt':q[':question/problem']=q[':question/problem'].replace('y=7','y=6',1)
        elif slot=='inner-binding':q[':question/worked-solution']=sol.replace(r'u=\operatorname{sin}⁡(x)',r'u=\operatorname{cos}⁡(x)',1)
        elif slot=='outer-binding':q[':question/worked-solution']=sol.replace('y=7','y=6',1)
        elif slot=='formal-outer':q[':question/worked-solution']=sol.replace('=-7','=-6',1)
        elif slot=='formal-inner':q[':question/worked-solution']=sol.replace(r'\frac{\text{d}u}{\text{d}x}=\operatorname{cos}',r'\frac{\text{d}u}{\text{d}x}=\operatorname{sin}',1)
        elif slot=='formal-target':q[':question/worked-solution']=sol.replace(r'\frac{\text{d}y}{\text{d}u}=',r'\frac{\text{d}y}{\text{d}x}=',1)
        elif slot=='chain-factor':q[':question/worked-solution']=sol.replace(r'\cdot \operatorname{cos}',r'\cdot \operatorname{sin}',1)
        elif slot=='substitution':q[':question/worked-solution']=sol.replace(r'\operatorname{sin}⁡(x)).',r'\operatorname{cos}⁡(x)).',1)
        elif slot=='key':q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='1'
        elif slot=='placeholder':q[':question/problem']=q[':question/problem'].replace('{{field-2}}','{{field-4}}')
        elif slot=='domain':r['generation']['domain']['restriction']='sin(x) != 0'
        elif slot=='control':q[':question/worked-solution']+='\x0c'
        assert r!=base,(slot,'mutation did not touch actual content');failure(lambda:displayed(r));negatives+=1
    # Regression: formerly the printed outer SUM was not grouped and only
    # individually split factors were checked. Recreate that precise error,
    # keeping the correct final derivative and answer bank unchanged.
    precedence_base=g.generate('moderate',template='q-31356',parameters={'a':1,'b':0})
    ps=precedence_base['question'][':question/worked-solution']
    block=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',ps,re.S)[0]
    row=block.split(r'\\')[1];middle=row.split('=',1)[1]
    factor=middle.split(r'\cdot')[0];assert factor.startswith('(') and factor.endswith(')')
    regressions={
        'ungrouped-outer-sum':ps.replace(middle,factor[1:-1]+r'\cdot'+middle.split(r'\cdot',1)[1],1),
        'formal-outer-summand':ps.replace(r'=- \cot^{2}{\left(u \right)} - 1',r'=- \cot^{2}{\left(u \right)} + 1',1),
        'formal-inner-argument':ps.replace(r'\frac{\text{d}u}{\text{d}x}=- \sin{\left(x \right)}',r'\frac{\text{d}u}{\text{d}x}=- \sin{\left(x + 1 \right)}',1),
        'chain-inner-argument':ps.replace(r'\cdot (- \sin{\left(x \right)})',r'\cdot (- \sin{\left(x + 1 \right)})',1)}
    for name,mutated in regressions.items():
        r=copy.deepcopy(precedence_base);assert mutated!=ps,(name,'operand mutation did not change actual display')
        r['question'][':question/worked-solution']=mutated
        assert r['question'][':question/answer-fields']==precedence_base['question'][':question/answer-fields']
        failure(lambda:displayed(r));negatives+=1
    save('chain-precedence-regression.json',{'correct_record':precedence_base,'negative_solution_mutations':regressions,'assertion':'The complete actual printed multiplication stage must equal the derivative under TeX precedence; the answer key alone cannot establish solution correctness.'})
    hard=g.generate('hard',template='q-48644',parameters={'a':4,'b':0,'phase':'1/6'})
    for name in ('point','evaluation','tangent-slope','final-line'):
        r=copy.deepcopy(hard);q=r['question']
        if name=='point':q[':question/problem']=q[':question/problem'].replace(r'\left(0,',r'\left(1,',1)
        elif name=='evaluation':q[':question/worked-solution']=q[':question/worked-solution'].replace("f'(0)&=","f'(1)&=",1)
        elif name=='tangent-slope':q[':question/worked-solution']=q[':question/worked-solution'].replace('(-2)\\cdot','(-1)\\cdot',1)
        elif name=='final-line':q[':question/worked-solution']=q[':question/worked-solution'].replace('y&=- 2 x','y&=- 3 x',1)
        assert r!=hard,(name,'mutation did not touch actual content');failure(lambda:displayed(r));negatives+=1
    save('review.json',{'source_anchors':raw,'boundary_and_changed_inputs':reviews})
    (HERE/'review.md').write_text('\n\n'.join(['# Trig composition source and changed-input review']+['## '+('Original MA evidence' if r['generation']['evidence_only'] else 'Eligible '+r['generation']['level'])+' / '+r['generation']['template']+' / '+str(r['generation']['parameters'])+'\n\n'+g.markdown(r) for r in raw+reviews])+'\n')
    cli=subprocess.run([str(ROOT/'.venv/bin/python'),str(HERE.with_suffix('.py')),'--difficulty','all','--count','1','--seed','7','--format','json'],capture_output=True,text=True,check=True);assert len(json.loads(cli.stdout))==3
    engine=[{'label':str(i),'record':r,'checks':native_checks(r)} for i,r in enumerate(normal)];save('engine-input.json',engine);binary=ROOT/'generate/runs/current/check-engine';assert hashlib.sha256(binary.read_bytes()).hexdigest()=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
    run=subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True);(HERE/'engine.log').write_text(run.stdout+run.stderr);assert run.returncode==0,run.stderr
    native=json.loads((HERE/'engine-report.json').read_text());assert native['documented_unresolved_checks']==0
    # Foreign IDs are invalid field ownership, an expected API error, and are
    # exercised separately from zero-gap learner mathematical grading probes.
    ownership=[]
    for m in ('authored-easy','q-31356','q-48643','q-72161','q-72173'):
        r=g.generate(g.LEVELS[m],template=m,parameters=g.DEFAULTS[m]);ownership.append({'label':m,'record':r,'checks':[{'field_index':0,'submitted':'999999','expected':'unresolved','purpose':'Expected rejection of an out-of-field answer ID at the API ownership guard'}]})
    save('native-ownership-input.json',ownership)
    own=subprocess.run([str(binary),str(HERE/'native-ownership-input.json'),str(HERE/'native-ownership-report.json')],capture_output=True,text=True);assert own.returncode==0,own.stderr
    own_report=json.loads((HERE/'native-ownership-report.json').read_text());assert all(c['reason']=='selected answer does not belong to this field' for r in own_report['records'] for c in r['checks'])
    baseline=json.loads((HERE/'registered-baseline.json').read_text());files=[ROOT/'generate/scratch/17592186064284.py']+sorted(p for p in (ROOT/'generate/scratch/17592186064284').rglob('*') if p.is_file());assert {str(p) for p in files}==set(baseline);assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in baseline.items())
    inv=json.loads((HERE/'independent-inventory.json').read_text());assert [e['record'] for e in inv['questions']]==[q for q in g.SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q]
    report={'status':'pass','private_draft_only':True,'source_basis':2275,'source_fidelity':counts,'MA_source_originals':11,'complete_radio_banks':4,'source_bank_options_matched':20,'source_bank_options_total':20,'exact_independent_inventory':5,'all_bounded_normal_records':len(normal),'explicit_nonserved_templates':sorted(g.EVIDENCE_ONLY_TEMPLATES),'semantic_tasks':{l:len(v) for l,v in fingerprints.items()},'slot_coverage':coverage,'default_sampling_template_coverage':seeds,'fail_closed_negative_controls':negatives,'native_grading':{k:native[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'registered_script_and_full_evidence_pathset_unchanged':True,'baseline_files':len(baseline),'expected_foreign_ID_ownership_errors':5,'supplemental_limitations':['No original easy MA practice exists: four ordinary sin/cos composition full-derivative radios and its complete five-pattern bank are explicitly authored.','The unlabeled q-31356 gains an authored moderate key and solution only in learning output.','The hard tangent original lacks fields: normal RHS blank is an explicit authored repair. q-72163/q-72170/q-342436 are explicitly evidence-only and rejected from normal serving due ordinary native wrong-probe failures.','Hard special-angle phase and outer coefficients are authored same-stage extensions with supplied x=0 fixed, not observed MA slots.','No plots occur. Exact immutable raw legacy TeX is evidence-only; served aligned displays are normalized.','Ordinary wrong probes unsupported by the frozen grader are fully recorded and their source families are explicitly nonserved; native-nonserved-exclusions.json retains exact fixture records. Foreign radio IDs intentionally fail the ownership guard in a separate API-negative report.'],'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),Path(__file__),HERE/'source.json',binary]}}
    save('validation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
