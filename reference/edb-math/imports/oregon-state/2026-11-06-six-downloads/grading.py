from pathlib import Path
import json
H=Path('/home/jake/Developer/Course_Academy/reference/edb-math/imports/oregon-state/2026-11-06-six-downloads');T=Path('/tmp/ingest-six');entities=json.loads((H/'entities.json').read_text());byid={r[':db/id']:r for r in entities};cases=[]
for e in entities:
 if ':question/id'not in e:continue
 fs=[];checks=[]
 for i,fid in enumerate(e[':question/answer-fields']):
  f=byid[fid];choices=[]
  for aid in f[':answer-field/choices']:
   a=byid[aid];choices.append({':answer/id':a[':answer/id']['$uuid'],':answer/type':a[':answer/type'],':answer/value':a[':answer/value']})
  fs.append({':answer-field/key':f[':answer-field/key'],':answer-field/type':f[':answer-field/type'],':answer-field/choices':choices,':answer-field/correct':[':answer/id',byid[f[':answer-field/correct']][':answer/id']['$uuid']]})
  if f[':answer-field/type'].endswith('/free'):continue
  value=choices[0][':answer/value'];kind=choices[0][':answer/type']
  if kind.endswith('/text'):wrong={'vector field':'scalar function','scalar function':'undefined','undefined':'vector field','CW':'CCW','no rotation':'CW'}[value]
  elif value=='0':wrong='1'
  elif 'pmatrix'in value:wrong=r'\begin{pmatrix}0\\0\\0\end{pmatrix}'
  elif value.startswith('\\left('):wrong=r'\left(0,0,0\right)'
  else:wrong='0'
  checks.extend([{'field_index':i,'submitted':value,'expected':'accepted','purpose':'canonical typed study answer'},{'field_index':i,'submitted':wrong,'expected':'rejected','purpose':'incorrect value, operator type, rotation, or missing general solution'}])
 if checks:cases.append({'label':e[':db/id'],'record':{'question':{':question/problem':e[':question/problem'],':question/answer-fields':fs},'knowledge_point':{'title':'Six requested F26 assignments'},'generation':{'template':'imported-assignment'}},'checks':checks})
(T/'grading-input.json').write_text(json.dumps(cases));print('Prepared',sum(len(c['checks'])//2 for c in cases),'typed-field checks, preserving native free-response fields.')
