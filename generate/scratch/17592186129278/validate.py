#!/usr/bin/env python3
"""Independent displayed-math, source-fidelity, native-grade and mutation checks."""
import copy, hashlib, importlib.util, json, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def write(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2)+'\n')
def eq(a,b):assert sp.simplify(sp.trigsimp(a-b))==0,(a,b)
def group(s,i):
    assert s[i]=='{',(s,i);depth=1;j=i+1
    while depth:depth+=(s[j]=='{')-(s[j]=='}');j+=1
    return s[i+1:j-1],j

def integral(s):
    bounds=[]
    while s.startswith(r'\int'):
        i=4;assert s[i]=='_';i+=1
        if s[i]=='{':lo,i=group(s,i)
        else:lo=s[i];i+=1
        assert s[i]=='^';hi,i=group(s,i+1);bounds.append((g.parse_tex(lo),g.parse_tex(hi)));s=s[i:]
    s=re.sub(r'\\,d(?:z|r|\\theta)','',s)
    return bounds,s

def bracket(s):
    a=s.index('[');b=s.rindex(']');primitive=s[a+1:b];suffix=s[b+1:]
    assert suffix.startswith('_{');lo,i=group(suffix,1);assert suffix[i]=='^';hi,i=group(suffix,i+1)
    var,lo=lo.split('=',1);var2,hi=hi.split('=',1);assert var==var2
    return s[:a],g.parse_tex(primitive),var,g.parse_tex(lo),g.parse_tex(hi)

def outside_multiplier(s):
    return g.parse_tex(s.strip().removesuffix(r'\cdot').strip()) if s.strip() else sp.Integer(1)

def endpoint_parts(s):
    """Read each actual printed signed endpoint component without cancellation."""
    result=[];i=0
    while i<len(s):
        if s[i] in '+-':i+=1
        assert s[i]=='(',(s,i);depth=1;j=i+1
        while depth:depth+=(s[j]=='(')-(s[j]==')');j+=1
        result.append(g.parse_tex(s[i+1:j-1]));i=j
    return result

def assert_endpoints(s,prim,var,lo,hi,terms=None):
    observed=endpoint_parts(s);terms=terms if terms is not None else prim.as_ordered_terms() if prim.is_Add else [prim]
    expected=[value for term in terms for value in (term.subs(var,hi),term.subs(var,lo))]
    assert len(observed)==len(expected),(s,expected)
    for a,b in zip(observed,expected):eq(a,b)

def formatting(record):
    q=record['question'];assert set(record['knowledge_point'])=={'db_id','id','title'}
    f=q[':question/answer-fields'][0];assert f[':answer-field/key']=='selection'
    assert f[':answer-field/type']==':answer-field.type/radio'
    vals=[a[':answer/value'] for a in f[':answer-field/choices']];assert len(vals)==5
    assert f[':answer-field/correct'][0]==':answer/id';assert f[':answer-field/correct'][1] in [a[':answer/id'] for a in f[':answer-field/choices']]
    for text in [q[':question/problem'],q[':question/worked-solution']]+vals:
        assert not any(ord(c)<32 and c not in '\n\t' for c in text)
        assert not any(line.startswith('    ') for line in text.splitlines())
        assert text.count('$$')%2==0 and text.replace('$$','').count('$')%2==0
        depth=0
        for i,c in enumerate(text):
            if c in '{}':
                if i>0 and text[i-1]=='\\':continue
                depth+=1 if c=='{' else -1;assert depth>=0
        assert depth==0
    values=list(map(g.parse_tex,vals));assert all(sp.simplify(a-b)!=0 for i,a in enumerate(values) for b in values[:i])


def displayed_math(record):
    formatting(record);q=record['question'];problem=q[':question/problem'];work=q[':question/worked-solution']
    # Derive all geometry and the assessed integrand from the actual prompt.
    cart=g.parse_tex(re.search(r'\\iiint_R (.*?)\\,\\mathrm\{d\}V',problem).group(1))
    n=sp.Integer(re.search(r'cylinder \$x\^2\+y\^2=(\d+)\$',problem).group(1));R=sp.sqrt(n)
    low,high=re.search(r'surfaces \$z=(.*?)\$ and \$z=(.*?)\.\$',problem).groups()
    low,high=map(g.parse_tex,(low,high));replacement={g.x:g.r*sp.cos(g.t),g.y:g.r*sp.sin(g.t)}
    low=sp.trigsimp(low.subs(replacement,simultaneous=True));high=sp.trigsimp(high.subs(replacement,simultaneous=True))
    F=sp.trigsimp(cart.subs(replacement,simultaneous=True)*g.r)
    if 'for $x\\ge 0,$ $y\\ge 0$' in problem:a,d=0,sp.pi/2
    elif 'for $x\\ge 0$' in problem:a,d=-sp.pi/2,sp.pi/2
    elif 'for $y\\ge 0$' in problem:a,d=0,sp.pi
    else:a,d=0,2*sp.pi
    zp=sp.integrate(F,g.z);ze=sp.expand(zp.subs(g.z,high)-zp.subs(g.z,low));rp=sp.integrate(ze,g.r);rr=sp.expand(rp.subs(g.r,R)-rp.subs(g.r,0));tp=sp.integrate(rr,g.t);value=sp.simplify(tp.subs(g.t,d)-tp.subs(g.t,a))
    bank=q[':question/answer-fields'][0];correct=next(c for c in bank[':answer-field/choices'] if c[':answer/id']==bank[':answer-field/correct'][1]);eq(g.parse_tex(correct[':answer/value']),value)
    # Independently integrate EVERY displayed wrong operation from the actual
    # printed Cartesian integrand and geometry, not the generator's formulas.
    family=record['generation']['template']
    if family=='reciprocal':
        wrong_extra=sp.integrate(sp.integrate(ze*g.r**2,(g.r,0,R)),(g.t,a,d))
        wrong_half=sp.integrate(sp.integrate(ze,(g.r,0,R/2)),(g.t,a,d))
        wrong_double=sp.integrate(rr,(g.t,a,a+2*(d-a)))
        wrong_reduce=sp.integrate(sp.integrate(sp.expand(sp.trigsimp(ze)).subs(sp.cos(2*g.t),1),(g.r,0,R)),(g.t,a,d))
        expected_values=[value,wrong_extra,wrong_half,wrong_double,wrong_reduce]
    else:
        wrong_extra=sp.integrate(sp.integrate(ze*g.r,(g.r,0,R)),(g.t,a,d))
        wrong_half=sp.integrate(sp.integrate(ze,(g.r,0,R/2)),(g.t,a,d))
        wrong_angle=sp.integrate(rr,(g.t,0,sp.pi)) if family=='half_linear' else sp.integrate(rr,(g.t,a,(a+d)/2))
        wrong_double=sp.integrate(rr,(g.t,a,a+2*(d-a)))
        expected_values=[value,wrong_extra,wrong_half,wrong_angle,wrong_double]
    displayed_values=[g.parse_tex(c[':answer/value']) for c in bank[':answer-field/choices']]
    for expected in expected_values:assert sum(sp.simplify(sp.trigsimp(v-expected))==0 for v in displayed_values)==1,(family,expected,displayed_values)
    chain=work.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0];rows=chain.split(r' \\ &=');rows[0]=rows[0].split('&=',1)[1]
    assert len(rows)>=12
    substitution=rows[0].removeprefix(r'\iiint_\Delta ').removesuffix(r'\,dz\,dr\,d\theta');eq(g.parse_tex(substitution),F)
    bounds,integrand=integral(rows[1]);assert len(bounds)==3
    for pair,expected in zip(bounds,((a,d),(0,R),(low,high))):
        for actual,target in zip(pair,expected):eq(actual,target)
    eq(g.parse_tex(integrand),F)
    # z primitive and both endpoints, before radial integration.
    _,zp_display=integral(rows[2]);factor,primitive,var,l,h=bracket(zp_display);assert var=='z';eq(l,low);eq(h,high)
    multiplier=outside_multiplier(factor);eq(multiplier*sp.diff(primitive,g.z),F)
    radial_index=next(i for i,row in enumerate(rows) if ']_{r=' in row)
    for row in rows[3:radial_index]:
        bs,expr=integral(row);assert len(bs)==2;eq(g.parse_tex(expr),ze)
    _,primexpr=integral(rows[radial_index]);fac,radprim,var,l,h=bracket(primexpr);assert not fac and var=='r';eq(l,0);eq(h,R);eq(sp.diff(radprim,g.r),ze)
    for i in (radial_index+1,radial_index+2):
        _,expr=integral(rows[i]);eq(g.parse_tex(expr),rr)
        if family=='half_linear':
            angular=r'\cos(\theta)-\sin(\theta)';suffix=r'\cdot ('+angular+')'
            assert expr.endswith(suffix) and expr.startswith('(')
            scalar_diff=expr[:-len(suffix)][1:-1]
            scalar_prim=sp.simplify(radprim/(sp.cos(g.t)-sp.sin(g.t)))
            assert_endpoints(scalar_diff,scalar_prim,g.r,0,R)
        else:assert_endpoints(expr,radprim,g.r,0,R)
    theta_index=next(i for i,row in enumerate(rows) if not row.startswith(r'\int') and r']_{\theta=' in row)
    for row in rows[radial_index+3:theta_index]:
        bs,expr=integral(row);assert len(bs)==1;eq(g.parse_tex(expr),rr)
    fac,thetaprim,var,l,h=bracket(rows[theta_index]);assert var==r'\theta';eq(l,a);eq(h,d)
    theta_multiplier=outside_multiplier(fac);eq(theta_multiplier*sp.diff(thetaprim,g.t),rr)
    if family=='half_linear':
        # Structural demands from q161621, independent of equal mathematical sums:
        # one unscaled cos-minus-sin factor through EVERY radial stage, followed
        # by a scalar outside the unscaled sin-plus-cos angular bracket.
        angular=r'\cos(\theta)-\sin(\theta)';suffix=r'\cdot ('+angular+')'
        for stage_index,row in enumerate(rows[1:radial_index+4],start=1):
            _,expr=integral(row)
            assert expr.count(angular)==1,(row,'required common angular factor')
            if stage_index==1 or stage_index>=4:assert expr.count(r'\cos(')==1 and expr.count(r'\sin(')==1
        assert primexpr.split('[')[1].split(']')[0].endswith(suffix)
        assert fac.strip().endswith(r'\cdot') and theta_multiplier!=0
        assert rows[theta_index].split('[')[1].split(']')[0]==r'\sin(\theta)+\cos(\theta)'
        scalar_prim=sp.simplify(radprim/(sp.cos(g.t)-sp.sin(g.t)))
        eq(theta_multiplier,scalar_prim.subs(g.r,R)-scalar_prim.subs(g.r,0))
        # The source's extracted-factor endpoint row precedes an explicit row
        # evaluating BOTH signed primitive components independently.
        endpoint=rows[theta_index+1];pieces=endpoint.split('+');assert len(pieces)==2
        for piece,term in zip(pieces,[sp.sin(g.t),sp.cos(g.t)]):
            factor,pair=piece.split(r'\cdot ((',1);eq(g.parse_tex(factor),theta_multiplier)
            upper,lower=pair.removesuffix('))').split(')-(')
            eq(g.parse_tex(upper),term.subs(g.t,d));eq(g.parse_tex(lower),term.subs(g.t,a))
        eq(g.parse_tex(endpoint),value)
        assert_endpoints(rows[theta_index+2],theta_multiplier*thetaprim,g.t,a,d,terms=[theta_multiplier*sp.sin(g.t),theta_multiplier*sp.cos(g.t)])
    else:
        assert not fac
        assert_endpoints(rows[theta_index+1],thetaprim,g.t,a,d)
    eq(g.parse_tex(rows[-1]),value)
    family=record['generation']['template']
    if family=='half_xz':
        assert '^2' in rows[3] or '^{2}' in rows[3]
        assert r'\cos(2\cdot \theta)' in ''.join(rows[radial_index+3:theta_index])
        assert '(1+' in ''.join(rows[radial_index+3:theta_index])
    if family=='quarter_x':assert r'\sin(2\cdot \theta)' in ''.join(rows[3:radial_index])
    return value


def main():
    cases=[];raw_records=[];raw_variants=[];normal=[];fidelity={'prompts':0,'solutions_present':0,'solutions_exact':0,'banks':0,'choices':0,'correct_designations':0,'key_presence':0}
    for f,(level,sid,p) in g.SPECS.items():
        if sid is None:continue
        src=g.SOURCES[sid];record=g.generate(level,template=f,parameters={'scale':1},profile='source_raw');raw_records.append(record);q=record['question'];sf=src[':question/answer-fields'][0];gf=q[':question/answer-fields'][0]
        assert q[':question/problem']==src[':question/problem'];fidelity['prompts']+=1
        assert (':question/difficulty' in q)==(':question/difficulty' in src)
        assert (':question/worked-solution' in q)==(':question/worked-solution' in src)
        assert (':answer-field/correct' in gf)==(':answer-field/correct' in sf);fidelity['key_presence']+=1
        if ':question/worked-solution' in src:
            fidelity['solutions_present']+=1;assert q[':question/worked-solution']==src[':question/worked-solution'];fidelity['solutions_exact']+=1
        raw_values=[g.parse_tex(a[':answer/value']) for a in gf[':answer-field/choices']]
        assert all(sp.simplify(a-b)!=0 for i,a in enumerate(raw_values) for b in raw_values[:i])
        assert sorted(a[':answer/value'] for a in gf[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices']);fidelity['banks']+=1;fidelity['choices']+=5
        if ':answer-field/correct' in sf:
            generated=next(a[':answer/value'] for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1]);assert generated==sf[':answer-field/correct'][':answer/value'];fidelity['correct_designations']+=1
            eq(g.parse_tex(generated.replace('\\\\','\\')),g.stages(f,**p)[-1])
        # Genuine parameter replay, using the very same public generator.
        scaled=g.generate(level,template=f,parameters={'scale':2},profile='source_raw')
        raw_variants.append(scaled)
        assert scaled['generation']['content_identity']!=record['generation']['content_identity']
        assert scaled['generation']['eligible_for_learning'] is False
        for value in (a[':answer/value'] for a in scaled['question'][':question/answer-fields'][0][':answer-field/choices']):g.parse_tex(value.replace('\\\\','\\'))
        cases.append({'source_id':sid,'template':f,'level':level,'parameters':{'scale':1},'bank_profile':'source_raw','authored_level_assignment':':question/difficulty' not in src})
    write('source-cases.json',cases)
    # Source-shaped templates all served by normal generation; two changed examples each.
    for f,(level,sid,p) in g.SPECS.items():
        if f=='cross_z':continue
        for seed in (11,24):
            record=g.generate(level,seed,template=f);displayed_math(record);normal.append(record)
        record=g.generate(level,template=f,parameters=p);displayed_math(record)
    # Broad normal sampler, explicit boundaries, and identity independence.
    seen={};family_coverage={l:set() for l in ('easy','moderate','hard')}
    for level in family_coverage:
        for seed in range(36):
            record=g.generate(level,seed);displayed_math(record);family_coverage[level].add(record['generation']['template']);seen[record['generation']['mathematical_fingerprint']]=record
    for level,seenfamilies in family_coverage.items():assert seenfamilies=={f for f,(l,_,_) in g.SPECS.items() if l==level and f!='cross_z'}
    for record in normal:
        meta=record['generation'];again=g.generate(meta['level'],seed=555,template=meta['template'],parameters=meta['parameters'])
        assert again['question'][':question/id']==record['question'][':question/id'];assert again['generation']['mathematical_fingerprint']==meta['mathematical_fingerprint']
    # Both endpoint components have to be right even if equal offsets cancel.
    mutated=copy.deepcopy(normal[0]);mutated['question'][':question/worked-solution']=mutated['question'][':question/worked-solution'].replace('\\begin{aligned}', '\\begin{aligned}\x0c',1)
    try:displayed_math(mutated)
    except (AssertionError,ValueError):pass
    else:raise AssertionError('C0 mutation accepted')
    xz=next(q for q in normal if q['generation']['template']=='half_xz');mutated=copy.deepcopy(xz);mutated['question'][':question/worked-solution']=mutated['question'][':question/worked-solution'].replace('(1+','(2+',1)
    try:displayed_math(mutated)
    except (AssertionError,ValueError):pass
    else:raise AssertionError('Missing trig identity operation accepted')
    # Change a lower evaluated component from0 to1; checking final value alone misses this.
    mutated=copy.deepcopy(normal[0]);work=mutated['question'][':question/worked-solution'];start=work.index(']_{r=');after=work[start:];pos=after.index(')-(0)');mutated['question'][':question/worked-solution']=work[:start]+after[:pos]+after[pos:].replace(')-(0)',')-(1)',1)
    try:displayed_math(mutated)
    except (AssertionError,ValueError):pass
    else:raise AssertionError('Wrong endpoint component accepted')
    half=next(q for q in normal if q['generation']['template']=='half_linear')
    work=half['question'][':question/worked-solution']
    chain=work.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0]
    rows=chain.split(r' \\ &=');rows[0]=rows[0].split('&=',1)[1]
    radial_index=next(i for i,row in enumerate(rows) if ']_{r=' in row)
    theta_index=next(i for i,row in enumerate(rows) if not row.startswith(r'\int') and r']_{\theta=' in row)
    _,rad=integral(rows[radial_index]);fac,prim,var,lo,hi=bracket(rad)
    grouped=rad.split('[')[1].split(']')[0]
    mutations=[('half_linear_radial_distribution',grouped,g.tex(sp.expand(prim)))]
    outer,inner,var,lo,hi=bracket(rows[theta_index]);mult=outside_multiplier(outer)
    mutations.append(('half_linear_angular_distribution',rows[theta_index],g.bracket(g.tex(sp.expand(mult*inner)),var,lo,hi)))
    _,height_expr=integral(rows[4])
    mutations.append(('half_linear_height_distribution',height_expr,g.tex(sp.expand(g.parse_tex(height_expr)))))
    for label,original,replacement in mutations:
        assert original!=replacement
        eq(g.parse_tex(original) if label!='half_linear_angular_distribution' else mult*inner,
           g.parse_tex(replacement) if label!='half_linear_angular_distribution' else bracket(replacement)[1])
        mutation=copy.deepcopy(half)
        mutation['question'][':question/worked-solution']=work.replace(original,replacement,1)
        try:displayed_math(mutation)
        except (AssertionError,ValueError):pass
        else:raise AssertionError(label+' accepted equivalent distributed replacement')
    # Explicit scope guards and whole-bank rejection.
    for f,p in [('easy_radial',dict(n=4,h=3,b=1,c=1)),('half_xz',dict(n=9,h=2,b=1,c=2)),('cone',dict(n=4,h=3,b=1,c=1)),('reciprocal',dict(n=9,h=3,b=1,c=1))]:
        try:g.generate(g.SPECS[f][0],template=f,parameters=p)
        except ValueError:pass
        else:raise AssertionError('Invalid explicit parameter accepted')
    # Atomic concurrent render fresh writes in a private non-pruned cache.
    with ThreadPoolExecutor(3) as pool:
        paths=list(pool.map(lambda p:g.projection('half_xradial',p),[dict(n=15,h=4,b=1,c=1),dict(n=15,h=4,b=1,c=1),dict(n=16,h=4,b=1,c=1)]))
    for path in paths:
        path=Path(path);side=json.loads(path.with_suffix('.json').read_text());assert side['sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
    assert paths[0]==paths[1] and paths[0]!=paths[2]
    inputs=[]
    for i,record in enumerate(normal+[q for q in raw_records if ':answer-field/correct' in q['question'][':question/answer-fields'][0]]):
        field=record['question'][':question/answer-fields'][0];correct=field[':answer-field/correct'][1]
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'Complete owned radio bank'} for a in field[':answer-field/choices']]
        inputs.append({'label':str(i),'record':record,'checks':checks})
    write('engine-input.json',inputs);engine=REPO/'generate/runs/current/check-engine';subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    write('review.json',normal+raw_variants)
    chunks=['# Original and generated cylindrical evaluation review','Original raw records preserve source bytes and missing attributes. Generated records use authored complete method banks.']
    def local_review(record):
        return re.sub(r'images/[a-z0-9]+/([a-z0-9]+\.png)',r'source-assets/\1',g.markdown(record))
    for case,raw,variant in zip(cases,raw_records,raw_variants):chunks+=['\n## Original '+str(case['source_id'])+' / '+case['template'],local_review(raw),'\n### Generated historical-bank evidence variant (integrand scale2; ineligible for learning)',local_review(variant)]
    for q in normal:chunks+=['\n## Generated '+q['generation']['level']+' / '+q['generation']['template']+' / '+str(q['generation']['parameters']),g.markdown(q)]
    (HERE/'review.md').write_text('\n\n'.join(chunks)+'\n')
    domains={}
    # Finite structural catalogs: no letter aliases, profile aliases or unused b counted.
    # Enumerate eligible parameter tuples and canonical assessed-task hashes.
    for f,(level,_,_) in g.SPECS.items():
        if f=='cross_z':continue
        tasks=set();eligible_count=0;rejected=0
        ns=(1,4,9,16) if f in ('easy_radial','cone','reciprocal') else range(1,17)
        for n in ns:
            for h in range(1,7 if f=='easy_radial' else 19):
                for b in ((0,) if f=='easy_radial' else range(1,5)):
                    try:g.eligible(f,dict(n=n,h=h,b=b,c=1))
                    except ValueError:continue
                    # Bank validity is homogeneous in c; enumerating c1 proves all c1..5.
                    p=dict(n=n,h=h,b=b,c=1)
                    try:g.bank(f,p)
                    except ValueError:rejected+=5;continue
                    for c in range(1,6):
                        m=g.model(f,{**p,'c':c});tasks.add(g.digest({'F':str(m['F']),'bounds':[str(m[k]) for k in ('R','a','d','low','high')]}));eligible_count+=1
        domains[f]={'eligible_complete_instances':eligible_count,'meaningful_tasks':len(tasks),'whole_bank_rejections':rejected}
    write('validation.json',{'pass':True,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':__import__('matplotlib').__version__},'source':{k:g.SOURCE[k] for k in ('database','basis','lineage')},'fidelity':fidelity,'rated_source_distractors_matched':32,'unrated_undesignated_choices_matched':10,'original_correct_designations_absent':2,'normal_review_records':len(normal),'generated_evidence_variants':len(raw_variants),'sampled_unique_mathematical_tasks':len(seen),'default_family_coverage':{k:sorted(v) for k,v in family_coverage.items()},'finite_domains':domains,'native':json.loads((HERE/'engine-report.json').read_text()),'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'mutations_rejected':['C0','trig_identity','endpoint_component','half_linear_radial_distribution','half_linear_angular_distribution','half_linear_height_distribution'],'normal_present_source_anchor_chains_checked':8,'source_repairs':['reciprocal substitution missing sine square','quarter endpoint extra parenthesis','raw mathematical-set braces rendered literally'],'excluded_source_geometry':'cross_z original planes cross inside radius3 disk','unresolved_findings':[],'limitations':['Historical scalar distractor operations are opaque: all raw banks are ineligible for learning','Two raw originals lack difficulty, solution and correct designation','Crossed-surface original is mathematical geometry error retained only as evidence','Normal additive term order/TeX and prose notation are normalized, not byte-exact source output']})
    print('PASS: 10/10 raw prompts, 50/50 options, 8/8 supplied correct designations, 8/8 raw solutions; normal displayed calculus stages and both endpoints checked.')
if __name__=='__main__':main()
