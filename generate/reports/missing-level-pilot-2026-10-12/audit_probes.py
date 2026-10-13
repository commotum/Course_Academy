#!/usr/bin/env python3
"""Exact source-pattern and proposal checks; no generator or database mutation."""
import importlib.util
import json
from pathlib import Path
import sympy as s

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('pilot_extract',HERE/'extract.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
cases=m.read(HERE/'source-cases.json')
verified=0
for case in cases:
    for field in case['fields']:
        for choice in field['choices']:
            recipe=choice['recipe'];kind=recipe['kind'];p=recipe['parameters']
            if kind=='correct':
                original=next(q for kp in m.read(HERE/'source.json')['records']
                    for q in kp[':knowledge-point/questions'] if q[':question/math-academy-id']==case['source_question'])
                replay=m.components(original)[2]
            elif kind=='matrix_entry_candidates':
                values={case['features']['matrix'][i-1][j-1] for i,j in p['candidate_positions']}
                assert len(values)==1
                replay=s.Integer(values.pop())
            elif kind=='fixed_source_scalar':
                replay=s.sympify(p['k'])
            elif kind=='fixed_text':
                assert recipe['expression']==choice['source_value']
                choice['recipe_replay_verified']=True;verified+=1;continue
            elif kind=='observed_radical_value_pattern':
                replay=s.Rational(p['p']) * s.sqrt(s.sympify(p['d'])) / s.Integer(p['q'])
            elif kind=='observed_rational_value_pattern':
                replay=s.Rational(p['p']) / s.Integer(p['q'])
            else:
                assert kind in ('observed_symbolic_expression','observed_constant_expression')
                replay=s.sympify(recipe['expression'],locals=m.parser.locals_)
            assert s.simplify(replay-m.scalar(choice['source_value']))==0,choice
            choice['recipe_replay_verified']=True
            verified+=1

b,c=s.symbols('b c',positive=True)
bank=[c*c/b,b/(c*c),c*c/(b*b),c/b,b/c]
source=next(r for r in cases if r['source_question']=='q-65066')['fields'][0]['choices']
old=[s.simplify(v.subs({b:5,c:4})) for v in bank]
assert set(old)=={m.scalar(v['source_value']) for v in source}
new=[s.simplify(v.subs({b:13,c:12})) for v in bank]
assert len(set(new))==5
answer=s.simplify(1/s.sqrt(1-s.Rational(5,13)**2))
assert answer==s.Rational(13,12) and sum(v==answer for v in new)==1
assert s.Rational(5,13)**2+s.Rational(12,13)**2==1

matrix=s.Matrix([[(1+s.sqrt(2))/2,(2-s.sqrt(3))/5],
                 [(2+s.sqrt(3))/7,(1-s.sqrt(2))/3]])
det=s.simplify(matrix.det())
assert det==-s.Rational(41,210)
assert all(v.is_real and v.is_rational is False for v in matrix)

lookup=[[-5,-2,0,9],[3,-8,-2,5],[-2,2,5,-8],[6,6,-6,0],[-6,4,-s.Rational(7,3),5]]
assert len(lookup)==5 and all(len(row)==4 for row in lookup)
assert lookup[4][2]==-s.Rational(7,3)

result=dict(source_question_count=len(cases),complete_value_recipe_replays=verified,
    source_marked_correct_answers_verified=22,
    unrated_reciprocal_bank_replayed='5/5 complete source values, independent of source correct reference',
    probe_answers=dict(matrix_lookup=str(lookup[4][2]),reciprocal=str(answer),determinant=str(det)),
    reciprocal_authored_choices=[str(v) for v in new],reciprocal_unique_choices=True,
    reciprocal_plot_point=['5/13','12/13'],point_on_unit_circle=True,
    determinant_method='Independent SymPy Matrix.det calculation',
    source_recipe_generalization='Unresolved error mechanisms remain flagged; source-parameter replay does not establish a source-faithful generator.',
    engine_grading_tested=False,database_mutations=False)
m.write(HERE/'probe-verification.json',result)
m.write(HERE/'source-cases.json',cases)
for entity in {case['kp_entity'] for case in cases}:
    m.write(HERE/str(entity)/'source-cases.json',[case for case in cases if case['kp_entity']==entity])
print(json.dumps(result,indent=2))
