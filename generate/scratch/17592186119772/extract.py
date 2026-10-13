"""Extract every current source bank and ordered solution at captured basis."""
import json,re
from pathlib import Path
H=Path(__file__).resolve().parent
raw=json.loads((H/'source.json').read_text())
def normalize(s):
 # Some imported math choice values have doubled TeX command and row escapes.
 return s.replace('\\\\','\\') if r'\\begin' in s else s
MATRIX=re.compile(r'([A-E])=\[\\begin\{aligned\}(.*?)\\end\{aligned\}\]',re.S)
def matrices(s):
 return {m[1]:[[int(v.strip()) for v in row.split('&')] for row in m[2].split(r'\\')] for m in MATRIX.finditer(normalize(s))}
def compile_text(s):
 s=normalize(s)
 return MATRIX.sub(lambda m:'@@MATRIX:'+m[1]+'@@',s)
profiles={}
for q in raw['record'][':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];fields=q[':question/answer-fields'];kind=fields[0][':answer-field/type'][':db/ident'].split('/')[-1]
 ms=matrices(q[':question/problem'])
 if kind=='radio':
  for f in fields:
   for a in f[':answer-field/choices']:ms.update(matrices(a[':answer/value']))
 assert len(ms)==(5 if kind=='radio' else 3)
 sol=compile_text(q[':question/worked-solution'])
 # Witness coordinates stay fixed; displayed values depend on the actual matrix.
 for lab,m in ms.items():
  for i,row in enumerate(m):
   for j,v in enumerate(row):
    needle='{'+lab.lower()+'}_{'+str(i+1)+str(j+1)+'} & ='+str(v)+r'\ne 0'
    sol=sol.replace(needle,'{'+lab.lower()+'}_{'+str(i+1)+str(j+1)+'} & =@@ENTRY:'+lab+':'+str(i)+':'+str(j)+'@@'+r'\ne 0')
 profiles[sid]={'source_entity':q[':db/id'],'difficulty':q[':question/difficulty'][':db/ident'].split('/')[-1],'kind':kind,'direction':'upper' if 'upper triangular' in q[':question/problem'] else 'lower','matrices':dict(sorted(ms.items())),'problem':compile_text(q[':question/problem']),'solution':sol,'fields':[{'key':f[':answer-field/key'],'type':kind,'choices':[{'type':a[':answer/type'][':db/ident'],'value':compile_text(a[':answer/value'])} for a in f[':answer-field/choices']],'correct':compile_text(f[':answer-field/correct'][':answer/value'])} for f in fields]}
(H/'contract.json').write_text(json.dumps({'basis':raw['basis'],'profiles':profiles},indent=2)+'\n')
print('Extracted',len(profiles),'complete profiles')
