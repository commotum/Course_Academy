#!/usr/bin/env python3
"""Bounded sum-rule exponent variants; only source-supported moderate questions.
CLI --difficulty moderate --count N --seed N --format json|markdown. No writes.
"""
import argparse,hashlib,json,random,uuid
from pathlib import Path
try:import sympy as sp
except ModuleNotFoundError:
 import os,sys
 runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python';os.execv(str(runtime),[str(runtime),str(Path(__file__).resolve()),*sys.argv[1:]])
KP_ID=17592186059864;KP_UUID='d3469bdd-a201-5219-a734-ed3caa6b039a';HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text());TITLE=SOURCE['kp'][':knowledge-point/title'];VERSION='1.0.0';SUPPORTED_LEVELS=('moderate',)
GENERATOR_UUID=str(SOURCE['kp'].get(':knowledge-point/question-generator',{}).get(':question-generator/id',uuid.uuid5(uuid.UUID(KP_UUID),'question-generator')))
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['kp'][':knowledge-point/questions']}
PROFILES={'q-10291':('moderate',{'a':3,'b':2}),'q-339462':('moderate',{'a':5})};x=sp.Symbol('x',positive=True)
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),v))
def candidates(sid):return [{'a':a,'b':b} for a in range(2,7) for b in range(2,5)] if sid=='q-10291' else [{'a':a} for a in range(3,8)]
def functions(sid,p):return x**p['a']+x**(-p['b'])-x if sid=='q-10291' else x**p['a']+x**sp.Rational(4,3)
def radio_text(t,p):
 a,b=p['a'],p['b']
 # Replace longest structures first through nonoverlapping named markers.
 substitutions=[(r'6{x}^{2}',f'{a*b}'+r'{x}^{'+str(a-1)+'}'),(r'3{x}^{(3-1)}',str(a)+r'{x}^{('+str(a)+'-1)}'),(r'(-2){x}^{(-2-1)}','(-'+str(b)+r'){x}^{(-'+str(b)+'-1)}'),(r'3{x}^{3}',str(a)+r'{x}^{'+str(a)+'}'),(r'3{x}^{2}',str(a)+r'{x}^{'+str(a-1)+'}'),(r'2{x}^{-3}',str(b)+r'{x}^{-'+str(b+1)+'}'),(r'\frac{2}{{x}^{3}}',r'\frac{'+str(b)+r'}{{x}^{'+str(b+1)+'}}'),(r'\frac{1}{{x}^{2}}',r'\frac{1}{{x}^{'+str(b)+'}}'),(r'{x}^{-2}',r'{x}^{-'+str(b)+'}'),(r'{x}^{3}',r'{x}^{'+str(a)+'}')]
 for i,(old,new) in enumerate(substitutions):t=t.replace(old,'@@'+str(i)+'@@')
 for i,(old,new) in enumerate(substitutions):t=t.replace('@@'+str(i)+'@@',new)
 return t

def blank_text(t,p):
 a=p['a'];t=t.replace(r'5{x}^{(5-1)}','@@derivative@@').replace(r'5{x}^{4}','@@simplified@@').replace(r'{x}^{5}',r'{x}^{'+str(a)+'}')
 return t.replace('@@derivative@@',str(a)+r'{x}^{('+str(a)+'-1)}').replace('@@simplified@@',str(a)+r'{x}^{'+str(a-1)+'}')
def generate(level,seed=0,template=None,parameters=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('unsupported level '+level)
 rng=random.Random(seed);sid=template or rng.choice(list(PROFILES))
 if sid not in PROFILES:raise ValueError('unsupported template')
 p=parameters or rng.choice(candidates(sid))
 if p not in candidates(sid) or any(type(z)!=int for z in p.values()):raise ValueError('outside bounded exponent parameters')
 old=SOURCES[sid];render=radio_text if sid=='q-10291' else blank_text;f=functions(sid,p);correct=sp.diff(f,x);fp=digest(str(sp.expand(f)))
 qid=uid('question:'+fp);of=old[':question/answer-fields'][0];fid=uid('field:'+qid+':'+of[':answer-field/key']);choices=[]
 for oa in of[':answer-field/choices']:
  value=render(oa[':answer/value'],p);choices.append({':answer/id':uid('answer:'+fid+':'+value),':answer/type':':answer.type/math',':answer/value':value})
 index=next(i for i,z in enumerate(of[':answer-field/choices']) if z[':answer/id']==of[':answer-field/correct'][':answer/id'])
 field={':answer-field/id':fid,':answer-field/key':of[':answer-field/key'],':answer-field/type':of[':answer-field/type'][':db/ident'],':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[index][':answer/id']]}
 q={':question/id':qid,':question/problem':render(old[':question/problem'],p),':question/worked-solution':render(old[':question/worked-solution'],p),':question/difficulty':':question.difficulty/moderate',':question/answer-fields':[field]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'template':sid,'profile':sid,'seed':seed,'parameters':p,'source_basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'source_question':old[':question/id'],'computed_correct':str(correct),'mathematical_fingerprint':fp,'domain':'real x != 0' if sid=='q-10291' else 'real x (cube roots interpreted as real roots)','dependencies':{'sympy':sp.__version__},'sampling_policy':'Explicit bounded exponent extension; radio a=2..6,b=2..4; blank a=3..7, fixed 4/3 root term; source coefficient magnitudes remain one'}}
def batch(level,count,seed):
 if level not in SUPPORTED_LEVELS:raise ValueError('unsupported level '+level)
 options=[(s,p) for s in PROFILES for p in candidates(s)]
 if type(count)!=int or count<1:raise ValueError('positive integer count required')
 if count>len(options):raise ValueError('finite-limit: '+str(len(options)))
 random.Random(seed).shuffle(options);return [generate(level,seed,s,p) for s,p in options[:count]]
def markdown(rec):
 q=rec['question'];return q[':question/problem']+'\n\n'+'\n'.join(a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',required=True);ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json','markdown'],default='json');args=ap.parse_args();records=batch(args.difficulty,args.count,args.seed);print(json.dumps({'instances':records},indent=2,ensure_ascii=False) if args.format=='json' else '\n\n'.join(map(markdown,records)))
