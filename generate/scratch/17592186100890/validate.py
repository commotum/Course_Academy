"""Local guide checks and review generation; neither EDB reads nor writes."""
from __future__ import annotations

import importlib.util
import hashlib
import json
import re
from pathlib import Path
import subprocess
import sys
import tempfile
import uuid
from source_fidelity import equation, expression, equivalent_equations, match_bank

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
spec = importlib.util.spec_from_file_location("trig_draft", ROOT.with_suffix(".py"))
g = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = g
spec.loader.exec_module(g)
SOLUTION_AUDIT = {}


def write(name, data):
    (ROOT/name).write_text(json.dumps(data, indent=2, ensure_ascii=False)+"\n")


def check_solution(record):
    """Read every rendered equality, independently of the generator's AST.

    Exact rational unit-circle coordinates test each intermediate equality,
    including opening isolation, identity derivation, quotient substitution,
    signed scales and expansion. The generator separately proves its final
    relation over the complete interval; these are checks of displayed steps.
    """
    meta = record['generation']
    p = meta['parameters']
    spec = g.TEMPLATES[meta['template']]
    quadrant = p.get('quadrant', 1)
    ss, cs = {1:(1,1), 2:(1,-1), 3:(-1,-1), 4:(-1,1)}[quadrant]
    family = spec.family
    if family.startswith('ellipse'):
        fx, fy = ('sin','cos') if family == 'ellipse_sin' else ('cos','sin')
    elif spec.level == 'hard':
        fx, fy = ('sin' if family.startswith('sin_double') else 'cos'), 'cos2'
    else:
        fx, fy = family.split('_')
    solution = record['question'][':question/worked-solution']
    groups = re.findall(r'\$\$(.*?)\$\$', solution, flags=re.S)
    groups += [block for block in re.findall(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)', solution, flags=re.S) if '=' in block]
    rows = []
    for block in groups:
        block = block.replace(r'\begin{aligned}', '').replace(r'\end{aligned}', '')
        previous = None
        for row in block.split(r'\\'):
            row = row.replace('&', '').strip().rstrip('.')
            if not row:
                continue
            for segment in re.split(r'\\Rightarrow(?:\\quad)?', row):
                segment = segment.replace(r'\quad', '').strip()
                sides = segment.split('=')
                if len(sides) < 2:
                    raise AssertionError(('Unverified solution row', segment))
                if not sides[0].strip():
                    assert previous is not None, segment
                    sides[0] = previous
                previous = sides[0]
                rows.append(sides)
    probes = (g.sp.Rational(1,5), g.sp.Rational(3,4))
    if spec.family.startswith('ellipse') or spec.level == 'hard':
        probes += (g.sp.Rational(4,3), g.sp.Rational(-1,3))
    for u in probes:
        s, c = ss*2*u/(1+u*u), cs*(1-u*u)/(1+u*u)
        values = {'sin':s, 'cos':c, 'tan':s/c, 'cot':c/s,
                  'sec':1/c, 'csc':1/s, 'cos2':c*c-s*s}
        xx, yy = p['a']*values[fx]+p.get('h',0), p['b']*values[fy]+p.get('k',0)
        for sides in rows:
            parsed = []
            for side in sides:
                side = side.strip().rstrip('.')
                side = re.sub(r'\\cos 2t', lambda _: '{'+g.tex(values['cos2'])+'}', side)
                side = re.sub(r'\\(sin|cos|tan|cot|sec|csc)(\^2)? t',
                              lambda m: '{'+g.tex(values[m[1]]**(2 if m[2] else 1))+'}', side)
                parsed.append(expression(side).subs({g.X:xx,g.Y:yy}, simultaneous=True))
            assert all(g.sp.simplify(value-parsed[0]) == 0 for value in parsed[1:]), (meta['template'],p,sides,parsed)
    SOLUTION_AUDIT[record['question'][':question/id']] = len(rows)
    return len(rows)


def check_record(record):
    q,meta = record['question'],record['generation']
    field = q[':question/answer-fields'][0]
    answers = field[':answer-field/choices']
    template = g.TEMPLATES[meta['template']]
    profile = meta['bank_profile']
    assert (profile is not None) == (template.kind == 'radio')
    if profile:
        assert g.BANK_PROFILES[profile].template == meta['template']
        assert g.profile_eligible(profile,meta['parameters'])
        assert {item['recipe'] for item in meta['distractor_recipes'].values()} == {r.label for r in g.BANK_PROFILES[profile].recipes}
    assert record == json.loads(json.dumps(record))
    assert len(q[':question/answer-fields']) == 1
    assert len(answers) == (5 if template.kind == 'radio' else 1)
    assert len({a[':answer/id'] for a in answers}) == len(answers)
    assert len(meta['distractor_recipes']) == (4 if template.kind == 'radio' else 0)
    assert sum(a[':answer/id'] == field[':answer-field/correct'][1] for a in answers) == 1
    for ident in [q[':question/id'],field[':answer-field/id']]+[a[':answer/id'] for a in answers]:
        assert str(uuid.UUID(ident)) == ident
    assert field[':answer-field/id'] not in {a[':answer/id'] for a in answers}
    # Verify what the learner actually sees, independently of the recipe AST.
    for answer in answers:
        if template.kind == 'blank':
            assert g.sp.simplify(expression(answer[':answer/value'])-g.sp.sympify(meta['answer_math']['fragment']))==0
        else:
            math=meta['answer_math'] if answer[':answer/id']==field[':answer-field/correct'][1] else meta['distractor_recipes'][answer[':answer/id']]
            expected=(g.sp.sympify(math['lhs']),g.sp.sympify(math['rhs']))
            assert equivalent_equations(equation(answer[':answer/value']),expected),answer
    assert all(a[':answer/type'] == ':answer.type/math' and ':answer/feedback' not in a and '$' not in a[':answer/value'] for a in answers)
    assert ':question/math-academy-id' not in q
    assert q[':question/worked-solution'].startswith(g.OPENING)
    assert q[':question/problem'].count('$') % 2 == 0
    assert q[':question/worked-solution'].count('$') % 2 == 0
    assert meta['plot_rating'] == 'none' and meta['plot_assets'] == {}
    assert meta['source_analysis']['basis_t'] == 1356
    if template.kind == 'blank':
        assert q[':question/problem'].count('{{field-1}}') == 1
        assert '=' not in answers[0][':answer/value']
        assert meta['answer_shape'] in ('lhs','rhs')
        assert ('{{field-1}}$=1.$' in q[':question/problem']) == (meta['answer_shape'] == 'lhs')
        assert ('So' not in q[':question/worked-solution']) == template.family.startswith('ellipse')
    if template.level == 'moderate':
        assert 'We used here that' in q[':question/worked-solution']
        definition = 'a cotangent' if template.family.endswith('_cot') else 'a tangent'
        assert 'Now, using the definition of '+definition+', we obtain' in q[':question/worked-solution']
        assert template.kind == 'radio'
        assert meta['bank_origin'] == g.BANK_PROFILES[profile].origin
        if meta['bank_origin'] == 'authored':
            assert meta['authored_extension']
            assert not any(a[':answer/feedback'] for a in answers if ':answer/feedback' in a)
    if template.family == 'cos_double':
        last_block = q[':question/worked-solution'].split('\\begin{aligned}')[-1].split('\\end{aligned}')[0]
        p = meta['parameters']
        expected_rows = (4 if p['a'] > 0 and p['b'] > 0 else 3) + (template.kind == 'blank')
        assert last_block.count(' & ') == expected_rows
    preview = g.markdown(record)
    assert 'Distractor reasoning' not in preview
    assert all(item['recipe'] not in preview for item in meta['distractor_recipes'].values())
    check_solution(record)


def engine_checks(record, label):
    meta = record['generation']
    template = g.TEMPLATES[meta['template']]
    field = record['question'][':question/answer-fields'][0]
    answers = field[':answer-field/choices']
    correct_uuid = field[':answer-field/correct'][1]
    correct_index = next(i for i,a in enumerate(answers) if a[':answer/id'] == correct_uuid)
    canonical = answers[correct_index][':answer/value']
    if template.kind == 'radio':
        checks = [{'submitted':str(100+i),'expected':'accepted' if i == correct_index else 'rejected',
                   'purpose':'canonical selection' if i == correct_index else 'authored distractor selection'} for i in range(5)]
    else:
        p = meta['parameters']
        built = g.BUILDERS[template.level](template,p)
        if meta['answer_shape'] == 'lhs':
            equivalent = g.tex(g.sp.expand(built.relation.lhs))
            shape_error = canonical+'=1'
        elif template.family == 'cot_csc':
            equivalent = f"{p['b']}*sqrt(1+(x/{p['a']})^2)"
            shape_error = 'y='+canonical
        else:
            equivalent = str(p['b'])+'*('+g.tex(built.relation.rhs/p['b'])+')'
            shape_error = 'y='+canonical
        checks = [{'submitted':canonical,'expected':'accepted','purpose':'canonical blank fragment'},
                  {'submitted':equivalent,'expected':'accepted','purpose':'equivalent correctly shaped blank entry'},
                  {'submitted':'('+canonical+')+1','expected':'rejected','purpose':'mathematically wrong expression'},
                  {'submitted':'-('+canonical+')','expected':'rejected','purpose':'wrong sign or branch'},
                  {'submitted':shape_error,'expected':'unresolved','purpose':'complete equation is not a valid blank fragment'}]
    return {'label':label,'record':record,'checks':checks}


def boundary_parameters(template, high):
    f = template.family
    if f.startswith('ellipse'):
        return {'a':6 if high else 2,'b':1,'h':0,'k':5 if high else -1} if template.kind == 'blank' else \
            {'a':5 if high else 1,'b':4 if high else 1,'h':4 if high else -1,'k':-4 if high else 1}
    if template.level == 'moderate':
        return {'a':4,'b':4} if high else {'a':1,'b':1}
    if template.level == 'easy':
        return {'a':6 if high else 2,'b':5 if high else 2} if template.kind == 'blank' else {'a':6 if high else 2,'b':1}
    a,b = (6,6) if high else (2,2)
    if f == 'sin_double_expanded': b = -b
    if f == 'cos_double':
        a = -a if high else a
        if template.kind == 'blank' and high: b = -b
    return {'a':a,'b':b}


def profile_boundary(profile, high):
    if profile == 'sin_shift_exchange':
        return {'a':5,'b':4,'h':5,'k':-5} if high else {'a':2,'b':3,'h':-5,'k':1}
    if profile == 'sin_compound_scale_offset':
        return {'a':5,'b':4,'h':5,'k':-4} if high else {'a':2,'b':3,'h':1,'k':-3}
    if profile == 'sin_unit_y_shift':
        return {'a':1,'b':1,'h':0,'k':-5 if high else -1}
    if profile == 'sin_unit_x_shift_identity':
        return {'a':1,'b':1,'h':-5 if high else -2,'k':0}
    if profile == 'cos_identity_scale':
        return {'a':5,'b':4,'h':5,'k':-5} if high else {'a':1,'b':2,'h':0,'k':0}
    if profile == 'cos_unit_shift_identity':
        return {'a':1,'b':1,'h':-5 if high else -1,'k':5 if high else 2}
    spec=g.TEMPLATES[g.BANK_PROFILES[profile].template]
    p=boundary_parameters(spec,high)
    if profile == 'cot_csc_source' and not high:p['a']=3
    if profile == 'cos_double_negative_source':p['a']=-abs(p['a'])
    if profile == 'cos_double_positive_source':p['a']=abs(p['a'])
    return p


def generated_options(record):
    field=record['question'][':question/answer-fields'][0]
    return [{'id':a[':answer/id'],'value':a[':answer/value'],
             'correct':a[':answer/id']==field[':answer-field/correct'][1]}
            for a in field[':answer-field/choices']]


def source_options(question):
    field=question[':question/answer-fields'][0]
    return [{'id':a[':db/id'],'value':a[':answer/value'],
             'correct':a[':db/id']==field[':answer-field/correct'][':db/id']}
            for a in field[':answer-field/choices']]


def main():
    # Rebuild the app's comparator offline, then link the same engine library
    # into a temporary fixture harness. This performs no database operations.
    subprocess.run(['cargo','build','--offline','--bin','compare-question-answers'],cwd=REPO,check=True)
    engine_lib=max((REPO/'target/debug/deps').glob('libcourse_academy_engine-*.rlib'),key=lambda p:p.stat().st_mtime)
    serde_lib=max((REPO/'target/debug/deps').glob('libserde_json-*.rlib'),key=lambda p:p.stat().st_mtime)
    harness_dir=tempfile.TemporaryDirectory(prefix='trig-generator-check-')
    harness=Path(harness_dir.name)/'check-engine'
    subprocess.run(['rustc','--edition=2024',str(ROOT/'check-engine.rs'),'-L','dependency='+str(REPO/'target/debug/deps'),
                    '--extern','course_academy_engine='+str(engine_lib),'--extern','serde_json='+str(serde_lib),'-o',str(harness)],check=True)
    records=[];engine=[];cases=[]
    assert g.polynomial_signature(g.Relation(g.X**2+g.Y**2,g.sp.Integer(1),'','')) == \
           g.polynomial_signature(g.Relation(2*g.X**2+2*g.Y**2,g.sp.Integer(2),'',''))
    assert not g.distinct(g.explicit(g.X+g.X),g.explicit(2*g.X),[{g.X:g.sp.Rational(1,3)}])
    for name,template in g.TEMPLATES.items():
        for seed in range(6):
            record = g.generate(template.level,seed,name,None,None)
            check_record(record)
            assert record == g.generate(template.level,seed,name,None,None)
            if template.level == 'moderate':
                assert all(1 <= value <= 4 for value in record['generation']['parameters'].values())
            label=f"{name}/seed={seed}"
            records.append(record);engine.append(engine_checks(record,label));cases.append(label)
        for high in ((False,True) if template.kind == 'blank' else ()):
            p=boundary_parameters(template,high)
            record=g.generate(template.level,90,name,None,p)
            check_record(record);engine.append(engine_checks(record,f'{name}/boundary={high}'))
            # Changing the seed can reorder choices, not create a new identity.
            replay=g.generate(template.level,91,name,None,p)
            assert record['question'][':question/id'] == replay['question'][':question/id']
            assert record['question'][':question/answer-fields'][0][':answer-field/id'] == replay['question'][':question/answer-fields'][0][':answer-field/id']
            assert sorted(record['question'][':question/answer-fields'][0][':answer-field/choices'],key=lambda a:a[':answer/id']) == \
                   sorted(replay['question'][':question/answer-fields'][0][':answer-field/choices'],key=lambda a:a[':answer/id'])
            cases.append(f'{name}/boundary={high}')
        print('Checked '+name,flush=True)
    for profile,bank in g.BANK_PROFILES.items():
        template=g.TEMPLATES[bank.template]
        for seed in (0,1):
            record=g.generate(template.level,seed,bank.template,None,None,profile=profile)
            check_record(record)
            assert record==g.generate(template.level,seed,bank.template,None,None,profile=profile)
            label=f'{profile}/sample={seed}'
            engine.append(engine_checks(record,label));cases.append(label)
        for high in (False,True):
            p=profile_boundary(profile,high)
            record=g.generate(template.level,90,bank.template,None,p,profile=profile)
            replay=g.generate(template.level,91,bank.template,None,p,profile=profile)
            check_record(record)
            assert record['question'][':question/id']==replay['question'][':question/id']
            assert sorted(generated_options(record),key=lambda a:a['id'])==sorted(generated_options(replay),key=lambda a:a['id'])
            label=f'{profile}/boundary={high}'
            engine.append(engine_checks(record,label));cases.append(label)
        print('Checked profile '+profile,flush=True)
    # Default selection must reach every complete profile, not just the first.
    selection_coverage={}
    for name in ('ellipse_sin_radio','ellipse_cos_radio','cos_double_radio'):
        seen=set()
        for seed in range(20):
            record=g.generate(g.TEMPLATES[name].level,seed,name,None,None)
            check_record(record)
            seen.add(record['generation']['bank_profile'])
        assert seen==set(g.profile_names(g.TEMPLATES[name])),(name,seen)
        selection_coverage[name]=sorted(seen)
    # Identity errors remain present with nonzero offsets and unequal scales.
    identity=g.generate_easy(7,'ellipse_cos_radio',parameters={'a':2,'b':3,'h':1,'k':-2},profile='cos_identity_scale')
    check_record(identity);engine.append(engine_checks(identity,'shifted-unequal-scales-identity-bank'));cases.append('shifted-unequal-scales-identity-bank')
    # Changing banks changes content identity; mere shuffling does not.
    p={'a':5,'b':3,'h':3,'k':-2}
    banks=[g.generate_easy(3,'ellipse_sin_radio',parameters=p,profile=profile)
           for profile in ('sin_shift_exchange','sin_compound_scale_offset')]
    assert len({r['question'][':question/id'] for r in banks})==2
    assert len({r['generation']['parameter_fingerprint'] for r in banks})==1
    source=json.loads((ROOT/'source.json').read_text())
    capture=json.loads((ROOT/'source-capture.json').read_text())
    assert capture['basis'] == g.SOURCE['basis_t'] == 1356
    assert capture['record'] == source
    previous_source=json.loads((ROOT/'source-basis-1308.json').read_text())
    current_by_id={q[':question/math-academy-id']:q for q in source[':knowledge-point/questions']}
    previous_by_id={q[':question/math-academy-id']:q for q in previous_source[':knowledge-point/questions']}
    assert previous_by_id == current_by_id
    assert previous_source[':knowledge-point/canonical-example'] == source[':knowledge-point/canonical-example']
    assert g.generate('easy') == g.generate_easy()
    assert g.generate('moderate') == g.generate_moderate()
    assert g.generate('hard') == g.generate_hard()
    by_id={q[':question/math-academy-id']:q for q in source[':knowledge-point/questions']}
    compare_requests=[]
    source_cases=json.loads((ROOT/'source-cases.json').read_text())
    assert {case['source_id'] for case in source_cases}==set(by_id)
    fidelity=[];ledger=[]
    for case in source_cases:
        name=case['template'];template=g.TEMPLATES[name];p=case['parameters']
        profile=case.get('bank_profile')
        record=g.generate(template.level,400,name,None,p,profile=profile)
        check_record(record);engine.append(engine_checks(record,'source-reproduction/'+case['source_id']))
        built=g.BUILDERS[template.level](template,p)
        canonical=by_id[case['source_id']][':question/answer-fields'][0][':answer-field/correct'][':answer/value'].replace('\\\\','\\')
        if template.kind == 'radio':
            lhs,rhs=canonical.split('=')
            pairs=[(lhs,built.relation.lhs_tex),(rhs,built.relation.rhs_tex)]
        else:
            pairs=[(canonical,built.blank_tex)]
        for a,b in pairs:
            compare_requests.append({'a':a,'b':b,'prompt':record['question'][':question/problem'],'kp_titles':[g.TITLE]})
        cases.append('source-reproduction/'+case['source_id'])
        original=source_options(by_id[case['source_id']]);generated=generated_options(record)
        matched=match_bank(original,generated,template.kind=='radio')
        fidelity.append({'source_id':case['source_id'],'template':name,'bank_profile':profile,
                         'source_options':original,'generated_options':generated,**matched})
        for match in matched['matches']:
            s=original[match['source_index']];a=generated[match['generated_index']]
            recipe_label='correct' if s['correct'] else record['generation']['distractor_recipes'][a['id']]['recipe']
            recipe=next((r for r in g.BANK_PROFILES[profile].recipes if r.label==recipe_label),None) if profile else None
            ledger.append({'source_id':case['source_id'],'source_field_id':by_id[case['source_id']][':question/answer-fields'][0][':db/id'],
                           'source_option_id':s['id'],'source_option_index':match['source_index'],'source_value':s['value'],
                           'correct':s['correct'],'parameters':p,'bank_profile':profile,'recipe':recipe_label,
                           'recipe_formula':{'lhs':str(recipe.lhs),'rhs':str(recipe.rhs)} if recipe else None,
                           'interpretation':'inferred; no learner-facing diagnosis','generated_value':a['value'],'reproduced':True})
    groups={};by_template={};by_profile={}
    for item in fidelity:
        group='ellipses' if item['template'].startswith('ellipse') else 'cosine double-angle' if item['template']=='cos_double_radio' else 'other radios'
        if item['bank_profile']:
            for collection,key in ((groups,group),(by_template,item['template']),(by_profile,item['bank_profile'])):
                counts=collection.setdefault(key,{'matched_distractors':0,'total_distractors':0,'complete_banks':0,'total_banks':0})
                counts['total_banks']+=1;counts['complete_banks']+=int(item['passed'])
                counts['total_distractors']+=sum(not a['correct'] for a in item['source_options'])
                counts['matched_distractors']+=sum(not item['source_options'][m['source_index']]['correct'] for m in item['matches'])
    write('source-bank-fidelity.json',{'database_writes':0,'source_basis':1356,'groups':groups,'by_template':by_template,'by_profile':by_profile,
        'matched_distractors':sum(c['matched_distractors'] for c in groups.values()),
        'total_distractors':sum(c['total_distractors'] for c in groups.values()),
        'complete_radio_banks':sum(c['complete_banks'] for c in groups.values()),
        'total_radio_banks':sum(c['total_banks'] for c in groups.values()),
        'all_fields_matched':all(i['passed'] for i in fidelity),'cases':fidelity})
    write('choice-extraction.json',{'database_writes':0,'source_basis':1356,'options':ledger})
    assert all(item['passed'] for item in fidelity),[item for item in fidelity if not item['passed']]
    # Regression checks for the fidelity comparator itself: scale, order, loss,
    # extra values, and incorrect designation must be handled independently.
    assert equivalent_equations(equation('x^2+y^2=1'),equation('3x^2+3y^2=3'))
    assert not equivalent_equations(equation('x^2+y^2=1'),equation('3x^2+y^2=1'))
    original=fidelity[0]['source_options'];generated=fidelity[0]['generated_options']
    assert match_bank(original,list(reversed(generated)))['passed']
    assert not match_bank(original,generated[:-1])['passed']
    assert not match_bank(original,generated+[generated[0]])['passed']
    incorrect_flag=[{**a,'correct':not a['correct']} for a in generated]
    assert not match_bank(original,incorrect_flag)['passed']
    result=subprocess.run([str(REPO/'target/debug/compare-question-answers')],
        input='\n'.join(map(json.dumps,compare_requests))+'\n',text=True,capture_output=True,check=True)
    outcomes=[json.loads(line) for line in result.stdout.splitlines()]
    assert len(outcomes)==len(compare_requests)
    assert all(outcome['outcome']=='equivalent' for outcome in outcomes),outcomes
    write('source-answer-comparison.json',{'database_writes':0,'requests':compare_requests,'outcomes':outcomes})
    # Independently prove and grade an equivalent form with the scale inside the root.
    limitation=g.generate_easy(0,'cot_csc_blank',parameters={'a':3,'b':2})
    item=engine_checks(limitation,'equivalent-radical-normalization')
    equivalent=g.sp.sqrt(4+g.sp.Rational(4,9)*g.X**2)
    assert g.sp.simplify(2*g.sp.sqrt(1+g.X**2/9)-equivalent)==0
    item['checks'].append({'submitted':r'\sqrt{4+\frac{4x^2}{9}}','expected':'accepted',
                           'purpose':'equivalent radical with scale moved inside the root'})
    engine.append(item)
    for level,name,kind in [('moderate','cos_tan_radio','blank'),('hard','sin_double_factored_radio','blank')]:
        try:g.generate(level,0,name,kind,None)
        except ValueError:pass
        else:raise AssertionError('unsupported field variant accepted')
    for parameters in [{'a':0,'b':2},{'a':2,'b':0},{'a':-2,'b':2}]:
        try:g.generate_easy(0,'cot_csc_blank',parameters=parameters)
        except ValueError:pass
        else:raise AssertionError('invalid scale accepted')
    moderate=g.generate_moderate(0,'cos_tan_radio',parameters={'a':2,'b':3})
    check_record(moderate)
    corrupted=json.loads(json.dumps(moderate))
    corrupted['question'][':question/worked-solution']=corrupted['question'][':question/worked-solution'].replace(r'\frac{y}{3}',r'\frac{y}{4}')
    try:check_solution(corrupted)
    except AssertionError:pass
    else:raise AssertionError('Rendered intermediate scale error escaped independent checking')
    assert moderate['generation']['parameters']=={'a':2,'b':3,'quadrant':1}
    assert moderate['question'][':question/id']==g.generate_moderate(99,'cos_tan_radio',
        parameters={'a':2,'b':3,'quadrant':1})['question'][':question/id']
    for name in ('cos_tan_radio','sin_tan_radio'):
        sampled={tuple(g.generate_moderate(seed,name)['generation']['parameters'][key] for key in ('a','b')) for seed in range(6)}
        assert len(sampled)>1 and sampled!={(1,1)},'Moderate default did not vary positive scales'
    # Independent exact coordinates check every family/quadrant and both edges
    # of each coefficient range, including the conditional unit-scale error.
    moderate_variations=[]
    signs={1:(1,1),2:(1,-1),3:(-1,-1),4:(-1,1)}
    intervals={1:'0 < t < pi/2',2:'pi/2 < t < pi',3:'pi < t < 3*pi/2',4:'3*pi/2 < t < 2*pi'}
    for family in ('sin_tan','cos_tan','sin_cot','cos_cot'):
        name=family+'_radio'
        for quadrant,(sine_sign,cosine_sign) in signs.items():
            for a,b in ((1,1),(1,4),(4,1),(4,4)):
                p={'a':a,'b':b,'quadrant':quadrant}
                record=g.generate_moderate(11,name,parameters=p)
                replay=g.generate_moderate(12,name,parameters=p)
                check_record(record)
                assert record['generation']['bank_profile']==family+'_variation'
                assert record['question'][':question/id']==replay['question'][':question/id']
                assert sorted(generated_options(record),key=lambda o:o['id'])==sorted(generated_options(replay),key=lambda o:o['id'])
                assert record['generation']['parameter_interval']==intervals[quadrant]
                fx,fy=family.split('_')
                x_sign=sine_sign if fx=='sin' else cosine_sign
                expected_domain=(f'0<x<{a}' if x_sign==1 else f'-{a}<x<0')+r'\quad '+('y>0' if sine_sign*cosine_sign==1 else 'y<0')
                assert record['generation']['curve_restrictions_latex']==expected_domain
                missing_sign=cosine_sign if fx=='sin' else sine_sign
                missing='cos' if fx=='sin' else 'sin'
                assert '$\\'+missing+' t'+('>' if missing_sign==1 else '<')+'0$' in record['question'][':question/worked-solution']
                for s,c in ((g.sp.Rational(3,5),g.sp.Rational(4,5)),(g.sp.Rational(5,13),g.sp.Rational(12,13))):
                    s,c=sine_sign*s,cosine_sign*c
                    xx=a*(s if fx=='sin' else c)
                    yy=b*(s/c if fy=='tan' else c/s)
                    options=generated_options(record)
                    for option in options:
                        lhs,rhs=equation(option['value'])
                        error=g.sp.simplify((lhs-rhs).subs({g.X:xx,g.Y:yy},simultaneous=True))
                        assert error.is_real is True,(family,quadrant,p,option)
                        assert (error==0)==option['correct'],(family,quadrant,p,option)
                label=f'moderate-variation/{family}/quadrant={quadrant}/a={a}/b={b}'
                moderate_variations.append({'template':name,'parameters':p,'bank_profile':family+'_variation'})
                engine.append(engine_checks(record,label));cases.append(label)
    for p in ({'a':1,'b':1,'quadrant':0},{'a':1,'b':1,'quadrant':5},{'a':5,'b':1},
              {'a':1,'b':1,'quadrant':True},{'a':1,'b':1,'interval':'0<t<pi'}):
        try:g.generate_moderate(parameters=p)
        except ValueError:pass
        else:raise AssertionError('invalid moderate domain or complexity accepted')
    try:g.generate_moderate(parameters={'a':2,'b':3,'quadrant':2},profile='sin_tan_source')
    except ValueError:pass
    else:raise AssertionError('observed first-quadrant bank used outside its domain')
    # Uniform family selection has no stage/curriculum state, and seeded defaults
    # reach every quadrant within each family rather than enforcing an order.
    for name in ('sin_tan_radio','cos_tan_radio','sin_cot_radio','cos_cot_radio'):
        quadrants={g.generate_moderate(seed,name)['generation']['parameters']['quadrant'] for seed in range(20)}
        assert quadrants=={1,2,3,4},(name,quadrants)
    write('moderate-variation-validation.json',{'database_writes':0,'cases':moderate_variations,
          'independent_curve_coordinates':'passed','real_distinct_incorrect_choices':'passed',
          'domain_and_branch_signs':'passed','seed_independent_identity':'passed',
          'all_default_quadrants_reachable':'passed','instructional_order':None})
    # An underdetermined distractor bank is rejected; fixed parameters never silently change.
    try:g.generate_easy(0,'ellipse_sin_radio',parameters={'a':1,'b':1,'h':0,'k':0})
    except g.SampleRejected:pass
    else:raise AssertionError('ambiguous/insufficient choice bank accepted')
    write('engine-input.json',engine)
    subprocess.run([str(harness),str(ROOT/'engine-input.json'),str(ROOT/'engine-validation.json')],check=True)
    write('validation.json',{'database_writes':0,'source_basis':1356,'templates':len(g.TEMPLATES),'observed_templates':13,'authored_templates':2,'moderate_variation_report':'moderate-variation-validation.json',
        'validation_scope':{'mathematical_correctness':'passed','displayed_solution_intermediates':'passed','actual_grading':'passed',
                            'source_correct_answers':'passed','source_distractor_banks':'passed'},
        'displayed_solution_checks':{'unique_questions':len(SOLUTION_AUDIT),'equalities':sum(SOLUTION_AUDIT.values()),
                                    'method':'independent parsing and exact rational unit-circle coordinates; final relation proved over full interval'},
        'current_snapshot':{'database':capture['database'],'basis':capture['basis'],'lineage':capture['lineage'],
                            'practice_questions_unchanged_from_basis':1308,'canonical_unchanged':True,
                            'new_metadata':'explicit knowledge-point/key-prerequisites'},
        'fidelity_status':'all 56 source distractors and all 14 complete radio banks reproduced',
        'source_bank_report':'source-bank-fidelity.json','bank_profiles':len(g.BANK_PROFILES),'default_profile_selection':selection_coverage,
        'checked_cases':len(cases),'cases':cases,'replay':True,'identity_independent_of_seed_and_order':True,
        'all_source_correct_answer_sides_verified':len(compare_requests),
        'real_grader_report':'engine-validation.json','plot_extraction_and_generation':'not required',
        'dependency_versions':{'sympy':g.sp.__version__,'engine_source_sha256':{
            name:hashlib.sha256((REPO/'engine/rust'/name).read_bytes()).hexdigest() for name in ('learning.rs','symbolic.rs')}},
        'version_status':'draft; side-by-side author review produced, not frozen'})
    # One source plus two generated instances for every extracted template.
    preview=['# Cartesian-equation rebuild review','',f"KP `{g.KP_ID}`; source basis `1356`; draft version `{g.VERSION}`.",'',
             'All 20 source questions are shown, each with two generated variants using the same complete bank profile or blank template. All 14 observed radio bank profiles are represented. Moderate source replay retains their banks; normal moderate generation uses four authored variation banks, positive coefficients, and single-quadrant intervals. These are variations at one difficulty with no instructional sequence. Domain restrictions are author metadata. Source mathematical content is retained; choice escaping is normalized for display.','']
    preview_records=[]
    used_by_template={name:{json.dumps(case['parameters'],sort_keys=True) for case in source_cases if case['template']==name} for name in g.TEMPLATES}
    for case in source_cases:
        name=case['template'];template=g.TEMPLATES[name];profile=case.get('bank_profile')
        q=by_id[case['source_id']];field=q[':question/answer-fields'][0]
        preview += ['# '+name+(' / '+profile if profile else ''),'','## Original source — '+template.level.title()+' — '+q[':question/math-academy-id'],'',q[':question/problem'],'']
        if template.kind == 'radio':
            for letter,answer in zip('ABCDE',field[':answer-field/choices'],strict=True):
                value=answer[':answer/value'].replace('\\\\','\\')
                preview.append(f'- **{letter}.** ${value}$')
            correct=next(letter for letter,answer in zip('ABCDE',field[':answer-field/choices'],strict=True) if answer[':db/id']==field[':answer-field/correct'][':db/id'])
            preview += ['',f'**Correct: {correct}**']
        else:
            value=field[':answer-field/correct'][':answer/value'].replace('\\\\','\\')
            preview += ['**Correct blank entry:** $'+value+'$']
        preview += ['','**Worked solution**','',q[':question/worked-solution'],'']
        used = used_by_template[name]
        for initial_seed in (17,29):
            seed = initial_seed
            while True:
                generated=g.generate(template.level,seed,name,None,None,profile)
                parameter_key=json.dumps(generated['generation']['parameters'],sort_keys=True)
                if parameter_key not in used:
                    used.add(parameter_key)
                    break
                seed += 1
                assert seed < initial_seed+100, 'No distinct review variant found'
            check_record(generated)
            preview_records.append(generated);preview += [g.markdown(generated),'']
        preview += ['---','']
    variations=['# Moderate variations — author review','',
        'All examples below are moderate multiple-choice questions with the same solution process; their display order is not an instructional sequence. The banks, cotangent counterparts, and quadrant variations are authored extensions. The two captured moderate originals and their faithful bank variants remain in [review.md](review.md).','']
    variation_records=[]
    for family in ('sin_tan','cos_tan','sin_cot','cos_cot'):
        for quadrant in (1,2,3,4):
            record=g.generate_moderate(70+quadrant,family+'_radio',parameters={'a':2,'b':3,'quadrant':quadrant})
            check_record(record);variation_records.append(record)
            variations += [g.markdown(record),'','---','']
    (ROOT/'moderate-review.md').write_text('\n'.join(variations)+'\n')
    write('moderate-review.json',variation_records)
    preview += ['# Authored moderate variations','',*variations[2:]]
    (ROOT/'review.md').write_text('\n'.join(preview)+'\n')
    write('review.json',preview_records+variation_records)
    print(f"Passed {len(cases)} cases, {len(compare_requests)} source answer-side comparisons, 56/56 distractors and 14/14 complete banks; review includes 20 originals and 40 generated variants.")
    harness_dir.cleanup()


if __name__=='__main__':main()
