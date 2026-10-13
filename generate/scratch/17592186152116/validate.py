#!/usr/bin/env python3
"""Independent printed-polynomial/stage/source/native grading validation. No EDB."""
import importlib.util,json,math,re,subprocess,hashlib,itertools
from pathlib import Path
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py')); g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
sp=g.sp

def write(name,obj): (HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def lcm(A,B,v):
    return sp.Poly(A,v,domain=sp.ZZ).lcm(sp.Poly(B,v,domain=sp.ZZ)).as_expr()
def split_top(s):
    depth=0;pieces=[];start=0
    for i,ch in enumerate(s):
        depth+= ch=='(';depth-=ch==')'
        if ch==',' and depth==0: pieces.append(s[start:i]);start=i+1
    return pieces+[s[start:]]
def value(s,v):
    s=s.strip().rstrip('.').replace(r'\,','')
    if s.startswith(r'\text{LCM}'):
        s=s[len(r'\text{LCM}'):]; assert s[0]=='(' and s[-1]==')',s
        args=split_top(s[1:-1]); assert len(args)==2,s
        A,B=map(g.parse_tex,args)
        if not A.free_symbols and not B.free_symbols: return sp.Integer(math.lcm(abs(int(A)),abs(int(B))))
        return lcm(A,B,v)
    return g.parse_tex(s)
def format_check(s):
    assert not any(ord(ch)<32 and ch not in '\n' for ch in s),'hidden control'
    assert not '\\\\' in s,'decoded adjacent slashes'
    assert s.count('$')%2==0,'math delimiter'
    depth=0
    for ch in s:
        if ch=='{':depth+=1
        if ch=='}':depth-=1
        assert depth>=0,'closing TeX brace'
    assert depth==0,'unbalanced TeX brace'
    assert '--' not in s and '+-' not in s,'bare signed operator'

def check(r,raw=False):
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    assert r['knowledge_point']['db_id']==g.KP
    q=r['question'];m=r['generation']; f=q[':question/answer-fields'][0]
    v=sp.Symbol(m['parameters']['v'])
    actual=re.findall(r'\$([^$]*)\$',q[':question/problem'])[:2]
    assert len(actual)==2
    A,B=[g.parse_tex(s.rstrip('.')) for s in actual]
    assert A.free_symbols==B.free_symbols=={v},'printed variable mismatch'
    assert sp.cancel(A/B).free_symbols==set(),'inputs do not differ by constant factor'
    expected=lcm(A,B,v)
    a=sp.Poly(A,v,domain=sp.ZZ);b=sp.Poly(B,v,domain=sp.ZZ)
    primitiveA=a.primitive()[1].as_expr();primitiveB=b.primitive()[1].as_expr()
    primitiveA*=sp.sign(a.LC());primitiveB*=sp.sign(b.LC())
    assert sp.expand(primitiveA-primitiveB)==0
    assert sp.Poly(expected,v).content()==math.lcm(int(a.content()),int(b.content()))
    if m['level']=='easy':
        assert 2<=int(a.content())<=9 and 2<=int(b.content())<=9
        assert math.gcd(int(a.content()),int(b.content()))==1,'easy lost coprime-content workload'
    elif m['level']=='moderate':
        assert math.gcd(int(a.content()),int(b.content()))>1,'moderate lost shared content'
        if a.degree()==1:
            ac,bc=int(a.content()),int(b.content());assert ac%bc and bc%ac
    if m['level']=='hard':
        assert a.degree()==b.degree()==2
        prim=sp.Poly(primitiveA,v);assert abs(prim.LC())>=2 and len(prim.terms())==3 and prim.content()==1
        assert min(a.LC(),b.LC())<0
        ac,bc=int(a.content()),int(b.content());assert ac%bc and bc%ac and math.gcd(ac,bc)>1
    format_check(q[':question/problem'])
    if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
    answers=f.get(':answer-field/choices',[])
    assert len(set(x[':answer/id'] for x in answers))==len(answers)
    vals=[g.parse_tex(x[':answer/value']) for x in answers]
    for x in answers: format_check(x[':answer/value']); assert '$' not in x[':answer/value']
    for i,x in enumerate(vals):
        assert x.free_symbols<= {v}
        assert all(sp.expand(x-y)!=0 for y in vals[i+1:])
    if ':answer-field/correct' in f:
        corr=f[':answer-field/correct'];assert corr[0]==':answer/id'
        good=[i for i,x in enumerate(answers) if x[':answer/id']==corr[1]]; assert len(good)==1
        assert sp.expand(vals[good[0]]-expected)==0,'normalized LCM is incorrect'
        assert sum(sp.expand(x-expected)==0 for x in vals)==1
    if ':question/worked-solution' in q:
        sol=q[':question/worked-solution'];format_check(sol)
        # Every math equality in the actual printed solution, including GCF products,
        # numeric LCM, formal primitive LCM, and final signed-polynomial LCM.
        equations=[]
        for chunk in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$([^$]*)\$(?!\$)',sol,re.S):
            text=next(s for s in chunk if s).strip()
            for eq in text.split(r'\qquad'):
                eq=eq.strip().strip(',')
                if '=' not in eq:continue
                terms=eq.rstrip('.').split('=')
                parsed=[value(s,v) for s in terms]
                assert all(sp.expand(x-parsed[0])==0 for x in parsed[1:]),eq
                equations.append(eq)
        assert len(equations)==(5 if m['level']=='hard' else 3),equations
        assert 'Since the variable part is the same in the expressions, we have' in sol
        assert 'Finally, we multiply all of our results together:' in sol
        for number,listed in re.findall(r'- Multiples of \$(\d+):\$ \$([^$]+)\$',sol):
            k=int(number);items=[int(x) for x in re.findall(r'\d+',listed)]
            assert all(x%k==0 for x in items) and items==sorted(set(items))
            assert math.lcm(int(a.content()),int(b.content())) in items
    return A,B,expected

def engine_item(r,label):
    f=r['question'][':question/answer-fields'][0]; choices=f[':answer-field/choices'];correct=f[':answer-field/correct'][1]
    _,_,answer=check(r)
    if f[':answer-field/type'].endswith('/radio'):
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'complete bank selection'} for a in choices]
    else:
        canonical=next(a[':answer/value'] for a in choices if a[':answer/id']==correct)
        # Meaningful distinct representations, plus normalization mistakes that divide
        # the inputs in Q[v] but fail the lesson's positive integer-content criterion.
        primitive=sp.Poly(answer,sp.Symbol(r['generation']['parameters']['v'])).primitive()[1].as_expr()
        checks=[{'submitted':canonical,'expected':'accepted','purpose':'canonical'},
                {'submitted':g.tex(answer),'expected':'accepted','purpose':'expanded polynomial equivalent'},
                {'submitted':'('+g.tex(answer)+')/1','expected':'accepted','purpose':'unreduced quotient equivalent'},
                {'submitted':'-('+canonical+')','expected':'rejected','purpose':'wrong sign associate'},
                {'submitted':g.tex(primitive),'expected':'rejected','purpose':'rational-unit LCM loses required integer content'},
                {'submitted':'2*('+canonical+')','expected':'rejected','purpose':'nonleast scalar multiple'},
                {'submitted':'('+canonical+')+1','expected':'rejected','purpose':'wrong polynomial'}]
    return {'label':label,'record':r,'checks':checks}

def main():
    source_cases=[];full_banks=0;choice_count=0;correct_count=0;solution_count=0;source_matches=[];engine=[];reviews=[]
    for sid,c in g.PROFILES.items():
        p={k:c[k] for k in ('a','b','v','h','n')};original=g.QUESTIONS[sid]
        case={'source_id':sid,'template':c['template'],'level':c['level'],'parameters':p,'bank_profile':'observed_'+sid,'derived_profile':'derived_'+sid,'original_rated':':question/difficulty' in original}
        source_cases.append(case)
        raw=g.generate(c['level'],parameters=p,template=c['template'],profile='observed_'+sid)
        check(raw,True);q=raw['question'];sf=original[':question/answer-fields'][0];gf=q[':question/answer-fields'][0]
        assert q[':question/problem']==original[':question/problem'],sid+' prompt'
        for key in (':question/difficulty',':question/worked-solution'):
            assert (key in q)==(key in original),(sid,key,'presence')
        assert gf[':answer-field/key']==sf[':answer-field/key']
        assert gf[':answer-field/type']==sf[':answer-field/type'][':db/ident']
        assert (':answer-field/correct' in gf)==(':answer-field/correct' in sf)
        assert (':answer-field/choices' in gf)==(':answer-field/choices' in sf)
        if ':answer-field/choices' in sf:
            expected=sorted(a[':answer/value'] for a in sf[':answer-field/choices']);actual=sorted(a[':answer/value'] for a in gf[':answer-field/choices'])
            assert actual==expected,(sid,actual,expected)
            full_banks+=1;choice_count+=len(expected)
        if ':answer-field/correct' in sf:
            correctval=next(a[':answer/value'] for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1])
            assert correctval==sf[':answer-field/correct'][':answer/value'];correct_count+=1
        if ':question/worked-solution' in original:
            assert q[':question/worked-solution']==original[':question/worked-solution'],sid+' full solution';solution_count+=1
        derived=g.generate(c['level'],parameters=p,profile='derived_'+sid);check(derived)
        engine.append(engine_item(derived,'source-derived/'+sid));reviews.append({'label':'Original / parameterized raw replay '+sid,'record':raw})
        source_matches.append({'source_id':sid,'exact_prompt':True,'field_shape_presence':True,'full_bank_exact':':answer-field/choices' in sf,'original_correct_designation_matched':':answer-field/correct' in sf,'exact_full_solution':':question/worked-solution' in original,'missing_fields_inferred':c.get('missing',False)})
        # Changed source-profile parameters retain structure and arithmetic masks;
        # Select an explicit changed content pair retaining the exact source
        # exponent/list masks AND its supported coprime/shared-content level.
        changed_pairs={'q-218482':(8,12),'q-76238':(2,7),'q-111582':(3,7),'q-221994':(5,9),'q-221998':(4,12),'q-221999':(6,15),'q-76409':(8,12)}
        ca,cb=changed_pairs[sid]
        changed={**p,'a':ca,'b':cb,'h':2 if p['h']!=2 else -3,'v':'t'}
        variant=g.generate(c['level'],seed=33,parameters=changed,profile='derived_'+sid);check(variant)
        reviews.append({'label':'Generated changed-parameter observed-profile variant '+sid,'record':variant});engine.append(engine_item(variant,'changed-profile/'+sid))
    records=[];identities=set();fingerprints=set();level_tasks={l:set() for l in ('easy','moderate','hard')}
    for sid,c in g.PROFILES.items():
        for seed in range(8):
            r=g.generate(c['level'],seed=seed,profile='derived_'+sid);check(r)
    for level in ('easy','moderate','hard'):
        for template,c in g.TEMPLATES.items():
            if level not in c['levels']:continue
            for seed in range(40):
                r=g.generate(level,seed=seed,template=template);check(r);records.append(r)
                identities.add(r['generation']['content_identity']);fingerprints.add(r['generation']['mathematical_fingerprint']);level_tasks[level].add(r['generation']['mathematical_fingerprint'])
                rerun=g.generate(level,seed=seed+991,template=template,parameters=r['generation']['parameters'])
                assert r['question'][':question/id']==rerun['question'][':question/id'],'identity depends on shuffle'
                if seed<2:
                    reviews.append({'label':f'Generated {level} {template}, seed {seed}','record':r})
                    engine.append(engine_item(r,f'{level}/{template}/{seed}'))
    # Boundaries and invalid explicit input never silently change input.
    invalid=[('easy',{'a':3,'b':9,'v':'x','h':1,'n':2}),('easy',{'a':9,'b':3,'v':'y','h':-2,'n':2}),('easy',{'a':2,'b':6,'v':'w','h':3,'n':2}),('moderate',{'a':2,'b':7,'v':'x','h':1,'n':2}),('easy',{'a':-2,'b':3,'v':'x','h':1,'n':1}),('moderate',{'a':3,'b':6,'v':'x','h':1,'n':1}),('hard',{'a':-6,'b':10,'v':'x','h':4,'n':2,'leading':2,'constant':6}),('hard',{'a':-6,'b':12,'v':'x','h':1,'n':2,'leading':2,'constant':3}),('hard',{'a':6,'b':10,'v':'x','h':1,'n':2,'leading':2,'constant':3}),('hard',{'a':-6,'b':10,'v':'x','h':1,'n':2,'leading':1,'constant':3})]
    for level,p in invalid:
        try:g.generate(level,parameters=p)
        except ValueError:pass
        else:raise AssertionError(('invalid input accepted',level,p))
    profile_rejections=0
    for profile in ('observed_q-111582','derived_q-111582'):
        for p in ({'a':3,'b':9,'v':'x','h':1,'n':2},{'a':9,'b':3,'v':'z','h':-2,'n':2},{'a':4,'b':10,'v':'w','h':3,'n':2}):
            try:g.generate('easy',parameters=p,profile=profile)
            except ValueError:profile_rejections+=1
            else:raise AssertionError(('easy source profile accepts shared content',profile,p))
    for profile in ('observed_q-221999','derived_q-221999'):
        try:g.generate('moderate',parameters={'a':2,'b':7,'v':'z','h':1,'n':2},profile=profile)
        except ValueError:profile_rejections+=1
        else:raise AssertionError(('moderate profile accepts coprime content',profile))
    for profile in ('observed_q-218482','derived_q-218482'):
        try:g.generate('easy',parameters={'a':6,'b':15,'v':'w','h':-8,'n':1},profile=profile)
        except ValueError:profile_rejections+=1
        else:raise AssertionError(('unrated 6/15 wrongly accepted at easy',profile))
    overlap_control=g.generate_moderate(parameters={'a':3,'b':9,'v':'x','h':1,'n':2},field_type='blank')
    control_alias=g.generate_moderate(parameters={'a':9,'b':3,'v':'t','h':1,'n':2},field_type='blank')
    assert overlap_control['generation']['mathematical_fingerprint']==control_alias['generation']['mathematical_fingerprint']
    engine.append(engine_item(overlap_control,'difficulty-boundary/3-and-9-squared-equivalence'))
    reviews.append({'label':'Generated moderate boundary control: 3F / 9F squared (rejected at easy)','record':overlap_control})
    for level,t,p in [('easy','factored_radio',{'a':2,'b':3,'v':'x','h':-9,'n':2}),('moderate','factored_blank',{'a':16,'b':12,'v':'z','h':9,'n':1}),('hard','expanded_content_radio',{'a':-16,'b':12,'v':'w','h':-9,'n':2,'leading':4,'constant':9}),('hard','expanded_content_blank',{'a':6,'b':-10,'v':'x','h':9,'n':2,'leading':2,'constant':-9})]:
        r=g.generate(level,parameters=p,template=t);check(r);engine.append(engine_item(r,'boundary/'+level+'/'+t))
    # raw public APIs retain omitted keys, and absent raw record cannot be fed to
    # native check-engine (which requires owned choices/correct), derived tested above.
    write('source-cases.json',source_cases);write('review.json',reviews);write('engine-input.json',engine)
    subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-validation.json')],check=True)
    engine_report=json.loads((HERE/'engine-validation.json').read_text())
    report={'status':'passed','version':g.VERSION,'source_provenance':{k:v for k,v in g.SOURCE.items() if k!='record'},'source_practice':7,'source_prompt_exact':7,'raw_field_layouts_and_presence_exact':7,'captured_complete_banks_exact':f'{full_banks}/6','captured_answer_values_exact':f'{choice_count}/18','captured_correct_designations_exact':f'{correct_count}/5','captured_shared_solutions_exact':f'{solution_count}/5','derived_missing_answer_keys':2,'authored_missing_difficulty_assignments':2,'authored_missing_worked_solutions':2,'source_replays':source_matches,'normal_instances_independently_checked':len(records),'different_content_identities':len(identities),'different_mathematical_fingerprints':len(fingerprints),'different_mathematical_tasks_per_level':{l:len(ts) for l,ts in level_tasks.items()},'source_profile_random_stage_checks':56,'all_printed_solution_equalities':'independently checked against parsed printed polynomials and ZZ LCM','native_accepted':engine_report['accepted_checks'],'native_rejected':engine_report['rejected_checks'],'native_unresolved':engine_report['documented_unresolved_checks'],'invalid_explicit_parameter_checks':len(invalid),'invalid_source_profile_difficulty_checks':profile_rejections,'easy_moderate_scope':'disjoint coprime versus shared integer content across default and source profiles','unrated_authored_assignments':{'q-218482':'moderate (gcd(6,15)=3, nondividing contents)','q-76238':'easy (gcd(3,5)=1)'},'difficulty_boundary_native_equivalence':'3F/9F squared accepted only as moderate; expanded/quotient answers accepted, wrong content rejected','database_writes':0,'plot_rating':'none','freeze':{'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'sympy':sp.__version__},'parent_qa':'required, pending'}
    write('validation.json',report)
    md=['# Source and generated review','All source replay omissions are preserved; generated/derived solutions are labeled.']
    for entry in reviews: md+=['\n## '+entry['label'],g.markdown(entry['record'])]
    (HERE/'review.md').write_text('\n\n'.join(md)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
