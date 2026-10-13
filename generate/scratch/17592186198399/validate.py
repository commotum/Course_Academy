#!/usr/bin/env python3
"""Independent checks read the actual displayed mathematics, not answer metadata."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
H=Path(__file__).parent;ROOT=H.parents[2]
spec=importlib.util.spec_from_file_location('volume_generator',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,z=s.symbols('x y z',real=True);u,v,w=s.symbols('u v w',positive=True);XYZ=(x,y,z);UVW=(u,v,w)
TRANS=standard_transformations+(implicit_multiplication_application,)

def parse(t):
    t=t.strip().rstrip('.').replace('⁡','').replace('∂',r'\partial').replace(r'\operatorname{ln}',r'\ln')
    t=t.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*')
    # Current decoded source choice commands have single backslash bytes.
    # Defensive evidence normalization is separate from normal formatting.
    t=t.replace('\\\\','\\')
    def group_at(pos):
        assert t[pos]=='{',(t,pos);start=pos;depth=1;pos+=1
        while depth:
            depth+=(t[pos]=='{')-(t[pos]=='}');pos+=1
        return t[start+1:pos-1],pos
    while r'\sqrt[' in t:
        pos=t.rfind(r'\sqrt[');end=t.index(']',pos);degree=t[pos+6:end];a,end2=group_at(end+1)
        t=t[:pos]+'(('+a+')**(1/('+degree+')))'+t[end2:]
    while r'\frac' in t:
        pos=t.rfind(r'\frac');a,end=group_at(pos+5);b,end2=group_at(end)
        t=t[:pos]+'(('+a+')/('+b+'))'+t[end2:]
    t=t.replace(r'\sqrt','sqrt').replace(r'\ln','log').replace('{','(').replace('}',')').replace('^','**')
    t=re.sub(r'log(\d+)',r'log(\1)',t)
    assert '\\' not in t,('Unparsed command',t)
    return parse_expr(t,local_dict=dict(zip(('x','y','z','u','v','w'),XYZ+UVW))|{'log':s.log,'sqrt':s.sqrt},transformations=TRANS)
def equal(a,b):assert s.simplify(a-b)==0,(a,b,s.simplify(a-b))
def shape(r,raw=False):
    assert set(r['knowledge_point'])=={'db_id','id','title'};assert r['knowledge_point']['db_id']==g.KP_ID
    uuid_re=r'[a-f0-9]{8}(?:-[a-f0-9]{4}){3}-[a-f0-9]{12}'
    assert re.fullmatch(uuid_re,r['question'][':question/id'])
    for field in r['question'][':question/answer-fields']:
        assert field[':answer-field/type']==':answer-field.type/radio'
        assert len(field[':answer-field/choices'])==5
        ids=[a[':answer/id'] for a in field[':answer-field/choices']];assert len(set(ids))==5
        if ':answer-field/correct' in field:assert field[':answer-field/correct'][0]==':answer/id' and field[':answer-field/correct'][1] in ids
        for a in field[':answer-field/choices']:
            assert re.fullmatch(uuid_re,a[':answer/id']);assert a[':answer/type']==':answer.type/math';assert '$' not in a[':answer/value']
            if not raw:assert '\\\\' not in a[':answer/value']
    for key in (':question/problem',':question/worked-solution'):
        if key not in r['question']:continue
        text=r['question'][key];assert text.count('$$')%2==0
        for chunk in text.split('$$')[::2]:assert chunk.count('$')%2==0
        depth=0
        for i,c in enumerate(text):
            if c in '{}':
                n=0;j=i-1
                while j>=0 and text[j]=='\\':n+=1;j-=1
                if n%2==0:depth+=(c=='{')-(c=='}');assert depth>=0
        assert depth==0
        assert '@@' not in text and '--' not in text and '+-' not in text

def read_prompt(r):
    text=r['question'][':question/problem']
    # Original first/last raw tokens vary but every inequality has complete bounds.
    if r['generation']['evidence_only']:
        exprs=g.RAW[str(r['generation']['source_id'])]['family']
        p={k:s.sympify(v) for k,v in r['generation']['resolved_model_parameters'].items()}
        # Full-component masks are independently checked below at stretch h=2..4.
        trans=g.model(exprs,p)['trans'];bounds=tuple((p['l'+q],p['h'+q]) for q in 'uvw')
        return trans,bounds
    text=text.split(r'\, :\, ')[1].split(r'\big\}')[0]
    inequalities=text.split(r',\quad ');assert len(inequalities)==3
    parts=[a.split(r'\le ') for a in inequalities];assert all(len(a)==3 for a in parts)
    return tuple(parse(a[1]) for a in parts),tuple((parse(a[0]),parse(a[2])) for a in parts)

def matrix_parse(t):
    t=t.removeprefix(r'\begin{vmatrix}').removesuffix(r'\end{vmatrix}')
    rows=t.split(r' \\ ');return s.Matrix([[parse(q) for q in row.split(' & ')] for row in rows])

def normal_math(r):
    shape(r);trans,bounds=read_prompt(r)
    sol=r['question'][':question/worked-solution'];blocks=sol.split('$$')[1::2]
    inverse_block=next(b for b in blocks if 'T(u,v,w)=' in b)
    inverse=tuple(parse(q) for q in inverse_block.split('=',1)[1].strip().rstrip('.').removeprefix(r'\left(').removesuffix(r'\right)').split(','))
    for target,q in zip(UVW,trans):equal(q.subs(dict(zip(XYZ,inverse)),simultaneous=True),target)
    # Positive nonlinear branch is taken directly from printed region.
    for i,(lo,hi) in enumerate(bounds):assert hi>lo
    M=s.Matrix(trans).jacobian(XYZ);det=s.factor(M.det());assert det!=0
    jacblock=next(b for b in blocks if r'\begin{vmatrix}' in b and r'\partial(u,v,w)' in b)
    matrices=re.findall(r'\\begin\{vmatrix\}(.*?)\\end\{vmatrix\}',jacblock,re.S)
    assert len(matrices)==5 # formal9, derivative9, all three cofactors
    printed=matrix_parse(r'\begin{vmatrix}'+matrices[1]+r'\end{vmatrix}');assert printed==M
    for j in range(3):assert matrix_parse(r'\begin{vmatrix}'+matrices[j+2]+r'\end{vmatrix}')==M.minor_submatrix(0,j)
    formal_expected=r' \\ '.join(' & '.join(r'\frac{\partial '+str(a)+r'}{\partial '+str(b)+'}' for b in XYZ) for a in UVW)
    assert matrices[0]==formal_expected
    jacrows=jacblock.split(r' \\  & =')
    # Every coefficient and cofactor sign must be present, not only minors.
    cofactor=jacrows[-3] if len(jacrows)==5 else jacrows[-2]
    for j in range(3):assert g.group(g.tex(M[0,j]))+r'(-1)^{1+'+str(j+1)+'}' in cofactor
    reduced_cofactor=cofactor
    for rawminor in re.findall(r'\\begin\{vmatrix\}(.*?)\\end\{vmatrix\}',cofactor,re.S):
        whole=r'\begin{vmatrix}'+rawminor+r'\end{vmatrix}'
        reduced_cofactor=reduced_cofactor.replace(whole,'('+str(matrix_parse(whole).det())+')')
    equal(parse(reduced_cofactor),det)
    detuv=s.simplify(det.subs(dict(zip(XYZ,inverse)),simultaneous=True));J=s.simplify(s.Abs(s.Matrix(inverse).jacobian(UVW).det()))
    determinant_rows=[row.strip().removesuffix(r'\end{aligned}') for row in jacrows]
    equal(parse(determinant_rows[3]),det)
    if len(determinant_rows)==5:equal(parse(determinant_rows[4]),detuv)
    substitution=next(b for b in blocks if b.strip().startswith('u='))
    for t,q in zip(substitution.strip().rstrip('.').split(r',\quad '),trans):equal(parse(t.split('=',1)[1]),q)
    domain=next(b for b in blocks if b.strip().startswith(r'\Delta='))
    domainparts=domain.split(':',1)[1].split(r'\big\}')[0].split(r',\quad ')
    for part,var,(lo,hi) in zip(domainparts,UVW,bounds):
        tokens=part.split(r'\le ');assert tokens[1]==str(var);equal(parse(tokens[0]),lo);equal(parse(tokens[2]),hi)

    jblock=next(b for b in blocks if r'\right)^{-1}=' in b);printedjac=parse(jblock.split('=')[-1]);equal(printedjac,s.Matrix(inverse).jacobian(UVW).det())
    last=blocks[-1];rows=re.split(r' \\\\ ',last.strip().removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}'))
    assert len(rows)==7,rows
    rowvals=[row.split(' & =',1)[1] for row in rows]
    # Read density and ALL endpoints from the printed repeated integral.
    repeated=rowvals[1];pattern=r'\\int_\{(.*?)\}\^\{(.*?)\}'
    parsedbounds=[(parse(lo),parse(hi)) for lo,hi in re.findall(pattern,repeated)];assert tuple(parsedbounds)==bounds
    density=parse(re.sub(pattern,'',repeated).split(r'\,\mathrm{d}')[0]);equal(density,J)
    V=s.integrate(J,(w,*bounds[2]),(v,*bounds[1]),(u,*bounds[0]))
    # Separated formal integral row recomputed from its actual factors.
    sep=rowvals[2].split(r'\cdot ');constant=parse(sep[0]);factorvalues=[]
    for factor,t,b in zip(sep[1:],UVW,bounds):
        found=re.findall(pattern,factor);assert len(found)==1;lo,hi=map(parse,found[0]);assert (lo,hi)==b
        f=parse(re.sub(pattern,'',factor).split(r'\,\mathrm{d}')[0]);factorvalues.append(s.integrate(f,(t,lo,hi)))
    equal(constant*s.prod(factorvalues),V)
    # Primitive row has exactly three actual primitives, each derivative checked.
    primitiveparts=rowvals[3].split(r'\cdot ');equal(parse(primitiveparts[0]),constant)
    primitive_values=[]
    for part,t,(lo,hi) in zip(primitiveparts[1:],UVW,bounds):
        found=re.fullmatch(r'\[(.*?)\]_\{(.*?)\}\^\{(.*?)\}',part);assert found,part
        P=parse(found[1]);equal(s.diff(P,t),density if density.has(t) else 1);equal(parse(found[2]),lo);equal(parse(found[3]),hi)
        primitive_values.append(P.subs(t,hi)-P.subs(t,lo))
    equal(constant*s.prod(primitive_values),V)
    # Endpoint rows must retain each individual upper and lower primitive value,
    # rather than merely have a total that happens to be correct.
    for renderedrow in rowvals[4:6]:
        components=renderedrow.split(r'\cdot ');equal(parse(components[0]),constant);assert len(components)==4
        for component,part,t,(lo,hi) in zip(components[1:],primitiveparts[1:],UVW,bounds):
            P=parse(re.fullmatch(r'\[(.*?)\]_\{(.*?)\}\^\{(.*?)\}',part)[1])
            plain=component.replace(r'\left','').replace(r'\right','');assert plain[0]=='(' and plain[-1]==')'
            plain=plain[1:-1];depth=0;split=None
            for i,ch in enumerate(plain):
                if ch in '({':depth+=1
                elif ch in ')}':depth-=1
                elif ch=='-' and depth==0:split=i;break
            assert split is not None,component
            equal(parse(plain[:split]),P.subs(t,hi));equal(parse(plain[split+1:]),P.subs(t,lo))
    # Independently evaluate BOTH substituted and individually evaluated endpoint rows.
    for row in rowvals[4:]:equal(parse(row),V)
    field=r['question'][':question/answer-fields'][0];values=[parse(a[':answer/value']) for a in field[':answer-field/choices']]
    assert all(a.is_positive is True for a in values)
    assert all(s.simplify(a-b)!=0 for i,a in enumerate(values) for b in values[i+1:])
    chosen=next(a for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1]);equal(parse(chosen[':answer/value']),V)
    return V

def fidelity():
    counts=dict(questions=0,prompts=0,solutions=0,solution_denominator=0,banks=0,options=0,correct_designations=0,missing_designations=0)
    for case in json.load(open(H/'source-cases.json')):
        r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);shape(r,True)
        source=next(q for q in g.RECORD[':knowledge-point/questions'] if q[':db/id']==case['source_id']);q=r['question'];counts['questions']+=1
        assert q[':question/problem']==source[':question/problem'];counts['prompts']+=1
        for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in source)==(key in q)
        if ':question/worked-solution' in source:
            counts['solution_denominator']+=1;assert q[':question/worked-solution']==source[':question/worked-solution'];counts['solutions']+=1
        for a,b in zip(q[':question/answer-fields'],source[':question/answer-fields']):
            assert (':answer-field/correct' in a)==(':answer-field/correct' in b)
            observed=[parse(c[':answer/value']) for c in b[':answer-field/choices']];generated=[parse(c[':answer/value']) for c in a[':answer-field/choices']]
            assert len(observed)==len(generated)==5
            for value in observed:assert sum(s.simplify(value-e)==0 for e in generated)==1
            counts['banks']+=1;counts['options']+=5
            if ':answer-field/correct' in b:
                correct=next(c for c in a[':answer-field/choices'] if c[':answer/id']==a[':answer-field/correct'][1]);equal(parse(correct[':answer/value']),parse(b[':answer-field/correct'][':answer/value']));counts['correct_designations']+=1
            else:counts['missing_designations']+=1
        # Public changed-parameter replay checks every exact mathematical component
        # and the final row using an independently computed geometric volume.
        for h in (2,3,4):
            variant=g.generate(case['level'],template=case['template'],parameters={'h':h},profile=case['bank_profile']);shape(variant,True)
            rp=variant['generation']['resolved_model_parameters'];p={k:s.sympify(v) for k,v in rp.items()};m=g.model(case['template'],p)
            inv=s.Matrix(m['inverse']).jacobian(g.UVW);independent=s.integrate(s.Abs(inv.det()),(g.w,*m['bounds'][2]),(g.v,*m['bounds'][1]),(g.u,*m['bounds'][0]));equal(independent,m['volume'])
            if ':question/worked-solution' in variant['question']:
                sol=variant['question'][':question/worked-solution'];mats=re.findall(r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|',sol,re.S)
                assert len(mats)>=2
                actual=s.Matrix([[parse(e) for e in row.split(' & ')] for row in mats[1].split(r' \\ ')])
                # The raw source uses x,y,z symbolic names but w,u proxy assumptions
                # do not enter these ordered derivatives.
                expected=s.Matrix(m['trans']).jacobian(g.XYZ)
                assert actual==expected
                sourceblocks=sol.split('$$')[1::2]
                detrows=sourceblocks[7].split(r' \\  & =')
                equal(parse(detrows[-1].strip().removesuffix(r'\end{aligned}')),m['detuv'])
                if len(detrows)==5:equal(parse(detrows[-2]),m['det'])
                equal(parse(sourceblocks[8].rsplit('=',1)[1]),m['jac'])
                if len(mats)>2:
                    actualminor=s.Matrix([[parse(e) for e in row.split(' & ')] for row in mats[2].split(r' \\ ')])
                    assert actualminor==expected.minor_submatrix(0,0)
                last=variant['question'][':question/worked-solution'].rsplit(' & =',1)[1].split(r'.\end{aligned}')[0];equal(parse(last),independent)
            assert variant['generation']['evidence_only'] and not variant['generation']['eligible_for_learning']
    return counts

def main():
    counts=fidelity();reviews=[];checks=[];coverage={};fingerprints={level:set() for level in g.FAMILIES}
    for level,fs in g.FAMILIES.items():
        for f in fs:
            for seed in range(24):
                r=g.generate(level,seed,template=f);normal_math(r);fingerprints[level].add(r['generation']['math_fingerprint'])
                # Fixed inputs/order retain content and owned IDs.
                p=r['generation']['parameters'];other=g.generate(level,seed+1000,template=f,parameters=p,profile=r['generation']['profile']);assert r['question'][':question/id']==other['question'][':question/id']
                field=r['question'][':question/answer-fields'][0]
                checks.append({'label':level+'/'+f+'/'+str(seed),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==field[':answer-field/correct'][1] else 'rejected','purpose':'owned radio option'} for a in field[':answer-field/choices']]})
                if seed<2:reviews.append(r)
            coverage[level+'/'+f]=24
    defaultcoverage={level:set() for level in g.FAMILIES}
    for level in g.FAMILIES:
        for seed in range(40):
            r=g.generate(level,seed);defaultcoverage[level].add(r['generation']['template']);normal_math(r)
        assert defaultcoverage[level]==set(g.FAMILIES[level])
    # Negative public guards and whole bank collision rejection.
    rejected=0
    for level,fs in g.FAMILIES.items():
        for f in fs:
            r=g.generate(level,template=f);p=r['generation']['parameters'];bad=dict(p);bad['a']='0'
            try:g.generate(level,template=f,parameters=bad)
            except ValueError:rejected+=1
            else:raise AssertionError('Invalid explicit parameter accepted')
    # Level-specific limits and whole-bank rejection hold for explicit inputs.
    for level,f,updates in [('easy','affine',{'lu':'1'}),('moderate','shear',{'a':'-4'}),('hard','log',{'lu':'0'}),('hard','sqrt',{'lw':'0'}),('hard','reciprocal',{'lu':'0'}),('hard','cube',{'hw':'3'})]:
        p=g.generate(level,template=f)['generation']['parameters'];p.update(updates)
        try:g.generate(level,template=f,parameters=p)
        except ValueError:rejected+=1
        else:raise AssertionError('Level/domain limit bypassed')
    p=g.generate('moderate',template='shear')['generation']['parameters'];p.update(lu='0',hu='5')
    try:g.generate('moderate',template='shear',parameters=p)
    except g.SampleRejected:rejected+=1
    else:raise AssertionError('Ambiguous whole bank accepted')
    # A simultaneous positive scaling of one complete coordinate inequality
    # changes notation/J bookkeeping but must not inflate region-task counts.
    p={'a':'2','b':'1','c':'2','d':'1','lu':'0','hu':'4','lv':'0','hv':'3','lw':'0','hw':'5'}
    a=g.generate('easy',template='affine',parameters=p)
    p.update(a='3',hu='6');b=g.generate('easy',template='affine',parameters=p)
    assert a['generation']['math_fingerprint']==b['generation']['math_fingerprint']
    assert a['question'][':question/id']!=b['question'][':question/id']
    # Printed mathematics mutation tests catch stage-specific errors.
    for stage in ('density','matrix','endpoint'):
        r=copy.deepcopy(reviews[0]);q=r['question'];sol=q[':question/worked-solution']
        if stage=='density':sol=sol.replace(g.tex(g.model('affine',{k:s.sympify(v) for k,v in r['generation']['parameters'].items()})['J'])+r'\,\mathrm{d}w','17'+r'\,\mathrm{d}w',1)
        elif stage=='matrix':sol=sol.replace(r'\begin{vmatrix}2 & 0 & 0',r'\begin{vmatrix}9 & 0 & 0',1)
        else:sol=sol.replace(r'\left(5\right)-\left(0\right)',r'\left(99\right)-\left(0\right)',1)
        if sol==q[':question/worked-solution']:continue
        q[':question/worked-solution']=sol
        try:normal_math(r)
        except AssertionError:pass
        else:raise AssertionError('Display mutation escaped validation')
    # Grade the five observed fields with actual correct designations. Missing
    # original designations cannot be passed to the harness or counted as graded.
    for case in json.load(open(H/'source-cases.json')):
        raw=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])
        raw['question'][':question/answer-fields']=[field for field in raw['question'][':question/answer-fields'] if ':answer-field/correct' in field]
        if not raw['question'][':question/answer-fields']:continue
        checks.append({'label':'confirmed original/'+str(case['source_id']),'record':raw,'checks':[{'field_index':n,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==field[':answer-field/correct'][1] else 'rejected','purpose':'Original designated owned option; legacy missing refs excluded'} for n,field in enumerate(raw['question'][':question/answer-fields']) for a in field[':answer-field/choices']]})
    (H/'engine-input.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(H/'engine-input.json'),str(H/'engine-report.json')],check=True)
    report={'status':'pass','source_fidelity':counts,'raw_profiles_eligible':0,'original_native_designated_fields':5,'original_native_ungraded_missing_correct_fields':2,'authored_generated_checked':sum(coverage.values()),'default_sample_checks':120,'family_coverage':coverage,'default_family_coverage':{k:sorted(v) for k,v in defaultcoverage.items()},'unique_math_tasks_in_family_QA':{k:len(v) for k,v in fingerprints.items()},'invalid_explicit_rejections':rejected,'native_grading':json.load(open(H/'engine-report.json')),'python':sys.version.split()[0],'sympy':s.__version__,'generator_sha256':hashlib.sha256(H.with_suffix('.py').read_bytes()).hexdigest(),'validator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'database_writes':0,'scope':'Volumes only; no nonconstant original integrands; step7 stop','unresolved_findings':['Two original fields omit correct refs; no original designation claimed for either.','Unrated reciprocal source has no solution/difficulty; authored hard normal completion only.','All historical wrong scalars have unresolved intended operations; raw banks ineligible, retained complete.','Raw reciprocal bank has a negative-volume option; normal banks require all positive.']}
    raw_review=[g.generate(case['level'],template=case['template'],profile=case['bank_profile'],parameters={'h':2}) for case in json.load(open(H/'source-cases.json'))]
    report['review_records']={'eligible_authored_defaults':len(reviews),'raw_ineligible_evidence_variants':len(raw_review)}
    (H/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(H/'review.json').write_text(json.dumps(reviews+raw_review,ensure_ascii=False,indent=2)+'\n')
    md=['# Review: originals and labeled generated variants\n']
    for case in json.load(open(H/'source-cases.json')):
        original=next(q for q in g.RECORD[':knowledge-point/questions'] if q[':db/id']==case['source_id']);md.extend(['## Original '+str(case['source_id'])+' — '+case['template'],original[':question/problem']])
        for field in original[':question/answer-fields']:md.append('Original complete bank: '+', '.join('$'+a[':answer/value'].replace('\\\\','\\')+'$' for a in field[':answer-field/choices']))
        md.append(original.get(':question/worked-solution','Original solution absent. Original difficulty/correct designation absent.'))
        md.extend(['### Generated raw evidence variant h=2 — ineligible',g.markdown(g.generate(case['level'],template=case['template'],profile=case['bank_profile'],parameters={'h':2}))])
    for r in reviews:md.extend(['## Authored/default '+r['question'][':question/difficulty'].split('/')[-1]+' — '+r['generation']['template'],g.markdown(r)])
    (H/'review.md').write_text('\n\n'.join(md)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='native_grading'},indent=2))
if __name__=='__main__':main()
