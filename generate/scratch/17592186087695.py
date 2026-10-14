#!/usr/bin/env python3
"""Bounded easy zero-matrix recognition; three field-owned checkbox decisions."""
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
try:
    import sympy as sp
except ModuleNotFoundError:
    import os, sys
    interpreter=Path(__file__).resolve().parents[2]/'.venv/bin/python'
    if Path(sys.executable).resolve()==interpreter.resolve():raise
    os.execv(str(interpreter),[str(interpreter),str(Path(__file__).resolve()),*sys.argv[1:]])
KP_ID=17592186087695
KP_UUID='ddb59990-7419-585f-aa1b-901d59c8cfc1'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
SUPPORTED_LEVELS=('easy',)
HERE=Path(__file__).with_suffix('')
VERSION='1.0.0'
TEMPLATES=json.loads((HERE/'templates.json').read_text())

def arrays(text):
    out={}
    pattern=r'([A-Z])\s*=\s*\\begin\{bmatrix\}([\s\S]*?)\\end\{bmatrix\}'
    for m in re.finditer(pattern,text):
        out[m[1]]=[[v.strip() for v in row.strip().split('&')] for row in m[2].split('\\\\')]
    if not out:raise ValueError('No complete named matrices')
    return out

def fingerprint_text(text):
    # Labels, ordering, nonzero magnitudes, seed and choice order are not new tasks.
    items=[]
    for rows in arrays(text).values():
        items.append((len(rows),len(rows[0]),tuple(tuple(int(sp.Rational(v)!=0) for v in row) for row in rows)))
    return json.dumps(sorted(items),separators=(',',':'))

def generate(difficulty='easy',seed=0,template=None,parameters=None,profile=None):
    if difficulty not in SUPPORTED_LEVELS:raise ValueError('Only easy certified; moderate/hard remain unsupported')
    rng=random.Random(seed)
    template=template or rng.choice(list(TEMPLATES))
    if template not in TEMPLATES or profile not in (None,template):raise ValueError('Unknown source template/profile')
    t=TEMPLATES[template]
    if parameters is None:
        labels=['A','B','C'];matrices=[];witnesses=[]
        for original in t['parameters']['matrices']:
            r,c=rng.randint(1,4),rng.randint(1,5)
            rows=[['0']*c for _ in range(r)]
            nonzero=sum(sp.Rational(v)!=0 for row in original for v in row)
            if nonzero:
                count=min(nonzero,r*c)
                cells=rng.sample(range(r*c),count)
                for cell in cells:rows[cell//c][cell%c]=rng.choice(['1','0.1','3','10'])
                witnesses.append([cells[0]//c+1,cells[0]%c+1])
            else:witnesses.append(None)
            matrices.append(rows)
        parameters={'labels':labels,'matrices':matrices,'witnesses':witnesses}
    p=json.loads(json.dumps(parameters));labels=p['labels'];matrices=p['matrices'];ws=p['witnesses']
    if len(labels)!=3 or len(set(labels))!=3 or any(not re.fullmatch('[A-Z]',z) for z in labels):raise ValueError('Three distinct matrix labels required')
    if len(matrices)!=3 or len(ws)!=3:raise ValueError('Three matrix/witness slots required')
    zero=[]
    for i,rows in enumerate(matrices):
        if not 1<=len(rows)<=4 or not rows or not 1<=len(rows[0])<=6 or any(len(row)!=len(rows[0]) for row in rows):raise ValueError('Shape outside bounded domain')
        if any(v not in ('0','1','0.1','3','10') for row in rows for v in row):raise ValueError('Entry outside observed domain')
        nz=[(r+1,c+1) for r,row in enumerate(rows) for c,v in enumerate(row) if sp.Rational(v)!=0]
        original=t['parameters']['matrices'][i]
        source_nz=sum(sp.Rational(v)!=0 for row in original for v in row)
        if bool(nz)!=bool(source_nz) or len(nz)!=min(source_nz,len(rows)*len(rows[0])):raise ValueError('Nonzero role/count changed')
        if (nz and tuple(ws[i] or []) not in nz) or (not nz and ws[i] is not None):raise ValueError('Witness must be a nonzero entry')
        zero.append(not nz)
    if sum(len(z)*len(z[0]) for z in matrices)>46:raise ValueError('Workload exceeds observed easy ceiling')
    render=lambda rows:r'\begin{bmatrix}'+' \\\\ '.join(' & '.join(row) for row in rows)+r'\end{bmatrix}'
    problem='Which of the following are zero matrices?\n\n$$\n'+r',\,'.join(name+'='+render(rows) for name,rows in zip(labels,matrices))+'\n$$\n\nSelect all that apply.'
    bullets=[]
    for i,name in enumerate(labels):
        bullet=t['bullet_templates'][i].replace('{LABEL}',name)
        if ws[i]:
            r,c=ws[i];bullet=bullet.replace('{lower}',name.lower()).replace('{row}',str(r)).replace('{col}',str(c)).replace('{value}',matrices[i][r-1][c-1])
        bullets.append(bullet)
    names=['$'+name+'$' for name,z in zip(labels,zero) if z]
    if len(names)==3:conclusion='Therefore, '+names[0]+', '+names[1]+', and '+names[2]+' are zero matrices.'
    elif len(names)==2:conclusion='Therefore, only '+' and '.join(names)+' are zero matrices.'
    else:conclusion='Therefore, only '+names[0]+' is a zero matrix.'
    worked='\n\n'.join(bullets)+'\n\n'+conclusion
    # Full mathematical values define immutable content identity; metadata seed does not.
    qid=str(uuid.uuid5(uuid.UUID(KP_UUID),json.dumps([problem,worked],sort_keys=True)))
    fields=[]
    for name,z in zip(labels,zero):
        fid=str(uuid.uuid5(uuid.UUID(qid),'field:'+name))
        choices=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),value)),':answer/type':':answer.type/text',':answer/value':value} for value in ('false','true')]
        fields.append({':answer-field/id':fid,':answer-field/key':name,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[int(z)][':answer/id']]})
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':'Identifying a Zero Matrix'},'question':{':question/id':qid,':question/problem':problem,':question/worked-solution':worked,':question/difficulty':':question.difficulty/easy',':question/answer-fields':fields},'generation':{'version':VERSION,'template':template,'bank_profile':template,'seed':seed,'parameters':p,'parameter_fingerprint':fingerprint_text(problem),'source_basis':t['basis'],'sympy_version':sp.__version__}}

def batch(difficulty,count,seed):
    if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported level')
    if not 0<=count<=1000:raise ValueError('Batch bounded to 1000 distinct tasks')
    records=[];used=set()
    for n in range(10000):
        if len(records)>=count:break
        try:r=generate(difficulty,seed+n,template=list(TEMPLATES)[n%len(TEMPLATES)])
        except ValueError:continue
        fp=r['generation']['parameter_fingerprint']
        if fp not in used:records.append(r);used.add(fp)
    return records

def markdown(r):
    q=r['question'];return q[':question/problem']+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args();rs=batch(a.difficulty,a.count,a.seed);print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
