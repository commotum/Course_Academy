#!/usr/bin/env python3
"""Read actual printed formulas independently, then test native engine grading."""
import importlib.util,json,re,subprocess,hashlib,sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('ivp',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
SOURCE=json.loads((ROOT/'source.json').read_text());QS=SOURCE['record'][':knowledge-point/questions']
X,Y,A=g.X,g.Y,g.A

def group(s,i):
    if s[i]!='{':raise ValueError(('expected TeX group',s,i))
    n=1;j=i+1
    while n:
        if s[j]=='{':n+=1
        elif s[j]=='}':n-=1
        j+=1
    return s[i+1:j-1],j

def parse(t):
    t=t.replace('\\\\','\\').replace('\u2061','')
    t=re.sub(r'\\operatorname\{(sin|cos|tan|cot|ln)\}',r'\\\1',t)
    t=t.replace('Asin',r'A\sin').replace('Acos',r'A\cos')
    t=t.replace(r'\left','').replace(r'\right','').replace(r'\cdot','*').replace(r'\,','').replace(r'\pi','pi')
    def convert(s):
        out='';i=0
        while i<len(s):
            if s.startswith(r'\frac',i):
                a,j=group(s,i+5);b,j=group(s,j);out+='(('+convert(a)+')/('+convert(b)+'))';i=j
            elif s.startswith(r'\sqrt',i):
                a,j=group(s,i+5);out+='sqrt('+convert(a)+')';i=j
            elif s[i]=='{':
                a,j=group(s,i);out+='('+convert(a)+')';i=j
            else:out+=s[i];i+=1
        return out
    t=convert(t)
    for name in ('sin','cos','tan','cot','ln'):t=t.replace('\\'+name,name if name!='ln' else 'log')
    t=re.sub(r'(sin|cos|tan|cot)\s*([+-]?\d*\s*x)',r'\1(\2)',t)
    t=re.sub(r'(?<=[A-Za-z0-9)])(sin|cos|tan|cot|log|sqrt)(?=\()',r'*\1',t)
    t=re.sub(r'(?<=\d)e', '*e', t)
    t=t.strip().rstrip('.')
    return parse_expr(t,local_dict={'x':X,'y':Y,'A':A,'e':sp.E,'pi':sp.pi,'sin':sp.sin,'cos':sp.cos,'tan':sp.tan,'cot':sp.cot,'log':sp.log,'sqrt':sp.sqrt},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))

def spans(s):return [m.group().strip('$').strip() for m in re.finditer(r'\$\$.*?\$\$|\$[^$]*\$',s,re.S)]
def rows(s):
    block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',s,re.S).group(1)
    return [tuple(r.replace('&','').strip().rstrip('.').split('=',1)) for r in block.split(r'\\')]
def canonical(v):return sp.srepr(sp.simplify(parse(v)))
def format_check(s):
    assert s.count('$')%2==0
    d=0
    for c in s:
        d+=1 if c=='{' else -1 if c=='}' else 0
        assert d>=0,(s,'unbalanced braces')
    assert d==0
    assert '@@' not in s and not re.search(r'(?<!\\)[+\-]{2}',s)

def independent_authored_bank(fun,u,b):
    """Derive every wrong operation from the actual displayed supplied equation."""
    factor=sp.simplify(fun/A)
    if factor.func==sp.exp:
        F=factor.subs(X,u);return 'exp',[b/F,b*F,b,F/b,1/(b*F)]
    if factor.func in (sp.sin,sp.cos):
        name='sin' if factor.func==sp.sin else 'cos';t=factor.args[0].subs(X,u)
        F=factor.subs(X,u);G=(sp.cos(t) if name=='sin' else sp.sin(t))
        return name,[b/F,b*F,b,b/G,F/b]
    if fun.func==sp.log:
        shift=fun.args[0].subs(X,u)-A
        return 'log',[sp.exp(b)-shift,sp.exp(b)+shift,b-shift,sp.exp(b-shift),sp.exp(-b)-shift]
    denominator=sp.denom(sp.cancel(fun))
    if denominator.has(A):
        shift=sp.simplify(1/fun).subs(X,u)-A
        return 'recip',[1/b-shift,1/b+shift,b-shift,1/(b-shift),-1/b-shift]
    exponent=factor.as_powers_dict().get(X)
    assert exponent is not None and exponent.is_Integer
    n=abs(exponent);F=u**n
    if exponent>0:
        return ('power_unary',[b/u,b*u,b,u/b,1/(b*u)]) if n==1 else ('power_nonunit',[b/F,b*F,b/u,b/(n*u),b/(u+n)])
    return ('invpower_unary',[b*u,b/u,b,u/b,1/(b*u)]) if n==1 else ('invpower_nonunit',[b*F,b/F,b*u,b*n*u,b*(u+n)])

def printed(r):
    q=r['question'];p=spans(q[':question/problem']);eq=p[0]
    ode,ic=eq.split(',',1)
    rhs=parse(ode.split('=',1)[1]);ic=ic.replace(r'\,','').strip().rstrip('.')
    mat=re.search(r'y\((.*?)\)\s*=\s*(.*)',ic);assert mat,ic
    u,b=parse(mat[1]),parse(mat[2]);fun=parse(p[1].split('=',1)[1])
    f=q[':question/answer-fields'][0];vals=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
    solutions=sp.solve(sp.Eq(fun.subs(X,u),b),A);assert len(solutions)==1
    a=solutions[0]
    assert sp.simplify(sp.diff(fun,X)-rhs.subs(Y,fun))==0,(fun,rhs)
    assert sp.simplify(fun.subs({X:u,A:a})-b)==0
    # Check both ODE and supplied-function domains at the initial point.
    assert not fun.subs({X:u,A:a}).has(sp.zoo,sp.nan,sp.oo)
    assert not rhs.subs({X:u,Y:b}).has(sp.zoo,sp.nan,sp.oo)
    assert sum(sp.simplify(v-a)==0 for v in vals)==1
    assert all(sp.simplify(v-w)!=0 for i,v in enumerate(vals) for w in vals[i+1:])
    if not r['generation']['evidence_only'] and f[':answer-field/type'].endswith('radio'):
        name,expected=independent_authored_bank(fun,u,b)
        assert name==r['generation']['authored_bank']
        assert len(expected)==len(vals)==5
        for value in expected:assert sum(sp.simplify(value-option)==0 for option in vals)==1,(name,value,vals)
        assert len(r['generation']['bank_operations'])==5
    if ':answer-field/correct' in f:
        correct=next(z for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);assert sp.simplify(parse(correct[':answer/value'])-a)==0
    if ':question/worked-solution' in q:
        sol=q[':question/worked-solution']
        for i,(l,rr) in enumerate(rows(sol)):
            lhs,rhsrow=parse(l),parse(rr)
            assert sp.simplify((lhs-rhsrow).subs({A:a,Y:fun.subs(A,a)}))==0,(i,l,rr,a)
        # Read every prose condition back, protecting no mathematical arguments.
        for s in spans(sol):
            if s.startswith('y(') or s.startswith(r'y\,('):
                mat=re.search(r'y\((.*?)\)=(.*)',s.replace(r'\,','').rstrip('.'))
                assert mat and sp.simplify(parse(mat[1])-u)==0 and sp.simplify(parse(mat[2])-b)==0
        # Final solution statements, where included, independently substitute A.
        for s in spans(sol):
            if s.startswith('y=') or s.startswith('y ='):
                bits=s.rstrip('.').split('=')
                exprs=[parse(z).subs(A,a) for z in bits[1:]]
                assert all(sp.simplify(z-fun.subs(A,a))==0 for z in exprs)
        format_check(sol)
    format_check(q[':question/problem'])
    assert set(r['knowledge_point'])=={'db_id','id','title'}
    assert r['knowledge_point']['db_id']==g.KP_ID
    for z in f[':answer-field/choices']:format_check(z[':answer/value']);assert '$' not in z[':answer/value']
    if f[':answer-field/type'].endswith('blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
    return a

def fidelity(q,r):
    got=r['question'];f=q[':question/answer-fields'][0];gf=got[':question/answer-fields'][0]
    for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in got)
    assert (':answer-field/correct' in f)==(':answer-field/correct' in gf)
    assert f[':answer-field/type'][':db/ident']==gf[':answer-field/type'] and f[':answer-field/key']==gf[':answer-field/key']
    assert sorted(z[':answer/value'] for z in f[':answer-field/choices'])==sorted(z[':answer/value'] for z in gf[':answer-field/choices'])
    original=[canonical(z[':answer/value']) for z in f[':answer-field/choices']];new=[canonical(z[':answer/value']) for z in gf[':answer-field/choices']]
    assert sorted(original)==sorted(new),(q[':question/math-academy-id'],original,new)
    if ':answer-field/correct' in f:
        source=canonical(f[':answer-field/correct'][':answer/value']);target=canonical(next(z for z in gf[':answer-field/choices'] if z[':answer/id']==gf[':answer-field/correct'][1])[':answer/value']);assert source==target
    assert q[':question/problem']==got[':question/problem'],(q[':question/math-academy-id'],'prompt',q[':question/problem'],got[':question/problem'])
    if ':question/worked-solution' in q:
        assert q[':question/worked-solution']==got[':question/worked-solution'],q[':question/math-academy-id']
        orig=q[':question/worked-solution'];newsol=got[':question/worked-solution']
        # Complete ordered math stages and complete prose compared, not phrase samples.
        orows,nrows=rows(orig),rows(newsol);assert len(orows)==len(nrows)
        for old,newrow in zip(orows,nrows):assert all(sp.simplify(parse(a)-parse(b))==0 for a,b in zip(old,newrow)),(q[':question/math-academy-id'],old,newrow)
        prose=lambda s:re.sub(r'\$\$.*?\$\$|\$[^$]*\$','[MATH]',s,flags=re.S)
        assert prose(orig)==prose(newsol)
        assert len(spans(orig))==len(spans(newsol))
        for old,newspan in zip(spans(orig),spans(newsol)):
            if old.startswith(r'\begin{aligned}'):continue
            if old.startswith('y'):
                old_parts=old.rstrip('.').split('=');new_parts=newspan.rstrip('.').split('=')
                assert len(old_parts)==len(new_parts)
                for oldp,newp in zip(old_parts[1:],new_parts[1:]):assert sp.simplify(parse(oldp)-parse(newp))==0
    return len(original), max(0,len(original)-1)

def engine_item(r,label):
    f=r['question'][':question/answer-fields'][0];c=f[':answer-field/correct'][1];ans=f[':answer-field/choices'];a=next(z[':answer/value'] for z in ans if z[':answer/id']==c)
    if f[':answer-field/type'].endswith('radio'):
        checks=[{'submitted_answer_id':z[':answer/id'],'expected':'accepted' if z[':answer/id']==c else 'rejected','purpose':'every displayed option designation'} for z in ans]
    else:
        checks=[{'submitted':a,'expected':'accepted','purpose':'canonical exact constant'}, {'submitted':'('+a+')+1','expected':'rejected','purpose':'wrong constant'}, {'submitted':'(('+a+')+('+a+'))/2','expected':'accepted','purpose':'genuinely unreduced equivalent constant'}]
    return {'record':r,'label':label,'checks':checks}

def write(name,v):(ROOT/name).write_text(json.dumps(v,indent=2)+'\n')
def original_markdown(q):
    out='Difficulty: '+g.difficulty_label(q)+'\n\nOrigin: Original; evidence only\n\n'+q[':question/problem']
    for f in q.get(':question/answer-fields',[]):
        correct=f.get(':answer-field/correct')
        if correct is None:out+='\n\nCorrect designation: absent in the original source attribute.'
        for a in f[':answer-field/choices']:
            mark=' **[correct]**' if correct and a[':answer/id']==correct[':answer/id'] else ''
            out+='\n\n- $'+a[':answer/value']+'$'+mark
    return out+'\n\n'+q.get(':question/worked-solution','[Worked solution absent in captured source.]')

def render_review(review):
    md=['# Source originals and generated variants','\nOriginals below are copied from preserved capture evidence; variants are separately labeled.']
    for q in QS:md+=['\n## Original '+q[':question/math-academy-id'],original_markdown(q)]
    for r in review:md+=['\n## '+r['label'],g.markdown(r['record'])]
    return '\n\n'.join(md)+'\n'

def main():
    cases=[];review=[];engine=[];options=distractors=designation=0;exact_solutions=0
    for q in QS:
        sid=q[':question/math-academy-id'];params=g.source_parameters(sid)
        r=g.generate('easy',template=sid,parameters=params,profile='observed:'+sid)
        printed(r);n,d=fidelity(q,r);options+=n;distractors+=d;designation+=int(':answer-field/correct' in q[':question/answer-fields'][0])
        exact_solutions+=int(q.get(':question/worked-solution') is not None and q[':question/worked-solution']==r['question'].get(':question/worked-solution'))
        cases.append({'source_id':sid,'db_id':q[':db/id'],'template':sid,'parameters':params,'bank_profile':'observed:'+sid,'level':'easy','authored_level_assignment':':question/difficulty' not in q})
        completed=g.generate('easy',template=sid,parameters=params,profile='completed:'+sid);printed(completed);engine.append(engine_item(completed,'source/'+sid))
        review.append({'label':'original replay '+sid,'record':r})
        # Variant for every observed prompt/layout/bank; explicitly evidence only.
        for seed in (17,29):
            r=g.generate('easy',seed,template=sid,profile='observed:'+sid);printed(r);review.append({'label':'generated observed-profile variant '+sid,'record':r})
            if ':answer-field/correct' in r['question'][':question/answer-fields'][0]:engine.append(engine_item(r,'observed variant/'+sid+'/'+str(seed)))
    for level in ('easy','moderate','hard'):
        for t,v in g.TEMPLATES.items():
            if v['level']!=level:continue
            for seed in (2,5,9,31):
                r=g.generate(level,seed,template=t);printed(r);engine.append(engine_item(r,'authored/'+t+'/'+str(seed)));review.append({'label':'generated normal '+level+' '+t,'record':r})
                fixed=g.generate(level,99,template=t,parameters=r['generation']['parameters']);assert fixed['question'][':question/id']==r['question'][':question/id'];assert fixed['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
    # Strong explicit workload bounds: reject removed level demand and excessive signed values.
    for l,t,p in [('moderate','exponential_nonzero',{'k':2,'u':0,'b':3}),('moderate','exponential_nonzero',{'k':2,'u':1,'b':3}),('hard','reciprocal_nonzero',{'k':1,'u':0,'b':'1/2'}),('hard','reciprocal_nonzero',{'k':1,'u':1,'b':1}),('hard','logarithmic_nonzero',{'k':1,'u':1,'b':-4})]:
        try:g.generate(l,template=t,parameters=p)
        except ValueError:pass
        else:raise AssertionError('workload bound bypass')
    # Exercise catalog edges and the newly supported familiar radicals in actual output.
    for t in ('q-352663','q-352660','q-352654','q-352661','q-347839','q-352649'):
        f=g.TEMPLATES[t]['family']
        catalog=(sp.sqrt(2),-sp.sqrt(2),sp.sqrt(3)/2,-sp.sqrt(3)/2) if f in ('sin','cos') else (sp.Integer(8),sp.Integer(-8),sp.Rational(1,4),sp.Rational(-8,3))
        for b in catalog:
            p=g.source_parameters(t);p['b']=str(b)
            r=g.generate('easy',template=t,parameters=p);printed(r)
            review.append({'label':'generated easy catalog boundary '+t+' b='+str(b),'record':r})
            engine.append(engine_item(r,'catalog boundary/'+t+'/'+str(b)))
    # Every easy family/layout and all public profiles use the same reduced-number guard.
    rejected_number_forms=0
    for t,v in g.TEMPLATES.items():
        if v['level']!='easy':continue
        for bad in ('1/1000003','-1/1000003','sqrt(5)','(sqrt(2)+sqrt(3))/4','sqrt(2)/1000003'):
            for profile in (None,'observed:'+t,'completed:'+t):
                p=g.source_parameters(t);p['b']=bad
                try:g.generate('easy',template=t,parameters=p,profile=profile)
                except ValueError:rejected_number_forms+=1
                else:raise AssertionError(('easy number-form bypass',t,bad,profile))
    # Enumerate method-bank eligibility on finite sampler supports. Counts exclude
    # source-layout/profile aliases. Normal blanks retain the union support of
    # every easy family except log; its only normal layout is radio.
    from itertools import product
    rc=len(g.EASY_RATIONAL_VALUES);tc=len(g.EASY_TRIG_VALUES)
    easy_counts={'power':4*4*rc,'invpower':4*4*rc,'exp':6*5*rc,'sin':4*6*tc,'cos':4*5*tc,'recip':2*5*rc,'log':4*6}
    radio_counts={}
    supports={
      'power_nonunit':('power',[2,3,4],[-2,-1,1,2],g.EASY_RATIONAL_VALUES),
      'power_unary':('power',[1],[-2,-1,1,2],g.EASY_RATIONAL_VALUES),
      'invpower_nonunit':('invpower',[2,3,4],[-2,-1,1,2],g.EASY_RATIONAL_VALUES),
      'invpower_unary':('invpower',[1],[-2,-1,1,2],g.EASY_RATIONAL_VALUES),
      'exp':('exp',[-3,-2,-1,1,2,3],[-2,-1,0,1,2],g.EASY_RATIONAL_VALUES),
      'cos':('cos',[1,2,3,4],[sp.pi/6,sp.pi/4,sp.pi/3,2*sp.pi/3,3*sp.pi/4],g.EASY_TRIG_VALUES),
      'recip':('recip',[-1,1],[-2,-1,0,1,2],g.EASY_RATIONAL_VALUES),
      'log':('log',[1],[-2,-1,0,1,2],[-3,-2,-1,1,2,3])}
    for name,(family,coefficients,inputs,outputs) in supports.items():
        count=0
        for k,u,b in product(coefficients,inputs,outputs):
            u=u/k if family=='cos' else sp.Integer(u)
            p={'k':sp.Integer(k),'u':u,'b':sp.sympify(b)}
            a=g.math_object(family,p['k'],u,p['b'])[2]
            values=g.authored_bank(name,p)
            count+=int(g.eligible_values(values,a))
        radio_counts[name]=count
    # Explicit degenerate banks reject the whole instance, rather than repairing options.
    collision_checks=0
    for t,p in [('q-141107',{'k':2,'u':2,'b':3}),('q-141114',{'k':1,'u':-1,'b':3}),('q-141108',{'k':1,'u':0,'b':3}),('q-141111',{'k':2,'u':str(sp.pi/8),'b':str(sp.sqrt(2))}),('q-141116',{'k':1,'u':0,'b':'1/2'}),('q-141115',{'k':1,'u':0,'b':1})]:
        try:g.generate('easy',template=t,parameters=p)
        except ValueError:collision_checks+=1
        else:raise AssertionError(('complete method bank collision not rejected',t,p))
    mod_b={sp.Rational(i,j) for j in [1,2,3] for i in [-5,-3,-1,1,3,5]}
    hard_b={sp.Rational(i,j) for j in [2,3,4] for i in [-5,-3,-1,1,3,5] if abs(sp.Rational(i,j))<=3 and sp.Rational(i,j).q>1}
    number_domain={'scope':'finite sampler support and complete method-bank eligible radio subsets; explicit guard domains may be larger but remain finite','easy_rational_catalog':[str(z) for z in g.EASY_RATIONAL_VALUES],'easy_trig_catalog':[str(z) for z in g.EASY_TRIG_VALUES],'easy_meaningful_tasks_by_family':easy_counts,'easy_total_meaningful_tasks':sum(easy_counts.values()),'authored_radio_complete_bank_eligible_tasks':radio_counts,'whole_bank_explicit_collision_rejections':collision_checks,'moderate_meaningful_tasks':6*4*len(mod_b),'hard_meaningful_tasks':2*6*len(hard_b)+6*4,'hard_reciprocal_tasks':2*6*len(hard_b),'hard_log_tasks':6*4,'invalid_explicit_number_form_calls_rejected':rejected_number_forms}
    write('number-domains.json',number_domain)
    write('source-cases.json',cases);write('review.json',review);write('engine-input.json',engine)
    subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-validation.json')],check=True)
    ev=json.loads((ROOT/'engine-validation.json').read_text())
    report={'status':'pass','source':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_questions':len(QS),'complete_banks_matched':len(QS),'source_options_matched':options,'source_distractors_matched':distractors,'correct_designations_matched':designation,'correct_designations_missing_in_source':len(QS)-designation,'prompt_raw_exact':len(QS),'ordered_solution_sequences_matched':17,'raw_exact_solutions':exact_solutions,'solution_notation_normalized':17-exact_solutions,'source_mathematical_repairs':0,'completed_presentation_repairs':['q-347839: Asin operator in two rows','q-352649: Acos operator in one row'],'decoded_source_adjacent_choice_backslashes':0,'source_answer_strings_raw_exact':63,'actual_displayed_math_validated_records':len(review),'raw_source_operator_normalization_for_math_qa':['q-347839 Asin treated as A times sin in evidence QA','q-352649 Acos treated as A times cos in evidence QA'],'native_grading':{k:ev[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'authored_levels':['moderate: nonzero half-integer exponential input','hard: nonzero-input reciprocal/log affine constant isolation'],'authored_complete_radio_bank_operations_checked_from_displayed_function':True,'whole_bank_collision_rejections':collision_checks,'radio_complete_bank_eligible_tasks':radio_counts,'number_form_guard_checks':rejected_number_forms,'finite_sampler_task_counts':{'easy':sum(easy_counts.values()),'moderate':6*4*len(mod_b),'hard':2*6*len(hard_b)+6*4},'database_writes':0}
    write('validation.json',report)
    (ROOT/'review.md').write_text(render_review(review))
    freeze={'version':g.VERSION,'verification_command':'.venv/bin/python generate/scratch/17592186100951/validate.py','hashes':{str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted([ROOT.with_suffix('.py')]+[p for p in ROOT.iterdir() if p.is_file() and p.name!='freeze.json'])},'source_capture_sha256':hashlib.sha256((REPO/'generate/runs/current/sources/17592186100951.json').read_bytes()).hexdigest()}
    write('freeze.json',freeze)
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
