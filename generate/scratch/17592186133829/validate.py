#!/usr/bin/env python3
"""Independent displayed mathematics, raw fidelity and real native grading.

The parser is the parent's fail-closed elementary TeX parser copied read-only
into this evidence directory. Checks read actual prompt/choice/solution text;
generation metadata is not the mathematical oracle. No EDB operations.
"""
import copy, importlib.util, itertools, json, re, subprocess, sys, hashlib, uuid
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2]
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('generator',ROOT.with_suffix('.py'))
p=module('display_parser',ROOT/'displayed_parser.py');t=p.t
def clean(raw):
    raw=raw.strip().rstrip('.,?').replace(r'\displaystyle','').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*')
    raw=re.sub(r'\\(?:mathrm|text)\{d\}t', 'dt',raw)
    return raw.replace('\u2061','').strip()
def math(raw):
    raw=clean(raw).replace('[','(').replace(']',')')
    while '|' in raw:
        a=raw.index('|');b=raw.index('|',a+1);inner=math(raw[a+1:b]);raw=raw[:a]+'sqrt{('+s.latex(inner)+')^2}'+raw[b+1:]
    return p.scalar(raw)
def group(raw,start):
    assert raw[start]=='{',(raw,start)
    depth=1;i=start+1
    while depth:
        assert i<len(raw),raw;depth+=(raw[i]=='{')-(raw[i]=='}');i+=1
    return raw[start+1:i-1],i
def integral(raw):
    raw=clean(raw.strip().rstrip('.,?').strip('$')).replace(r'{\int }',r'\int').replace(r'{\int}',r'\int')
    # Complete-component amplitude wrapper around a definite integral.
    factor=s.Integer(1)
    m=re.fullmatch(r'(-?\d+)\((.*)\)',raw,re.S)
    if m:factor=s.Integer(m[1]);raw=m[2]
    start=raw.index(r'\int');prefactor=raw[:start].strip();factor*=math(prefactor) if prefactor else 1
    pos=start+len(r'\int');assert raw[pos]=='_';lo,pos=group(raw,pos+1);assert raw[pos]=='^';hi,pos=group(raw,pos+1)
    tail=raw[pos:].strip();assert tail.endswith('dt'),raw;fn=math(tail[:-2].rstrip().rstrip('*'))
    return math(lo),math(hi),s.simplify(factor*fn)
def vector(raw):
    raw=clean(raw)
    if '⟨' in raw or r'\langle' in raw:
        raw=raw.replace(r'\langle','⟨').replace(r'\rangle','⟩');assert raw.startswith('⟨') and raw.endswith('⟩'),raw
        return tuple(math(a) for a in raw[1:-1].split(','))
    expr=s.expand(math(raw));v=tuple(expr.coeff(b) for b in (p.i,p.j,p.k));assert s.simplify(expr-sum(a*b for a,b in zip(v,(p.i,p.j,p.k))))==0
    return v[:3 if v[2]!=0 else 2]
def blocks(text):return [m[0][2:-2] if m[0].startswith('$$') else m[0][1:-1] for m in g.MATH.finditer(text)]
def prompt(text):
    chunks=blocks(text);curve=vector(next(q for q in chunks if 'r(t)=' in q or 'r(t) =' in q).split('=',1)[1])
    fdefinition=next((q for q in chunks if re.match(r'f\(x,y(?:,z)?\)=',q)),None)
    if fdefinition:scalar=math(fdefinition.split('=',1)[1])
    else:
        raw=next(q for q in chunks if r'\int' in q)
        raw=clean(raw).replace(r'{\int }',r'\int').replace(r'\int_(C)',r'\int_C')
        raw=re.sub(r'^\\int_(?:\{C\}|C)','',raw);raw=re.split(r'(?:\\(?:text|mathrm|textrm)\{d\}s|ds)',raw)[0]
        scalar=math(raw)
    interval=next(q for q in chunks if (r'\le t' in q or r't\in [' in q))
    interval=clean(interval)
    if r't\in [' in interval:lo,hi=interval.split('[',1)[1].rstrip(']').split(',')
    else:lo,hi=re.split(r'\\le\s*t\s*\\le',interval)
    return curve,scalar,(math(lo),math(hi))
def same(a,b,bounds):
    a=s.trigsimp(s.expand(a));b=s.trigsimp(s.expand(b));delta=s.simplify(a-b)
    if delta==0:return True
    if bounds[0]>=0:delta=s.refine(delta,s.Q.nonnegative(t))
    return s.simplify(delta)==0
def formatting(text):
    assert '$' not in g.MATH.sub('',text),'unbalanced math dollars'
    for chunk in blocks(text):
        depth=0
        for i,c in enumerate(chunk):
            if c in '{}':
                # Ignore literal escaped brace glyphs; all actual TeX groups balance.
                if i and chunk[i-1]=='\\':continue
                depth+=(c=='{')-(c=='}');assert depth>=0,chunk
        assert depth==0,chunk
        assert '+-' not in chunk and '--' not in chunk,chunk
def derivative_operators(raw):
    # Replace each formal derivative of the displayed complete argument.
    pattern=re.compile(r'\\frac\{\\(?:mathrm|text)\{d\}\}\{\\(?:mathrm|text)\{d\}t\}\(')
    while (m:=pattern.search(raw)):
        start=m.end();i=start;depth=1
        while depth:assert i<len(raw);depth+=(raw[i]=='(')-(raw[i]==')');i+=1
        argument=math(raw[start:i-1]);raw=raw[:m.start()]+'('+s.latex(s.diff(argument,t))+')'+raw[i:]
    return raw
def solution_stages(text,curve,scalar,bounds):
    dim=len(curve);der=tuple(s.diff(q,t) for q in curve)
    speed=s.sqrt(s.trigsimp(s.expand(sum(q*q for q in der))))
    sub=s.trigsimp(s.expand(scalar.subs(dict(zip((p.x,p.y,p.z),curve)),simultaneous=True)));correct=sub*speed
    counts={'derivative_rows':0,'norm_rows':0,'substitution_rows':0,'integral_rows':0,'operator_components':0}
    roles=[]
    for body in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S):
        mode='integral' if r'\int' in body else 'sub' if body.startswith('f(r(t))') else 'derivative'
        rows=re.split(r'\\\\',body)
        for row in rows:
            raw=row.split('=',1)[1].replace('&','').strip().rstrip('.,?')
            if mode=='sub':
                assert same(math(raw),sub,bounds),(raw,sub);counts['substitution_rows']+=1;roles.append('sub');continue
            if mode=='integral':
                if 'f(r(t))' in raw:
                    # Generic symbols refer to the actual printed curve and scalar.
                    raw=raw.replace('f(r(t))','('+s.latex(sub)+')')
                    raw=raw.replace('‖{r}^{′}(t)‖','('+s.latex(speed)+')').replace(r"\|r'(t)\|",'('+s.latex(speed)+')')
                a,b,value=integral(raw);assert a==bounds[0] and b==bounds[1] and same(value,correct,bounds),(raw,value,correct)
                counts['integral_rows']+=1;roles.append('integral');continue
            # Formal dx/dt rows are meaningful: substitute actual printed
            # derivatives and then validate their complete vector/norm structure.
            for name,d in zip(('x','y','z'),der):
                for command in ('text','mathrm'):
                    raw=raw.replace('\\frac{\\'+command+'{d}'+name+'}{\\'+command+'{d}t}', '('+s.latex(d)+')')
            isoperator=bool(re.search(r'\\frac\{\\(?:text|mathrm)\{d\}\}\{\\(?:text|mathrm)\{d\}t\}',raw))
            if isoperator:
                counts['operator_components']+=len(re.findall(r'\\frac\{\\(?:text|mathrm)\{d\}\}',raw));raw=derivative_operators(raw)
            if re.search(r'[ijk](?:\s|[+\\]|$)',raw):
                v=vector(raw);assert len(v)==dim and all(same(a,b,bounds) for a,b in zip(v,der)),(raw,v,der)
                counts['derivative_rows']+=1;roles.append('operator' if isoperator else 'derivative')
            else:
                assert same(math(raw),speed,bounds),(raw,math(raw),speed)
                counts['norm_rows']+=1;roles.append('norm')
    assert counts['derivative_rows']>=3 and counts['operator_components']==dim and counts['substitution_rows']>=1 and counts['integral_rows']>=3,counts
    return roles,counts
def check(record,raw=False):
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    q=record['question'];field=q[':question/answer-fields'][0]
    uuid.UUID(q[':question/id']);uuid.UUID(field[':answer-field/id'])
    assert field[':answer-field/type']==':answer-field.type/radio' and field[':answer-field/key']=='selection'
    formatting(q[':question/problem'])
    curve,scalar,bounds=prompt(q[':question/problem']);der=[s.diff(v,t) for v in curve];speed=s.sqrt(s.trigsimp(s.expand(sum(v*v for v in der))))
    sub=s.trigsimp(s.expand(scalar.subs(dict(zip((p.x,p.y,p.z),curve)),simultaneous=True)));correct=sub*speed
    choices=field[':answer-field/choices'];assert len(choices)==5
    parsed=[];correct_rows=[]
    for a in choices:
        uuid.UUID(a[':answer/id'])
        value=a[':answer/value'];formatting(value if a[':answer/type']==':answer.type/text' else '$'+value+'$')
        lo,hi,expr=integral(value);assert (lo,hi)==bounds
        parsed.append(expr)
        if same(expr,correct,bounds):correct_rows.append(a[':answer/id'])
    assert len(correct_rows)==1,(record['generation']['template'],parsed,correct)
    if ':answer-field/correct' in field:assert field[':answer-field/correct']==[':answer/id',correct_rows[0]]
    if not raw:
        # Feed only independently read-back mathematical objects to exact
        # complete-value validation, not the generator's choice metadata.
        converted=[e.xreplace({t:g.t}) for e in parsed]
        values=g.distinct_bank(converted,{'lo':bounds[0],'hi':bounds[1]})
        assert len(values)==5
    if ':question/worked-solution' in q:
        structural_stages(record)
        formatting(q[':question/worked-solution']);roles,counts=solution_stages(q[':question/worked-solution'],curve,scalar,bounds)
        return {'roles':roles,'counts':counts}
    assert raw;return None
def structural_stages(record):
    family=record['generation']['template'];text=record['question'][':question/worked-solution']
    bodies=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S)
    subbody=next(q for q in bodies if q.startswith('f(r(t))'))
    rows=[q.split('=',1)[1].strip().rstrip('.,?') for q in re.split(r'\\\\',subbody)]
    if family=='hard_product_square':
        assert len(rows)==3 and r')(' in rows[0] and r')^2' in rows[0]
        assert r't^3' in rows[1] and r't^2' in rows[1] and r'\left(' in rows[1]
        assert rows[1]!=rows[2],'expanded and collected stages must remain distinct'
    elif family=='linear_cubic':
        assert len(rows)==3 and '^3' in rows[0] and r'8t^3-2+t' in rows[1]
    else:
        source=g.QUESTIONS[g.FAMILIES[family][1]][':question/worked-solution']
        oldbodies=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',source,re.S)
        assert [len(re.split(r'\\\\',q)) for q in bodies]==[len(re.split(r'\\\\',q)) for q in oldbodies]
        expected=next(q for q in oldbodies if q.startswith('f(r(t))'))
        expectedrows=[q.split('=',1)[1].strip().rstrip('.,?') for q in re.split(r'\\\\',expected)]
        for original,actual in zip(expectedrows,rows):
            # Complete source operation mask, allowing the outer amplitude slot.
            assert original in actual,(family,original,actual)
def engine_fixture(record,label):
    field=record['question'][':question/answer-fields'][0];correct=field[':answer-field/correct'][1]
    checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'owned radio ID; displayed mathematics checked independently'} for a in field[':answer-field/choices']]
    return {'label':label,'record':record,'checks':checks}
def assert_rejected(call):
    try:call()
    except (ValueError,AssertionError):return
    raise AssertionError('invalid explicit input was accepted')
def source_bank_values(case):
    """All real historical options: exact full values, plus exact helix bounds.

    The two nonreal members are invalid distractor evidence, not passed real
    values. Non-elementary helix values are separated by analytic inequalities.
    """
    family=case['template'];lo=g.exact(case['parameters']['lo']);hi=g.exact(case['parameters']['hi'])
    invalid={'difference':{2},'quadratic3':{3}}.get(family,set())
    expressions=g.RAW_RECIPES[family]
    if family=='helix':
        # sqrt(1+2u) >= 1+(sqrt3-1)u for0<=u<=1 (concavity chord).
        # Thus I1>=sqrt2[Integral(t cos t)+(sqrt3-1)Integral(t cos³t)].
        assert s.integrate(g.t*s.cos(g.t)**3,(g.t,0,s.pi/2))==s.pi/3-s.Rational(7,9)
        pl,pu=s.Rational(333,106),s.Rational(355,113)
        first_lower=s.sqrt(2)*(pl/2-1+(s.sqrt(3)-1)*(pl/3-s.Rational(7,9)))
        first_upper=s.sqrt(6)*(pu/2-1)
        fifth_upper=pu**2/4-pl/2
        fifth_lower=pl**2/4-pu/2
        assert s.simplify(first_lower-fifth_upper).is_positive
        assert s.simplify(2*s.sqrt(6)-first_upper).is_positive
        assert fifth_lower>0
        assert s.simplify(4-s.sqrt(2)/2-pu).is_positive
        return {'real_options':5,'unequal_full_value_pairs':10,'method':'exact SymPy primitives for2/4/5, analytic positive bounds for1/3; rational333/106<pi<355/113 separates every pair'}
    values=[g.full_value(e,lo,hi) for i,e in enumerate(expressions) if i not in invalid]
    assert all(not q.has(s.Integral) for q in values)
    for a,b in itertools.combinations(values,2):
        delta=s.expand(a-b);assert delta!=0 and delta.is_zero is False,(family,a,b)
    return {'real_options':len(values),'nonreal_option_indices_zero_based':sorted(invalid),'unequal_full_value_pairs':len(values)*(len(values)-1)//2,'exact_real_values':[str(q) for q in values]}
def main():
    cases=json.loads((ROOT/'source-cases.json').read_text());fixtures=[];review=[];source_report=[]
    for c in cases:
        r=g.generate(c['level'],2,c['template'],parameters=c['parameters'],profile=c['bank_profile']);q=r['question'];o=g.QUESTIONS[c['source_id']]
        assert q[':question/problem']==o[':question/problem']
        for key in (':question/difficulty',':question/worked-solution'):
            assert (key in q)==(key in o)
            if key in o:assert q[key]==(g.enum(o[key]) if key==':question/difficulty' else o[key])
        f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0]
        assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
        assert sorted((a[':answer/value'],a[':answer/type']) for a in f[':answer-field/choices'])==sorted((a[':answer/value'],g.enum(a[':answer/type'])) for a in of[':answer-field/choices'])
        if ':answer-field/correct' in of:
            expected=of[':answer-field/correct'][':answer/value'];actual=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert expected==actual
        stage=check(r,True)
        # Changed parameter raw replay goes through the same public recipe API.
        changed={**c['parameters'],'m':-2}
        if c['template']!='helix':changed['hi']='3' if c['template']!='linear_cubic' else '5/2'
        rr=g.generate(c['level'],8,c['template'],parameters=changed,profile=c['bank_profile']);check(rr,True)
        source_report.append({'source_id':c['source_id'],'prompt_exact':True,'bank_exact_options':5,'solution_exact':stage is not None,'correct_designation_exact':':answer-field/correct' in of,'raw_omissions':r['generation']['raw_attribute_omissions'],'raw_evidence_only':True,'full_value_checks':source_bank_values(c)})
        review.append({'label':'Raw original '+c['source_id'],'record':r})
        if ':answer-field/correct' in f:fixtures.append(engine_fixture(r,'raw/'+c['source_id']))
    generated=0;stage_counts={};task_sets={};default_coverage={}
    for family,spec in g.FAMILIES.items():
        task_sets[family]=set()
        for seed in range(8):
            r=g.generate(spec[0],seed,family);stage=check(r);generated+=1
            stage_counts[family]=stage;task_sets[family].add(r['generation']['mathematical_fingerprint'])
            fixtures.append(engine_fixture(r,family+'/'+str(seed)))
            if seed<2:review.append({'label':'Generated '+family+' seed '+str(seed),'record':r})
            assert r==g.generate(spec[0],seed,family)
            # Seed/order does not change mathematical/content/field identity.
            alternate=g.generate(spec[0],100+seed,family,parameters=r['generation']['parameters'])
            assert r['question'][':question/id']==alternate['question'][':question/id']
        assert len(task_sets[family])>=7
        print('Checked family '+family,flush=True)
    for level in ('easy','moderate','hard'):
        seen=set()
        for seed in range(30):
            r=g.generate(level,seed);seen.add(r['generation']['template'])
        assert seen==set(k for k,v in g.FAMILIES.items() if v[0]==level),(level,seen)
        default_coverage[level]=sorted(seen)
    # Mathematical-task identity is bank independent; presentation IDs are not.
    c=cases[0];raw=g.generate(c['level'],0,c['template'],parameters=c['parameters'],profile=c['bank_profile']);normal=g.generate(c['level'],0,c['template'],parameters=c['parameters'])
    assert raw['generation']['mathematical_fingerprint']==normal['generation']['mathematical_fingerprint']
    assert raw['question'][':question/id']!=normal['question'][':question/id']
    completed=g.generate_moderate(0,'linear_cubic',parameters=cases[-1]['parameters'],profile='completed-source');check(completed);fixtures.append(engine_fixture(completed,'completed/inferred-key'))
    assert ':question/difficulty' in completed['question'] and ':answer-field/correct' in completed['question'][':question/answer-fields'][0]
    # Explicit/sampler difficulty guards and entire-bank value-collision regression.
    assert_rejected(lambda:g.generate_easy(parameters={'m':0,'lo':0,'hi':1}))
    assert_rejected(lambda:g.generate_easy(parameters={'m':7,'lo':0,'hi':1}))
    assert_rejected(lambda:g.generate_easy(parameters={'m':1,'lo':-1,'hi':1}))
    assert_rejected(lambda:g.generate_moderate(template='helix',parameters={'m':1,'lo':0,'hi':'pi'}))
    hp={'a':1,'b':1,'d':1,'c':1,'e':1,'m':1,'lo':0,'hi':2}
    for k,v in [('a',0),('a',4),('c',0),('e',-4),('m',4),('lo',-1)]:assert_rejected(lambda k=k,v=v:g.generate_hard(parameters={**hp,k:v}))
    # Different-looking integrals of equal full value must fail as a whole bank.
    assert_rejected(lambda:g.distinct_bank([g.t,2*g.t**3,g.t+1,g.t+2,g.t+3],{'lo':s.Integer(0),'hi':s.Integer(1)}))
    # Mutation retains algebraic equality but removes the required expanded stage.
    r=g.generate_hard(5);q=copy.deepcopy(r);body=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q['question'][':question/worked-solution'],re.S)[1];rows=re.split(r'\\\\',body)
    q['question'][':question/worked-solution']=q['question'][':question/worked-solution'].replace(rows[1],rows[2])
    # Structural regression independently checks the source-aligned expansion mask.
    assert '(' in rows[1] and r't^3' in rows[1] and r't^2' in rows[1] and r'\left(' in rows[1]
    assert rows[1]!=rows[2]
    assert_rejected(lambda:check(q))
    # Large honest finite task domains, without counting bank/variable aliases.
    endpoint_count=len(set([s.Rational(n,d) for d in (1,2,3) for n in range(6*d+1)]+[s.sqrt(2),s.sqrt(3)]))
    domain_counts={'parabola':12*endpoint_count*(endpoint_count-1)//2,'difference':12*endpoint_count*(endpoint_count-1)//2,'squares':12*endpoint_count*(endpoint_count-1)//2,'quadratic3':12*endpoint_count*(endpoint_count-1)//2,'helix':12*21,'linear_cubic':12*4*5,'hard_product_square':3**3*6**2*6*3*4}
    # These are candidate task counts; collisions are rejected and not counted as
    # accepted. Exhaustive accepted totals are explicitly not claimed.
    (ROOT/'native-input.json').write_text(json.dumps(fixtures,indent=2,ensure_ascii=False)+'\n')
    checker=REPO/'generate/runs/current/check-engine';subprocess.run([str(checker),str(ROOT/'native-input.json'),str(ROOT/'native-report.json')],check=True)
    native=json.loads((ROOT/'native-report.json').read_text())
    report={'status':'passed','source':{k:g.SOURCE[k] for k in ('database','basis','lineage')},'source_coverage':source_report,'source_counts':{'practices':6,'exact_prompts':6,'exact_complete_banks':6,'exact_options':30,'exact_available_solutions':5,'available_solutions':5,'exact_correct_designations':5,'available_designations':5,'missing_designation_completed_separately':1,'raw_unrated_omissions':1},'normal_generated_checked':generated,'raw_changed_parameter_checks':6,'default_family_coverage':default_coverage,'stage_counts':stage_counts,'candidate_task_domain_counts':domain_counts,'candidate_counts_exclude':'Rejected whole-bank collisions; accepted exhaustive counts not claimed. Banks/aliases excluded.','native':{k:v for k,v in native.items() if k!='records'},'native_binary_sha256':hashlib.sha256(checker.read_bytes()).hexdigest(),'source_anomalies':{'nonreal_wrong_options':['q-40253 option sqrt(2t^2-1)','q-76356 option sqrt(t^2-t)'],'source_correct_setups_sound':True,'q-76356_endpoint_prose':'raw t>0 retained; normal t>=0','q-76368':'unrated; missing correct designation and solution preserved raw; completed independently as moderate'},'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__},'plots':'No practice plots. Canonical reference inspected at original resolution; generator has no plot dependency.'}
    report['source_native_grading']={'captured_profiles':6,'keyed_radio_fixture_profiles':5,'unkeyed_raw_profiles_not_gradeable':1,'evidence_only_profiles':6,'documented_native_unresolved':0,'note':'Missing key remains omitted raw; native fixture is not fabricated. Separate completed-source is keyed but evidence-only because its historical wrong-operation intent is opaque.'}
    report['native_equivalent_entry_probes']='Not applicable: all observed fields are radio selections. Equivalent math is checked on actual displayed full integrals; no unsupported blank fields are invented.'
    report['outside_submission_domain_probe']={'submitted':'99999','actual':'error: selected answer does not belong to this field','note':'The initial extra probe incorrectly expected a Boolean rejection for a non-owned ID. Native radio submissions must select an owned option; this deliberate malformed submission is recorded separately and excluded from valid learner-answer counts.'}
    (ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');(ROOT/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
    (ROOT/'review.md').write_text('# Scalar line-integral setup review\n\nRaw source banks are evidence only. Generated records are explicitly labeled; no integral evaluation is requested.\n\n'+'\n\n---\n\n'.join('## '+r['label']+'\n\n'+g.markdown(r['record']) for r in review)+'\n')
    print(json.dumps({k:report[k] for k in ('status','source_counts','normal_generated_checked','native')},indent=2))
if __name__=='__main__':main()
