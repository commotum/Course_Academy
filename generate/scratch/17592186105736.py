#!/usr/bin/env python3
"""Determinant scalar triple products, math basis 1356; local review only.

Observed profiles use compiled arithmetic masks and a positive bottom-row scale.
Opaque historical scalar banks are homogeneous evidence recipes, never defaults.
Normal defaults use independent coordinates and complete cofactor-error banks.
Every source has its own source-shaped stage/layout family. No plot is required.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186105736
EVIDENCE=Path(__file__).with_suffix('')
CAPTURE=json.loads((EVIDENCE/'source.json').read_text())
KP=CAPTURE['record']
TITLE=KP[':knowledge-point/title']
VERSION='determinant-triple-product-1'
QUESTIONS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
LEVELS={sid:q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/moderate').split('/')[-1] for sid,q in QUESTIONS.items()}
TEMPLATES={sid:{'level':LEVELS[sid], 'source_ids':[sid], 'plot':'none'} for sid in QUESTIONS}
TEMPLATES['dense_signed']={'level':'hard','source_ids':[],'plot':'none'}
PROFILES=('cofactor_signs','omit_terms')

def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x): return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+str(x)))
def ft(f): return f[':answer-field/type'][':db/ident']
def source_vectors(q):
    pairs=re.findall(r'([a-z])\s*=\s*⟨([^⟩]+)⟩',q[':question/problem'])
    vectors={n:tuple(map(int,v.split(','))) for n,v in pairs}
    found=re.search(r'Find \$([a-z])\\cdot \(([a-z])\\times ([a-z])\)',q[':question/problem'])
    order=tuple(found.groups()) if found else ('a','b','c')
    return vectors,order

def split_terms(s):
    """Top-level summands, keeping source separators and grouped negatives."""
    starts=[0];depth=0
    for i,c in enumerate(s):
        if c=='(':depth+=1
        elif c==')':depth-=1
        elif c in '+-' and depth==0 and i:starts.append(i)
    starts.append(len(s));return [s[a:b] for a,b in zip(starts,starts[1:])]

def scale_digits(s, degrees, scale):
    matches=list(re.finditer(r'\d+',s));assert len(matches)==len(degrees),(s,degrees)
    it=iter(degrees)
    return re.sub(r'\d+',lambda m:str(int(m[0])*scale**next(it)),s)

def arithmetic_rows(solution):
    pieces=solution.split(' & =')
    return [p.split(r'\end{aligned}\n')[0] for p in pieces[1:]]

def replay_solution(q,scale):
    """Compile each original operative stage; no literal-payload answer branch.

    Top row stays fixed; both lower rows scale. Entries scale by s, evaluated
    minor/product/collected terms by s². Structural zeros and omitted units are
    retained. Historical mistakes are preserved only in flagged evidence.
    """
    if ':question/worked-solution' not in q:return None
    sol=q[':question/worked-solution'];parts=sol.split(' & =')
    out=[parts[0]]
    for index,row in enumerate(parts[1:]):
        n=len(re.findall(r'\d+',row))
        if index==0: degrees=[0]*3+[1]*6
        elif index==1:degrees=([0]+[1]*4)*3
        elif index==2:
            degrees=[]
            for term in split_terms(row):
                k=len(re.findall(r'\d+',term))
                if k==5:degrees += [0]+[1]*4
                elif k==4:degrees += [1]*4
                elif k==1:degrees += [2]
                elif k==0:pass
                else:raise ValueError(('substitution mask',q[':question/math-academy-id'],term,k))
        elif index<len(parts)-3:
            degrees=[]
            for term in split_terms(row):
                k=len(re.findall(r'\d+',term))
                if q[':question/math-academy-id']=='q-275350' and k==2:
                    degrees += [2,2]
                else:degrees += ([0]+[2]*(k-1)) if k>1 else [2]*k
        else:degrees=[2]*n
        out.append(scale_digits(row,degrees,scale))
    return ' & ='.join(out)

def matrix_tex(rows):return r'|\begin{aligned}'+r' \\ '.join(' & '.join(map(str,row)) for row in rows)+r'\end{aligned}|'
def g(n):return '('+str(n)+')' if n<0 else str(n)
def product(a,b):return g(a)+r'\cdot '+g(b)
def summation(values):
    return ''.join(('+' if i and x>=0 else '')+str(x) for i,x in enumerate(values))

def solution(rows,order,style='dense_signed'):
    a,b,c=rows
    minors=[[(b[k],b[l]),(c[k],c[l])] for k,l in ((1,2),(0,2),(0,1))]
    minorvalues=[sp.Matrix(m).det() for m in minors]
    terms=[a[0]*minorvalues[0],-a[1]*minorvalues[1],a[2]*minorvalues[2]]
    expr=order[0]+r'\cdot ('+order[1]+r'\times '+order[2]+')'
    cofactor=''
    substituted=''
    evaluated=''
    expanded=''
    isblank=style=='dense_signed' or (style in QUESTIONS and ft(QUESTIONS[style][':question/answer-fields'][-1]).endswith('/blank'))
    detailed=isblank and style!='q-275350'
    active=[]
    for j,m in enumerate(minors):
        op=('', '-', '+')[j]
        cofactor+=op+g(a[j])+r'\cdot '+matrix_tex(m)
        x,y=m[0];z,w=m[1]
        inside=product(x,w)+'-'+product(y,z)
        # Radio source masks omit unit coefficients and occasionally zero terms.
        if not isblank and a[j]==0:
            if style=='q-73461':continue
            substituted+=op+'0';active.append(j);continue
        coeff='' if not isblank and a[j]==1 else g(a[j])+r'\cdot '
        substituted+=op+coeff+'('+inside+')'
        evaluated+=op+g(a[j])+r'\cdot ('+str(minorvalues[j])+')'
        expanded+=op+coeff+'('+str(x*w)+('+' if -y*z>=0 else '')+str(-y*z)+')'
        active.append(j)
    chain=[matrix_tex(rows),cofactor,substituted]
    if detailed:chain.append(evaluated)
    if style=='q-275350':chain.append(expanded)
    chain.extend([summation([terms[j] for j in active]),str(sum(terms))+'.'])
    prose=('Remember that the scalar triple product $'+expr+'$ is just the determinant of the matrix whose rows are given by $'+order[0]+',$ $'+order[1]+',$ and $'+order[2]+'.$\n\nSo, we have\n\n$$\n')
    return prose+r'\begin{aligned}'+expr+' & ='+r' \\  & ='.join(chain)+r'\end{aligned}'+'\n$$'

def bank_values(rows,profile):
    m=sp.Matrix(rows);a=list(m.row(0));d=[m.minor_submatrix(0,j).det() for j in range(3)]
    t=[a[0]*d[0],-a[1]*d[1],a[2]*d[2]];v=sum(t)
    active=[j for j in range(3) if a[j]!=0]
    unweighted=d[0]-d[1]+d[2]
    if profile=='cofactor_signs':
        # Eligible recipe slots depend on structural nonzero coefficients,
        # established by the family before numerical parameters are sampled.
        j=active[0]
        b,c=rows[1:]
        added=[b[1]*c[2]+b[2]*c[1],b[0]*c[2]+b[2]*c[0],b[0]*c[1]+b[1]*c[0]]
        wrongminor=a[0]*added[0]-a[1]*added[1]+a[2]*added[2]
        return [v,-v,v-2*t[j],unweighted,wrongminor]
    if profile=='omit_terms':return [v,-v,v-t[active[0]],v-t[active[1]],unweighted]
    raise ValueError('unknown bank')

def check_parameters(level,rows,style):
    if len(rows)!=3 or any(len(r)!=3 for r in rows):raise ValueError('three 3D input vectors required')
    if any(type(x)!=int for r in rows for x in r):raise ValueError('integer coordinates required')
    ceiling={'easy':9,'moderate':9,'hard':6}[level]
    if any(abs(x)>ceiling for r in rows for x in r):raise ValueError('coordinate workload bound')
    if style=='dense_signed':
        if level!='hard' or any(abs(x)<2 for r in rows for x in r) or any(abs(x)<4 for x in rows[0]) or sum(x<0 for r in rows for x in r)<3:raise ValueError('hard requires dense signed rows and three first-row magnitudes 4 through 6')
    elif style in QUESTIONS:
        vectors,order=source_vectors(QUESTIONS[style]);anchor=[vectors[n] for n in order]
        # Each observed family retains its signed/zero/unit arithmetic form.
        for j,(old,new) in enumerate(zip(sum((list(r) for r in anchor),[]),sum((list(r) for r in rows),[]))):
            if old==0 and new!=0 or old!=0 and old*new<=0:raise ValueError('source family signs/zeros')
            if j<3 and abs(old)==1 and new!=old:raise ValueError('source omitted-unit workload')
        if style=='q-20053' and any(abs(x)>3 for x in rows[0]):raise ValueError('easy dense-family first-row magnitude ceiling3')
    return rows

def normal_prompt(rows,order,style,kind):
    if style in QUESTIONS:
        q=QUESTIONS[style];vectors,_=source_vectors(q);replacement=dict(zip(order,rows))
        prompt=re.sub(r'([a-z])\s*=\s*⟨([^⟩]+)⟩',lambda m:m[0][:m[0].index('⟨')+1]+','.join(map(str,replacement[m[1]]))+'⟩',q[':question/problem'])
        if style=='q-20051':prompt=prompt.replace(r'b \cdot c',r'b \times c')
        if kind=='blank':
            prompt=re.sub(r'\n\n\$-?\d+\$$','\n{{field-1}}',prompt)
        elif '{{field-1}}' in prompt:prompt=prompt.split('\n\n')[0]
    else:
        expr=order[0]+r'\cdot ('+order[1]+r'\times '+order[2]+')'
        prompt='Let '+', '.join('$'+n+'=⟨'+','.join(map(str,row))+'⟩$' for n,row in zip(order,rows))+'. Find $'+expr+'$ using a determinant.'
        if kind=='blank':prompt+='\n\n$'+expr+'=$\n{{field-1}}'
    if kind=='blank' and '{{field-1}}' not in prompt:prompt+='\n\n{{field-1}}'
    return prompt

def record(level,seed,style,profile,prompt,sol,fields,params,rows,raw=False):
    # Presentation identity excludes source/profile aliases and option order.
    content={'level':None if raw and style=='q-20051' else level,'prompt':prompt,'solution':sol,'fields':[{k:v for k,v in f.items() if k not in (':answer-field/id',':db/id',':answer-field/choices',':answer-field/correct')}|{'values':sorted(a[':answer/value'] for a in f[':answer-field/choices']),'correct':f.get('_correct')} for f in fields]}
    fingerprint=digest({'assessment':'ordered 3x3 determinant','rows':rows})
    identity=digest(content);q={':question/id':uid(identity),':question/problem':prompt}
    if not raw or ':question/difficulty' in QUESTIONS[style]:q[':question/difficulty']=':question.difficulty/'+level
    if sol is not None:q[':question/worked-solution']=sol
    outfields=[]
    for i,f in enumerate(fields):
        field={k:v for k,v in f.items() if k not in (':db/id',':answer-field/id',':answer-field/choices',':answer-field/correct','_correct')}
        field[':answer-field/id']=uid(identity+':field:'+str(i));answers=[];correct=f.get('_correct')
        for a in f[':answer-field/choices']:
            value=a[':answer/value'];answers.append({':answer/id':uid(identity+':field:'+str(i)+':'+value),':answer/type':':answer.type/math',':answer/value':value})
        random.Random(str(seed)+':'+str(i)).shuffle(answers)
        field[':answer-field/choices']=answers
        if correct is not None:field[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in answers if a[':answer/value']==correct)]
        outfields.append(field)
    q[':question/answer-fields']=outfields
    return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':TITLE},'question':q,'generation':{'version':VERSION,'template':style,'profile':profile,'level':level,'seed':seed,'parameters':params,'mathematical_fingerprint':fingerprint,'content_fingerprint':identity,'source':{k:CAPTURE[k] for k in ('database','basis','lineage')},'evidence_only':raw,'eligible_for_learning':not raw,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
    rng=random.Random(seed)
    if profile and profile.startswith('observed:'):
        sid=profile.split(':',1)[1]
        if sid not in QUESTIONS or template not in (None,sid) or level!=LEVELS[sid]:raise ValueError('observed family mismatch')
        q=QUESTIONS[sid];p=parameters or {'scale':rng.choice((1,2))}
        if set(p)!={'scale'} or type(p['scale'])!=int or not 1<=p['scale']<=2:raise ValueError('evidence profile requires scale in {1,2}')
        s=p['scale'];vectors,order=source_vectors(q);new={n:tuple(x*(1 if n==order[0] else s) for x in v) for n,v in vectors.items()}
        prompt=re.sub(r'([a-z])\s*=\s*⟨([^⟩]+)⟩',lambda m:m[0][:m[0].index('⟨')+1]+re.sub(r'\d+',lambda n:str(int(n[0])*(1 if m[1]==order[0] else s)),m[2])+'⟩',q[':question/problem'])
        prompt=re.sub(r'\n\n\$(-?\d+)\$$',lambda m:'\n\n$'+str(int(m[1])*s*s)+'$',prompt)
        fields=[]
        for f in q.get(':question/answer-fields',[]):
            nf={':answer-field/key':f[':answer-field/key'],':answer-field/type':ft(f),':answer-field/choices':[{':answer/value':str(int(a[':answer/value'])*s*s)} for a in f[':answer-field/choices']]}
            if ':answer-field/correct' in f:nf['_correct']=str(int(f[':answer-field/correct'][':answer/value'])*s*s)
            fields.append(nf)
        return record(level,seed,sid,profile,prompt,replay_solution(q,s),fields,p,[list(new[n]) for n in order],True)
    styles=[sid for sid in QUESTIONS if LEVELS[sid]==level]
    if level=='hard':styles=['dense_signed']
    style=template or rng.choice(styles)
    if style not in styles:raise ValueError('family difficulty mismatch')
    original=QUESTIONS.get(style)
    kind=field_type or (ft(original[':question/answer-fields'][-1]).split('/')[-1] if original else rng.choice(('radio','blank')))
    kind=kind.split('/')[-1]
    if kind not in ('radio','blank'):raise ValueError('unsupported field')
    chosen=profile or (rng.choice(PROFILES) if kind=='radio' else 'blank')
    if kind=='radio' and chosen not in PROFILES or kind=='blank' and chosen!='blank':raise ValueError('bank/field mismatch')
    if original:
        vectors,order=source_vectors(original);anchor=[vectors[n] for n in order]
    else:order=('a','b','c');anchor=None
    for attempt in range(10000):
        if parameters is not None:
            if set(parameters)!={'rows'}:raise ValueError('normal parameters require rows')
            rows=copy.deepcopy(parameters['rows'])
        elif anchor:
            rows=[[0 if x==0 else x if i==0 and abs(x)==1 else (1 if x>0 else -1)*rng.randint(1,3 if style=='q-20053' and i==0 else 6) for x in r] for i,r in enumerate(anchor)]
        else:rows=[[rng.choice((-1,1))*rng.randint(4 if i==0 else 2,6) for _ in range(3)] for i in range(3)]
        try:
            check_parameters(level,rows,style)
            values=[sp.Matrix(rows).det()] if kind=='blank' else bank_values(rows,chosen)
            if len(set(values))!=len(values):raise ValueError('whole bank collision')
        except ValueError:
            if parameters is not None:raise
            continue
        fields=[{':answer-field/key':'field-1' if kind=='blank' else 'selection',':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':[{':answer/value':str(x)} for x in values],'_correct':str(values[0])}]
        return record(level,seed,style,chosen,normal_prompt(rows,order,style,kind),solution(rows,order,style),fields,{'rows':rows},rows)
    raise RuntimeError('no eligible complete bank')

# Easy: observed signed/zero/unit source forms, direct ordered determinant.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: observed forms including reversed input order and signed cofactors.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard (authored): dense signed entries, three nonunit cofactor products; same method.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def markdown(r):
    q=r['question'];parts=[q[':question/problem']]
    for f in q.get(':question/answer-fields',[]):parts+=['- $'+a[':answer/value']+'$' for a in f[':answer-field/choices']]
    if ':question/worked-solution' in q:parts.append(q[':question/worked-solution'])
    return '\n\n'.join(parts)

def main():
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=('easy','moderate','hard','all'),default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=('json','markdown'),default='markdown');p.add_argument('--template');p.add_argument('--profile');a=p.parse_args()
    records=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in (('easy','moderate','hard') if a.difficulty=='all' else (a.difficulty,)) for i in range(a.count)]
    print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
