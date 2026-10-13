#!/usr/bin/env python3
"""Independent actual-display mathematics, stage/shape, omissions, and native QA."""
import copy, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y=sp.symbols('x y')
def parse(s):
    s=s.replace('&','').replace(r'\,','').replace(' ','')
    s=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'(\1)/(\2)',s)
    return parse_expr(s,local_dict={'x':x,'y':y},transformations=standard_transformations+(implicit_multiplication_application,))
def eq(s):
    lhs,rhs=s.replace('&','').split('=');return parse(lhs),parse(rhs)
def tuple_value(s):
    assert s.startswith('(') and s.endswith(')');return tuple(parse(v) for v in s[1:-1].split(','))
def rows(block):return [s.strip() for s in block.split(r'\\') if s.strip()]
def printed_system(q):
    text=q[':question/problem']
    blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S)
    if blocks:return [eq(s) for s in rows(blocks[0])]
    s=text.split('${',1)[1].split('$',1)[0];return [eq(t) for t in s.split(';')]
def actual_math(r):
    q=r['question'];raw=r['generation']['evidence_only'];sysrows=printed_system(q);assert len(sysrows)==2
    L1,R1=sysrows[0];L2,R2=sysrows[1]
    assert all(not R.free_symbols and L.free_symbols=={x,y} and sp.Poly(L,x,y).total_degree()==1 for L,R in sysrows)
    solution=sp.solve([L1-R1,L2-R2],(x,y));assert set(solution)=={x,y};X,Y=solution[x],solution[y]
    a,b,c,d=L1.coeff(x),L1.coeff(y),L2.coeff(x),L2.coeff(y)
    row=r['generation']['parameters']['row'];k=-d/b if row==1 else -b/d
    A,B,R=(a,b,R1) if row==1 else (c,d,R2)
    U,V,RR=(k*L1,L2,k*R1+R2) if row==1 else (L1,k*L2,R1+k*R2)
    h=sp.expand(U+V).coeff(x)
    if raw:
        for f in q[':question/answer-fields']:
            if ':answer-field/choices' in f:
                vals=[tuple_value(v[':answer/value']) for v in f[':answer-field/choices']];assert len(set(vals))==5
                assert sum(all(sp.expand(L.subs({x:t[0],y:t[1]})-R)==0 for L,R in sysrows) for t in vals)==1
        return {'x':X,'y':Y,'h':h,'n':RR,'A':A,'B':B,'R':R}
    level=r['generation']['authored_level']
    assert q[':question/difficulty']==':question.difficulty/'+level
    assert all(v.q==1 and 1<=abs(v)<=5 for v in (X,Y))
    assert all(v.q==1 and v!=0 for v in (a,b,c,d)) and R1.q==1 and R2.q==1
    assert abs(a)<=7 and abs(c)<=7 and abs(h)>=2
    assert sp.gcd(abs(a),abs(b))==1 and sp.gcd(abs(c),abs(d))==1
    assert max(abs(R1),abs(R2))<=dict(easy=25,moderate=35,hard=40)[level]
    if level=='easy':assert B==1 and 2<=abs(k)<=7
    elif level=='moderate':assert 2<=abs(B)<=3 and 2<=abs(k)<=4
    else:assert 2<=abs(B)<=3 and 5<=abs(k)<=7
    assert k.q==1
    fields=q[':question/answer-fields']
    assert r['generation']['version']==g.VERSION
    values=sorted(a[':answer/value'] for f in fields for a in f[':answer-field/choices'])
    expected_id=g.uid(g.serial([g.VERSION,level,q[':question/problem'],q[':question/worked-solution'],values]))
    assert q[':question/id']==expected_id
    for f in fields:
        assert f[':answer-field/id']==g.uid(expected_id+f[':answer-field/key'])
        for a0 in f[':answer-field/choices']:
            assert a0[':answer/id']==g.uid(expected_id+f[':answer-field/key']+a0[':answer/value'])
            assert a0[':answer/type']==':answer.type/math'
    for f in fields:
        bank=f[':answer-field/choices'];ref=f[':answer-field/correct'];assert ref[0]==':answer/id';assert len({v[':answer/id'] for v in bank})==len(bank)
        correct=[v for v in bank if v[':answer/id']==ref[1]];assert len(correct)==1
        if f[':answer-field/type'].endswith('/radio'):
            vals=[tuple_value(v[':answer/value']) for v in bank];assert len(vals)==5 and len(set(vals))==5
            iscorrect=[all(sp.expand(L.subs({x:t[0],y:t[1]})-R)==0 for L,R in sysrows) for t in vals];assert sum(iscorrect)==1
            assert tuple_value(correct[0][':answer/value'])==(X,Y)
            # Reconstruct the ENTIRE selected mistake bank from the actual displayed system.
            def back(t):return (t,(R-A*t)/B)
            scaled_rhs=R;unscaled_rhs=R2 if row==1 else R1
            omission=back((scaled_rhs+unscaled_rhs)/h);addition=(X,(R+A*X)/B)
            if r['generation']['profile']=='signed_substitution':expected_bank=[(X,Y),omission,back((unscaled_rhs-k*scaled_rhs)/h),addition,(X,-Y)]
            else:
                assert abs(B)>1 and a+c!=0
                expected_bank=[(X,Y),back(RR/(a+c)),omission,addition,(X,R-A*X)]
            assert set(vals)==set(expected_bank)
        else:
            assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
            assert parse(correct[0][':answer/value'])==(X if f[':answer-field/key']=='field-1' else Y)
    s=q[':question/worked-solution'];blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',s,re.S);assert len(blocks)==2
    elim=rows(blocks[0]);sub=rows(blocks[1]);assert len(elim)==5;assert len(sub)==(4 if B==1 else 5)
    # Whole-line relation plus exact distributed sides: no scalar normalization hides wrong stage coefficients.
    expected=[(U,k*R1 if row==1 else R1),(V,R2 if row==1 else k*R2),(U+V,RR),(h*x,RR),(x,X)]
    for line,(l,rhs) in zip(elim,expected):
        l0,r0=eq(line);assert sp.expand(l0-l)==0 and sp.expand(r0-rhs)==0,(line,l,rhs)
        assert sp.expand((l0-r0).subs({x:X,y:Y}))==0
    # Independently demand grouped addition of the two retained-x coefficients and two scaled RHS components.
    l,rhs=elim[2].replace('&','').split('=');assert l.startswith('(') and l.endswith(')') and rhs.startswith('(') and rhs.endswith(')')
    lparts=re.findall(r'[+-]?\d*x',l[1:-1]);rparts=re.findall(r'[+-]?\d+',rhs[1:-1]);assert len(lparts)==2 and len(rparts)==2
    assert [parse(v).coeff(x) for v in lparts]==[sp.expand(U).coeff(x),sp.expand(V).coeff(x)]
    assert [parse(v) for v in rparts]==[k*R1 if row==1 else R1,R2 if row==1 else k*R2]
    expected_sub=[(A*x+B*y,R),(A*X+B*y,R),(A*X+B*y,R)]+([(y,Y)] if B==1 else [(B*y,R-A*X),(y,Y)])
    for line,(l,rhs) in zip(sub,expected_sub):
        l0,r0=eq(line);assert sp.expand(l0-l)==0 and sp.expand(r0-rhs)==0
        assert sp.expand((l0-r0).subs({x:X,y:Y}))==0
    # Distinct unevaluated substitution and evaluated product, before collection.
    assert '('+str(X)+')' in sub[1];assert '(' not in sub[2]
    assert 'x' in sub[0] and 'x' not in sub[1]
    assert re.search(r'x\s*=\s*'+re.escape(str(X)),s) and re.search(r'y\s*=\s*'+re.escape(str(Y)),s)
    conclusion=re.search(r'which can be expressed as \$(.*?)\$\.',s);assert conclusion and tuple_value(conclusion[1])==(X,Y)
    # Annotation scales exactly one complete equation, keeping signs/group boundaries explicit.
    annotation=s.split('$$')[1].strip();assert annotation.count(r'\cdot')==1
    assert ('first equation' if row==1 else 'second equation') in s
    unscaled,scaled=(L2,R2) if row==1 else (L1,R1)
    parts=annotation.removeprefix(r'\{ ').split('; ');assert len(parts)==2
    for i,part in enumerate(parts):
        if i==row-1:
            mt=re.fullmatch(r'\\left\((.*?)\\right\)\\cdot \((.*?)\)',part);assert mt
            l0,r0=eq(mt[1]);assert parse(mt[2])==k
        else:l0,r0=eq(part)
        lp,rp=sysrows[i];assert sp.expand(l0-lp)==0 and sp.expand(r0-rp)==0
    # All normal nonliteral TeX groups, inline/display delimiters are balanced.
    clean=re.sub(r'\\[{}]','',q[':question/problem']+'\n'+s)
    assert clean.count('{')==clean.count('}')
    displays=clean.count('$$');assert displays%2==0
    assert clean.replace('$$','').count('$')%2==0
    assert not any(v in clean for v in ('+-','--'))
    return {'x':X,'y':Y,'h':h,'n':RR,'A':A,'B':B,'R':R}

def write(name,v):(HERE/name).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def shape_keys(a,b):
    assert set(a)==set(b),(set(a),set(b))
    for k in a:
        if isinstance(a[k],dict):
            if ':db/ident' in a[k]:assert b[k]==a[k][':db/ident']
            else:shape_keys(a[k],b[k])
        elif isinstance(a[k],list) and a[k] and isinstance(a[k][0],dict):
            assert len(a[k])==len(b[k]);
            for old,new in zip(sorted(a[k],key=lambda t:t.get(':answer/value',t.get(':answer-field/key',''))),sorted(b[k],key=lambda t:t.get(':answer/value',t.get(':answer-field/key','')))):shape_keys(old,new)

cases=[{'source_id':'q-170145','template':'radio_hint','level':'easy','parameters':{'a':3,'b':-2,'c':4,'d':1,'C':-1,'D':-5,'row':2},'bank_profile':'source_radio'}, {'source_id':'q-238087','template':'pair_blank','level':'moderate','parameters':{'a':-5,'b':2,'c':7,'d':4,'C':11,'D':5,'row':1},'bank_profile':'source_blank'}]
def main():
    write('source-cases.json',cases);raws=[];source_checks=[];native=[];reviews=[]
    for case,original in zip(cases,g.SOURCE['record'][':knowledge-point/questions']):
        r=g.generate(case['level'],parameters=case['parameters'],template=case['template'],profile=case['bank_profile']);raws.append(r)
        shape_keys(original,r['question']);assert r['question'][':question/problem']==original[':question/problem']
        if case['bank_profile']=='source_radio':assert sorted(v[':answer/value'] for v in r['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(v[':answer/value'] for v in original[':question/answer-fields'][0][':answer-field/choices'])
        actual_math(r);source_checks.append({'source_id':case['source_id'],'prompt_exact':True,'attribute_presence_exact':True,'bank_values_exact':True,'correct_designation':'absent in original and replay','worked_solution':'absent in original and replay'})
        # Exercise changed-parameter raw profiles through PUBLIC API, rather than copied snapshots.
        p=dict(case['parameters']);p['C']+=p['a'];p['D']+=p['c'];changed=g.generate(case['level'],parameters=p,profile=case['bank_profile']);actual_math(changed)
        reviews.append({'label':'raw source '+case['source_id'],'record':r});reviews.append({'label':'changed raw evidence '+case['source_id'],'record':changed})
    coverage={};unique={};samples=[]
    for level in g.LEVELS:
        fingerprints=set();families=set()
        for seed in range(1000):
            r=g.generate(level,seed);z=actual_math(r);families.add((r['generation']['template'],r['generation']['profile']));fingerprints.add(r['generation']['mathematical_fingerprint'])
            assert set(r['knowledge_point'])=={'db_id','id','title'}
            p=r['generation']['parameters'];z0=g.guard(level,p)
            assert z['x']==z0['x'] and z['y']==z0['y']
            if seed<8:samples.append(r)
        unique[level]=len(fingerprints);coverage[level]=[list(v) for v in sorted(families)]
        expected={(t,p) for t in g.TEMPLATES for p in (g.PROFILES[:1] if level=='easy' else g.PROFILES)};assert families==expected
        for template in g.TEMPLATES:
            for profile in (g.PROFILES[:1] if level=='easy' else g.PROFILES):
                for seed in (14,27):
                    r=g.generate(level,seed,template=template,profile=profile);z=actual_math(r);reviews.append({'label':f'authored {level}/{template}/{profile} seed{seed}','record':r})
                    r2=g.generate(level,seed+20,template=template,profile=profile,parameters=r['generation']['parameters']);assert r2['question'][':question/id']==r['question'][':question/id']
                    checks=[]
                    for i,f in enumerate(r['question'][':question/answer-fields']):
                        if f[':answer-field/type'].endswith('/radio'):
                            for a in f[':answer-field/choices']:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'all displayed tuple choices'})
                        else:
                            val=z['x'] if i==0 else z['y'];equiv=f"({z['n']})/({z['h']})" if i==0 else f"({z['R']}-({z['A']})*({z['x']}))/({z['B']})"
                            checks.extend([{'field_index':i,'submitted':str(val),'expected':'accepted','purpose':'canonical coordinate fragment'}, {'field_index':i,'submitted':equiv,'expected':'accepted','purpose':'independent unreduced elimination or back-substitution expression'}, {'field_index':i,'submitted':str(val+1),'expected':'rejected','purpose':'incorrect coordinate'}])
                    native.append({'label':reviews[-1]['label'],'record':r,'checks':checks})
    # Explicit inputs must obey each authored band; unsupported number forms never silently resample.
    rejects=0
    for level in g.LEVELS:
        r=g.generate(level,7);p=r['generation']['parameters']
        for mutation in ({**p,'C':101},{**p,'a':8},{**p,'b':0},{**p,'C':'1/2'}):
            try:g.generate(level,parameters=mutation)
            except ValueError:rejects+=1
            else:raise AssertionError('invalid explicit parameters accepted')
        other='hard' if level!='hard' else 'moderate'
        try:g.generate(other,parameters=p,profile=r['generation']['profile'])
        except ValueError:rejects+=1
        else:raise AssertionError('difficulty workload overlap')
    for level,p in [('easy',dict(a=4,b=2,c=1,d=1,C=6,D=2,row=2)),('moderate',dict(a=2,b=2,c=2,d=4,C=4,D=6,row=1)),('hard',dict(a=2,b=2,c=2,d=10,C=4,D=12,row=1))]:
        try:g.generate(level,parameters=p)
        except ValueError:rejects+=1
        else:raise AssertionError('GCF reduced unit workload accepted')
    for level in g.LEVELS:
        r=g.generate(level,29);p=r['generation']['parameters'];fid=r['generation']['mathematical_fingerprint']
        # Swap original row order with scaled-row selector; calculation is identical.
        swapped=dict(a=p['c'],b=p['d'],C=p['D'],c=p['a'],d=p['b'],D=p['C'],row=3-p['row'])
        assert g.generate(level,parameters=swapped,profile=r['generation']['profile'])['generation']['mathematical_fingerprint']==fid
        # Flip unscaled complete equation; same cancellation/arithmetic up to whole-line sign.
        alias=dict(p)
        for key in (('c','d','D') if p['row']==1 else ('a','b','C')):alias[key]=-alias[key]
        assert g.generate(level,parameters=alias,profile=r['generation']['profile'])['generation']['mathematical_fingerprint']==fid
    # Regressions must detect algebraic and structural corruption in actual strings.
    base=g.generate('moderate',17,template='radio_hint');solution=base['question'][':question/worked-solution'];blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S)
    e=rows(blocks[0]);mutations=[]
    mutations.append(solution.replace(e[1],e[1].replace('&=','&=1+',1),1))
    mutations.append(solution.replace(e[2],e[3],1))
    mutations.append(re.sub(r'which can be expressed as \$(.*?)\$\.', 'which can be expressed as $(999,999)$.', solution))
    for s in mutations:
        bad=copy.deepcopy(base);bad['question'][':question/worked-solution']=s
        try:actual_math(bad)
        except (AssertionError,ValueError,TypeError,SyntaxError):pass
        else:raise AssertionError('display mutation undetected')
    for case in cases:
        r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile='signed_substitution');z=actual_math(r);checks=[]
        reviews.append({'label':'authored completion at original parameters '+case['source_id'],'record':r})
        for i,f in enumerate(r['question'][':question/answer-fields']):
            if f[':answer-field/type'].endswith('/radio'):
                for a in f[':answer-field/choices']:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'source-parameter authored complete bank'})
            else:
                v=z['x'] if i==0 else z['y'];equiv=f"({z['n']})/({z['h']})" if i==0 else f"({z['R']}-({z['A']})*({z['x']}))/({z['B']})"
                for submitted,expected in [(str(v),'accepted'),(equiv,'accepted'),(str(v+1),'rejected')]:checks.append({'field_index':i,'submitted':submitted,'expected':expected,'purpose':'source-parameter inferred blank fragment'})
        native.append({'label':reviews[-1]['label'],'record':r,'checks':checks})
    for level in g.LEVELS:
        assert g.generate(level,field_type='blank')['generation']['template']=='pair_blank'
        assert g.generate(level,field_type='radio')['generation']['template']=='radio_hint'
    # Source malformed TeX is evidence only; completed normal records are normalized.
    write('native-input.json',native)
    engine=HERE.parents[1]/'runs/current/check-engine'
    subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
    write('review.json',reviews);write('raw-replays.json',raws)
    report={'status':'passed','source_provenance':{k:g.SOURCE[k] for k in ('database','basis','lineage')},'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'source_fidelity':{'practice_questions':2,'exact_prompts':2,'presence_parity':2,'complete_observed_banks':1,'choices_matched':5,'choices_total':5,'wrong_choices_matched':4,'wrong_choices_total':4,'original_correct_refs':0,'matched_original_correct_refs':0,'original_worked_solutions':0,'source_checks':source_checks},'mathematics':{'actual_prompt_and_all_stages_instances':3000,'mutations_rejected':3,'explicit_scope_rejections':rejects},'default_coverage':coverage,'meaningful_sampled_tasks_out_of_1000':unique,'native_grading':json.loads((HERE/'native-report.json').read_text()),'raw_source_anomalies':['both unrated; omit difficulty in raw replay','both lack worked solutions and correct refs','radio bank opaque historical wrong tuples','blank fields have no choices','unescaped opening system brace both; blank interleaved dollar rendering malformed'], 'authored_extensions':'All levels and completed normal solutions; integer-only, exactly one scaling/addition/back-substitution. Raw source profiles ineligible for learning. No plots required.','finite_catalog':json.loads((HERE/'catalog.json').read_text()) if (HERE/'catalog.json').exists() else None,'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest()}
    write('validation.json',report)
    text=['# Review: second-variable one-transformation solve','Raw historical evidence preserves missing attributes and malformed presentation. All difficulty labels below are authored. Historical distractor offsets are opaque and ineligible for normal learning.']
    for item in reviews:text.extend(['\n## '+item['label'],g.markdown(item['record'])])
    (HERE/'review.md').write_text('\n\n'.join(text)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('native_grading','source_provenance','source_fidelity')},indent=2))
if __name__=='__main__':main()
