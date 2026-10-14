"""Independent displayed-math readback, fidelity, stage, identity and native checks."""
import copy,hashlib,importlib.util,itertools,json,re,subprocess,sys,uuid
from pathlib import Path
import sympy as sp
D=Path(__file__).resolve().parent;R=D.parents[2]
spec=importlib.util.spec_from_file_location('secant_draft',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
spec=importlib.util.spec_from_file_location('rootF',R/'generate/runs/current/root-source-fidelity.py');F=importlib.util.module_from_spec(spec);spec.loader.exec_module(F)
from scripts.question_capture.math_format import validate_generated_record,validate_prose,validate_tex

def save(name,value):(D/name).write_text(json.dumps(value,ensure_ascii=False,indent=2,default=str)+'\n')
def zero(e):return g.reduced(e)==0

def primitive(e,x):
    # Independent integration by the finite lesson table, from actual printed input.
    table={sp.sec(x)**2:sp.tan(x),sp.sin(x):-sp.cos(x),sp.cos(x):sp.sin(x),sp.sec(x)*sp.tan(x):sp.sec(x),sp.csc(x)*sp.cot(x):-sp.csc(x)}
    out=0
    for term in sp.Add.make_args(sp.expand(e)):
        c,f=term.as_coeff_Mul();assert f in table,('outside lesson direct method',term)
        out+=c*table[f]
    assert zero(sp.diff(out,x)-e)
    return out

def evaluate(text,x):
    # Interpret EVERY formal integral by the independent table, including first
    # distributed rows and all recalled primitives; then read scalar factors.
    text=re.sub(r'\\int\s*(.*?)(?:\\text\{d\}|\\textrm\{?d\}?|d[xyz])\s*(?:\\theta|[xyz])?',lambda m:'('+str(primitive(g.expression(m[1]),x))+')',text)
    return g.expression(text.strip().rstrip('.,'))

def source_math(q):
    e=g.integrand(q[':question/problem']);x=next(iter(e.free_symbols));F0=primitive(e,x)
    total=0
    for f in q.get(':question/answer-fields',[]):
        vals=[g.expression(a[':answer/value']) for a in f[':answer-field/choices']]
        valid=[zero(sp.diff(v,x)-e) for v in vals];assert sum(valid)==1
        for i,v in enumerate(vals):
            # Pairwise equality uses actual antiderivative criterion, modulo constants.
            assert not any(zero(sp.diff(v-w,x)) for w in vals[:i])
            assert not (v.atoms(sp.Function)-set().union(*(w.atoms(sp.Function) for w in vals)))
        if ':answer-field/correct' in f:assert f[':answer-field/choices'][valid.index(True)][':answer/id']==f[':answer-field/correct'][1]
        total+=len(vals)
    return x,e,F0,total

def stages(q,template=None):
    x,e,F0,total=source_math(q)
    if ':question/worked-solution' not in q:return 0
    solution=q[':question/worked-solution'];displays=re.findall(r'\$\$\n(.*?)\n\$\$',solution,re.S);assert displays
    count=0
    for i,display in enumerate(displays):
        display=re.sub(r'\\(?:begin|end)\{aligned\}','',display)
        prev=None
        for line in display.split(r'\\'):
            line=line.strip()
            if not line:continue
            assert line.count('=')==1,line
            left,right=line.replace('&','').split('=')
            if left.strip():prev=evaluate(left,x)
            assert prev is not None
            rhs=evaluate(right,x)
            assert zero(sp.diff(prev-rhs,x)),('bad displayed stage',line)
            if i==len(displays)-1:assert zero(sp.diff(rhs,x)-e),('wrong main stage',line)
            prev=rhs;count+=1
    # Operative stages stay ordered, independent of mathematical equality.
    if template:
        chain=displays[-1]
        rr=chain.split(r'\\')
        expected={'q-113936':2,'q-113937':3,'q-113944':3,'q-2164':3,'q-49122':4,'fraction':3,'single-positive':2,'sine-sum':3,'secant-difference':2,'reverse-product':4,'three-term-plus':5,'three-term-minus':5}
        assert len(rr)==expected[template],('operative stage count',template)
        if template in ('q-49122','reverse-product','three-term-plus','three-term-minus'):
            lhs,rhs=rr[0].split('=');assert '(' in lhs and '(' in rhs and r'\int' in rhs,'distribution stage absent'
            assert rr[1].count(r'\int')==(3 if template.startswith('three-term') else 2),'termwise split stage absent'
        if template.startswith('three-term'):
            assert rr[2].count(r'\int')==3 and re.search(r'\d+\\int',rr[2]),'constant-extraction stage absent'
            assert r'(-\csc x)' in rr[3] and r'\int' not in rr[3],'component primitive/sign stage absent'
        if template in ('q-49122','reverse-product'):assert rr[2].count(r'\int')==2 and re.search(r'\d+\\int',rr[2]),'constant-extraction stage absent'
    return count

def independent(r):
    q=r['question'];m=r['generation'];assert set(r['knowledge_point'])=={'db_id','id','title'}
    assert r['knowledge_point']['db_id']==g.KP_ID and r['knowledge_point']['id']==g.KP_UUID
    for text in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices']]:
        assert all(ord(c)>=32 or c in '\n\t' for c in text),'control character'
        assert '@' not in text and '{a}' not in text and '{b}' not in text,'unfilled mask'
    validate_prose(q[':question/problem'])
    if ':question/worked-solution' in q:validate_prose(q[':question/worked-solution'])
    for f in q.get(':question/answer-fields',[]):
        for a in f[':answer-field/choices']:validate_tex(a[':answer/value'])
    assert m['parameter_fingerprint']==g.fingerprint_text(q[':question/problem'])
    # Recalculate actual displayed-content identity (all banks/feedback/keys included).
    bare=copy.deepcopy(q);bare.pop(':question/id')
    for f in bare.get(':question/answer-fields',[]):
        f.pop(':answer-field/id')
        if ':answer-field/correct' in f:f[':answer-field/correct']=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        for a in f[':answer-field/choices']:a.pop(':answer/id')
        f[':answer-field/choices']=sorted(f[':answer-field/choices'],key=lambda a:json.dumps(a,sort_keys=True))
    assert m['content_fingerprint']==g.digest([g.VERSION,bare])
    ids=[q[':question/id']]+[f[':answer-field/id'] for f in q.get(':question/answer-fields',[])]+[a[':answer/id'] for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices']]
    assert len(ids)==len(set(ids))
    for v in ids:uuid.UUID(v)
    if not m['evidence_only']:
        validate_generated_record(r);assert m['eligible_for_learning'];assert q[':question/difficulty']==':question.difficulty/'+g.TEMPLATES[m['template']]['difficulty']
        steps=stages(q,m['template'])
    else:
        assert not m['eligible_for_learning'];steps=stages(q)
    return steps

def engine_checks(r):
    f=r['question'][':question/answer-fields'][0]
    return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Actual learner grade_field, every field-owned radio ID'} for a in f[':answer-field/choices']]

def unchanged():
    baseline=json.load(open(D/'registered-baseline-hashes.json'));files=[D.parent/'17592186064180.py']+sorted(p for p in (D.parent/'17592186064180').rglob('*') if p.is_file())
    assert sorted(str(p.relative_to(R)) for p in files)==sorted(baseline['paths'])
    for p in files:assert hashlib.sha256(p.read_bytes()).hexdigest()==baseline['sha256'][str(p.relative_to(R))]
    save('registered-baseline-verification.json',{'status':'unchanged','pathset_unchanged':True,'files_checked':len(files),'sha256':baseline['sha256']})

def main():
    unchanged();originals,counts=F.check(g,g.KP_ID,D)
    records=[];reviews=[];raw=[];steps=0;negative=0;slot_coverage={};source_equivalence=0
    for c in json.load(open(D/'source-cases.json')):
        replay=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['profile']);steps+=independent(replay);raw.append(replay);source_equivalence+=source_math(replay['question'])[3]
        # Changed parameters exercise every complete raw mask, not a source lookup.
        p={k:(v+1 if v<9 else v-1) for k,v in c['parameters'].items()}
        if c['template']=='q-49118':p={'a':6}
        if c['template']=='q-113935':p={'n':5,'d':3}
        changed=g.generate(c['level'],template=c['template'],parameters=p,profile=c['profile']);steps+=independent(changed)
        reviews.append({'label':c['source_id']+' original / exact raw replay / changed raw evidence','original':originals[c['source_id']],'replay':replay,'variant':changed})
    # ALL default families, meaningful boundaries and slot perturbations.
    for level,names in g.DEFAULTS.items():
        for name in names:
            for seed in range(6):
                r=g.generate(level,seed=seed+137,template=name);steps+=independent(r);records.append(r)
            keys=list(records[-1]['generation']['parameters']);low={k:1 for k in keys};high={k:9 for k in keys}
            if name in ('q-113936','q-113937','single-positive'):low={'a':2}
            if name=='fraction':low={'n':2,'d':3};high={'n':9,'d':8}
            if name in ('sine-sum','secant-difference','reverse-product'):low={k:2 for k in keys}
            for p in (low,high):
                r=g.generate(level,template=name,parameters=p);steps+=independent(r);records.append(r)
            slot_coverage[name]={k:sorted({r['generation']['parameters'][k] for r in records if r['generation']['template']==name}) for k in keys}
            a=g.generate(level,template=name,parameters=high,seed=1);b=g.generate(level,template=name,parameters=high,seed=41)
            assert a['question'][':question/id']==b['question'][':question/id']
            assert a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint']
            assert a['question'][':question/answer-fields'][0][':answer-field/choices']!=b['question'][':question/answer-fields'][0][':answer-field/choices']
            # Public aliases must not change identity.
            assert a['question'][':question/id']==g.generate(level,profile=name,parameters=high,seed=1)['question'][':question/id']
            variants=[r for r in records if r['generation']['template']==name][:2];reviews.append({'label':name+' authored/generated variants','records':variants})
    for level in g.SUPPORTED_LEVELS:
        sampled=[g.generate(level,seed=i) for i in range(48)]
        assert set(g.DEFAULTS[level])=={r['generation']['template'] for r in sampled},'default family coverage'
        assert len({r['generation']['parameter_fingerprint'] for r in sampled})>=12
        records.extend(sampled)
    # Same task across variable spelling/bank masks deduplicates semantically.
    a=g.generate('easy',template='q-113936',parameters={'a':3});b=g.generate('easy',template='single-positive',parameters={'a':3})
    assert a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint']
    assert a['question'][':question/id']!=b['question'][':question/id'],'different displayed banks must differ'
    bad=[('easy','q-113936',{'a':1}),('easy','fraction',{'n':4,'d':2}),('easy','fraction',{'n':3,'d':3}),('moderate','sine-sum',{'a':1,'b':4}),('hard','three-term-plus',{'a':0,'b':4,'c':2}),('hard','three-term-minus',{'a':2,'b':4,'c':10}),('hard','q-49122',{'a':2,'b':4}),('easy','single-positive',{'a':True}),('easy','single-positive',{'a':3,'unused':8})]
    for level,name,p in bad:
        try:g.generate(level,template=name,parameters=p)
        except ValueError:negative+=1
        else:raise AssertionError('invalid public parameter accepted')
    specimen=g.generate('hard',template='three-term-minus',parameters={'a':3,'b':4,'c':5})
    for part in ('correct','wrong','distribution','constant-stage','component-sign','control','conclusion'):
        r=copy.deepcopy(specimen);q=r['question'];f=q[':question/answer-fields'][0]
        if part=='correct':next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])[':answer/value']='0+C'
        elif part=='wrong':next(a for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])[':answer/value']=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])+'+7'
        elif part=='distribution':q[':question/worked-solution']=q[':question/worked-solution'].replace('3{sec}^{2}x+4', '3{sec}^{2}x-4',1)
        elif part=='constant-stage':
            # Algebraically equal replacement with removed teaching operation.
            q[':question/worked-solution']=q[':question/worked-solution'].replace(r'3\int {sec}^{2}x\,\text{d}x+4\int \sec x\tan x\,\text{d}x-5\int \csc x\cot x\,\text{d}x',r'\int (3{sec}^{2}x+4\sec x\tan x-5\csc x\cot x)\,\text{d}x')
        elif part=='component-sign':q[':question/worked-solution']=q[':question/worked-solution'].replace(r'-5(-\csc x)',r'-5(\csc x)')
        elif part=='control':q[':question/worked-solution']+='\f'
        elif part=='conclusion':q[':question/worked-solution']=q[':question/worked-solution'].replace(r'+5\csc x+C.',r'+6\csc x+C.')
        assert r!=specimen,'mutation must actually change learner bytes: '+part
        try:
            if part=='control':independent(r)
            else:stages(q,'three-term-minus')
        except (AssertionError,ValueError,SyntaxError):negative+=1
        else:raise AssertionError('corruption accepted: '+part)
    inputs=[{'label':str(i)+'/'+r['generation']['template'],'record':r,'checks':engine_checks(r)} for i,r in enumerate(records)]
    # Raw complete keys grade; missing keys/fields remain explicitly ineligible.
    inputs.extend({'label':'raw/'+r['generation']['template'],'record':r,'checks':engine_checks(r)} for r in raw if r['question'].get(':question/answer-fields') and ':answer-field/correct' in r['question'][':question/answer-fields'][0])
    save('engine-input.json',inputs);subprocess.run([str(R/'generate/runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True,timeout=60)
    engine=json.load(open(D/'engine-report.json'));assert engine['documented_unresolved_checks']==0
    # Enumerate actual meaningful integrand domain independently, without aliases.
    tasks={l:set() for l in g.SUPPORTED_LEVELS}
    for level,names in g.DEFAULTS.items():
        for name in names:
            p=g.sample(name,__import__('random').Random(0));keys=list(p)
            for values in itertools.product(range(1,10),repeat=len(keys)):
                try:p=g.validate_parameters(name,dict(zip(keys,values)))
                except ValueError:continue
                q=g.normal(name,p);tasks[level].add(g.fingerprint_text(q[':question/problem']))
    save('review.json',reviews)
    out=[]
    for row in reviews:
        out.append('## '+row['label'])
        if 'original' in row:
            q=row['original'];out.append('Original captured evidence:\n\n'+q[':question/problem']+'\n\n'+q.get(':question/worked-solution','[Absent]'));out.append('Exact raw replay:\n\n'+g.markdown(row['replay']));out.append('Changed raw evidence (ineligible for learning):\n\n'+g.markdown(row['variant']))
        else:
            for r in row['records']:out.append('Generated variant:\n\n'+g.markdown(r))
    (D/'review.md').write_text('\n\n'.join(out)+'\n')
    unchanged()
    save('validation.json',{'status':'pass','basis':g.SOURCE_BASIS,'source_fidelity':counts,'complete_original_banks':7,'original_bank_values_mathematically_checked':source_equivalence,'mathematics':{'normal_records':len(records),'source_records':len(raw),'displayed_rows_checked':steps,'negative_controls':negative,'semantic_domain_counts':{l:len(s) for l,s in tasks.items()},'slot_coverage':slot_coverage},'native_grading':{k:engine[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'ineligible_source_profiles':['q-2035 missing key/solution/level','q-49118 missing key/solution/level and opaque cross-function half-scale pattern','q-113935/q-2162/q-2165 missing fields (normal completions labeled authored)'],'authored_missing_level':'Hard: three existing direct primitive terms, one source-shaped distribution, same variable; calibration is authored and uncertain.','versions':{'python':sys.version.split()[0],'sympy':sp.__version__},'hashes':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (D.with_suffix('.py'),Path(__file__),D/'source.json',D/'source-profiles.json',R/'generate/runs/current/check-engine')}})
    print(json.dumps({'status':'pass','source_fidelity':counts,'tasks':{l:len(s) for l,s in tasks.items()},'native_checks':len(inputs)*5,'negative_controls':negative}))
if __name__=='__main__':main()
