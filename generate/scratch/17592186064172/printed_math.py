"""Independent reader of actual displayed restricted TeX; no generator helpers.

Reads full expressions, derivatives modulo C, integrands and every solution row.
Numbers are obtained from printed prompts, never generation parameter metadata.
"""
import itertools,re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
x=sp.Symbol('x',positive=True);C=sp.Symbol('C')
COMMON='To compute the integral of a general exponential function, we just need to divide by the natural logarithm of the base of the exponential function:'

def translate(s):
    s=s.replace('ln\u2061','LOG').replace(r'\ln','LOG').replace(r'\cdot','*').replace(r'\,','').replace(r'\displaystyle','')
    def delimited(pos,left,right):
        assert s[pos]==left
        start=pos+1;depth=1;pos+=1
        while depth:
            assert pos<len(s),'Unbalanced mathematical grouping'
            if s[pos]==left:depth+=1
            if s[pos]==right:depth-=1
            pos+=1
        return s[start:pos-1],pos
    out='';i=0
    while i<len(s):
        if s.startswith(r'\frac',i):
            i+=5;a,i=delimited(i,'{','}');b,i=delimited(i,'{','}');out+='(('+translate(a)+')/('+translate(b)+'))'
        elif s.startswith('LOG',i):
            i+=3
            while i<len(s) and s[i].isspace():i+=1
            if s[i]=='(':a,i=delimited(i,'(',')')
            elif s[i]=='{':a,i=delimited(i,'{','}')
            else:
                m=re.match(r'\d+|x',s[i:]);assert m,'Missing log argument';a=m.group(0);i+=len(a)
            out+='log('+translate(a)+')'
        elif s[i]=='{':
            a,i=delimited(i,'{','}');out+='('+translate(a)+')'
        else:out+=s[i];i+=1
    return out

def parse(s):
    s=s.strip().rstrip('.')
    a=parse_expr(translate(s),local_dict={'x':x,'C':C,'log':sp.log},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))
    assert a.free_symbols<={x,C},('Unexpected displayed variable',s,a)
    assert not a.has(sp.nan,sp.zoo,sp.oo,-sp.oo)
    return a

def equal(a,b):return sp.simplify(a-b)==0

def integral_body(s):
    m=re.search(r'\\int\s*(.*?)((?:\\,)?\\text\{d\}x|dx)',s,re.S)
    assert m,('No readable integral',s)
    return m.group(1)

def normalize_ln(s):return s.replace('ln\u2061',r'\ln ')

def prose_mask(s):
    """Full prose/stage sequence independent of numeric slots/ln notation."""
    s=normalize_ln(s)
    return re.sub(r'-?\d+','N',s)

def validate(r,source_solutions):
    q=r['question'];field=q[':question/answer-fields'][0]
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    assert field[':answer-field/type']==':answer-field.type/radio'
    assert field[':answer-field/key']=='selection'
    # Full math parser first, plus structural family demands from the printed body.
    body=integral_body(q[':question/problem']);integrand=parse(body)
    powers=list(integrand.atoms(sp.Pow));expo=[p for p in powers if p.exp==x and not p.base.free_symbols]
    assert len(expo)==1,('Exactly one constant-base x exponential required',body)
    a=expo[0].base;c=sp.simplify(integrand/expo[0]);assert c.is_Integer and c!=0
    level=r['generation']['level']
    assert a>0 and a!=1
    if level=='hard':assert c==1 and a.p==1 and 2<=a.q<=20
    else:
        assert a.is_Integer and 2<=a<=20
        if level=='easy':assert c==1
        else:assert 2<=abs(c)<=12
    values=[parse(v[':answer/value']) for v in field[':answer-field/choices']]
    assert len(values)==5 and all(v.has(C) for v in values)
    derivatives=[sp.diff(v,x) for v in values]
    correct=[i for i,d in enumerate(derivatives) if equal(d,integrand)];assert len(correct)==1
    for i,j in itertools.combinations(range(5),2):assert not equal(derivatives[i],derivatives[j]),'Derivative-equivalent pair'
    ids=[v[':answer/id'] for v in field[':answer-field/choices']];assert len(set(ids))==5
    for v in ids+[field[':answer-field/id'],q[':question/id']]:
        import uuid
        assert str(uuid.UUID(v))==v
    if ':answer-field/correct' in field:assert field[':answer-field/correct']==[':answer/id',ids[correct[0]]]
    rows_checked=0
    strings=[q[':question/problem']]+[v[':answer/value'] for v in field[':answer-field/choices']]
    if ':question/worked-solution' in q:
        sol=q[':question/worked-solution'];strings.append(sol)
        target=source_solutions['q-113893' if level=='hard' else ('q-113890' if level=='moderate' else 'q-66139')]
        assert prose_mask(sol)==prose_mask(target),'Full source prose/stage mask changed'
        chains=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)
        assert len(chains)==(3 if level=='hard' else 1)
        first=chains[0].split(r'\\')
        assert len(first)==(2 if level=='moderate' else 1)
        lhs,rhs=first[0].split('& =');assert equal(parse(integral_body(lhs)),integrand)
        if level=='moderate':
            p=re.search(r'First, we factor out the constant \$(.*?)\.\$',sol);assert p and equal(parse(p.group(1)),c)
            outer,basic=rhs.split(r'\int');outer=parse(outer.strip());basic=parse(integral_body(r'\int'+basic))
            assert equal(outer,c) and equal(basic,a**x),'Constant factorization stage changed'
            assert equal(outer*basic,integrand)
            final=first[1].split('& =')[1];assert equal(sp.diff(parse(final),x),integrand)
            # The factorized integral and final base-rule quotient are operative structures.
            assert r'\cdot \frac{' in final and normalize_ln(final).count(r'\ln ')==1
            rows_checked=3
        else:
            primitive=parse(rhs);assert equal(sp.diff(primitive,x),integrand)
            assert rhs.lstrip().startswith(r'\frac{') and normalize_ln(rhs).count(r'\ln ')==1
            rows_checked=1
        if level=='hard':
            b=int(a.q);logrows=chains[1].split(r'\\');assert len(logrows)==3
            lr=normalize_ln(logrows[0]);l,rh=lr.split(' & =')
            # Required log quotient, ln1-ln b, 0-ln b and -ln b masks.
            assert l==r'\ln (\frac{1}{'+str(b)+'})'
            assert rh==r'\ln 1-\ln '+str(b)+' '
            assert equal(parse(l),parse(rh));rows_checked+=1
            second=normalize_ln(logrows[1]).strip();assert second=='& =0-'+r'\ln '+str(b)
            third=normalize_ln(logrows[2]).strip();assert third=='& =-'+r'\ln '+str(b)+'.'
            last=parse(rh)
            for row in logrows[1:]:
                v=parse(row.split('& =')[1]);assert equal(last,v);last=v;rows_checked+=1
            left,right=chains[2].split('=');assert equal(parse(left),parse(right))
            assert equal(sp.diff(parse(left),x),integrand) and equal(sp.diff(parse(right),x),integrand)
            assert normalize_ln(left).endswith(r'\ln (\frac{1}{'+str(b)+'})}+C')
            assert normalize_ln(right).startswith(r'-\frac{') and normalize_ln(right).endswith(r'\ln '+str(b)+'}+C')
            rows_checked+=2
    for s in strings:
        assert not any(ord(z)<32 and z not in '\n\t' for z in s),'Control character'
        assert s.count('$')%2==0
        depth=0
        for z in s:
            if z=='{':depth+=1
            elif z=='}':depth-=1;assert depth>=0
        assert depth==0,'Unbalanced TeX braces'
    assert all(':answer/feedback' not in v for v in field[':answer-field/choices'])
    return {'integrand':str(integrand),'printed_base':str(a),'printed_coefficient':str(c),'solution_rows_checked':rows_checked,'inferred_correct_value':field[':answer-field/choices'][correct[0]][':answer/value']}
