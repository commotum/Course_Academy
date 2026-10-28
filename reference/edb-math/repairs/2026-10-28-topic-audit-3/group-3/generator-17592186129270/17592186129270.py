#!/usr/bin/env python3
"""Critical loci of spatial transformations, math basis 1356. No database writes.

Observed moderate: twelve complete independent Markdown/stage templates, thirteen
five-option historical banks. Their wrong-option intent is underdetermined;
observed profiles are explicitly evidence-only. A translation slot renderer
preserves each source's omitted rows, prose, fields and missing correct attribute.
Every algebraic component is translated, while coordinate/function/derivative
labels are protected. No literal-source-return or answer lookup branch exists.
Normal learning defaults use complete authored method banks, chosen before
sampling and rejected wholesale on collisions. Easy is authored diagonal;
moderate retains all twelve families plus a sparse product/linear block; hard uses three nonzero cofactors.
All ask for the critical locus, never just a Jacobian or an inverse Jacobian.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
from audit_runtime import asset_payload,normalize_question
from math_format import normalize_prose,normalize_tex
import argparse, copy, hashlib, json, platform, random, re, uuid, sys
from pathlib import Path
import sympy as sp

from math_format import normalize_prose, validate_generated_record

KP_ID=17592186129270
KP_UUID='4b4a31c6-01be-5b15-88f5-9150f350e944'
TITLE='Determining the Critical Points of a Transformation'
VERSION='critical-locus-2-audit9837'
HERE=Path(__file__).with_suffix('')
CAPTURE=json.loads((HERE/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in CAPTURE['record'][':knowledge-point/questions']}
U,V,W=sp.symbols('u v w', real=True)
VARS=(U,V,W)
OBSERVED=tuple(SOURCES)
TEMPLATES={'easy':('diagonal',),'moderate':('product_block',)+OBSERVED,'hard':('three_cofactors',)}
DOMAIN={'diagonal':'R^3','product_block':'R^3','three_cofactors':'R^3'}

def digest(x): return hashlib.sha256(json.dumps(asset_payload(x),sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(x): return str(uuid.uuid5(uuid.NAMESPACE_URL,'critical-locus:'+x))
def tex(e): return sp.latex(sp.sympify(e)).replace(r'\log',r'\ln')
def matrix(rows): return r'\begin{aligned}'+r' \\ '.join(' & '.join(map(str,row)) for row in rows)+r'\end{aligned}'
def display(x): return '$$\n'+x+'\n$$'
JLABEL=r'\frac{∂(x,y,z)}{∂(u,v,w)}'
FORMAL=matrix([[r'\frac{∂'+f+'}{∂'+v+'}' for v in ('u','v','w')] for f in ('x','y','z')])
OPENING='For a transformation \n\n'+display('T:['+matrix([['u'],['v'],['w']])+r']\to ['+matrix([[f+'(u,v,w)'] for f in ('x','y','z')])+'],')+'\n\nthe Jacobian determinant of $T,$ denoted $'+JLABEL+',$ is given by\n\n'+display(r'\begin{aligned}'+JLABEL+' & =|'+FORMAL+r'|.\end{aligned}')


def translate(text,p):
    """Compile complete math components; protect labels, never function arguments.

    The independent-coordinate translation has derivative one, so every original
    derivative/cofactor/evaluation node transforms without extra factors.
    """
    shifts=dict(zip('uvw',(p['h'],p['k'],p['l'])))
    # Coordinate-plane names are categorical components, not implicit products.
    plane_slots=[]
    def plane(m):
        raw=m.group(0); letters=m.group(1).replace(' ','').replace('-','')
        absent=next(v for v in 'uvw' if v not in letters)
        plane_slots.append(raw if not shifts[absent] else 'plane $'+absent+'='+str(shifts[absent])+'$')
        return 'ZZPLANESLOT'+str(len(plane_slots)-1)+'ZZ'
    text=re.sub(r'\$([uvw]{2}\s*-?)\$(?:-\s*|\s*)plane',plane,text)
    def math(m):
        full=m.group(0); n=2 if full.startswith('$$') else 1; part=full[n:-n]
        saved=[]
        def protect(mm): saved.append(mm.group(0));return 'ZZTOKEN'+str(len(saved)-1)+'ZZ'
        # Protect formal coordinate tuples, derivative labels, and input vector.
        part=re.sub(r'T:\[\\begin\{aligned\}u \\\\ v \\\\ w\\end\{aligned\}\]',protect,part)
        part=re.sub(r'\(u,v,w\)|∂[uvw]|\\[A-Za-z]+',protect,part)
        def slot(mm):
            v=mm.group(0); s=shifts[v]
            return v if s==0 else '('+v+('-'+str(s) if s>0 else '+'+str(-s))+')'
        part=re.sub(r'[uvw]',slot,part)
        for i,val in enumerate(saved):part=part.replace('ZZTOKEN'+str(i)+'ZZ',val)
        return '$'*n+part+'$'*n
    result=re.sub(r'\$\$.*?\$\$|\$[^$]*\$',math,text,flags=re.S)
    for i,value in enumerate(plane_slots):result=result.replace('ZZPLANESLOT'+str(i)+'ZZ',value)
    return result


def bounds(level,template,p):
    """The same guards apply to explicit inputs and samplers; no silent repair."""
    if template in OBSERVED:
        if level!='moderate' or set(p)!=set('hkl') or any(type(p[k]) is not int or abs(p[k])>3 for k in p):raise ValueError('Observed translations: moderate, integer h,k,l in [-3,3].')
    elif template=='diagonal':
        if level!='easy' or set(p)!={'h','axis'} or p['axis'] not in range(3) or type(p['h']) is not int or not 1<=abs(p['h'])<=5:raise ValueError('Easy requires nonzero integer shift of magnitude <=5, axis 0..2.')
    elif template=='product_block':
        if level!='moderate' or set(p)!=set('ab') or any(type(p[k]) is not int or not 2<=p[k]<=8 for k in 'ab') or p['a']==p['b'] or sp.gcd(p['a'],p['b'])!=1:raise ValueError('Moderate requires distinct coprime a,b in [2,8].')
    elif template=='three_cofactors':
        if level!='hard' or set(p)!=set('abcdk') or any(type(p[k]) is not int or not 1<=abs(p[k])<=4 for k in p):raise ValueError('Hard: nonzero signed integer a,b,c,d,k magnitude <=4.')
        a,b,c,d,k=(p[x] for x in 'abcdk')
        if a*c+b*d==0 or 1-b*k==0 or a*c==b*d:raise ValueError('Hard requires two unequal nonzero products, nonzero sum and numerator.')
    else:raise ValueError('Unknown template.')


def sample(level,t,rng):
    if t in OBSERVED:return dict(zip('hkl',[rng.randint(-3,3) for _ in range(3)]))
    if t=='diagonal':return {'h':rng.choice([i for i in range(-5,6) if i]),'axis':rng.randrange(3)}
    if t=='product_block':return {'a':rng.randint(2,8),'b':rng.randint(2,8)}
    return {k:rng.choice([i for i in range(-4,5) if i]) for k in 'abcdk'}


def authored(level,t,p):
    """Shared staged rendering preserves unevaluated signed cofactor operations."""
    if t=='diagonal':
        axis,h=p['axis'],p['h']; f=list(VARS);f[axis]=(VARS[axis]-h)**2
        correct=VARS[axis]-h
        other=[v for v in VARS if v!=VARS[axis]]
        bank=[correct,other[0]-h,other[1]-h,VARS[axis]+h,VARS[axis]]
        recipes=['correct','differentiate wrong coordinate 1','differentiate wrong coordinate 2','reverse input shift','omit input shift']
        loci=[f'The critical points lie on the plane ${tex(v)}=0.$' for v in bank]
    elif t=='product_block':
        a,b=p['a'],p['b'];f=[U*V,a*U+b*V,W]; correct=b*V-a*U
        bank=[correct,b*V+a*U,V-a*U,b*V-U,b*U-a*V]
        recipes=['correct','wrong cofactor sign','omit coefficient b','omit coefficient a','exchange held coordinates']
        loci=[f'The critical points lie on the plane ${tex(v)}=0.$' for v in bank]
    else:
        a,b,c,d,k=(p[x] for x in 'abcdk');f=[U+a*V+b*W,c*U**2+V,d*U**2+k*U+W]
        correct=1-2*a*c*U-b*(2*d*U+k)
        bank=[correct,1-b*(2*d*U+k),1-2*a*c*U,1+2*a*c*U-b*(2*d*U+k),-2*a*c*U-b*(2*d*U+k)]
        recipes=['correct','omit middle cofactor','omit last cofactor','wrong middle cofactor sign','omit constant cofactor']
        loci=[f'The critical points lie on the plane ${tex(sp.expand(v))}=0.$' for v in bank]
    # Entire preselected bank must be eligible; no replacement pool.
    norm=[]
    for e in bank:
        pol=sp.Poly(e,*VARS);coeff=pol.coeffs()[0];norm.append(sp.expand(e/coeff))
    if len(set(map(str,norm)))!=5:raise ValueError('Whole bank rejected: equivalent zero sets.')
    m=sp.Matrix(f).jacobian(VARS);det=sp.factor(m.det())
    prompt='Find the locations of all of the critical points of the transformation $T,$ where $T$ is defined as\n\n'+display('T:['+matrix([[v] for v in 'uvw'])+']⟶['+matrix([[tex(e)] for e in f])+'].')
    partial=matrix([[r'\frac{∂'+name+'}{∂'+str(v)+'} & ='+tex(m[i,j]) for j,v in enumerate(VARS)] for i,name in enumerate('xyz')])
    numeric='|'+matrix([[tex(m[i,j]) for j in range(3)] for i in range(3)])+'|'
    # Cofactor expansion chosen structurally, including every nonzero first-row entry.
    terms=[];eval_terms=[]
    for j in range(3):
        if m[0,j]==0:continue
        minor=m.minor_submatrix(0,j)
        coefficient=(-1)**j*m[0,j]
        terms.append('('+tex(coefficient)+')'+'|'+matrix([[tex(minor[i,k]) for k in range(2)] for i in range(2)])+'|')
        eval_terms.append('('+tex(coefficient)+')('+tex(minor[0,0])+r'\cdot('+tex(minor[1,1])+')-('+tex(minor[0,1])+r')\cdot('+tex(minor[1,0])+'))')
    rows=[JLABEL+' & ='+numeric,' & ='+'+'.join(terms),' & ='+'+'.join(eval_terms),' & ='+tex(det)+'.']
    solution=OPENING+'\n\nHere, we have \n\n'+display(r'\,'.join(name+'(u,v,w)='+tex(e)+',' for name,e in zip('xyz',f))[:-1]+'.')+'\n\nFirst, we find the partial derivatives:\n\n'+display(partial)+'\n\nTherefore, the corresponding Jacobian determinant is\n\n'+display(r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}')+'\n\nThe function has critical points when $'+JLABEL+'=0.$ So, we obtain\n\n'+display(r'\begin{aligned}'+JLABEL+' & =0'+r' \\ '+tex(det)+r' & =0.\end{aligned}')+'\n\n'+loci[0]
    return prompt,solution,[{'values':loci,'correct_index':0,'key':'selection'}],recipes,det


def observed(t,p,profile):
    q=SOURCES[t]
    if profile not in ('observed','repaired'):raise ValueError('Observed template requires observed/repaired profile.')
    prompt=translate(q[':question/problem'],p);solution=translate(q[':question/worked-solution'],p)
    fields=[]
    for f in q[':question/answer-fields']:
        values=[translate(a[':answer/value'],p) for a in f[':answer-field/choices']]
        corr=f.get(':answer-field/correct',{}).get(':answer/id')
        ci=next((i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==corr),None)
        fields.append({'values':values,'correct_index':ci,'key':f[':answer-field/key']})
    if profile=='repaired':
        fields=[f for f in fields if f['correct_index'] is not None]
        solution=solution.replace('v=u..$','v=u.$')
        if t=='q-161815':prompt+='\n\nAssume $u>'+str(p['h'])+'$.'
        if t=='q-161813':prompt+='\n\nAssume $u\\ne '+str(p['h'])+'$.'
    domain=f"u>{p['h']}" if t=='q-161815' else f"u!={p['h']}" if t=='q-161813' else 'R^3'
    return prompt,solution,fields,['historical expression pattern; original error intent unresolved'],domain


# Complete authored method profiles for each observed mathematical family.
# Values are zero conditions obtained by the stated derivative/cofactor mistakes;
# the translation is applied to the entire symbolic expression, never to a final
# numeric answer. Historical banks remain separate evidence profiles.
METHOD_BANKS={
 'q-161819':([U+W**2,U-W**2,U+W,W,U],['correct','wrong sign in second cofactor','omit one w factor in second cofactor','omit first cofactor','omit second cofactor']),
 'q-39709':([U,W,V,U**2-V,U**2+V],['correct','set exponential exponent to zero','use wrong independent coordinate','equate first component to zero','equate second component to zero']),
 'q-161809':([V-U,V+U,V,U,U*V],['correct','add minor products','omit second minor product','omit first minor product','equate first component to zero']),
 'q-161812':([V**2-W**2,V**2+W**2,V-W**2,V**2-W,V],['correct','add minor products','differentiate v^3 as 3v instead of 3v^2','differentiate w^3 as 3w instead of 3w^2','omit second minor product']),
 'q-161815':([W,V,U,V*W,U+W],['correct','differentiate product with wrong held coordinate','equate derivative denominator to zero','equate second component to zero','equate third component to zero']),
 'q-161817':([3-V,3+V,V,W,3-W],['correct','add minor products','omit first minor product','set exponential exponent to zero','replace held v factor by w in derivative y_w']),
 'q-161818':([3-4*V,3+4*V,3-2*V,V,3-4*W],['correct','wrong minor sign','omit derivative factor two','omit last cofactor','differentiate with wrong held coordinate']),
 'q-161813':([2*V**2-W,2*V**2+W,V**2-W,V,W],['correct','add minor products','omit derivative factor two','omit second minor product','omit first minor product']),
 'q-161814':([U-2*W,U+2*W,U-W,U,W],['correct','wrong last cofactor sign','omit first-row coefficient two','omit last cofactor','omit first cofactor']),
 'q-161816':([U,V,W,2*U+W,U*V+W],['correct','differentiate product with wrong held coordinate','drop u from second exponential exponent and falsely set remaining w to zero','set final exponential exponent to zero','equate third component to zero']),
 'q-161810':([V,U,W,U+V*W,W+V],['correct','differentiate with wrong independent coordinate u','differentiate with wrong independent coordinate w','equate first component to zero','equate third component to zero']),
 'q-161811':([V-W,V+W,V,W,V*W],['correct','add minor products','omit second minor product','omit first minor product','equate third component to zero']),
}

def real_locus_key(expr,domain='R^3'):
    """Exact keys for this bounded polynomial response catalog on its C1 domain.

    Repeated factors have the same zero set; a sum of positive coordinate
    squares vanishes on an intersection, not on their union. Domain-excluded
    linear factors contribute no points. No arbitrary transcendental solver is
    claimed: all normal options belong to this explicit polynomial catalog.
    """
    factors=sp.factor_list(sp.expand(expr),*VARS)[1];keys=[]
    for factor,_ in factors:
        poly=sp.Poly(factor,*VARS);normalized=sp.expand(factor/poly.LC())
        if domain!='R^3':
            h=int(domain.split('>')[1] if '>' in domain else domain.split('!=')[1])
            if sp.simplify(normalized-(U-h))==0:continue
        if poly.total_degree()==2:
            hessian=sp.hessian(factor,VARS)
            if hessian.is_diagonal() and all(hessian[i,i]>=0 for i in range(3)):
                sol=sp.solve([sp.diff(factor,v) for v in VARS],VARS,dict=True)
                if sol and sp.simplify(factor.subs(sol[0]))==0:
                    equations=tuple(sorted(str(sp.expand(v-value)) for v,value in sol[0].items()))
                    keys.append(('intersection',equations));continue
        keys.append(('polynomial',str(normalized)))
    return ('union',tuple(sorted(keys,key=str))) if keys else ('empty',)


def observed_method(t,p):
    prompt,solution,_,_,domain=observed(t,p,'repaired')
    exprs,recipes=METHOD_BANKS[t];sub={U:U-p['h'],V:V-p['k'],W:W-p['l']}
    vals=[];locus_keys=[]
    for expr in exprs:
        e=sp.expand(expr.subs(sub,simultaneous=True));locus_keys.append(real_locus_key(e,domain))
        # A response condition represents the complete locus; geometric labels
        # are not required when a union is naturally expressed by one equation.
        vals.append('The critical points are exactly the domain points satisfying $'+tex(e)+'=0.$')
    if len(set(locus_keys))!=5:raise ValueError('Whole method bank rejected: equivalent real loci.')
    return prompt,solution,[{'values':vals,'correct_index':0,'key':'selection'}],recipes,domain


def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in TEMPLATES:raise ValueError('Invalid difficulty.')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only radio supported.')
    rng=random.Random(seed)
    template=template or rng.choice(TEMPLATES[level])
    if template not in TEMPLATES[level]:raise ValueError('Template outside level scope.')
    profile=profile or 'method'
    if template not in OBSERVED and profile!='method':raise ValueError('Authored template requires method profile.')
    for attempt in range(1000):
        p=copy.deepcopy(parameters) if parameters is not None else sample(level,template,rng)
        try:
            bounds(level,template,p)
            if template in OBSERVED:
                if profile=='method':prompt,solution,fields,recipes,domain=observed_method(template,p)
                else:prompt,solution,fields,recipes,domain=observed(template,p,profile)
            else:prompt,solution,fields,recipes,_=authored(level,template,p);domain=DOMAIN[template]
            break
        except ValueError:
            if parameters is not None:raise
    else:raise RuntimeError('No valid complete instance.')
    if profile=='method':
        prompt=normalize_prose(prompt);solution=normalize_prose(solution)
    identity=digest({'version':VERSION,'difficulty':level,'problem':prompt,'solution':solution,'fields':[{'values':sorted(f['values']),'correct':None if f['correct_index'] is None else f['values'][f['correct_index']],'key':f['key']} for f in fields]})
    # Canonical assessed task includes printed map/domain; excludes profile/bank/seed.
    if template in OBSERVED:
        critical=METHOD_BANKS[template][0][0].subs({U:U-p['h'],V:V-p['k'],W:W-p['l']},simultaneous=True)
        # Method family captures differentiated functions/zero-factor reasoning;
        # unused shifts (e.g. exponential scale or additive constant) do not count.
        task={'method_family':template,'locus':real_locus_key(critical,domain)}
    elif template=='diagonal':task={'method_family':'diagonal','locus':real_locus_key(VARS[p['axis']]-p['h'])}
    elif template=='product_block':task={'method_family':'product_block','locus':real_locus_key(p['b']*V-p['a']*U)}
    else:
        a,b,c,d,k=(p[x] for x in 'abcdk')
        task={'method_family':'three_cofactors','cofactor_products':[a*c,b*d,b*k],'locus':real_locus_key(1-2*a*c*U-b*(2*d*U+k))}
    mathematical=digest({'level':level,'task':task,'domain':domain})
    question={':question/id':uid(identity),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[]}
    for i,f in enumerate(fields):
        fid=uid(identity+':field:'+str(i));choices=[]
        for val in f['values']:choices.append({':answer/id':uid(fid+':'+val),':answer/type':':answer.type/text',':answer/value':val})
        field={':answer-field/id':fid,':answer-field/key':f['key'],':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
        if f['correct_index'] is not None:field[':answer-field/correct']=[':answer/id',choices[f['correct_index']][':answer/id']]
        rng.shuffle(choices);question[':question/answer-fields'].append(field)
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'level':level,'seed':seed,'template':template,'parameters':p,'profile':profile,'content_hash':identity,'mathematical_fingerprint':mathematical,'source':{k:CAPTURE[k] for k in ('database','basis','lineage')},'source_ids':[template] if template in OBSERVED else [],'origin':'observed template with authored method bank' if template in OBSERVED and profile=='method' else 'observed translated template' if template in OBSERVED else 'authored missing-level extension' if level!='moderate' else 'authored bank and template extension','evidence_only':profile!='method','eligible_for_learning':profile=='method','domain':domain,'recipes':recipes,'plots':{'rating':'none','assets':[]},'dependencies':{'python':platform.python_version(),'sympy':sp.__version__}}}

# EASY — authored: one diagonal nonlinear derivative, shifted coordinate plane.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE — normal source families with authored banks, plus sparse product block.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD — authored: three nonzero first-row cofactors and two signed quadratic slopes.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)


def preview(record):
    q=record['question'];meta=record['generation']
    evidence='EVIDENCE ONLY' if meta['evidence_only'] else 'GENERATED normal learning record'
    lines=[f"Difficulty: {meta['level']} | {evidence} | Origin: {meta['origin']} | Profile: {meta['profile']}",q[':question/problem']]
    for i,f in enumerate(q.get(':question/answer-fields',[])):
        correct=f.get(':answer-field/correct')
        lines.append('\nField '+str(i+1)+(' — original correct ref ABSENT; designation not inferred' if correct is None else ':'))
        for a in f[':answer-field/choices']:
            mark=' [correct]' if correct and a[':answer/id']==correct[1] else ''
            lines.append('- '+a[':answer/value']+mark)
    lines+=['\nWorked solution:',q.get(':question/worked-solution','')]
    return '\n'.join(lines)


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in (TEMPLATES if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(preview,records)))
if __name__=='__main__':main()
