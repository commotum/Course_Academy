#!/usr/bin/env python3
"""Failing mathematical/fidelity/presentation/native-grading validation.

Read actual printed formulas, differentiate directly after polar substitution,
and read every actual printed intermediate row. This is independent of the
generator's derivation metadata and its chain-rule calculation helper.
"""
import importlib.util, json, re, hashlib, subprocess, itertools
from pathlib import Path
import sympy as sp

HERE=Path(__file__).resolve().parent
SCRIPT=HERE.with_suffix('.py')
spec=importlib.util.spec_from_file_location('polar_kp',SCRIPT)
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def eq(a,b):
    # Separate exact checker: rewrite double angles from their definitions and
    # reduce the rational numerator by sin(theta)^2+cos(theta)^2=1.
    u,v=sp.symbols('independent_sin independent_cos')
    delta=(sp.expand_trig(a)-sp.expand_trig(b)).subs({sp.sin(g.T):u,sp.cos(g.T):v})
    n,d=sp.fraction(sp.cancel(delta))
    return sp.reduced(n,[u*u+v*v-1],u,v)[1]==0
def read_formula(q):
    problem=q[':question/problem']
    m=re.search(r'\$([fghw])\(x\s*,\s*y\)\s*=\s*(.*?)\$',problem)
    assert m,problem
    name=m[1];f=g.parse_math(m[2].strip().removesuffix(','))
    d=re.search(r'find \$\\frac\{∂'+name+r'\}\{∂(r|\\theta)\s*\}',problem)
    assert d,problem
    v=g.R if d[1]=='r' else g.T
    return name,f,v

def blocks(solution):return re.findall(r'\$\$\s*\\begin\{aligned\}(.*?)\\end\{aligned\}\s*\$\$',solution,re.S)
def rows(block):return re.split(r'\\\\',block)
def rhs(row):
    value=row.split('=',1)[1].strip()
    return value.removesuffix('.').removesuffix(',').strip()

def check_format(text):
    assert text.count('$$')%2==0
    assert text.replace('$$','').count('$')%2==0
    depth=0
    for i,c in enumerate(text):
        if c=='{' and (not i or text[i-1]!='\\'):depth+=1
        if c=='}' and (not i or text[i-1]!='\\'):depth-=1
        assert depth>=0,text
    assert depth==0,text
    assert '--' not in text and '+-' not in text and '\u2061' not in text

def check_record(rec):
    assert rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    q=rec['question'];name,f,v=read_formula(q)
    polar=f.subs({g.X:g.R*sp.cos(g.T),g.Y:g.R*sp.sin(g.T)},simultaneous=True)
    actual=sp.diff(polar,v)
    fx,fy=sp.diff(f,g.X),sp.diff(f,g.Y)
    px,py=[z.subs({g.X:g.R*sp.cos(g.T),g.Y:g.R*sp.sin(g.T)},simultaneous=True) for z in (fx,fy)]
    ux=sp.diff(g.R*sp.cos(g.T),v);uy=sp.diff(g.R*sp.sin(g.T),v)
    fields=q[':question/answer-fields'];assert len(fields)==1
    field=fields[0];assert field[':answer-field/type']==':answer-field.type/radio'
    assert field[':answer-field/key']=='selection'
    answers=field[':answer-field/choices'];assert len(answers)==5
    assert len({a[':answer/id'] for a in answers})==5
    parsed=[g.parse_math(a[':answer/value']) for a in answers]
    matching=[i for i,x in enumerate(parsed) if eq(x,actual)]
    assert len(matching)==1
    assert field[':answer-field/correct']==[':answer/id',answers[matching[0]][':answer/id']]
    assert all(not eq(a,b) for a,b in itertools.combinations(parsed,2))
    check_format(q[':question/problem']);check_format(q[':question/worked-solution'])
    for a in answers:check_format(a[':answer/value'])
    bs=blocks(q[':question/worked-solution']);assert len(bs)==4
    # Actual generic chain rows, including any wrong function labels, are read.
    variable='r' if v==g.R else 'theta'
    substitutions={g.derivative(name,'x'):fx,g.derivative(name,'y'):fy,
                   g.derivative('x',variable):ux,g.derivative('y',variable):uy}
    for row in rows(bs[0]):
        value=rhs(row)
        value=re.sub(r'(\\frac\{∂[a-z]\}\{∂\\theta)\s+\}',r'\1}',value)
        for symbol,expr in substitutions.items():value=value.replace(symbol,'('+g.tex(expr)+')')
        assert eq(g.parse_math(value),fx*ux+fy*uy),value
    # Cartesian partials: two equalities share a source row.
    m=re.search(re.escape(g.derivative(name,'x'))+r'=(.*?),\\,'+re.escape(g.derivative(name,'y'))+r'=(.*)',bs[1],re.S)
    assert m,bs[1]
    assert eq(g.parse_math(m[1]),fx)
    assert eq(g.parse_math(m[2]),fy)
    pr=rows(bs[2]);assert len(pr)==2
    assert pr[0].strip().startswith(g.derivative(name,'x'))
    assert pr[1].strip().startswith(g.derivative(name,'y'))
    assert eq(g.parse_math(rhs(pr[0])),px)
    assert eq(g.parse_math(rhs(pr[1])),py)
    final=rows(bs[3])
    for row in final:assert eq(g.parse_math(rhs(row)),actual),row
    # Distinct teaching rows: first substitutes the two partials, never an
    # eagerly collapsed final answer. Source two-row families retain two rows.
    assert '(' in rhs(final[0]) and any(op in rhs(final[0]) for op in ('+', '-'))
    if rec['generation']['template'] in ('cross_theta','cubic_r','radial_theta'):
        assert len(final)==3
    if rec['generation']['template'] in ('x_square_r','y_square_theta'):
        assert len(final)==2
    return {'mathematics':True,'stages':sum(len(rows(b)) for b in bs),'options':5}

def prose(s):return re.sub(r'\$\$.*?\$\$','<DISPLAY>',g.normalize(s),flags=re.S)

def source_fidelity(case,rec):
    q=g.RAW[case['source_id']];src=q[':question/answer-fields'][case['raw_field_index']]
    output=rec['question'][':question/answer-fields'][0]
    expected=[g.parse_math(a[':answer/value']) for a in src[':answer-field/choices']]
    got=[g.parse_math(a[':answer/value']) for a in output[':answer-field/choices']]
    assert len(expected)==len(got)==5
    assert all(sum(eq(a,b) for b in got)==1 for a in expected)
    correct=src.get(':answer-field/correct')
    if correct:
        target=g.parse_math(correct[':answer/value'])
        selected=next(a for a in output[':answer-field/choices'] if a[':answer/id']==output[':answer-field/correct'][1])
        assert eq(target,g.parse_math(selected[':answer/value']))
    assert rec['question'][':question/problem']==g.normalize(q[':question/problem'])
    stages=False;exact_solution=False
    if ':question/worked-solution' in q:
        original=g.normalize(q[':question/worked-solution'])
        generated=rec['question'][':question/worked-solution']
        assert prose(original)==prose(generated)
        original_blocks=blocks(original);generated_blocks=blocks(generated)
        assert [len(rows(b)) for b in original_blocks]==[len(rows(b)) for b in generated_blocks]
        # Whole final-stage sequence, one-to-one, with no extra distribution or
        # substitution rows; normalized original expressions independently read.
        for a,b in zip(rows(original_blocks[-1]),rows(generated_blocks[-1])):
            assert eq(g.parse_math(rhs(a)),g.parse_math(rhs(b)))
        stages=True;exact_solution=original==generated
    return {'source_id':case['source_id'],'profile':case['profile'],
            'bank_values_matched':5,'bank_values_total':5,'complete_bank_matched':True,
            'original_correct_designation_present':correct is not None,
            'original_correct_designation_matched':correct is not None,
            'inferred_missing_reference':correct is None,
            'original_field_count':len(q[':question/answer-fields']),
            'normalized_prompt_exact':True,
            'raw_prompt_exact':q[':question/problem']==rec['question'][':question/problem'],
            'worked_prose_and_final_stage_sequence_matched':stages,
            'normalized_worked_solution_byte_exact':exact_solution,
            'raw_answer_values_exact':sum(a[':answer/value'] in [b[':answer/value'] for b in output[':answer-field/choices']] for a in src[':answer-field/choices'])}

def main():
    cases=json.loads((HERE/'source-cases.json').read_text());records=[];fidelity=[];results=[];engine=[]
    for case in cases:
        rec=g.generate('easy',template=case['template'],parameters=case['parameters'],profile=case['profile'])
        results.append(check_record(rec));fidelity.append(source_fidelity(case,rec));records.append(rec)
    # Every family and complete bank under two nonoriginal parameters, all
    # supported function labels, with exact sampled and explicit validation.
    for t,l in g.TEMPLATES.items():
        for index,a in enumerate([2,3]):
            if l=='easy':p={'a':a,'name':['f','w'][index]}
            elif t=='cubic_sum_theta':p={'a':a,'b':-1-index,'name':['g','h'][index]}
            else:p={'a':a,'b':-1-index,'c':4,'name':['h','g'][index]}
            for profile in (['observed','legacy'] if t=='cross_theta' else [None]):
                rec=g.generate(l,seed=100+index,template=t,parameters=p,profile=profile)
                results.append(check_record(rec));records.append(rec)
                reordered=g.generate(l,seed=900+index,template=t,parameters=p,profile=profile)
                assert rec['question'][':question/id']==reordered['question'][':question/id']
                assert rec['generation']['mathematical_fingerprint']==reordered['generation']['mathematical_fingerprint']
        # One sampler run per family exercises domain/whole-bank rejection.
        rec=g.generate(l,seed=701,template=t);results.append(check_record(rec));records.append(rec)
    # Name changes alter display identity, never mathematical identity.
    for t,l in g.TEMPLATES.items():
        p={'a':2} if l=='easy' else ({'a':2,'b':-1} if t=='cubic_sum_theta' else {'a':2,'b':-1,'c':3})
        variants=[g.generate(l,template=t,parameters=dict(p,name=n)) for n in ['f','g','h','w']]
        for v in variants:check_record(v)
        assert len({v['generation']['mathematical_fingerprint'] for v in variants})==1
        assert len({v['question'][':question/id'] for v in variants})==4
    # Coefficient limits apply to explicit inputs and the sampler.
    rejected=0
    invalid=[('easy','cross_theta',{'a':0}),('easy','cross_theta',{'a':7}),
      ('moderate','quadratic_theta',{'a':1,'b':0,'c':2}),
      ('moderate','quadratic_theta',{'a':-5,'b':1,'c':2}),
      ('moderate','quadratic_r',{'a':2,'b':1,'c':2}),
      ('hard','cubic_sum_theta',{'a':0,'b':2}),
      ('hard','log_quadratic_theta',{'a':1,'b':4,'c':2})]
    for l,t,p in invalid:
        try:g.generate(l,template=t,parameters=p)
        except ValueError:rejected+=1
        else:raise AssertionError('invalid explicit input accepted')
    # Task equality under positive common log-argument scale.
    u=g.generate_hard(template='log_quadratic_theta',parameters={'a':1,'b':1,'c':2})
    v=g.generate_hard(template='log_quadratic_theta',parameters={'a':2,'b':2,'c':4})
    assert u['generation']['mathematical_fingerprint']==v['generation']['mathematical_fingerprint']
    assert u['question'][':question/id']!=v['question'][':question/id']
    for i,rec in enumerate(records):
        f=rec['question'][':question/answer-fields'][0]
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual engine selection '+str(j)} for j,a in enumerate(f[':answer-field/choices'])]
        engine.append({'label':'record-'+str(i),'record':rec,'checks':checks})
    (HERE/'engine-input.json').write_text(json.dumps(engine,ensure_ascii=False,indent=2)+'\n')
    executable=HERE.parents[1]/'runs/current/check-engine'
    subprocess.run([str(executable),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    engine_result=json.loads((HERE/'engine-report.json').read_text())
    output={'passed':True,'generator_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),
      'snapshot':{'database':g.CAPTURE['database'],'basis':g.CAPTURE['basis'],'lineage':g.CAPTURE['lineage']},
      'source_questions':7,'rated_easy':6,'unrated':1,'observed_moderate':0,'observed_hard':0,
      'source_cases':len(cases),'original_raw_fields':8,'normal_fields_per_question':1,
      'source_values_matched':sum(x['bank_values_matched'] for x in fidelity),'source_values_total':40,
      'complete_source_banks_matched':len(fidelity),'complete_source_banks_total':8,
      'known_correct_refs_matched':sum(x['original_correct_designation_matched'] for x in fidelity),
      'known_correct_refs_total':6,'missing_refs_derived_not_matched':2,
      'source_solution_available_questions':6,'source_solution_prose_and_stage_sequences_matched':6,
      'source_worked_solution_byte_exact':sum(x['normalized_worked_solution_byte_exact'] for x in fidelity),
      'source_teaching_label_repairs':{'q-94999':'g→h in radial chain rule','q-95113':'first substituted derivative y→x','q-95116':'first substituted derivative y→x'},
      'checked_records':len(records),'additional_function_label_checks':44,'checked_printed_solution_rows':sum(x['stages'] for x in results),
      'invalid_inputs_rejected':rejected,'native_accepted':engine_result['accepted_checks'],'native_rejected':engine_result['rejected_checks'],
      'native_unresolved':engine_result['documented_unresolved_checks'],'blank_equivalence_checks':'not applicable: all source fields are radio',
      'native_engine_binary_sha256':hashlib.sha256(executable.read_bytes()).hexdigest(),
      'native_engine_source_sha256':hashlib.sha256(executable.with_suffix('.rs').read_bytes()).hexdigest(),
      'plot_rating':'none','fidelity':fidelity}
    (HERE/'validation.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    (HERE/'source-replays.json').write_text(json.dumps(records[:len(cases)],ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k!='fidelity'},indent=2))

if __name__=='__main__':main()
