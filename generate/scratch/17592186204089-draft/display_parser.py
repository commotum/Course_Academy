"""Independent exact parser for the actual displayed affine question and solution.

No generator helpers and no root QA imports. Only affine TeX supported; unknown
syntax, stages, response layouts, and domains fail closed.
"""
import re
import sympy as sp
LABELS=('I','II','III')

def expression(text,variable):
    text=text.strip().rstrip('.').replace(' ','').replace('&','')
    text=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1)/(\2)',text)
    assert re.fullmatch(r'[0-9xuyzwv+*/()\-]+',text),text
    text=re.sub(r'(\d)([xuyzwv])',r'\1*\2',text)
    value=sp.sympify(text,locals={variable:sp.Symbol(variable,real=True)})
    assert value.free_symbols<= {sp.Symbol(variable,real=True)}
    assert sp.Poly(value,sp.Symbol(variable,real=True)).degree()<=1
    return value

def equation(text,variable):
    parts=text.replace('&','').strip().rstrip('.').split('=');assert len(parts)==2
    return tuple(expression(s,variable) for s in parts)

def read_prompt(text):
    assert text.startswith('Which of the following equations has no solutions?\n\n')
    raw=re.findall(r'\$([^$]*=[^$]*)\$',text);assert len(raw)==3
    labels=re.findall(r'(?:^|\n)(?:- \*\*)?(III|II|I)\.',text);assert labels==list(LABELS),labels
    variable=re.search('[xuyzwv]',raw[0])[0];x=sp.Symbol(variable,real=True)
    equations=[equation(t,variable) for t in raw];rows=[]
    for lhs,rhs in equations:
        values=[lhs.coeff(x),lhs.subs(x,0),rhs.coeff(x),rhs.subs(x,0)]
        assert all(v.is_Integer for v in values);rows.append([int(v) for v in values])
    statuses=[sp.solveset(sp.Eq(lhs,rhs),x,domain=sp.S.Reals) for lhs,rhs in equations]
    return variable,equations,rows,statuses

def selection(text):
    table={'I only':{0},'II only':{1},'III only':{2},'I and II only':{0,1},'I and III only':{0,2},'II and III only':{1,2},'I, II, and III':{0,1,2}}
    assert text in table,text
    return table[text]

def validate(rec):
    q=rec['question'];meta=rec['generation'];variable,equations,rows,statuses=read_prompt(q[':question/problem']);x=sp.Symbol(variable,real=True)
    assert variable==meta['parameters']['variable'] and rows==meta['parameters']['equations']
    assert meta['domain']['domain']=='real numbers'
    no_solutions={i for i,s in enumerate(statuses) if s==sp.S.EmptySet}
    fields=q[':question/answer-fields'];radio=meta['template']=='radio-detailed-scaled'
    assert set(meta['parameters'])==({'variable','equations','label_permutation'} if radio else {'variable','equations'})
    if radio:
        assert len(fields)==1 and fields[0][':answer-field/key']=='selection' and fields[0][':answer-field/type']==':answer-field.type/radio'
        assert q[':question/problem'].count('Select all that apply.')==0
        bank=fields[0][':answer-field/choices'];sets=[selection(a[':answer/value']) for a in bank]
        order=meta['parameters']['label_permutation'];assert len(order)==3 and all(type(i) is int for i in order) and sorted(order)==[0,1,2]
        role_status=[sp.S.EmptySet,None,sp.S.Reals]
        for i,old_index in enumerate(order):
            if old_index==1:assert isinstance(statuses[i],sp.FiniteSet) and len(statuses[i])==1
            else:assert statuses[i]==role_status[old_index]
        source_subsets=({0},{0,2},{0,1},{0,1,2},{1,2})
        wanted=[{new_index for new_index,old_index in enumerate(order) if old_index in old_subset} for old_subset in source_subsets]
        assert sets==wanted and len({tuple(sorted(s)) for s in sets})==5
        ref=fields[0][':answer-field/correct'];assert next(sets[i] for i,a in enumerate(bank) if a[':answer/id']==ref[1])==no_solutions
    else:
        assert [f[':answer-field/key'] for f in fields]==list(LABELS)
        assert q[':question/problem'].count('Select all that apply.')==1
        for i,f in enumerate(fields):
            assert f[':answer-field/type']==':answer-field.type/checkbox';bank=f[':answer-field/choices'];assert [a[':answer/value'] for a in bank]==['false','true']
            assert next(a[':answer/value'] for a in bank if a[':answer/id']==f[':answer-field/correct'][1])==('true' if i in no_solutions else 'false')
    ids=[q[':question/id']]
    for f in fields:
        ids+=[f[':answer-field/id']]+[a[':answer/id'] for a in f[':answer-field/choices']]
        assert all(a[':answer/type']==':answer.type/text' for a in f[':answer-field/choices'])
        assert f[':answer-field/correct'][0]==':answer/id'
    assert len(ids)==len(set(ids))
    solution=q[':question/worked-solution'];stages=0
    if meta['template']=='summary-spaced':
        assert solution.startswith('The equations reduce respectively to ')
        parts=solution.split('respectively to ',1)[1].split('. Only',1)[0].replace('$','').replace(', and ', ', ').split(', ');assert len(parts)==3
        for raw,status,(a,b,c,d) in zip(parts,statuses,rows):
            if status==sp.S.Reals:assert raw=='an identity'
            else:
                lhs,rhs=equation(raw,variable)
                assert (lhs,rhs)==(sp.Integer(b),sp.Integer(d)) if status==sp.S.EmptySet else (lhs,rhs)==(x,sp.Rational(d-b,a-c))
            stages+=1
        ordinal=('first','second','third')[next(iter(no_solutions))];assert solution.endswith('Only the '+ordinal+' has no solutions.')
    else:
        displays=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S);assert len(displays)==3
        for index,(display,(lhs,rhs),(a,b,c,d),status) in enumerate(zip(displays,equations,rows,statuses)):
            expected=[(lhs,rhs)]
            if a==c:expected += [(lhs-a*x,rhs-a*x),(sp.Integer(b),sp.Integer(d))]
            else:
                expected += [(lhs-c*x-b,rhs-c*x-b)]
                if a-c!=1:expected += [((a-c)*x,sp.Integer(d-b))]
                expected += [(x,sp.Rational(d-b,a-c))]
            actual=[equation(t,variable) for t in display.split(r'\\')];assert len(actual)==len(expected)
            for pair,wanted in zip(actual,expected):assert all(sp.simplify(u-v)==0 for u,v in zip(pair,wanted)),(pair,wanted);stages+=1
            if status==sp.S.EmptySet:assert f'This equation is false for all values of ${variable}.$' in solution
            elif status==sp.S.Reals:assert f'This equation is true for all values of ${variable}.$' in solution
        conclusion=re.search(r'Therefore, the correct answer is "(.*?)\."$',solution);assert conclusion and selection(conclusion[1])==no_solutions
        # Every prose repeated equation and unique solution is checked from display.
        repeats=re.findall(r'Therefore, the equation \$([^$]*=[^$]*)\$ (has no solutions|has the unique solution \$([^$]*)\$)',solution)
        expected_nonidentities=[(pair,status) for pair,status in zip(equations,statuses) if status!=sp.S.Reals];assert len(repeats)==len(expected_nonidentities)
        for match,(pair,status) in zip(repeats,expected_nonidentities):
            assert equation(match[0],variable)==pair
            if status==sp.S.EmptySet:assert match[1]=='has no solutions'
            else:assert sp.solveset(sp.Eq(*equation(match[2],variable)),x,domain=sp.S.Reals)==status
    return {'equations':3,'displayed_stages':stages,'banks':len(fields),'status_pattern':''.join('N' if s==sp.S.EmptySet else 'I' if s==sp.S.Reals else 'U' for s in statuses)}
