"""Deterministic extraction into named numeric-role skeletons; no source lookup in generation."""
import json,re,sys,importlib.util
from pathlib import Path
P=Path(__file__).parent
s=json.loads((P/'source.json').read_text())
params={'q-15370':dict(a=1500,n0=300,n1=500,tau=10,target=800),'q-37389':dict(a=500,n1=390,n2=400,t1=3,t2=6,time=42),'q-37400':dict(a=2500,n0=800,k='0.016',time=4),'q-335280':dict(a=20,n0=8,n1=12,tau=5,target=16),'q-335282':dict(a=3,n0='1.5',k='0.4',target=2),'q-335578':dict(a=1200,n0=200,n1=500,tau=4,target=900),'q-335542':dict(a=800,n0=80,n1=300,tau=10,target=600),'q-335590':dict(a=600,n1=480,n2=500,t1=4,t2=8,time=40),'q-335619':dict(a=800,n1=620,n2=720,t1=3,t2=9,target=760)}
shapes={'q-37400':'school','q-335280':'soda','q-335282':'volume','q-335590':'hard_value','q-37389':'hard_value','q-335619':'hard_time'}
# All complete source profile choices retained. Source math IDs identify templates.
def tag(expr,mode='n'):return '@@'+mode+':'+expr+'@@'
def compile_text(text,mapping):
 keys=sorted(mapping,key=len,reverse=True)
 pattern=r'(?<![\d.])(?:'+ '|'.join(re.escape(k) for k in keys)+r')(?!\d|\.\d)'
 return re.sub(pattern,lambda m:mapping[m.group()],text)
T={}
for q in s['record'][':knowledge-point/questions']:
 name=q[':question/math-academy-id'];p=params[name];shape=shapes.get(name,'moderate')
 mapping={str(v):tag(k,'g' if int(float(v))>=1000 and float(v)==int(float(v)) else 'n') for k,v in p.items()}
 for k,v in p.items():
  if int(float(v))>=1000:mapping[f'{int(v):,}'.replace(',',r'\,')]=tag(k,'g')
 prompt=compile_text(q[':question/problem'],mapping)
 if name=='q-37389':
  solution=None
 else:
  solution=q[':question/worked-solution']
  # Protect complete reduced fractions before numeric-role substitution.
  fractions={
   'q-15370':[(r'\frac{5}{6}','(a-n1)/K'),(r'\frac{7}{12}','(a-target)/K')],
   'q-335280':[(r'\frac{2}{3}','(a-n1)/K'),(r'\frac{1}{3}','(a-target)/K')],
   'q-335282':[(r'\frac{2}{3}','(a-target)/K')],
   'q-335578':[(r'\frac{7}{10}','(a-n1)/K'),(r'\frac{3}{10}','(a-target)/K')],
   'q-335542':[(r'\frac{25}{36}','(a-n1)/K'),(r'\frac{5}{18}','(a-target)/K')],
   'q-335590':[(r'\frac{6}{5}','D0/D2'),('6/5','D0/D2')],
   'q-335619':[(r'\frac{9}{4}','D0/D2'),('9/4','D0/D2'),(r'\frac{3}{2}','sqrt(D0/D2)'),(r'\frac{4}{27}','(a-target)/K')]
  }.get(name,[])
  protected={}
  for i,(text,expr) in enumerate(fractions):
   key=f'ZZ{chr(65+i)}ZZ';solution=solution.replace(text,key);protected[key]=tag(expr,'r' if '/' in text and not text.startswith('\\') else 'f')
  # Numeric values derived by exact model; source decimals are truncations.
  extras={
   'q-15370':{'1\\,200':'K','1\\,000':'a-n1','700':'a-target','29.562':('result','d3'),'30':('result','i')},
   'q-37400':{'1\\,700':'K','2500':('a','n'),'2,500':('a','c'),'905':('result','i')},
   'q-335280':{'4':'a-target','13.547':('result','d3'),'14':('result','i')},
   'q-335282':{'1.013':('result','d3')},
   'q-335578':{'1\\,000':'K','700':'a-n1','300':'a-target','13.502':('result','d3'),'14':('result','i')},
   'q-335542':{'720':'K','500':'a-n1','200':'a-target','35.128':('result','d3'),'35':('result','i')},
   'q-335590':{'120':'D0','100':'D2','144':'K','576.743':('result','d3'),'577':('result','i')},
   'q-335619':{'180':'D0','80':'D2','270':'K','40':'a-target','6':'delta','14.1285':('result','d4'),'14':('result','i')}
  }[name]
  smap=dict(mapping)
  for val,v in extras.items():
   expr,mode=v if isinstance(v,tuple) else (v,'g' if '\\,' in val else 'n');smap[val]=tag(expr,mode)
  if name=='q-335280':
   smap['12']=tag('K')
   solution=solution.replace('after $5$ minutes, the temperature of the soda was $12', 'after $5$ minutes, the temperature of the soda was $'+tag('n1'))
   solution=solution.replace('T(5)=12','T(5)='+tag('n1'))
   solution=solution.replace(r'\begin{aligned}12 & =20-12',r'\begin{aligned}'+tag('n1')+' & =20-12')
   # Deficit after calibration differs from initial temperature in varied instances.
   solution=solution.replace(r'\\ 8 & =12{e}^{-5k}',r'\\ '+tag('a-n1')+r' & =12{e}^{-5k}')
  if name=='q-335282':
   solution=solution.replace(r'\\ 1 & =1.5',r'\\ '+tag('a-target')+' & =1.5')
   solution=solution.replace(r'≈1\,\text{minute}',r'≈'+tag('result','i')+r'\,\text{minute}')
  solution=compile_text(solution,smap)
  for key,val in protected.items():solution=solution.replace(key,val)
  # Avoid source prose/plural minute mismatch in variants.
 bank=[int(re.search(r'\$(\d+)',a[':answer/value']).group(1)) for a in q[':question/answer-fields'][0][':answer-field/choices']]
 pattern=re.sub(r'\$(\d+)',r'$@@value@@',q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'])
 T[name]={'source_id':name,'level':q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/hard').split('/')[-1],'shape':shape,'parameters':p,'prompt':prompt,'solution':solution,'bank':bank,'choice_pattern':pattern}
T['q-37389']['solution']=T['q-335590']['solution'].replace('bread production','egg production').replace('bread','eggs').replace('bakery','farm').replace('loaves baked','eggs laid').replace('loaves','eggs')
(P/'templates.json').write_text(json.dumps(T,indent=2,ensure_ascii=False)+'\n')
(P/'source-cases.json').write_text(json.dumps([{'source_id':n,'template':n,'level':v['level'],'parameters':v['parameters'],'bank_profile':n+'_empirical','authored_level':n=='q-37389'} for n,v in T.items()],indent=2)+'\n')
