#!/usr/bin/env python3
"""Independent displayed-math validation and native learner-engine fixtures."""
import importlib.util, json, re, hashlib, subprocess, sys
from functools import lru_cache
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('ivp',HERE.with_suffix('.py')); g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x=g.x; Y=sp.Symbol('y'); D=sp.Symbol('D'); C=g.C

def clean(s):
    return s.replace('\\\\frac','\\frac').replace('\\\\operatorname','\\operatorname').replace('\\u2061','').replace('⁡','').replace('\u2061','')

def group(s,i):
    while i<len(s) and s[i].isspace():i+=1
    assert s[i]=='{',(s,i)
    start=i+1; depth=1;i+=1
    while depth:
        if s[i]=='{':depth+=1
        if s[i]=='}':depth-=1
        i+=1
    return s[start:i-1],i

def parse(s):
    s=clean(s).strip().rstrip('.').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\!','')
    s=re.sub(r'\\operatorname\{(sin|cos|ln)\}',lambda m:'\\'+m.group(1),s)
    s=re.sub(r'\\ln\{x\}\^\{(\d+)\}',r'\\ln(x^{\1})',s)
    s=s.replace(r'\dfrac',r'\frac').replace(r'\tfrac',r'\frac')
    while r'\frac' in s:
        i=s.index(r'\frac'); a,j=group(s,i+5);b,k=group(s,j);s=s[:i]+'(('+str(parse(a))+')/('+str(parse(b))+'))'+s[k:]
    for a,b in [(r'\cdot','*'),(r'\pi','pi'),(r'\sin',' sin '),(r'\cos',' cos '),(r'\ln',' log ')]:s=s.replace(a,b)
    s=s.replace('{','(').replace('}',')').replace('^','**')
    return parse_expr(s,local_dict={'x':x,'y':Y,'D':D,'C':C,'e':sp.E,'pi':sp.pi,'sin':sp.sin,'cos':sp.cos,'log':sp.log},transformations=standard_transformations+(implicit_multiplication_application,convert_xor),evaluate=True)

@lru_cache(maxsize=20000)
def equal(a,b):
    delta=sp.expand(a-b)
    if delta==0:return True
    if delta.is_zero is False:return False
    return sp.simplify(delta)==0

def displayed_problem(rec):
    prompt=clean(rec['question'][':question/problem'])
    math=re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)\$',prompt,re.S)
    ode=next((a or b) for a,b in math if 'dy' in a+b or r'\text{d}y' in a+b)
    ode=re.sub(r'\\frac\{\\text\{d\}y\}\{\\text\{d\}x\}|\\frac\{dy\}\{dx\}', 'D',ode)
    ode=ode.replace(r'\cdot','*').replace(r'\,','')
    initial=re.search(r'y\((.*?)\)\s*=\s*(-?\d+)',ode);assert initial,ode
    t=parse(initial.group(1));h=sp.Integer(initial.group(2))
    equation=ode[:initial.start()].rstrip(' ,').replace(r'\quad','').replace('x>0','').rstrip(' ,')
    lhs,rhs=equation.split('=',1); L=parse(lhs);Q=parse(rhs)
    coefficient=sp.expand(L).coeff(D); P=sp.expand(L).coeff(Y)/coefficient; Q=Q/coefficient
    assert equal(L,coefficient*D+coefficient*P*Y)
    return P,Q,t,h

def formatting(s):
    assert s.count('$$')%2==0
    s=s.replace('$$',''); assert s.count('$')%2==0
    depth=0
    for c in s:
        if c=='{':depth+=1
        elif c=='}':depth-=1
        assert depth>=0
    assert depth==0
    assert not re.search(r'(?<!\\)(?:\+\-|\-\-)',s)

def stage_expr(raw,general,particular,constant,initial=False):
    raw=clean(raw).strip().rstrip('.')
    raw=re.sub(r'\\frac\{\\text\{d\}y\}\{\\text\{d\}x\}', 'D',raw)
    marker=r'\frac{\text{d}}{\text{d}x}'
    if raw.startswith(marker):
        inner=raw[len(marker):].strip()
        assert inner.startswith('(') and inner.endswith(')'),raw
        return sp.diff(parse(inner[1:-1]).subs(Y,general),x)
    if raw=='I(x)': return None
    if raw.startswith('y(') and raw.endswith(')'):
        return general.subs(x,parse(raw[2:-1])).subs(C,constant)
    val=parse(raw).subs(Y,general).subs(D,sp.diff(general,x))
    if initial:val=val.subs(C,constant)
    return val

def check_printed_stages(solution,general,particular,m):
    checked=0
    for block in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S):
        previous=None
        for row in re.split(r'\\\\',block):
            if '&' not in row:continue
            left,right=row.split('&',1);left=left.strip();right=right.strip().removeprefix('=').rstrip('.')
            if left:previous=left
            else:left=previous
            if not left or r'\int' in left+right or 'P(x)' in left+right or 'Q(x)' in left+right:continue
            if left=='C':assert equal(parse(right),m['c']);checked+=1;continue
            if left=='I(x)':
                assert equal(parse(right),m['I']);checked+=1;continue
            initial=left.startswith('y(') or not ('y' in left or r'\frac{\text{d}}' in left)
            a=stage_expr(left,general,particular,m['c'],initial)
            b=stage_expr(right,general,particular,m['c'],initial)
            u=sp.Symbol('u'); b=b.subs(u,sp.integrate(m['P'],x))
            if left=='y' and not b.has(C):a=particular
            assert equal(a,b),(left,right,a,b)
            checked+=1
    return checked

def check_record(rec,allow_ambiguous=False):
    assert set(rec['knowledge_point'])=={'db_id','id','title'}
    q=rec['question'];gen=rec['generation'];fields=q[':question/answer-fields']
    g.generate_normal.__wrapped__ if False else None
    from scripts.question_capture.math_format import validate_generated_record
    validate_generated_record(rec)
    assert not any(ord(c)<32 and c not in '\n\t' for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for f in fields for a in f[':answer-field/choices']] for c in text)
    formatting(q[':question/problem']);formatting(q[':question/worked-solution'])
    P,Q,t,h=displayed_problem(rec)
    solutions=[]
    for i,f in enumerate(fields):
        assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
        choices=f[':answer-field/choices'];right=f[':answer-field/correct'][1]
        ids=[a[':answer/id'] for a in choices];assert len(ids)==len(set(ids))
        assert right in ids
        exprs=[parse(a[':answer/value']) for a in choices]
        correct=exprs[ids.index(right)]; solutions.append(correct)
        mathematically_correct=[]
        for z in exprs:
            ok=(equal(sp.diff(z,x),P*z) and z!=0) if i==0 else equal(sp.diff(z,x)+P*z,Q) and equal(z.subs(x,t),h)
            mathematically_correct.append(ok)
        assert mathematically_correct[ids.index(right)]
        assert sum(mathematically_correct)==1 or allow_ambiguous
        if not allow_ambiguous:
            assert len(set(map(sp.srepr,map(sp.simplify,exprs))))==len(exprs)
            for j,z in enumerate(exprs):
                for z2 in exprs[:j]:
                    assert not equal(z,z2)
                    if i==0:assert (ratio:=sp.simplify(z/z2)).has(x) or ratio==0
    # Verify displayed final solution and every printed algebraic y/C row.
    solution=q[':question/worked-solution']; particular=solutions[1]
    last=re.findall(r'\$\$(.*?)\$\$',solution,re.S)[-1]
    if r'\begin{aligned}' not in last:
        assert equal(parse(last.strip().removeprefix('y=').rstrip('.')),particular)
    f=gen['template']; family=g.TEMPLATES[f][1]; I=solutions[0];F=sp.integrate(I*Q,x);constant=sp.simplify(h*I.subs(x,t)-F.subs(x,t));m={'P':P,'Q':Q,'I':I,'F':F,'t':t,'h':h,'c':constant}
    general=(sp.integrate(m['I']*Q,x)+C)/m['I']
    assert equal(sp.diff(general,x)+P*general,Q)
    # Read every explicit y=... general/particular row back from the actual text.
    rows=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S)
    checked=0
    for block in rows:
        for row in re.split(r'\\\\',block):
            if '&' not in row:continue
            left,right=row.split('&',1);left=left.strip();right=right.strip().removeprefix('=').rstrip('.')
            if left=='y' and not (r'\int' in right):
                val=parse(right); assert equal(val,general if val.has(C) else particular),(left,right,val,general);checked+=1
            if left=='C':assert equal(parse(right),m['c']);checked+=1
            # Product/general-solution arithmetic rows, actual printed expressions.
            if left.startswith('y') and '(' not in left and '\\frac' not in left and left!='y' and '\\text' not in left and '\\int' not in right:
                lhs=parse(left).subs(Y,general);rhs=parse(right)
                if rhs.has(sp.Symbol('u')):continue
                assert equal(lhs,rhs),(left,right,lhs,rhs);checked+=1
    return checked+check_printed_stages(solution,general,particular,m)+formal_stages(solution,P,Q,m)

def prose(s):return re.sub(r'\$\$.*?\$\$|(?<!\$)\$(?!\$).*?\$', '<MATH>',s,flags=re.S)


def formal_expression(raw):
    raw=clean(raw).strip().rstrip('.')
    raw=raw.replace(g.D,'D')
    if raw.startswith(g.DX):
        inner=raw[len(g.DX):].strip();assert inner[0]=='(' and inner[-1]==')'
        z=parse(inner[1:-1]);return sp.diff(z,x)+sp.diff(z,Y)*D
    return parse(raw)

def all_rows(solution):
    return [re.split(r'\\\\',b) for b in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S)]

def formal_stages(solution,P,Q,m):
    n=0;I=m['I'];F=m['F'];general=(F+C)/I
    # Named definitions are read from their actual prose; metadata is not the oracle.
    for label,expected in [('P',P),('Q',Q)]:
        for match in re.finditer(r'\$'+label+r'\(x\)\s*=\s*(.*?)\$',solution):assert equal(parse(match[1]),expected);n+=1
    for rows in all_rows(solution):
        prior='';integral_count=0
        for row in rows:
            if '&' not in row:continue
            a,b=row.split('&',1);a=a.strip() or prior;prior=a;b=b.strip().removeprefix('=').rstrip('.')
            if a=='P(x)' and 'Q(x)=' in b:
                part,qpart=b.split(r',\,Q(x)=');assert equal(parse(part),P) and equal(parse(qpart),Q);n+=2;continue
            if a=='I(x)' and r'\int' in b:
                # The definition row is symbolic; following rows must use actual P.
                if 'P(x)' in b:n+=1;continue
                exponent=b[b.index('{')+1:b.rindex('}')]
                coefficient,integrand=exponent.split(r'\int',1)
                integrand=integrand.split(r'\,')[0].split(r'\text')[0].strip()
                assert equal((parse(coefficient) if coefficient.strip() else 1)*parse(integrand),P),(a,b,P);n+=1;continue
            if g.D in a and r'\int' not in a+b:
                left=formal_expression(a);right=parse(b)
                residual=sp.expand(left-right); original=D+P*Y-Q
                multiplier=sp.simplify(residual.coeff(D))
                assert multiplier!=0 and equal(residual,multiplier*original),(a,b,residual,original);n+=1
            elif a.startswith(g.DX) and r'\int' not in a+b:
                z=formal_expression(a);assert equal(z,I*D+sp.diff(I,x)*Y);assert equal(parse(b),I*Q);n+=1
            elif r'\int' in a+b and a!='I(x)':
                # Every x-integrand and substitution u-integrand is independently checked.
                if r'\int' in b:
                    v=b.split(r'\int',1)[1]
                    if r'\text{d}u' in v:
                        v=v.split(r'\,')[0].split(r'\text')[0];assert equal(parse(v).subs(sp.Symbol('u'),sp.integrate(P,x))*P,I*Q);n+=1
                    else:
                        v=v.split(r'\,')[0].split(r'\text')[0];assert equal(parse(v),I*Q);n+=1
                integral_count+=1
            elif a.startswith('y') and '(' not in a and a!='y' and r'\int' not in b:
                # Full primitive and arbitrary constant, not just its derivative.
                value=parse(b).subs(sp.Symbol('u'),sp.integrate(P,x))
                assert equal(value,F+C),(a,b,F+C)
                assert equal(sp.diff(value,C),1);n+=1
    return n

def operative_structure(rec):
    q=rec['question'];sol=q[':question/worked-solution'];family=g.TEMPLATES[rec['generation']['template']][1]
    groups=all_rows(sol)
    IF=next(rows for rows in groups if 'I(x)' in rows[0]);assert len(IF)==({'cosine':6,'nonstandard':6,'sine':4}.get(family,3))
    integral=next(rows for rows in groups if r'\int' in rows[0] and 'I(x)' not in rows[0]);assert len(integral)==({'constant':4,'quadratic':5,'cubic':5}.get(family,3))
    initial=next(rows for rows in groups if 'C &' in rows[-1]);assert len(initial)==3
    assert '(' in initial[0] and '=' in initial[1]
    substitution=initial[0].split('&',1)[1]
    if family in ('constant','quadratic','cubic','cancellation','trig_cancellation'):assert 'e^{' in substitution and '(0)' in substitution
    if family=='nonstandard':assert '(1)^2' in substitution
    if family=='cosine':assert r'\sin(' in substitution
    if family in ('sine','trig_cancellation'):assert r'\cos(' in substitution
    if family in ('quadratic','cubic'):
        assert r'\text{d}u' in integral[1] and 'e^u+C' in integral[2] and 'u' not in integral[3].split('&',1)[1]
    if family=='constant':assert r'\left(' in integral[1] and r'\cdot' in integral[1]
    if family in ('cosine','nonstandard'):assert r'\int (1/x)' in IF[2] and r'\ln' in IF[4] and 'x^2' in IF[4]
    if family=='sine':
        final=groups[-1];assert len(final)==3 and r'\frac{' in final[0] and final[1].count(r'\frac{')==2 and '{2x}' in final[2]
    if family=='nonstandard':
        standard=groups[0];assert len(standard)==3 and r'\frac{1}{x}' in standard[1]
    assert '\x0c' not in sol

def baseline_check():
    old=json.loads((HERE/'baseline.json').read_text());paths=[HERE.parent/'17592186087879.py']+sorted((HERE.parent/'17592186087879').rglob('*'));paths=[str(p.relative_to(g.ROOT)) for p in paths if p.is_file()]
    assert paths==old['pathset'],'Registered baseline path set changed'
    assert all(hashlib.sha256((g.ROOT/p).read_bytes()).hexdigest()==v for p,v in old['files'].items()),'Registered baseline bytes changed'
    return len(paths)

def raw_recipes(qid,p):
    h=sp.Integer(p['h']);e=sp.exp
    if qid=='q-334916':return [x,e(x),x**3,1/x],[1+(h-1)*e(x),1+(h-1)*e(-x),h*e(x),e(-x)+h-1,h*e(-x)]
    if qid=='q-335808':return [1/x,e(x*x/4),e(4*x),x**3],[2*x+h,e(2*x*x),2+(h-2)*e(x*x),2+(h-2)*e(-x*x/4),2*x*x+h]
    if qid=='q-335810':return [2*x,e(2*x),e(x),x*x],[(h+1)*x*x-(h-1)/x**2,x*x+(h-1)/x**2,x+(h-1)/x**2,(h+1)*x-(h-1)/x**2]
    if qid=='q-335811':
        v=p['k']*sp.sin(x);return [e(x*x),e(2*x),x*x,2*x],[x*x*v,v/x,v/x**2,v/x**2,x*v]
    if qid=='q-335812':return [1/x,e(x),x,sp.log(x)],[(h*sp.pi+3*sp.cos(x))/(2*x),(h*sp.pi+4*sp.cos(x))/(2*x),(h*sp.pi-sp.cos(x))/(2*x),(h*sp.pi-2*sp.cos(x))/(2*x),(h*sp.pi-2*sp.cos(x))/(2*x)]
    if qid=='q-335806':return [e(x),x,e(-x),x*x],[(x+h)*e(x),(x*x+h)*e(x),h*e(-x),(x+h)*e(-x),(x*x+h)*e(-x)]
    if qid=='q-335829':return [e(2*x),4*x,e(4*x),e(8*x)],[2+(h-2)*e(-4*x),1+(h-1)*e(-4*x),4+(h-4)*e(4*x),h*e(4*x),h*e(-4*x)]
    if qid=='q-339145':return [e(12*x),1/x,x**6,e(x*x/12)],[6+(h-6)*e(x*x),6*x+h,e(6*x*x),6*x*x+h,6+(h-6)*e(-x*x/12)]
    if qid=='q-335830':return [e(-2*x),-2*x,e(2*x),2*x],[e(-2*x)*(h-3+(h-1)*sp.cos(x)),h*e(-2*x)*(1+sp.cos(x))/2,e(2*x)*(h+1-sp.cos(x)),e(2*x)*(h-1+sp.cos(x)),h*e(2*x)*sp.cos(x)]
    raise ValueError(qid)

def check_raw_math(rec):
    ib,yb=raw_recipes(rec['generation']['template'],rec['generation']['parameters'])
    P,Q,t,h=displayed_problem(rec)
    out=[]
    for key,expected in [('field-1',ib),('field-2',yb)]:
        f=next(f for f in rec['question'][':question/answer-fields'] if f[':answer-field/key']==key)
        remaining=list(expected)
        for a in f[':answer-field/choices']:
            value=parse(a[':answer/value']);j=next((i for i,v in enumerate(remaining) if equal(value,v)),None);assert j is not None,(rec['generation']['template'],value,remaining);remaining.pop(j)
            out.append({'field_key':key,'displayed_raw_value':a[':answer/value'],'derived_symbolic_value':str(value),'recipe_status':'whole captured expression pattern; original intent unresolved where opaque'})
        assert not remaining
        if ':answer-field/correct' in f:
            z=parse(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]))
            assert (equal(sp.diff(z,x),P*z) if key=='field-1' else equal(sp.diff(z,x)+P*z,Q) and equal(z.subs(x,t),h))
    return out

def raw_check(rec,q):
    actual=rec['question'];assert rec['generation']['evidence_only'] and not rec['generation']['eligible']
    for key in (':question/problem',':question/worked-solution',':question/difficulty'):
        assert (key in q)==(key in actual)
        if key in q:assert actual[key]==(q[key][':db/ident'] if isinstance(q[key],dict) else q[key])
    assert len(q[':question/answer-fields'])==len(actual[':question/answer-fields'])
    for a,b in zip(q[':question/answer-fields'],actual[':question/answer-fields']):
        assert a[':answer-field/key']==b[':answer-field/key']
        assert a[':answer-field/type'][':db/ident']==b[':answer-field/type']
        assert sorted(x[':answer/value'] for x in a[':answer-field/choices'])==sorted(x[':answer/value'] for x in b[':answer-field/choices'])
        assert (':answer-field/correct' in a)==(':answer-field/correct' in b)
        if ':answer-field/correct' in a:assert next(x[':answer/value'] for x in b[':answer-field/choices'] if x[':answer/id']==b[':answer-field/correct'][1])==a[':answer-field/correct'][':answer/value']

def native_checks(rec):
    checks=[]
    for i,f in enumerate(rec['question'][':question/answer-fields']):
        for a in f[':answer-field/choices']:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Actual select-field owned designation (raw duplicates remain evidence-only)'})
    return checks

def diagnostics(rec):
    """Native expression checks are supplemental blank fixtures, never served layouts."""
    import copy
    clone=copy.deepcopy(rec);checks=[]
    for i,f in enumerate(clone['question'][':question/answer-fields']):
        f[':answer-field/type']=':answer-field.type/blank';a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);value=a[':answer/value'];z=parse(value)
        # Visible unreduced quotient is algebraically equivalent and nonidentical.
        if i==0:
            if z.func==sp.exp:
                half=sp.simplify(z.args[0]/2);alternative=r'e^{'+g.tex(half)+'+('+g.tex(half)+')}'
            else:alternative='x\\cdot x' if equal(z,x**2) else 'x+x-x'
        else:
            P,Q,t,h=displayed_problem(rec);IF=parse(next(a[':answer/value'] for a in rec['question'][':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']==rec['question'][':question/answer-fields'][0][':answer-field/correct'][1]));primitive=sp.integrate(IF*Q,x);constant=sp.simplify(h*IF.subs(x,t)-primitive.subs(x,t))
            family=g.TEMPLATES[rec['generation']['template']][1]
            if family in ('constant','quadratic','cubic'):
                b=sp.simplify(primitive/IF);half=-sp.integrate(P,x)/2
                alternative=g.tex(b)+'+('+g.tex(constant)+r')e^{'+g.tex(half)+'+('+g.tex(half)+')}'
            elif family in ('cosine','sine','nonstandard'):
                alternative=r'\frac{'+g.tex(primitive)+'}{'+g.tex(IF)+r'}+\frac{'+g.tex(constant)+'}{'+g.tex(IF)+'}'
            else:alternative=g.tex(sp.expand(z))
        assert equal(parse(alternative),z)
        checks.extend([{'field_index':i,'submitted':value,'expected':'accepted','purpose':'Diagnostic native math canonical value; no blank served'},
                       {'field_index':i,'submitted':alternative,'expected':'accepted','purpose':'Diagnostic native nonidentical unreduced equivalent function'},
                       {'field_index':i,'submitted':g.tex(z+1),'expected':'rejected','purpose':'Diagnostic native known-wrong function'}])
    return {'label':'expression diagnostic '+rec['generation']['template'],'record':clone,'checks':checks}

def native_split(native,fixtures):
    lookup={row['label']:row for row in fixtures};groups={name:{'accepted':0,'rejected':0,'unresolved':0} for name in ('normal_served_select','raw_captured_select','supplemental_blank_diagnostics')}
    for row in native['records']:
        fixture=lookup[row['label']];r=fixture['record'];blank=any(f[':answer-field/type']==':answer-field.type/blank' for f in r['question'][':question/answer-fields'])
        name='supplemental_blank_diagnostics' if blank else 'raw_captured_select' if r['generation']['evidence_only'] else 'normal_served_select'
        for check in row['checks']:groups[name][check['outcome']]+=1
    assert groups['normal_served_select']['unresolved']==0
    return groups

def main():
    import copy
    baseline=baseline_check();counts={'MA_originals':0,'raw_prompts_exact':0,'raw_solutions_exact':0,'fields':0,'raw_values_exact':0,'correct_refs_exact':0,'missing_correct_refs_preserved':0,'missing_solutions_preserved':0,'unrated_preserved':0};cases=[];review=[];fixtures=[];steps=0;raw_mapping=[]
    # Exact raw API coverage; no completion masquerades as a captured designation.
    for qid,(level,family,p,*_) in g.OBS.items():
        rec=g.generate(level,template=qid,parameters=p,profile='raw');q=g.QUESTIONS[qid];raw_check(rec,q)
        raw_mapping.append({'source_id':qid,'parameters':p,'values':check_raw_math(rec)})
        counts['MA_originals']+=1;counts['raw_prompts_exact']+=1;counts['raw_solutions_exact']+=(':question/worked-solution' in q);counts['missing_solutions_preserved']+=(':question/worked-solution' not in q);counts['unrated_preserved']+=(':question/difficulty' not in q)
        for f in q[':question/answer-fields']:
            counts['fields']+=1;counts['raw_values_exact']+=len(f[':answer-field/choices']);counts['correct_refs_exact']+=(':answer-field/correct' in f);counts['missing_correct_refs_preserved']+=(':answer-field/correct' not in f)
        cases.append({'source_id':qid,'template':qid,'level':level,'parameters':p,'profile':'raw','bank_profile':'raw','evidence_only':True});review.append({'label':'Exact raw original '+qid,'record':rec})
        if all(':answer-field/correct' in f for f in rec['question'][':question/answer-fields']):fixtures.append({'label':'Captured native '+qid,'record':rec,'checks':native_checks(rec)})
        # Original source grade including duplicate correct value distinction remains captured.
        changed=dict(p);changed['k']=2 if family=='cosine' else changed.get('k',1)
        if family!='cosine':
            if 'k' not in p:changed.pop('k',None)
            lo,hi=g.RAW_H[qid];changed['h']=next(h for h in range(lo,hi+1) if h!=p['h'] and (qid!='q-335830' or not h%2))
        var=g.generate(level,template=qid,parameters=changed,profile='raw');assert var['question'][':question/problem']!=rec['question'][':question/problem'];review.append({'label':'Parameterized raw evidence '+qid,'record':var});raw_mapping.append({'source_id':qid,'parameters':changed,'values':check_raw_math(var)})
    # Exact independent inventory coverage, not an original-template denominator.
    independent=json.loads((HERE/'independent-inventory.json').read_text());captured=[q for q in g.SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q]
    assert [r['record'] for r in independent['questions']]==captured
    slots={};tasks={};samples={};raw_maths=0
    # Every source-shaped family plus authored easy/canonical cubic; fixed formal controls.
    for template,(level,family) in g.TEMPLATES.items():
        print('Checking',template,flush=True);seen={key:set() for key in g.REQUIRED[family]};fps=set();samples[template]=0
        for seed in range(8):
            rec=g.generate(level,seed,template=template);steps+=check_record(rec);operative_structure(rec);samples[template]+=1;fps.add(rec['generation']['mathematical_fingerprint'])
            for key,value in rec['generation']['parameters'].items():seen[key].add(value)
            same=g.generate(level,seed+100,template=template,parameters=rec['generation']['parameters'],profile='method');assert same['question'][':question/id']==rec['question'][':question/id']
            assert same['generation']['content_sha256']==rec['generation']['content_sha256']
            if seed<2:review.append({'label':'Normal generated '+template+' seed '+str(seed),'record':rec});fixtures.append({'label':template+' '+str(seed),'record':rec,'checks':native_checks(rec)})
            if seed==0:fixtures.append(diagnostics(rec))
        tasks[template]=len(fps);slots[template]={k:sorted(v) for k,v in seen.items()};assert len(fps)>=6
    # Public defaults must include every eligible family; seed/order cannot alter IDs.
    default_coverage={}
    for level in ('easy','moderate','hard'):
        names=set()
        for seed in range(24):names.add(g.generate(level,seed)['generation']['template'])
        expected={t for t,v in g.TEMPLATES.items() if v[0]==level};assert names==expected,(level,names,expected);default_coverage[level]=sorted(names)
    rejected=0
    for template,(level,family) in g.TEMPLATES.items():
        p=g.generate(level,2,template=template)['generation']['parameters']
        for bad in (dict(p,h=7),dict(p,**{next(k for k in p if k!='h'):0})):
            try:g.generate(level,template=template,parameters=bad)
            except ValueError:rejected+=1
            else:raise AssertionError(('Bad parameter accepted',template,bad))
    boundary_passes=0;boundary_collisions=0
    for template,(level,family) in g.TEMPLATES.items():
        base=g.generate(level,2,template=template)['generation']['parameters']
        for key in base:
            options=(-6,0,6) if key=='h' and family=='cosine' else (-6,6) if key=='h' else (-4,-1) if key=='a' and family=='trig_cancellation' else (1,) if key=='a' and level=='easy' else (2,6) if key=='a' and family=='constant' else (2,6) if key=='d' and family=='quadratic' else (1,4) if key=='d' else (1,6)
            for value in options:
                pp=dict(base,**{key:value})
                try:rr=g.generate(level,17,template=template,parameters=pp)
                except ValueError:
                    assert pp['h']==0 or g.model(family,pp)['c']==0
                    boundary_collisions+=1;continue
                steps+=check_record(rr);operative_structure(rr);boundary_passes+=1
        # Structure mutations preserve algebraic equality but erase assessed operations.
    mutations=0
    for template in ('q-335829','q-335808','q-335810','q-335812'):
        level=g.TEMPLATES[template][0];rec=g.generate(level,2,template=template);bad=copy.deepcopy(rec);sol=bad['question'][':question/worked-solution'];groups=list(re.finditer(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S))
        match=(groups[0] if template=='q-335810' else groups[-1] if template=='q-335812' else next(m for m in groups if r'\int' in m[1] and 'I(x)' not in m[1]))
        rows=re.split(r'\\\\',match[1]);rows[1]=rows[0] if template=='q-335812' else rows[-1] if template=='q-335810' else rows[-2];bad['question'][':question/worked-solution']=sol[:match.start(1)]+r' \\ '.join(rows)+sol[match.end(1):]
        try:operative_structure(bad)
        except AssertionError:mutations+=1
        else:raise AssertionError('Structure mutation accepted')
    rec=g.generate('easy',2);bad=copy.deepcopy(rec);bad['question'][':question/worked-solution']+='\x0c'
    try:check_record(bad)
    except (AssertionError,ValueError):mutations+=1
    else:raise AssertionError('Control character accepted')
    rec=g.generate('hard',2,template='q-335808');bad=copy.deepcopy(rec);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('e^u+C','2e^u+C',1)
    try:check_record(bad)
    except AssertionError:mutations+=1
    else:raise AssertionError('Wrong primitive coefficient accepted')
    (HERE/'raw-bank-mapping.json').write_text(json.dumps(raw_mapping,indent=2,ensure_ascii=False)+'\n')
    (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(HERE/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n');(HERE/'review.md').write_text('# Original and parameterized source evidence / normal variants\n\n'+''.join('## '+r['label']+'\n\n'+g.markdown(r['record'])+'\n\n' for r in review))
    # Known current native restriction: equivalent exponential quotient.
    diagnostic=diagnostics(g.generate('hard',0,template='q-335808'));r=diagnostic['record'];mP,mQ,mt,mh=displayed_problem(r);IF=parse(next(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1]));prim=sp.integrate(IF*mQ,x);cc=sp.simplify(mh*IF.subs(x,mt)-prim.subs(x,mt));entry=r'\frac{('+g.tex(prim)+')+('+g.tex(cc)+')}{'+g.tex(IF)+'}'
    fixtures.append({'label':'Documented diagnostic exponential-quotient restriction','record':r,'checks':[{'field_index':1,'submitted':entry,'expected':'unresolved','purpose':'Equivalent whole function with nonzero exponential denominator; current native rules cannot prove it; diagnostic blank never served'}]})
    (HERE/'engine-input.json').write_text(json.dumps(fixtures,indent=2)+'\n');engine=g.ROOT/'generate/runs/current/check-engine';subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine.json')],check=True);native=json.loads((HERE/'engine.json').read_text())
    out={'status':'validated_draft_with_ineligible_raw_source_defects','basis':2275,'source_fidelity':counts,'independent_inventory_exact_records':len(captured),'normal_instances':samples,'distinct_sampled_tasks':tasks,'slot_coverage':slots,'default_family_coverage':default_coverage,'independent_displayed_rows_checked':steps,'invalid_explicit_inputs_rejected':rejected,'mutation_controls_rejected':mutations,'boundary_passes':boundary_passes,'boundary_whole_instance_rejections':boundary_collisions,'native':{k:v for k,v in native.items() if k!='records'},'native_by_contract':native_split(native,fixtures),'baseline_paths_unchanged':baseline_check(),'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'grader_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'raw_ineligible_findings':['q334916: omitted solution/two designations/unrated preserved','q335811/q335812: duplicate full correct functions preserved','q335830: wrong IF ±2x redundant under IF scalar-equivalence'],'database_writes':0}
    (HERE/'validation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
