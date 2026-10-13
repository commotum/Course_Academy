"""Independent actual displayed TeX mathematics, source fidelity and real grading."""
import concurrent.futures,hashlib,importlib.util,json,re,subprocess,tempfile
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def read_tex(text):
    def group(s,i):
        assert s[i]=='{';depth=1;j=i+1
        while depth:
            if s[j]=='{':depth+=1
            if s[j]=='}':depth-=1
            j+=1
        return s[i+1:j-1],j
    def convert(s):
        out='';i=0
        while i<len(s):
            if s.startswith('\\frac',i):
                n,j=group(s,i+5);d,i=group(s,j);out+='(('+convert(n)+')/('+convert(d)+'))'
            elif s.startswith('\\sqrt',i):
                a,i=group(s,i+5);out+='sqrt('+convert(a)+')'
            elif s[i]=='{':a,i=group(s,i);out+='('+convert(a)+')'
            else:out+=s[i];i+=1
        return out
    text=convert(text.replace('\\cdot','*').strip().rstrip('.')).replace('^','**')
    return parse_expr(text,local_dict={'sqrt':S.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))
def format_check(s):
    assert s.count('$')%2==0
    depth=0
    for char in s:
        if char=='{':depth+=1
        if char=='}':depth-=1
        assert depth>=0
    assert depth==0

def independent(r):
    q=r['question'];gen=r['generation'];assert set(r['knowledge_point'])=={'db_id','id','title'}
    assert r['knowledge_point']['db_id']==g.ID
    for t in (q[':question/problem'],q[':question/worked-solution']):format_check(t)
    # Read vectors from the exact rendered geometry sidecar, not answer metadata.
    geo=json.loads(Path(gen['plots']['prompt'].replace('-prompt.png','.json')).read_text())['geometry'];assert geo==gen['geometry']
    A=geo['A'];B=geo['B'];P=geo.get('P');vs={}
    if P:vs={geo['names'][0]:[S.Rational(str(P[i]))-S.Rational(str(A[i])) for i in range(2)],geo['names'][1]:[S.Rational(str(B[i]))-S.Rational(str(P[i])) for i in range(2)]}
    else:vs={geo['names'][0]:[S.Rational(str(B[i]))-S.Rational(str(A[i])) for i in range(2)]}
    target=[S.Rational(str(B[i]))-S.Rational(str(A[i])) for i in range(2)];length=S.sqrt(sum(x*x for x in target));field=q[':question/answer-fields'][0];valid=[];vectors=[]
    for choice in field[':answer-field/choices']:
        expression=read_tex(choice[':answer/value']);xy=[S.simplify(expression.subs({S.Symbol(k):v[i] for k,v in vs.items()})) for i in range(2)];vectors.append(xy)
        eligible=S.simplify(sum(x*x for x in xy)-1)==0 and S.simplify(xy[0]*target[1]-xy[1]*target[0])==0
        if eligible:valid.append(choice[':answer/id'])
    assert valid==[field[':answer-field/correct'][1]]
    assert len({tuple(v) for v in vectors})==5
    # Full arithmetic stage sequence, independently read from displayed aligned math.
    blocks=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S);assert len(blocks)==2
    lines=re.split(r'\\\\',blocks[0]);assert len(lines)==(5 if gen['bank_profile']=='observed_hard' else 4)
    hx,hy=map(abs,target)
    for label,expected in [('AH',hx),('BH',hy)]:
        prose=re.search(label+r'=([^$]+)\$',q[':question/worked-solution']).group(1)
        for displayed in prose.split('='):assert S.simplify(read_tex(displayed)-expected)==0
    magnitude_prose=re.search(r'magnitude of \$[^$]+\$ is \$([^$]+)',q[':question/worked-solution']).group(1);assert S.simplify(read_tex(magnitude_prose)-length)==0
    numeric=[]
    for line in lines:
        if '&' not in line:continue
        rhs=line.split('&',1)[1].lstrip().lstrip('=').strip().replace('\\end{aligned}','')
        if rhs=='AB':continue
        rhs=rhs.replace('A{H}','AH').replace('B{H}','BH').replace('AH',g.tex(hx)).replace('BH',g.tex(hy))
        value=read_tex(rhs);assert S.simplify(value-length)==0,(rhs,value,length)
        numeric.append(rhs)
    assert '^' in numeric[1] and '+' in numeric[1] and '^' not in numeric[2] and '+' in numeric[2] and '+' not in numeric[3]
    assert len(numeric)==4 and numeric[0]!=numeric[1] # symbolic and substituted rows stay distinct
    unitlines=re.split(r'\\\\',blocks[1]);assert len(unitlines)==2
    rhs=unitlines[-1].split('&',1)[1].lstrip().lstrip('=').strip().replace('\\end{aligned}','').rstrip('.')
    answer=read_tex(rhs);unit=[S.simplify(answer.subs({S.Symbol(k):v[i] for k,v in vs.items()})) for i in range(2)]
    assert all(S.simplify(unit[i]-target[i]/length)==0 for i in range(2))
    formal=unitlines[0].split('&',1)[1].lstrip().lstrip('=').strip();formal=re.sub(r'\|[^|]+\|',lambda _:g.tex(length),formal)
    formalexpr=read_tex(formal);formalunit=[S.simplify(formalexpr.subs({S.Symbol(k):v[i] for k,v in vs.items()})) for i in range(2)]
    assert all(S.simplify(formalunit[i]-target[i]/length)==0 for i in range(2))

def main():
    cases=[{'source_id':sid,'template':'single' if sid=='q-20407' else 'sum','level':'moderate' if sid=='q-20407' else 'hard','parameters':p,'bank_profile':{'q-20407':'observed_c','q-19276':'observed_qr','q-119805':'observed_hard'}[sid]} for sid,p in g.SOURCE_PARAMS.items()]
    for c in cases:
        c['completion_profile']=c['bank_profile'];c['bank_profile']={'observed_c':'raw_c','observed_qr':'raw_qr','observed_hard':'raw_hard'}[c['completion_profile']]
        c['raw_profile']=c['bank_profile']
    (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');records=[];fidelity=[];raw_records=[]
    for case in cases:
        r=g.generate(case['level'],seed=21,template=case['template'],parameters=case['parameters'],profile=case['completion_profile']);records.append(r);source=g.SOURCES[case['source_id']];q=r['question'];assert q[':question/problem'].replace('/media/jake/SSD/EDB/math/','')==source[':question/problem']
        observed=source.get(':question/answer-fields',[])
        if observed:assert sorted(a[':answer/value'] for a in observed[0][':answer-field/choices'])==sorted(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])
        if ':question/worked-solution' in source:assert q[':question/worked-solution'].replace('/media/jake/SSD/EDB/math/','')==source[':question/worked-solution']
        raw=g.generate(case['level'],seed=21,template=case['template'],parameters=case['parameters'],profile=case['raw_profile'])
        raw_records.append(raw)
        for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in raw['question'])==(key in source)
        if observed:assert all(':answer-field/correct' not in f for f in raw['question'][':question/answer-fields'])
        raw2=g.generate(case['level'],seed=934,template=case['template'],parameters=case['parameters'],profile=case['raw_profile']);assert raw['question'][':question/id']==raw2['question'][':question/id']
        assert raw['question'][':question/problem']==source[':question/problem']
        if ':question/worked-solution' in source:assert raw['question'][':question/worked-solution']==source[':question/worked-solution']
        fidelity.append({'raw_profile':case['raw_profile'],'raw_metadata_omissions_preserved':True,'raw_prompt_byte_exact':True,'completed_prompt_image_path_normalization_only':True,'source_id':case['source_id'],'prompt_exact':True,'options_matched':5 if observed else 0,'options_total':5 if observed else 0,'original_correct_designation_present':False,'solution_exact':True if ':question/worked-solution' in source else None,'repairs':r['generation']['source_repairs']})
    for level in ('easy','moderate','hard'):
        for seed in (0,1,2,3):records.append(g.generate(level,seed))
    # Changed similarity cases exercise all members of complete opaque evidence banks.
    for profile,level,template,p in [('observed_c','moderate','single',{'a':[4,-7],'names':['c'],'scale':2}),('observed_qr','hard','sum',{'a':[5,-3],'b':[3,6],'names':['q','r'],'scale':2}),('observed_hard','hard','sum',{'a':[-.5,2],'b':[2,-.5],'names':['m','n']})]:records.append(g.generate(level,8,template=template,parameters=p,profile=profile))
    for r in records:
        independent(r);gen=r['generation'];r2=g.generate(r['question'][':question/difficulty'].split('/')[-1],234,template=gen['template'],parameters=gen['parameters'],profile=gen['bank_profile']);assert r['question'][':question/id']==r2['question'][':question/id'];assert sorted(a[':answer/id'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/id'] for a in r2['question'][':question/answer-fields'][0][':answer-field/choices'])
    # Explicit workload rejection, including integer moderate and nonfractional hard.
    for level,p in [('easy',{'a':[.5,2],'names':['a']}),('moderate',{'a':[2,3],'names':['c']}),('hard',{'a':[1,-1],'b':[-2,3],'names':['m','n']}),('easy',{'a':[2,3],'b':[100,100],'names':['a']}),('moderate',{'a':[.5,2],'b':[100,100],'names':['c']})]:
        try:g.generate(level,parameters=p)
        except ValueError:pass
        else:raise AssertionError('invalid explicit workload')
    for profile,level,p in [('observed_c','moderate',{'a':[200,-350],'names':['c'],'scale':100}),('raw_qr','hard',{'a':[250,-150],'b':[150,300],'names':['q','r'],'scale':100})]:
        try:g.generate(level,parameters=p,profile=profile)
        except ValueError:pass
        else:raise AssertionError('unbounded similarity')
    # Fresh atomic renders: same output concurrently and different instance concurrently.
    fresh=HERE/'concurrency';fresh.mkdir(exist_ok=True)
    geo1={'A':[0,0],'B':[-2.5,3],'names':['c'],'grid_increment':.5};geo2={'A':[0,0],'P':[2,-1.5],'B':[.5,2],'names':['m','n'],'grid_increment':.5}
    def call(geometry,key):
        with tempfile.NamedTemporaryFile('w',suffix='.json',dir=fresh,delete=False) as f:json.dump({'geometry':geometry,'output':str(fresh/key)},f);p=Path(f.name)
        try:subprocess.run([str(ROOT/'.venv/bin/python'),str(HERE/'render.py'),str(p)],check=True)
        finally:p.unlink()
    with concurrent.futures.ThreadPoolExecutor(4) as pool:list(pool.map(lambda x:call(*x),[(geo1,'same'),(geo1,'same'),(geo2,'different'),(geo2,'different')]))
    for geo,key in [(geo1,'same'),(geo2,'different')]:assert json.loads((fresh/(key+'.json')).read_text())['geometry']==geo
    assert not list(fresh.glob('tmp*.json')) and not list(fresh.glob('*.tmp*'))
    checks=[]
    for idx,r in enumerate(records):
        field=r['question'][':question/answer-fields'][0];correct=field[':answer-field/correct'][1];checks.append({'label':str(idx),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'actual complete-bank selection'} for a in field[':answer-field/choices']]})
    (HERE/'engine-input.json').write_text(json.dumps(checks));subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    (HERE/'raw-review.json').write_text(json.dumps(raw_records,indent=2)+'\n')
    (HERE/'review.json').write_text(json.dumps(records,indent=2)+'\n')
    review=['# Original evidence and generated variants','The original source JSON is preserved unchanged. Two unrated radios have inferred correct designations; hard has an authored field. Evidence profiles are excluded from learner defaults.']
    for c,r in zip(cases,records):
        original=g.SOURCES[c['source_id']];review+=['## Original '+c['source_id'],original[':question/problem'].replace('images/','/media/jake/SSD/EDB/math/images/'),json.dumps(original.get(':question/answer-fields',[]),indent=2),original.get(':question/worked-solution','No original worked solution captured.')]
    for i,r in enumerate(records):
        q=r['question'];review+=['## Generated '+str(i)+' '+q[':question/difficulty']+' / '+r['generation']['bank_profile'],q[':question/problem'],'\n'.join('$'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices']),q[':question/worked-solution']]
    (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    report={'status':'pass','source_coverage':3,'observed_complete_banks':2,'matched_options':10,'total_options':10,'observed_correct_designations':0,'inferred_correct_designations':2,'authored_hard_field':1,'worked_solutions_exact':1,'worked_solutions_available':1,'raw_source_unrated':2,'raw_metadata_replays':3,'raw_available_solution_byte_exact':1,'completed_available_solution_path_normalized_exact':1,'source_fidelity':fidelity,'independent_displayed_math_records':len(records),'native_grading':json.loads((HERE/'engine-report.json').read_text()),'concurrent_fresh_render_calls':4,'identity_replays':len(records),'database_writes':0,'limitations':['Original correct designations are absent in all three source records; no designation fidelity can be claimed.','Two opaque banks are evidence-only similarity recipes, not recovered error intent.','Hard field/bank authored from independently verified original solution.'],'sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),HERE/'render.py',HERE/'validate.py',ROOT/'generate/runs/current/check-engine']}}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(records),'records; ten of ten observed options; native all choices; concurrent renders')

if __name__ == '__main__':
    main()
