#!/usr/bin/env python3
"""Vector-field recognition with the live three-checkbox contract.

Reviewed mathematical templates live in legacy.py. Old radio banks remain replay
evidence. Coefficients, names and candidate order do not create distinct tasks.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
HERE = Path(__file__).with_suffix('')
spec = importlib.util.spec_from_file_location('vector_field_legacy', HERE/'legacy.py')
legacy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(legacy)
KP_ID, KP_UUID, TITLE = legacy.KP_ID, legacy.KP_UUID, legacy.TITLE
VERSION = 'vector-field-3d-checkbox-3'
LEVELS = legacy.LEVELS
CURRENT = json.loads((HERE/'source-current.json').read_text())
SOURCES = {q[':question/math-academy-id']:q for q in CURRENT['record'][':knowledge-point/questions']}
digest, uid = legacy.digest, legacy.uid
KEYS = ('I','II','III')

def task_signature(dims):
    return digest(sorted(map(tuple,dims)))

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
    if field_type not in (None,'checkbox',':answer-field.type/checkbox'):
        raise ValueError('Only three-checkbox response fields are supported')
    r = legacy.generate(level,seed,template,None,parameters,profile)
    q,meta = r['question'],r['generation']
    lines = q[':question/problem'].splitlines()
    candidates = [s for s in lines if s.startswith('- $')]
    q[':question/problem'] = lines[0]+'\n\nSelect all that apply.\n\n'+'\n'.join(
        '- **'+key+'.** '+s[2:] for key,s in zip(KEYS,candidates))
    dims = meta['semantic_signature']
    identity = {'version':VERSION,'level':level,'problem':q[':question/problem'],
        'solution':q[':question/worked-solution'],'keys':KEYS,'dimensions':dims}
    cid = digest(identity)
    q[':question/id'] = uid(cid)
    fields = []
    for key,(n,m) in zip(KEYS,dims):
        fid = uid([cid,key])
        answers = [{':answer/id':uid([fid,value]),':answer/type':':answer.type/text',':answer/value':value}
            for value in ('false','true')]
        correct = str(n==m==3).lower()
        fields.append({':answer-field/id':fid,':answer-field/key':key,
            ':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':answers,
            ':answer-field/correct':[':answer/id',next(a[':answer/id'] for a in answers if a[':answer/value']==correct)]})
    q[':question/answer-fields'] = fields
    meta.update(version=VERSION,content_id=cid,mathematical_fingerprint=task_signature(dims),
        response_contract='three field-owned Boolean checkbox banks',current_source_basis=CURRENT['basis'])
    return r

def generate_easy(seed=0,**kwargs): return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs): return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs): return generate('hard',seed,**kwargs)

def markdown(r):
    return r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution']

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all')
    p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1)
    p.add_argument('--format',choices=('json','markdown'),default='markdown')
    p.add_argument('--template');p.add_argument('--profile')
    a=p.parse_args()
    records=[generate(l,a.seed+i,template=a.template,profile=a.profile)
        for l in (LEVELS if a.difficulty=='all' else (a.difficulty,)) for i in range(a.count)]
    print(json.dumps(records,ensure_ascii=False,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))


# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate', 'generate_easy', 'generate_hard', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name], none_label='None of the above')

if __name__=='__main__':main()
