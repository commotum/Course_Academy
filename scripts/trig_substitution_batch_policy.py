"""Publication guard for the reviewed scaffolded topic478 task contracts.

Independent printed-math and native-grading checks establish mathematics. This
guard preserves support, workload, answer transitions and delivered coverage.
"""
from collections import defaultdict
from fractions import Fraction
import re

KPS={17592186068915,17592186068916,17592186068917,17592186068918}
TRIG={'sin','cos','sec2','csc2','sec_tan','csc_cot'}
RECIP=TRIG-{'sin','cos'}
LINEAR={'indef_sin','indef_cos','def_sin','def_cos'}
RECIP_CASES={prefix+fn for prefix in ('indef_','def_')for fn in RECIP}
FAMILIES={
    17592186068915:{band:LINEAR for band in ('easy','moderate','hard')},
    17592186068916:{'easy':RECIP,'moderate':RECIP_CASES,'hard':RECIP_CASES},
    17592186068917:{'easy':TRIG,'moderate':TRIG,'hard':{'reciprocal_'+fn for fn in TRIG}|{'sqrt_sin','sqrt_cos'}},
    17592186068918:{'easy':{'sin','cos','tan','sec'},'moderate':{'sin','cos','tan','sec','csc','cot','sin2','cos3'},
        'hard':{'rearranged_tan','rearranged_sec','nested_sin','nested_tan','def_sin2','def_cos3'}},
}


def validate_delivery_batch(records,kp_id):
    kp=int(kp_id)
    if kp not in KPS:return
    groups=defaultdict(list);shapes=set()
    for record in records:
        q,m=record['question'],record.get('generation',{})
        if m.get('batch_contract')!='trig-scaffolding-v4':
            raise ValueError('Trig substitution requires the reviewed scaffolded band contract')
        band=str(q[':question/difficulty']).rsplit('/',1)[-1];family=m.get('family')
        if family not in FAMILIES[kp].get(band,set()):raise ValueError('Unsupported scaffolded family or difficulty')
        problem=q[':question/problem'];fields=q[':question/answer-fields']
        if any(int(n)>12 for n in re.findall(r'\d+',problem)):
            raise ValueError('Displayed parameters exceed the reviewed arithmetic budget')
        if len(fields)!=1:raise ValueError('Scaffolded substitution has one assessed response')
        field=fields[0];choices=field[':answer-field/choices'];correct=field[':answer-field/correct']
        correct_id=str(correct.get(':answer/id'))if isinstance(correct,dict)else str(correct[1])
        key=next(a[':answer/value']for a in choices if str(a[':answer/id'])==correct_id)
        easy=band=='easy'
        if easy:
            if field[':answer-field/type']!=':answer-field.type/radio'or len(choices)!=5:
                raise ValueError('Easy needs the reviewed transformed-integral choice support')
            if not m.get('provided_substitution')or m.get('operation')!='transform'or 'Use the substitution $u='not in problem:
                raise ValueError('Easy must supply u and assess transformation only')
            if any(r'\int'not in a[':answer/value']for a in choices):raise ValueError('Easy options must be transformed integrals')
        else:
            if field[':answer-field/type']!=':answer-field.type/blank'or len(choices)!=1:
                raise ValueError('Full calculation needs one canonical exact answer fragment')
            if not m.get('provided_primitive')or 'You may use $'not in problem:
                raise ValueError('Full calculation must supply the prerequisite primitive')
            if m['model']['lower']is not None and(not m.get('provided_endpoint_values')or 'Endpoint values:'not in problem):
                raise ValueError('Endpoint evaluation facts must be supplied')
        blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/worked-solution'],re.S)
        outside_c=bool(re.search(r'\{\{answer\}\}\s*\$\+C\$',problem))
        if not blocks or blocks[-1].strip().rstrip('.')!=key+('+C'if outside_c else ''):
            raise ValueError('Worked solution must reach the exact displayed canonical answer fragment')
        params=m['parameters']
        if kp in(17592186068915,17592186068916):
            a=Fraction(params['slope']);A=Fraction(params['amplitude'])
            if a.denominator!=1 or not 1<=abs(a)<=4 or A.denominator!=1 or not 1<=A<=4:
                raise ValueError('No fractional amplitude/slope composition or large coefficients')
            if(a<0)!=(band=='hard'):raise ValueError('Hard adds only the negative inner derivative condition')
        if kp==17592186068917:
            role=params.get('inner_role')
            if(role in('reciprocal','sqrt'))!=(band=='hard'):raise ValueError('Product band must reflect inner recognition, not heavier arithmetic')
            if m['model']['lower']is not None:raise ValueError('Product recognition tasks must not stack radical bounds')
        model=m['model'];shape=(band,family,model['substitution'],model['lower'],model['upper'])
        if shape in shapes:raise ValueError('Amplitude-only repetition in delivered practice')
        shapes.add(shape)
        if not easy and model['lower']is not None and key.strip()in{'0','0.0'}:raise ValueError('Zero-result padding is not eligible')
        groups[band].append(record)
    for band,rows in groups.items():
        if len({r['generation']['family']for r in rows})<min(len(rows),len(FAMILIES[kp][band])):
            raise ValueError('Delivered batch lost required family coverage')
