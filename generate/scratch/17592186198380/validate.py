#!/usr/bin/env python3
"""Failing fidelity, independent mathematics, layout, identity and native checks."""
import copy,hashlib,importlib.util,json,re,subprocess,sys,uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ROOT=Path(__file__).resolve().parent;PROJECT=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('flux_generator',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)


def latex(s):
    s=s.strip().rstrip('.').rstrip(',').replace(r'\,','').replace(r'\cdot','*').replace(r'\left','').replace(r'\right','')
    s=s.replace(r'\end{aligned}','').strip().rstrip('.')
    while r'\frac' in s:
        i=s.rfind(r'\frac');j=i+len(r'\frac')
        def brace(start):
            assert s[start]=='{'
            depth=1;end=start+1
            while depth:
                if s[end]=='{':depth+=1
                elif s[end]=='}':depth-=1
                end+=1
            return s[start+1:end-1],end
        numerator,j=brace(j);denominator,j=brace(j)
        s=s[:i]+'(('+numerator+')/('+denominator+'))'+s[j:]
    s=re.sub(r'\^\{([^{}]+)\}',r'**(\1)',s).replace('^','**').replace('{','(').replace('}',')')
    return parse_expr(s,local_dict=g.SYMBOLS,transformations=standard_transformations+(implicit_multiplication_application,))

def independent(p,math):
    u,v=g.u,g.v;r=[g.expr(t) for t in math['r']];F=[g.expr(t) for t in math['F']]
    ru=[sp.diff(t,u) for t in r];rv=[sp.diff(t,v) for t in r]
    N=[ru[1]*rv[2]-ru[2]*rv[1],ru[2]*rv[0]-ru[0]*rv[2],ru[0]*rv[1]-ru[1]*rv[0]]
    FF=[sp.expand(t.subs(dict(zip((g.x,g.y,g.z),r)),simultaneous=True)) for t in F]
    integrand=sp.expand(sum(a*b for a,b in zip(N,FF)))
    # Independent exact polynomial moment formula, no SymPy integrate or generator bank.
    C=sum(c*(p['u_max']**(i+1)-p['u_min']**(i+1))*(p['v_max']**(j+1)-p['v_min']**(j+1))/((i+1)*(j+1)) for (i,j),c in sp.Poly(integrand,u,v).terms())
    return {'ru':ru,'rv':rv,'normal':N,'composed':FF,'f':integrand,'correct':sp.simplify(C),'F':F}

def verify(record):
    q=record['question'];a=record['generation'];name=a['template'];p=g.exact_bounds(a['parameters']);m=independent(p,a['math'])
    assert record['knowledge_point']['db_id']==g.KP_ID
    assert q[':question/difficulty']==':question.difficulty/'+g.TEMPLATES[name]
    assert a['source_analysis']['basis']==1356 and a['domain']=='rectangle' and a['orientation']=='r_u cross r_v'
    assert a['plot_rating']=='none' and a['plot_assets']=={}
    assert g.digest({'template':name,'parameters':a['parameters']})==a['parameter_fingerprint']
    for key in ('ru','rv','normal','composed'):
        assert all(sp.simplify(g.expr(s)-t)==0 for s,t in zip(a['math'][key],m[key])),key
    assert sp.simplify(g.expr(a['math']['f'])-m['f'])==0
    assert sp.simplify(g.expr(a['math']['correct'])-m['correct'])==0
    assert q[':question/problem']==g.prompt(name,p,g.evaluate(name,p)), 'Prompt geometry/domain'
    solution=q[':question/worked-solution'];assert '<<' not in solution+q[':question/problem']
    assert solution.count('$$')%2==0 and q[':question/problem'].count('$$')%2==0
    assert '{{' not in q[':question/problem'];assert 'images/' not in solution
    # Parse every displayed evaluated vector in fixed source solution independently.
    prefix=solution.split('Therefore, the surface integral evaluates to')[0]
    candidates=[m[key] for key in ('ru','rv','normal','composed','F')]
    for vv in re.findall('⟨([^⟨⟩]+)⟩',prefix):
        if '∂' in vv or '|' in vv:continue
        vals=[latex(t) for t in vv.split(r'\,')]
        assert len(vals)==3
        assert any(all(sp.simplify(a-b)==0 for a,b in zip(vals,old)) for old in candidates),(name,vv)
    dot=prefix.split('we calculate the dot product')[1].split('$$')[1]
    if name in g.DATA:
        for row in dot.split(' & =')[1:]:
            if '⟨' in row:continue
            scalar=row.split(r' \\')[0]
            assert sp.simplify(latex(scalar)-m['f'])==0,(name,scalar)
    else:assert sp.simplify(latex(dot.split('=')[-1])-m['f'])==0
    # Parse displayed antiderivatives; verify both derivative and evaluated reductions.
    final=solution.split('Therefore, the surface integral evaluates to')[1]
    steps=a['solution_steps'];inside=g.SYMBOLS[steps['inner']];outside=g.v if inside==g.u else g.u;factor=g.expr(steps['factor'])
    primitive=g.expr(steps['primitive']);reduced=g.expr(steps['reduced']);op=g.expr(steps['outer_primitive'])
    assert sp.simplify(sp.diff(primitive,inside)-m['f']/factor)==0
    assert sp.simplify(primitive.subs(inside,p[inside.name+'_max'])-primitive.subs(inside,p[inside.name+'_min'])-reduced)==0
    assert sp.simplify(sp.diff(op,outside)-reduced)==0
    assert sp.simplify(factor*(op.subs(outside,p[outside.name+'_max'])-op.subs(outside,p[outside.name+'_min']))-m['correct'])==0
    printed=[latex(t) for t in re.findall(r'\[([^\[\]]+)\]',final)]
    kind=g.DATA[name]['evaluation'] if name in g.DATA else 'generic'
    if kind=='separable_v':expect=[g.u,sp.integrate(m['f'],g.v)]
    elif kind=='separable_uv':expect=[g.u**2/2,g.v**2/2]
    else:expect=[primitive,op]
    assert len(printed)==len(expect),(name,'printed primitive count',printed)
    assert all(sp.simplify(a-b)==0 for a,b in zip(printed,expect)),(name,printed,expect)
    last=final.split(' & =')[-1]
    assert sp.simplify(latex(last.replace('$$','').replace(r'\end{aligned}',''))-m['correct'])==0
    fields=q[':question/answer-fields'];assert len(fields)==1
    field=fields[0];assert field[':answer-field/key']=='selection' and field[':answer-field/type']==':answer-field.type/radio'
    choices=field[':answer-field/choices'];assert len(choices)==5
    assert field[':answer-field/correct'][0]==':answer/id'
    ids=[a[':answer/id'] for a in choices];assert len(set(ids))==5
    assert field[':answer-field/correct'][1] in ids
    vals=[]
    for aa in choices:
        assert aa[':answer/type']==':answer.type/math' and '$' not in aa[':answer/value']
        value=latex(aa[':answer/value']);assert not value.free_symbols and value.is_real
        assert sp.simplify(value-g.expr(a['answer_recipes'][aa[':answer/id']]['value']))==0
        assert (sp.simplify(value-m['correct'])==0)==(aa[':answer/id']==field[':answer-field/correct'][1])
        vals.append(value)
        uuid.UUID(aa[':answer/id'])
    assert len(set(vals))==5
    content=g.digest({'parameters':a['parameter_fingerprint'],'problem':q[':question/problem'],'solution':solution,'bank':sorted(map(str,vals))})
    assert content==a['content_fingerprint']
    qid=uuid.uuid5(uuid.NAMESPACE_URL,f'flux/{g.KP_UUID}/{g.VERSION}/{content}');assert str(qid)==q[':question/id']
    assert str(uuid.uuid5(qid,'selection'))==field[':answer-field/id']
    return True


def write(name,obj): (ROOT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def main():
    raw=json.loads((ROOT/'source.json').read_text());cases=json.loads((ROOT/'source-cases.json').read_text());source={q[':question/id']:q for q in raw['record'][':knowledge-point/questions']}
    assert len(cases)==len(source) and {c['source_id'] for c in cases}==set(source), 'Complete unique source coverage'
    records=[];coverage=[];generated=[]
    for case in cases:
        r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);verify(r)
        old=source[case['source_id']];q=r['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
        assert q[':question/problem']==old[':question/problem'];assert q[':question/worked-solution']==old[':question/worked-solution']
        nb=sorted((str(latex(a[':answer/value'])),a[':answer/id']==f[':answer-field/correct'][1]) for a in f[':answer-field/choices'])
        ob=sorted((str(latex(a[':answer/value'])),a[':answer/id']==of[':answer-field/correct'][':answer/id']) for a in of[':answer-field/choices'])
        assert nb==ob and f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident']
        records.append({'label':'Original replay '+case['math_academy_id'],'record':r})
        coverage.append({'source_id':case['source_id'],'template':case['template'],'bank_profile':case['bank_profile'],'complete_bank':True,'values_matched':5,'distractors_matched':4,'correct_designation_matched':True,'prompt_exact':True,'solution_exact':True})
        # Two mathematical variants of EACH original complete profile, explicit empirical extrapolation.
        found=0
        for change in (1,2,3,4):
            p=copy.deepcopy(case['parameters']);p['v_max']+=change
            try:rr=g.generate(case['level'],template=case['template'],parameters=p,profile=case['bank_profile']);verify(rr)
            except g.SampleRejected:continue
            records.append({'label':f"Generated empirical bank variant {case['math_academy_id']} {found+1}",'record':rr});generated.append(rr);found+=1
            if found==2:break
        assert found==2,(case['template'],'needs two observed-bank variants')
    checked_profiles=[]
    for name,level in g.TEMPLATES.items():
        for profile in g.PROFILES:
            count=0
            for seed in range(8):
                rr=g.generate(level,seed,template=name,profile=profile);verify(rr);count+=1
                if seed<2:
                    records.append({'label':f'Generated authored bank {name} / {profile} / {seed}','record':rr});generated.append(rr)
                # Fixed mathematical parameters and displayed bank are seed invariant.
                again=g.generate(level,seed+100,template=name,profile=profile,parameters=rr['generation']['parameters']);verify(again)
                assert rr['question'][':question/id']==again['question'][':question/id']
                assert rr['question'][':question/worked-solution']==again['question'][':question/worked-solution']
            checked_profiles.append({'template':name,'profile':profile,'instances':count,'passed':True})
    rational_checks=[]
    for case in cases:
        p=copy.deepcopy(case['parameters']);p['v_max']=str(sp.Rational(p['v_max'])+sp.Rational(1,2))
        rr=g.generate(case['level'],template=case['template'],parameters=p,profile=case['bank_profile']);verify(rr)
        rational_checks.append(case['template'])
    # A displayed-bank change at fixed parameters changes content identity.
    aa=g.generate_easy(2,profile='authored_primitive')
    bb=g.generate_easy(2,profile='authored_rectangle',parameters=aa['generation']['parameters'])
    assert aa['generation']['parameter_fingerprint']==bb['generation']['parameter_fingerprint']
    assert aa['question'][':question/id']!=bb['question'][':question/id']
    # Explicit invalid inputs must fail, never silently replace them.
    invalid=[('easy',{'template':'q-161263'}),('easy',{'field_type':'blank'}),('easy',{'parameters':{'u_min':0,'u_max':0,'v_min':0,'v_max':1}}),('hard',{'template':'q-161283','parameters':{'u_min':-1,'u_max':1,'v_min':0,'v_max':1}}),('easy',{'profile':'observed:q-160845'})]
    for level,kwargs in invalid:
        try:g.generate(level,**kwargs)
        except ValueError:pass
        else:raise AssertionError(('Invalid explicit input accepted',level,kwargs))
    # Verify the validator itself rejects math, field/format, identity and scope corruption.
    mutant_failures=[];base=records[0]['record']
    for kind in ('choice_math','solution_math','identity','scope','format'):
        bad=copy.deepcopy(base)
        if kind=='choice_math':bad['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='999'
        elif kind=='solution_math':bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('6v-8','6v-9')
        elif kind=='identity':bad['question'][':question/id']=str(uuid.uuid4())
        elif kind=='scope':bad['question'][':question/difficulty']=':question.difficulty/easy'
        elif kind=='format':bad['question'][':question/answer-fields'][0][':answer-field/key']='other'
        try:verify(bad)
        except (AssertionError,ValueError):mutant_failures.append(kind)
        else:raise AssertionError(('Validator failed to reject',kind))
    engine=[]
    for item in records:
        field=item['record']['question'][':question/answer-fields'][0]
        engine.append({**item,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==field[':answer-field/correct'][1] else 'rejected','purpose':'Full owned radio bank selection'} for a in field[':answer-field/choices']]})
    write('engine-input.json',engine)
    subprocess.run([str(PROJECT/'generate/runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-validation.json')],check=True)
    native=json.loads((ROOT/'engine-validation.json').read_text());assert native['documented_unresolved_checks']==0
    write('review.json',records)
    lines=['# Flux original and generated review','\nDatabase math, basis 1356. Originals are generator replays compared exactly to the capture. Generated empirical bank variants preserve complete observed density profiles; these extrapolations have unresolved error intent. Authored bank variants use explicitly defined method errors. Metadata appears in review JSON only.']
    for item in records:lines+=['\n## '+item['label']+'\n',g.markdown(item['record'])]
    (ROOT/'review.md').write_text('\n'.join(lines))
    write('validation.json',{'passed':True,'source_provenance':{k:raw[k] for k in ('database','basis','lineage')},'source_coverage':coverage,
        'source_count':len(cases),'complete_banks_matched':len(cases),'displayed_values_matched':5*len(cases),'source_distractors_matched':4*len(cases),
        'source_designations_matched':len(cases),'source_prompt_and_solution_exact':len(cases),'mathematics':'independent determinant and exact polynomial moment formula; all displayed vectors, dot-product rows and primitives parsed',
        'generated_profile_checks':checked_profiles,'generated_review_counts':{level:sum(item['record']['generation']['template'] in g.TEMPLATES and g.TEMPLATES[item['record']['generation']['template']]==level for item in records if item['label'].startswith('Generated')) for level in ('easy','moderate','hard')},
        'native_grading':{'entry_point':native['entry_point'],'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':0,'engine_sha256':hashlib.sha256((PROJECT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'engine_source_sha256':hashlib.sha256((PROJECT/'generate/runs/current/check-engine.rs').read_bytes()).hexdigest()},
        'rational_boundary_checks':rational_checks,'different_bank_identity_checked':True,'invalid_input_checks':len(invalid),'failing_validator_mutations':mutant_failures,'known_limits':['Observed scalar distractor intent is unresolved; empirical profiles are explicit replay-only profiles, never default.','The source q-161262 has a zero normal curve and signed parameterized-patch interpretation; same calculation retained without claiming globally regular geometry.'],
        'database_writes':0})
    print(f'PASS: {len(cases)} complete source banks / {5*len(cases)} values / {4*len(cases)} distractors; {len(checked_profiles)*8} varied math checks; native {native["accepted_checks"]} accepted / {native["rejected_checks"]} rejected.')
if __name__=='__main__':
    try:main()
    except Exception as exc:
        write('validation.json',{'passed':False,'failure':type(exc).__name__+': '+str(exc)});raise
