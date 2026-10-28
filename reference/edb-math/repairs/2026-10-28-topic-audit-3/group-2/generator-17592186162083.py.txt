#!/usr/bin/env python3
"""Relocatable, deterministic scalar-line-integral practice generator.

Runtime uses only the standard library and the bundled shared math formatter.
Curve/decision assignments are selected before incidental numeric parameters.
"""
import argparse
import hashlib
import json
import random
import uuid
from fractions import Fraction
from pathlib import Path
from math_format import normalize_prose, normalize_tex, validate_generated_record

VERSION = '3.1.0'
KP = {'db_id':17592186162083, 'id':'96d48adf-a293-54ae-88fd-ee8471e5fc65',
      'title':'Applying Independence of Parametrization and Orientation'}
NS = uuid.UUID(KP['id'])
FAMILIES = {'easy':['orientation'], 'moderate':['quartic','circle','power'], 'hard':['hyperbola','root']}
SOURCE = {'quartic':'5b1e210e-8810-5093-9deb-eb8812e9311b',
          'circle':'533221ac-cdcc-53a5-adcd-03f57c6b1b57',
          'power':'aba31fa9-c0e0-5ac2-bdfd-ad58b74f6f1a',
          'hyperbola':'67eba06b-e142-51bc-86cf-6cd55545886d',
          'root':'261c6852-f708-5ef6-9e89-3d88f4dbba8b',
          'orientation':'50893ffd-9138-5cfe-bb3a-272da37be841'}
IMAGE = 'images/e4/e4f68e10429fa4bda69366751c303216d27df995edf2502b61ab9bfe84c3ff45.png'

def tex(v):
    if isinstance(v, str): return v
    v=Fraction(v)
    if v.denominator==1: return str(v.numerator)
    return ('-' if v<0 else '')+r'\frac{'+str(abs(v.numerator))+'}{'+str(v.denominator)+'}'

def times(n, term):
    if n==1:return term
    if n==-1:return '-'+term
    return tex(n)+term

def vector(f,z,p,branch=False):
    z='('+z+')'
    if f=='quartic':return r'\langle '+times(p['c'],z+'^4')+'-'+times(p['d'],z+'^2')+','+z+r'\rangle'
    if f=='circle':return r'\langle '+times(p['c'],r'\cos'+z)+','+times(p['c'],r'\sin'+z)+r'\rangle'
    if f=='power':return r'\langle '+z+','+times(p['c'],z+'^{3/2}')+r'\rangle'
    if f=='hyperbola':return r'\langle '+('-' if branch else '')+r'\sqrt{'+str(p['c'])+'+'+z+'^2},'+z+r'\rangle'
    if f=='root':return r'\langle '+times(p['c'],z)+','+times(-p['d'] if branch else p['d'],r'\sqrt{'+z+'}')+r'\rangle'
    raise ValueError(f)

def integral(label):
    return r'\int_{'+label+r'} f(x,y)\,\mathrm{d}s'

def val(factor,k):
    if k=='k':return times(factor,'k')
    return tex(factor*k)

def assemble(band,problem,solution,fields,generation):
    problem=normalize_prose(problem);solution=normalize_prose(solution)
    for field in fields:
        field[':answer-field/key']=normalize_prose(field[':answer-field/key'])
        for a in field[':answer-field/choices']:
            a[':answer/value']=(normalize_tex if a[':answer/type']==':answer.type/math' else normalize_prose)(a[':answer/value'])
    # Identity is calculated after shared normalization, independently of seed.
    body={'band':band,'problem':problem,'solution':solution,'fields':fields}
    identity=hashlib.sha256(json.dumps(body,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    qid=str(uuid.uuid5(NS,identity))
    for i,field in enumerate(fields):
        fid=str(uuid.uuid5(uuid.UUID(qid),'field:'+str(i)))
        field[':answer-field/id']=fid
        for j,a in enumerate(field[':answer-field/choices']):
            a[':answer/id']=str(uuid.uuid5(uuid.UUID(fid),str(j)+':'+a[':answer/value']))
        correct_index=field.pop('correct_index')
        field[':answer-field/correct']=[':answer/id',field[':answer-field/choices'][correct_index][':answer/id']]
    q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,
       ':question/difficulty':':question.difficulty/'+band,':question/answer-fields':fields}
    r={'knowledge_point':KP.copy(),'question':q,'generation':{'version':VERSION,**generation}}
    return validate_generated_record(r)

def checkbox(statement,truth):
    return {':answer-field/key':statement,':answer-field/type':':answer-field.type/checkbox',
            ':answer-field/choices':[{':answer/type':':answer.type/text',':answer/value':v} for v in ['false','true']],
            'correct_index':int(truth)}

def easy(rng,p=None):
    if p is None:
        omit=rng.randrange(4);reverse=rng.choice([True,False])
        p=dict(omit=omit,reverse=reverse,s=rng.choice([2,3]),k=rng.choice([-8,-5,-3,2,4,7]))
    else:p=dict(p)
    k,s=p['k'],p['s']
    errors=[-k,0,s*k,Fraction(k,s)]
    wrong=[x for i,x in enumerate(errors) if i!=p['omit']]
    values=[Fraction(k),*wrong];rng.shuffle(values)
    diagram=('\n\n![The same curve traversed in opposite directions.]('+IMAGE+')') if p['reverse'] else ''
    orientation='opposite directions' if p['reverse'] else 'the same direction'
    # The diagram's labels remain C and -C; D is named as that same reversed path.
    desc=(r'The path $D=-C$ is the reversed path in the diagram.' if p['reverse'] else r'The path $D$ follows $C$ in the same direction.')
    problem=(r'The paths $C$ and $D$ trace exactly the same geometric arc once, in '+orientation+'. '+desc+diagram+
             '\n\n'+r'The parametrization of $D$ runs '+str(s)+r' times as fast, with its parameter interval shortened accordingly. Suppose $f$ is continuous along the arc and'+'\n\n$$\n'+integral('C')+'='+str(k)+'.\n$$\n\n'+
             r'What is the value of $'+integral('D')+'$?')
    solution=(r'Scalar line integrals with respect to arc length are independent of parametrization and orientation. Both paths cover the same arc once, so'+'\n\n$$\n'+integral('D')+'='+integral('C')+'='+str(k)+'.\n$$\n\n'+
              r'The speed change is offset by the shortened parameter interval. Reversing direction does not negate the integral, and a single traversal does not cancel it. Neither multiplying nor dividing by the parameter speed is appropriate.')
    fields=[{':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',
             ':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':tex(x)} for x in values],
             'correct_index':values.index(Fraction(k))}]
    return assemble('easy',problem,solution,fields,{'template':'orientation','parameters':p,'source_question':SOURCE['orientation'],'bank_profile':'omit-'+str(p['omit'])})

def claim_plan(case,rng):
    """Use the same bank construction for matching and nonmatching arcs.

    An unchanged comparison must be offered so deciding whether it transfers
    requires inspecting the curves. The bank itself must not encode that relation.
    """
    chosen=[(0,'one'),(rng.choice([1,2]),'one')]
    errors=[(role,error) for role in range(3) for error in ['neg','speed','inverse']]
    chosen.append(rng.choice(errors))
    rng.shuffle(chosen)
    return chosen

def sample_parameters(band,rng):
    return {'a':1 if band=='moderate' else rng.choice([2,3]),'b':rng.choice([4,5]) if band=='hard' else rng.choice([2,3]),
            'L':rng.choice([1,2]),'c':rng.choice([1,2,3]),'d':rng.choice([1,2,3]),
            'reverse':rng.choice([False,True]),'known':rng.choice([1,2]),
            'k':'k' if band=='hard' else rng.choice([-7,-4,-2,3,5,8])}

def generate(band,family,case,rng,p=None,claims=None):
    if band=='easy':return easy(rng,p)
    plan=claim_plan(case,rng) if claims is None else None
    p=dict(p) if p else sample_parameters(band,rng)
    a,b,L=p['a'],p['b'],p['L'];k=p['k'];ratio=Fraction(b,a)
    if family=='circle':
        end=r'\pi';other_end=r'\frac{\pi}{2}' if case=='subarc' else end
        tbound=tex(Fraction(1,a))+r'\pi' if a!=1 else r'\pi'
        ubound=tex(Fraction(1,2*b) if case=='subarc' else Fraction(1,b))+r'\pi'
    else:
        end=tex(L);other_end=tex(Fraction(L,2)) if case=='subarc' else end
        tbound=tex(Fraction(L,a));ubound=tex(Fraction(L,2*b) if case=='subarc' else Fraction(L,b))
    z1=times(a,'t');z2=(other_end+'-'+times(b,'u')) if p['reverse'] else times(b,'u')
    known='C_'+str(p['known']);other='C_'+str(3-p['known'])
    v1=vector(family,z1,p);v2=vector(family,z2,p,case=='branch')
    problem=(r'The curve $'+known+r'$ is parametrized by'+'\n\n$$\n'+r'\mathbf r_'+str(p['known'])+'(t)='+v1+'\n$$\n\n'+
             r'for $0\le t\le '+tbound+r'$. The curve $'+other+r'$ is parametrized by'+'\n\n$$\n'+r'\mathbf r_'+str(3-p['known'])+'(u)='+v2+'\n$$\n\n'+
             r'for $0\le u\le '+ubound+r'$. Suppose $f$ is continuous along both curves and'+'\n\n$$\n'+integral(known)+'='+tex(k)+'.\n$$\n\n'+
             r'A minus sign on a curve means its orientation is reversed. **Which statements must be true** for every such $f$'+(r' and every real $k$ satisfying the given equality' if band=='hard' else '')+r'? Select all that apply.')
    labels=['-'+known,other,'-'+other]
    if claims is None:
        factors={'one':Fraction(1),'neg':Fraction(-1),'speed':ratio,'inverse':1/ratio}
        chosen=[(labels[role],factors[error]) for role,error in plan]
    else:chosen=[(label,Fraction(factor)) for label,factor in claims]
    truths=[factor==1 and (label.lstrip('-')==known or case=='same') for label,factor in chosen]
    if not any(truths):raise ValueError('A selectable true statement is required')
    fields=[checkbox('$'+integral(label)+'='+val(factor,k)+'$',truth) for (label,factor),truth in zip(chosen,truths)]
    # Ordered locus and domain derivation, without a CAS choosing presentation.
    z=r'z';v=vector(family,z,p)
    solution=(r'Write points on the known curve in terms of a geometric parameter $z$:'+'\n\n$$\n'+r'\mathbf R(z)='+v+'.\n$$\n\n'+
              r'For $'+known+r'$, $z='+z1+r'$ increases from $0$ to $'+end+r'$. For $'+other+r'$, $z='+z2+r'$ '+
              ('decreases from $'+other_end+r'$ to $0$' if p['reverse'] else 'increases from $0$ to $'+other_end+'$')+'. ')
    if family=='quartic':locus=r'x='+times(p['c'],'y^4')+'-'+times(p['d'],'y^2')
    elif family=='circle':locus=r'x^2+y^2='+str(p['c']**2)+r',\quad y\ge0'
    elif family=='power':locus='y='+times(p['c'],'x^{3/2}')
    elif family=='hyperbola':locus=r'x=\sqrt{'+str(p['c'])+'+y^2}'
    else:locus='y='+times(p['d'],r'\sqrt{x/'+str(p['c'])+'}')
    solution+=r'Eliminating the parameter on $'+known+r'$ gives $'+locus+r'$. '
    if case=='same':
        solution+=r'The other curve has the same locus, branch and full parameter range; both traverse the arc once. '
        solution+=r'The parameter map is $t=('+z2+')/'+str(a)+r'$. Its sign controls direction, not the scalar integral. '
    elif case=='subarc':
        solution+=r'The other curve covers only the part with $0\le z\le '+other_end+r'$, rather than $0\le z\le '+end+r'$. A shared Cartesian equation alone is insufficient. '
        solution+=r'A continuous function supported near an interior point of the omitted arc can be scaled to give any prescribed nonzero integral on the full curve, while its integral on the subarc stays zero. Thus no nonzero fixed multiple of the full integral is guaranteed on the subarc. '
    else:
        if family=='hyperbola':
            solution+=r'The other curve instead lies on $x=-\sqrt{'+str(p['c'])+r'+y^2}$. The left and right branches are different arcs. A continuous function supported near the right branch can vanish on the left branch. '
        else:
            solution+=r'The other curve instead has $y=-'+times(p['d'],r'\sqrt{x/'+str(p['c'])+'}')+r'$. The lower and upper branches differ. A continuous function supported near an interior point of the upper branch can vanish on the lower branch. '
        solution+=r'Consequently no proposed nonzero multiple transfers to the other branch for every continuous function. '
    solution+='\n\n'+r'Reversing $'+known+r'$ always preserves its value:'+'\n\n$$\n'+integral('-'+known)+'='+integral(known)+'='+tex(k)+'.\n$$\n\n'
    if case=='same':solution+=r'Independence of parametrization and orientation also gives $'+integral(other)+'='+integral('-'+other)+'='+tex(k)+r'$. '
    solution+=r'Changing the parameter speed does not supply a multiplicative factor. '
    if k=='k':solution+=r'A proposed multiple can coincide at $k=0$, but that does not make it a guarantee for every $f$. '
    solution+='\n\n'
    for i,((label,factor),truth) in enumerate(zip(chosen,truths),1):
        solution+=r'Statement '+str(i)+r', $'+integral(label)+'='+val(factor,k)+r'$, is **'+('true' if truth else 'not guaranteed')+'**. '
    return assemble(band,problem,solution,fields,{'template':family,'relation_case':case,'parameters':p,
                    'source_question':SOURCE[family],'bank_profile':[(label,str(factor)) for label,factor in chosen]})

def batch(band,count,seed):
    if count<1:raise ValueError('count must be positive')
    rng=random.Random(seed);families=FAMILIES[band][:];rng.shuffle(families)
    # Each repeated visible family must include both an eligible transfer and
    # a nonmatching arc. Global cycling can strand one family on mismatches.
    mismatch=['subarc','branch'] if band=='hard' else ['subarc']
    rng.shuffle(mismatch)
    case_orders={}
    for i,family in enumerate(families):
        order=['same',mismatch[i%len(mismatch)]] if band!='easy' else ['same']
        rng.shuffle(order)
        if band=='hard':order += [c for c in mismatch if c not in order]
        case_orders[family]=order
    out=[];seen=set();attempt=0
    while len(out)<count:
        if attempt>max(100,count*50):raise ValueError('Requested count exceeds unique practice support')
        index=len(out)
        family=families[index%len(families)]
        order=case_orders[family];case=order[(index//len(families))%len(order)]
        r=generate(band,family,case,rng)
        # Content uniqueness includes decision assignments; UUIDs/seeds are not evidence of variety.
        signature=r['question'][':question/problem']+json.dumps([f[':answer-field/key'] for f in r['question'][':question/answer-fields']])
        attempt+=1
        if signature in seen:continue
        seen.add(signature);out.append(r)
    return out

def replay_sources():
    cases=json.loads(Path(__file__).with_name('source_cases.json').read_text())
    return [assemble(c['band'],c['problem'],c['solution'],c['fields'],{'source_question':c['id'],'template':'source-replay','evidence_only':True}) for c in cases]

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--difficulty',choices=['easy','moderate','hard','unclassified','all'],default='moderate')
    ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--format',choices=['json'],default='json');ap.add_argument('--replay-source',action='store_true')
    args=ap.parse_args();band='moderate' if args.difficulty=='unclassified' else args.difficulty
    records=replay_sources() if args.replay_source else [r for b in (FAMILIES if band=='all' else [band]) for r in batch(b,args.count,args.seed)]
    print(json.dumps(records,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
