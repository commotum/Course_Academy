#!/usr/bin/env python3
"""Full bank/prose/shape fidelity, independently parsed stages, native grading.

Writes only this private evidence directory. No database reads or writes.
"""
import copy,hashlib,importlib.util,json,re,subprocess,sys,uuid
from pathlib import Path
import sympy as sp
from math_check import A,X,ALPHA,expression,audit,family_equivalent
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('ode_general',ROOT.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def formatting(text):
    assert not any(ord(c)<32 and c!='\n' for c in text),'hidden control character'
    assert text.count('$')%2==0,'unbalanced dollars'
    for block in re.findall(r'\$\$[\s\S]*?\$\$|(?<!\$)\$(?!\$)[^$]*?\$',text):
        depth=0
        for c in block:
            if c=='{':depth+=1
            if c=='}':depth-=1
            assert depth>=0
        assert depth==0,'unbalanced group'
    assert '--' not in text and '+-' not in text,'ungrouped signed tokens'
    assert '@@' not in text

def check_record(r,raw_missing=False):
    assert set(r)=={'knowledge_point','question','generation'}
    assert r['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    q=r['question'];f=q[':question/answer-fields'][0]
    assert len(q[':question/answer-fields'])==1
    assert f[':answer-field/key']=='field-1' and f[':answer-field/type']==':answer-field.type/blank'
    assert q[':question/problem'].count('{{field-1}}')==1
    for t in [q[':question/problem'],q.get(':question/worked-solution','')]:formatting(t)
    assert ':question/math-academy-id' not in q
    if raw_missing:
        assert ':question/difficulty' not in q and ':question/worked-solution' not in q
        assert set(f)=={':answer-field/id',':answer-field/key',':answer-field/type'}
    else:
        assert q[':question/worked-solution'].startswith(g.OPENING)
        assert f[':answer-field/correct'][0]==':answer/id'
        answers=f[':answer-field/choices'];assert len(answers) in [1,2]
        assert len(set(a[':answer/id'] for a in answers))==len(answers)
        assert f[':answer-field/correct'][1] in [a[':answer/id'] for a in answers]
        for a in answers:
            assert set(a)=={':answer/id',':answer/type',':answer/value'}
            assert a[':answer/type']==':answer.type/math'
            assert '$' not in a[':answer/value'] and '=' not in a[':answer/value']
            formatting(a[':answer/value'])
    for value in [q[':question/id'],f[':answer-field/id']]+[a[':answer/id'] for a in f.get(':answer-field/choices',[])]:assert str(uuid.UUID(value))==value
    assert r==json.loads(json.dumps(r))
    assert r['generation']['plot_rating']=='none' and r['generation']['plot_assets']=={}
    return audit(r)

def engine_case(r,label):
    f=r['question'][':question/answer-fields'][0];p=r['generation']['parameters'];level=r['generation']['level']
    canonical=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
    a,k,b=p['a'],p['k'],p['b']
    if level=='moderate':equiv='(A'+g.signed(b,'x')+')'+g.exponential(a)
    else:
        q=sp.Rational(p.get('c',b),k-a)
        equiv=g.exponential(a)+'(A'+(g.signed(b,'x') if level=='hard' else '')+g.signed(q,g.exponential(k-a))+')'
    assert sp.simplify(expression(equiv)-expression(canonical))==0
    checks=[{'submitted':canonical,'expected':'accepted','purpose':'canonical complete RHS'},
            {'submitted':equiv,'expected':'accepted','purpose':'meaningful factored equivalent exponential family with prescribed A placement'},
            {'submitted':'('+canonical+')+1','expected':'rejected','purpose':'incorrect added nonhomogeneous constant'},
            {'submitted':g.multiply(b,g.exponential(k)),'expected':'rejected','purpose':'forcing is not complete general family'},
            {'submitted':g.multiply(p.get('c',b),'x'+g.exponential(a)) if level=='moderate' else g.multiply(sp.Rational(p.get('c',b),k-a),g.exponential(k)), 'expected':'rejected','purpose':'particular solution alone omits arbitrary complementary term'}]
    return {'label':label,'record':r,'checks':checks}

def main():
    sources=json.loads((ROOT/'source.json').read_text())['record'][':knowledge-point/questions']
    fidelity=[];reviews=[];audits=[];engine=[]
    for c,q in zip(g.CASES,sources):
        raw=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])
        qr=raw['question'];sourcefield=q[':question/answer-fields'][0];f=qr[':question/answer-fields'][0]
        assert qr[':question/problem']==q[':question/problem']
        assert qr.get(':question/worked-solution')==q.get(':question/worked-solution')
        assert (':question/difficulty' in qr)==(':question/difficulty' in q)
        assert f[':answer-field/key']==sourcefield[':answer-field/key']
        assert f[':answer-field/type']==sourcefield[':answer-field/type'][':db/ident']
        bank=sourcefield.get(':answer-field/choices',[]);newbank=f.get(':answer-field/choices',[])
        # Alias values are retained exactly and paired with their original designation.
        expected=[(a[':answer/value'],a[':answer/id']==sourcefield[':answer-field/correct'][':answer/id']) for a in bank]
        generated=[(a[':answer/value'],a[':answer/id']==f[':answer-field/correct'][1]) for a in newbank]
        assert sorted(expected)==sorted(generated),(c,expected,generated)
        if not bank:assert ':answer-field/correct' not in f and ':answer-field/choices' not in f
        fidelity.append({'source_id':c['source_id'],'raw_prompt_exact':True,'raw_solution_exact':True if ':question/worked-solution' in q else None,'bank_values':len(bank),'designation_match':True if bank else None,'field_shape_match':True,'unrated':c['unrated_authored_assignment']})
        audits.append(check_record(raw,not bank));reviews.append({'label':'raw source replay '+c['source_id'],'record':raw})
        normal=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile='observed:'+c['source_id'])
        audits.append(check_record(normal));reviews.append({'label':'normal source replay '+c['source_id'],'record':normal});engine.append(engine_case(normal,'normal-source/'+c['source_id']))
        if bank:engine.append(engine_case(raw,'raw-source/'+c['source_id']))
        # Both changed signs and changed exponents exercise each original layout.
        pp=dict(c['parameters']);pp['a']=-pp['a'];pp['k']=-pp['k'];pp['b']=-pp['b']
        variant=g.generate(c['level'],parameters=pp,profile='observed:'+c['source_id'])
        audits.append(check_record(variant));reviews.append({'label':'generated signed variant '+c['source_id'],'record':variant});engine.append(engine_case(variant,'variant/'+c['source_id']))
    for level in ['easy','moderate','hard']:
        for seed in [42,73]:
            r=g.generate(level,seed);audits.append(check_record(r));reviews.append({'label':'generated '+level+' seed '+str(seed),'record':r});engine.append(engine_case(r,level+'/'+str(seed)))
    samples=[]
    for level in ['easy','moderate','hard']:
        for seed in range(30):
            r=g.generate(level,seed);audits.append(check_record(r));samples.append(r)
            fixed=g.generate(level,seed+10000,parameters=r['generation']['parameters'])
            assert r['question']==fixed['question']
            assert r['generation']['mathematical_fingerprint']==fixed['generation']['mathematical_fingerprint']
    # Boundary and explicit-input scope enforcement, positive/negative inputs.
    for level,ps in [('easy',[{'a':8,'k':-8,'b':48},{'a':-8,'k':8,'b':-48}]),('moderate',[{'a':8,'k':8,'b':12},{'a':-8,'k':-8,'b':-12}]),('hard',[{'a':6,'k':-6,'b':18,'c':18},{'a':-6,'k':6,'b':-18,'c':-18}])]:
        for pp in ps:
            r=g.generate(level,parameters=pp);audits.append(check_record(r));engine.append(engine_case(r,'boundary/'+level+'/'+str(pp)))
    invalid=[('easy',{'a':1,'k':1,'b':2}),('easy',{'a':1,'k':2,'b':49}),('moderate',{'a':2,'k':3,'b':4}),('moderate',{'a':2,'k':2,'b':13}),('moderate',{'a':2,'k':2,'b':-13}),('hard',{'a':7,'k':2,'b':4,'c':3}),('hard',{'a':-7,'k':2,'b':4,'c':3}),('hard',{'a':6,'k':-5,'b':4,'c':1}),('hard',{'a':1,'k':2,'b':0,'c':3}),('hard',{'a':1,'k':2,'b':4,'c':0})]
    for level,pp in invalid:
        try:g.generate(level,parameters=pp)
        except ValueError:pass
        else:raise AssertionError(('guard accepted invalid',level,pp))
    # Actual source bytes: one backslash before alpha/control names; two row breaks.
    assert ord(sources[0][':question/worked-solution'][sources[0][':question/worked-solution'].index('alpha')-1])==92
    # Presentation aliases and equivalent family spellings do not inflate task identity.
    p={'a':2,'k':2,'b':5}
    r1=g.generate_moderate(parameters=p,profile='observed:q-332895');r2=g.generate_moderate(parameters=p,profile='observed:q-332898');r3=g.generate_moderate(parameters=p,profile='observed:q-333168')
    assert r1['question']==r2['question']
    assert r1['question'][':question/id']!=r3['question'][':question/id']
    assert r1['generation']['mathematical_fingerprint']==r3['generation']['mathematical_fingerprint']
    f=A*sp.exp(2*X)+5*X*sp.exp(2*X)
    assert family_equivalent(f,(2*A+3+5*X)*sp.exp(2*X),2)
    assert not family_equivalent(f,5*X*sp.exp(2*X),2)
    assert not family_equivalent(f,f+1,2)
    # Mutation tests prove the independent displayed-math auditor checks actual
    # product inputs, distributed signs, reductions, final families and row sequence.
    mutations=[]
    base=g.generate_hard(parameters={'a':-5,'k':1,'b':15,'c':12})
    for before,after in [(r'\alpha ({e}^{-5x}-5x{e}^{-5x})',r'\alpha ({e}^{-5x}+5x{e}^{-5x})'),('(1-5x+5x)','(1-5x-5x)'),('6\\beta {e}^{x}','5\\beta {e}^{x}'),('(x{e}^{-5x})^{′}','(x{e}^{-4x})^{′}')]:
        changed=copy.deepcopy(base);sol=changed['question'][':question/worked-solution'];assert before in sol,before
        changed['question'][':question/worked-solution']=sol.replace(before,after,1)
        try:check_record(changed)
        except (AssertionError,ValueError):mutations.append(before)
        else:raise AssertionError('mutation was missed')
    # Real grader restriction: preserving the same A coefficient is the normal
    # response form. The complete rescaled family is mathematically equivalent,
    # but the native comparator treats A as an ordinary fixed symbol.
    limitation=engine_case(r1,'documented-native-constant-rescaling-restriction')
    limitation['checks']=[{'submitted':r'(2A+5x)e^{2x}','expected':'rejected','purpose':'documented form-sensitive limitation: equivalent family under A rescaling violates prescribed coefficient A'}]
    engine.append(limitation)
    write('engine-input.json',engine)
    subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-validation.json')],check=True)
    write('source-fidelity.json',fidelity);write('review.json',reviews)
    sections=['# Original captures and generated variants','All raw source evidence is retained, including the incomplete unrated question. Raw replays use exact captured wording. Normal questions prescribe the arbitrary complementary coefficient A for native grading. Hard is authored from the preceding lesson, not an observed hard rating.']
    for c,q in zip(g.CASES,sources):
        sections += ['## Original '+c['source_id']+' ('+('unrated' if c['unrated_authored_assignment'] else c['level'])+')',q[':question/problem'],'Captured answer values: '+json.dumps([a[':answer/value'] for a in q[':question/answer-fields'][0].get(':answer-field/choices',[])]),q.get(':question/worked-solution','**No captured solution or answer; raw replay retains this omission.**')]
    for item in reviews:
        if item['label'].startswith('raw source replay'):continue
        sections += ['## '+item['label'],g.markdown(item['record'])]
    (ROOT/'review.md').write_text('\n\n'.join(sections)+'\n')
    result={'status':'passed','database_writes':0,'source_provenance':g.SOURCE,'source_coverage':{'questions':10,'easy':5,'moderate':4,'unrated':1,'raw_exact_prompts':10,'raw_exact_existing_solutions':9,'raw_exact_existing_solution_denominator':9,'raw_complete_field_shapes':10,'observed_bank_values_matched':10,'observed_bank_values_total':10,'complete_nonempty_banks_matched':9,'complete_nonempty_banks_total':9,'correct_designations_matched':9,'correct_designations_total':9,'missing_original_designations':1,'missing_original_solutions':1,'normal_answer_form_clarifications':10,'normal_missing_answer_solution_level_repairs':1,'normal_existing_solutions_exact':9,'normal_existing_solutions_denominator':9},'authored_hard':{'template':'mixed','lesson_step':17592186230049,'preceding_kp':17592186229163,'prerequisites':[1007,6678,1109],'hard_source_count':0},'independent_checks':{'records':len(audits),'printed_equalities':sum(a['equations'] for a in audits),'formal_derivative_rows':sum(a['derivative_rows'] for a in audits),'random_samples_per_level':30,'scope_rejection_cases':len(invalid),'mutation_failures_detected':len(mutations),'sample_distinct_mathematical_tasks':{l:len(set(r['generation']['mathematical_fingerprint'] for r in samples if r['generation']['level']==l)) for l in ['easy','moderate','hard']}},'native_grader_report':'engine-validation.json','grading_limitation':'Arbitrary-constant rescaling is mathematically family-equivalent but native comparator treats A as fixed. Normal prompt prescribes coefficient A; sum/factored equivalent forms accepted. Raw wording preserved.','plots':'none','review_records':len(reviews),'final_frozen_hashes':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ['layouts.json','source.json','source-cases.json','math_check.py','validate.py','classification.md','template-extraction.md','README.md','review.json','review.md','engine-input.json','engine-validation.json']},'generator_sha256':hashlib.sha256(ROOT.with_suffix('.py').read_bytes()).hexdigest(),'engine_sha256':hashlib.sha256((REPO/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'engine_source_sha256':{n:hashlib.sha256((REPO/'engine/rust'/n).read_bytes()).hexdigest() for n in ['learning.rs','symbolic.rs']},'sympy_version':sp.__version__}
    write('validation.json',result)
    print(json.dumps({k:result[k] for k in ['status','source_coverage','independent_checks']},indent=2))
if __name__=='__main__':main()
