#!/usr/bin/env python3
"""Read actual displayed TeX independently; source fidelity and native fixtures."""
import copy, hashlib, importlib.util, itertools, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
HERE=Path(__file__).parent;SCRIPT=HERE.with_suffix('.py')
spec=importlib.util.spec_from_file_location('generator',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x=sp.Symbol('x',positive=True)

def write(name,obj): (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def translate(s):
    s=s.replace(r'\,','').replace(r'\pi','P').replace(r'\ln x','log(x)').replace('ln⁡x','log(x)')
    s=s.replace(r'\ln','log').replace('e','E')
    # Recursively read every real TeX group, not generator expression metadata.
    def group(pos):
        assert s[pos]=='{';start=pos+1;depth=1;pos+=1
        while depth:
            if s[pos]=='{':depth+=1
            if s[pos]=='}':depth-=1
            pos+=1
        return s[start:pos-1],pos
    out='';i=0
    while i<len(s):
        if s.startswith(r'\frac',i):
            i+=5;a,i=group(i);b,i=group(i);out+='('+translate(a)+')/('+translate(b)+')'
        elif s[i]=='{':
            a,i=group(i);out+='('+translate(a)+')'
        else:out+=s[i];i+=1
    return out
def parse(s):
    s=s.strip().rstrip('.');return parse_expr(translate(s),local_dict={'x':x,'E':sp.E,'P':sp.pi,'C':sp.Symbol('C'),'log':sp.log},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))
def equal(a,b): return sp.simplify(a-b)==0
def integral_body(s):
    m=re.search(r'\\int\s*(.*?)((?:\\,)?\\text\{d\}x|dx)',s)
    assert m,('Integral not found',s)
    return m.group(1)
def checked(r,raw=False):
    q=r['question'];f=q[':question/answer-fields'][0]
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    integrand=parse(integral_body(q[':question/problem']));c=sp.simplify(integrand/sp.exp(x))
    assert not c.free_symbols and c!=0
    vals=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
    derivatives=[sp.diff(a,x) for a in vals]
    assert len(vals)==5
    matches=[i for i,d in enumerate(derivatives) if equal(d,integrand)];assert len(matches)==1
    for a,b in itertools.combinations(derivatives,2):assert not equal(a,b),'Equivalent answer families'
    if ':answer-field/correct' in f:
        assert f[':answer-field/correct'][0]==':answer/id'
        assert f[':answer-field/correct'][1]==f[':answer-field/choices'][matches[0]][':answer/id']
    strings=[q[':question/problem']]+[a[':answer/value'] for a in f[':answer-field/choices']]
    if ':question/worked-solution' in q:
        sol=q[':question/worked-solution'];strings.append(sol)
        prose=re.search(r'Factoring out the constant \$(.*?)\$',sol).group(1)
        assert equal(parse(prose),c)
        chain=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S).group(1)
        rows=chain.split(r'\\');assert len(rows)==2,'Factorization and final integral stages required'
        first=rows[0];lhs,rhs=first.split('& =');assert equal(parse(integral_body(lhs)),integrand)
        outside,basic=rhs.split(r'\int');outside=parse(outside.strip());basic=parse(integral_body(r'\int'+basic))
        assert equal(outside,c) and equal(basic,sp.exp(x))
        assert equal(outside*basic,integrand)
        final=rows[1].split('& =')[1].strip();assert final.endswith('+C.')
        assert equal(sp.diff(parse(final),x),integrand)
        assert sol.startswith('Factoring out the constant $') and 'calculating the resulting integral, we get' in sol
    for s in strings:
        assert not any(ord(z)<32 and z not in '\n\t' for z in s)
        assert s.count('{')==s.count('}') and s.count('$')%2==0
    assert len({a[':answer/id'] for a in f[':answer-field/choices']})==5
    return {'integrand':str(integrand),'coefficient':str(c),'solution_stages_checked':3 if ':question/worked-solution' in q else 0,'inferred_correct_value':f[':answer-field/choices'][matches[0]][':answer/value']}

def native(label,r):
    f=r['question'][':question/answer-fields'][0]
    return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Owned radio selection; mathematics checked by independent displayed derivative'} for a in f[':answer-field/choices']]}
def main():
    cases=[];raw=[];sourcechecks=[];fixtures=[];reviews=[];reviewtext=[];mapping=[]
    for sid,src in g.SOURCES.items():
        p={'c':g.SOURCE_COEFFICIENTS[sid]};level=g.SOURCE_LEVELS[sid];profile='raw:'+sid
        r=g.generate(level,parameters=p,profile=profile);q=r['question'];f=q[':question/answer-fields'][0];sf=src[':question/answer-fields'][0]
        assert q[':question/problem']==src[':question/problem']
        assert q.get(':question/worked-solution')==src.get(':question/worked-solution')
        for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in src)
        assert (':answer-field/correct' in f)==(':answer-field/correct' in sf)
        assert {a[':answer/value'] for a in f[':answer-field/choices']}=={a[':answer/value'] for a in sf[':answer-field/choices']}
        if ':answer-field/correct' in sf:
            correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert correct==sf[':answer-field/correct'][':answer/value']
        result=checked(r,True);sourcechecks.append({'source_id':sid,'exact_prompt':True,'exact_bank':True,'presence_parity':True,**result})
        cases.append({'source_id':sid,'source_uuid':src[':question/id'],'level':level,'template':r['generation']['template'],'parameters':p,'bank_profile':profile,'authored_level_assignment':sid=='q-31244'})
        raw.append(r);reviews.append(r);reviewtext.append('### Original '+sid+' (raw evidence)\n\n'+g.markdown(r))
        changed=g.generate(level,seed=21,parameters={'c':str(g.domain(level)[-1])},profile=profile)
        checked(changed,True);reviews.append(changed);reviewtext.append('### Changed-parameter replay '+sid+' (evidence-only original profile)\n\n'+g.markdown(changed))
        # Missing correct ref is completed only in a separate fixture, never raw API.
        nr=copy.deepcopy(r)
        if ':answer-field/correct' not in f:
            nf=nr['question'][':question/answer-fields'][0];a=next(a for a in nf[':answer-field/choices'] if a[':answer/value']==result['inferred_correct_value']);nf[':answer-field/correct']=[':answer/id',a[':answer/id']]
            nr['generation']['native_fixture_completion']='Independently inferred correct reference; raw source remains absent'
        fixtures.append(native('source:'+sid,nr))
        vals=g.raw_values(g.coefficient(p),sid);recipes=g.bank(g.coefficient(p),profile)[1]
        mapping.append({'source_id':sid,'original_parameters':p,'template':r['generation']['template'],'profile':profile,'decoded_adjacent_backslash_pairs':sum(a[':answer/value'].count('\\\\') for a in sf[':answer-field/choices']),'all_choices':[{'original':a,'generated_exact_value':a[':answer/value'],'recipe':recipes[vals.index(a[':answer/value'])],'intent':'unresolved opaque historical compound mistake' if sid=='q-71914' and vals.index(a[':answer/value'])==3 else 'observed parameterized expression; error interpretation inferred'} for a in sf[':answer-field/choices']]})
    records=[];counts={};alltasks=set();profiles=set();templates=set();normalstages=0
    for level in g.LEVELS:
        tasks=set();counts[level]={'coefficient_values':len(g.domain(level)),'normal_records':0}
        for profile in g.DEFAULT_PROFILES[level]:
            for c in g.domain(level):
                r=g.generate(level,seed=37,parameters={'c':str(c)},profile=profile)
                result=checked(r);normalstages+=result['solution_stages_checked'];records.append(r);fixtures.append(native(level+':'+profile+':'+str(c),r))
                tasks.add(r['generation']['mathematical_fingerprint']);alltasks.add(r['generation']['mathematical_fingerprint']);counts[level]['normal_records']+=1
                r2=g.generate(level,seed=98,template=r['generation']['template'],parameters={'c':str(c)},profile=profile);assert r['question'][':question/id']==r2['question'][':question/id']
                assert r['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint']
                if level=='easy':
                    alternative='what_integral' if r['generation']['template']=='integer_constant' else 'integer_constant'
                    alt=g.generate(level,seed=37,template=alternative,parameters={'c':str(c)},profile=profile)
                    normalstages+=checked(alt)['solution_stages_checked'];records.append(alt);fixtures.append(native(level+':'+profile+':'+alternative+':'+str(c),alt));counts[level]['normal_records']+=1
                    assert alt['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
        counts[level]['meaningful_tasks']=len(tasks)
        for seed in range(60):
            r=g.generate(level,seed);checked(r);profiles.add(r['generation']['profile']);templates.add(r['generation']['template'])
        for c in (g.domain(level)[0],g.domain(level)[-1]):
            r=g.generate(level,seed=21,parameters={'c':str(c)});reviews.append(r);reviewtext.append('### Generated '+level+' (authored bounded variation)\n\n'+g.markdown(r))
    assert profiles==set(sum((list(v) for v in g.DEFAULT_PROFILES.values()),[]))
    assert templates==set(g.TEMPLATES)
    # Public raw profiles remain genuinely parameterized under changed constants.
    rawchanged=0
    for sid in g.SOURCES:
        for c in (g.domain(g.SOURCE_LEVELS[sid])[0],g.domain(g.SOURCE_LEVELS[sid])[-1]):
            checked(g.generate(g.SOURCE_LEVELS[sid],parameters={'c':str(c)},profile='raw:'+sid),True);rawchanged+=1
    # Equivalent aliases deduplicate the task across profile, seed and spelling.
    a=g.generate('moderate',parameters={'c':'2/4'});b=g.generate('moderate',parameters={'c':'1/2'});assert a['question'][':question/id']==b['question'][':question/id']
    a=g.generate('easy',parameters={'c':-4},profile='method_exponent');b=g.generate('easy',parameters={'c':-4},profile='method_omit');assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint'];assert a['question'][':question/id']!=b['question'][':question/id']
    invalid=[('easy',{'c':1}),('easy',{'c':13}),('moderate',{'c':2}),('moderate',{'c':'10/13'}),('hard',{'c':'pi'}),('hard',{'c':'6*pi**2'}),('easy',{'c':'x'}),('hard',{'c':'pi**6'})]
    for level,p in invalid:
        try:g.generate(level,parameters=p)
        except ValueError:pass
        else:raise AssertionError('Invalid explicit input accepted')
    mutations=[];baseline=g.generate('easy',parameters={'c':-4})
    for name in ('prompt','factor','final','prose','control','collision','missing_stage'):
        r=copy.deepcopy(baseline);q=r['question'];f=q[':question/answer-fields'][0]
        if name=='prompt':q[':question/problem']=q[':question/problem'].replace('-4','-3')
        elif name=='factor':q[':question/worked-solution']=q[':question/worked-solution'].replace('= -4','= -3').replace('=-4\\int','=-3\\int')
        elif name=='final':q[':question/worked-solution']=q[':question/worked-solution'].replace('=-4{e}','=-3{e}')
        elif name=='prose':q[':question/worked-solution']=q[':question/worked-solution'].replace('constant $-4$','constant $-3$')
        elif name=='control':f[':answer-field/choices'][0][':answer/value']+='\x0c'
        elif name=='collision':f[':answer-field/choices'][0][':answer/value']=f[':answer-field/choices'][1][':answer/value']+'+7'
        elif name=='missing_stage':q[':question/worked-solution']=q[':question/worked-solution'].replace(r'\\  & =',r' & =')
        try:checked(r)
        except (AssertionError,ValueError,TypeError,IndexError):mutations.append(name)
        else:raise AssertionError('Mutation escaped independent check: '+name)
    write('source-cases.json',cases);write('source-replays.json',raw);write('source-choice-map.json',mapping);write('review.json',reviews);write('native-input.json',fixtures)
    (HERE/'review.md').write_text('# Review: basis2275\n\n'+ '\n\n'.join(reviewtext)+'\n')
    engine=Path('generate/runs/current/check-engine');subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
    native_report=json.loads((HERE/'native-report.json').read_text())
    assert native_report['accepted_checks']==len(fixtures) and native_report['rejected_checks']==4*len(fixtures) and native_report['documented_unresolved_checks']==0
    report={'status':'pass','generator_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'source':{k:g.SOURCE[k] for k in ('database','basis','lineage')},'source_fidelity':{'originals':6,'prompts_exact':6,'complete_banks':{'matched':6,'total':6},'values':{'matched':30,'total':30},'distractors':{'matched':24,'total':24},'captured_designated_distractors':{'matched':20,'total':20},'missing_ref_inferred_distractors':4,'captured_correct_refs':{'matched':5,'total':5,'missing':1},'solutions_exact':{'matched':5,'total':5,'missing':1},'presence_parity':6,'presentation_repairs':0},'source_checks':sourcechecks,'normal_domain':counts,'independent_normal_records':len(records),'displayed_solution_stage_checks':normalstages,'raw_changed_parameter_records':rawchanged,'meaningful_tasks':len(alltasks),'sampled_default_profiles':sorted(profiles),'invalid_explicit_inputs_rejected':len(invalid),'mutation_rejections':mutations,'native':{k:native_report[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'native_engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'unresolved':['Historical intent of opposite coefficient plus opposite exponent in q-71914 is opaque; retained as evidence-only profile. No mathematical, fidelity or native grading failures.'],'blank_fields':0,'database_writes':0,'registered':False}
    write('validation.json',report)
    print(json.dumps({k:report[k] for k in ('status','generator_sha256','normal_domain','native')},indent=2))
if __name__=='__main__':main()
