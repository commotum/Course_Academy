"""Verify the refreshed captured banks and complete worked arithmetic independently."""
import copy, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('validation',H/'validate.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
g=v.g

def parameters(q):
    t=q[':question/problem']; target=re.search(r'eliminate the variable \$([a-z])',t)[1]
    if '\\begin{aligned}' in t:
        block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',t,re.S)[1]
        rows=[v.equation(z) for z in block.split('\\\\')]
    else:rows=v.printed_system({'question':q})
    symbols=set().union(*(a.free_symbols for a,b in rows));x=sp.Symbol(target);assert x in symbols and len(symbols)==2
    y=next(z for z in symbols if z!=x);p={'variables':str(x)+str(y)}
    for i,(l,r) in enumerate(rows,1):
        assert l==l.coeff(x)*x+l.coeff(y)*y and r.is_Integer
        for key,z in [('a',l.coeff(x)),('b',l.coeff(y)),('c',r)]:assert z.is_Integer;p[key+str(i)]=int(z)
    return p

def fingerprint(q):
    p=parameters(q);return g.digest([abs(p['a1']),p['a2']*(1 if p['a1']>0 else -1)])

def projected(q):
    q=copy.deepcopy(q)
    if ':question/difficulty' in q:q[':question/difficulty']=q[':question/difficulty'][':db/ident']
    for f in q.get(':question/answer-fields',[]):
        f[':answer-field/type']=f[':answer-field/type'][':db/ident']
        for a in f[':answer-field/choices']:a[':answer/type']=a[':answer/type'][':db/ident']
        if ':answer-field/correct' in f:f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
    return q

def source_check(q):
    p=parameters(q);x,y=map(sp.Symbol,p['variables']);row,m=g.operation(p)
    fields={f[':answer-field/key']:f for f in q[':question/answer-fields']}
    vals=[sp.Rational(a[':answer/value']) for a in fields['field-2'][':answer-field/choices']]
    assert len(vals)==4 and len(set(vals))==4 and g.eligible(p,vals)==(row,m)
    assert {a[':answer/value'] for a in fields['field-1'][':answer-field/choices']}=={'first','second'}
    # Full observed profile replay, with an explicit unresolved distractor interpretation.
    mid=q[':question/math-academy-id']
    if mid=='q-210858':bank=[p['b2'],-p['a2'],p['a2'],-p['b2']]
    elif mid=='q-210859':bank=[p['b1'],-p['a1'],p['a1'],-p['b1']]
    else:assert mid=='q-238035';bank=[m,-m,abs(m)+1,-abs(m)-1]
    assert sorted(vals)==sorted(bank)
    if ':question/difficulty' not in q:return {'source_id':mid,'complete':False,'bank_choices_matched':6,'ineligible':'unrated; missing correct references and worked solution'}
    for key,correct in [('field-1',['first','second'][row]),('field-2',str(m))]:
        assert fields[key][':answer-field/correct'][':answer/value']==correct
        assert fields[key][':answer-field/correct'][':answer/id'] in {a[':answer/id'] for a in fields[key][':answer-field/choices']}
    # Independently read each rendered distributed, grouped, collected and solved row.
    blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)
    assert len(blocks)==3
    def clean(t):
        t=t.replace('\\begin{aligned}','').replace('\\,','')
        return re.sub(r'\\cancel\{([^{}]+)\}',r'\1',t)
    distributed=[v.equation(clean(z)) for z in blocks[1].split('\\\\')]
    expected=[(sp.Integer(p[f'a{i+1}'])*x+sp.Integer(p[f'b{i+1}'])*y,sp.Integer(p[f'c{i+1}'])) for i in (0,1)]
    expected[row]=tuple(sp.expand(z*m) for z in expected[row]);assert distributed==expected
    stages=[v.equation(clean(z)) for z in blocks[2].split('\\\\')];assert len(stages)==5
    total=tuple(sp.expand(expected[0][i]+expected[1][i]) for i in (0,1))
    assert stages[:2]==expected and stages[2]==total and stages[3]==total
    assert total[0].coeff(x)==0 and total[0].coeff(y)!=0
    assert stages[4]==(y,total[1]/total[0].coeff(y))
    assert sp.solve([a-b for a,b in expected],(x,y))[y]==stages[4][1]
    assert ('second' if row else 'first') in q[':question/worked-solution']
    assert f'({m})' in blocks[0]
    return {'source_id':mid,'complete':True,'bank_choices_matched':6,'difficulty':q[':question/difficulty'][':db/ident'],'rendered_solution_stages_verified':5,'mathematical_fingerprint':fingerprint(q)}

def main():
    src=json.loads((H/'current-source.json').read_text());results=[];native=[]
    for q in src['record'][':knowledge-point/questions']:
        result=source_check(q);results.append(result)
        if result['complete']:
            r={'question':projected(q)}
            native.append({'label':q[':question/math-academy-id'],'record':r,'checks':[{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Full current source choice bank with independently calculated cancellation'} for i,f in enumerate(r['question'][':question/answer-fields']) for a in f[':answer-field/choices']]})
    (H/'current-source-native-input.json').write_text(json.dumps(native,indent=2)+'\n')
    subprocess.run([str(H.parents[2]/'generate/runs/current/check-engine'),str(H/'current-source-native-input.json'),str(H/'current-source-native-report.json')],check=True)
    result={'passed':True,'basis':src['basis'],'lineage':src['lineage'],'source_checks':results,'validated_question_ids':[q[':question/id'] for q,r in zip(src['record'][':knowledge-point/questions'],results) if r['complete']],'full_current_bank_choices_matched':18,'full_current_banks_matched':6,'new_captured_profile_generation':'excluded; ±(|m|+1) reproduces observed values but distractor reasoning is not established'}
    (H/'current-source-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
