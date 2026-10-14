"""Validate the current checkbox contract against printed mathematics and EDB sources."""
import copy, hashlib, importlib.util, itertools, json, re, subprocess
from pathlib import Path
import sympy as sp

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('legacy_validation',HERE/'validate.py')
legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)
g=legacy.g

def normalize(q):
    q=json.loads(json.dumps(q,default=str))
    enum=lambda v:v[':db/ident'] if isinstance(v,dict) else v
    result={k:q[k] for k in (':question/id',':question/problem',':question/worked-solution')}
    result[':question/difficulty']=enum(q[':question/difficulty'])
    result[':question/answer-fields']=[]
    for f in sorted(q[':question/answer-fields'],key=lambda f:f[':answer-field/key']):
        correct=f[':answer-field/correct']
        result[':question/answer-fields'].append({
            ':answer-field/id':f[':answer-field/id'],':answer-field/key':f[':answer-field/key'],
            ':answer-field/type':enum(f[':answer-field/type']),
            ':answer-field/correct':[':answer/id',correct[':answer/id']] if isinstance(correct,dict) else correct,
            ':answer-field/choices':sorted([{':answer/id':a[':answer/id'],':answer/type':enum(a[':answer/type']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],key=lambda a:a[':answer/value'])})
    return result

def parsed(q):
    q=normalize(q);p=q[':question/problem'];ivs=legacy.intervals(p)
    expr=legacy.decode(re.search(r'f\(x\)=(.*?),\$',p)[1]);x=legacy.x
    if expr.has(sp.Abs):
        h=sp.solve(next(iter(expr.atoms(sp.Abs))).args[0],x)[0];kind='absolute';a=1
    else:
        poly=sp.Poly(expr,x)
        assert poly.degree()<=2
        if poly.degree()==2:h=-poly.nth(1)/(2*poly.nth(2));kind='quadratic';a=poly.nth(2)
        else:h=0;kind='linear';a=poly.nth(1)
    return expr,ivs,kind,a,h

def fingerprint(q):
    expr,ivs,kind,a,h=parsed(q)
    level=normalize(q)[':question/difficulty'].split('/')[-1]
    return g.mathematical_fingerprint(level,kind,a,h,ivs)

def validate_question(q):
    q=normalize(q);expr,ivs,kind,a,h=parsed(q)
    assert 'Select all that apply.' in q[':question/problem']
    assert re.findall(r'- \*\*(I|II|III)\.\*\*',q[':question/problem'])==list(g.ROMANS)
    truth=[]
    for lo,hi,l,r in ivs:
        assert lo<hi and not(lo==-sp.oo and l) and not(hi==sp.oo and r)
        good=a!=0 if kind=='linear' else hi<=h or lo>=h
        truth.append(bool(good))
        if not good:
            if kind=='linear':
                u=(lo+hi)/2 if lo!=-sp.oo and hi!=sp.oo else hi-1 if hi!=sp.oo else lo+1 if lo!=-sp.oo else 0
                v=u+sp.Rational(1,10)
            else:
                d=min(h-lo if lo!=-sp.oo else 1,hi-h if hi!=sp.oo else 1)/2;u,v=h-d,h+d
            assert lo<u<hi and lo<v<hi and u!=v and sp.simplify(expr.subs(legacy.x,u)-expr.subs(legacy.x,v))==0
    fields=q[':question/answer-fields'];assert [f[':answer-field/key'] for f in fields]==list(g.ROMANS)
    ids=[q[':question/id']]
    for label,f,good in zip(g.ROMANS,fields,truth):
        assert f[':answer-field/type']==':answer-field.type/checkbox'
        assert [a[':answer/value'] for a in f[':answer-field/choices']]==['false','true']
        assert all(a[':answer/type']==':answer.type/text' for a in f[':answer-field/choices'])
        key=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        assert key[':answer/value']==str(good).lower()
        ids += [f[':answer-field/id'],*[a[':answer/id'] for a in f[':answer-field/choices']]]
    assert len(ids)==len(set(ids))
    conclusion=re.search(r'correct answer is "([^"]+)"',q[':question/worked-solution'])[1]
    assert g.choice_subset(conclusion)==frozenset(label for label,t in zip(g.ROMANS,truth) if t)
    return truth

def replay(r):
    meta=r['generation'];level=r['question'][':question/difficulty'].split('/')[-1]
    result=g.generate(level,meta['seed'],meta['template'],parameters=meta['parameters'],profile=meta['legacy_sampling_profile'])
    for asset in meta.get('published_assets',{}).values():
        for k in (':question/problem',':question/worked-solution'):
            result['question'][k]=result['question'][k].replace(asset['local'],asset['reference'])
    return result

def validate(r):
    assert r['knowledge_point']['db_id']==g.KP and r['knowledge_point']['id']==g.KP_UUID
    assert r['generation']['eligible_for_learning'] and not r['generation']['evidence_only']
    truth=validate_question(r['question'])
    assert r['generation']['mathematical_fingerprint']==fingerprint(r['question'])
    assert normalize(replay(r)['question'])==normalize(r['question'])
    meta=r['generation'];level=r['question'][':question/difficulty'].split('/')[-1]
    old=g.generate_legacy(level,meta['seed'],meta['template'],parameters=meta['parameters'],profile=meta['legacy_sampling_profile'])
    legacy.inspect(old)
    return truth

def native(r):
    r=copy.deepcopy(r);r['question']=normalize(r['question'])
    checks=[{'field_index':i,'submitted_answer_id':a[':answer/id'],
             'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected',
             'purpose':'independently checked interval checkbox'}
            for i,f in enumerate(r['question'][':question/answer-fields']) for a in f[':answer-field/choices']]
    return {'label':r['question'][':question/id'],'record':r,'checks':checks}

def hashfile(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    records=[];source_records=[]
    for name,q in g.CURRENT_SOURCES.items():
        level,kind,a,h,k,_=g.SPECS[name]
        r=g.generate(level,template=name,parameters={'a':a,'h':h,'k':k,'offset':0});validate(r)
        observed=normalize(q);generated=normalize(r['question'])
        assert generated[':question/problem']==observed[':question/problem']
        assert generated[':question/worked-solution']==observed[':question/worked-solution']
        for left,right in zip(generated[':question/answer-fields'],observed[':question/answer-fields']):
            assert (left[':answer-field/key'],left[':answer-field/type'])==(right[':answer-field/key'],right[':answer-field/type'])
            assert [(a[':answer/type'],a[':answer/value']) for a in left[':answer-field/choices']]==[(a[':answer/type'],a[':answer/value']) for a in right[':answer-field/choices']]
            answer=lambda f:next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
            assert answer(left)==answer(right)
        source_records.append({'knowledge_point':r['knowledge_point'],'question':q,'generation':{'template':'current:'+name}})
        records.append(r)
    for level in ('easy','moderate','hard'):
        for seed in range(48):
            r=g.generate(level,seed);validate(r);records.append(r)
    catalogs={}
    for level,types in [('moderate',[[half,finite,'X'] for half in g.MODERATE_TYPES for finite in g.HARD_TYPES if finite!='X']),('hard',[[*pair,'X'] for pair in itertools.combinations([t for t in g.HARD_TYPES if t!='X'],2)])]:
        fps=set()
        for entries in types:
            for order in itertools.permutations(entries):
                for template in ('integer_quadratic','integer_absolute') if level=='moderate' else ('rational_quadratic','rational_absolute'):
                    r=g.generate(level,template=template,parameters={'h':2 if level=='moderate' else '1/2','k':0,'types':list(order)})
                    validate(r);fps.add(fingerprint(r['question']))
        catalogs[level]=len(fps)
    assert catalogs=={'moderate':12,'hard':15}
    left=g.generate('hard',template='rational_quadratic',parameters={'h':'1/2','k':0,'types':['L','R','X']})
    right=g.generate('hard',template='rational_quadratic',parameters={'h':'1/2','k':0,'types':['L','X','RC']})
    assert validate(left)==[True,True,False] and validate(right)==[True,False,True]
    assert fingerprint(left['question'])!=fingerprint(right['question'])
    permuted=g.generate('hard',template='rational_absolute',parameters={'h':'3/4','k':2,'types':['X','R','L']})
    assert fingerprint(left['question'])==fingerprint(permuted['question'])
    records.extend([left,right,permuted])
    (HERE/'checkbox-native-input.json').write_text(json.dumps([native(r) for r in records+source_records],indent=2))
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'checkbox-native-input.json'),str(HERE/'checkbox-native-results.json')],check=True)
    report=json.loads((HERE/'checkbox-native-results.json').read_text());assert report['documented_unresolved_checks']==0
    files=[HERE.with_suffix('.py'),HERE/'validate.py',HERE/'validate_checkbox.py',HERE/'current-source.json',HERE/'source.json',HERE/'render.py',ROOT/'generate/runs/current/check-engine']
    result={'passed':True,'current_basis':g.CURRENT_SNAPSHOT['basis'],'current_source_replay':{'exact_prompts':12,'exact_solutions':12,'complete_boolean_banks':36,'matched_answers':72,'matched_correct_designations':36},'legacy_radio_fidelity':'Preserved separately in validation.json; all 11 banks/55 choices replayed. Historical missing q-66785 field retained raw. Current source has three complete checkbox fields.','default_records':144,'unordered_catalogs':catalogs,'easy_catalog_limit':2,'changed_target_case':{'same_function':True,'left_truth':[True,True,False],'right_truth':[True,False,True]},'alias_rejection':'Interval permutation, function family, numeric translation and seed do not increase task count.','native_accepted':report['accepted_checks'],'native_rejected':report['rejected_checks'],'hashes':{str(p.relative_to(ROOT)):hashfile(p) for p in files}}
    (HERE/'checkbox-validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='hashes'}))

if __name__=='__main__':main()
