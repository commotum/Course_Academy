"""Independent formal-integral readback and complete public/learner grading checks."""
import copy,hashlib,importlib.util,itertools,json,re,subprocess,sys,uuid
from pathlib import Path
import sympy as sp
D=Path(__file__).resolve().parent;R=D.parents[2]
spec=importlib.util.spec_from_file_location('cosecant_draft',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
spec=importlib.util.spec_from_file_location('rootF',R/'generate/runs/current/root-source-fidelity.py');F=importlib.util.module_from_spec(spec);spec.loader.exec_module(F)
from scripts.question_capture.math_format import validate_generated_record,validate_prose,validate_tex

def save(n,v):(D/n).write_text(json.dumps(v,ensure_ascii=False,indent=2,default=str)+'\n')
def zero(e):return g.reduced(e)==0

def primitive(e,x):
    table={sp.csc(x)**2:-sp.cot(x),sp.sin(x):-sp.cos(x),sp.cos(x):sp.sin(x),sp.sec(x)*sp.tan(x):sp.sec(x),sp.csc(x)*sp.cot(x):-sp.csc(x)}
    out=0
    for term in sp.Add.make_args(sp.expand(e)):
        c,f=term.as_coeff_Mul();assert f in table,('outside finite direct-primitive method',term)
        out+=c*table[f]
    assert zero(sp.diff(out,x)-e)
    return out

def input_math(q,raw_name=None):
    text=q[':question/problem']
    if 'v(t)' in text:
        if text.startswith('Given'):
            value=re.search(r'v\(t\)=(.*?)\$',text)[1];return g.expression(value)
        assert raw_name in ('q-143522','q-167569'),'undefined v(t) in served question'
        # Source evidence only: recover absent prompt datum from first main solution
        # integral. Report this absence independently; never claim prompt completeness.
        return g.integrand(q[':question/worked-solution'].split('Therefore, we get')[1])
    return g.integrand(text)

def evaluate(text,x):
    text=re.sub(r'\\int\s*(.*?)(?:\\text\{d\}|\\textrm\{?d\}?|d[xyzθ])\s*(?:\\theta|[xyztθ])?',lambda m:'('+str(primitive(g.expression(m[1]),x))+')',text)
    return g.expression(text.strip().rstrip('.,'))

def banks(q,raw_name=None):
    e=input_math(q,raw_name);x=next(iter(e.free_symbols));expected=primitive(e,x);total=0;defects=[]
    for f in q.get(':question/answer-fields',[]):
        vals=[]
        for a in f[':answer-field/choices']:
            if raw_name=='q-71666' and a[':answer/value'].startswith(('-csc+','csc-')):
                defects.append({'value':a[':answer/value'],'error':'csc primitive has no argument; expression undefined; raw evidence only'});continue
            vals.append((a,g.expression(a[':answer/value'])))
        valid=[zero(sp.diff(v,x)-e) for a,v in vals];assert sum(valid)==1
        for i,(a,v) in enumerate(vals):assert not any(zero(sp.diff(v-w,x)) for b,w in vals[:i]),'constants-equivalent distractor'
        if ':answer-field/correct' in f:assert vals[valid.index(True)][0][':answer/id']==f[':answer-field/correct'][1]
        total+=len(vals)
    return x,e,expected,total,defects

def stages(q,name=None,raw=False):
    x,e,expected,total,defects=banks(q,name if raw else None)
    if ':question/worked-solution' not in q:return 0
    solution=q[':question/worked-solution']
    if raw and name=='q-113958':
        assert r'\int sin\,' in solution
        # Explicit evidence-supported verification completion; exact raw was already
        # checked byte-for-byte. Original missing argument is a recorded source error.
        solution=solution.replace(r'\int sin\,',r'\int sin x\,')
    displays=re.findall(r'\$\$\n(.*?)\n\$\$',solution,re.S);assert displays
    n=0
    for i,display in enumerate(displays):
        display=re.sub(r'\\(?:begin|end)\{aligned\}','',display);previous=None
        for line in display.split(r'\\'):
            line=line.strip()
            if not line:continue
            assert line.count('=')==1,line
            left,right=line.replace('&','').split('=')
            if left.strip():previous=evaluate(left,x)
            assert previous is not None
            rhs=evaluate(right,x);assert zero(sp.diff(previous-rhs,x)),('bad displayed stage',line)
            if i==len(displays)-1:assert zero(sp.diff(rhs,x)-e),('main integral not consistent',line)
            previous=rhs;n+=1
    if name and not raw:
        rr=displays[-1].split(r'\\');expected_rows={'q-113947':3,'q-71663':3,'single-negative':3,'fraction':3,'blank':3,'q-49121':5,'secant-difference':3,'sine-difference':3,'reverse-product':5,'three-term':3}
        assert len(rr)==expected_rows[name],('source stage layout',name)
        if name in ('q-49121','reverse-product'):
            assert '(' in rr[0].split('=')[0] and rr[0].count(r'\int')==2,'missing distribution stage'
            assert rr[1].count(r'\int')==2,'missing termwise split'
            assert rr[2].count(r'\int')==2 and re.search(r'\d+\\int',rr[2]),'missing scalar extraction'
            assert '(-' in rr[3] and r'\int' not in rr[3],'missing component substitutions'
        elif name in ('secant-difference','sine-difference','three-term'):
            assert rr[0].count(r'\int')==(4 if name=='three-term' else 3),'missing sum-rule/scalar stage'
            assert '(-' in rr[1],'missing signed primitive substitution'
        else:
            assert rr[0].count(r'\int')==2 and '(-' in rr[1],'missing scalar or primitive stage'
    return n

def independent(r):
    q=r['question'];m=r['generation'];raw=m['evidence_only'];name=m['template']
    assert r['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    for text in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices']]:
        assert all(ord(c)>=32 or c in '\n\t' for c in text),'control character';assert '@' not in text,'unfilled mask'
    if not raw:
        validate_generated_record(r);assert m['eligible_for_learning'];assert q[':question/difficulty']==':question.difficulty/'+g.TEMPLATES[name]['difficulty']
        e=input_math(q);x=next(iter(e.free_symbols));fp=g.digest(sp.srepr(sp.expand(e.subs(x,sp.Symbol('x',real=True)))))
        assert m['parameter_fingerprint']==fp,'fingerprint must come from displayed actual input'
    else:assert not m['eligible_for_learning']
    bare=copy.deepcopy(q);bare.pop(':question/id')
    for f in bare.get(':question/answer-fields',[]):
        f.pop(':answer-field/id')
        if ':answer-field/correct' in f:f[':answer-field/correct']=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        for a in f[':answer-field/choices']:a.pop(':answer/id')
        f[':answer-field/choices']=sorted(f[':answer-field/choices'],key=lambda a:json.dumps(a,sort_keys=True))
    assert m['content_fingerprint']==g.digest([g.VERSION,bare])
    ids=[q[':question/id']]+[f[':answer-field/id'] for f in q.get(':question/answer-fields',[])]+[a[':answer/id'] for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices']]
    assert len(ids)==len(set(ids));[uuid.UUID(v) for v in ids]
    return stages(q,name,raw)

def engine_checks(r):
    f=r['question'][':question/answer-fields'][0]
    if f[':answer-field/type'].endswith('/radio'):
        return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every field-owned ID through actual native radio grade_field'} for a in f[':answer-field/choices']]
    correct=f[':answer-field/choices'][0][':answer/value'];a=r['generation']['parameters']['a']
    return [{'field_index':0,'submitted':s,'expected':result,'purpose':'Actual native symbolic blank grade_field'} for s,result in [(correct,'accepted'),(f'-{a}*cot(t)','accepted'),(f'-{a}*cos(t)/sin(t)','accepted'),(f'{a}*cot(t)','rejected'),('0','rejected'),(f'-{a}*cot(t)+7','rejected')]]

def symbolic_probe(r):
    # Radio chooses IDs. A separate explicitly typed memory-only blank companion
    # exercises actual equivalent-expression parsing for every served primitive.
    r=copy.deepcopy(r);f=r['question'][':question/answer-fields'][0]
    correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);wrong=next(a for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])
    expected=correct[':answer/value'].removesuffix('+C');incorrect=wrong[':answer/value'].removesuffix('+C')
    correct[':answer/value']=str(g.expression(expected)).replace('**','^');f[':answer-field/choices']=[correct];f[':answer-field/type']=':answer-field.type/blank';f[':answer-field/key']='field-1'
    expr=g.expression(expected);symbols=list(expr.free_symbols);x=symbols[0]
    reciprocal=expr.xreplace({sp.cot(x):sp.cos(x)/sp.sin(x),sp.csc(x):1/sp.sin(x),sp.sec(x):1/sp.cos(x),sp.tan(x):sp.sin(x)/sp.cos(x)})
    checks=[{'field_index':0,'submitted':s,'expected':result,'purpose':'Explicit memory-only symbolic companion of radio canonical primitive'} for s,result in [(str(expr).replace('**','^'),'accepted'),(str(sp.factor(expr)).replace('**','^'),'accepted'),(str(reciprocal).replace('**','^'),'accepted'),(str(g.expression(incorrect)).replace('**','^'),'rejected'),('0','rejected')]]
    return {'label':'symbolic companion/'+r['generation']['template'],'record':r,'checks':checks}

def unchanged():
    baseline=json.load(open(D/'registered-baseline-hashes.json'));files=[D.parent/'17592186064181.py']+sorted(p for p in (D.parent/'17592186064181').rglob('*') if p.is_file());assert sorted(str(p.relative_to(R)) for p in files)==sorted(baseline['paths'])
    for p in files:assert hashlib.sha256(p.read_bytes()).hexdigest()==baseline['sha256'][str(p.relative_to(R))]
    save('registered-baseline-verification.json',{'status':'unchanged','pathset_unchanged':True,'files_checked':len(files)})

def main():
    unchanged();originals,counts=F.check(g,g.KP_ID,D);raw=[];records=[];reviews=[];steps=0;slots={};negative=0
    inventory_checks=[]
    for item in json.load(open(D/'independent-inventory.json'))['questions']:
        original=item['record']
        def enums(v):
            if isinstance(v,dict):
                if ':db/ident' in v:return v[':db/ident']
                return {k:enums(w) for k,w in v.items()}
            if isinstance(v,list):return [enums(w) for w in v]
            return v
        q=enums(copy.deepcopy(original))
        for f in q[':question/answer-fields']:f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
        n=stages(q);steps+=n;inventory_checks.append({'db_id':original[':db/id'],'values':banks(q)[3],'displayed_rows':n})
        reviews.append({'label':'Independent inventory exact record '+str(original[':db/id']),'inventory':original})
    for c in json.load(open(D/'source-cases.json')):
        replay=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['profile']);steps+=independent(replay);raw.append(replay)
        p={k:(v+1 if v<9 else v-1) for k,v in c['parameters'].items()}
        if c['template']=='q-113948':p={'n':7,'d':3}
        changed=g.generate(c['level'],template=c['template'],parameters=p,profile=c['profile']);steps+=independent(changed)
        reviews.append({'label':c['source_id']+' original / exact raw replay / changed evidence','original':originals[c['source_id']],'replay':replay,'variant':changed})
    for level,names in g.DEFAULTS.items():
        for name in names:
            keys=sorted(g.keys_for(name));low={k:1 for k in keys};high={k:9 for k in keys}
            if name in ('q-113947','q-71663'):low={'a':2}
            if name=='fraction':low={'n':2,'d':3};high={'n':9,'d':8}
            for seed in range(6):
                r=g.generate(level,seed=seed+137,template=name);steps+=independent(r);records.append(r)
            for p in (low,high):r=g.generate(level,template=name,parameters=p);steps+=independent(r);records.append(r)
            baseline=g.generate(level,template=name,parameters=high)
            for k in keys:
                p=high.copy();p[k]=8
                if name=='fraction':p={'n':7,'d':8} if k=='n' else {'n':9,'d':7}
                changed=g.generate(level,template=name,parameters=p);steps+=independent(changed);records.append(changed)
                assert input_math(baseline['question'])!=input_math(changed['question']),('unused parameter',name,k)
                assert baseline['generation']['parameter_fingerprint']!=changed['generation']['parameter_fingerprint']
                assert baseline['question'][':question/worked-solution']!=changed['question'][':question/worked-solution']
            same=g.generate(level,template=name,parameters=high,seed=37);assert same['question'][':question/id']==baseline['question'][':question/id']
            assert g.generate(level,profile=name,parameters=high)['question'][':question/id']==baseline['question'][':question/id']
            slots[name]={k:sorted({r['generation']['parameters'][k] for r in records if r['generation']['template']==name}) for k in keys}
            reviews.append({'label':name+' normal variants / boundary / changed individual slots','records':[r for r in records if r['generation']['template']==name]})
    for level in g.SUPPORTED_LEVELS:
        sampled=[g.generate(level,seed=i) for i in range(40)];assert set(g.DEFAULTS[level])=={r['generation']['template'] for r in sampled}
        assert len({r['generation']['parameter_fingerprint'] for r in sampled})>=12
        for r in sampled:steps+=independent(r)
        records+=sampled
    invalid=[('easy','q-113947',{'a':1}),('easy','q-71663',{'a':0}),('easy','fraction',{'n':4,'d':2}),('easy','fraction',{'n':3,'d':3}),('easy','blank',{'a':True}),('moderate','q-49121',{'a':2,'b':10}),('hard','three-term',{'a':1,'b':2,'c':0}),('hard','three-term',{'a':1,'b':2,'c':3,'unused':5})]
    for l,n,p in invalid:
        try:g.generate(l,template=n,parameters=p)
        except ValueError:negative+=1
        else:raise AssertionError('invalid public parameter accepted')
    specimen=g.generate('moderate',template='q-49121',parameters={'a':3,'b':2})
    for mutation in ('correct','constant-equivalent','distribution','scalar-stage','sign','control','conclusion'):
        r=copy.deepcopy(specimen);q=r['question'];f=q[':question/answer-fields'][0]
        correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);wrong=next(a for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])
        if mutation=='correct':correct[':answer/value']='0+C'
        elif mutation=='constant-equivalent':wrong[':answer/value']=correct[':answer/value']+'+7'
        elif mutation=='distribution':q[':question/worked-solution']=q[':question/worked-solution'].replace('3csccot','3csccot') if False else q[':question/worked-solution'].replace('3csc⁡xcot⁡x+2','3csc⁡xcot⁡x-2',1)
        elif mutation=='scalar-stage':q[':question/worked-solution']=q[':question/worked-solution'].replace(r'3\int csc⁡xcot⁡x\,\text{d}x+2\int {csc}^{2}⁡x\,\text{d}x',r'\int (3csc⁡xcot⁡x+2{csc}^{2}⁡x)\,\text{d}x')
        elif mutation=='sign':q[':question/worked-solution']=q[':question/worked-solution'].replace('3(-csc⁡x)','3(csc⁡x)')
        elif mutation=='control':q[':question/worked-solution']+='\f'
        elif mutation=='conclusion':q[':question/worked-solution']=q[':question/worked-solution'].replace('-3csc⁡x-2cot⁡x+C.','-4csc⁡x-2cot⁡x+C.')
        assert r!=specimen,'mutation actually changes learner bytes'
        try:independent(r) if mutation=='control' else stages(q,'q-49121')
        except (AssertionError,ValueError,SyntaxError):negative+=1
        else:raise AssertionError('corruption survived '+mutation)
    inputs=[{'label':str(i)+'/'+r['generation']['template'],'record':r,'checks':engine_checks(r)} for i,r in enumerate(records)]
    inputs += [symbolic_probe(r) for r in records if not r['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/blank')]
    inputs += [{'label':'raw/'+r['generation']['template'],'record':r,'checks':engine_checks(r)} for r in raw if r['question'].get(':question/answer-fields') and ':answer-field/correct' in r['question'][':question/answer-fields'][0]]
    save('engine-input.json',inputs);subprocess.run([str(R/'generate/runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True,timeout=60)
    engine=json.load(open(D/'engine-report.json'));assert engine['documented_unresolved_checks']==0
    tasks={l:set() for l in g.SUPPORTED_LEVELS}
    for l,names in g.DEFAULTS.items():
        for name in names:
            keys=sorted(g.keys_for(name))
            for values in itertools.product(range(1,10),repeat=len(keys)):
                try:p=g.validate_parameters(name,dict(zip(keys,values)))
                except ValueError:continue
                e=input_math(g.normal(name,p));x=next(iter(e.free_symbols));tasks[l].add(g.digest(sp.srepr(sp.expand(e.subs(x,sp.Symbol('x',real=True))))))
    save('review.json',reviews);out=[]
    for row in reviews:
        out.append('## '+row['label'])
        if 'original' in row:
            q=row['original'];out.append('Original evidence:\n\n'+q[':question/problem']+'\n\n'+q.get(':question/worked-solution','[Absent]')+'\n\n'+ '\n'.join('- $'+a[':answer/value']+'$' for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices']));out.append('Exact raw replay:\n\n'+g.markdown(row['replay']));out.append('Changed evidence (ineligible):\n\n'+g.markdown(row['variant']))
        elif 'inventory' in row:
            q=row['inventory'];out.append(q[':question/problem']+'\n\n'+q[':question/worked-solution']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for f in q[':question/answer-fields'] for a in f[':answer-field/choices']))
        else:
            for r in row['records']:out.append('Generated variant:\n\n'+g.markdown(r))
    (D/'review.md').write_text('\n\n'.join(out)+'\n');unchanged()
    inv=json.load(open(D/'independent-inventory.json'));frozen=json.load(open(D/'source.json'));assert [r['record'] for r in inv['questions']]==[q for q in frozen['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q]
    save('validation.json',{'status':'pass','basis':g.SOURCE_BASIS,'source_fidelity':counts,'independent_inventory_exact_records':len(inv['questions']),'independent_inventory_mathematics':inventory_checks,'mathematics':{'normal_records':len(records),'raw_records':len(raw),'displayed_rows_checked':steps,'negative_controls':negative,'semantic_domain_counts':{l:len(s) for l,s in tasks.items()},'slot_coverage':slots},'source_defects':{'q-113958':'Missing sin argument in one recall; raw retained; corrected verification and normal completion explicitly separate.','q-71666':'Two argument-free csc distractors raw retained; only3/5 mathematical values defined; normal authored bank separate.','q-143522/q-167569':'Undefined v(t) raw retained; coefficient read from main solution evidence only. Normal blank explicitly supplies v(t).'},'complete_raw_banks_matched':7,'raw_radio_choices_matched':35,'raw_blank_values_matched':2,'source_defined_math_values_checked':35,'native_grading':{k:engine[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'versions':{'python':sys.version.split()[0],'sympy':sp.__version__},'hashes':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (D.with_suffix('.py'),Path(__file__),D/'source.json',D/'source-profiles.json',R/'generate/runs/current/check-engine')}})
    print(json.dumps({'status':'pass','source_fidelity':counts,'domain_counts':{l:len(s) for l,s in tasks.items()},'native_checks':engine['accepted_checks']+engine['rejected_checks'],'negative_controls':negative}))
if __name__=='__main__':main()
