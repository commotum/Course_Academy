#!/usr/bin/env python3
"""Source-profile augmented-matrix generator; easy and moderate only.

Magnitude slots shared by their observed literal are intentionally coupled.
Units, zeros, signs, equation placement and five-choice profiles remain fixed.
No equation solving, row operations, additional stages or generated plots.
"""
import argparse, hashlib, json, random, re, uuid, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts/question_capture'))
from math_format import normalize_prose, normalize_tex, checked_math_content

KP_ID=17592186059768
KP_UUID='3f9ccaa5-d69c-584d-946e-0c57b3050160'
TITLE='Finding the Augmented Matrix of a System of Linear Equations'
VERSION='1.0.1'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
PROFILES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
SUPPORTED=('easy','moderate')

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def slots(q):
    texts=[q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']]
    return sorted({int(n) for t in texts for n in re.findall(r'\d+',t) if int(n)>1})
def render(text,parameters):
    text=re.sub(r'\d+',lambda m:str(parameters.get(m[0],int(m[0]))),text)
    text=normalize_prose(text)
    def coefficient(match):
        paragraph=text[:match.start()].rstrip().split('\n\n')[-1]
        if 'coefficient matrix' not in paragraph.lower() or 'augment' in paragraph.lower():return match[0]
        return re.sub(r'\\left\[\\begin\{array\}\{c+\|c\}(.*?)\\end\{array\}\\right\]',lambda matrix:r'\begin{bmatrix}'+matrix[1]+r'\end{bmatrix}',match[0],flags=re.S)
    return re.sub(r'\$\$.*?\$\$',coefficient,text,flags=re.S)
@checked_math_content
def generate(difficulty,seed,template=None,parameters=None,profile=None):
    if difficulty not in SUPPORTED:raise ValueError('Unsupported difficulty: '+difficulty)
    rng=random.Random(seed)
    names=[n for n,q in PROFILES.items() if q[':question/difficulty'][':db/ident'].endswith('/'+difficulty)]
    name=profile or template or rng.choice(names)
    if name not in names:raise ValueError('Profile does not belong to requested difficulty')
    src=PROFILES[name]
    parameters={str(k):int(v) for k,v in (parameters or dict(zip(map(str,slots(src)),rng.sample(range(2,25),len(slots(src)))))).items()}
    assert set(parameters)==set(map(str,slots(src))) and all(2<=n<=24 for n in parameters.values())
    values=[normalize_tex(render(a[':answer/value'],parameters)) for a in src[':question/answer-fields'][0][':answer-field/choices']]
    assert len(set(parameters.values()))==len(parameters), "Magnitude slots must remain distinct"
    assert len(set(values))==5
    problem=render(src[':question/problem'],parameters)
    qid=str(uuid.uuid5(uuid.UUID(KP_UUID),digest([problem,sorted(values)])))
    fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
    choices=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),value)),':answer/type':':answer.type/math',':answer/value':value} for value in values]
    correct=normalize_tex(render(src[':question/answer-fields'][0][':answer-field/correct'][':answer/value'],parameters))
    question={':question/id':qid,':question/problem':problem,':question/worked-solution':render(src[':question/worked-solution'],parameters),':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',next(a[':answer/id'] for a in choices if a[':answer/value']==correct)]}]}
    return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'seed':seed,'template':name,'bank_profile':name,'parameters':parameters,'source_question_id':src[':db/id'],'source_basis':SOURCE['basis'],'eligible_for_learning':True,'evidence_only':False,'slot_policy':'Observed equal magnitudes coupled; units/zeros/signs/placement fixed; magnitude bounds 2..24'}}
def markdown(rec):
    q=rec['question'];f=q[':question/answer-fields'][0]
    return q[':question/problem']+'\n\n'+'\n\n'.join('$'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
    p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=SUPPORTED,required=True);p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--template');p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args()
    records=[generate(a.difficulty,a.seed+i,a.template) for i in range(a.count)]
    print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
