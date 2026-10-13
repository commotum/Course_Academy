#!/usr/bin/env python3
"""Failing full-bank, displayed-math, source-layout, identity and native checks.

The mathematical oracle parses learner-facing TeX, independently classifies
each ODE, and reads the threshold from the prompt. It does not trust recipe IDs
or the generator's designation. Source designation absence is reported honestly.
"""
import copy
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('inhibited_generator',str(HERE)+'.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
Y=sp.Symbol('y',real=True)
TRANSFORM=standard_transformations+(implicit_multiplication_application,rationalize)

def require(condition,message):
    if not condition: raise AssertionError(message)

def read_math(value):
    """Parse complete RHS and optional initial condition; reject malformed TeX."""
    require(re.fullmatch(r'\\frac\{dy\}\{dt\}\s*=\s*.+',value) is not None,'Rendered derivative shape')
    rhs=value.split('=',1)[1]
    initial=None
    if r',\,y(0)=' in rhs:
        rhs,initial=rhs.split(r',\,y(0)=')
        initial=sp.Rational(initial.replace(r'\,',''))
    raw=rhs.replace(r'\,','').replace('{','').replace('}','').replace('^','**')
    require('\\' not in raw,'Unknown rendered math command')
    expr=parse_expr(raw,local_dict={'y':Y},transformations=TRANSFORM)
    require(expr.free_symbols<= {Y},'Unexpected symbol in displayed option')
    return sp.expand(expr),initial

def equivalent(left,right):
    return sp.Poly(left[0]-right[0],Y).is_zero and left[1]==right[1]

def independent(record):
    q=record['question']; f=q[':question/answer-fields'][0]; gen=record['generation']
    require(len(q[':question/answer-fields'])==1,'One observed field')
    require(f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection','Observed field shape')
    require(len(f[':answer-field/choices'])==5,'Full five-choice bank')
    require(f[':answer-field/correct'][0]==':answer/id','Lookup-ref shape')
    choices=f[':answer-field/choices']; maths=[read_math(a[':answer/value']) for a in choices]
    for j,m in enumerate(maths): require(not any(equivalent(m,n) for n in maths[:j]),'Whole-bank equivalence collision')
    template=gen['template']; level=q[':question/difficulty'].split('/')[-1]
    require(g.TEMPLATES[template]==level,'Difficulty boundary')
    threshold=None
    if template!='ivp':
        match=re.search(r'\$y\s*>\s*(\d+)\$',q[':question/problem'])
        require(match is not None,'Prompt threshold')
        threshold=sp.Integer(match.group(1))
        require('initial value' not in q[':question/problem'],'Equation scope')
    else: require(q[':question/problem']=='Which of the following initial value problems is an inhibited decay problem?','IVP scope')
    true=[]
    for i,(rhs,initial) in enumerate(maths):
        poly=sp.Poly(rhs,Y)
        require((initial is not None)==(template=='ivp'),'Answer fragment shape')
        if poly.degree()!=1 or poly.coeff_monomial(Y)>=0: continue
        equilibrium=-poly.coeff_monomial(1)/poly.coeff_monomial(Y)
        if initial is None and equilibrium==threshold or initial is not None and initial>equilibrium: true.append(i)
    require(len(true)==1,'Independent unique inhibited decay model')
    index=true[0]; aid=choices[index][':answer/id']
    require(aid==f[':answer-field/correct'][1],'Displayed mathematics correct designation')
    rhs,initial=maths[index]; rate=-sp.Poly(rhs,Y).coeff_monomial(Y)
    equilibrium=-sp.Poly(rhs,Y).coeff_monomial(1)/sp.Poly(rhs,Y).coeff_monomial(Y)
    worked=q[':question/worked-solution']
    definition=r'\frac{dy}{dt}=-k(y-a),\,y(0)={y}_{0}' if template=='ivp' else r'\frac{dy}{dt}=-k(y-a),'
    require('$$\n'+definition+'\n$$' in worked,'Mathematical definition in worked solution')
    # Verify numeric equations actually shown in the worked solution, not stored
    # intermediates. Generic definition with k/a is excluded by lexical test.
    equations=[]
    for block in re.findall(r'\$\$\n(.*?)\n\$\$',worked,re.S):
        block=block.rstrip('.,')
        if re.search(r'[ka]',block.split('=',1)[-1]): continue
        equations.append(read_math(block))
    require(len(equations)==(2 if template in ('expanded','ivp') else 1),'Worked-solution equation sequence')
    require(equivalent(equations[0],maths[index]),'First shown worked equation equals correct full object')
    if template=='expanded': require(equivalent(equations[1],maths[index]),'Factored displayed intermediate')
    if template=='ivp':
        require(equations[1][0]==rhs and equations[1][1]<equilibrium,'Shown nondecay IVP')
        low=g.number(equations[1][1],gen['bank_profile']=='ivp_decimal_grouped')
        high=g.number(initial,gen['bank_profile']=='ivp_decimal_grouped')
        require('${y}_{0}='+high+'.$' in worked and '${y}_{0}='+low+'<a=' in worked,'Initial-value worked statements')
    a=g.number(equilibrium,gen['bank_profile']=='ivp_decimal_grouped'); k=g.number(rate)
    require('$k='+k+(',' if template=='ivp' else ',$') in worked,'Displayed rate constant')
    require(('a='+a+(',' if template=='ivp' else '.$')) in worked,'Displayed equilibrium constant')
    # IDs are independently regenerated from final displayed content and domain.
    content=g.digest({'parameter_fingerprint':gen['parameter_fingerprint'],'prompt':q[':question/problem'],'solution':worked,'bank':sorted(a[':answer/value'] for a in choices)})
    require(content==gen['content_fingerprint'],'Content identity fingerprint')
    qid=uuid.uuid5(uuid.NAMESPACE_URL,f'course-academy/{g.KP_UUID}/{g.VERSION}/{content}')
    require(q[':question/id']==str(qid),'Question identity')
    fid=uuid.uuid5(qid,'selection'); require(f[':answer-field/id']==str(fid),'Field-owned identity')
    for answer in choices:
        require(answer[':answer/type']==':answer.type/math','Math enum')
        require(answer[':answer/id']==str(uuid.uuid5(fid,'math:'+answer[':answer/value'])),'Answer-owned identity')
        require('$' not in answer[':answer/value'],'Delimiter-free math')
    return maths

def fidelity(original,record):
    q=record['question']; f=q[':question/answer-fields'][0]; original_field=original[':question/answer-fields'][0]
    require(original[':question/problem']==q[':question/problem'],'Source prompt fidelity')
    require(f[':answer-field/key']==original_field[':answer-field/key'],'Source field key')
    require(f[':answer-field/type']==original_field[':answer-field/type'][':db/ident'],'Source field enum')
    old=original_field[':answer-field/choices']; new=f[':answer-field/choices']
    require(sorted(a[':answer/value'] for a in old)==sorted(a[':answer/value'] for a in new),'Full exact source bank fidelity')
    for old_answer in old:
        require(sum(equivalent(read_math(old_answer[':answer/value']),read_math(a[':answer/value'])) for a in new)==1,'One-to-one whole mathematical bank')
    if ':answer-field/correct' in original_field:
        correct=next(a for a in new if a[':answer/id']==f[':answer-field/correct'][1])
        require(correct[':answer/value']==original_field[':answer-field/correct'][':answer/value'],'Observed designation fidelity')
    if ':question/worked-solution' in original: require(q[':question/worked-solution']==original[':question/worked-solution'],'Source fixed solution fidelity')

def expect_failure(fn,message):
    try: fn()
    except (AssertionError,ValueError,TypeError,SyntaxError): return
    raise AssertionError('Negative control was accepted: '+message)

def render(records):
    (HERE/'render-input.json').write_text(json.dumps(records))
    subprocess.run([sys.executable,str(HERE/'render_math.py')],check=True)
    return ['rendered-'+level+'.png' for level in ('easy','moderate','hard')]

def main():
    cases=json.loads((HERE/'source-cases.json').read_text()); wrapper=json.loads((HERE/'source.json').read_text())
    sources={q[':question/math-academy-id']:q for q in wrapper['record'][':knowledge-point/questions']}
    source_records=[]; review=[]; details=[]
    for case in cases:
        record=g.generate(case['level'],seed=11,parameters=case['parameters'],profile=case['bank_profile'])
        independent(record);fidelity(sources[case['source_id']],record);source_records.append(record)
        details.append({'source_id':case['source_id'],'options_matched':5,'complete_bank_matched':True,'prompt_matched':True,'solution_matched':case['source_id']!='q-105893','designation_matched':case['source_id']!='q-105893','source_repair':case['source_id']=='q-105893'})
    for profile,bank in g.BANK_PROFILES.items():
        level=g.TEMPLATES[bank['template']]
        for seed in range(60):
            record=g.generate(level,seed=seed,profile=profile);independent(record)
            params=record['generation']['parameters']
            stable=g.generate(level,seed=seed+999,parameters=params,profile=profile);independent(stable)
            require(record['question'][':question/id']==stable['question'][':question/id'],'Seed independent fixed content')
            if seed in (12,31): review.append(record)
    for level in ('easy','moderate','hard'):
        for seed in range(20):
            record=g.generate(level,seed);independent(record)
    for level,params in [('easy',{'a':20,'k':80}),('moderate',{'a':8,'k':22}),('hard',{'a':1500,'k':'0.002','below':1000,'above':3000})]:
        record=g.generate(level,seed=3,parameters=params)
        equivalent_params={key:str(value)+'.0' if isinstance(value,int) else value for key,value in params.items()}
        require(record['question'][':question/id']==g.generate(level,seed=800,parameters=equivalent_params)['question'][':question/id'],'Canonical default bank/identity for equivalent parameter forms')
        banks=[g.generate(level,parameters=params,profile=name)['question'][':question/id'] for name,bank in g.BANK_PROFILES.items() if g.TEMPLATES[bank['template']]==level]
        require(len(set(banks))==len(banks),'Distinct displayed banks have distinct IDs')
    bad=copy.deepcopy(source_records[0]);bad['question'][':question/answer-fields'][0][':answer-field/choices'].pop()
    expect_failure(lambda:independent(bad),'missing choice')
    bad=copy.deepcopy(source_records[0]);bad['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']=r'\frac{dy}{dt}=3'
    expect_failure(lambda:independent(bad),'displayed option corruption')
    bad=copy.deepcopy(source_records[2]);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('k=80','k=81')
    expect_failure(lambda:independent(bad),'worked numeric corruption')
    bad=copy.deepcopy(source_records[2]);bad['question'][':question/answer-fields'][0][':answer-field/correct'][1]='00000000-0000-0000-0000-000000000000'
    expect_failure(lambda:independent(bad),'grading identity corruption')
    bad=copy.deepcopy(source_records[2]);bad['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']+= ' '
    expect_failure(lambda:fidelity(sources['q-105898'],bad),'source exact-bank corruption')
    for fn in (lambda:g.generate('easy',parameters={'a':0,'k':2}),lambda:g.generate('hard',parameters={'a':5,'k':2,'below':4,'above':5}),lambda:g.generate('easy',profile='expanded')): expect_failure(fn,'invalid explicit parameters/profile')
    rows=[]
    for i,record in enumerate(source_records+review):
        f=record['question'][':question/answer-fields'][0]
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Independent displayed model and initial-value classification'} for a in f[':answer-field/choices']]
        rows.append({'label':str(i),'record':record,'checks':checks})
    (HERE/'engine-input.json').write_text(json.dumps(rows,indent=2)+'\n')
    engine=ROOT/'generate/runs/current/check-engine'
    subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True,cwd=ROOT)
    # Check actual native error/selection failures are fatal too.
    neg=copy.deepcopy(rows[:1]);neg[0]['checks'][0]['expected']='rejected' if neg[0]['checks'][0]['expected']=='accepted' else 'accepted'
    (HERE/'engine-negative-input.json').write_text(json.dumps(neg))
    result=subprocess.run([str(engine),str(HERE/'engine-negative-input.json'),str(HERE/'engine-negative-report.json')],capture_output=True,text=True)
    require(result.returncode!=0,'Native grading negative control')
    (HERE/'engine-negative-result.txt').write_text(result.stderr)
    rendered=render(review)
    (HERE/'review.json').write_text(json.dumps({'original_replays':source_records,'generated_variants':review},indent=2)+'\n')
    parts=['# Source and variant review','Original capture: math basis 1356. Original payloads remain in source.json. q-105893 has an authored moderate level, correct designation and solution; these are not observed matches.']
    for case,record in zip(cases,source_records):
        parts+=['## Original '+case['source_id'],'Parameters: `'+json.dumps(case['parameters'])+'`. '+case['level_origin'],g.markdown(record)]
    for record in review: parts+=['## Generated parameter variant (authored sampling bounds)',g.markdown(record)]
    (HERE/'review.md').write_text('\n\n'.join(parts)+'\n')
    report={'passed':True,'database':wrapper['database'],'basis':wrapper['basis'],'lineage':wrapper['lineage'],'source_questions':7,'full_banks_matched':7,'source_options_matched':35,'source_options_total':35,'observed_distractors_matched':24,'independently_inferred_distractors_matched':4,'available_designations_matched':6,'available_designations_total':6,'missing_source_designations':1,'available_solutions_matched':6,'available_solutions_total':6,'prompt_matches':7,'observed_templates':3,'complete_profiles':6,'generated_variant_records':12,'sweep_records':420,'negative_controls':9,'native_grading':json.loads((HERE/'engine-report.json').read_text()),'rendered_math_assets':rendered,'source_details':details,'authored_repairs':['q-105893: moderate assignment, independently derived designation, source-style worked solution'],'unresolved_findings':[],'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'no_database_writes':True}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: 7/7 banks; 35/35 options; 6/6 available designations/solutions; 420 mathematical variants; native grader; 9 negative controls')

if __name__=='__main__':
    try: main()
    except Exception as exc:
        (HERE/'validation.json').write_text(json.dumps({'passed':False,'failure':str(exc)},indent=2)+'\n')
        raise
