#!/usr/bin/env python3
"""Fail-closed source fidelity, independent displayed math and native grader audit."""
from pathlib import Path
import importlib.util,json,re,subprocess,uuid
import sympy as sp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
sources=json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions']
cases=json.loads((HERE/'source-cases.json').read_text())
by_id={q[':question/math-academy-id']:q for q in sources}
counts={'source_questions':0,'source_complete_banks':0,'source_options':0,'source_distractors':0,'source_designations':0,'source_worked_solutions':0,'generated_records':0,'displayed_math_options':0,'displayed_solution_stages':0,'displayed_P_Q_pairs':0,'identity_checks':0,'invalid_input_checks':0}

def independent_linear(residual):
    # Polynomial degree in the actual displayed derivative, then verify the
    # normalized vector field lies in span{1,y}; do not use generator's flow.
    if residual.has(g.D2):return False
    n,d=sp.together(residual).as_numer_denom()
    if d.has(g.D):return False
    poly=sp.Poly(n,g.D)
    if poly.degree()!=1:return False
    a,b=poly.all_coeffs()
    flow=sp.cancel(-b/a)
    y0=flow.subs(g.Y,0)
    # Differentiation handles nonlinear functions that Poly(y) cannot parse.
    return sp.simplify(sp.diff(flow,g.Y,2))==0

def equation_equivalent(a,b):
    ratio=sp.cancel(a/b)
    return ratio!=0 and not ratio.has(g.D,g.D2)

def expression(t):
    r=g.LatexReader(t);v=r.expr();assert r.peek() is None,(t,r.tokens[r.i:]);return v

def audit(r):
    q=r['question'];f=q[':question/answer-fields'][0];answers=f[':answer-field/choices']
    assert len(answers)==5 and f[':answer-field/type']==':answer-field.type/radio'
    uuid.UUID(q[':question/id']);uuid.UUID(f[':answer-field/id'])
    assert f[':answer-field/correct'][0]==':answer/id'
    cid=f[':answer-field/correct'][1];assert sum(a[':answer/id']==cid for a in answers)==1
    target='**NOT**' not in q[':question/problem']
    residuals=[];correct=None
    for a in answers:
        uuid.UUID(a[':answer/id']);assert a[':answer/type']==':answer.type/math'
        value=a[':answer/value'];assert '$' not in value and '@@' not in value
        residual=g.read_equation(value);residuals.append(residual)
        truth=independent_linear(residual)
        assert (truth==target)==(a[':answer/id']==cid),(value,truth,cid)
        if a[':answer/id']==cid:correct=residual
        counts['displayed_math_options']+=1
    for i,a in enumerate(residuals):
        for b in residuals[:i]:assert not equation_equivalent(a,b)
    solution=q[':question/worked-solution'];assert '@@' not in solution
    # Every worked equation in a displayed aligned stage must be the same ODE
    # up to an invertible local factor; assess full equations, never sides alone.
    for block in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S):
        for stage in block.split(r'\\'):
            stage=stage.replace('&','').strip()
            if stage:
                parsed=g.read_equation(stage)
                assert equation_equivalent(parsed,correct),(stage,correct)
                counts['displayed_solution_stages']+=1
    for p,qv in re.findall(r'P\(x\)\s*=\s*(.*?)\$ and \$Q\(x\)\s*=\s*(.*?)\.\$',solution):
        flow=expression(qv)-expression(p)*g.Y
        n=sp.cancel(correct.subs(g.D,flow))
        assert sp.simplify(n)==0,(p,qv,n)
        counts['displayed_P_Q_pairs']+=1
    return r

review=[];engine=[]
for c in cases:
    source=by_id[c['source_id']];r=audit(g.generate(g.TEMPLATES[c['template']]['level'],template=c['template'],profile=c['bank_profile'],parameters=c['parameters']))
    q=r['question'];of=source[':question/answer-fields'][0];gf=q[':question/answer-fields'][0]
    assert q[':question/problem']==source[':question/problem']
    expected_solution=source[':question/worked-solution']
    if c['source_id']=='q-79750':expected_solution=expected_solution.replace('right-hand side depends on $y.$','right-hand side depends on $y$ through the nonlinear term $y^2.$')
    assert q[':question/worked-solution']==expected_solution
    oa={a[':answer/value']:a for a in of[':answer-field/choices']};ga={a[':answer/value']:a for a in gf[':answer-field/choices']}
    assert set(oa)==set(ga) and len(oa)==len(ga)==5
    assert of[':answer-field/key']==gf[':answer-field/key']
    correct_value=of[':answer-field/correct'][':answer/value']
    assert ga[correct_value][':answer/id']==gf[':answer-field/correct'][1]
    counts['source_questions']+=1;counts['source_complete_banks']+=1;counts['source_options']+=5;counts['source_distractors']+=4;counts['source_designations']+=1;counts['source_worked_solutions']+=1
    engine.append({'label':'source '+c['source_id'],'record':r})
    # Two reviewed variants of EVERY bank, not just every level.
    for p in ({'a':2,'h':-1},{'a':-1,'h':3}):
        v=audit(g.generate(g.TEMPLATES[c['template']]['level'],template=c['template'],parameters=p))
        review.append({'label':'Generated affine variant of '+c['source_id'],'record':v});engine.append({'label':review[-1]['label']+' '+str(p),'record':v})
    # Nine parameter boundary combinations, same complete profile selected.
    for a in (-6,-1,1,6):
        for h in (-8,0,8):
            v=audit(g.generate(g.TEMPLATES[c['template']]['level'],template=c['template'],parameters={'a':a,'h':h}))
            counts['generated_records']+=1
    one=g.generate(g.TEMPLATES[c['template']]['level'],seed=1,template=c['template'],parameters={'a':2,'h':-1})
    two=g.generate(g.TEMPLATES[c['template']]['level'],seed=99,template=c['template'],parameters={'a':2,'h':-1})
    assert one['question'][':question/id']==two['question'][':question/id']
    assert one['generation']['parameter_fingerprint']==two['generation']['parameter_fingerprint']
    assert one['question'][':question/id']!=r['question'][':question/id']
    assert one==g.generate(g.TEMPLATES[c['template']]['level'],seed=1,template=c['template'],parameters={'a':2,'h':-1})
    counts['identity_checks']+=4
for kwargs in ({'parameters':{'a':0,'h':1}},{'parameters':{'a':1}},{'parameters':{'a':True,'h':0}},{'parameters':{'a':7,'h':0}},{'field_type':'blank'},{'template':'q_8352'},{'template':'q_8349','profile':'q_79753'}):
    try:g.generate('easy',**kwargs)
    except ValueError:counts['invalid_input_checks']+=1
    else:raise AssertionError('Invalid explicit inputs accepted '+repr(kwargs))
for item in engine:
    f=item['record']['question'][':question/answer-fields'][0];cid=f[':answer-field/correct'][1]
    item['checks']=[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'all five owned source/variant radio options'} for a in f[':answer-field/choices']]
(HERE/'engine-input.json').write_text(json.dumps(engine,indent=2)+'\n')
subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
native=json.loads((HERE/'engine-report.json').read_text())
assert native['documented_unresolved_checks']==0
(HERE/'review.json').write_text(json.dumps(review,indent=2)+'\n')
lines=['# Original and generated question review','', 'All originals below are the exact captured banks at basis 1356. Generated affine variants are explicitly labeled. Correct designations appear only in this author review.','']
for c in cases:
    s=by_id[c['source_id']];lines+=['## Original '+c['source_id']+' ('+g.TEMPLATES[c['template']]['level']+')','',s[':question/problem'],'']
    f=s[':question/answer-fields'][0]
    lines += [('- Correct: ' if a[':answer/id']==f[':answer-field/correct'][':answer/id'] else '- ')+ '$'+a[':answer/value']+'$' for a in f[':answer-field/choices']]
    lines+=['',s[':question/worked-solution'],'']
    for v in review:
        if v['record']['generation']['template']==c['template']:
            r=v['record'];lines+=['### '+v['label']+' '+str(r['generation']['parameters']),'',g.markdown(r),'']
(HERE/'review.md').write_text('\n'.join(lines)+'\n')
report={'status':'pass','source_provenance':g.SOURCE,'counts':counts,'source_fidelity':{'banks':'12/12','options':'60/60','distractors':'48/48','correct_designations':'12/12','exact_prompts':'12/12','exact_worked_solutions':'11/12','supported_solution_repairs':'q-79750: identify quadratic RHS dependence, not dependence alone'},'native_grading':{k:native[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks','database_writes')},'authored_extensions':'Affine independent-variable function substitutions across all observed profiles; no new levels or template branches.','unresolved_findings':[]}
(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
