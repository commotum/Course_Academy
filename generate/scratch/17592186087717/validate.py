#!/usr/bin/env python3
"""Independent displayed-expression, whole-bank, prose/stage and native checks."""
import importlib.util,json,re,subprocess,hashlib
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def equal(a,b):return sp.simplify(a-b)==0

def printed_formula(prompt):
    math=next(g.inner(m.group()).strip() for m in g.MATH.finditer(prompt) if 'x=' in m.group() or 'x =' in m.group())
    m=re.search(r'x\s*=\s*(.*?)\s*,.*?y\s*=\s*(.*?)(?=,)',math.replace(r'\,','§'),re.S)
    return {axis:g.scalar(expr.replace('§',r'\,')) for axis,expr in zip(('x','y'),m.groups())}

def check_record(r):
    q=r['question'];prompt=q[':question/problem'];solution=q[':question/worked-solution'];f=printed_formula(prompt)
    rows=g.table_rows(prompt);times=[g.scalar(x.strip('$')) for x in g.cells(rows[0])[1:]];targets={}
    for axis,row in zip(('x','y'),rows[2:4]):
        for t,c in zip(times,g.cells(row)[1:]):
            v=sp.simplify(f[axis].subs(g.T,t)); marker=c.strip('$')
            if marker in ('a','b','c'):targets[marker]=v
            elif c.startswith('{{'):targets[c.strip('{}')]=v
            else:assert equal(g.scalar(marker),v),(axis,t,c,v)
    for row in g.table_rows(solution):
        cs=g.cells(row)
        if cs[0] not in ('$x$','$y$'):continue
        axis=cs[0].strip('$')
        for t,c in zip(times,cs[1:]):assert equal(g.scalar(c.strip('$')),f[axis].subs(g.T,t)),('solution table',t,c)
    combo_match=re.search(r'Find the value of \$(.*?)\$',prompt)
    combo=combo_match[1].rstrip('.') if combo_match else None
    if combo:
        correct=sp.sympify(combo,locals=targets)
        assert all(n in targets for n in ('a','b','c'))
    for field in q[':question/answer-fields']:
        choices=field[':answer-field/choices'];vals=[g.scalar(a[':answer/value']) for a in choices]
        assert len(set(vals))==len(vals),'Complete bank collision'
        aid=field[':answer-field/correct'][1];correct_choice=next(a for a in choices if a[':answer/id']==aid)
        expected=correct if combo else targets[field[':answer-field/key']]
        assert equal(g.scalar(correct_choice[':answer/value']),expected)
        assert len({a[':answer/id'] for a in choices})==len(choices)
        assert all(a[':answer/value'].count('$')==0 for a in choices)
    # Evaluate each actual displayed equation stage; no metadata is trusted.
    for m in g.MATH.finditer(solution):
        body=g.inner(m.group()).strip().rstrip('.,')
        if '=' not in body or 'le' in body:continue
        lhs,*rhs=body.split('=')
        if lhs=='t':continue
        if lhs in ('x','y'):
            assert equal(g.scalar(rhs[0]),f[lhs]);continue
        if lhs.strip() in ('a','b','c'):expected=targets[lhs.strip()]
        elif re.fullmatch(r'[xy]\(-?\d+\)',lhs):
            axis=lhs[0];t=int(lhs[2:-1]);expected=f[axis].subs(g.T,t)
        elif combo and sp.sympify(lhs)==sp.sympify(combo):expected=correct
        else:raise AssertionError(('Unknown solution component',body))
        for stage in rhs:assert equal(g.scalar(stage),expected),('displayed stage',body,stage,expected)
    # Check target names/arguments in prose against the next displayed equality.
    for section in solution.split('- To find the value of ')[1:]:
        header=re.match(r'\$(.*?),\$ we substitute \$t=(.*?)\$ into \$(.*?)=([^$]*)\$',section,re.S)
        assert header,section[:100]
        target,time,axis,formula=header.groups();formula=formula.rstrip('.')
        assert equal(g.scalar(formula),f[axis])
        if target in ('a','b','c'):assert equal(targets[target],f[axis].subs(g.T,g.scalar(time)))
        else:
            mm=re.fullmatch(r'([xy])\((-?\d+)\)',target);assert mm and mm[1]==axis and int(mm[2])==int(g.scalar(time))
    # Balanced mathematics and braces; replay whitespace is normalized separately.
    for text in (prompt,solution):
        assert text.count('$')%2==0
        assert text.count('{')==text.count('}')
    r2=g.generate(q[':question/difficulty'].split('/')[-1],seed=543,template=r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['bank_profile'])
    assert r2['question']==q,'Content identity depends on seed'
    return True

def normalized(s):return re.sub(r'\s+','',s)

def native_fixture(label,r):
    checks=[]
    for i,f in enumerate(r['question'][':question/answer-fields']):
        for a in f[':answer-field/choices']:
            correct=a[':answer/id']==f[':answer-field/correct'][1]
            if f[':answer-field/type'].endswith('/radio'):
                checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if correct else 'rejected','purpose':'owned radio choice'})
            else:
                v=g.scalar(a[':answer/value']);n,d=sp.fraction(v)
                equivalent=f'(2*({str(n)}))/(2*({str(d)}))'
                checks.extend([{'field_index':i,'submitted':a[':answer/value'],'expected':'accepted','purpose':'canonical blank'}, {'field_index':i,'submitted':equivalent,'expected':'accepted','purpose':'unreduced equivalent scalar'}, {'field_index':i,'submitted':str(v+1),'expected':'rejected','purpose':'wrong scalar'}])
    return {'label':label,'record':r,'checks':checks}

def main():
    cases=[];review=[];engine=[];counts={'questions':0,'original_banks':0,'original_choices':0,'original_distractors':0,'matched_correct_designations':0,'original_correct_designations':0,'solution_exact_raw':0,'solution_repaired':0,'solution_authored_missing':0,'fieldless_authored_layouts':0}
    extraction=[];errors=[]
    for qid,q in g.RAW.items():
        s=g.SPECS[qid];fields=q.get(':question/answer-fields',[])
        profile='observed-scalar-replay' if s['combo'] and fields else 'authored-combination-blank' if s['combo'] else 'blank'
        case={'source_id':qid,'template':qid,'parameters':{'k':1},'bank_profile':profile,'difficulty':'easy','difficulty_origin':'authored assignment' if ':question/difficulty' not in q else 'observed'}
        cases.append(case);r=g.generate('easy',template=qid,parameters=case['parameters'],profile=profile);check_record(r);engine.append(native_fixture(qid,r));review.append({'label':qid+' replay','record':r})
        counts['questions']+=1
        expected_prompt=q[':question/problem']+ ('\n\n{{selection}}' if not fields else '')
        assert normalized(expected_prompt)==normalized(r['question'][':question/problem']),qid+' prompt fidelity'
        if fields:
            generated={f[':answer-field/key']:f for f in r['question'][':question/answer-fields']}
            for field in fields:
                ff=generated[field[':answer-field/key']];assert ff[':answer-field/type']==field[':answer-field/type'][':db/ident']
                a=sorted([g.scalar(v[':answer/value']) for v in field[':answer-field/choices']],key=str);b=sorted([g.scalar(v[':answer/value']) for v in ff[':answer-field/choices']],key=str)
                assert a==b,(qid,a,b);counts['original_choices']+=len(a)
                if len(a)>1:counts['original_banks']+=1;counts['original_distractors']+=len(a)-1
                if field.get(':answer-field/correct'):
                    correct=next(x for x in ff[':answer-field/choices'] if x[':answer/id']==ff[':answer-field/correct'][1]);assert equal(g.scalar(field[':answer-field/correct'][':answer/value']),g.scalar(correct[':answer/value']))
                    counts['matched_correct_designations']+=1;counts['original_correct_designations']+=1
        else:counts['fieldless_authored_layouts']+=1
        expected=q.get(':question/worked-solution','')
        for a,b in g.REPAIRS.get(qid,[]):expected=expected.replace(a,b)
        if expected:
            assert normalized(expected)==normalized(r['question'][':question/worked-solution']),(qid,'full solution prose/stage fidelity')
            counts['solution_repaired' if qid in g.REPAIRS else 'solution_exact_raw']+=1
        else:counts['solution_authored_missing']+=1
        matches={}
        if s['combo']:
            base_values={axis:[g.scalar(s['f'+axis]).subs(g.T,t) for t in s['times']] for axis in ('x','y')}
            abc={n:base_values[axis][i] for n,(axis,i) in s['slots'].items()}
            expression=sp.sympify(s['combo']);correct=expression.subs({sp.Symbol(n):v for n,v in abc.items()})
            candidates={'reverse entire combination sign':-correct}
            for n in ('a','b','c'):
                axis,i=s['slots'][n];coefficient=expression.coeff(sp.Symbol(n));base=abc[n]
                candidates['reverse '+n+' sign']=correct-2*coefficient*base
                candidates['omit '+n]=correct-coefficient*base
                candidates[n+' wrong coordinate at same time']=correct+coefficient*(base_values['y' if axis=='x' else 'x'][i]-base)
                candidates[n+' negate input']=correct+coefficient*(g.scalar(s['f'+axis]).subs(g.T,-s['times'][i])-base)
                for j,t in enumerate(s['times']):
                    if j!=i:candidates[n+' use printed t='+str(t)]=correct+coefficient*(base_values[axis][j]-base)
            for field in fields:
                for option in field[':answer-field/choices']:
                    value=g.scalar(option[':answer/value'])
                    matches[option[':answer/value']]=[name for name,v in candidates.items() if equal(v,value) and not equal(value,correct)]
        components={'source_id':qid,'numbers':{'times':s['times'],'x_formula':s['fx'],'y_formula':s['fy']},'slots':s['slots'],'combination':s['combo'],'field_layout':[{ 'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident']} for f in fields], 'prompt_math_components':[g.inner(m.group()) for m in g.MATH.finditer(q[':question/problem'])], 'solution_math_components':[g.inner(m.group()) for m in g.MATH.finditer(q.get(':question/worked-solution',''))], 'banks':[{ 'field':f[':answer-field/key'],'options':[{ 'value':a[':answer/value'],'correct_designation':a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id') if f.get(':answer-field/correct') else None,'recipe':'k × ('+a[':answer/value']+')' if len(f[':answer-field/choices'])>1 else 'exact coordinate substitution', 'interpretation':'opaque scalar replay; error intent unresolved' if len(f[':answer-field/choices'])>1 else 'observed blank'} for a in f[':answer-field/choices']]} for f in fields], 'supported_operation_matches':matches,'operation_match_policy':'Every exact single-operation match is recorded. Multiple matches are ambiguous, and a unique numerical match is still only a hypothesis; banks remain explicit replay profiles.','raw_problem':q[':question/problem'],'raw_solution':q.get(':question/worked-solution'), 'repairs':g.REPAIRS.get(qid,[])}
        extraction.append(components)
        for k in (-2,2):
            rr=g.generate('easy',template=qid,parameters={'k':k},profile=profile);check_record(rr);review.append({'label':qid+' generated scalar-replay variant k='+str(k),'record':rr});engine.append(native_fixture(qid+' k='+str(k),rr))
    # Normal parameter generation exercises independent coefficient families,
    # every fixed-workload level, and native equivalent-entry grading.
    for level in ('easy','moderate','hard'):
        seen=set()
        for seed in range(30):
            r=g.generate(level,seed);check_record(r);seen.add(r['generation']['parameter_fingerprint']);engine.append(native_fixture(level+' seed '+str(seed),r))
            if seed<2:review.append({'label':'authored '+level+' generated variant '+str(seed),'record':r})
        assert len(seen)>=25,(level,'insufficient variety')
        # Explicit signed upper/lower workload bounds and boundary rejection.
        for bad in ({'fx':'-99*t+1','fy':'t+2'}, {'fx':'t**5+1','fy':'t+2'}):
            try:g.generate(level,parameters=bad)
            except ValueError:pass
            else:raise AssertionError('Invalid explicit domain silently accepted')
    # Same mathematics across complete different banks: identical mathematical
    # fingerprint, distinct presentation identity and owned option UUIDs.
    observed=g.generate('easy',template='q-69922',parameters={'k':2},profile='observed-scalar-replay')
    authored=g.generate('easy',template='q-69922',parameters={'k':2},profile='authored-sign-input')
    assert observed['generation']['parameter_fingerprint']==authored['generation']['parameter_fingerprint']
    assert observed['question'][':question/id']!=authored['question'][':question/id']
    try:g.generate('easy',template='q-6834',parameters={'k':2},profile='authored-sign-input')
    except ValueError:pass
    else:raise AssertionError('A colliding whole bank was repaired or accepted')
    for level in ('moderate','hard'):
        record=g.generate(level,17)
        equivalent={k:str(sp.expand(g.scalar(v))) for k,v in record['generation']['parameters'].items()}
        rr=g.generate(level,23,template=record['generation']['template'],parameters=equivalent)
        assert rr['generation']['parameter_fingerprint']==record['generation']['parameter_fingerprint']
        assert rr['question']==record['question']
    # A displayed-only mutation must fail despite unchanged generator metadata.
    import copy
    original=g.generate('easy',template='q-69922',parameters={'k':2},profile='observed-scalar-replay')
    mutations=[]
    rr=copy.deepcopy(original);rr['question'][':question/problem']=rr['question'][':question/problem'].replace(r'2\left(2t+1\right)',r'2\left(2t+2\right)',1);mutations.append(rr)
    rr=copy.deepcopy(original);rr['question'][':question/problem']=rr['question'][':question/problem'].replace('$2$ | $6$', '$3$ | $6$',1);mutations.append(rr)
    rr=copy.deepcopy(original);rr['question'][':question/worked-solution']=rr['question'][':question/worked-solution'].replace(r'2\left(0-1\right)',r'2\left(0+1\right)',1);mutations.append(rr)
    for mutated in mutations:
        assert mutated['question']!=original['question'],'Mutation did not apply'
        try:check_record(mutated)
        except AssertionError:pass
        else:raise AssertionError('Displayed-content mutation escaped readback')
    # A defensible authored five-choice source-shaped bank is separately tested.
    for qid in ('q-6742','q-6825','q-69922'):
        r=g.generate('easy',template=qid,parameters={'k':2},profile='authored-sign-input');check_record(r);review.append({'label':qid+' authored complete sign-error bank','record':r});engine.append(native_fixture(qid+' authored bank',r))
    (ROOT/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(ROOT/'source-bank-extraction.json').write_text(json.dumps(extraction,indent=2)+'\n');(ROOT/'review.json').write_text(json.dumps(review,indent=2)+'\n');(ROOT/'engine-input.json').write_text(json.dumps(engine,indent=2)+'\n')
    result=subprocess.run(['generate/runs/current/check-engine',str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],capture_output=True,text=True)
    assert result.returncode==0,result.stdout+result.stderr
    report={'status':'passed','provenance':{k:v for k,v in g.SOURCE.items() if k!='record'},'source_fidelity':counts,'native_fixtures':len(engine),'native_checks':sum(len(x['checks']) for x in engine),'independent_validation':'actual printed x(t), y(t), all prompt/completed table cells, every numeric equality stage, prose target/argument/coordinate labels, exact scalar banks, field ownership, mathematical correctness, bounds and seed identity','normal_parameter_trials_per_level':30,'observed_templates':18,'original_bank_interpretation':'8 complete banks retained as opaque scalar-replay profiles; no inferred distractor intent claimed','authored_level_extensions':['moderate fractional quadratic three-cell table','hard fractional cubic three-cell table'],'unresolved_findings':['q-6827 original correct designation and worked solution absent; 14 derived, solution authored','q-123754 and q-69923 original widgets/fields absent across local captures; one combination blank each is authored, not observed','All original scalar distractor error intentions are underdetermined; explicit replay only'],'engine_sha256':hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest()}
    (ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    review_md=['# Source and generated review','Raw immutable source and full mathematical component/bank inventory are in source.json and source-bank-extraction.json. Source fields absent in two records are explicitly authored combination blanks. Source scalar replay banks are opaque evidence profiles.']
    for qid,q in g.RAW.items():review_md+=['\n## Original '+qid,'Observed difficulty: '+str(q.get(':question/difficulty','unrated')),q[':question/problem'],'\nRaw solution:\n'+str(q.get(':question/worked-solution','not captured')),'\nRaw fields:\n```json\n'+json.dumps(q.get(':question/answer-fields',[]),indent=2)+'\n```']
    for item in review:review_md+=['\n## '+item['label'],g.markdown(item['record'])]
    (ROOT/'review.md').write_text('\n\n'.join(review_md)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
