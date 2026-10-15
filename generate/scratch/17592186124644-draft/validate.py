#!/usr/bin/env python3
"""Independent printed-prompt/stage/bank checks plus unchanged native grading.

Run from repository root: .venv/bin/python -B generate/scratch/17592186124644-draft/validate.py
"""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,itertools,json,random,re,subprocess
from pathlib import Path
import sympy as S
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
sys.path.insert(0,str(D));import texmath as tm
audit_spec=importlib.util.spec_from_file_location('partial_workload_audit',D/'audit-workload.py');audit_module=importlib.util.module_from_spec(audit_spec);audit_spec.loader.exec_module(audit_module)
spec=importlib.util.spec_from_file_location('partial_draft',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
COUNTS={'records':0,'displayed_solution_rows':0,'displayed_bank_options':0,'bank_pair_comparisons':0,'held_coefficient_derivative_checks':0,'substitution_coordinate_operands':0}
def write(name,value):
    (D/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def check(q,allow_missing=False):
    fun,t,pt=tm.prompt(q[':question/problem']);derivative=S.diff(fun,t);expected=derivative.subs(pt)
    assert expected.is_finite is not False
    for text in [q.get(':question/worked-solution','')]+[z[':answer/value'] for f in q[':question/answer-fields'] for z in f[':answer-field/choices']]:
        assert not re.search(r'(?<![A-Za-z])\d+ e(?=[+\-\s]|$)',text),'Ambiguous numeric Euler-e product'
        for arg in re.findall(r'\\ln\{\(\s*(\d+)\s*\)\}',text):assert int(arg)<=5,'Log coefficient compressed into an unfamiliar large logarithm'
    fields=q[':question/answer-fields'];assert len(fields)==1
    f=fields[0];assert f[':answer-field/type'] in (':answer-field.type/radio',{':db/ident':':answer-field.type/radio'})
    values=[tm.parse(a[':answer/value']) for a in f[':answer-field/choices']];assert len(values)==5
    for i,value in enumerate(values):
        for other in values[:i]:assert not tm.equivalent(value,other),'Equivalent pair in complete bank'
    correct=[i for i,value in enumerate(values) if tm.equivalent(value,expected)];assert len(correct)==1
    ref=f.get(':answer-field/correct')
    if ref:
        selected=ref[1] if isinstance(ref,list) else ref[':answer/id']
        assert selected==f[':answer-field/choices'][correct[0]][':answer/id'],'Incorrect key'
    else:assert allow_missing,'Unexpected absent correct ref'
    rows=[]
    if ':question/worked-solution' in q:
        sol=q[':question/worked-solution'];rows=tm.rows(sol);assert len(rows)==2
        assert len(rows[0]) in (5,6);assert len(rows[1]) in (2,3)
        assert re.search(r'with respect to \$'+str(t)+r',\$',sol),'Stale prose derivative target'
        for text,value in rows[0]:assert tm.equivalent(value,derivative),('Incorrect displayed derivative row',text)
        for text,value in rows[1]:assert tm.equivalent(value,expected),('Incorrect displayed point row',text)
        assert not rows[1][0][1].free_symbols,'Coordinate not fully substituted'
        # Actual first row must still differentiate the displayed whole sum.
        first=rows[0][0][1];assert isinstance(first,S.Derivative)
        assert tm.equivalent(first.expr,fun) and first.variables==(t,)
        # Ordered source stage topology: full derivative; optional reciprocal
        # rewrite; split two derivatives; factor constants; evaluate; collect.
        offset=len(rows[0])-5
        if offset:assert re.search(r'\^\{-1\}',rows[0][1][0]),'Missing reciprocal negative-power operation'
        if r'\sec' in q[':question/problem']:
            assert rows[1][1][0].count(r'\cdot')==2,'Secant and tangent evaluated operands must remain separate'
        if r'\cot' in q[':question/problem']:
            assert r'\csc' in rows[0][-1][0] and r'\cot' not in rows[0][-1][0],'Preserve source csc-squared derivative notation'
            assert rows[1][1][0].count(r'\cdot')==1,'Keep the evaluated csc-squared factor'
        for row in rows[0][1:1+offset]:assert len(row[1].atoms(S.Derivative))==1
        split=rows[0][1+offset][1];factored=rows[0][2+offset][1]
        assert len(split.atoms(S.Derivative))==2 and len(factored.atoms(S.Derivative))==2
        for node in factored.atoms(S.Derivative):
            assert node.variables==(t,) and node.expr.free_symbols<={t},'Held variable differentiated'
            COUNTS['held_coefficient_derivative_checks']+=1
        # Each factor outside a derivative must be independent of the target;
        # replacing derivative nodes with formal independent placeholders makes
        # every coefficient readable without using generator internals.
        nodes=list(factored.atoms(S.Derivative));symbols=S.symbols('P0:'+str(len(nodes)))
        held=factored.xreplace(dict(zip(nodes,symbols)))
        for symbol in symbols:assert S.diff(S.expand(held).coeff(symbol),t)==0,'Target treated as held data'
        assert not rows[0][-2][1].atoms(S.Derivative)
        assert not rows[0][-1][1].atoms(S.Derivative)
        # Read physical point in the solution's point prose independently.
        pointtext=re.search(r'Finally,.*?\$\((.*?)\)(?::|\\mathbin)',sol,re.S)
        if pointtext:
            X,Y=tm.point_parts(pointtext[1]);assert tm.equivalent(X,pt[tm.SYMBOLS['x']]) and tm.equivalent(Y,pt[tm.SYMBOLS['y']])
        COUNTS['displayed_solution_rows']+=sum(map(len,rows));COUNTS['substitution_coordinate_operands']+=2
    else:assert allow_missing
    COUNTS['records']+=1;COUNTS['displayed_bank_options']+=5;COUNTS['bank_pair_comparisons']+=10
    return {'inferred_correct_index':correct[0],'source_key_present':bool(ref),'derivative_rows':len(rows[0]) if rows else 0,'evaluation_rows':len(rows[1]) if rows else 0},rows

def source_fidelity(original,record):
    q=record['question'];a,ar=check(original,True);b,br=check(q,True)
    of,ot,op=tm.prompt(original[':question/problem']);gf,gt,gp=tm.prompt(q[':question/problem'])
    assert tm.equivalent(of,gf) and ot==gt and op==gp
    # Compare complete prose, including punctuation outside mathematical islands.
    prose=lambda s: ' '.join(re.sub(r'\$\$.*?\$\$|(?<!\$)\$(?!\$).*?\$', '<math>',s,flags=re.S).split())
    assert prose(original[':question/problem'])==prose(q[':question/problem'])
    for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):
        assert (key in original)==(key in q),'Source key-presence mismatch '+key
    original_values=[tm.parse(a[':answer/value']) for a in original[':question/answer-fields'][0][':answer-field/choices']]
    values=[tm.parse(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices']]
    mapping=[[i for i,v in enumerate(values) if tm.equivalent(a,v)] for a in original_values]
    assert all(len(m)==1 for m in mapping) and len({m[0] for m in mapping})==5
    if ar:
        assert prose(original[':question/worked-solution'])==prose(q[':question/worked-solution'])
        assert [len(s) for s in ar]==[len(s) for s in br]
        for ss,gg in zip(ar,br):
            for (st,se),(gt,ge) in zip(ss,gg):
                assert tm.equivalent(se,ge),(st,gt)
                assert len(se.atoms(S.Derivative))==len(ge.atoms(S.Derivative))
        if len(ar[1])==3:assert ar[1][1][0].count(r'\cdot')==br[1][1][0].count(r'\cdot'),'Source evaluated-product operands changed'
    return dict(source_id=original[':question/math-academy-id'],matched_options=5,matched_distractors=4,matched_complete_bank=True,source_key_present=a['source_key_present'],matched_designation=a['source_key_present'],missing_solution=not bool(ar),source_derivative_rows=a['derivative_rows'],source_evaluation_rows=a['evaluation_rows'],notation='Presentation normalized; stage-wise mathematical equivalence and derivative topology, complete source prose preserved',mapping=mapping)

def baseline():
    before=json.loads((D/'numeric-baseline.json').read_text());paths=[]
    for name in ('generate/scratch/17592186124644.py','generate/scratch/17592186124644'):
        p=ROOT/name
        if p.is_file():paths.append(p)
        elif p.is_dir():paths.extend(z for z in p.rglob('*') if z.is_file())
    paths.extend((ROOT/'generate/scratch/__pycache__').glob('17592186124644.*.pyc'))
    actual={str(z.relative_to(ROOT)):hashlib.sha256(z.read_bytes()).hexdigest() for z in paths}
    for name,state in before.get('numeric_roots',{}).items():assert (ROOT/name).exists()==state['exists'],'Numeric root existence changed'
    actual_dirs=sorted(str(p.relative_to(ROOT)) for p in (ROOT/'generate/scratch/17592186124644').rglob('*') if p.is_dir()) if (ROOT/'generate/scratch/17592186124644').is_dir() else []
    assert actual_dirs==before.get('numeric_directory_paths',[]),'Numeric directory pathset changed'
    assert sorted(str(p.relative_to(ROOT)) for p in (ROOT/'generate/scratch/__pycache__').glob('17592186124644.*.pyc'))==before.get('sibling_pyc_paths',[]),'Sibling pyc pathset changed'
    assert actual==before['numeric_paths'],'Numeric script/tree/cache or sibling pyc changed'
    return dict(unchanged=True,files=len(actual),absence=not actual,paths=actual)
def hashes():
    build=json.loads((ROOT/'generate/scratch/17592186059716-draft/reference/grader-build.json').read_text());checks=[]
    for key in ('source','library','binary'):
        p=ROOT/build[key];actual=hashlib.sha256(p.read_bytes()).hexdigest();assert actual==build[key+'_sha256'];checks.append(str(p.relative_to(ROOT)))
    for section in ('engine_sources','dependencies'):
        for name,expected in build[section].items():
            p=ROOT/name;assert hashlib.sha256(p.read_bytes()).hexdigest()==expected;checks.append(name)
    assert len(checks)==42,len(checks)
    write('reference/grader-build.json',build);return build,checks

def native(records,filename):
    fixtures=[]
    for label,record in records:
        r=copy.deepcopy(record);q=r['question'];f=q[':question/answer-fields'][0]
        if ':answer-field/correct' not in f:
            result,_=check(q,True);f[':answer-field/correct']=[':answer/id',f[':answer-field/choices'][result['inferred_correct_index']][':answer/id']]
            label+='-local-synthetic-inferred-key'
        correct=f[':answer-field/correct'][1]
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'Native radio ID selection; complete actual displayed bank; no free-text equivalence contract'} for a in f[':answer-field/choices']]
        fixtures.append({'label':label,'record':r,'checks':checks})
    write(filename+'-input.json',fixtures)
    subprocess.run([str(ROOT/'generate/scratch/17592186059716-draft/check-engine'),str(D/(filename+'-input.json')),str(D/(filename+'-report.json'))],check=True)
    return json.loads((D/(filename+'-report.json')).read_text())

def must_fail(action,reason):
    try:action()
    except (AssertionError,ValueError):return reason
    raise AssertionError('Negative control passed: '+reason)
def main():
    initial=baseline();build,verified=hashes();sources=[];cases=[];replays=[];reviews=[];generated=[];source_maps=[]
    for sid,original in g.ORIGINALS.items():
        key=g.SOURCE_FAMILY[sid];f=g.FAMILIES[key]
        record=g.generate(f['level'],template=key,parameters=f['anchor'],profile='observed-'+sid)
        result=source_fidelity(original,record);audit_module.audit(original,key);audit_module.audit(record['question'],key);sources.append(result);replays.append((sid,record))
        shuffled=g.generate(f['level'],seed=99991,template=key,parameters=f['anchor'],profile='observed-'+sid)
        assert shuffled['question'][':question/id']==record['question'][':question/id']
        assert {z[':answer/id'] for z in shuffled['question'][':question/answer-fields'][0][':answer-field/choices']}=={z[':answer/id'] for z in record['question'][':question/answer-fields'][0][':answer-field/choices']}
        cases.append({'source_id':sid,'template':key,'parameters':f['anchor'],'bank_profile':'observed-'+sid,'difficulty':f['level'],'difficulty_assignment':'observed' if ':question/difficulty' in original else 'authored for an unrated original; raw replay omits rating'})
        source_maps.append({'source_id':sid,'raw':original,'replay':record,'fidelity':result})
    # Canonical is kept separate from the 12 MA practice originals; no answer
    # fields are invented for its source-fidelity denominator.
    canonical=g.KP[':knowledge-point/canonical-example'];fun,t,pt=tm.prompt(canonical[':question/problem']);cs=tm.rows(canonical[':question/worked-solution']);canonical_rows=0
    for section_index,section in enumerate(cs):
        for text,val in section:
            assert tm.equivalent(val,S.diff(fun,t) if section_index==0 else S.diff(fun,t).subs(pt));canonical_rows+=1
    coverage={};identity_checks=0;target_checks=0;boundary_checks=0;negatives=[]
    for key,f in g.FAMILIES.items():
        fingerprints=set();targets=set();coords=set();samples=[];review_signs=set()
        for seed in range(48):
            r=g.generate(f['level'],seed=seed,template=key);check(r['question']);audit_module.audit(r['question'],key);generated.append((key+'-'+str(seed),r));samples.append(r)
            fingerprints.add(r['generation']['mathematical_fingerprint']);targets.add(r['generation']['parameters']['target']);coords.add((r['generation']['parameters']['U'],r['generation']['parameters']['V']))
            same=g.generate(f['level'],seed=seed+100000,template=key,parameters=r['generation']['parameters'],profile='method-sum-bank')
            assert same['question'][':question/id']==r['question'][':question/id'];assert same['question'][':question/answer-fields'][0][':answer-field/id']==r['question'][':question/answer-fields'][0][':answer-field/id'];identity_checks+=1
            if (int(S.sign(g.sym(r['generation']['parameters']['U']))) not in review_signs if key=='easy-polynomial' else seed<2):
                reviews.append({'role':'generated variant','level':f['level'],'template':key,'record':r});review_signs.add(int(S.sign(g.sym(r['generation']['parameters']['U']))))
        assert targets=={'x','y'};assert len(fingerprints)>=16
        # Hold all mathematical data fixed, switch physical differentiated
        # variable, then independently read point order, derivative and bank.
        p=dict(samples[0]['generation']['parameters']);r1=g.generate(f['level'],template=key,parameters=p);p['target']='y' if p['target']=='x' else 'x';r2=g.generate(f['level'],template=key,parameters=p)
        check(r2['question']);assert r1['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint'];assert r1['question'][':question/id']!=r2['question'][':question/id'];target_checks+=1
        # Both ends of every independent coordinate slot and every exponent
        # domain. Colliding complete banks are expected rejections, never mixed.
        for U,V,N,M in itertools.product((f['coords'][0][0],f['coords'][0][-1]),(f['coords'][1][0],f['coords'][1][-1]),(f['ns'][0],f['ns'][-1]),(f['ms'][0],f['ms'][-1])):
            p={'a':1,'b':4,'U':str(U),'V':str(V),'n':N,'m':M}
            try:r=g.generate(f['level'],template=key,parameters=p)
            except ValueError as exc:
                assert 'collision' in str(exc) or 'Arithmetic workload:' in str(exc);continue
            check(r['question']);boundary_checks+=1
        for name,value in [('a',0),('b',-1),('a',5),('U',-100),('V',0),('n',99),('m',99),('target','z')]:
            p=dict(samples[0]['generation']['parameters']);p[name]=value
            negatives.append(must_fail(lambda p=p:g.generate(f['level'],template=key,parameters=p),'out-of-domain '+key+' '+name))
        coverage[key]={'level':f['level'],'sampled_records':len(samples),'distinct_mathematical_tasks':len(fingerprints),'targets':sorted(targets),'role_coordinate_pairs':sorted(coords),'first_48_seeds':True}
        # Normal source-family solution at its original mathematical inputs,
        # using the raw profile solely where a zero term makes five-term method
        # bank ineligible; the arithmetic stage comparison is unchanged.
        if f['source']:
            source=next(z for _,z in replays if z['generation']['template']==key)
            expected_source=g.ORIGINALS[f['source']]
            if ':question/worked-solution' in expected_source:
                original_rows=tm.rows(expected_source[':question/worked-solution']);current_rows=tm.rows(source['question'][':question/worked-solution'])
                assert [len(z) for z in original_rows]==[len(z) for z in current_rows]
    # Default sampling must actually serve every family in each supported level.
    alias_a=g.generate('hard',template='log-power-exp',parameters={'a':1,'b':1,'U':1,'V':'ln(4)','n':5})
    alias_b=g.generate('hard',template='log-power-exp',parameters={'a':1,'b':1,'U':1,'V':'2*ln(2)','n':5})
    assert alias_a['question'][':question/id']==alias_b['question'][':question/id']
    defaults={};easy_default_signs=set()
    for level in ('easy','moderate','hard'):
        default_records=[g.generate(level,seed=i) for i in range(150)]
        seen={r['generation']['template'] for r in default_records}
        if level=='easy':
            for r in default_records:
                _,target,point=tm.prompt(r['question'][':question/problem']);easy_default_signs.add(int(S.sign(point[target])))
            assert easy_default_signs=={-1,1}
        required={k for k,f in g.FAMILIES.items() if f['level']==level};assert seen==required;defaults[level]=sorted(seen)
    # Mutations exercise mathematical parsing, source stage topology, target
    # roles, full wrong/wrong equivalence, coordinate order and C0 rejection.
    test=copy.deepcopy(generated[10][1]['question'])
    mutant=copy.deepcopy(test);mutant[':question/worked-solution']=mutant[':question/worked-solution'].replace(' & =',' & =1+',1)
    negatives.append(must_fail(lambda:check(mutant),'incorrect first differentiated expression'))
    mutant2=copy.deepcopy(test);f=mutant2[':question/answer-fields'][0];f[':answer-field/choices'][1][':answer/value']=f[':answer-field/choices'][0][':answer/value']
    negatives.append(must_fail(lambda:check(mutant2),'equivalent pair in complete bank'))
    mutant3=copy.deepcopy(test);mutant3[':question/worked-solution']=mutant3[':question/worked-solution'].replace('with respect to $x,$','with respect to $y,$') if 'with respect to $x,$' in mutant3[':question/worked-solution'] else mutant3[':question/worked-solution'].replace('with respect to $y,$','with respect to $x,$')
    negatives.append(must_fail(lambda:check(mutant3),'stale differentiated-variable prose'))
    mutant4=copy.deepcopy(test);mutant4[':question/worked-solution']+='\f'
    negatives.append(must_fail(lambda:g.format_checks(mutant4),'C0 formfeed in learner solution'))
    # Reciprocal rewrite cannot be dropped while retaining equal mathematics.
    rr=next(r['question'] for sid,r in replays if sid=='q-159587');bad=copy.deepcopy(rr);block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',bad[':question/worked-solution'],re.S);parts=block[1].split(r'\\');parts[1]=parts[0].split('&',1)[1];new=bad[':question/worked-solution'][:block.start(1)]+r'\\'.join(parts)+bad[':question/worked-solution'][block.end(1):]
    bad[':question/worked-solution']=new
    def rewrite_guard(q):
        rs=tm.rows(q[':question/worked-solution']);assert re.search(r'\^\{-1\}',rs[0][1][0]),'Missing reciprocal-to-power operation'
    rewrite_guard(rr);negatives.append(must_fail(lambda:rewrite_guard(bad),'equal-but-missing reciprocal rewrite'))
    swap=copy.deepcopy(test)
    islands=list(re.finditer(r'(?<!\$)\$(?!\$)(.*?)\$',swap[':question/problem'],re.S))
    pointisland=islands[-1];pointvalue=pointisland[1].rstrip('.')
    XX,YY=tm.point_parts(pointvalue[1:-1]);reversedpoint='('+g.tex(YY)+','+g.tex(XX)+')'
    swap[':question/problem']=swap[':question/problem'][:pointisland.start()]+'$'+reversedpoint+'.$'+swap[':question/problem'][pointisland.end():]
    negatives.append(must_fail(lambda:check(swap),'swapped physical point-coordinate order'))
    sec=copy.deepcopy(next(r['question'] for _,r in generated if r['generation']['template']=='sec-power'))
    rs=tm.rows(sec[':question/worked-solution']);old=rs[1][1][0]
    collapsed=g.tex(tm.parse(old))
    sec[':question/worked-solution']=sec[':question/worked-solution'].replace(old,collapsed)
    negatives.append(must_fail(lambda:check(sec),'equal-but-collapsed secant tangent operand row'))
    for regression_key,regression_parameters in [('power-log-root',{'a':2,'b':4,'n':4,'U':9,'V':'e**2'}),('power-log-root',{'a':3,'b':3,'n':4,'U':9,'V':'e'}),('root-reciprocal',{'a':4,'b':3,'n':3,'U':4,'V':1}),('log-power-exp',{'a':1,'b':2,'n':5,'U':1,'V':'ln(5)'})]:
        negatives.append(must_fail(lambda k=regression_key,p=regression_parameters:g.generate(g.FAMILIES[k]['level'],template=k,parameters=p),'oversized coupled arithmetic '+regression_key))
    source_native=native(replays,'source-native');generated_native=native(generated,'generated-native')
    subprocess.run([sys.executable,'-B',str(D/'scalar-probes.py')],check=True)
    scalar_report=json.loads((D/'scalar-native-report.json').read_text())
    write('source-cases.json',cases);write('source-replays.json',[r for _,r in replays]);write('source-maps.json',source_maps);write('review.json',reviews);write('independent-inventory.json',{'database':g.SOURCE['database'],'basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'questions':[]});write('samples.json',[r for _,r in generated]);write('canonical-validation.json',{'source':canonical,'checked_rows':canonical_rows,'fieldless':True,'role':'canonical, excluded from practice fidelity denominator'})
    final=baseline()
    report={'status':'ready for independent root QA; not registered or approved','source_basis':g.SOURCE['basis'],'source_lineage':g.SOURCE['lineage'],'source_sha256':hashlib.sha256((D/'source.json').read_bytes()).hexdigest(),'source_counts':{'MA_practice_originals':12,'canonical':1,'independent_inventory':0,'complete_banks':12,'matched_options':60,'matched_distractors':48,'observed_correct_designations':10,'matched_correct_designations':10,'missing_correct_designations':2,'observed_worked_solutions':10,'matched_solution_stage_chains':10,'raw_exact_prompt_strings':sum(original[':question/problem']==record['question'][':question/problem'] for original,(_,record) in zip(g.ORIGINALS.values(),replays)),'presentation_normalized_prompt_math_and_prose':12},'source_fidelity':sources,'math_checks':COUNTS,'variation':coverage,'default_family_coverage':defaults,'default_easy_active_sign_coverage':sorted(easy_default_signs),'seed_order_identity_checks':identity_checks,'held_data_target_swap_checks':target_checks,'boundary_records':boundary_checks,'negative_controls':negatives,'native':{'binary_sha256':build['binary_sha256'],'verified_build_hashes':len(verified),'source':{k:source_native[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'generated':{k:generated_native[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'limitation':'Observed and generated fields are radio ID selection; two missing-key sources are tested only as explicitly synthetic inferred-key fixtures. Separate synthetic blank probes verify explicit-Euler-e semantics and preserve the known raw source scientific-notation limitation without engine changes.','scalar_diagnostics':{k:scalar_report[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks','normal_explicit_e_semantic_checks','raw_source_known_semantic_failures')}},'numeric_baseline':final,'runtime':{'python':sys.version.split()[0],'sympy':S.__version__},'plots':'none','canonical_checked_rows':canonical_rows,'arithmetic_domain_report':'finite-domain-counts.json; every finite explicit tuple accepted/rejected through public API, every accepted prompt and bank independently audited'}
    write('validation.json',report);print(json.dumps({k:report[k] for k in ('source_counts','math_checks','native','numeric_baseline')},indent=2))
if __name__=='__main__':main()
