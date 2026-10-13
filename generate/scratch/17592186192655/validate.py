#!/usr/bin/env python3
"""Independent display parsing, raw replay, task domains, identities and real grading.
Run .venv/bin/python generate/scratch/17592186192655/validate.py.
"""
import copy
import importlib.util
import itertools
import json
from pathlib import Path
import re
import subprocess
import sys
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
spec=importlib.util.spec_from_file_location('second_variable',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
SOURCE=json.loads((HERE/'source.json').read_text())
transformations=standard_transformations+(implicit_multiplication_application,)


def expr(text,variables):
    return parse_expr(text.replace(' ','').replace('&',''),local_dict={v:s.Symbol(v) for v in variables},transformations=transformations)


def residual(text,variables):
    left,right=text.split('=')
    return s.expand(expr(left,variables)-expr(right,variables))


def coefficients(text,variables):
    e=residual(text,variables);u,v=[s.Symbol(x) for x in variables]
    assert e.is_polynomial(u,v)
    assert s.Poly(e,u,v).total_degree()<=1
    return tuple(e.coeff(x) for x in (u,v))+(-e.subs({u:0,v:0}),)


def balanced(text):
    # Literal \{ glyph doesn't begin a TeX group; field placeholders aren't TeX.
    text=re.sub(r'\{\{field-[12]\}\}','',text).replace('\\{','').replace('\\}','')
    depth=0
    for c in text:
        if c=='{':depth+=1
        elif c=='}':depth-=1
        assert depth>=0,'Closing TeX group without opening'
    assert depth==0,'Unbalanced nonliteral TeX groups'
    assert text.count('$')%2==0
    assert not re.search(r'(?<![A-Za-z])(?:--|\+-)',text),'Bare signed operator'


def check_record(record):
    assert record['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    q=record['question'];meta=record['generation'];variables=meta['parameters']['variables']
    assert meta['source']==g.PROVENANCE
    assert meta['dependencies']['python']==sys.version.split()[0]
    for f in q[':question/answer-fields']:
        assert f[':answer-field/type']==':answer-field.type/select'
        for a in f[':answer-field/choices']:
            assert a[':answer/type']==(':answer.type/math' if f[':answer-field/key']=='field-2' else ':answer.type/text')
            assert str(__import__('uuid').UUID(a[':answer/id']))==a[':answer/id']
    assert str(__import__('uuid').UUID(q[':question/id']))==q[':question/id']
    if meta['evidence_only'] and meta['profile'].startswith('raw-'):
        assert ':question/difficulty' not in q and ':question/worked-solution' not in q
        assert all(':answer-field/correct' not in f for f in q[':question/answer-fields'])
        assert not meta['eligible_for_learning']
        bare=re.search(r'\$\{([^$]+)\$',q[':question/problem']).group(1)
        rawrows=[coefficients(r,variables) for r in bare.split(';')]
        choices=next(f[':answer-field/choices'] for f in q[':question/answer-fields'] if f[':answer-field/key']=='field-2')
        rawvalid=[(i,s.Rational(a[':answer/value'])) for i in range(2) for a in choices if s.Rational(a[':answer/value'])*rawrows[i][1]+rawrows[1-i][1]==0]
        assert len(rawvalid)==1
        try:balanced(q[':question/problem'])
        except AssertionError:pass
        else:raise AssertionError('Documented raw formatting anomaly disappeared')
        return
    balanced(q[':question/problem']);balanced(q[':question/worked-solution'])
    assert meta['eligible_for_learning']==(not meta['evidence_only'])
    assert q[':question/difficulty']==':question.difficulty/'+meta['level']
    # Read actual equations from prompt; no generation coefficients used for math.
    system=re.search(r'\$\\\{([^$]+)\$',q[':question/problem']).group(1)
    rows=[coefficients(row,variables) for row in system.split(';')]
    a,b=rows;assert a[1] and b[1]
    scale_first=-b[1]/a[1];scale_second=-a[1]/b[1]
    viable=[(0,scale_first)] if abs(scale_first)>=2 and scale_first.q==1 else [(1,scale_second)]
    assert len(viable)==1
    row,m=viable[0];assert m.q==1 and abs(m)>=2
    fields={f[':answer-field/key']:f for f in q[':question/answer-fields']}
    assert set(fields)=={'field-1','field-2'}
    selected={}
    ids=[]
    for key,field in fields.items():
        assert '{{'+key+'}}' in q[':question/problem']
        assert field[':answer-field/type']==':answer-field.type/select'
        choices=field[':answer-field/choices'];assert len(choices)==(2 if key=='field-1' else 4)
        assert len({a[':answer/id'] for a in choices})==len(choices)
        ids += [a[':answer/id'] for a in choices]
        ref=field[':answer-field/correct'];assert ref[0]==':answer/id'
        selected[key]=next(a[':answer/value'] for a in choices if a[':answer/id']==ref[1])
    assert len(ids)==len(set(ids))
    assert selected=={'field-1':'first' if row==0 else 'second','field-2':g.tex(m)}
    values=[s.Rational(a[':answer/value']) for a in fields['field-2'][':answer-field/choices']]
    valid=[]
    for i in range(2):
        for value in values:
            if value*rows[i][1]+rows[1-i][1]==0:valid.append((i,value))
    assert valid==[(row,m)],'Full paired-dropdown combination is not uniquely valid'
    # The unchanged row is read from the operative marked-row block, not implied
    # by equation equivalence or solution-set equivalence.
    sol=q[':question/worked-solution']
    marked=re.search(r'\$\$\n\\\{([^$]+)\n\$\$',sol).group(1).split('; ')
    for i,text in enumerate(marked):
        if i==row:
            mo=re.fullmatch(r'\((.+)\)\\cdot \(([-0-9]+)\)',text)
            assert mo and s.Rational(mo.group(2))==m
            assert coefficients(mo.group(1),variables)==rows[i]
        else:
            assert '\\cdot' not in text and coefficients(text,variables)==rows[i]
    actual=re.search(r'\\begin\{aligned\}\n(.+?)\n\\end\{aligned\}',sol,re.S).group(1).split(' \\\\\n')
    assert len(actual)==4,'Canonical ordered four-row elimination chain changed'
    changed=list(rows);changed[row]=tuple(m*x for x in rows[row])
    for i in (0,1):assert coefficients(actual[i],variables)==changed[i]
    expected=tuple(changed[0][i]+changed[1][i] for i in range(3))
    assert expected[1]==0 and expected[0]!=0
    assert coefficients(actual[2],variables)==expected
    assert actual[2].startswith('(') and ') &= (' in actual[2], 'Grouped sum stage collapsed'
    assert coefficients(actual[3],variables)==expected
    assert variables[1] not in actual[2] and variables[1] not in actual[3]
    # Read all inline coefficient, marked multiplier and conclusion values.
    opening=f"Notice that the coefficient of ${variables[1]}$ in the first equation is ${g.tex(a[1])}$, while in the second equation it is ${g.tex(b[1])}$."
    assert sol.startswith(opening)
    name='first' if row==0 else 'second';other='second' if row==0 else 'first'
    assert f'If we multiply the {name} equation by ${{\\color{{blue}}{g.tex(m)}}}$' in sol
    assert f'will turn into ${g.tex(m*rows[row][1])}$' in sol
    assert f'coefficient of ${g.tex(rows[1-row][1])}$ in the {other} equation.' in sol
    assert f'\\text{{{name}}}' in sol.split('Therefore, the correct answer')[1]
    assert f'\\color{{blue}}{g.tex(m)}' in sol.split('Therefore, the correct answer')[1]
    assert 'substitute' not in sol and 'solution to the system' not in sol
    if not meta['evidence_only']:g.validate_parameters(meta['parameters'],meta['level'])


def normalized_fields(q):
    return {f[':answer-field/key']:{'type':f[':answer-field/type'].get(':db/ident') if isinstance(f[':answer-field/type'],dict) else f[':answer-field/type'],
      'correct_present':':answer-field/correct' in f,'choices':sorted((a[':answer/type'].get(':db/ident') if isinstance(a[':answer/type'],dict) else a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices'])} for f in q[':question/answer-fields']}


def main():
    cases=[];fidelity=[];review=[];bank_map=[]
    canonical=SOURCE['record'][':knowledge-point/canonical-example']
    canonical_parameters=dict(a1=3,b1=4,c1=2,a2=1,b2=-2,c2=4,variables=['x','y'])
    canonical_normal=g.generate_moderate(13,template='spaced',profile='coefficient',parameters=canonical_parameters)
    check_record(canonical_normal)
    normalized_canonical=canonical[':question/worked-solution'].replace('{(3x + 4y = 2;', r'\{3x + 4y = 2;')
    assert canonical_normal['question'][':question/worked-solution']==normalized_canonical
    review.append({'label':'Canonical-derived normal completion (presentation normalization only)','record':canonical_normal})
    for original in SOURCE['record'][':knowledge-point/questions']:
        source_id=original[':question/math-academy-id'];parameters=g.ANCHORS[source_id];template=g.SOURCE_TEMPLATES[source_id]
        case={'source_id':source_id,'template':template,'parameters':parameters,'bank_profile':'raw-'+source_id,'authored_level':'easy' if source_id=='q-210947' else 'hard'}
        cases.append(case)
        level=case['authored_level']
        generated=g.generate(level,seed=17,template=template,parameters=parameters,profile=case['bank_profile'])
        q=generated['question'];check_record(generated)
        assert q[':question/problem']==original[':question/problem']
        assert normalized_fields(q)==normalized_fields(original)
        for key in [':question/difficulty',':question/worked-solution',':question/answer-fields']:
            assert (key in q)==(key in original),'Raw source attribute presence changed'
        fidelity.append({'source_id':source_id,'raw_prompt_exact':True,'complete_fields_exact':True,'answer_values':6,'original_correct_designations':0,'matched_correct_designations':0,'missing_difficulty':True,'missing_worked_solution':True,'missing_correct_refs':2,'raw_tex_ineligible':True})
        review.append({'label':'Original raw '+source_id,'record':generated})
        completed=g.generate(level,seed=17,parameters=parameters,profile='completed-'+source_id);check_record(completed)
        review.append({'label':'Authored supported completion '+source_id+' (evidence-only opaque bank)','record':completed})
        for f in original[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                val=a[':answer/value'];row,m=g.operation(parameters)
                if f[':answer-field/key']=='field-1':recipe='row-direction label '+val
                elif abs(int(val))==abs(m):recipe='integer target ratio with '+('positive' if int(val)>0 else 'negative')+' sign'
                elif source_id=='q-210947':recipe='±abs(first-row FIRST-variable coefficient); opaque evidence-only hypothesis'
                else:recipe='±abs(unchanged target coefficient); coefficient copied instead of ratio'
                bank_map.append({'source_id':source_id,'field_key':f[':answer-field/key'],'original_answer_id':a[':answer/id'],'value':val,'profile':case['bank_profile'],'recipe':recipe,'exact_value_replayed':True})
        changed=dict(parameters)
        if source_id=='q-210947':changed.update(a1=7,b1=8,a2=-3,b2=-1,c1=2,c2=-4)
        else:changed.update(a1=5,b1=3,a2=4,b2=18,c1=-2,c2=5)
        for profile in ['raw-'+source_id,'completed-'+source_id]:
            r=g.generate(level,22,parameters=changed,profile=profile);check_record(r);review.append({'label':'Changed-parameter public '+profile,'record':r})
    (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
    (HERE/'bank-mapping.json').write_text(json.dumps(bank_map,indent=2)+'\n')
    tested=[];counts={};templates={};profiles={};signs={};directions={};correct_positions={}
    for level in g.BOUNDS:
        pool=[]
        for seed in range(160):
            r=g.generate(level,seed);check_record(r);pool.append(r);tested.append(r)
        counts[level]=len({r['generation']['mathematical_fingerprint'] for r in pool})
        templates[level]=sorted({r['generation']['template'] for r in pool});profiles[level]=sorted({r['generation']['profile'] for r in pool})
        signs[level]=sorted({int(s.sign(s.Rational(r['generation']['operation']['multiplier']))) for r in pool})
        directions[level]=sorted({r['generation']['operation']['transformed_row'] for r in pool})
        correct_positions[level]=sorted({next(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1]) for r in pool})
        assert len(templates[level])==2 and signs[level]==[-1,1] and directions[level]==[1,2]
        assert correct_positions[level]==[0,1,2,3]
        for template in g.TEMPLATES:
            for profile in (['difference'] if level=='easy' else ['difference','coefficient']):
                for seed in range(12):
                    r=g.generate(level,seed,template=template,profile=profile);check_record(r)
                review.append({'label':f'Generated {level} {template} {profile}', 'record':g.generate(level,7,template=template,profile=profile)})
        # Fixed displayed values mean identity independent of seed/bank order.
        r=pool[0];meta=r['generation'];same=g.generate(level,901,template=meta['template'],profile=meta['profile'],parameters=meta['parameters'])
        assert r['question'][':question/id']==same['question'][':question/id']
        assert r['generation']['mathematical_fingerprint']==same['generation']['mathematical_fingerprint']
        if level!='easy':
            alt=g.generate(level,0,template=meta['template'],profile='coefficient' if meta['profile']=='difference' else 'difference',parameters=meta['parameters'])
            assert alt['question'][':question/id']!=r['question'][':question/id']
            assert alt['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
    # Complete finite substantive target-ratio catalog, including all sign/row directions.
    domain={}
    for level,((lo,hi),(rlo,rhi)) in g.BOUNDS.items():
        tasks=set();operands=set();n=0
        for small,ratio,s1,s2,d in itertools.product(range(lo,hi+1),range(rlo,rhi+1),[-1,1],[-1,1],[0,1]):
            b1,b2=small*s1,small*ratio*s2
            if d:b1,b2=b2,b1
            p={'a1':1,'b1':b1,'c1':1,'a2':2,'b2':b2,'c2':3,'variables':['x','y']}
            if p['a1']*p['b2']==p['a2']*p['b1']:p['a2']=3
            # nonunit target operands differ but global target scaling doesn't create a new ratio task.
            for profile in (['difference'] if level=='easy' else ['difference','coefficient']):
                r=g.generate(level,11,parameters=p,profile=profile);check_record(r);n+=1;tasks.add(r['generation']['mathematical_fingerprint'])
            operands.add((b1,b2))
        domain[level]={'full_target_operand_catalog':len(operands),'canonical_division_operand_tasks':len(tasks),'whole_profile_instances_checked':n}
    # Same task under positive common row scaling; no bank/profile inflation.
    p={'a1':1,'b1':2,'c1':1,'a2':4,'b2':6,'c2':-1,'variables':['x','y']}
    a=g.generate_moderate(parameters=p,profile='difference');q={k:([*v] if k=='variables' else 2*v) for k,v in p.items()};b=g.generate_moderate(parameters=q,profile='difference')
    assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
    assert a['question'][':question/id']!=b['question'][':question/id']
    # Explicit input rejects number forms that remove workload, outside limits and bank collisions.
    rejected=0
    for level,p,profile in [('easy',g.ANCHORS['q-211000'],'difference'),('moderate',g.ANCHORS['q-210947'],'difference'),('hard',p,'difference'),('easy',g.ANCHORS['q-210947'],'coefficient')]:
        try:g.generate(level,parameters=p,profile=profile)
        except ValueError:rejected+=1
        else:raise AssertionError('Explicit workload/profile guard bypass')
    # Regression catches corrupted unchanged row, collapsed grouped stage, final prose multiplier.
    corruptions=0
    base=tested[0]
    bad=copy.deepcopy(base);sol=bad['question'][':question/worked-solution'];block=re.search(r'\\begin\{aligned\}\n(.+?)\n\\end\{aligned\}',sol,re.S).group(1);stages=block.split(' \\\\\n');new=list(stages);new[2]=new[3];sol=sol.replace(block,' \\\\\n'.join(new));bad['question'][':question/worked-solution']=sol
    try:check_record(bad)
    except (AssertionError,AttributeError,ValueError):corruptions+=1
    else:raise AssertionError('Grouped-stage regression missed')
    bad=copy.deepcopy(base);sol=bad['question'][':question/worked-solution'];head,tail=sol.split('Therefore, the correct answer',1);tail=tail.replace('\\text{first}','\\text{WRONG}').replace('\\text{second}','\\text{WRONG}');bad['question'][':question/worked-solution']=head+'Therefore, the correct answer'+tail
    try:check_record(bad)
    except AssertionError:corruptions+=1
    else:raise AssertionError('Final conclusion regression missed')
    bad=copy.deepcopy(base);sol=bad['question'][':question/worked-solution'];row=base['generation']['operation']['transformed_row']-1
    mark=re.search(r'\$\$\n\\\{([^$]+)\n\$\$',sol).group(1);parts=mark.split('; ');unchanged=1-row;parts[unchanged]='('+parts[unchanged]+r')\cdot (2)';bad['question'][':question/worked-solution']=sol.replace(mark,'; '.join(parts))
    try:check_record(bad)
    except AssertionError:corruptions+=1
    else:raise AssertionError('Unchanged-row operation regression missed')
    native=[]
    # All normal generated review instances plus observed supported completions.
    for item in review:
        r=item['record']
        if ':question/worked-solution' not in r['question']:continue
        checks=[]
        for i,f in enumerate(r['question'][':question/answer-fields']):
            for answer in f[':answer-field/choices']:
                correct=answer[':answer/id']==f[':answer-field/correct'][1]
                checks.append({'field_index':i,'submitted_answer_id':answer[':answer/id'],'expected':'accepted' if correct else 'rejected','purpose':'all displayed bank choices; field IDs owned by actual question'})
        native.append({'label':item['label'],'record':r,'checks':checks})
    (HERE/'engine-input.json').write_text(json.dumps(native,indent=2)+'\n')
    result=subprocess.run([str(ROOT/'runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True)
    assert result.returncode==0,result.stdout+result.stderr
    native_report=json.loads((HERE/'engine-report.json').read_text())
    (HERE/'review.json').write_text(json.dumps(review,indent=2)+'\n')
    paragraphs=['# Elimination of the second variable: originals and generated variants','Sources: math basis1356; all difficulty labels in normal output are authored. Raw evidence is ineligible for learning. Raw source system braces are deliberately retained; normal output escapes the literal brace. Missing original designation is never counted as matched.']
    for item in review:paragraphs += ['## '+item['label'],g.markdown(item['record'])]
    (HERE/'review.md').write_text('\n\n'.join(paragraphs)+'\n')
    report={'passed':True,'source':g.PROVENANCE,'runtime':{'python':sys.version.split()[0],'sympy':s.__version__},'source_questions':2,'raw_prompt_matches':2,'complete_source_question_banks_matched':2,'complete_source_field_banks_matched':4,'answer_values_matched':12,'answer_values_total':12,'original_correct_ref_matches':0,'original_correct_refs_total':0,'missing_original_correct_refs':4,'raw_key_presence_matches':2,'raw_missing_solutions_preserved':2,'raw_unrated_preserved':2,'normal_presentation_repairs':2,'normal_designations_authored':4,'source_practice_solution_fidelity_denominator':0,'canonical_stage_sequence':'notice/marked-row/two-equations/grouped-addition/collected-row/conclusion','canonical_mathematical_repairs':0,'canonical_full_prose_sequence_matches':1,'canonical_full_prose_sequence_denominator':1,'raw_formatting_ineligible_count':2,'native_grading':{k:native_report[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']},'random_normal_records_checked':len(tested),'sampled_task_counts':counts,'finite_task_catalog':domain,'default_templates':templates,'default_profiles':profiles,'sign_coverage':signs,'row_direction_coverage':directions,'correct_position_coverage':correct_positions,'explicit_rejections':rejected,'corruption_regressions':corruptions,'unresolved_source_bank_interpretations':['q-210947 ±first-row first-variable coefficient; evidence only'],'remaining_blockers':[]}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2));print(result.stdout.strip())

if __name__=='__main__':main()
