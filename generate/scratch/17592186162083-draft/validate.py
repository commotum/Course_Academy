#!/usr/bin/env python3
"""Independent checks read displayed curves, claims, Cartesian rows and conclusions."""
import hashlib,importlib.util,json,random,re,subprocess,sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('arc_draft',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
t,u,x,y,z,k,theta=sp.symbols('t u x y z k theta',nonnegative=True)

def balanced(s,start):
    assert s[start]=='{';depth=1;i=start+1
    while depth:
        if s[i]=='{':depth+=1
        if s[i]=='}':depth-=1
        i+=1
    return s[start+1:i-1],i

def math(s):
    s=s.replace('π',r'\pi').replace('⁡','').replace('θ','theta').replace(r'\,','').replace(' ','').strip('.,')
    s=s.replace(r'\operatorname{cos}','cos').replace(r'\operatorname{sin}','sin').replace(r'\cos','cos').replace(r'\sin','sin')
    while r'\frac' in s or r'\sqrt' in s:
        m=re.search(r'\\(frac|sqrt)\{',s);a,end=balanced(s,m.end()-1)
        if m[1]=='frac':b,end=balanced(s,end);val='(('+a+')/('+b+'))'
        else:val='sqrt('+a+')'
        s=s[:m.start()]+val+s[end:]
    s=s.replace(r'\pi','pi').replace('{','(').replace('}',')').replace('^','**')
    s=re.sub(r'(cos|sin)(\d*)(theta|[tu])',lambda m:m[1]+'('+str(m[2] or 1)+'*'+m[3]+')',s)
    return sp.simplify(parse_expr(s,local_dict={'t':t,'u':u,'x':x,'y':y,'z':z,'k':k,'theta':theta,'pi':sp.pi,'sqrt':sp.sqrt,'sin':sp.sin,'cos':sp.cos},transformations=standard_transformations+(implicit_multiplication_application,rationalize)))

def geometry(q):
    text=q[':question/problem'].replace(' ','');vectors=re.findall('⟨([^⟩]+)⟩',text);assert len(vectors)==2,vectors
    vec=[[math(c) for c in v.replace(r'\,','').split(',')] for v in vectors];assert all(len(v)==2 for v in vec)
    bounds=re.findall(r'0\\le([tuθ])\\le(.*?)(?=[$.,]|\\\\|\\end)',text);assert len(bounds)==2,bounds
    variables=[{'t':t,'u':u,'θ':theta}[v] for v,end in bounds];ends=[math(end) for v,end in bounds];assert all(e>0 for e in ends)
    normalized=[[sp.simplify(c.subs(var,end*z)) for c in v] for v,var,end in zip(vec,variables,ends)]
    assert all(sp.simplify(a-b)==0 for a,b in zip(*normalized)),('different paths',normalized)
    return normalized[0],vec[0],variables[0],ends[0]

def claimed(line):
    m=re.search(r'(?:\\text\{d\}s|ds)\s*=\s*([^$]+)',line);assert m,line
    return math(m[1])

def correct_value(f):return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])

def structural(rec):
    q=rec['question'];text=q[':question/problem'];sol=q.get(':question/worked-solution');norm,v,var,end=geometry(q)
    assert set(rec['knowledge_point'])=={'db_id','id','title'}
    for s in (text,sol or ''):
        assert s.count('$')%2==0 and s.count('{')==s.count('}')
        assert not any(ord(c)<32 and c not in '\n\t\r' for c in s)
    assumed=claimed(text.split('Which of the following')[0])
    lines=[line for line in text.splitlines() if line.startswith('- **') or re.match(r'^[123]\. ',line)];assert len(lines)==3
    truth=[bool(sp.simplify(claimed(line)-assumed)==0) for line in lines]
    roles=[]
    for line,valid in zip(lines,truth):
        compact=line.replace('{','').replace('}','').replace(' ','')
        target=re.search(r'\\int_(-?C_[12])',compact)[1]
        roles.append(('reverse-same' if valid else 'reverse-negative') if target=='-C_1' else ('reparam-same' if valid else 'reparam-scaled'))
    actual_fp=g.digest({'curve':[sp.srepr(sp.simplify(c)) for c in norm],'relations':sorted(roles)})
    assert actual_fp==rec['generation']['mathematical_fingerprint']
    fs=q[':question/answer-fields'];typ=fs[0][':answer-field/type']
    if typ.endswith('/checkbox'):
        assert [f[':answer-field/key'] for f in fs]==['I','II','III']
        for f,c in zip(fs,truth):
            assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==['false','true']
            assert correct_value(f)==str(c).lower()
    else:
        assert len(fs)==1 and len(fs[0][':answer-field/choices'])==5
        actual=set(name for name,c in zip(('I','II','III'),truth) if c)
        options=[]
        for a in fs[0][':answer-field/choices']:
            subset=set(re.findall(r'\b(?:III|II|I)\b',a[':answer/value']));assert subset not in options;options.append(subset)
        assert sum(o==actual for o in options)==1
        if ':answer-field/correct' in fs[0]:assert set(re.findall(r'\b(?:III|II|I)\b',correct_value(fs[0])))==actual
    if sol is not None:
        assertions=re.findall(r'Statement (I|II|III) is (true|false)',sol)+re.findall(r'while statement (I|II|III) is (true|false)',sol)
        assert len(assertions)==3,assertions
        for i,val in assertions:assert truth[{'I':0,'II':1,'III':2}[i]]==(val=='true')
        blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S)
        assert len(blocks)==(2 if 'circle' in sol else 3)
        for block in blocks:
            if r'\int' in block:assert math(block.split('=')[-1])==assumed
            else:
                relation,domain=block.strip().rstrip('.').split(r'\,');lhs,rhs=relation.split('=');target={'x':v[0],'y':v[1]}[lhs]
                assert sp.simplify(target-math(rhs).subs({x:v[0],y:v[1]}))==0,(target,rhs)
                family=rec['generation']['template']
                masks={'q-122478':r'\d*\{x\}\^\{2\}', 'q-122814':r'\d*\{y\}\^\{4\}-\d*\{y\}\^\{2\}', 'q-122816':r'\d*\{x\}\^\{3/2\}', 'q-122851':r'\\sqrt\{\{y\}\^\{2\}\+\d+\}', 'q-122868':r'\\sqrt\{.+x\}|\\sqrt\{x\}'}
                assert re.fullmatch(masks[family],rhs.rstrip(',')),('operative Cartesian structure changed',family,rhs)
                dm=re.fullmatch(r'0\\le ([xy])\\le (.*)',domain);assert dm
                comp={'x':v[0],'y':v[1]}[dm[1]]
                assert comp.subs(var,0)==0 and sp.simplify(comp.subs(var,end)-math(dm[2]))==0
        if 'circle' in sol:
            R=math(re.search(r'radius \$(.*?)\$',sol)[1]);assert sp.simplify(sum(c*c for c in v)-R*R)==0
            if 'half-circle' in sol:assert norm[0].subs(z,0)==R and norm[0].subs(z,1)==-R and norm[1].subs(z,sp.Rational(1,2))==R
            else:assert norm[0].subs(z,0)==0 and norm[0].subs(z,sp.Rational(1,4))==R and norm[1].subs(z,1)==R
        names=[name for name,b in zip(('I','II','III'),truth) if b]
        assert '"'+' and '.join(names)+' only."' in sol
        # Preserve every operative prose stage in normal rated families at all parameters.
        family=rec['generation']['template']
        if family not in ('q-122478','q-122571'):
            old=g.SOURCES[family][':question/worked-solution']
            strip=lambda s:re.sub(r'\$\$.*?\$\$|\$.*?\$', '<math>',s,flags=re.S)
            assert strip(sol)==strip(old)
    return g.digest([sp.srepr(sp.simplify(c)) for c in norm])

def native_checks(rec):
    return [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'full categorical response criterion'} for i,f in enumerate(rec['question'][':question/answer-fields']) if ':answer-field/correct' in f for a in f[':answer-field/choices']]

def inventory():
    out=[];base=ROOT/'generate/scratch'
    for p in sorted([base/'17592186162083.py',*(base/'17592186162083').rglob('*')]):
        row={'path':str(p.relative_to(ROOT)),'kind':'directory' if p.is_dir() else 'file'}
        if p.is_file():row.update(size=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
        out.append(row)
    return out

def main():
    records=[];reviews=[];coverage={};cases=[];level_for={f:lev for lev,fs in g.LEVELS.items() for f in fs};level_for['q-122571']='moderate'
    for family,src in g.SOURCES.items():
        level=level_for[family];cases.append({'source_id':src[':db/id'],'math_academy_id':family,'template':family,'level':level,'parameters':g.CASES[family],'profile':'raw:'+family})
        replay=g.generate(level,template=family,parameters=g.CASES[family],profile='raw:'+family);structural(replay)
        reviews.append({'role':'original raw replay','record':replay})
        pool=list(g.candidates(family));sample=[];slotseen={key:set() for key in pool[0]}
        for p in pool:
            if any(p[key] not in slotseen[key] for key in p):
                sample.append(p)
                for key in p:slotseen[key].add(p[key])
        sample+=random.Random(71).sample(pool,min(12,len(pool)))
        sample+=[g.CASES[family]]
        for p in sample:
            r=g.generate(level,template=family,parameters=p);structural(r);records.append(r)
            r2=g.generate(level,seed=19,template=family,parameters=p)
            assert r['question'][':question/id']==r2['question'][':question/id']
            assert r['generation']['content_fingerprint']==r2['generation']['content_fingerprint']
        reviews.extend({'role':'generated normal variant','record':g.generate(level,seed=13,template=family,parameters=p)} for p in (pool[0],pool[-1]))
        # Finite counts exclude supplied k and speed changes; enumerate actual normalized curves.
        projected={tuple((key,p[key]) for key in p if key not in {'k','s','d','n','a','b'} or (family=='q-122814' and key in {'a','b'})) for p in pool}
        fps={g.mathematical_fingerprint(family,dict(pp,**{key:g.CASES[family][key] for key in g.CASES[family] if key not in dict(pp)})) for pp in projected}
        coverage[family]={'sampled':len(sample),'slots':{key:sorted(vals) for key,vals in slotseen.items()},'finite_mathematical_tasks':len(fps)}
    (D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
    spec=importlib.util.spec_from_file_location('rootF',ROOT/'generate/runs/current/root-source-fidelity.py');F=importlib.util.module_from_spec(spec);spec.loader.exec_module(F)
    originals,fidelity=F.check(g,17592186162083,D)
    # Changed-parameter raw replay works through public API and preserves absence contracts.
    for case in cases:
        raw=g.generate(case['level'],template=case['template'],parameters=list(g.candidates(case['template']))[-1],profile=case['profile']);structural(raw)
        src=g.SOURCES[case['template']]
        for key in (':question/worked-solution',':question/difficulty',':question/answer-fields'):assert (key in raw['question'])==(key in src)
    default_families={level:sorted({g.generate(level,seed=seed)['generation']['template'] for seed in range(100)}) for level in g.LEVELS}
    for level,seen in default_families.items():assert set(seen)==set(g.LEVELS[level])
    # Reparametrization speed and supplied scalar cannot inflate task identities.
    original=g.generate('easy',template='q-122478',parameters=g.CASES['q-122478'])
    for change in ({'s':3},{'k':5}):
        shifted=g.generate('easy',template='q-122478',parameters={**g.CASES['q-122478'],**change})
        assert shifted['generation']['mathematical_fingerprint']==original['generation']['mathematical_fingerprint']
        assert shifted['question'][':question/id']!=original['question'][':question/id']
    # Parameterized anchors run through normal source-shaped generation.
    # Every domain bound and unsupported parameter is rejected by the public API.
    invalid=0
    for case in cases:
        for key in case['parameters']:
            for value in (0,-99,99):
                p={**case['parameters'],key:value}
                try:g.generate(case['level'],template=case['template'],parameters=p)
                except ValueError:invalid+=1
                else:
                    assert key=='k' and value!=0,('boundary accepted',case,key,value)
    # Structural mutations catch a wrong curve, missing teaching operation and stale conclusion.
    mutations=0
    import copy
    sample=g.generate('moderate',template='q-122814',parameters=g.CASES['q-122814'])
    for key,old,new in [(':question/problem','16{u}^{4}','17{u}^{4}'),(':question/worked-solution','x={y}^{4}-3{y}^{2}','x={y}^{4}-4{y}^{2}'),(':question/worked-solution','x={y}^{4}-3{y}^{2}','x={y}^{2}({y}^{2}-3)'),(':question/worked-solution','"III only."','"II only."'),(':question/problem','Which','\x0cWhich')]:
        bad=copy.deepcopy(sample);bad['question'][key]=bad['question'][key].replace(old,new)
        try:structural(bad)
        except AssertionError:mutations+=1
        else:raise AssertionError('Mutation escaped independent validation')
    # Include faithful rated raw banks in real native checks. Missing-ref legacy
    # evidence remains explicitly ungradable, not a passing grading fixture.
    signed_boundary_records=[]
    for case in cases:
        if 'k' in case['parameters']:
            for val in (-9,9):
                r=g.generate(case['level'],template=case['template'],parameters={**case['parameters'],'k':val});structural(r);signed_boundary_records.append(r)
    raw_graded=[item['record'] for item in reviews if item['role']=='original raw replay' and all(':answer-field/correct' in f for f in item['record']['question'][':question/answer-fields'])]
    grading_records=records+signed_boundary_records+raw_graded
    inputs=[{'label':str(i),'record':r,'checks':native_checks(r)} for i,r in enumerate(grading_records)]
    (D/'engine-input.json').write_text(json.dumps(inputs,ensure_ascii=False,indent=2)+'\n')
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
    engine=json.loads((D/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
    after=inventory();before=json.loads((D/'baseline-before.json').read_text());assert before==after
    (D/'baseline-after.json').write_text(json.dumps(after,indent=2)+'\n')
    (D/'review.json').write_text(json.dumps(reviews,ensure_ascii=False,indent=2)+'\n')
    text=['# Original replays and normal variants','Original MA grades are retained; easy and unrated circle completion are authored calibrations.']
    for item in reviews:
        r=item['record'];q=r['question'];text+=['\n## '+r['generation']['template']+' — '+item['role'],q[':question/problem'],q.get(':question/worked-solution','[Absent in captured original.]'),json.dumps(q[':question/answer-fields'],ensure_ascii=False,indent=2)]
    (D/'review.md').write_text('\n\n'.join(text)+'\n')
    result={'status':'pass','basis':g.SNAPSHOT['basis'],'lineage':g.SNAPSHOT['lineage'],'fidelity':fidelity,'native_grading':{key:engine[key] for key in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'coverage':coverage,'default_family_coverage':default_families,'normal_records':len(records),'native_raw_originals':len(raw_graded),'signed_scalar_boundary_records':len(signed_boundary_records),'invalid_parameters_rejected':invalid,'mutation_checks':mutations,'baseline_unchanged':True,'baseline_registered_commit_basis':2287,'independent_inventory':0,'raw_unrated_missing_correct_refs':2,'raw_unrated_missing_solutions':2,'authored_levels':['easy'],'authored_unrated_moderate_completion':['q-122571'],'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'grader_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()}
    (D/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
