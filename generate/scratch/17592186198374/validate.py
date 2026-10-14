#!/usr/bin/env python3
"""Read actual learner math, test all stages/operands and native radio grading."""
import copy,hashlib,importlib.util,json,re,subprocess,sys,concurrent.futures
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('integrand_kp',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,u,v=g.x,g.y,g.u,g.v

def write(name,value):(D/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def eq(a,b):
    delta=s.simplify(a-b)
    assert delta==0 or delta.equals(0),(a,b,delta)
def balanced(t):
    assert not any(ord(c)<32 and c not in '\n\t' for c in t),'C0 control character'
    assert t.count('$')%2==0,'math delimiters'
    depth=0
    for i,c in enumerate(t):
        if c in '{}':
            n=0;j=i-1
            while j>=0 and t[j]=='\\':n+=1;j-=1
            if n%2:continue
            depth+=(1 if c=='{' else -1);assert depth>=0,'TeX closing group'
    assert depth==0,'TeX group depth'
    assert '+-' not in t and '--' not in t,'ungrouped signed components'
def group(t,i):
    assert t[i]=='{',(t,i);d=1;j=i+1
    while d:
        assert j<len(t),(t,'unclosed group');d+=(1 if t[j]=='{' else -1 if t[j]=='}' else 0);j+=1
    return t[i+1:j-1],j

def math(t):
    t=t.strip().replace('\u2061','').replace('\xa0','')
    for st in (r'\left',r'\right',r'\,',r'\:',r'\quad',r'\text{ }'):t=t.replace(st,'')
    for fn in ('sin','cos','ln'):t=t.replace(r'\operatorname{'+fn+'}','\\'+fn)
    def expand(t):
        out='';i=0
        while i<len(t):
            m=re.match(r'\\(d?frac|sqrt)',t[i:])
            if not m:out+=t[i];i+=1;continue
            j=i+len(m[0]);a,j=group(t,j)
            if m[1]=='sqrt':out+='sqrt('+expand(a)+')'
            else:b,j=group(t,j);out+='(('+expand(a)+')/('+expand(b)+'))'
            i=j
        return out
    t=expand(t.rstrip('.,')).replace(r'\cdot','*').replace(r'\pi','pi')
    t=re.sub(r'\|([^|]+)\|',r'Abs(\1)',t)
    for a,b in ((r'\sin','sin'),(r'\cos','cos'),(r'\ln','log')):t=t.replace(a,b)
    t=t.replace('{','(').replace('}',')').replace('[','(').replace(']',')').replace('^','**')
    t=re.sub(r'(?<![A-Za-z])e(?![A-Za-z])','E',t)
    t=re.sub(r'(sin|cos|log)\s*([uv]|[0-9]+)(?![a-zA-Z])',r'\1(\2)',t)
    assert '\\' not in t,('unsupported TeX',t)
    return parse_expr(t,local_dict=dict(x=x,y=y,u=u,v=v,pi=s.pi,E=s.E,sqrt=s.sqrt,Abs=s.Abs,sin=s.sin,cos=s.cos,log=s.log),transformations=standard_transformations+(implicit_multiplication_application,))

def calculus(t,ctx):
    t=t.replace(r'\left','').replace(r'\right','')
    t=t.replace(r'|\frac{\partial(x,y)}{\partial(u,v)}|',g.tex(ctx['J']))
    if t.startswith(r'\iint_D '):
        f=math(t[len(r'\iint_D '):].split(r'\mathrm{d}x')[0].rstrip('\\,'))
        expr=s.simplify(f.subs({x:ctx['X'],y:ctx['Y']},simultaneous=True)*ctx['J'])
        return s.integrate(expr,(u,ctx['a0'],ctx['a1']),(v,ctx['b0'],ctx['b1']))
    if t.startswith(r'\iint_\Delta '):
        f=math(t[len(r'\iint_\Delta '):].split(r'\mathrm{d}u')[0].rstrip('\\,'))
        return s.integrate(f,(u,ctx['a0'],ctx['a1']),(v,ctx['b0'],ctx['b1']))
    for _ in range(40):
        pos=t.rfind(r'\int_')
        if pos>=0:
            lo,i=group(t,pos+len(r'\int_'));assert t[i]=='^';hi,j=group(t,i+1)
            close=re.search(r'\\mathrm\{d\}([uv])',t[j:]);assert close,(t,'integral differential')
            end=j+close.end();body=t[j:j+close.start()];var={'u':u,'v':v}[close[1]]
            value=s.integrate(calculus(body,ctx),(var,math(lo),math(hi)))
            t=t[:pos]+'('+g.tex(value)+')'+t[end:];continue
        candidates=list(re.finditer(r'\[([^\[\]]*)\]_\{',t))
        if candidates:
            m=candidates[-1];lo,i=group(t,m.end()-1);assert t[i]=='^';hi,j=group(t,i+1)
            expr=math(m[1]);vs=expr.free_symbols & {u,v};assert len(vs)==1,(expr,'primitive variable');var=vs.pop()
            value=expr.subs(var,math(hi))-expr.subs(var,math(lo));t=t[:m.start()]+'('+g.tex(value)+')'+t[j:];continue
        return math(t)
    raise AssertionError('calculus recursion ceiling')

def read_context(r):
    q=r['question'];prob=q[':question/problem'];sol=q[':question/worked-solution']
    F=math(re.search(r'\\iint_D (.*?)\\,\\mathrm\{d\}x',prob,re.S)[1])
    transform=re.search(r'\$\$\nu=(.*?),\\qquad v=(.*?)\.\n\$\$',sol,re.S);assert transform
    U,V=math(transform[1]),math(transform[2]);M=s.Matrix([[s.diff(U,x),s.diff(U,y)],[s.diff(V,x),s.diff(V,y)]]);det=M.det();assert det!=0
    inv=s.solve([U-u,V-v],[x,y]);X,Y=inv[x],inv[y];eq(U.subs(inv,simultaneous=True),u);eq(V.subs(inv,simultaneous=True),v)
    inverse=re.search(r'\$\$\nx=(.*?),\\qquad y=(.*?)\.\n\$\$',sol,re.S);assert inverse;eq(math(inverse[1]),X);eq(math(inverse[2]),Y)
    rect=re.search(r'\\Delta=\\\{\(u,v\):(.*?)\\le u\\le (.*?),\\ (.*?)\\le v\\le (.*?)\\\}',sol);assert rect
    a0,a1,b0,b1=[math(t) for t in rect.groups()];assert a1>a0 and b1>b0
    pts=re.findall(r'\$\((.*?),(.*?)\)\$',prob);assert len(pts)==4
    mapped=[(s.simplify(U.subs({x:math(A),y:math(B)})),s.simplify(V.subs({x:math(A),y:math(B)}))) for A,B in pts]
    expected=[(a0,b0),(a1,b0),(a1,b1),(a0,b1)];assert mapped==expected,(mapped,expected)
    transformed=s.simplify(F.subs(inv,simultaneous=True));J=abs(1/det);ans=s.integrate(transformed*J,(u,a0,a1),(v,b0,b1));ans=s.simplify(ans)
    block3=sol.split('**Step 3**')[1].split('**Step 4**')[0];numeric=re.findall(r'&=\\begin\{vmatrix\}(.*?)&(.*?)\\\\(.*?)&(.*?)\\end\{vmatrix\}',block3)[-1];numeric=(None,*numeric);assert numeric
    actual=s.Matrix([[math(numeric[1]),math(numeric[2])],[math(numeric[3]),math(numeric[4])]]);assert M==actual
    jac=re.search(r'&=(.*?)\.\\end\{aligned\}',block3);assert jac;eq(math(jac[1]),det)
    block4=sol.split('**Step 4**')[1].split('Note that')[0];eq(math(block4.split('^{-1}=')[1].split('$$')[0]),1/det)
    return dict(F=F,U=U,V=V,M=M,det=det,J=J,X=X,Y=Y,a0=a0,a1=a1,b0=b0,b1=b1,answer=ans,transformed=transformed)

def check_normal(r):
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    assert r['generation']['eligible_for_learning'] and not r['generation']['evidence_only']
    q=r['question']
    for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]:balanced(text)
    ctx=read_context(r);sol=q[':question/worked-solution'];chain=sol.rsplit(r'\begin{aligned}',1)[1].split(r'\end{aligned}')[0];rows=chain.split(r' \\ ')
    family=r['generation']['template'];expected_rows=10+(family=='cosine_square')+(family=='rational' and g.parse(r['generation']['parameters']['scale'])*ctx['J']==1)
    assert len(rows)==expected_rows,('operative stage count',family,len(rows),expected_rows)
    for row in rows:
        sides=row.split('&=');assert len(sides)==2,(row,'equality stage')
        if sides[0]:eq(calculus(sides[0],ctx),ctx['answer'])
        eq(calculus(sides[1],ctx),ctx['answer'])
    # Required operations, independent of algebraic equality.
    assert r'\iint_\Delta ' in rows[0 if family!='cosine_square' else 1]
    assert '|'+g.tex(1/ctx['det'])+'|' in rows[1 if family!='cosine_square' else 2].replace(r'\left','').replace(r'\right','')
    assert rows[-7].count(r'\int_')==2,'nested integral stage'
    assert rows[-6].count(r'\int_')==2 and r'\cdot ' in rows[-6],'separated factors stage'
    primitive_row=rows[-5];brackets=re.findall(r'\\left\[(.*?)\\right\]_\{(.*?)\}\^\{(.*?)\}',primitive_row);assert len(brackets)==2
    primitives={}
    for expr,lo,hi in brackets:
        P=math(expr);vars=P.free_symbols & {u,v};assert len(vars)==1;var=vars.pop();primitives[str(var)]=(P,math(lo),math(hi))
    fu=s.diff(primitives['u'][0],u);fv=s.diff(primitives['v'][0],v);scale=g.parse(r['generation']['parameters']['scale']);eq(scale*fu*fv,ctx['transformed'])
    # Reversed endpoints shared errors cannot hide in final equality.
    ev_matches=re.findall(r'\\left\(\\left\((.*?)\\right\)-\\left\((.*?)\\right\)\\right\)',rows[-3]);assert len(ev_matches)==2,(rows[-3],ev_matches)
    order=['u','v'] if family=='rational' else ['v','u']
    for (hi_value,lo_value),name in zip(ev_matches,order):
        P,lo,hi=primitives[name];var=u if name=='u' else v;eq(math(hi_value),P.subs(var,hi));eq(math(lo_value),P.subs(var,lo))
    assert r'^{2}' in rows[-4] or family=='rational','substitution operation must remain visible'
    fields=q[':question/answer-fields'];assert len(fields)==1;f=fields[0];choices=f[':answer-field/choices'];assert len(choices)==5
    values=[math(a[':answer/value']) for a in choices];assert len({a[':answer/id'] for a in choices})==5
    for i,val in enumerate(values):
        for oth in values[:i]:assert not g.eq(val,oth) and abs(float(s.N(val-oth,18)))>1e-12
    correct=[a for a in choices if a[':answer/id']==f[':answer-field/correct'][1]];assert len(correct)==1;eq(math(correct[0][':answer/value']),ctx['answer']);eq(g.parse(r['generation']['answer_exact']),ctx['answer'])
    # Regenerate complete chosen profile independently from printed transform/bounds.
    p={'matrix':list(ctx['M']),'shift':[s.simplify(ctx['U']-ctx['M'][0,0]*x-ctx['M'][0,1]*y),s.simplify(ctx['V']-ctx['M'][1,0]*x-ctx['M'][1,1]*y)],'bounds':[ctx['a0'],ctx['a1'],ctx['b0'],ctx['b1']],'scale':scale}
    z=g.components(family,p);bank,_=g.bank(family,p,z)
    for val in values:assert sum(g.eq(val,b) for b in bank)==1
    plot=Path(r['generation']['plot']);assert plot.exists();sidecar=json.loads(plot.with_suffix('.json').read_text());assert sidecar['bounds']==[str(t) for t in p['bounds']];assert sidecar['image_sha256']==hashlib.sha256(plot.read_bytes()).hexdigest()
    return ctx


def check_raw(r,source):
    q=r['question'];assert not r['generation']['eligible_for_learning'] and r['generation']['evidence_only']
    for k in [':question/difficulty',':question/worked-solution',':question/answer-fields']:assert (k in q)==(k in source),(k,'attribute parity')
    assert q[':question/problem']==source[':question/problem'];assert q.get(':question/worked-solution')==source.get(':question/worked-solution')
    pairs=list(zip(q.get(':question/answer-fields',[]),source.get(':question/answer-fields',[])));assert len(pairs)==len(source.get(':question/answer-fields',[]))
    for f,orig in pairs:
        assert f[':answer-field/type']==g.enum(orig[':answer-field/type']);assert f[':answer-field/key']==orig[':answer-field/key']
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in orig[':answer-field/choices'])
        assert (':answer-field/correct' in f)==(':answer-field/correct' in orig)
        if ':answer-field/correct' in f:
            chosen=[a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]];assert len(chosen)==1;assert chosen[0][':answer/value']==orig[':answer-field/correct'][':answer/value']


def expect_failure(fn):
    try:fn()
    except (AssertionError,ValueError):return
    raise AssertionError('negative regression was accepted')

def run():
    cases=[];raw=[];counts=dict(questions=0,fields=0,options=0,designations=0,missing_correct=0,solution_exact=0,unrated=0)
    for sid,source in g.SOURCES.items():
        level=g.FAMILIES[g.SOURCE_FAMILY[sid]];case=dict(source_id=sid,template=g.SOURCE_FAMILY[sid],parameters={'scale':1},bank_profile='raw:'+sid,level=level,authored_level=':question/difficulty' not in source)
        cases.append(case);r=g.generate(level,profile=case['bank_profile'],parameters=case['parameters']);check_raw(r,source);raw.append(r)
        counts['questions']+=1;counts['fields']+=len(source.get(':question/answer-fields',[]));counts['options']+=sum(len(f[':answer-field/choices']) for f in source.get(':question/answer-fields',[]));counts['designations']+=sum(':answer-field/correct' in f for f in source.get(':question/answer-fields',[]));counts['missing_correct']+=sum(':answer-field/correct' not in f for f in source.get(':question/answer-fields',[]));counts['solution_exact']+=(':question/worked-solution' in source);counts['unrated']+=(':question/difficulty' not in source)
        scaled=g.generate(level,profile=case['bank_profile'],parameters={'scale':2});assert scaled['question'][':question/problem']!=r['question'][':question/problem'];assert scaled['generation']['answer_exact']!=r['generation']['answer_exact']
    write('source-cases.json',cases)
    records=[];fingerprints={lev:set() for lev in ['easy','moderate','hard']};family_counts={f:0 for f in g.FAMILIES}
    for family,level in g.FAMILIES.items():
        for seed in range(12):
            r=g.generate(level,seed,template=family);check_normal(r);family_counts[family]+=1;fingerprints[level].add(r['generation']['mathematical_fingerprint'])
            if seed<2:records.append(r)
        p=g.ANCHORS[family];r=g.generate(level,31,template=family,parameters=p);check_normal(r);records.append(r)
        r2=g.generate(level,999,template=family,parameters=p);assert r['question'][':question/id']==r2['question'][':question/id'];assert r['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint']
        for field_type in ['radio',':answer-field.type/radio']:check_normal(g.generate(level,3,template=family,field_type=field_type))
        expect_failure(lambda:g.generate(level,template=family,field_type='blank'))
    defaults=set(g.generate('hard',k)['generation']['template'] for k in range(40));assert defaults=={f for f,l in g.FAMILIES.items() if l=='hard'}
    # Display mutations: operand corruption at both endpoints leaves difference unchanged.
    r=copy.deepcopy(records[0]);r['question'][':question/worked-solution']+='\f';expect_failure(lambda:check_normal(r))
    r=copy.deepcopy(records[0]);text=r['question'][':question/worked-solution'];chain=text.rsplit(r'\begin{aligned}',1)[1].split(r'\end{aligned}')[0];rows=chain.split(r' \\ ');rows[-4]=rows[-3];r['question'][':question/worked-solution']=text.replace(chain,r' \\ '.join(rows));expect_failure(lambda:check_normal(r))
    r=copy.deepcopy(records[0]);text=r['question'][':question/worked-solution'];chain=text.rsplit(r'\begin{aligned}',1)[1].split(r'\end{aligned}')[0];rows=chain.split(r' \\ ');rows[-3]=re.sub(r'\\left\((.*?)\\right\)',lambda m:r'\left('+m[1]+'+1'+r'\right)',rows[-3]);r['question'][':question/worked-solution']=text.replace(chain,r' \\ '.join(rows));expect_failure(lambda:check_normal(r))
    expect_failure(lambda:g.generate_moderate(parameters=dict(matrix=[2,0,1,1],shift=[0,0],bounds=[1,3,1,4])))
    expect_failure(lambda:g.generate_hard(template='rational',parameters=dict(matrix=[1,1,2,1],shift=[0,0],bounds=[1,2,0,2])))
    # Same and different renderer instances concurrently: assets + sidecars consistent.
    inputs=[g.canonical_parameters(g.ANCHORS['polynomial']),g.canonical_parameters(g.ANCHORS['sine'])]*2
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:paths=list(pool.map(g.rectangle_plot,inputs))
    assert paths[0]==paths[2] and paths[1]==paths[3] and paths[0]!=paths[1]
    engine=[]
    for i,r in enumerate(records):
        f=r['question'][':question/answer-fields'][0];checks=[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete radio bank selected-ID grading'} for a in f[':answer-field/choices']]
        engine.append({'label':str(i),'record':r,'checks':checks})
    for r in raw:
        if any(':answer-field/correct' not in f for f in r['question'][':question/answer-fields']):continue
        f=r['question'][':question/answer-fields'][0];checks=[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'faithful original bank radio grading'} for a in f[':answer-field/choices']]
        engine.append({'label':r['generation']['source_id'],'record':r,'checks':checks})
    write('engine-input.json',engine);subprocess.run([str(g.ROOT.parent/'runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
    er=json.loads((D/'engine-report.json').read_text())
    write('review.json',records)
    review=['# Inferred-from-integrand source and generated review\n\nFrozen math basis1356. Raw sources are evidence-only, opaque banks. Normal banks are authored method-derived complete profiles.\n']
    for r in raw:review+=['\n## Original raw '+r['generation']['source_id']+'\n',g.markdown(r)]
    for r in records:review+=['\n## Generated '+r['generation']['difficulty']+' / '+r['generation']['template']+'\n',g.markdown(r)]
    (D/'review.md').write_text('\n'.join(review))
    report={'status':'passed with documented ineligible raw evidence','source_provenance':{k:g.SOURCE[k] for k in ['database','basis','lineage']},'source_fidelity':counts,'raw_bank_options_matched':counts['options'],'normal_checked_by_family':family_counts,'unique_sampled_mathematical_tasks':{lev:len(val) for lev,val in fingerprints.items()},'native':{k:er[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']},'native_raw_unsupported_fields_missing_correct':2,'native_raw_unchecked_records_due_missing_correct':2,'raw_normal_solution_exact_separated':{'raw_exact_existing':5,'normal_exact':0,'normal_shared_prose_and_required_operations':True,'normal_additions':['explicit inverse equations','individual endpoint substitution and signed evaluation rows'],'presentation_normalization':'balanced literal domain brace; standard LaTeX operators; remove stray differential after completed primitive product'},'authored_extensions':['easy canonical polynomial family','moderate shifted polynomial completion and level assignment','all normal whole method banks'],'regressions':['control character','same-equality primitive substitution removal','correlated endpoint corruption','moderate unshifted scope escape','rational zero denominator','enum/nonenum field selector','identity/order','default hard family coverage','concurrent render sidecars'],'runtime':records[0]['generation']['runtime'],'database_writes':0,'unresolved':['historical scalar distractor intention opaque; raw banks remain public evidence-only','missing original correct designation on unrated source and legacy duplicate: never counted matched']}
    write('validation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':run()
