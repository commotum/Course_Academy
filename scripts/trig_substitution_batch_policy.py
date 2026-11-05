"""Publication guard for reviewed independent topic478 task contracts.

Independent printed-math and native-grading checks establish mathematics. This
guard preserves independent work, bounded arithmetic and answer transitions.
Family/sign/rank frequencies belong to generator review over a population, not
mandatory quotas for every fragment that survives inventory deduplication.
"""
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
    shapes=set()
    for record in records:
        q,m=record['question'],record.get('generation',{})
        contract=m.get('batch_contract')
        if contract not in {'trig-substitution-recognition-v6','trig-substitution-recognition-v7'}:
            raise ValueError('Trig substitution requires the reviewed scaffolded band contract')
        band=str(q[':question/difficulty']).rsplit('/',1)[-1];family=m.get('family')
        if family not in FAMILIES[kp].get(band,set()):raise ValueError('Unsupported scaffolded family or difficulty')
        problem=q[':question/problem'];fields=q[':question/answer-fields']
        from scripts.integration_support_policy import validate_prerequisite_recall
        validate_prerequisite_recall(record)
        if any(int(n)>12 for n in re.findall(r'\d+',problem)):
            raise ValueError('Displayed parameters exceed the reviewed arithmetic budget')
        if len(fields)!=1:raise ValueError('Scaffolded substitution has one assessed response')
        field=fields[0];choices=field[':answer-field/choices'];correct=field[':answer-field/correct']
        if any(int(n)>12 for a in choices for n in re.findall(r'\d+',a[':answer/value'])):
            raise ValueError('Displayed answer choices exceed the reviewed arithmetic budget')
        correct_id=str(correct.get(':answer/id'))if isinstance(correct,dict)else str(correct[1])
        key=next(a[':answer/value']for a in choices if str(a[':answer/id'])==correct_id)
        easy=band=='easy'
        if m.get('provided_substitution')or m.get('operation')!='evaluate'or 'Use the substitution' in problem:
            raise ValueError('Practice must retain substitution recognition and full calculation')
        if easy and field[':answer-field/type']==':answer-field.type/radio':
            if not 2<=len(choices)<=5:
                raise ValueError('Complete-answer choices require distinct alternatives')
            if any(r'\int'in a[':answer/value']for a in choices):raise ValueError('Easy choices must give complete answers')
        else:
            if field[':answer-field/type']!=':answer-field.type/blank'or len(choices)!=1:
                raise ValueError('Full calculation needs one canonical exact answer fragment')
        blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/worked-solution'],re.S)
        outside_c=bool(re.search(r'\{\{answer\}\}\s*\$\+C\$',problem))
        if not blocks or blocks[-1].strip().rstrip('.')!=key+('+C'if outside_c else ''):
            raise ValueError('Worked solution must reach the exact displayed canonical answer fragment')
        params=m['parameters']
        if kp in(17592186068915,17592186068916):
            a=Fraction(params['slope']);A=Fraction(params['amplitude'])
            # Keep one familiar scaling operation. Reciprocal slopes include
            # the canonical x/3; fractional amplitudes stacked with fractional
            # slopes remain outside this reviewed, deliberately bounded model.
            if a not in {Fraction(n)for n in(-4,-3,-2,-1,1,2,3,4)}|{Fraction(1,2),Fraction(1,3),Fraction(-1,2),Fraction(-1,3)} or A.denominator!=1 or not 1<=A<=4:
                raise ValueError('No fractional amplitude/slope composition or large coefficients')
        if kp==17592186068917:
            role=params.get('inner_role')
            if(role in('reciprocal','sqrt'))!=(band=='hard'):raise ValueError('Product band must reflect inner recognition, not heavier arithmetic')
            if m['model']['lower']is not None:raise ValueError('Product recognition tasks must not stack radical bounds')
        model=m['model'];shape=(band,family,model['substitution'],model['lower'],model['upper'])
        if shape in shapes:raise ValueError('Amplitude-only repetition in delivered practice')
        shapes.add(shape)
        # Zero is a legitimate endpoint result. The ordinary generator must
        # also serve nonzero cases; that is reviewed across independent draws,
        # not inferred from the size or composition of this filtered fragment.
