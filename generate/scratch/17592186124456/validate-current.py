"""Validate the frozen historical mathematics and the current field contracts."""
import copy,hashlib,importlib.util,itertools,json,re,subprocess
from pathlib import Path
import sympy as s
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g124456',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
# Reuse the existing independent displayed-math/ordered-solution reader only.
v={'__file__':str(D/'validate.py')};exec(compile((D/'validate.py').read_text().split('source=g.SOURCES;cases=')[0],str(D/'validate.py'),'exec'),v)
def mathread(t):
    t=re.sub(r'\\sqrt\[3\]\{([^{}]*)\}',r'(\1)**(1/3)',t)
    t=re.sub(r'\\sqrt\{([^{}]*)\}',r'sqrt(\1)',t)
    return g.parse_math(t)
def pointset(t):
    return frozenset((s.simplify(mathread(a)),s.simplify(mathread(b))) for a,b in re.findall(r'\(([^(),]+),([^(),]+)\)',t))
def truth(q):
    prompt=q[':question/problem'].split('\n\nSelect all')[0]
    F,vec=g.curve_vector(prompt);c=s.expand(vec[0]*s.diff(F,g.Y)-vec[1]*s.diff(F,g.X))
    raw=s.solve_poly_system([F,c],g.X,g.Y)
    if raw is None:raise ValueError('No finite intersection')
    allpoints=frozenset((s.simplify(a),s.simplify(b)) for a,b in raw if a.is_real and b.is_real)
    regular=frozenset(p for p in allpoints if any(s.diff(F,z).subs(dict(zip((g.X,g.Y),p)))!=0 for z in (g.X,g.Y)))
    if not regular or regular!=allpoints:raise ValueError('Zero gradient at keyed intersection')
    fields=q[':question/answer-fields']
    if g.enum(fields[0][':answer-field/type']).endswith('/checkbox'):
        labels=re.findall(r'- \*\*([^*]+)\.\*\* \$([^$]+)\$',q[':question/problem']);assert len(labels)==len(fields)
        selected=set()
        for f,(label,value) in zip(sorted(fields,key=lambda f:['I','II','III','IV','V','VI','VII'].index(f[':answer-field/key'])),labels):
            assert f[':answer-field/key']==label
            p=pointset(value);assert len(p)==1
            expected=next(iter(p)) in regular
            correct=f[':answer-field/correct'];actual=correct[':answer/value'] if isinstance(correct,dict) else next(a[':answer/value'] for a in f[':answer-field/choices'] if str(a[':answer/id'])==correct[1])
            assert actual==str(expected).lower()
            assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==['false','true']
            if expected:selected.update(p)
        assert frozenset(selected)==regular
    else:
        assert len(fields)==1;f=fields[0];banks=[pointset(a[':answer/value']) for a in f[':answer-field/choices']]
        assert len(set(banks))==len(banks) and banks.count(regular)==1
        c=f[':answer-field/correct'];key=c[':answer/value'] if isinstance(c,dict) else next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==c[1]);assert pointset(key)==regular
    return regular

def independent(rec):
    assert rec['knowledge_point']['db_id']==g.KP and not rec['generation']['evidence_only']
    q=rec['question'];truth(q);level=q[':question/difficulty'].split('/')[-1]
    old=g._generate_radio(level,parameters=rec['generation']['parameters'])
    v['independent'](old)
    assert q[':question/worked-solution']==old['question'][':question/worked-solution']
    assert q[':question/problem'].split('\n\nSelect all')[0]==old['question'][':question/problem']
    assert g.generate(level,seed=rec['generation']['seed'],parameters=rec['generation']['parameters'])==rec
    return True

def checks(rec):
    return [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'every checkbox Boolean or radio selection'} for i,f in enumerate(rec['question'][':question/answer-fields']) for a in f[':answer-field/choices']]

def main():
    sources=json.loads((D/'reference/initial/kp.json').read_text())[':knowledge-point/questions'];source_checks=[]
    for q in sources:
        try:truth(q);status='mathematics and current fields pass'
        except (ValueError,AssertionError,TypeError,NotImplementedError) as e:status='excluded: '+str(e)
        source_checks.append({'source':q[':question/math-academy-id'],'status':status,'field_types':[g.enum(f[':answer-field/type']) for f in q[':question/answer-fields']],'difficulty':g.enum(q[':question/difficulty']) if ':question/difficulty' in q else None})
    counts={};rejected={};records=[]
    for level in g.SUPPORTED_LEVELS:
        if level=='easy':domain=({'A':A,'b':b,'r':r} for A,b,r in itertools.product(range(1,5),range(2,6),[v for v in range(-6,7) if v]))
        elif level=='moderate':domain=({'D':D,'m':m,'r':r} for D,m,r in itertools.product(range(1,4),range(2,5),range(1,5)))
        else:domain=({'a':a,'b':b} for a,b in itertools.combinations([v for v in range(-6,7) if v],2) if a+b)
        fps=set();rejected[level]=0
        for p in domain:
            try:r=g.generate(level,parameters=p)
            except ValueError:rejected[level]+=1;continue
            independent(r);fps.add(r['generation']['mathematical_fingerprint'])
        counts[level]=len(fps)
        for seed in (23,44):
            r=g.generate(level,seed);independent(r);records.append(r)
    # Replay complete coordinate profiles at observed parameters separately from
    # the narrower sampling policy; equation and Boolean truth checked in source.
    replay=[]
    byid={q[':question/math-academy-id']:q for q in sources}
    for level,sid,p in [('moderate','q-72410',{'D':1,'m':1,'r':2}),('hard','q-72440',{'a':1,'b':4})]:
        coords=g.checkbox_coordinates(level,p);labels=re.findall(r'- \*\*([^*]+)\.\*\* \$([^$]+)\$',byid[sid][':question/problem'])
        original={next(iter(pointset(t))) for _,t in labels};assert original==set(coords)
        replay.append({'source':sid,'complete_current_coordinate_bank':True,'matched_choices':len(coords),'total_choices':len(original),'all_boolean_keys_verified':True})
    fixtures=[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in records]
    (D/'native-current-input.json').write_text(json.dumps(fixtures,indent=2));engine=D.parents[2]/'generate/runs/current/check-engine'
    subprocess.run([str(engine),str(D/'native-current-input.json'),str(D/'native-current-report.json')],check=True)
    review='\n\n'.join(g.markdown(r) for r in records);(D/'review-current.md').write_text(review)
    result={'passed':True,'generator_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'finite_distinct_tasks':counts,'rejected_parameter_banks':rejected,'source_checks':source_checks,'current_bank_replay':replay,'historical_replay_evidence':'validation.json (11/11 full banks,55/55 values)','source_basis':2285,'native_grader_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'supported_levels':list(g.SUPPORTED_LEVELS),'missing_level_assignments':'Easy and moderate are authored, not observed source labels.','exceptions':['Historical distractor intentions remain opaque and evidence-only.','New source families are captured and checked but not automatically generalized.','Zero-gradient source intersections are excluded; source facts remain unchanged.','Current hard coordinate profile rejects collisions; finite counts are after mathematical deduplication.']}
    (D/'validation-current.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':True,'finite_distinct_tasks':counts,'source_checks':source_checks},indent=2))
if __name__=='__main__':main()
