#!/usr/bin/env python3
"""Divergence templates with complete source banks and bounded parameter variants.

Easy: radicand slopes/shifts, root degrees and logarithmic cutoffs.
Moderate: endpoint variants of each observed three-integral checklist.
Hard is unobserved and unsupported. Source q-6294 has malformed fields.
"""
import argparse,copy,hashlib,json,random,sys,uuid
from pathlib import Path
try:
 import sympy as s
except ImportError:
 sys.path.insert(0,str(next((Path(__file__).resolve().parents[2]/'.venv/lib').glob('python*/site-packages'))))
 import sympy as s
KP_ID=17592186083201
KP_UUID='dc6d9b69-0459-515a-ba7b-c62cab96ca00'
TITLE='Identifying Divergent Improper Integrals'
VERSION='1.0.0-bounded-source-profiles'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
SUPPORTED_LEVELS=('easy','moderate')
P=Path(__file__).with_suffix('')
SOURCE=json.loads((P/'source.json').read_text())['record']
BY_ID={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
# Each source remains a separate layout/profile. Parameter meanings and bounds
# are deliberate narrow policies; they are not inferred misconception algorithms.
POLICY={
'q-100642':('root_degree',3,list(range(3,22,2))),
'q-5964':('root_degree',5,list(range(3,22,2))),
'q-100643':('slope',3,list(range(1,21))),
'q-80342':('radicand_shift',1,list(range(1,21))),
'q-80347':('radicand_shift',8,list(range(1,31))),
'q-6034':('lower_endpoint',6,list(range(2,31))),
'q-20700':('lower_endpoint',2,list(range(2,31))),
'q-20698':('slope',3,list(range(2,31))),
'q-6032':('endpoint_root',3,list(range(1,21))),
'q-101735':('third_lower_endpoint',2,list(range(1,21))),
'q-101738':('endpoint_root',1,list(range(1,21))),
'q-101734':('endpoint_root',1,list(range(1,21))),
'q-101736':('third_endpoint_magnitude',2,list(range(1,21)))}
TEMPLATES=[{'template':mid,'source_id':mid,'level':BY_ID[mid][':question/difficulty'][':db/ident'].split('/')[-1],'bank_profile':mid,'source_parameters':{name:base},'parameter':name,'observed_value':base,'sampling_values':bounds,'plot_rating':'none'} for mid,(name,base,bounds) in POLICY.items()]

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),x))
def latex(x):return s.latex(x).replace(' \\sqrt','\\sqrt').replace(r'\log',r'\operatorname{ln}')
def replace(text,pairs):
 # Simultaneous replacements: inserted parameter values never get substituted again.
 for i,(a,b) in enumerate(pairs):text=text.replace(a,'@SLOT'+str(i)+'@')
 for i,(a,b) in enumerate(pairs):text=text.replace('@SLOT'+str(i)+'@',b)
 return text

def render(mid,n):
 source=BY_ID[mid];problem=source[':question/problem'];solution=source[':question/worked-solution']
 bank_values=None;name,base,bounds=POLICY[mid]
 if n!=base:
  if mid=='q-100642':
   pairs=[(r'\sqrt[3]',r'\sqrt['+str(n)+']'),(r'\frac{3}{2}',latex(s.Rational(n,n-1))),('(2z+1)^{2/3}','(2z+1)^{'+str(n-1)+'/'+str(n)+'}'),('(2a+1)^{2/3}','(2a+1)^{'+str(n-1)+'/'+str(n)+'}')]
   bank_values=[latex(s.Rational(n+1,n)),None,str(n),str(2*n),latex(s.Rational(n-1,n))]
  elif mid=='q-5964':
   K=s.Rational(6*n,n-1)
   pairs=[(r'\sqrt[5]',r'\sqrt['+str(n)+']'),(r'\frac{5}{4}',latex(s.Rational(n,n-1))),(r'\frac{15}{2}',latex(K)),('^{4/5}','^{'+str(n-1)+'/'+str(n)+'}')]
   bank_values=[None,latex(-K/4),latex(-K/15),latex(-K),latex(-K/5)]
  elif mid=='q-100643':
   pairs=[(r'\frac{2\sqrt{5}}{3}',latex(2*s.sqrt(n+2)/n)),('2-3t','2-'+str(n)+'t'),('2-3a','2-'+str(n)+'a'),('2+3','2+'+str(n)),(r'\frac{2}{3}',latex(s.Rational(2,n))),(r'\sqrt{5}',r'\sqrt{'+str(n+2)+'}')]
   bank_values=[None,latex(-s.Rational(2,n)),latex(s.Rational(n,2)),latex(2*s.sqrt(n+2)/n),latex(-2*s.sqrt(n+2))]
  elif mid=='q-80342':
   pairs=[('1-z',str(n)+'-z'),('1-a',str(n)+'-a'),('1-0',str(n)+'-0')]
   problem=replace(problem,pairs);solution=replace(solution,pairs)
   # At the evaluated endpoint only, -2 becomes -2 sqrt(b); primitive remains -2 sqrt(b-z).
   solution=solution.replace(r' & =-2+',r' & =-'+latex(2*s.sqrt(n))+'+')
   bank_values=[latex(-s.sqrt(n)),None,latex(-s.sqrt(n)/2),latex(-2*s.sqrt(n)),latex(-4*s.sqrt(n))];pairs=[]
  elif mid=='q-80347':
   pairs=[('8-',str(n)+'-'),('u=8','u='+str(n)),(' & 9 &',' & '+str(n+1)+' &'),('^{9}','^{'+str(n+1)+'}'),('_{9}','_{'+str(n+1)+'}'),(r'\sqrt{9}',r'\sqrt{'+str(n+1)+'}')]
  elif mid in ('q-6034','q-20700'):
   pairs=[('_{'+str(base)+'}','_{'+str(n)+'}'),(r'\operatorname{ln}⁡'+str(base),r'\operatorname{ln}⁡'+str(n)),('x & '+str(base)+' &','x & '+str(n)+' &')]
   if mid=='q-6034':bank_values=[latex(1/s.log(n)),latex(n*s.log(n)),latex(s.log(n)),None,latex(s.exp(n))]
   else:bank_values=[None,latex(s.exp(n)),latex(n*s.log(n)),latex(s.log(n)),latex(1/s.log(n))]
  elif mid=='q-20698':
   pairs=[('3x+1',str(n)+'x+1'),('3a+1',str(n)+'a+1'),(r'\frac{1}{3}',latex(s.Rational(1,n)))]
   bank_values=[None,latex(s.log(n)),latex(s.Rational(1,n)),latex(1/(n*s.log(n))),latex(n*s.log(n))]
  elif mid in ('q-6032','q-101734','q-101738'):
   shift={'q-6032':1,'q-101734':5,'q-101738':2}[mid];L=n*n+shift;old=base*base+shift;factor=4 if mid=='q-101738' else 2
   pairs=[('_{'+str(old)+'}', '_{'+str(L)+'}'),(r'\sqrt{'+str(old)+'-'+str(shift)+'}',r'\sqrt{'+str(L)+'-'+str(shift)+'}')]
   problem=replace(problem,pairs);solution=replace(solution,pairs)
   if mid=='q-6032':solution=solution.replace(r'-6)', '-'+str(2*n)+')')
   elif mid=='q-101734':solution=solution.replace(r'\sqrt{a-5}-2)',r'\sqrt{a-5}-'+str(2*n)+')')
   else:solution=solution.replace(r'\sqrt{a-2}-1)',r'\sqrt{a-2}-'+str(n)+')')
   pairs=[]
  elif mid=='q-101735':
   # Only the third integral varies; the first two endpoints are fixed.
   pairs=[('_{2}','_{'+str(n)+'}'),(r'\operatorname{ln}⁡2',r'\operatorname{ln}⁡'+str(n))]
  elif mid=='q-101736':
   # Restrict edits to the third integral's solution section.
   pairs=[('^{-2}','^{-'+str(n)+'}')];problem=replace(problem,pairs)
   prefix,third=solution.split('For the third integral, we have',1)
   third=replace(third,pairs+[(r'\frac{1}{2}',latex(s.Rational(1,n)))])
   solution=prefix+'For the third integral, we have'+third;pairs=[]
  problem=replace(problem,pairs);solution=replace(solution,pairs)
 # Correct the recorded finite-truncation typo in generated variants only.
 if mid=='q-101734':
  solution=solution.replace(r'{lim}_{a\to \infty }{\int }_{1}^{\infty }',r'{lim}_{a\to \infty }{\int }_{1}^{a}')
 banks=[]
 for fi,f in enumerate(source[':question/answer-fields']):
  bank=[]
  for ai,a in enumerate(f[':answer-field/choices']):
   val=a[':answer/value'] if bank_values is None or bank_values[ai] is None else bank_values[ai]
   bank.append({'value':val,'type':a[':answer/type'][':db/ident'],'correct':a[':answer/id']==f[':answer-field/correct'][':answer/id']})
  banks.append(bank)
 return problem,solution,banks

def generate(difficulty,seed=0,template=None,*,parameters=None,profile=None):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty: '+difficulty)
 rng=random.Random(seed);eligible=[t for t in TEMPLATES if t['level']==difficulty]
 t=next((t for t in eligible if t['template']==template),None) if template else rng.choice(eligible)
 if t is None:raise ValueError('Invalid template for level')
 mid=t['template'];name,base,bounds=POLICY[mid]
 if profile is not None and profile!=mid:raise ValueError('Cannot mix profiles')
 if parameters is not None:
  if set(parameters)!={name}:raise ValueError('Unexpected parameters')
  n=parameters[name]
 else:n=rng.choice(bounds)
 if type(n)!=int or n not in bounds:raise ValueError('Parameter outside bounded policy')
 problem,solution,banks=render(mid,n)
 content=digest({'problem':problem,'solution':solution,'banks':banks,'difficulty':difficulty})
 qid=uid('question:'+content);fields=[]
 for f,bank in zip(BY_ID[mid][':question/answer-fields'],banks):
  key=f[':answer-field/key'];fid=uid('field:'+qid+':'+key)
  answers=[{':answer/id':uid('answer:'+fid+':'+a['type']+':'+a['value']),':answer/type':a['type'],':answer/value':a['value']} for a in bank]
  cid=answers[next(i for i,a in enumerate(bank) if a['correct'])][':answer/id'];rng.shuffle(answers)
  fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':f[':answer-field/type'][':db/ident'],':answer-field/choices':answers,':answer-field/correct':[':answer/id',cid]})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':fields},'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'template':mid,'bank_profile':mid,'seed':seed,'parameters':{name:n},'source_references':[mid],'domain':'No finite interval crosses an integrand pole or root boundary; roots stay positive. Negative tails use real primitives.','recipes':['See templates.json complete field-owned bank mappings'],'content_fingerprint':content,'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__},'plots':[],'sampling_policy':'Bounded source-specific root, slope, shift or endpoint changes; no coefficient-only or option-order padding'}}

def batch(difficulty,count,seed=0):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty')
 if count<0:raise ValueError('Nonnegative count required')
 records=[];seen=set()
 for attempt in range(10000):
  if len(records)==count:return records
  r=generate(difficulty,seed+attempt);key=r['question'][':question/problem']
  if key not in seen:seen.add(key);records.append(r)
 raise ValueError('Finite bounded search exhausted; shortage remains explicit')

def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join(f[':answer-field/key']+': '+', '.join(a[':answer/value']+(' [correct]' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices']) for f in q[':question/answer-fields'])+'\n\n'+q[':question/worked-solution']
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',required=True);ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--format',choices=['json','markdown'],default='json');ap.add_argument('--template');a=ap.parse_args()
 records=[generate(a.difficulty,a.seed,a.template)] if a.template else batch(a.difficulty,a.count,a.seed)
 print(json.dumps(records,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['batch', 'generate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__=='__main__':main()
