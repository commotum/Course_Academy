"""Seeded determinant-statement generator. No database or runtime repository access."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import random
import uuid
import sympy as sp
from math_format import normalize_prose, validate_prose, validate_generated_record

VERSION='1.0.0'
LEVELS=('easy','moderate','hard')
KP={'db_id':17592186119931,'id':'a6a3d254-c96f-5aa0-9db6-a587eb7cb2de',
    'title':'Calculating an Expression Involving Given Determinants and Matrix Types'}
SOURCES=json.loads((Path(__file__).parent/'source-cases.json').read_text())
SUPPORT={'easy':['8ad15905-c4cb-5380-ab37-e1b30677ecfc'],
         'given':['dcce1957-fa55-5f89-a722-cbd09d149dbf','029d7f47-3f9c-597a-ac75-8fbf40dc3193'],
         'scalar':['c9c4599b-e53c-5c27-98df-6174c3f82a89','35e600df-b2a1-5526-a22d-d7aabd8d69d2'],
         'scaled':['4524ce2c-6b42-5e23-be24-247fd51db7f6','8c56c883-f05b-52a6-84d1-a47095dbd707','2ee41fdf-2985-5db6-8a3d-0bea273a05a9']}

def tex(v): return sp.latex(sp.sympify(v))
def uid(v): return str(uuid.uuid5(uuid.NAMESPACE_URL,'det-statement-v1:'+v))
def values(p):
    return {'A':sp.sympify(p['d']),'T':sp.sympify(p['d']), 'I':sp.Integer(1),
            'S':sp.sympify(p['c'])**p['n']}
def object_tex(obj,p):
    label=p['label']
    return {'A':rf'\det({label})','T':rf'\det({label}^T)','I':r'\det(I)',
            'S':rf'\det({tex(p["c"])}I)'}[obj]
def linear(terms,render):
    parts=[]
    for k,obj in terms:
        if not k: continue
        atom=render(obj)
        coefficient='' if abs(k)==1 else str(abs(k))
        term=coefficient+atom
        parts.append(('-' if k<0 else ('+' if parts else ''))+term)
    return ''.join(parts) or '0'
def expression(terms,p): return linear(terms,lambda o: object_tex(o,p))
def substitution(terms,p): return linear(terms,lambda o:'('+tex(values(p)[o])+')')
def evaluate(terms,p): return sp.expand(sum(k*values(p)[o] for k,o in terms))
def statement(terms,rhs,p): return '$'+expression(terms,p)+'='+tex(rhs)+'$'
def diagonal(p):
    c=tex(p['c']);n=p['n']
    return r'\begin{bmatrix}'+r' \\ '.join(' & '.join(c if i==j else '0' for j in range(n)) for i in range(n))+r'\end{bmatrix}'
def prompt(p):
    label=p['label']; d=tex(p['d']); n=p['n']; c=tex(p['c'])
    if p['family']=='scalar':
        text=f'Let ${label}={c}I$, where $I$ is the ${n}\\times {n}$ identity matrix.'
    else:
        inp=label+('^T' if p['given_transpose'] else '')
        text=f'Let ${label}$ be a square matrix with $\\det({inp})={d}$, and let $I$ be the identity matrix of the same size.'
        if p['family']=='scaled':
            text=f'Let ${label}$ be a ${n}\\times {n}$ matrix with $\\det({inp})={d}$, and let $I$ be the ${n}\\times {n}$ identity matrix.'
    if p['difficulty']=='easy':
        text+='\n\nRecall that transposing a matrix leaves its determinant unchanged and that $\\det(I)=1$.'
    return text+'\n\nWhich of the following statements are true? Select all that apply.'

def derivation(p):
    out=[]; label=p['label'];d=tex(p['d']);c=tex(p['c']);n=p['n']
    if p['family'] in ('scalar','scaled'):
        target=label if p['family']=='scalar' else c+'I'
        out.append(f'The matrix ${target}$ is diagonal:\n\n$$\n{target}={diagonal(p)}.\n$$')
        product=r'\cdot '.join('('+c+')' for _ in range(n))
        out.append('Its determinant is the product of its diagonal entries:\n\n$$\n'+rf'\det({target})={product}=({c})^{{{n}}}={tex(values(p)["S"])}.'+'\n$$')
    out.append('Transposition preserves the determinant, and the identity matrix has determinant $1$:\n\n$$\n'+
               r'\begin{aligned}'+rf'\det({label}^T)&=\det({label})={d}'+r' \\ '+r'\det(I)&=1.'+r'\end{aligned}'+'\n$$')
    truths=[]
    for s in p['statements']:
        v=evaluate(s['terms'],p);rhs=sp.sympify(s['rhs']);truth=sp.simplify(v-rhs)==0
        eq=s.get('label') or statement(s['terms'],rhs,p)
        out.append('For '+eq+',\n\n$$\n'+expression(s['terms'],p)+'='+substitution(s['terms'],p)+'='+tex(v)+
                   ('.' if truth else r'\ne '+tex(rhs)+'.')+'\n$$\n\nThis statement is **'+('true' if truth else 'false')+'**.')
        truths.append((eq,truth))
    good=[eq for eq,t in truths if t]
    if good: out.append('Select '+', '.join(good)+'.'+ (' **None of the above** is false.' if p['none'] else ''))
    else:
        if not p['none']: raise ValueError('No selectable true statement')
        out.append('All three mathematical statements are false. Select **None of the above** only.')
    return normalize_prose('\n\n'.join(out)),truths

def build(p,seed=0,shuffle=True):
    p=copy.deepcopy(p)
    text=normalize_prose(p.get('prompt') or prompt(p))
    solution,truths=derivation(p)  # Ordered path exists before fields/bank.
    if p['none']: truths.append(('None of the above',not any(t for _,t in truths)))
    if shuffle: random.Random(str(seed)+json.dumps(p,sort_keys=True)).shuffle(truths)
    for eq,_ in truths: validate_prose(eq)
    identity=hashlib.sha256(json.dumps([text,solution,truths],ensure_ascii=False).encode()).hexdigest()
    fields=[]
    for j,(eq,t) in enumerate(truths):
        fid=uid(identity+':field:'+str(j));choices=[{':answer/id':uid(fid+':'+str(v)),':answer/type':':answer.type/text',':answer/value':str(v).lower()} for v in (False,True)]
        fields.append({':answer-field/id':fid,':answer-field/key':eq,':answer-field/type':':answer-field.type/checkbox',
                       ':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[int(t)][':answer/id']]})
    source=[p['source_id']] if 'source_id' in p else SUPPORT['easy' if p['difficulty']=='easy' else p['family']]
    record={'knowledge_point':KP,'question':{':question/id':uid(identity),':question/problem':text,
        ':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+p['difficulty'],':question/answer-fields':fields},
        'generation':{'generator_version':VERSION,'seed':seed,'template':p['family'],'parameters':p,
                      'source_question_ids':source,'domains':'real square matrices; common identity dimension',
                      'dependencies':{'python':'3.13.5','packages':{'sympy':sp.__version__}}}}
    return validate_generated_record(record)

def wrong_values(terms,p):
    actual=evaluate(terms,p);base=values(p);attempts=[]
    # Concrete mistake profiles: wrong transpose sign, wrong identity value,
    # missing scalar power, omitted addend, sign error on one addend.
    for obj,wrong in [('T',-base['T']),('A',-base['A']),('I',sp.Integer(p['n'])),('I',sp.Integer(0)),('S',sp.sympify(p['c'])),('S',-base['S'])]:
        if any(o==obj for _,o in terms):
            v=sum(k*(wrong if o==obj else base[o]) for k,o in terms)
            attempts.append((sp.expand(v),'wrong '+obj+' value'))
    for j,(k,o) in enumerate(terms):
        attempts.append((actual-2*k*base[o],'sign of addend'))
        attempts.append((actual-k*base[o],'omitted addend'))
        if abs(k)>1: attempts.append((actual-(k-(1 if k>0 else -1))*base[o],'omitted coefficient'))
    result=[]
    for v,error in attempts:
        if v!=actual and v.is_Integer and (v,error) not in result: result.append((v,error))
    return result

def sample(level,rng,mask=None,family=None):
    # Decide answer-bearing roles first, then choose compatible data.
    if mask is None: mask=rng.randrange(8)
    none=mask==0 or rng.choice((False,True))
    family=family or ('given' if level!='hard' else rng.choice(('scalar','scaled')))
    for _ in range(200):
        n=rng.choice((3,4));c=rng.choice(('-3','-2','2','3'))
        if family=='scaled' and rng.randrange(3)==0: n=4;c=rng.choice(('sqrt(2)','sqrt(3)'))
        d=sp.sympify(c)**n if family=='scalar' else rng.randint(-9,9)
        p=dict(difficulty=level,family=family,n=n,c=c,d=str(d),label=rng.choice(('A','B','K','M')),given_transpose=rng.choice((False,True)),none=none,statements=[])
        if level=='easy':
            sign=rng.choice((-1,1));other='A' if p['given_transpose'] else 'T'
            patterns=[[(1,other)],[(1,'I')],[(1,other),(sign,'I')]]
        else:
            k=rng.choice((-3,-2,2,3));m=rng.choice((1,2,3));sign=rng.choice((-1,1))
            if family=='scaled':
                patterns=[[(1,'A'),(-1,'S')],[(k,'T'),(sign,'S')],[(1,'T'),(sign*2,'S')]]
                if rng.randrange(3)==0: patterns[2]=[(1,'S'),(-int(sp.sympify(c)),'I')] if sp.sympify(c).is_Integer else [(1,'S'),(-2,'I')]
            else:
                patterns=[[(k,'T')],[(1,'A'),(sign*m,'I')],[(rng.choice((-2,-1,1,2)),'T'),(rng.choice((-2,-1,1,2)),'A')]]
        failed=False
        for j,terms in enumerate(patterns):
            actual=evaluate(terms,p);good=bool(mask&(1<<j))
            candidates=wrong_values(terms,p)
            if not good and not candidates: failed=True;break
            rhs,error=(actual,'correct substitution') if good else rng.choice(candidates)
            p['statements'].append({'terms':terms,'rhs':str(rhs),'recipe':error})
        if not failed: return p
    raise RuntimeError('Could not construct the requested decision case')

def generate(level,count,seed):
    if level=='unclassified': level='moderate'
    if level not in LEVELS or count<0: raise ValueError('Invalid difficulty/count')
    rng=random.Random(seed);out=[];seen=set();schedule=[]
    for attempt in range(max(1000,count*50)):
        if len(out)==count: return out
        if not schedule:
            schedule=list(range(8));rng.shuffle(schedule)
        mask=schedule.pop()
        family=('scalar','scaled')[len(out)%2] if level=='hard' else 'given'
        p=sample(level,rng,mask,family);r=build(p,seed)
        # Semantic signature ignores matrix-label and field-order changes.
        signature=json.dumps({k:v for k,v in p.items() if k!='label'},sort_keys=True)
        if signature in seen: continue
        seen.add(signature);out.append(r)
    raise RuntimeError('Requested batch exceeds construction capacity')

def replay(): return [build(p,0,False) for p in SOURCES]
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=LEVELS+('unclassified',),default='moderate')
    parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=('json',),default='json');args=parser.parse_args()
    print(json.dumps(generate(args.difficulty,args.count,args.seed),ensure_ascii=False,indent=2))
if __name__=='__main__': main()
