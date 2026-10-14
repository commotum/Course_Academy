#!/usr/bin/env python3
"""Read displayed mathematics independently; exact source fidelity and native grader."""
import concurrent.futures, copy, hashlib, importlib.util, itertools, json, os, re, subprocess, sys
from pathlib import Path
import sympy as S
from PIL import Image
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('given_area',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def group(text,start):
    assert text[start]=='{'
    depth=1;i=start+1
    while depth:
        if text[i]=='{':depth+=1
        if text[i]=='}':depth-=1
        i+=1
    return text[start+1:i-1],i

def parse(text):
    """Restricted independent parser for the displayed rational/power/log grammar."""
    text=text.strip().rstrip('.').replace('⁡','').replace(r'\operatorname{ln}',r'\ln')
    for z in (r'\left',r'\right',r'\,',r'\!',r'\ '):text=text.replace(z,'')
    text=text.replace(r'\cdot','*')
    while r'\frac' in text:
        i=text.rfind(r'\frac');a,e=group(text,i+5);b,f=group(text,e)
        text=text[:i]+'(('+str(parse(a))+')/('+str(parse(b))+'))'+text[f:]
    while r'\ln' in text:
        i=text.index(r'\ln');start=i+3
        while start<len(text) and text[start].isspace():start+=1
        if text[start]=='{':a,e=group(text,start)
        else:
            m=re.match(r'[0-9]+|[a-z]',text[start:]);assert m,text;a=m.group();e=start+len(a)
        text=text[:i]+'log('+str(parse(a))+')'+text[e:]
    text=text.replace('{','(').replace('}',')')
    assert '\\' not in text,text
    return parse_expr(text,local_dict={'x':g.x,'y':g.y,'u':g.u,'v':g.v,'log':S.log},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))

def equal(a,b):return S.simplify(S.expand_log(a-b,force=True))==0

def format_check(text):
    assert not any(ord(c)<32 and c not in '\n\t' for c in text),'C0 character'
    assert text.count('$$')%2==0
    rest=text.replace('$$','');assert rest.count('$')%2==0
    depth=0
    for i,c in enumerate(text):
        if c in '{}' and (i==0 or text[i-1]!='\\'):
            depth+=1 if c=='{' else -1
            assert depth>=0
    assert depth==0
    assert '--' not in text and '+-' not in text

def read_prompt(q):
    text=q[':question/problem'];blocks=re.findall(r'\$\$(.*?)\$\$',text,re.S)
    assert len(blocks)==2
    m=re.fullmatch(r'\s*u=(.*?),\\qquad v=(.*?),\s*',blocks[0],re.S);assert m
    U,V=[parse(z) for z in m.groups()]
    borders=blocks[1].strip().rstrip('.').split(r',\qquad ')
    assert len(borders)==4
    curves=[parse(z.split('=',1)[1]) for z in borders]
    vals=[S.simplify(U.subs(g.y,z)) for z in curves[:2]]+[S.simplify(V.subs(g.y,z)) for z in curves[2:]]
    assert all(z.is_number for z in vals)
    L,H,j,k=vals;assert L<H and 0<j<k
    return U,V,curves,(L,H,j,k)

def check_raw_parameterization(r):
    q=r['question'];text=q[':question/problem']
    blocks=re.findall(r'\$\$(.*?)\$\$',text,re.S)
    if not blocks:blocks=re.findall(r'\$(.*?)\$',text,re.S)
    defs=blocks[0].strip().rstrip(',').replace(r'\,','')
    m=re.fullmatch(r'\s*u\s*=\s*(.*?),\s*v\s*=\s*(.*?)\s*',defs,re.S);assert m
    U,V=[parse(z) for z in m.groups()]
    boundary=blocks[-1].strip().rstrip('.')
    curves=[parse(z.split('=',1)[1]) for z in re.split(r',\s*(?:\\,)?\s*',boundary)]
    assert len(curves)==4
    vals=[S.simplify(U.subs(g.y,z)) for z in curves[:2]]+[S.simplify(V.subs(g.y,z)) for z in curves[2:]]
    L,H,j,k=vals
    jac=S.det(S.Matrix([[S.diff(U,g.x),S.diff(U,g.y)],[S.diff(V,g.x),S.diff(V,g.y)]]))
    f=q[':question/answer-fields'][0];bank=[parse(z[':answer/value']) for z in f[':answer-field/choices']]
    assert all(not equal(a,b) for a,b in itertools.combinations(bank,2))
    template=r['generation']['template']
    if template.startswith('linear'):A=(H-L)*(k-j)/abs(jac)
    else:
        J=-1/(3*g.u) if template=='quotient' else 1/(g.u**2*g.v)
        assert equal(J.subs({g.u:U,g.v:V},simultaneous=True)*jac,(-1 if template=='quotient' else 1)*(-1 if template=='quotient' else 1))
        A=S.integrate(S.integrate(abs(J),(g.v,j,k)),(g.u,L,H))
    assert sum(equal(z,A) for z in bank)==1
    if ':question/worked-solution' in q:
        solution=q[':question/worked-solution'];math=re.findall(r'\$\$(.*?)\$\$',solution,re.S)
        for index,bounds,var in [(5,[L,H],'u'),(6,[j,k],'v')]:
            targets=re.findall(r'& '+var+r'=(-?\d+)',math[index]);assert list(map(S.Integer,targets))==bounds
        final=math[10].split(r' & =')[-1].replace(r'\end{aligned}','').strip().rstrip('.')
        assert equal(parse(final),A)
    return str(A)

def check_record(r):
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    q=r['question'];f=q[':question/answer-fields'][0]
    assert f[':answer-field/type']==':answer-field.type/radio';assert len(f[':answer-field/choices'])==5
    assert f[':answer-field/key']=='selection'
    for a in f[':answer-field/choices']:assert a[':answer/type']==':answer.type/math'
    assert len({a[':answer/id'] for a in f[':answer-field/choices']})==5
    for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for a in f[':answer-field/choices']]:format_check(text)
    U,V,curves,(L,H,j,k)=read_prompt(q)
    jac=S.det(S.Matrix([[S.diff(U,g.x),S.diff(U,g.y)],[S.diff(V,g.x),S.diff(V,g.y)]]))
    blocks=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S)
    assert len(blocks)==11
    assert equal(parse(blocks[3].strip().split(r',\,')[0].split('=',1)[1]),U)
    assert equal(parse(blocks[3].strip().split(r',\,')[1].split('=',1)[1]),V)
    for B,transform,boundaries,values,var in [(blocks[5],U,curves[:2],[L,H],'u'),(blocks[6],V,curves[2:],[j,k],'v')]:
        rows=B.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r' \\ ')
        assert len(rows)==2
        for row,curve,value in zip(rows,boundaries,values):
            eqs=row.split('&')[1::2]
            assert len(eqs)==3
            assert equal(parse(eqs[0].split('=',1)[1]),curve)
            lhs,rhs=eqs[1].replace('⟹','').replace(r'\,','').split('=',1)
            assert equal(parse(lhs),transform);assert equal(parse(rhs),value)
            assert equal(parse(eqs[2].split('=',1)[1]),value)
    bounds=re.search(r'(-?\d+)\\le u\\le (-?\d+),\\,(\d+)\\le v\\le (\d+)',blocks[7]);assert bounds
    assert tuple(map(S.Integer,bounds.groups()))==(L,H,j,k)
    # Second displayed matrix must be the derivatives of the ACTUAL prompt.
    matrices=re.findall(r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|',blocks[8],re.S)
    assert len(matrices)==2
    assert matrices[0]==r'\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}'
    entries=re.split(r' & | \\\\ ',matrices[1]);assert len(entries)==4
    expected=[S.diff(U,g.x),S.diff(U,g.y),S.diff(V,g.x),S.diff(V,g.y)]
    assert all(equal(parse(a),b) for a,b in zip(entries,expected))
    finaljac=blocks[8].split(r' & =')[-1].replace(r'\end{aligned}','').strip().rstrip('.')
    assert equal(parse(finaljac),jac)
    stages=blocks[9].strip().rstrip('.').split('=')[2:]
    assert len(stages)>=2
    for stage in stages:
        value=parse(stage).subs({g.u:U,g.v:V},simultaneous=True)
        assert equal(value*jac,S.Integer(1)),stage
    if r['generation']['template'].startswith('reciprocal'):
        assert len(stages)==3,'Source cancellation stage missing'
        assert r'x^{2} y^{2}' in stages[1],'Unevaluated numerator cancellation mask missing'
    J=parse(stages[-1])
    A=S.integrate(S.integrate(abs(J),(g.v,j,k)),(g.u,L,H))
    values=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
    assert all(not equal(a,b) for a,b in itertools.combinations(values,2)),'Equivalent pair in whole bank'
    correct=[a for a,z in zip(f[':answer-field/choices'],values) if equal(z,A)]
    assert len(correct)==1 and correct[0][':answer/id']==f[':answer-field/correct'][1]
    # Integral stages and endpoint arithmetic read from actual displayed output.
    rows=blocks[10].split(r' \\  & =')
    assert len(rows)==6
    first_abs=re.search(r'\|(.*?)\|',rows[1]);assert first_abs
    assert equal(abs(parse(first_abs.group(1))),abs(J))
    assert equal(parse(rows[-1].replace(r'\end{aligned}','').strip().rstrip('.')),A)
    assert equal(parse(rows[-2]),A),'Printed endpoint/product row wrong'
    if r['generation']['template'].startswith('linear'):
        assert equal(parse(rows[2].split('{∬}')[0]),abs(J))
        assert equal(parse(rows[3].split(r'\cdot')[0]),abs(J))
        assert r'\text{Area}(Δ)' in rows[3]
    else:
        m=re.fullmatch(r'\\int_\{(-?\d+)\}\^\{(-?\d+)\}\\int_\{(\d+)\}\^\{(\d+)\}(.*?)\\,\\mathrm d v\\,\\mathrm d u',rows[2]);assert m
        assert tuple(map(S.Integer,m.groups()[:4]))==(L,H,j,k)
        assert equal(parse(m.group(5)),abs(J))
        m=re.fullmatch(r'(.*?)\\int_\{(-?\d+)\}\^\{(-?\d+)\}(.*?)\\,\\mathrm d u\\int_\{(\d+)\}\^\{(\d+)\}(.*?)\\,\\mathrm d v',rows[3]);assert m
        C,a,b,fu,c,d,fv=m.groups();assert tuple(map(S.Integer,[a,b,c,d]))==(L,H,j,k)
        assert equal((parse(C) if C else 1)*parse(fu)*parse(fv),abs(J))
    return str(A)

def fixture(r,label):
    f=r['question'][':question/answer-fields'][0]
    return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'whole owned bank choice'} for a in f[':answer-field/choices']]}

def check_plot(path,data):
    # Independent transcription: the source's dashed strokes are external
    # guides, not any of the four region boundary inclusion predicates.
    assert data['edge_inclusion']==dict(left=True,right=True,bottom=True,top=True)
    assert data['edge_strokes']==dict(left='fill-only',right='fill-only',bottom='solid',top='solid')
    image=Image.open(path).convert('RGB');w,h=image.size;assert (w,h)==(559,468)
    pix=image.load();fill=[(a,b) for a in range(w) for b in range(h) if pix[a,b]==(223,234,242)]
    assert len(fill)>100
    actual=[min(z[0] for z in fill),max(z[0] for z in fill),min(z[1] for z in fill),max(z[1] for z in fill)]
    L,H,j,k=data['bounds'];xmin,xmax,ymin,ymax=data['limits']
    xp=lambda z:w*(.04+.90*(z-xmin)/(xmax-xmin));yp=lambda z:h*(1-(.10+.84*(z-ymin)/(ymax-ymin)))
    expected=[xp(L),xp(H),yp(k),yp(j)]
    assert all(abs(a-b)<=3 for a,b in zip(actual,expected)),(actual,expected)
    # Separate horizontal edges and both arrowed zero axes visible at actual pixels.
    for value,color in [(j,data['lower']),(k,data['upper'])]:
        at=.3*L+.7*H
        if abs(at)<.1:at=.7*L+.3*H
        xx=int(xp(at));yy=int(yp(value));target=(255,0,0) if color=='red' else (0,0,255)
        assert any(pix[xx,by]==target for by in range(max(0,yy-3),min(h,yy+4)))
    for xx,yy in [(xp(0),yp(k+.7)),(xp(H+.8),yp(0))]:
        xx=int(xx);yy=int(yy)
        assert any(max(pix[bx,by])<90 for bx in range(xx-3,xx+4) for by in range(yy-3,yy+4))

def clipped_source_area():
    # Exact polygon clipping, independent of generator area metadata.
    U=g.y-3*g.x;V=g.y+2*g.x
    inverse=S.solve([g.u-U,g.v-V],[g.x,g.y]);poly=[(S.Integer(-2),S.Integer(1)),(S.Integer(2),S.Integer(1)),(S.Integer(2),S.Integer(3)),(S.Integer(-2),S.Integer(3))]
    for expr in [inverse[g.x],inverse[g.y]]:
        new=[]
        for a,b in zip(poly,poly[1:]+poly[:1]):
            fa=expr.subs({g.u:a[0],g.v:a[1]});fb=expr.subs({g.u:b[0],g.v:b[1]})
            if fa>=0:new.append(a)
            if (fa<0<=fb) or (fb<0<=fa):
                t=fa/(fa-fb);new.append(tuple(S.simplify(a[i]+t*(b[i]-a[i])) for i in (0,1)))
        poly=new
    area=abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(poly,poly[1:]+poly[:1])))/2/5
    assert area==S.Rational(89,60)
    return str(area)

def main():
    coverage=[];records=[];fixtures=[];fidelity=[];quadrant_area=clipped_source_area()
    for c in g.CASES:
        r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);q=g.QUESTIONS[c['source_id']];got=r['question']
        check_raw_parameterization(r);records.append(r)
        for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):
            assert (key in got)==(key in q)
        for key in (':question/problem',':question/worked-solution'):assert got.get(key)==q.get(key),(c['source_id'],key)
        sf=q[':question/answer-fields'][0];gf=got[':question/answer-fields'][0]
        assert (':answer-field/correct' in sf)==(':answer-field/correct' in gf)
        assert sorted(a[':answer/value'] for a in sf[':answer-field/choices'])==sorted(a[':answer/value'] for a in gf[':answer-field/choices'])
        if ':answer-field/correct' in sf:
            target=next(a[':answer/value'] for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1]);assert target==sf[':answer-field/correct'][':answer/value']
            fixtures.append(fixture(r,c['source_id']+'/raw'))
        fidelity.append({'source_id':c['source_id'],'prompt_exact':True,'solution_presence_and_text_exact':True,'bank_values_matched':5,'bank_total':5,'designation':'matched' if ':answer-field/correct' in sf else 'absent in source; not counted matched','evidence_only':True})
        # All replay profiles are genuinely parameterized; bank and prompt change.
        p=dict(c['parameters']);p['k']+=1
        try:changed=g.generate(c['level'],template=c['template'],parameters=p,profile=c['bank_profile'])
        except ValueError:
            p=dict(c['parameters']);p['h']+=1;changed=g.generate(c['level'],template=c['template'],parameters=p,profile=c['bank_profile'])
        assert changed['question'][':question/problem']!=got[':question/problem']
        check_raw_parameterization(changed);records.append(changed)
    for t,l in g.TEMPLATES.items():
        seen=set()
        for seed in range(16):
            r=g.generate(l,seed=seed,template=t);check_record(r);seen.add(r['generation']['mathematical_fingerprint'])
            if seed<2:check_plot(r['generation']['plot']['path'],r['generation']['plot']['spec'])
            assert r==g.generate(l,seed=seed,template=t)
            fixtures.append(fixture(r,t+'/'+str(seed)))
            if seed<2:records.append(r)
            p=r['generation']['parameters'];other=g.generate(l,seed=seed+99,template=t,parameters=p)
            assert other['question'][':question/id']==r['question'][':question/id']
        coverage.append({'template':t,'difficulty':l,'sampled_mathematical_tasks':len(seen)})
    boundaries={'linear':dict(a=2,b=4,l=-5,h=3,j=4,k=10),'linear_legacy':dict(a=4,b=2,l=-5,h=3,j=4,k=10),'quotient':dict(n=2,l=2,h=9,j=1,k=10),'reciprocal':dict(c=1,d=1,n=2,l=1,h=9,j=2,k=10),'reciprocal_scaled':dict(c=4,d=4,n=3,l=1,h=9,j=2,k=10)}
    for t,p in boundaries.items():
        r=g.generate(g.TEMPLATES[t],template=t,parameters=p);check_record(r);check_plot(r['generation']['plot']['path'],r['generation']['plot']['spec']);fixtures.append(fixture(r,t+'/explicit-boundary'))
    for t,p in boundaries.items():
        bad=dict(p);bad['h']=99
        try:g.generate(g.TEMPLATES[t],template=t,parameters=bad);raise AssertionError('Out-of-range bypass')
        except ValueError:pass
    # Normal completion at ALL original mathematical anchors, including unit
    # endpoints/coefficient banks, with full displayed operative-stage checks.
    for c in g.CASES:
        r=g.generate(c['level'],template=c['template'],parameters=c['parameters']);check_record(r);fixtures.append(fixture(r,c['source_id']+'/normal-anchor'))
    for t,l in g.TEMPLATES.items():
        expected={p for p,z in g.PROFILES.items() if z==t and not p.startswith('observed-')}
        selected={g.generate(l,seed=s,template=t)['generation']['profile'] for s in range(30)}
        assert selected==expected,(t,selected,expected)
    # Normal default must serve BOTH observed families per level.
    for l in ('easy','moderate','hard'):
        observed={g.generate(l,seed=s)['generation']['template'] for s in range(30)}
        assert observed=={t for t,z in g.TEMPLATES.items() if z==l}
    # Hard guard cannot accept a moderate task by explicit inputs.
    try:g.generate_hard(parameters=dict(c=1,d=1,n=2,l=2,h=3,j=1,k=3));raise AssertionError('Guard bypass')
    except ValueError:pass
    # Mutations target displayed math, not answer metadata.
    mutations=[]
    r=g.generate_moderate(seed=5,template='reciprocal')
    for name,modify in [('wrong distributed derivative',lambda z:z.replace(r'\frac{1}{y}',r'\frac{2}{y}',1)),('missing cancellation stage',lambda z:re.sub(r'=\\frac\{x\^\{2\} y\^\{2\}\}\{x\^\{2\} y\}', '',z)),('wrong endpoint arithmetic',lambda z:z.replace(r'\ln ',r'\ln 99+',1)),('control character',lambda z:z+'\x0c')]:
        mutant=copy.deepcopy(r);s=mutant['question'][':question/worked-solution'];new=modify(s);assert new!=s,name;mutant['question'][':question/worked-solution']=new
        try:check_record(mutant)
        except (AssertionError,ValueError,TypeError):mutations.append(name)
        else:raise AssertionError('Mutation escaped '+name)
    # Fresh concurrent render calls, distinct and identical params, without cache.
    params=[dict(l=-5,h=3,j=2,k=9,a=2,b=3),dict(l=-3,h=4,j=1,k=10,a=2,b=3)]
    # Private isolated render directory prevents deleting active review assets.
    original=g.ROOT;private=ROOT/'concurrent-fresh';private.mkdir(exist_ok=True);g.ROOT=private
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            out=list(pool.map(lambda p:g.render_plot(p,'linear'),[params[0],params[1],params[0],params[1]]))
        assert out[0]==out[2] and out[1]==out[3] and out[0]!=out[1]
        for path,data in out:assert json.loads(Path(path).with_suffix('.json').read_text())==data;check_plot(path,data)
        assert not list((private/'plots').glob('rect-*'))
    finally:g.ROOT=original
    bad=copy.deepcopy(out[0][1]);bad['edge_inclusion']['left']=False
    try:check_plot(out[0][0],bad);raise AssertionError('Edge inclusion mutation escaped')
    except AssertionError as exc:
        if str(exc)=='Edge inclusion mutation escaped':raise
        mutations.append('source left-edge inclusion mutation')
    (ROOT/'engine-input.json').write_text(json.dumps(fixtures,indent=2))
    subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],check=True)
    (ROOT/'source-cases.json').write_text(json.dumps(g.CASES,indent=2))
    (ROOT/'review.json').write_text(json.dumps(records,indent=2,ensure_ascii=False))
    review=['# Original and generated review','All original previews below are exact public raw replays. Missing ratings/solutions/keys remain missing. Historical profiles are evidence-only. The source easy quadrant error is retained here and repaired in normal examples.','Source coverage: 4/4 complete banks, 20/20 values, 2/2 observed refs; 2 missing refs not counted matched.']
    for r in records:
        meta=r['generation'];label=('Original raw replay' if meta['evidence_only'] and meta['parameters']==g.BY_TEMPLATE[meta['template']]['parameters'] else 'Changed-parameter historical bank (evidence-only)' if meta['evidence_only'] else 'Generated method-bank variant')
        review+=['## '+label+' — '+meta['template'],f"Difficulty: {g.TEMPLATES[meta['template']]} ({'authored assignment' if meta['authored_level'] else 'observed level'}); profile: {meta['profile']}; parameters: `{json.dumps(meta['parameters'],sort_keys=True)}`.",g.markdown(r).replace('![](images/','![](/media/jake/SSD/EDB/math/images/')]
    (ROOT/'review.md').write_text('\n\n'.join(review)+'\n')
    report={'status':'pass','source_banks':fidelity,'full_source_banks_matched':4,'source_options_matched':20,'source_options_total':20,'observed_correct_designations_matched':2,'observed_correct_designations_total':2,'missing_source_correct_designations':2,'raw_source_solutions_exact':2,'raw_source_solutions_total':2,'raw_absent_solutions_preserved':2,'normal_source_solution_repairs':['q-160870 quadrant claim removed and literal set braces escaped','q-160891 positive Jacobian sign restored inside absolute value; dv du integral order restored; literal set braces escaped'],'source_scope_error':{'source_id':'q-160870','literal_first_quadrant_area':quadrant_area,'source_key_area':'8/5','mathematically_correct_for_literal_prompt':False,'raw_profile_ineligible':True},'coverage':coverage,'mutations_rejected':mutations,'native_grading':json.loads((ROOT/'engine-report.json').read_text()),'dependencies':{'python':sys.version.split()[0],'sympy':S.__version__,'matplotlib':__import__('matplotlib').__version__},'engine_binary_sha256':hashlib.sha256((REPO/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'concurrent_fresh_rendering':True,'database_writes':0}
    (ROOT/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
    print('PASS: 4/4 complete raw banks, 20/20 values, 2/2 observed refs; 89 normal displayed-math checks; native 91 fixtures; 5 mutation rejections; known source quadrant error retained.')
if __name__=='__main__':main()
