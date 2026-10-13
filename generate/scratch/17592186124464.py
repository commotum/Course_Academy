#!/usr/bin/env python3
"""Normal lines to surfaces, steps 3–7 only. Coordinate-isometry recipes retain
all source derivative/evaluation/line stages; raw banks are public evidence.
Normal defaults use separately authored complete method banks. No EDB writes.
Easy is an authored supplied-level quadratic surface task (three simple partials,
integer evaluation, vector line). Moderate/hard preserve observed family labels.
All transformations use axis reflections and integer translations, preserving
source number forms and differentiation workload. No tangent-plane branches.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
ROOT=Path(__file__).with_suffix(''); KP=17592186124464
VERSION='normal-surface-v1'
CAPTURE=json.loads((ROOT/'source.json').read_text()); SRC=CAPTURE['record']
Q={q[':question/math-academy-id']:q for q in SRC[':knowledge-point/questions']}
x,y,z,t=S.symbols('x y z t',real=True); V=(x,y,z)
TRANS=standard_transformations+(implicit_multiplication_application,convert_xor)

def parse(s):
    s=s.replace('\u2061','').replace('−','-').replace('⟨','(').replace('⟩',')')
    s=re.sub(r'\\(?:,|;|:|!| )','',s)
    s=re.sub(r'\\(?:left|right|big|Big|bigg|Bigg)','',s)
    s=re.sub(r'\\(?:operatorname|mathrm|mathbf|text)\{([^{}]*)\}',lambda m:'' if not m[1].strip() else ' '+m[1]+' ',s)
    def group(a,i):
        if a[i]!='{': raise ValueError(('expected group',a,i))
        n=1;j=i+1
        while n:
            n+=(a[j]=='{')-(a[j]=='}');j+=1
        return a[i+1:j-1],j
    while '\\frac' in s or '\\dfrac' in s or '\\sqrt' in s:
        m=re.search(r'\\(d?frac|sqrt)',s);i=m.end()
        a,j=group(s,i)
        if m[1]=='sqrt': out='sqrt('+a+')'
        else:
            b,k=group(s,j);j=k;out='(('+a+')/('+b+'))'
        s=s[:m.start()]+out+s[j:]
    s=s.replace('\\pi','pi').replace('\\sin',' sin ').replace('\\cos',' cos ').replace('\\ln',' log ').replace('ln(','log(')
    s=s.replace('[','(').replace(']',')').replace('{','(').replace('}',')').replace('\\cdot','*').replace('^','**').replace('∇','')
    s=s.strip().rstrip('.,:')
    return parse_expr(s,local_dict={'x':x,'y':y,'z':z,'t':t,'e':S.E,'pi':S.pi,'sin':S.sin,'cos':S.cos,'log':S.log,'sqrt':S.sqrt},transformations=TRANS)

def tex(a):return S.latex(S.sympify(a)).replace('\\log','\\ln')
def components(s):return re.split(r'(?<!\\),',s)
def vec(a):return '⟨'+','.join(tex(v) for v in a)+'⟩'
def point(a):return '('+','.join(tex(v) for v in a)+')'
def digest(o):return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False,default=str).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'normal-surface/'+s))
def enum(v):return v[':db/ident'] if isinstance(v,dict) else v

def grouped(s):
    return '{'+s+'}' if s.startswith('-') else s

def translate_variables(text,h,sign):
    """Tokenize commands before coordinate replacement; protect names/indices.
    Only called for complete function/derivative/line expressions, never prose,
    basis labels, generic f arguments or formal operator denominators.
    """
    tokens=re.split(r'(\\[A-Za-z]+|\\.|[xyz])',text)
    for i,a in enumerate(tokens):
        if a in 'xyz' and len(a)==1:
            j='xyz'.index(a);inner=tex(V[j]-h[j]);v=inner if h[j]==0 else r'\left('+inner+r'\right)'
            if sign[j]<0:v='-'+v;v=r'\left('+v+r'\right)'
            tokens[i]=v
    return ''.join(tokens)

def vector_parts(row):
    """Parse actually displayed basis-vector row, preserving coefficient masks."""
    text=row.split('&',1)[-1].strip().removeprefix('=')
    text=re.sub(r'\\text\{[^{}]*\}|\\,',' ',text)
    text=text.replace('\\mathbf ','').replace('\\mathbf','')
    chunks=[]; start=0
    for m in re.finditer(r'(?<![A-Za-z\\])[ijk](?![A-Za-z])',text):
        coefficient=text[start:m.start()].strip()
        if coefficient in ('','+'):coefficient='1'
        if coefficient=='-':coefficient='-1'
        chunks.append((m[0],coefficient));start=m.end()
    if not chunks or text[start:].strip().rstrip('.')!='':raise ValueError(('vector row',row))
    values=[S.Integer(0)]*3
    for name,c in chunks:values['ijk'.index(name)]=parse(c)
    return tuple(values)

def vector_masks(row):
    text=row.split('&',1)[-1].strip().removeprefix('=')
    text=re.sub(r'\\text\{[^{}]*\}|\\,',' ',text)
    start=0;by=['0']*3
    for mt in re.finditer(r'(?<![A-Za-z\\])[ijk](?![A-Za-z])',text):
        c=text[start:mt.start()].strip();by['ijk'.index(mt[0])]='1' if c in ('','+') else '-1' if c=='-' else c;start=mt.end()
    return by

def substituted_tex(text,P):
    tokens=re.split(r'(\\[A-Za-z]+|\\.|[xyz])',text)
    return ''.join(r'\left('+tex(P['xyz'.index(a)])+r'\right)' if a in 'xyz' and len(a)==1 else a for a in tokens)

def basis_row(coeff):
    return '+'.join(r'\left('+tex(c)+r'\right)'+k for c,k in zip(coeff,'ijk'))

def line(value):
    """Whole vector/parametric/symmetric line: actual complete object."""
    pairs=re.findall('⟨([^⟩]*)⟩',value)
    if len(pairs)==2:return tuple(parse(a) for a in components(pairs[0])),tuple(parse(a) for a in components(pairs[1]))
    ss=value.split('=')
    if len(ss)!=3:raise ValueError(('not complete symmetric line',value))
    p=[];d=[]
    for j,s in enumerate(ss):
        a=parse(s);alpha=S.diff(a,V[j]);beta=S.simplify(a-alpha*V[j])
        if alpha==0 or beta.free_symbols or a.free_symbols!={V[j]}:raise ValueError(('non-affine coordinate',value))
        p.append(S.simplify(-beta/alpha));d.append(S.simplify(1/alpha))
    return tuple(p),tuple(d)

def parallel(a,b):return all(S.simplify(c)==0 for c in S.Matrix(a).cross(S.Matrix(b))) and any(S.simplify(c)!=0 for c in a) and any(S.simplify(c)!=0 for c in b)
def equivalent(A,B,t0=False):
    samepoint=all(S.simplify(a-b)==0 for a,b in zip(A[0],B[0]))
    offset=tuple(S.simplify(a-b) for a,b in zip(A[0],B[0]))
    collinear=all(S.simplify(c)==0 for c in S.Matrix(offset).cross(S.Matrix(B[1])))
    return parallel(A[1],B[1]) and (samepoint if t0 else collinear)

def extract(q):
    m=re.search(r'surface \$(.*?)\$ at the point \$(.*?)\$',q[':question/problem'])
    surface=m[1];pt=m[2].rstrip('.,');P=tuple(parse(c) for c in components(pt.strip('()')))
    lhs,rhs=surface.split('=');L,R=parse(lhs),parse(rhs)
    # Owning solution explicitly chooses the level function and sign convention.
    sm=re.search(r'f\(x,y,z\)=(.*?)\$',q[':question/worked-solution']);fs=sm[1].rstrip('.,')
    F=parse(fs);C=S.simplify(F.subs(dict(zip(V,P))))
    G=tuple(S.simplify(S.diff(F,a).subs(dict(zip(V,P)))) for a in V)
    blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)
    return {'surface':surface,'point_tex':pt,'P':P,'Ftex':fs,'F':F,'C':C,'G':G,'blocks':blocks,'t0':'parameter $t=0$' in q[':question/problem']}
MODELS={k:extract(q) for k,q in Q.items()}

def transform_vector_literals(text,h,sign,m):
    def sub(match):
        vals=tuple(parse(v) for v in components(match[1]))
        # Point vs vector roles are resolved from whole tuple; source P != G.
        result=tuple(sign[j]*v+(h[j] if vals==m['P'] else 0) for j,v in enumerate(vals))
        return '⟨'+','.join(components(match[1])[j] if sign[j]==1 and (vals!=m['P'] or h[j]==0) else tex(a) for j,a in enumerate(result))+'⟩'
    return re.sub('⟨([^⟩]*)⟩',sub,text)

def source_line(value,h,sign):
    pairs=list(re.finditer('⟨([^⟩]*)⟩',value))
    if len(pairs)==2:
        out=value
        for i,mt in reversed(list(enumerate(pairs))):
            vals=tuple(parse(v) for v in components(mt[1]));outvals=[sign[j]*a+(h[j] if i==0 else 0) for j,a in enumerate(vals)]
            # A component is a complete mask. Identity transform retains original
            # notation (including thin spaces), never a literal payload branch.
            bits=components(mt[1]);render=[]
            for j,a in enumerate(outvals):render.append(bits[j] if h[j]==0 and sign[j]==1 or i==1 and sign[j]==1 else tex(a))
            out=out[:mt.start()]+'⟨'+','.join(render)+'⟩'+out[mt.end():]
        return out
    return translate_variables(value,h,sign)

def displayed_point(m,h,sign):
    bits=components(m['point_tex'].strip('()'))
    return '('+','.join(bits[j] if h[j]==0 and sign[j]==1 else tex(sign[j]*m['P'][j]+h[j]) for j in range(3))+')'

def solution(q,m,h,sign,raw):
    text=q[':question/worked-solution'];P=tuple(sign[j]*a+h[j] for j,a in enumerate(m['P']));G=tuple(sign[j]*a for j,a in enumerate(m['G']));PT=displayed_point(m,h,sign)
    # All actual function expressions in formal operators and prose are slots.
    # Surface rearrangement rows and symbolic partial row are separate slots.
    blocks=[]
    for block in m['blocks']:
        rows=block.split(r'\\');new=[]
        gradblock='∇f' in block;actual_masks=None
        for idx,row in enumerate(rows):
            if not gradblock:
                if 'x-{x}_{0}' in row or 'v}_{x}' in row:new.append(row);continue
                if 'r &' in row:
                    rr=transform_vector_literals(row,h,sign,m);rr=rr.replace(m['point_tex'],PT);new.append(rr);continue
                rr=translate_variables(row,h,sign)
                if not raw and q[':question/math-academy-id']=='q-131124' and idx==0:rr=rr+'+12'
                new.append(rr);continue
            if '∂' in row:
                # Full function slots; hold-coordinate operator labels unchanged.
                new.append(row.replace(m['Ftex'],translate_variables(m['Ftex'],h,sign)));continue
            if '{f}_{x}' in row:new.append(row);continue
            if '⟨' in row:
                out=transform_vector_literals(row,h,sign,m);new.append(out);continue
            values=vector_parts(row)
            is_symbolic=any(a.free_symbols for a in values)
            if is_symbolic:
                transformed=tuple(sign[j]*a.subs(dict(zip(V,[sign[k]*(V[k]-h[k]) for k in range(3)])),simultaneous=True) for j,a in enumerate(values))
            else:transformed=tuple(sign[j]*a for j,a in enumerate(values))
            # Preserve source masks and arithmetic stages for identity/reflection
            # with no applicable sign change; otherwise explicit scalar grouping.
            if tuple(sign)==(1,1,1) and (not is_symbolic or not any(h)):out=row
            else:
                chunks=[]
                if is_symbolic:
                    for j,a in enumerate(values):
                        c=translate_variables(vector_masks(row)[j],h,sign)
                        if sign[j]<0:c=r'-\left('+c+r'\right)'
                        chunks.append(r'\left('+c+r'\right)'+'ijk'[j])
                else:
                    # Sign-multiply source coefficients without collapsing the
                    # substituted/evaluated arithmetic component masks.
                    ct=row.split('&',1)[-1].strip().removeprefix('=')
                    ct=re.sub(r'\\text\{[^{}]*\}|\\,',' ',ct)
                    start=0;by={}
                    for mt in re.finditer(r'(?<![A-Za-z\\])[ijk](?![A-Za-z])',ct):by['ijk'.index(mt[0])]=ct[start:mt.start()].strip() or '1';start=mt.end()
                    for j in range(3):
                        c=by.get(j,'0');c='1' if c=='+' else '-1' if c=='-' else c
                        if sign[j]<0:c=r'-\left('+c+r'\right)'
                        chunks.append(r'\left('+c+r'\right)'+'ijk'[j])
                out=row.split('&',1)[0]+'& ='+ '+'.join(chunks)
            if is_symbolic:
                actual_masks=[translate_variables(c,h,sign) for c in vector_masks(row)]
                actual_masks=[r'-\left('+c+r'\right)' if sign[j]<0 else c for j,c in enumerate(actual_masks)]
            if '∇f' in out:
                out=out.replace(m['point_tex'],PT)
                if not raw and (any(h) or tuple(sign)!=(1,1,1)) and actual_masks is not None:
                    new.append('∇f'+PT+'& ='+ '+'.join(r'\left('+substituted_tex(c,P)+r'\right)'+'ijk'[j] for j,c in enumerate(actual_masks)))
                    out='  &'+out.split('&',1)[1]
            new.append(out)
        blocks.append(r'\\'.join(new))
    for old,new in zip(m['blocks'],blocks):text=text.replace(old,new)
    text=text.replace(m['Ftex'],translate_variables(m['Ftex'],h,sign))
    # Points in prose/evaluation labels and concluding line are distinct masks.
    text=text.replace(m['point_tex'],PT)
    return text

def normal_options(P,G,t0,shape,profile):
    active=[j for j,g in enumerate(G) if g!=0]
    if profile=='axis':
        j=active[0];others=[k for k in range(3) if k!=j];gs=[G]
        for k in others:
            d=[S.Integer(0)]*3;d[k]=G[j];gs.append(tuple(d))
        for k in others:
            d=list(G);d[k]=G[j];gs.append(tuple(d))
        return [(P,d) for d in gs],['gradient','wrong_coordinate_axis_1','wrong_coordinate_axis_2','spurious_partial_1','spurious_partial_2']
    gs=[G]
    for j in active:
        d=list(G);d[j]=G[j]+G[j] if shape=='symmetric' else S.Integer(0);gs.append(tuple(d))
    if len(active)==2:
        zero=next(j for j in range(3) if j not in active);d=list(G);d[zero]=G[active[0]];gs.append(tuple(d));offset=zero
    else:offset=0
    wrong=list(P);wrong[offset]+=1
    return [(P,d) for d in gs]+[(tuple(wrong),G)], ['gradient']+[('repeat_partial_' if shape=='symmetric' else 'omit_partial_')+str(j) for j in active]+(['spurious_partial'] if len(active)==2 else [])+['use_wrong_basepoint']

def render_line(P,G,shape,r_prefix=True,suffix=True):
    if shape=='vector':return ('r=' if r_prefix else '')+vec(P)+r'+t\,'+vec(G)+(r',\,t\in (-\infty ,\infty )' if suffix else '')
    return '='.join(r'\frac{'+tex(a-b)+'}{'+tex(c)+'}' for a,b,c in zip(V,P,G))

def check_parameters(p,level):
    if set(p)!={'translation','signs'}:raise ValueError('parameters require translation and signs only')
    h=tuple(S.sympify(a) for a in p['translation']);sg=tuple(p['signs'])
    bound=2 if level=='easy' else 3
    if len(h)!=3 or len(sg)!=3 or any(a.is_Integer!=True or abs(a)>bound for a in h) or any(type(a) is not int or a not in (-1,1) for a in sg):raise ValueError('level translation/sign workload bounds')
    return h,sg

def easy_model():
    F=x*x+2*y*y-z;P=(S.Integer(1),S.Integer(1),S.Integer(3));G=(S.Integer(2),S.Integer(4),S.Integer(-1))
    return {'F':F,'P':P,'G':G,'C':S.Integer(0),'t0':False}

# Easy: authored missing-level workload, supplied level form, one-term partials.
def generate_easy(seed=0,**kw):return generate('easy',seed=seed,**kw)
# Moderate: all six observed vector-equation families, original workload retained.
def generate_moderate(seed=0,**kw):return generate('moderate',seed=seed,**kw)
# Hard: all eight observed symmetric-equation families, complete line construction.
def generate_hard(seed=0,**kw):return generate('hard',seed=seed,**kw)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('sources only support radio')
    rng=random.Random(seed)
    if profile and profile.startswith(('raw:','observed:')):
        template=profile.split(':',1)[1];raw=True
    else:raw=False
    family=[k for k,q in Q.items() if enum(q[':question/difficulty']).endswith('/'+level)] if level!='easy' else ['easy_quadratic']
    template=template or rng.choice(family)
    if template not in family:raise ValueError('template/difficulty mismatch')
    m=easy_model() if level=='easy' else MODELS[template];q=Q.get(template)
    shape='vector' if level in ('easy','moderate') else 'symmetric'
    axis=sum(a!=0 for a in m['G'])==1
    default_bank='axis' if axis else ('two_partials' if sum(a!=0 for a in m['G'])==2 else 'three_partials')
    if profile and not raw and profile not in (default_bank,'method','method:'+template):raise ValueError('ineligible complete bank')
    # Select complete bank above, before sampling any parameters.
    for attempt in range(200):
        p=parameters if parameters is not None else {'translation':[rng.randint(-2 if level=='easy' else -3,2 if level=='easy' else 3) for _ in V],'signs':[rng.choice([-1,1]) for _ in V]}
        h,sg=check_parameters(p,level);P=tuple(sg[j]*a+h[j] for j,a in enumerate(m['P']));G=tuple(sg[j]*a for j,a in enumerate(m['G']))
        F=m['F'].subs(dict(zip(V,[sg[j]*(V[j]-h[j]) for j in range(3)])),simultaneous=True)
        if level=='easy':
            Ftext=translate_variables('x^{2}+2y^{2}-z',h,sg)
            prompt='Find a vector equation of the normal line to the level surface $'+Ftext+'=0$ at the point $'+point(P)+'.$'
            d=tuple(S.diff(F,a) for a in V)
            subs=[a.subs(dict(zip(V,P)),simultaneous=True) for a in d]
            sol="Let's set $f(x,y,z)="+Ftext+'.$ Then, our surface can be viewed as the level surface $f(x,y,z)=0.$\n\nA normal vector to the level surface that passes through the point $'+point(P)+'$ can be found by computing $∇f'+point(P)+'.$\n\nSo, we find the gradient and evaluate it at $'+point(P)+':$\n\n$$\n\\begin{aligned}∇f(x,y,z)&={f}_{x}(x,y,z)i+{f}_{y}(x,y,z)j+{f}_{z}(x,y,z)k\\\\&='+ '+'.join(r'\frac{∂}{∂'+str(a)+'}('+Ftext+')'+k for a,k in zip(V,'ijk'))+r'\\&='+basis_row(d)+r'\\∇f'+point(P)+'&='+basis_row(subs)+r'\\&='+vec(G)+'\\end{aligned}\n$$\n\nFinally, the vector equation of the line that is parallel to $∇f'+point(P)+'$ and passes through the point $'+point(P)+'$ can be written as\n\n$$r='+vec(P)+r'+t\,∇f'+point(P)+'='+vec(P)+r'+t\,'+vec(G)+'.$$\n\nwhere $t\\in (-\\infty,\\infty).$'
        else:
            prompt=q[':question/problem'].replace(m['surface'],translate_variables(m['surface'],h,sg)).replace(m['point_tex'],displayed_point(m,h,sg))
            sol=solution(q,m,h,sg,raw)
        if raw:
            fields=[]
            for f in q[':question/answer-fields']:
                ff={k:copy.deepcopy(v) for k,v in f.items() if k!=':answer-field/choices' and k!=':answer-field/correct'}
                ff[':answer-field/type']=enum(f[':answer-field/type']);choices=[]
                for a in f[':answer-field/choices']:
                    aa=copy.deepcopy(a);aa[':answer/type']=enum(aa[':answer/type']);aa[':answer/value']=source_line(a[':answer/value'],h,sg);choices.append(aa)
                ff[':answer-field/choices']=choices
                if ':answer-field/correct' in f:ff[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
                fields.append(ff)
            objects=[line(a[':answer/value']) for f in fields for a in f[':answer-field/choices']];recipes=['opaque_observed_geometric_isometry']*len(objects)
        else:
            objects,recipes=normal_options(P,G,m['t0'],shape,default_bank)
            if any(not any(v!=0 for v in d) for _,d in objects) or any(equivalent(a,b,m['t0']) for i,a in enumerate(objects) for b in objects[i+1:]):
                if parameters is not None:raise ValueError('entire bank rejected: equivalent or singular lines')
                continue
            original_correct=None if q is None else q[':question/answer-fields'][-1].get(':answer-field/correct')
            prefix=level=='easy' or (original_correct is not None and original_correct[':answer/value'].startswith('r='));suffix=level=='easy' or (original_correct is not None and '\\in' in original_correct[':answer/value'])
            values=[render_line(a,b,shape,prefix,suffix) for a,b in objects]
            fields=[{':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':v} for v in values]}]
        break
    else:raise ValueError('no eligible instance for complete selected bank')
    residual=S.expand(F-m['C'])
    if residual.is_polynomial(*V):
        canonical=S.Poly(residual,*V).monic().as_expr()
    else:
        coefficient,canonical=residual.as_content_primitive()
        if canonical.could_extract_minus_sign():canonical=-canonical
    task=digest({'surface_relation':str(canonical),'P':[str(a) for a in P],'response':shape,'t0':m['t0']})
    content=digest({'version':VERSION,'difficulty':level,'prompt':prompt,'solution':sol,'fields':[{k:v for k,v in f.items() if k in (':answer-field/key',':answer-field/type')}|{'values':sorted(a[':answer/value'] for a in f[':answer-field/choices']), 'correct_value':next((a[':answer/value'] for a in f[':answer-field/choices'] if ':answer-field/correct' in f and a.get(':answer/id')==f[':answer-field/correct'][1]),None) if raw else f[':answer-field/choices'][0][':answer/value']} for f in fields]})
    if not raw:
        for i,f in enumerate(fields):
            f[':answer-field/id']=uid(content+'/field/'+str(i))
            for a in f[':answer-field/choices']:a[':answer/id']=uid(content+'/field/'+str(i)+'/'+a[':answer/value'])
            f[':answer-field/correct']=[':answer/id',f[':answer-field/choices'][0][':answer/id']];rng.shuffle(f[':answer-field/choices'])
    anchor=not any(h) and tuple(sg)==(1,1,1)
    if raw and not anchor:
        for i,f in enumerate(fields):
            f[':answer-field/id']=uid(content+'/field/'+str(i))
            refs={}
            for a in f[':answer-field/choices']:
                old=a[':answer/id'];a[':answer/id']=uid(content+'/field/'+str(i)+'/'+a[':answer/value']);refs[old]=a[':answer/id']
            if ':answer-field/correct' in f:f[':answer-field/correct']=[':answer/id',refs[f[':answer-field/correct'][1]]]
    question={':question/id':q[':question/id'] if raw and anchor else uid(content),':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':fields}
    if raw:
        for k,v in q.items():
            if k not in question:question[k]=copy.deepcopy(v)
        if ':question/difficulty' not in q:question.pop(':question/difficulty')
    return {'knowledge_point':{'db_id':KP,'id':SRC[':knowledge-point/id'],'title':SRC[':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'template':template,'profile':('raw:'+template if raw else default_bank),'source':{k:CAPTURE[k] for k in ('database','basis','lineage')},'parameters':{'translation':list(map(int,h)),'signs':list(sg)},'mathematical_fingerprint':task,'content_fingerprint':content,'seed':seed,'eligible_for_learning':not raw,'evidence_only':raw,'original_question_ref':q[':question/id'] if q else None,'original_field_refs':[f[':answer-field/id'] for f in q[':question/answer-fields']] if q else [],'authored_scope':'easy missing level; method-derived complete bank' if not raw else 'opaque observed complete-bank isometry; missing refs retained','recipes':recipes,'runtime':{'python':sys.version.split()[0],'sympy':S.__version__},'plot':'none'}}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
    records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    if args.format=='json':print(json.dumps(records,ensure_ascii=False,indent=2))
    else:
        for a in records:
            q=a['question'];print(q[':question/problem']);print('\n'.join('- $'+c[':answer/value']+'$' for f in q.get(':question/answer-fields',[]) for c in f[':answer-field/choices']));print('\n'+q.get(':question/worked-solution',''))
if __name__=='__main__':main()
