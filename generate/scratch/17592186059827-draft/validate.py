"""Independent displayed finite-set readback, source fidelity, native radio grading."""
from pathlib import Path
import copy,hashlib,importlib.util,json,re,subprocess,sys,uuid
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('half_open_draft',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,obj): (HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def clean(s):
    s=s.strip().removesuffix('.').replace(r'\,','').replace(r'\leq',r'\le').replace(r'\lt','<').replace(r'\geq',r'\ge').replace(r'\gt','>')
    return re.sub(r'\\in(?![A-Za-z])','∈',s)
def endpoint(s):
    s=s.replace(' ','')
    if s==r'\infty':return sp.oo
    if s==r'-\infty':return -sp.oo
    s=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',s)
    s=re.sub(r'\\sqrt(?:\{(\d+)\}|(\d+))',lambda m:'*sqrt('+(m[1] or m[2])+')',s)
    s=s.removeprefix('*').replace('-*sqrt','-sqrt')
    assert re.fullmatch(r'[-0-9()+*/sqrt]+',s),s
    return sp.sympify(s)
def parse(text,variable=None):
    text=clean(text)
    if text.startswith(('(','[')):
        assert variable is not None;text=variable+'∈'+text
    if '∈' in text:
        v,rest=text.split('∈');rest=rest.strip();assert rest[0] in '([' and rest[-1] in ')]'
        aa,bb=rest[1:-1].split(',');a,b=endpoint(aa),endpoint(bb);lc=rest[0]=='[';rc=rest[-1]==']'
    else:
        text=text.replace(r'\le','≤').replace(r'\ge','≥')
        parts=re.split(r'\s*(≤|≥|<|>)\s*',text);assert len(parts)==5,text
        aa,op,v,op2,bb=parts
        if op in ('>','≥'):
            assert op2 in ('>','≥');aa,bb=bb,aa;op,op2=op2,op;lc=op=='≥';rc=op2=='≥'
        else:assert op2 in ('<','≤');lc=op=='≤';rc=op2=='≤'
        a,b=endpoint(aa),endpoint(bb)
    v=v.strip();assert v in ('x','y','t','u'),v
    return (sp.EmptySet if a>b else sp.Interval(a,b,left_open=not lc,right_open=not rc)),(a,b,v,lc,rc)
def prompt_info(q):
    block=re.search(r'\$(.*?)\$',q[':question/problem']);assert block
    return parse(block[1])
def enum(x):return x[':db/ident'] if isinstance(x,dict) else x
def task(q):
    _,(a,b,v,lc,rc)=prompt_info(q)
    return (str(a),str(b),lc,'interval_to_inequality' if '∈' in clean(re.search(r'\$(.*?)\$',q[':question/problem'])[1]) else 'inequality_to_interval')
def inspect(r):
    assert r['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    q=r['question'];uuid.UUID(q[':question/id']);assert len(q[':question/answer-fields'])==1
    f=q[':question/answer-fields'][0];uuid.UUID(f[':answer-field/id']);assert enum(f[':answer-field/type'])==':answer-field.type/radio' and f[':answer-field/key']=='selection'
    target,info=prompt_info(q);a,b,var,lc,rc=info;assert a<b and lc!=rc
    choices=f[':answer-field/choices'];assert len(choices)==5
    sets=[]
    for choice in choices:
        value,ci=parse(choice[':answer/value']);assert ci[2]==var
        sets.append(value);uuid.UUID(choice[':answer/id']);assert enum(choice[':answer/type'])==':answer.type/math'
        g.fmt.validate_tex(choice[':answer/value']);assert g.fmt.normalize_tex(choice[':answer/value'])==choice[':answer/value']
    assert len(set(sets))==5 and sets.count(target)==1
    expected=g.digest({'a':str(a),'b':str(b),'left_closed':lc,'direction':task(q)[3]});assert expected==r['generation']['mathematical_fingerprint']
    g.fmt.validate_prose(q[':question/problem'])
    if r['generation']['raw_missing_fields_preserved']:
        assert ':answer-field/correct' not in f and ':question/difficulty' not in q and ':question/worked-solution' not in q
        return 0
    key=f[':answer-field/correct'];assert key[0]==':answer/id'
    match=[c for c in choices if c[':answer/id']==key[1]];assert len(match)==1 and parse(match[0][':answer/value'])[0]==target
    assert enum(q[':question/difficulty'])==':question.difficulty/'+r['generation']['difficulty']
    sol=q[':question/worked-solution'];g.fmt.validate_prose(sol)
    blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);assert len(blocks)==2
    for block in blocks:
        val,bi=parse(block,var);assert val==target and bi==info,(block,bi,info)
    for side,index,closed in [('left',0,lc),('right',1,rc)]:
        m=re.search('The '+side+r' endpoint \$(.*?)\$ (.*?) included in the interval. Therefore, we use \$(.*?)\$',sol)
        assert m and endpoint(m[1])==info[index]
        assert ('not' in m[2])==(not closed)
        sym=clean(m[3]).strip()
        expected=(('[' if closed else '(') if side=='left' else (']' if closed else ')')) if task(q)[3]=='inequality_to_interval' else (r'\le' if closed else '<')
        assert sym==expected,(sym,expected)
    # Ordered stages: notation convention, displayed given, left decision, right decision, conclusion.
    assert sol.index('Parentheses')<sol.index('Brackets')<sol.index('For the given')<sol.index('The left endpoint')<sol.index('The right endpoint')<sol.rindex('Therefore,')
    assert sol.count('The left endpoint')==sol.count('The right endpoint')==1
    return 2

def fixture_from_source(q):
    sid=q.get(':question/math-academy-id',str(q[':db/id']));_,(a,b,v,lc,rc)=prompt_info(q)
    direction=task(q)[3];level=enum(q.get(':question/difficulty',':question.difficulty/'+('hard' if sid=='q-25754' else 'easy'))).split('/')[-1]
    profile={'q-1253':'observed_1253_raw','q-25754':'observed_25754_raw','q-28834':'observed_28834','q-73902':'observed_73902'}.get(sid,'authored_endpoint_bank')
    r=g.generate(level,template=direction,profile=profile,parameters={'a':str(a),'b':str(b),'variable':v,'left_closed':lc})
    return {'source_id':sid,'record':r}

def main():
    source=json.loads((HERE/'source.json').read_text());assert source['basis']==2275
    questions=source['record'][':knowledge-point/questions'];assert len(questions)==17
    fixtures=[fixture_from_source(q) for q in questions];save('source-cases.json',[f for f in fixtures if str(f['source_id']).startswith('q-')])
    fidelity=[];stages=0
    for q,fixture in zip(questions,fixtures):
        r=fixture['record'];stages+=inspect(r);out=r['question'];sf=q[':question/answer-fields'][0];f=out[':question/answer-fields'][0]
        raw_prompt=out[':question/problem']==q[':question/problem'];assert out[':question/problem']==g.fmt.normalize_prose(q[':question/problem'])
        assert len(f[':answer-field/choices'])==len(sf[':answer-field/choices'])==5
        # Full mathematical objects and displayed normalized notation separately.
        source_bank=[parse(x[':answer/value'])[0] for x in sf[':answer-field/choices']]
        generated_bank=[parse(x[':answer/value'])[0] for x in f[':answer-field/choices']]
        assert sorted(map(str,source_bank))==sorted(map(str,generated_bank))
        assert sorted(g.fmt.normalize_tex(x[':answer/value']) for x in sf[':answer-field/choices'])==sorted(x[':answer/value'] for x in f[':answer-field/choices'])
        assert f[':answer-field/key']==sf[':answer-field/key'] and enum(sf[':answer-field/type'])==f[':answer-field/type']
        for attr in (':question/worked-solution',':question/difficulty'):
            original=enum(q.get(attr));normal=g.fmt.normalize_prose(original) if attr==':question/worked-solution' and original is not None else original
            assert out.get(attr)==normal,(fixture['source_id'],attr)
        if ':answer-field/correct' in sf:
            key=next(x for x in f[':answer-field/choices'] if x[':answer/id']==f[':answer-field/correct'][1])
            assert parse(key[':answer/value'])[0]==parse(sf[':answer-field/correct'][':answer/value'])[0]
        else:assert ':answer-field/correct' not in f
        fidelity.append({'source_id':fixture['source_id'],'raw_prompt_exact':raw_prompt,'normalized_prompt_exact':True,'normalized_bank_choices':5,'complete_mathematical_bank_match':True,'raw_solution_exact':out.get(':question/worked-solution')==q.get(':question/worked-solution'),'normalized_solution_and_ordered_stages_match':True,'key_and_difficulty_presence_and_values_match':True})
    records=[];coverage={}
    for level in g.LEVELS:
        rs=g.generate_many(level,seed=174,count=120)
        assert len({task(r['question']) for r in rs})==120
        for r in rs:stages+=inspect(r)
        records+=rs
        coverage[level]={'tasks_sampled':120,'capacity':len(g._CATALOG[level])*2,'directions':sorted({task(r['question'])[3] for r in rs}),'left_closed':sorted({task(r['question'])[2] for r in rs}),'lower_signs':sorted({int(sp.sign(prompt_info(r['question'])[1][0])) for r in rs}),'upper_signs':sorted({int(sp.sign(prompt_info(r['question'])[1][1])) for r in rs})}
        assert len(coverage[level]['directions'])==len(coverage[level]['left_closed'])==2
    # Independent same-endpoint closure/direction/variable probes catch stale keyed targets.
    probes=[]
    for level,a,b in [('easy','-7','4'),('moderate','-7/3','4/5'),('hard','-2*sqrt(3)','sqrt(5)')]:
        for c in (False,True):
            for t in g.TEMPLATES:
                for v in ('x','y','t','u'):
                    r=g.generate(level,31,template=t,parameters={'a':a,'b':b,'left_closed':c,'variable':v});stages+=inspect(r);probes.append(r)
    profiles=[]
    for prof,level,t,a,b,c in [('observed_1253_raw','easy','inequality_to_interval','3','11',False),('observed_1253','easy','inequality_to_interval','3','11',False),('observed_25754_raw','hard','interval_to_inequality','-6','3*sqrt(2)',True),('observed_25754','hard','interval_to_inequality','-6','3*sqrt(2)',True),('observed_28834','easy','inequality_to_interval','-7','0',True),('observed_28834','easy','inequality_to_interval','0','15',True),('observed_73902','moderate','interval_to_inequality','-3','2',True),('observed_73902','moderate','interval_to_inequality','-1','15',True)]:
        r=g.generate(level,32,template=t,profile=prof,parameters={'a':a,'b':b,'variable':'t','left_closed':c});stages+=inspect(r);profiles.append(r)
    for original in list(profiles):
        m=original['generation'];p=dict(m['parameters']);p['left_closed']=not p['left_closed']
        changed=g.generate(m['difficulty'],44,template=m['template'],profile=m['profile'],parameters=p);stages+=inspect(changed);profiles.append(changed)
    # Preserve semantic identity under seed/variable/profile aliases and exact number spelling.
    for r in records[:30]+probes:
        m=r['generation'];again=g.generate(m['difficulty'],999,m['template'],parameters=m['parameters'],profile=m['profile'])
        assert again['question'][':question/id']==r['question'][':question/id']
    p={'a':'-1/2','b':'3/2','left_closed':True,'variable':'x'};a=g.generate('moderate',parameters=p);p['a']='-2/4';b=g.generate('moderate',parameters=p);assert a['question'][':question/id']==b['question'][':question/id']
    p['variable']='y';b=g.generate('moderate',parameters=p,template=a['generation']['template']);assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
    a=g.generate('easy',template='inequality_to_interval',parameters={'a':'3','b':'11','variable':'x','left_closed':False});b=g.generate('easy',template='inequality_to_interval',profile='observed_1253',parameters=a['generation']['parameters']);assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
    # Orientation and endpoint closures are mathematical, not textual comparisons.
    assert parse(r'13 \ge x > 9')[0]==parse('x ∈ (9,13]')[0]
    assert parse(r'13 > x \ge 9')[0]!=parse('x ∈ (9,13]')[0]
    negative=[]
    base=g.generate('easy',template='inequality_to_interval',parameters={'a':'-7','b':'4','variable':'x','left_closed':True})
    for kind in ('wrong_key','bad_given_endpoint_final_correct','stale_variable_final_correct','wrong_inclusion_final_correct','wrong_symbol_final_correct','stale_endpoint_statement_final_correct'):
        bad=copy.deepcopy(base);q=bad['question'];f=q[':question/answer-fields'][0];sol=q[':question/worked-solution']
        if kind=='wrong_key':f[':answer-field/correct'][1]=next(c[':answer/id'] for c in f[':answer-field/choices'] if c[':answer/id']!=f[':answer-field/correct'][1])
        elif kind=='bad_given_endpoint_final_correct':q[':question/worked-solution']=sol.replace('-7 \\le x < 4','-6 \\le x < 4',1)
        elif kind=='stale_variable_final_correct':q[':question/worked-solution']=sol.replace('\\le x <','\\le y <',1)
        elif kind=='wrong_inclusion_final_correct':q[':question/worked-solution']=sol.replace('endpoint $-7$ *is*','endpoint $-7$ *is not*',1)
        elif kind=='wrong_symbol_final_correct':q[':question/worked-solution']=sol.replace('we use $[$','we use $($',1)
        else:q[':question/worked-solution']=sol.replace('endpoint $-7$','endpoint $-6$',1)
        assert bad!=base,kind
        try:inspect(bad)
        except AssertionError:negative.append(kind)
        else:raise AssertionError('Accepted mutation '+kind)
    guards=0
    def fails(fn):
        nonlocal guards
        try:fn()
        except (ValueError,TypeError):guards+=1
        else:raise AssertionError('Expected guard rejection')
    for seed in (True,1.0,'1',None):fails(lambda seed=seed:g.generate('easy',seed))
    for count in (True,1.0,'1',0,-1):fails(lambda count=count:g.generate_many('easy',count=count))
    for l in g.LEVELS:fails(lambda l=l:g.generate_many(l,count=len(g._CATALOG[l])*2+1))
    invalid=[('easy','authored_endpoint_bank','inequality_to_interval','-16','3',True),('moderate','authored_endpoint_bank','interval_to_inequality','-1','3',True),('hard','authored_endpoint_bank','interval_to_inequality','-1','3',True),('hard','authored_endpoint_bank','interval_to_inequality','-sqrt(2)/2','3',True),('hard','authored_endpoint_bank','interval_to_inequality','sqrt(2)','3',True),('easy','observed_25754','interval_to_inequality','-5','2*sqrt(2)',True),('hard','observed_1253','inequality_to_interval','9','13',False),('moderate','observed_1253','inequality_to_interval','3','11',False),('moderate','observed_73902','interval_to_inequality','-2','2',True)]
    for l,p,t,a,b,c in invalid:fails(lambda l=l,p=p,t=t,a=a,b=b,c=c:g.generate(l,template=t,profile=p,parameters={'a':a,'b':b,'variable':'x','left_closed':c}))
    # CLI JSON always returns a list; count applies separately to each selected level.
    for form in ('json','markdown'):
        run=subprocess.run([sys.executable,'-B',str(HERE.with_suffix('.py')),'--difficulty','all','--count','1','--format',form],check=True,text=True,capture_output=True)
        if form=='json':assert isinstance(json.loads(run.stdout),list) and len(json.loads(run.stdout))==3
        else:assert run.stdout.count('The inequality')+run.stdout.count('The interval')>=3
    # Native radio grading submits owned answer IDs. Genuine algebraic-equivalent string
    # entry is not a radio response contract; all complete canonical+wrong choices tested.
    normal=[f['record'] for f in fixtures if not f['record']['generation']['raw_missing_fields_preserved']]+records+probes+[r for r in profiles if not r['generation']['raw_missing_fields_preserved']]
    engine=[]
    for index,r in enumerate(normal):
        f=r['question'][':question/answer-fields'][0];key=f[':answer-field/correct'][1]
        engine.append({'label':str(index),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key else 'rejected','purpose':'complete displayed bank, independently read as sets'} for a in f[':answer-field/choices']]})
    save('native-input.json',engine);subprocess.run([str(HERE/'reference/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
    save('variants.json',{'sampled':records,'same_endpoint_roles':probes,'changed_profile_cases':profiles})
    save('review.json',{'originals':fixtures,'variants':[next(r for r in records if r['generation']['difficulty']==l and r['generation']['template']==t) for l in g.LEVELS for t in g.TEMPLATES]+profiles})
    review=json.loads((HERE/'review.json').read_text());(HERE/'review.md').write_text('\n\n---\n\n'.join('Original '+f['source_id']+'\n\n'+g.markdown(f['record']) for f in fixtures)+'\n\n---\n\n'+ '\n\n---\n\n'.join('Authored/changed variant '+r['generation']['profile']+' / '+r['generation']['difficulty']+'\n\n'+g.markdown(r) for r in review['variants']))
    baseline=json.loads((HERE/'reference/registered-baseline.json').read_text());assert all(hashlib.sha256(Path(f['path']).read_bytes()).hexdigest()==f['sha256'] for f in baseline['files'])
    baseline_paths={f['path'] for f in baseline['files']}
    registered_paths={str(p) for p in Path('generate/scratch/17592186059827').rglob('*') if p.is_file()}|{'generate/scratch/17592186059827.py'}|{str(p) for p in Path('generate/scratch/__pycache__').glob('17592186059827*') if p.is_file()}
    assert registered_paths==baseline_paths,'Registered directory or cache inventory changed'
    report={'passed':True,'source_basis':2275,'source_fidelity':fidelity,'original_records':17,'MA_originals':4,'prior_generated_lineage_records':13,'complete_banks':17,'choices_matched':85,'records_mathematically_inspected':len(fixtures)+len(records)+len(probes)+len(profiles),'complete_displayed_choices_inspected':5*(len(fixtures)+len(records)+len(probes)+len(profiles)),'captured_keys_solutions':15,'MA_observed_keys_solutions':2,'prior_generated_keys_solutions':13,'raw_missing_key_solution_difficulty_preserved':2,'sampled':len(records),'same_endpoint_role_probes':len(probes),'changed_profiles':len(profiles),'solution_set_stages':stages,'coverage':coverage,'negative_controls':negative,'guard_rejections':guards,'native':{k:v for k,v in json.loads((HERE/'native-report.json').read_text()).items() if k!='records'},'registered_baseline_files_unchanged':len(baseline['files']),'database_writes':0,'remaining_limits':['Two MA originals have no captured key, rating or solution and remain native-grading ineligible.','Moderate rational and hard surd levels are authored; generated lineage records are not independent MA evidence.','Radio fields grade owned option IDs; expression-entry equivalents are outside the response contract.'],'root_independent_QA_required':True}
    save('validation.json',report);print(json.dumps({k:v for k,v in report.items() if k not in ('source_fidelity','coverage')},indent=2))
if __name__=='__main__':main()
