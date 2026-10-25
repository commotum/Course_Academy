"""Preserve the target skill, actual normalization work and endpoint coverage."""
from collections import defaultdict
import math
import re
import sympy as s
from fractions import Fraction

KPS={17592186064218,17592186064219,17592186064220,17592186064250}
VERSION='inverse-substitution-quality-4'

def pi_coefficient(text):
    compact=re.sub(r'\s+','',text)
    match=re.fullmatch(r'\\frac\{(\d*)\\pi\}\{(\d+)\}',compact)
    if match:return Fraction(int(match[1]or 1),int(match[2]))
    match=re.fullmatch(r'(\d*)\\pi',compact)
    if match:return Fraction(int(match[1]or 1))
    raise ValueError('Displayed endpoint bank contains generic filler or unsupported values')

def validate_delivery_batch(records,kp_id):
    kp=int(kp_id)
    if kp not in KPS:return
    from scripts.integration_support_policy import validate_prerequisite_recall
    groups=defaultdict(list);seen=set()
    for row in records:
        q=row['question'];m=row['generation'];p=m['parameters'];band=q[':question/difficulty'].rsplit('/',1)[-1]
        if m.get('batch_contract')!=VERSION:raise ValueError('Reviewed inverse quality contract required')
        validate_prerequisite_recall(row)
        if band not in('easy','moderate','hard'):raise ValueError('Unsupported band')
        families={17592186064218:{'sine'},17592186064219:{'tangent'},17592186064250:{'secant'},17592186064220:{'sine','tangent'}}
        if m['family']not in families[kp]:raise ValueError('Family mismatch')
        fields=q[':question/answer-fields']
        if len(fields)!=1:raise ValueError('One assessed response required')
        f=fields[0];choices=f[':answer-field/choices'];radio=kp!=17592186064220 or band=='easy'
        if f[':answer-field/type']!=(':answer-field.type/radio'if radio else':answer-field.type/blank')or len(choices)!=(5 if radio else 1):raise ValueError('Unsupported complete-answer response')
        if any(r'\int'in a[':answer/value']for a in choices):raise ValueError('Complete answers required')
        ref=f[':answer-field/correct'];cid=str(ref.get(':answer/id'))if isinstance(ref,dict)else str(ref[1]);key=next(a[':answer/value']for a in choices if str(a[':answer/id'])==cid)
        blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/worked-solution'],re.S)
        if not blocks or blocks[-1].strip().rstrip('.')!=key:raise ValueError('Solution does not reach the displayed key')
        if any(int(n)>25 for n in re.findall(r'\d+',q[':question/problem'])):raise ValueError('Rendered arithmetic budget exceeded')
        A,B,N=(s.Rational(p[k])for k in('A','B','numerator'))
        if N.q!=1 or not 1<=N<=(12 if kp==17592186064250 and band=='easy'else 8 if band=='easy'else 4):raise ValueError('No fractional or oversized numerator composition')
        if kp==17592186064250:
            factor=s.Rational(m['model']['factor'])
            if band=='easy'and(factor.q!=1 or not 1<=factor<=3)or band=='moderate'and factor.q==1:raise ValueError('Secant differential progression mismatch')
            if band=='hard'and m['challenge']!='absolute_value_normalization':raise ValueError('Secant hard must explain absolute-value normalization')
        elif band=='easy':
            ratio=B/A;scale=s.sqrt(ratio);coefficient=N/(s.sqrt(A)if m['family']=='sine'else A)
            if not(scale.is_Integer and 2<=scale<=5 and coefficient.is_Integer and 1<=coefficient<=4):raise ValueError('Easy must reduce to a direct standard form with small integer amplitude')
        elif band=='moderate':
            if B!=1 or A not in(4,9,16,25):raise ValueError('Moderate requires one familiar square normalization')
        elif kp==17592186064220:
            if B!=1 or A not in((2,8)if m['family']=='sine'else(3,12)):raise ValueError('Definite hard requires a familiar small radical normalization')
        else:
            a,b=s.sqrt(A),s.sqrt(B)
            if not(a.is_Integer and b.is_Integer and 2<=a<=5 and 2<=b<=5 and math.gcd(int(a),int(b))==1):raise ValueError('Hard calibration must survive coefficient cancellation')
        if radio:
            recipes=m['bank_recipes']
            if len(recipes)!=5 or any('return_substitution'in v or 'offset'in v or 'shift_inner'in v for v in recipes):raise ValueError('Diagnostic distractors required; generic filler is forbidden')
            if kp==17592186064220:
                # Easy endpoints and differential factors give positive
                # rational multiples of pi. Inspect the displayed bank too:
                # metadata must not conceal arbitrary +1/+2 fallback choices.
                for answer in choices:
                    pi_coefficient(answer[':answer/value'])
                rank=sum(pi_coefficient(a[':answer/value'])<pi_coefficient(key)for a in choices)
                if m.get('bank_correct_rank')!=rank:raise ValueError('Displayed bank rank differs from metadata')
            else:
                name={'sine':r'\arcsin','tangent':r'\arctan','secant':r'\operatorname{arcsec}'}[m['family']]
                if any(name not in a[':answer/value']for a in choices):raise ValueError('Displayed primitive bank contains generic filler')
            if kp!=17592186064220 and any('+C'not in a[':answer/value']for a in choices):raise ValueError('Each antiderivative choice needs C')
        identity=(band,m['mathematical_fingerprint'])
        if identity in seen:raise ValueError('Duplicate task')
        seen.add(identity);groups[band].append(row)
    for band,rows in groups.items():
        if len(rows)>=8:
            if len({r['generation']['model']['substitution']for r in rows})<3:raise ValueError('Pool overconcentrates one substitution')
            if kp==17592186064220:
                for fn in('sine','tangent'):
                    pairs={(r['generation']['parameters']['normalized_lower'],r['generation']['parameters']['normalized_upper'])for r in rows if r['generation']['family']==fn}
                    if len(pairs)<(2 if band=='easy'else 3):raise ValueError('Endpoint coverage lost after delivery')
                    if band=='easy':
                        ranks=[r['generation']['bank_correct_rank']for r in rows if r['generation']['family']==fn]
                        if any(ranks.count(rank)>(len(ranks)+1)//2 for rank in set(ranks)):raise ValueError('Conditional numerical rank balance lost after delivery')
                if band!='easy':
                    n=sum(s.sympify(r['generation']['parameters']['normalized_lower'])!=0 and s.sympify(r['generation']['parameters']['normalized_upper'])!=0 for r in rows)
                    if not 2<=n<=len(rows)-2:raise ValueError('Mix one and two nonzero endpoint contributions')
            if band=='easy'and len({tuple(sorted(r['generation']['bank_recipes']))for r in rows})<2:raise ValueError('Fixed bank profiles reveal the answer')
