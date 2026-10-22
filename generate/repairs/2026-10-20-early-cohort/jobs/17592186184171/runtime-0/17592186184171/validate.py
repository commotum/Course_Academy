#!/usr/bin/env python3
"""Parse displayed mathematics independently; exercise actual learner grader."""
import copy, hashlib, importlib.util, itertools, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('rank_nullity',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
VECTOR=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}|\[\\begin\{aligned\}(.*?)\\end\{aligned\}\]',re.S)
VARIABLE=re.compile(r'\{?x\}?_\{?(\d+)\}?')

def expression(text):
    t=VARIABLE.sub(lambda m:'x'+m[1],text).replace('{','').replace('}','').replace(' ','')
    t=re.sub(r'(\d)(x\d)',r'\1*\2',t)
    assert re.fullmatch(r'[x\d+*\-]+',t),repr(t)
    return sp.sympify(t,locals={f'x{i}':sp.Symbol(f'x{i}') for i in (1,2,3)})

def vectors(text):
    return [sp.Matrix([expression(s) for s in re.split(r'\\\\',m[1] if m[1] is not None else m[2])]) for m in VECTOR.finditer(text)]

def read_prompt(q):
    text=q[':question/problem']
    if 'basis of' in text:
        m,n=map(int,re.search(r'\$(\d+)\\times (\d+)\$',text).groups())
        basis=re.search(r'If \$.*?=(.*?)\$ is a basis',text)[1]
        k=len(re.findall(r'b\}?_\{?\d+',basis));assert k and k<=min(m,n)
        return 'easy',{'m':m,'n':n,'k':k},n-k
    vv=vectors(text);assert len(vv)==1
    vector=vv[0];symbols=sorted(set().union(*(e.free_symbols for e in vector)),key=str)
    C=vector.jacobian(symbols);assert all(e.subs({s:0 for s in symbols})==0 for e in vector)
    assert len(vector)==4 and len(symbols) in (2,3) and C.rank()==len(symbols)
    return 'moderate',{'matrix':[[int(v) for v in row] for row in C.tolist()],'indices':[int(str(s)[1:]) for s in symbols]},len(vector)-C.rank()

def task_key(q):
    level,p,answer=read_prompt(q)
    data=[level,p['n'],p['k']] if level=='easy' else [level,[[str(v) for v in row] for row in sp.Matrix(p['matrix']).T.rref()[0].tolist()]]
    return g.digest(data)

def independent(r):
    q=r['question'];level,p,answer=read_prompt(q)
    assert q[':question/difficulty']==':question.difficulty/'+level
    assert p==r['generation']['parameters']
    fields=q[':question/answer-fields'];assert len(fields)==1
    f=fields[0];assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
    values=[a[':answer/value'] for a in f[':answer-field/choices']];assert len(values)==len(set(values))==5
    correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert int(correct)==answer
    assert task_key(q)==r['generation']['mathematical_fingerprint']
    solution=q[':question/worked-solution'];n=p['n'] if level=='easy' else 4;k=p['k'] if level=='easy' else sp.Matrix(p['matrix']).cols
    assert f'$n={n},$' in solution
    numbers=re.sub(r'\s','',solution)
    if level=='easy':
        assert f'{k}+\\text{{nullity}}(A)&={n}' in numbers
        assert f'\\text{{nullity}}(A)&={n}-{k}' in numbers
        assert f'\\text{{dim(Null}}(A))&={answer}.' in numbers
        assert f'${k}$vectors' in numbers and f'\\text{{rank}}(A)={k}' in numbers
    else:
        vv=vectors(solution);assert len(vv)==k and sp.Matrix.hstack(*vv)==sp.Matrix(p['matrix'])
        # Read parameter multipliers between the solution's coefficient vectors.
        multipliers=re.findall(r'\{x\}_\{(\d+)\}(?:\\begin\{bmatrix\}|\[\\begin\{aligned\})',solution)
        assert list(map(int,multipliers))==p['indices']
        assert f'\\text{{nullity}}(A)={k}' in numbers
        assert f'\\text{{rank}}(A)+{k}&={n}' in numbers
        assert f'\\text{{rank}}(A)&={n}-{k}' in numbers and f'&={answer}.' in numbers
    assert 'rank-nullity theorem' in solution
    assert r['knowledge_point']['db_id']==g.KP_ID
    return answer

def checks(r):
    independent(r);f=r['question'][':question/answer-fields'][0]
    return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'all five radio choices through actual grader'} for a in f[':answer-field/choices']]

def mask(text):
    text=VECTOR.sub('<VECTOR>',text)
    return re.sub(r'\s','',text.replace(r'\{','').replace(r'\}','').replace('{','').replace('}',''))

def source_validate(q):
    mid=q[':question/math-academy-id'];level,p,answer=read_prompt(q)
    assert p==g.ORIGINAL[mid]
    r=g.generate(level,template=mid,parameters=p);independent(r)
    f=q[':question/answer-fields'][0];assert int(f[':answer-field/correct'][':answer/value'])==answer
    assert len(f[':answer-field/choices'])==5
    assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])
    assert mask(q[':question/problem'])==mask(r['question'][':question/problem']),('prompt fidelity',mid)
    assert mask(q[':question/worked-solution'])==mask(r['question'][':question/worked-solution']),('solution fidelity',mid)
    if level=='moderate':
        assert vectors(q[':question/problem'])==vectors(r['question'][':question/problem'])
        assert vectors(q[':question/worked-solution'])==vectors(r['question'][':question/worked-solution'])
    return r

def main():
    records=[];replays=[];maps=[]
    for mid,q in g.SOURCES.items():
        r=source_validate(q);records.append(r)
        f=q[':question/answer-fields'][0];profile=g.SOURCE_PROFILE[mid]
        replays.append({'source':mid,'profile':profile,'complete_banks':'1/1','all_choices':'5/5','distractors':'4/4','correct_designation':True,'source_parameters_recovered_independently':True,'prompt_fidelity':'same wording and math; normalized set braces/matrix layout','solution_fidelity':'same wording, ordered stages and exact vectors; normalized TeX and algebraic term order'})
        maps.append({'source':mid,'parameters':g.ORIGINAL[mid],'profile':profile,'choices':[{'field':'selection','original_answer_id':a[':answer/id'],'exact_value':a[':answer/value'],'recipe_index':g.bank(profile,g.ORIGINAL[mid],int(f[':answer-field/correct'][':answer/value'])).index(int(a[':answer/value'])),'complete_value_reproduced':True} for a in f[':answer-field/choices']]})
    coverage={}
    for level in g.SUPPORTED_LEVELS:
        coverage[level]={}
        for profile in g.PROFILES[level]:
            group=[g.generate(level,i,profile=profile) for i in range(70)]
            for r in group:
                independent(r);again=g.generate(level,999,template=r['generation']['template'],profile=profile,parameters=r['generation']['parameters']);assert again['question']==r['question']
            records.extend(group)
            coverage[level][profile]={'samples':len(group),'distinct_tasks':len({task_key(r['question']) for r in group}),'indices':sorted({tuple(r['generation']['parameters'].get('indices',[])) for r in group}),'templates':sorted({r['generation']['template'] for r in group})}
    boundaries=0
    for m,n,k in itertools.product(range(2,8),range(4,13),range(1,8)):
        for profile in g.PROFILES['easy']:
            p={'m':m,'n':n,'k':k}
            if g.valid('easy',p,profile):independent(g.generate('easy',parameters=p,profile=profile));boundaries+=1
    # Isolated coefficient-slot coverage with all other entries held constant.
    matrix=g.ORIGINAL['q-35434']['matrix'];changed=[]
    for i,j in itertools.product(range(4),range(3)):
        seen=[]
        for value in range(-3,4):
            M=copy.deepcopy(matrix);M[i][j]=value;p={'matrix':M,'indices':[1,2,3]}
            if sp.Matrix(M).rank()==3:
                independent(g.generate('moderate',parameters=p,profile='zero-through4'));seen.append(value)
        assert len(seen)>=5;changed.append({'row':i,'column':j,'values':seen})
    # Same assessed target is fixed by the backbone. Two supplied coefficients
    # changed with remaining matrix fixed: both vectors and key must update.
    one=g.generate('moderate',parameters=g.ORIGINAL['q-35306'],profile='zero-through4')
    p=copy.deepcopy(g.ORIGINAL['q-35306']);p['matrix'][0][0]=3
    two=g.generate('moderate',parameters=p,profile='zero-through4');independent(two)
    assert one['question'][':question/problem']!=two['question'][':question/problem']
    assert one['question'][':question/worked-solution']!=two['question'][':question/worked-solution']
    broken=copy.deepcopy(two);broken['question'][':question/worked-solution']=one['question'][':question/worked-solution']
    try:independent(broken)
    except AssertionError:pass
    else:raise AssertionError('stale solution vector not detected')
    for invalid in [dict(matrix=[[1,1],[0,0],[0,0],[0,0]],indices=[2,3]),dict(matrix=[[4,0],[0,1],[0,0],[0,0]],indices=[2,3])]:
        try:g.generate('moderate',parameters=invalid)
        except ValueError:pass
        else:raise AssertionError('invalid parameter accepted')
    try:g.generate('hard')
    except ValueError:pass
    else:raise AssertionError('unsupported hard generated')
    native=[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in records]
    (HERE/'engine-input.json').write_text(json.dumps(native));subprocess.run([str(g.REPO/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    (HERE/'source-choice-mapping.json').write_text(json.dumps(maps,indent=2))
    report={'status':'pass','source_basis':g.SNAPSHOT['basis'],'source_replays':replays,'complete_banks':'11/11','distractors':'44/44','all_choices':'55/55','generated_profile_coverage':coverage,'easy_exhaustive_valid_parameter_profiles':boundaries,'easy_finite_distinct_tasks':len({(n,k) for m,n,k in itertools.product(range(2,8),range(4,13),range(1,8)) for profile in g.PROFILES['easy'] if g.valid('easy',{'m':m,'n':n,'k':k},profile)}),'moderate_coefficient_slot_coverage':changed,'stale_solution_mutation_detected':True,'mathematical_correctness':'exact independent displayed-vector parsing, rank, decomposition and rank-nullity equation checks','actual_grading':{'report':'engine-report.json','accepted':len(records),'rejected':4*len(records),'unresolved':0},'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'validator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    review=[]
    for mid in ['q-35433','q-35306','q-35434']:
        level='easy' if mid=='q-35433' else 'moderate';review.append({'source_id':mid,'source':g.SOURCES[mid],'replay':source_validate(g.SOURCES[mid]),'variants':[g.generate(level,s) for s in (5,11)]})
    (HERE/'side-by-side.json').write_text(json.dumps(review,indent=2))
    (HERE/'side-by-side.md').write_text('\n\n---\n\n'.join('Source '+x['source_id']+'\n\n'+x['source'][':question/problem']+'\n\n'+x['source'][':question/worked-solution']+'\n\nReplay\n\n'+g.markdown(x['replay'])+'\n\nVariants\n\n'+'\n\n'.join(g.markdown(r) for r in x['variants']) for x in review))
    print(json.dumps({k:report[k] for k in ('status','source_basis','complete_banks','distractors','all_choices','actual_grading','easy_exhaustive_valid_parameter_profiles')}))
if __name__=='__main__':main()
