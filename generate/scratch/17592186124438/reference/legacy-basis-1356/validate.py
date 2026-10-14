#!/usr/bin/env python3
"""Independent printed-data, source/full-bank, structure and native-engine checks."""
import copy, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
import sympy as sp
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('tangent',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def check_format(s):
    assert s.count('$')%2==0,'math delimiters'
    depth=0
    for i,c in enumerate(s):
        if c in '{}':
            if i and s[i-1]=='\\':continue
            depth+=1 if c=='{' else -1
            assert depth>=0,'TeX groups'
    assert depth==0,('TeX groups',depth,s)
    assert not re.search(r'(?<!\\)\{\\begin',s),'unescaped opening system brace'
    assert not re.search(r'(?<!\\)\\\\(?:begin|end)',s),'doubled command bytes'
def replace_eval(s,pattern,value):
    m=re.search(pattern,s)
    if not m:return s
    i=m.end();assert s[i]=='{'
    depth=1;j=i+1
    while depth:
        depth+=(s[j]=='{')-(s[j]=='}');j+=1
    return s[:m.start()]+value+s[j:]
def assert_math(r,raw=False):
    q=r['question'];assert set(r['knowledge_point'])=={'db_id','id','title'}
    coords,v,der=g.point_data(q); a,b,h=map(g.parse,coords);u=g.x if v=='y' else g.y;u0=a if u==g.x else b;v0=b if v=='y' else a
    partial=re.search(r'and that \$(.*?)\$, find',q[':question/problem']).group(1)
    assert re.search(r'_\{?([xy])',partial).group(1)==str(u),'partial direction'
    d=g.parse(der);m=sp.simplify(d.subs({g.x:a,g.y:b}));target=g.relation(v,v0,m*(u-u0)+h)
    # Read every actual derivative-evaluation stage, not saved intermediate data.
    blocks=g.blocks(q[':question/worked-solution']);assert len(blocks)==3
    first=g.rhs_rows(blocks[0]);assert len(first)>=2
    initial=g.rows(blocks[0])[0].split('=',1)[0]
    evaluated=re.search(r'\((.*)\)',initial).group(1).split(',')
    assert tuple(map(g.parse,evaluated))==(a,b),'evaluated coordinate label'
    if r['generation']['template'] in g.TEMPLATES:
        original=g.TEMPLATES[r['generation']['template']]
        _,_,base_der=g.point_data(original);scale=sp.simplify(d/g.parse(base_der))
        source_stages=g.rhs_rows(g.blocks(original[':question/worked-solution'])[0])
        assert len(first)==len(source_stages),'operative row count'
        for got,old in zip(first[:-1],source_stages[:-1]):
            expected=old if scale==1 else g.tex(scale)+r'\left('+old+r'\right)'
            assert re.sub(r'\s+','',got)==re.sub(r'\s+','',expected),'operative stage structure'
    elif r['generation']['template']=='canonical_trig':
        assert len(first)==3 and first[0].count(r'\cos')==2 and r'\cos' not in first[1] and first[1].count(')(')==1,'canonical trig stages'
    else:
        assert len(first)==2 and '(' in first[0],'single-component substitution stage'
    for expression in first:assert sp.simplify(g.parse(expression)-m)==0,('slope stage',expression,m)
    # Read complete substituted point-slope equations, including rearrangement.
    ps=g.rows(blocks[1]);assert len(ps)>=3
    formal=r'\\frac\{∂z\}\{∂[xy]\}\{\|\}_\{\([^}]*\)\}'
    for i,row in enumerate(ps):
        lhs,rhs=row.replace('&','').split('=',1)
        if i==0:
            lhs=replace_eval(lhs,r'z\{\|\}_',g.tex(h))
            rhs=replace_eval(rhs,r'\\frac\{∂z\}\{∂[xy]\}\{\|\}_','('+g.tex(m)+')')
        assert sp.simplify(g.parse(lhs)-g.parse(rhs)-(g.z-m*(u-u0)-h))==0,('line stage',row)
    assert g.line_key(r'\{\begin{aligned}'+blocks[-1]+r'\end{aligned}')==g.line_key(target),'conclusion'
    assert q[':question/worked-solution'].count('P('+','.join(coords)+')')>=2,'prose point'
    for f in q[':question/answer-fields']:
        keys=[g.line_key(a[':answer/value']) for a in f[':answer-field/choices']]
        assert len(keys)==5 and len(set(keys))==5,'complete line ambiguity'
        assert sum(k==g.line_key(target) for k in keys)==1,'tangent point/slope'
        if ':answer-field/correct' in f:
            cv=next(t for t in f[':answer-field/choices'] if t[':answer/id']==f[':answer-field/correct'][1]);assert g.line_key(cv[':answer/value'])==g.line_key(target)
        if not raw:
            for choice in f[':answer-field/choices']:check_format(choice[':answer/value'])
    if not raw:
        check_format(q[':question/problem']);check_format(q[':question/worked-solution'])
    return True

def main():
    cases=[];review=[];engine=[];counts={'source_questions':0,'banks':0,'choices':0,'correct_designations':0,'raw_exact_prompts':0,'raw_exact_solutions':0,'raw_choice_strings':0,'missing_correct_designations':0}
    for name,src in g.TEMPLATES.items():
        z0=g.parse(g.point_data(src)[0][2]);params={'scale':'1','z':str(z0)}
        case={'source_id':src[':question/id'],'math_academy_id':name,'template':name,'parameters':params,'bank_profile':'raw_'+name};cases.append(case)
        r=g.generate('moderate',template=name,parameters=params,profile='raw_'+name);assert_math(r,True)
        q=r['question'];assert q[':question/difficulty']==src[':question/difficulty'][':db/ident'],'captured difficulty VALUE'
        assert q[':question/problem']==src[':question/problem'];assert q[':question/worked-solution']==src[':question/worked-solution']
        counts['source_questions']+=1;counts['raw_exact_prompts']+=1;counts['raw_exact_solutions']+=1
        for sf,f in zip(src[':question/answer-fields'],q[':question/answer-fields'],strict=True):
            assert f[':answer-field/type']==sf[':answer-field/type'][':db/ident'];assert f[':answer-field/key']==sf[':answer-field/key']
            assert (':answer-field/correct' in f)==(':answer-field/correct' in sf),'correct presence'
            observed=sorted(a[':answer/value'] for a in sf[':answer-field/choices']);generated=sorted(a[':answer/value'] for a in f[':answer-field/choices']);assert observed==generated
            assert sorted(map(g.line_key,observed),key=str)==sorted(map(g.line_key,generated),key=str)
            counts['banks']+=1;counts['choices']+=len(observed);counts['raw_choice_strings']+=len(observed)
            if ':answer-field/correct' in f:counts['correct_designations']+=1
            else:counts['missing_correct_designations']+=1
        review.append({'label':'original public raw evidence '+name,'record':r})
        # Non-anchor replay proves parameterized evidence recipes are operative.
        rr=g.generate('moderate',template=name,parameters={'scale':2,'z':7},profile='raw_'+name);assert_math(rr,True)
        review.append({'label':'generated raw evidence variant '+name,'record':rr})
        for seed in (7,11):
            normal=g.generate('moderate',seed,template=name);assert_math(normal);review.append({'label':'generated authored operation bank '+name,'record':normal})
    for level in ('easy','hard'):
        for seed in (7,11):
            r=g.generate(level,seed);assert_math(r);review.append({'label':'generated authored '+level,'record':r})
    unique={l:set() for l in ('easy','moderate','hard')};families=set()
    for level in unique:
        for seed in range(80):
            r=g.generate(level,seed);assert_math(r);unique[level].add(r['generation']['mathematical_fingerprint'])
            if level=='moderate':families.add(r['generation']['template'])
            p=r['generation']['parameters'];t=r['generation']['template'];p0=r['generation']['profile']
            again=g.generate(level,999,template=t,parameters=p,profile=p0)
            assert r['question'][':question/id']==again['question'][':question/id']
            # JSON roundtrip must preserve the complete metadata and record.
            assert json.loads(json.dumps(r))==r
            assert g.generate(level,seed,template=t,parameters=p,profile=p0)==r,'complete fresh/repeated-record equality'
            if seed<4:review.append({'label':'sample '+level+' '+str(seed),'record':r})
    assert families==set(g.TEMPLATES),'default family coverage'
    for level,p in [('easy',{'a':0,'b':1,'k':1,'z':1}),('moderate',{'scale':4,'z':1}),('hard',{'a':1,'k':0,'z':1})]:
        try:g.generate(level,parameters=p)
        except ValueError:pass
        else:raise AssertionError('bounds accepted')
    boundaries=0
    for template in g.TEMPLATES:
        for parameters in ({'scale':-3,'z':'1/2'},{'scale':3,'z':'2*pi'}):
            assert_math(g.generate_moderate(template=template,parameters=parameters));boundaries+=1
    for parameters in ({'a':-4,'b':4,'k':-4,'z':-12},{'a':4,'b':-4,'k':4,'z':12}):
        assert_math(g.generate_easy(parameters=parameters));boundaries+=1
    for parameters in ({'a':-4,'k':-3,'z':12},{'a':4,'k':3,'z':-12}):
        assert_math(g.generate_hard(parameters=parameters));boundaries+=1
    # Algebraically equivalent collapse must still fail source operation structure.
    collapsed=copy.deepcopy(g.generate_moderate(7,template='q-132595'))
    bb=g.blocks(collapsed['question'][':question/worked-solution'])[0];rr=g.rows(bb);rr[0]=rr[0].split('=',1)[0]+'='+g.rhs_rows(bb)[-1];collapsed['question'][':question/worked-solution']=collapsed['question'][':question/worked-solution'].replace(bb,r' \\ '.join(rr),1)
    try:assert_math(collapsed)
    except AssertionError:pass
    else:raise AssertionError('collapsed source operation survived')
    # Nonzero scalar equivalence of full relations, and a geometry near-miss.
    assert g.line_key(r'\{\begin{aligned}2y=4 \\ 3z=6x+9\end{aligned}')==g.line_key(g.relation('y',2,2*g.x+3))
    assert g.line_key(g.relation('y',2,2*g.x+3))!=g.line_key(g.relation('x',2,2*g.y+3))
    # Mutation regressions: every printed operation and final prose checked.
    test=g.generate_hard(7)
    for transform in [lambda s:s.replace(' & =',' & =1+',1),lambda s:s.replace('z & =','z & =1+',1),lambda s:s.replace('P(', 'P(9,',1)]:
        bad=copy.deepcopy(test);bad['question'][':question/worked-solution']=transform(bad['question'][':question/worked-solution'])
        try:assert_math(bad)
        except (AssertionError,ValueError):pass
        else:raise AssertionError('mutation survived')
    for item in review:
        r=item['record'];fields=r['question'][':question/answer-fields']
        if any(':answer-field/correct' not in f for f in fields):
            r=copy.deepcopy(r);fields=r['question'][':question/answer-fields']
            cs,v,der=g.point_data(r['question']);a,b,h=map(g.parse,cs);u=g.x if v=='y' else g.y;u0=a if u==g.x else b;v0=b if v=='y' else a;m=g.parse(der).subs({g.x:a,g.y:b}).simplify();target=g.relation(v,v0,m*(u-u0)+h)
            for f in fields:
                if ':answer-field/correct' not in f:
                    inferred=next(t for t in f[':answer-field/choices'] if g.line_key(t[':answer/value'])==g.line_key(target));f[':answer-field/correct']=[':answer/id',inferred[':answer/id']]
            r['generation']['native_fixture_repairs']=['legacy correct designation independently inferred; raw API retains omission']
        checks=[]
        for i,f in enumerate(fields):
            for a in f[':answer-field/choices']:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'native selection, independently verified whole-line geometry'})
        engine.append({'label':item['label']+(' [legacy designation inferred for native fixture]' if 'native_fixture_repairs' in r['generation'] else ''),'record':r,'checks':checks})
    (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(HERE/'review.json').write_text(json.dumps(review,indent=2)+'\n');(HERE/'engine-input.json').write_text(json.dumps(engine,indent=2)+'\n')
    exe=HERE.parent.parent/'runs/current/check-engine';report=HERE/'engine-report.json';subprocess.run([str(exe),str(HERE/'engine-input.json'),str(report)],check=True)
    native=json.loads(report.read_text());result={'status':'passed','fidelity':counts,'generated_mathematical_checks':240,'boundary_mathematical_checks':boundaries,'sampled_unique_tasks':{k:len(v) for k,v in unique.items()},'normal_default_families':sorted(families),'native':{k:native[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'raw_native_ungradeable_records':2,'native_repaired_legacy_records':2,'limitations':['q-36369 raw duplicate legacy field has no captured correct designation; the two faithful raw records lack a valid fixture, so separately labeled native copies infer that designation mathematically and grade both fields; raw API retains omission.','Observed distractor intent underdetermined: public raw profiles preserve whole affine vertical transformations; normal banks independently authored.','Moderate source coordinates fixed to preserve original arithmetic, varying nonzero scale and altitude.'],'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'engine_sha256':hashlib.sha256(exe.read_bytes()).hexdigest(),'database_writes':0}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    (HERE/'review.md').write_text('# Original evidence and generated variants\n\nAll raw entries are evidence only; authored normal banks are labeled.\n\n'+'\n\n---\n\n'.join('## '+i['label']+'\n\n'+g.markdown(i['record']) for i in review)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
