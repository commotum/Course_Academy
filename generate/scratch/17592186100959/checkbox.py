#!/usr/bin/env python3
"""Current three-checkbox layout for the frozen, exact ODE generator.
The original radio generator and its complete source-bank replay stay intact.
This adapter retains all mathematical parameters, domains and solution stages.
"""
from pathlib import Path
import argparse,copy,importlib.util,json,re
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('ode_core',HERE.with_suffix('.py'))
core=importlib.util.module_from_spec(spec);spec.loader.exec_module(core)
VERSION='1.1.0-checkbox'
KEYS=('I','II','III')

def convert(record):
    r=copy.deepcopy(record);q=r['question'];f=q[':question/answer-fields'][0]
    answer=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
    mask=next(m for m,label in core.LABELS.items() if label==answer)
    i=iter(KEYS)
    q[':question/problem']=re.sub(r'- \$y',lambda m:'- **'+next(i)+'.** $y',q[':question/problem'])
    q[':question/problem']=q[':question/problem'].replace('\n\n- **I.**','\n\nSelect all that apply.\n\n- **I.**',1)
    content=core.digest([VERSION,q[':question/problem'],q[':question/worked-solution'],mask])
    qid=core.uid(content);q[':question/id']=qid;fields=[]
    for n,key in enumerate(KEYS):
        fid=core.uid(qid+'/'+key)
        choices=[{':answer/id':core.uid(fid+'/'+value),':answer/type':':answer.type/text',':answer/value':value} for value in ('false','true')]
        fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':choices,':answer-field/correct':[':answer/id',core.uid(fid+'/'+('true' if mask&(1<<n) else 'false'))]})
    q[':question/answer-fields']=fields
    r['generation'].update({'version':VERSION,'content_hash':content,'layout':'three field-owned boolean checkbox banks; complete subset required','legacy_core_version':core.VERSION})
    return r

def generate(level,seed=0,template=None,parameters=None,profile=None):
    return convert(core.generate(level,seed,template=template,parameters=parameters,profile=profile))

def markdown(r):
    q=r['question'];flags=[next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]) for f in q[':question/answer-fields']]
    return '**Difficulty and origin:** '+core.preview_label(r)+'\n\n'+q[':question/problem']+'\n\n**Correct checkbox values:** '+', '.join(k+'='+a for k,a in zip(KEYS,flags))+'\n\n'+q[':question/worked-solution']


# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name], none_label='None of the above')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json','markdown'],default='json');ap.add_argument('--template');args=ap.parse_args()
    if args.count<1:ap.error('--count must be positive')
    rows=[generate(l,args.seed+i,template=args.template) for l in (core.FAMILIES if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
    print(json.dumps(rows,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rows))
