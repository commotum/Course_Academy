"""Fail-closed validation of displayed givens, formal stages, full banks,
immutable source fidelity, public APIs, content identity and frozen native grading.
No live generator, parser, formatter, EDB or shared QA imports.
"""
import copy
from functools import lru_cache
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import re
import subprocess
import sys
from mpmath import iv
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('private_84350',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
sp=g.sp;x=g.x;u=g.parser.u
iv.dps=40
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def clean(raw):return raw.replace('&','').replace(r'\,','').strip().rstrip('.,').strip()
def math(raw):return g.scalar(clean(raw))
def equal(a,b):return g.equal(a,b)
def blocks(text):return [s[2:-2] if s.startswith('$$') else s[1:-1] for s in re.findall(r'\$\$.*?\$\$|\$[^$]*\$',text,re.S)]
def exponent(prompt):
    # Independently extract the complete numeric-base exponent from actual text.
    match=re.search(r'\{?(\d+)\}?\^\{',prompt);assert match,prompt
    start=match.end();pos=start;depth=1
    while depth:
        depth+=(prompt[pos]=='{')-(prompt[pos]=='}');pos+=1
    return int(match[1]),math(prompt[start:pos-1])
def stage_derivative(raw,U):
    raw=clean(raw)
    if r'\int' not in raw:return sp.diff(math(raw).subs(u,U),x)
    assert raw.count(r'\int')==1,raw
    before,after=raw.split(r'\int');outside=math(before) if before.strip() else sp.Integer(1)
    m=re.search(r'\\(?:text|textrm)\{d\}([xu])',after)
    assert m and not clean(after[m.end():]),raw
    integrand=clean(after[:m.start()])
    if integrand.endswith(r'\cdot'):integrand=integrand[:-len(r'\cdot')]
    integrand=math(integrand)
    if m[1]=='u':return outside*integrand.subs(u,U)*sp.diff(U,x)
    return outside*integrand
def check_stages(record):
    q=record['question'];solution=q.get(':question/worked-solution')
    if solution is None:return {'raw_missing_solution':True}
    J=g.displayed_integrand(q[':question/problem']);base,U=exponent(q[':question/problem'])
    Bs=blocks(solution)
    introduction=next(b for b in Bs if b.startswith('u='));assert equal(math(introduction[2:]),U)
    differential=next(b for b in Bs if r'\frac{\text{d}u}{\text{d}x}' in b)
    prefix=r'\frac{\text{d}u}{\text{d}x}='
    assert differential.strip().startswith(prefix)
    derivative,relation=differential.strip()[len(prefix):].split('⟹')
    assert equal(math(derivative),sp.diff(U,x)),(derivative,U)
    left,right=relation.rstrip('.\n ').split('=')
    assert r'\text{d}u' in left and r'\text{d}x' in right
    left=clean(left.replace(r'\text{d}u',''));right=clean(right.replace(r'\text{d}x',''))
    L=math(left) if left else sp.Integer(1);R=math(right) if right else sp.Integer(1)
    assert equal(L*sp.diff(U,x),R),(L,U,R)
    aligned=next(b for b in Bs if r'\begin{aligned}' in b)
    body=aligned.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0]
    rows=[row.strip() for row in body.split(r'\\')]
    template=record['generation']['template']
    direct=template in ('q-73801','q-73800')
    assert len(rows)==(4 if direct else 5),(template,rows)
    parts=[]
    for index,row in enumerate(rows):
        assert row.count('=')==1,row
        left,right=row.replace('&','').split('=');parts.append(right)
        if index==0:
            assert equal(stage_derivative(left,U),J)
            assert r'\int' in right and r'\cdot' in right and r'\text{d}x' in right
        elif index==1:
            assert r'\int' in right and r'\cdot' in right and r'\text{d}u' in right
        elif not direct and index==2:
            assert r'\int' in right and r'\text{d}u' in right
            # Operative extraction stage: constant outside, never inside again.
            assert r'\cdot' not in right.split(r'\int',1)[1]
        elif index==len(rows)-2:
            assert r'\int' not in right and re.search(r'\^\{u\}',right) and '+C' in right
        else:
            assert index==len(rows)-1 and r'\int' not in right and 'x' in right and '+C' in right
        assert equal(stage_derivative(right,U),J),(template,index,right,stage_derivative(right,U),J)
    assert "Let's introduce the new variable $u=" in solution
    assert '.$ Differentiating gives' in solution and '\n\nTherefore,\n\n' in solution
    return {'formal_derivative':True,'differential_relation':True,'ordered_integral_rows':len(rows),'every_printed_row_checked':True}

def interval(expr):
    if expr.is_Rational:return iv.mpf(int(expr.p))/iv.mpf(int(expr.q))
    if expr.func==sp.Add:return sum((interval(v) for v in expr.args),iv.mpf(0))
    if expr.func==sp.Mul:
        value=iv.mpf(1)
        for term in expr.args:value*=interval(term)
        return value
    if expr.func==sp.Pow:return interval(expr.base)**interval(expr.exp)
    if expr.func==sp.log:return iv.ln(interval(expr.args[0]))
    raise AssertionError(('Unsupported interval expression',expr))
@lru_cache(maxsize=65536)
def nonzero(expr):
    for point in (sp.Integer(1),sp.Integer(0),sp.Rational(1,2),sp.Integer(2)):
        enclosure=interval(expr.subs(x,point))
        if enclosure.a>0 or enclosure.b<0:return True
    return False
def check(record):
    assert set(record['knowledge_point'])=={'db_id','id','title'} and record['knowledge_point']['db_id']==g.KP_ID
    q=record['question'];meta=record['generation'];f=q[':question/answer-fields'][0];bank=f[':answer-field/choices']
    assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection' and len(bank)==5
    assert len({a[':answer/id'] for a in bank})==5
    for value in (q[':question/problem'],q.get(':question/worked-solution',''),*[a[':answer/value'] for a in bank]):
        assert not any(ord(c)<32 and c not in '\n\t\r' for c in value)
    J=g.displayed_integrand(q[':question/problem']);base,U=exponent(q[':question/problem'])
    assert base in g.BASES and U.is_polynomial(x) and sp.degree(U,x) in (2,3,4)
    derivatives=[g.derivative_tex(a[':answer/value']) for a in bank]
    correct=[i for i,v in enumerate(derivatives) if equal(v,J)];assert len(correct)==1
    if ':answer-field/correct' in f:assert f[':answer-field/correct']==[':answer/id',bank[correct[0]][':answer/id']]
    else:assert meta['template']=='q-73800' and meta['evidence_only'] and not meta['eligible_for_learning']
    for i,v in enumerate(derivatives):
        if i not in correct:assert nonzero(v-J)
        for w in derivatives[i+1:]:assert nonzero(v-w),('Bank equality modulo C',v,w)
    for a in bank:
        assert a[':answer/type']==':answer.type/math' and '$' not in a[':answer/value']
        expression=math(a[':answer/value'])
        assert expression.is_real is True,(a[':answer/value'],'not proved globally real')
        assert expression.free_symbols <= {x,g.parser.locals_['C']}
        for point in (-2,-1,0,1,2):assert expression.subs(x,point).is_real is not False
    assert meta['mathematical_fingerprint']==g.mathematical_fingerprint(q[':question/problem'])
    assert meta['dependencies']['python']==sys.version.split()[0]
    g.fmt.validate_prose(q[':question/problem'])
    if ':question/worked-solution' in q:g.fmt.validate_prose(q[':question/worked-solution'])
    for a in bank:g.fmt.validate_tex(a[':answer/value'])
    return check_stages(record)

def native(label,record):
    f=record['question'][':question/answer-fields'][0]
    if ':answer-field/correct' not in f:return None
    checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned radio ID, independently mathematically verified'} for a in f[':answer-field/choices']]
    # Native structured errors are the correct input-contract behavior for
    # these non-choice submissions. They are not mathematical equivalence gaps.
    checks.extend({'submitted':text,'expected':'unresolved','purpose':purpose} for text,purpose in [(f[':answer-field/choices'][0][':answer/value'],'math text cannot stand in for owned radio ID'),('9999999','foreign ID does not belong to field'),('{not-an-id}','malformed choice ID')])
    return {'label':label,'record':record,'checks':checks}

def main():
    # Assert original registered implementation AND every preexisting byte/path.
    baseline=json.loads((HERE/'baseline.json').read_text());basepaths={r['path'] for r in baseline}
    registered=ROOT/'generate/scratch/17592186184350';actual={str(p.relative_to(ROOT)) for p in registered.rglob('*') if p.is_file()}|{'generate/scratch/17592186184350.py'}
    assert actual==basepaths,('Registered evidence path set changed',actual^basepaths)
    for row in baseline:assert digest(ROOT/row['path'])==row['sha256'],row['path']
    source=g.capture();assert source['basis']==2275
    original_source=ROOT/'generate/runs/current/refresh-2026-10-14/sources/17592186184350.json'
    assert (HERE/'source.json').read_bytes()==original_source.read_bytes()
    questions=source['record'][':knowledge-point/questions'];MA=[q for q in questions if ':question/math-academy-id' in q]
    independent=[{'record':q,'role':'independently authored inventory','relationship_to_source_templates':'Exact registered base-only transport of MA q-211989 rational cubic template and full observed bank; current inventory, not independent evidence of an original MA difficulty.'} for q in questions if ':question/math-academy-id' not in q]
    save('independent-inventory.json',{'database':source['database'],'basis':source['basis'],'lineage':source['lineage'],'questions':independent})
    # Follow actual lesson links rather than Pull array ordering.
    lesson=json.loads((HERE/'lesson.json').read_text());activity=lesson['record'][0];steps={r[':db/id']:r for r in activity[':activity/steps']};route=[];current=activity[':activity/first-step'][':db/id']
    while current is not None:
        row=steps[current];content=row[':step/content'];route.append({'step':current,'content_db_id':content[':db/id'],'title':content.get(':knowledge-point/title',content.get(':tutorial/title'))});current=row.get(':step/next',{}).get(':db/id')
    save('ordered-lesson-route.json',{'basis':lesson['basis'],'route':route})
    fidelity=[];cases=[];components=[];reviews=[];native_inputs=[];records=[];stage_results=[]
    for old in MA:
        t=old[':question/math-academy-id'];info=g.DATA[t];level=info['level'];params={'base':info['base']}
        case={'source_id':t,'source_question_uuid':old[':question/id'],'template':t,'parameters':params,'bank_profile':'observed-'+t,'profile':'observed-'+t,'level':level,'level_assignment':'authored API placement only; raw output omits rating' if t=='q-73800' else 'observed'};cases.append(case)
        record=g.generate(level,0,t,parameters=params,profile='observed-'+t);q=record['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
        assert q[':question/problem']==old[':question/problem']
        for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in old)==(key in q),(t,key)
        assert (':answer-field/correct' in of)==(':answer-field/correct' in f)
        if ':question/worked-solution' in old:assert q[':question/worked-solution']==old[':question/worked-solution']
        values=sorted(a[':answer/value'] for a in f[':answer-field/choices']);original_values=sorted(a[':answer/value'] for a in of[':answer-field/choices']);assert values==original_values
        if ':answer-field/correct' in of:
            actual=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert actual==of[':answer-field/correct'][':answer/value']
        check(record)
        changed=g.generate(level,1,t,parameters={'base':2 if info['base']!=2 else 3},profile='observed-'+t);check(changed)
        reviews.append({'kind':'observed original and changed-base evidence profile','template':t,'original_record':old,'original_replay':record,'generated_variant':changed})
        fidelity.append({'source_id':t,'complete_bank_matched':True,'values_matched':5,'distractors_matched':4 if t!='q-73800' else None,'correct_designation_matched':t!='q-73800','raw_omissions_preserved':True,'worked_solution_exact':True if t!='q-73800' else None})
        components.append({'source_id':t,'field':of[':answer-field/key'],'prompt':old[':question/problem'],'worked_solution':old.get(':question/worked-solution'),'choices':[{'source_answer_id':a[':answer/id'],'exact_value':a[':answer/value'],'recipe':g.base_transport(a[':answer/value'],info['base'],'b'),'profile':'observed-'+t,'interpretation':'Explicit parameterized expression transport. The original misconception operation is not recovered.','is_correct':a[':answer/id']==of.get(':answer-field/correct',{}).get(':answer/id') if ':answer-field/correct' in of else None} for a in of[':answer-field/choices']]})
        records.extend((record,changed))
    save('source-cases.json',cases);save('source-components.json',components);save('source-fidelity.json',{'sources':fidelity,'MA_questions':8,'complete_banks':8,'values':40,'distractors_with_original_designations':28,'original_designations':7,'worked_solutions':7,'unrated_missing_correct_solution':['q-73800']})
    completion=g.generate_easy(0,'q-73800',parameters={'base':3,'shift':-5})
    check(completion)
    save('normal-completion.json',{'source_id':'q-73800','raw_missing_attributes':[':question/difficulty',':question/worked-solution',':answer-field/correct'],'original_correct_designation_recovered':False,'mathematically_inferred_value':r'\frac{3^{x^{3}-5}}{\ln 3}+C','derivative_verified_against_displayed_integrand':True,'normal_authored_record':completion})
    # Exhaust finite supported domains for every raw profile and every normal
    # family, including shared mathematical tasks under distinct bank profiles.
    counts={};tasks={level:set() for level in g.LEVELS};family_tasks={};default_coverage=set()
    for t,domain in g.DOMAINS.items():
        level=g.DATA[t]['level'];family_tasks[t]=set();n=0
        for values in itertools.product(*domain.values()):
            params=dict(zip(domain,values));record=g.generate(level,17,t,parameters=params);stage=check(record);n+=1
            fp=record['generation']['mathematical_fingerprint'];tasks[level].add(fp);family_tasks[t].add(fp)
            records.append(record)
            if len(stage_results)<200:stage_results.append({'template':t,'parameters':params,**stage})
        counts[t]=n;print('Checked normal finite domain',t,n,flush=True)
    for t,info in g.DATA.items():
        if t=='negative-quartic':continue
        for base in g.BASES:
            record=g.generate(info['level'],31,t,parameters={'base':base},profile='observed');check(record);records.append(record)
        print('Checked complete observed-bank base domain',t,flush=True)
    # Normal solution fidelity at anchors is separate from raw evidence fidelity.
    normal_solution=[]
    for t,info in g.DATA.items():
        params={k:info[k] for k in g.DOMAINS[t]};record=g.generate(info['level'],0,t,parameters=params)
        if t not in ('negative-quartic','q-73800'):assert record['question'][':question/worked-solution']==g.sources()[t][':question/worked-solution'];normal_solution.append(t)
        for seed in (3,27):
            changed=g.generate(info['level'],seed,t);check(changed)
            reviews.append({'kind':'normal authored bank; source-shaped solution' if t not in ('negative-quartic','q-73800') else 'authored normal completion / missing-level extension','template':t,'generated_variant':changed});records.append(changed)
    for level in g.LEVELS:
        # API strictness and deterministic content identity under option shuffle.
        for seed in range(80):default_coverage.add(g.generate(level,seed)['generation']['template'])
        batch=g.batch(level,20,8);fps=[r['generation']['mathematical_fingerprint'] for r in batch];assert len(fps)==len(set(fps))
        again=g.batch(level,20,8);assert batch==again
        try:g.batch(level,len(tasks[level])+1,8)
        except ValueError:pass
        else:raise AssertionError('Finite task domain not enforced')
    assert default_coverage==set(g.DATA)
    for t,info in g.DATA.items():
        params={k:info[k] for k in g.DOMAINS[t]};a=g.generate(info['level'],0,t,parameters=params);b=g.generate(info['level'],998,t,parameters=params)
        assert a['question'][':question/id']==b['question'][':question/id']
        assert sorted(a['question'][':question/answer-fields'][0][':answer-field/choices'],key=str)==sorted(b['question'][':question/answer-fields'][0][':answer-field/choices'],key=str)
        for bad in ({},{'base':True},{**params,'base':1},{**params,'base':13},{**params,'extra':1},{**params,next(iter(params)):2.5}):
            try:g.generate(info['level'],template=t,parameters=bad)
            except ValueError:pass
            else:raise AssertionError(('Invalid explicit parameters accepted',t,bad))
    for kwargs in ({'seed':True},{'seed':1.5},{'profile':'unknown'},{'template':'unknown'},{'field_type':'blank'}):
        try:g.generate('easy',**kwargs)
        except ValueError:pass
        else:raise AssertionError(('Invalid API accepted',kwargs))
    # Independent display mutation regressions include a mathematically equal
    # row that erases the operative scalar extraction, plus actual wrong stages.
    anchor=g.generate_easy(0,'q-31420',parameters={'base':8,'a':3})
    mutations=[]
    for name,old,new in [('formal derivative','6x','7x'),('substituted factor',r'\frac{1}{6}\,\text{d}u',r'\frac{1}{5}\,\text{d}u'),('erased extraction',r'\frac{1}{6}\int {8}^{u}\,\text{d}u',r'\int {8}^{u}\cdot \frac{1}{6}\,\text{d}u'),('control character',r'\frac{1}{6}','\x0crac{1}{6}')]:
        mutant=copy.deepcopy(anchor);text=mutant['question'][':question/worked-solution'];assert old in text;mutant['question'][':question/worked-solution']=text.replace(old,new,1)
        try:check(mutant)
        except (AssertionError,ValueError):mutations.append(name)
        else:raise AssertionError(('Mutation not rejected',name))
    # Every unique served content has all five owned IDs graded separately.
    # All original malformed q-73800 raw replays deliberately stay ungraded;
    # their completed normal records are checked mathematically and natively.
    unique={r['question'][':question/id']:r for r in records}
    for qid,record in unique.items():
        item=native(qid,record)
        if item:native_inputs.append(item)
    save('native-input.json',native_inputs)
    subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
    report=json.loads((HERE/'native-grading.json').read_text())
    save('review.json',reviews)
    text=[]
    for row in reviews:
        text.append('## '+row['template']+' — '+row['kind'])
        if 'original_replay' in row:text.append('Original exact evidence replay:\n\n'+g.markdown(row['original_replay']))
        text.append('Generated variant:\n\n'+g.markdown(row['generated_variant']))
    (HERE/'review.md').write_text('\n\n'.join(text)+'\n')
    save('stage-validation.json',stage_results)
    # Recheck baseline after all runtime imports and native validation.
    assert {str(p.relative_to(ROOT)) for p in registered.rglob('*') if p.is_file()}|{'generate/scratch/17592186184350.py'}==basepaths
    for row in baseline:assert digest(ROOT/row['path'])==row['sha256']
    files=[HERE.with_suffix('.py')]+[HERE/name for name in ('validate.py','source.json','topic.json','lesson.json','frozen_math_format.py','frozen_parser.py','check-engine','check-engine.rs','source-cases.json','source-components.json','source-fidelity.json','independent-inventory.json','ordered-lesson-route.json','native-input.json','native-grading.json','review.json','review.md','baseline.json','README.md','classification.md','template-extraction.md','plot-extraction.md','normal-completion.json','frozen-dependencies.json')]
    validation={'passed':True,'basis':2275,'database_operations':0,'registered_paths_unchanged':len(baseline),'MA_source_banks':8,'MA_source_values':40,'MA_source_correct_designations':7,'MA_source_worked_solutions':7,'missing_raw_fields_preserved':['q-73800 difficulty','q-73800 worked-solution','q-73800 correct designation'],'independently_authored_inventory_records':len(independent),'normal_source_shaped_solutions_exact_at_anchors':normal_solution,'normal_finite_family_records':counts,'finite_distinct_mathematical_tasks':{k:len(v) for k,v in tasks.items()},'finite_family_tasks':{k:len(v) for k,v in family_tasks.items()},'observed_bank_parameter_checks':88,'default_template_coverage':sorted(default_coverage),'native':{'records':len(native_inputs),'owned_ID_checks':len(native_inputs)*5,'mathtext_foreign_malformed_contract_checks':len(native_inputs)*3,'accepted':report['accepted_checks'],'rejected_owned_wrong_IDs':report['rejected_checks'],'expected_structured_input_errors':report['documented_unresolved_checks'],'unexpected_failures':0,'blank_fields':0,'blank_equivalence_gaps':'not applicable: all observed and normal fields are radio'},'mutation_regressions_rejected':mutations,'limitations':['No hard difficulty label is observed. Hard is authored from canonical negative quartic workload.','Raw q-73800 has no rating, key or solution; cannot grade it without fabrication and is never eligible. Its completed normal record is separately authored and checked.','Historical distractor intent cannot be established from scalar/expression snapshots. Entire original banks remain public ineligible parameterized profiles.','Native radio IDs are required. Math text, foreign IDs and malformed IDs produce documented structured errors, not mathematical equivalence results.'],'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'hashes':{str(p.relative_to(ROOT)):digest(p) for p in files}}
    save('validation.json',validation);print(json.dumps({k:v for k,v in validation.items() if k!='hashes'},indent=2),flush=True)
if __name__=='__main__':main()
