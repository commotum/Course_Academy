"""Reuse independent printed-math reader without the draft's top-level fixture run."""
from pathlib import Path
import json,copy,importlib.util
H=Path(__file__).resolve().parent
ns={'__file__':str(H/'validate.py'),'__name__':'point_validation_definitions'}
exec((H/'validate.py').read_text().split('\nsources=[];fixtures=[];')[0],ns)
g=ns['g'];verify=ns['verify'];s=ns['s']
def fingerprint(q):
    x,y,r,a,R,b,answer=ns['read_prompt']({'question':q})
    return g.digest([str(s.simplify(v)) for v in (x,y,a,R,b%(2*s.pi))])
def independent(rec):
    assert rec['generation']['eligible_for_learning'] and not rec['generation']['evidence_only']
    assert rec['knowledge_point']['db_id']==g.KP[':db/id']
    verify(rec)
    q=rec['question'];m=rec['generation']
    replay=g.generate(q[':question/difficulty'].split('/')[-1],m['seed'],template=m['template'],profile=m['profile'],parameters=m['parameters'],field_type=q[':question/answer-fields'][0][':answer-field/type'].split('/')[-1])
    def canonical_record(r):
        r=copy.deepcopy(r)
        for f in r['question'][':question/answer-fields']:
            f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
        return r
    assert canonical_record(replay)==canonical_record(rec),'Record does not reproduce its complete content (choice order ignored)'
    assert len({f[':answer-field/id'] for f in q[':question/answer-fields']})==len(q[':question/answer-fields'])
    ids=[a[':answer/id'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]
    assert len(ids)==len(set(ids)),'Answers must be field-owned'
def checks(rec):
    result=[]
    for i,f in enumerate(rec['question'][':question/answer-fields']):
        if f[':answer-field/type'].endswith('/radio'):
            result += [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every displayed choice'} for a in f[':answer-field/choices']]
        else:
            v=f[':answer-field/choices'][0][':answer/value'];math=g.parse(v)
            d=ns['read_prompt'](rec);R,b=d[4],d[5];trig=s.cos(b) if f[':answer-field/key']=='field-1' else s.sin(b)
            result += [{'field_index':i,'submitted':v,'expected':'accepted','purpose':'Canonical scalar'}, {'field_index':i,'submitted':g.tex(R)+r'\cdot('+g.tex(trig)+')','expected':'accepted','purpose':'Unreduced equivalent radius times trig factor'}, {'field_index':i,'submitted':g.tex(math+1),'expected':'rejected','purpose':'Incorrect scalar'}]
    return result

def finite_records(level):
    if level=='easy':
        for radius in range(1,13):
            for factor in (2,3,4,5):
                for angle in ['1/6','1/3','2/3','5/6','7/6','4/3','5/3','11/6']:
                    yield g.generate(level,field_type='blank',parameters={'radius':radius,'factor':factor,'angle':angle})
    else:
        # Interleave scales across all source families to preserve coverage in small batches.
        for scale in range(1,17 if level=='hard' else 9):
            for name,spec in g.SPEC.items():
                if spec[-1]==level:yield g.generate(level,template=name,parameters={'scale':scale})
