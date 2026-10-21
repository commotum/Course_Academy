import sys,json,re
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'workspace'))
import generator as g
JOB=Path(__file__).resolve().parent.parent
def save(n,v):Path(n).write_text(json.dumps(v,indent=2)+'\n')
def ms(text):
 return [[[int(x.strip()) for x in row.split('&')] for row in body.split(r'\\')] for body in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]
inv=json.load(open(JOB/'source/inventory.json'))
sourceids={q[':question/id'] for q in json.load(open(JOB/'source/source.json'))['material']['kp'][':knowledge-point/questions']}
out=[]; report=[]
for q in inv['questions']:
 if q[':question/id'] in sourceids:continue
 fmap={re.search(r'\$([ABC])\s*=',f[':answer-field/key'])[1]:f for f in q[':question/answer-fields']}
 matrices=[ms(fmap[x][':answer-field/key'])[0] for x in 'ABC']; shapes=[(len(m),len(m[0])) for m in matrices]
 candidates=[]
 for p in g.PROFILES:
  orig=g.original(p)['matrices']
  if [(len(m),len(m[0])) for m in orig]!=shapes:continue
  if ('**not**' in q[':question/problem'])!=('**not**' in g.SOURCES[p][':question/problem']):continue
  r=g.generate('easy',0,profile=p,parameters={'matrices':matrices})
  sol=q[':question/worked-solution']==r['question'][':question/worked-solution']
  if sol:out.append(r)
  candidates.append({'profile':p,'solution_equal':sol,'generated_input_id':r['question'][':question/id']})
 report.append({'stored_id':q[':question/id'],'entity_id':q[':db/id'],'candidates':candidates,'selected':''.join(x for x in 'ABC' if fmap[x][':answer-field/correct'][':answer/value']=='true')})
save('inventory-reproduction-input.json',out);save('inventory-probe-results.json',report)
empty={**inv,'questions':[],'fingerprints':[]};save('inventory-empty-for-identity-check.json',empty)
print(json.dumps(report,indent=2))
