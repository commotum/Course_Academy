import json,re,pathlib
p=pathlib.Path(__file__).parent; root=p.parents[2]
w=json.loads((root/'generate/runs/current/sources/17592186078583.json').read_text());(p/'source.json').write_text(json.dumps(w,indent=2)+'\n')
spec=[('q-105917','easy',25,None),('q-37365','moderate',64,100),('q-106883','moderate',67,145),('q-106934','moderate',76,200),('q-106935','moderate',19,90),('q-106936','easy',30,None),('q-106937','moderate',75,450),('q-106878','easy',21,None)]
qs={q[':question/math-academy-id']:q for q in w['record'][':knowledge-point/questions']}
def mask(text,S,I):
 for val,key in [(S,'S'),(I,'I')]:
  if val is not None:text=re.sub(r'(?<!\d)'+str(val)+r'(?!\d)','@@'+key+'@@',text)
 return text
shared=qs['q-106936'][':question/worked-solution']
templates={};cases=[]
for sid,level,S,I in spec:
 q=qs[sid];field=q[':question/answer-fields'][0]
 templates[sid]={'level':level,'prompt':mask(q[':question/problem'],S,I),'solution':mask(q.get(':question/worked-solution',shared.replace('30','25')),S,I),'bank':[mask(a[':answer/value'],S,I) for a in field[':answer-field/choices']],'unit':'F' if 'Fahrenheit' in q[':question/problem'] else 'C','key':field[':answer-field/key'],'solution_origin':'observed' if ':question/worked-solution' in q else 'authored from shared observed solution','level_origin':'observed' if ':question/difficulty' in q else 'authored easy based on direct-proportionality prompt'}
 cases.append({'source_id':sid,'level':level,'template':sid,'parameters':dict(S=S,**({'I':I} if I else {})),'bank_profile':sid,'level_origin':templates[sid]['level_origin']})
(p/'templates.json').write_text(json.dumps(templates,indent=2)+'\n');(p/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
templates['q-37365']['bank'][3]=templates['q-37365']['bank'][3].replace('164','@@SUM@@')
(p/'templates.json').write_text(json.dumps(templates,indent=2)+'\n')
j=json.load(open('/home/jake/Developer/MA/DATA/Lessons/649/Source/649.json'))
def visit(obj):
 if isinstance(obj,dict):
  if obj.get('question_id')=='105917':(p/'q-105917-widget.json').write_text(json.dumps(obj,indent=2)+'\n')
  for value in obj.values():visit(value)
 elif isinstance(obj,list):
  for value in obj:visit(value)
visit(j)
