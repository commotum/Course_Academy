#!/usr/bin/env python3
"""Bounded faithful homogeneous RHS variants for KP 17592186096674.
Only scale is sampled: fixed upper-triangular coefficient matrices retain the
source reduction workload. Each complete observed bank scales with the RHS.
No claim is made about the cognitive origin of the source distractors.
"""
import argparse,hashlib,json,random,re,uuid
from pathlib import Path
import sympy as s
KP_ID=17592186096674
HERE=Path(__file__).with_suffix('')
CAPTURE=json.loads((HERE/'source.json').read_text());SOURCE=CAPTURE['record']
KP_UUID=SOURCE[':knowledge-point/id'];GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
SOURCES={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
EXCLUDED={'q-20589':'Missing difficulty, correct answer and worked solution; malformed system markup. Original retained unchanged.'}
SUPPORTED_LEVELS=('easy',);SCALES=tuple(range(1,13));VERSION='1.0.0'

def parse_matrices(text):
    # Some stored answer math has one redundant level of LaTeX escaping.
    if r'\\begin' in text:text=text.replace('\\\\','\\')
    return [s.Matrix([[s.Rational(v.strip()) for v in row.split('&')] for row in b.split(r'\\')]) for b in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]

def triple(text):
    ms=parse_matrices(text)
    if ms:return tuple(ms[0][:,3])
    if '⟨' in text:return tuple(s.Rational(x) for x in text.split('⟨')[1].split('⟩')[0].split(','))
    return tuple(s.Rational(v) for v in re.findall(r'[xyz]\s*=\s*([+-]?\d+)',text))

def matrix(m):return r'\begin{bmatrix}'+' \\\\ '.join(' & '.join(str(v) for v in m.row(i)) for i in range(m.rows))+r'\end{bmatrix}'

def components(mid):
    q=SOURCES[mid];m=parse_matrices(q[':question/worked-solution'])[0]
    f=q[':question/answer-fields'][0];values=[triple(a[':answer/value']) for a in f[':answer-field/choices']]
    answer=triple(f[':answer-field/correct'][':answer/value'])
    shape='rref' if 'reduce the augmented' in q[':question/problem'] and 'then solve' not in q[':question/problem'] else ('text' if f[':answer-field/correct'][':answer/type'][':db/ident']==':answer.type/text' else 'vector')
    return m,values,answer,shape

def render_value(v,shape):
    if shape=='rref':return 'M∼'+matrix(s.eye(3).row_join(s.Matrix(v)))
    if shape=='vector':return '⟨'+','.join(map(str,v))+'⟩'
    return f'$x={v[0]}$, $y={v[1]}$, and $z={v[2]}$'

def scaled_text(text,k):
    # Parameterize every matrix and every explicit system/solution occurrence.
    def mat(m):
        z=parse_matrices(m[0])[0];z[:,3]=z[:,3]*k;return matrix(z)
    text=re.sub(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}',mat,text,flags=re.S)
    text=re.sub(r'(?<![:=])=(\s*)(-?\d+)',lambda m:'='+m[1]+str(int(m[2])*k),text)
    text=re.sub(r'⟨(-?\d+),(-?\d+),(-?\d+)⟩',lambda m:'⟨'+','.join(str(int(v)*k) for v in m.groups())+'⟩',text)
    return text

def generate(difficulty='easy',seed=0,template=None,parameters=None,profile=None):
    if difficulty!='easy':raise ValueError('Unsupported difficulty: no validated source backbone for '+difficulty)
    rng=random.Random(seed);mid=template or rng.choice(sorted(set(SOURCES)-set(EXCLUDED)))
    if mid in EXCLUDED or mid not in SOURCES:raise ValueError('Unsupported source profile')
    if profile is not None and profile!=mid:raise ValueError('Profile must match its source template')
    k=int((parameters or {}).get('scale',rng.choice(SCALES)))
    if k not in SCALES:raise ValueError('scale outside validated bounded domain 1..12')
    src=SOURCES[mid];m,bank,answer,shape=components(mid);m[:,3]=m[:,3]*k
    vals=[tuple(v*k for v in a) for a in bank];correct=tuple(v*k for v in answer)
    assert m[:,:3]*s.Matrix(correct)==m[:,3] and len(set(vals))==5
    fingerprint='gauss-jordan|'+str(list(m))
    qid=str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),fingerprint+'|'+shape+'|'+mid));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    choices=[]
    for vs in vals:
        val=render_value(vs,shape);aid=str(uuid.uuid5(uuid.UUID(fid),val));choices.append({':answer/id':aid,':answer/type':':answer.type/text' if shape=='text' else ':answer.type/math',':answer/value':val})
    ca=choices[vals.index(correct)][':answer/id']
    q={':question/id':qid,':question/problem':scaled_text(src[':question/problem'],k),':question/worked-solution':scaled_text(src[':question/worked-solution'],k),':question/difficulty':':question.difficulty/easy',':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',ca]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':SOURCE[':knowledge-point/title']},'question':q,'generation':{'generator_id':GENERATOR_UUID,'generator_version':VERSION,'seed':seed,'template':shape,'source_profile':mid,'bank_profile':mid,'parameters':{'scale':k},'source_basis':CAPTURE['basis'],'source_question_id':src[':question/id'],'domain':{'scale':list(SCALES)},'sympy_version':s.__version__,'eligible_for_learning':True,'evidence_only':False,'mathematical_fingerprint':hashlib.sha256(fingerprint.encode()).hexdigest()}}

def batch(difficulty,count,seed):
    if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty '+difficulty)
    cells=[(m,k) for m in sorted(set(SOURCES)-set(EXCLUDED)) for k in SCALES];random.Random(seed).shuffle(cells)
    if count>len(cells):raise ValueError(f'Finite capacity {len(cells)} before excluding existing or shown questions')
    return [generate(difficulty,seed,m,{'scale':k}) for m,k in cells[:count]]

def markdown(r):
    q=r['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n'.join(('* ' if a[':answer/id']==f[':answer-field/correct'][1] else '- ')+a[':answer/value'] for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--difficulty',default='easy');p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args()
    records=batch(a.difficulty,a.count,a.seed);print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
