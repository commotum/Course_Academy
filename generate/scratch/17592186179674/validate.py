#!/usr/bin/env python3
"""Fail-closed checks of actual displayed curves, one-forms, every math stage,
full observed banks/layouts, native grading, domains, guards and identities."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as s
E=Path(__file__).resolve().parent;SCRIPT=E.with_suffix('.py')
spec=importlib.util.spec_from_file_location('cartesian_oneform',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
p=g.PARSER;X,Y,T=p.x,p.y,p.t
MATH=re.compile(r'\$\$(.*?)\$\$|\$([^$]*)\$',re.S)
def blocks(text):return [(m[1] if m[1] is not None else m[2]).strip() for m in MATH.finditer(text)]
def eq(a,b):return s.simplify(s.trigsimp(a-b))==0
def scalar(raw):
    raw=raw.strip().rstrip('.,')
    raw=re.sub(r'\\sqrt\[3\]\{([^{}]*)\}',r'(\1)^{\\frac{1}{3}}',raw)
    return g.scalar(raw.replace('[','(').replace(']',')'))
def group(raw,start,opening='{',closing='}'):
    assert raw[start]==opening,raw;depth=1;i=start+1
    while depth:
        assert i<len(raw),raw;depth+=(raw[i]==opening)-(raw[i]==closing);i+=1
    return raw[start+1:i-1],i

def path(solution):
    bs=blocks(solution);parameter=bs[1] if bs[0].startswith('y=') else next(b for b in bs if b.startswith(r'\begin{aligned}r(t)'))
    body=parameter.split('=',2)[-1].split(r'\end{aligned}')[0]
    match=re.search(r',\\,t\\in \[(.*?),(.*?)\]',body);assert match,body
    u,v=map(scalar,match.groups());assert u<v
    V=p.vector(body[:match.start()]);return tuple(V[:2]),(u,v)

def form(prompt):
    bs=blocks(prompt);curve=next(z for z in bs if z.startswith('y='));relation=scalar(curve.split('=',1)[1])
    endpts=[]
    for z in bs:
        mt=re.match(r'[ABPQ]\((.*),(.*)\)',z)
        if mt:endpts.append(tuple(map(scalar,mt.groups())))
    assert len(endpts)==2
    one=next(z for z in bs if r'\int' in z).removesuffix('=')
    # Read the actual outer uniform scale in evidence replay.
    scale=1
    mt=re.match(r'(\d+)\\left\((.*)\\right\)$',one,re.S)
    if mt:scale=int(mt[1]);one=mt[2]
    marker=re.search(r'\{?\\int\s*\}?\s*_\{?C\}?',one);assert marker,one
    body=one[marker.end():].replace(r'\,','')
    if body==r'\frac{dx+dy}{y}':P,Q=1/Y,1/Y
    else:
        assert body.endswith('dy'),body;body=body[:-2]
        first,second=body.split('dx',1);assert second.startswith('+'),body
        P,Q=scalar(first),scalar(second[1:]) if second[1:] else s.Integer(1)
    return relation,endpts,scale*P,scale*Q

def clean_symbolic(raw,path):
    dx,dy=map(lambda z:s.diff(z,T),path)
    for axis,val in [('x',dx),('y',dy)]:
        raw=raw.replace(r'\frac{\text{d}'+axis+r'}{\text{d}t}', '('+g.tex(val)+')')
    raw=raw.replace(r'\,\text{d}t','').replace(r'\text{d}t','').replace(r'\,dt','').replace('dt','')
    return scalar(raw).subs({X:path[0],Y:path[1]},simultaneous=True)

def stage_value(rhs,path,interval,multiplier=1):
    rhs=rhs.strip().rstrip('.,')
    # Strip no-op grouping introduced by parameterized source scaling.
    mt=re.match(r'(\d+)\\left\((.*)\\right\)$',rhs,re.S)
    if mt:return int(mt[1])*stage_value(mt[2],path,interval,multiplier*int(mt[1]))
    mt=re.search(r'\{?\\int\s*\}?_',rhs)
    if mt:
        prefix=rhs[:mt.start()];factor=scalar(prefix) if prefix else 1
        at=mt.end();assert rhs[at]=='{',rhs;lo,at=group(rhs,at);assert rhs[at]=='^';at+=1;hi,at=group(rhs,at)
        lo,hi=scalar(lo),scalar(hi);assert (lo,hi)==interval
        f=clean_symbolic(rhs[at:],path)
        assert eq(multiplier*factor*f,CURRENT_INTEGRAND),('pointwise displayed integrand',rhs,f,CURRENT_INTEGRAND)
        # Pointwise equality + equal limits proves the integral row. The
        # independent displayed-prompt reference is integrated once per task.
        return CURRENT_VALUE/multiplier
    rhs=rhs.replace(r'\left[','[').replace(r'\right]',']')
    # Source antiderivative evaluation wrappers: {[F]}_a^b and [F]_a^b.
    if re.search(r'\]\}?_',rhs):
        start=rhs.index('[');end=rhs.rfind(']');f=scalar(rhs[start+1:end]);tail=rhs[end+1:].lstrip('}')
        assert tail.startswith('_');at=1;lo,at=group(tail,at);assert tail[at]=='^';hi,at=group(tail,at+1)
        assert at==len(tail),tail
        prefix=rhs[:start].rstrip('{');factor=scalar(prefix) if prefix else 1
        lo,hi=scalar(lo),scalar(hi);assert (lo,hi)==interval
        assert eq(multiplier*factor*s.diff(f,T),CURRENT_INTEGRAND),('antiderivative derivative',rhs,CURRENT_INTEGRAND)
        return factor*(f.subs(T,hi)-f.subs(T,lo))
    return scalar(rhs)

CURRENT_INTEGRAND=None
CURRENT_VALUE=None

def inspect(record,allow_ambiguity=False):
    global CURRENT_INTEGRAND,CURRENT_VALUE
    q=record['question'];prompt=q[':question/problem'];solution=q[':question/worked-solution']
    assert set(record['knowledge_point'])=={'db_id','id','title'}
    assert record['knowledge_point']['db_id']==g.KP_ID
    curve,A,P,Q=form(prompt);(xt,yt),interval=path(solution);u,v=interval
    # Nonnegative root branch, verified at all endpoints/interior samples.
    residual=s.refine(curve.subs(X,xt)-yt,s.Q.nonnegative(T))
    assert eq(residual,0),(curve,xt,yt,residual)
    for bound,point in zip(interval,A):assert all(eq(z.subs(T,bound),a) for z,a in zip((xt,yt),point))
    PP=s.simplify(P.subs({X:xt,Y:yt},simultaneous=True));QQ=s.simplify(Q.subs({X:xt,Y:yt},simultaneous=True))
    f=s.expand(PP*s.diff(xt,T)+QQ*s.diff(yt,T));CURRENT_INTEGRAND=f
    # Detect interior/endpoint poles from the actual composed scalar expression.
    den=s.denom(s.cancel(f));roots=s.solveset(den,T,domain=s.Interval(u,v))
    assert roots is s.S.EmptySet,('composed poles',f,roots)
    if P.has(s.cos) and u==0:
        assert record['generation']['profile']=='raw_observed' or 'one-sided continuous extension' in prompt
        assert eq(s.limit(f,T,u,dir='+'),f.subs(T,u))
    true=s.simplify(s.integrate(f,(T,u,v)));CURRENT_VALUE=true
    # Source derivative vectors and all actual displayed evaluation stages.
    derivative=next(z for z in blocks(solution) if 'r}^{′}' in z)
    actual=p.vector(derivative.split('=')[-1].split(r'\end{aligned}')[0].rstrip('.'))
    assert all(eq(z,s.diff(w,T)) for z,w in zip(actual,(xt,yt)))
    evaluation=[z for z in blocks(solution) if r'\begin{aligned}' in z and r'\int' in z][-1]
    rows=evaluation.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}')[0].split(r'\\')
    for row in rows:
        assert '=' in row,row;rhs=row.split('=',1)[1]
        try:val=stage_value(rhs,(xt,yt),interval)
        except Exception as ex:raise AssertionError(('stage parse',row,str(ex))) from ex
        assert eq(val,true),('displayed stage incorrect',row,val,true)
    fields=q[':question/answer-fields'];assert len(fields)==1;field=fields[0]
    assert field[':answer-field/type']==':answer-field.type/radio';assert field[':answer-field/key']=='selection';assert len(field[':answer-field/choices'])==5
    cid=field[':answer-field/correct'][1];ans=field[':answer-field/choices'];vals=[scalar(a[':answer/value']) for a in ans]
    truths=[a[':answer/id'] for a,val in zip(ans,vals) if eq(val,true)]
    assert truths==[cid],(truths,cid,true)
    assert allow_ambiguity or all(not eq(a,b) for i,a in enumerate(vals) for b in vals[i+1:])
    assert all(v.is_real and not v.has(s.zoo,s.oo,s.nan) for v in vals)
    # Normal records use valid grouped TeX, balanced math delimiters, scalar math.
    for text in [prompt,solution]+[a[':answer/value'] for a in ans]:
        assert text.count('$')%2==0
        depth=0
        for mt in re.finditer(r'(?<!\\)[{}]',text):
            depth+=1 if mt[0]=='{' else -1;assert depth>=0,text
        assert depth==0,text
    return len(rows)


def main():
    assert set(g.FAMILIES.values())==set(g.SOURCE_QUESTIONS)
    counts=dict(source_questions=11,source_values=55,source_designations=11,raw_exact_prompts=0,raw_exact_solutions=0,raw_exact_values=0,raw_banks_replayed=0,valid_raw_banks=10,repaired_valid_banks=11,repaired_original_value_matches=54,authored_questions=0,displayed_math_rows=0,native_checks=0)
    cases=[];reviews=[];fixtures=[]
    for name,sid in g.FAMILIES.items():
        level=g.TEMPLATES[name]['level'];case={'source_id':sid,'template':name,'level':level,'parameters':{'scale':1},'bank_profile':'raw_observed'};cases.append(case)
        raw=g.generate(level,template=name,parameters=case['parameters'],profile='raw_observed');q=raw['question'];old=g.SOURCE_QUESTIONS[sid]
        counts['displayed_math_rows']+=inspect(raw,allow_ambiguity=name=='sqrt_linear')
        assert q[':question/problem']==old[':question/problem'];counts['raw_exact_prompts']+=1
        assert q[':question/worked-solution']==old[':question/worked-solution'];counts['raw_exact_solutions']+=1
        actual=sorted(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']);original=sorted(a[':answer/value'] for a in old[':question/answer-fields'][0][':answer-field/choices'])
        assert actual==original
        field=q[':question/answer-fields'][0]
        assert next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1])==old[':question/answer-fields'][0][':answer-field/correct'][':answer/value']
        assert len(q[':question/answer-fields'])==len(old[':question/answer-fields'])
        assert len(g.source_parts(old)[1])==len([b for b in blocks(q[':question/worked-solution']) if r'\int' in b][-1].split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0].split(r'\\'))
        counts['raw_exact_values']+=5;counts['raw_banks_replayed']+=1
        reviews.append({'label':'Original raw evidence '+sid,'record':raw})
        repaired=g.generate(level,template=name,parameters={'scale':1},profile='observed_repaired');counts['displayed_math_rows']+=inspect(repaired);reviews.append({'label':'Observed replay with documented corrections '+sid,'record':repaired});fixtures.extend([raw,repaired])
        for scale in (2,3):
            replay=g.generate(level,template=name,parameters={'scale':scale},profile='observed_repaired');counts['displayed_math_rows']+=inspect(replay);reviews.append({'label':'Generated observed-profile scaling '+sid,'record':replay})
            fixtures.append(replay)
    for name,t in g.TEMPLATES.items():
        identities=set();tasks=set()
        for seed in range(12):
            r=g.generate(t['level'],seed,template=name);counts['displayed_math_rows']+=inspect(r);counts['authored_questions']+=1
            if seed<2:reviews.append({'label':'Generated authored '+t['level']+' '+name,'record':r})
            fixtures.append(r);identities.add(r['question'][':question/id']);tasks.add(r['generation']['math_task_fingerprint'])
            fixed=g.generate(t['level'],seed+100,template=name,parameters=r['generation']['parameters'])
            assert fixed['question'][':question/id']==r['question'][':question/id']
            assert fixed['generation']['math_task_fingerprint']==r['generation']['math_task_fingerprint']
        assert len(tasks)>=5,(name,len(tasks))
    # Same actual task across source-scale and authored layouts; complete bank
    # belongs to content identity, never the mathematical fingerprint.
    source=g.generate('moderate',template='parabola_xy',parameters={'scale':2},profile='observed_repaired')
    authored=g.generate('moderate',template='parabola_xy',parameters={**g.BASE['parabola_xy'],'a':2,'b':2})
    assert source['generation']['math_task_fingerprint']==authored['generation']['math_task_fingerprint']
    assert source['question'][':question/id']!=authored['question'][':question/id']
    widget_capture=json.loads((E/'widget-evidence.json').read_text())
    for widget in widget_capture['captured_relevant_original_widgets']:
        original=g.SOURCE_QUESTIONS['q-'+widget['question_id']][':question/answer-fields'][0][':answer-field/choices']
        values=[scalar(c['readable_text'].removeprefix('[MATH: ').removesuffix(']')) for c in widget['choices']]
        assert len(values)==5 and all(any(eq(scalar(a[':answer/value']),v) for a in original) for v in values)
    # Scope/domain boundaries are applied to explicit parameters too.
    rejected=[]
    for name,change in [('easy_xy',{'v':2}),('parabola_xy',{'v':1}),('cubic_recip',{'u':0}),('trig_sin',{'d':1}),('cuberoot_exp',{'v':2}),('hard_poly',{'a':0}),('sqrt_poly',{'v':3}),('shift_log',{'h':-1})]:
        p={**g.BASE[name],**change}
        try:g.generate(g.TEMPLATES[name]['level'],template=name,parameters=p)
        except ValueError:rejected.append([name,change])
        else:raise AssertionError(('accepted invalid explicit domain',name,p))
    (E/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
    (E/'review.json').write_text(json.dumps(reviews,indent=2,ensure_ascii=False)+'\n')
    lines=['# Review: Cartesian-curve one-form integrals','Raw originals retain captured evidence. Generated records label observed-pattern replays or authored method banks. The duplicate wrong option in q-124664 is evidence-only.']
    for entry in reviews:lines+=['\n## '+entry['label'],g.markdown(entry['record'])]
    (E/'review.md').write_text('\n\n'.join(lines)+'\n')
    payload=[]
    for i,r in enumerate(fixtures):
        f=r['question'][':question/answer-fields'][0];cid=f[':answer-field/correct'][1]
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'all five complete-bank owned IDs'} for a in f[':answer-field/choices']]
        payload.append({'label':str(i)+' '+r['generation']['template'],'record':r,'checks':checks});counts['native_checks']+=5
    (E/'engine-input.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([str(E.parents[1]/'runs/current/check-engine'),str(E/'engine-input.json'),str(E/'engine-report.json')],check=True)
    out={'status':'passed with explicit source repairs','script_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'counts':counts,'invalid_domains_rejected':rejected,'source_anomalies':['q-124664 contains equivalent wrong values 6 and 42/7; raw replay evidence only, repaired one value to 53/12 by omitting source common factor 2','q-90871 has undefined one-form at initial x=0; composed integrand has finite one-sided limit, normal observed/default prompt states this interpretation','captured answer banks contain overescaped TeX and invisible function application markers; normal profiles normalize these without mathematical changes'],'original_distractor_intent':'unresolved; scalar expression-pattern profiles are replay-only uniform one-form scaling, not default error banks','provenance':{'sympy':s.__version__,'source_sha256':hashlib.sha256((E/'source.json').read_bytes()).hexdigest(),'native_grader_sha256':hashlib.sha256((E.parents[1]/'runs/current/check-engine').read_bytes()).hexdigest(),'printed_expression_parser_sha256':hashlib.sha256((E.parents[1]/'runs/current/vector-math-parser.py').read_bytes()).hexdigest()},'database_writes':0}
    (E/'validation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
