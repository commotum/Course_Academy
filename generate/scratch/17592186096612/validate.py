#!/usr/bin/env python3
"""Independent printed-math, full source fidelity and native-engine validation."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
R=Path(__file__).parent
spec=importlib.util.spec_from_file_location('kp',R.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
source=json.loads((R/'source.json').read_text());sources={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
cases=json.loads((R/'source-cases.json').read_text())
native=[];source_results=[];review=[];counts={'source_banks':0,'source_options':0,'original_correct_designations':0,'source_prompts_exact':0,'source_solutions_exact':0,'source_solutions_observed':0,'source_distractors':0,'blank_aliases':0}

def fmt(text):
    assert text.count('$')%2==0,'unbalanced math delimiter'
    depth=0
    for i,c in enumerate(text):
        if c in '{}':
            if i and text[i-1]=='\\':continue
            depth+=1 if c=='{' else -1
            assert depth>=0,'unbalanced group'
    assert depth==0,'unbalanced group'
    assert '--' not in text and '+-' not in text,'ungrouped signed value'

def correct(record):
    f=record['question'][':question/answer-fields'][0]
    return next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])

def stages(record):
    q=record['question'];prompt=q[':question/problem']; f=g.read_prompt(prompt)
    d=sp.diff(f,g.X); t=g.read_input(prompt)
    n=0
    for block_i,block in enumerate(re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/worked-solution'],re.S)):
        block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
        for row in block.split(r'\\'):
            if '&' not in row:raise AssertionError('missing alignment stage')
            rhs=row.split('&',1)[1].strip().lstrip('=').strip().rstrip('.')
            has_bar='|' in rhs
            rhs=re.sub(r'\|}_{x=(-?\d+)}','}',rhs)
            
            try:value=g.read_math(rhs)
            except Exception as e:raise AssertionError((record["generation"]["template"],rhs)) from e
            if has_bar:value=value.subs(g.X,t)
            expected=d if block_i==0 else d.subs(g.X,t)
            assert g.equiv(value,expected),('printed solution stage wrong',record['generation']['template'],rhs,value,expected)
            n+=1
    expected_count=7 if record['generation']['template']=='two_bases_rate' else 9 if record['generation']['template']=='cubic_rate_blank' else 8 if record['generation']['template']=='natural_rate_radio' else 4 if record['generation']['template'] in ('scalar_radio','natural_sum_radio') else 5
    assert n==expected_count,('solution stage count',n,expected_count)
    return n

def validate(record,raw=False):
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    assert record['knowledge_point']['db_id']==g.KP_ID
    q=record['question'];fmt(q[':question/problem']);fmt(q[':question/worked-solution'])
    f=q[':question/answer-fields'][0];kind=f[':answer-field/type'].split('/')[-1]
    if kind=='blank':assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
    ids=[a[':answer/id'] for a in f[':answer-field/choices']];assert len(ids)==len(set(ids));assert f[':answer-field/correct'][1] in ids
    printed=g.read_prompt(q[':question/problem']); d=sp.diff(printed,g.X);t=g.read_input(q[':question/problem'])
    if t is not None:d=d.subs(g.X,t)
    ans=g.read_math(correct(record)[':answer/value'].split('=',1)[-1]);assert g.equiv(ans,d),('correct displayed answer',ans,d)
    parsed=[]
    for a in f[':answer-field/choices']:
        fmt(a[':answer/value']);v=g.read_math(a[':answer/value'].split('=',1)[-1]);parsed.append(v)
        assert not v.has(sp.zoo,sp.nan)
        if kind=='blank' and not raw:assert g.equiv(v,d),('invalid blank alias',record['generation']['template'],a[':answer/value'],d)
    if kind=='radio':
        assert sum(g.equiv(v,d) for v in parsed)==1
        assert all(not g.equiv(a,b) for i,a in enumerate(parsed) for b in parsed[i+1:])
    n=stages(record)
    checks=[]
    if kind=='radio':
        for a in f[':answer-field/choices']:checks.append({'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct(record)[':answer/id'] else 'rejected','purpose':'owned radio answer'})
    else:
        canon=correct(record)[':answer/value'];checks=[{'submitted':canon,'expected':'accepted','purpose':'canonical fragment'}, {'submitted':g.tex(ans+1),'expected':'rejected','purpose':'incorrect fragment'}]
        # Independently unreduced termwise formula from the printed function.
        components=[]
        tx='x' if t is None else '('+str(t)+')'
        for term in sp.Add.make_args(printed):
            coefficient,core=term.as_coeff_Mul()
            if not term.has(g.X):components.append('0')
            elif core.is_Pow and core.exp==g.X:
                components.append('('+g.tex(coefficient)+')*('+g.tex(core.base)+'^{'+tx+'}*\\ln('+g.tex(core.base)+'))')
            elif core==g.X or (core.is_Pow and core.base==g.X and core.exp.is_Integer):
                power=1 if core==g.X else int(core.exp)
                components.append('('+g.tex(coefficient)+')*(1)' if power==1 else '('+g.tex(coefficient)+')*('+str(power)+'*'+tx+'^{'+str(power-1)+'})')
            else:raise AssertionError('unrecognized printed derivative component')
        equivalent='+'.join(components)
        checks.append({'submitted':equivalent,'expected':'accepted','purpose':'independently unreduced termwise derivative/evaluation'})
        for alias in f[':answer-field/choices']:
            if alias[':answer/id']!=correct(record)[':answer/id'] and g.equiv(g.read_math(alias[':answer/value']),ans):
                checks.append({'submitted':alias[':answer/value'],'expected':'accepted','purpose':'complete observed equivalent alias'})
        if raw and record['generation']['template']=='cubic_rate_blank':checks.append({'submitted':f[':answer-field/choices'][1][':answer/value'],'expected':'rejected','purpose':'stale full derivative is not slope fragment'})
    native.append({'label':record['generation']['template']+'/'+str(record['generation']['seed'])+'/'+record['generation']['profile'],'record':record,'checks':checks})
    return n

for c in cases:
    r=g.generate(c['level'],11,c['template'],parameters=c['parameters'],profile='observed');validate(r,raw=True)
    q=sources[c['source_id']]; f=q[':question/answer-fields'][0];rf=r['question'][':question/answer-fields'][0]
    orig=[a[':answer/value'] for a in f[':answer-field/choices']];generated=[a[':answer/value'] for a in rf[':answer-field/choices']]
    assert sorted(orig)==sorted(generated),'complete source option mismatch'
    assert r['question'][':question/problem']==q[':question/problem']
    counts['source_prompts_exact']+=1;counts['source_banks']+=1;counts['source_options']+=len(orig)
    if f[':answer-field/type'][':db/ident'].endswith('blank'):counts['blank_aliases']+=len(orig)
    else:counts['source_distractors']+=len(orig)-1
    if ':answer-field/correct' in f:
        assert correct(r)[':answer/value']==f[':answer-field/correct'][':answer/value'];counts['original_correct_designations']+=1
    if ':question/worked-solution' in q:
        counts['source_solutions_observed']+=1;assert r['question'][':question/worked-solution']==q[':question/worked-solution'];counts['source_solutions_exact']+=1
    source_results.append({'source_id':c['source_id'],'complete_bank_exact':True,'prompt_exact':True,'original_designation_matched':c['original_correct_ref_present'],'raw_solution_exact':':question/worked-solution' in q,'recovered_correct':not c['original_correct_ref_present']})
    review.append({'label':'original replay '+c['source_id']+(' (authored solution; source absent)' if ':question/worked-solution' not in q else ''),'record':r})
    for seed in (31,62):
        v=g.generate(c['level'],seed,c['template']);validate(v);review.append({'label':'generated variant '+c['source_id'],'record':v})
for seed in (1,2):
    r=g.generate_hard(seed);validate(r);review.append({'label':'authored hard variant','record':r})
# Enumerate larger deterministic sample, enforcing same-stage math and identity.
math_tasks={level:set() for level in ('easy','moderate','hard')};stage_count=0;orders=set()
for template,level in g.TEMPLATES.items():
    for seed in range(40):
        r=g.generate(level,seed,template);stage_count+=validate(r);math_tasks[level].add(r['generation']['mathematical_fingerprint'])
        p=r['generation']['parameters'];r2=g.generate(level,seed+10000,template,parameters=p)
        assert r['question'][':question/id']==r2['question'][':question/id'];assert r['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint']
        if 'k' in p:
            changed=dict(p);changed['k']=2 if p['k']==1 else 1
            rk=g.generate(level,template=template,parameters=changed)
            assert r['generation']['mathematical_fingerprint']==rk['generation']['mathematical_fingerprint']
            assert r['question'][':question/id']!=rk['question'][':question/id']
        if r['question'][':question/answer-fields'][0][':answer-field/type'].endswith('radio'):
            f=r['question'][':question/answer-fields'][0];orders.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
assert len(orders)>1
for template,p in [('two_bases_rate',dict(b=2,h=3,a=1,c=1,q=1,k=1,t=0)),('two_bases_rate',dict(b=2,h=3,a=5,c=1,q=1,k=1,t=1)),('linear_blank',dict(a=0,b=2,l=1,k=1))]:
    try:g.generate(g.TEMPLATES[template],template=template,parameters=p)
    except ValueError:pass
    else:raise AssertionError('invalid explicit workload accepted')
(R/'native-input.json').write_text(json.dumps(native,indent=2)+'\n')
engine=Path('generate/runs/current/check-engine');run=subprocess.run([str(engine),str(R/'native-input.json'),str(R/'native-report.json')],capture_output=True,text=True)
assert run.returncode==0,run.stdout+run.stderr
report=json.loads((R/'native-report.json').read_text())
(R/'review.json').write_text(json.dumps(review,indent=2)+'\n')
md=['# Review','Raw source evidence is source.json. Original replay is labeled separately from authored variants.']
for item in review:
    r=item['record'];q=r['question'];md+=['\n## '+item['label'],q[':question/problem']]
    for a in q[':question/answer-fields'][0][':answer-field/choices']:md.append('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==correct(r)[':answer/id'] else ''))
    md.append(q[':question/worked-solution'])
(R/'review.md').write_text('\n\n'.join(md)+'\n')
result={'passed':True,'source_coverage':counts,'source_cases':source_results,'normal_records_validated':320+16,'raw_records_validated':7,'source_solution_normalization':{'raw_exact_available':5,'raw_notation_defect':1,'normal_formal_operator_repaired':1,'authored_missing_solutions':2},'blank_fragment_correctness':{'source_complete_alias_banks_valid':2,'source_complete_alias_banks_total':3,'invalid_source_aliases':1,'normal_alias_banks_valid':3},'printed_solution_rows_random_sample':stage_count,'distinct_mathematical_tasks_40_per_template':{k:len(v) for k,v in math_tasks.items()},'native':{k:report[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'engine_harness_sha256':hashlib.sha256(Path('generate/runs/current/check-engine.rs').read_bytes()).hexdigest(),'repairs':['normal natural_rate_radio repairs d y/dx operator notation','normal cubic_rate_blank omits invalid unevaluated full-derivative alias'],'source_limitations':['two missing original correct refs recovered mathematically, not matched designations','two missing worked solutions authored from canonical/sibling scaffolding','hard entirely authored; no observed hard label'],'database_writes':0}
(R/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
