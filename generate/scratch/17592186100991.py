#!/usr/bin/env python3
"""Three-matrix arithmetic: seeded, exact, source-shaped questions.

CLI: --difficulty easy|moderate --count N --seed N --format json|markdown.
Hard is unsupported: no source-backed hard backbone. No database writes.
See the sibling package for source profiles, replay and capability evidence.
"""
from __future__ import annotations
import argparse, hashlib, json, os, random, re, sys, uuid
from pathlib import Path
try:
    import sympy as sp
except ModuleNotFoundError as error:
    # Inventory workers can run the system Python. Reuse this repository's
    # existing dependency environment instead of installing packages globally.
    interpreter=Path(__file__).resolve().parents[2]/'.venv/bin/python'
    if error.name!='sympy' or __name__!='__main__' or not interpreter.is_file() or Path(sys.executable).resolve()==interpreter.resolve():
        raise
    os.execv(str(interpreter),[str(interpreter),str(Path(__file__).resolve()),*sys.argv[1:]])

KP_ID = 17592186100991
KP_UUID = '667ac53c-36b8-56a0-9699-fe27c8373c6b'
TITLE = 'Calculating the Sum or Difference of Three or More Matrices'
VERSION = 'three-matrix-1'
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(KP_UUID), 'question-generator'))
HERE = Path(__file__).with_suffix('')
TEMPLATES = {'easy': ('flat_sum_blank', 'flat_difference_blank', 'flat_sum_radio'),
             'moderate': ('nested_difference_blank', 'nested_sum_blank')}
SOURCE_IDS = {'flat_sum_blank':['q-279526'], 'flat_difference_blank':['q-275408','q-279525'],
              'flat_sum_radio':['q-69636'], 'nested_difference_blank':['q-279527'],
              'nested_sum_blank':['q-279528']}
EXPR = {'flat_sum_blank':'{a}+{b}+{c}', 'flat_difference_blank':'{a}+{b}-{c}',
        'flat_sum_radio':'{a}+{b}+{c}', 'nested_difference_blank':'{a}-({b}-{c})',
        'nested_sum_blank':'{a}+({b}-{c})'}

def digest(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(',',':')).encode()).hexdigest()

def uid(x):
    return str(uuid.uuid5(uuid.UUID(KP_UUID), x))

def matrix(rows):
    return r'\begin{bmatrix}'+r' \\ '.join(' & '.join(map(str,row)) for row in rows)+r'\end{bmatrix}'

def parse_matrices(text):
    return [[[int(v.strip()) for v in row.split('&')] for row in m.split('\\\\')]
            for m in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]

def expression(template, names):
    return EXPR[template].format(a=names[0], b=names[1], c=names[2])

def scalar(v, following=False):
    return '('+str(v)+')' if following and v<0 else str(v)

def cell_ops(a,b,c,template):
    return str(a)+'+'+scalar(b,True)+('+' if template.startswith('flat_sum') else '-')+scalar(c,True)

def evaluated(template, matrices):
    a,b,c = map(sp.Matrix, matrices)
    if template.startswith('flat_sum'): return a+b+c
    if template=='flat_difference_blank': return a+b-c
    if template=='nested_difference_blank': return a-(b-c)
    if template=='nested_sum_blank': return a+(b-c)
    raise ValueError('Unsupported template')

def radio_bank(matrices):
    """Complete observed q-69636 bank. Per-cell sign changes are explicit.

    These reproduce the observed objects; why learners make the compound
    sign mistakes is unresolved. No misconception explanations are displayed.
    """
    a,b,c=map(sp.Matrix,matrices); z=a+b+c
    first=z.copy();first[0,1]=-a[0,1]+b[0,1]+c[0,1];first[1,0]=-z[1,0]
    first[2,0]=-z[2,0];first[2,1]=a[2,1]-b[2,1]+c[2,1]
    second=z.copy();second[1,1]=a[1,1]-b[1,1]+c[1,1]
    second[2,0]=-z[2,0];second[2,1]=a[2,1]-b[2,1]+c[2,1]
    third=first.copy();third[2,0]=z[2,0];third[2,1]=z[2,1]
    fifth=z.copy();fifth[0,1]=a[0,1]-b[0,1]+c[0,1]
    fifth[1,1]=a[1,1]-b[1,1]+c[1,1];fifth[2,1]=-z[2,1]
    return [first,second,third,z,fifth]

def prompt(template,p):
    names=p['names']; expr=expression(template,names)
    text='Calculate $'+expr+'$, where\n\n$$\n'
    text+=r',\,'.join(n+'='+matrix(m) for n,m in zip(names,p['matrices']))+'.\n$$'
    if template.endswith('blank'):
        text+='\n\n| $'+expr+r'=\,\,$ |  | {{field-1}} | {{field-2}} |  |'+'\n| --- | --- | --- | --- | --- |\n|  | {{field-3}} | {{field-4}} |  |  |'
    return text

def solution(template,p):
    a,b,c = map(sp.Matrix,p['matrices']); names=p['names'];expr=expression(template,names)
    z=evaluated(template,p['matrices']); n,m=a.shape
    if template.startswith('flat'):
        stages=[matrix(a.tolist())+'+'+matrix(b.tolist())+('+' if template.startswith('flat_sum') else '-')+matrix(c.tolist()),
                matrix([[cell_ops(a[i,j],b[i,j],c[i,j],template) for j in range(m)] for i in range(n)]),matrix(z.tolist())]
    else:
        op='-' if template=='nested_difference_blank' else '+'
        inner=b-c
        stages=[matrix(a.tolist())+op+'('+matrix(b.tolist())+'-'+matrix(c.tolist())+')',
                matrix(a.tolist())+op+matrix([[str(b[i,j])+'-'+scalar(c[i,j],True) for j in range(m)] for i in range(n)]),
                matrix(a.tolist())+op+matrix(inner.tolist()),
                matrix([[str(a[i,j])+op+scalar(inner[i,j],True) for j in range(m)] for i in range(n)]), matrix(z.tolist())]
    radio=template.endswith('radio')
    return ('Performing the operations on each corresponding entry, we get'+(':' if radio else '')+'\n\n$$\n'+
            r'\begin{aligned}'+expr+' & ='+r' \\  & ='.join(stages)+('' if radio else '.')+r'\end{aligned}'+'\n$$')

def task_fingerprint(template,matrices):
    # Matrix letters, seeds, option order and authored field UUIDs are irrelevant.
    signs=(1,-1,1) if template=='nested_difference_blank' else (1,1,-1) if template in ('flat_difference_blank','nested_sum_blank') else (1,1,1)
    return digest({'operands':matrices,'signs':signs})

def fingerprint(q):
    text=q[':question/problem'];mats=parse_matrices(text)
    if len(mats)!=3: return digest({'excluded_prompt':text})
    expr=re.search(r'Calculate \$(.*?)\$',text)[1].replace(' ','')
    template='nested_difference_blank' if '-(' in expr else 'nested_sum_blank' if '+(' in expr else 'flat_difference_blank' if '-' in expr else 'flat_sum_blank'
    return task_fingerprint(template,mats)

def generate(level,seed,template=None,parameters=None):
    if level not in TEMPLATES: raise ValueError('Unsupported difficulty: '+level)
    rng=random.Random(seed);template=template or rng.choice(TEMPLATES[level])
    if template not in TEMPLATES[level]:raise ValueError('Template/difficulty mismatch')
    if parameters is None:
        rows=3 if template.endswith('radio') else 2
        names=rng.choice([['A','B','C'],['C','D','E'],['R','S','T'],['X','Y','Z']])
        # Preserve the observed 3x2 bank's sign configuration; magnitudes vary.
        while True:
            matrices=[[[rng.randint(-9,9) for _ in range(2)] for _ in range(rows)] for _ in range(3)]
            if template.endswith('radio'):
                signs=[[[-1,-1],[-1,1],[-1,-1]],[[1,-1],[1,-1],[1,-1]],[[1,0],[0,1],[0,1]]]
                matrices=[[[signs[k][i][j]*rng.randint(1,12) for j in range(2)] for i in range(3)] for k in range(3)]
                if len({tuple(m) for m in radio_bank(matrices)})<5:continue
            break
        p={'matrices':matrices,'names':names}
    else:p=json.loads(json.dumps(parameters))
    assert len(p['names'])==3 and len(set(p['names']))==3 and all(re.fullmatch('[A-Z]',n) for n in p['names'])
    shape=(3,2) if template.endswith('radio') else (2,2)
    assert len(p['matrices'])==3
    for m in p['matrices']:
        assert len(m)==shape[0] and all(len(r)==shape[1] for r in m)
        assert all(isinstance(v,int) and not isinstance(v,bool) for r in m for v in r)
    z=evaluated(template,p['matrices']);fp=task_fingerprint(template,p['matrices'])
    # Exact content identity also distinguishes authored backbone and response shape.
    content=digest({'task':fp,'template':template,'names':p['names'],'version':VERSION})
    qid=uid('question:'+content);fields=[]
    if template.endswith('radio'):
        bank=radio_bank(p['matrices']);assert len({tuple(m) for m in bank})==5
        values=[matrix(m.tolist()) for m in bank];correct=matrix(z.tolist())
        fid=uid(qid+':selection');choices=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
        fields=[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid(fid+':'+correct)]}]
    else:
        for i,v in enumerate(z):
            key='field-'+str(i+1);fid=uid(qid+':'+key);aid=uid(fid+':'+str(v))
            fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/blank',':answer-field/choices':[{':answer/id':aid,':answer/type':':answer.type/math',':answer/value':str(v)}],':answer-field/correct':[':answer/id',aid]})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},
            'question':{':question/id':qid,':question/problem':prompt(template,p),':question/worked-solution':solution(template,p),':question/difficulty':':question.difficulty/'+level,':question/answer-fields':fields},
            'generation':{'version':VERSION,'template':template,'bank_profile':'q-69636' if template.endswith('radio') else 'blank','seed':seed,'parameters':p,'source_ids':SOURCE_IDS[template],'sympy_version':sp.__version__,'mathematical_fingerprint':fp,'eligible_for_learning':True,'domain':'integer entries, real matrix entrywise addition/subtraction; same dimensions','sampling_policy':'2x2 blanks or observed 3x2 radio sign pattern; entries -9..9, radio magnitudes 1..12'}}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--difficulty',required=True);parser.add_argument('--count',type=int,default=1);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--template');parser.add_argument('--format',choices=['json','markdown'],default='json');args=parser.parse_args()
    if args.count<1:parser.error('Positive count required')
    if args.difficulty not in TEMPLATES:parser.error('Unsupported level; hard lacks source-backed difficulty evidence')
    records=[];seen=set()
    for i in range(args.count*100):
        r=generate(args.difficulty,args.seed+i,args.template);fp=r['generation']['mathematical_fingerprint']
        if fp in seen:continue
        records.append(r);seen.add(fp)
        if len(records)==args.count:break
    if len(records)!=args.count:raise ValueError('Finite sampling bound reached')
    if args.format=='json':print(json.dumps(records,indent=2))
    else:
        print('\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in records))

if __name__=='__main__':main()
