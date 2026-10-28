#!/usr/bin/env python3
"""Seeded sparse-determinant practice. No filesystem writes or repository imports."""
import argparse
import itertools
import json
from pathlib import Path
import random
import re
import uuid
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP={'db_id':17592186119930,'id':'02e65c73-8c02-5403-8c5c-b1e81f81a7b6','title':'Calculating the Determinant of a Matrix With Many Zeros'}
NS=uuid.UUID('814da390-eef1-4e02-a520-1c495e32be6f')
SOURCES={'triangular':['1a43a5f7-bf85-5fa1-b02e-c33727064a7d','c1038fde-ed05-5c15-a434-43fa62ec2a0c','1d6c75b7-d9d1-5c4f-a63e-3df78db605e9'], 'recursive':['192bc61f-95e6-574d-85ae-b6351c8929be','1cded5b0-233c-51be-b7fc-66e328db8e2f'], 'cycle':['bffca4e7-0bf9-53f7-83df-1f634b854d33','5cc1443c-03cd-5f86-bcfc-b9b7f4c6a565']}

def parse(s):
    s=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',s)
    s=re.sub(r'\\sqrt\{([^{}]+)\}',r'sqrt(\1)',s)
    s=s.replace('\\,','').replace('\\cdot','*')
    return parse_expr(s, transformations=standard_transformations+(implicit_multiplication_application,))

def tex(x):return normalize_tex(sp.latex(sp.simplify(x)))
def mat(a,env='vmatrix'):
    return '\\begin{'+env+'}'+' \\\\ '.join(' & '.join(tex(x) for x in row) for row in a)+'\\end{'+env+'}'
def product(xs):return sp.prod(xs)
def minor(a,i,j):return [row[:j]+row[j+1:] for k,row in enumerate(a) if k!=i]
def axis(a):
    n=len(a)
    options=[(sum(x!=0 for x in a[i]),'row',i) for i in range(n)]+[(sum(a[i][j]!=0 for i in range(n)),'column',j) for j in range(n)]
    def cost(option):
        count,orientation,k=option
        coords=[(k,j) for j in range(n) if a[k][j]!=0] if orientation=='row' else [(i,k) for i in range(n) if a[i][k]!=0]
        return count,sum(not triangular(minor(a,i,j)) for i,j in coords),orientation,k
    return min(options,key=cost)
def triangular(a):
    n=len(a)
    return all(a[i][j]==0 for i in range(n) for j in range(i)) or all(a[i][j]==0 for i in range(n) for j in range(i+1,n))

def tree(a,name='D',force=False,preferred_axis=None):
    n=len(a)
    if n==2:
        v=sp.simplify(a[0][0]*a[1][1]-a[0][1]*a[1][0]);return {'a':a,'name':name,'kind':'two','value':v}
    if triangular(a) and not force:return {'a':a,'name':name,'kind':'triangular','value':product(a[i][i] for i in range(n))}
    count,orientation,k=axis(a)
    if preferred_axis is not None:orientation,k=preferred_axis
    pairs=[(k,j) for j in range(n) if a[k][j]!=0] if orientation=='row' else [(i,k) for i in range(n) if a[i][k]!=0]
    children=[]
    for t,(i,j) in enumerate(pairs):
        child=tree(minor(a,i,j),name+'_{'+str(t+1)+'}' if name=='D' else name[:-1]+str(t+1)+'}')
        children.append((i,j,child))
    value=sp.simplify(sum(a[i][j]*(-1)**(i+j)*c['value'] for i,j,c in children))
    return {'a':a,'name':name,'kind':'expand','orientation':orientation,'index':k,'children':children,'value':value}

def explain(t):
    a,nm=t['a'],t['name'];n=len(a)
    if t['kind']=='triangular':
        rhs='\\cdot'.join('('+tex(a[i][i])+')' for i in range(n))
        return f'The matrix in ${nm}$ is triangular, so multiply its diagonal entries.\n\n$$\n'+r'\begin{aligned}'+nm+' &='+mat(a)+r' \\ &='+rhs+r' \\ &='+tex(t['value'])+r'.\end{aligned}'+'\n$$'
    if t['kind']=='two':
        rhs=f'({tex(a[0][0])})({tex(a[1][1])})-({tex(a[0][1])})({tex(a[1][0])})'
        return 'Evaluate the two by two determinant:\n\n$$\n'+r'\begin{aligned}'+nm+' &='+mat(a)+r' \\ &='+rhs+r' \\ &='+tex(t['value'])+r'.\end{aligned}'+'\n$$'
    terms=[];values=[];labels=[]
    for i,j,c in t['children']:
        terms.append(f'({tex(a[i][j])})(-1)^{{{i+1}+{j+1}}}{mat(c["a"])}')
        values.append(f'({tex(a[i][j])})(-1)^{{{i+1}+{j+1}}}({tex(c["value"])})')
        labels.append(f'${c["name"]}$ for the minor obtained by deleting row {i+1} and column {j+1}')
    intro=f'Expand ${nm}$ along {t["orientation"]} {t["index"]+1}; only {len(terms)} nonzero '+('entry contributes.' if len(terms)==1 else 'entries contribute.')
    expansion=(r'\begin{aligned}'+nm+' &='+terms[0]+''.join(r' \\ &\quad +'+term for term in terms[1:])+r'.\end{aligned}') if len(terms)>1 else nm+'='+terms[0]+'.'
    block='\n\n$$\n'+expansion+'\n$$\n\n'
    defs='Write '+', and '.join(labels)+'.\n\n'
    children='\n\n'.join(explain(c) for _,_,c in t['children'])
    radicals=sorted({str(p.base) for x in sum(a,[]) for p in x.atoms(sp.Pow) if p.exp==sp.Rational(1,2)})
    reminder=('\n\nUse '+', '.join('$'+tex(sp.sqrt(sp.sympify(k)))+r'\cdot'+tex(sp.sqrt(sp.sympify(k)))+'='+k+'$' for k in radicals)+'.') if radicals else ''
    end=reminder+'\n\nSubstituting these minor values,\n\n$$\n\\begin{aligned}'+nm+' &='+'+'.join(values)+r' \\ &='+tex(t['value'])+r'.\end{aligned}'+'\n$$'
    return intro+block+defs+children+end

def mutations(t):
    """Single local mistakes, propagated through the same ordered expansion."""
    a=t['a'];v=t['value'];out=[]
    if t['kind']=='two':
        ad=a[0][0]*a[1][1];bc=a[0][1]*a[1][0]
        return [('add cross products',ad+bc),('omit second product',ad),('omit first product',-bc),('reverse subtraction',-v)]
    if t['kind']=='triangular':
        ds=[a[i][i] for i in range(len(a))]
        out.append(('sum diagonal instead of product',sum(ds)))
        out.extend(('omit diagonal factor '+str(i+1),product(ds[:i]+ds[i+1:])) for i in range(len(ds)))
        out.extend(('repeat diagonal factor '+str(i+1),v*ds[i]) for i in range(len(ds)))
        return out
    for i,j,c in t['children']:
        factor=a[i][j]*(-1)**(i+j);term=factor*c['value']
        out.extend([('omit branch',v-term),('reverse one cofactor sign',v-2*term),('omit entry factor',v-term+(-1)**(i+j)*c['value']),('repeat entry factor',v-term+a[i][j]*term)])
        out.extend((label,v-term+factor*val) for label,val in mutations(c))
    return out

def bank(t,profile,rng):
    v=t['value'];mut=[(s,sp.simplify(x)) for s,x in mutations(t)]
    if v == 0:
        # A cancelling minor is a valid determinant, not a failed bank. Keep
        # actual local mistakes (and their sign errors) instead of duplicating
        # the correct zero as its own negative.
        errors={}
        for label,value in mut:
            if value != 0:
                errors.setdefault(value,label)
                errors.setdefault(-value,label+' and reverse final sign')
        if len(errors)<4:return None
        candidates=list(errors.items());rng.shuffle(candidates)
        vals=[(v,'correct')]+[(x,label) for x,label in candidates[:4]]
        rng.shuffle(vals)
        return vals
    # Each chosen tuple is a complete authored profile, including compound sign errors.
    if profile in ('paired-factor','paired-sum','paired-repeat'):
        eligible=[(s,x) for s,x in mut if ('omit' in s if profile=='paired-factor' else ('repeat' in s if profile=='paired-repeat' else ('sum diagonal' in s or 'add cross' in s)))]
        if not eligible:return None
        s,e=rng.choice(eligible)
        z=product(t['a'][i][i] for i in range(4))
        vals=[(v,'correct'),(-v,'reverse final sign'),(e,s),(-e,s+' and reverse sign')]
        # A diagonal pivot can make the original diagonal product correct even
        # when the full matrix is not triangular. Do not exclude that source
        # family merely to keep this particular distractor.
        used={sp.simplify(x) for x,_ in vals}
        if z not in used:vals.append((z,'multiply original diagonal'))
        else:
            extras=[(x,label) for label,x in mut if x not in used]
            if not extras:return None
            x,label=rng.choice(extras);vals.append((x,label))
    else:
        if t['kind']!='expand' or len(t['children'])!=2:return None
        terms=[t['a'][i][j]*(-1)**(i+j)*c['value'] for i,j,c in t['children']]
        p,q=terms
        vals=[(v,'correct'),(p,'omit second branch'),(q,'omit first branch'),(p-q,'reverse second cofactor sign'),(-p+q,'reverse first cofactor sign')]
    if len(set(sp.simplify(x) for x,_ in vals))!=5:return None
    rng.shuffle(vals)
    return vals

def collect_matrices(t):
    return [t['a']]+[a for _,_,child in t.get('children',[]) for a in collect_matrices(child)]

def identity(s):return str(uuid.uuid5(NS,s))
def record(a,band,rng,profile='paired-factor',source=None,source_bank=None,preferred_axis=None):
    a=[[sp.sympify(x) for x in row] for row in a]
    t=tree(a,force=(band=='easy'),preferred_axis=preferred_axis)
    vals=source_bank or bank(t,profile,rng)
    if vals is None:return None
    prompt='Find the determinant of the matrix\n\n$$\nA='+mat(a,'bmatrix')+'.\n$$'
    if band=='easy':prompt+=f'\nUse a Laplace expansion along {t["orientation"]} {t["index"]+1}, then evaluate the triangular minor.'
    if source:prompt=source['problem']
    prompt=normalize_prose(prompt);solution=normalize_prose('Write $D=\\det(A)$.\n\n'+explain(t)+'\n\nTherefore, $\\det(A)='+tex(t['value'])+'$.')
    if source:solution=normalize_prose(source['solution'])
    key_data=json.dumps([prompt,solution,sorted(tex(v) for v,_ in vals)],sort_keys=True)
    qid=identity(key_data)
    choices=[{':answer/id':identity(qid+':'+tex(v)),':answer/type':':answer.type/math',':answer/value':tex(v)} for v,_ in vals]
    correct=identity(qid+':'+tex(t['value']))
    q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+band,':question/answer-fields':[{':answer-field/id':identity(qid+':field'),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]}
    result={'knowledge_point':KP,'question':q,'generation':{'version':1,'profile':profile,'matrix':[[tex(x) for x in row] for row in a],'source_question_ids':[source['id']] if source else SOURCES['cycle' if band=='hard' else ('recursive' if any(len(m)==2 and m[0][1]!=0 and m[1][0]!=0 for m in collect_matrices(t)) else 'triangular')], 'error_recipes':{identity(qid+':'+tex(v)):s for v,s in vals}}}
    return validate_generated_record(result)

def insert(m,r,c,p,rng):
    n=len(m)+1;a=[];idx=0
    for i in range(n):
        if i==r:a.append([p if j==c else sp.Integer(0) for j in range(n)])
        else:
            row=m[idx][:];row.insert(c,sp.Integer(rng.choice([-3,-2,-1,1,2,3])));a.append(row);idx+=1
    return a

def sample(rng,band):
    nz=lambda:sp.Integer(rng.choice([-2,-1,1,2] if band=='moderate' else [-3,-2,-1,1,2,3]))
    family='triangular' if band=='easy' else rng.choice(['triangular','recursive'])
    # Structural assignments are drawn before incidental values.
    r,c=rng.randrange(4),rng.randrange(4);transpose=rng.choice([True,False]);lower=rng.choice([True,False]);r2,c2=rng.randrange(3),rng.randrange(3)
    if band=='hard':
        rows=rng.sample(range(4),4);cols=rng.sample(range(4),4);preferred=(rng.choice(['row','column']),rng.randrange(4))
        a=[[sp.Integer(0) for _ in range(4)] for _ in range(4)]
        for i in range(4):a[i][i]=nz();a[i][(i+1)%4]=nz()
        return [[a[i][j] for j in cols] for i in rows], 'cycle',preferred
    if family=='triangular':
        m=[[nz() if (i>=j if lower else i<=j) else sp.Integer(0) for j in range(3)] for i in range(3)]
    else:
        m=insert([[nz(),nz()],[nz(),nz()]],r2,c2,nz(),rng)
    a=insert(m,r,c,nz(),rng)
    if band=='moderate':
        arithmetic=rng.randrange(6)
        if arithmetic==0:
            # Rational row scaling preserves zero structure and expansion workload.
            k=rng.randrange(4);a[k]=[x/sp.Integer(2) for x in a[k]]
        elif arithmetic==1:
            # Paired radicals replicate the source's sqrt(k)*sqrt(k) cancellation.
            k,l=rng.sample(range(4),2);root=sp.sqrt(rng.choice([2,3,5]));a[k]=[x*root for x in a[k]];a[l]=[x*root for x in a[l]]
    if transpose:a=list(map(list,zip(*a)))
    return a,family,('column' if transpose else 'row',r)

def generate(band,count,seed):
    rng=random.Random(seed);records=[];seen=set();attempts=0;last_roles={}
    while len(records)<count:
        attempts+=1
        if attempts>max(1000,1000*count):raise RuntimeError('Unable to construct requested distinct banks')
        profile=rng.choice(['paired-factor','paired-sum','paired-repeat']+(['branches'] if band=='hard' else []))
        a,family,preferred=sample(rng,band)
        if band in ('easy','moderate') and triangular(a):continue
        rec=record(a,band,rng,profile,preferred_axis=preferred)
        if rec is None:continue
        # A finite batch must not teach a fixed rank or answer position within
        # its recognizable zero-pattern/arithmetic/hint families. Resample a
        # complete, mathematically derived bank rather than adding filler or
        # changing the seed. This does not constrain which determinant is valid.
        prompt=rec['question'][':question/problem']
        arithmetic='radical' if '\\sqrt' in prompt else ('rational' if '\\frac' in prompt else 'integer')
        terms=sum(all(a[i][p[i]]!=0 for i in range(4)) for p in itertools.permutations(range(4)))
        group=(arithmetic,terms,preferred[0] if band=='easy' else 'unhinted')
        field=rec['question'][':question/answer-fields'][0]
        values=[parse(choice[':answer/value']) for choice in field[':answer-field/choices']]
        correct=next(parse(choice[':answer/value']) for choice in field[':answer-field/choices'] if choice[':answer/id']==field[':answer-field/correct'][1])
        roles=(sorted(values,key=float).index(correct),values.index(correct))
        if group in last_roles and any(x==y for x,y in zip(roles,last_roles[group])):continue
        signature=tuple(tuple(row) for row in a)
        if signature in seen:continue
        last_roles[group]=roles
        seen.add(signature);rec['generation'].update(seed=seed,index=len(records),family=family)
        records.append(rec)
    return records

def replay():
    out=[]
    for s in json.loads(Path(__file__).with_name('source_cases.json').read_text()):
        a=[[parse(x) for x in row] for row in s['matrix']]
        # SymPy parses adjacent radical factors after the small capture grammar rewrite.
        vals=[(parse(v),'source bank') for v in s['choices']]
        out.append(record(a,'moderate',random.Random(0),'source-replay',s,vals))
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate');ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json'],default='json');ap.add_argument('--replay-source',action='store_true');args=ap.parse_args()
    if args.count<0:ap.error('count must be nonnegative')
    result=replay() if args.replay_source else generate('moderate' if args.difficulty=='unclassified' else args.difficulty,args.count,args.seed)
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
