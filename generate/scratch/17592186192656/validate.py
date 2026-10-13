#!/usr/bin/env python3
"""Read displayed systems, full tuple choices, every calculation/prose conclusion.
Mathematical checks are independent of generation answers and native radio IDs.
"""
import copy, hashlib, importlib.util, itertools, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[2]
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def algebra(text):
    text=text.replace('&','').strip()
    text=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',text)
    assert '\\' not in text,text
    return sp.expand(parse_expr(text,transformations=standard_transformations+(implicit_multiplication_application,)))
def equation(text):
    left,right=text.split('=');return algebra(left),algebra(right)
def pair(text):
    parts=text.strip().removeprefix('(').removesuffix(')').split(',');assert len(parts)==2
    return tuple(algebra(s) for s in parts)
def formatting(text):
    errors=[]
    if text.count('$')%2:errors.append('odd dollar count')
    if text.count('$$')%2:errors.append('unpaired display delimiter')
    # Placeholder braces and literal system glyph do not count as TeX groups.
    text=re.sub(r'\{\{[\w-]+\}\}','',text).replace('\\{','')
    balance=0
    for c in text:
        if c=='{':balance+=1
        if c=='}':balance-=1
        if balance<0:errors.append('closing group without opener')
    if balance:errors.append('unbalanced group')
    if re.search(r'--|\+-',text):errors.append('ungrouped adjacent signs')
    return errors

def printed_system(r):
    q=r['question'];match=re.search(r'\n\$(?:\\)?\{(.*?)\$',q[':question/problem']);assert match
    return [equation(s) for s in match[1].split('; ')],match[1].split('; ')
def correct_value(field):return next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1])
def validate_record(r):
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    q=r['question'];assert q[':question/difficulty'] in {':question.difficulty/'+l for l in ('easy','moderate','hard')}
    prompt=q[':question/problem'];opening=re.search(r'solution \$\((\w), ?(\w)\)\$',prompt);assert opening
    x,y=map(sp.Symbol,opening.groups());rows,strings=printed_system(r)
    solved=sp.solve([l-rr for l,rr in rows],(x,y));assert set(solved)=={x,y}
    X,Y=solved[x],solved[y]
    # Scope is enforced on the actual printed equations, independently of sampler.
    level=q[':question/difficulty'].split('/')[-1]
    coefficients=[(l.coeff(x),l.coeff(y),rr) for l,rr in rows]
    small=min(abs(z[0]) for z in coefficients);big=max(abs(z[0]) for z in coefficients)
    lo,hi=(2,7) if level=='easy' else ((2,4) if level=='moderate' else (5,7))
    assert (small==1 if level=='easy' else 2<=small<=3) and lo<=big/small<=hi and (big/small).q==1
    reduced=[]
    for z in coefficients:
        factor=sp.igcd(*z)
        reduced.append(tuple(v/factor for v in z))
    primitive_small=min(abs(z[0]) for z in reduced);primitive_big=max(abs(z[0]) for z in reduced)
    assert (primitive_small==1 if level=='easy' else 2<=primitive_small<=3)
    assert (primitive_big/primitive_small).q==1 and lo<=primitive_big/primitive_small<=hi
    assert all(1<=abs(z[1])<=7 and abs(z[2])<={'easy':25,'moderate':35,'hard':40}[level] for z in coefficients)
    assert all(v.q==1 and 1<=abs(v)<=5 for v in (X,Y))
    fields=q[':question/answer-fields'];kind=r['generation']['template']
    assert len(fields)==(1 if kind=='radio_solution' else 2)
    if kind=='radio_solution':
        field=fields[0];assert field[':answer-field/type']==':answer-field.type/radio';assert field[':answer-field/key']=='selection'
        choices=[pair(a[':answer/value']) for a in field[':answer-field/choices']];assert len(choices)==len(set(choices))==5
        good=[v for v in choices if all(sp.expand(l-rr).subs({x:v[0],y:v[1]})==0 for l,rr in rows)]
        assert good==[(X,Y)] and pair(correct_value(field))==(X,Y)
        if r['generation']['eligible_for_learning']:
            assert sum(all(v.q==1 for v in z) for z in choices)>=2,'correct tuple is the only integer pair'

    else:
        assert [f[':answer-field/key'] for f in fields]==['field-1','field-2']
        for field,v in zip(fields,(X,Y)):
            assert field[':answer-field/type']==':answer-field.type/blank'
            assert '{{'+field[':answer-field/key']+'}}' in prompt
            assert len(field[':answer-field/choices'])==1 and algebra(correct_value(field))==v
    all_ids=[]
    for field in fields:
        assert set(field)=={':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct'}
        assert field[':answer-field/correct'][0]==':answer/id'
        for a in field[':answer-field/choices']:
            assert set(a)=={':answer/id',':answer/type',':answer/value'} and a[':answer/type']==':answer.type/math'
            assert not '$' in a[':answer/value'];all_ids.append(a[':answer/id']);g.uuid.UUID(a[':answer/id'])
    assert len(set(all_ids))==len(all_ids)
    assert not formatting(prompt),formatting(prompt)
    solution=q[':question/worked-solution'];assert not formatting(solution),formatting(solution)
    blocks=re.findall(r'\$\$\n(.*?)\n\$\$',solution,re.S);assert len(blocks)==3
    operation=blocks[0].replace('\\{','').split('; ');assert sum('\\cdot' in s for s in operation)==1
    row=next(i for i,s in enumerate(operation) if '\\cdot' in s)
    match=re.fullmatch(r'\((.*?)\) \\cdot \((-?\d+)\)',operation[row]);assert match
    m=sp.Rational(match[2]);assert 2<=abs(m)<=7
    assert equation(match[1])==rows[row] and equation(operation[1-row])==rows[1-row]
    transformed=[(sp.expand(m*l),m*rr) if i==row else (l,rr) for i,(l,rr) in enumerate(rows)]
    def stage(block):return block.replace('\\begin{aligned}\n','').replace('\n\\end{aligned}','').split(' \\\\\n')
    elimination=stage(blocks[1]);assert len(elimination)==5
    derived=[equation(s) for s in elimination]
    assert derived[:2]==transformed
    assert all('(' not in st and ')' not in st for st in elimination[:2])
    assert transformed[0][0].coeff(x)+transformed[1][0].coeff(x)==0
    total=(sp.expand(transformed[0][0]+transformed[1][0]),transformed[0][1]+transformed[1][1])
    assert derived[2]==derived[3]==total
    assert '(' in elimination[2] and ')' in elimination[2] and '(' not in elimination[3]
    assert str(x) not in elimination[2] and str(x) not in elimination[3]
    assert derived[4]==(y,Y)
    # Reconstruct grouped operands in order from the individually displayed rows.
    left,right=elimination[2].replace('&','').split('=');parts=re.fullmatch(r'\((.*?)\)',left.strip());assert parts
    # Exactly two y operands, even if their sum happens to simplify substantially.
    assert len(re.findall(str(y),parts[1]))==2
    def printed_term(n,var):return ('-' if n<0 else '')+('' if abs(n)==1 else str(abs(n)))+str(var)
    b0,b1=[z[0].coeff(y) for z in transformed];c0,c1=[z[1] for z in transformed]
    expected_left='('+printed_term(b0,y)+(' + ' if b1>0 else ' - ')+printed_term(abs(b1),y)+')'
    expected_right='('+str(c0)+(' + ' if c1>=0 else ' - ')+str(abs(c1))+')'
    assert left.strip()==expected_left and right.strip()==expected_right
    aa=rows[row][0].coeff(x);bb=rows[row][0].coeff(y);cc=rows[row][1]
    back=stage(blocks[2]);assert len(back)==(4 if abs(aa)==1 else 5)
    bd=[equation(s) for s in back]
    assert bd[0]==rows[row]
    assert bd[1]==bd[2]==(sp.expand(aa*x+bb*Y),cc)
    # Printed substitution needs the actual solved y as a grouped arithmetic input.
    substituted=back[1].split('&=')[0];assert str(y) not in substituted
    assert '('+g.tex(Y)+')' in substituted
    expected_substitution=printed_term(aa,x)+(' + ' if bb>0 else ' - ')+('' if abs(bb)==1 else str(abs(bb)))+'('+str(Y)+')'
    expected_evaluated=printed_term(aa,x)+(' + ' if bb*Y>=0 else ' - ')+str(abs(bb*Y))
    assert substituted.strip()==expected_substitution
    assert back[2].split('&=')[0].strip()==expected_evaluated
    assert '(' not in back[2] and str(y) not in back[2]
    if abs(aa)!=1:assert bd[3]==(aa*x,cc-bb*Y)
    assert bd[-1]==(x,X)
    # Every displayed row must hold for the actual system's independent solution.
    for l,rr in derived+bd:assert sp.expand(l-rr).subs(solved)==0
    assert f'first equation is ${rows[0][0].coeff(x)}$' in solution
    assert f'second equation it is ${rows[1][0].coeff(x)}$' in solution
    assert f'multiply the {["first","second"][row]} equation by ${m}$' in solution
    assert f'will become ${m*aa}$' in solution
    assert f'choose the {["first","second"][row]} equation' in solution
    assert f'${y} = {Y}$' in solution
    conclusion=re.search(r'Therefore,.*?\$'+str(x)+r'=(.*?), \\,'+str(y)+r'=(.*?)\$, which can be expressed as \$(.*?)\$\.',solution)
    assert conclusion and algebra(conclusion[1])==X and algebra(conclusion[2])==Y and pair(conclusion[3])==(X,Y)
    # Native blank/radio shapes do not permit extra assessment stages or fields.
    return row,int(sp.sign(m)),(X,Y)

def source_enum_projection(question):
    # Independently project exactly the two schema enum-ref attributes only.
    q=copy.deepcopy(question)
    for field in q.get(':question/answer-fields',[]):
        if isinstance(field[':answer-field/type'],dict):field[':answer-field/type']=field[':answer-field/type'][':db/ident']
        for answer in field.get(':answer-field/choices',[]):
            if isinstance(answer[':answer/type'],dict):answer[':answer/type']=answer[':answer/type'][':db/ident']
    return q

def main():
    cases=json.loads((HERE/'source-cases.json').read_text());fidelity=[];native_records=[];reviews=[]
    for c in cases:
        raw=g.generate(c['authored_level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])
        assert raw['question']==source_enum_projection(g.ORIGINALS[c['source_id']])
        assert all(isinstance(f[':answer-field/type'],str) and all(isinstance(a[':answer/type'],str) for a in f.get(':answer-field/choices',[])) for f in raw['question'][':question/answer-fields'])
        assert raw['generation']['evidence_only'] and not raw['generation']['eligible_for_learning']
        assert ':question/difficulty' not in raw['question'] and ':question/worked-solution' not in raw['question']
        assert all(':answer-field/correct' not in f for f in raw['question'][':question/answer-fields'])
        assert formatting(raw['question'][':question/problem'])==c['raw_format_findings']
        if c['source_id']=='q-208816':assert all(':answer-field/choices' not in f for f in raw['question'][':question/answer-fields'])
        else:
            rows,_=printed_system(raw);x,y=map(sp.Symbol,'xy');solutions=[pair(a[':answer/value']) for a in raw['question'][':question/answer-fields'][0][':answer-field/choices']]
            assert sum(all((l-rr).subs({x:v[0],y:v[1]})==0 for l,rr in rows) for v in solutions)==1
        changed=copy.deepcopy(c['parameters']);changed['c1']+=1
        altered=g.generate(c['authored_level'],template=c['template'],parameters=changed,profile=c['bank_profile'])
        assert altered['question'][':question/problem']!=raw['question'][':question/problem']
        assert set(altered['question'])==set(raw['question'])
        for f1,f2 in zip(altered['question'][':question/answer-fields'],raw['question'][':question/answer-fields']):assert set(f1)==set(f2)
        complete=g.generate(c['authored_level'],template=c['template'],parameters=c['parameters']);validate_record(complete);native_records.append(complete)
        reviews += [dict(label='RAW ORIGINAL '+c['source_id'],record=raw),dict(label='AUTHORED supported completion '+c['source_id'],record=complete),dict(label='RAW PARAMETERIZED EVIDENCE VARIANT '+c['source_id'],record=altered)]
        fidelity.append(dict(source_id=c['source_id'],all_raw_attributes_exact_after_enum_projection=True,enum_projection_only=True,prompt_exact=True,observed_bank_options_matched=5 if c['source_id']=='q-18787' else 0,correct_designations_observed=0,solution_presence_exact=True))
    opaque=g.generate('moderate',parameters=g.ANCHORS['q-18787'],profile='completed-opaque-q-18787');validate_record(opaque);native_records.append(opaque)
    assert opaque['generation']['evidence_only'] and not opaque['generation']['eligible_for_learning']
    reviews.append(dict(label='AUTHORED grading/format completion of OPAQUE original bank; evidence only',record=opaque))
    variety={};layouts={};orientations={};signs={};first_positions=set();integer_pair_counts={}
    for level in ('easy','moderate','hard'):
        seen=set();families=set();rr=set();ss=set();integer_forms={}
        for seed in range(500):
            record=g.generate(level,seed);row,sign,answer=validate_record(record)
            assert record['question'][':question/difficulty']==':question.difficulty/'+level
            seen.add(record['generation']['mathematical_fingerprint']);families.add(record['generation']['template']);rr.add(row);ss.add(sign)
            if seed<16:native_records.append(record)
            fixed=g.generate(level,seed+10000,template=record['generation']['template'],parameters=record['generation']['parameters'],profile=record['generation']['profile'])
            assert fixed['question'][':question/id']==record['question'][':question/id']
            assert fixed['generation']['mathematical_fingerprint']==record['generation']['mathematical_fingerprint']
            if record['generation']['template']=='radio_solution':
                n=sum(all(v.q==1 for v in pair(a[':answer/value'])) for a in record['question'][':question/answer-fields'][0][':answer-field/choices'])
                integer_forms[n]=integer_forms.get(n,0)+1
                first_positions.add(next(i for i,a in enumerate(record['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==record['question'][':question/answer-fields'][0][':answer-field/correct'][1]))
        assert len(seen)>450 and families==set(g.TEMPLATES) and rr=={0,1} and ss=={-1,1}
        integer_pair_counts[level]=integer_forms
        variety[level]=len(seen);layouts[level]=sorted(families);orientations[level]=sorted(rr);signs[level]=sorted(ss)
        for template in g.TEMPLATES:
            for seed in (2,11):reviews.append(dict(label=f'AUTHORED {level} {template} variant seed {seed}',record=g.generate(level,seed,template=template)))
    assert first_positions==set(range(5))
    domain=json.loads((HERE/'variety-domain.json').read_text());enumerated={}
    for level in ('easy','moderate','hard'):
        seen=set();smallrange=(1,) if level=='easy' else (2,3)
        ratios=range(2,8) if level=='easy' else (range(2,5) if level=='moderate' else range(5,8))
        for small,ratio,b1,b2,x,y in itertools.product(smallrange,ratios,domain['subset']['b1_b2'],domain['subset']['b1_b2'],(-2,-1,1,2),(-2,-1,1,2)):
            params=dict(a1=small*ratio,b1=b1,c1=small*ratio*x+b1*y,a2=small,b2=b2,c2=small*x+b2*y,variables='xy')
            try:record=g.generate(level,parameters=params,profile='authored-method-errors')
            except ValueError:continue
            seen.add(record['generation']['mathematical_fingerprint'])
        enumerated[level]=len(seen)
    assert enumerated==domain['eligible_canonical_mathematical_tasks'] and min(enumerated.values())>1000
    # Explicit authored profile must choose its own layout at every seed.
    for seed in range(10):
        assert g.generate('easy',seed,profile='authored-blanks')['generation']['template']=='blank_solution'
        assert g.generate('easy',seed,profile='authored-method-errors')['generation']['template']=='radio_solution'
    # Full identity is bank/layout dependent; task identity excludes either layout.
    p=g.ANCHORS['q-208816'];b=g.generate('easy',parameters=p,template='blank_solution');r=g.generate('easy',parameters=p,template='radio_solution')
    assert b['question'][':question/id']!=r['question'][':question/id'] and b['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
    # Permitted negative values and both orientations exercised; strict explicit bounds.
    bad=[('easy',g.ANCHORS['q-18787']),('moderate',g.ANCHORS['q-208816']),('hard',g.ANCHORS['q-18787']),('moderate',dict(g.ANCHORS['q-18787'],a1=-30)),('hard',dict(g.ANCHORS['q-18787'],a1=8)),('easy',dict(p,b1=0)),('easy',dict(p,c1=100))]
    for level,params in bad:
        try:g.generate(level,parameters=params)
        except ValueError:pass
        else:raise AssertionError(('invalid scope accepted',level,params))
    # Parent stored parameters, independent of changed sampler seed sequences:
    # mathematically valid complete banks whose correct tuple alone is integer.
    shortcuts=[
        ('moderate',dict(a1=3,b1=5,c1=-13,a2=-6,b2=1,c2=4,variables='xy')),
        ('hard',dict(a1=3,b1=5,c1=-13,a2=-15,b2=1,c2=13,variables='xy')),
        ('hard',dict(a1=21,b1=1,c1=22,a2=-3,b2=-5,c2=-8,variables='xy')),
        ('hard',dict(a1=3,b1=-4,c1=2,a2=21,b2=-2,c2=-38,variables='st'))]
    shortcut_evidence=[]
    for index,(level,shortcut) in enumerate(shortcuts):
        try:g.generate(level,parameters=shortcut,template='radio_solution')
        except ValueError as exc:assert 'integer wrong pair' in str(exc)
        else:raise AssertionError('Explicit correct-only integer bank accepted')
        # The two scalar blank family remains eligible at identical parameters.
        blank=g.generate(level,parameters=shortcut,template='blank_solution');validate_record(blank)
        mutation=copy.deepcopy(blank);mutation['question'][':question/problem']=g.prompt(shortcut,'radio_solution')
        mutation['generation']['template']='radio_solution';mutation['generation']['profile']='authored-method-errors'
        pairs=g.bank(shortcut,'authored-method-errors');g.check_bank(shortcut,pairs)
        correct=g.values(shortcut);answers=[{':answer/id':g.uid('shortcut-regression'+g.tuple_string(z)),':answer/type':':answer.type/math',':answer/value':g.tuple_string(z)} for z in pairs]
        mutation['question'][':question/answer-fields']=[{':answer-field/id':g.uid('shortcut-regression-field'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[pairs.index(correct)][':answer/id']]}]
        try:validate_record(mutation)
        except AssertionError as exc:assert 'only integer pair' in str(exc)
        else:raise AssertionError('Actual displayed integer shortcut not caught')
        shortcut_evidence.append(dict(label=f'Rejected parent shortcut parameters {index}; mathematically valid whole bank',record=mutation,evidence_only=True,eligible_for_learning=False,expected_failure='correct tuple is the only integer pair',normal_radio_explicit_rejected=True,normal_blank_same_parameters_accepted=True))
        native_records.append(blank)
    (HERE/'integer-shortcut-regression.json').write_text(json.dumps(shortcut_evidence,indent=2)+'\n')
    # Actual global-factor regression: twice an eligible easy displayed system
    # meets the old raw moderate bounds but must fail its primitive-row demand.
    easy_params=dict(a1=3,b1=1,c1=4,a2=1,b2=-2,c2=-1,variables='xy')
    doubled={k:(v if k=='variables' else 2*v) for k,v in easy_params.items()}
    try:g.generate('moderate',parameters=doubled,template='blank_solution')
    except ValueError as exc:assert 'Primitive-row' in str(exc)
    else:raise AssertionError('Global2x easy accepted as moderate')
    easy=g.generate('easy',parameters=easy_params,template='blank_solution')
    mutation=copy.deepcopy(easy);mutation['question'][':question/difficulty']=':question.difficulty/moderate'
    mutation['question'][':question/problem']=g.prompt(doubled,'blank_solution')
    mutation['question'][':question/worked-solution']=g.worked_solution(doubled)
    try:validate_record(mutation)
    except AssertionError:pass
    else:raise AssertionError('Actual displayed global2x easy not caught')
    # Individual row factors can also lower either the back-sub coefficient or
    # the multiplier; guards do not restrict themselves to the global GCF.
    row_easy=dict(a1=4,b1=3,c1=7,a2=1,b2=-1,c2=0,variables='xy')
    row_scaled=dict(row_easy,a2=2,b2=-2,c2=0)
    try:g.generate('moderate',parameters=row_scaled,template='blank_solution')
    except ValueError as exc:assert 'Primitive-row' in str(exc)
    else:raise AssertionError('Individual-row unit collapse accepted')
    # Same-level individual row scaling is permitted and must deduplicate.
    primitive=dict(a1=4,b1=1,c1=5,a2=2,b2=-3,c2=-1,variables='xy')
    scaled=dict(primitive,a1=8,b1=2,c1=10)
    left=g.generate('moderate',parameters=primitive,template='blank_solution')
    right=g.generate('moderate',parameters=scaled,template='blank_solution')
    validate_record(left);validate_record(right)
    assert left['generation']['mathematical_fingerprint']==right['generation']['mathematical_fingerprint']
    assert left['question'][':question/id']!=right['question'][':question/id']
    native_records.extend((left,right))
    reviews.extend((dict(label='AUTHORED same-level primitive-row instance',record=left),dict(label='AUTHORED same-level individually scaled-row instance; same mathematical task',record=right)))
    # Ordered-stage regression: preserve equality/row count while erasing grouping.
    original=copy.deepcopy(native_records[0]);solution=original['question'][':question/worked-solution'];blocks=re.findall(r'\$\$\n(.*?)\n\$\$',solution,re.S);rows=blocks[1].split(' \\\\\n');rows[2]=rows[3]
    original['question'][':question/worked-solution']=solution.replace(blocks[1],' \\\\\n'.join(rows))
    try:validate_record(original)
    except AssertionError:pass
    else:raise AssertionError('Collapsed addition stage not caught')
    # Wrong concluding coordinate must fail even if every displayed row is intact.
    original=copy.deepcopy(native_records[0]);original['question'][':question/worked-solution']=re.sub(r'which can be expressed as \$.*?\$','which can be expressed as $(999,999)$',original['question'][':question/worked-solution'])
    try:validate_record(original)
    except AssertionError:pass
    else:raise AssertionError('Stale concluding tuple not caught')
    native=[]
    for index,record in enumerate(native_records):
        checks=[]
        for fi,field in enumerate(record['question'][':question/answer-fields']):
            if field[':answer-field/type']==':answer-field.type/radio':
                for a in field[':answer-field/choices']:checks.append(dict(field_index=fi,submitted_answer_id=a[':answer/id'],expected='accepted' if a[':answer/id']==field[':answer-field/correct'][1] else 'rejected',purpose='Complete tuple independently reinserted in both printed equations'))
            else:
                v=correct_value(field)
                checks += [dict(field_index=fi,submitted=v,expected='accepted',purpose='Exact scalar fragment'),dict(field_index=fi,submitted=f'({v}*3)/3',expected='accepted',purpose='Unreduced arithmetic equivalent'),dict(field_index=fi,submitted=str(algebra(v)+1),expected='rejected',purpose='Wrong scalar fragment')]
        native.append(dict(label=f'completed-{index}',record=record,checks=checks))
    (HERE/'engine-input.json').write_text(json.dumps(native,indent=2)+'\n')
    subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    report=json.loads((HERE/'engine-report.json').read_text())
    result=dict(status='passed',source_provenance={k:v for k,v in g.SOURCE.items() if k!='record'},source_questions=2,raw_exact_questions_after_enum_projection=2,raw_enum_shape='local ident strings',source_literal_values_and_attribute_presence_preserved=True,primitive_workload_regressions='global2x easy, individual-row easy collapse rejected; same-level rescaling deduplicates',observed_complete_radio_banks_matched=1,observed_radio_options_matched=5,observed_blank_field_shapes_matched=2,source_correct_designations_present=0,source_correct_designation_fidelity='unobservable; source references omitted',source_practice_worked_solutions_present=0,raw_format_findings=[dict(source_id=c['source_id'],findings=c['raw_format_findings']) for c in cases],normal_format_repairs=2,authored_levels=['easy','moderate','hard'],authored_supported_completions=2,opaque_completed_bank_eligible_for_learning=False,samples_per_level=500,meaningful_sampled_tasks=variety,enumerated_meaningful_domain_lower_bound=enumerated,radio_integer_pair_count_distribution=integer_pair_counts,radio_number_form_regression='four parent parameter sets rejected from actual display and explicit radio API; all four identical blank parameter sets remain eligible',default_layout_coverage=layouts,row_scaling_coverage=orientations,multiplier_sign_coverage=signs,correct_option_positions=sorted(first_positions),independent_displayed_system_every_tuple_every_stage_prose_checks='passed',ordered_stage_and_stale_conclusion_mutation_regressions='passed',native={k:v for k,v in report.items() if k!='records'},native_binary_sha256=hashlib.sha256((REPO/'generate/runs/current/check-engine').read_bytes()).hexdigest(),runtime=dict(python=sys.version.split()[0],sympy=sp.__version__),unresolved_findings=['All difficulty labels and practice worked solutions are authored; neither source has rating, correct references or worked solution.','Four historical wrong tuples have no defensible inferred operation. Their explicit parameterized profiles remain evidence only.','Raw source TeX is malformed and intentionally retained only in evidence replay; authored completion repairs literal system brace and blank punctuation.'])
    (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    (HERE/'source-fidelity.json').write_text(json.dumps(fidelity,indent=2)+'\n')
    (HERE/'review.json').write_text(json.dumps(reviews,indent=2)+'\n')
    (HERE/'review.md').write_text('# First-variable full-system solution review\n\nRaw originals preserve omissions. Completed records and all level labels are authored; opaque profiles remain evidence only.\n\n'+'\n\n---\n\n'.join('## '+r['label']+'\n\n'+g.markdown(r['record']) for r in reviews)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
