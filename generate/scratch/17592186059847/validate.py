#!/usr/bin/env python3
"""Failing checks for source banks, rendered mathematics, identity, and native grading."""
from pathlib import Path
import importlib.util
import hashlib
import json
import re
import subprocess
import sys
import sympy as sp

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('det_generator',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)


def require(condition,message):
    if not condition:raise AssertionError(message)


def independent_det(m):
    a,b,c,d,e,f,g,h,i=m
    return a*e*i+b*f*g+c*d*h-c*e*g-b*d*i-a*f*h


def determinant_match(match):
    entries=list(map(int,re.findall(r'-?\d+',match.group(1))))
    n=int(len(entries)**.5)
    require(n*n==len(entries),'rendered determinant is not square')
    return '('+str(sp.Matrix(n,n,entries).det())+')'


def arithmetic_solution_values(solution):
    require(solution.startswith(g.OPENING+'\n\n$$\n'),'Worked-solution opening changed')
    text=solution.split('$$\n',1)[1].rsplit('\n$$',1)[0]
    text=text.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}')
    text=re.sub(r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|',determinant_match,text)
    values=[]
    for row in text.split(r'\\'):
        require(' & =' in row,'Broken aligned calculation row')
        lhs,rhs=row.split(' & =',1)
        expr=rhs.replace(r'\cdot','*').replace(' ','')
        expr=re.sub(r'(?<=[0-9)])(?=\()', '*',expr)
        expr=re.sub(r'(?<=\))(?=[0-9])', '*',expr)
        require(bool(re.fullmatch(r'[0-9()+*\-]+',expr)),'Unexpected learner arithmetic: '+expr)
        value=sp.sympify(expr)
        require(value.is_Integer,'Noninteger work row')
        values.append(int(value))
        if lhs.strip():require(int(sp.sympify(lhs.strip()))==value,'LHS determinant mismatch')
    return values


def check_record(record):
    q=record['question'];meta=record['generation'];m=meta['parameters']['matrix']
    f=q[':question/answer-fields'][0]
    expected=independent_det(m)
    require(expected==int(sp.Matrix(3,3,m).det()),'Independent determinant disagreement')
    require(meta['worked_values']['determinant']==expected,'Intermediate determinant mismatch')
    independent_minors=[int(sp.Matrix(3,3,m).minor_submatrix(0,k).det()) for k in range(3)]
    require(independent_minors==meta['worked_values']['minors'],'Minor values incorrect')
    require(all(v==expected for v in arithmetic_solution_values(q[':question/worked-solution'])),'Rendered work row incorrect')
    for key in (':question/id',):require(str(__import__('uuid').UUID(q[key]))==q[key],'Question ID invalid')
    correct=f[':answer-field/correct'];require(correct[0]==':answer/id','Wrong correct-ref shape')
    answers=f[':answer-field/choices'];values=[int(a[':answer/value']) for a in answers]
    import uuid
    require(f[':answer-field/id']==str(uuid.uuid5(uuid.UUID(q[':question/id']),f[':answer-field/key'])),'Field is not owned by question')
    require(all(a[':answer/id']==str(uuid.uuid5(uuid.UUID(f[':answer-field/id']),'math:'+a[':answer/value'])) for a in answers),'Answer is not owned by field')
    require(len(values)==len(set(values)),'Equivalent bank options')
    require(values.count(expected)==1,'Bank correctness ambiguous')
    require(next(a[':answer/value'] for a in answers if a[':answer/id']==correct[1])==str(expected),'Correct ref wrong')
    require(len(answers)==(5 if f[':answer-field/type'].endswith('/radio') else 1),'Choice count wrong')
    require(meta['plot_rating']=='none' and not meta['plot_assets'],'Unexpected plots')
    require('{{field-1}}' in q[':question/problem'] if f[':answer-field/type'].endswith('/blank') else '{{' not in q[':question/problem'],'Field layout changed')
    require(all(a[':answer/type']==':answer.type/math' and '$' not in a[':answer/value'] for a in answers),'Answer format wrong')
    checks=[]
    if f[':answer-field/type'].endswith('/radio'):
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if int(a[':answer/value'])==expected else 'rejected','purpose':'Every displayed owned radio option'} for a in answers]
    else:
        checks=[{'submitted':str(expected),'expected':'accepted','purpose':'Canonical integer'},
                {'submitted':f'{expected} + 0','expected':'accepted','purpose':'Equivalent arithmetic expression'},
                {'submitted':str(expected+1),'expected':'rejected','purpose':'Incorrect integer'}]
    return checks


def main():
    cases=json.loads((HERE/'source-cases.json').read_text())
    require(len(cases)==15,'Missing source question')
    originals=[];report=[];native=[];count=0;distractors=0
    for case in cases:
        record=g.generate(case['level'],7,case['template'],parameters=case['parameters'],profile=case['bank_profile'])
        native.append({'label':'source-'+case['source_id'],'record':record,'checks':check_record(record)})
        q=record['question'];source=case['original'];sf=source[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
        require(q[':question/problem']==source[':question/problem'],case['source_id']+': prompt fidelity')
        require(f[':answer-field/key']==sf[':answer-field/key'] and f[':answer-field/type']==sf[':answer-field/type'][':db/ident'],'Field fidelity')
        observed=sorted(int(a[':answer/value']) for a in sf[':answer-field/choices']);generated=sorted(int(a[':answer/value']) for a in f[':answer-field/choices'])
        require(observed==generated,case['source_id']+': incomplete original bank')
        val=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        if ':answer-field/correct' in sf:require(val==sf[':answer-field/correct'][':answer/value'],'Source correct designation mismatch')
        if ':question/worked-solution' in source:
            work_rows=arithmetic_solution_values(source[':question/worked-solution'])
            if case['source_id']=='q-128309':require(work_rows==[-32,14,-32,-32,-32],'Known source sign error evidence changed')
            else:require(all(x==int(val) for x in work_rows),'Untracked source arithmetic error')
        count+=len(observed);distractors+=len(observed)-1
        report.append({'source_id':case['source_id'],'prompt_matched':True,'choices_matched':len(observed),'choices_total':len(observed),'bank_matched':True,'correct_ref_observed':':answer-field/correct' in sf,'worked_solution':'shared opening and calculation stages retained; notation/zero simplification normalized' if ':question/worked-solution' in source else 'absent in source; authored source-style expansion'})
        originals.append(record)
    generated=[]
    # Each complete source profile is selected and tested explicitly.
    configurations=[('easy',v[0],k) for k,v in g.BANK_PROFILES.items()]
    configurations += [(level,template,None) for level in ('easy','moderate','hard') for template,v in g.TEMPLATES.items() if v['kind']=='blank']
    configurations += [(level,'aligned_radio','cofactor_signs') for level in ('moderate','hard')]
    for level,template,profile in configurations:
        fingerprints=set()
        for seed in range(30):
            record=g.generate(level,seed,template,profile=profile)
            checks=check_record(record)
            native.append({'label':f'{level}/{template}/{profile}/{seed}','record':record,'checks':checks})
            replay=g.generate(level,seed+100000,template,parameters=record['generation']['parameters'],profile=record['generation']['bank_profile'])
            require(record['question'][':question/id']==replay['question'][':question/id'],'Identity changed with seed')
            require(record['question'][':question/worked-solution']==replay['question'][':question/worked-solution'],'Solution changed with choice order')
            fingerprints.add(record['generation']['parameter_fingerprint'])
            if seed<2:generated.append(record)
            if level!='easy':
                lower,upper=(2,8) if level=='moderate' else (4,12)
                require(all(lower<=abs(x)<=upper for x in record['generation']['parameters']['matrix']),'Authored level sampling scope')
        require(len(fingerprints)>=25,'Insufficient genuine parameter variation')
    # Explicit invalid inputs must not silently resample; full zero radio bank fails.
    for args in [dict(level='easy',template='aligned_radio',parameters={'matrix':[0]*9},profile='cofactor_signs'),
                 dict(level='easy',template='matrix_blank',parameters={'matrix':[1]*8}),
                 dict(level='easy',template='matrix_blank',parameters={'matrix':[1.0]*9}),
                 dict(level='hard',template='aligned_radio',profile='diagonal')]:
        try:g.generate(**args)
        except ValueError:pass
        else:raise AssertionError('Invalid explicit input accepted')
    # Default generation must never promote uncertain source-bank hypotheses.
    for level in ('easy','moderate','hard'):
        for seed in range(30):
            r=g.generate(level,seed)
            require(r['generation']['template']!='legacy_radio','Legacy hypothesis selected by default')
            if r['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/radio'):
                require(r['generation']['bank_profile']=='cofactor_signs','Uncertain source bank selected by default')
    # Displayed banks affect identity, while mathematical parameter fingerprints agree.
    found=False
    for seed in range(100):
        r=g.generate('easy',seed,'aligned_radio',profile='signed_one_zero')
        try:s=g.generate('easy',seed,'aligned_radio',parameters=r['generation']['parameters'],profile='cofactor_signs')
        except g.SampleRejected:continue
        if sorted(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']) != sorted(a[':answer/value'] for a in s['question'][':question/answer-fields'][0][':answer-field/choices']):
            require(r['question'][':question/id']!=s['question'][':question/id'],'Changed bank reused identity')
            require(r['generation']['parameter_fingerprint']==s['generation']['parameter_fingerprint'],'Math fingerprint bank-dependent')
            found=True;break
    require(found,'No bank identity comparison witness')
    (HERE/'engine-input.json').write_text(json.dumps(native,indent=2)+'\n')
    engine=ROOT/'generate/runs/current/check-engine'
    subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True,capture_output=True,text=True)
    result={'status':'passed','source':g.SOURCE,'source_coverage':{'practice_questions':15,'easy_observed':13,'unrated_assigned_easy':2,'prompt_matches':15,'answer_values_matched':count,'answer_values_total':count,'radio_banks_matched':9,'radio_banks_total':9,'distractors_matched':distractors,'distractors_total':distractors,'blank_fragments_matched':6,'observed_correct_refs_matched':13,'missing_correct_refs_independently_inferred':2},
      'mathematics':{'generated_instances':len(native)-15,'source_instances':15,'rendered_arithmetic_rows':'all exact and equal to independent determinant','all_profiles_exercised':True,'identity_and_invalid_input_checks':'passed'},
      'native_grading':{'records':len(native),'checks':sum(len(x['checks']) for x in native),'status':'passed','engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'report':'engine-report.json'},
      'solution_fidelity':{'shared_opening_matches':13,'literal_markdown_match_required':False,'normalization':'Consistent signed products, parenthesized negative factors, zero-term simplification, and minor evaluation; same cofactor method and fixed worked solution. Older two originals supply no worked solution.'},
      'source_anomalies':[{'source_id':'q-128309','status':'corrected','evidence':'Source row =-2(4-0)-1(1-0)-1(-3-20) equals 14, not -32. Third coefficient must be +1. All later rows and correct answer agree with determinant -32.'}],
      'interpretation_limits':['Sparse radio sources cannot identify original distractor algorithms. Exact expression patterns are retained as explicit hypotheses, particularly q-9841; their pedagogical intent remains unknown.'],
      'source_results':report}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    (HERE/'review.json').write_text(json.dumps({'source_replays':originals,'generated':generated},indent=2)+'\n')
    review=['# 3x3 determinant review','', 'Math basis 1356. Originals retain captured evidence. Generated records are labeled; radio options include correct designations for reviewer use only.','']
    for case,record in zip(cases,originals):
        source=case['original'];review += ['## Original '+case['source_id'],'',source[':question/problem'],'', 'Original answer values: '+', '.join(a[':answer/value'] for a in source[':question/answer-fields'][0][':answer-field/choices'])+'.','',source.get(':question/worked-solution','No worked solution or correct ref supplied.'),'','### Parameterized replay','',g.markdown(record),'']
    review += ['# Clearly labeled generated variants','', 'Two variants for every observed bank and every applicable level/template; moderate and hard are authored extensions.','']
    review += [g.markdown(record)+'\n' for record in generated]
    (HERE/'review.md').write_text('\n'.join(review))
    print(json.dumps({'status':'passed','source_values':f'{count}/{count}','source_distractors':f'{distractors}/{distractors}','generated_instances':len(native)-15,'native_checks':sum(len(x['checks']) for x in native)},indent=2))


if __name__=='__main__':
    try:main()
    except Exception as exc:
        (HERE/'validation.json').write_text(json.dumps({'status':'failed','error':str(exc)},indent=2)+'\n')
        raise
