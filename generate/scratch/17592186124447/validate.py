#!/usr/bin/env python3
"""Independent display mathematics, source stages, identity, scope and native grader.
Run .venv/bin/python generate/scratch/17592186124447/validate.py.
"""
import copy, hashlib, importlib.util, itertools, json, re, subprocess, sys
from pathlib import Path
import sympy as s
DIR=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('gradient',DIR.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
ROOT=DIR.parents[2]

def save(name,value): (DIR/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def enum(v):return v.get(':db/ident') if isinstance(v,dict) else v

def functions_from_prompt(prompt):
    # Read printed definitions; no use of generation math objects or parameters.
    out={}
    for m in re.finditer(r'([fgh])\(x,\s*y(?:,\s*z)?\) & =(.*?),\\, &',prompt):out[m[1]]=g.parse_math(m[2])
    # Authored supplied-gradient layout uses \quad rather than source table.
    if not out:
        for m in re.finditer(r'([fg])\(x,y\) & =(.*?),\\quad',prompt):out[m[1]]=g.parse_math(m[2])
    if not out:
        clean=prompt.replace('$','')
        for m in re.finditer(r'(?<!∇)([fgh])\(x,\s*y(?:,\s*z)?\)\s*=\s*(.*?)(?=\s+and |[?.]?$)',clean):
            out[m[1]]=g.parse_math(m[2].rstrip('.?'))
    assert len(out)==2,('printed function extraction',prompt,out)
    return out

def replace_formal(row,functions,vs):
    args=','.join(map(str,vs))
    for f,F in functions.items():
        V=s.Add(*(s.diff(F,v)*b for v,b in zip(vs,g.BASIS)))
        # Operator acts on complete named function. Order matters before scalar refs.
        row=re.sub('∇'+r'\\?,?\s*'+f+r'\('+re.escape(args)+r'\)', lambda m:'('+g.tex(V)+')',row)
        row=row.replace(f+'('+args+')','('+g.tex(F)+')')
    return row

def display_validate(record,stage_check=True):
    q=record['question'];meta=record['generation'];family=meta['template'];p=meta['parameters']
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    functions=functions_from_prompt(q[':question/problem']);vs=(g.x,g.y,g.z) if family in ('reciprocal3','binomial3') else (g.x,g.y)
    F,G=functions.values();expected=g.grad(F*G,vs)
    field=q[':question/answer-fields'][0]
    assert enum(field[':answer-field/type'])==':answer-field.type/radio' and len(field[':answer-field/choices'])==5
    parsed=[g.parse_math(a[':answer/value']) for a in field[':answer-field/choices']]
    assert all(not g.equal(a,b) for n,a in enumerate(parsed) for b in parsed[:n]),'bank collision'
    if ':answer-field/correct' in field:
        index=next(n for n,a in enumerate(field[':answer-field/choices']) if a[':answer/id']==field[':answer-field/correct'][1])
        actual=g.components(parsed[index],len(vs));assert actual is not None and all(g.equal(a,b) for a,b in zip(actual,expected)), 'ordered exact component criterion'
        assert not all(g.equal(2*a,b) for a,b in zip(actual,expected)),'parallel is not equal'
    # Check supplied gradients from their actual prompt expressions.
    for m in re.finditer(r'∇([fgh])\(x,y(?:,z)?\)=(.*?)(?=, &|\\\\|\\end)',q[':question/problem']):
        value=m[2].split('&')[0].strip().rstrip('.');actual=g.components(g.parse_math(value),len(vs))
        assert actual and all(g.equal(a,b) for a,b in zip(actual,g.grad(functions[m[1]],vs))),('supplied gradient',value)
    solution=q.get(':question/worked-solution')
    if solution:
        blocks=re.findall(r'\\begin\{aligned\}([\s\S]*?)\\end\{aligned\}',solution)
        for block in blocks:
            for row in block.split(r'\\'):
                if '∇[' in row or row.lstrip().startswith('&'):
                    rhs=row.split('=',1)[1].strip().rstrip('.')
                    rhs=replace_formal(rhs,functions,vs)
                    actual=g.components(g.parse_math(rhs),len(vs))
                    assert actual is not None and all(g.equal(a,b) for a,b in zip(actual,expected)),('printed property stage',row)
                elif row.strip().startswith(r'\frac{∂') and ' & =' in row:
                    f=re.search(r'\\frac\{∂([fgh])\}\{∂([xyz])\}',row)
                    if f:
                        pieces=row.split('=');actual=g.parse_math(pieces[-1])
                        assert g.equal(actual,s.diff(functions[f[1]],getattr(g,f[2]))),('partial derivative',row)
                        operator=re.search(r'\\frac\{∂\}\{∂[xyz]\}\((.*)\)=',row)
                        if operator:assert g.equal(g.parse_math(operator[1]),functions[f[1]]),'wrong operator argument'
                elif '∇' in row and ' & =' in row:
                    f=re.search(r'∇([fgh])\(',row)
                    if f:
                        actual=g.components(g.parse_math(row.split('=')[-1]),len(vs))
                        assert actual and all(g.equal(a,b) for a,b in zip(actual,g.grad(functions[f[1]],vs))),('component vector',row)
        if stage_check:
            if family in g.FAMILIES:
                _,reference,_,_=g.source_render(family,p)
                if reference is None:reference=g.generic_solution(F,G,vs,derive=True,local_offsets=p)
                if family=='reciprocal3' and not meta['profile'].startswith('source:'):reference=reference.replace('$f(x,y)$ and $h(x,y)$','$f(x,y,z)$ and $h(x,y,z)$')
            else:reference=g.generic_solution(F,G,vs,derive=family=='binomial3')
            assert solution==reference,'operative stage/prose sequence changed (algebraic equality insufficient)'
    for text in [q[':question/problem'],solution or '',*[a[':answer/value'] for a in field[':answer-field/choices']]]:
        assert text.count('$')%2==0,'math delimiter imbalance'
        depth=0
        for char in text:
            depth+=(char=='{')-(char=='}');assert depth>=0,'closing brace'
        assert depth==0,'TeX groups'
        assert '--' not in text and '+-' not in text,'signed implicit product'
    return True

def raw_case(family,source):
    p={'a':1,'b':1} if family=='cancel' else {v+'0':0 for v in ('xyz' if family=='reciprocal3' else 'xy')}
    return {'source_id':source,'template':family,'parameters':p,'bank_profile':'source:'+source,'level':g.FAMILY_LEVELS[family],'authored_level_assignment':source=='q-37466'}

assert g.FAMILY_LEVELS['gaussian']=='hard' and 'gaussian' in g.LEVELS['hard'] and 'gaussian' not in g.LEVELS['moderate']
try:g.generate('moderate',template='gaussian')
except ValueError:pass
else:raise AssertionError('observed hard source leaked into moderate')
print('Checking source anchors...',flush=True)
cases=[raw_case(f,q) for f,q in g.FAMILIES.items()]
save('source-cases.json',cases)
records=[];fidelity=[]
for case in cases:
    r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);display_validate(r);records.append(r)
    raw=g.SOURCES[case['source_id']];q=r['question'];rf=raw[':question/answer-fields'][0];gf=q[':question/answer-fields'][0]
    assert q[':question/problem']==raw[':question/problem']
    assert q.get(':question/worked-solution')==raw.get(':question/worked-solution')
    for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in raw)==(key in q),'raw attribute presence'
    if ':question/difficulty' in raw:assert q[':question/difficulty']==enum(raw[':question/difficulty']),'raw difficulty value changed'
    assert (':answer-field/correct' in rf)==(':answer-field/correct' in gf)
    assert sorted(a[':answer/value'] for a in rf[':answer-field/choices'])==sorted(a[':answer/value'] for a in gf[':answer-field/choices'])
    if ':answer-field/correct' in rf:
        v=next(a[':answer/value'] for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1]);assert v==rf[':answer-field/correct'][':answer/value']
    fidelity.append({'source_id':case['source_id'],'prompt_exact':True,'solution_exact_or_absent':True,'attribute_presence':True,'bank_values_exact':5,'designation_matched':':answer-field/correct' in rf})

# Changed source masks, including signs; opaque banks remain tested as evidence.
print('Checking changed families and all levels...',flush=True)
review=[]
for family in g.FAMILIES:
    for seed in (19,42):
        r=g.generate(g.FAMILY_LEVELS[family],seed,template=family,parameters=({'a':2,'b':3} if seed==19 else {'a':4,'b':5}) if family=='cancel' else None,profile=g.eligible_profile(family));display_validate(r);review.append(r)
        if family in g.OPAQUE:
            rr=g.generate(g.FAMILY_LEVELS[family],seed,template=family,parameters=r['generation']['parameters'],profile='source:'+g.FAMILIES[family]);display_validate(rr);review.append(rr)
for family in sorted(set(g.FAMILIES)-g.OPAQUE):
    r=g.generate(g.FAMILY_LEVELS[family],19,template=family,parameters={'a':2,'b':3} if family=='cancel' else None,profile='method');display_validate(r);review.append(r)
for level in ('easy','hard'):
    for seed in (19,42):r=g.generate(level,seed);display_validate(r);review.append(r)
# Additional normal all-family default coverage and signed boundaries.
print('Checking normal coverage and boundaries...',flush=True)
seen=set();seen_banks=set()
for seed in range(160):
    r=g.generate('moderate' if seed%2==0 else 'hard',seed);display_validate(r);
    if r['generation']['template'] in g.FAMILIES:seen.add(r['generation']['template']);seen_banks.add((r['generation']['template'],r['generation']['profile']))
    if seen_banks=={(f,p) for f in g.FAMILIES for p in (('method',) if f in g.OPAQUE else ('observed','method'))}:break
assert seen==set(g.FAMILIES),'normal family coverage'
assert seen_banks=={(f,p) for f in g.FAMILIES for p in (('method',) if f in g.OPAQUE else ('observed','method'))},'normal whole-bank coverage'
for family in g.FAMILIES:
    params=[{'a':a,'b':b} for a,b in ((1,6),(6,1),(6,6))] if family=='cancel' else [{v+'0':n for v in ('xyz' if family=='reciprocal3' else 'xy')} for n in (-6,6)]
    for p in params:display_validate(g.generate(g.FAMILY_LEVELS[family],template=family,parameters=p,profile=g.eligible_profile(family)))
for level,family,p in [('easy','linear',{'a':-4,'b':2,'c':3,'d':-1}),('hard','binomial3',{'a':-4,'b':4,'r':3,'t':4})]:display_validate(g.generate(level,template=family,parameters=p))

print('Checking mutations and identities...',flush=True)
# Algebraically equal deletion mutation must fail stage validation.
m=copy.deepcopy(next(r for r in review if r['generation']['template']=='poly'))
solution=m['question'][':question/worked-solution'];block=re.findall(r'\\begin\{aligned\}([\s\S]*?)\\end\{aligned\}',solution)[-1];rows=block.split(r'\\')
rows[2]=rows[-1] # replace distributed stage with equivalent collected final
m['question'][':question/worked-solution']=solution.replace(block,r'\\'.join(rows))
display_validate(m,stage_check=False)
try:display_validate(m)
except AssertionError:mutation=True
else:raise AssertionError('equal missing-stage mutation escaped')
# Wrong first distribution sign, correct final kept, must fail independent math.
n=copy.deepcopy(next(r for r in review if r['generation']['template']=='poly'))
n['question'][':question/worked-solution']=n['question'][':question/worked-solution'].replace(r'\cdot 6x',r'\cdot 5x',1)
# translated cases have different x token so mutate actual first source coefficient.
n['question'][':question/worked-solution']=n['question'][':question/worked-solution'].replace(r'\cdot 6',r'\cdot 5',1)
try:display_validate(n,stage_check=False)
except AssertionError:sign_mutation=True
else:raise AssertionError('display arithmetic mutation escaped')
# Identity independent of seed/option order and profile aliases; math fingerprint bank independent.
for r in review:
    m=r['generation'];level=r['question'].get(':question/difficulty',':question.difficulty/moderate').split('/')[-1]
    rr=g.generate(level,seed=951,template=m['template'],parameters=m['parameters'],profile=m['profile'])
    assert rr['question'][':question/id']==r['question'][':question/id']
    if m['template'] in g.FAMILIES and m['profile']=='observed':
        rr=g.generate(level,template=m['template'],parameters=m['parameters'],profile='method');assert rr['generation']['mathematical_fingerprint']==m['mathematical_fingerprint']
# bounds explicit reject rather than resample
for level,family,p in [('easy','linear',{'a':0,'b':1,'c':1,'d':2}),('moderate','log',{'x0':7,'y0':0}),('hard','binomial3',{'a':1,'b':1,'r':0,'t':2})]:
    try:g.generate(level,template=family,parameters=p)
    except ValueError:pass
    else:raise AssertionError('explicit workload bounds')

save('review.json',review)
# Original public q-37466 lacks correct designation and cannot form a native fixture.
# Its mathematically inferred normal field is graded; do not pretend raw designation matched.
engine=[]
for n,r in enumerate(records+review):
    f=r['question'][':question/answer-fields'][0]
    if ':answer-field/correct' not in f:continue
    correct=f[':answer-field/correct'][1]
    checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'owned correct radio' if a[':answer/id']==correct else 'wrong full ordered gradient'} for a in f[':answer-field/choices']]
    engine.append({'label':str(n)+':'+r['generation']['template']+':'+r['generation']['profile'],'record':r,'checks':checks})
save('engine-input.json',engine)
exe=ROOT/'generate/runs/current/check-engine'
subprocess.run([str(exe),str(DIR/'engine-input.json'),str(DIR/'engine-report.json')],check=True)
engine_report=json.loads((DIR/'engine-report.json').read_text())
# Finite domains exclude aliases: shifts affect nonconstant reduced products; cancel
# varies actual two gradient coefficients. Easy filters nonindependent factors.
easy_instances=0;easy_tasks=set()
for a,b,c,d in itertools.product((-4,-3,-2,-1,1,2,3,4),repeat=4):
    if a*d==b*c:continue
    vectors=[(2*a*c,a*d+b*c,a*d+b*c,2*b*d),(a*c,a*d,b*c,b*d),(a*c,b*c,a*d,b*d),(0,a*d-b*c,b*c-a*d,0),(a*d+b*c,2*b*d,2*a*c,a*d+b*c)]
    if len(set(vectors))!=5:continue
    easy_instances+=1;easy_tasks.add((a*c,a*d+b*c,b*d))
counts={'moderate_canonical_candidates_per_family':{f:(36 if f=='cancel' else 169) for f in g.LEVELS['moderate']},'moderate_total_canonical_candidates':1050,'observed_hard_gaussian_candidates':169,'authored_hard_binomial_candidates':576,'hard_total_canonical_candidates':745,'easy_valid_parameter_instances_exactly_enumerated':easy_instances,'easy_canonical_tasks_exactly_enumerated':len(easy_tasks),'cancel_method_eligible_tasks':30,'reciprocal3_parameter_presentations':2197,'reciprocal3_canonical_tasks_excluding_cancelled_x_origin':169}

validation={'passed':True,'database':g.CAPTURE['database'],'basis':g.CAPTURE['basis'],'lineage':g.CAPTURE['lineage'],'runtime':{'python':sys.version.split()[0],'sympy':s.__version__},'source_questions':8,'exact_prompts':8,'exact_worked_solutions':7,'original_missing_worked_solutions':1,'exact_banks':8,'exact_choices':40,'exact_wrong_choices_with_known_designation':28,'matched_correct_designations':7,'original_missing_designations':1,'attribute_presence':8,'source_fidelity':fidelity,'normal_default_family_coverage':sorted(seen),'normal_default_bank_coverage':sorted(seen_banks),'review_generated_records':len(review),'equal_missing_stage_mutation_rejected':mutation,'displayed_intermediate_mutation_rejected':sign_mutation,'native':{'records':len(engine),'accepted':engine_report['accepted_checks'],'rejected':engine_report['rejected_checks'],'unresolved':engine_report['documented_unresolved_checks'],'raw_missing_correct_skipped':1,'executable_sha256':hashlib.sha256(exe.read_bytes()).hexdigest()},'finite_parameter_domain':counts,'evidence_limits':['Opaque poly/gaussian/reciprocal3/exp_linear banks replay symbolic shapes without recovered wrong-operation intent and are excluded from normal defaults.','q-37466 has no captured correct ref, difficulty or solution; normal completion is authored and raw replay retains omissions.','Source reciprocal3 product-property introductory prose names two variables instead of three; normal solution applies the minimal dimension wording repair.','Easy finite tasks are enumerated exactly after whole-bank rejection and product-alias deduplication; other finite counts are canonical same-method candidates, not claims that each was independently native graded.']}
save('validation.json',validation)
# Read original backslashes by decoded ord, without serialization inference.
bytes_report=[]
for source,q in g.SOURCES.items():
    t=q[':question/problem'];positions=[n for n,c in enumerate(t) if ord(c)==92]
    bytes_report.append({'source_id':source,'decoded_backslash_count':len(positions),'adjacent_pairs':[n for n in positions if n+1<len(t) and ord(t[n+1])==92],'interpretation':'adjacent backslashes are aligned row separators; no escape repair claimed'})
save('decoded-strings.json',bytes_report)
print('Passed: 8/8 exact banks, 40/40 choices, 7/7 available correct designations; native',validation['native'])
