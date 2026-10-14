#!/usr/bin/env python3
"""Independent read-back of actual learner TeX, source fidelity, native radio QA.
No database clients. Only this evidence directory is written.
"""
from pathlib import Path
import importlib.util,json,re,sys,subprocess,hashlib,itertools,copy
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor

ROOT=Path(__file__).resolve().parent
SCRIPT=ROOT.with_suffix('.py')
spec=importlib.util.spec_from_file_location('segment_generator',SCRIPT)
g=importlib.util.module_from_spec(spec);sys.modules[spec.name]=g;spec.loader.exec_module(g)
T,X,Y=g.T,g.X,g.Y
I,J,A,B=s.symbols('i j a b')
LOCAL={'t':T,'x':X,'y':Y,'i':I,'j':J,'a':A,'b':B,'E':s.E,'sqrt':s.sqrt,'log':s.log,'cos':s.cos,'sin':s.sin}
TRANS=standard_transformations+(implicit_multiplication_application,convert_xor)

def assert_equal(a,b,why):
    assert s.simplify(a-b)==0,(why,str(a),str(b))

def group_at(z,at):
    assert z[at]=='{'
    depth=1;k=at+1
    while depth:
        assert k<len(z),'unbalanced TeX group'
        depth+=int(z[k]=='{')-int(z[k]=='}');k+=1
    return z[at+1:k-1],k

def expression(z):
    z=z.strip().rstrip('.,')
    z=z.replace(r'\operatorname{ln}','log').replace(r'\operatorname{cos}','cos').replace('⁡','')
    z=z.replace(r'\,','').replace(r'\left','').replace(r'\right','')
    # Recursively convert full mathematical components, never replace short
    # variable names across prose or differential/function labels.
    while r'\frac' in z or r'\sqrt' in z:
        matches=list(re.finditer(r'\\(?:frac|sqrt)',z));m=matches[-1]
        a,end=group_at(z,m.end())
        if m.group()==r'\frac':
            b,end=group_at(z,end);replacement='(('+a+')/('+b+'))'
        else:replacement='sqrt('+a+')'
        z=z[:m.start()]+replacement+z[end:]
    z=z.replace('{','(').replace('}',')').replace('[','(').replace(']',')')
    z=re.sub(r'\be\b','E',z)
    z=re.sub(r'(cos|log)\s*([+-]?(?:\d+)?[txy])',r'\1(\2)',z)
    z=re.sub(r'(cos|log)\s*(-?\d+)(?=$|[+\-)])',r'\1(\2)',z)
    z=re.sub(r'(\d|\))([ijtxy])',r'\1*\2',z)
    assert '\\' not in z,('unsupported actual TeX',z)
    out=parse_expr(z,local_dict=LOCAL,transformations=TRANS,evaluate=True)
    assert out.free_symbols<={T,X,Y,I,J,A,B},('unexpected symbol',z,out)
    return out

def integral(z):
    marker=r'{\int }_{0}^{1}'
    assert z.count(marker)==1,('bounds/integral',z)
    factor,inside=z.split(marker)
    assert inside.endswith(r'\text{d}t') or inside.endswith(r'\text{d}t.')
    inside=inside.removesuffix('.').removesuffix(r'\text{d}t').removesuffix(r'\,')
    # Product row contains \cdot speed\cdot; final answer has outside factor.
    inside=inside.strip().removesuffix(r'\cdot').strip().replace(r'\cdot','*')
    return (expression(factor) if factor else s.Integer(1),expression(inside))

def formatting(z):
    assert all(ord(c)>=32 or c in '\n\t' for c in z),'control character'
    assert z.count('$')%2==0,'math delimiters'
    stack=0
    for k,c in enumerate(z):
        if c in '{}' and (k==0 or z[k-1]!='\\'):
            stack+=1 if c=='{' else -1
            assert stack>=0,'TeX brace'
    assert stack==0,'TeX brace'

def verify(record):
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    assert record['knowledge_point']['db_id']==g.KP_ID
    q=record['question'];sol=q[':question/worked-solution'];prompt=q[':question/problem']
    fields=q[':question/answer-fields'];assert len(fields)==1
    field=fields[0];assert field[':answer-field/type']==':answer-field.type/radio'
    for z in [prompt,sol]+[a[':answer/value'] for a in field[':answer-field/choices']]:formatting(z)
    assert sol.count('$$')==10 and sol.count(r'\begin{aligned}')==4
    assert 'Evaluate' not in prompt and 'We can solve this' not in sol
    # Independent function and segment read from the actual learner prompt.
    f=expression(re.search(r'\$f\(x,y\)=(.*?),\$',prompt).group(1))
    coords=re.search(r'from \$\((.*?)\)\$ to \$\((.*?)\)\?\$',prompt)
    ax,ay=[expression(z) for z in coords[1].split(',')]
    bx,by=[expression(z) for z in coords[2].split(',')]
    dx,dy=bx-ax,by-ay;L=s.sqrt(dx**2+dy**2)
    assert L>0
    param=re.search(r'Thus, we have that \$x=(.*?)\$ and \$y=(.*?)\$',sol)
    xt,yt=expression(param[1]),expression(param[2])
    assert_equal(xt,ax+dx*T,'displayed x(t)');assert_equal(yt,ay+dy*T,'displayed y(t)')
    assert_equal(xt.subs(T,0),ax,'direction t0x');assert_equal(yt.subs(T,1),by,'direction t1y')
    for lg in f.atoms(s.log):assert min(lg.args[0].subs({X:ax,Y:ay}),lg.args[0].subs({X:bx,Y:by}))>0
    av,bv=ax*I+ay*J,bx*I+by*J
    vectors=re.search(r'are \$a=(.*?)\$ and \$b=(.*?)\.\$',sol)
    assert_equal(expression(vectors[1]),av,'initial position vector')
    assert_equal(expression(vectors[2]),bv,'terminal position vector')
    blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)
    rows=[b.split(r' \\ ') for b in blocks]
    # Every line-parametrization row including the symbolic formula and masks.
    for row in rows[0]:
        z=expression(row.split('& =')[1]).subs({A:av,B:bv})
        assert_equal(z,xt*I+yt*J,'operative parameter vector row')
    drows=rows[1]
    differentiated=re.findall(r'\\frac\{\\text\{d\}\}\{\\text\{d\}t\}\((.*?)\)[ij]',drows[1])
    assert len(differentiated)==2
    assert_equal(expression(differentiated[0]),xt,'displayed derivative input x')
    assert_equal(expression(differentiated[1]),yt,'displayed derivative input y')
    assert_equal(expression(drows[2].split('& =')[1]),s.diff(xt,T)*I+s.diff(yt,T)*J,'derivative vector')
    assert drows[0]==r"{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j"
    assert drows[3]==r'‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}}'
    for row in drows[4:]:assert_equal(expression(row.split('& =')[1]),L,'speed row')
    pull=s.expand(f.subs({X:xt,Y:yt},simultaneous=True))
    assert len(rows[2])==2,'source substitution and collection stages required'
    for row in rows[2]:assert_equal(expression(row.split('& =')[1]),pull,'full function substitution')
    # Enforce substituted operation structure, not merely two equal rows.
    fam=record['generation']['template'];first=rows[2][0]
    if fam=='quadratic':assert ')^{2}-(' in first
    if fam=='log':assert r'\operatorname{ln}⁡(' in first and '+' in first
    if fam=='cos':assert '=1+(' in first and r'-\operatorname{cos}⁡' in first
    if fam=='linear':assert '=2(' in first and ')+(' in first
    if fam=='exp':assert first.startswith('f(r(t)) & ={e}^{')
    assert len(rows[3])==3
    assert rows[3][0]==r'{\int }_{C}f(x,y)\,\text{d}s & ={\int }_{0}^{1}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t'
    for row in rows[3][1:]:
        factor,inner=integral(row.split('& =')[1]);assert_equal(factor*inner,L*pull,'weighted integral stage')
    expected=s.integrate(L*pull,(T,0,1))
    vals=[];correct=None
    answers=field[':answer-field/choices'];assert len(answers)==5
    assert len({a[':answer/id'] for a in answers})==5
    for a in answers:
        assert a[':answer/type']==':answer.type/math'
        factor,inner=integral(a[':answer/value'])
        assert factor.is_real and factor>0
        for lg in inner.atoms(s.log):assert min(lg.args[0].subs(T,0),lg.args[0].subs(T,1))>0
        val=s.integrate(factor*inner,(T,0,1));vals.append(val)
        is_correct=g.equal_values(val,expected)
        assert is_correct==(a[':answer/id']==field[':answer-field/correct'][1]),'designation vs actual definite value'
        if is_correct:correct=a
    assert correct is not None
    for i,val in enumerate(vals):
        for other in vals[:i]:assert not g.equal_values(val,other),'two actual definite values coincide'
    assert record['generation']['parameter_fingerprint']==g.task_fingerprint(pull,L)
    assert re.search(r'where \$0\\le t\\le 1\.\$',sol)
    return 10

ANCHORS=[dict(ax=0,ay=2,bx=3,by=1),dict(ax=1,ay=3,bx=0,by=3),dict(ax=-1,ay=1,bx=1,by=2),dict(ax=-3,ay=1,bx=2,by=3),dict(ax=0,ay=0,bx=-3,by=4)]

def source_cases(source):
    return [{'source_id':q[':question/math-academy-id'],'template':f,'level':'easy','parameters':p,'bank_profile':f+'_observed'} for f,q,p in zip(g.FAMILIES,source,ANCHORS)]

def main():
    wrapper=json.loads((ROOT/'source.json').read_text());source=wrapper['record'][':knowledge-point/questions']
    assert wrapper['basis']==2275
    immutable=ROOT.parents[1]/'runs/current/refresh-2026-10-14/sources/17592186179724.json'
    assert (ROOT/'source.json').read_bytes()==immutable.read_bytes()
    cases=source_cases(source);(ROOT/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
    original_records=[];review=[];fidelity=[];pair_checks=0
    for case,q in zip(cases,source):
        r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])
        rq=r['question'];sf=q[':question/answer-fields'][0];rf=rq[':question/answer-fields'][0]
        assert rq[':question/problem']==q[':question/problem']
        assert rq[':question/worked-solution']==q[':question/worked-solution']
        assert set(rq)=={':question/id',':question/difficulty',':question/problem',':question/worked-solution',':question/answer-fields'}
        original_values=sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
        assert sorted(a[':answer/value'] for a in rf[':answer-field/choices'])==original_values
        designated=next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1])
        assert designated==sf[':answer-field/correct'][':answer/value']
        assert sf[':answer-field/type'][':db/ident']==rf[':answer-field/type']
        pair_checks+=verify(r);original_records.append(r)
        fidelity.append({'source_id':case['source_id'],'prompt_exact':True,'solution_exact':True,'exact_options':5,'distractors_matched':4,'correct_designation':True,'complete_bank':True})
        review.append({'role':'observed source replay','source_id':case['source_id'],'original':q,'generated':r})
        # One changed-parameter replay per entire observed profile.
        changed=g.generate('easy',seed=37,template=case['template'],profile=case['bank_profile'])
        pair_checks+=verify(changed);review.append({'role':'changed-parameter observed empirical evidence','generated':changed})
    records=[];coverage={};tasks={};identity_checks=0
    for level in ('easy','moderate','hard'):
        families=set();fps=set()
        for seed in range(60):
            r=g.generate(level,seed);pair_checks+=verify(r);records.append(r)
            families.add(r['generation']['template']);fps.add(r['generation']['parameter_fingerprint'])
            if seed<2:review.append({'role':'authored '+level+' variant','generated':r})
        assert families==set(g.FAMILIES),'default sampler silently omitted family'
        coverage[level]=sorted(families);tasks[level]=len(fps)
        for fam in g.FAMILIES:
            r=g.generate(level,seed=19,template=fam);pair_checks+=verify(r)
            review.append({'role':'authored '+level+' family demonstration','generated':r})
            same=g.generate(level,seed=999,template=fam,parameters=r['generation']['parameters'],profile=r['generation']['bank_profile'])
            assert same['question'][':question/id']==r['question'][':question/id'];identity_checks+=1
    # Regression mutations must be detected by read-back, not metadata.
    mutations=[]
    base=original_records[0]
    for label,old,new in [('coordinate','x=3t','x=2t'),('derivative',' & =3\\,i-j',' & =2\\,i-j'),('substitution','(3t)^{2}-(2-t)','(2t)^{2}-(2-t)'),('bounds','{\\int }_{0}^{1}','{\\int }_{1}^{0}'),('control','We will','We\x0cwill')]:
        r=copy.deepcopy(base);r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace(old,new)
        try:verify(r)
        except (AssertionError,ValueError):mutations.append(label)
        else:raise AssertionError('mutation escaped '+label)
    # Equivalent values despite unequal integrands, reparameterization and scale.
    assert g.equal_values(s.integrate(T,(T,0,1)),s.integrate(1-T,(T,0,1)))
    assert g.equal_values(s.integrate(2*T,(T,0,1)),2*s.integrate(T,(T,0,1)))
    for level,bad in [('easy',dict(ax='1/2',ay=1,bx=2,by=3)),('moderate',dict(ax=0,ay=1,bx=2,by=3)),('hard',dict(ax='1/2',ay=1,bx=2,by=3))]:
        try:g.generate(level,template='linear',parameters=bad)
        except ValueError:pass
        else:raise AssertionError('explicit workload bounds bypassed')
    engine=[]
    for n,r in enumerate(original_records+records):
        field=r['question'][':question/answer-fields'][0]
        engine.append({'label':'segment-'+str(n),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==field[':answer-field/correct'][1] else 'rejected','purpose':'actual owned radio answer selection; independent integral mathematics checked separately'} for a in field[':answer-field/choices']]})
    (ROOT/'engine-input.json').write_text(json.dumps(engine,ensure_ascii=False,indent=2)+'\n')
    harness=ROOT.parents[1]/'runs/current/check-engine'
    subprocess.run([str(harness),str(ROOT/'engine-input.json'),str(ROOT/'engine-validation.json')],check=True)
    engine_result=json.loads((ROOT/'engine-validation.json').read_text())
    # Conservative fully enumerated all-family capacity slices, excluding
    # translations, reverse traversal and bank aliases from task identities.
    capacities={};slice_counts={};capacity_family={}
    for level in ('easy','moderate','hard'):
        fps=set();valid=0
        counts={}
        for family in g.FAMILIES:
            family_fps=set()
            for ax,dx,dy in itertools.product(((-2,0,2) if family!='exp' else (0,)),(-3,-2,-1,1,2,3),(-3,-2,-1,1,2,3)):
                ay=0 if family=='exp' else 1
                if family=='log':ax+=3;ay=3
                p={'ax':str(ax),'ay':str(ay),'bx':str(ax+dx),'by':str(ay+dy)}
                if level!='easy':p['bx']=str(s.Rational(p['bx'])+s.Rational(1,2))
                if level=='hard':p['by']=str(s.Rational(p['by'])+s.Rational(1,3))
                try:
                    checked=g.parameters_checked(level,family,p)
                    g.bank(family,checked,family+'_method')
                except ValueError:continue
                _,_,_,_,_,_,_,_,pull,L=g.components(family,checked)
                fp=g.task_fingerprint(pull,L)
                valid+=1;fps.add(fp);family_fps.add(fp)
            counts[family]=len(family_fps)
        capacities[level]=len(fps);slice_counts[level]=valid
        capacity_family[level]=counts
    assert min(capacities.values())>=100,'insufficient meaningful same-method variety'
    (ROOT/'review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
    md=['# Line segment construction review','Worker draft; parent QA remains required.','Observed originals below preserve source problem, every choice and the full fixed solution. Empirical evidence profiles are ineligible for ordinary learner generation.']
    for item in review:
        md+=['## '+item['role']+' — '+item['generated']['generation']['template']]
        if 'original' in item:
            q=item['original'];md+=['### Immutable original '+item['source_id'],q[':question/problem']]+['- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices']]+[q[':question/worked-solution']]
        md+=['### Parameterized generator',g.markdown(item['generated'])]
    (ROOT/'review.md').write_text('\n\n'.join(md)+'\n')
    result={'status':'worker validation passed; pending independent parent QA','source_basis':2275,'source_wrapper_sha256':hashlib.sha256((ROOT/'source.json').read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'source_practice_count':5,'fidelity':fidelity,'matched_complete_banks':5,'matched_choices':25,'matched_distractors':20,'exact_prompts':5,'exact_solutions':5,'designations':5,'source_errors':[],'authored_levels':['moderate','hard'],'authored_banks':5,'observed_profiles':5,'default_family_coverage':coverage,'sample_counts':{l:60 for l in coverage},'sample_unique_tasks':tasks,'capacity_lower_bound_by_level':capacities,'capacity_slice_valid_instances':slice_counts,'capacity_family_lower_bounds':capacity_family,'capacity_basis':'enumerated bounded coordinate slice across all five families; mathematical weighted pullbacks canonicalized against t->1-t, no profile/bank/label/translation aliases counted','independent_actual_display_pair_checks':pair_checks,'identity_seed_checks':identity_checks,'mutation_regressions':mutations,'native_accepted':engine_result['accepted_checks'],'native_rejected':engine_result['rejected_checks'],'native_unresolved':engine_result['documented_unresolved_checks'],'engine_sha256':hashlib.sha256(harness.read_bytes()).hexdigest(),'python':sys.version.split()[0],'sympy':s.__version__,'plots':'none','calculator_flag':'unknown; not inferred','database_writes':0,'unresolved':['Historical distractor intent underidentified; explicit observed profiles retain empirical operation patterns, excluded from learner defaults.','Moderate/hard grades are conservative authored rational-bookkeeping definitions, not recovered source labels.']}
    (ROOT/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
