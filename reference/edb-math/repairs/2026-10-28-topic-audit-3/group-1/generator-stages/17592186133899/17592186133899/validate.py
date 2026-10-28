#!/usr/bin/env python3
"""Independent readback of actual operand equations, orientation prose,
symbolic sign row, ordered substitution operands, final scalar and each bank.
Native choice grading is separately exercised, never treated as math proof.
"""
from pathlib import Path
import copy,hashlib,importlib.util,itertools,json,re,subprocess,sys,tempfile
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
import sympy as sp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('circulation_generator',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def parse(text):
    text=text.strip().replace('π','pi').replace(r'\pi','pi')
    text=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',text)
    text=text.replace(' ','')
    text=re.sub(r'(?<=\d)pi',r'*pi',text)
    assert re.fullmatch(r'[\d+*/().pi-]+',text),('invalid printed scalar',text)
    return sp.sympify(text)

def read_prompt(prompt):
    pattern=r'\\text\{d\}r\s*=\s*([^,\n$]+)' if r'\text{d}' in prompt else r' dr =\s*([^,\n$]+)'
    values=[parse(t.replace(r'\,','')) for t in re.findall(pattern,prompt)]
    assert len(values)==3,('not three supplied operands',values)
    prose=prompt.split('where ',1)[1].split(', calculate',1)[0]
    directions={}
    for m in re.finditer(r'(.*?)(?:is|are) oriented (counterclockwise|clockwise)',prose):
        for index in re.findall(r'C[^\d]*([123])',m.group(1)):
            directions[int(index)]=m.group(2)
    assert set(directions)=={1,2,3},('orientation clauses',prose,directions)
    signs=[1 if directions[i]==('counterclockwise' if i==1 else 'clockwise') else -1 for i in (1,2,3)]
    return values,signs

def check_format(text):
    assert not any(ord(c)<32 and c not in '\n\t' for c in text),'control character'
    # Literal braces are absent from these source templates.
    stack=[]
    for c in text:
        if c=='{':stack.append(c)
        elif c=='}':assert stack,'unbalanced TeX brace';stack.pop()
    assert not stack,'unbalanced TeX brace'
    assert text.count('$')%2==0,'unbalanced math delimiter'
    assert '+-' not in text and '--' not in text,'ungrouped signed arithmetic'

def read_solution(solution,values,signs,hard=False):
    assert solution.count(r'\begin{aligned}')==1
    chain=solution.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0]
    rows=chain.split(r'\\')
    assert len(rows)==(4 if hard else 3),('source stages plus authored hard common-denominator row',rows)
    symbolic=rows[0].split('& =',1)[1].strip()
    tokens=re.findall(r'([+-]?)\{∮\}_\{\{C\}_\{([123])\}\}F\\cdot \\text\{d\}r',symbolic)
    assert len(tokens)==3 and [int(i) for _,i in tokens]==[1,2,3],'symbolic summation structure'
    assert [(-1 if op=='-' else 1) for op,_ in tokens]==signs,'wrong symbolic orientation signs'
    # Independently read each numerical operand. Do not rely on generator masks
    # or a CAS-equal collapsed final expression to establish stage fidelity.
    arithmetic=rows[1].split('& =',1)[1].strip()
    scalar=r'(?:-?\s*\\frac\{\d+\}\{\d+\}|-?\d+)'
    matcher=re.compile(r'([+-]?)(\('+scalar+r'\)|'+scalar+r')')
    pos=0;items=[]
    while pos<len(arithmetic):
        m=matcher.match(arithmetic,pos);assert m,('unreadable ordered arithmetic',arithmetic,pos)
        op,term=m.groups();items.append((-1 if op=='-' else 1,parse(term)));pos=m.end()
    assert len(items)==3,'three unevaluated signed components required'
    assert [sgn for sgn,v in items]==signs,'substitution sign mismatch'
    assert [v for sgn,v in items]==values,'printed substitution operands mismatch'
    total=sum(v*s for v,s in zip(values,signs))
    assert sp.simplify(parse(arithmetic)-total)==0,'signed arithmetic mismatch'
    if hard:
        common=rows[2].split('& =',1)[1].strip()
        m=re.fullmatch(r'\\frac\{([^{}]+)\}\{(\d+)\}',common)
        assert m,('missing common-denominator operation',common)
        den=int(m[2]);assert den==sp.ilcm(*[v.q for v in values])
        numerator=m[1];pos=0;scaled=[]
        while pos<len(numerator):
            match=matcher.match(numerator,pos);assert match
            sign,term=match.groups();scaled.append((-1 if sign=='-' else 1,parse(term)));pos=match.end()
        assert scaled==[(sign,value*den) for sign,value in zip(signs,values)],'individual common-denominator operands'
        assert parse(numerator)/den==total
    conclusion=rows[-1].split('& =',1)[1].strip().removesuffix('.')
    assert parse(conclusion)==total,'wrong concluding scalar'
    return total

def check_record(record,raw=False):
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    assert record['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    q=record['question'];meta=record['generation'];field=q[':question/answer-fields'][0]
    assert field[':answer-field/type']==':answer-field.type/radio'
    values,signs=read_prompt(q[':question/problem']);total=sum(v*s for v,s in zip(values,signs))
    for text in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for a in field[':answer-field/choices']]:check_format(text)
    if ':question/worked-solution' in q:assert read_solution(q[':question/worked-solution'],values,signs,hard=not raw and q[':question/difficulty'].endswith('/hard'))==total
    else:assert raw and meta['source_id']=='q-126558'
    answers=field[':answer-field/choices'];bank=[parse(a[':answer/value']) for a in answers]
    assert len(bank)==5 and len(set(bank))==5,'whole bank ambiguity'
    assert bank.count(total)==1,'one mathematically correct choice required'
    if ':answer-field/correct' in field:
        chosen=field[':answer-field/correct'][1]
        assert parse(next(a[':answer/value'] for a in answers if a[':answer/id']==chosen))==total
    else:assert raw and meta['source_id']=='q-126558'
    if not raw:
        assert '∮_(' not in q[':question/problem'],'legacy subscript presentation repaired'
        level=q[':question/difficulty'].split('/')[-1]
        assert all(0<abs(v)<=10 for v in values) and min(values)<0<max(values)
        if level=='easy':assert signs==[1,1,1] and all(v.q==1 for v in values)
        elif level=='moderate':assert signs!=[1,1,1] and all(v.q==1 for v in values)
        else:assert {v.q for v in values}=={2,3} and all(v.q in (2,3) and abs(v.p)<=29 for v in values)
        if meta['bank_profile']=='method_signs':
            expected=[total]+[total-2*values[i]*signs[i] for i in range(3)]+[-total]
        else:expected=[total]+[total-values[i]*signs[i] for i in range(3)]+[-total]
        assert set(expected)==set(bank),'each method-bank value must follow actual displayed operations'
        assert not meta['evidence_only'] and meta['eligible_for_learning']
    else:
        assert meta['evidence_only'] and not meta['eligible_for_learning']
        sid=meta['source_id']
        # Independent source recipe audit uses separate explicit coefficients.
        coefficients={
            'q-126558':[None,(1,0,0),(1,1,1),(1,-1,-1),(0,0,0)],
            'q-126654':[(-1,1,1),(1,1,-1),(1,-1,-1),(-1,-1,0),(1,1,1)],
            'q-126862':[(1,1,-1),(1,-1,-1),(1,-1,1),(-1,-1,-1),(1,1,1)],
            'q-126863':[(1,1,-1),(1,-1,1),(-1,1,1),(1,1,1),(1,-1,-1)],
            'q-126865':[None,(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)],
            'q-126867':[(0,1,-1),(1,-1,-1),(-1,-1,-1),(1,1,1),(1,-1,1)],
            'q-126870':[(1,1,-1),(-1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,-1)],
            'q-126868':[(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,1,1)],
            'q-126864':[(1,-1,1),(1,1,-1),(1,1,1),(-1,1,-1),(1,-1,-1)],
            'q-126855':[(1,1,1),(1,1,-1),(1,-1,1),(0,-1,-1),None],
            'q-126861':[(1,-1,-1),(1,1,1),(1,-1,1),(0,-1,0),(1,1,-1)]}
        expected=[sum(c*v for c,v in zip(op,values)) if op is not None else {'q-126558':sp.pi*values[0]/5,'q-126865':-sp.Rational(5,7)*values[0],'q-126855':3*values[0]}[sid] for op in coefficients[sid]]
        assert set(expected)==set(bank),'source operation-bank readback'
    return total

def rejection_regressions(record):
    mutations=[]
    bad=copy.deepcopy(record);s=bad['question'][':question/worked-solution'];a=s.index('& =')+4
    bad['question'][':question/worked-solution']=s[:a]+'-'+s[a:];mutations.append(bad)
    bad=copy.deepcopy(record);s=bad['question'][':question/worked-solution'];rows=s.split(r'\\');rows[1]=rows[2].split(r'\end{aligned}')[0];bad['question'][':question/worked-solution']=r'\\'.join(rows);mutations.append(bad)
    bad=copy.deepcopy(record);bad['question'][':question/worked-solution']+='\x0c';mutations.append(bad)
    bad=copy.deepcopy(record);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('clockwise* for the *inner*','counterclockwise* for the *inner*');
    # Prefix is checked by structural source-mask parity separately below.
    mutations.append(bad)
    for bad in mutations:
        try:check_record(bad);check_prose(bad)
        except (AssertionError,ValueError,IndexError):continue
        raise AssertionError('Mutation escaped independent validation')
    return len(mutations)

def check_prose(record):
    q=record['question'];sid=record['generation']['source_id']
    if ':question/worked-solution' not in q:return
    original=g.QUESTIONS[sid].get(':question/worked-solution',g.QUESTIONS['q-126862'][':question/worked-solution'])
    expected=original.split(r'\begin{aligned}')[0]
    actual=q[':question/worked-solution'].split(r'\begin{aligned}')[0]
    # Full prose/paragraph/row sequence; asset spellings normalized separately.
    clean=lambda s:re.sub(r'!\[\]\([^)]+\)','![](PLOT)',s)
    assert clean(actual)==clean(expected),'family prose sequence mismatch'

def meaningful_count():
    """Finite exact enumeration; simultaneous hole-label swaps identified.
    Integer arithmetic uses a 6x scale for the fractional domain, so no float
    equality enters either count. Union of whole eligible authored banks.
    """
    result={}
    for level in ('easy','moderate','hard'):
        domain=list(range(-10,0))+list(range(1,11)) if level!='hard' else sorted({int(6*Fraction(n,d)) for d in (2,3) for n in range(-29,30) if n and Fraction(n,d).denominator==d and abs(Fraction(n,d))<=10})
        signs=[(1,1,1)] if level=='easy' else sorted({s['signs'] for s in g.FAMILIES.values() if s['level']=='moderate'})
        seen=set();eligible_profiles={p:0 for p in g.METHOD_PROFILES}
        for values in itertools.product(domain,repeat=3):
            if not min(values)<0<max(values):continue
            if level=='hard' and {Fraction(v,6).denominator for v in values}!={2,3}:continue
            for sign in signs:
                components=[v*s for v,s in zip(values,sign)];total=sum(components)
                banks={'method_signs':[total]+[total-2*c for c in components]+[-total], 'method_omissions':[total]+[total-c for c in components]+[-total]}
                if any(len(set(bank))==5 for bank in banks.values()):
                    task=(values[0],sign[0],tuple(sorted(zip(values[1:],sign[1:]))));seen.add(task)
                for profile,bank in banks.items():
                    if len(set(bank))==5:eligible_profiles[profile]+=1
        result[level]={'meaningful_tasks':len(seen),'eligible_ordered_bank_instances':eligible_profiles,'incidental_excluded':'diagram, template alias, bank profile, C2/C3 simultaneous operand/orientation relabeling'}
    return result

def plot_concurrency():
    # Fresh private cache, never prune or overwrite assets used in review.
    previous=g.HERE
    with tempfile.TemporaryDirectory(prefix='circulation-plot-') as directory:
        g.HERE=Path(directory)
        try:
            with ThreadPoolExecutor(max_workers=4) as pool:
                paths=list(pool.map(lambda _:g.legacy_solution_asset(),range(4)))
            assert len(set(paths))==1
            path=Path(paths[0]);assert path.is_file() and path.with_suffix('.json').is_file()
            assert not list(path.parent.glob('tmp*.png')) and not list(path.parent.glob('tmp*.json'))
            assert json.loads(path.with_suffix('.json').read_text())['holes'][0]['center']==[.25,.25]
            return {'fresh_concurrent_calls':4,'unique_atomic_target':True,'no_private_temporary_leaks':True}
        finally:g.HERE=previous

def main():
    cases=json.loads((HERE/'source-cases.json').read_text());replays=[];fidelity=[]
    for case in cases:
        record=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);raw=g.QUESTIONS[case['source_id']];q=record['question']
        check_record(record,raw=True);check_prose(record)
        assert q[':question/problem']==raw[':question/problem']
        assert q.get(':question/worked-solution')==raw.get(':question/worked-solution')
        for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in raw),'source attribute presence'
        f=q[':question/answer-fields'][0];rf=raw[':question/answer-fields'][0]
        assert (':answer-field/correct' in f)==(':answer-field/correct' in rf),'correct-ref presence'
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in rf[':answer-field/choices'])
        if ':answer-field/correct' in rf:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==rf[':answer-field/correct'][':answer/value']
        fidelity.append({'source_id':case['source_id'],'prompt_exact':True,'solution_exact_or_absent':True,'bank_values':5,'correct_designation_matched':':answer-field/correct' in rf,'attribute_presence_exact':True})
        replays.append(record)
        # Genuine changed-parameter public replay, full raw operations checked.
        changed=copy.deepcopy(case['parameters']);changed['values']=[str(sp.Rational(v)*sp.Rational(3,2)) for v in changed['values']]
        variant=g.generate(case['level'],template=case['template'],parameters=changed,profile=case['bank_profile']);check_record(variant,raw=True);check_prose(variant)
    records=[];coverage={};diagram_coverage={};identities=0
    for level in ('easy','moderate','hard'):
        for seed in range(160):
            record=g.generate(level,seed);check_record(record);check_prose(record);records.append(record)
            coverage.setdefault(level,set()).add(record['generation']['template'])
            diagram_coverage.setdefault(level,set()).add(record['generation']['source_id'])
        expected={f for f,s in g.FAMILIES.items() if s['level']==('moderate' if level=='hard' else level)}
        assert coverage[level]==expected,'normal default family coverage'
        assert diagram_coverage[level]=={sid for family in expected for sid in g.FAMILIES[family]['sources']},'normal source-shaped diagram coverage'
        for family in expected:
            for profile in g.METHOD_PROFILES:
                r=g.generate(level,template=family,profile=profile,seed=37);check_record(r);check_prose(r)
                r2=g.generate(level,seed=999,template=family,profile=profile,parameters=r['generation']['parameters'])
                assert r['question'][':question/id']==r2['question'][':question/id'];identities+=1
    mutations=rejection_regressions(records[0])
    reviewed=json.loads((HERE/'review.json').read_text())
    for item in reviewed:
        record=item['record'];check_record(record,raw=record['generation']['evidence_only']);check_prose(record)
    plots=plot_concurrency()
    correct_positions={next(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1]) for r in records}
    assert correct_positions==set(range(5)),'normal choices not shuffled across all positions'
    # Boundary/invalid inputs must reject, never silently resample.
    rejected=0
    for level,template,values in [('easy','positive',[1,2,3]),('easy','positive',[1,-2,'1/2']),('moderate','outer_reverse',[11,-2,3]),('moderate','inner2_reverse',['1/2',-2,3]),('hard','outer_reverse',[1,-2,3]),('hard','outer_reverse',['1/2','-3/2','5/2']),('hard','outer_reverse',['1/2','-2/3','31/3'])]:
        try:g.generate(level,template=template,parameters={'values':values})
        except g.SampleRejected:rejected+=1
        else:raise AssertionError('Explicit parameter workload guard bypass')
    # Independent actual engine; full displayed banks already mathematically read.
    fixtures=[]
    for record in records[:40]+records[160:200]+records[320:360]+replays:
        f=record['question'][':question/answer-fields'][0]
        if ':answer-field/correct' not in f:continue
        fixtures.append({'label':record['question'][':question/id'],'record':record,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'native owned radio choice'} for a in f[':answer-field/choices']]})
    input_path=HERE/'native-input.json';output_path=HERE/'native-report.json';input_path.write_text(json.dumps(fixtures,indent=2))
    engine=ROOT/'generate/runs/current/check-engine'
    completed=subprocess.run([str(engine),str(input_path),str(output_path)],capture_output=True,text=True)
    assert completed.returncode==0,completed.stderr+completed.stdout
    native=json.loads(output_path.read_text())
    counts=meaningful_count()
    report={'status':'passed','runtime':{'python':sys.version.split()[0],'sympy':sp.__version__,'renderer':json.loads((HERE/'plots/legacy-positive.json').read_text())},'source_provenance':{k:g.WRAPPER[k] for k in ('database','basis','lineage')},'source_coverage':fidelity,'fidelity':{'source_questions':11,'exact_prompts':11,'exact_present_solutions':10,'absent_solutions_preserved':1,'exact_bank_values':55,'complete_banks':11,'correct_designations_matched':10,'missing_designation_not_counted':1,'raw_presence_parity':11},'generated_readback_records':len(records),'review_records_readback':len(reviewed),'changed_raw_replays':11,'native_fixtures':len(fixtures),'native_checks':sum(len(f['checks']) for f in fixtures),'native_report':native,'native_engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'default_family_coverage':{k:sorted(v) for k,v in coverage.items()},'default_source_diagram_coverage':{k:sorted(v) for k,v in diagram_coverage.items()},'identity_checks':identities,'explicit_rejections':rejected,'mutation_regressions':mutations,'plot_concurrency':plots,'correct_choice_positions':sorted(correct_positions),'finite_meaningful_variation':counts,'authored_hard':True,'unresolved_source_findings':['q-126558 lacks difficulty, worked solution and correct reference; raw replay preserves all absences; default completes sum=4 and authored easy designation.','Three historical scalar responses (2π, -5,12) have underdetermined intent and remain common-scaling evidence only; all raw banks are ineligible for normal learning.']}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:report[k] for k in ('status','fidelity','generated_readback_records','native_checks','finite_meaningful_variation')},indent=2))

if __name__=='__main__':main()
