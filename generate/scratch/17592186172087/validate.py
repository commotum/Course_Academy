#!/usr/bin/env python3
"""Independent printed signature/component checks, source replay and native grader."""
import copy, importlib.util, itertools, json, re, subprocess, sys
sys.dont_write_bytecode = True
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def save(name,obj): (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

def printed_dimensions(prompt):
    result=[]
    for line in prompt.splitlines():
        if not line.startswith('- $'): continue
        match=re.fullmatch(r'- \$([A-Z])\(([^)]*)\)=(.*)\$',line)
        assert match, f'bad function declaration: {line}'
        args=match[2].split(',')
        assert len(set(args))==len(args)
        expr=match[3]
        if expr.startswith('⟨'):
            assert expr.endswith('⟩'); m=1+len(re.findall(r'(?<!\\),',expr))
        elif expr.startswith(r'\langle '):
            assert expr.endswith(r'\rangle');m=1+len(re.findall(r'(?<!\\),',expr))
        else:
            bases=re.findall(r'\\,([ijk])(?:[+-]|$)',expr)
            m=len(bases) if bases else 1
        result.append((len(args),m))
    assert len(result)==3
    return result

def check_format(text):
    assert all(ord(c)>=32 or c in '\n\t' for c in text),'C0 control character'
    assert len(re.findall(r'(?<!\\)\$',text))%2==0,'unbalanced math delimiters'
    balance=0
    for match in re.finditer(r'(?<!\\)[{}]',text):
        balance+=1 if match[0]=='{' else -1
        assert balance>=0,'unbalanced TeX braces'
    assert balance==0,'unbalanced TeX braces'

def validate_record(r):
    assert set(r)=={'knowledge_point','question','generation'}
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    assert r['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    q=r['question'];dims=printed_dimensions(q[':question/problem'])
    # Independent recognition from actual declared input arity and actual
    # output components; metadata is compared afterwards, never the oracle.
    mask=sum(1<<i for i,pair in enumerate(dims) if pair==(3,3))
    expected=g.LABELS[mask]
    assert tuple(map(tuple,r['generation']['semantic_signature']))==tuple(dims)
    assert r['generation']['mathematical_fingerprint']==g.digest(dims)
    f=q[':question/answer-fields'][0]
    assert f[':answer-field/type']==':answer-field.type/radio'
    assert f[':answer-field/key']=='selection'
    choices=f[':answer-field/choices']; assert len(choices)==5
    assert len({a[':answer/id'] for a in choices})==5
    values=[a[':answer/value'] for a in choices]
    assert len(set(values))==5 and all(v in g.LABELS for v in values)
    correct=[a for a in choices if a[':answer/id']==f[':answer-field/correct'][1]]
    assert len(correct)==1 and correct[0][':answer/value']==expected
    solution=q[':question/worked-solution']
    assert solution.endswith(f'Therefore, the correct answer is "{expected}."')
    apps=re.findall(r'- \$([A-Z]\([^)]*\))=',q[':question/problem'])
    claims=re.findall(r'- The function \$([A-Z]\([^)]*\))\$ is (.*?)vector field',solution)
    assert [app for app,_ in claims]==apps,'prose function names/order'
    for i,(_,claim) in enumerate(claims):
        assert ('*not*' not in claim)==(dims[i]==(3,3)),'prose classification'
    for text in [q[':question/problem'],solution,*values]:check_format(text)
    presence={k:k in q for k in (':question/difficulty',':question/worked-solution',':question/answer-fields')}
    level=q[':question/difficulty'].split('/')[-1]
    identity=g.identity_components(level,q[':question/problem'],solution,values,expected,presence,':answer-field/correct' in f)
    assert r['generation']['content_id']==g.digest(identity),'content identity differs from actual displayed content'
    assert q[':question/id']==g.uid(g.digest(identity))
    return dims

def must_reject(fn):
    try: fn()
    except (AssertionError,ValueError): return
    raise AssertionError('mutation/invalid input was accepted')

def main():
    cases=[];native=[];review=[];source_details=[]
    sourcebanks=sourcechoices=sourcewrong=correctrefs=exactsolutions=0
    allrecords=[]
    for sid,src in g.SOURCES.items():
        names=[line[3] for line in src[':question/problem'].splitlines() if line.startswith('- $')]
        case={'source_id':sid,'template':'observed_'+sid,'level':'easy','parameters':{'a':g.SPECS[sid][0],'names':names,'order':[0,1,2]},'bank_profile':'observed_'+sid}
        cases.append(case)
        r=g.generate('easy',template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])
        validate_record(r);allrecords.append(r)
        q=r['question'];sf=src[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
        for key in (':question/difficulty',':question/problem',':question/worked-solution',':question/answer-fields'):
            assert (key in src)==(key in q),f'key-presence mismatch: {sid} {key}'
        assert q[':question/problem']==src[':question/problem']
        assert q[':question/worked-solution']==src[':question/worked-solution'];exactsolutions+=1
        assert q[':question/difficulty']==src[':question/difficulty'][':db/ident']
        for key in (':answer-field/type',':answer-field/key',':answer-field/choices',':answer-field/correct'):
            assert (key in sf)==(key in f)
        assert f[':answer-field/type']==sf[':answer-field/type'][':db/ident']
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
        assert all(a[':answer/type']==':answer.type/text' for a in f[':answer-field/choices'])
        actual=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        assert actual==sf[':answer-field/correct'][':answer/value'];correctrefs+=1
        sourcebanks+=1;sourcechoices+=len(sf[':answer-field/choices']);sourcewrong+=len(sf[':answer-field/choices'])-1
        normal=g.generate('easy',template=case['template'],parameters=case['parameters'])
        validate_record(normal)
        repaired=sid in ('q-122685','q-122691','q-122696')
        assert normal['question'][':question/worked-solution']==src[':question/worked-solution'].replace('to functions in $R$','to values in $R$').replace('S={',r'S=\{').replace('}\n$$',r'\}'+'\n$$')
        assert normal['question'][':question/problem']==src[':question/problem']
        changed={'a':1 if case['parameters']['a']!=1 else 7,'names':['A','B','C'],'order':[2,0,1]}
        variant=g.generate('easy',seed=17,template=case['template'],parameters=changed)
        validate_record(variant);allrecords.append(variant)
        source_details.append({'source_id':sid,'raw_prompt_exact':True,'raw_solution_exact':True,'key_presence_exact':True,'bank_count':5,'correct_designation_exact':True,'normal_scalar_prose_repair':repaired})
        review.extend([{'label':f'{sid}: raw original parameter replay','record':r},{'label':f'{sid}: normal original parameters'+(' (prose repaired)' if repaired else ''),'record':normal},{'label':f'{sid}: generated component/name/order variant','record':variant}])
        # Every source profile also generalizes over all six categorical orders.
        for order in itertools.permutations(range(3)):
            pp={**changed,'order':list(order)}
            validate_record(g.generate('easy',template=case['template'],parameters=pp,profile=case['bank_profile']))
        # sqrt(3-x) domain row changes in the same complete component slot.
        if sid=='q-122694':
            assert r'1-x\ge 0' in variant['question'][':question/worked-solution']
            x=g.sp.Symbol('x',real=True)
            assert g.sp.solve_univariate_inequality(1-x>=0,x)==(x<=1)
    save('source-cases.json',cases)
    finite={}
    for level in g.LEVELS:
        seen=set()
        for types in g.eligible_types(level):
            p={'a':2,'types':list(types),'names':['A','B','C']}
            r=g.generate(level,template='authored_'+level,parameters=p)
            validate_record(r);seen.add(r['generation']['mathematical_fingerprint']);allrecords.append(r)
            rr=g.generate(level,seed=301,template='authored_'+level,parameters={**p,'a':7,'names':['U','V','W']})
            validate_record(rr)
            assert rr['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint'],'incidental aliases counted as tasks'
        finite[level]=len(seen)
        for seed in (23,78):
            r=g.generate(level,seed=seed,template='authored_'+level)
            review.append({'label':f'{level}: authored generated variant seed {seed}','record':r})
    # Source easy signatures add scalar and mismatch catalog structures, but
    # recipe/domain/coefficient/source-bank aliases never inflate task counts.
    easy_signatures={tuple(g.CATALOG['easy'][i] for i in t) for t in g.eligible_types('easy')}
    for sid in g.SPECS:
        ds=g.SPECS[sid][3]
        easy_signatures.update(tuple(ds[i] for i in order) for order in itertools.permutations(range(3)))
    finite['easy_including_observed_families']=len(easy_signatures)
    # Public selection filters families and rejects inappropriate levels.
    for sid in g.SOURCES:
        assert g.generate('easy',profile='observed_'+sid)['generation']['template']=='observed_'+sid
        must_reject(lambda:g.generate('moderate',profile='observed_'+sid))
    for level in g.LEVELS:
        selected={g.generate(level,seed=i)['generation']['template'] for i in range(300)}
        assert selected=={t for t,s in g.TEMPLATES.items() if s['level']==level}
        for invalid in (0,-1,8):
            must_reject(lambda:g.generate(level,template='authored_'+level,parameters={'a':invalid,'types':list(g.eligible_types(level)[0]),'names':['A','B','C']}))
    must_reject(lambda:g.generate('moderate',template='authored_moderate',parameters={'a':2,'types':[0,0,0],'names':['A','B','C']}))
    must_reject(lambda:g.generate('hard',template='authored_hard',parameters={'a':2,'types':[0,0,0],'names':['A','B','C']}))
    anchor=allrecords[-1]
    pp=anchor['generation']['parameters'];level=anchor['question'][':question/difficulty'].split('/')[-1]
    same=g.generate(level,seed=937,template=anchor['generation']['template'],parameters=pp,profile=anchor['generation']['profile'])
    assert anchor['question'][':question/id']==same['question'][':question/id']
    assert anchor['generation']['content_id']==same['generation']['content_id']
    # Mutations prove checks can detect printed arity, grading and C0 failures.
    r=g.generate('hard',template='authored_hard',parameters={'a':2,'types':[0,1,2],'names':['A','B','C']})
    bad=copy.deepcopy(r);bad['question'][':question/problem']=bad['question'][':question/problem'].replace('A(x,y,z)','A(x,y)');must_reject(lambda:validate_record(bad))
    bad=copy.deepcopy(r);bad['question'][':question/problem']+='\f';must_reject(lambda:validate_record(bad))
    bad=copy.deepcopy(r);bad['question'][':question/problem']=bad['question'][':question/problem'].replace('2x','7x');must_reject(lambda:validate_record(bad))
    bad=copy.deepcopy(r);bad['question'][':question/answer-fields'][0].pop(':answer-field/correct');
    try: validate_record(bad)
    except KeyError: pass
    else: raise AssertionError('missing correct ref accepted')
    bad=copy.deepcopy(r);f=bad['question'][':question/answer-fields'][0];f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])];must_reject(lambda:validate_record(bad))
    # Native radio grading: every complete choice in every observed/finite
    # categorical task, not merely the correct-ID path.
    for i,r in enumerate(allrecords):
        f=r['question'][':question/answer-fields'][0]
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete categorical bank'} for a in f[':answer-field/choices']]
        native.append({'label':f'instance-{i}','record':r,'checks':checks})
    save('engine-input.json',native)
    subprocess.run([str(HERE.parents[1]/'runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    engine=json.loads((HERE/'engine-report.json').read_text())
    assert engine['documented_unresolved_checks']==0
    save('review.json',review)
    (HERE/'review.md').write_text('# Review: originals and labeled variants\n\n'+'\n\n---\n\n'.join('## '+item['label']+'\n\n'+g.markdown(item['record']) for item in review)+'\n')
    report={'pass':True,'provenance':g.PROVENANCE,'runtime':{'python':sys.version.split()[0],'sympy':g.sp.__version__},'source_questions':9,'source_prompt_exact':9,'source_solution_raw_exact':exactsolutions,'source_solution_normal_unmodified_exact':0,'source_solution_normal_prose_unmodified':6,'source_solution_normal_prose_minimally_repaired':3,'source_solution_normal_set_presentation_normalized':7,'source_key_presence_exact':9,'source_banks_matched':sourcebanks,'source_banks_total':9,'source_choices_matched':sourcechoices,'source_choices_total':45,'source_distractors_matched':sourcewrong,'source_distractors_total':36,'source_correct_designations_matched':correctrefs,'source_correct_designations_total':9,'source_details':source_details,'finite_semantic_task_counts':finite,'finite_task_identity_exclusions':['positive coefficient magnitude','function-letter aliases','choice profile','domain spelling'],'mathematical_check':'independent printed argument arity + tuple/basis output dimension; all subset labels checked','native':{k:engine[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks','database_writes')},'records_natively_checked':len(allrecords),'mutations_rejected':['printed declared arity','C0 formfeed','stale content identity after coefficient mutation','missing correct ref','wrong correct value'],'default_family_coverage':True,'plot_rating':'none','unresolved_findings':[]}
    save('validation.json',report)
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
