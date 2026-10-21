#!/usr/bin/env python3
"""Seeded, relocatable logarithm rewriting generator. No writes or assets."""
import argparse
import itertools
import json
from pathlib import Path
import random
import uuid
from math_format import normalize_prose, normalize_tex, checked_math_content

VERSION = '1.1.0-source-scope'
KP = {'db_id': 17592186054624, 'id': '22382eaf-2654-5c65-b7ba-ac71015e84b8',
      'title': 'Rewriting an Expression Using the Product and Quotient Rules of Logarithms'}
SIGNS = tuple(s for s in itertools.product((1, -1), repeat=3) if len(set(s)) == 2)
LETTERS = ('x','y','z','p','q')

def uid(value):
    return str(uuid.uuid5(uuid.UUID(KP['id']), value))

def log(base, arg):
    name = r'\ln' if base == 'e' else r'\log' if base == '10' else r'\log_{' + base + '}'
    return name + r'\left(' + arg + r'\right)'

def signed_sum(terms, signs, order=None):
    order = range(len(terms)) if order is None else order
    result = ''
    for i in order:
        if not signs[i]: continue
        result += ('-' if signs[i] < 0 else '+' if result else '') + terms[i]
    return result

def product_ratio(factors, signs, order=None):
    order = list(range(3)) if order is None else list(order)
    top = [factors[i] for i in order if signs[i] > 0]
    bottom = [factors[i] for i in order if signs[i] < 0]
    numerator = r'\cdot '.join(top) or '1'
    return r'\frac{' + numerator + '}{' + r'\cdot '.join(bottom) + '}' if bottom else numerator

def factors(p, evaluated=True):
    if p['template'] == 'combine': return [str(p['c']),p['u'],p['v']]
    b,k=p['base'],p['k']
    power = ('e' if k==1 else 'e^{'+str(k)+'}') if b=='e' else str(int(b)**k) if evaluated else b+'^{'+str(k)+'}'
    return [power,str(p['c']),p['u']]

def answer(p, signs):
    if p['template']=='combine': return log(p['base'], product_ratio(factors(p), signs))
    order=p.get('order',[0,1,2])
    order=[i for i in order if signs[i]>0]+[i for i in order if signs[i]<0]
    return signed_sum([str(p['k']),log(p['base'],str(p['c'])),log(p['base'],p['u'])],signs,order)

def validate_scope(p, source_index=None):
    """Retain observed factor roles and the source's two-positive/one-negative move."""
    s=tuple(p['signs']);order=p.get('order',[0,1,2])
    if sorted(order)!=[0,1,2]:raise ValueError('Exactly one occurrence of every factor is required')
    allowed=((1,1,-1),) if p['template']=='combine' else ((1,-1,1),(-1,1,1)) if p['template']=='expand' else ()
    if s not in allowed:raise ValueError('Outside the saved product/quotient KP source structure')
    if source_index is None and [s[i] for i in order]!=[1,1,-1]:
        raise ValueError('Present the two positive terms before the subtracted term')
    if p['base'] not in (('10','e') if p['template']=='combine' else ('2','3','5','10','e')):
        raise ValueError('Unsupported logarithm base')
    if p['u'] not in LETTERS or (p['template']=='combine' and (p['v'] not in LETTERS or p['v']==p['u'])):
        raise ValueError('Distinct source-supported variable slots required')
    if type(p['c'])is not int or not 2<=p['c']<=9:raise ValueError('Constant must be an integer from 2 to 9')
    if p['template']=='expand' and (type(p['k'])is not int or not 1<=p['k']<=3 or (p['base']=='e' and p['k']!=1)):
        raise ValueError('Unsupported known-logarithm value')

def display_chain(*rows):
    return '\n\n$$\n'+r'\begin{aligned}&'+(r' \\ &='.join(rows))+r'.\end{aligned}'+'\n$$'

def solution(p):
    b,s=p['base'],p['signs'];fs=factors(p);order=p.get('order',[0,1,2])
    top=[fs[i]for i in order if s[i]>0];bottom=[fs[i]for i in order if s[i]<0]
    if len(top)!=2 or len(bottom)!=1:raise ValueError('Worked solution requires the saved source structure')
    quotient=log(b,r'\cdot '.join(top))+'-'+log(b,bottom[0])
    if p['template']=='combine':
        start=signed_sum([log(b,f)for f in fs],s,order)
        return ('Using the product rule for logarithms, combine the first two terms:'
                +display_chain(start,quotient)+'\n\n'
                +'Now use the quotient rule to combine the remaining difference:'
                +display_chain(quotient,answer(p,s)))
    ordered=[i for i in order if s[i]>0]+[i for i in order if s[i]<0]
    expanded=signed_sum([log(b,f)for f in fs],s,ordered)
    power=log(b,factors(p,False)[0])
    return ('Using the quotient rule for logarithms, separate the numerator and denominator:'
            +display_chain(log(b,product_ratio(fs,s,order)),quotient)+'\n\n'
            +'Now use the product rule to expand the logarithm of the numerator:'
            +display_chain(quotient,expanded)+'\n\n'
            +'Since $'+log(b,fs[0])+('='+power if power!=log(b,fs[0]) else '')+'='+str(p['k'])+'$, we obtain'
            +display_chain(expanded,answer(p,s)))


def source_bank(index,p):
    b,c,u,k=p['base'],str(p['c']),p['u'],p.get('k')
    L=lambda a: log(b,a)
    if index==0:
        return [answer(p,s) for s in [(1,1,-1),(-1,-1,1),(-1,1,-1),(1,-1,1),(0,1,-1)]],0
    if index==1:
        v=L(u); d=L(c)
        return [f'{k+1}+2{v}-{d}',f'{int(b)**k}+{v}-{d}',f'{v}-2{d}',f'{2*k}+3{v}-2{d}',f'{k}+{v}-{d}'],4
    if index==2:
        return ['e+'+L(u)+'+'+L(c),'1+'+L(u+'-'+c),'1-'+L(u)+r'+\frac{'+c+'}{e}', '1+'+L(u)+'-'+L(c),'e-'+L(u)+'-'+c],3
    a=L(c); v=L(u)
    return [f'{a}+{v}-{k*k}',f'{a}+{v}+{k}',f'{a}+{v}-{k}',f'{a}-{v}+{k}',f'{a}-{v}-{k*k}'],2

@checked_math_content
def make_record(p, rng, seed=None, source_index=None):
    p=json.loads(json.dumps(p)); p.setdefault('order',[0,1,2])
    s=tuple(p['signs'])
    if s not in SIGNS: raise ValueError('Both numerator and denominator required')
    validate_scope(p,source_index)
    fs=factors(p); b=p['base']; st=p['template']
    if st=='combine': prompt='Express $'+signed_sum([log(b,f) for f in fs],s,p['order'])+'$ as a single logarithm.'
    else: prompt='$'+log(b,product_ratio(fs,s,p['order']))+'=$'
    worked=solution(p)
    original_label=None
    if source_index is None:
        alternatives=rng.sample([v for v in SIGNS if v!=s],4)
        vectors=[s]+alternatives
        rng.shuffle(vectors)
        values=[answer(p,v) for v in vectors]; key=vectors.index(s)
        profile='signed-factor-five-v1'
        if st=='combine': prompt+=' Assume $'+p['u']+'>0$ and $'+p['v']+'>0$.'
        else: prompt='Assume $'+p['u']+'>0$.\n\n'+prompt
    else:
        case=json.loads(Path(__file__).with_name('source_cases.json').read_text())[source_index]
        values,key=source_bank(source_index,p); vectors=None
        profile='source-'+case['source'][':question/math-academy-id']
        if p==dict(case['params'],order=[0,1,2]):
            prompt=case['source'][':question/problem']
            worked=case['source'].get(':question/worked-solution',worked)
        original_label=case['source'].get(':question/difficulty')
    prompt=normalize_prose(prompt); worked=normalize_prose(worked)
    values=[normalize_tex(v) for v in values]
    # Order-independent content identity includes the complete bank and key value.
    identity=json.dumps([prompt,sorted(values),values[key]],ensure_ascii=False)
    qid=uid(identity); fid=uid(qid+':selection')
    choices=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
    q={':question/id':qid,':question/problem':prompt,':question/worked-solution':worked,
       ':question/difficulty':':question.difficulty/moderate', ':question/answer-fields':[
           {':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',
            ':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[key][':answer/id']]}]}
    return {'knowledge_point':KP.copy(),'question':q,'generation':{
        'version':VERSION,'seed':seed,'template':st,'profile':profile,'parameters':p,
        'scope':'source factor roles; two positive terms and one subtracted term',
        'choice_vectors':vectors,'source_index':source_index,'original_difficulty':original_label,
        'source_references':['q-47200','e-4085'] if st=='combine' else ['q-47203','q-100242','q-66781']}}

def sample(rng):
    # Select decision structure before compatible numerical and cosmetic slots.
    st=rng.choice(['combine','expand'])
    s=(1,1,-1) if st=='combine' else rng.choice(((1,-1,1),(-1,1,1)))
    b=rng.choice(['10','e']) if st=='combine' else rng.choice(['2','3','5','10','e'])
    k=1 if b=='e' else rng.randint(1,3)
    cs=list(range(2,10))
    if st=='expand' and b!='e': cs=[c for c in cs if c not in [int(b)**j for j in range(1,4)]]
    c=rng.choice(cs); u,v=rng.sample(LETTERS,2)
    top=[i for i in range(3)if s[i]>0];rng.shuffle(top)
    order=top+[i for i in range(3)if s[i]<0]
    p=dict(template=st,signs=list(s),base=b,c=c,u=u,order=order)
    if st=='combine':p['v']=v
    else:p['k']=k
    return p

def generate(difficulty,count,seed):
    if difficulty!='moderate': raise ValueError('Only source-justified moderate difficulty is supported')
    if count<0: raise ValueError('count must be nonnegative')
    rng=random.Random(seed); records=[]; seen=set(); attempts=0
    while len(records)<count:
        attempts+=1
        if attempts>max(100,count*100):raise ValueError('Requested batch exhausts practical unique instances')
        rec=make_record(sample(rng),rng,seed)
        qid=rec['question'][':question/id']
        if qid in seen:continue
        seen.add(qid); records.append(rec)
    return records

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--difficulty',default='moderate',choices=['easy','moderate','hard'])
    a.add_argument('--count',type=int,default=5);a.add_argument('--seed',type=int,default=0)
    a.add_argument('--format',choices=['json'],default='json')
    a.add_argument('--replay-source',action='store_true')
    args=a.parse_args()
    if args.replay_source:
        if args.difficulty!='moderate':a.error('Source replay supports moderate author classification only')
        cases=json.loads(Path(__file__).with_name('source_cases.json').read_text())
        records=[make_record(c['params'],random.Random(args.seed),args.seed,i) for i,c in enumerate(cases)]
    else:
        try:records=generate(args.difficulty,args.count,args.seed)
        except ValueError as e:a.error(str(e))
    print(json.dumps(records,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
