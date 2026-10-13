"""Frozen order generator validation: decoded printed derivatives, full fidelity,
SymPy derivative objects, finite catalogs, strict domains and real field grading.
"""
import hashlib, importlib.util, itertools, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('order_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,value):(HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def printed_orders(text):
    """Independent grammar: strip d fonts, read complete fraction numerator and
    denominator, then count prime glyphs. Uses actual printed strings, no params.
    """
    t=text.replace(r'\text{d}','d')
    out=[]
    for m in re.finditer(r'\\frac\{\{d\}\^\{(\d+)\}y\}\{d\{x\}\^\{(\d+)\}\}|\\frac\{dy\}\{dx\}',t):
        if m[1]:assert m[1]==m[2];out.append((m.start(),int(m[1])))
        else:out.append((m.start(),1))
    for m in re.finditer(r'\{y\}\^\{(\'+|[′″‴])\}',t):
        out.append((m.start(),{'′':1,'″':2,'‴':3}.get(m[1],len(m[1]))))
    assert out, 'no actual displayed derivative parsed'
    orders=[n for _,n in sorted(out)]
    x=sp.Symbol('x');y=sp.Function('y')(x)
    for n in orders:assert sp.Derivative(y,(x,n)).derivative_count==n
    return orders
WORDS={'first':1,'second':2,'third':3,'fourth':4,'fifth':5,'sixth':6,'seventh':7,'eighth':8}
def check_format(s):
    assert s.count('$')%2==0
    stack=0
    for i,c in enumerate(s):
        if c in '{}':
            # Escaped braces are literal glyphs, not grouping.
            prev=0;j=i-1
            while j>=0 and s[j]=='\\':prev+=1;j-=1
            if prev%2:continue
            stack+=1 if c=='{' else -1;assert stack>=0
    assert stack==0
    assert not re.search(r'(?<!\\)(?:\+\-|\-\-)',s)
def value(field):
    return next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1])
def check(r):
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    q=r['question'];p=q[':question/problem'];sol=q[':question/worked-solution'];check_format(p);check_format(sol)
    fields=q[':question/answer-fields']
    for f in fields:
        vals=[a[':answer/value'] for a in f[':answer-field/choices']];assert len(vals)==len(set(vals))
        assert f[':answer-field/correct'][0]==':answer/id';assert sum(a[':answer/id']==f[':answer-field/correct'][1] for a in f[':answer-field/choices'])==1
        if f[':answer-field/type']==':answer-field.type/blank':assert '{{'+f[':answer-field/key']+'}}' in p
    if len(fields)==1:
        orders=printed_orders(p);correct=max(orders);assert sp.Integer(value(fields[0]))==correct
        sorder=re.search(r'which has order \$(\d+)\.\$',sol);assert sorder and int(sorder[1])==correct
        assert int(re.search(r'order of the ODE is \$(\d+)\.\$',sol)[1])==correct
        sds=printed_orders(sol)
        if r['generation']['source_id']=='q-167787':
            assert max(printed_orders(sol.split('$$')[1]))==correct
            assert all(n==correct for n in printed_orders(sol.split('$$')[-1]))
        else:assert all(n==correct for n in sds)
        if r['generation']['authored']:
            assert len(orders)==2
            # Full authored bank independently from displayed equation.
            masked=re.sub(r'\\frac\{.*?\}\{.*?\}\}', '',p)
            # Read the ordinary x exponent from the prompt; fractions' x powers
            # are separately removed by selecting the exponent outside each span.
            matches=[]
            for m in re.finditer(r'\{x\}\^\{(\d+)\}',p):
                if p[m.end():m.end()+2]!='}':matches.append(int(m[1]))
            exponent=max(matches);expected={correct,min(orders),exponent,correct-1,correct+1}
            assert set(map(lambda a:int(a[':answer/value']),fields[0][':answer-field/choices']))==expected
    else:
        target=WORDS[re.search(r'are (\w+)-order',p)[1]]
        rows=re.findall(r'- \*\*(I|II|III)\.\*\* \$(.*?)\$',p);assert len(rows)==3
        sentences=[x for x in sol.split('\n\n') if x.startswith('- Equation')];assert len(sentences)==3
        expected_selected=[]
        for (key,eq),f,s in zip(rows,fields,sentences):
            orders=printed_orders(eq);n=max(orders);assert f[':answer-field/key']==key;assert value(f)==('true' if n==target else 'false')
            assert max(printed_orders(s))==n
            assert (' is not ' in s)==(n!=target)
            if n==target:expected_selected.append(key)
            if r['generation']['authored']:
                if r['generation']['level']=='moderate':assert 1<=n<=3 and len(orders)<=2
                else:assert 4<=n<=8 and len(orders)==4 and r'\frac' in eq and re.search('[′″‴]',eq)
        conclusion=sol.split('Therefore, the correct answer is ')[-1]
        selected=re.findall(r'\b(?:I|II|III)\b',conclusion)
        if 'all three' in conclusion:selected=['I','II','III']
        assert selected==expected_selected
    return r

def native(label,r):
    checks=[]
    for i,f in enumerate(r['question'][':question/answer-fields']):
        if f[':answer-field/type']==':answer-field.type/blank':
            n=value(f)
            for text,expected,purpose in [(n,'accepted','canonical'),(n+'/1','accepted','unreduced quotient'),('sqrt('+str(int(n)**2)+')','accepted','equivalent square root'),(str(int(n)+1),'rejected','wrong order')]:checks.append({'field_index':i,'submitted':text,'expected':expected,'purpose':purpose})
        else:
            for a in f[':answer-field/choices']:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'every owned displayed choice'})
    return {'label':label,'record':r,'checks':checks}

def main():
    review=[];fixtures=[];cases=[];source_log=[];changed=[]
    for sid,q in g.ORIGINALS.items():
        level=q[':question/difficulty'][':db/ident'].split('/')[-1];p=g.source_parameters(sid);r=check(g.generate(level,template=sid,parameters=p,profile='observed'))
        gen=r['question'];assert gen[':question/problem']==q[':question/problem'];assert gen[':question/worked-solution']==q[':question/worked-solution']
        assert set(gen)==set(q)-{':db/id',':question/math-academy-id'}
        options=0
        for f,a in zip(q[':question/answer-fields'],gen[':question/answer-fields']):
            assert f[':answer-field/key']==a[':answer-field/key'];assert f[':answer-field/type'][':db/ident']==a[':answer-field/type']
            assert sorted((x[':answer/value'],x[':answer/type'][':db/ident']) for x in f[':answer-field/choices'])==sorted((x[':answer/value'],x[':answer/type']) for x in a[':answer-field/choices'])
            assert f[':answer-field/correct'][':answer/value']==value(a);options+=len(f[':answer-field/choices'])
        case={'source_id':sid,'template':sid,'level':level,'parameters':p,'bank_profile':'observed'};cases.append(case)
        source_log.append({'source_id':sid,'prompt_exact':True,'solution_exact':True,'attribute_presence_exact':True,'complete_bank_match':True,'matched_options':options,'correct_designations':len(q[':question/answer-fields'])})
        fixtures.append(native('source/'+sid,r));review.append({'label':'Original '+sid+' / exact observed replay / '+level,'record':r})
        # Shift derivatives together, retaining every source solution paragraph.
        delta=1 if max(p['orders'].values())<8 else -1
        varied={'orders':{k:v+delta for k,v in p['orders'].items()}}
        try:v=check(g.generate(level,17,template=sid,parameters=varied,profile='observed'))
        except ValueError:
            # If the source contains first order and order8, an increasing map
            # preserving the eight-order cap can vary an interior component.
            varied={'orders':dict(p['orders'])};ks=list(varied['orders']);varied['orders'][ks[-2]]-=1
            v=check(g.generate(level,17,template=sid,parameters=varied,profile='observed'))
        assert v['question'][':question/problem']!=gen[':question/problem'];assert v['generation']['mathematical_fingerprint']!=r['generation']['mathematical_fingerprint']
        assert len(v['question'][':question/worked-solution'].split('\n\n'))==len(gen[':question/worked-solution'].split('\n\n'))
        changed.append({'source_id':sid,'parameters':varied});review.append({'label':'Generated source-recipe variant '+sid+' / '+level+' / observed evidence profile','record':v});fixtures.append(native('changed/'+sid,v))
    fixed=g.generate('easy',template='q-167787',profile='source_repaired');assert '=f(x).' in fixed['question'][':question/worked-solution'];check(fixed);fixtures.append(native('source RHS prose repair',fixed));review.append({'label':'Generated q-167787 with documented RHS prose repair','record':fixed})
    fingerprints={};instances={};positions=set()
    for level in ('easy','moderate','hard'):
        seen=set()
        for seed in range(400):
            r=check(g.generate(level,seed));seen.add(r['generation']['mathematical_fingerprint'])
            p=r['generation']['parameters'];other=check(g.generate(level,seed+301,parameters=p))
            assert r['question'][':question/id']==other['question'][':question/id'];assert r['generation']['content_fingerprint']==other['generation']['content_fingerprint']
            if level=='easy':
                f=r['question'][':question/answer-fields'][0]
                positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
            if seed<8:fixtures.append(native(level+'/'+str(seed),r))
            if seed<2:review.append({'label':'Generated authored '+level+' example '+str(seed+1),'record':r})
        fingerprints[level]=len(seen);instances[level]=400
    assert positions==set(range(5)), 'radio order must not fix the correct slot'
    # Enumerate actual finite easy and moderate meaningful catalog fingerprints.
    catalogs={}
    tasks=set();count=0
    for n in range(3,8):
        for m in range(1,n-1):
            for e in range(n+2,10):
                for layout in ('left','right'):
                    r=check(g.generate_easy(parameters=dict(n=n,m=m,e=e,layout=layout)));count+=1;tasks.add(r['generation']['mathematical_fingerprint'])
    catalogs['easy']={'explicit_parameter_tuples':count,'semantic_tasks':len(tasks)}
    tasks=set();count=0
    for target in range(1,4):
        for orders in itertools.product(range(1,4),repeat=3):
            for forms in itertools.product(range(3),repeat=3):
                r=check(g.generate_moderate(parameters={'target':target,'orders':list(orders),'forms':list(forms)}));count+=1;tasks.add(r['generation']['mathematical_fingerprint'])
    catalogs['moderate']={'explicit_parameter_tuples':count,'semantic_tasks':len(tasks)}
    # Hard is a bounded finite product, not an unbounded numeric sampler. Distinct
    # full order/power/exponent/layout tuples; no variable/seed aliases counted.
    equation_count=sum((n-2)*4*(10-n)*3 for n in range(4,9))
    catalogs['hard']={'per_equation_structures':equation_count,'three_equation_tasks':5*equation_count**3,'formula':'5 targets * (sum[n=4..8](n−2)*4 powers*(10−n) exponents*3 layouts)^3','enumeration':'factorized; equation structures independently enumerated below'}
    tasks=set()
    for n in range(4,9):
        for m in range(1,n-1):
            for power in range(2,6):
                for exponent in range(n+1,11):
                    for form in range(3):
                        p={'target':4,'orders':[n]*3,'forms':[form]*3,'lower':[m]*3,'powers':[power]*3,'exponents':[exponent]*3};r=check(g.generate_hard(parameters=p));tasks.add(json.dumps(g.semantic_equations(r['question'][':question/problem'])[0],sort_keys=True))
    assert len(tasks)==equation_count;catalogs['hard']['verified_equation_structures']=len(tasks)
    invalid=[('easy',dict(n=2,m=1,e=5,layout='left')),('easy',dict(n=7,m=6,e=9,layout='left')),('easy',dict(n=3,m=1,e=4,layout='left')),('moderate',dict(target=4,orders=[1,2,3],forms=[0,1,2])),('hard',dict(target=4,orders=[3,4,5],forms=[0,1,2],lower=[1,1,1],powers=[2,2,2],exponents=[7,7,7])),('hard',dict(target=4,orders=[4,4,4],forms=[0,1,2],lower=[3,1,1],powers=[2,2,2],exponents=[7,7,7]))]
    for level,p in invalid:
        try:g.generate(level,parameters=p)
        except ValueError:pass
        else:raise AssertionError('invalid accepted '+str(p))
    api_invalid=[dict(level='easy',field_type='checkbox'),dict(level='easy',template='mixed_selection'),dict(level='hard',profile='observed'),dict(level='easy',template='q-95982',parameters={'orders':{'1':2,'2':1}}),dict(level='easy',template='q-95982',parameters={'orders':{'1':1,'2':9}})]
    for kw in api_invalid:
        try:g.generate(**kw)
        except ValueError:pass
        else:raise AssertionError('invalid API accepted')
    # Negative controls: actual equation mismatch and conclusion mismatch must fail.
    negatives=0
    for edit in ('prompt','solution'):
        r=g.generate_easy(parameters=dict(n=4,m=1,e=7,layout='left'))
        key=':question/problem' if edit=='prompt' else ':question/worked-solution';r['question'][key]=r['question'][key].replace('^{4}','^{5}',1)
        try:check(r)
        except AssertionError:negatives+=1
        else:raise AssertionError('negative control accepted')
    ledger=json.loads((HERE/'choice-recipes.json').read_text());assert len(ledger)==73
    captured={a[':answer/id']:(sid,f[':answer-field/key'],a[':answer/value'],a[':answer/id']==f[':answer-field/correct'][':answer/id']) for sid,q in g.ORIGINALS.items() for f in q[':question/answer-fields'] for a in f[':answer-field/choices']}
    assert {x['original_answer_uuid']:(x['source_id'],x['field_key'],x['value'],x['correct']) for x in ledger}==captured
    save('source-cases.json',cases);save('source-fidelity.json',source_log);save('changed-source-parameters.json',changed);save('review.json',review);save('native-input.json',fixtures)
    engine=ROOT/'generate/runs/current/check-engine';proc=subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-report.json')],capture_output=True,text=True);assert proc.returncode==0,proc.stdout+proc.stderr
    native_report=json.loads((HERE/'native-report.json').read_text())
    result={'passed':True,**g.PROVENANCE,'version':g.VERSION,'source_questions':len(cases),'exact_prompts':len(cases),'exact_full_solutions':len(cases),'exact_attribute_presence':len(cases),'complete_banks':len(cases),'matched_options':sum(x['matched_options'] for x in source_log),'correct_designations':sum(x['correct_designations'] for x in source_log),'changed_source_recipes':len(changed),'source_prose_repairs':1,'authored_levels':['easy','moderate','hard'],'random_instances_checked':instances,'sampled_meaningful_tasks':fingerprints,'finite_catalogs':catalogs,'strict_domain_rejections':len(invalid),'api_domain_rejections':len(api_invalid),'radio_correct_positions_verified':sorted(positions),'negative_controls':negatives,'native_grading':{k:native_report[k] for k in ['entry_point','accepted_checks','rejected_checks','documented_unresolved_checks']},'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'unresolved_findings':['Historical scalar radio distractor intent is underdetermined; relative-order catalogs retained only as explicit evidence replay.'],'source_anomalies':['q-167787 prompt RHS f(x), worked solution RHS (1/2)e^x. Order unaffected; raw replay exact, separate repaired prose profile.'],'database_writes':0}
    save('validation.json',result)
    (HERE/'review.md').write_text('Order of an ordinary differential equation — review\n\nSource math basis1356. Correct answers are labeled for author review. Raw replay is evidence-only.\n\n'+'\n\n---\n\n'.join('### '+x['label']+'\n\n'+g.markdown(x['record']) for x in review)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
