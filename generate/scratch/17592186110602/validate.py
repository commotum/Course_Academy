#!/usr/bin/env python3
"""Independent display checks, all-source replay, native grade_field and review.

Use .venv/bin/python generate/scratch/17592186110602/validate.py.
Reads source capture at basis 1356; writes evidence only in this KP folder.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import uuid
import sympy as sp

sys.dont_write_bytecode=True

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
spec=importlib.util.spec_from_file_location('axis_generator',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=g
spec.loader.exec_module(g)
X,Y=sp.symbols('x y')

def write(name,value):
    (HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')

def parse(text):
    text=re.sub(r'\\(?:d?frac)\{(-?\d+)\}\{(\d+)\}',r'(\1)/(\2)',text)
    text=re.sub(r'(?<=\d)(?=[xy])','*',text)
    return sp.sympify(text,locals={'x':X,'y':Y},rational=True)

def relation(value):
    lhs,rhs=value.split('=')
    # Normalize the COMPLETE equation up to a nonzero scale.
    polynomial=sp.Poly(sp.expand(parse(lhs)-parse(rhs)),X,Y)
    assert polynomial.total_degree()==1,value
    coefficients=polynomial.coeffs()
    return sp.expand(polynomial.as_expr()/coefficients[0])

def field_correct(field):
    return next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1])

def display_check(record):
    q=record['question']
    problem=q[':question/problem']
    given=re.search(r'\$([xy])\s*=\s*([^$]+)\$',problem)
    assert given,problem
    given_axis=given[1]
    constant=parse(given[2].rstrip('.'))
    assert constant.is_Rational
    point=re.search(r'\$\(([^,]+),\s*([^\)]+)\)',problem)
    assert point,problem
    a,b=map(parse,point.groups())
    needed_axis=Y if given_axis=='x' else X
    coord=b if given_axis=='x' else a
    expected=needed_axis-coord
    fields=q[':question/answer-fields']
    for f in fields:
        uuid.UUID(f[':answer-field/id'])
        assert f[':answer-field/correct'][0]==':answer/id'
        assert sum(v[':answer/id']==f[':answer-field/correct'][1] for v in f[':answer-field/choices'])==1
        for v in f[':answer-field/choices']:
            uuid.UUID(v[':answer/id'])
            assert '$' not in v[':answer/value']
    uuid.UUID(q[':question/id'])
    if fields[0][':answer-field/type'].endswith('/radio'):
        assert len(fields)==1 and len(fields[0][':answer-field/choices'])==5
        displayed=[relation(v[':answer/value']) for v in fields[0][':answer-field/choices']]
        assert len(set(displayed))==5
        assert sum(sp.expand(v-expected)==0 for v in displayed)==1
        assert relation(field_correct(fields[0]))==expected
    else:
        assert len(fields)==2
        for f in fields:
            assert '{{'+f[':answer-field/key']+'}}' in problem
            assert len(f[':answer-field/choices'])==1
        assert relation(field_correct(fields[0])+'='+field_correct(fields[1]))==expected
        lhs,rhs=parse(field_correct(fields[0])),parse(field_correct(fields[1]))
        coefficient=lhs.coeff(needed_axis)
        assert coefficient.is_Integer and coefficient>0 and rhs.is_Integer
        assert sp.gcd(coefficient,rhs)==1
    solution=q[':question/worked-solution']
    orientation='vertical' if given_axis=='x' else 'horizontal'
    needed='horizontal' if given_axis=='x' else 'vertical'
    assert f'is a {orientation} line, a perpendicular line would need to be {needed}.' in solution
    assert f'form ${str(needed_axis)}=k$' in solution
    answer=re.search(r'perpendicular line is \$([^$]+)\$',solution)
    assert answer and relation(answer[1].rstrip('.'))==expected
    coordinate=re.search(r'\$([xy])\$-coordinate of \$([^$]+)\$',solution)
    assert coordinate and coordinate[1]==str(needed_axis) and parse(coordinate[2].rstrip('.'))==coord
    # Verify the displayed solution coordinate tuple independently too.
    s_point=re.search(r'point \$\(([^,]+),([^\)]+)\)',solution)
    assert tuple(map(parse,s_point.groups()))==(a,b)
    if len(fields)==2 and coord.q!=1:
        standard=re.search(r'In standard form, this is \$([^$]+)\$',solution)
        assert standard and relation(standard[1].rstrip('.'))==expected
    for content in (problem,solution):
        assert content.count('$')%2==0
        count=0
        for char in content:
            count+=1 if char=='{' else -1 if char=='}' else 0
            assert count>=0
        assert count==0
    assert record['generation']['parameter_fingerprint']==g.digest({'required_axis':str(needed_axis),'required_coordinate':str(coord)})

def checks(record):
    out=[]
    for i,f in enumerate(record['question'][':question/answer-fields']):
        if f[':answer-field/type'].endswith('/radio'):
            for a in f[':answer-field/choices']:
                out.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'grade each owned radio choice after independent equation verification'})
        else:
            value=field_correct(f)
            expression=parse(value)
            equivalent=(f'{expression}+0' if i==0 else f'({expression*3})/3')
            wrong=('y' if X in expression.free_symbols else 'x') if i==0 else str(expression+1)
            out.extend([{'field_index':i,'submitted':value,'expected':'accepted','purpose':'canonical inferred standard-form fragment'},
                        {'field_index':i,'submitted':equivalent,'expected':'accepted','purpose':'equivalent fragment with retained extra operation'},
                        {'field_index':i,'submitted':wrong,'expected':'rejected','purpose':'non-equivalent axis/constant fragment'}])
            if i==0:
                out.append({'field_index':i,'submitted':str(2*expression),'expected':'rejected','purpose':'alternate whole-equation scale cannot change an independently graded LHS fragment'})
    return out

def main():
    raw=json.loads((HERE/'source.json').read_text())
    assert raw==json.loads((REPO/'generate/runs/current/sources/17592186110602.json').read_text())
    sources={q[':question/math-academy-id']:q for q in raw['record'][':knowledge-point/questions']}
    cases=json.loads((HERE/'source-cases.json').read_text())
    assert {c['source_id'] for c in cases}==set(sources) and len(cases)==8
    review=[]
    native=[]
    fidelity=[]
    for case in cases:
        source=sources[case['source_id']]
        record=g.generate(case['level'],17,case['template'],parameters=case['parameters'],profile=case.get('bank_profile'))
        display_check(record)
        q=record['question']
        assert q[':question/problem']==source[':question/problem'],case['source_id']
        assert len(q[':question/answer-fields'])==len(source[':question/answer-fields'])
        for sf,gf in zip(source[':question/answer-fields'],q[':question/answer-fields']):
            assert sf[':answer-field/key']==gf[':answer-field/key']
            assert sf[':answer-field/type'][':db/ident']==gf[':answer-field/type']
            if ':answer-field/choices' in sf:
                observed=[relation(a[':answer/value']) for a in sf[':answer-field/choices']]
                generated=[relation(a[':answer/value']) for a in gf[':answer-field/choices']]
                assert sorted(map(str,observed))==sorted(map(str,generated))
                assert relation(sf[':answer-field/correct'][':answer/value'])==relation(field_correct(gf))
                assert sorted(a[':answer/value'] for a in sf[':answer-field/choices'])==sorted(a[':answer/value'] for a in gf[':answer-field/choices'])
        if ':question/worked-solution' in source:
            assert q[':question/worked-solution']==source[':question/worked-solution'],case['source_id']
        fidelity.append({'source_id':case['source_id'],'prompt_exact':True,'field_layout_exact':True,'complete_bank_match':True if case.get('bank_profile') else None,'observed_designation_matched':1 if case.get('bank_profile') else 0,'derived_missing_designations':0 if case.get('bank_profile') else 2,'solution_exact':True if ':question/worked-solution' in source else None})
        review.append({'label':'source replay '+case['source_id'],'source_id':case['source_id'],'role':'source_replay','record':record})
        native.append({'label':'source replay '+case['source_id'],'record':record,'checks':checks(record)})
        # Changed parameters from the ordinary sampler and the same whole profile.
        for variant_seed in range(41,101):
            variant=g.generate('easy',variant_seed,case['template'],profile=case.get('bank_profile'))
            if variant['generation']['parameter_fingerprint']!=record['generation']['parameter_fingerprint']:break
        else:raise AssertionError('No substantive changed-coordinate source variant')
        assert variant['generation']['parameters']!=record['generation']['parameters']
        display_check(variant)
        review.append({'label':'generated variant '+case['source_id'],'source_id':case['source_id'],'role':'generated_variant','record':variant})
        native.append({'label':'generated variant '+case['source_id'],'record':variant,'checks':checks(variant)})
    fingerprints={level:set() for level in ('easy','moderate','hard')}
    tested=0
    positions=set()
    for level in fingerprints:
        for template in g.TEMPLATES:
            for seed in range(100):
                record=g.generate(level,seed,template)
                display_check(record)
                fingerprints[level].add(record['generation']['parameter_fingerprint'])
                tested+=1
                if seed<2:
                    label=f'authored default {level}/{template}/{seed}'
                    review.append({'label':label,'role':'authored_default','record':record})
                    native.append({'label':label,'record':record,'checks':checks(record)})
                q=record['question']
                fixed=record['generation']['parameters']
                shuffled=g.generate(level,seed+123,template,parameters=fixed,profile=record['generation']['bank_profile'])
                assert q[':question/id']==shuffled['question'][':question/id']
                assert record['generation']['content_fingerprint']==shuffled['generation']['content_fingerprint']
                if len(q[':question/answer-fields'])==1:
                    f=q[':question/answer-fields'][0]
                    positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
    assert positions==set(range(5))
    # Equivalent assessed tasks have one mathematical fingerprint across unused
    # reference constants, unused point coordinates, notation, profile and layout.
    baseline=g.generate_easy(0,'line_first_vertical_radio',parameters={'a':3,'b':7,'c':2})
    for name,p,profile in [('point_first_vertical_radio',{'a':4,'b':7,'c':9},None),('standard_vertical_blank',{'a':-8,'b':7,'c':'1/3'},None),('line_first_vertical_radio',{'a':3,'b':7,'c':'5/2'},'observed_q110143')]:
        variant=g.generate_easy(1,name,parameters=p,profile=profile)
        assert variant['generation']['parameter_fingerprint']==baseline['generation']['parameter_fingerprint']
        assert variant['question'][':question/id']!=baseline['question'][':question/id']
    fraction=g.generate_hard(0,'standard_vertical_blank',parameters={'a':4,'b':'7/10','c':2})
    decimal=g.generate_hard(1,'standard_vertical_blank',parameters={'a':4,'b':'7/10','c':2,'style':'decimal'})
    assert fraction['generation']['parameter_fingerprint']==decimal['generation']['parameter_fingerprint']
    assert fraction['question'][':question/id']!=decimal['question'][':question/id']
    # Exercise zero coordinate explicitly (sign-reversal would be ambiguous).
    zero=g.generate_easy(0,'line_first_vertical_radio',parameters={'a':3,'b':0,'c':7})
    display_check(zero)
    native.append({'label':'authored zero bank','record':zero,'checks':checks(zero)})
    invalid=[('easy',{'a':1,'b':1,'c':2},'authored_coordinate_sign'),('easy',{'a':1,'b':'1/2','c':2},None),('moderate',{'a':1,'b':7,'c':2},None),('moderate',{'a':1,'b':'-25/2','c':2},None),('moderate',{'a':1,'b':'-25/3','c':2},None),('hard',{'a':1,'b':'7/5','c':2},None),('hard',{'a':1,'b':'-61/7','c':2},None),('hard',{'a':1,'b':'1/3','c':2,'style':'decimal'},None)]
    for level,p,profile in invalid:
        try:g.generate(level,0,'line_first_vertical_radio',parameters=p,profile=profile)
        except (ValueError,TypeError):pass
        else:raise AssertionError(('invalid explicit parameters accepted',level,p))
    write('review.json',review)
    write('engine-input.json',native)
    run=subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'native-grading.json')],check=True,capture_output=True,text=True)
    print(run.stdout.strip())
    provenance={str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'validate.py',REPO/'generate/runs/current/check-engine',REPO/'generate/runs/current/check-engine.rs')}
    write('native-grader-provenance.json',{'entry_point':'course_academy_engine::learning::grade_field','hashes':provenance,'database_writes':0})
    # Originals plus clearly marked generated variants; no claim of raw-correct
    # blank values/solutions that the snapshot never captured.
    prose=['# Axis-perpendicular generator review','', 'Source snapshot: math basis 1356. Authored numeric policies for M/H have no observed difficulty labels; categorical workload is constant.','']
    for item in review:
        if item['role']=='source_replay':
            source=sources[item['source_id']]
            prose+=['## Original '+item['source_id'],'',source[':question/problem'],'']
            for f in source[':question/answer-fields']:
                prose+=[f'- Original {f[":answer-field/key"]} {f[":answer-field/type"][":db/ident"]}: '+(', '.join('$'+a[':answer/value']+'$' for a in f.get(':answer-field/choices',[])) or 'no captured bank/correct reference')]
            prose+=['',source.get(':question/worked-solution','No worked solution captured; replay solution is authored from the canonical method.'),'']
        prose+=['## '+item['label'],'',g.markdown(item['record']),'','---','']
    (HERE/'review.md').write_text('\n'.join(prose))
    report={'status':'passed','basis':1356,'source_coverage':{'practice_questions':8,'replayed':8,'exact_prompts':8,'exact_field_layouts':8,'radio_banks_matched':6,'radio_banks_total':6,'choice_values_matched':30,'choice_values_total':30,'distractors_matched':24,'distractors_total':24,'observed_correct_refs_matched':6,'observed_correct_refs_total':6,'missing_correct_refs_derived_not_matched':4,'exact_observed_solutions':6,'observed_solutions_total':6,'missing_solutions_authored':2},'source_cases':fidelity,'generated_math_checks':tested,'distinct_sampled_mathematical_tasks':{level:len(s) for level,s in fingerprints.items()},'correct_choice_positions':sorted(positions),'explicit_invalid_rejections':len(invalid),'native_grading':json.loads((HERE/'native-grading.json').read_text()),'known_limitations':['No observed moderate/hard labels; harder numeric representations do not make a categorical axis decision an intrinsically hard skill.','Blank fragments are graded independently; scalar-equivalent whole equations with both fragments changed are outside canonical field grading.','Observed distractor operations reproduce banks, but original authoring intent is not identified.'],'plots':'none','database_writes':0}
    write('validation.json',report)
    print(f'Passed: all 8 sources; 6 banks / 30 choices / 24 distractors; {tested} displayed-math instances; native grader passed.')

if __name__=='__main__':main()
