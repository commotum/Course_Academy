"""Extract coefficient slots from the captured source layouts; no database writes."""
import json,sys
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent
src=json.loads((P/'source.json').read_text())['record'][':knowledge-point/questions']
# Fixed exponent, lower endpoint, variable, coefficient, and observed complete bank.
META={
'q-5962':(3,1,'\\theta ',3,'inline', ['3/2','1','3/4','7/4','1/2']),
'q-152755':(6,1,'\\theta ',2,'inline',['1/5','diverges','2/5','1/3','4/5']),
'q-152758':(2,3,'x',5,'inline',['1/5','5/2','1/3','diverges','5/3']),
'q-100310':(2,2,'z',4,'short',['1/2','2','4/3','1','1/3']),
'q-350322':(4,3,'x',18,'pulled',['2/9']),
'q-350324':(3,2,'x',16,'pulled',['2']),
'q-152777':('9/2',1,'x',2,'pulled',['4','4/7','2/7','diverges','7/2']),
'q-152762':('4/3',8,'z',2,'pulled',['1/3','3','diverges','4/3','6']),
'q-350331':('8/3',1,'y',5,'pulled',['3']),
'q-350333':('7/3',1,'s',12,'pulled',['9']),
'q-350337':('13/5',1,'t',8,'pulled',['5']),
'q-152754':('3/2',2,'t','1/4','pulled',['sqrt(2)/4','diverges','1/4','3*sqrt(2)/2','sqrt(2)/2'])}

def frac_span(text):
 start=text.index('\\frac');pos=start+5;depth=0
 for group in range(2):
  assert text[pos]=='{';depth=1;pos+=1
  while depth:
   if text[pos]=='{':depth+=1
   if text[pos]=='}':depth-=1
   pos+=1
 return text[start:pos]

templates=[]
for q in src:
 mid=q[':question/math-academy-id']
 if mid not in META:continue
 p,L,var,C,layout,values=META[mid];p=s.Rational(p);C=s.Rational(C);K=C/(p-1);V=s.simplify(K*s.Integer(L)**(1-p))
 cs,ks,vs=map(s.latex,(C,K,V));integrand=frac_span(q[':question/problem'])
 problem=q[':question/problem'].replace(integrand,'@INTEGRAND@')
 sol=q[':question/worked-solution'];prefix,body=sol.split('\\begin{aligned}',1);math,suffix=body.split('\\end{aligned}',1)
 lines=math.split(r' \\  & =')
 lines[0]=lines[0].replace(integrand,'@INTEGRAND@')
 if layout=='short':
  assert len(lines)==5
  lines[1]=lines[1].replace('\\frac{'+cs+'}',r'\frac{@C@}')
  lines[2]=lines[2].replace('\\frac{'+cs+'}',r'\frac{@C@}')
  lines[3]=lines[3].replace(vs,'@V@');lines[4]=lines[4].replace(vs,'@V@')
 else:
  assert len(lines)==7
  if layout=='inline':
   lines[1]=lines[1].replace('}^{a}'+cs+'{','}^{a}@C@{')
   lines[2]=lines[2].replace('(-'+ks,'(-@K@')
  else:
   assert lines[1].startswith(cs) and lines[2].startswith(cs)
   lines[1]='@C@'+lines[1][len(cs):];lines[2]='@C@'+lines[2][len(cs):]
  for i in (3,4,5):
   assert lines[i].startswith('-'+ks)
   lines[i]='-@K@'+lines[i][len(ks)+1:]
  assert lines[6].startswith(vs)
  lines[6]='@V@'+lines[6][len(vs):]
 skeleton=prefix+'\\begin{aligned}'+r' \\  & ='.join(lines)+'\\end{aligned}'+suffix
 fields=q[':question/answer-fields']; f=fields[0]; bank=[]
 assert len(values)==len(f[':answer-field/choices'])
 for val,a in zip(values,f[':answer-field/choices']):
  if val!='diverges':assert s.latex(s.sympify(val)).replace(' \\sqrt', '\\sqrt')==a[':answer/value'],(mid,val,a)
  bank.append({'source_answer_id':a[':answer/id'],'source_value':a[':answer/value'],'type':a[':answer/type'][':db/ident'],'ratio':None if val=='diverges' else str(s.simplify(s.sympify(val)/C)),'correct':a[':answer/id']==f[':answer-field/correct'][':answer/id'],'recipe':'The integral diverges' if val=='diverges' else 'C * ('+str(s.simplify(s.sympify(val)/C))+')','interpretation':'Correct integral' if a[':answer/id']==f[':answer-field/correct'][':answer/id'] else 'Observed coefficient-scaling pattern; error interpretation unresolved'})
 templates.append({'source_id':mid,'level':q[':question/difficulty'][':db/ident'].split('/')[-1],'template':mid,'bank_profile':mid if len(bank)>1 else None,'source_parameters':{'coefficient':str(C)},'exponent':str(p),'lower':L,'variable':var,'layout':layout,'problem':problem,'solution':skeleton,'integrand':integrand,'source_coefficient':str(C),'field_type':f[':answer-field/type'][':db/ident'],'field_key':f[':answer-field/key'],'bank':bank})
(P/'templates.json').write_text(json.dumps(templates,indent=2,ensure_ascii=False)+'\n')
print('Extracted',len(templates),'layouts and',sum(len(t['bank'])>1 for t in templates),'complete banks')
