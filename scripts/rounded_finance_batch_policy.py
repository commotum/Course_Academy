"""Publication guard against financial banks that assess rounding granularity."""
from decimal import Decimal
import re

KPS={17592186059796,17592186059797,17592186059798}
CONTRACT='rounded-finance-spacing-v1'

def displayed_number(text):
    value=text.replace(r'\,','').replace(',','')
    numbers=re.findall(r'(?<![\w.])-?\d+(?:\.\d+)?',value)
    if len(numbers)!=1:raise ValueError('Expected one numeric financial answer')
    return Decimal(numbers[0])

def validate_delivery_batch(records,kp_id):
    kp=int(kp_id)
    if kp not in KPS:return
    for row in records:
        q=row['question'];meta=row.get('generation',{})
        if meta.get('batch_contract')!=CONTRACT:raise ValueError('Rounded financial choices require the reviewed spacing contract')
        family=meta.get('template')
        if family not in({17592186059796:{'gas','profit'},17592186059797:{'rate','time'},17592186059798:{'annual','daily'}}[kp]):raise ValueError('Unsupported financial answer family')
        fields=q[':question/answer-fields']
        if len(fields)!=1 or fields[0][':answer-field/type']!=':answer-field.type/radio':raise ValueError('Five complete financial choices required')
        f=fields[0];choices=f[':answer-field/choices'];ref=f[':answer-field/correct'];cid=str(ref.get(':answer/id'))if isinstance(ref,dict)else str(ref[1])
        if len(choices)!=5:raise ValueError('Five complete financial choices required')
        values=[displayed_number(a[':answer/value'])for a in choices];key=next(value for a,value in zip(choices,values)if str(a[':answer/id'])==cid)
        places=2 if family=='gas'else 0;scale=Decimal(10)**places
        units=[v*scale for v in values]
        if any(v!=v.to_integral_value()or v<=0 for v in units):raise ValueError('Financial choices must respect the requested rounding unit')
        key_units=int(key*scale)
        gap=2 if family=='time'else 3 if family=='rate'else max(5,(key_units+999)//1000)
        ordered=sorted(units)
        if any(b-a<gap for a,b in zip(ordered,ordered[1:])):raise ValueError('Financial choices are too close: spacing must exceed rounding granularity')
        if meta.get('bank_profile')=='authored-nearby-rounded-amounts':raise ValueError('Numeric jitter around the key is not a diagnostic answer bank')
