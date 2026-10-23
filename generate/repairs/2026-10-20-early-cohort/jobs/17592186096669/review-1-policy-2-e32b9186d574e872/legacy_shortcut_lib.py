"""Reproduce bank-shape shortcuts using rendered prompt signatures, never generation metadata.
Usage: repo/.venv/bin/python probe_shortcuts.py [--strict]
--strict exits nonzero while any tested profile is perfectly predictable.
"""
import json,re,sys,hashlib,collections
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parent

def read(p):return json.loads((ROOT/p).read_text())
def write(p,obj):(ROOT/p).write_text(json.dumps(obj,indent=2,ensure_ascii=False))
def vec(s):
 if s.startswith('\\\\begin') or s.startswith('⟨') and '\\\\frac' in s:s=s.replace('\\\\','\\')
 s=s.replace(' ','');s=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'\1/\2',s)
 return tuple(F(a) for a in (s[1:-1].split(',') if s.startswith('⟨') else s.removeprefix(r'\begin{bmatrix}').removesuffix(r'\end{bmatrix}').split(r'\\')))
def signature(q):
 text=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/problem'],re.S)[1]
 lhs=','.join(re.sub(r'\s+','',r.split('=')[0].replace('&','')) for r in text.split(r'\\'))
 shape='angle' if q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'].startswith('⟨') else 'column'
 return lhs+'; '+shape
sources=json.loads((ROOT.parent/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']
labels={signature(q):q[':question/math-academy-id'] for q in sources}
rules={
'q-20418':('choose the sole vector with first = second',lambda v:v[0]==v[1]),
'q-10195':('choose the negative first coordinate closest to zero',None),
'q-10196':('choose first = 0 and last > 0',lambda v:v[0]==0 and v[2]>0),
'q-10197':('choose the largest first coordinate',None),
'q-10198':('choose largest middle coordinate, breaking ties by smallest last coordinate',None),
'q-10199':('among positive middle coordinates choose largest first coordinate',None),
'q-129447':('among positive middle coordinates choose largest first coordinate',None),
'q-129452':('choose the largest middle coordinate',None),
'q-129453':('choose the sole positive middle coordinate',lambda v:v[1]>0),
'q-129455':('among positive middle coordinates choose smallest first coordinate',None),
'q-20421':('among negative middle coordinates choose largest first coordinate',None)}
def predict(q):
 sig=signature(q);p=labels[sig];bank=[vec(c[':answer/value']) for c in q[':question/answer-fields'][0][':answer-field/choices']];pred=rules[p][1]
 if pred:indices=[i for i,v in enumerate(bank) if pred(v)]
 else:
  candidates=list(range(len(bank)))
  if p=='q-10195':candidates=[i for i in candidates if bank[i][0]<0];key=lambda i:bank[i][0]
  elif p=='q-10197':key=lambda i:bank[i][0]
  elif p=='q-10198':key=lambda i:(bank[i][1],-bank[i][2])
  elif p in ('q-10199','q-129447','q-129455'):
   candidates=[i for i in candidates if bank[i][1]>0];key=(lambda i:-bank[i][0]) if p=='q-129455' else (lambda i:bank[i][0])
  elif p=='q-129452':key=lambda i:bank[i][1]
  elif p=='q-20421':candidates=[i for i in candidates if bank[i][1]<0];key=lambda i:bank[i][0]
  best=max(map(key,candidates));indices=[i for i in candidates if key(i)==best]
 assert len(indices)==1,(p,bank,indices)
 f=q[':question/answer-fields'][0];idx=indices[0];cid=f[':answer-field/correct'];cid=cid[1] if isinstance(cid,list) else cid[':answer/id']
 return {'question_id':q[':question/id'],'visible_signature':sig,'source_profile_for_reporting':p,'rule':rules[p][0],'predicted_value':f[':answer-field/choices'][idx][':answer/value'],'predicted_id':f[':answer-field/choices'][idx][':answer/id'],'correct':f[':answer-field/choices'][idx][':answer/id']==cid}
