#!/usr/bin/env python3
"""Fail closed on independent displayed-math, source, scope and native grading checks."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('kp',HERE.with_suffix('.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
x,y=S.symbols('x y'); symbols={n:S.Symbol(n) for n in ('x','y','k','p','q','t')}

def parse(s):
    s=s.strip().rstrip('.,?');s=s.replace(r'\dfrac',r'\frac')
    while r'\frac' in s:
        match=re.search(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',s)
        assert match,('invalid fraction',s)
        s=s[:match.start()]+'(('+match[1]+')/('+match[2]+'))'+s[match.end():]
    for token in (r'\left',r'\right',r'\,',r'\qquad'): s=s.replace(token,'')
    s=s.replace(r'\cdot','*').replace('{','(').replace('}',')')
    assert '\\' not in s,('unparsed TeX',s)
    return parse_expr(s,local_dict=symbols,transformations=standard_transformations+(implicit_multiplication_application,rationalize))
def eq(s):
    l,r=s.replace('&','').split('=');return S.expand(parse(l)-parse(r))
def proportional(a,b):
    ratio=S.cancel(a/b)
    return ratio!=0 and not ratio.free_symbols

def check_record(r):
    q=r['question'];g=r['generation'];p=q[':question/problem'];sol=q[':question/worked-solution'];kind=m.TEMPLATES[g['template']]['kind']
    for text in (p,sol):
        assert text.count('$')%2==0
        assert text.count('{')==text.count('}'),('braces',text)
        assert '{{field-1}}' not in text or kind=='blank'
        assert not re.search(r'\+\-|--',text),('sign display',text)
    if kind=='blank': assert '{{field-1}}' in p
    spans=re.findall(r'\$([^$]+)\$',p)
    equations=[eq(v) for v in spans if '=' in v and 'x' in v and 'y' in v]
    assert len(equations)==2,('prompt equations',p)
    unknown=next(iter((equations[0].free_symbols|equations[1].free_symbols)-{x,y}))
    coeff=[]
    for e in equations:
        A=e.coeff(x);B=e.coeff(y);assert B!=0;coeff.append((A,B))
    constraint=S.expand(coeff[0][0]*coeff[1][0]+coeff[0][1]*coeff[1][1])
    result=S.solve(constraint,unknown);assert len(result)==1
    correct=result[0];assert correct!=0
    f=q[':question/answer-fields'][0]; options=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
    assert len(set(options))==len(options)==(5 if kind=='radio' else 1)
    selected=[parse(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]]
    assert selected==[correct],('wrong designation',g,selected,correct)
    # Every displayed conversion row must describe the complete same line.
    aligned=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)
    expected_count=0 if g['family'].startswith('both') else 1 if g['family'].startswith('one') or g['family']=='known_standard' else 2
    assert len(aligned)==expected_count
    for i,block in enumerate(aligned):
        rows=block.split(r'\\')
        line=equations[i] if len(aligned)==2 or g['family']=='known_standard' else equations[1]
        for row in rows: assert proportional(eq(row),line),('conversion mismatch',row,line)
    if g['template']=='q-44407': assert len(aligned[0].split(r'\\'))==4
    if g['template']=='q-215944': assert len(aligned[1].split(r'\\'))==2
    # Parse the actual printed product and implication, without metadata answers.
    final=re.findall(r'\$\$(.*?)\$\$',sol,re.S)[-1]
    product,end=final.split('⟹'); product=product.replace(r'\,','').strip()
    assert eq(product).subs(unknown,correct)==0
    final_result=eq(end); assert final_result.subs(unknown,correct)==0
    assert final_result.coeff(unknown)!=0
    # Read claimed slopes from source-style prose and verify against actual lines.
    for line,claimed in re.findall(r'slope of the line \$([^$]+)\$ is \$([^$]+)\$',sol):
        e=eq(line); expected=-e.coeff(x)/e.coeff(y)
        assert S.simplify(parse(claimed)-expected)==0
    # All UUIDs owned and stable, no learner-facing generation metadata.
    import uuid
    uuid.UUID(q[':question/id']);uuid.UUID(f[':answer-field/id'])
    for a in f[':answer-field/choices']:uuid.UUID(a[':answer/id'])
    return correct

def native_item(r,label):
    q=r['question'];f=q[':question/answer-fields'][0];correct=check_record(r);checks=[]
    if f[':answer-field/type'].endswith('radio'):
        for a in f[':answer-field/choices']:
            checks.append({'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned radio choice'})
    else:
        n,d=correct.as_numer_denom()
        checks=[{'submitted':m.tex(correct),'expected':'accepted','purpose':'canonical exact answer'}, {'submitted':r'\frac{'+str(2*n)+'}{'+str(2*d)+'}','expected':'accepted','purpose':'unreduced equivalent exact answer'}, {'submitted':m.tex(-correct),'expected':'rejected','purpose':'wrong sign parameter'}]
    return {'label':label,'record':r,'checks':checks}

def main():
    cases=json.loads((HERE/'source-cases.json').read_text());source_records=[];fidelity=[];native=[];bank_values=0;refs=0;solutions=0
    for case in cases:
        n=case['source_id'];r=m.generate(case['level'],seed=0,template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);raw=m.RAW[n];q=r['question'];check_record(r)
        assert q[':question/problem']==raw[':question/problem']+('\n\n{{field-1}}' if n=='q-72548' else '')
        if ':question/worked-solution' in raw:assert q[':question/worked-solution']==raw[':question/worked-solution'];solutions+=1
        fs=raw.get(':question/answer-fields',[])
        if fs:
            assert len(fs)==len(q[':question/answer-fields'])
            orig=fs[0];f=q[':question/answer-fields'][0]
            assert orig[':answer-field/type'][':db/ident']==f[':answer-field/type']
            assert orig[':answer-field/key']==f[':answer-field/key']
            choices=orig.get(':answer-field/choices',[])
            if choices:
                assert sorted(map(str,[parse(a[':answer/value']) for a in choices]))==sorted(map(str,[parse(a[':answer/value']) for a in f[':answer-field/choices']]))
                # Delimiter-free exact source answer fragments, not just scalar equivalence.
                assert sorted(a[':answer/value'] for a in choices)==sorted(a[':answer/value'] for a in f[':answer-field/choices'])
                bank_values+=len(choices)
            if ':answer-field/correct' in orig:
                original=parse(orig[':answer-field/correct'][':answer/value']);selected=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert parse(selected[':answer/value'])==original;refs+=1
        fidelity.append({'source_id':n,'prompt_exact':n!='q-72548','prompt_repaired':n=='q-72548','solution_exact':True if ':question/worked-solution' in raw else None,'observed_bank_values':len(fs[0].get(':answer-field/choices',[])) if fs else 0,'correct_designation_matched':':answer-field/correct' in fs[0] if fs else False,'repair':case['repair']})
        source_records.append(r);native.append(native_item(r,'source '+n))
    records=[];unique={};sample_count=0
    for name,spec in m.TEMPLATES.items():
        fingerprints=set()
        for seed in range(60):
            r=m.generate(spec['level'],seed=seed,template=name);check_record(r);fingerprints.add(r['generation']['parameter_fingerprint']);sample_count+=1
            fixed=m.generate(spec['level'],seed=seed+1000,template=name,parameters=r['generation']['parameters'],profile=r['generation']['bank_profile'])
            assert r['question'][':question/id']==fixed['question'][':question/id'] and r['generation']['parameter_fingerprint']==fixed['generation']['parameter_fingerprint']
            def ordered(q):
                q=json.loads(json.dumps(q));q[':question/answer-fields'][0][':answer-field/choices'].sort(key=lambda a:a[':answer/id']);return q
            assert ordered(r['question'])==ordered(fixed['question'])
            if seed<2:records.append(r);native.append(native_item(r,'variant '+name+' '+str(seed)))
        assert len(fingerprints)>=15,(name,len(fingerprints));unique[name]=len(fingerprints)
        # Zero key coefficients must be rejected without division/slope exceptions.
        for key in ('a','m','A','B','D'):
            if key in spec['original']:
                p=dict(spec['original']);p[key]=0
                try:m.generate(spec['level'],template=name,parameters=p)
                except ValueError:pass
                else:raise AssertionError(('degenerate accepted',name,key))
        p=dict(spec['original']);key=next(iter(p));p[key]=25
        try:m.generate(spec['level'],template=name,parameters=p)
        except ValueError:pass
        else:raise AssertionError('scope bound bypass')
    # Exercise changed-parameter observed banks separately from authored defaults.
    for name in ('q-28328','q-44407','q-44515'):
        for seed in range(2):
            r=m.generate(m.TEMPLATES[name]['level'],seed=seed+24,template=name,profile='observed');check_record(r);records.append(r);native.append(native_item(r,'observed-bank variant '+name+' '+str(seed)))
    # Equivalent task identity excludes intercepts, sign-scaled equations and banks.
    a=m.generate('hard',template='q-44407',parameters=m.TEMPLATES['q-44407']['original'],profile='observed')
    p=dict(m.TEMPLATES['q-44407']['original']);p['A']*=2;p['B']*=2;p['C']*=2;p['E']=6
    b=m.generate('hard',template='q-44407',parameters=p,profile='authored')
    assert a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint']
    assert a['question'][':question/id']!=b['question'][':question/id']
    # Whole-bank collision must reject explicit parameters, never replace options.
    p=dict(m.TEMPLATES['q-28328']['original']);p['a']=1;p['m']=-1
    try:m.generate('easy',template='q-28328',parameters=p)
    except ValueError:pass
    else:raise AssertionError('collision accepted')
    (HERE/'review.json').write_text(json.dumps(records,indent=2)+'\n')
    review=['# Originals and parameterized variants','Raw EDB evidence is source.json; authored repairs and difficulty placements are labeled below.']
    for case,original in zip(cases,source_records):
        name=case['source_id'];review+=['## Original '+name,'Repair: '+case['repair'],'### Raw original',m.RAW[name][':question/problem'],m.RAW[name].get(':question/worked-solution','No captured worked solution.'),'### Parameterized source replay',m.markdown(original)]
        for variant in records:
            if variant['generation']['template']==name:review+=['### Generated '+('explicit observed-bank replay variant; distractor interpretation limits apply' if variant['generation']['bank_profile']=='observed' else 'authored variant'),m.markdown(variant)]
    (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    (HERE/'native-input.json').write_text(json.dumps(native,indent=2)+'\n')
    engine=HERE.parents[1]/'runs/current/check-engine'
    result=subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-report.json')],capture_output=True,text=True)
    assert result.returncode==0,(result.stdout,result.stderr)
    report={'passed':True,'source_coverage':{'practice_questions':11,'exact_prompts':'10/11','supported_repaired_prompts':'1/1','captured_exact_solutions':f'{solutions}/8','observed_answer_values':f'{bank_values}/19','observed_complete_banks':'7/7','observed_correct_designations':f'{refs}/7','unrated_missing_answer_repairs':3,'fieldless_authored_blank_repair':1,'absent_original_designations_not_counted':4},'fidelity':fidelity,'independent_display_math_samples':sample_count+17,'unique_tasks_per_template_60_samples':unique,'review_variants':len(records),'native_grader':{'passed':True,'fixtures':len(native),'checks':sum(len(i['checks']) for i in native),'report':'native-report.json','engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest()},'scope':'0/1/2 conversions only, finite nonzero slopes, exact rational parameter solving','plots':'none','unresolved_findings':['q-28328 and q-44515 distractor intentions underdetermined; explicit observed replay formulas only, excluded from default generation'],'freeze_script_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest()}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
if __name__=='__main__':main()
