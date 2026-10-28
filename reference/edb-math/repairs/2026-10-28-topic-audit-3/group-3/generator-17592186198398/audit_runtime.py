"""Format displayed content before identity; identify image content by bytes."""
import copy,hashlib,re
from pathlib import Path
from math_format import normalize_prose,normalize_tex
_IMAGE=re.compile(r'(?:/[A-Za-z0-9_.~+-]+)+\.(?:png|jpg|jpeg|svg|webp|gif)')
def asset_payload(value):
    if isinstance(value,str):
        def replace(m):
            p=Path(m[0])
            return 'asset-sha256:'+hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else m[0]
        return _IMAGE.sub(replace,value)
    if isinstance(value,dict):return {k:asset_payload(v)for k,v in value.items()}
    if isinstance(value,(tuple,list)):return [asset_payload(v)for v in value]
    return value

def normalize_question(q):
    q=copy.deepcopy(q)
    for attr in [':question/problem',':question/worked-solution']:
        if attr in q:q[attr]=normalize_prose(q[attr])
    for f in q.get(':question/answer-fields',[]):
        typ=f[':answer-field/type'];typ=typ.get(':db/ident')if isinstance(typ,dict)else typ
        if typ==':answer-field.type/checkbox':f[':answer-field/key']=normalize_prose(f[':answer-field/key'])
        old_to_new={}
        for a in f[':answer-field/choices']:
            typ=a[':answer/type'];typ=typ.get(':db/ident')if isinstance(typ,dict)else typ
            before=a[':answer/value'];after=normalize_tex(before)if typ==':answer.type/math'else normalize_prose(before)if typ==':answer.type/text'else before;a[':answer/value']=after;old_to_new[before]=after
        if isinstance(f.get(':answer-field/correct'),str):f[':answer-field/correct']=old_to_new.get(f[':answer-field/correct'],f[':answer-field/correct'])
    return q
