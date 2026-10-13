#!/usr/bin/env python3
"""Read actual ODE/condition/options/stages; preserve absence and separate grading."""
import importlib.util,json,re,hashlib,subprocess
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
D=s.Symbol('D',real=True)

def save(name,v):(HERE/name).write_text(json.dumps(v,indent=2)+'\n')
def eq(a,b):
    a=s.sympify(a);b=s.sympify(b)
    # All logarithmic source intervals contain x=0, hence 1+2x>0.
    diff=s.simplify((a-b).replace(s.Abs,lambda z:z).replace(s.sign,lambda z:s.Integer(1)))
    assert diff==0,(a,b,diff)
def formatting(t):
    assert t.count('$')%2==0
    n=0
    for c in re.sub(r'\\[{}]','',t):
        if c=='{':n+=1
        if c=='}':n-=1
        assert n>=0
    assert n==0
    assert '--' not in t and '+-' not in t and '+ -' not in t

def clean(t):return t.strip().rstrip('.').replace(r'\,','').strip()
def ode(q):
    text=q[':question/problem'];ic=re.search(r'([fgy])\(([-\d]+)\)\s*=\s*(-?\d+)',text);assert ic,text
    name,t,v=ic.groups();t=s.Integer(t);v=s.Integer(v)
    math=re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',text,re.S)
    ode=None
    for a,b in math:
        m=clean(a or b)
        if '′' not in m and "'" not in m and r'\text{d}y' not in m:continue
        m=m.replace(r'\frac{\text{d}y}{\text{d}x}','D')
        m=re.sub(r'\{?[fgy]\}?\^\{′\}(?:\(x\))?','D',m)
        m=re.sub(r"[fgy]'(?:\(x\))?",'D',m)
        m=m.replace("y^{′}",'D')
        m=m.replace('D',r'\mathit{Q}')
        left,right=m.split('=');left=left.replace(r'\mathit{Q}','Q');right=right.replace(r'\mathit{Q}','Q')
        expr=g.parse(left)-g.parse(right);Q=next(z for z in expr.free_symbols if str(z)=='Q');der=s.solve(expr,Q)[0];ode=der;break
    assert ode is not None,text
    return ode,t,v,name

def integral_value(rhs,solution):
    while r'\int' in rhs:
        match=re.search(r'\\int\s*(.*?)\\text\{d\}([xu])',rhs,re.S)
        assert match,('unparsed integral',rhs)
        inside=clean(match.group(1));var=g.X if match.group(2)=='x' else s.Symbol('u',real=True)
        value=s.integrate(g.parse(inside) if inside else s.Integer(1),var)
        rhs=rhs[:match.start()]+'('+g.tex(value)+')'+rhs[match.end():]
    value=g.parse(rhs)
    if value.has(s.Symbol('u',real=True)):
        u=re.search(r'Let \$u=(.*?)\.\$',solution).group(1)
        value=value.subs(s.Symbol('u',real=True),g.parse(u))
    return value

def response(q):
    f=q[':question/answer-fields'][0];vals=[g.parse(a[':answer/value'].split('=')[-1]) for a in f[':answer-field/choices']]
    if f[':answer-field/type'].endswith('blank'):
        assert len(vals)==1 and '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
        prefix=re.search(r'\$[^$]*?=([^$]*)\$\{\{field-1\}\}',q[':question/problem'])
        assert prefix,q[':question/problem'];part=clean(prefix.group(1)).rstrip('+');full=vals[0]+(g.parse(part) if part else 0)
        return vals,[full]
    return vals,vals

def readback(r,raw=False):
    q=r['question'];assert set(r['knowledge_point'])=={'db_id','id','title'}
    assert r['generation']['evidence_only']==r['generation']['profile'].startswith('observed_')
    assert r['generation']['eligible_for_learning']==(not r['generation']['evidence_only'])
    formatting(q[':question/problem']);der,t,v,name=ode(q);vals,full=response(q)
    valid=[]
    for z in full:
        try:eq(s.diff(z,g.X),der);eq(z.subs(g.X,t),v);valid.append(True)
        except AssertionError:valid.append(False)
    assert sum(valid)==1,(r['generation'],vals,der,t,v,valid)
    field=q[':question/answer-fields'][0]
    owned_correct=field.get(':answer-field/correct',[None,None])[1]
    correct_value=next((a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==owned_correct),None)
    presence={'difficulty':q.get(':question/difficulty','').split('/')[-1] or None,'solution':':question/worked-solution' in q,'correct_value':correct_value}
    assert r['generation']['content_hash']==g.fingerprint([g.VERSION,q[':question/problem'],q.get(':question/worked-solution'),field[':answer-field/type'].split('/')[-1],field[':answer-field/key'],sorted(a[':answer/value'] for a in field[':answer-field/choices']),presence])
    if field[':answer-field/type'].endswith('radio'):
        for a in field[':answer-field/choices']:
            assert a[':answer/value'].split('=')[0].strip()==('y' if name=='y' else name+'(x)')
    for val in vals:assert val.free_symbols <= {g.X}
    ids=[a[':answer/id'] for a in field[':answer-field/choices']];assert len(ids)==len(set(ids))
    if ':answer-field/correct' in field:
        actual=field[':answer-field/correct'][1];assert actual in ids and valid[ids.index(actual)]
    for i,a in enumerate(vals):
        for b in vals[i+1:]:assert s.simplify(a-b)!=0
    sol=q.get(':question/worked-solution')
    if sol:
        formatting(sol)
        # ODE output and final expression are read from the displayed blocks.
        blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)
        final=clean(blocks[-1]);lhs,rhs=final.split('=',1);z=g.parse(rhs)
        eq(s.diff(z,g.X),der);eq(z.subs(g.X,t),v)
        known_bad=r['generation']['template']=='q-50044' and raw
        assert lhs in ('y','f(x)','g(x)')
        if not known_bad:assert lhs==('y' if name=='y' else name+'(x)')
        # Every arithmetic row in the initial-condition block includes actual C.
        aligned=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)
        cond=aligned[-1];rows=re.split(r'\\\\',cond)
        k=s.simplify((z-s.integrate(der,g.X)).replace(s.Abs,lambda u:u))
        assert not k.has(g.X)
        for row in rows:
            if '&' not in row:continue
            l,rhs=row.split('&',1);l=clean(l);rhs=clean(rhs.lstrip().lstrip('='))
            if l in ('y','f(x)','g(x)'):continue
            eq(g.parse(l).subs(g.C,k),g.parse(rhs).subs(g.C,k))
        # Every nonintegral primitive row before condition must differentiate
        # to the independently read ODE. Individual factors remain unevaluated.
        for block in aligned[:-1]:
            for row in re.split(r'\\\\',block):
                if '&' not in row:continue
                l,rhs=row.split('&',1);rhs=clean(rhs.lstrip().lstrip('='))
                if r'\int' in rhs:
                    eq(s.diff(integral_value(rhs,sol),g.X),der);continue
                value=g.parse(rhs)
                if value.has(s.Symbol('u',real=True)):
                    u=re.search(r'Let \$u=(.*?)\.\$',sol).group(1);value=value.subs(s.Symbol('u',real=True),g.parse(u))
                eq(s.diff(value,g.X),der)
    return vals,valid

def engine_case(r,label):
    f=r['question'][':question/answer-fields'][0];checks=[]
    if f[':answer-field/type'].endswith('radio'):
        for a in f[':answer-field/choices']:checks.append({'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every owned radio option'})
    else:
        a=f[':answer-field/choices'][0][':answer/value'];z=g.parse(a)
        alternate=g.tex(s.expand(z))
        if alternate==a:alternate='('+a+')+'+r'\sin^2(x)+\cos^2(x)-1'
        checks=[{'submitted':a,'expected':'accepted','purpose':'Canonical exact fragment'}, {'submitted':alternate,'expected':'accepted','purpose':'Expanded or trigonometric identity equivalent fragment'}, {'submitted':g.tex(z+1),'expected':'rejected','purpose':'Incorrect constant'}]
    return {'label':label,'record':r,'checks':checks}

def run():
    cases=[];originals=[];variants=[];engine=[];counts={'practice_sources':len(g.QUESTIONS),'prompts':0,'solutions_present':0,'solutions_exact':0,'option_values':0,'banks':0,'correct_designations_present':0,'absence_parity':0};variants_by_level={l:[] for l in ('easy','moderate','hard')}
    for t,q in g.QUESTIONS.items():
        print('Source',t,flush=True)
        lev=q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/easy').split('/')[-1];b=g.DEFS[t][3]
        case={'source_id':t,'template':t,'level':lev,'parameters':{'target':b},'bank_profile':'observed_raw','level_authored_if_unrated':':question/difficulty' not in q};cases.append(case)
        raw=g.generate(lev,template=t,parameters=case['parameters'],profile='observed_raw');z=raw['question'];readback(raw,True)
        assert q[':question/problem']==z[':question/problem'];counts['prompts']+=1
        if ':question/worked-solution' in q:
            counts['solutions_present']+=1;assert q[':question/worked-solution']==z[':question/worked-solution'];counts['solutions_exact']+=1
        assert set(q)-{':db/id',':question/id',':question/math-academy-id'}==set(z)-{':question/id'}
        for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in z)
        sf=q[':question/answer-fields'][0];gf=z[':question/answer-fields'][0]
        assert set(sf)-{':db/id',':answer-field/id'}==set(gf)-{':answer-field/id'}
        assert (':answer-field/correct' in sf)==(':answer-field/correct' in gf);counts['absence_parity']+=1
        sv=[g.parse(a[':answer/value'].split('=')[-1]) for a in sf[':answer-field/choices']]
        gv=[g.parse(a[':answer/value'].split('=')[-1]) for a in gf[':answer-field/choices']]
        assert len(sv)==len(gv)
        for a in sv:assert sum(s.simplify(a-b)==0 for b in gv)==1
        # Verify the explicit symbolic recipes actually map to every source option.
        for a,bexpr in zip(sv,g.DEFS[t][5]):eq(a,bexpr)
        counts['option_values']+=len(sv);counts['banks']+=1
        if ':answer-field/correct' in sf:counts['correct_designations_present']+=1
        if t not in ('q-119078','q-49942','q-119045','q-50044'):
            alias=g.generate(lev,template=t,parameters=case['parameters'],profile='observed_repaired');assert alias['question'][':question/id']==raw['question'][':question/id']
        originals.append({'source_id':t,'raw':raw,'repaired':g.generate(lev,template=t,parameters=case['parameters'],profile='observed_repaired')})
        repaired=originals[-1]['repaired'];readback(repaired);engine.append(engine_case(repaired,t))
        var=g.generate(lev,seed=15,template=t,parameters={'target':b+2},profile='observed_repaired');readback(var);variants.append(var)
    # Independent moderate/hard/easy authored runs cover both layouts, signed
    # coefficients and function names; each whole selected bank must stay valid.
    fingerprints={l:set() for l in variants_by_level};generated=0
    for lev in variants_by_level:
        for seed in range(40):
            for kind in ('blank','radio'):
                r=g.generate(lev,seed=seed,field_type=kind);readback(r);fingerprints[lev].add(r['generation']['math_fingerprint']);generated+=1
                if seed<2:variants_by_level[lev].append(r);engine.append(engine_case(r,lev+'-'+str(seed)+'-'+kind))
                r2=g.generate(lev,seed=seed+1000,field_type=kind,template=r['generation']['template'],parameters=r['generation']['parameters']);assert r['question'][':question/id']==r2['question'][':question/id']
    # Verify explicit requests outside each level's workload fail, no resampling.
    for lev in ('easy','moderate','hard'):
        r=g.generate(lev,field_type='blank');p=dict(r['generation']['parameters']);p['a']=100
        try:g.generate(lev,parameters=p)
        except AssertionError:pass
        else:raise AssertionError('bounds accepted')
        for key,value in [('a','3/2'),('a','10000000000000000000000000000000000000001/10000000000000000000000000000000000000000'),('v','1/2'),('t','1/2')]+([('b','3/2')] if lev in ('moderate','hard') else [])+([('d','3/2')] if lev=='hard' else []):
            invalid=dict(r['generation']['parameters']);invalid[key]=value
            try:g.generate(lev,parameters=invalid)
            except AssertionError:pass
            else:raise AssertionError('fractional workload accepted: '+lev+' '+key)
    save('source-cases.json',cases);save('review.json',{'originals':originals,'observed_variants':variants,'authored_variants':variants_by_level});save('engine-input.json',engine)
    command=['generate/runs/current/check-engine',str(HERE/'engine-input.json'),str(HERE/'engine-validation.json')]
    subprocess.run(command,check=True)
    native=json.loads((HERE/'engine-validation.json').read_text())
    report={'status':'pass','source':{k:SOURCE for k,SOURCE in g.SOURCE.items() if k!='record'},'fidelity':counts,'generated_math_checked':generated,'task_counts_in_sample':{l:len(v) for l,v in fingerprints.items()},'native':{'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':native['documented_unresolved_checks']},'raw_anomalies':['q-119078 and q-49942 lack difficulty, worked solution and correct ref; retained absent in raw replay','q-119045 general solution calls dependent variable y; repaired to f(x)','q-50044 primitive has extraneous dx and final dependent label f(x); repaired to +C and y'],'source_designation_inference':{'observed':counts['correct_designations_present'],'inferred':2},'hard_authored':True,'bank_rendering':'standard TeX normalization from explicit symbolic recipes; raw source strings retained as evidence','database_writes':0}
    save('validation.json',report)
    review='# Particular-solution generator review\n\nObserved raw originals preserve absent attributes and teaching errors. Repaired variants are labeled. No plots.\n\n'
    for item,var in zip(originals,variants):review+='## '+item['source_id']+' — '+('unrated (authored easy in repaired completion)' if ':question/difficulty' not in g.QUESTIONS[item['source_id']] else g.QUESTIONS[item['source_id']][':question/difficulty'][':db/ident'].split('/')[-1])+' — original raw replay\n\n'+g.markdown(item['raw'])+'\n\n### '+var['question'][':question/difficulty'].split('/')[-1]+' — generated initial-ordinate variant (repaired source presentation)\n\n'+g.markdown(var)+'\n\n'
    for l,rs in variants_by_level.items():
        for i,r in enumerate(rs):review+='## '+l+' authored peer '+str(i+1)+'\n\n'+g.markdown(r)+'\n\n'
    (HERE/'review.md').write_text(review)
    print(json.dumps(report,indent=2))
if __name__=='__main__':run()
