#!/usr/bin/env python3
"""Independent QA of actual printed matrices, complete banks and stage masks.

Does not use generation parameters to infer the correct answer. Native grading
is a separate real-engine test. Full source prose and every bank are separately
checked against fixed-basis raw evidence. Any failure exits nonzero.
"""
import copy,hashlib,importlib.util,json,pathlib,re,subprocess,uuid,sys
sys.dont_write_bytecode=True
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
D=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('det_generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
MATRIX=re.compile(r'\\begin\{(aligned|vmatrix)\}(-?\d+) & (-?\d+) \\\\ (-?\d+) & (-?\d+)\\end\{\1\}')
def scalar(t):
    return parse_expr(t.strip().rstrip('.').replace('\\cdot','*'),transformations=standard_transformations+(implicit_multiplication_application,))
def check(record):
    assert set(record)=={'knowledge_point','question','generation'}
    assert record['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    q=record['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];f=q[':question/answer-fields'][0]
    for uid in [q[':question/id'],f[':answer-field/id']]+[a[':answer/id'] for a in f[':answer-field/choices']]:uuid.UUID(uid)
    assert len(q[':question/answer-fields'])==1
    for text in [prompt,sol]:
        assert text.count('$')%2==0 and text.count('$$')%2==0
        depth=0
        for ch in text:
            depth+= (ch=='{')-(ch=='}');assert depth>=0
        assert depth==0
        assert not any(s in text for s in ['+-','--','-+'])
    m=MATRIX.findall(prompt);assert len(m)==1
    a,b,c,d=map(int,m[0][1:]);expected=int(sp.Matrix([[a,b],[c,d]]).det())
    if record['generation']['profile']=='authored_operations':
        v=[a,b,c,d];level=q[':question/difficulty'].split('/')[-1]
        if level=='easy':assert max(map(abs,v))<=9 and sum(n<0 for n in v)<=1 and sum(n==0 for n in v)<=1 and max(abs(a*d),abs(b*c))>=2
        elif level=='moderate':assert all(n and abs(n)<=10 for n in v) and any(n<0 for n in v) and max(abs(a*d),abs(b*c))>=10
        else:assert level=='hard' and all(6<=abs(n)<=15 for n in v) and 2<=sum(n<0 for n in v)<=3 and max(map(abs,v))>=11 and min(abs(a*d),abs(b*c))>=50
    sm=MATRIX.findall(sol);assert len(sm)==1 and sm[0][1:]==m[0][1:]
    assert '|\\begin{aligned}a & b \\\\ c & d\\end{aligned}|=ad-bc.' in sol
    key=f[':answer-field/key'];kind=f[':answer-field/type'].split('/')[-1]
    assert kind in ['radio','blank'];assert key==('field-1' if kind=='blank' else 'selection')
    if kind=='blank':assert prompt.count('{{'+key+'}}')==1
    bank=f[':answer-field/choices'];assert len(bank)==(1 if kind=='blank' else 5)
    ids=[x[':answer/id'] for x in bank];assert len(set(ids))==len(ids)
    assert f[':answer-field/correct'][0]==':answer/id';cid=f[':answer-field/correct'][1];assert cid in ids
    values=[scalar(x[':answer/value']) for x in bank];assert len(set(values))==len(values)
    for entry,v in zip(bank,values):
        assert entry[':answer/type']==':answer.type/math' and v.is_Integer
        assert (v==expected)==(entry[':answer/id']==cid)
        assert '$' not in entry[':answer/value']
    # Derive all authored choices from the printed matrix, independently.
    if record['generation']['profile']=='authored_operations' and kind=='radio':
        assert set(values)=={a*d-b*c,a*d+b*c,b*c-a*d,a*d,a*b-c*d}
    # Read the actual final display, temporarily mask nested integer matrix,
    # then retain arithmetic rows as unevaluated strings and ordered operands.
    final=re.findall(r'\$\$(.*?)\$\$',sol,re.S)[-1].strip()
    final=MATRIX.sub('MATRIX',final)
    assert final.startswith(r'\begin{aligned}') and final.endswith(r'\end{aligned}')
    final=final[len(r'\begin{aligned}'):-len(r'\end{aligned}')]
    rows=final.split(r' \\ ')
    named='Calculate' in prompt
    assert len(rows)==(4 if named else 3)
    first=rows[0]
    assert first.count('MATRIX')==1
    if named:
        name=re.search(r'det\}?\(([A-Z])\)',prompt).group(1)
        assert name in first and first.endswith('=|MATRIX|')
        arithmetic=[r.split('=',1)[1].strip() for r in rows[1:]]
    else:
        assert first.startswith('|MATRIX| & =')
        arithmetic=[r.split('=',1)[1].strip() for r in rows]
    assert len(arithmetic)==3
    substitution,products,result=arithmetic
    # Every ordered coefficient occurrence must be exactly the printed factor,
    # including the source c*b variant (not merely equivalent final answer).
    order=[a,d,c,b] if record['generation']['template']=='named_dot_swapped' else [a,d,b,c]
    if kind=='blank':
        operands=re.fullmatch(r'\((-?\d+)\)\((-?\d+)\)-\((-?\d+)\)\((-?\d+)\)',substitution)
        wanted=f'({a})({d})-({b})({c})'
    else:
        term=r'(-?\d+|\(-?\d+\))'
        operands=re.fullmatch(term+r'\\cdot '+term+'-'+term+r'\\cdot '+term,substitution)
        def fct(n):return '('+str(n)+')' if n<0 else str(n)
        wanted=f'{a}\\cdot {fct(d)}-{fct(order[2])}\\cdot {fct(order[3])}'
    assert operands and [int(x.strip('()')) for x in operands.groups()]==order
    assert substitution==wanted
    assert scalar(substitution)==expected
    if kind=='blank' and b*c<0:wanted_products=f'{a*d}+{abs(b*c)}'
    else:wanted_products=str(a*d)+'-'+('('+str(b*c)+')' if b*c<0 else str(b*c))
    assert products==wanted_products and scalar(products)==expected
    assert result==str(expected)+('.' if kind=='blank' else '') and scalar(result)==expected
    # Mathematical identities exclude banks/presentation; content identity uses
    # actual learner data. Verify from displayed values rather than metadata.
    assert record['generation']['mathematical_fingerprint']==g.digest([a,b,c,d])
    hash_=g.digest([g.VERSION,prompt,sol,kind,sorted(x[':answer/value'] for x in bank)])
    assert record['generation']['content_fingerprint']==hash_
    assert q[':question/id']==g.ident(hash_)
    return (a,b,c,d),expected

def native(label,rec):
    f=rec['question'][':question/answer-fields'][0];cid=f[':answer-field/correct'][1]
    if f[':answer-field/type'].endswith('/radio'):
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'Every complete owned radio choice'} for a in f[':answer-field/choices']]
    else:
        v=f[':answer-field/choices'][0][':answer/value'];matrix,_=check(rec);a,b,c,d=matrix
        checks=[{'submitted':v,'expected':'accepted','purpose':'Canonical exact integer'}, {'submitted':f'({a})*({d})-({b})*({c})','expected':'accepted','purpose':'Unreduced determinant arithmetic equivalent entry'}, {'submitted':str(int(v)+1),'expected':'rejected','purpose':'Incorrect integer'}, {'submitted':str(2*int(v))+'/2','expected':'accepted','purpose':'Unreduced rational equivalent entry'}]
    return {'label':label,'record':rec,'checks':checks}

def main():
    cases=json.loads((D/'source-cases.json').read_text());sources=json.loads((D/'source.json').read_text())['record'][':knowledge-point/questions']
    assert len(cases)==len(sources)==9
    outputs=[];native_cases=[];fidelity=[];matched_choices=matched_designations=matched_solutions=0;covariance_checks=0
    for src,case in zip(sources,cases):
        assert case['original']==src
        rec=g.generate(case['level'],seed=13,template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);check(rec)
        q=rec['question'];f=q[':question/answer-fields'][0];sf=src[':question/answer-fields'][0]
        assert q[':question/problem']==src[':question/problem']
        assert f[':answer-field/key']==sf[':answer-field/key'] and f[':answer-field/type']==sf[':answer-field/type'][':db/ident']
        sv=sorted(a[':answer/value'] for a in sf[':answer-field/choices']);gv=sorted(a[':answer/value'] for a in f[':answer-field/choices'])
        assert sv==gv;matched_choices+=len(sv)
        gc=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        if ':answer-field/correct' in sf:
            assert gc==sf[':answer-field/correct'][':answer/value'];matched_designations+=1
        else:assert case['source_id']=='q-11648' and gc=='6'
        if ':question/worked-solution' in src:
            assert q[':question/worked-solution']==src[':question/worked-solution'];matched_solutions+=1
        fidelity.append({'source_id':case['source_id'],'prompt_byte_exact':True,'full_bank_byte_exact':True,'choices_matched':len(sv),'designation_matched':':answer-field/correct' in sf,'designation_inferred':':answer-field/correct' not in sf,'solution_byte_exact':':question/worked-solution' in src,'solution_authored':':question/worked-solution' not in src,'difficulty_authored':case['source_id']=='q-11648'})
        outputs.append(('Observed replay '+case['source_id'],rec));native_cases.append(native(case['source_id'],rec))
        # Changed common scale tests every original complete bank profile, not
        # only the default authored bank. Source profiles retain their limits.
        p={k:(-2*case['parameters'][k] if k in 'abcd' else case['parameters'][k]) for k in case['parameters']}
        changed=g.generate(case['level'],seed=22,template=case['template'],parameters=p,profile=case['bank_profile']);check(changed)
        assert changed['question'][':question/id']!=q[':question/id']
        outputs.append(('Generated observed scalar covariance variant '+case['source_id']+' (opaque intent)',changed));native_cases.append(native(case['source_id']+' scaled',changed))
        # Exhaust the supported finite covariance domain, independently derive
        # EVERY choice from the raw bank and t², not generator recipe metadata.
        maxscale=40//max(abs(case['parameters'][k]) for k in 'abcd')
        for scale in range(-maxscale,maxscale+1):
            if not scale:continue
            p={k:(scale*case['parameters'][k] if k in 'abcd' else case['parameters'][k]) for k in case['parameters']}
            varied=g.generate(case['level'],seed=81,template=case['template'],parameters=p,profile=case['bank_profile']);check(varied)
            bank=varied['question'][':question/answer-fields'][0][':answer-field/choices']
            assert sorted(int(a[':answer/value']) for a in bank)==sorted(scale*scale*int(a[':answer/value']) for a in sf[':answer-field/choices'])
            covariance_checks+=1
    assert matched_choices==33 and matched_designations==8 and matched_solutions==8
    variety={};checks=18+covariance_checks;order_positions=set()
    for level in ['easy','moderate','hard']:
        for template,t in g.TEMPLATES.items():
            if level not in t['levels']:continue
            fingerprints=set()
            for seed in range(140):
                rec=g.generate(level,seed,template=template);check(rec);checks+=1;fingerprints.add(rec['generation']['mathematical_fingerprint'])
                f=rec['question'][':question/answer-fields'][0]
                if f[':answer-field/type'].endswith('/radio'):order_positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
                replay=g.generate(level,seed+982,template=template,parameters=rec['generation']['parameters']);check(replay)
                assert replay['question'][':question/id']==rec['question'][':question/id']
                if seed<2:
                    outputs.append(('Authored default '+level+' '+template,rec));native_cases.append(native(level+' '+template+' '+str(seed),rec))
            assert len(fingerprints)>=125,(level,template,len(fingerprints))
            variety[level+':'+template]=len(fingerprints)
    assert order_positions==set(range(5))
    # All entrypoints and alternate presentation/complete bank identities.
    for level in ['easy','moderate','hard']:check(getattr(g,'generate_'+level)(42))
    src=cases[2];p=src['parameters'];observed=g.generate('moderate',parameters=p,profile=src['source_id']);default=g.generate('moderate',parameters=p,template=src['template'])
    assert observed['generation']['mathematical_fingerprint']==default['generation']['mathematical_fingerprint']
    assert observed['question'][':question/id']!=default['question'][':question/id']
    # Reject invalid explicit workloads and profiles rather than silently fixing.
    invalid=[('easy',dict(a=-2,b=-3,c=4,d=5,name='A')),('easy',dict(a=0,b=0,c=4,d=5,name='A')),('easy',dict(a=1,b=1,c=1,d=1,name='A')),('moderate',dict(a=2,b=3,c=4,d=5,name='A')),('moderate',dict(a=-2,b=1,c=1,d=2,name='A')),('moderate',dict(a=-11,b=3,c=4,d=5,name='A')),('hard',dict(a=-6,b=-6,c=7,d=7,name='A')),('hard',dict(a=-11,b=0,c=-12,d=13,name='A')),('hard',dict(a=-16,b=-12,c=12,d=13,name='A'))]
    for level,p in invalid:
        try:g.generate(level,parameters=p,template='named_parentheses_blank')
        except ValueError:pass
        else:raise AssertionError('Invalid explicit workload accepted')
    try:g.generate('moderate',parameters=dict(a=3,b=-4,c=-2,d=7,name='A'),profile='q-11648')
    except ValueError:pass
    else:raise AssertionError('Noncovariant opaque replay accepted')
    # Mutations prove the printed-math validator catches structural corruption.
    base=outputs[0][1]
    changes=[(':question/problem','1 & 2','2 & 2'),(':question/worked-solution','1\\cdot 0-2\\cdot 3','1\\cdot 0+2\\cdot 3'),(':question/worked-solution','0-6','0+6'),(':question/worked-solution','1\\cdot 0-2\\cdot 3','0\\cdot 1-2\\cdot 3')]
    for key,old,new in changes:
        bad=copy.deepcopy(base);assert old in bad['question'][key];bad['question'][key]=bad['question'][key].replace(old,new,1)
        try:check(bad)
        except AssertionError:pass
        else:raise AssertionError('Corrupt matrix/arithmetic structure escaped')
    (D/'native-input.json').write_text(json.dumps(native_cases,indent=2)+'\n')
    engine=pathlib.Path('generate/runs/current/check-engine')
    subprocess.run([str(engine),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
    nr=json.loads((D/'native-report.json').read_text())
    result={'passed':True,'provenance':g.PROVENANCE,'source_questions':9,'source_prompts_byte_exact':9,'source_complete_banks_exact':9,'source_radio_banks_exact':6,'source_choices_exact':33,'source_distractors_exact':24,'source_designations_matched':8,'source_designations_present':8,'source_designations_inferred':1,'source_solutions_byte_exact':8,'source_solutions_present':8,'source_solutions_authored':1,'source_mathematical_repairs':0,'source_presentation_repairs':0,'authored_unrated_level':'q-11648 moderate','authored_missing_level':'hard','printed_math_checks':checks,'exhaustive_observed_covariance_profile_instances':covariance_checks,'unique_math_tasks_in_140_samples_per_level_template':variety,'all_five_correct_option_positions_observed':True,'native_records':len(native_cases),'native_accepted':nr['accepted_checks'],'native_rejected':nr['rejected_checks'],'native_unresolved':nr['documented_unresolved_checks'],'native_engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'generator_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'fidelity':fidelity,'limitations':['Scalar observed banks underdetermine original distractor errors; numerical covariance replay is limited to common integer scaling and excluded from default authored generation.','q-11648 has no captured rating/correct ref/solution; moderate, 6 and full solution are authored/inferred separately.','No original hard rating exists; integer arithmetic bounds are an authored same-KP scope claim.'],'database_writes':0}
    (D/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    (D/'review.json').write_text(json.dumps([{'label':label,'record':rec} for label,rec in outputs],indent=2)+'\n')
    review=['# Originals and generated determinant review','Original choices may be shuffled; full banks are compared independently. Scalar covariance variants retain unresolved error intent and are not default generation.']
    for src in sources:
        f=src[':question/answer-fields'][0]
        review+=['## Raw original '+src[':question/math-academy-id'],src[':question/problem'],'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices']),src.get(':question/worked-solution','[No captured worked solution or correct designation; unrated.]')]
    for label,rec in outputs:review+=['## '+label,g.markdown(rec)]
    (D/'review.md').write_text('\n\n'.join(review)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
