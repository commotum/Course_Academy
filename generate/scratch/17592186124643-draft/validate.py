#!/usr/bin/env python3
"""Independent validation of actual prompt, substitution and quotient text.

No source of expected mathematics is imported from the generator. The strict
TeX reader evaluates the displayed f in the displayed target/coordinate roles.
"""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,itertools,json,subprocess
from pathlib import Path
import sympy as S
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
sys.path.insert(0,str(D));import texmath as tm
sp=importlib.util.spec_from_file_location('kp124643',D.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
COUNTS={'records':0,'displayed_options':0,'bank_pairs':0,'displayed_solution_stages':0,'displayed_substitutions':0,'point_coordinate_checks':0}
def write(name,value):(D/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def equals(a,b):return S.simplify(a-b)==0

def check(record,raw=False):
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    q=record['question'];fun,t,point=tm.prompt(q[':question/problem']);x,y,h=(tm.SYMBOLS[k] for k in ['x','y','h'])
    expected=(fun.subs(t,t+h)-fun)/h
    if point:expected=expected.subs({x:point[0],y:point[1]},simultaneous=True);COUNTS['point_coordinate_checks']+=2
    f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/radio'
    values=[tm.quotient(a[':answer/value']) for a in f[':answer-field/choices']];assert len(values)==5
    indices=[]
    for i,value in enumerate(values):
        if not tm.witness_unequal(value,expected):
            assert equals(value,expected),'Unresolved bank equivalence'
            indices.append(i)
        for other in values[:i]:assert tm.witness_unequal(value,other),'Equivalent complete-bank pair'
    assert len(indices)==1,'Correct quotient not unique'
    ref=f.get(':answer-field/correct')
    if ref:assert ref[0]==':answer/id' and f[':answer-field/choices'][indices[0]][':answer/id']==ref[1]
    else:assert raw and record['generation']['template']=='root_product'
    sol=q.get(':question/worked-solution')
    if sol is not None:
        blocks=__import__('re').findall(r'\$\$(.*?)\$\$',sol,__import__('re').S);assert len(blocks)==3,'Changed operative stage sequence'
        first=blocks[0].split('=',1)[1].strip().rstrip('.')
        assert equals(tm.quotient(first,fun),expected),'Formal quotient wrong'
        for segment in blocks[1].split(r'\qquad'):
            lhs,rhs=segment.strip().rstrip('.,').split('=',1)
            assert equals(tm.parse(lhs,fun),tm.parse(rhs)),'Displayed coordinate/held-variable substitution wrong'
            COUNTS['displayed_substitutions']+=1
        last=blocks[2].split('=',1)[1].strip().rstrip('.')
        assert equals(tm.quotient(last,fun),expected),'Final displayed quotient wrong'
        for b in [blocks[0],blocks[2]]:
            lhs=b.split('=',1)[0]
            if point:
                assert 'f_'+str(t)+'('+str(point[0])+','+str(point[1])+')' in lhs,'Stale point/target in solution'
            else:assert __import__('re').search(r'(?:∂|\\partial)\s*'+str(t),lhs),'Stale target in solution'
        if not raw:
            u='y' if str(t)=='x' else 'x'
            assert '$'+u+('='+str(point[1] if str(t)=='x' else point[0]) if point else '')+'$ is held constant.' in sol
            assert r'$h\ne 0$' in sol
        COUNTS['displayed_solution_stages']+=3
    else:assert raw and record['generation']['template']=='root_product'
    if not raw:g.mf.validate_generated_record(record)
    for text in [q[':question/problem'],sol or '',*[a[':answer/value'] for a in f[':answer-field/choices']]]:g.guard(text)
    COUNTS['records']+=1;COUNTS['displayed_options']+=5;COUNTS['bank_pairs']+=10
    return {'inferred_correct_value':f[':answer-field/choices'][indices[0]][':answer/value'],'target':str(t),'point':list(map(str,point)) if point else None}

def source_checks():
    source=json.loads((D/'source.json').read_text());qs=source['record'][':knowledge-point/questions'];cases=json.loads((D/'source-cases.json').read_text());assert len(qs)==len(cases)==12
    reports=[];records=[]
    for original,case in zip(qs,cases):
        r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['profile']);q=r['question'];check(r,True)
        assert q[':question/problem']==g.mf.normalize_prose(original[':question/problem'])
        for key in [':question/difficulty',':question/worked-solution',':question/answer-fields']:assert (key in q)==(key in original),'Source attribute presence changed'
        if ':question/worked-solution' in original:assert q[':question/worked-solution']==g.mf.normalize_prose(original[':question/worked-solution'])
        a=original[':question/answer-fields'][0];b=q[':question/answer-fields'][0]
        assert sorted(g.mf.normalize_tex(v[':answer/value']) for v in a[':answer-field/choices'])==sorted(v[':answer/value'] for v in b[':answer-field/choices'])
        assert (':answer-field/correct' in a)==(':answer-field/correct' in b)
        reports.append({'source_id':case['source_id'],'matched_options':5,'matched_distractors':4 if case['source_key_present'] else None,'complete_bank':True,'key_present':case['source_key_present'],'designation_match':case['source_key_present'],'solution_present':':question/worked-solution' in original,'exact_normalized_prompt':True,'exact_normalized_solution':':question/worked-solution' in original,'key_presence_parity':True})
        records.append(r)
    write('source-replays.json',records);write('source-fidelity.json',reports)
    return records,reports

def build_checks(records):
    out=[]
    for i,r in enumerate(records):
        f=r['question'][':question/answer-fields'][0]
        if ':answer-field/correct' not in f:continue
        correct=f[':answer-field/correct'][1]
        out.append({'label':str(i)+'-'+r['generation']['template'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'Complete real radio control bank'} for a in f[':answer-field/choices']]})
    return out

def grader_provenance():
    build=json.loads((D/'reference/grader-build.json').read_text());paths={build['source']:build['source_sha256'],build['library']:build['library_sha256'],build['binary']:build['binary_sha256']}|build['engine_sources']|build['dependencies']
    rows=[{'path':p,'sha256':hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),'expected':s} for p,s in paths.items()]
    assert len(rows)==42 and all(r['sha256']==r['expected'] for r in rows),'Native grader build drift'
    write('native-provenance.json',{'verified_hashes':len(rows),'files':rows});return ROOT/build['binary']

def baseline():
    snap=json.loads((D/'immutable-baseline.json').read_text());root=ROOT/'generate/scratch';kp='17592186124643'
    found=set()
    for p in [root/(kp+'.py'),root/kp]:
        if p.is_dir():found.update(x.relative_to(ROOT).as_posix() for x in p.rglob('*') if x.is_file())
        elif p.is_file():found.add(p.relative_to(ROOT).as_posix())
    found.update(p.relative_to(ROOT).as_posix() for p in (root/'__pycache__').glob(kp+'.*.pyc'))
    assert found=={r['path'] for r in snap['files']}
    for row in snap['files']:assert hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()==row['sha256']
    write('immutable-baseline-verification.json',{'passed':True,'complete_pathset_verified':True,'numeric_files':len(found),'absence_proof':not found,'dispatch_registration_context':'registration-context.json'})

def main():
    baseline();source,source_report=source_checks();records=[]
    canonical=json.loads((D/'source.json').read_text())['record'][':knowledge-point/canonical-example']
    fun,t,point=tm.prompt(canonical[':question/problem']);h=tm.SYMBOLS['h'];expected=(fun.subs(t,t+h)-fun)/h
    blocks=__import__('re').findall(r'\$\$(.*?)\$\$',canonical[':question/worked-solution'],__import__('re').S)
    assert len(blocks)==3 and equals(tm.quotient(blocks[0].split('=',1)[1].strip().rstrip('.'),fun),expected) and equals(tm.quotient(blocks[2].split('=',1)[1].strip().rstrip('.'),fun),expected)
    lhs,rhs=blocks[1].strip().rstrip('.').split('=',1);assert equals(tm.parse(lhs,fun),tm.parse(rhs))
    write('canonical-validation.json',{'canonical_id':canonical[':question/math-academy-id'],'displayed_stages_verified':3,'practice_count':0,'passed':True})
    records=[];coverage={l:set() for l in g.LEVELS}
    # Every observed family at every boundary and both target-role orientations.
    boundary_counts={}
    for name,spec in g.TEMPLATES.items():
        domain=g.DOMAINS[name];points=list(itertools.product(*[list(v) for v in domain.values()])) if domain else [()]
        boundary_counts[name]=0
        for point,swap in itertools.product(points,[False,True]):
            p=dict(zip(domain,point))|{'swap':swap};r=g.generate(spec['level'],template=name,parameters=p);check(r);records.append(r);boundary_counts[name]+=1
        # Changed parameters with observed raw bank (all masks are active recipes).
        p={k:max(v) for k,v in domain.items()}|{'swap':True};check(g.generate(spec['level'],template=name,parameters=p,profile='observed'),True)
    # Exhaust all authored hard parameters: max absolute evaluated monomial <= 24.
    for template in ['point_monomial','point_sine']:
        for X,Y,swap in itertools.product([-3,-2,-1,1,2,3],[-3,-2,-1,1,2,3],[False,True]):
            if template=='point_sine' and X==Y:continue
            for a in ([-5,-4,-3,-2,-1,1,2,3,4,5] if template=='point_monomial' else [None]):
                if template=='point_monomial' and abs(a*((Y if swap else X)**2)*(X if swap else Y))>24:continue
                p={'X':X,'Y':Y,'swap':swap}|({'a':a} if a else {});r=g.generate('hard',template=template,parameters=p);check(r);records.append(r)
    for level in g.LEVELS:
        for seed in range(80):
            r=g.generate(level,seed);check(r);records.append(r);coverage[level].add(r['generation']['template'])
    assert coverage['easy']=={k for k,v in g.TEMPLATES.items() if v['level']=='easy'}
    assert coverage['moderate']=={k for k,v in g.TEMPLATES.items() if v['level']=='moderate'}
    assert coverage['hard']=={'point_monomial','point_sine'}
    # Same content/IDs under changed seed; all answer identities field-owned.
    for r in records:
        z=g.generate(r['question'][':question/difficulty'].split('/')[-1],seed=9281,template=r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['profile'])
        assert z['question'][':question/id']==r['question'][':question/id']
        a=r['question'][':question/answer-fields'][0];b=z['question'][':question/answer-fields'][0]
        assert a[':answer-field/id']==b[':answer-field/id'] and {v[':answer/id'] for v in a[':answer-field/choices']}=={v[':answer/id'] for v in b[':answer-field/choices']}
    # Deliberate corruptions must be detected from displayed math, not metadata.
    mutations=[]
    r=g.generate('easy',template='monomial',parameters={'a':3,'n':2,'swap':False})
    for name,old,new in [('shift-held',r'f(x+h,y)=',r'f(x,y+h)='),('wrong-final-denominator',r'{h}).',r'{h+1}).'),('wrong-final-increment',r'3(x+h)',r'3(x-h)')]:
        z=copy.deepcopy(r);z['question'][':question/worked-solution']=z['question'][':question/worked-solution'].replace(old,new)
        try:check(z)
        except (AssertionError,ValueError):mutations.append(name)
        else:raise AssertionError('Mutation survived '+name)
    try:g.guard('bad\x0cfrac')
    except ValueError:mutations.append('C0-formfeed')
    else:raise AssertionError('C0 survived')
    for level,template,p in [('easy','monomial',{'a':10,'n':2}),('moderate','rational',{'p':2,'q':6,'a':1}),('hard','point_monomial',{'a':-3,'X':3,'Y':1})]:
        try:g.generate(level,template=template,parameters=p)
        except ValueError:mutations.append('workload-'+level)
        else:raise AssertionError('Workload boundary escaped')
    grader=grader_provenance();native=build_checks(source+records);write('native-input.json',native)
    subprocess.run([str(grader),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
    review=[]
    for name,spec in g.TEMPLATES.items():
        for j in range(2):
            p={k:(min(v) if j==0 else max(v)) for k,v in g.DOMAINS[name].items()}|{'swap':bool(j)}
            review.append(g.generate(spec['level'],template=name,parameters=p,seed=j))
    for name in ['point_monomial','point_sine']:
        for j in range(2):review.append(g.generate('hard',template=name,parameters={'X':j+1,'Y':2-j,'swap':bool(j)}|({'a':j+1} if name=='point_monomial' else {}),seed=j))
    review.extend([g.generate('hard',template='point_monomial',parameters={'a':-3,'X':-2,'Y':-2,'swap':False}),g.generate('hard',template='point_sine',parameters={'X':-3,'Y':2,'swap':True})])
    write('review.json',review);write('samples.json',records)
    markdown=['# Source originals and generated variants','All originals are evidence only; generated variants are labeled by difficulty and bank profile.']
    for r in source:markdown+=['## Original MA '+r['generation']['source_id'],g.markdown(r)]
    for r in review:markdown+=['## Generated variant',g.markdown(r)]
    (D/'review.md').write_text('\n\n'.join(markdown)+'\n')
    nr=json.loads((D/'native-report.json').read_text())
    report={'passed':True,'source_basis':2275,'original_ma_questions':12,'independent_inventory':0,'canonical_examples_not_practice':1,'source_option_matches':60,'source_complete_bank_matches':12,'source_designation_matches':11,'source_designation_omissions':1,'source_solution_matches':11,'source_solution_omissions':1,'normal_difficulty_counts':{l:sum(r['question'][':question/difficulty'].endswith('/'+l) for r in records) for l in g.LEVELS},'default_family_coverage':{k:sorted(v) for k,v in coverage.items()},'boundary_counts':boundary_counts,'finite_domain_exhaustive':True,'meaningful_task_domains':json.loads((D/'domains.json').read_text())['meaningful_tasks_by_level'],'math':COUNTS,'native':{k:nr[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']},'mutation_regressions':mutations,'immutable_baseline_verified':True,'runtime':{'python':sys.version.split()[0],'sympy':S.__version__},'limitations':['Hard difficulty is an authored point-specialization design claim; no observed hard practice.','Raw root-product source has no key, solution or difficulty; its 5 options match, its key is inferred only in normal output.','Quotient banks are compared as complete increment expressions; divergent limit expressions are not merged merely because they share nonexistence.','Radio ID grading establishes control selection only; displayed mathematics is independently parsed.','One exponential source distractor contains yy; its parameterized raw evidence remains exact and ineligible, normal method bank uses a declared held-coordinate shift replacement.'],'root_approval':'pending'}
    write('validation.json',report);baseline();print(json.dumps(report,indent=2))
if __name__=='__main__':main()
