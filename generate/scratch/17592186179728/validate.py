#!/usr/bin/env python3
"""Fail-closed independent displayed-math, source fidelity and native grading QA."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
sys.path.insert(0,str(ROOT));import texmath as tm
spec=importlib.util.spec_from_file_location('generator',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def write(name,data): (ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def eq(a,b):return s.simplify(a-b)==0

def formatting(text):
    assert text.count('$$')%2==0
    # Distinguish block delimiters from inline math, then pair all inline ones.
    assert text.replace('$$','').count('$')%2==0
    depth=0
    for ch in text:
        if ch=='{':depth+=1
        elif ch=='}':depth-=1
        assert depth>=0,'Unmatched closing TeX group'
    assert depth==0,'Unmatched opening TeX group'
    assert not re.search(r'--|\+-',text),'Ungrouped signed operands'


def check_record(r):
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    assert r['knowledge_point']['db_id']==g.KP_ID
    q=r['question'];gg=r['generation'];f=q[':question/answer-fields'][0]
    assert len(q[':question/answer-fields'])==1 and f[':answer-field/type']==':answer-field.type/radio'
    assert len(f[':answer-field/choices'])==5
    for key in (':question/problem',':question/worked-solution'):formatting(q[key])
    coords,P,Q=tm.read_prompt(q[':question/problem'])
    assert P.free_symbols <= {tm.x,tm.y} and Q.free_symbols <= {tm.x,tm.y}
    x0,y0,x1,y1=coords;dx=x1-x0;dy=y1-y0
    xt=x0+dx*tm.t;yt=y0+dy*tm.t
    # Independent actual-prompt calculation; generation parameters are not read.
    R=s.expand(P.subs({tm.x:xt,tm.y:yt},simultaneous=True)*dx+Q.subs({tm.x:xt,tm.y:yt},simultaneous=True)*dy)
    C=s.simplify(s.integrate(R,(tm.t,0,1)))
    path=tm.check_path_stages(q[':question/worked-solution'],coords)
    lhs,rows=tm.integral_rows(q[':question/worked-solution'])
    # The displayed assessment on the first solution LHS is also independently
    # interpreted as a one-form and compared with the actual question.
    pseudo='from the point $A('+str(x0)+','+str(y0)+')$ to the point $B('+str(x1)+','+str(y1)+'),$ then $'+lhs+'=$'
    cc,lp,lq=tm.read_prompt(pseudo)
    assert cc==coords and eq(lp,P) and eq(lq,Q),'Printed solution changes the one-form'
    kinds=[]
    for row in rows:
        value,kind,expr=tm.row_value(row,coords)
        assert eq(value,C),('Displayed row does not equal printed integral',row,value,C)
        # Verify each integrand as a function of t, beyond definite-value equality.
        if kind=='integral':assert eq(expr,R),('Displayed integrand differs',row,expr,R)
        if kind=='antiderivative':assert eq(s.diff(expr,tm.t),R),('Wrong displayed antiderivative',row)
        kinds.append(kind)
    assert kinds[-1]=='scalar' and 'antiderivative' in kinds
    if gg['origin']=='authored':
        assert len(rows)==9 and kinds[:5]==['integral']*5
        # Ordered operations retain actual products, two separately distributed
        # components, a collected sum, endpoint inputs, then evaluated endpoints.
        assert rows[2].count(r'\cdot') >= (3 if gg['template']=='easy_linear' else 4)
        assert rows[3].count(r'\left(')==2 and rows[3].count(r'\right)')==2
        assert r'\left(1\right)' in rows[6] and r'\left(0\right)' in rows[6]
        assert 't' not in rows[7].replace(r'\left','').replace(r'\right','')
        _,primitive_kind,primitive_expr=tm.row_value(rows[5],coords)
        assert primitive_kind=='antiderivative'
        primitive_terms=primitive_expr.as_ordered_terms()
        # Two outer endpoint groups, with one separately evaluated component
        # group per primitive term at EACH endpoint, including zero terms.
        assert rows[7].count(r'\left(')==2+2*len(primitive_terms),'Endpoint components collapsed before collection'
        expected_endpoint='+'.join(g.par(g.tex(term.subs(tm.t,1))) for term in primitive_terms)
        expected_start='+'.join(g.par(g.tex(term.subs(tm.t,0))) for term in primitive_terms)
        assert rows[7]==g.par(expected_endpoint)+'-'+g.par(expected_start),'Evaluated endpoint components changed or reordered'
        level=q[':question/difficulty'].split('/')[-1]
        if level in ('moderate','hard'):assert s.degree(R,tm.t)==3 and x0 and y0
    vals=[];checks=[];correct_ids=[]
    for a in f[':answer-field/choices']:
        formatting(a[':answer/value']);v=tm.parse_tex(a[':answer/value']);assert not v.free_symbols
        assert not any(eq(v,u) for u in vals),'Equivalent complete scalar choices'
        vals.append(v);correct=eq(v,C)
        if correct:correct_ids.append(a[':answer/id'])
        checks.append({'submitted_answer_id':a[':answer/id'],'expected':'accepted' if correct else 'rejected','purpose':'Independent printed-math scalar selection'})
    assert correct_ids==[f[':answer-field/correct'][1]]
    # Content hash from exactly displayed content, independent of parameter labels.
    expected=g.digest({'version':g.VERSION,'prompt':q[':question/problem'],'solution':q[':question/worked-solution'],'bank':sorted(a[':answer/value'] for a in f[':answer-field/choices'])})
    assert expected==gg['content_sha256']
    canonical={'A':list(coords[:2]),'B':list(coords[2:]),'P':s.srepr(s.expand(P)),'Q':s.srepr(s.expand(Q)),'limits':[0,1]}
    assert g.digest(canonical)==gg['mathematical_fingerprint']
    return checks,{'template':gg['template'],'level':q[':question/difficulty'].split('/')[-1],'parameters':gg['parameters'],'integral_rows':len(rows),'kinds':kinds,**path}


def run():
    records=[];engine=[];coverage=[];stages=[];review=['# Line-segment one-form generator review','Local author preview at math basis 1356. Observed source masks and banks are separate from authored defaults. Raw q-124663 has an endpoint typo; generated versions repair +10 to +1.']
    cases=json.loads((ROOT/'source-cases.json').read_text());assert {c['source_id'] for c in cases}==set(g.QS)
    for case in cases:
        name=case['template'];src=g.QS[case['source_id']]
        r=g.generate('easy',template=name,parameters=case['parameters'],profile=case['bank_profile'])
        checks,st=check_record(r);stages.append(st);records.append(r);engine.append({'label':'source/'+name,'record':r,'checks':checks})
        q=r['question'];origf=src[':question/answer-fields'][0];newf=q[':question/answer-fields'][0]
        a=[tm.parse_tex(v[':answer/value']) for v in origf[':answer-field/choices']];b=[tm.parse_tex(v[':answer/value']) for v in newf[':answer-field/choices']]
        assert len(a)==len(b)==5 and all(sum(eq(v,w) for w in b)==1 for v in a)
        original_correct=tm.parse_tex(origf[':answer-field/correct'][':answer/value'])
        generated_correct=next(tm.parse_tex(v[':answer/value']) for v in newf[':answer-field/choices'] if v[':answer/id']==newf[':answer-field/correct'][1]);assert eq(original_correct,generated_correct)
        assert q[':question/problem']==src[':question/problem']
        exact_solution=q[':question/worked-solution']==src[':question/worked-solution']
        repaired=src[':question/worked-solution'].replace(r'4[\frac{4}{3}+10]',r'4[\frac{4}{3}+1]')
        assert q[':question/worked-solution']==repaired
        coverage.append({'source_id':name,'prompt_exact':True,'bank_values_matched':5,'distractors_matched':4,'correct_designation_matched':True,'solution_raw_exact':exact_solution,'solution_repaired_exact':True,'row_sequence_exact':True})
        review += ['\n## Original '+name,src[':question/problem'],'\nBank: '+', '.join('$'+v[':answer/value']+'$' for v in origf[':answer-field/choices']), '\n'+src[':question/worked-solution'], '\n### Generated original-parameter replay',g.markdown(r)]
        for k in (-3,2):
            v=g.generate('easy',seed=73,template=name,parameters={'k':k},profile=case['bank_profile']);checks,st=check_record(v);stages.append(st);records.append(v);engine.append({'label':f'profile-variation/{name}/{k}','record':v,'checks':checks});review+=['\n### Generated observed-profile variant (uniform one-form multiplier)',g.markdown(v)]
        v=g.generate('easy',seed=9,template=name,parameters={'k':2},profile='method');checks,st=check_record(v);stages.append(st);records.append(v);engine.append({'label':'method-variation/'+name,'record':v,'checks':checks});review+=['\n### Generated authored method-bank variant',g.markdown(v)]
    diversity={};counts={};positions=set()
    for name,spec in g.TEMPLATES.items():
        if spec['origin']!='authored':continue
        fingerprints=set()
        for seed in range(24):
            r=g.generate(spec['level'],seed=seed,template=name);checks,st=check_record(r);stages.append(st);records.append(r);engine.append({'label':f'authored/{name}/{seed}','record':r,'checks':checks});fingerprints.add(r['generation']['mathematical_fingerprint'])
            f=r['question'][':question/answer-fields'][0];positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
            if seed<2:review+=['\n### Generated authored '+spec['level']+' example',g.markdown(r)]
            changed=g.generate(spec['level'],seed=seed+300,template=name,parameters=r['generation']['parameters'])
            assert r['question'][':question/id']==changed['question'][':question/id'],'Seed affects content ID'
        assert len(fingerprints)>=20,'Too little substantive endpoint/form variation'
        diversity[name]=len(fingerprints);counts[spec['level']]=counts.get(spec['level'],0)+24
    assert len(positions)>=4,'Radio answer position not varied'
    # Every legal observed k value is checked for parameter identity, values and
    # stage scaling; fixed path geometry never inflates endpoint variety claims.
    for name in g.OBS:
        for k in range(-9,10):
            if not k:continue
            v=g.generate('easy',template=name,parameters={'k':k},profile=name+'_observed')
            check_record(v)
    # Boundary guards apply to explicit authored inputs as well as samplers.
    invalid=[]
    for name in ('moderate_canonical','hard_coupled'):
        valid=g.generate(g.TEMPLATES[name]['level'],template=name)['generation']['parameters']
        for key,val in [('a',0),('b',-4),('x0',0),('y0',0),('x1',8),('x0',-8)]:
            bad={**valid,key:val}
            try:g.generate(g.TEMPLATES[name]['level'],template=name,parameters=bad)
            except ValueError:invalid.append([name,key,val])
            else:raise AssertionError('Invalid explicit scope accepted')
    for k in (0,10,-10):
        try:g.generate('easy',template='q-39345',parameters={'k':k})
        except ValueError:invalid.append(['observed','k',k])
        else:raise AssertionError('Invalid multiplier accepted')
    # Deliberate corruption proves validation actually reads printed stages and
    # prompt endpoints, rather than trusting generator metadata/final answer.
    mutation_failures=[]
    baseline=g.generate('hard',seed=5)
    for label,modify in [('endpoint',lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem'].replace('point $A(','point $A(8,',1))),('distribution',lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace(r'\right)+\left(',r'\right)-\left(',1)))]:
        rr=json.loads(json.dumps(baseline));modify(rr)
        try:check_record(rr)
        except Exception:mutation_failures.append(label)
        else:raise AssertionError('Displayed corruption undetected')
    rr=json.loads(json.dumps(baseline))
    q=rr['question'];lhs,rows=tm.integral_rows(q[':question/worked-solution'])
    cc,pp,qq=tm.read_prompt(q[':question/problem'])
    total,_,_=tm.row_value(rows[7],cc)
    q[':question/worked-solution']=q[':question/worked-solution'].replace(rows[7],g.par(g.tex(total))+'-'+g.par('0'))
    try:check_record(rr)
    except Exception:mutation_failures.append('collapsed-evaluated-endpoint-components')
    else:raise AssertionError('Pedagogically collapsed endpoint row undetected')
    rawq=g.QS['q-124663']
    rawlhs,rawrows=tm.integral_rows(rawq[':question/worked-solution'])
    rawbad=next(v for v in rawrows if '+10]' in v)
    rawvalue,_,_=tm.row_value(rawbad,(-1,1,1,3))
    assert rawvalue==s.Rational(136,3) and rawvalue!=s.Rational(28,3)
    write('raw-source-reconstruction.json',{'source_id':'q-124663','raw_question':rawq,'raw_endpoint_row':rawbad,'independently_evaluated_raw_row':str(rawvalue),'correct_value':'28/3','eligible_for_normal_output':False,'repair':'replace +10 with +1 only'})
    write('engine-input.json',engine)
    subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-validation.json')],check=True)
    native=json.loads((ROOT/'engine-validation.json').read_text());assert native['documented_unresolved_checks']==0
    result={'passed':True,'database':g.SOURCE['database'],'basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'generator_sha256':hashlib.sha256(ROOT.with_suffix('.py').read_bytes()).hexdigest(),'source_questions':9,'source_prompts_exact':9,'source_bank_values_matched':45,'source_bank_values_total':45,'source_distractors_matched':36,'source_distractors_total':36,'source_complete_banks_matched':9,'source_correct_designations_matched':9,'source_solutions_raw_exact':8,'source_solutions_raw_total':9,'source_solutions_repaired_exact':9,'source_solutions_repaired_total':9,'source_solution_stage_sequences_matched':9,'mathematical_repairs':{'q-124663':{'raw':'4[4/3+10]-4[0]','repaired':'4[4/3+1]-4[0]','evidence':'t=1 in 4[4t³/3+t] equals 4[4/3+1] =28/3; raw row equals136/3'}},'displayed_question_and_stages_checked_records':len(stages)+9*18,'native_records':len(engine),'native_accepted':native['accepted_checks'],'native_rejected':native['rejected_checks'],'unresolved_grading':0,'authored_scope':'easy linear/product; moderate one cubic plus quadratic product; hard two cubic products; all line-segment parameterization and polynomial integration','authored_diversity_24_seeds':diversity,'authored_level_records':counts,'source_profile_interpretation':'wrong scalar intent remains unresolved; complete uniform one-form multiplier patterns only; not default banks','invalid_inputs_rejected':invalid,'displayed_mutations_rejected':mutation_failures,'plots':'none','no_database_writes':True,'source_coverage':coverage,'stage_checks':stages,'engine_binary_sha256':hashlib.sha256((REPO/'generate/runs/current/check-engine').read_bytes()).hexdigest()}
    write('validation.json',result);write('review.json',records);(ROOT/'review.md').write_text('\n\n'.join(review)+'\n')
    print('PASS: 9/9 prompts; 45/45 choices; 36/36 distractors; 9/9 banks; solutions 8/9 raw and 9/9 repaired; '+str(len(stages)+9*18)+' independently printed-math records; native '+str(native['accepted_checks'])+' accepted / '+str(native['rejected_checks'])+' rejected.')
if __name__=='__main__':run()
