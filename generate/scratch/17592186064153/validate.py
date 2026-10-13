#!/usr/bin/env python3
"""Fail on bank/source/semantic/display/identity/native-grading regressions.

Semantic audit reads the actual prompt's derivative/slope and actual options.
It does not use generation parameters to infer the displayed correct answer.
Fidelity uses exact full text, not only correct IDs. Known raw source defects
are reported separately; supplied missing key/solution never count as observed.
"""
import importlib.util,json,re,hashlib,subprocess,uuid
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('generator',ROOT.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def write(name,value):
    (ROOT/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')

def number(tex):
    tex=tex.replace(r'\,','').rstrip('.')
    match=re.fullmatch(r'\\frac\{(-?\d+)\}\{(\d+)\}',tex)
    return sp.Rational(int(match[1]),int(match[2])) if match else sp.Rational(tex)

def numbers(text):
    values=[]
    for math in re.findall(r'\$([^$]+)\$',text):
        try: values.append(number(math.removesuffix('m')))
        except (TypeError,ValueError): pass
    return values

def printed_task(q):
    prompt=q[':question/problem']; simple=prompt.replace('{','').replace('}','')
    if 'slope of the tangent' in prompt:
        match=re.search(r'at \$[tv]=(\d+)\$ is equal to \$(-?[\d.]+)',prompt)
        assert match,('bad slope',prompt)
        t,r=int(match[1]),number(match[2])
    else:
        match=re.search(r"[UWSTBxPV](?:\^′|')\((\d+)\)\s*=\s*(-?[\d.]+(?:\\,\d+)*)",simple)
        assert match,('bad derivative',prompt)
        t,r=int(match[1]),number(match[2])
    if 'lemonade' in prompt: context='price'; units='cents per liter'; scale=100
    elif 'in thousands' in prompt: context='visitors';units='visitors per hour';scale=1000
    elif 'sheet of ice' in prompt:context='ice';units='squared centimeters per minute';scale=1
    elif 'cup of tea' in prompt:context='temperature';units='degrees Celsius per minute';scale=1
    elif "school's budget" in prompt:context='budget';units='dollars per student';scale=1
    elif 'Sam' in prompt:context='walking';units='meters per day';scale=1
    elif 'car' in prompt:context='car';units='meters per second';scale=1
    else:context='app';units='users per hour';scale=1
    return t,r,context,units,scale

def implied(choice,task):
    t,r,context,units,scale=task
    if any(word in choice for word in ('constant','constantly','total','increased by','decreased by')):
        return False
    if 'at a rate of' not in choice or units not in choice: return False
    if context=='price' and not choice.startswith('When $') or context=='price' and 'liters of lemonade are sold' not in choice:
        return False
    nums=numbers(choice)
    if nums!=[sp.Integer(t),abs(r)*scale]:return False
    positive=bool(re.search(r'\b(increased|increases|increasing)\b',choice))
    negative=bool(re.search(r'\b(decreased|decreases|decreasing)\b',choice))
    return (positive and not negative) if r>0 else (negative and not positive)

def balanced(text):
    assert text.count('$')%2==0,'unbalanced math delimiter'
    depth=0
    for character in text:
        if character=='{':depth+=1
        elif character=='}':depth-=1
        assert depth>=0,'unbalanced TeX brace'
    assert depth==0,'unbalanced TeX brace'
    assert '--' not in text and '+-' not in text

def audit_option_numbers(choice,task,profile):
    """Independently check all numeric recipe components in displayed prose."""
    t,r,context,units,scale=task; m=abs(r)*scale
    expected=[sp.Integer(t),m]
    if context=='app':
        if 'constant rate' in choice:expected=[r/t]
        elif 'increased by' in choice:expected=[m,sp.Integer(t)]
    elif context=='car':
        if 'constant rate' in choice:expected=[t/r if profile=='observed' else r/t]
        elif 'increased by' in choice:expected=[m,sp.Integer(t)]
        elif profile=='authored' and 'at a rate of' in choice and numbers(choice)[-1]!=m:
            expected=[sp.Integer(t),sp.Integer(t)]
    elif context=='walking':
        if 'constant rate' in choice:expected=[sp.Integer(t),r/t]
        elif 'walked a distance' in choice or 'increased by' in choice:expected=[m,sp.Integer(t)]
    elif context=='price':
        if 'When the price' in choice:expected=[m,sp.Integer(t)]
    elif context=='visitors':
        if 'constant rate' in choice:expected=[sp.Integer(t),m/t]
    elif context=='ice':
        if 'observation began' in choice or f'${g.num(m)}$ minutes' in choice and 'area of the sheet is' in choice:
            expected=[m,sp.Integer(t)]
    elif context=='budget':
        if 'constant rate' in choice:expected=[r/t]
        elif 'budget increased by' in choice:expected=[m,sp.Integer(t)]
    assert numbers(choice)==expected,('wrong displayed recipe value',choice,numbers(choice),expected)

def audit(record):
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    q=record['question']; uuid.UUID(q[':question/id'])
    field=q[':question/answer-fields'][0]
    uuid.UUID(field[':answer-field/id'])
    assert field[':answer-field/type']==':answer-field.type/radio'
    assert field[':answer-field/key']=='selection'
    assert len(q[':question/answer-fields'])==1
    values=field[':answer-field/choices'];assert len(values)==5
    assert len({a[':answer/id'] for a in values})==5
    assert len({a[':answer/value'] for a in values})==5
    for a in values:
        uuid.UUID(a[':answer/id'])
        assert a[':answer/type']==':answer.type/text'
        assert a[':answer/id']==str(uuid.uuid5(uuid.UUID(field[':answer-field/id']),a[':answer/value']))
    assert field[':answer-field/correct'][0]==':answer/id'
    correct=field[':answer-field/correct'][1]
    task=printed_task(q)
    if task[2]=='visitors' and task[1]<0:
        assert 'visitors currently on' in q[':question/problem'],'negative visitors count lacks stock-domain clarification'
    if record['generation']['bank_profile']=='authored' and task[2]=='car':
        assert not any('decreas' in a[':answer/value'] for a in values),'negative cumulative-distance option'
    inferred=[a[':answer/id'] for a in values if implied(a[':answer/value'],task)]
    assert inferred==[correct],('wrong displayed bank/key',q,task,inferred)
    for a in values:audit_option_numbers(a[':answer/value'],task,record['generation']['bank_profile'])
    for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for a in values]:balanced(text)
    # Verify every explicit derivative equality in the worked solution agrees
    # with the actual statement in the prompt (including tangent-to-derivative).
    simple=q[':question/worked-solution'].replace('{','').replace('}','')
    matches=re.findall(r"[UWSTBxPV](?:\^′|')\((\d+)\)\s*=\s*(-?[\d.]+(?:\\,\d+)*)",simple)
    assert matches,'solution omitted derivative/slope conversion'
    assert all(int(t)==task[0] and number(r)==task[1] for t,r in matches)
    final=q[':question/worked-solution'].split('*')[-2].strip()
    assert implied(final,task),('wrong printed solution',final,task)
    if record['generation']['bank_profile']=='authored' and task[2]=='ice':
        assert 'is changing $t$' in q[':question/worked-solution']
    return task

def engine_case(record,label):
    f=record['question'][':question/answer-fields'][0]; correct=f[':answer-field/correct'][1]
    return {'label':label,'record':record,'checks':[{'submitted_answer_id':a[':answer/id'],
       'expected':'accepted' if a[':answer/id']==correct else 'rejected',
       'purpose':'native radio ownership and correct designation'} for a in f[':answer-field/choices']]}

def main():
    capture=json.loads((ROOT/'source.json').read_text());sources=capture['record'][':knowledge-point/questions']
    cases=[{'source_id':'q-48571','template':'app','level':'easy','parameters':{'input':4,'rate':'650'},'bank_profile':'observed'},
       {'source_id':'q-48615','template':'walking','level':'easy','parameters':{'input':3,'rate':'120'},'bank_profile':'observed','authored_level':True,'correct_ref':'missing; independently derived'},
       {'source_id':'q-112091','template':'ice','level':'hard','parameters':{'input':5,'rate':'-7'},'bank_profile':'observed'},
       {'source_id':'q-48688','template':'car','level':'moderate','parameters':{'input':30,'rate':'10'},'bank_profile':'observed'},
       {'source_id':'q-48691','template':'price','level':'moderate','parameters':{'input':4,'rate':'1/2'},'bank_profile':'observed'},
       {'source_id':'q-48709','template':'visitors','level':'moderate','parameters':{'input':10,'rate':'3/2'},'bank_profile':'observed'}]
    write('source-cases.json',cases)
    fidelity=[];engine=[];reviews=[];observed=[]
    for case,source in zip(cases,sources):
        assert case['source_id']==source[':question/math-academy-id']
        r=g.generate(case['level'],17,case['template'],parameters=case['parameters'],profile='observed');audit(r)
        q=r['question'];f=q[':question/answer-fields'][0];sf=source[':question/answer-fields'][0]
        assert q[':question/problem']==source[':question/problem'],case
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices']),case
        assert f[':answer-field/key']==sf[':answer-field/key']
        if ':question/worked-solution' in source:assert q[':question/worked-solution']==source[':question/worked-solution'],case
        if ':answer-field/correct' in sf:
            generated_correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
            assert generated_correct==sf[':answer-field/correct'][':answer/value']
        fidelity.append({'source_id':case['source_id'],'prompt':'exact','options':5,'bank':'exact','correct_designation':'matched' if ':answer-field/correct' in sf else 'absent; supported authored key',
          'worked_solution':'exact' if ':question/worked-solution' in source else 'absent; authored solution','raw_teaching_defect':'global decrease preamble' if case['template']=='ice' else None})
        observed.append({'source':source,'generated_replay':r});engine.append(engine_case(r,case['source_id']))
    # Substantial random coverage at each level and every template/profile.
    coverage={};unique={level:set() for level in ('easy','moderate','hard')};record_count=0
    for template,level in g.TEMPLATES.items():
        for profile in (['authored','observed'] if template in g.OBSERVED else ['authored']):
            for seed in range(80):
                r=g.generate(level,seed,template,profile=profile);audit(r);record_count+=1
                unique[level].add(r['generation']['mathematical_fingerprint'])
                p=r['generation']['parameters']
                replay=g.generate(level,seed+100,template,parameters=p,profile=profile)
                assert r['question'][':question/id']==replay['question'][':question/id']
                assert r['generation']['content_hash']==replay['generation']['content_hash']
                if seed<2:
                    reviews.append({'label':'generated variant','template':template,'profile':profile,'record':r})
                    engine.append(engine_case(r,f'{template}/{profile}/{seed}'))
            coverage[f'{template}/{profile}']=80
    # Boundary and invalid explicit inputs cannot bypass scope guards.
    for template,level in g.TEMPLATES.items():
        for t in (2,60):
            rate='1/10' if template in ('price','visitors','signed_visitors') else '3'
            if level=='hard':rate='-'+rate
            r=g.generate(level,0,template,parameters={'input':t,'rate':rate});audit(r)
        for bad in ({'input':-1,'rate':'10'},{'input':True,'rate':'10'},{'input':3,'rate':'0'},
                    {'input':3,'rate':'-1' if level!='hard' else '1'}, {'input':61,'rate':'10'}):
            try:g.generate(level,0,template,parameters=bad)
            except ValueError:pass
            else:raise AssertionError(('invalid parameters accepted',template,bad))
    try:g.generate_hard(0,'ice',parameters={'input':7,'rate':'-7'})
    except ValueError:pass
    else:raise AssertionError('duplicate whole ice bank accepted')
    try:g.generate_moderate(0,'car',parameters={'input':10,'rate':'10'})
    except ValueError:pass
    else:raise AssertionError('duplicate authored car bank accepted')
    # Same context interpretation may have different displayed banks; identities
    # differ but mathematical fingerprint must agree. Profile alias with identical
    # rendered content must not itself create a content identity.
    normal=g.generate_moderate(0,'car',parameters={'input':30,'rate':'10'})
    raw=g.generate_moderate(0,'car',parameters={'input':30,'rate':'10'},profile='observed')
    assert normal['generation']['mathematical_fingerprint']==raw['generation']['mathematical_fingerprint']
    assert normal['question'][':question/id']!=raw['question'][':question/id']
    app=g.generate_easy(0,'app',parameters={'input':4,'rate':'650'})
    assert app['question'][':question/id']==g.generate_easy(12,'app',parameters={'input':4,'rate':'650'},profile='observed')['question'][':question/id']
    positions={next(i for i,a in enumerate(g.generate_easy(s,'app',parameters={'input':4,'rate':'650'})['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==app['question'][':question/answer-fields'][0][':answer-field/correct'][1]) for s in range(50)}
    assert positions==set(range(5))
    # Deliberately corrupt the displayed magnitude while retaining metadata/key.
    corrupt=json.loads(json.dumps(app));cf=corrupt['question'][':question/answer-fields'][0]
    for a in cf[':answer-field/choices']:
        if a[':answer/id']==cf[':answer-field/correct'][1]:a[':answer/value']=a[':answer/value'].replace('650','651')
    try:audit(corrupt)
    except AssertionError:pass
    else:raise AssertionError('displayed wrong magnitude escaped audit')
    write('source-bank-fidelity.json',fidelity);write('review.json',reviews);write('engine-input.json',engine)
    subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-validation.json')],check=True)
    report={'status':'passed','database':'math','basis':1356,'lineage':capture['lineage'],'database_writes':0,
       'source_coverage':{'practice_questions':6,'replayed':6,'exact_prompts':6,'complete_banks':6,'all_options':30,
            'wrong_options':24,'matched_correct_designations':5,'available_correct_designations':5,'missing_correct_designations':1,
            'raw_exact_worked_solutions':5,'available_worked_solutions':5,'missing_worked_solutions':1,
            'raw_solution_teaching_defects':1,'normal_solution_repairs':1},
       'correctness':{'displayed_prompt_and_choice_semantics':'passed','all_displayed_choice_recipe_numbers':'passed','solution_equations_and_local_conclusions':'passed',
         'mutation_detection':'passed','formatting':'passed','stable_identity':'passed','shuffling':'passed',
         'explicit_scope_bounds':'passed','whole_bank_rejection':'passed','native_grading':'passed'},
       'generated_records_checked':record_count,'sampler_coverage':coverage,'distinct_task_samples':{k:len(v) for k,v in unique.items()},
       'native_records':len(engine),'native_checks':len(engine)*5,
       'anomalies':['q-48615 missing key/solution/difficulty; supported authored key, solution, easy level',
                    'q-48615 observed day-index/elapsed wording differs; authored on-day clarification',
                    'q-48688 scalar constant-rate distractor has ambiguous intent; explicit t/r replay vs authored r/t; authored positive input-as-rate replaces impossible cumulative-distance decrease',
                    'q-112091 global decrease preamble retained raw, corrected to changing in authored profile'],
       'plot_rating':'none','authored_templates':['budget','temperature','signed_visitors'],
       'engine_sha256':hashlib.sha256((REPO/'generate/runs/current/check-engine').read_bytes()).hexdigest()}
    write('validation.json',report)
    text=['# Review: interpreting a supplied contextual derivative','', 'Raw originals and parameterized replays below retain source defects explicitly. Generated variants are labelled by bank profile. Correct refs remain author-only metadata.','']
    for item in observed:
        s=item['source'];text+=['## Original '+s[':question/math-academy-id'],s[':question/problem'],'',*[f'- {a[":answer/value"]}' for a in s[':question/answer-fields'][0][':answer-field/choices']],'',s.get(':question/worked-solution','No original worked solution or correct designation captured.'),'','### Observed parameterized replay',g.markdown(item['generated_replay']),'']
    for item in reviews:text+=['## Generated variant: '+item['template']+' / '+item['profile'],g.markdown(item['record']),'']
    (ROOT/'review.md').write_text('\n'.join(text)+'\n')
    hashes={str(path.relative_to(REPO)):hashlib.sha256(path.read_bytes()).hexdigest() for path in [ROOT.with_suffix('.py'),*sorted(ROOT.iterdir())] if path.is_file() and path.name!='frozen-hashes.json'}
    write('frozen-hashes.json',{'version':g.VERSION,'files':hashes})
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
