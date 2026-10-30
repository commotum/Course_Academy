"""Seeded coordinate-range practice. No runtime repository or database access.

The coordinate inequality stages retain the legacy generator's scale/reverse/
translate method; the restricted-domain and attainment design follows the
investigation's complete hard exemplar. See instructional-account.md.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid
from fractions import Fraction as F
from math_format import normalize_prose, normalize_tex, validate_generated_record

VERSION = '2.0.2'
KP = {'db_id':17592186087736,'id':'cddc940d-2185-569c-a62b-b507e95d3c35',
      'title':'Determining the Range of a Parametric Equation Defined in Terms of Trigonometric Functions'}
SUPPORT = {'easy':['cbb8764c-a924-5241-b809-c578415b87f2','b4154359-18f0-56b5-8f88-83b3d5f9fa49','39f52df2-f7c2-52ca-a128-fe39a8ac5d3e'],
           'moderate':['988a63cd-e232-53ca-b2d0-b9ce061f192c','4c592e38-9872-58d6-ad10-d75e6115be4c'],
           'hard':['8714e1c8-2824-5d74-a7c0-997378cd464d','72d3f4c9-33bf-5f30-b80b-da478efa9772']}

def tex(v):
    v=F(v)
    if v.denominator==1:return str(v.numerator)
    return ('-' if v<0 else '')+r'\frac{'+str(abs(v.numerator))+'}{'+str(v.denominator)+'}'

def angle(q):
    if not q:return '0'
    if q==2:return r'\pi'
    if q%2==0:return str(q//2)+r'\pi'
    return r'\frac{'+('' if q==1 else str(q))+r'\pi}{2}'

def value(fn,q):return ((1,0,-1,0) if fn=='cos' else (0,1,0,-1))[q%4]
def cmp(included):return r'\le ' if included else '<'
def trig(fn):return '\\'+fn+r'\theta'
def scaled(c,fn):return ('' if c==1 else '-' if c==-1 else tex(c))+trig(fn)
def formula(c,d,fn):
    return scaled(c,fn)+('+'+tex(d) if d>0 else tex(d) if d<0 else '')
def bounds_text(v,var):return tex(v[0])+cmp(v[2])+var+cmp(v[3])+tex(v[1])
def display(rows):return '$$\n'+r'\begin{aligned}'+'\n'+(' '+r'\\'+'\n').join(rows)+'\n'+r'\end{aligned}'+'\n$$'
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'parametric-range-v2:'+s))

def trig_image(fn,domain):
    start,end,left,right=domain
    points=[(q,value(fn,q),(q>start or left) and (q<end or right)) for q in range(start,end+1)]
    lo=min(p[1] for p in points);hi=max(p[1] for p in points)
    return (F(lo),F(hi),any(v==lo and inc for _,v,inc in points),any(v==hi and inc for _,v,inc in points)),points

def coordinate(c,d,fn,domain,var):
    c,d=F(c),F(d)
    if c==0:raise ValueError('A nonzero scale is required')
    base,points=trig_image(fn,domain)
    lo,hi,lc,rc=base
    final=(c*lo+d,c*hi+d,lc,rc) if c>0 else (c*hi+d,c*lo+d,rc,lc)
    pieces=[]
    if domain==(0,4,True,False):
        pieces.append('Over the full turn, $'+trig(fn)+'$ attains both $-1$ and $1$, including at permitted parameter values.')
    else:
        pieces.append('Check the quarter-turn points in the parameter interval and its endpoint limits: '+
          '; '.join('$'+r'\theta='+angle(q)+'$ gives $'+trig(fn)+'='+str(v)+'$'+(' (included)' if inc else ' (excluded endpoint)') for q,v,inc in points)+'.')
        for bound,included in [(lo,lc),(hi,rc)]:
            hits=[angle(q) for q,v,inc in points if v==bound and inc]
            pieces.append('The value $'+tex(bound)+'$ '+('is attained at $'+r'\theta='+', '.join(hits)+'$.' if included else 'is approached at an excluded endpoint and is not attained elsewhere in the interval.'))
    rows=[tex(lo)+' &'+cmp(lc)+trig(fn)+cmp(rc)+tex(hi)]
    if c<0:
        lcmp=r'\ge' if lc else '>'; rcmp=r'\ge' if rc else '>'
        pieces.append('Multiplying by $'+tex(c)+'$ reverses both comparisons; translate by $'+tex(d)+'$, then write the bounds in increasing order.')
    else:
        lcmp=cmp(lc);rcmp=cmp(rc)
        pieces.append('Multiply by $'+tex(c)+'$'+(' and translate by $'+tex(d)+'$' if d else '')+'.')
    if c!=1:rows.append(tex(c*lo)+' &'+lcmp+scaled(c,fn)+rcmp+tex(c*hi))
    if d:rows.append(tex(c*lo+d)+' &'+lcmp+formula(c,d,fn)+rcmp+tex(c*hi+d))
    rows.append(tex(final[0])+' &'+cmp(final[2])+var+cmp(final[3])+tex(final[1])+'.')
    pieces.append(display(rows))
    pieces.append('Thus $'+bounds_text(final,var)+'$.')
    return final,'\n\n'.join(pieces),{'base_image':[str(lo),str(hi),lc,rc],'witnesses':points,'rows':rows,'final':bounds_text(final,var)}

def build(level,a,b,h,k,domain=(0,4,True,False),functions=('cos','sin'),family=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Invalid difficulty')
    domain=tuple(domain);a,b,h,k=map(F,(a,b,h,k))
    start,end,left,right=domain
    if not (isinstance(start,int) and isinstance(end,int) and start<end and all(isinstance(x,bool) for x in (left,right))):raise ValueError('Quarter-turn domain required')
    if set(functions)!={'cos','sin'}:raise ValueError('One sine and one cosine required')
    xr,xsolution,xpath=coordinate(a,h,functions[0],domain,'x')
    yr,ysolution,ypath=coordinate(b,k,functions[1],domain,'y')
    prompt='Given that a curve is defined parametrically as\n\n$$\nx='+formula(a,h,functions[0])+'\n$$\n\n$$\ny='+formula(b,k,functions[1])+'\n$$\n\n$$\n'+angle(start)+cmp(left)+r'\theta'+cmp(right)+angle(end)+'\n$$\n\nwhat are the ranges of $x$ and $y$?'
    vals=[]
    if level=='hard':
        prompt+=' Use $<$ or $\\le$ in the comparison blanks.'
        for j,(var,v) in enumerate([('x',xr),('y',yr)]):
            n=4*j+1
            prompt+='\n\nThe range of $'+var+'$ is {{field-'+str(n)+'}} {{field-'+str(n+1)+'}} $'+var+'$ {{field-'+str(n+2)+'}} {{field-'+str(n+3)+'}}.'
            vals.extend([tex(v[0]),cmp(v[2]),cmp(v[3]),tex(v[1])])
    else:
        if not all(xr[2:]+yr[2:]):raise ValueError('Six-blank scaffold requires attained bounds')
        prompt+='\n\nThe range of $x$ is {{field-1}} {{field-2}} $x\\le$ {{field-3}}.\n\nThe range of $y$ is {{field-4}} $\\le y$ {{field-5}} {{field-6}}.'
        vals=[tex(xr[0]),cmp(xr[2]),tex(xr[1]),tex(yr[0]),cmp(yr[3]),tex(yr[1])]
    solution='Consider each coordinate separately.\n\nFor $x$:\n\n'+xsolution+'\n\nFor $y$:\n\n'+ysolution+'\n\nContinuity gives every value between the stated bounds. The coordinate extrema need not occur at the same parameter value.'
    prompt,solution=map(normalize_prose,(prompt,solution));vals=list(map(normalize_tex,vals))
    identity=hashlib.sha256(json.dumps([level,prompt,solution,vals],ensure_ascii=False).encode()).hexdigest()
    fields=[]
    for i,v in enumerate(vals,1):
        fid=uid(identity+':field:'+str(i));aid=uid(fid+':'+v)
        fields.append({':answer-field/id':fid,':answer-field/key':'field-'+str(i),':answer-field/type':':answer-field.type/blank',':answer-field/choices':[{':answer/id':aid,':answer/type':':answer.type/math',':answer/value':v}],':answer-field/correct':[':answer/id',aid]})
    record={'knowledge_point':KP.copy(),'question':{':question/id':uid(identity),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields},
     'generation':{'version':VERSION,'template':family or ('restricted-domain' if level=='hard' else 'full-turn'),'parameters':dict(zip(('a','b','h','k'),map(str,(a,b,h,k)))),'functions':list(functions),'domain_quarters':list(domain),'source_question_ids':SUPPORT[level],
      'solution_path':{'x':xpath,'y':ypath,'required_conversions':['reverse inequalities under negative multiplication'] if a<0 or b<0 else [],'keyed_fragments':vals},'plot_assets':{},'semantic_identity':identity}}
    return validate_generated_record(record)

def generate_batch(difficulty,count,seed):
    level='moderate' if difficulty=='unclassified' else difficulty
    rng=random.Random(seed)
    records=[];seen=set()
    cases=list(range(32)) if level=='hard' else list(range(8))
    while len(records)<count:
        rng.shuffle(cases)
        for case in cases:
            functions=('cos','sin') if rng.randrange(2) else ('sin','cos')
            signs=[rng.choice([-1,1]) for _ in range(2)]
            if level=='easy':
                if case%2:
                    a,b=signs;h,k=[rng.randint(-4,4) for _ in range(2)];family='unit-translation'
                else:
                    a,b=[s*rng.randint(2,7) for s in signs];h=k=0;family='scale-only'
                domain=(0,4,True,False)
            else:
                a,b=[F(s*rng.randint(2,5)) for s in signs];h,k=[rng.choice([-3,-2,-1,1,2,3]) for _ in range(2)]
                if level=='moderate':
                    if case%4==0:
                        if case<4:a=signs[0]*F(rng.choice([3,5]),2)
                        else:b=signs[1]*F(rng.choice([3,5]),2)
                    domain=(0,4,True,False);family='scale-translation'
                else:
                    start=case//8;length=2+(case//4)%2
                    domain=(start,start+length,bool(case&1),bool(case&2));family='restricted-domain'
            rec=build(level,a,b,h,k,domain,functions,family)
            semantic=(str(a),str(b),str(h),str(k),domain,functions)
            if semantic in seen:continue
            seen.add(semantic);rec['generation']['seed']=seed;rec['generation']['batch_index']=len(records)
            records.append(rec)
            if len(records)==count:break
    return records

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified','all'],default='moderate')
    parser.add_argument('--count',type=int,default=1);parser.add_argument('--seed',type=int,default=0)
    parser.add_argument('--format',choices=['json'],default='json')
    args=parser.parse_args()
    if not 1<=args.count<=10000:parser.error('count must be between 1 and 10000')
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    print(json.dumps([r for level in levels for r in generate_batch(level,args.count,args.seed)],indent=2,ensure_ascii=False))
if __name__=='__main__':main()
