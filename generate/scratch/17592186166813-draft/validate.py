"""Frozen order generator validation: decoded printed derivatives, full fidelity,
SymPy derivative objects, finite catalogs, strict domains and real field grading.
"""
import hashlib, importlib.util, itertools, json, math, re, subprocess, sys
from pathlib import Path
import sympy as sp
from functools import lru_cache
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
HERE=Path(__file__).parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('order_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
from scripts.question_capture.math_format import validate_generated_record,validate_prose,normalize_prose
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

@lru_cache(maxsize=None)
def actual_equation(eq):
    """Read the whole printed equation to a second symbolic model. Derivatives
    are independent jet coordinates D1–D8; x/y are the one ordinary variable and
    its dependent value. This rejects variable-binding damage, unsupported PDE
    operators, zero highest coefficients and algebraically cancelled derivatives.
    """
    raw=eq.replace(r'\text{d}','d')
    pattern=r'\\frac\{\{d\}\^\{(\d+)\}y\}\{d\{x\}\^\{(\d+)\}\}|\\frac\{dy\}\{dx\}|\{y\}\^\{(\'+|[′″‴])\}'
    def slot(m):
        if m[1]:assert m[1]==m[2];n=int(m[1])
        elif m[3]:n={'′':1,'″':2,'‴':3}.get(m[3],len(m[3]))
        else:n=1
        return ' D'+str(n)+' '
    text=re.sub(pattern,slot,raw)
    text=text.replace(r'\operatorname{sin}⁡x','sin(x)')
    # Convert sqrt's complete braced argument before dropping grouping braces.
    while r'\sqrt{' in text:
        start=text.index(r'\sqrt{');begin=start+5;depth=1;end=begin+1
        while depth:
            assert end<len(text)
            depth+=(text[end]=='{')-(text[end]=='}');end+=1
        text=text[:start]+'sqrt('+text[begin+1:end-1]+')'+text[end:]
    assert '\\' not in text,'unparsed operator or derivative variable binding'
    text=text.replace('{','(').replace('}',')').replace('⁡','')
    assert text.count('=')==1
    x,y=sp.symbols('x y');ds={f'D{i}':sp.Symbol(f'D{i}') for i in range(1,9)}
    env={**ds,'x':x,'y':y,'e':sp.E,'f':sp.Function('f'),'sin':sp.sin,'sqrt':sp.sqrt}
    left,right=[parse_expr(side,local_dict=env,transformations=standard_transformations+(implicit_multiplication_application,convert_xor)) for side in text.split('=')]
    residual=sp.simplify(left-right);assert residual.free_symbols <= {x,y,*ds.values()}
    order=max(printed_orders(eq));assert sp.simplify(sp.diff(residual,ds['D'+str(order)]))!=0,'highest derivative cancels or has zero coefficient'
    return {'order':order,'left':left,'right':right,'residual':residual,'x':x,'y':y}

def independent_source_bank(sid,eq):
    model=actual_equation(eq);orders=sorted(set(printed_orders(eq)));h=orders[-1];lo=orders[0];next_high=orders[-2] if len(orders)>1 else h
    powers=model['left'].atoms(sp.Pow)|model['right'].atoms(sp.Pow)
    xp=[int(p.exp) for p in powers if p.base==model['x'] and p.exp.is_Integer]
    yp=[int(p.exp) for p in powers if p.base==model['y'] and p.exp.is_Integer]
    if sid=='q-95982':expected=[max(yp),lo,h,max(xp),max(yp)+1]
    elif sid=='q-118780':expected=[h+1,next_high-1,h,min(xp),next_high]
    elif sid=='q-118779':expected=[h,max(xp),h+1,lo,lo+1]
    elif sid=='q-118781':expected=[h,lo,min(yp),max(yp)+1,max(yp)]
    elif sid=='q-96662':expected=[max(yp),1,lo,h,h+1]
    elif sid=='q-96663':expected=[lo,h+1,next_high,h,next_high+1]
    elif sid=='q-167787':expected=[h]
    else:raise AssertionError('unknown scalar profile')
    return set(map(str,expected))

def read_feedback(text):
    bare=re.findall(r"\by('+)(?!')",text)
    orders=[len(s) for s in bare]
    if '$' in text:orders+=printed_orders(text)
    assert orders,'feedback derivative reference missing'
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
    validate_generated_record(r)
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    q=r['question'];p=q[':question/problem'];sol=q[':question/worked-solution'];check_format(p);check_format(sol)
    fields=q[':question/answer-fields']
    for f in fields:
        vals=[a[':answer/value'] for a in f[':answer-field/choices']];assert len(vals)==len(set(vals))
        assert f[':answer-field/correct'][0]==':answer/id';assert sum(a[':answer/id']==f[':answer-field/correct'][1] for a in f[':answer-field/choices'])==1
        if f[':answer-field/type']==':answer-field.type/blank':assert '{{'+f[':answer-field/key']+'}}' in p
        sid=r['generation']['source_id']
        if sid:
            source_field=next(x for x in g.ORIGINALS[sid][':question/answer-fields'] if x[':answer-field/key']==f[':answer-field/key'])
            for a in f[':answer-field/choices']:
                source_answer=next((x for x in source_field[':answer-field/choices'] if x[':answer/value']==a[':answer/value']),None)
                expected_feedback=source_answer is not None and ':answer/feedback' in source_answer
                assert (':answer/feedback' in a)==expected_feedback,'source feedback attribute presence mismatch'
    if len(fields)==1:
        orders=printed_orders(p);correct=max(orders);assert sp.Integer(value(fields[0]))==correct
        eq=p.split('$$')[1] if '$$' in p else p.split('$')[1].rstrip('?')
        assert actual_equation(eq)['order']==correct
        sorder=re.search(r'which has order \$(\d+)\.\$',sol);assert sorder and int(sorder[1])==correct
        assert int(re.search(r'order of the ODE is \$(\d+)\.\$',sol)[1])==correct
        sds=printed_orders(sol)
        if r['generation']['source_id']=='q-167787':
            assert max(printed_orders(sol.split('$$')[1]))==correct
            assert all(n==correct for n in printed_orders(sol.split('$$')[-1]))
        else:assert all(n==correct for n in sds)
        if r['generation']['source_id']:
            assert {a[':answer/value'] for a in fields[0][':answer-field/choices']}==independent_source_bank(r['generation']['source_id'],eq)
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
        opening=sol.split('\n\n')[0]
        assert WORDS[re.search(r'is of (\w+)-order',opening)[1]]==target
        assert printed_orders(opening)==[target]
        rows=re.findall(r'- \*\*(I|II|III)\.\*\* \$(.*?)\$',p);assert len(rows)==3
        if r['generation']['authored']:
            assert len({eq for _,eq in rows})==3,'authored equations must be distinct'
            assert len({json.dumps(e,sort_keys=True) for e in g.semantic_equations(p)})==3,'assessed shapes must be distinct'
            assert not re.search(r'\ba eighth-order\b',sol)
            assert not re.search(r'\ban (?!eighth-order)',sol)
        sentences=[x for x in sol.split('\n\n') if x.startswith('- Equation')];assert len(sentences)==3
        expected_selected=[]
        for (key,eq),f,s in zip(rows,fields,sentences):
            orders=printed_orders(eq);n=max(orders);assert f[':answer-field/key']==key;assert value(f)==('true' if n==target else 'false')
            assert actual_equation(eq)['order']==n
            assert max(printed_orders(s))==n
            assert (' is not ' in s)==(n!=target)
            named_target=re.search(r' is (?:not )?(?:also )?an? (\w+)-order',s)[1];assert WORDS[named_target]==target
            if n!=target:assert WORDS[re.search(r'so this is an? (\w+)-order',s)[1]]==n
            if n==target:expected_selected.append(key)
            for answer in f[':answer-field/choices']:
                if ':answer/feedback' in answer:
                    text=answer[':answer/feedback'];validate_prose(text);assert normalize_prose(text)==text
                    assert text.startswith('Equation '+key+' contains ')
                    assert all(k==n for k in read_feedback(text))
                    if 'highest derivative is' in text:
                        ordinal=re.search(r'highest derivative is (\w+) order',text)[1];assert WORDS[ordinal]==n
                    if key=='II':assert 'The factor y^5 does not change the differential order.' in text
                    if key=='III':assert 'The square root does not change the differential order.' in text
            if r['generation']['authored']:
                params=r['generation']['parameters'];i=('I','II','III').index(key)
                assert n==params['orders'][i]
                model=actual_equation(eq);x,y=model['x'],model['y'];dn=sp.Symbol('D'+str(n));d1=sp.Symbol('D1');form=params['forms'][i]
                if r['generation']['level']=='moderate':
                    assert 1<=n<=3 and len(orders)<=2
                    expected=[(dn+3*x*d1,x**5*y),(sp.sqrt(dn+x),3*y**4),(dn**2+x*d1,y**5)][form]
                else:
                    assert 4<=n<=8 and len(orders)==4 and r'\frac' in eq and re.search('[′″‴]',eq)
                    m,power,e=(params[name][i] for name in ('lower','powers','exponents'))
                    a=sp.Symbol('D'+str(m))*dn**power;b=x**e*d1;c=y*sp.Symbol('D'+str(m+1))
                    expected=[(a+b,c),(a,b+c),(b+c,a)][form]
                assert sp.simplify(model['left']-expected[0])==0 and sp.simplify(model['right']-expected[1])==0,'declared joint slots must match printed equation'
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

def permutation_check(r,level):
    """Permute every joint equation component together; canonical presentation,
    all owned fields/banks, task/content IDs and parameter metadata must agree.
    """
    p=r['generation']['parameters'];checked=0
    for permutation in itertools.permutations(range(3)):
        permuted={name:([value[i] for i in permutation] if isinstance(value,list) else value) for name,value in p.items()}
        other=check(g.generate(level,r['generation']['seed'],parameters=permuted))
        assert other['question']==r['question'],'parallel equation permutation changed displayed content or owned bank'
        assert other['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
        assert other['generation']['content_fingerprint']==r['generation']['content_fingerprint']
        assert other['generation']['parameters']==p,'joint canonical metadata not stable'
        checked+=1
    return checked

def main():
    review=[];fixtures=[];cases=[];source_log=[];changed=[];feedback_matches=0;attribute_matches=0
    for sid,q in g.ORIGINALS.items():
        level=q[':question/difficulty'][':db/ident'].split('/')[-1];p=g.source_parameters(sid);r=check(g.generate(level,template=sid,parameters=p,profile='observed'))
        gen=r['question'];assert gen[':question/problem']==q[':question/problem'];assert gen[':question/worked-solution']==q[':question/worked-solution']
        assert set(gen)==set(q)-{':db/id',':question/math-academy-id'}
        options=0
        for f,a in zip(q[':question/answer-fields'],gen[':question/answer-fields']):
            assert set(a)==set(f)-{':db/id'}
            assert f[':answer-field/key']==a[':answer-field/key'];assert f[':answer-field/type'][':db/ident']==a[':answer-field/type']
            assert sorted((x[':answer/value'],x[':answer/type'][':db/ident']) for x in f[':answer-field/choices'])==sorted((x[':answer/value'],x[':answer/type']) for x in a[':answer-field/choices'])
            assert f[':answer-field/correct'][':answer/value']==value(a);options+=len(f[':answer-field/choices'])
            for old,new in zip(sorted(f[':answer-field/choices'],key=lambda x:x[':answer/value']),sorted(a[':answer-field/choices'],key=lambda x:x[':answer/value'])):
                assert set(new)==set(old)-{':db/id'}
                assert old.get(':answer/feedback')==new.get(':answer/feedback');attribute_matches+=1
                if ':answer/feedback' in old:feedback_matches+=1
        case={'source_id':sid,'template':sid,'level':level,'parameters':p,'bank_profile':'observed'};cases.append(case)
        source_log.append({'source_id':sid,'prompt_exact':True,'solution_exact':True,'attribute_presence_exact':True,'complete_bank_match':True,'matched_options':options,'correct_designations':len(q[':question/answer-fields'])})
        fixtures.append(native('source/'+sid,r));review.append({'label':'Original '+sid+' / exact observed replay / '+level,'record':r})
        # Enumerate complete eligible maps in QA; rejected complete catalogs are
        # not repaired by replacing individual choices. Explicit API never resamples.
        found=None
        for values in itertools.combinations(range(1,9),len(p['orders'])):
            varied={'orders':dict(zip(p['orders'],values))}
            if varied==p:continue
            try:v=check(g.generate(level,17,template=sid,parameters=varied,profile='observed'))
            except ValueError:continue
            found=varied;break
        assert found is not None,'no eligible changed source instance';varied=found
        assert v['question'][':question/problem']!=gen[':question/problem'];assert v['generation']['mathematical_fingerprint']!=r['generation']['mathematical_fingerprint']
        assert len(v['question'][':question/worked-solution'].split('\n\n'))==len(gen[':question/worked-solution'].split('\n\n'))
        changed.append({'source_id':sid,'parameters':varied});review.append({'label':'Generated source-recipe variant '+sid+' / '+level+' / observed evidence profile','record':v});fixtures.append(native('changed/'+sid,v))
    fixed=g.generate('easy',template='q-167787',profile='source_repaired');assert '=f(x).' in fixed['question'][':question/worked-solution'];check(fixed);fixtures.append(native('source RHS prose repair',fixed));review.append({'label':'Generated q-167787 with documented RHS prose repair','record':fixed})
    source_domains={};feedback_changed=0
    for sid,q in g.ORIGINALS.items():
        level=q[':question/difficulty'][':db/ident'].split('/')[-1];keys=list(g.source_parameters(sid)['orders']);accepted=rejected=0
        for values in itertools.combinations(range(1,9),len(keys)):
            p={'orders':dict(zip(keys,values))}
            try:r=g.generate(level,template=sid,parameters=p)
            except ValueError as error:
                assert 'catalog invalid' in str(error);rejected+=1;continue
            check(r);accepted+=1
            if sid=='q-96676':
                fixtures.append(native('feedback slot map/'+str(values),r))
                feedback_changed+=sum(':answer/feedback' in a for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices'])
                if values in [(2,3),(3,4),(4,8)]:review.append({'label':'Generated q-96676 complete feedback operand slots '+str(values),'record':r})
        source_domains[sid]={'eligible_maps':accepted,'whole_catalog_rejections':rejected,'considered_maps':accepted+rejected}
    fingerprints={};instances={};positions=set();slot_coverage={};permutation_checks={'moderate':0,'hard':0}
    for level in ('easy','moderate','hard'):
        seen=set();covered={}
        for seed in range(400):
            r=check(g.generate(level,seed));seen.add(r['generation']['mathematical_fingerprint'])
            p=r['generation']['parameters'];other=check(g.generate(level,seed+301,parameters=p))
            for name,parameter in p.items():
                if isinstance(parameter,list):
                    for i,item in enumerate(parameter):covered.setdefault(name+'['+str(i)+']',set()).add(item)
                else:covered.setdefault(name,set()).add(parameter)
            assert r['question'][':question/id']==other['question'][':question/id'];assert r['generation']['content_fingerprint']==other['generation']['content_fingerprint']
            if level=='easy':
                f=r['question'][':question/answer-fields'][0]
                positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
            if seed<8:fixtures.append(native(level+'/'+str(seed),r))
            if level=='hard' and seed<32:permutation_checks['hard']+=permutation_check(r,level)
            if seed<2:review.append({'label':'Generated authored '+level+' example '+str(seed+1),'record':r})
        fingerprints[level]=len(seen);instances[level]=400;slot_coverage[level]={k:sorted(v) for k,v in covered.items()}
        if level=='easy':assert covered['n']==set(range(3,8)) and covered['layout']=={'left','right'}
        else:
            assert covered['target']==set(range(4,9) if level=='hard' else range(1,4))
            # Labels are canonical sorting positions, not separate assessed roles.
            # Report each position but require coverage over the unordered pool.
            aggregate=lambda name:set.union(*(covered[name+'['+str(i)+']'] for i in range(3)))
            assert aggregate('orders')==set(range(4,9) if level=='hard' else range(1,4))
            assert aggregate('forms')==set(range(3))
            if level=='hard':assert aggregate('powers')==set(range(2,6))
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
    moderate_shapes=list(itertools.product(range(1,4),range(3)))
    for target in range(1,4):
        for shapes in itertools.combinations(moderate_shapes,3):
            r=check(g.generate_moderate(parameters={'target':target,'orders':[s[0] for s in shapes],'forms':[s[1] for s in shapes]}));count+=1;tasks.add(r['generation']['mathematical_fingerprint']);permutation_checks['moderate']+=permutation_check(r,'moderate')
    assert count==len(tasks)==3*math.comb(9,3)==252
    catalogs['moderate']={'per_equation_structures':9,'unordered_distinct_equation_sets':math.comb(9,3),'explicit_canonical_parameter_tuples':count,'semantic_tasks':len(tasks),'formula':'3 targets * C(9 distinct equation shapes,3); permutations excluded; repeated shapes rejected'}
    # Hard is a bounded finite product, not an unbounded numeric sampler. Distinct
    # full order/power/exponent/layout tuples; no variable/seed aliases counted.
    equation_count=sum((n-2)*4*(10-n)*3 for n in range(4,9))
    catalogs['hard']={'per_equation_structures':equation_count,'unordered_distinct_equation_sets':math.comb(equation_count,3),'three_equation_tasks':5*math.comb(equation_count,3),'formula':'5 targets * C(sum[n=4..8](n−2)*4 powers*(10−n) exponents*3 layouts,3); distinct shapes; permutations excluded','enumeration':'factorized; each equation shape checked with two distinct eligible companions'}
    hard_shapes=[(n,form,m,power,e) for n in range(4,9) for form in range(3) for m in range(1,n-1) for power in range(2,6) for e in range(n+1,11)]
    tasks=set()
    for n in range(4,9):
        for m in range(1,n-1):
            for power in range(2,6):
                for exponent in range(n+1,11):
                    for form in range(3):
                        shape=(n,form,m,power,exponent);companions=[x for x in hard_shapes if x!=shape][:2];shapes=sorted([shape,*companions])
                        p={'target':4,'orders':[s[0] for s in shapes],'forms':[s[1] for s in shapes],'lower':[s[2] for s in shapes],'powers':[s[3] for s in shapes],'exponents':[s[4] for s in shapes]}
                        r=check(g.generate_hard(parameters=p));tasks.add(json.dumps(g.semantic_equations(r['question'][':question/problem'])[shapes.index(shape)],sort_keys=True))
    assert len(tasks)==equation_count;catalogs['hard']['verified_equation_structures']=len(tasks)
    invalid=[('easy',dict(n=2,m=1,e=5,layout='left')),('easy',dict(n=7,m=6,e=9,layout='left')),('easy',dict(n=3,m=1,e=4,layout='left')),('moderate',dict(target=4,orders=[1,2,3],forms=[0,1,2])),('hard',dict(target=4,orders=[3,4,5],forms=[0,1,2],lower=[1,1,1],powers=[2,2,2],exponents=[7,7,7])),('hard',dict(target=4,orders=[4,4,4],forms=[0,1,2],lower=[3,1,1],powers=[2,2,2],exponents=[7,7,7]))]
    duplicate_inputs=[('moderate',dict(target=1,orders=[1,1,1],forms=[0,0,0])),('moderate',dict(target=2,orders=[1,1,2],forms=[0,0,2])),('hard',dict(target=4,orders=[4,4,4],forms=[0,0,0],lower=[1,1,1],powers=[2,2,2],exponents=[5,5,5])),('hard',dict(target=4,orders=[4,4,5],forms=[0,0,2],lower=[1,1,2],powers=[2,2,3],exponents=[5,5,8]))]
    for level,p in duplicate_inputs:
        try:g.generate(level,parameters=p)
        except ValueError as error:assert 'three distinct assessed equation shapes' in str(error)
        else:raise AssertionError('repeated equation accepted')
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
    for mutation in ('zero_highest','cancel_highest','wrong_binding','pde','stale_feedback','drop_feedback','wrong_feedback_factor'):
        if 'feedback' in mutation:
            r=g.generate_moderate(template='q-96676')
            if mutation=='stale_feedback':r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/feedback']=r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/feedback'].replace("y''","y'''")
            elif mutation=='drop_feedback':del r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/feedback']
            else:r['question'][':question/answer-fields'][1][':answer-field/choices'][0][':answer/feedback']=r['question'][':question/answer-fields'][1][':answer-field/choices'][0][':answer/feedback'].replace('y^5','y^6')
        else:
            r=g.generate_easy(parameters=dict(n=4,m=1,e=7,layout='left'));p=r['question'][':question/problem'];component=r'y\frac{{\text{d}}^{4}y}{\text{d}{x}^{4}}'
            if mutation=='zero_highest':p=p.replace(component,component.replace('y\\frac','0\\frac'))
            elif mutation=='cancel_highest':p=p.replace('={x}^{7}', '-'+component+'={x}^{7}')
            elif mutation=='wrong_binding':p=p.replace(r'\text{d}{x}^{4}',r'\text{d}{t}^{4}')
            else:p=p.replace(r'\text{d}',r'\partial')
            r['question'][':question/problem']=p
        try:check(r)
        except (AssertionError,ValueError):negatives+=1
        else:raise AssertionError('mutation accepted '+mutation)
    changed_targets=[]
    for level,orders in [('moderate',[1,2,3]),('hard',[4,5,6])]:
        base={'target':orders[0],'orders':orders,'forms':[0,1,2]}
        if level=='hard':base.update(lower=[1,1,1],powers=[2,2,2],exponents=[8,8,8])
        a=check(g.generate(level,parameters=base));other=dict(base,target=orders[1]);b=check(g.generate(level,parameters=other))
        rows=lambda r:re.findall(r'- \*\*(?:I|II|III)\.\*\* \$(.*?)\$',r['question'][':question/problem'])
        assert rows(a)==rows(b),'target-only test must hold every equation fixed'
        assert [value(f) for f in a['question'][':question/answer-fields']]==['true','false','false']
        assert [value(f) for f in b['question'][':question/answer-fields']]==['false','true','false']
        assert a['generation']['mathematical_fingerprint']!=b['generation']['mathematical_fingerprint']
        mutated=g.generate(level,parameters=other);mutated['question'][':question/worked-solution']=a['question'][':question/worked-solution']
        try:check(mutated)
        except AssertionError:negatives+=1
        else:raise AssertionError('stale target solution accepted')
        changed_targets.append({'level':level,'parameters_before':base,'parameters_after':other,'equations_held_fixed':True});review.extend([{'label':'Generated '+level+' target-only baseline','record':a},{'label':'Generated '+level+' target-only changed target','record':b}]);fixtures.extend([native(level+' fixed equations first target',a),native(level+' fixed equations changed target',b)])
    article_checks=0
    for target in (7,8):
        p={'target':target,'orders':[7,8,8],'forms':[0,1,2],'lower':[1,2,3],'powers':[2,3,4],'exponents':[9,10,9]}
        r=check(g.generate_hard(parameters=p));assert 'an eighth-order' in r['question'][':question/worked-solution'];article_checks+=1
        review.append({'label':'Generated authored hard article check / target '+str(target),'record':r});fixtures.append(native('hard eighth-order article / target '+str(target),r))
        mutated=g.generate_hard(parameters=p);mutated['question'][':question/worked-solution']=mutated['question'][':question/worked-solution'].replace('an eighth-order','a eighth-order',1)
        try:check(mutated)
        except AssertionError:negatives+=1
        else:raise AssertionError('wrong eighth-order article accepted')
    # Feedback participates in content identity; changing a comment in an in-memory
    # source fixture leaves mathematical identity fixed. Restore immediately.
    source_choice=g.ORIGINALS['q-96676'][':question/answer-fields'][0][':answer-field/choices'][0];original_feedback=source_choice[':answer/feedback']
    a=g.generate_moderate(template='q-96676')
    try:
        source_choice[':answer/feedback']=original_feedback+' Additional note.';b=g.generate_moderate(template='q-96676')
        assert a['question'][':question/id']!=b['question'][':question/id'];assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
    finally:source_choice[':answer/feedback']=original_feedback
    ledger=json.loads((HERE/'choice-recipes.json').read_text());assert len(ledger)==73
    captured={a[':answer/id']:(sid,f[':answer-field/key'],a[':answer/value'],a[':answer/id']==f[':answer-field/correct'][':answer/id']) for sid,q in g.ORIGINALS.items() for f in q[':question/answer-fields'] for a in f[':answer-field/choices']}
    assert {x['original_answer_uuid']:(x['source_id'],x['field_key'],x['value'],x['correct']) for x in ledger}==captured
    assert (HERE/'source.json').read_bytes()==(ROOT/'generate/runs/current/refresh-2026-10-14/sources/17592186166813.json').read_bytes()
    inventory=json.loads((HERE/'independent-inventory.json').read_text());captured_independent=[q for q in g.SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q]
    assert inventory['basis']==g.PROVENANCE['basis'] and inventory['lineage']==g.PROVENANCE['lineage'];assert [x['record'] for x in inventory['questions']]==captured_independent
    assert all(x['role']=='independently authored inventory' and x['relationship_to_source_templates'] for x in inventory['questions'])
    baseline=json.loads((HERE/'registered-baseline.json').read_text());assert all(Path(p).is_file() and hashlib.sha256(Path(p).read_bytes()).hexdigest()==digest for p,digest in baseline['files'].items())
    base=Path(baseline['script']).with_suffix('');assert {str(p) for p in base.rglob('*') if p.is_file()}==set(baseline['files'])-{baseline['script']}
    assert sorted(str(p) for p in base.rglob('*') if p.is_dir())==baseline['directories']
    save('source-cases.json',cases);save('source-fidelity.json',source_log);save('changed-source-parameters.json',changed);save('review.json',review);save('native-input.json',fixtures)
    engine=ROOT/'generate/runs/current/check-engine';proc=subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-report.json')],capture_output=True,text=True);assert proc.returncode==0,proc.stdout+proc.stderr
    native_report=json.loads((HERE/'native-report.json').read_text())
    result={'passed':True,**g.PROVENANCE,'version':g.VERSION,'source_questions':len(cases),'matched_feedback':feedback_matches,'feedback_total':6,'answer_attribute_presence_matches':attribute_matches,'feedback_operand_checks':feedback_changed,'source_profile_domains':source_domains,'sampled_slot_coverage':slot_coverage,'changed_target_cases':changed_targets,'symbolic_equation_readback':{'unique_equations':actual_equation.cache_info().currsize,'rejects':'zero/cancelled highest derivative, foreign bound variable, unsupported derivative/PDE operator'},'registered_baseline_unchanged':True,'exact_prompts':len(cases),'exact_full_solutions':len(cases),'exact_attribute_presence':len(cases),'complete_banks':len(cases),'matched_options':sum(x['matched_options'] for x in source_log),'correct_designations':sum(x['correct_designations'] for x in source_log),'changed_source_recipes':len(changed),'source_prose_repairs':1,'authored_levels':['easy','moderate','hard'],'random_instances_checked':instances,'sampled_meaningful_tasks':fingerprints,'finite_catalogs':catalogs,'strict_domain_rejections':len(invalid),'api_domain_rejections':len(api_invalid),'radio_correct_positions_verified':sorted(positions),'negative_controls':negatives,'duplicate_equation_input_rejections':len(duplicate_inputs),'parallel_equation_permutation_checks':permutation_checks,'eighth_order_article_checks':article_checks,'canonicalization_policy':'three distinct assessed equation shapes; joint tuples sorted before presentation, metadata and identity; source order untouched','native_grading':{k:native_report[k] for k in ['entry_point','accepted_checks','rejected_checks','documented_unresolved_checks']},'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'unresolved_findings':['Historical scalar radio distractor intent is underdetermined; displayed-component catalogs retained only as explicit evidence replay; no recovered historical-error-intent claim.'],'source_anomalies':['q-167787 prompt RHS f(x), worked solution RHS (1/2)e^x. Order unaffected; raw replay exact, separate repaired prose profile.'],'database_writes':0}
    save('validation.json',result)
    (HERE/'review.md').write_text('Order of an ordinary differential equation — review\n\nSource math basis2275. Correct answers are labeled for author review. Raw replay is evidence-only.\n\n'+'\n\n---\n\n'.join('### '+x['label']+'\n\n'+g.markdown(x['record']) for x in review)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
