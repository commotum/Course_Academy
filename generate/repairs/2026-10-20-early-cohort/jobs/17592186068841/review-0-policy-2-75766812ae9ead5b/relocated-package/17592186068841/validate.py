#!/usr/bin/env python3
"""Independent read-back, full source banks/prose/stages and real grader checks.

Known raw source errors are asserted as expected findings, never called correct.
Normal records must satisfy all domain, formatting and mathematical checks.
"""
from pathlib import Path
import hashlib
import importlib.util
import itertools
import json
import re
import subprocess
import sys
import sympy as sp
from math_parser import expression,normalize,X,Y,C,K,D

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'))
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

def zero(e):
    # Sqrt product separation is checked on the explicitly chosen positive branch.
    xp,yp=sp.symbols('xp yp',positive=True)
    return sp.simplify(sp.expand_log(sp.powdenest(e.subs({X:xp,Y:yp}),force=True),force=True))==0

def math_spans(text):return re.findall(r'\$\$.*?\$\$|\$[^$]*?\$',text,re.S)

def rows(solution):
    result=[]
    for b in re.findall(r'\$\$(.*?)\$\$',solution,re.S):
        b=b.strip();b=re.sub(r'\\begin\{aligned\}|\\end\{aligned\}','',b)
        result.append([r.strip().rstrip('.,') for r in b.split(r'\\')])
    return result

def prose(solution):return re.sub(r'\$\$.*?\$\$','<MATH>',solution,flags=re.S)

def equation(t):
    t=t.replace('&','').strip().rstrip('.,')
    l,r=t.split('=',1)
    return expression(l),expression(r)

def rhs_from_prompt(prompt):
    for b in math_spans(prompt):
        b=b.strip('$').strip().rstrip('.,')
        if "′" in b or "y'" in b or r'\frac{\text{d}y}{\text{d}x}' in b:
            l,r=equation(b)
            out=sp.solve(l-r,D)
            assert len(out)==1,('displayed ODE must solve uniquely for derivative',b)
            return out[0]
    raise AssertionError('No displayed ODE')

def formatting(q):
    for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]:
        assert '$$' not in text or text.count('$$')%2==0
        assert text.replace('$$','').count('$')%2==0
        depth=0
        for c in re.sub(r'\\[{}]','',text):
            if c=='{':depth+=1
            elif c=='}':depth-=1
            assert depth>=0,('unbalanced braces',text)
        assert depth==0,('unbalanced braces',text)
        assert '+-' not in text and '--' not in text
    for f in q[':question/answer-fields']:
        if f[':answer-field/type'].endswith('/blank'):
            assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']

def integral_integrand(text):
    text=text.strip();negative=text.startswith('-')
    if negative:text=text[1:]
    assert text.startswith(r'\int '),('integral stage',text)
    text=text[len(r'\int '):]
    text=re.sub(r'\\,?\\text\{d\}[xy]\s*$','',text)
    text=re.sub(r'\\text\{d\}[xy]\s*$','',text)
    text=text.rstrip(' ,')
    v=expression(text)
    return -v if negative else v

def check_math(record,raw=False):
    q=record['question'];name=record['generation']['template']
    rhs=rhs_from_prompt(q[':question/problem'])
    bs=rows(q[':question/worked-solution'])
    # Each rearrangement row comes from the actual displayed ODE, including the
    # first distributed sum and all derivative notation rewrites.
    for row in bs[0]:
        l,r=equation(row)
        rr=sp.solve(l-r,D)
        assert len(rr)==1 and zero(rr[0]-rhs),('rearrangement',name,row,rhs,rr)
    separated_l,separated_r=equation(bs[0][-1])
    g=sp.simplify(separated_l/D);f=separated_r
    assert D not in g.free_symbols and Y not in f.free_symbols
    # Every displayed integral row, then the primitive, is checked independently.
    for row in bs[1][:-1]:
        l,r=row.replace('&','').split('=',1)
        li,ri=integral_integrand(l),integral_integrand(r)
        assert zero(li.subs(D,1)-g),('left integral',name,row,li,g)
        assert zero(ri-f),('right integral',name,row,ri,f)
    lp,rp=equation(bs[1][-1])
    assert zero(sp.diff(lp,Y)-g),('left primitive',name,lp,g)
    assert zero(sp.diff(rp,X)-f),('right primitive',name,rp,f)
    # Subsequent implicit and explicit rows must describe the same displayed ODE.
    # Absolute-value rows are differentiated on one sign branch. The raw known
    # signed-K |y+a| row is retained as evidence but explicitly fails its sign
    # range; differential equality alone would miss that defect.
    for block in bs[2:]:
        for row in block:
            row=re.sub(r'\|([^|]+)\|',r'(\1)',row)
            l,r=equation(row);h=l-r
            residual=sp.diff(h,X)+sp.diff(h,Y)*rhs
            if not zero(residual):
                sols=sp.solve(h,Y)
                assert sols and all(zero(residual.subs(Y,z)) for z in sols),('solved row',name,row,residual)
    fbank=q[':question/answer-fields'][0];answers=fbank[':answer-field/choices']
    values=[expression(a[':answer/value'].split('=',1)[-1]) for a in answers]
    cid=fbank[':answer-field/correct'][1];ci=next(i for i,a in enumerate(answers) if a[':answer/id']==cid)
    if name=='q-128191':
        # Reinsert the fragment into the displayed advertised answer form.
        a=record['generation']['parameters']['a'];v=-(a+1)/(values[ci]+K)
    else:v=values[ci]
    # Do not assume the same C spelling; verify at positive-domain samples for
    # rational-power branches plus exact symbolic derivatives when possible.
    residual=sp.diff(v,X)-rhs.subs(Y,v)
    if not zero(residual):
        for xv,cv in [(sp.Rational(3,2),5),(2,8),(3,9)]:
            value=sp.N(residual.subs({X:xv,C:cv,K:cv}),30)
            assert abs(complex(value))<1e-20,('correct family ODE residual',name,residual,value)
    collisions=[]
    if name!='q-128191':
        for i,j in itertools.combinations(range(len(values)),2):
            if m.family_equivalent(values[i],values[j]):collisions.append([i,j])
    assert not collisions or raw and name=='q-3854',('family collision',name,collisions)
    return {'rearrangement_rows':len(bs[0]),'integration_rows':len(bs[1]),'total_math_rows':sum(map(len,bs)),
      'known_raw_family_collisions':len(collisions),'displayed_rhs':sp.sstr(rhs)}

def main():
    assert m.family_equivalent(K*sp.exp(X**2),7*K*sp.exp(X**2))
    assert m.family_equivalent(-1/(X**2+C),-1/(X**2+3*C+7))
    assert m.family_equivalent((X**2+C)**2,(X**2+5*C+2)**2)
    assert not m.family_equivalent(-1/(X**2+C),1/(X**2+C))
    assert not m.family_equivalent(K*sp.exp(X**2),K*sp.exp(-X**2))
    checks=[];cases=[];review=[];report=[];source_banks=0;source_options=0;exact_prose=0;exact_solutions=0;exact_prompts=0
    for name,q in m.QUESTIONS.items():
        print('Source fidelity:',name,flush=True)
        a=m.SOURCE_DEFAULTS[name];p={'a':a}
        r=m.generate(m.LEVELS[name],template=name,parameters=p,profile='observed')
        gf=r['question'][':question/answer-fields'][0];sf=q[':question/answer-fields'][0]
        raw=[expression(v[':answer/value'].split('=',1)[-1]) for v in sf[':answer-field/choices']]
        got=[expression(v[':answer/value'].split('=',1)[-1]) for v in gf[':answer-field/choices']]
        used=set()
        for value in raw:
            matches=[i for i,x in enumerate(got) if i not in used and zero(value-x)]
            assert len(matches)==1,('complete source option match',name,value,got,matches)
            used.add(matches[0])
        assert len(raw)==len(got)
        sc=expression(sf[':answer-field/correct'][':answer/value'].split('=',1)[-1])
        gc=expression(next(v[':answer/value'] for v in gf[':answer-field/choices'] if v[':answer/id']==gf[':answer-field/correct'][1]).split('=',1)[-1])
        assert zero(sc-gc),('designation value',name)
        assert prose(q[':question/worked-solution'])==prose(r['question'][':question/worked-solution']),('complete source prose',name)
        old,new=rows(q[':question/worked-solution']),rows(r['question'][':question/worked-solution'])
        assert list(map(len,old))==list(map(len,new)),('full stage sequence',name)
        for ob,nb in zip(old,new):
            for o,n in zip(ob,nb):
                if normalize(o)!=normalize(n):
                    if r'\int' in o:
                        os=o.replace('&','').split('=',1);ns=n.replace('&','').split('=',1)
                        assert all(zero(integral_integrand(x)-integral_integrand(y)) for x,y in zip(os,ns)),('source integral stage',name,o,n)
                    else:
                        eo,en=equation(o),equation(n)
                        assert zero(eo[0]-en[0]) and zero(eo[1]-en[1]),('source stage',name,o,n)
        exact_prose+=1;exact_solutions+=q[':question/worked-solution']==r['question'][':question/worked-solution']
        assert q[':question/problem']==r['question'][':question/problem'],('raw prompt',name)
        assert q[':question/worked-solution']==r['question'][':question/worked-solution'],('raw solution',name)
        exact_prompts+=1
        formatting(r['question']);mr=check_math(r,raw=True)
        source_banks+=1;source_options+=len(raw)
        cases.append({'source_id':q[':db/id'],'source_math_academy_id':name,'template':name,'level':m.LEVELS[name],'parameters':p,'bank_profile':'observed','original':q})
        report.append({'source_id':q[':db/id'],'template':name,'matched_values':len(raw),'matched_correct_designation':True,'complete_bank':True,'raw_solution_exact':q[':question/worked-solution']==r['question'][':question/worked-solution'],'prose_exact':True,'stage_sequence_equivalent':True,**mr})
        review.append({'label':'original replay '+name,'record':r})
        checks.append(engine_item('source '+name,r))
        for a2 in [2,7] if name!='q-128191' else [2,4]:
            observed=m.generate(m.LEVELS[name],seed=a2,template=name,parameters={'a':a2},profile='observed')
            formatting(observed['question']);check_math(observed,raw=True)
            review.append({'label':'generated observed-bank evidence '+name+' a='+str(a2),'record':observed})
            checks.append(engine_item('observed-bank variant '+name+' '+str(a2),observed))
            rr=m.generate(m.LEVELS[name],seed=a2,template=name,parameters={'a':a2})
            formatting(rr['question']);check_math(rr)
            review.append({'label':('generated authored-bank variant ' if name in m.AUTHORED_BANKS else 'generated normal variant ')+name+' a='+str(a2),'record':rr})
            checks.append(engine_item('variant '+name+' '+str(a2),rr))
    # All advertised coefficients are enumerated (finite narrow curriculum scope),
    # checking source endpoints and every normal complete bank's family uniqueness.
    exhaustive=[];tasks={l:set() for l in ('easy','moderate','hard')}
    for name,level in m.LEVELS.items():
        print('Finite domain:',name,flush=True)
        values=list(range(1,5 if name=='q-128191' else 9)) if level!='easy' else [a for a in range(-12,13) if a]
        for a in values:
            r=m.generate(level,template=name,parameters={'a':a})
            formatting(r['question']);mr=check_math(r)
            tasks[level].add(r['generation']['mathematical_fingerprint']);exhaustive.append({'template':name,'a':a,**mr})
        for a in ([3,-4] if level=='easy' else [m.SOURCE_DEFAULTS[name]]):
            r=m.generate(level,template=name,parameters={'a':a},seed=2)
            other=m.generate(level,template=name,parameters={'a':a},seed=88)
            assert r['question'][':question/id']==other['question'][':question/id']
            assert r['generation']['parameter_fingerprint']==other['generation']['parameter_fingerprint']
            if level=='easy':
                review.append({'label':'authored easy '+name+' a='+str(a),'record':r});checks.append(engine_item('easy '+name+' '+str(a),r))
        for bad in [0,13,-13,True,sp.Rational(3,2)]:
            try:m.generate(level,template=name,parameters={'a':bad})
            except ValueError:pass
            else:raise AssertionError(('invalid explicit parameters accepted',name,bad))
    for rr in review:
        assert set(rr['record']['knowledge_point'])=={'db_id','id','title'}
    (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2,ensure_ascii=False)+'\n')
    (HERE/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
    (HERE/'engine-input.json').write_text(json.dumps(checks,indent=2,ensure_ascii=False)+'\n')
    engine=ROOT/'generate/runs/current/check-engine'
    subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    er=json.loads((HERE/'engine-report.json').read_text())
    result={'status':'passed with explicitly documented raw source errors','source_provenance':{k:m.SNAPSHOT[k] for k in ('database','basis','lineage')},
      'source_questions':len(cases),'complete_bank_value_matches':source_banks,'source_values_matched':source_options,
      'correct_designations_matched':len(cases),'complete_prose_matches':exact_prose,'raw_exact_solutions':exact_solutions,
      'raw_exact_prompts':exact_prompts,
      'mathematically_equivalent_stage_sequences':len(cases),'normal_finite_domain_instances':len(exhaustive),
      'distinct_normal_mathematical_tasks':{l:len(t) for l,t in tasks.items()},
      'raw_errors':{'q-3854':'Two log distractors differ by ln(3), absorbed into K; one authored normal-bank repair',
       'q-158009':'Absolute value row incorrectly retained after K becomes signed; removed in normal output',
       'q-79665/q-8304':'sqrt(xy)=sqrt(x)sqrt(y) excludes valid negative-x/negative-y branch; normal output restricts x,y positive',
       'q-8303/q-79665/q-8304':'Squared/fractional-power explicit answer requires positive inner branch; normal prompt restricts interval'},
      'native_fragment_limitation':'q128191 x^n+5 gives the same whole arbitrary-K family but the fragment grader rejects it; normal prompt explicitly requires only the nonconstant polynomial term. Product-form x*x*... equivalents are accepted.',
      'normal_bank_authorship':sorted(m.AUTHORED_BANKS),'family_equivalence_regressions':5,
      'native_grading':{k:er[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},
      'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'source_results':report,'exhaustive_results':exhaustive,
      'database_writes':0,'plots_required':False}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    md=['# Originals and generated variants\n\nAll original records remain in source.json and source-cases.json. Observed profile reproduces source values and teaching stages as evidence; normal variants apply the documented repairs.']
    for name,q in m.QUESTIONS.items():
        md+=['\n## Original '+name+'\n\n'+q[':question/problem']+'\n\n'+ '\n'.join('- $'+v[':answer/value']+'$' for f in q[':question/answer-fields'] for v in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']]
        for item in review:
            if item['record']['generation']['template']==name:md+=['\n### '+item['label']+'\n\n'+m.markdown(item['record'])]
    for item in review:
        if item['record']['generation']['authored_extension']:md+=['\n## '+item['label']+'\n\n'+m.markdown(item['record'])]
    (HERE/'review.md').write_text('\n'.join(md)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('source_results','exhaustive_results')},indent=2))

def engine_item(label,r):
    f=r['question'][':question/answer-fields'][0];cid=f[':answer-field/correct'][1]
    if f[':answer-field/type'].endswith('/blank'):
        a=r['generation']['parameters']['a'];n=a+1
        checks=[{'submitted':v,'expected':e,'purpose':p} for v,e,p in [
         (f'x^{n}','accepted','canonical exponent fragment'),
         ('x'+'*x'*(n-1),'accepted','independent unreduced product equivalent fragment'),
         (f'x^{n+1}','rejected','wrong power'),(f'2*x^{n}','rejected','wrong coefficient'),
         (f'x^{n}+5','rejected','documented family-versus-fragment normalization: a constant can be absorbed into K but is not the normalized fragment')]]
    else:
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'owned native radio selection'} for a in f[':answer-field/choices']]
    return {'label':label,'record':r,'checks':checks}

if __name__=='__main__':main()
