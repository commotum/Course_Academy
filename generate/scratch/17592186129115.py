#!/usr/bin/env python3
"""Finite, source-faithful moderate entry-removal questions. Easy/hard unsupported.

Structural extension: move columns and every bank target together, accepting only
instances with the original sole correct option and unchanged removal workload.
Column movement is sampling, never an operation requested of the learner.
Coefficient changes are presentation variants and do not create fresh tasks.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import re
import sys
import uuid
try:
    import sympy as sp
except ModuleNotFoundError:
    import os
    runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
    if __name__=='__main__' and runtime.is_file():
        os.execv(str(runtime),[str(runtime),str(Path(__file__).resolve()),*sys.argv[1:]])
    raise

HERE = Path(__file__).with_suffix('')
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT/'scripts/question_capture'))
from math_format import checked_math_content, matrix_tex, normalize_prose
S = json.loads((HERE/'source.json').read_text())
KP_ID = 17592186129115
KP_UUID = S['record'][':knowledge-point/id']
SOURCES = {q[':question/math-academy-id']:q for q in S['record'][':knowledge-point/questions']}
PROFILES = tuple(SOURCES)
VERSION = 'entry-removal-v1'
EXCLUDED = {'q-73151':'Malformed source choice conjunction; original retained, generated profile corrected.'}
MATRIX = re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', re.S)
INDEX = re.compile(r'\{a\}_\{(\d)(\d)\}')
IDENTITY = [0,1,2,3]

def parse(text):
    return [[[int(v.strip()) for v in row.split('&')] for row in body.split(r'\\')]
            for body in MATRIX.findall(text)]

def targets(text):
    return [[int(i)-1,int(j)-1] for i,j in INDEX.findall(text)]

def original(profile):
    return {'matrix':parse(SOURCES[profile][':question/problem'])[0], 'columns':IDENTITY[:]}

def bank(profile, columns):
    f = SOURCES[profile][':question/answer-fields'][0]
    inverse = {old:new for new,old in enumerate(columns)}
    return [[[i,inverse[j]] for i,j in targets(a[':answer/value'])] for a in f[':answer-field/choices']]

def erase(matrix, entries):
    m = [row[:] for row in matrix]
    for i,j in entries:m[i][j]=0
    return m

def leading(matrix):
    return [next((j for j,v in enumerate(row) if v),4) for row in matrix]

def echelon(matrix):
    prev=-1; zero=False
    for p in leading(matrix):
        if p==4:zero=True
        elif zero or p<=prev:return False
        else:prev=p
    return True

def correct_index(profile):
    f=SOURCES[profile][':question/answer-fields'][0]
    return next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id'])

def valid(profile, parameters):
    m=parameters['matrix']; cols=parameters['columns']
    if sorted(cols)!=IDENTITY or len(m)!=4 or any(len(row)!=4 for row in m):return False
    bs=bank(profile,cols); ci=correct_index(profile)
    if echelon(m) or any(m[i][j]==0 for i,j in bs[ci]):return False
    return [echelon(erase(m,b)) for b in bs]==[i==ci for i in range(5)]

def fingerprint_data(m, bs):
    # Ignore coefficients, signs, IDs, seeds, profile, distractors and order.
    # A changed bank alone is not a new assessed task. Identify the sole valid
    # correction and the before/after leading-entry relations.
    good=[b for b in bs if echelon(erase(m,b))]
    assert len(good)==1
    data=[leading(m),sorted(good[0]),leading(erase(m,good[0]))]
    return hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()

def fingerprint(q):
    f=q[':question/answer-fields'][0]
    return fingerprint_data(parse(q[':question/problem'])[0],[targets(a[':answer/value']) for a in f[':answer-field/choices']])

def structural_catalog():
    result=[]; seen=set()
    for profile in PROFILES:
        orig=original(profile)['matrix']
        for cols in itertools.permutations(IDENTITY):
            p={'matrix':[[row[j] for j in cols] for row in orig],'columns':list(cols)}
            if not valid(profile,p):continue
            fp=fingerprint_data(p['matrix'],bank(profile,cols))
            if fp not in seen:result.append({'profile':profile,'parameters':p,'fingerprint':fp});seen.add(fp)
    return result

def entry_text(entries):
    labels=['${a}_{'+str(i+1)+str(j+1)+'}$' for i,j in entries]
    if len(labels)==1:return labels[0]
    if len(labels)==2:return ' and '.join(labels)
    return ', '.join(labels[:-1])+', and '+labels[-1]

@checked_math_content
def generate(difficulty, seed, profile=None, parameters=None, replay=False):
    if difficulty!='moderate':raise ValueError('Unsupported level: '+difficulty+'; only observed moderate entry-removal workload is validated')
    rng=random.Random(seed)
    if parameters is None:
        domain=[x for x in structural_catalog() if profile is None or x['profile']==profile]
        if not domain:raise ValueError('No validated structural variants')
        chosen=rng.choice(domain);profile=chosen['profile']
        parameters=json.loads(json.dumps(chosen['parameters']))
        parameters['matrix']=[[rng.choice([i for i in range(-9,10) if i]) if v else 0 for v in row] for row in parameters['matrix']]
    parameters=json.loads(json.dumps(parameters))
    assert profile in SOURCES and valid(profile,parameters)
    m=parameters['matrix'];bs=bank(profile,parameters['columns']);ci=correct_index(profile)
    corrected=erase(m,bs[ci]);source=SOURCES[profile];sf=source[':question/answer-fields'][0]
    prompt='Consider the matrix $A$ given below.\nWhich entries of $A$ could be replaced by $0$ in order to get a matrix in row echelon form?\n\n$$\nA='+matrix_tex(m)+'\n$$'
    solution='Notice that by replacing '+entry_text(bs[ci])+' with $0$, we get a matrix in row echelon form:\n\n$$\nA='+matrix_tex(m)+r'\,⟶\,'+matrix_tex(corrected)+'.\n$$\n\nThe other options will not give us a matrix in row echelon form.'
    values=[entry_text(b)+' only' for b in bs]
    if replay:
        assert parameters==original(profile)
        prompt=source[':question/problem'];solution=source[':question/worked-solution']
        values=[a[':answer/value'] for a in sf[':answer-field/choices']]
        # q-73151 has a malformed two-entry distractor. Replay original evidence;
        # serving uses the supported set reading and normal English above.
    prompt=normalize_prose(prompt);solution=normalize_prose(solution)
    content={'problem':prompt,'solution':solution,'choices':sorted(values),'correct':values[ci]}
    qid=str(uuid.uuid5(uuid.UUID(KP_UUID),json.dumps(content,sort_keys=True)))
    fid=str(uuid.uuid5(uuid.UUID(qid),'field/selection'))
    answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/text',':answer/value':v} for v in values]
    q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/moderate',
       ':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[ci][':answer/id']]}]}
    return {'question':q,'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':S['record'][':knowledge-point/title']},
       'generation':{'version':VERSION,'template':'replace-entries-4x4','profile':profile,'seed':seed,'parameters':parameters,'replay':replay,
       'mathematical_fingerprint':fingerprint(q),'source_db_id':source[':db/id'],'source_question':profile,'domain':'nonzero signed integers [-9,9]; finite validated column domain',
       'dependencies':{'sympy':sp.__version__},'assets':[]}}

def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+ '\n'.join('- '+a[':answer/value'] for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',required=True);ap.add_argument('--count',type=int,default=5);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json','markdown'],default='json');ap.add_argument('--profile',choices=PROFILES)
    a=ap.parse_args()
    if a.difficulty!='moderate':ap.error('Unsupported difficulty; easy and hard have no source-supported templates')
    domain=[x for x in structural_catalog() if a.profile is None or x['profile']==a.profile]
    if a.count<1 or a.count>len(domain):ap.error('finite-limit: requested count exceeds '+str(len(domain))+' distinct tasks')
    random.Random(a.seed).shuffle(domain)
    records=[]
    for i,x in enumerate(domain[:a.count]):
        p=json.loads(json.dumps(x['parameters']));rng=random.Random(a.seed+i)
        p['matrix']=[[rng.choice([n for n in range(-9,10) if n]) if v else 0 for v in row] for row in p['matrix']]
        records.append(generate(a.difficulty,a.seed+i,x['profile'],p))
    print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))

if __name__=='__main__':main()
