#!/usr/bin/env python3
"""Independent read-back validation, exhaustive finite domains and native radio grading.

Run from the repository root: .venv/bin/python generate/scratch/17592186133926/validate.py
All assertions concern displayed mathematics/attributes, not generator metadata
answers. The captured raw teaching errors are expected evidence failures, kept
separate from the normal correctness pass. No database operations are performed.
"""
import importlib.util
import itertools
import json
from pathlib import Path
import re
import subprocess
import sys
import hashlib
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application

sys.dont_write_bytecode=True
HERE=Path(__file__).parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('circulation',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
symbols={v:sp.Symbol(v,real=True) for v in 'txyzijk'}
t=symbols['t']

def eq(a,b):
    return sp.simplify(sp.trigsimp(a-b))==0

def parse(s):
    s=s.strip().rstrip('.,').replace('⁡',' ').replace('π',r'\pi ').replace('−','-')
    s=s.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\;','')
    s=s.replace(r'\operatorname{sin}',r'\sin').replace(r'\operatorname{cos}',r'\cos')
    s=re.sub(r'\\(sin|cos)\s+t\b',r'\1(t)',s)
    s=re.sub(r'\{(sin|cos)\}\^\{2\}\s*\(([^()]*)\)',r'(\1(\2))^2',s)
    s=re.sub(r'\{(sin|cos)\}\^\{2\}\s*t',r'(\1(t))^2',s)
    def fractions(v):
        while '\\frac' in v:
            start=v.index('\\frac');n=start+5
            def take(n):
                assert v[n]=='{',(v,n)
                depth=1;j=n+1
                while depth:
                    depth+=(v[j]=='{')-(v[j]=='}');j+=1
                return v[n+1:j-1],j
            a,n=take(n);b,n=take(n)
            v=v[:start]+'(('+fractions(a)+')/('+fractions(b)+'))'+v[n:]
        return v
    s=fractions(s)
    s=s.replace(r'\pi','pi').replace(r'\sin','sin').replace(r'\cos','cos')
    s=s.replace(r'\cdot','*').replace('{','(').replace('}',')').replace('^','**')
    s=s.replace('[','(').replace(']',')')
    assert '\\' not in s,s
    value=parse_expr(s,local_dict={**symbols,'pi':sp.pi,'sin':sp.sin,'cos':sp.cos},
                     transformations=standard_transformations+(implicit_multiplication_application,))
    assert value.free_symbols<=set(symbols.values()),(s,value)
    return value

def formatting(s):
    assert s.count('$')%2==0
    depth=0
    for c in s:
        if c=='{':depth+=1
        elif c=='}':depth-=1
        assert depth>=0,s
    assert depth==0,s
    assert '--' not in s and '+-' not in s

def vector(s,formal=False):
    parts=re.split(r'\\,([ijk])',s)
    assert len(parts)==7,parts
    out=[]
    for i in range(3):
        assert parts[2*i+1]=='ijk'[i]
        term=parts[2*i].lstrip('+')
        if formal:
            prefix=r'\frac{\mathrm d}{\mathrm dt}'
            assert term.startswith(prefix),term
            out.append(sp.diff(parse(term[len(prefix):]),t))
        else:out.append(parse(term))
    assert not parts[-1].strip()
    return out

def rows(sol):
    blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)
    return [[v.split('& =',1)[1].strip() for v in b.split(r'\\')] for b in blocks]

def bounds(s):
    m=re.match(r'\\int_\{(.*?)\}\^\{(.*?)\}(.*)',s)
    assert m,s
    return parse(m[1]),parse(m[2]),m[3]

def normal(r):
    q=r['question'];f=q[':question/answer-fields'][0]
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    assert r['knowledge_point']['db_id']==g.DB_ID
    assert f[':answer-field/type']==':answer-field.type/radio'
    assert len(f[':answer-field/choices'])==5
    for s in (q[':question/problem'],q[':question/worked-solution']):formatting(s)
    # Derive all mathematics from the ACTUAL displayed prompt.
    prompt=q[':question/problem']
    Fs=re.search(r'F\(x,y,z\)=(.*?)\$',prompt)[1]
    rs=re.search(r'r\(t\)=(.*?)\$',prompt)[1]
    F=vector(Fs);curve=vector(rs)
    interval=re.search(r't\\in \[(.*?),(.*?)\)',prompt)
    lo,hi=parse(interval[1]),parse(interval[2]);assert hi>lo
    assert all(eq(e.subs(t,hi),e.subs(t,lo)) for e in curve)
    dr=[sp.diff(e,t) for e in curve]
    Fr=[e.subs(dict(zip([symbols[c] for c in 'xyz'],curve)),simultaneous=True) for e in F]
    product=sum(a*b for a,b in zip(Fr,dr))
    answer=sp.integrate(sp.expand_trig(product),(t,lo,hi));answer=sp.simplify(answer)
    sol=q[':question/worked-solution'];rr=rows(sol)
    assert list(map(len,rr))==[2,2,4,5]
    coords=re.search(r'\$\$\s*x=(.*?)\.\s*\$\$',sol,re.S)[1].split(',\\quad ')
    for component,e,v in zip(coords,curve,'xyz'):
        expression=component.split('=',1)[1] if component.startswith(v+'=') else component
        assert eq(parse(expression),e),(component,e)
    for a,b in zip(vector(rr[0][0]),F):assert eq(a,b)
    for a,b in zip(vector(rr[0][1]),Fr):assert eq(a,b)
    for a,b in zip(vector(rr[1][0],True),dr):assert eq(a,b)
    for a,b in zip(vector(rr[1][1]),dr):assert eq(a,b)
    # The first dot row has two separate vectors; scalar product rows are read
    # independently, including every displayed zero contribution/product.
    ds=rr[2][0]
    m=re.match(r'\\left\((.*)\\right\)\\cdot\\left\((.*)\\right\)$',ds)
    assert m,ds
    for a,b in zip(vector(m[1]),Fr):assert eq(a,b)
    for a,b in zip(vector(m[2]),dr):assert eq(a,b)
    for stage in rr[2][1:]:assert eq(parse(stage),product),(stage,product)
    # Formal definition and symbolic integral are substantive displayed stages.
    assert r'Γ=\oint_C F\cdot\mathrm dr=\int_a^b F(r(t))\cdot r^{\prime}(t)\,\mathrm dt.' in sol
    slo,shi,body=bounds(rr[3][0]);assert eq(slo,lo) and eq(shi,hi)
    assert body==r'F(r(t))\cdot r^{\prime}(t)\,\mathrm dt'
    slo,shi,body=bounds(rr[3][1]);assert eq(slo,lo) and eq(shi,hi)
    integrand=parse(body.removesuffix(r'\,\mathrm dt'));assert eq(integrand,product)
    m=re.match(r'\\left\[(.*?)\\right\]_\{(.*?)\}\^\{(.*?)\}$',rr[3][2]);assert m
    primitive=parse(m[1]);assert eq(sp.diff(primitive,t),product)
    assert eq(parse(m[2]),lo) and eq(parse(m[3]),hi)
    ep=rr[3][3];m=re.match(r'\[(.*)\]-\[(.*)\]',ep);assert m
    # Independent individually evaluated terms, not merely their collected sum.
    pterms=sorted(sp.Add.make_args(sp.expand(primitive)),key=sp.default_sort_key)
    for displayed,endpoint in ((m[1],hi),(m[2],lo)):
        pieces=re.findall(r'\\left\((.*?)\\right\)',displayed)
        assert '+'.join(r'\left('+piece+r'\right)' for piece in pieces)==displayed
        assert len(pieces)==len(pterms)
        for piece,term in zip(pieces,pterms):assert eq(parse(piece),term.subs(t,endpoint)),(piece,term,endpoint)
    assert eq(parse(ep),answer) and eq(parse(rr[3][4]),answer)
    values=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
    assert not any(eq(a,b) for a,b in itertools.combinations(values,2))
    designated=[a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]]
    assert len(designated)==1 and eq(parse(designated[0][':answer/value']),answer)
    # Recompute all method error values from displayed components.
    key=r['generation']['template']
    if key in ('xy_rotation','xy_rotation_z','yz_rotation'):expected=[answer,-answer,answer/2,sp.S.Zero,2*answer]
    elif key=='xy_symmetric':
        ia=sp.integrate(Fr[0]*dr[0],(t,lo,hi));ib=sp.integrate(Fr[1]*dr[1],(t,lo,hi))
        expected=[answer,ia-ib,-ia+ib,ia,ib]
    elif key=='polynomial_sine':
        px=sp.integrate(Fr[0]*dr[0],t);pz=sp.integrate(Fr[2]*dr[2],t)
        xe=px.subs(t,hi)+px.subs(t,lo)
        peak=2*pz.subs(t,sp.Rational(1,2))
        expected=[answer,-xe,xe,-peak,peak]
    else:
        # Recover a,b from printed curve, and verify intended field relation.
        a=sp.Poly(curve[0],t).coeff_monomial(t*t);b=sp.Poly(curve[1],t).coeff_monomial(t**3)
        omitted_y=F[0].subs(symbols['y'],0).subs(symbols['x'],curve[0])
        wrongcubic=F[0].subs({symbols['x']:curve[0],symbols['y']:curve[1]-b*t**3},simultaneous=True)
        wrongderivative=dr[0]+a
        expected=[answer,-answer,sp.integrate(omitted_y*dr[0],(t,lo,hi)),
                  sp.integrate(wrongcubic*dr[0],(t,lo,hi)),sp.integrate(Fr[0]*wrongderivative,(t,lo,hi))]
    assert all(sum(eq(v,e) for e in expected)==1 for v in values),(key,values,expected)
    return answer

def original_math(sid):
    # Independent transcription of ALL original prompt components, not metadata.
    x,y,z=[symbols[c] for c in 'xyz']
    cases={
      'q-161925':([sp.cos(sp.pi*t),sp.sin(sp.pi*t),1-t*t],[y,-x,0],-1,1),
      'q-162238':([t*t-t,t**3-t,sp.sin(2*sp.pi*t)],[y-x,0,0],0,1),
      'q-162220':([sp.sin(t),sp.cos(t),2*sp.sin(t)],[y,x,0],0,2*sp.pi),
      'q-162230':([sp.sin(t),sp.cos(t),t*t],[y,-x,z],-sp.pi,sp.pi),
      'q-162235':([1-t*t,t*t,sp.sin(sp.pi*t)],[x+y,0,-z],-1,1),
      'q-162237':([sp.sin(t),sp.cos(t),sp.sin(t)],[0,-z,y],0,2*sp.pi),
      'q-162229':([2*sp.cos(sp.pi*t),sp.sin(sp.pi*t),2],[-y,x,0],0,2),
      'q-162228':([t*t-t,sp.cos(2*sp.pi*t),sp.sin(2*sp.pi*t)],[0,z,-y],0,1),
    }
    r,F,lo,hi=cases[sid]
    assert all(eq(sp.sympify(e).subs(t,lo),sp.sympify(e).subs(t,hi)) for e in r)
    sub=dict(zip((x,y,z),r));prod=sum(sp.sympify(f).subs(sub,simultaneous=True)*sp.diff(e,t) for f,e in zip(F,r))
    return sp.simplify(sp.integrate(sp.expand_trig(prod),(t,lo,hi)))

def source_vector(s,formal=False):
    # Source basis components may be absent or bare (i, rather than 1 i).
    s=s.strip().rstrip('.').replace(r'\,',' ')
    if not formal:
        value=sp.expand(parse(s))
        out=[value.coeff(symbols[c]) for c in 'ijk']
        assert eq(value,sum(e*symbols[c] for e,c in zip(out,'ijk'))),(s,value)
        return out
    parts=re.split(r'\b([ijk])\b',s)
    assert len(parts)%2==1,parts
    out=[sp.S.Zero]*3
    for n in range(0,len(parts)-1,2):
        coeff=parts[n].strip()
        if formal:
            prefix=r'\frac{\text{d}}{\text{d}t}'
            assert coeff.lstrip('+').startswith(prefix),coeff
            value=sp.diff(parse(coeff.lstrip('+')[len(prefix):]),t)
        else:
            value=parse({'':'1','+':'1','-':'-1'}.get(coeff,coeff))
        out['ijk'.index(parts[n+1])]=value
    assert not parts[-1].strip(),parts
    return out

def audit_source(sid,record=None):
    """Read every captured operator/vector/product/integral stage independently.

    The result lists mathematical failures instead of treating exact replay or
    a correct final scalar as proof of the intervening teaching calculation.
    Original endpoint layout is retained (some originals omit that row).
    """
    q=g.ORIGINALS[sid] if record is None else record['question'];prompt=q[':question/problem']
    F=source_vector(re.search(r'F\(x,\s*y,\s*z\)\s*=\s*(.*?)\$',prompt)[1])
    curve=source_vector(re.search(r'r\(t\)\s*=\s*(.*?)\$',prompt)[1])
    interval=re.search(r't\s*(?:\\in|∈)\s*\[(.*?),(.*?)\)',prompt)
    lo,hi=parse(interval[1]),parse(interval[2]);assert hi>lo
    assert all(eq(e.subs(t,lo),e.subs(t,hi)) for e in curve)
    dr=[sp.diff(e,t) for e in curve]
    Fr=[e.subs(dict(zip([symbols[c] for c in 'xyz'],curve)),simultaneous=True) for e in F]
    prod=sum(f*d for f,d in zip(Fr,dr));answer=sp.integrate(sp.expand_trig(prod),(t,lo,hi))
    if record is None:assert eq(answer,original_math(sid))
    if ':question/worked-solution' not in q:return {'source_id':sid,'checked':'prompt and all bank values; original solution absent','failed_stages':[]}
    sol=q[':question/worked-solution'];rr=rows(sol);failed=[];checked=0
    def check(v,e,label):
        nonlocal checked
        checked+=1
        if not eq(v,e):failed.append(label)
    # Formal circulation definition is read as its exact source symbolic row.
    assert 'Γ={∮}_{C}F\\cdot \\text{d}r={\\int }_{a}^{b}F(r(t))\\cdot {r}^{′}(t)\\,\\text{d}t.' in sol
    coords=re.search(r'\$\$\s*x=(.*?)\.\s*\$\$',sol,re.S)[1].split(r'\,')
    assert len(coords)==3
    for v,e,c in zip(coords,curve,'xyz'):check(parse(v.removeprefix(c+'=')),e,'coordinate '+c)
    for n,row in enumerate(rr[0]):
        for c,v,e in zip('ijk',source_vector(row),F if n==0 else Fr):check(v,e,'F substitution '+str(n)+' '+c)
    for c,v,e in zip('ijk',source_vector(rr[1][0],True),dr):check(v,e,'formal derivative '+c)
    for c,v,e in zip('ijk',source_vector(rr[1][1]),dr):check(v,e,'evaluated derivative '+c)
    def unwrap(s):
        m=re.match(r'^(-?\d+)\\left\((.*)\\right\)$',s,re.S)
        return (sp.Integer(m[1]),m[2]) if m else (sp.S.One,s)
    scale,inner=unwrap(rr[2][0]);left,right=inner.split(r'\cdot ',1)
    assert left.startswith('(') and left.rstrip().endswith(')') and right.startswith('(') and right.rstrip().endswith(')')
    for label,raw,expected in (('dot first vector',left,Fr),('dot second vector',right,dr)):
        for c,v,e in zip('ijk',source_vector(raw.strip()[1:-1]),expected):check((scale*v if label=='dot first vector' else v),e,label+' '+c)
    for n,row in enumerate(rr[2][1:]):check(parse(row),prod,'dot scalar row '+str(n+1))
    primitive=None
    for n,row in enumerate(rr[3]):
        scale,inner=unwrap(row)
        canonical=inner.replace(r'{\int }',r'\int').replace('{[','[').replace(']}',']')
        if canonical.startswith(r'\int'):
            a,b,body=bounds(canonical);check(a,lo,'integral lower bound '+str(n));check(b,hi,'integral upper bound '+str(n))
            if n==0:assert body==r'F(r(t))\cdot {r}^{′}(t)\,\text{d}t'
            else:check(scale*parse(body.removesuffix(r'\,\text{d}t')),prod,'integrand row '+str(n))
        elif re.search(r'\]_\{',canonical):
            m=re.match(r'(.*?)\[(.*?)\]_\{(.*?)\}\^\{(.*?)\}',canonical);assert m,canonical
            primitive=scale*parse(m[1] or '1')*parse(m[2]);check(sp.diff(primitive,t),prod,'primitive derivative')
            check(parse(m[3]),lo,'primitive lower bound');check(parse(m[4]),hi,'primitive upper bound')
        else:
            if n!=len(rr[3])-1:
                assert primitive is not None
                if sid in ('q-161925','q-162229','q-162228'):
                    m=re.match(r'^(.*?)\((.*?)\-\((.*?)\)\)$',canonical)
                    if not m:m=re.match(r'^(.*?)\((.*?)\-(.*?)\)$',canonical)
                    assert m,canonical
                    check(scale*parse(m[1]),sp.expand(primitive).coeff(t),'endpoint coefficient')
                    check(parse(m[2]),hi,'individually evaluated upper t')
                    check(parse(m[3]),lo,'individually evaluated lower t')
                elif sid=='q-162230':
                    m=re.match(r'^\(\((.*?)\-\((.*?)\)\)\+\\frac\{(.*?)\}\{2\}\)$',canonical);assert m,canonical
                    upper,lower=m[3].split('-(',1)
                    pterms=sp.Add.make_args(sp.expand(primitive))
                    linear=next(e for e in pterms if sp.degree(e,t)==1)
                    quartic=next(e for e in pterms if sp.degree(e,t)==4)
                    check(scale*parse(m[1]),linear.subs(t,hi),'individual upper linear term')
                    check(scale*parse(m[2]),linear.subs(t,lo),'individual lower linear term')
                    check(scale*parse(upper)/2,quartic.subs(t,hi),'individual upper quartic term')
                    check(scale*parse('('+lower)/2,quartic.subs(t,lo),'individual lower quartic term')
                elif sid=='q-162235':
                    m=re.match(r'^\((.*?)\)-\((.*?)\)$',canonical);assert m,canonical
                    terms=sp.Add.make_args(sp.expand(primitive))
                    for evaluated,endpoint in ((m[1],hi),(m[2],lo)):
                        first,second=evaluated.split(r'-\frac',1)
                        displayed=[scale*parse(first),scale*parse(r'-\frac'+second)]
                        assert len(terms)==2
                        assert all(sum(eq(v,e.subs(t,endpoint)) for e in terms)==1 for v in displayed)
                        checked+=2
                else:raise AssertionError('Unexpected source endpoint layout')
            check(scale*parse(canonical),answer,'endpoint/final row '+str(n))
    expected={'q-162230':['dot scalar row 2'],
              'q-162235':['dot scalar row 1','dot scalar row 2','integrand row 1','primitive derivative']}.get(sid,[])
    assert failed==expected,(sid,failed,expected)
    return {'source_id':sid,'force_scale':1 if record is None else record['generation']['parameters']['force_scale'],'checked_components':checked,'failed_stages':failed,'eligible_for_learning':False}

def native_case(r,label):
    f=r['question'][':question/answer-fields'][0]
    return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],
       'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected',
       'purpose':'native owned radio choice; mathematical value checked independently'} for a in f[':answer-field/choices']]}

def main():
    sourcecases=[];reviews=[];native=[];fidelity=[];source_audits=[]
    for local,captured in (('source.json','sources/17592186133926.json'),('topic.json','topics/17592186049762.json'),('lesson.json','lessons/17592186049762.json')):
        assert (HERE/local).read_bytes()==(ROOT/'generate/runs/current'/captured).read_bytes(),local
    assert g.SOURCE['database']=='math' and g.SOURCE['basis']==1356
    for sid,orig in g.ORIGINALS.items():
        template=g.SOURCE_TEMPLATE[sid];level=g.TEMPLATES[template][0]
        sourcecases.append({'source_id':sid,'source_db_id':orig[':db/id'],'template':template,
          'level':level,'parameters':{'force_scale':1},'bank_profile':'raw:'+sid,
          'original_level':g.enum(orig[':question/difficulty']) if ':question/difficulty' in orig else None})
        r=g.generate(level,seed=7,template=template,parameters={'force_scale':1},profile='raw:'+sid);q=r['question']
        assert g.generate(level,seed=103,template=template,parameters={'force_scale':1},profile='raw:'+sid)['question'][':question/id']==q[':question/id']
        for k in (':question/problem',':question/worked-solution',':question/difficulty',':question/math-academy-id',':question/answer-fields'):
            assert (k in q)==(k in orig),(sid,k)
        assert q[':question/problem']==orig[':question/problem']
        assert q.get(':question/worked-solution')==orig.get(':question/worked-solution')
        f=q[':question/answer-fields'][0];of=orig[':question/answer-fields'][0]
        for k in (':answer-field/choices',':answer-field/correct',':answer-field/key',':answer-field/type'):assert (k in f)==(k in of)
        assert f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==g.enum(of[':answer-field/type'])
        ov=[a[':answer/value'] for a in of[':answer-field/choices']]
        gv=[a[':answer/value'] for a in f[':answer-field/choices']]
        assert sorted(ov)==sorted(gv)
        answer=original_math(sid)
        source_audits.append(audit_source(sid))
        assert sum(eq(parse(v),answer) for v in ov)==1
        if ':answer-field/correct' in of:
            correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
            assert correct==of[':answer-field/correct'][':answer/value'] and eq(parse(correct),answer)
            native.append(native_case(r,'original:'+sid))
        reviews.append(r)
        for c in (2,-2):
            variant=g.generate(level,template=template,parameters={'force_scale':c},profile='raw:'+sid)
            assert variant['question'][':question/id']!=q[':question/id']
            source_audits.append(audit_source(sid,variant))
            vq=variant['question'];vf=vq[':question/answer-fields'][0]
            assert str(c)+r'\left(' in vq[':question/problem']
            assert all(sum(eq(parse(a[':answer/value']),c*parse(v)) for v in ov)==1 for a in vf[':answer-field/choices'])
            assert (':answer-field/correct' in vf)==(':answer-field/correct' in of)
            if ':question/worked-solution' in q:
                src=rows(q[':question/worked-solution']);changed=rows(vq[':question/worked-solution'])
                assert list(map(len,src))==list(map(len,changed))
                for blockindex in (0,2,3):
                    for rowindex,(before,after) in enumerate(zip(src[blockindex],changed[blockindex])):
                        if blockindex==3 and rowindex==0:assert before==after
                        else:assert after==g.scale_rhs(before,c)
                assert changed[1]==src[1]
            reviews.append(variant)
        fidelity.append({'source_id':sid,'prompt_raw_exact':True,'solution_raw_exact_or_absent':True,
                        'choices_matched':5,'choices_total':5,'designation_matched':':answer-field/correct' in of,
                        'original_answer':g.tex(answer),'missing_correct_preserved':':answer-field/correct' not in of})
    allrecords=[];counts={};fingerprints=set();identitychecks=0
    for template,(level,_) in g.TEMPLATES.items():
        counts[template]=len(g.domains(template))
        for i,p in enumerate(g.domains(template)):
            r=g.generate(level,seed=i,template=template,parameters=p);normal(r);allrecords.append(r)
            fp=r['generation']['mathematical_fingerprint'];assert fp not in fingerprints;fingerprints.add(fp)
            other=g.generate(level,seed=i+700,template=template,parameters=p)
            assert other['question'][':question/id']==r['question'][':question/id']
            assert other['generation']['content_identity']==r['generation']['content_identity'];identitychecks+=1
            native.append(native_case(r,'generated:'+template+':'+str(p)))
        # Two variants for EVERY normal family, in addition to two per raw mask.
        for p in (g.domains(template)[-1],g.domains(template)[len(g.domains(template))//2]):
            reviews.append(g.generate(level,seed=9,template=template,parameters=p))
    # Level guards must apply equally to explicit calls; no aliases/common scales.
    for level in ('easy','moderate','hard'):
        try:g.generate(level,parameters={'a':2,'b':2,**({'sign':1} if level=='easy' else {})})
        except ValueError:pass
        else:raise AssertionError('Common scale alias allowed')
        try:g.generate(level,parameters={'a':7,'b':1,**({'sign':1} if level=='easy' else {})})
        except ValueError:pass
        else:raise AssertionError('Explicit arithmetic bound bypass')
    familycoverage={level:sorted({g.generate(level,seed=n)['generation']['template'] for n in range(25)}) for level in ('easy','moderate','hard')}
    for level,seen in familycoverage.items():assert seen==sorted(k for k,(l,_) in g.TEMPLATES.items() if l==level)
    positions={next(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices'])
                    if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1]) for r in allrecords}
    assert positions==set(range(5)),positions
    (HERE/'source-cases.json').write_text(json.dumps(sourcecases,indent=2)+'\n')
    (HERE/'review.json').write_text(json.dumps(reviews,indent=2,ensure_ascii=False)+'\n')
    (HERE/'review.md').write_text('# Circulation over space curves — author review\n\nOriginal profiles preserve captured anomalies and are evidence only. Generated normal records are authored, with actual difficulty and correct choice labels. Raw q-162238 stays unrated and lacks an original correct key/solution. Independent inferred value: $-1/60$.\n\n'+'\n\n---\n\n'.join(map(g.markdown,reviews))+'\n')
    (HERE/'native-input.json').write_text(json.dumps(native,indent=2,ensure_ascii=False)+'\n')
    engine=ROOT/'generate/runs/current/check-engine'
    subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-results.json')],check=True)
    result={'pass':True,'basis':1356,'normal_math_instances':len(allrecords),'normal_displayed_stage_checks':'all prompt components, formal definitions, F substitution, formal coordinate derivatives, products, integrand, primitive, each endpoint term and final equation',
            'meaningful_domain_counts':counts,'default_family_coverage':familycoverage,
            'source_fidelity':{'sources':8,'prompt_exact':8,'solution_exact':7,'solution_absent_preserved':1,'complete_banks':8,'choice_values':40,'correct_designations_matched':7,'correct_designations_absent_preserved':1},
            'raw_math_findings':[
              {'source_id':'q-162230','status':'expected raw error; ineligible','detail':'cos^2(pi t) must be cos^2(t) in the first reduced product row'},
              {'source_id':'q-162235','status':'expected raw error; ineligible','detail':'negative z term becomes positive in scalar product; reduced sine and primitive signs are consequently wrong although zero circulation remains correct'},
              {'source_id':'q-162238','status':'missing original key/solution/unrated preserved','inferred_value':'-1/60','authored_level':'hard'}],
            'opaque_banks':8,'raw_eligible':False,'native':json.loads((HERE/'native-results.json').read_text()),
            'content_identity_checks':identitychecks,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},
            'frozen_hashes':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ('source.json','topic.json','lesson.json')},
            'runtime_hashes':{'generator':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'validator':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'native_engine':hashlib.sha256(engine.read_bytes()).hexdigest(),'native_engine_source':hashlib.sha256(engine.with_suffix('.rs').read_bytes()).hexdigest()},
            'fidelity_by_source':fidelity,'independent_source_stage_audits':source_audits,'plots':'none','database_writes':0,'stopped_at_step':7}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k in ('pass','normal_math_instances','meaningful_domain_counts','source_fidelity')},indent=2))

if __name__=='__main__':main()
