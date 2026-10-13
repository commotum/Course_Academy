#!/usr/bin/env python3
"""Component scalar projections; captured masks and explicitly authored E/M/H banks.

Opaque historical banks are evidence-only profiles: their whole-expression
ratios are retained honestly, never presented as recovered learner error recipes.
Normal banks derive every wrong answer from the displayed component operation.
"""
from __future__ import annotations
import argparse, hashlib, json, math, random, re, sys, uuid
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parent/'17592186105917'
VERSION='1.0.0'
KP={'db_id':17592186105917,'id':'91691448-c59a-56dc-a775-d4e9c3297036','title':'Calculating a Scalar Projection Using Components'}
NS=uuid.UUID('da8a1521-86cc-5747-88a7-e2ec56010c11')
class SampleRejected(ValueError): pass

def expr(x):
    if isinstance(x,(int,s.Expr)):return s.sympify(x)
    return s.sympify(str(x),locals={'sqrt':s.sqrt})

def tex(x):return s.latex(expr(x)).replace(' ','')
def frac(n,d,negative_outside=True):
    n,d=expr(n),expr(d)
    sign=''
    if negative_outside and n.is_negative:sign,n='-',-n
    return sign+r'\frac{'+tex(n)+'}{'+tex(d)+'}'
def rootfrac(n,d2,negative_outside=True):
    n=expr(n);sign=''
    if negative_outside and n.is_negative:sign,n='-',-n
    return sign+r'\frac{'+tex(n)+r'}{\sqrt{'+tex(d2)+'}}'
def finaltex(x):
    x=s.together(s.radsimp(s.simplify(x)));n,d=s.fraction(x);n=s.expand(n)
    if d==1:return tex(x)
    if n.is_Add:
        positive=[a for a in s.Add.make_args(n) if not a.could_extract_minus_sign()]
        negative=[a for a in s.Add.make_args(n) if a.could_extract_minus_sign()]
        if positive and negative:
            nt='+'.join(tex(a) for a in positive)+''.join('-'+tex(-a) for a in negative)
            return r'\frac{'+nt+'}{'+tex(d)+'}'
    return frac(n,d)
def fact(x):
    t=tex(x)
    return '('+t+')' if expr(x).is_negative or expr(x).is_Add else t

def signed_sum(values):
    out=tex(values[0])
    for v in values[1:]:
        out+=('-'+tex(-v)) if expr(v).is_negative else '+'+tex(v)
    return out

def data(p):
    a,b=list(map(expr,p['a'])),list(map(expr,p['b']))
    D=s.expand(sum(x*y for x,y in zip(a,b))); A2=s.expand(sum(x*x for x in a));B2=s.expand(sum(x*x for x in b))
    A,B=s.sqrt(A2),s.sqrt(B2)
    P,Q=s.simplify(D/B),s.simplify(D/A)
    op=p.get('operation','single');R=P if op=='single' else s.simplify(P+(Q if op=='sum' else -Q))
    return dict(a=a,b=b,D=D,A2=A2,B2=B2,A=A,B=B,P=P,Q=Q,R=R,op=op)

def compact_parameters(p):return {'a':[str(expr(x)) for x in p['a']],'b':[str(expr(x)) for x in p['b']],'operation':p.get('operation','single')}

def square_component(x,style='default',display=None):
    t=display or tex(x)
    if expr(x).is_negative or (not expr(x).is_Integer and style!='braced_radical'):return '('+t+')^{2}'
    return '{'+t+'}^{2}'
def normsum(v,style='default',displays=None):return '+'.join(square_component(x,style,displays[i] if displays else None) for i,x in enumerate(v))
def product(v,w,style='dot',bare_first=False,vt=None,wt=None):
    terms=[]
    for i,(x,y) in enumerate(zip(v,w)):
        xt=vt[i] if vt else tex(x);yt=wt[i] if wt else tex(y)
        xf=('('+xt+')') if expr(x).is_negative or expr(x).is_Add else xt
        yf=('('+yt+')') if expr(y).is_negative or expr(y).is_Add else yt
        if style=='paren':terms.append('('+xt+')('+yt+')')
        else:terms.append((xt if bare_first and i==0 else xf)+r'\cdot '+yf)
    return '+'.join(terms)
def subrow(d,which,style='dot',normstyle='default',bare_first=False):
    return r'\frac{'+product(d['a'],d['b'],style,bare_first,d.get('at'),d.get('bt'))+r'}{\sqrt{'+normsum(d['b' if which=='P' else 'a'],normstyle,d.get('bt' if which=='P' else 'at'))+'}}'
def evalrow(d,which,negative_outside=False):
    return r'\frac{'+signed_sum([s.expand(x*y) for x,y in zip(d['a'],d['b'])])+r'}{\sqrt{'+tex(d['B2' if which=='P' else 'A2'])+'}}'
def comp(u,v):return r'{\text{comp}}_{'+v+r'}\,'+u

def row_value(tag,d,which):
    """Ordered arithmetic renderers keep substitution, evaluation and reduction distinct."""
    N2=d['B2' if which=='P' else 'A2'];N=d['B' if which=='P' else 'A'];D=d['D'];X=d[which]
    if tag.startswith('sub:'):
        _,style,normstyle,bare=tag.split(':');return subrow(d,which,style,normstyle,bare=='1')
    if tag=='eval':return evalrow(d,which)
    if tag=='raw':return rootfrac(D,N2)
    if tag=='raw_inside':return rootfrac(D,N2,False)
    if tag=='norm':return frac(D,N)
    if tag=='norm_inside':return frac(D,N,False)
    if tag=='known_dot':return r'\frac{'+tex(D)+r'}{\sqrt{'+normsum(d['a'],displays=d.get('at'))+'}}'
    if tag=='known_dot_braced':return r'\frac{'+tex(D)+r'}{\sqrt{'+normsum(d['a'],'braced_radical',d.get('at'))+'}}'
    if tag=='final':return finaltex(X)
    if tag=='raw_final':return rootfrac(D,N2)
    if tag=='rationalized':return finaltex(X)
    op='+' if d['op']=='sum' else '-'
    if tag=='combine':return finaltex(d['P'])+op+('('+finaltex(d['Q'])+')' if d['Q'].is_negative else finaltex(d['Q']))
    if tag=='combine_raw':return rootfrac(D,d['B2'])+op+('('+rootfrac(D,d['A2'])+')' if D.is_negative else rootfrac(D,d['A2']))
    if tag=='factor':return fact(D)+r'(\frac{1}{'+tex(d['B'])+'}'+op+r'\frac{1}{'+tex(d['A'])+'})'
    if tag=='lcm':
        L=s.ilcm(int(d['A']),int(d['B']));return fact(D)+r'(\frac{'+str(L//int(d['B']))+'}{'+str(L)+'}'+op+r'\frac{'+str(L//int(d['A']))+'}{'+str(L)+'})'
    if tag=='common_radical':
        n=tex(D*s.sqrt(d['A2']))+op+fact(D*s.sqrt(d['B2']))
        return r'\frac{'+n+r'}{\sqrt{'+tex(d['A2']*d['B2'])+'}}'
    if tag=='collect_same_den':
        # Original 40/13 - 4 combines to (40 - 52)/13.
        return r'\frac{'+tex(D)+op+tex(d['Q']*d['B'])+'}{'+tex(d['B'])+'}'
    if tag=='result':return finaltex(d['R'])
    raise ValueError(tag)


def source_build(recipe,p):
    """Render captured component masks; no literal source-question return path."""
    d=data(p);q={}
    for key in ('a','b'):
        d[key+'t']=[('-' if x.is_negative else '')+r'\sqrt{'+tex(s.expand(x*x))+'}' if i in recipe.get('root_forms',{}).get(key,[]) else tex(x) for i,x in enumerate(d[key])]
    separator=recipe.get('separator',',')
    a='⟨'+separator.join(d['at'])+'⟩';b='⟨'+separator.join(d['bt'])+'⟩'
    if recipe.get('spaced_negative'):
        b=b.replace('⟨-','⟨ - ')
    q[':question/problem']=recipe['prompt_mask'].replace('@A@',a).replace('@B@',b)
    if 'solution_mask' in recipe:
        solution=recipe['solution_mask']
        for i,row in enumerate(recipe['rows']):solution=solution.replace('@ROW'+str(i)+'@',row_value(row['tag'],d,row['which']))
        q[':question/worked-solution']=solution
    return q,d


def mathematical_fingerprint(p):
    """Ignore names, banks/order and common positive magnitude of either vector.

    Projection direction depends on normalized b; the assessed dot/norm workload
    depends on component ratios of a. Keep signs and operation; exclude common
    positive scaling so magnitude-only variants do not inflate task counts.
    """
    d=data(p)
    def normalize(v):
        first=next(abs(x) for x in v if x!=0)
        return [str(s.simplify(x/first)) for x in v]
    return hashlib.sha256(json.dumps({'a':normalize(d['a']),'b':normalize(d['b']),'operation':d['op']},sort_keys=True).encode()).hexdigest()


def check_parameters(level,p,evidence=False):
    if set(p)-{'a','b','operation'}:raise ValueError('Unknown parameter keys')
    if len(p.get('a',[]))!=3 or len(p.get('b',[]))!=3:raise ValueError('Two three-component vectors required')
    d=data(p)
    if any(x.is_real is not True or x.is_finite is not True for v in [d['a'],d['b']] for x in v):raise ValueError('Finite exact real components required')
    if d['A2']==0 or d['B2']==0:raise ValueError('Nonzero vectors required')
    if d['op'] not in ('single','sum','difference'):raise ValueError('Invalid scalar operation')
    if evidence:
        if any(abs(x)>30 or s.expand(x*x).is_Integer is not True for v in [d['a'],d['b']] for x in v):raise ValueError('Evidence coordinates require integer squares and abs<=30')
        if d['R']==0:raise ValueError('Evidence ratio bank requires a nonzero result')
        return
    if d['D']==0:raise ValueError('Perpendicular recognition belongs to the sibling KP')
    if level=='easy':
        if d['op']!='single':raise ValueError('Easy assesses one scalar projection')
        if any((x*x).is_Integer is not True or abs(x)>8 for v in [d['a'],d['b']] for x in v) or max(d['A2'],d['B2'])>144:raise ValueError('Easy familiar integer/radical components, abs<=8 and squared norms<=144')
    elif level=='moderate':
        if d['op']=='single' or not d['A'].is_Integer or not d['B'].is_Integer or d['D'].is_Integer is not True:raise ValueError('Moderate combines two projections with integer dot product and norms')
        if d['A']==d['B']:raise ValueError('Moderate uses unequal norms')
        if any(s.denom(x)!=1 and not (x*x).is_Integer for v in [d['a'],d['b']] for x in v):raise ValueError('Moderate familiar integer/radical components')
        if any(abs(x)>12 for v in [d['a'],d['b']] for x in v) or max(d['A2'],d['B2'])>225:raise ValueError('Moderate workload ceiling')
    elif level=='hard':
        if d['op']=='single' or d['A'].is_Integer or d['B'].is_Integer or s.simplify(d['A']/d['B']).is_Rational or d['D'].is_rational is not False:raise ValueError('Hard requires an irrational dot product and two distinct nonsquare norm radicals')
        if any(s.expand(x*x).is_Integer is not True or x==0 or abs(x)>4 for v in [d['a'],d['b']] for x in v) or max(d['A2'],d['B2'])>40:raise ValueError('Hard three nonzero integer/radical products; abs coordinates <=4, norm squares <=40')
    else:raise ValueError('Unknown level')


def authored_bank(d,profile):
    D,A,B=d['D'],d['A'],d['B'];P,Q=d['P'],d['Q'];op=1 if d['op']=='sum' else -1
    if profile=='single_method':
        # Denominator confusion, missing square root, omitted x product, sign reversal.
        return [('correct',P),('wrong_projection_direction',Q),('norm_squared',D/d['B2']),('omit_x_product',(D-d['a'][0]*d['b'][0])/B),('reverse_dot_sign',-P)]
    if profile=='pair_method':
        R=d['R']
        return [('correct',R),('wrong_combination',P-op*Q),('omit_second_projection',P),('second_norm_squared',P+op*D/d['A2']),('reverse_dot_sign',-R)]
    raise ValueError('Unknown authored complete bank')


def raw_bank(recipe,d):
    # Complete-expression ratio masks retain evidence without claiming error intent.
    # Each source choice is a parameterized scalar formula ratio*R (zero remains zero).
    out=[]
    for item in recipe['bank']:
        ratio=expr(item['ratio']);value=s.simplify(ratio*d['R'])
        spelling=item['mask']
        # Template multiplier is a full mathematical slot, not a payload lookup.
        multiplier=s.simplify(d['R']/expr(recipe['reference_result']))
        display=spelling.replace('@MULTIPLIER@',tex(multiplier))
        if multiplier==1:display=display.replace(r'\left(1\right)\left(', '').removesuffix(r'\right)')
        out.append((item['name'],value,display))
    return out


def aligned(lhs,rows,punctuation='.'):
    return '$$\n'+r'\begin{aligned}'+lhs+' & ='+r' \\  & ='.join(rows)+punctuation+r'\end{aligned}'+'\n$$'
def normal_solution(d,level):
    a,b='a','b';D=d['D'];opsign='+' if d['op']=='sum' else '-'
    formal=r'\frac{a\cdot b}{|\,b\,|}'
    expansion=r'\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}}'
    rows=[formal,expansion,subrow(d,'P','paren'),evalrow(d,'P'),rootfrac(D,d['B2'],False)]
    if level!='hard':rows.append(finaltex(d['P']))
    result='Using the scalar projection formula, we obtain\n\n'+aligned(comp(a,b),rows)
    if d['op']!='single':
        expansion2=expansion.replace('{b}_{','{TEMP}_{').replace('{a}_{','{b}_{').replace('{TEMP}_{','{a}_{')
        rows2=[r'\frac{b\cdot a}{|\,a\,|}',expansion2,r'\frac{'+tex(D)+r'}{\sqrt{'+normsum(d['a'],displays=d.get('at'))+'}}',rootfrac(D,d['A2'],False)]
        if level!='hard':rows2.append(finaltex(d['Q']))
        result+='\n\nand\n\n'+aligned(comp(b,a),rows2)
        combine=(row_value('combine_raw',d,'R') if level=='hard' else finaltex(d['P'])+opsign+('('+finaltex(d['Q'])+')' if d['Q'].is_negative else finaltex(d['Q'])))
        rows3=[combine]
        if level=='hard':rows3.append(row_value('common_radical',d,'R'))
        else:rows3.append(finaltex(d['R']))
        result+='\n\nTherefore,\n\n'+aligned(comp(a,b)+opsign+comp(b,a),rows3)
    return result


def assemble(level,p,q,d,bank,profile,template,seed,evidence=False,correct_missing=False):
    values=[s.simplify(x[1]) for x in bank]
    if not evidence and any(s.simplify(x-y)==0 for i,x in enumerate(values) for y in values[i+1:]):raise SampleRejected('Whole bank collision')
    choices_content=sorted(x[2] if len(x)>2 else finaltex(x[1]) for x in bank)
    content={'version':VERSION,'difficulty':None if correct_missing else level,'problem':q[':question/problem'],'solution':q.get(':question/worked-solution'),'bank':choices_content,'correct_missing':correct_missing}
    identity=hashlib.sha256(json.dumps(content,sort_keys=True).encode()).hexdigest()
    QID=str(uuid.uuid5(NS,identity));FID=str(uuid.uuid5(NS,identity+'/field'))
    choices=[];correctid=None
    for item in bank:
        name,value=item[:2];display=item[2] if len(item)>2 else finaltex(value)
        aid=str(uuid.uuid5(NS,FID+'/'+display))
        choices.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':display})
        if name=='correct':correctid=aid
    kind='blank' if len(bank)==1 else 'radio'
    field={':answer-field/id':FID,':answer-field/key':'field-1' if kind=='blank' else 'selection',':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices}
    if not correct_missing:field[':answer-field/correct']=[':answer/id',correctid]
    random.Random(seed).shuffle(choices)
    q={':question/id':QID,**q,':question/answer-fields':[field]}
    if not correct_missing:q[':question/difficulty']=':question.difficulty/'+level
    return {'knowledge_point':dict(KP),'question':q,'generation':{'version':VERSION,'template':template,'bank_profile':profile,'seed':seed,'parameters':compact_parameters(p),'mathematical_fingerprint':mathematical_fingerprint(p),'content_sha256':identity,'evidence_only':evidence,'eligible_for_learning':not evidence,'source_id':template if template.startswith('q-') else None,'runtime':{'python':sys.version.split()[0],'sympy':s.__version__},'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}}


def recipes():return json.loads((ROOT/'recipes.json').read_text())

# EASY — observed one projection; integer/radical observed replays, integer defaults.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE — observed sum/difference; two norms and one combination, familiar square norms.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('moderate',seed,template,field_type,parameters,profile)
# HARD — authored same formula twice; irrational dot sum and two nonsquare norms.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
    return generate('hard',seed,template,field_type,parameters,profile)

def sample(level,rng,template):
    if level=='easy':
        if template=='single_radical':
            roots=[s.sqrt(2),s.sqrt(3),s.sqrt(6),s.sqrt(8)]
            return {'a':[rng.choice((-1,1))*rng.choice([1,2,3,4,*roots]) for _ in range(3)],'b':[rng.choice((-1,1))*rng.choice([1,2,3,*roots]) for _ in range(3)],'operation':'single'}
        return {'a':[rng.randint(-8,8) for _ in range(3)],'b':[rng.randint(-6,6) for _ in range(3)],'operation':'single'}
    if level=='moderate':
        # Square norms observed repeatedly; orientations and lengths vary independently.
        bases=[(2,1,2),(4,3,0),(6,2,3),(1,2,2),(3,4,0),(0,5,12),(1,0,0),(2,0,0)]
        def vector():
            v=list(rng.choice(bases));rng.shuffle(v);return [x*rng.choice((-1,1)) for x in v]
        if rng.choice((False,True)):
            pairs=[((1,s.sqrt(6),3),(-7,s.sqrt(6),3)),((-1,2,s.sqrt(11)),(4,3,s.sqrt(11))),((1,4,2*s.sqrt(2)),(1,1,s.sqrt(2)))]
            a,b=rng.choice(pairs);order=list(range(3));rng.shuffle(order)
            a=[a[i]*rng.choice((-1,1)) for i in order];b=[b[i]*rng.choice((-1,1)) for i in order]
        else:a,b=vector(),vector()
        return {'a':a,'b':b,'operation':'sum' if template=='pair_sum' else 'difference'}
    def vector():return [rng.choice((-1,1))*rng.choice([1,2,3,4,s.sqrt(2),s.sqrt(3),s.sqrt(5),s.sqrt(6)]) for _ in range(3)]
    return {'a':vector(),'b':vector(),'operation':'sum' if template=='pair_sum' else 'difference'}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
    rng=random.Random(seed)
    allrecipes=recipes()
    if profile and profile.startswith('observed:'):
        implied=profile.split(':',1)[1]
        if template and template!=implied:raise ValueError('Profile/template mismatch')
        template=implied
    if template in allrecipes:
        recipe=allrecipes[template]
        if level!=recipe['level']:raise ValueError('Source profile difficulty mismatch')
        if profile not in (None,'observed:'+template):raise ValueError('Use the observed profile for source masks')
        kind=recipe['field_type']
        if field_type and field_type!=kind:raise ValueError('Source field shape is fixed')
        p=parameters or recipe['parameters'];check_parameters(level,p,True)
        if p.get('operation','single')!=recipe['parameters']['operation']:raise ValueError('Cannot change source operation')
        d=data(p)
        if any(row['tag']=='lcm' for row in recipe.get('rows',[])) and (d['A'].is_Integer is not True or d['B'].is_Integer is not True):raise ValueError('Observed common-denominator stage requires integer norms')
        q,d=source_build(recipe,p)
        q[':question/math-academy-id']=template
        bank=raw_bank(recipe,d)
        return assemble(level,p,q,d,bank,'observed:'+template,template,seed,True,recipe['correct_missing'])
    eligible=['single','single_radical'] if level=='easy' else ['pair_sum','pair_difference']
    inferred=('single_radical' if any(not expr(x).is_Integer for key in ('a','b') for x in parameters[key]) else 'single') if parameters is not None and level=='easy' else ('pair_sum' if parameters and parameters.get('operation')=='sum' else 'pair_difference')
    name=template or (inferred if parameters is not None else rng.choice(eligible))
    if name not in eligible:raise ValueError('Template incompatible with difficulty')
    bankprofile='single_method' if level=='easy' else 'pair_method'
    if profile not in (None,bankprofile):raise ValueError('Unsupported authored bank')
    if field_type not in (None,'radio','blank'):raise ValueError('Unsupported field type')
    kind=field_type or ('radio' if parameters is not None else rng.choice(('radio','blank')))
    for _ in range(256):
        p=compact_parameters(parameters) if parameters is not None else sample(level,rng,name)
        try:
            check_parameters(level,p);d=data(p)
            has_radical=any(not x.is_Integer for key in ('a','b') for x in d[key])
            if level=='easy' and has_radical!=(name=='single_radical'):raise ValueError('Integer/radical family workload mismatch')
            if d['op']!=('single' if name in ('single','single_radical') else 'sum' if name=='pair_sum' else 'difference'):raise ValueError('Template/operation mismatch')
            fullbank=authored_bank(d,bankprofile)
            if any(s.simplify(x[1]-y[1])==0 for i,x in enumerate(fullbank) for y in fullbank[i+1:]):raise SampleRejected('Whole bank collision')
        except ValueError:
            if parameters is not None:raise
            continue
        requested=comp('a','b') if level=='easy' else comp('a','b')+('+' if d['op']=='sum' else '-')+comp('b','a')
        prompt='Let $a=⟨'+','.join(tex(x) for x in d['a'])+'⟩$ and $b=⟨'+','.join(tex(x) for x in d['b'])+'⟩.$ '
        prompt+=('Find the scalar projection of $a$ onto $b.$' if level=='easy' else 'Find $'+requested+'.$')
        if kind=='blank':prompt+='\n\n$'+requested+'=$\n{{field-1}}'
        q={':question/problem':prompt,':question/worked-solution':normal_solution(d,level)}
        if level=='hard':
            opposite={**d,'op':'sum' if d['op']=='difference' else 'difference'}
            op='+' if d['op']=='sum' else '-'
            correct_tex=row_value('common_radical',d,'R')
            second_tex=frac(d['D'],d['A2'],False)
            shown={'correct':correct_tex,'wrong_combination':row_value('common_radical',opposite,'R'),'omit_second_projection':rootfrac(d['D'],d['B2'],False),'second_norm_squared':rootfrac(d['D'],d['B2'],False)+op+('('+second_tex+')' if d['D'].is_negative else second_tex),'reverse_dot_sign':'-('+correct_tex+')'}
            fullbank=[(name,value,shown[name]) for name,value in fullbank]
        return assemble(level,p,q,d,fullbank[:1] if kind=='blank' else fullbank,bankprofile,name,seed)
    raise SampleRejected('Bounded whole-instance sampling exhausted')


def markdown(record,label='Generated'):
    q=record['question'];g=record['generation'];f=q[':question/answer-fields'][0]
    text=['## '+label+' — '+q.get(':question/difficulty','unrated').split('/')[-1],f"Template `{g['template']}`, profile `{g['bank_profile']}`, seed {g['seed']}.",'',q[':question/problem'],'']
    for i,a in enumerate(f[':answer-field/choices']):text.append(f"- {'ABCDE'[i]}. ${a[':answer/value']}$")
    correct=f.get(':answer-field/correct')
    text+=['','Correct: '+(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct[1]) if correct else 'absent in raw source evidence'),'','Worked solution:',q.get(':question/worked-solution','Absent in raw source evidence.')]
    return '\n'.join(text)
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--field-type',choices=['radio','blank']);args=ap.parse_args()
    if args.count<1:ap.error('Positive count required')
    if (args.template or args.profile) and args.difficulty=='all':ap.error('Specify a difficulty with a template/profile')
    levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
    records=[generate(level,args.seed+i,args.template,args.field_type,profile=args.profile) for level in levels for i in range(args.count)]
    print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
