#!/usr/bin/env python3
"""Read displayed systems/each solution stage independently; real native grading."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import sympy as sp

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
spec=importlib.util.spec_from_file_location('solution_count_generator',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X,Y=sp.symbols('x y')
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
TRANS=standard_transformations+(implicit_multiplication_application,)


def expr(text):
    text=text.strip().replace(' ', '')
    text=re.sub(r'\\frac\{(-?\d+)\}\{(-?\d+)\}',r'(\1/\2)',text)
    assert not '\\' in text,text
    return sp.expand(parse_expr(text,local_dict={'x':X,'y':Y},transformations=TRANS))


def equation(text):
    lhs,rhs=text.replace('&','').split('=')
    return expr(lhs),expr(rhs)


def coefficients(pair):
    exp=sp.expand(pair[0]-pair[1])
    assert sp.Poly(exp,X,Y).total_degree() <= 1
    return (exp.coeff(X),exp.coeff(Y),-exp.subs({X:0,Y:0}))


def displayed_system(rec):
    prompt=rec['question'][':question/problem']
    math=re.search(r'\$([^$]*)\$',prompt).group(1)
    math=math.removeprefix('\\{').removeprefix('{')
    eqs=[equation(row) for row in math.split(';')]
    assert len(eqs)==2
    return [coefficients(pair) for pair in eqs]


def independent_count(rows):
    A=sp.Matrix([[r[0],r[1]] for r in rows]); aug=A.row_join(sp.Matrix([r[2] for r in rows]))
    return g.VALUES[0] if A.rank()!=aug.rank() else g.VALUES[2] if A.rank()==2 else g.VALUES[1]


def format_check(text):
    assert text.count('$')%2==0
    # Raw malformed brace stays evidence-only; never exempt normal output.
    groups=re.sub(r'\\[{}]','',text)
    depth=0
    for char in groups:
        if char=='{':depth+=1
        if char=='}':depth-=1
        assert depth>=0
    assert depth==0,(depth,text)
    assert not any(s in text for s in ('+-','--','None','nan','z^','x^2','y^2'))


def check_record(rec):
    q=rec['question']; meta=rec['generation']; fields=q[':question/answer-fields'];f=fields[0]
    assert rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    assert len(fields)==1 and f[':answer-field/type']==':answer-field.type/select'
    assert '{{field-1}}' in q[':question/problem']
    vals=[a[':answer/value'] for a in f[':answer-field/choices']]
    assert sorted(vals)==sorted(g.VALUES) and len(set(vals))==3
    assert all(a[':answer/type']==':answer.type/text' for a in f[':answer-field/choices'])
    rows=displayed_system(rec)
    independent=independent_count(rows)
    assert meta['inferred_correct_value']==independent
    if meta['raw_evidence']:
        assert not meta['eligible_for_learning']
        assert ':question/difficulty' not in q and ':question/worked-solution' not in q and ':answer-field/correct' not in f
        return
    assert meta['eligible_for_learning']
    assert q[':question/difficulty']==':question.difficulty/'+meta['authored_level']
    correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
    assert correct[':answer/value']==independent
    for text in (q[':question/problem'],q[':question/worked-solution']):format_check(text)
    solution=q[':question/worked-solution']
    assert solution.startswith("Let's start by solving the system using elimination.")
    match=re.search(r'multiply the (first|second) equation by \$([^$]+)\$',solution)
    index=0 if match.group(1)=='first' else 1
    factor=expr(match.group(2)); assert factor!=0 and factor.is_integer
    before=rows[index];other=rows[1-index]
    assert factor*before[0]+other[0]==0
    # The conclusion's variable cancellation term also agrees with prompt.
    term=re.search(r'get a \$([^$]+)\$ term',solution).group(1)
    assert expr(term)==factor*before[0]*X
    blocks=re.findall(r'\\begin\{aligned\}\n(.*?)\n\\end\{aligned\}',solution,re.S)
    parsed=[[equation(row) for row in block.split('\\\\\n')] for block in blocks]
    if meta['template']=='zero_rhs':
        assert 'rearrange each equation' in solution and len(parsed[0])==2
        assert [coefficients(pair) for pair in parsed.pop(0)]==rows
    else:
        assert 'rearrange each equation' not in solution
    elimination=parsed.pop(0)
    transformed=list(rows)
    transformed[index]=tuple(factor*v for v in before)
    assert [coefficients(pair) for pair in elimination[:2]]==transformed
    summed=tuple(sum(r[i] for r in transformed) for i in range(3))
    assert summed[0]==0
    assert coefficients(elimination[2])==summed
    assert coefficients(elimination[3])==summed
    # Ensure unevaluated constant-addition stage wasn't replaced by final value.
    raw_block=blocks[1 if meta['template']=='zero_rhs' else 0]
    sum_row=raw_block.split('\\\\\n')[2]
    assert re.search(r'&= \([^()]+ [+-] [^()]+\)',sum_row),sum_row
    annotation=re.search(r'\$\$\n\\\{(.*?)\n\$\$',solution,re.S).group(1)
    annotated=annotation.split('; ')
    for i,line in enumerate(annotated):
        base=line.split(r'\mid')[0].strip()
        assert coefficients(equation(base))==rows[i]
        assert (r'\cdot (' in line)==(i==index)
    if independent==g.VALUES[2]:
        assert len(elimination)==5 and len(parsed)==1 and len(parsed[0])==3
        yy=elimination[-1][1];xx=parsed[0][-1][1]
        assert elimination[-1][0]==Y and parsed[0][-1][0]==X
        for aa,bb,cc in rows:assert aa*xx+bb*yy==cc
        sub=parsed[0]
        assert expr(str(sub[0][0]))==rows[0][0]*X+rows[0][1]*yy
        assert sub[0][1]==rows[0][2]
        assert sub[1]==(rows[0][0]*X,rows[0][2]-rows[0][1]*yy)
        final=re.search(r'single solution\*, \$\((.*?),(.*?)\)\$',solution)
        assert (expr(final.group(1)),expr(final.group(2)))==(xx,yy)
    else:
        assert len(elimination)==4 and not parsed
        truth='true' if independent==g.VALUES[1] else 'false'
        assert f'*always {truth}*' in solution and f'*{independent}*' in solution
        final=re.search(r'The statement \$0=([^$]+)\$',solution)
        assert expr(final.group(1))==summed[2]


def engine_item(rec,label):
    f=rec['question'][':question/answer-fields'][0]
    correct=f[':answer-field/correct'][1]
    return {'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],
             'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'actual select grading; '+a[':answer/value']}
            for a in f[':answer-field/choices']]}


def write(name,obj):
    (HERE/name).write_text(json.dumps(obj,indent=2)+'\n')


def main():
    write('validation.json',{'passed':False,'status':'validation running'})
    capture=json.loads((HERE/'source.json').read_text());sources=capture['record'][':knowledge-point/questions']
    cases=json.loads((HERE/'source-cases.json').read_text())
    native=[];review=[];notes=['# Number-of-solutions review','','Raw captures lack difficulty, correct refs and worked solutions. Completion/level labels below are authored. Literal raw braces remain evidence; normal output escapes the literal system brace.']
    banks=options=raw_prompts=0
    for case,source in zip(cases,sources,strict=True):
        assert case['source_id']==source[':question/math-academy-id']
        rec=g.generate(case['authored_level'],parameters=case['parameters'],template=case['template'],profile=case['bank_profile'])
        check_record(rec)
        q=rec['question'];sf=source[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
        assert q[':question/problem']==source[':question/problem'];raw_prompts+=1
        for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):
            assert (key in q)==(key in source)
        assert (':answer-field/correct' in f)==(':answer-field/correct' in sf)
        assert f[':answer-field/key']==sf[':answer-field/key']
        assert f[':answer-field/type']==sf[':answer-field/type'][':db/ident']
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
        banks+=1;options+=3
        for raw_seed in range(12):
            changed_raw=g.generate(case['authored_level'],seed=raw_seed,profile=case['bank_profile'])
            check_record(changed_raw)
            assert changed_raw['question'][':question/problem']!=source[':question/problem']
        review.append(rec)
        notes.extend(['','## Original '+case['source_id'],'',g.markdown(rec)])
        normal=g.generate(case['authored_level'],parameters=case['parameters'],template=case['template'])
        check_record(normal);native.append(engine_item(normal,'completed '+case['source_id']));review.append(normal)
        notes.extend(['','### Inferred completion at the original parameters','',g.markdown(normal)])
        changed=g.generate(case['authored_level'],seed=31+len(review),template=case['template'])
        check_record(changed);native.append(engine_item(changed,'changed '+case['source_id']));review.append(changed)
        notes.extend(['','### Generated variant','',g.markdown(changed)])
    diversity={};coverage={};tested=0
    for level in g.LEVELS:
        seen=set();branches=set();correct_positions=set();templates=set();multiplier_rows=set();review_branches=set()
        for seed in range(360):
            rec=g.generate(level,seed=seed);check_record(rec);tested+=1
            multiplier_rows.add(re.search(r'multiply the (first|second) equation',rec['question'][':question/worked-solution']).group(1))
            seen.add(rec['generation']['parameter_fingerprint']);branches.add(rec['generation']['inferred_correct_value']);templates.add(rec['generation']['template'])
            f=rec['question'][':question/answer-fields'][0];correct_positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
            if seed<18:native.append(engine_item(rec,f'{level} default {seed}'))
            if rec['generation']['inferred_correct_value'] not in review_branches:
                review_branches.add(rec['generation']['inferred_correct_value'])
                review.append(rec);notes.extend(['','## Generated '+level+' variant '+str(seed),'',g.markdown(rec)])
            again=g.generate(level,seed=seed+5000,template=rec['generation']['template'],parameters=rec['generation']['parameters'])
            assert again['question'][':question/id']==rec['question'][':question/id']
            assert again['generation']['content_fingerprint']==rec['generation']['content_fingerprint']
        assert branches==set(g.VALUES) and correct_positions=={0,1,2}
        assert len(seen)>=100
        assert multiplier_rows==({'first','second'} if level=='moderate' else {'first'})
        diversity[level]={'sampled_records':360,'distinct_canonical_line_pairs':len(seen),'not_exhaustive':True}
        coverage[level]={'templates':sorted(templates),'response_branches':sorted(branches),'correct_positions':sorted(correct_positions),'multiplier_rows':sorted(multiplier_rows)}
    # Canonical alias/scalar checks, distinguishing actual changed line objects.
    p=cases[0]['parameters'];fp=g.mathematical_fingerprint(p,'standard')
    scaled={k:2*v for k,v in p.items()}
    individual_scaled={**p,**{k:2*p[k] for k in 'abc'}}
    assert g.mathematical_fingerprint(individual_scaled,'standard')==fp
    swapped=dict(zip('abcdef',[p[k] for k in 'bac edf'.replace(' ', '')]))
    assert g.mathematical_fingerprint(scaled,'standard')==fp
    assert g.mathematical_fingerprint(swapped,'standard')==fp
    rowswap=dict(zip('abcdef',[p[k] for k in 'defabc']))
    assert g.mathematical_fingerprint(rowswap,'standard')==fp
    assert g.mathematical_fingerprint({**p,'f':p['f']+1},'standard')!=fp
    # Deliberately corrupt the visible prompt/stage/conclusion/field designation.
    sample=next(g.generate('moderate',seed=s) for s in range(100) if g.generate('moderate',seed=s)['generation']['inferred_correct_value']==g.VALUES[2])
    corrupt=[]
    r=copy.deepcopy(sample);r['question'][':question/problem']=r['question'][':question/problem'].replace(' = ',' = 1 + ',1);corrupt.append(r)
    r=copy.deepcopy(sample);r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace('y &=','y &= 1 +',1);corrupt.append(r)
    r=copy.deepcopy(sample);r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace('x &=','x &= 1 +',1);corrupt.append(r)
    r=copy.deepcopy(sample);r['question'][':question/worked-solution']=re.sub(r'&= \([^\n]*\)', '&= 0',r['question'][':question/worked-solution'],count=1);corrupt.append(r)
    r=copy.deepcopy(sample);f=r['question'][':question/answer-fields'][0];f[':answer-field/correct'][1]=next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1]);corrupt.append(r)
    for r in corrupt:
        try:check_record(r)
        except (AssertionError,ValueError):pass
        else:raise AssertionError('Validator accepted a corrupt display/stage/key')
    boundary_records=[]
    for level,p in [('easy',dict(zip('abcdef',(5,-5,12,-5,3,-12)))),
                    ('moderate',dict(zip('abcdef',(-2,5,30,-8,-10,-30)))),
                    ('hard',dict(zip('abcdef',(-3,1,30,-12,4,-30))))]:
        rec=g.generate(level,parameters=p);check_record(rec);boundary_records.append(rec)
        native.append(engine_item(rec,'signed boundary '+level))
        review.append(rec);notes.extend(['','## Generated signed boundary '+level,'',g.markdown(rec)])
    invalid=[('easy','standard',cases[0]['parameters']),('moderate','zero_rhs',cases[0]['parameters']),
             ('hard','zero_rhs',{**cases[1]['parameters'],'b':2}),('moderate','standard',{**cases[0]['parameters'],'a':-13}),
             ('easy','standard',dict(zip('abcdef',(1,1,0,2,2,1)))),
             ('moderate','standard',dict(zip('abcdef',(1,1,0,5,2,1)))),
             ('hard','zero_rhs',{**cases[1]['parameters'],'c':0}),
             ('hard','zero_rhs',{**cases[1]['parameters'],'e':-5}),
             ('hard','zero_rhs',{**cases[1]['parameters'],'d':-13}),
             ('moderate','standard',{**cases[0]['parameters'],'c':31}),
             ('moderate','standard',{**cases[0]['parameters'],'b':0}),
             ('moderate','standard',{**cases[0]['parameters'],'c':1.5})]
    for level,t,p in invalid:
        try:g.generate(level,template=t,parameters=p)
        except ValueError:pass
        else:raise AssertionError('Explicit level bound bypassed')
    write('review.json',review);(HERE/'review.md').write_text('\n'.join(notes)+'\n')
    write('engine-input.json',native)
    harness=REPO/'generate/runs/current/check-engine'
    subprocess.run([str(harness),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True,capture_output=True,text=True)
    eng=json.loads((HERE/'engine-report.json').read_text())
    assert eng['documented_unresolved_checks']==0
    report={'passed':True,'basis':capture['basis'],'source_questions':3,'raw_exact_prompts':raw_prompts,
            'matched_complete_banks':banks,'matched_options':options,'source_correct_designations':{'matched':0,'total_present':0,'inferred':3},
            'source_solution_fidelity':{'present':0,'raw_omission_matches':3,'authored_completions':3},
            'raw_difficulty_omission_matches':3,'raw_correct_omission_matches':3,'presentation_repairs':3,
            'normal_math_records':tested+6+len(boundary_records),'mutation_failures_caught':len(corrupt),'invalid_explicit_calls_rejected':len(invalid),'signed_boundaries_checked':len(boundary_records),'default_coverage':coverage,
            'variety':diversity,'native_grading':{'accepted':eng['accepted_checks'],'rejected':eng['rejected_checks'],'unresolved':0},
            'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'engine_sha256':hashlib.sha256(harness.read_bytes()).hexdigest(),
            'engine_source_sha256':hashlib.sha256(harness.with_suffix('.rs').read_bytes()).hexdigest(),
            'changed_raw_parameterized_replays':36,
            'no_database_writes':True,'unresolved_findings':[]}
    write('validation.json',report)
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        write('validation.json',{'passed':False,'failure_type':type(exc).__name__,'failure':str(exc)})
        raise
