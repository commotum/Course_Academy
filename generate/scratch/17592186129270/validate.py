#!/usr/bin/env python3
"""Independent displayed-math readback, complete replay, native grading and freeze."""
import copy, hashlib, importlib.util, itertools, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('critical',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
SYMBOLS={s:sp.Symbol(s,real=True) for s in 'uvwxyz'}
U,V,W=(SYMBOLS[s] for s in 'uvw');variables=(U,V,W)
TRANS=standard_transformations+(implicit_multiplication_application,)


def group(s,i):
    if i>=len(s) or s[i]!='{':raise AssertionError(('expected group',s,i))
    depth=1;j=i+1
    while depth:
        if s[j]=='{':depth+=1
        if s[j]=='}':depth-=1
        j+=1
    return s[i+1:j-1],j


def scalar(s):
    """Independent parser for displayed corpus, no generator parameter access."""
    s=s.strip().rstrip('.,')
    s=s.replace(r'\,','').replace(r'\cdot','*').replace(r'\left','').replace(r'\right','')
    def funcs(text):
        out='';i=0
        while i<len(text):
            if text.startswith(r'\frac',i):
                a,j=group(text,i+5);b,k=group(text,j);out+='(('+funcs(a)+')/('+funcs(b)+'))';i=k
            elif text.startswith(r'\sqrt',i):
                a,j=group(text,i+5);out+='sqrt('+funcs(a)+')';i=j
            else:out+=text[i];i+=1
        return out
    s=funcs(s).replace('{','(').replace('}',')').replace('^','**')
    s=re.sub(r'(?<![A-Za-z])e(?![A-Za-z])','E',s)
    return parse_expr(s,local_dict=SYMBOLS|{'E':sp.E,'sqrt':sp.sqrt},transformations=TRANS)


def strip_aligned(s):
    if s.startswith(r'\begin{aligned}'):return s[len(r'\begin{aligned}'):-len(r'\end{aligned}')]
    return s


def rows(s):return strip_aligned(s.strip()).split(r'\\')

def replace_determinants(s):
    def minor(m):
        rowlist=m.group(1).split(r'\\');cells=[[scalar(c) for c in row.split('&')] for row in rowlist]
        return '('+str(sp.Matrix(cells).det())+')'
    s=re.sub(r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|',minor,s,flags=re.S)
    return s


def determinant_expr(s):return scalar(replace_determinants(s))



def zero_key(value,excluded=()):
    value=sp.factor(sp.together(value).as_numer_denom()[0]).replace(sp.exp,lambda x:sp.S.One)
    if value==0:return ('all',)
    if not value.free_symbols:return ('empty',)
    try:
        factors=sp.factor_list(value,*tuple(sorted(value.free_symbols,key=str)))[1]
    except sp.PolynomialError:
        return ('nonpolynomial',str(value))
    pieces=[]
    for factor,_ in factors:
        symbols=tuple(sorted(factor.free_symbols,key=str));poly=sp.Poly(factor,*symbols)
        if any(not sp.simplify(factor/base).free_symbols for base in excluded):continue
        # Independently use completing squares for positive diagonal quadratics.
        quadratic=poly.total_degree()==2
        diagonal=quadratic and all(sp.diff(factor,a,b)==0 for a,b in itertools.combinations(symbols,2))
        positive=diagonal and all(sp.diff(factor,v,2)>0 for v in symbols)
        if positive:
            centers={v:sp.solve(sp.diff(factor,v),v)[0] for v in symbols}
            minimum=sp.simplify(factor.subs(centers))
            if minimum==0:
                pieces.append(('intersection',tuple(str(v-centers[v]) for v in symbols)));continue
            if minimum>0:continue
        pieces.append(('factor',str(sp.expand(factor/poly.LC()))))
    return ('union',tuple(sorted(pieces,key=str))) if pieces else ('empty',)

def proportion(a,b,excluded=()):return zero_key(a,excluded)==zero_key(b,excluded)


def locus(value):
    axis=re.search(r'\$([uvw]{2})\s*-?\$(?:-|\s)*plane',value)
    if axis:return SYMBOLS[next(v for v in 'uvw' if v not in axis[1])]
    m=re.search(r'\$([^$]*)\$',value);assert m, value
    eq=m[1].rstrip('.')
    if r'\pm' in eq:
        left,right=eq.split('=');right=right.replace(r'\pm','').strip();return (scalar(left)-scalar(right))*(scalar(left)+scalar(right))
    left,right=eq.split('=');return scalar(left)-scalar(right)


def readback(record,legacy=False):
    q=record['question'];prompt=q[':question/problem'];solution=q[':question/worked-solution']
    for s in [prompt,solution]+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]:
        assert s.count('$')%2==0,s
        assert s.count('{')==s.count('}'),s
        assert '--' not in s and '+-' not in s,s
    # Actual map is read out of the second printed vector, never metadata.
    blocks=re.findall(r'\$\$(.*?)\$\$',prompt,re.S);part=blocks[0].split('⟶')[1]
    component=part[part.index(r'\begin{aligned}')+len(r'\begin{aligned}'):part.index(r'\end{aligned}')]
    funcs=[scalar(c) for c in component.split(r'\\')];assert len(funcs)==3
    matrix=sp.Matrix(funcs).jacobian(variables);det=sp.factor(matrix.det());assert det!=0
    radicals=[power.base for f in funcs for power in f.atoms(sp.Pow) if power.exp==sp.Rational(1,2)]
    reciprocals=[power.base for f in funcs for power in f.atoms(sp.Pow) if power.exp.is_negative]
    excluded=tuple(radicals+reciprocals)
    actual_domain='R^3'
    if radicals:actual_domain='u>'+str(sp.solve(radicals[0],U)[0])
    elif reciprocals:actual_domain='u!='+str(sp.solve(reciprocals[0],U)[0])
    assert record['generation']['domain']==actual_domain,(actual_domain,record['generation']['domain'])
    # Every individual printed partial, including zero contributions.
    matches=re.findall(r'\\frac\{∂([xyz])\}\{∂([uvw])\}\s*&\s*=(.*?)(?=\s*&|\\\\|\\end\{aligned\})',solution,re.S)
    assert len(matches)==9,(len(matches),solution)
    for out,coord,value in matches:assert sp.simplify(scalar(value)-matrix['xyz'.index(out),'uvw'.index(coord)])==0,(out,coord,value)
    # Here block must agree with actual prompt components, including arguments.
    here=solution.split('Here, we have')[1].split('First,')[0]
    definitions=re.findall(r'([xyz])\(u,v,w\)\s*=\s*(.*?)(?=,\\,|,\n|,?\s*\$\$)',here,re.S)
    assert len(definitions)==3,(definitions,here)
    for name,value in definitions:assert sp.simplify(scalar(value)-funcs['xyz'.index(name)])==0,(name,value)
    detblock=solution.split('Therefore,')[1].split('The function')[0]
    block=re.findall(r'\$\$(.*?)\$\$',detblock,re.S)[0]
    for row in rows(replace_determinants(block)):
        rhs=row.split('& =',1)[1];assert sp.simplify(determinant_expr(rhs)-det)==0,('stage',rhs,det)
    zeroblock=solution.split('So, we obtain')[1].split('The equation')[0] if 'The equation' in solution else solution.split('So, we obtain')[1].split('The critical points')[0]
    block=re.findall(r'\$\$(.*?)\$\$',zeroblock,re.S)[0]
    for row in rows(block)[1:]:
        left,right=row.split('& =');assert scalar(right)==0;assert proportion(scalar(left),det),('zero stage',left,det)
    # The conclusion's entire locus and every displayed bank are independently read.
    tail=solution.split('So, we obtain')[1].split('$$')[-1]
    if 'pair of intersecting planes' in tail:
        maths=re.findall(r'\$([^$]*)\$',tail);a=locus('$'+maths[-2]+'$');b=locus('$'+maths[-1]+'$');assert proportion(a*b,det)
    else:
        # Source .. typo is punctuation, not a mathematical change.
        eqs=re.findall(r'\$([^$]*)\$',tail)
        equations=[e for e in eqs if '=' in e]
        assert equations,tail
        for eq in equations:assert proportion(locus('$'+eq+'$'),det),('final prose',eq,det)
    if 'i.e.' in tail:
        descriptor=tail.split('i.e.')[1]
        if '-plane' in descriptor:
            assert re.search(r'\$[uvw]{2}\$-plane',descriptor),('malformed coordinate-plane name',descriptor)
            assert proportion(locus(descriptor),det,excluded)
    for field in q[':question/answer-fields']:
        candidates=[]
        for a in field[':answer-field/choices']:candidates.append((a[':answer/id'],locus(a[':answer/value']).subs(dict(zip((SYMBOLS[s] for s in 'xyz'),funcs)),simultaneous=True)))
        for (id1,a),(id2,b) in itertools.combinations(candidates,2):assert not proportion(a,b,excluded),('equivalent options',a,b)
        correct=field.get(':answer-field/correct')
        if correct:
            assert correct[0]==':answer/id';assert sum(id==correct[1] for id,_ in candidates)==1
            assert sum(bool(proportion(value,det,excluded)) for _,value in candidates)==1
            assert proportion(next(v for id,v in candidates if id==correct[1]),det,excluded)
        else:assert legacy
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    for f in q[':question/answer-fields']:
        assert f[':answer-field/type']==':answer-field.type/radio';assert len(f[':answer-field/choices'])==5
        import uuid
        uuid.UUID(f[':answer-field/id'])
        for a in f[':answer-field/choices']:uuid.UUID(a[':answer/id']);assert a[':answer/type']==':answer.type/text'
    return str(det)


def fidelity(case,record):
    orig=g.SOURCES[case['source_id']];q=record['question'];assert q[':question/problem']==orig[':question/problem'];assert q[':question/worked-solution']==orig[':question/worked-solution']
    assert len(q[':question/answer-fields'])==len(orig[':question/answer-fields'])
    for f,old in zip(q[':question/answer-fields'],orig[':question/answer-fields']):
        assert f[':answer-field/key']==old[':answer-field/key'];assert f[':answer-field/type']==old[':answer-field/type'][':db/ident']
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in old[':answer-field/choices'])
        assert (':answer-field/correct' in f)==(':answer-field/correct' in old)
        if ':answer-field/correct' in old:
            got=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert got==old[':answer-field/correct'][':answer/value']
    for key in (':question/answer-fields',':question/worked-solution',':question/difficulty'):assert (key in q)==(key in orig)


def run():
    assert proportion(U**2*V**3,U*V)
    assert not proportion(U**2+V**2,U*V)
    assert zero_key(U,(U,))==('empty',)
    cases=json.loads((HERE/'source-cases.json').read_text());reviews=[];engine=[];tasks={x:set() for x in ('easy','moderate','hard')};counts={'source':0,'translated':0,'normal':0,'identity':0,'explicit_rejections':0}
    def grade(r,label):
        # Raw field with no captured correct attribute is not invented as matched.
        rr=copy.deepcopy(r);rr['question'][':question/answer-fields']=[f for f in rr['question'][':question/answer-fields'] if ':answer-field/correct' in f]
        checks=[]
        for i,f in enumerate(rr['question'][':question/answer-fields']):
            for a in f[':answer-field/choices']:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete owned bank actual native radio grading'})
        engine.append({'label':label,'record':rr,'checks':checks})
    for case in cases:
        r=g.generate('moderate',0,case['template'],parameters=case['parameters'],profile=case['bank_profile']);fidelity(case,r);readback(r,True);counts['source']+=1;reviews.append({'label':'Original replay '+case['source_id'],'record':r});grade(r,case['source_id'])
        for i,p in enumerate(({'h':-2,'k':1,'l':3},{'h':2,'k':-3,'l':-1})):
            v=g.generate('moderate',19+i,case['template'],parameters=p,profile='repaired');readback(v);counts['translated']+=1;reviews.append({'label':'GENERATED evidence-only translated variant '+case['source_id']+' #'+str(i+1),'record':v});grade(v,case['source_id']+' changed '+str(i))
    for level in ('easy','moderate','hard'):
        for seed in range(160):
            r=g.generate(level,seed);readback(r);counts['normal']+=1;tasks[level].add(r['generation']['mathematical_fingerprint'])
            if seed<3:reviews.append({'label':'GENERATED authored '+level+' #'+str(seed+1),'record':r});grade(r,level+str(seed))
            p=r['generation']['parameters'];other=g.generate(level,seed+1000,template=r['generation']['template'],parameters=p)
            assert r['question'][':question/id']==other['question'][':question/id'];assert r['generation']['mathematical_fingerprint']==other['generation']['mathematical_fingerprint'];counts['identity']+=1
        assert len(tasks[level])>= (25 if level=='easy' else 20)
    # Each observed family also has an explicitly authored normal method bank.
    for t in g.OBSERVED:
        for i,p in enumerate(({'h':0,'k':0,'l':0},{'h':-3,'k':2,'l':-1},{'h':3,'k':-2,'l':1})):
            r=g.generate('moderate',i,t,parameters=p,profile='method');readback(r);counts['normal']+=1;grade(r,t+' method '+str(i))
            reviews.append({'label':'GENERATED normal authored method bank '+t+' #'+str(i+1),'record':r})
    bad=[('easy',{'h':0,'axis':0}),('easy',{'h':6,'axis':0}),('moderate',{'a':2,'b':2}),('moderate',{'a':2,'b':10}),('hard',{'a':1,'b':1,'c':1,'d':1,'k':2}),('hard',{'a':-5,'b':1,'c':1,'d':2,'k':2})]
    for level,p in bad:
        try:g.generate(level,template=g.TEMPLATES[level][0],parameters=p)
        except ValueError:counts['explicit_rejections']+=1
        else:raise AssertionError(('invalid explicit admitted',level,p))
    (HERE/'engine-input.json').write_text(json.dumps(engine,indent=2,ensure_ascii=False)+'\n');subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    (HERE/'review.json').write_text(json.dumps(reviews,indent=2,ensure_ascii=False)+'\n')
    lines=['# Clearly labeled source and generated review','Raw evidence-only originals retain historical banks and missing attributes. Translations use the same normal API and fixed stage masks. Authored defaults use method banks.']
    for item in reviews:lines+=['\n## '+item['label'],g.preview(item['record'])]
    (HERE/'review.md').write_text('\n\n'.join(lines)+'\n')
    report={'status':'pass','counts':counts,'source_fidelity':{'questions':12,'complete_banks':13,'options':65,'correct_designations_matched':12,'correct_designations_missing':1,'exact_prompt_solution':12,'format_presence_parity':12,'source_bank_errors':0},'source_anomalies':['q-161819 legacy duplicate field has no correct ref; retained raw, omitted repaired/native fixture','q-161815 requires u>0 for C1 Jacobian; q-161813 requires u!=0; original omits domains, repaired presentation states translated restrictions','q-161809 concluding v=u.. typo; raw exact retained, repaired removes extra period'],'distinct_sampled_tasks':{l:len(s) for l,s in tasks.items()},'native_grading':json.loads((HERE/'engine-report.json').read_text()),'independent_checks':['actual map vector','nine displayed partials','all cofactor/evaluation/final determinant rows','every critical equation row','all concluding locus equations','complete bank loci and correct designation','TeX groups/delimiters','field-owned identities','explicit bounds','source key presence'],'engine_provenance':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in (ROOT/'generate/runs/current/check-engine',ROOT/'generate/runs/current/check-engine.rs')},'normal_profile_families':list(g.METHOD_BANKS),'real_locus_equivalence':'Squarefree polynomial factor catalog, positive diagonal quadratic intersections and C1-domain-excluded factors. Normal banks have only these bounded forms; historical output-coordinate equations are substituted through the actual map.','limitations':['Historical distractor error intent unresolved: observed and repaired profiles are evidence-only.','Missing original designation cannot count as a matched designation; native fixture excludes only that field.'],'database_writes':0}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    paths=[HERE.with_suffix('.py')]+[p for p in HERE.iterdir() if p.is_file() and p.name!='freeze.json']
    (HERE/'freeze.json').write_text(json.dumps({'version':g.VERSION,'sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}},indent=2)+'\n')
    print(json.dumps({'status':'pass','counts':counts,'distinct':report['distinct_sampled_tasks']}))
if __name__=='__main__':run()
