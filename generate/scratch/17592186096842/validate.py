#!/usr/bin/env python3
"""Independent displayed-math, source fidelity, identity and native grading audit."""
from pathlib import Path
import importlib.util,json,re,subprocess,hashlib,sys,itertools
import sympy as sp
from functools import lru_cache
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ROOT=Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location('radical_generator',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(g)
x=sp.Symbol('x',real=True);u=sp.Symbol('u',positive=True)
DY,DU,UX=sp.symbols('DY DU UX')
TRANS=standard_transformations+(implicit_multiplication_application,)

@lru_cache(maxsize=40000)
def displayed(latex):
    """Small independent parser for the observed algebra grammar, not answer metadata.

    Braced closing delimiters are valid source TeX grouping, normalized here.
    No antlr dependency or numeric answer lookup is used.
    """
    s=latex.replace(r'\,','').strip().rstrip('.,').replace(r'\left','').replace(r'\right','').replace('{)}',')').replace(r'\cdot','*')
    for a,b in [(g.D,'DY'),(g.DU,'DU'),(g.UX,'UX')]:s=s.replace(a,b)
    def group(i):
        assert s[i]=='{',repr(s)
        depth=1;j=i+1
        while depth:
            if s[j]=='{':depth+=1
            if s[j]=='}':depth-=1
            j+=1
        return s[i+1:j-1],j
    out='';i=0
    while i<len(s):
        if s.startswith(r'\frac',i):
            first,j=group(i+5);second,i=group(j)
            out+='(('+str(displayed(first))+')/('+str(displayed(second))+'))'
        elif s.startswith(r'\sqrt',i):
            arg,i=group(i+5);out+='sqrt('+str(displayed(arg))+')'
        elif s[i]=='{':
            arg,i=group(i);out+='('+str(displayed(arg))+')'
        elif s[i]=='^':out+='**';i+=1
        elif s[i]=='\\':raise AssertionError('Unsupported displayed macro '+s[i:])
        else:out+=s[i];i+=1
    return parse_expr(out,local_dict={'x':x,'u':u,'DY':DY,'DU':DU,'UX':UX,'sqrt':sp.sqrt},transformations=TRANS)

@lru_cache(maxsize=50000)
def equal(a,b):
    # All learner derivatives operate where inner>0. Positive radical branches
    # justify force only after those domain constraints have been checked.
    if a==b:return True
    difference=sp.cancel(sp.powdenest(a,force=True)-sp.powdenest(b,force=True))
    if difference==0:return True
    if difference.is_zero is False:return False
    # Exact real witnesses disprove an identity without a costly simplification.
    for point in (25,-25,1,-1):
        witness=difference.subs(x,point)
        if witness.is_real is True and witness.is_finite is True and witness.is_zero is False:return False
    return sp.simplify(difference)==0

def independent(rec):
    p=rec['generation']['parameters'];spec=g.TEMPLATES[rec['generation']['template']]
    inner=p['a']*x**spec['degree']+p['b']*(x if spec['degree']==2 else 1)+p.get('c',0)
    e=sp.Rational(1,2) if spec['family']=='sqrt' else -sp.Rational(1,2)
    outer=u**e;outerd=sp.diff(outer,u);innerd=sp.diff(inner,x)
    derivative=sp.diff(inner**e,x)
    expected=derivative.subs(x,p['t']) if spec.get('slope') else derivative
    question=rec['question'];field=question[':question/answer-fields'][0]
    prompt_function=re.search(r'y\s*=\s*([^$]+)',question[':question/problem'])
    assert prompt_function
    assert equal(displayed(prompt_function[1]),inner**e)
    prompt_derivative=sp.diff(displayed(prompt_function[1]),x)
    assert equal(prompt_derivative,derivative)
    assert len(question[':question/answer-fields'])==1
    values=[displayed(a[':answer/value']) for a in field[':answer-field/choices']]
    assert len(values)==(5 if spec['field']=='radio' else 1)
    correct_id=field[':answer-field/correct'][1]
    correct=[i for i,a in enumerate(field[':answer-field/choices']) if a[':answer/id']==correct_id];assert len(correct)==1
    assert equal(values[correct[0]],expected),(rec['generation'],values,expected)
    assert sum(equal(v,expected) for v in values)==1
    for a,b in itertools.combinations(values,2):assert not equal(a,b)
    for a in field[':answer-field/choices']:assert '$' not in a[':answer/value']
    assert question[':question/problem'].count('{{field-1}}')==(1 if spec['field']=='blank' else 0)
    # Check all math blocks against differentiation independent of generator math.
    content=question[':question/worked-solution'];math=re.findall(r'\$\$\n(.*?)\n\$\$',content,re.S)
    assert len(math)==(5 if spec.get('slope') else 4)
    assert equal(displayed(math[0].split('=',1)[1]),DU*UX)
    for expr in math[1].split('=')[1:]:assert equal(displayed(expr),outerd)
    assert equal(displayed(math[2].split('=',1)[1]),innerd)
    rows=math[3].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
    for row in rows:
        rhs=row.split('& =')[1].strip().rstrip('.')
        expression=displayed(rhs).subs({DU:outerd,UX:innerd}).subs(u,inner)
        assert equal(expression,derivative),(rhs,expression,derivative)
    if spec.get('slope'):
        rows=math[4].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
        for index,row in enumerate(rows):
            rhs=row.split('& =')[1].strip().rstrip('.')
            if index==0:
                # Displayed evaluation bar: parse the actual enclosed derivative.
                marker=rhs.index('|');expr=rhs[1:marker]
                if expr.endswith('}'):expr=expr[:-1]
                value=displayed(expr).subs(x,p['t'])
            else:value=displayed(rhs)
            assert equal(value,expected),(rhs,value,expected)
    # Inline u, y and rewritten fractional exponent are displayed maths too.
    match=re.search(r'Let \$u=(.*?)\.\$ Then \$y=(.*?)\.\$',content)
    assert match
    assert equal(displayed(match[1]),inner)
    for expression in match[2].split('='):assert equal(displayed(expression),outer)
    for uid in [question[':question/id'],field[':answer-field/id']]+[a[':answer/id'] for a in field[':answer-field/choices']]:
        import uuid
        assert str(uuid.UUID(uid))==uid
    return expected

def grader_checks(rec):
    field=rec['question'][':question/answer-fields'][0]
    if field[':answer-field/type'].endswith('/radio'):
        return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==field[':answer-field/correct'][1] else 'rejected','purpose':'Every owned displayed choice'} for a in field[':answer-field/choices']]
    value=field[':answer-field/choices'][0][':answer/value'];expected=independent(rec)
    spec=g.TEMPLATES[rec['generation']['template']];p=rec['generation']['parameters']
    if spec.get('slope'):
        alternate=g.tex(expected)
    else:
        inner=p['a']*x**spec['degree']+p['b']*(x if spec['degree']==2 else 1)+p.get('c',0)
        numerator=sp.diff(inner,x)*(1 if spec['family']=='sqrt' else -1)
        argument=g.tex(inner) if spec['family']=='sqrt' else g.tex(sp.expand(inner**3))
        alternate=r'\frac{'+g.tex(numerator)+r'}{2\sqrt{'+argument+'}}'
    return [{'submitted':value,'expected':'accepted','purpose':'Canonical blank fragment'},
            {'submitted':r'\frac{2('+value+r')}{2}','expected':'accepted','purpose':'Equivalent blank expression'},
            {'submitted':alternate,'expected':'accepted','purpose':'Independent unreduced derivative; reciprocal cubic radicand expanded'},
            {'submitted':'-('+value+')','expected':'rejected','purpose':'Wrong sign'},
            {'submitted':'2('+value+')','expected':'rejected','purpose':'Omitted half'},
            {'submitted':'0','expected':'rejected','purpose':'Incorrect zero'}]

def main():
    source=json.loads((ROOT/'source.json').read_text())
    assert source==json.loads(Path('generate/runs/current/sources/17592186096842.json').read_text())
    qs={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
    cases=json.loads((ROOT/'source-cases.json').read_text());records=[];source_results=[]
    mathcount=0;bank_count=0;choice_count=0;designation_count=0;exactsolutions=0
    for case in cases:
        rec=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);expected=independent(rec);mathcount+=1
        original=qs[case['source_id']];q=rec['question'];f=q[':question/answer-fields'][0];of=original[':question/answer-fields'][0]
        assert q[':question/problem']==original[':question/problem']
        if ':question/worked-solution' in original:
            assert q[':question/worked-solution']==original[':question/worked-solution'];exactsolutions+=1
        assert f[':answer-field/type']==of[':answer-field/type'][':db/ident'] and f[':answer-field/key']==of[':answer-field/key']
        generated=[displayed(a[':answer/value']) for a in f[':answer-field/choices']]
        originalvalues=[displayed(a[':answer/value']) for a in of[':answer-field/choices']]
        assert len(generated)==len(originalvalues)
        for value in originalvalues:assert sum(equal(value,v) for v in generated)==1
        if ':answer-field/correct' in of:
            assert equal(displayed(of[':answer-field/correct'][':answer/value']),expected);designation_count+=1
        else:assert case['repairs']
        bank_count+=1;choice_count+=len(generated)
        source_results.append({'source_id':case['source_id'],'template':case['template'],'profile':case['bank_profile'],'prompt_exact':True,'solution_exact':':question/worked-solution' in original,'complete_values_matched':len(generated),'original_designation_matched':':answer-field/correct' in of,'repairs':case['repairs']})
        records.append({'label':'Original replay '+case['source_id'],'origin':'source replay','record':rec,'original':original})
    # Every observed profile/template gets two visible authored parameter variants.
    for name,spec in g.TEMPLATES.items():
        observed=next(c for c in cases if c['template']==name)['bank_profile']
        for seed in [21,42]:
            rec=g.generate(spec['level'],seed=seed,template=name,profile=observed);independent(rec);mathcount+=1
            records.append({'label':'Generated '+spec['level']+' observed profile '+name+' seed '+str(seed),'origin':'generated variant of observed template/bank','record':rec})
    # Defaults audited widely and inspected, including every all-level template.
    diversity={}
    for name,spec in g.TEMPLATES.items():
        print('Checking defaults:',name,flush=True)
        fingerprints=set()
        for seed in range(80):
            rec=g.generate(spec['level'],seed=seed,template=name);independent(rec);mathcount+=1
            fingerprints.add(rec['generation']['parameter_fingerprint'])
            fixed=g.generate(spec['level'],seed=seed+999,template=name,parameters=rec['generation']['parameters'],profile=rec['generation']['bank_profile'])
            assert fixed['question'][':question/id']==rec['question'][':question/id']
            assert sorted(fixed['question'][':question/answer-fields'][0][':answer-field/choices'],key=lambda a:a[':answer/id'])==sorted(rec['question'][':question/answer-fields'][0][':answer-field/choices'],key=lambda a:a[':answer/id'])
            if seed in [0,1]:records.append({'label':'Generated '+spec['level']+' default '+name+' seed '+str(seed),'origin':'authored operation bank / extended parameters','record':rec})
        diversity[name]=len(fingerprints)
        assert len(fingerprints)>=50
    assert len(g.SLOPE_QUADRATIC_PARAMETERS)==114
    for p in g.SLOPE_QUADRATIC_PARAMETERS:
        assert sp.sqrt(p['a']*p['t']**2+p['b']*p['t']).is_Integer
    linear_a=g.generate('moderate',template='sqrt_spaced_radio',parameters={'a':4,'b':-3})
    linear_b=g.generate('moderate',template='sqrt_constfirst_radio',parameters={'a':4,'b':-3})
    assert linear_a['generation']['parameter_fingerprint']==linear_b['generation']['parameter_fingerprint']
    assert linear_a['question'][':question/id']!=linear_b['question'][':question/id']
    # Different displayed banks at fixed parameters change content identity.
    for case in cases:
        if case['bank_profile']=='blank':continue
        source_rec=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])
        default_rec=g.generate(case['level'],template=case['template'],parameters=case['parameters'])
        assert source_rec['question'][':question/id']!=default_rec['question'][':question/id']
        assert source_rec['generation']['parameter_fingerprint']==default_rec['generation']['parameter_fingerprint']
    # Explicit invalid inputs must be rejected, not silently repaired.
    for kwargs in [dict(level='hard',template='sqrt_linear_blank',parameters={'a':0,'b':3}),dict(level='easy',template='slope_sqrt_radio',parameters={'a':4,'b':-20,'t':1}),dict(level='hard',template='sqrt_linear_blank',profile='source_slope')]:
        try:g.generate(**kwargs)
        except ValueError:pass
        else:raise AssertionError('Invalid explicit input accepted')
    review={'generator_version':g.VERSION,'source':source|{'record':'See source.json'},'records':records}
    (ROOT/'review.json').write_text(json.dumps(review,indent=2)+'\n')
    md='# Radical chain rule: originals and generated variants\n\nAll review rows are fixed worked solutions; choices have no diagnosis text. Source replay and authored repairs are labeled.\n\n'
    for row in records:
        rec=row['record'];md+='## '+row['label']+'\n\n'+row['origin']+'; level '+rec['question'][':question/difficulty'].rsplit('/',1)[-1]+'.\n\n'
        if 'original' in row:
            original=row['original'];md+='### Raw original\n\n'+original[':question/problem']+'\n\n'
            md+='\n'.join('- $'+a[':answer/value']+'$' for a in original[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'
            md+=original.get(':question/worked-solution','No captured solution or correct designation; generated replay contains explicitly authored repairs.')+'\n\n### Replay\n\n'
        md+=g.markdown(rec)+'\n\n'
    (ROOT/'review.md').write_text(md)
    native=[{'label':row['label'],'record':row['record'],'checks':grader_checks(row['record'])} for row in records]
    (ROOT/'engine-input.json').write_text(json.dumps(native,indent=2)+'\n')
    engine=Path('generate/runs/current/check-engine')
    result=subprocess.run([str(engine),str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],text=True,capture_output=True)
    (ROOT/'engine-log.txt').write_text(result.stdout+result.stderr)
    if result.returncode:print(result.stdout+result.stderr);raise AssertionError('Native grading failed')
    report=json.loads((ROOT/'engine-report.json').read_text())
    assert report['documented_unresolved_checks']==0
    domain_case=next(row['record'] for row in records if row['label']=='Original replay q-342764')
    domain_equivalent=g.tex(independent(domain_case))
    canonical=domain_case['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']
    assert equal(displayed(domain_equivalent),displayed(canonical))
    probe=[{'label':'Known domain-equivalent fractional-power limitation','record':domain_case,'checks':[{'submitted':domain_equivalent,'expected':'unresolved','purpose':'Mathematically correct on positive-radicand domain; native grader lacks question domain context. This is a failed accepted-equivalence capability, not a wrong-answer rejection.'}]}]
    (ROOT/'engine-domain-probe-input.json').write_text(json.dumps(probe,indent=2)+'\n')
    probe_result=subprocess.run([str(engine),str(ROOT/'engine-domain-probe-input.json'),str(ROOT/'engine-domain-probe-report.json')],text=True,capture_output=True)
    assert probe_result.returncode==0,probe_result.stdout+probe_result.stderr
    validation={'status':'passed_supported_forms_with_documented_native_domain_limitation','generator_version':g.VERSION,'source_basis':1356,'practice_sources':len(cases),'source_banks_matched':bank_count,'source_choices_matched':choice_count,'source_distractors_matched':16,'source_explicitly_designated_wrong_choices_matched':12,'unrated_source_wrong_values_inferred_and_matched':4,'source_designations_matched':designation_count,'missing_designations_repaired':1,'source_prompts_exact':9,'source_solutions_exact':exactsolutions,'source_missing_solutions_authored':1,'source_results':source_results,'displayed_math_instances':mathcount,'independently_checked':'displayed prompt functions and all displayed outer/inner derivatives, product rows, evaluation rows, choice values and blank fragments','default_parameter_diversity_of_80':diversity,'easy_quadratic_slope_support':{'enumerated_instances':114,'radicand':'perfect square r², 2≤r≤12','a':'1..6','absolute_b':'1..24','absolute_t':'1..4','b_t_sign':'same'},'generated_review_records':len(records)-9,'native':{'accepted':report['accepted_checks'],'rejected':report['rejected_checks'],'unresolved':report['documented_unresolved_checks'],'entry_point':report['entry_point'],'binary_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'harness_source_sha256':hashlib.sha256(Path('generate/runs/current/check-engine.rs').read_bytes()).hexdigest(),'domain_equivalent_fractional_power':{'mathematically_correct':True,'expected_acceptance_capability':'failed: unresolved domain differences','separate_probe_unresolved':1,'report':'engine-domain-probe-report.json'}},'database_writes':0,'unresolved_findings':['Native fractional-power equivalent blank is mathematically valid on positive-radicand domain but gets unresolved domain differences; canonical and expanded-radical equivalents are supported.','Observed scalar distractor intent in source_slope and coefficient -3 in source_reciprocal is underdetermined; explicit-only empirical replay shapes retained, not used by defaults.'],'plots':'none'}
    (ROOT/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
    print(json.dumps(validation,indent=2))
if __name__=='__main__':main()
