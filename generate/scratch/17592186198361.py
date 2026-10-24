#!/usr/bin/env python3
"""Performing a Change of Variables; source math basis 1356, local review only.

Seven practice sources, five rated (four easy setup families, one moderate
nonlinear evaluation). Public observed profiles retain missing source attributes
and anomalous banks as evidence; normal output always has a derived correct ref.
Easy keeps the original four operative setup sequences and additionally completes
an unrated sum/difference setup. Moderate evaluates xy under u=y/x²,v=xy.
Authored hard evaluates (xy)² with the SAME supplied transformation, requiring
cubic instead of quadratic endpoint arithmetic. Transformations are always given:
inferring a transformation belongs to the neighboring knowledge points.
Rectangle bounds vary, affecting the assessed transformed limits or arithmetic.
All choices are complete banks, rejected together on full-value equivalence.
This script does not transact or import database clients and needs no new plots.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186198361
KP_UUID='9fed8ac2-8d21-5bc9-b1cc-df20760cfbfb'
TITLE='Performing a Change of Variables'
VERSION='change-variables-3'
HERE=Path(__file__).with_suffix('')
TEMPLATES=json.loads((HERE/'templates.json').read_text())
RAW=json.loads((HERE/'source.json').read_text())
x,y,u,v=sp.symbols('x y u v',positive=True)
EASY=('difference','triangular_quadratic','product','exponential','sum_square')
LEVELS={**{n:'easy' for n in EASY},'ratio_product':'moderate','ratio_product_squared':'hard','sum_product_evidence':'moderate'}
MATRICES={'difference':[[1,1],[-1,1]],'triangular_quadratic':[[2,1],[0,1]],'product':[[-1,1],[1,1]],'exponential':[[2,5],[1,3]],'sum_square':[[1,1],[-1,1]]}
INTEGRANDS={'difference':y*y-x*x,'triangular_quadratic':2*x*y+x*x,'product':8*x*y,'exponential':sp.exp(x+y),'sum_square':3*(x+y)**2}

def tex(z):
    return sp.latex(sp.sympify(z)).replace(r'\log',r'\ln')
def wrap(z):return '('+tex(z)+')'
def uid(z):return str(uuid.uuid5(uuid.UUID(KP_UUID),z))
def digest(z):return hashlib.sha256(json.dumps(z,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def dump(z):return {k:(str(val) if isinstance(val,sp.Basic) else val) for k,val in z.items()}
def filled(t,p):
    for k,val in p.items():t=t.replace('@@'+k+'@@',str(val))
    if '@@' in t:raise ValueError('unfilled complete component slot')
    return t

def visible_sets(text):
    # Source outer set braces are TeX groups; normal output needs visible glyphs.
    starts=list(re.finditer(r'(?<!\\)\{\([xu],\s*[yv]\)',text))
    for match in reversed(starts):
        start=match.start();depth=1;end=start+1
        while depth:
            if text[end]=='{' and text[end-1]!='\\':depth+=1
            elif text[end]=='}' and text[end-1]!='\\':depth-=1
            end+=1
        text=text[:start]+r'\{'+text[start+1:end-1]+r'\}'+text[end:]
    return text

def check_bounds(level,p,template,raw=False):
    if set(p)!= {'ul','uh','vl','vh'}:raise ValueError('exactly ul,uh,vl,vh required')
    if any(type(z)!=int for z in p.values()):raise ValueError('bounds must be integers')
    if not(-4<=p['ul']<p['uh']<=(16 if template.startswith('ratio_product') else 8) and -4<=p['vl']<p['vh']<=10):raise ValueError('bound workload outside [-4,10]')
    if level=='easy' and not raw and (p['vh']>8 or p['uh']-p['ul']>5 or p['vh']-p['vl']>5):raise ValueError('easy bound widths at most5, endpoints -4 through8')
    if template.startswith('ratio_product'):
        if p['ul']!=1 or p['uh'] not in (4,9,16) or not(1<=p['vl']<p['vh']<=8):raise ValueError('nonlinear bounds: u in [1,4|9|16], v positive integers through8')
        if level=='hard' and p['vh']>6:raise ValueError('hard cubic endpoint ceiling 6')

def integrate_rectangle(expr,p,order='uv'):
    """Exact elementary rectangular moments; no floating sampling or answer lookup."""
    expr=sp.powsimp(sp.sympify(expr),force=True)
    exponentials=list(expr.atoms(sp.exp))
    if exponentials:
        if len(exponentials)!=1:raise ValueError('one separable exponential required')
        term=exponentials[0];arg=sp.expand(term.args[0]);a=arg.coeff(u);b=arg.coeff(v)
        coefficient=sp.simplify(expr/term)
        if coefficient.has(u,v) or sp.simplify(arg-a*u-b*v)!=0:raise ValueError('not separable linear exponential')
        def epart(c,lo,hi):return (sp.exp(c*hi)-sp.exp(c*lo))/c if c else sp.Integer(hi-lo)
        return coefficient*epart(a,p['ul'],p['uh'])*epart(b,p['vl'],p['vh'])
    total=0
    for term in sp.Add.make_args(sp.expand(expr)):
        powers=term.as_powers_dict();a=powers.get(u,0);b=powers.get(v,0);coefficient=sp.cancel(term/u**a/v**b)
        if coefficient.has(u,v):raise ValueError('nonseparable authored moment')
        def moment(n,lo,hi):
            return sp.log(sp.Rational(hi,lo)) if n==-1 else sp.Rational(hi**(n+1)-lo**(n+1),n+1)
        total+=coefficient*moment(a,p['ul'],p['uh'])*moment(b,p['vl'],p['vh'])
    return sp.expand_log(total,force=True)

def integral(z,p,order='uv'):
    outer,inner=('v','u') if order=='uv' else ('u','v')
    return (r'{\int }_{'+str(p[outer+'l'])+'}^{'+str(p[outer+'h'])+'}'+r'{\int }_{'+str(p[inner+'l'])+'}^{'+str(p[inner+'h'])+'}'+tex(z)+r'\,d'+inner+r'\,d'+outer)

def mathematical_data(template,p):
    if template in MATRICES:
        mat=sp.Matrix(MATRICES[template]);inv=mat.inv()*sp.Matrix([u,v]);j=mat.det()
        f=INTEGRANDS[template];sub=sp.expand(f.subs({x:inv[0],y:inv[1]},simultaneous=True))
        # Preserve exp exponent collection rather than polynomial expansion machinery.
        sub=sp.simplify(sub)
        return dict(matrix=mat,inverse=inv,jacobian=j,integrand=f,substitution=sub,correct=sp.expand(sub/abs(j)))
    if template.startswith('ratio_product'):
        f=(x*y)**(2 if template.endswith('squared') else 1)
        jac=sp.det(sp.Matrix([[sp.diff(y/x**2,x),sp.diff(y/x**2,y)],[sp.diff(x*y,x),sp.diff(x*y,y)]]))
        return dict(jacobian=jac,integrand=f,substitution=v**(2 if template.endswith('squared') else 1),correct=v**(2 if template.endswith('squared') else 1)/(3*u))
    return dict(jacobian=y-x,integrand=sp.Abs(y-x)*sp.exp(x*y))

def ratio_chain(p,power=1):
    """Ten operative source rows; each evaluation is a separate node, not CAS collapsed."""
    a,b,c,d=[p[k] for k in ('ul','uh','vl','vh')];root=int(sp.sqrt(b));ln=rf'\operatorname{{ln}}⁡{root}'
    n=power+1;vs='v' if power==1 else '{v}^{2}';fs='xy' if power==1 else '(xy)^{2}'
    logdiff=rf'\operatorname{{ln}}⁡{b}-\operatorname{{ln}}⁡{a}'
    q=sp.Rational(2,n*3);coef=(r'\frac{'+str(q.p)+r'\operatorname{ln}⁡'+str(root)+'}{'+str(q.q)+'}') if q.p!=1 else (r'\frac{\operatorname{ln}⁡'+str(root)+'}{'+str(q.q)+'}')
    final=tex(sp.Rational(2*(d**n-c**n),3*n)*sp.log(root)).replace(r'\ln{\left('+str(root)+r' \right)}',r'\operatorname{ln}⁡'+str(root))
    # This spelling exactly matches the observed original; no literal source-payload branch.
    final=final.replace(' '+r'\operatorname',''+r'\operatorname')
    rows=[rf'{{∬}}_{{Δ}}{vs}|\frac{{∂(x,y)}}{{∂(u,v)}}|\text{{d}}u\,\text{{d}}v',
          rf'{{∬}}_{{Δ}}{vs}\cdot |\frac{{1}}{{3u}}|\,\text{{d}}u\,\text{{d}}v',
          rf'\frac{{1}}{{3}}{{\int }}_{{{c}}}^{{{d}}}{{\int }}_{{{a}}}^{{{b}}}\frac{{{vs}}}{{u}}\,\text{{d}}u\,\text{{d}}v',
          rf'\frac{{1}}{{3}}{{\int }}_{{{c}}}^{{{d}}}{vs}[{{\int }}_{{{a}}}^{{{b}}}\frac{{1}}{{u}}\,\text{{d}}u]\text{{d}}v',
          rf'\frac{{1}}{{3}}{{\int }}_{{{c}}}^{{{d}}}{vs}[\operatorname{{ln}}⁡|u|\,{{|}}_{{{a}}}^{{{b}}}]dv',
          rf'\frac{{1}}{{3}}{{\int }}_{{{c}}}^{{{d}}}{vs}({logdiff})\,dv',
          rf'\frac{{2\operatorname{{ln}}⁡{root}}}{{3}}{{\int }}_{{{c}}}^{{{d}}}{vs}\,dv',
          rf'\frac{{2\operatorname{{ln}}⁡{root}}}{{3}}\cdot \frac{{1}}{{{n}}}{{v}}^{{{n}}}\,{{|}}_{{{c}}}^{{{d}}}',
          rf'{coef}\cdot ({d**n}-{c**n})',final]
    return (rf'\begin{{aligned}}{{∬}}_{{D}}{fs}\,dx\,dy & ='+r' \\  & ='.join(rows)+r'.\end{aligned}'),final

def normal_solution(template,p):
    if template=='difference':
        # No source solution exists: completed from the shared formal four-step teaching route.
        m=mathematical_data(template,p)
        return common_completed_solution(template,p,m)
    if template=='ratio_product_squared':
        source=TEMPLATES['ratio_product'];chain,result=ratio_chain(p,2)
        values={**p,'ulcoef':'','chain':chain,'result':result}
        return filled(source[':question/worked-solution'],values).replace('as follows::','as follows:')
    source=TEMPLATES[template];values={**p,'ulcoef':''}
    if template=='ratio_product':values['chain'],values['result']=ratio_chain(p)
    solution=filled(source[':question/worked-solution'],values)
    return solution.replace('as follows::','as follows:')

def common_completed_solution(template,p,m):
    j=m['jacobian'];inv=m['inverse'];mat=m['matrix'];f=m['integrand'];z=m['substitution']
    return ("Let's define a transformation $T$ as follows:\n\n"+
      r'$$T:\begin{bmatrix}u\\v\end{bmatrix}\longmapsto\begin{bmatrix}x(u,v)\\y(u,v)\end{bmatrix}$$'+
      '\n\nThis transformation maps some region $Δ$ in the $uv$-plane to our region $D$ in the $xy$-plane.\n\n'+
      'To compute the required integral, we can use the change of variables formula\n\n'+
      r'$$\iint_D f(x,y)\,dx\,dy=\iint_Δ f(x(u,v),y(u,v))\left|\frac{∂(x,y)}{∂(u,v)}\right|\,du\,dv.$$'+
      '\n\nThe supplied change of variables gives us the inverse function $T^{-1}$.\n\n'+
      '**Step 1**: Find $Δ,$ which is the image of $D$ under the action of $T^{-1}$.\n\n'+
      rf'$$Δ=\{{(u,v):{p["ul"]}\le u\le {p["uh"]},\ {p["vl"]}\le v\le {p["vh"]}\}}.$$'+
      '\n\n**Step 2**: Compute the Jacobian determinant corresponding to $T^{-1}$.\n\n'+
      rf'$$\frac{{∂(u,v)}}{{∂(x,y)}}=\begin{{vmatrix}}\frac{{∂u}}{{∂x}}&\frac{{∂u}}{{∂y}}\\\frac{{∂v}}{{∂x}}&\frac{{∂v}}{{∂y}}\end{{vmatrix}}=\begin{{vmatrix}}1&1\\-1&1\end{{vmatrix}}={j}.$$'+
      '\n\n**Step 3**: Compute the Jacobian determinant corresponding to $T$.\n\n'+
      rf'$$\frac{{∂(x,y)}}{{∂(u,v)}}=\left(\frac{{∂(u,v)}}{{∂(x,y)}}\right)^{{-1}}={tex(1/j)}.$$'+
      '\n\nNote that the Jacobian determinant is nonzero everywhere inside $Δ$.\n\n'+
      '**Step 4**: Perform the change of variables.\n\nIn this case, we first need to solve the transformation equations for $x$ and $y$, which gives\n\n'+
      rf'$$x={tex(inv[0])},\qquad y={tex(inv[1])}.$$'+
      '\n\nPerforming the change of variables, we obtain\n\n'+
      r'$$\begin{aligned}\iint_D(y^2-x^2)\,dx\,dy&=\iint_Δ\left[\left(\frac{u+v}{2}\right)^2-\left(\frac{u-v}{2}\right)^2\right]\left|\frac{∂(x,y)}{∂(u,v)}\right|\,du\,dv\\&=\iint_Δuv\left|\frac12\right|\,du\,dv\\&='+
      integral(m['correct'],p,'vu')+r'.\end{aligned}$$')

def ratio_answer_tex(value,p):
    # The solution evaluates ln(uh) as 2 ln(sqrt(uh)); keep that same base
    # throughout the bank instead of independently reducing ln(4) to ln(2).
    root=int(sp.sqrt(p['uh']))
    coefficient=sp.simplify(value/sp.log(root))
    assert coefficient.is_Rational
    return tex(coefficient*sp.Symbol(r'\ln('+str(root)+')'))

def bank(template,p,profile):
    data=mathematical_data(template,p)
    if profile=='observed':
        source=TEMPLATES[template];vals={**p,'ulcoef':''}
        if template=='ratio_product':vals['chain'],vals['result']=ratio_chain(p)
        if template=='sum_product_evidence':
            a,b,c,d=[p[k] for k in ('ul','uh','vl','vh')]
            vals.update(dict(s0=tex(d-c)+rf'(e^{{{b-a}}} - e^{{{a}}})',s1=tex(d-c)+rf'(e^{{{b}}} - e^{{{a}}})',s2=tex(d)+rf'(e^{{{b}}} - 1)',s3=tex(sp.Rational(d,2))+rf'(1 - e^{{{b-a}}})',s4=tex(sp.Rational(d,2))+rf'(e^{{{b}}} - 1)'))
            # Unit lower exponent is the source e spelling, not e^{1}.
            vals={k:(val.replace('e^{1}','e') if isinstance(val,str) else val) for k,val in vals.items()}
        return [filled(z,vals) for z in source['choices']],source['correct_index'],[]
    correct=data['correct']
    if template in EASY:
        sub=data['substitution'];j=abs(data['jacobian']);order='vu' if template in ('difference','sum_square') else 'uv'
        if template=='difference':wrongs=[sub,sub*j,-correct,(u*u-v*v)/2];labels=['omit_inverse_jacobian','use_forward_jacobian','retain_negative_area','difference_instead_of_product']
        elif template=='triangular_quadratic':
            inv=data['inverse'];badx=(u+v)/2
            wrongs=[sub,sub*j,sp.expand((2*badx*v+badx**2)/j),sp.expand((2*inv[0]*v)/j)];labels=['omit_inverse_jacobian','use_forward_jacobian','wrong_sign_in_inverse_x','omit_x_squared']
        elif template=='product':wrongs=[sub,sub*j,(v-u)**2,(v+u)**2];labels=['omit_inverse_jacobian','use_forward_jacobian','replace_conjugate_product_by_square_difference','replace_conjugate_product_by_square_sum']
        elif template=='exponential':
            # Source-complete bank is defensible as exponent collection patterns, but intention uncertain.
            wrongs=[2*sp.exp(3*u-2*v),sp.exp(2*u-v),sp.exp(u+v),sp.exp(3*u-2*v)/2];labels=['swapped_exponent_coefficients_and_double','drop_two_v_terms','treat_x_plus_y_as_u_plus_v','swapped_exponent_coefficients_and_half']
        else:wrongs=[6*u*u,sp.Rational(3,2)*(u+v)**2,sp.Rational(3,4)*(u+v)**2,sp.Rational(9,2)*u*u];labels=['forward_jacobian','wrong_sum_substitution','wrong_sum_and_extra_half','duplicate_integrand_coefficient']
        exprs=[correct]+wrongs
        return [integral(z,p,order) for z in exprs],0,list(zip(['correct']+labels,exprs))
    power=2 if template.endswith('squared') else 1
    wrongs=[v**power/u,-v**power/(3*u),1/(3*u),v**(power+1)/(3*u)]
    exprs=[correct]+wrongs;labels=['correct','omit_three_in_jacobian','signed_jacobian','omit_integrand_v_power','extra_v_factor']
    values=[ratio_answer_tex(integrate_rectangle(z,p),p) for z in exprs]
    values[0]=ratio_chain(p,power)[1]
    return values,0,list(zip(labels,exprs))

def eligible(values):
    # Exact equality in the transcendental E field, with familiar logarithms reduced.
    formal_e=sp.Symbol('formal_e',positive=True)
    canonical=[]
    for z in values:
        z=sp.expand_log(z,force=True)
        z=z.xreplace({term:formal_e**term.args[0] for term in z.atoms(sp.exp) if term.args[0].is_Integer})
        canonical.append(sp.cancel(z))
    return all(sp.cancel(a-b)!=0 for i,a in enumerate(canonical) for b in canonical[:i])

def sample(level,template,rng):
    if template.startswith('ratio_product'):
        a=1;b=rng.choice([4,9,16]);ceiling=6 if level=='hard' else 8;c=rng.randint(1,ceiling-1);d=rng.randint(c+1,ceiling)
    else:
        a=rng.randint(-4,7);b=a+rng.randint(1,min(5,8-a));c=rng.randint(-4,7);d=c+rng.randint(1,min(5,8-c))
    return dict(ul=a,uh=b,vl=c,vh=d)

# EASY: supplied linear maps; preserve original quadratic/exponential substitution stages.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: supplied y/x²,xy; separate v/u and evaluate logarithm plus quadratic endpoints.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('moderate',seed,template,field_type,parameters,profile)
# HARD (authored): supplied SAME nonlinear map; v²/u adds cubic endpoint arithmetic, no new topic.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('hard',seed,template,field_type,parameters,profile)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio only')
    if profile not in (None,'authored','observed'):raise ValueError('unknown complete bank profile')
    rng=random.Random(seed);template=template or rng.choice(EASY if level=='easy' else ['ratio_product' if level=='moderate' else 'ratio_product_squared'])
    if template not in LEVELS or LEVELS[template]!=level:raise ValueError('template/level scope mismatch')
    profile=profile or 'authored';raw=profile=='observed'
    if raw and template not in TEMPLATES:raise ValueError('no observed profile for authored hard')
    if template=='sum_product_evidence' and not raw:raise ValueError('two-branch invalid-domain historical evidence only')
    for attempt in range(500):
        p=dict(parameters) if parameters is not None else sample(level,template,rng)
        check_bounds(level,p,template,raw)
        choices,correct,recipes=bank(template,p,profile)
        data=mathematical_data(template,p)
        if recipes:
            full=[integrate_rectangle(z,p) for _,z in recipes]
            if not eligible(full):
                if parameters is not None:raise ValueError('whole bank rejected: equivalent complete mathematical values')
                continue
        break
    else:raise ValueError('could not sample eligible complete bank')
    if template=='ratio_product_squared':
        base=TEMPLATES['ratio_product'];prompt=filled(base[':question/problem'],{**p,'ulcoef':''}).replace('{∬}_{D}xy','{∬}_{D}(xy)^{2}')
    else:
        base=TEMPLATES[template];prompt=filled(base[':question/problem'],{**p,'ulcoef':''})
    # Preserve source raw key presence. Completed normal originals remain authored repairs.
    q={':question/problem':prompt}
    if raw:q[':question/math-academy-id']=base['math_academy_id']
    if not raw or base['level'] is not None:q[':question/difficulty']=':question.difficulty/'+level
    if raw:
        if ':question/worked-solution' in base:
            vals={**p,'ulcoef':''}
            if template=='ratio_product':vals['chain'],vals['result']=ratio_chain(p)
            q[':question/worked-solution']=filled(base[':question/worked-solution'],vals)
    else:
        prompt=visible_sets(prompt);q[':question/problem']=prompt
        q[':question/worked-solution']=visible_sets(normal_solution(template,p))
    # Sorted banks give order-independent content identity; metadata aliases cannot change it.
    content=dict(version=VERSION,level=q.get(':question/difficulty'),problem=prompt,solution=q.get(':question/worked-solution'),bank=sorted(choices),correct=None if correct is None else choices[correct])
    identity=digest(content);qid=uid('question/'+identity);fid=uid(qid+'/selection')
    answers=[{':answer/id':uid(fid+'/'+value),':answer/type':':answer.type/math',':answer/value':value} for i,value in enumerate(choices)]
    field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
    if correct is not None:field[':answer-field/correct']=[':answer/id',answers[correct][':answer/id']]
    rng.shuffle(answers)
    q[':question/id']=qid;q[':question/answer-fields']=[field]
    task=digest(dict(template=template,level=level,integrand=str(data['integrand']),bounds=p,transformation=str(data.get('matrix','u=y/x²,v=xy'))))
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'difficulty':level,'template':template,'profile':profile,'parameters':p,'source':{'database':RAW['database'],'basis':RAW['basis'],'lineage':RAW['lineage']},'source_id':base['source_id'],'authored':not raw,'evidence_only':raw,'eligible_for_learning':not raw,'mathematical_fingerprint':task,'content_fingerprint':identity,'recipes':[label for label,_ in recipes],'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'plot_rating':'none'}}

def markdown(record):
    q=record['question'];out=q[':question/problem']+'\n\n'
    for a in q[':question/answer-fields'][0][':answer-field/choices']:out+='- $'+a[':answer/value']+'$\n'
    if ':question/worked-solution' in q:out+='\n'+q[':question/worked-solution']+'\n'
    return out

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile',choices=['authored','observed'])
    args=parser.parse_args();levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in levels for i in range(args.count)]
    print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
