#!/usr/bin/env python3
"""Seeded, relocatable integrating-factor practice. Standard library only."""
import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
import math
import random
import uuid
from math_format import normalize_prose, normalize_tex, validate_generated_record

KP = {'db_id': 17592186217247, 'id': '54d19544-7156-58e9-a090-12f8e9492226',
      'title': 'Testing Integrating Factors for ODEs in Differential Form'}
SOURCES = {'A': {'entity_id':17592186217794,'id':'a9a8802d-3d4d-5564-8390-a80c9704bb8e','math_academy_id':'q-337133','difficulty':'easy'},
           'B': {'entity_id':17592186311824,'id':'9e2b872a-4e35-5059-b33b-25da543bae2e','math_academy_id':'q-337259','difficulty':'easy'}}

class InvalidInstance(ValueError):
    pass

@dataclass(frozen=True)
class Mono:
    c: Fraction
    x: int = 0
    y: int = 0
    def __post_init__(self): object.__setattr__(self,'c',Fraction(self.c))
    def mul(self,o): return Mono(self.c*o.c,self.x+o.x,self.y+o.y)
    def inv(self): return Mono(1/self.c,-self.x,-self.y)
    def neg(self): return Mono(-self.c,self.x,self.y)
    def scale(self,k): return Mono(self.c*k,self.x,self.y)
    def shift(self,x=0,y=0): return Mono(self.c,self.x+x,self.y+y)
    def diff(self,var):
        k = self.x if var=='x' else self.y
        return Mono(self.c*k,self.x-(var=='x'),self.y-(var=='y'))
    def tex(self):
        if self.c==0: return '0'
        num=[]; den=[]
        c=abs(self.c)
        for v,e in [('x',self.x),('y',self.y)]:
            if e: (num if e>0 else den).append(v if abs(e)==1 else v+'^{'+str(abs(e))+'}')
        if c.numerator!=1 or not num: num.insert(0,str(c.numerator))
        if c.denominator!=1: den.insert(0,str(c.denominator))
        body=' '.join(num)
        if den: body=r'\frac{'+body+'}{'+' '.join(den)+'}'
        return ('-' if self.c<0 else '')+body

def form(p,q):
    return p.tex()+r'\,\mathrm{d}x'+(' - ' if q.c<0 else ' + ')+Mono(abs(q.c),q.x,q.y).tex()+r'\,\mathrm{d}y'

def display(t): return '$$\n'+t+'\n$$'
def aligned(rows): return display(r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}')

SOURCE_PARAMS = {'A':dict(a=1,b=1,u=0,m=1,n=1,v=0,r=-3,s=1),
                 'B':dict(a=1,b=1,u=0,m=2,n=2,v=0,r=0,s=-1)}

def construct(params,profile,rng=None,seed=None,bank_style="authored"):
    a,b,u,m,n,v,r,s=[params[k] for k in ('a','b','u','m','n','v','r','s')]
    P,Q,I=Mono(-b,u,m),Mono(a,n,v),Mono(1,r,s)
    if I.x==0 and I.y==0: raise InvalidInstance('Constant factor eliminates multiplication skill')
    p,q=P.mul(I),Q.mul(I); d,e=p.diff('y'),q.diff('x')
    if not d.c or not e.c or P.diff('y')==Q.diff('x'):
        raise InvalidInstance('Require an inexact original and two nonzero cross partials')
    exact=d==e
    if profile=='A':
        forms=[(p,q),(p.inv(),q.inv().neg()),(q,p),(q.inv(),p.inv())]
        dbank=[d,d.scale(Fraction(1,2)),d.shift(y=-1),d.neg()]
        ebank=[e,q.shift(y=-1).neg(),q,e.neg()]
    else:
        forms=[(p,q),(Q.mul(I.inv()),p),(q,p),(p,Q.mul(I.inv()).neg())]
        dbank=[d,d.neg(),d.shift(y=-1),d.shift(y=-1).neg()]
        ebank=[e,e.scale(Fraction(1,2)),p.shift(y=-2),e.shift(x=-1)]
    if not (len(set(forms))==4 and len(set(dbank))==4 and len(set(ebank))==4):
        raise InvalidInstance('Coincident choices in complete selected bank')
    if bank_style == 'authored':
        # Both fields offer the entire same Cartesian bank. Bank intersection,
        # repeated coefficients and unique opposite-sign pairs cannot supply keys.
        bank_rng = rng or random.Random(json.dumps(params, sort_keys=True)+profile)
        coefficients = list(dict.fromkeys([d.c, e.c]))
        powers = list(dict.fromkeys([(d.x,d.y), (e.x,e.y)]))
        if len(coefficients) == 1:
            multiplier = bank_rng.choice([Fraction(1,2), Fraction(2), Fraction(-1), Fraction(-2), Fraction(-1,2)])
            coefficients.append(d.c * multiplier)
        if len(powers) == 1:
            axis, delta = bank_rng.choice([('x',-1),('x',1),('y',-1),('y',1)])
            powers.append((d.x+(delta if axis=='x' else 0),d.y+(delta if axis=='y' else 0)))
        dbank = [Mono(c,px,py) for c in coefficients for px,py in powers]
        ebank = dbank.copy()
        assert len(set(dbank)) == 4 and d in dbank and e in ebank
    elif bank_style != 'source':
        raise ValueError('Unknown bank style')
    relation=r'\frac{\partial P}{\partial y}'+('=' if exact else r'\ne')+r'\frac{\partial Q}{\partial x}'
    verdict='is' if exact else "isn't"
    banks=[([form(*z) for z in forms],form(p,q),'math'),
           ([z.tex() for z in dbank],d.tex(),'math'),
           ([z.tex() for z in ebank],e.tex(),'math'),
           ([r'\frac{\partial P}{\partial y}=\frac{\partial Q}{\partial x}',r'\frac{\partial P}{\partial y}\ne\frac{\partial Q}{\partial x}'],relation,'math'),
           (['is',"isn't"],verdict,'text'),(['is',"isn't"],verdict,'text')]
    prompt='Consider the following inexact differential equation, on a region where $x\\ne0$ and $y\\ne0$.\n\n'+display(form(P,Q)+'=0')
    prompt+='\n\nSelect the correct options in the reasoning below about whether $I(x,y)='+I.tex()+'$ is an integrating factor of this equation.\n\n'
    prompt+='To test this candidate, multiply both coefficients and check whether the following equation is exact:\n\n'+display('{{field-1}}=0')
    prompt+='\n\nFor this equation, let\n\n'+display('P='+p.tex()+r',\qquad Q='+q.tex()+'.')
    prompt+='\n\nThe corresponding partial derivatives are\n\n'+display(r'\frac{\partial P}{\partial y}={{field-2}},\qquad \frac{\partial Q}{\partial x}={{field-3}}.')
    prompt+='\n\nNow, since\n\n'+display('{{field-4}},')+'\n\nthe transformed equation {{field-5}} exact.\n\nTherefore, $I(x,y)='+I.tex()+'$ {{field-6}} an integrating factor for the initial differential equation.'
    solution='A candidate is an integrating factor if multiplying the equation by it gives an exact equation. First multiply both coefficients:\n\n'
    solution+=aligned([I.tex()+r'\left('+form(P,Q)+r'\right)&=0',form(p,q)+'&=0'])
    solution+='\n\nFor the transformed equation,\n\n'+display('P='+p.tex()+r',\qquad Q='+q.tex()+'.')
    solution+='\n\nThe exactness test compares the partial derivatives as functions on the region:\n\n'
    solution+=aligned([r'\frac{\partial P}{\partial y}&=\frac{\partial}{\partial y}\left('+p.tex()+r'\right)='+d.tex(),r'\frac{\partial Q}{\partial x}&=\frac{\partial}{\partial x}\left('+q.tex()+r'\right)='+e.tex()])
    solution+='\n\nSince\n\n'+display(relation+',')+'\n\nthe transformed equation '+verdict+' exact. Therefore, $I(x,y)='+I.tex()+'$ '+verdict+' an integrating factor for the initial equation.'
    prompt=normalize_prose(prompt); solution=normalize_prose(solution)
    banks=[([normalize_tex(z) if typ=='math' else normalize_prose(z) for z in bank],normalize_tex(correct) if typ=='math' else normalize_prose(correct),typ) for bank,correct,typ in banks]
    # All prose/TeX is normalized before any content-derived identity.
    payload=json.dumps([prompt,solution,[(sorted(bank),correct,typ) for bank,correct,typ in banks]],sort_keys=True)
    qid=uuid.uuid5(uuid.UUID(KP['id']),hashlib.sha256(payload.encode()).hexdigest())
    fields=[]
    for i,(bank,correct,typ) in enumerate(banks,1):
        fid=uuid.uuid5(qid,'field-'+str(i)); answers=[]; correct_id=None
        for value in bank:
            aid=str(uuid.uuid5(fid,typ+':'+value)); answers.append({':answer/id':aid,':answer/type':':answer.type/'+typ,':answer/value':value})
            if value==correct: correct_id=aid
        if rng: rng.shuffle(answers)
        fields.append({':answer-field/id':str(fid),':answer-field/key':'field-'+str(i),':answer-field/type':':answer-field.type/select',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]})
    rec={'knowledge_point':KP.copy(),'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/easy',':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields},
         'generation':{'generator':'integrating-factor-v2','template':'monomial-six-select','profile':profile,'derivative_bank':bank_style,'derivative_ranks':[sorted(bank,key=lambda z:(z.c*Fraction(2)**z.x*Fraction(3)**z.y,z.tex())).index(target) for bank,target in [(dbank,d),(ebank,e)]],'seed':seed,'parameters':params.copy(),'domain':'x != 0, y != 0','source_questions':[SOURCES[profile]],'lesson_support':[17592186218336,17592186218357,17592186216979],'source_replay':bank_style=='source' and params==SOURCE_PARAMS[profile]}}
    return validate_generated_record(rec)

def sample_params(rng,case,sign_pattern=None):
    if case=='mismatch':
        return dict(a=rng.randint(1,3),b=rng.randint(1,3),u=0,m=2,n=2,v=0,r=rng.choice([-3,-1,0]),s=rng.choice([-1,0]))
    n=rng.choice([1,2]); m=rng.choice([1,2])
    # t=m+s and h=n+r are the differentiated powers. Their signs are
    # independent of success: both same-sign and opposite-sign original
    # coefficients can satisfy -b*t=a*h. Keep all power-rule work small.
    t=rng.choice([-1,1])*rng.choice([1,2,3])
    h=(1 if t>0 else -1)*(1 if sign_pattern=='same' else -1)*rng.choice([1,2,3])
    g=math.gcd(abs(t),abs(h)); scale=rng.choice([1,2,3])
    a=t//g*scale; b=-h//g*scale
    if case=='no': b += 1 if b>0 else -1
    return dict(a=a,b=b,u=n-1,m=m,n=n,v=m-1,r=h-n,s=t-m)

def _draw(count,rng,seed):
    records=[]; seen=set()
    while len(records)<count:
        patterns=['same','opposite']; rng.shuffle(patterns)
        schedule=[('yes','A',patterns[0]),('no','B',patterns[0]),
                  ('yes','B',patterns[1]),('no','A',patterns[1]),
                  ('mismatch',rng.choice(['A','B']),None)]; rng.shuffle(schedule)
        for case,profile,sign_pattern in schedule:
            if len(records)==count: break
            for attempt in range(10000):
                try:
                    params=sample_params(rng,case,sign_pattern)
                    direction=rng.choice([-1,1])
                    params['a']*=direction; params['b']*=direction
                    rec=construct(params,profile,rng,seed)
                except InvalidInstance: continue
                semantic_key=tuple(sorted(params.items()))
                if semantic_key not in seen: break
            else: raise ValueError('Requested count exhausted supported semantic catalog')
            seen.add(semantic_key); rec['generation']['decision_case']=case; records.append(rec)
    return records

def _cue_groups(records):
    groups=[records]
    groups += [[r for r in records if r['generation']['profile']==p] for p in ['A','B']]
    for same in [True,False]:
        groups.append([r for r in records if (-r['generation']['parameters']['a']*r['generation']['parameters']['b']>0)==same])
    return [group for group in groups if len(group)>=2]

def _varied_ranks(records):
    return all(len({r['generation']['derivative_ranks'][field] for r in group})>1
               for group in _cue_groups(records) for field in [0,1])

def _balance_positions(records,rng):
    groups=_cue_groups(records)
    by_identity={id(record):index for index,record in enumerate(records)}
    for field in range(6):
        size=len(records[0]['question'][':question/answer-fields'][field][':answer-field/choices'])
        for attempt in range(10000):
            positions=[rng.randrange(size) for _ in records]
            if all(len({positions[by_identity[id(r)]] for r in group})>1 for group in groups): break
        else: raise ValueError('Could not arrange varied answer positions')
        for record,wanted in zip(records,positions):
            f=record['question'][':question/answer-fields'][field];bank=f[':answer-field/choices']
            current=next(i for i,a in enumerate(bank) if a[':answer/id']==f[':answer-field/correct'][1])
            bank[current],bank[wanted]=bank[wanted],bank[current]

def generate(count,seed,difficulty='easy'):
    if difficulty=='unclassified': difficulty='easy'
    if difficulty!='easy': raise ValueError('Difficulty not implemented in this easy-focused package: '+difficulty)
    if count<0: raise ValueError('count must be nonnegative')
    if not count: return []
    rng=random.Random(seed)
    # A candidate batch is accepted only after the same bank-only rank probes
    # used in review have counterexamples overall and within the two source
    # form-bank signatures and original coefficient-sign groups. The draw
    # remains deterministic from the caller's seed; no seed search is used.
    for attempt in range(10000):
        records=_draw(count,rng,seed)
        if _varied_ranks(records):
            _balance_positions(records,rng)
            return records
    raise ValueError('Could not construct a batch without the declared bank cues')

def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--difficulty',default='easy'); p.add_argument('--count',type=int,default=5); p.add_argument('--seed',type=int,required=True); p.add_argument('--format',choices=['json'],default='json'); a=p.parse_args()
    try: records=generate(a.count,a.seed,a.difficulty)
    except ValueError as e: p.error(str(e))
    print(json.dumps(records,indent=2,ensure_ascii=False))
if __name__=='__main__': main()
