#!/usr/bin/env python3
"""Seeded sine sum/difference practice; runtime uses only the standard library."""
import argparse
import hashlib
import json
from pathlib import Path
import random
import uuid
from math_format import normalize_prose, normalize_tex, validate_tex, validate_generated_record

KP = 17592186059820
VERSION = '2.0.0'
# Angle numerator/denominator in turns of pi, exact cosine, exact sine.
AXES = [(1, 2, '0', '1'), (1, 1, '-1', '0'),
        (3, 2, '0', '-1')]
HALF = r'\frac{1}{2}'
R2 = r'\frac{\sqrt{2}}{2}'
R3 = r'\frac{\sqrt{3}}{2}'
NONAXES = [(1,6,R3,HALF),(1,4,R2,R2),(1,3,HALF,R3),
           (2,3,'-'+HALF,R3),(3,4,'-'+R2,R2),(5,6,'-'+R3,HALF),
           (7,6,'-'+R3,'-'+HALF),(5,4,'-'+R2,'-'+R2),(4,3,'-'+HALF,'-'+R3),
           (5,3,HALF,'-'+R3),(7,4,R2,'-'+R2),(11,6,R3,'-'+HALF)]

def enum(kind, name):
    return {':db/ident': ':'+kind+'/'+name}

def uid(s):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'course-academy/sine-radians/v1/'+s))

def neg(v):
    return '0' if v=='0' else v[1:] if v.startswith('-') else '-'+v

def angle(n,d):
    p=(str(n) if n!=1 else '')+r'\pi'
    return p if d==1 else r'\frac{'+p+'}{'+str(d)+'}'

def term(c,fn):
    if c=='0': return ''
    if c=='1': return fn
    if c=='-1': return '-'+fn
    return c+fn

def expression(a,b,var):
    left,right=term(a,r'\sin '+var),term(b,r'\cos '+var)
    if not left: return right or '0'
    return left+('' if not right or right.startswith('-') else '+')+right

def field(key,kind,values,correct=0):
    choices=[{':answer/type':enum('answer.type','math'),':answer/value':normalize_tex(v)} for v in values]
    return {':answer-field/key':key,':answer-field/type':enum('answer-field.type',kind),
            ':answer-field/choices':choices, '_correct_index':correct}

def finalize(q,metadata):
    for f in q[':question/answer-fields']:
        for a in f[':answer-field/choices']:
            a[':answer/value']=validate_tex(normalize_tex(a[':answer/value']))
            if ':answer/feedback' in a: a[':answer/feedback']=normalize_prose(a[':answer/feedback'])
    # Normalize before content identity. IDs deliberately ignore seed and cosmetic order.
    q[':question/problem']=normalize_prose(q[':question/problem'])
    q[':question/worked-solution']=normalize_prose(q[':question/worked-solution'])
    # Use rendered content and correct values, never incidental UUIDs.
    identity={'problem':q[':question/problem'],'solution':q[':question/worked-solution'],
              'difficulty':q[':question/difficulty'],'fields':[{'key':f[':answer-field/key'],
              'kind':f[':answer-field/type'],'bank':sorted(a[':answer/value'] for a in f[':answer-field/choices']),
              'correct':f[':answer-field/choices'][f['_correct_index']][':answer/value']} for f in q[':question/answer-fields']]}
    digest=hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest()
    q[':question/id']=uid(digest)
    for f in q[':question/answer-fields']:
        key=digest+'/'+f[':answer-field/key']; f[':answer-field/id']=uid(key)
        correct=f.pop('_correct_index')
        for a in f[':answer-field/choices']: a[':answer/id']=uid(key+'/'+a[':answer/value'])
        f[':answer-field/correct']=[':answer/id',f[':answer-field/choices'][correct][':answer/id']]
    r={'knowledge_point':KP,'question':q,'generation':{'version':VERSION,**metadata}}
    validate_generated_record(r)
    return r

def build(level, row, op, shape, var='x', rng=None, error_sign_offset=None):
    rng=rng or random.Random(0)
    n,d,c,s=row; ang=angle(n,d); b=s if op=='+' else neg(s)
    inp=r'\sin\left('+var+op+ang+r'\right)'
    final=expression(c,b,var)
    identity=r'\sin(u'+op+r'v)=\sin u\cos v'+op+r'\cos u\sin v'
    problem='Express $'+inp+r'$ in terms of $\sin '+var+r'$ and $\cos '+var+'$.'
    fields=[]
    profile='signed-coefficients'
    if shape=='blank':
        problem+=' Enter both signed coefficients, including zero when needed.\n\n$'+inp+'=$ {{field-1}} $'+r'\sin '+var+'+$ {{field-2}} $'+r'\cos '+var+'$'
        fields=[field('field-1','blank',[c]),field('field-2','blank',[b])]
    else:
        if level!='hard':
            values=[r'\sin '+var,r'-\sin '+var,r'\cos '+var,r'-\cos '+var,'1']
            profile='axis-functions-and-constant'
        else:
            ac,ab=c.lstrip('-'),b.lstrip('-')
            values=[expression(a,bv,var) for a in (ac,'-'+ac) for bv in (ab,'-'+ab)]
            if error_sign_offset is None:
                error_sign_offset=rng.randrange(4)
            # A complete four-sign grid necessarily repeats the fifth option's
            # signs. Rotate the relationship to the key, rather than letting
            # a short batch accidentally teach "copy the odd option's signs".
            extra_a='-' if c.startswith('-') ^ bool(error_sign_offset & 1) else ''
            extra_b='-' if b.startswith('-') ^ bool(error_sign_offset & 2) else ''
            # One wrong reference-angle evaluation, alongside the complete sign grid.
            if ac!=ab:
                extra=expression(extra_a+ab,extra_b+ac,var); profile='sign-grid-and-swapped-values'
            else:
                wrong=HALF if ac==R2 else R2
                extra=expression(extra_a+wrong,extra_b+wrong,var)
                profile='sign-grid-and-reference-value'
            values.append(extra)
        assert len(values)==len(set(values))==5 and final in values
        rng.shuffle(values)
        fields=[field('selection','radio',values,values.index(final))]
    name='sum' if op=='+' else 'difference'
    solution='Use the '+name+' formula for sine:\n\n$$\n'+identity+'.\n$$\n\n'
    if level=='hard':
        from fractions import Fraction
        f=Fraction(n,d)
        quadrant=min(int(f*2)+1,4)
        ref=min(f%1,1-f%1)
        reftex=angle(ref.numerator,ref.denominator)
        solution+='The fixed angle $'+ang+'$ is in quadrant '+['I','II','III','IV'][quadrant-1]+' with reference angle $'+reftex+'$. Thus\n\n'
    else:
        solution+='The fixed angle has exact values\n\n'
    solution+='$$\n'+r'\cos\left('+ang+r'\right)='+c+r',\qquad \sin\left('+ang+r'\right)='+s+'.\n$$\n\n'
    solution+='Substitute $u='+var+'$ and $v='+ang+'$, then simplify the coefficients:\n\n$$\n'+r'\begin{aligned}'+'\n'+inp+'&='+r'\sin '+var+r'\cos\left('+ang+r'\right)'+op+r'\cos '+var+r'\sin\left('+ang+r'\right)'+r'\\'+'\n'
    solution+='&='+r'\sin '+var+r'\left('+c+r'\right)'+op+r'\cos '+var+r'\left('+s+r'\right)'+r'\\'+'\n'+'&='+final+'.\n'+r'\end{aligned}'+'\n$$'
    if shape=='blank':
        solution+='\n\nThe requested coefficients are $'+c+'$ and $'+b+'$, respectively. A negative coefficient goes inside its blank.'
    return finalize({':question/problem':problem,':question/worked-solution':solution,
                     ':question/difficulty':enum('question.difficulty',level),':question/answer-fields':fields},
                    {'template':'axis' if level!='hard' else 'nonaxis','shape':shape,'profile':profile,
                     'parameters':{'n':n,'d':d,'operator':op,'variable':var},'domain':'all real variable values',
                     'source_support':['78f7a073-b897-5930-bd54-7d5e600e42be','7d2e5f2f-dd16-5fbd-88cd-c72fe86e0b28'] if level!='hard' else ['0ce71d86-7470-5d53-ac94-20b473889dee','78623ec6-7143-54b5-8ec3-a1bf17721f5e']})

def replay(source_id):
    q=json.loads((Path(__file__).parent/'replay-data.json').read_text())[source_id]
    q.pop(':question/id',None)
    for f in q[':question/answer-fields']:
        correct=f[':answer-field/correct'][1]
        f['_correct_index']=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==correct)
        f.pop(':answer-field/id',None); f.pop(':answer-field/correct',None)
        for a in f[':answer-field/choices']: a.pop(':answer/id',None)
    return finalize(q,{'template':'source-replay','source_question_ids':[source_id]})

def generate(level,count,seed):
    if level=='unclassified': level='moderate'
    if count<0:raise ValueError('count must be nonnegative')
    rng=random.Random(seed)
    catalog=[(row,op) for row in (NONAXES if level=='hard' else AXES) for op in ['+','-']]
    if count>len(catalog):raise ValueError(f'{level} supports {len(catalog)} mathematical shifts; requested {count}')
    records=[]; cycle=0
    # Separate response shapes must not accidentally freeze an answer-bearing role
    # in a small batch. Alternate the decisive role within each served shape,
    # while exhausting every compatible semantic case before starting again.
    previous={}
    error_offsets={}
    while len(records)<count:
        remaining=list(catalog)
        while remaining and len(records)<count:
            i=len(records)
            shape='radio' if level=='easy' else ('radio' if i%2==0 else 'blank')
            candidates=remaining
            old=previous.get(shape)
            if old:
                if level=='hard':
                    opposite=[c for c in candidates if c[0][2].startswith('-') != old[0][2].startswith('-')]
                    if opposite:candidates=opposite
                    different_reference=[c for c in candidates if c[0][1]!=old[0][1]]
                    if different_reference:candidates=different_reference
                else:
                    different_survivor=[c for c in candidates if (c[0][2]=='0') != (old[0][2]=='0')]
                    if different_survivor:candidates=different_survivor
                    # When returning to a role, prefer its opposite sign if available.
                    role=candidates[0][0][2]=='0'
                    earlier=[r for r in records if r['generation']['shape']==shape
                             and (r['generation']['parameters']['d']==2)==role]
                    if earlier:
                        oldrow=next(c[0] for c in catalog if c[0][:2]==(earlier[-1]['generation']['parameters']['n'],earlier[-1]['generation']['parameters']['d']))
                        oldop=earlier[-1]['generation']['parameters']['operator']
                        oldcoef=oldrow[2] if oldrow[2]!='0' else (oldrow[3] if oldop=='+' else neg(oldrow[3]))
                        different_sign=[c for c in candidates if (c[0][2] if c[0][2]!='0' else (c[0][3] if c[1]=='+' else neg(c[0][3])))!=oldcoef]
                        if different_sign:candidates=different_sign
            row,op=rng.choice(candidates)
            remaining.remove((row,op));previous[shape]=(row,op)
            offset=None
            if level=='hard' and shape=='radio':
                family='sqrt2' if row[1]==4 else 'sqrt3'
                if not error_offsets.get(family):
                    offsets=[0,1,2,3]
                    rng.shuffle(offsets)
                    # Adjacent four-case cycles also cannot repeat a match.
                    if error_offsets.get(family+'_last')==0 and offsets[-1]==0:
                        offsets[0],offsets[-1]=offsets[-1],offsets[0]
                    error_offsets[family]=offsets
                offset=error_offsets[family].pop()
                error_offsets[family+'_last']=offset
            r=build(level,row,op,shape,'x',rng,error_sign_offset=offset)
            r['generation'].update({'seed':seed,'catalog_cycle':cycle,'mathematical_capacity':len(catalog),'calibration':'authored overlapping axis band; no imported easy anchor' if level=='easy' else 'imported same-skill family'})
            records.append(r)
        cycle+=1
    return records

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified'],default='moderate')
    p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0)
    p.add_argument('--format',choices=['json'],default='json');p.add_argument('--replay',help='Complete source question UUID')
    args=p.parse_args()
    if args.count<0: p.error('count must be nonnegative')
    print(json.dumps([replay(args.replay)] if args.replay else generate(args.difficulty,args.count,args.seed),ensure_ascii=False,indent=2))

if __name__=='__main__': main()
