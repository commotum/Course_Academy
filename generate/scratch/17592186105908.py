#!/usr/bin/env python3
"""Coplanarity generators; math basis 2535; no database writes.

Observed evidence profiles preserve every source field, missing label/reference and
worked-solution stage. Their public affine-coordinate recipes are evidence-only:
replace the source unknown by (unknown+shift), and translate every observed scalar
or root-set choice by -shift. This is a coherent change of variable, NOT an
inferred distractor algorithm. Authored normal banks instead use determinant
operations. Mathematical fingerprints exclude the bank/profile and letter names.
Easy and hard are authored missing levels; see classification.md. CLI and API
always validate explicit parameters. Source templates accept shift only, normal
ones accept complete vectors and variable; no literal question replay branch.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
KP_ID=17592186105908
KP_UUID='26c84e5b-97a7-5116-a90c-e4f011e87cf0'
TITLE='Determining Whether Three Vectors are Coplanar'
VERSION='coplanar-1'
HERE=Path(__file__).with_suffix('')
SNAP=json.loads((HERE/'source.json').read_text())
SOURCE={k:SNAP[k] for k in ('database','basis','lineage')}
ORIGINALS={q[':question/math-academy-id']:q for q in SNAP['record'][':knowledge-point/questions']}
TRANS=standard_transformations+(implicit_multiplication_application,)

def tex(e): return sp.latex(sp.sympify(e),fold_short_frac=False).replace(' ','')
def group(s): return '('+s+')'
def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.UUID(KP_UUID),x))
def parse_math(s):
    """Independent scalar TeX reader, also used by displayed-stage validators."""
    s=str(s).strip().strip('$').rstrip('.')
    while r'\frac' in s or r'\sqrt' in s:
        # innermost commands first (groups without commands are sufficient here)
        old=s
        s=re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',lambda m:'(('+m[1]+')/('+m[2]+'))',s)
        s=re.sub(r'\\sqrt\{([^{}]*)\}',lambda m:'sqrt('+m[1]+')',s)
        if s==old: raise ValueError('Unsupported TeX '+s)
    s=s.replace(r'\cdot','*').replace(r'\,','').replace('^','**').replace('{','(').replace('}',')')
    return parse_expr(s,transformations=TRANS)

def printed_vectors(prompt):
    tuples=re.findall('⟨([^⟩]+)⟩',prompt)
    if len(tuples)!=3:raise ValueError('Expected three printed vectors')
    return sp.Matrix([[parse_math(x)for x in t.split(',')]for t in tuples])

def roots_from_prompt(prompt):
    v=re.search(r'Find \$([ktx])\$',prompt)[1]
    x=sp.Symbol(v)
    d=sp.expand(printed_vectors(prompt).det())
    roots=sp.solve(d,x)
    return v,d,sorted(roots,key=lambda z:float(z))

def affine_slot(s,v,shift):
    # Slots are mathematical unknown tokens, protected from command names/prose.
    component=v if shift==0 else group(v+('+' if shift>0 else '')+str(shift))
    return re.sub(r'(?<![A-Za-z\\])'+v+r'(?![A-Za-z])',lambda _:component,s)

def scalar_atom(s,shift):
    e=parse_math(s)-shift
    # Source notation (including unsimplified radical) remains a complete atom;
    # translating it keeps that atom intact instead of fitting scalar distractors.
    if shift==0:return s
    return s+('-'+str(shift) if shift>0 else '+'+str(-shift))

def observed_option(s,v,shift):
    if '=' not in s:return scalar_atom(s,shift)
    # Preserve text/equation fragments and separators; only RHS atoms are slots.
    pat=re.escape(v)+r'=([^$,]+?)(?=\$|,|$)'
    return re.sub(pat,lambda m:v+'='+scalar_atom(m[1],shift),s)

def field(key,kind,values,answer_type='math',correct_index=0):
    return {'key':key,'kind':kind,'values':values,'answer_type':answer_type,'correct_index':correct_index}

def assemble(level,seed,template,profile,parameters,prompt,solution,fs,mathematical,missing_rating=False):
    content={'version':VERSION,'difficulty':None if missing_rating else level,'prompt':prompt,'solution':solution,'fields':[{'key':f['key'],'kind':f['kind'],'type':f['answer_type'],'values':sorted(f['values']),'correct':f['values'][f['correct_index']] if f['correct_index'] is not None else None}for f in fs]}
    identity=digest(content);qid=uid(identity);fields=[]
    for f in fs:
        fid=uid(identity+':field:'+f['key']); answers=[{':answer/id':uid(fid+':'+s),':answer/type':':answer.type/'+f['answer_type'],':answer/value':s}for s in f['values']]
        out={':answer-field/id':fid,':answer-field/key':f['key'],':answer-field/type':':answer-field.type/'+f['kind'],':answer-field/choices':answers}
        if f['correct_index'] is not None:out[':answer-field/correct']=[':answer/id',answers[f['correct_index']][':answer/id']]
        if f['kind']=='radio':random.Random(str(seed)+fid).shuffle(answers)
        fields.append(out)
    q={':question/id':qid,':question/problem':prompt,':question/answer-fields':fields}
    if solution is not None:q[':question/worked-solution']=solution
    if not missing_rating:q[':question/difficulty']=':question.difficulty/'+level
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'source':SOURCE,'level':level,'template':template,'profile':profile,'parameters':parameters,'seed':seed,'parameter_fingerprint':digest(mathematical),'content_fingerprint':identity,'evidence_only':profile.startswith('source:') if profile else False,'eligible_for_learning':not profile.startswith('source:') if profile else True}}

def observed(level,seed,template,parameters,profile,field_type):
    source=ORIGINALS[template]; raw=profile=='source:'+template+':raw'
    if profile not in ('source:'+template+':raw','source:'+template+':normalized'):raise ValueError('Wrong complete profile')
    if level!='moderate':raise ValueError('Observed template is moderate; two unrated sources assigned moderate for normal repair')
    p={'shift':0}if parameters is None else dict(parameters)
    if set(p)!={'shift'}or type(p['shift'])is not int or abs(p['shift'])>4:raise ValueError('Evidence shift must be integer |h|<=4')
    h=p['shift'];v,d,rs=roots_from_prompt(source[':question/problem'])
    # Prompt slots occur only AFTER Find $k$, preserving the requested unknown.
    left,right=source[':question/problem'].split('given that',1)
    prompt=left+'given that'+affine_slot(right,v,h)
    # Blanks must continue to ask for k, rather than the translated component.
    prompt=prompt.replace('$'+(v if h==0 else group(v+('+'if h>0 else '')+str(h)))+'=${{','$'+v+'=${{')
    solution=source.get(':question/worked-solution')
    if solution is not None:
        solution=affine_slot(solution,v,h)
        if h:solution+='\n\nThus $'+v+'='+('$ or $'+v+'=').join(tex(r-h)for r in rs)+'.$'
    fs=[]
    for f in source[':question/answer-fields']:
        values=[a[':answer/value'] if f[':answer-field/type'][':db/ident']==':answer-field.type/checkbox' else observed_option(a[':answer/value'],v,h)for a in f[':answer-field/choices']]
        oldcorrect=f.get(':answer-field/correct',{}).get(':answer/id')
        ci=next((i for i,a in enumerate(f[':answer-field/choices'])if a[':answer/id']==oldcorrect),None)
        if not raw:
            if oldcorrect is None:
                ci=next(i for i,s in enumerate(values)if sp.simplify(parse_math(s)-(rs[0]-h))==0)
            if template=='q-18266':ci=1 # supported source designation correction: BOTH roots
        fs.append(field(f[':answer-field/key'],f[':answer-field/type'][':db/ident'].split('/')[-1],values,f[':answer-field/choices'][0][':answer/type'][':db/ident'].split('/')[-1],ci))
    if field_type and any(f['kind']!=field_type for f in fs):raise ValueError('Observed field layout fixed')
    if not raw and solution is None:solution=normal_solution(printed_vectors(prompt),v,rs=[r-h for r in rs],names=[a for a,b in re.findall(r'([a-z])\s*=\s*⟨(.*?)⟩',prompt)])
    return assemble(level,seed,template,profile,p,prompt,solution,fs,{'vectors':[[str(printed_vectors(prompt)[i,j]).replace(v,'U')for j in range(3)]for i in range(3)]},missing_rating=raw and ':question/difficulty'not in source)

def determinant_tex(m):return r'|\begin{aligned}'+r' \\ '.join(' & '.join(tex(x)for x in row)for row in m.tolist())+r'\end{aligned}|'
def sum_terms(ss):return '+'.join('('+s+')'for s in ss)
def normal_solution(m,v,rs=None,names=None):
    names=names or ['a','b','c'];triple=names[0]+r'\cdot('+names[1]+r'\times '+names[2]+')'
    x=sp.Symbol(v);d=sp.expand(m.det());rs=sp.solve(d,x)if rs is None else rs
    minors=[m.minor_submatrix(0,j)for j in range(3)]
    cofactor=sum_terms([group(tex((-1)**j*m[0,j]))+r'\cdot '+determinant_tex(minors[j])for j in range(3)])
    substituted=sum_terms([group(tex((-1)**j*m[0,j]))+r'\cdot '+group(group(tex(n[0,0]))+r'\cdot '+group(tex(n[1,1]))+'-'+group(tex(n[0,1]))+r'\cdot '+group(tex(n[1,0])))for j,n in enumerate(minors)])
    evaluated=sum_terms([group(tex((-1)**j*m[0,j]))+r'\cdot '+group(tex(n.det()))for j,n in enumerate(minors)])
    distributed=sum_terms([tex(sp.expand((-1)**j*m[0,j]*n.det()))for j,n in enumerate(minors)])
    rows=[determinant_tex(m),cofactor,substituted,evaluated,distributed,tex(d)]
    calc=r'\begin{aligned}'+triple+'&='+r'\\ &='.join(rows)+r'\end{aligned}'
    degree=sp.degree(d,x);a=d.coeff(x,degree);b=d.subs(x,0)
    solve=[tex(d)+'&=0',tex(a*x**degree)+'&='+tex(-b),tex(x**degree)+'&='+tex(-b/a)]
    if degree==2:solve.append(v+r'&=\pm '+tex(sp.sqrt(-b/a)))
    final=('$ or $'+v+'=').join(tex(r)for r in rs)
    return 'Computing the triple product, we get\n\n$$\n'+calc+'\n$$\n\nThree vectors are coplanar if and only if their triple product is zero:\n\n$$\n'+r'\begin{aligned}'+r'\\ '.join(solve)+r'\end{aligned}'+'\n$$\n\nTherefore, the three vectors are coplanar if and only if $'+v+'='+final+'.$'

# EASY (authored missing level): single linear unknown, sparse small determinant.
# MODERATE (observed scope): single/repeated linear unknown OR a single square;
#     integer coordinates |c|<=8; no mixed-variable products or general quadratics.
# HARD (authored missing level): dense signed determinant, unknown in row 2/3;
#     all numeric entries 2<=|c|<=8, six nonzero products and linear isolation.
def bounds(m,v,level,template):
    x=sp.Symbol(v);nums=[];slots=[]
    for i in range(3):
        for j in range(3):
            e=m[i,j]
            if x in e.free_symbols:
                if e not in (x,x*x):raise ValueError('Only complete k or k^2 components supported')
                slots.append((i,j,e))
            elif e.is_Integer:nums.append(int(e))
            else:raise ValueError('Integer coordinates required')
    if not slots or any(e.free_symbols-{x}for e in m):raise ValueError('Unknown variable')
    if template=='quadratic':
        if level!='moderate'or len(slots)!=1 or slots[0][2]!=x*x:raise ValueError('Quadratic observed scope')
    elif any(z[2]!=x for z in slots):raise ValueError('Linear slots required')
    if len({z[0]for z in slots})!=1:raise ValueError('Repeated unknown limited to one vector')
    if level=='easy' and (len(slots)!=1 or max(map(abs,nums))>3 or nums.count(0)<2):raise ValueError('Easy sparse workload')
    if level=='moderate'and template=='linear'and len(slots)==1 and max(map(abs,nums))<=3 and nums.count(0)>=2:raise ValueError('Moderate cannot reduce to authored easy workload')
    if level=='hard'and(len(slots)!=1 or slots[0][0]==0 or any(not 2<=abs(n)<=8 for n in nums)):raise ValueError('Hard dense signed workload')
    if level=='hard'and not(any(n<0 for n in nums)and any(n>0 for n in nums)):raise ValueError('Hard needs mixed signs')
    if max(map(abs,nums))>8:raise ValueError('Coordinate bound')
    d=sp.expand(m.det());degree=sp.degree(d,x)
    if degree!=(2 if template=='quadratic'else 1)or d.subs(x,0)==0:raise ValueError('Nondegenerate determinant required')
    if degree==2 and -d.subs(x,0)/d.coeff(x,2)<=0:raise ValueError('Two real distinct roots required')

def normal_bank(m,v,template):
    x=sp.Symbol(v);d=sp.expand(m.det());degree=sp.degree(d,x);A=d.coeff(x,degree);B=d.subs(x,0)
    if template=='quadratic':
        z=-B/A;r=sp.sqrt(z)
        if z==1:raise ValueError('Root bank collision')
        sets=[[-r,r],[r],[-r],[-z,z],[-sp.sqrt(1/z),sp.sqrt(1/z)]]
        if len({tuple(map(str,a))for a in sets})!=5:raise ValueError('Bank collision')
        return ['$'+v+'='+('$ or $'+v+'=').join(tex(a)for a in s)+'$'+(' only'if len(s)==1 else '')for s in sets],'text'
    r=-B/A;allplus=sp.expand(sum(m[0,j]*m.minor_submatrix(0,j).det()for j in range(3)))
    if sp.degree(allplus,x)!=1:raise ValueError('All-plus cofactor bank ineligible')
    wrong=-allplus.subs(x,0)/allplus.coeff(x)
    bank=[r,-r,-B,-A/B,wrong]
    if any(z.has(sp.zoo,sp.oo)for z in bank)or len(set(bank))!=5:raise ValueError('Reject whole operation bank')
    return [tex(z)for z in bank],'math'

def sample(rng,level,template):
    x=sp.Symbol('k');lim=3 if level=='easy'else 8
    if level=='hard':vals=[n for n in range(-8,9)if abs(n)>=2]
    else:vals=list(range(-lim,lim+1))
    m=sp.Matrix(3,3,[rng.choice(vals)for _ in range(9)])
    row=rng.choice((1,2))if level=='hard'else rng.randrange(3);col=rng.randrange(3)
    m[row,col]=x*x if template=='quadratic'else x
    if level=='easy':
        loc=[(i,j)for i in range(3)for j in range(3)if(i,j)!=(row,col)]
        for i,j in rng.sample(loc,2):m[i,j]=0
    elif level=='moderate'and template=='linear'and rng.randrange(2):m[row,(col+1)%3]=x
    return {'vectors':[[str(m[i,j])for j in range(3)]for i in range(3)],'variable':'k'}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
    if template in ORIGINALS:return observed(level,seed,template,parameters,profile or 'source:'+template+':normalized',field_type)
    rng=random.Random(seed)
    template=template or ('quadratic'if level=='moderate'and rng.randrange(3)==0 else 'linear')
    if template not in ('linear','quadratic'):raise ValueError('Unknown template')
    if profile not in (None,'method'):raise ValueError('Unknown authored profile')
    kind=field_type or rng.choice(('radio','blank'))
    if kind not in ('radio','blank'):raise ValueError('Unsupported field type')
    explicit=parameters is not None
    for _ in range(10000):
        p=dict(parameters)if explicit else sample(rng,level,template)
        if set(p)!={'vectors','variable'}or p['variable']not in ('k','t'):raise ValueError('Complete vectors/variable required')
        v=p['variable'];m=sp.Matrix([[parse_math(s)for s in row]for row in p['vectors']])
        if m.shape!=(3,3):raise ValueError('3x3 vectors required')
        try:
            bounds(m,v,level,template);rs=sorted(sp.solve(m.det(),sp.Symbol(v)),key=lambda z:float(z))
            values,typ=normal_bank(m,v,template)if kind=='radio'else ([tex(r)for r in rs],'math')
            break
        except ValueError:
            if explicit:raise
    else:raise ValueError('No eligible complete instance')
    tuples=['⟨'+','.join(tex(m[i,j])for j in range(3))+'⟩'for i in range(3)]
    prompt='Find $'+v+'$ given that the vectors $a='+tuples[0]+'$, $b='+tuples[1]+'$, and $c='+tuples[2]+'$ are coplanar.'
    if kind=='radio':fs=[field('selection','radio',values,typ)]
    else:
        fs=[field('field-'+str(i+1),'blank',[a])for i,a in enumerate(values)]
        if len(fs)==2:prompt+='\n\n**In ascending order:**'
        prompt+='\n\n'+('\nand\n'.join('$'+v+'=${{'+f['key']+'}}'for f in fs))
    canonical=[[str(m[i,j]).replace(v,'U')for j in range(3)]for i in range(3)]
    return assemble(level,seed,template,'method',p,prompt,normal_solution(m,v,rs),fs,{'vectors':canonical})

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
    q=r['question'];s=q[':question/problem']+'\n\n'
    for f in q[':question/answer-fields']:
        s+=f[':answer-field/key']+': '+', '.join(a[':answer/value']for a in f[':answer-field/choices'])+'\n'
    return s+'\n'+q.get(':question/worked-solution','[No source solution supplied]')

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate', 'generate_easy', 'generate_hard', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
    levels=['easy','moderate','hard']if a.difficulty=='all'else[a.difficulty]
    out=[generate(l,a.seed+i,template=a.template,profile=a.profile)for l in levels for i in range(a.count)]
    print(json.dumps(out,indent=2)if a.format=='json'else'\n\n---\n\n'.join(markdown(r)for r in out))
