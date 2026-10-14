from pathlib import Path
P=Path(__file__).resolve().parent.with_suffix('.py');text=P.read_text()
text=text.replace('import argparse,hashlib,json,random,re,uuid','import argparse,hashlib,json,random,re,uuid,sys,copy\nsys.dont_write_bytecode=True\nFORMAT_SPEC=__import__("importlib.util",fromlist=["util"]).spec_from_file_location("math_format",Path(__file__).resolve().parents[2]/"scripts/question_capture/math_format.py")' ) if False else text
text=text.replace('import argparse,hashlib,json,random,re,uuid','import argparse,hashlib,json,random,re,uuid,sys,copy,importlib.util\nsys.dont_write_bytecode=True')
text=text.replace("VERSION='particular-direct-1'", "VERSION='particular-direct-draft-2275-2'")
text=text.replace("QUESTIONS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}","QUESTIONS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions'] if ':question/math-academy-id' in q}\nINDEPENDENT=[q for q in KP[':knowledge-point/questions'] if ':question/math-academy-id' not in q]\n_fs=importlib.util.spec_from_file_location('math_format',Path(__file__).resolve().parents[2]/'scripts/question_capture/math_format.py');fmt=importlib.util.module_from_spec(_fs);_fs.loader.exec_module(fmt)")
a=text.index('def source_render(');b=text.index('def completed_solution(',a)
text=text[:a]+r'''
Q=s.Symbol('Q',real=True)
def kind_of(template):return QUESTIONS[template][':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1]
def level_of(template):return QUESTIONS[template].get(':question/difficulty',{}).get(':db/ident',':question.difficulty/easy').split('/')[-1]
def derivative_tex(template):
    prompt=QUESTIONS[template][':question/problem']
    if r'\frac{\text{d}y}{\text{d}x}' in prompt:return r'\frac{\text{d}y}{\text{d}x}'
    return r'{f}^{′}(x)' if ('f(' in prompt or '{f}' in prompt) else r'{y}^{′}'
def derivative_replace(math,template):
    math=math.replace(r'\frac{\text{d}y}{\text{d}x}','Q')
    math=re.sub(r'\{?[fgy]\}?\^\{′\}(?:\(x\))?','Q',math)
    math=re.sub(r"[fgy]'(?:\(x\))?",'Q',math)
    return math

def scalar_mask(math,r):
    """One unevaluated complete-component multiplier, with grouped signs.
    Unit multipliers suppress themselves as a general notation rule. The
    underlying integral/primitive/substitution structure is never simplified.
    """
    return math if r==1 else '('+tex(r)+r')\cdot('+math+')'
def c_rhs(rhs,r):
    match=re.search(r'\+\s*C',rhs)
    if match:return scalar_mask(rhs[:match.start()],r)+'+C'+rhs[match.end():]
    punctuation='.' if rhs.endswith('.') else ''
    return scalar_mask(rhs[:-1] if punctuation else rhs,r)+punctuation

def source_render(template,r,v,raw=True):
    q=QUESTIONS[template];der,P,t,b,fragment,bank=DEFS[template];P=s.sympify(P);r=s.Rational(r);v=s.Rational(v);K=s.simplify(v-r*P.subs(X,t))
    name='f(x)' if ('f(' in q[':question/problem'] or '{f}' in q[':question/problem']) else 'y'
    source_prompt=q[':question/problem'];cond=re.search(r'(?:f|y)\([^)]*\)\s*=\s*-?\d+',source_prompt).group()
    newcond=re.sub(r'-?\d+$',lambda m:tex(v),cond)
    prompt=source_prompt.replace(cond,newcond)
    def prompt_math(match):
        whole=match.group();width=2 if whole.startswith('$$') else 1;math=whole[width:-width].strip()
        if ('′' in math or r'\text{d}y' in math or "'" in math):
            original=math;left,right=derivative_replace(math,template).rstrip('.').split('=')
            def side(z):
                z=parse(z);return z.coeff(Q)*Q+r*z.subs(Q,0)
            replacement=tex(s.expand(side(left)))+'='+tex(s.expand(side(right)))
            replacement=replacement.replace('Q',derivative_tex(template))
            if r==1:replacement=original
            elif original.endswith('.'):replacement+='.'
            return ('$$\n'+replacement+'\n$$') if width==2 else '$'+replacement+'$'
        if '{{field-1}}' in prompt and math.startswith('y=') and fragment!=0:
            supplied=math.split('=',1)[1].rstrip('+').strip();return '$y='+scalar_mask(supplied,r)+'+$'
        return whole
    prompt=fmt.MATH.sub(prompt_math,prompt)
    sol=q.get(':question/worked-solution')
    if sol is not None:
        sol=sol.replace(cond,newcond)
        def solution_math(match):
            whole=match.group();width=2 if whole.startswith('$$') else 1;math=whole[width:-width].strip()
            if r'\begin{aligned}' in math:
                head=r'\begin{aligned}';tail=r'\end{aligned}';body=math[len(head):-len(tail)];rows=re.split(r'\\',body);new=[]
                for row in rows:
                    lhs,rhs=row.split('&',1);right=rhs.lstrip();equal_space=right[:right.index('=')+1];value=right[right.index('=')+1:]
                    numeric=lhs.strip()
                    if numeric=='C':value=tex(K)+('.' if value.rstrip().endswith('.') else '')
                    elif numeric==str(b):
                        lhs=lhs.replace(str(b),tex(v));value=c_rhs(value,r)
                    elif numeric=='0' and template=='q-8311' and 'C' in value:lhs=lhs.replace('0',tex(K))
                    else:value=c_rhs(value,r)
                    new.append(lhs+'&'+equal_space+value)
                replacement=head+r'\\'.join(new)+tail
            elif math.startswith(('f(x)=','y=')) and '+C' in math:
                left,right=math.split('=',1);replacement=left+'='+c_rhs(right,r)
            elif '′' in math or r'\text{d}y' in math:
                left,right=math.split('=',1);replacement=left+'='+c_rhs(right,r)
            elif math.startswith(('f(x)=','y=')) and width==2:
                left,_=math.split('=',1)
                # A complete explicit-function slot; recover source notation at
                # the identity scale by generic component rendering only.
                replacement=left+'='+tex(r*P+K)+'.'
                if r==1 and v==b:replacement=math
            else:return whole
            return ('$$\n'+replacement+'\n$$') if width==2 else '$'+replacement+'$'
        sol=fmt.MATH.sub(solution_math,sol)
    values=[(name+'=' if kind_of(template)=='radio' else '')+tex(r*s.sympify(expr)) for expr in bank]
    return prompt,sol,values,r*P+K,r*s.sympify(fragment),name

''' +text[b:]
# source prompt math matching framework above uses raw literal double escapes:
# its Python runtime math strings already correspond to source TeX.
text=text.replace("assessment_presence={'difficulty'", "prompt=fmt.normalize_prose(prompt)\n    solution=fmt.normalize_prose(solution) if solution is not None else None\n    values=[fmt.normalize_tex(v) for v in values]\n    assessment_presence={'difficulty'")
text=text.replace("meta['sympy_version']=s.__version__", "meta['sympy_version']=s.__version__\n    meta['python_version']=sys.version.split()[0]\n    meta['math_format']=fmt.FORMAT_VERSION")
# public source branch now permits scale only; no additive source-bank offsets.
text=text.replace("params=parameters or {'target':DEFS[template][3]};assert set(params)=={'target'}\n        B=s.Rational(params['target']);assert B.q==1 and abs(B)<=20\n        prompt,sol,values,F,fragment,name=source_render(template,B)", "params=parameters or {'scale':1};assert set(params)=={'scale'}\n        scale=s.Rational(params['scale']);assert scale.q==1 and scale in (-2,-1,1,2,3,4)\n        B=scale*DEFS[template][3]\n        prompt,sol,values,F,fragment,name=source_render(template,scale,B)")
text=text.replace("sol=completed_solution(der,P,t,B,name)", "sol=completed_solution(scale*s.sympify(der),scale*s.sympify(P),t,B,name)")
text=text.replace("'parameters':{'target':str(B)}", "'parameters':{'scale':str(scale)}")
text=text.replace("'authorship':'observed bank; interpretation opaque; replay-only'", "'authorship':'observed complete-bank dependent-variable scaling; opaque error intent; replay-only'")
text=text.replace("s.srepr(s.sympify(DEFS[template][0])),str(DEFS[template][2]),str(B)", "s.srepr(scale*s.sympify(DEFS[template][0])),str(DEFS[template][2]),str(B)")
# Template requests to source IDs with the authored operation profile dispatch to
# family-shaped normal masks, while explicit observed profiles remain replay.
text=text.replace("if template in QUESTIONS:", "if template in QUESTIONS and profile in ('observed_raw','observed_repaired'):")
# Replace normal generation branch, retaining existing hard authored implementation.
a=text.index("    assert profile in (None,'authored_operations');profile='authored_operations'");b=text.index('\ndef generate_easy',a)
text=text[:a]+'''
    assert profile in (None,'authored_operations');profile='authored_operations'
    if level!='hard':
        eligible=[t for t in QUESTIONS if level_of(t)==level]
        template=template or rng.choice(eligible);assert template in eligible
        kind=kind_of(template);assert field_type in (None,kind)
        for attempt in range(1000):
            p=parameters if parameters is not None else {'scale':rng.choice([-2,-1,1,2,3,4]),'target':rng.choice([n for n in range(-12,13) if n])}
            try:return normal_source(level,seed,template,p)
            except AssertionError:
                if parameters is not None:raise
        raise ValueError('No eligible whole method-derived bank')
    template=template or 'three';assert template=='three'
    kind=field_type or rng.choice(['blank','radio']);assert kind in ('blank','radio')
    for attempt in range(1000):
        if parameters is None:
            p={'a':rng.choice([-6,-4,-2,2,4,6]),'b':rng.choice([-3,-2,-1,1,2,3]),'d':rng.choice([-4,-3,-2,2,3,4]),'k':rng.choice([-2,-1,1,2]),'t':0,'v':rng.randint(-8,8),'name':rng.choice(['y','f','g']),'family':'three'}
        else:p=dict(parameters);assert set(p)=={'a','b','d','k','t','v','name','family'}
        try:return authored(level,seed,template,kind,p,profile)
        except AssertionError:
            if parameters is not None:raise
    raise ValueError('no eligible whole-bank instance')
''' +text[b:]
# Add source-family normal authoring before generate.
a=text.index('def generate(level,')
text=text[:a]+r'''
def normal_source(level,seed,template,p):
    assert set(p)=={'scale','target'}
    r=s.Rational(p['scale']);v=s.Rational(p['target']);assert r.q==1 and r in (-2,-1,1,2,3,4) and v.q==1 and 0<abs(v)<=12
    der,P,t,b,fragment,bank=DEFS[template];der=r*s.sympify(der);P=r*s.sympify(P);K=s.simplify(v-P.subs(X,t));F=P+K
    prompt,solution,_,_,supplied,name=source_render(template,r,v,False)
    if template=='q-119045':solution=solution.replace('general solution is $y=', 'general solution is $f(x)=')
    if template=='q-50044':
        solution=solution.replace(r'6(\frac{{x}^{3}}{3})\,\text{d}x',r'6(\frac{{x}^{3}}{3})+C').replace('f(x)=','y=')
        # The raw source's dx is not part of an evaluated primitive. Its repair
        # applies inside the scaled complete-component mask as well.
        solution=solution.replace(r')+C)','.placeholder)') if False else solution
    if solution is None:solution=completed_solution(der,P,t,v,name)
    if template in ('q-119078','q-352066'):
        wrong=P+v+P.subs(X,t);recipe='add primitive value when solving C instead of subtracting'
    elif template=='q-49942':
        wrong=P+v+P.subs(X,t);recipe='add primitive value when solving C instead of subtracting'
    elif template in ('q-119045','q-352075'):
        primitive_basis=P/r;original_amplitude=primitive_basis.as_coeff_Mul()[0];basis=primitive_basis/original_amplitude
        wrong_primitive=basis/(r*original_amplitude);wrong=wrong_primitive+v-wrong_primitive.subs(X,t);recipe='reciprocate displayed integral coefficient'
    elif template in ('q-119075','q-119083'):
        k=-2 if template=='q-119075' else s.Rational(1,2)
        exponential=next(z for z in s.Add.make_args(der) if z.has(s.exp));poly=der-exponential
        wrong_primitive=s.integrate(poly,X)+exponential*k;wrong=wrong_primitive+v-wrong_primitive.subs(X,t);recipe='differentiate exponential scale instead of integrating it'
    elif template=='q-352068':
        wrong_primitive=P/2;wrong=wrong_primitive+v-wrong_primitive.subs(X,t);recipe='omit division by new exponent 1/2'
    elif template=='q-50159':
        wrong_primitive=2*P;wrong=wrong_primitive+v-wrong_primitive.subs(X,t);recipe='omit inner-linear divisor 2'
    elif template=='q-8311':
        wrong_primitive=der*X**2/2;wrong=wrong_primitive+v-wrong_primitive.subs(X,t);recipe='treat constant derivative as a linear power term'
    else:
        wrong_primitive=sum(z*X for z in s.Add.make_args(der));wrong=wrong_primitive+v-wrong_primitive.subs(X,t);recipe='raise each power but omit each new-degree divisor'
    candidates=[F,P-P.subs(X,t),-P+v+P.subs(X,t),der+v-der.subs(X,t),wrong]
    kind=kind_of(template)
    if kind=='radio':
        for i,a in enumerate(candidates):
            for z in candidates[i+1:]:assert s.simplify(a-z)!=0,'whole bank collision'
        values=[name+'='+tex(z) for z in candidates]
    else:values=[tex(F-supplied)]
    domain={'q-119078':'x>1','q-352066':'x>3','q-352068':'x>-1','q-50159':'x>-1/2','q-50044':'x<0'}.get(template,'real x')
    return record(level,prompt,solution,values,0,kind,QUESTIONS[template][':question/answer-fields'][0][':answer-field/key'],{'version':VERSION,'seed':seed,'template':template,'profile':'authored_operations','parameters':dict(p),'authorship':'authored complete method-derived bank with observed family solution masks','math_fingerprint':fingerprint([s.srepr(der),str(t),str(v)]),'domain':domain,'recipes':['correct','discard supplied initial value','reverse primitive sign then impose condition','use derivative as primitive then impose condition',recipe] if kind=='radio' else [],'source_id':template})

''' +text[a:]
# Public wrapper validates raw absent solution on a temporary record only.
a=text.index('\ndef generate_easy')
text=text[:a]+'''
_unchecked_generate=generate
def generate(*args,**kwargs):
    result=_unchecked_generate(*args,**kwargs)
    checked=copy.deepcopy(result)
    checked['question'].setdefault(':question/worked-solution','')
    fmt.validate_generated_record(checked)
    for text in [result['question'][':question/problem'],result['question'].get(':question/worked-solution','')]+[a[':answer/value'] for f in result['question'].get(':question/answer-fields',[]) for a in f.get(':answer-field/choices',[])]:
        assert not any(ord(c)<32 and c not in '\\n\\t' for c in text),'unexpected control character'
    return result
''' +text[a:]
P.write_text(text)
