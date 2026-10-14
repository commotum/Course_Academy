"""Scoped native-record normalization and replay checks for durable import."""
import copy
import json
import re
import validate as original

g=original.g

def source_normalize(x):
    if isinstance(x,dict):return {k:source_normalize(v) for k,v in x.items() if k!=':db/id'}
    if isinstance(x,list):return sorted([source_normalize(v) for v in x],key=lambda v:json.dumps(v,sort_keys=True))
    return str(x) if not isinstance(x,(str,int,float,bool,type(None))) else x

def normalize(q):
    q=copy.deepcopy(q)
    for key in (':question/difficulty',):
        if isinstance(q.get(key),dict):q[key]=str(q[key][':db/ident'])
    q.pop(':db/id',None)
    for f in q[':question/answer-fields']:
        f.pop(':db/id',None)
        if isinstance(f[':answer-field/type'],dict):f[':answer-field/type']=str(f[':answer-field/type'][':db/ident'])
        if isinstance(f.get(':answer-field/correct'),dict):f[':answer-field/correct']=[':answer/id',str(f[':answer-field/correct'][':answer/id'])]
        for a in f[':answer-field/choices']:
            a.pop(':db/id',None)
            a[':answer/id']=str(a[':answer/id'])
            if isinstance(a[':answer/type'],dict):a[':answer/type']=str(a[':answer/type'][':db/ident'])
        f[':answer-field/id']=str(f[':answer-field/id'])
        f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
    q[':question/id']=str(q[':question/id'])
    return q

def local(r):
    r=copy.deepcopy(r)
    for a in r['generation'].get('published_assets',{}).values():
        for key in (':question/problem',':question/worked-solution'):
            r['question'][key]=r['question'][key].replace(a['reference'],a['local'])
        for f in r['question'][':question/answer-fields']:
            for choice in f[':answer-field/choices']:
                if choice[':answer/value']==a['reference']:choice[':answer/value']=a['local']
    return r

def replay(r):
    meta=r['generation']
    return g.generate(meta['difficulty'],meta['seed'],meta['template'],parameters=meta['parameters'],profile=meta['bank_profile'])

def validate(r):
    meta=r['generation']
    assert meta['version']==g.VERSION and meta['eligible_for_learning'] and not meta['evidence_only']
    assert r['knowledge_point']['db_id']==g.KP_ID and r['knowledge_point']['id']==g.KP_UUID
    assert meta['mathematical_fingerprint']==replay(r)['generation']['mathematical_fingerprint']
    original.check_display(local(r))
    assert normalize(local(r)['question'])==normalize(replay(r)['question'])
    return r

def native(r):return original.engine_rows([r])[0]
