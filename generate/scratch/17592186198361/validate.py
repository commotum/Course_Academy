#!/usr/bin/env python3
"""Independent readback QA plus native radio checks; writes local evidence only."""
import copy, importlib.util, itertools,json,re,subprocess,sys,hashlib
from pathlib import Path
sys.dont_write_bytecode=True
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
D=Path(__file__).parent
spec=importlib.util.spec_from_file_location('change_variables',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,u,v=g.x,g.y,g.u,g.v

def balanced(text):
    assert not any(ord(c)<32 and c not in '\n\t' for c in text),'C0 control character'
    assert text.count('$')%2==0,'unbalanced dollar math'
    depth=0
    for i,c in enumerate(text):
        if c in '{}':
            n=0;j=i-1
            while j>=0 and text[j]=='\\':n+=1;j-=1
            if n%2:continue
            depth+=(1 if c=='{' else -1)
            assert depth>=0,'closing group without opening'
    assert depth==0,'unbalanced groups'
    assert '@@' not in text

def math(t):
    """Independent exact parser of actual emitted subset; never generation metadata."""
    t=t.replace('\u2061','').replace('⁡','').replace('\xa0',' ')
    t=t.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\:','').replace(r'\cdot','*')
    t=t.replace(r'\operatorname{ln}',r'\ln').replace(r'\displaystyle','')
    def group(text,start):
        assert text[start]=='{';depth=1;i=start+1
        while depth:
            assert i<len(text),'unterminated fraction'
            depth+= (1 if text[i]=='{' else -1 if text[i]=='}' else 0);i+=1
        return text[start+1:i-1],i
    def expand(text):
        out='';i=0
        while i<len(text):
            m=re.match(r'\\(?:d?frac)',text[i:])
            if m:
                j=i+len(m[0])
                if text[j]=='{':a,j=group(text,j)
                else:a=text[j];j+=1
                if text[j]=='{':b,j=group(text,j)
                else:b=text[j];j+=1
                out+='(('+expand(a)+')/('+expand(b)+'))';i=j
            else:out+=text[i];i+=1
        return out
    t=expand(t)
    # Abs arguments have no nested bars in this generator.
    t=re.sub(r'\|([^|]+)\|',r'Abs(\1)',t)
    t=t.replace('{','(').replace('}',')').replace('[','(').replace(']',')').replace('^','**')
    # Logs have either an explicit grouped argument, |u|, or a single integer.
    t=t.replace(r'\ln','log')
    t=re.sub(r'log\s*Abs\(([^()]*)\)',r'log(Abs(\1))',t)
    t=re.sub(r'log\s*([0-9]+)',r'log(\1)',t)
    t=t.replace('e**','E**').replace('e','E') if '\\' not in t and 'log' not in t else t.replace('e**','E**')
    assert '\\' not in t,(t,'unsupported TeX remaining')
    t=re.sub(r'([a-zA-Z0-9)])(Abs|log)\(',r'\1*\2(',t)
    t=t.strip().rstrip('.,')
    return parse_expr(t,local_dict={'x':x,'y':y,'u':u,'v':v,'E':s.E,'Abs':s.Abs,'log':s.log},transformations=standard_transformations+(implicit_multiplication_application,))

def eq(a,b):
    z=s.simplify(a-b)
    assert z==0 or z.equals(0),(a,b,z)

def integral_value(text):
    # Full integral parser accepts both captured spacing/styles and authored exact expressions.
    t=text.replace(r'\displaystyle','').replace(r'{\int }',r'\int').replace(r'{\int}',r'\int')
    pat=r'\\int_\{(-?\d+)\}\^\{(-?\d+)\}'
    matches=list(re.finditer(pat,t));assert len(matches)==2,('two integral limits',text)
    coef=math(t[:matches[0].start()].strip() or '1')
    tail=t[matches[1].end():]
    differentials=re.findall(r'd([uv])',tail);assert len(differentials)==2
    expr=re.split(r'(?:\\,)?d[uv]',tail,maxsplit=1)[0]
    z=coef*math(expr);inner,outer=[{'u':u,'v':v}[ch] for ch in differentials]
    lo,hi=map(int,matches[1].groups());outlo,outhi=map(int,matches[0].groups())
    return s.integrate(s.integrate(z,(inner,lo,hi)),(outer,outlo,outhi)),z,{str(inner):(lo,hi),str(outer):(outlo,outhi)}

def read_prompt(record):
    q=record['question'];prompt=q[':question/problem'];name=record['generation']['template']
    # Read the learner's supplied coordinate definitions before any normalization.
    um=re.search(r'\bu\s*=\s*(.*?)\$',prompt,re.S);vm=re.search(r'\bv\s*=\s*(.*?)\$',prompt,re.S)
    assert um and vm
    ut=um[1].rstrip(',');vt=vm[1].rstrip(',')
    U,V=math(ut),math(vt)
    jac=s.det(s.Matrix([[s.diff(U,x),s.diff(U,y)],[s.diff(V,x),s.diff(V,y)]]))
    im=re.search(r'(?:\{∬\}_\{D\}|∬_\(D\))(.*?)dx',prompt,re.S)
    assert im
    f=math(im[1].replace(r'\,',''))
    if name.startswith('ratio_product'):
        lower=re.search(r'(\d*)\{x\}\^\{2\}\\le y\\le (\d+)\{x\}\^\{2\}',prompt)
        vp=re.search(r'(\d+)\\le xy\\le (\d+)',prompt)
        assert lower and vp
        p={'ul':int(lower[1] or 1),'uh':int(lower[2]),'vl':int(vp[1]),'vh':int(vp[2])}
        eq(U,y/x**2);eq(V,x*y)
        inverse={x:(v/u)**s.Rational(1,3),y:u**s.Rational(1,3)*v**s.Rational(2,3)}
        z=s.simplify(f.subs(inverse,simultaneous=True)*s.Abs(1/jac).subs(inverse,simultaneous=True))
    else:
        constraints=re.findall(r'(-?\d+)\s*\\le\s*(.*?)\s*\\le\s*(-?\d+)',prompt,re.S)
        assert len(constraints)==2
        (a,first,b),(c,second,d)=constraints
        eq(math(first),U);eq(math(second),V)
        p=dict(ul=int(a),uh=int(b),vl=int(c),vh=int(d))
        inverse=s.solve([U-u,V-v],[x,y]);z=s.simplify(f.subs(inverse,simultaneous=True)/s.Abs(jac))
    return p,U,V,f,jac,z

def check_solution(record,p,U,V,f,jac,z):
    name=record['generation']['template'];solution=record['question'][':question/worked-solution'];balanced(solution)
    blocks=re.findall(r'\$\$(.*?)\$\$',solution,re.S)
    assert solution.count('**Step')==4
    # Source family operative sequences: protect formal map/formula/determinant/inverse rows.
    if name=='difference':
        assert r'\begin{vmatrix}1&1\\-1&1\end{vmatrix}' in solution
        assert r'\left[\left(\frac{u+v}{2}\right)^2-\left(\frac{u-v}{2}\right)^2\right]' in solution
        eq(math(re.search(r'\$\$x=(.*?),\\qquad y=(.*?)\.\$\$',solution)[1]),(u-v)/2)
    else:
        base=g.TEMPLATES['ratio_product' if name.endswith('squared') else name][':question/worked-solution']
        baseblocks=re.findall(r'\$\$(.*?)\$\$',base,re.S)
        assert len(blocks)==len(baseblocks)
        for idx in (0,1,2,3,5,6):assert blocks[idx]==baseblocks[idx],('operative formal block changed',idx)
        # Derive determinant from PRINTED supplied definitions, and read last matrix row value.
        printedjac=blocks[5].rsplit(' & =',1)[1].split(r'.\end{aligned}')[0]
        eq(math(printedjac),jac)
        determinant_matrices=re.findall(r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|',blocks[5],re.S)
        assert len(determinant_matrices)==2
        entries=[]
        for matrix_row in determinant_matrices[-1].split(r'\\'):
            entries.extend(math(re.sub(r'\\text\{[^}]*\}','',entry)) for entry in matrix_row.split('&'))
        assert len(entries)==4
        for printed,actual in zip(entries,[s.diff(U,x),s.diff(U,y),s.diff(V,x),s.diff(V,y)]):eq(printed,actual)
        invjac=blocks[6].split('=')[-1].strip().rstrip('.')
        eq(math(invjac),1/jac if not name.startswith('ratio_product') else -1/(3*u))
        if name in ('triangular_quadratic','product','exponential'):
            bm=re.search(r'x=(.*?),\\,y=(.*?)\.',blocks[8],re.S);assert bm
            xx,yy=math(bm[1]),math(bm[2]);eq(U.subs({x:xx,y:yy},simultaneous=True),u);eq(V.subs({x:xx,y:yy},simultaneous=True),v)
    # Independent region readback from the solution, not metadata.
    for variable in ('u','v'):
        m=re.search(r'(-?\d+)\\le '+variable+r'\\le (-?\d+)',solution)
        assert m and tuple(map(int,m.groups()))==(p[variable+'l'],p[variable+'h'])
    chain=blocks[-1];rows=chain.split(r'\\')
    if name.startswith('ratio_product'):
        power=2 if name.endswith('squared') else 1;n=power+1
        assert len(rows)==10,('source operative row count',len(rows))
        # Verify substitution and signed/absolute Jacobian operative forms independently.
        assert ('{v}^{2}' if power==2 else 'v')+r'|\frac{∂(x,y)}{∂(u,v)}|' in rows[0]
        eq(z,v**power/(3*u))
        for row in rows[:2]:
            rhs=row.split(' & =')[-1].replace('{∬}_{Δ}','').replace(r'|\frac{∂(x,y)}{∂(u,v)}|',r'|\frac{1}{3u}|')
            rhs=re.split(r'\\text\{d\}u',rhs)[0]
            eq(math(rhs),z)
        val,integrand,bounds=integral_value(rows[2].split(' & =')[-1].replace(r'\text{d}','d'))
        eq(integrand,z);assert bounds=={'u':(p['ul'],p['uh']),'v':(p['vl'],p['vh'])}
        assert r'\frac{1}{u}' in rows[3] and '[{\\int }' in rows[3]
        def intparts(row):
            return list(re.finditer(r'\\int \}_\{(-?\d+)\}\^\{(-?\d+)\}',row))
        matches=intparts(rows[3]);assert len(matches)==2
        assert tuple(map(int,matches[0].groups()))==(p['vl'],p['vh'])
        assert tuple(map(int,matches[1].groups()))==(p['ul'],p['uh'])
        outerfactor=rows[3][matches[0].end():].split('[')[0];eq(math(outerfactor),v**power)
        eq(math(rows[3].split(' & =')[-1].split('{\\int }')[0]),s.Rational(1,3))
        # Primitive and each endpoint are read from the individual displayed rows.
        prim=re.search(r'\[(.*?)\\,\{\|\}',rows[4])[1];eq(s.diff(math(prim),u),1/u)
        logterms=re.search(r'(?:v|\{v\})(?:\^\{2\})?\((.*?)\)\\,dv',rows[5])[1]
        first,second=logterms.split('-');eq(math(first),s.log(p['uh']));eq(math(second),s.log(p['ul']))
        reduced=re.search(r'\\frac\{(.*?)\}\{3\}',rows[6])[1];eq(math(reduced),s.log(p['uh'])-s.log(p['ul']))
        for idx in (4,5,6):
            matches=intparts(rows[idx]);assert len(matches)==1
            assert tuple(map(int,matches[0].groups()))==(p['vl'],p['vh'])
            body=rows[idx][matches[0].end():]
            factor=body.split('[')[0] if idx==4 else body.split('(')[0] if idx==5 else body.split(r'\,dv')[0]
            eq(math(factor),v**power)
            coef=rows[idx].split(' & =')[-1].split('{\\int }')[0]
            eq(math(coef),s.Rational(1,3) if idx in (4,5) else (s.log(p['uh'])-s.log(p['ul']))/3)
        primv=re.search(r'\\cdot (.*?)\\,\{\|\}',rows[7])[1];eq(s.diff(math(primv),v),v**power)
        for idx in (4,7):
            endpoints_label=re.search(r'\{\|\}_\{(\d+)\}\^\{(\d+)\}',rows[idx]);assert endpoints_label
            assert tuple(map(int,endpoints_label.groups()))==((p['ul'],p['uh']) if idx==4 else (p['vl'],p['vh']))
        eq(math(rows[7].split(' & =')[-1].split(r'\cdot')[0]),(s.log(p['uh'])-s.log(p['ul']))/3)
        eq(math(rows[8].split(' & =')[-1].split(r'\cdot')[0]),(s.log(p['uh'])-s.log(p['ul']))/(3*n))
        endpoints=re.search(r'\\cdot \((-?\d+)-(-?\d+)\)',rows[8]);assert endpoints
        eq(s.Integer(endpoints[1])/n,math(primv).subs(v,p['vh']));eq(s.Integer(endpoints[2])/n,math(primv).subs(v,p['vl']))
        eq(math(rows[-1].split(' & =')[-1].split(r'.\end{aligned}')[0]),val)
    else:
        operative={'triangular_quadratic':r'uv-{v}^{2}+\frac{{u}^{2}-2uv+{v}^{2}}{4}','product':r'8(\frac{v-u}{2})(\frac{v+u}{2})','exponential':r'{e}^{3u-5v+2v-u}','sum_square':r'3{u}^{2}|\frac{∂(x,y)}{∂(u,v)}|'}
        if name in operative:assert operative[name] in chain,'missing operative source stage'
        expected_rows={'difference':3,'triangular_quadratic':3,'product':4,'exponential':4,'sum_square':3}
        assert len(rows)==expected_rows[name],('operative family row count',name,len(rows))
        # Every actual substitution/expansion/product row represents f(T), with numeric J only at its source stage.
        for row in rows[:-1]:
            rhs=row.split('&=')[-1] if '&=' in row else row.split(' & =')[-1]
            rhs=re.sub(r'\{∬\}_\{Δ\}|\\iint_Δ','',rhs)
            rhs=rhs.replace(r'\left|\frac{∂(x,y)}{∂(u,v)}\right|',str(1/s.Abs(jac)))
            rhs=rhs.replace(r'|\frac{∂(x,y)}{∂(u,v)}|',str(1/s.Abs(jac)))
            rhs=re.split(r'(?:\\text\{d\}|d)u',rhs)[0].replace(r'\,','')
            eq(math(rhs),z)
        final=rows[-1].split(' & =')[-1] if ' & =' in rows[-1] else rows[-1].split('&=')[-1]
        val,zi,bounds=integral_value(final.split(r'.\end{aligned}')[0]);eq(zi,z)
        assert bounds=={'u':(p['ul'],p['uh']),'v':(p['vl'],p['vh'])}

def validate(record):
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    q=record['question'];balanced(q[':question/problem']);p,U,V,f,jac,z=read_prompt(record)
    assert p==record['generation']['parameters']
    field=q[':question/answer-fields'][0]
    assert field[':answer-field/type']==':answer-field.type/radio'
    assert len(field[':answer-field/choices'])==5
    ids=[a[':answer/id'] for a in field[':answer-field/choices']];assert len(set(ids))==5
    assert field[':answer-field/correct'][0]==':answer/id' and field[':answer-field/correct'][1] in ids
    vals=[];answer=s.integrate(s.integrate(z,(u,p['ul'],p['uh'])),(v,p['vl'],p['vh']))
    for a in field[':answer-field/choices']:
        balanced(a[':answer/value']);assert a[':answer/type']==':answer.type/math'
        if record['generation']['difficulty']=='easy':
            val,integrand,bounds=integral_value(a[':answer/value'])
            assert bounds=={'u':(p['ul'],p['uh']),'v':(p['vl'],p['vh'])}
        else:val=math(a[':answer/value'])
        vals.append(val)
        if a[':answer/id']==field[':answer-field/correct'][1]:eq(val,answer)
    assert g.eligible(vals),'ambiguous complete scalar values'
    check_solution(record,p,U,V,f,jac,z)
    return True

def replay_fidelity():
    cases=json.loads((D/'source-cases.json').read_text());raw=g.RAW['record'][':knowledge-point/questions']
    choices=0;solutions=0;designations=0
    originals=[]
    for case,source in zip(cases,raw):
        r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile='observed');q=r['question'];sf=source[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
        assert set(source)-{':db/id'}==set(q),'all normalized question-key presence parity'
        assert q[':question/math-academy-id']==source[':question/math-academy-id']
        assert f[':answer-field/key']==sf[':answer-field/key']
        assert f[':answer-field/type']==sf[':answer-field/type'][':db/ident']
        for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
            assert (key in source)==(key in q),(case,key,'presence parity')
        assert q[':question/problem']==source[':question/problem']
        if ':question/worked-solution' in source:assert q[':question/worked-solution']==source[':question/worked-solution'];solutions+=1
        assert (':answer-field/correct' in f)==(':answer-field/correct' in sf)
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices']);choices+=len(f[':answer-field/choices'])
        if ':answer-field/correct' in sf:
            correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert correct[':answer/value']==sf[':answer-field/correct'][':answer/value'];designations+=1
        originals.append(r)
    return dict(practice_questions=7,prompts_exact=7,choices_exact=choices,choices_total=35,complete_banks_exact=7,worked_solutions_exact=solutions,worked_solutions_present=5,correct_designations_matched=designations,correct_designations_present=5,missing_correct_designations=2,raw_key_presence_parity=7),originals

def mutation_regressions(record):
    # Algebraic equality alone cannot excuse removal of a source teaching operation.
    src=g.generate('easy',template='triangular_quadratic',parameters=dict(ul=0,uh=5,vl=0,vh=1))
    mutant=copy.deepcopy(src);text=mutant['question'][':question/worked-solution']
    text=text.replace(r'uv-{v}^{2}+\frac{{u}^{2}-2uv+{v}^{2}}{4}',r'\frac{{u}^{2}+2uv-3{v}^{2}}{4}')
    mutant['question'][':question/worked-solution']=text
    # Require the expanded square to remain an operative node under all bound variants.
    def operative(r):assert r'uv-{v}^{2}+\frac{{u}^{2}-2uv+{v}^{2}}{4}' in r['question'][':question/worked-solution']
    operative(src)
    try:validate(mutant)
    except AssertionError:pass
    else:raise AssertionError('operative mutation accepted')
    mutant=copy.deepcopy(record);mutant['question'][':question/worked-solution']=mutant['question'][':question/worked-solution'].replace('125-64','126-65')
    if mutant['question']==record['question']:raise AssertionError('endpoint mutation was not applied')
    try:validate(mutant)
    except AssertionError:pass
    else:raise AssertionError('correlated both-endpoint mutation accepted')
    mutant=copy.deepcopy(record);mutant['question'][':question/problem']+='\x0c'
    try:validate(mutant)
    except AssertionError:pass
    else:raise AssertionError('C0 mutation accepted')
    return {'operative_equal_expression_rejected':True,'correlated_both_endpoint_error_rejected':True,'C0_byte_rejected':True}

def main():
    fidelity,originals=replay_fidelity();records=[];seen={}
    source_math=[]
    for raw in originals:
        name=raw['generation']['template'];field=raw['question'][':question/answer-fields'][0]
        vals=[integral_value(a[':answer/value'])[0] if r'\int' in a[':answer/value'] else math(a[':answer/value']) for a in field[':answer-field/choices']]
        if name=='sum_product_evidence':
            lower=12*(s.exp(4)-s.E)
            # e>2 implies this lower bound strictly exceeds the largest observed option10(e⁴−1).
            assert all(s.N(lower-z,50)>0 for z in vals)
            exact=12*s.exp(4)-16*s.E+2*s.sqrt(s.pi)*(s.erfi(2)-s.erfi(1))
            source_math.append(dict(template=name,bank_valid=False,reason='nonrectangular image; two branches; all options below rigorous true-integral lower bound',exact_value=str(exact)))
            continue
        p,U,V,f,jac,z=read_prompt(raw);expected=s.integrate(s.integrate(z,(u,p['ul'],p['uh'])),(v,p['vl'],p['vh']))
        if ':answer-field/correct' in field:
            selected=next(a for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1])
            eq(integral_value(selected[':answer/value'])[0] if r'\int' in selected[':answer/value'] else math(selected[':answer/value']),expected)
        elif name=='difference':eq(expected,s.Rational(9,2))
        valid=g.eligible(vals)
        assert valid==(name!='product')
        source_math.append(dict(template=name,bank_valid=valid,correct_value=str(expected),designation_present=':answer-field/correct' in field))
    for name in g.EASY:
        for seed in range(12):records.append(g.generate('easy',seed,template=name))
    for level in ('moderate','hard'):
        for seed in range(18):records.append(g.generate(level,seed))
    for record in records:validate(record)
    finite={}
    for level,ceiling in [('moderate',8),('hard',6)]:
        tasks=[]
        for b in (4,9,16):
            for c in range(1,ceiling):
                for d in range(c+1,ceiling+1):
                    r=g.generate(level,template='ratio_product' if level=='moderate' else 'ratio_product_squared',parameters=dict(ul=1,uh=b,vl=c,vh=d));validate(r);tasks.append(r['generation']['mathematical_fingerprint'])
        assert len(set(tasks))==len(tasks);finite[level]=len(tasks)
    special=g.generate('hard' ,template='ratio_product_squared',parameters=dict(ul=1,uh=9,vl=4,vh=5));validate(special)
    regressions=mutation_regressions(special)
    # Strict explicit scope and selectors; order/seed do not change fixed content identity.
    invalid=0
    for kwargs in [dict(level='hard',parameters=dict(ul=1,uh=9,vl=1,vh=7)),dict(level='moderate',parameters=dict(ul=0,uh=4,vl=1,vh=5)),dict(level='easy',parameters=dict(ul=-4,uh=4,vl=0,vh=2)),dict(level='easy',parameters=dict(ul=0,uh=3,vl=7,vh=9)),dict(level='easy',field_type='blank'),dict(level='easy',profile='unknown'),dict(level='hard',template='ratio_product')]:
        try:g.generate(**kwargs)
        except ValueError:invalid+=1
        else:raise AssertionError(('invalid explicit input accepted',kwargs))
    for r in records:
        a=g.generate(r['generation']['difficulty'],seed=122,template=r['generation']['template'],parameters=r['generation']['parameters']);assert a['question'][':question/id']==r['question'][':question/id']
        seen.setdefault(r['generation']['difficulty'],set()).add(r['generation']['mathematical_fingerprint'])
    # All observed families participate in default easy sampling.
    assert set(g.generate('easy',i)['generation']['template'] for i in range(40))==set(g.EASY)
    inputs=[]
    for i,r in enumerate(records+[r for r in originals if ':answer-field/correct' in r['question'][':question/answer-fields'][0]]):
        f=r['question'][':question/answer-fields'][0];checks=[dict(submitted_answer_id=a[':answer/id'],expected='accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected',purpose='owned radio selection') for a in f[':answer-field/choices']]
        inputs.append(dict(label=str(i),record=r,checks=checks))
    (D/'native-input.json').write_text(json.dumps(inputs,ensure_ascii=False,indent=2)+'\n')
    root=D.parents[2];engine=root/'generate/runs/current/check-engine'
    subprocess.run([str(engine),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
    native=json.loads((D/'native-report.json').read_text())
    # Per observed template/bank, original plus a clearly labeled changed-bound variant.
    reviewrecords=[]
    for n in g.EASY:reviewrecords.extend(g.generate('easy',seed,template=n) for seed in (31,32))
    for l in ('moderate','hard'):reviewrecords.extend(g.generate(l,seed) for seed in (31,32))
    for case in json.loads((D/'source-cases.json').read_text()):
        p=case['parameters'].copy();p['vh']+=1 if p['vh']<10 else 0
        if case['template']=='sum_product_evidence':p['uh']+=1
        reviewrecords.append(g.generate(case['level'],33,template=case['template'],parameters=p,profile='observed'))
    (D/'review.json').write_text(json.dumps(reviewrecords,ensure_ascii=False,indent=2)+'\n')
    review=['# Performing a Change of Variables: review','Frozen source: math, basis1356. Raw originals preserve missing attributes; observed replays are evidence-only. Normal variants are authored complete banks.']
    for raw,case in zip(originals,json.loads((D/'source-cases.json').read_text())):
        review+=['\n## Original '+str(case['source_id'])+' / '+case['template'],g.markdown(raw)]
    for r in reviewrecords:review+=['\n## Generated '+r['generation']['difficulty']+' / '+r['generation']['template']+' / '+r['generation']['profile'],g.markdown(r)]
    (D/'review.md').write_text('\n\n'.join(review)+'\n')
    report=dict(status='pass',database_writes=0,source_fidelity=fidelity,source_mathematics=source_math,normal_math={'records':len(records),'actual_printed_prompt_bank_jacobian_substitution_region_stages_checked':len(records),'nonlinear_both_endpoint_components_checked':36,'unique_sample_tasks':{k:len(v) for k,v in seen.items()},'finite_nonlinear_tasks_all_checked':finite},scope={'invalid_explicit_cases_rejected':invalid,'hard_authored':True,'default_easy_families':list(g.EASY),'same_supplied_transformation_all_levels':True},regressions=regressions,native={'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':native['documented_unresolved_checks'],'normal_records':96,'present_source_designation_records':5,'source_missing_key_records_excluded':2,'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest()},anomalies=[{'source_id':17592186198948,'finding':'missing difficulty, solution and correct designation','normal':'authored completed easy solution/designation'},{'source_id':17592186198950,'finding':'missing correct ref, difficulty, solution; rectangular-image/one-to-one hypotheses fail; no bank answer independently supported','normal':'excluded from learning; raw public replay only'},{'source_id':17592186375495,'finding':'two designated/doubled complete integral values both zero','normal':'reject whole bank/instance on full-value collisions'}],dependencies={'python':sys.version.split()[0],'sympy':s.__version__})
    (D/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
