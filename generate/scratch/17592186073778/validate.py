#!/usr/bin/env python3
"""Independent displayed equations/family/stages and actual native grading."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[2]
spec=importlib.util.spec_from_file_location('general_family',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X,Y,T,U=sp.symbols('x y t u');D={'x':X,'y':Y,'t':T,'u':U}
TRANS=standard_transformations+(implicit_multiplication_application,)
def expr(s):
    s=s.replace(' ', '').replace(r'\left','').replace(r'\right','').replace(r'\dfrac',r'\frac')
    while r'\frac' in s:
        new=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',s)
        assert new!=s,s;s=new
    assert '\\' not in s,s
    return sp.expand(parse_expr(s,local_dict=D,transformations=TRANS))
def eq(s):return tuple(expr(v) for v in s.replace('&','').split('='))
def coeff(e):
    v=sp.expand(e[0]-e[1]);assert sp.Poly(v,X,Y).total_degree()==1
    return v.coeff(X),v.coeff(Y),-v.subs({X:0,Y:0})
def pair(s):return tuple(expr(v) for v in s.strip().removeprefix(r'\left').removesuffix(r'\right').strip()[1:-1].split(','))
def signature(pair):
    """Independent affine-image equation, not the production signature helper."""
    x,y=pair;syms=x.free_symbols|y.free_symbols;assert len(syms)==1
    z=next(iter(syms));vx=sp.diff(x,z);vy=sp.diff(y,z);assert not vx.has(z) and not vy.has(z) and (vx or vy)
    h=sp.expand(vy*(X-x.subs(z,0))-vx*(Y-y.subs(z,0)))
    co=(h.coeff(X),h.coeff(Y),h.subs({X:0,Y:0}));pivot=next(v for v in co if v)
    return tuple(sp.simplify(v/pivot) for v in co)
def formatting(text):
    assert text.count('$')%2==0
    clean=re.sub(r'\\[{}]','',text);depth=0
    for ch in clean:
        if ch=='{':depth+=1
        elif ch=='}':depth-=1
        assert depth>=0
    assert depth==0
    assert not any(v in text for v in ['--','+-','None','nan'])
def check(rec):
    q=rec['question'];meta=rec['generation'];f=q[':question/answer-fields'][0]
    assert rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    equations=re.findall(r'\$([^$]*=[^$]*)\$',q[':question/problem'])[:2]
    assert len(equations)==2
    rows=[coeff(eq(e)) for e in equations];a,b,c=rows[0];d,e,ff=rows[1]
    assert all((a,b,c,d,e,ff));assert a*e-b*d==0 and a*ff-c*d==0
    m,k=-a/b,c/b;v=D[meta['parameters']['variable']];target=signature((v,m*v+k))
    assert f[':answer-field/type'] in [':answer-field.type/radio',':answer-field.type/blank']
    assert meta['inferred_correct_value']==g.aff(m,k,str(v)) if f[':answer-field/type'].endswith('blank') else signature(pair(meta['inferred_correct_value']))==target
    if meta['raw_evidence']:
        assert not meta['eligible_for_learning']
        if f[':answer-field/type'].endswith('radio'):
            actual=[signature(pair(z[':answer/value'])) for z in f[':answer-field/choices']]
            expected=[signature((v,mm*v+kk)) for mm,kk in [(k,-m),(1,k),(m,k),(1,m),(m,-k)]]
            assert sorted(map(str,actual))==sorted(map(str,expected))
        assert ':question/difficulty' not in q and ':question/worked-solution' not in q and ':answer-field/correct' not in f
        return
    assert meta['eligible_for_learning'];formatting(q[':question/problem']);formatting(q[':question/worked-solution'])
    g.guard(meta['authored_level'],meta['parameters'])
    ans=f[':answer-field/choices'];correct=next(z for z in ans if z[':answer/id']==f[':answer-field/correct'][1])
    if f[':answer-field/type'].endswith('radio'):
        assert len(ans)==5
        signatures=[signature(pair(z[':answer/value'])) for z in ans]
        assert len(set(signatures))==5 and signatures.count(target)==1
        expected=[signature((v,mm*v+kk)) for mm,kk in [(m,k),(-m,k),(m,-k),(-b/a,c/a),(0,k)]]
        assert set(signatures)==set(expected)
        assert signature(pair(correct[':answer/value']))==target
    else:
        assert '{{field-1}}' in q[':question/problem'];assert len(ans)==1
        assert sp.simplify(expr(correct[':answer/value'])-(m*v+k))==0
    for obj in [q,f,*ans]:
        for key in [':question/id',':answer-field/id',':answer/id']:
            if key in obj:assert len(obj[key])==36
    assert all(z[':answer/type']==':answer.type/math' for z in ans)
    sol=q[':question/worked-solution'];assert sol.startswith('The points of intersection of the lines correspond to the solutions of the following system:')
    multiplier=expr(re.search(r'multiply the first equation by \$([^$]+)\$',sol).group(1));assert multiplier==-d/a
    cancellation=expr(re.search(r'get a \$([^$]+)\$ term',sol).group(1));assert cancellation==multiplier*a*X
    systems=re.findall(r'\$\$\n\\\{([^\n]+)\n\$\$',sol);assert len(systems)==2
    for block in systems:assert [coeff(eq(s.split(r'\mid')[0])) for s in block.split(';')]==rows
    assert r'\cdot ('+g.tex(multiplier)+')' in systems[1]
    blocks=re.findall(r'\\begin\{aligned\}\n(.*?)\n\\end\{aligned\}',sol,re.S);assert len(blocks)==2
    raw0=blocks[0].split('\\\\\n');raw1=blocks[1].split('\\\\\n');assert len(raw0)==4 and len(raw1)==4
    elimination=[eq(s) for s in raw0];isolation=[eq(s) for s in raw1]
    assert [coeff(s) for s in elimination[:2]]==[(-d,-e,-ff),(d,e,ff)]
    assert re.search(r'&= \([^()]+ [+-] [^()]+\)',raw0[2])
    assert elimination[2]==(0,0) and elimination[3]==(0,0)
    assert coeff(isolation[0])==rows[0]
    assert isolation[1]==(b*Y,c-a*X)
    assert r'\frac{' in raw1[2] and r'}{'+g.tex(b)+'}' in raw1[2]
    assert isolation[2]==(Y,m*X+k) and isolation[3]==(Y,m*X+k)
    final=re.search(r'\$\$\n(\\left\([^\n]+)\n\$\$',sol).group(1)
    assert signature(pair(final.replace(r' \right', '')))==target
    assert 'where $'+str(v)+'$ is any number.' in sol
    assert 'Any value of $x$ can be chosen' in sol
    if v!=X:assert 'Let $'+str(v)+'=x$ be the free coordinate.' in sol

def native(rec,label):
    f=rec['question'][':question/answer-fields'][0];checks=[]
    if f[':answer-field/type'].endswith('radio'):
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Displayed complete family '+a[':answer/value']} for a in f[':answer-field/choices']]
    else:
        val=f[':answer-field/choices'][0][':answer/value'];m,k=map(sp.Rational,[-sp.Rational(rec['generation']['parameters']['a'])/sp.Rational(rec['generation']['parameters']['b']),sp.Rational(rec['generation']['parameters']['c'])/sp.Rational(rec['generation']['parameters']['b'])]);v=rec['generation']['parameters']['variable']
        equivalent=f'({g.tex(m)}({v}-1))+({g.tex(m+k)})'
        checks=[{'submitted':val,'expected':'accepted','purpose':'Canonical coordinate fragment'}, {'submitted':equivalent,'expected':'accepted','purpose':'Shifted grouped equivalent fragment'}, {'submitted':g.aff(-m,k,v),'expected':'rejected','purpose':'Sign error fragment'}, {'submitted':g.aff(m,k+m,v),'expected':'rejected','purpose':'Shifted parameter fragment violates the supplied first-coordinate convention'}]
    return {'label':label,'record':rec,'checks':checks}
def write(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2)+'\n')
def main():
    write('validation.json',{'passed':False,'status':'running'})
    capture=json.loads((HERE/'source.json').read_text());cases=json.loads((HERE/'source-cases.json').read_text());sources=capture['record'][':knowledge-point/questions'];review=[];notes=['# General family review','','All source level assignments/keys/solutions are explicitly authored completions. Raw records retain omissions.'];engine=[];changed=0
    for source,case in zip(sources,cases,strict=True):
        rec=g.generate(case['authored_level'],parameters=case['parameters'],template=case['template'],profile=case['bank_profile']);check(rec);q=rec['question'];f=q[':question/answer-fields'][0];sf=source[':question/answer-fields'][0]
        assert q[':question/problem']==source[':question/problem']
        for attr in [':question/difficulty',':question/worked-solution',':question/answer-fields']:assert (attr in q)==(attr in source)
        for attr in [':answer-field/correct',':answer-field/choices']:assert (attr in f)==(attr in sf)
        assert f[':answer-field/key']==sf[':answer-field/key'] and f[':answer-field/type']==sf[':answer-field/type'][':db/ident']
        assert sorted(a[':answer/value'] for a in f.get(':answer-field/choices',[]))==sorted(a[':answer/value'] for a in sf.get(':answer-field/choices',[]))
        if ':answer-field/choices' in f:
            signs=[signature(pair(z[':answer/value'])) for z in f[':answer-field/choices']]
            target=signature(pair(rec['generation']['inferred_correct_value']));assert len(set(signs))==5 and signs.count(target)==1
        review.append(rec);notes+=['','## Original '+case['source_id'],'',g.markdown(rec)]
        for seed in range(12):
            r=g.generate(case['authored_level'],seed=seed,profile=case['bank_profile']);check(r);assert r['question'][':question/problem']!=source[':question/problem'];changed+=1
        normal=g.generate(case['authored_level'],parameters=case['parameters'],template=case['template']);check(normal);engine.append(native(normal,'Inferred completion '+case['source_id']));review.append(normal);notes+=['','### Authored completion','',g.markdown(normal)]
        rawchanged=g.generate(case['authored_level'],seed=42,profile=case['bank_profile']);review.append(rawchanged);notes+=['','### Parameterized raw bank/layout variant (evidence only)','',g.markdown(rawchanged)]
    # Full canonical worked chain: minimal escaped-brace/prose/notation repairs only.
    canonical=capture['record'][':knowledge-point/canonical-example'][':question/worked-solution']
    authored=g.solution(g.parameters(dict(a=3,b=2,c=2,r=2)))
    def normalize(t):return re.sub(r'\s+','',t.replace(r'\{','{').replace(r'\dfrac',r'\frac').replace('can be chosen','is a solution'))
    assert normalize(canonical)==normalize(authored)
    tested=0;diversity={};coverage={}
    for level in g.LEVELS:
        seen=set();types=set();positions=set()
        for seed in range(240):
            rec=g.generate(level,seed);check(rec);tested+=1;seen.add(rec['generation']['parameter_fingerprint']);types.add(rec['generation']['template']);f=rec['question'][':question/answer-fields'][0]
            again=g.generate(level,seed+1000,template=rec['generation']['template'],parameters=rec['generation']['parameters']);assert rec['question'][':question/id']==again['question'][':question/id']
            if f[':answer-field/type'].endswith('radio'):positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
            if seed<12:engine.append(native(rec,level+' '+str(seed)))
            if seed<2:review.append(rec);notes+=['','## Generated '+level+' variant '+str(seed),'',g.markdown(rec)]
        assert types==set(g.TEMPLATES) and positions==set(range(5)) and len(seen)>=90
        diversity[level]={'sampled':240,'distinct_mathematical_lines':len(seen),'not_exhaustive':True};coverage[level]={'layouts':sorted(types),'correct_positions':sorted(positions)}
        for template in g.TEMPLATES:
            for seed in (31,71):
                rec=g.generate(level,seed,template=template);check(rec);engine.append(native(rec,level+template+str(seed)));review.append(rec);notes+=['','## Generated '+level+' '+template+' '+str(seed),'',g.markdown(rec)]
    # Finite meaningful family catalog over documented base sampler domain, r=2.
    catalog={}
    for level in g.LEVELS:
        fps=set()
        brange=[-1,1] if level=='easy' else [i for i in range(-4 if level=='moderate' else -6,5 if level=='moderate' else 7) if abs(i)>=2]
        arange=[-6,-5,-4,-3,-2,2,3,4,5,6] if level=='easy' else [i for i in range(-12,13) if i]
        crange=[i for i in range(-8 if level=='easy' else -12,9 if level=='easy' else 13) if i]
        for a in arange:
            for b in brange:
                for c in crange:
                    p=g.parameters(dict(a=a,b=b,c=c,r=2))
                    try:g.guard(level,p);g.eligible_bank(p,'method')
                    except ValueError:continue
                    fps.add(g.fingerprint(p))
        assert len(fps)>=160;catalog[level]=len(fps)
    # Parameter aliases, independent whole-line scaling/signs, second-row order/scaling ignored.
    p=g.parameters(dict(a=3,b=2,c=2,r=2));fp=g.fingerprint(p)
    assert g.fingerprint({**p,'variable':'t'})==fp
    assert g.fingerprint(g.parameters(dict(a=-6,b=-4,c=-4,r='1/2')))==fp
    assert g.fingerprint(g.parameters(dict(a=6,b=4,c=4,r='1/2')))==fp
    assert g.fingerprint({**p,'r':'3'})==fp
    assert signature((2*T+5,3*(2*T+5)+2))==signature((X,3*X+2))
    assert g.canonical_family((2*T+5,3*(2*T+5)+2))==g.canonical_family((X,3*X+2))
    bad=[]
    for level,p0 in [('easy',dict(a=3,b=2,c=2,r=2)),('moderate',dict(a=1,b=4,c=3,r=2)),('hard',dict(a=3,b=2,c=2,r=2)),('hard',dict(a=1,b=2,c=1,r=2)),('easy',dict(a=6,b=1,c=8,r=5)),('hard',dict(a=-25,b=-4,c=3,r=2))]:
        try:g.generate(level,parameters=p0)
        except ValueError:bad.append(p0)
        else:raise AssertionError('Explicit workload bound bypassed')
    sample=g.generate('moderate',seed=8,template='radio_family');mut=[]
    r=copy.deepcopy(sample);r['question'][':question/problem']=r['question'][':question/problem'].replace(' =',' = 1 +',1);mut.append(r)
    r=copy.deepcopy(sample);r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace('y &=','y &= 1 +',1);mut.append(r)
    r=copy.deepcopy(sample);r['question'][':question/worked-solution']=re.sub(r'0 &= \([^\n]*\)','0 &= 0',r['question'][':question/worked-solution'],count=1);mut.append(r)
    r=copy.deepcopy(sample);r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace('where $','where $2',1);mut.append(r)
    r=copy.deepcopy(sample);f=r['question'][':question/answer-fields'][0];f[':answer-field/choices'][1][':answer/value']=f[':answer-field/choices'][0][':answer/value'];mut.append(r)
    r=copy.deepcopy(sample);f=r['question'][':question/answer-fields'][0];p0=sample['generation']['parameters'];mm=-sp.Rational(p0['a'])/sp.Rational(p0['b']);kk=sp.Rational(p0['c'])/sp.Rational(p0['b']);wrong=next(z for z in f[':answer-field/choices'] if z[':answer/id']!=f[':answer-field/correct'][1]);wrong[':answer/value']='(2t+5, ('+g.tex(mm)+')(2t+5) + ('+g.tex(kk)+'))';mut.append(r)
    for rec in mut:
        try:check(rec)
        except (AssertionError,ValueError):pass
        else:raise AssertionError('Accepted altered actual display/math/stage')
    notes+=['','## Native wrong-shape limitation','','A complete coordinate tuple submitted to the scalar-fragment blank produces native parser error unclosed group, rather than a Boolean rejection. This is tested separately as one documented unresolved wrong-shape probe. Canonical, grouped-equivalent and incorrect scalar fragments are all supported and checked normally. Raw incomplete questions remain ineligible; normal fields are scalar-fragment assessments.']
    write('review.json',review);(HERE/'review.md').write_text('\n'.join(notes)+'\n');write('engine-input.json',engine)
    harness=REPO/'generate/runs/current/check-engine';subprocess.run([str(harness),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True,capture_output=True,text=True)
    result=json.loads((HERE/'engine-report.json').read_text());assert result['documented_unresolved_checks']==0
    probe=copy.deepcopy(engine[0]);probe['label']='Known wrong-shape tuple parser limitation';val=probe['record']['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'];probe['checks']=[{'submitted':'(x, '+val+')','expected':'unresolved','purpose':'Complete tuple is outside required scalar-fragment response; native parser returns unclosed group'}];write('engine-wrong-shape-input.json',[probe]);subprocess.run([str(harness),str(HERE/'engine-wrong-shape-input.json'),str(HERE/'engine-wrong-shape-report.json')],check=True,capture_output=True,text=True);shape=json.loads((HERE/'engine-wrong-shape-report.json').read_text());assert shape['documented_unresolved_checks']==1
    report={'passed':True,'source_questions':2,'raw_exact_prompts':2,'complete_source_banks':{'matched':1,'total':1,'options_matched':5,'options_total':5},'blank_layout_presence_matches':1,'raw_omissions':{'difficulty':2,'worked_solution':2,'correct_refs':2,'blank_choices':1},'original_correct_designations':{'present':0,'matched':0,'inferred_normal':2},'source_worked_solutions':{'present':0,'matched':0,'authored_completions':2},'canonical_full_solution_normalized_match':True,'canonical_repairs':['escape 2 unmatched literal system braces','Any value of x can be chosen (rather than itself a solution)','dfrac/whitespace normalization'],'changed_public_raw_replays':changed,'normal_math_records':tested+14,'default_coverage':coverage,'variety_sample':diversity,'finite_base_domain_distinct_lines':catalog,'native':{'accepted':result['accepted_checks'],'rejected':result['rejected_checks'],'unresolved':0},'native_wrong_shape_probe':{'documented_unresolved':1,'reason':'Complete tuple in scalar-fragment blank gives unclosed group parser error'},'mutation_failures_caught':len(mut),'invalid_explicit_calls_rejected':len(bad),'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'engine_sha256':hashlib.sha256(harness.read_bytes()).hexdigest(),'engine_source_sha256':hashlib.sha256(harness.with_suffix('.rs').read_bytes()).hexdigest(),'provenance':g.SOURCE,'unresolved_findings':['Historical wrong-option intention opaque: replay-only profile ineligible for learning','Out-of-shape complete tuple submission to scalar blank returns native parser error, rather than Boolean rejection'],'no_database_writes':True}
    write('validation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':
    try:main()
    except Exception as exc:
        write('validation.json',{'passed':False,'failure_type':type(exc).__name__,'failure':str(exc)});raise
